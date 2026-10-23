"""
Base Travel Tool - Extension of qwen-agent BaseTool for travel planning
"""
import json
import os
from typing import Dict, List, Optional, Union

# Import base components from qwen-agent framework
from qwen_agent.tools.base import BaseTool, register_tool, TOOL_REGISTRY

# Pandas lazy import flag (only imported when CSV is used)
PANDAS_AVAILABLE = None


# ========== Tool Schema Loader ==========

def load_tool_schemas(schema_file: str = 'tool_schema.json', language: str = 'en') -> Dict[str, dict]:
    """
    Load tool definitions from JSON file
    
    Args:
        schema_file: Path to the tool schema JSON file (default: 'tool_schema.json')
                    If 'tool_schema.json', will use 'tool_schema_{language}.json'
        language: Language code ('zh' or 'en', default: 'en')
        
    Returns:
        Dictionary of {tool_name: schema_dict}
        
    Example:
        >>> schemas = load_tool_schemas(language='zh')
        >>> train_schema = schemas['query_train_info']
    """
    # Use language-specific schema file if using default name
    if schema_file == 'tool_schema.json':
        schema_file = f'tool_schema_{language}.json'
    
    # Find schema file
    if not os.path.exists(schema_file):
        # Try to find in current directory
        schema_file = os.path.join(os.path.dirname(__file__), schema_file)
    
    if not os.path.exists(schema_file):
        print(f"Warning: Tool schema file not found: {schema_file}")
        return {}
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schemas_list = json.load(f)
        
        # Convert to {tool_name: schema} format
        schemas = {}
        for schema in schemas_list:
            if 'function' in schema:
                tool_name = schema['function']['name']
                schemas[tool_name] = schema['function']
        
        print(f"✓ Loaded {len(schemas)} tool definitions from {schema_file}")
        return schemas
    except Exception as e:
        print(f"✗ Failed to load tool schema file: {e}")
        return {}


def get_tool_schema(tool_name: str, schemas: Dict[str, dict] = None) -> dict:
    """
    Get schema for a specific tool
    
    Args:
        tool_name: Name of the tool
        schemas: Tool schema dictionary (auto-loaded if None)
        
    Returns:
        Tool schema dictionary
    """
    if schemas is None:
        schemas = load_tool_schemas()
    
    if tool_name not in schemas:
        raise KeyError(f"Tool definition not found: '{tool_name}'")
    
    return schemas[tool_name]


# Global cache for tool schemas (separate cache per language)
_TOOL_SCHEMAS_CACHE: Dict[str, Dict[str, dict]] = {}

def get_cached_tool_schemas(language: str = 'en') -> Dict[str, dict]:
    """Get cached tool schemas (cached on first load per language)"""
    global _TOOL_SCHEMAS_CACHE
    if language not in _TOOL_SCHEMAS_CACHE:
        _TOOL_SCHEMAS_CACHE[language] = load_tool_schemas(language=language)
    return _TOOL_SCHEMAS_CACHE[language]


# Note: We use the framework's register_tool directly.
# Schema auto-loading from JSON is handled in BaseTravelTool.__init__


# ========== Base Travel Tool Class ==========

# ========== Per-language Label Resolver ==========
#
# Tool RESPONSE strings (the text the agent reads back from a tool call) carry
# small per-language labels like "Attraction ID:", "City:", "Address:". The
# baseline zh/en labels live as LANG_FIELDS dicts inside each tool file (with
# some entries as lambdas for templates). For non-baseline languages we load
# templates from tools/labels/<code>.json — a single file per language keyed
# by tool class name, containing the same keys as LANG_FIELDS['en'].
#
# Templates use named placeholders ({count}, {path}, etc.) matching the
# parameter names of the baseline lambdas. This helper wraps each template
# string back into a callable with the original lambda signature, so the
# tool's call sites (`self.fields['db_loaded'](count, path)`) need no change.
#
# If labels/<code>.json is missing OR a specific key is missing inside it, the
# resolver falls back to the English baseline for that key. Missing labels are
# a soft failure (label renders in English) — they don't break the eval.

import inspect as _inspect
import sys as _sys

_LABELS_DIR = os.path.join(os.path.dirname(__file__), 'labels')
_LABELS_CACHE: Dict[str, Optional[Dict[str, Dict[str, str]]]] = {}


