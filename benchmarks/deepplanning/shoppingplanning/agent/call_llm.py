"""
Universal LLM calling module
Supports OpenAI-compatible APIs
"""
import json
import os
import random
import socket
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

import httpx
import openai

# Belt-and-suspenders against half-open TLS sockets: even with httpx.Timeout,
# we've observed ssl.recv() wedge indefinitely (e.g. kazakh L3 case_7 hang
# 7h20m, chinese L2 wedge 2026-06-22). A process-wide socket default timeout
# forces the kernel-level recv() to raise after this many seconds, bypassing
# whatever httpx layer is failing to honor the read timeout.
socket.setdefaulttimeout(300.0)

# Bound every leg of the HTTP request so a stuck TCP connection can't wedge a
# ThreadPoolExecutor worker forever. The per-request `timeout=` on
# chat.completions.create() doesn't reliably bubble down to the ssl.recv layer
# in all openai-python/httpx version combinations — setting it at client
# construction time does. Read leg is the long one (model latency), the others
# are connection setup and should be quick.
_DEFAULT_HTTPX_TIMEOUT = httpx.Timeout(connect=15.0, read=180.0, write=30.0, pool=30.0)


def load_model_config(model_name: str) -> Dict[str, Any]:
    """
    Load model configuration from models_config.json
    
    Searches for models_config.json in the following order:
    1. Current domain directory (shoppingplanning/)
    2. Parent directory (project root)
    
    Args:
        model_name: Name of the model
        
    Returns:
        Model configuration dict
        
    Raises:
        FileNotFoundError: If config file not found
        ValueError: If model not found in config
    """
    explicit_config = 'DEEPPLANNING_MODELS_CONFIG' in os.environ
    if explicit_config:
        config_path = Path(os.environ['DEEPPLANNING_MODELS_CONFIG'])
        if not config_path.is_file():
            raise FileNotFoundError(
                f"DEEPPLANNING_MODELS_CONFIG is not a regular file: {config_path}"
            )
    else:
        domain_config_path = Path(__file__).parent.parent / 'models_config.json'
        root_config_path = Path(__file__).parent.parent.parent / 'models_config.json'
        if domain_config_path.is_file():
            config_path = domain_config_path
        elif root_config_path.is_file():
            config_path = root_config_path
        else:
            raise FileNotFoundError(
                f"models_config.json not found in:\n"
                f"  - Domain directory: {domain_config_path}\n"
                f"  - Project root: {root_config_path}\n"
                f"Please create models_config.json in the project root or domain directory."
            )

    try:
        with config_path.open('r', encoding='utf-8') as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        source = 'DEEPPLANNING_MODELS_CONFIG' if explicit_config else 'models_config.json'
        raise ValueError(f"Unable to load {source} at {config_path}: {exc}") from exc

    if not isinstance(config, dict):
        raise ValueError(f"Model config must contain a JSON object: {config_path}")
    models = config.get('models')
    if not isinstance(models, dict):
        raise ValueError(f"Model config must contain a 'models' object: {config_path}")
    if model_name not in models:
        available = ', '.join(models.keys())
        raise ValueError(
            f"Model '{model_name}' not found in models_config.json\n"
            f"Available models: {available}"
        )
    
    model_config = models[model_name]
    if not isinstance(model_config, dict):
        raise ValueError(f"Configuration for model '{model_name}' must be an object")
    return model_config


def create_client(model_name: str, model_config: Optional[Dict[str, Any]] = None):
    """
    Create OpenAI client based on model configuration
    
    Args:
        model_name: Name of the model
        model_config: Model configuration (if None, will load from config file)
        
    Returns:
        Initialized OpenAI client instance
    """
    if model_config is None:
        model_config = load_model_config(model_name)
    
    model_type = model_config.get('model_type', 'openai')
    base_url = model_config['base_url']
    api_key_env = model_config.get('api_key_env')
    api_key = os.getenv(api_key_env) if api_key_env else None
    
    if not api_key:
        raise RuntimeError(
            f"API key not found for model '{model_name}'\n"
            f"Please set environment variable: {api_key_env}"
        )
    
    if model_type == 'openai':
        # OpenAI and OpenAI-compatible APIs (Qwen, DeepSeek, etc.)
        return openai.OpenAI(api_key=api_key, base_url=base_url, timeout=_DEFAULT_HTTPX_TIMEOUT)


def call_llm(
    config_name: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None
):
    """
    Universal LLM call with automatic client creation and retry logic
    
    Args:
        config_name: Configuration name from models_config.json (display name)
        messages: Message list
        tools: Tool definitions (optional)
    
    Returns:
        API response object
        
    Note:
        All parameters (model_name, temperature, extra_body, etc.) are loaded
        from models_config.json based on the config_name.
    """
    # Load model config and create client
    model_config = load_model_config(config_name)
    client = create_client(config_name, model_config)
    
    # Get actual model name for API call (fallback to config_name if not specified)
    actual_model_name = model_config.get('model_name', config_name)
    
    # Get parameters from config or use defaults
    temperature = model_config.get('temperature', None)
    max_retries = model_config.get('max_retries', 30)
    backoff = model_config.get('backoff', 1.5)
    extra_body = model_config.get('extra_body')  # Get from config
    # Per-call timeout. Without this the OpenAI SDK can hang for many minutes
    # on a stuck TCP connection; combined with max_retries that's effectively
    # forever.
    request_timeout = model_config.get('timeout', 300)

    # Detect reasoning models (don't support temperature)
    is_reasoning_model = any(x in actual_model_name.lower() for x in ['o1', 'o3', 'o4-mini', 'reasoner'])

    last_err = None

    for attempt in range(max_retries):
        try:
            params = {
                "model": actual_model_name,
                "messages": messages,
                "timeout": request_timeout,
            }
            
            if tools:
                params["tools"] = tools
            
            if not is_reasoning_model and temperature is not None:
                params["temperature"] = temperature
            
            if extra_body:
                params["extra_body"] = extra_body
            response = client.chat.completions.create(**params)
            
            # Validate response
            msg = response.choices[0].message
            has_content = msg.content and msg.content.strip()
            has_tool_calls = hasattr(msg, 'tool_calls') and msg.tool_calls
            
            if not has_content and not has_tool_calls:
                raise ValueError("Model returned an empty response without tool calls")
            
            return response
            
        except Exception as e:
            last_err = e
            
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff with jitter (see travel call_llm). Rate-limit
            # storms under high concurrency get a longer cap; jitter
            # de-synchronizes concurrent workers so they don't re-storm.
            emsg = str(e).lower()
            is_rate_limit = ('429' in emsg or 'rate limit' in emsg
                             or 'limit_requests' in emsg or 'rpm' in emsg
                             or 'too many requests' in emsg)
            if is_rate_limit:
                wait_time = min(backoff * (2 ** attempt), 60.0)
            else:
                wait_time = min(backoff * (1.5 ** attempt), 20.0)
            wait_time += random.uniform(0, wait_time)
            print(f"  ⚠️  LLM API error (attempt {attempt + 1}/{max_retries}): {e}")
            print(f"     Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)

    raise last_err if last_err else RuntimeError("LLM API call failed")
