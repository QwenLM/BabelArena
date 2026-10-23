"""
Custom Agent implementation - Framework-independent

Uses universal LLM calling for multiple providers
"""

import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from threading import Lock

try:
    from .call_llm import call_llm
except ImportError:
    from call_llm import call_llm




class ShoppingFnAgent:
    """
    Lightweight function-calling Agent (shopping scenario):
    - Loads shopping_tool_schema.json as OpenAI Chat Completions tools
    - Dynamically loads tool classes (BaseShoppingTool subclasses) from shopping_tools directory
    - Iteratively calls LLM and executes tool_calls until final answer
    """

    def __init__(self,
                 model: str | None = None,
                 tool_schema_path: str | None = None,
                 base_url: str | None = None,
                 api_key: str | None = None,
                 sample_id: str | None = None,
                 database_base_path: str | None = None,
                 language: str | None = None) -> None:
        """
        Initialize Agent

        Args:
            model: Model name (must exist in models_config.json)
            tool_schema_path: Path to tool schema JSON file
            base_url: Base URL for API (deprecated, loaded from models_config.json)
            api_key: API key (deprecated, loaded from models_config.json)
            sample_id: Sample ID for database path resolution
            database_base_path: Base path to database directory
            language: Language ISO code ('en', 'zh', or any 2-letter ISO from
                      the per-language labels file). Threaded into the tool
                      config so each shopping tool returns target-language
                      error/status strings. Defaults to 'en'.
        """
        self._load_env_from_dotenv()

        self.model = model or os.getenv("TOOLS_AGENT_MODEL", "qwen-plus")
        self.language = language or 'en'
        default_schema = Path(__file__).resolve().parent / 'tools' / 'shopping_tool_schema.json'
        self.tool_schema_path = tool_schema_path or os.getenv("SHOPPING_SCHEMA_PATH", str(default_schema))

        self.sample_id = sample_id
        if database_base_path:
            self.database_base_path = Path(database_base_path)
        else:
            # Default path: ShoppingBench/database
            project_root = Path(__file__).resolve().parent
            self.database_base_path = project_root / 'database'

        self.tool_config = self._build_tool_config()
        self.tools_schema = self._load_tool_schemas()
        self.openai_tools = self._build_openai_tools(self.tools_schema)
        self.tool_instances = self._load_tool_instances()

        if not Path(self.tool_schema_path).exists():
            raise FileNotFoundError(f"Tool schema not found: {self.tool_schema_path}")

    def _build_tool_config(self) -> Dict[str, Any]:
        """
        Build tool configuration with database path.
        All shopping tools use the same products.jsonl file, simplifying the logic.
        """
        cfg = {'language': self.language}
        if self.sample_id is not None:
            # Shopping scenario database path structure: database/case_{sample_id}/products.jsonl
            db_path = self.database_base_path / f'case_{self.sample_id}'
            
            if db_path.exists():
                cfg['database_path'] = str(db_path)
            else:
                if os.getenv('DEBUG_TOOLS') == '1':
                    print(f"[ShoppingFnAgent] WARN: Database not found for case {self.sample_id}: {db_path}")
        return cfg
    
    def _load_tool_instances(self) -> Dict[str, Any]:
        """
        Dynamically load tool instances from TOOL_REGISTRY.
        
        Tool registration mechanism:
        1. Tool classes use the @register_tool('tool_name') decorator
        2. The decorator executes at class definition time, registering the tool class to base_shopping_tool.TOOL_REGISTRY
        3. When importing the tools package, __init__.py imports all tool modules, triggering decorator execution
        4. Retrieve registered tool classes from TOOL_REGISTRY and instantiate them
        """
        instances: Dict[str, Any] = {}

        tools_dir = Path(__file__).resolve().parent.parent / 'tools'
        # Add tools_dir to sys.path to enable 'from base_shopping_tool import ...' in tool files
        sys.path.insert(0, str(tools_dir))
        sys.path.insert(0, str(tools_dir.parent))

        # Import tools package to trigger @register_tool decorator execution for all tool modules
        # tools/__init__.py imports all tool modules, and decorators register tool classes to TOOL_REGISTRY
        # Failures here are fatal — see _load_tool_instances comment below.
        try:
            import tools  # noqa: F401
        except Exception as e:
            print(f"[ShoppingFnAgent] FATAL: import tools failed: {e}", flush=True)
            raise

        # Get TOOL_REGISTRY from base_shopping_tool module
        try:
            import base_shopping_tool  # type: ignore
            tool_registry = getattr(base_shopping_tool, 'TOOL_REGISTRY', None)
            if tool_registry is None:
                raise RuntimeError("TOOL_REGISTRY not found in base_shopping_tool")
        except Exception as e:
            print(f"[ShoppingFnAgent] FATAL: import base_shopping_tool failed: {e}", flush=True)
            raise

        if not tool_registry:
            raise RuntimeError("TOOL_REGISTRY is empty. No tools were registered.")

        # Create tool instances from TOOL_REGISTRY. Failures here are fatal:
        # silent skip used to mean tools like search_products would be missing
        # from `instances` for the whole agent lifetime, and every call would
        # return "tool not found" — the failure mode that hid the Qwen3
        # tokenizer rate-limit bug.
        tool_cfg = self.tool_config
        for tool_name, tool_cls in tool_registry.items():
            try:
                inst = tool_cls(cfg=tool_cfg)
                instances[tool_name] = inst
            except Exception as e:
                print(
                    f"[ShoppingFnAgent] FATAL: Failed to instantiate tool "
                    f"'{tool_name}': {e}",
                    flush=True,
                )
                raise

        return instances

    def _load_env_from_dotenv(self) -> None:
        """
        Load environment variables from .env file
        
        Searches for .env in the following order:
        1. Domain directory (shoppingplanning/)
        2. Project root (parent of domain)
        """
        try:
            # Try domain directory first
            domain_root = Path(__file__).resolve().parent.parent
            domain_dotenv = domain_root / '.env'
            
            # Try project root
            project_root = domain_root.parent
            project_dotenv = project_root / '.env'
            
            # Use project root .env if it exists, otherwise domain .env
            dotenv_path = project_dotenv if project_dotenv.exists() else domain_dotenv
            
            if not dotenv_path.exists():
                return
            
            for line in dotenv_path.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and (key not in os.environ):
                    os.environ[key] = val
        except Exception:
            pass

    def _load_tool_schemas(self) -> List[Dict[str, Any]]:
        """Load tool schemas from JSON file"""
        with open(self.tool_schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _build_openai_tools(self, schemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Build OpenAI tools format
        - If schema is already {type:function, function:{...}}, use as-is
        - Otherwise wrap as function definition
        """
        tools: List[Dict[str, Any]] = []
        for s in schemas:
            if isinstance(s, dict) and s.get('type') == 'function' and isinstance(s.get('function'), dict):
                tools.append(s)
        return tools

    def _exec_tool(self, name: str, arguments_json: str) -> str:
        """Execute tool call"""
        inst = self.tool_instances.get(name)
        if not inst:
            return json.dumps({"error": f"tool '{name}' not found"}, ensure_ascii=False)
        try:
            res = inst.call(arguments_json)  # Pass raw JSON string
            return res if isinstance(res, str) else json.dumps(res, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    def _call_llm(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None):
        """Call LLM with unified handling for all models"""
        return call_llm(
            config_name=self.model,
            messages=messages,
            tools=tools
        )

    def _detect_tool_calls(self, assistant_message) -> List[Dict[str, Any]]:
        """Detect and normalize tool calls"""
        tool_calls = getattr(assistant_message, 'tool_calls', None)
        calls: List[Dict[str, Any]] = []
        if not tool_calls:
            return calls

        for idx, tc in enumerate(tool_calls):
            try:
                # Generate unique ID if not provided by the model
                tool_call_id = tc.id
                if tool_call_id is None or not tool_call_id:
                    tool_call_id = f"call_{uuid.uuid4().hex[:24]}"

                # Sanitize arguments: some models occasionally emit invalid JSON
                # (e.g. trailing `</user_parameter>` tags). Once such a call is in
                # messages history, every subsequent API call 400s on the whole
                # session because the API revalidates all historical tool_calls.
                # Replace invalid JSON with "{}" so the tool layer gets empty args
                # and the conversation stays alive.
                raw_args = tc.function.arguments
                if not isinstance(raw_args, str):
                    args = '{}'
                else:
                    try:
                        json.loads(raw_args)
                        args = raw_args
                    except (json.JSONDecodeError, ValueError):
                        args = '{}'

                calls.append({
                    'id': tool_call_id,
                    'name': tc.function.name,
                    'arguments': args,
                })
            except Exception:
                continue

        return calls

    def _add_to_cart(self, history_messages: List[Any]) -> List[Any]:
        # Per-language follow-up turn. Strict resolver — raises if the
        # requested language has no translation, never silently falls back.
        try:
            from .prompts import get_verify_cart_prompt
        except ImportError:
            from prompts import get_verify_cart_prompt
        history_messages = list(history_messages)
        history_messages.append({
            "role": "user",
            "content": get_verify_cart_prompt(self.language),
        })
        return history_messages

    def run(self, user_query: str, system_prompt: str | None = None, max_llm_calls: int = 100, save_messages: bool = True, messages_output_dir: str | None = None, sample_id: str | None = None) -> List[Any]:
        """
        Agent main loop: Call LLM → Execute tools → Repeat until final answer
        
        Args:
            user_query: User query
            system_prompt: System prompt
            max_llm_calls: Maximum LLM calls
            save_messages: Whether to save messages to file
            messages_output_dir: Output directory for messages (if sample_id not provided)
            sample_id: Sample ID for database path resolution
            
        Returns:
            Complete message history
        """
        if save_messages:
            # If sample_id exists, save to {database_base_path}/case_{sample_id}/messages.json
            # Use self.database_base_path for proper isolation when running concurrent instances
            if sample_id:
                db_case_dir = self.database_base_path / f'case_{sample_id}'
                db_case_dir.mkdir(parents=True, exist_ok=True)
                messages_file = db_case_dir / 'messages.json'
            else:
                # Otherwise fallback to result/messages
                msg_dir = Path(messages_output_dir or (Path(__file__).resolve().parent.parent / 'result' / 'messages'))
                msg_dir.mkdir(parents=True, exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                messages_file = msg_dir / f'messages_{ts}.json'

        messages: List[Any] = ([{"role": "system", "content": system_prompt}] if system_prompt else []) + [{"role": "user", "content": user_query}]
        if save_messages:
            self._save_messages(messages, messages_file, 0, "Initial messages")

        # Non-convergence cap: measured normal cases finish in <=37 tool-call rounds
        # while "churner" cases (agent keeps searching/inspecting different products
        # with varied args but never commits a cart) run to 54-88+ and grind for hours
        # against a large/growing context. There is a clean gap at ~40-50, so cap the
        # effective budget at HARD_CALL_CAP: normal cases are untouched, churners are
        # cut early and scored on whatever cart they have (they score ~0 regardless).
        # Applied per-loop below; overrides the (larger) configured max_llm_calls, so
        # the effective per-case budget is min(--max-llm-calls, this cap) — NOT the
        # documented 400. Override via BENCHMARK_SHOPPING_HARD_CALL_CAP; changing it
        # changes the protocol, so results are only comparable at equal cap values.
        HARD_CALL_CAP = int(os.environ.get('BENCHMARK_SHOPPING_HARD_CALL_CAP', '60'))
        max_llm_calls = min(max_llm_calls, HARD_CALL_CAP)

        # Per-case wall-clock deadline: a case that runs far longer than a normal one
        # (measured: a full 50-case level finishes in ~36 min, single normal cases run
        # a few-to-~15 min) is definitionally not going to produce a correct answer --
        # it's just grinding a huge context. Independent of step count, abort any case
        # that exceeds MAX_CASE_SECONDS and score it on its current cart (fails anyway).
        # This HARD-bounds how long a single case can block a level's completion.
        # Same comparability caveat as the call cap; override via
        # BENCHMARK_SHOPPING_CASE_DEADLINE_S.
        MAX_CASE_SECONDS = int(os.environ.get('BENCHMARK_SHOPPING_CASE_DEADLINE_S', str(20 * 60)))
        _case_deadline = time.time() + MAX_CASE_SECONDS

        # Loop-guard: an agent that emits the exact same tool call(s) many times in a
        # row is stuck in a dead loop (it will never satisfy the task and only burns
        # LLM calls up to the cap while its context balloons). Break out after
        # STUCK_LIMIT consecutive identical tool-call signatures and let the case be
        # scored on whatever cart it has (a stuck agent scores ~0 anyway).
        STUCK_LIMIT = 10
        last_sig, repeat = None, 0
        for step_count in range(1, max_llm_calls + 1):
            if time.time() > _case_deadline:
                print(f"  ⏱️ [{threading.current_thread().name}] case exceeded "
                      f"{MAX_CASE_SECONDS//60}min at step {step_count}; aborting (scored on current cart)")
                break
            resp = self._call_llm(messages=messages, tools=self.openai_tools)
            msg = resp.choices[0].message
            
            # Convert message object to serializable dict
            msg_dict = {
                "role": "assistant",
                "content": msg.content or '',
            }
            
            # Preserve reasoning_content if present
            if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
                msg_dict['reasoning_content'] = msg.reasoning_content
            
            calls = self._detect_tool_calls(msg)
            if calls:
                msg_dict["tool_calls"] = [
                    {
                        'id': call['id'],
                        'type': 'function',
                        'function': {
                            'name': call['name'],
                            'arguments': call['arguments']
                        }
                    }
                    for call in calls
                ]
            
            messages.append(msg_dict)
            if save_messages:
                self._save_messages(messages, messages_file, step_count, f"LLM response - {len(calls)} tool calls")
            
            if not calls:
                break

            sig = tuple((c['name'], c['arguments']) for c in calls)
            if sig == last_sig:
                repeat += 1
                if repeat >= STUCK_LIMIT:
                    print(f"  ⛔ [{threading.current_thread().name}] dead-loop detected "
                          f"(same tool call x{STUCK_LIMIT}) at step {step_count}; aborting case")
                    break
            else:
                repeat = 0
            last_sig = sig

            for call in calls:
                tool_result = self._exec_tool(call['name'], call['arguments'])
                messages.append({"role": "tool", "tool_call_id": call['id'], "content": tool_result})
            if save_messages:
                self._save_messages(messages, messages_file, step_count, f"Tool execution completed - {len(calls)} tools")

        messages = self._add_to_cart(messages)
        last_sig, repeat = None, 0
        for step_count in range(1, max_llm_calls + 1):
            if time.time() > _case_deadline:
                print(f"  ⏱️ [{threading.current_thread().name}] case exceeded "
                      f"{MAX_CASE_SECONDS//60}min at add-to-cart step {step_count}; aborting (scored on current cart)")
                break
            resp = self._call_llm(messages=messages, tools=self.openai_tools)
            msg = resp.choices[0].message
            
            # Convert message object to serializable dict
            msg_dict = {
                "role": "assistant",
                "content": msg.content or '',
            }
            
            # Preserve reasoning_content if present
            if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
                msg_dict['reasoning_content'] = msg.reasoning_content
            
            calls = self._detect_tool_calls(msg)
            if calls:
                msg_dict["tool_calls"] = [
                    {
                        'id': call['id'],
                        'type': 'function',
                        'function': {
                            'name': call['name'],
                            'arguments': call['arguments']
                        }
                    }
                    for call in calls
                ]
            
            messages.append(msg_dict)
            if save_messages:
                self._save_messages(messages, messages_file, step_count, f"LLM response - {len(calls)} tool calls")
            
            if not calls:
                return messages

            sig = tuple((c['name'], c['arguments']) for c in calls)
            if sig == last_sig:
                repeat += 1
                if repeat >= STUCK_LIMIT:
                    print(f"  ⛔ [{threading.current_thread().name}] dead-loop detected "
                          f"(same tool call x{STUCK_LIMIT}) at add-to-cart step {step_count}; aborting case")
                    break
            else:
                repeat = 0
            last_sig = sig

            for call in calls:
                tool_result = self._exec_tool(call['name'], call['arguments'])
                messages.append({"role": "tool", "tool_call_id": call['id'], "content": tool_result})
            if save_messages:
                self._save_messages(messages, messages_file, step_count, f"Tool execution completed - {len(calls)} tools")

        return messages
    
    def _save_messages(self, messages: List[Any], filepath: Path, step: int, description: str):
        """Save messages to file"""
        serializable_messages = [m.model_dump() if hasattr(m, 'model_dump') else m for m in messages]
        save_data = {"step": step, "description": description, "messages": serializable_messages}
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            thread_info = threading.current_thread().name
            print(f"  💾 [{thread_info}] Step {step}: {description} - Saved {len(messages)} messages")
        except Exception as e:
            thread_info = threading.current_thread().name
            print(f"  ⚠️  [{thread_info}] Failed to save messages: {e}")


def run_agent_inference(
    model: str,
    test_data_path: Path,
    database_dir: Path,
    tool_schema_path: Path,
    system_prompt: str,
    workers: int = 10,
    max_llm_calls: int = 100,
    rerun_ids: Optional[List[int]] = None,
    language: str = 'en',
) -> Dict[str, Any]:
    """
    Run agent inference (batch processing)
    
    Args:
        model: Configuration name from models_config.json
        test_data_path: Path to test data JSON file
        database_dir: Base path to database directory
        tool_schema_path: Path to tool schema JSON file
        system_prompt: System prompt for the agent
        workers: Number of parallel workers
        max_llm_calls: Maximum LLM calls per sample
        rerun_ids: Optional list of specific IDs to rerun. If None, run all samples.
    
    Returns:
        Results summary dict
    """
    with open(test_data_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    # Pre-warm the Qwen3 BPE tokenizer AND tool registry ONCE before workers
    # fan out. Concurrent first-time `import tools` / `from transformers import
    # AutoTokenizer` calls from 50 threads racing on uninitialised modules
    # caused per-worker ImportErrors that left ShoppingFnAgent with an empty
    # tool_instances dict for the rest of its lifetime — every tool call then
    # returned "tool 'X' not found". One synchronous load up front populates
    # sys.modules + the module-level tokenizer global so workers just hit the
    # cache. Note: must import each tool module via its package path
    # (`tools.search_products_tool`) — a bare `import search_products_tool`
    # would create a SECOND module identity and re-trigger @register_tool,
    # which raises and silently empties tool_instances in workers.
    try:
        _tools_dir = Path(__file__).resolve().parent.parent / 'tools'
        if str(_tools_dir) not in sys.path:
            sys.path.insert(0, str(_tools_dir))
        if str(_tools_dir.parent) not in sys.path:
            sys.path.insert(0, str(_tools_dir.parent))
        import tools as _prewarm_tools  # noqa: F401
        from base_shopping_tool import TOOL_REGISTRY as _prewarm_registry
        if not _prewarm_registry:
            raise RuntimeError("TOOL_REGISTRY is empty after import")
        from tools.search_products_tool import _resolve_tokenize_fn as _prewarm_tok
        _prewarm_tok(language)("warm")
        print(
            f"[run_agent_inference] pre-warm OK: "
            f"{len(_prewarm_registry)} tools, tokenizer for language={language}",
            flush=True,
        )
    except Exception as e:
        print(f"[run_agent_inference] FATAL: pre-warm failed: {e}", flush=True)
        raise
    
    # Filter samples if rerun_ids is specified
    if rerun_ids is not None:
        rerun_ids_set = set(str(id) for id in rerun_ids)  # Convert to strings for comparison
        original_count = len(test_data)
        test_data = [s for s in test_data if str(s.get('id')) in rerun_ids_set]
        print(f"  🔄 Filtered {original_count} samples to {len(test_data)} samples for rerun")
        
        if len(test_data) != len(rerun_ids):
            raise ValueError(
                f"Selected {len(rerun_ids)} task IDs but found {len(test_data)} query records"
            )
    
    print(f"\n{'='*80}")
    print(f"Agent Inference")
    print(f"{'='*80}")
    print(f"Model: {model}")
    print(f"Samples: {len(test_data)}")
    print(f"Workers: {workers}")
    print(f"{'='*80}\n")
    
    print_lock = Lock()
    results = []
    
    def process_sample(sample):
        sample_id = sample.get('id', 'unknown')
        query = sample.get('query', '')
        
        try:
            
            agent = ShoppingFnAgent(
                model=model,
                sample_id=str(sample_id),
                database_base_path=str(database_dir),
                tool_schema_path=str(tool_schema_path),
                language=language,
            )
            
            start_time = time.time()
            
            messages = agent.run(
                user_query=query,
                system_prompt=system_prompt,
                save_messages=True,
                sample_id=str(sample_id),
                max_llm_calls=max_llm_calls
            )
            
            elapsed = time.time() - start_time
            
            result = {
                'id': sample_id,
                'query': query,
                'model': model,
                'messages': messages,
                'elapsed_time': elapsed,
                'success': True,
            }
            
            with print_lock:
                print(f"✅ Sample {sample_id} completed in {elapsed:.2f}s")
            
            return result
            
        except Exception as e:
            with print_lock:
                print(f"❌ Sample {sample_id} failed: {e}")
                import traceback
                traceback.print_exc()
            
            return {
                'id': sample_id,
                'query': query,
                'success': False,
                'error': str(e),
            }
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_sample, sample) for sample in test_data]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    success_count = sum(1 for r in results if r['success'])
    
    return {
        'total': len(results),
        'success': success_count,
        'failed': len(results) - success_count,
        'results': results
    }


if __name__ == '__main__':
    """Simple test"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='qwen-plus', help='Configuration name from models_config.json')
    parser.add_argument('--level', type=int, default=1, choices=[1, 2, 3], help='Shopping level: 1, 2, or 3')
    args = parser.parse_args()
    
    base_dir = Path(__file__).resolve().parent.parent
    test_output_dir = base_dir / 'results' / 'test'
    
    # Get system prompt for the specified level
    try:
        from .prompts import prompt_lib
    except ImportError:
        from prompts import prompt_lib
    
    system_prompt = getattr(prompt_lib, f'SYSTEM_PROMPT_level{args.level}', None)
    if system_prompt is None:
        raise ValueError(f"System prompt for level {args.level} not found")
    
    result = run_agent_inference(
        model=args.model,
        test_data_path=base_dir / 'data' / f'level_{args.level}_query_meta.json',
        database_dir=base_dir / 'database',
        tool_schema_path=base_dir / 'tools' / 'shopping_tool_schema.json',
        system_prompt=system_prompt,
        workers=2,
        max_llm_calls=100,
    )
    print(f"\nTest completed: {result['success']}/{result['total']} succeeded")