def _load_translated_labels(language: str) -> Optional[Dict[str, Dict[str, str]]]:
    """Load tools/labels/<code>.json. Returns {ClassName: {label_key: template_str}}
    or None when the language file is missing or unreadable."""
    if language in _LABELS_CACHE:
        return _LABELS_CACHE[language]
    path = os.path.join(_LABELS_DIR, f'{language}.json')
    if not os.path.exists(path):
        _LABELS_CACHE[language] = None
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = None
    except Exception as exc:
        print(f"[base_travel_tool] WARN: failed to load {path}: {exc}", file=_sys.stderr)
        data = None
    _LABELS_CACHE[language] = data
    return data


def _wrap_template_as_callable(template, params):
    """Wrap a translated template string so it has the same signature as the
    baseline lambda (positional args, in the original parameter order)."""
    def call(*args, **kwargs):
        bound = dict(zip(params, args))
        bound.update(kwargs)
        try:
            return template.format(**bound)
        except (KeyError, IndexError):
            # Translator dropped or renamed a placeholder — degrade gracefully
            # rather than crash the tool.
            return template
    return call


def get_tool_labels(class_name, language, baseline):
    """Resolve the label dict for one tool class in the requested language.

    For baseline languages (zh / en) returns baseline[language] directly so
    behavior is byte-identical to the original repo. For any other language
    looks up translated templates in tools/labels/<code>.json keyed by the
    tool class name, wraps templates back into callables matching the
    baseline lambdas, and falls back per-key to English for anything missing.
    """
    if language in baseline:
        return baseline[language]
    translated_all = _load_translated_labels(language)
    en_baseline = baseline.get('en', {})
    if translated_all is None:
        return en_baseline
    class_labels = translated_all.get(class_name, {}) or {}
    out = {}
    for key, baseline_value in en_baseline.items():
        translated_value = class_labels.get(key)
        if not isinstance(translated_value, str) or not translated_value.strip():
            out[key] = baseline_value
            continue
        if callable(baseline_value):
            try:
                params = list(_inspect.signature(baseline_value).parameters.keys())
            except (TypeError, ValueError):
                params = []
            out[key] = _wrap_template_as_callable(translated_value, params)
        else:
            out[key] = translated_value
    return out


class BaseTravelTool(BaseTool):
    """
    Base class for travel tools, extending qwen-agent's BaseTool
    
    Design principles:
    1. Inherits from qwen-agent framework's BaseTool
    2. Adds travel-specific functionality (database loading, result formatting)
    3. Supports automatic schema loading from JSON files
    4. Compatible with OpenAI Function Calling and other formats
    
    Usage:
    ```python
    @register_tool('query_train_info')
    class TrainQueryTool(BaseTravelTool):
        # Schema will be auto-loaded from tool_schema.json in __init__
        
        def call(self, params, **kwargs):
            # Your implementation
        pass
    ```
    """
    
    def __init__(self, cfg: Optional[Dict] = None):
        """
        Initialize travel tool
        
        Args:
            cfg: Tool configuration dictionary, may contain:
                - database_path: Path to database file
                - load_schema: Whether to load schema from JSON (default True)
                - language: Language code ('zh' or 'en', default 'en')
        """
        # Try to load schema from JSON before calling parent __init__
        if cfg is None:
            cfg = {}
        
        # Set language (default to 'en')
        self.language = cfg.get('language', 'en')
        
        if not self.__class__.description and cfg.get('load_schema', True):
            self._load_schema_from_json()
        
        # Call parent __init__ (framework's BaseTool)
        super().__init__(cfg)
        
        # Initialize travel-specific attributes
        self.database_path = None
        self.data = None
    
    def _load_schema_from_json(self):
        """Load tool schema from language-specific JSON file"""
        # Get tool name from registry
        tool_name = None
        for name, cls in TOOL_REGISTRY.items():
            if cls == self.__class__:
                tool_name = name
                break
        
        if not tool_name:
            # If not found in registry, check class attribute
            if hasattr(self.__class__, 'name') and self.__class__.name:
                tool_name = self.__class__.name
            else:
                return  # Cannot find tool name, skip loading
        
        # Load all tool schemas for this language
        schemas = get_cached_tool_schemas(language=self.language)
        
        if tool_name in schemas:
            schema = schemas[tool_name]
            # Set class attributes (not instance attributes)
            self.__class__.name = schema.get('name', tool_name)
            self.__class__.description = schema.get('description', '')
            self.__class__.parameters = schema.get('parameters', {})
    
    def load_json_database(self, path: str) -> dict:
        """
        Load JSON format database
        
        Args:
            path: File path
            
        Returns:
            Loaded JSON data
            
        Raises:
            FileNotFoundError: File does not exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_csv_database(self, path: str):
        """
        Load CSV format database
        
        Args:
            path: File path
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: File does not exist
            ImportError: pandas not installed or import failed
        """
        global PANDAS_AVAILABLE
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database file not found: {path}")
        
        # Lazy import pandas (only when needed)
        if PANDAS_AVAILABLE is None:
            try:
                # Set environment variables to avoid some pandas internal library issues
                os.environ['OMP_NUM_THREADS'] = '1'
                os.environ['MKL_NUM_THREADS'] = '1'
                os.environ['OPENBLAS_NUM_THREADS'] = '1'
                
                import pandas as pd
                PANDAS_AVAILABLE = pd
                print("✓ pandas imported successfully")
            except Exception as e:
                PANDAS_AVAILABLE = False
                raise ImportError(
                    f"pandas import failed: {e}\n"
                    "Please run: pip install pandas\n"
                    "Or use JSON format database"
                )
        
        if PANDAS_AVAILABLE is False:
            raise ImportError(
                "pandas not installed or import failed, cannot load CSV database.\n"
                "Please run: pip install pandas\n"
                "Or use JSON format database"
            )
        
        # Use imported pandas
        pd = PANDAS_AVAILABLE
        # Read all as strings to avoid precision/trailing zero loss for lat/lon values
        return pd.read_csv(path, dtype=str)
    
    def format_result_as_json(self, result: Union[dict, list]) -> str:
        """
        Format result as JSON string
        
        Args:
            result: Result data
            
        Returns:
            JSON formatted string
        """
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    # ========== OpenAI Function Calling Schema Support ==========
    
    @property
    def openai_schema(self) -> Dict:
        """
        Get OpenAI Function Calling format schema
        
        Returns:
            Full schema in OpenAI function calling format
            
        Example:
            >>> tool = TrainQueryTool()
            >>> schema = tool.openai_schema
            >>> print(schema)
            {
                "type": "function",
                "function": {
                    "name": "query_train_info",
                    "description": "...",
                    "parameters": {...}
                }
            }
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def get_schema(self, format: str = "openai") -> Dict:
        """
        Get tool schema in specified format
        
        Args:
            format: Schema format, supports 'openai', 'anthropic', 'qwen'
            
        Returns:
            Schema in corresponding format
            
        Example:
            >>> tool = TrainQueryTool()
            >>> openai_schema = tool.get_schema('openai')
            >>> anthropic_schema = tool.get_schema('anthropic')
        """
        if format == "openai" or format == "qwen":
            return self.openai_schema
        elif format == "anthropic":
            # Anthropic Claude format
            return {
                "name": self.name,
                "description": self.description,
                "input_schema": self.parameters
            }
        else:
            raise ValueError(
                f"Unsupported format: {format}. "
                f"Supported formats: openai, anthropic, qwen"
            )
    
    @classmethod
    def get_openai_schema_from_class(cls) -> Dict:
        """
        Get OpenAI schema directly from class definition (without instantiation)
        
        Returns:
            Schema in OpenAI function calling format
            
        Example:
            >>> schema = TrainQueryTool.get_openai_schema_from_class()
        """
        return {
            "type": "function",
            "function": {
                "name": cls.name,
                "description": cls.description,
                "parameters": cls.parameters
            }
        }


# Export framework components for convenience
__all__ = [
    'BaseTool',  # Framework's base class
    'BaseTravelTool',  # Extended travel tool base class
    'register_tool',  # Framework's registration decorator (use this directly)
    'TOOL_REGISTRY',  # Framework's tool registry
    'load_tool_schemas',
    'get_tool_schema',
    'get_cached_tool_schemas',
]
