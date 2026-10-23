import json
import os
import sys
import threading
import unicodedata
from pathlib import Path
from typing import Callable, Dict, List, Union

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

from base_shopping_tool import BaseShoppingTool, register_tool

# Make the project-root `languages` registry importable so we can dispatch
# tokenization on script family. The tools dir sits at deepplanning/shoppingplanning/tools/.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
try:
    from languages import resolve_language as _resolve_language
except Exception:
    _resolve_language = None

_SHOPPING_ROOT = Path(__file__).resolve().parent.parent
if str(_SHOPPING_ROOT) not in sys.path:
    sys.path.insert(0, str(_SHOPPING_ROOT))
from tokenizer_config import (  # noqa: E402
    load_prepared_manifest,
    resolve_tokenizer_settings,
)

# BM25 similarity score threshold; only products with score above this value are returned
BM25_SCORE_THRESHOLD = 2

# Script families whose text has no (or only partial) whitespace word boundaries.
# For these, `.split()` collapses multi-character compound nouns into one giant
# token and BM25 can't match common queries. Use the Qwen3 BPE tokenizer instead.
_NON_WHITESPACE_FAMILIES = frozenset({'cjk', 'thai', 'khmer', 'burmese', 'lao'})

_QWEN_TOK = None
_QWEN_TOK_KEY = None
_QWEN_TOK_LOCK = threading.Lock()


def _get_qwen_tokenizer():
    """Lazy-load the Qwen3 tokenizer once per process.

    The explicit setup command must have completed first. Runtime loading is
    always local-only and guarded by a lock so worker threads share one object.
    """
    global _QWEN_TOK, _QWEN_TOK_KEY
    settings = resolve_tokenizer_settings()
    cache_key = (settings.model, settings.revision, str(settings.cache_dir))
    if _QWEN_TOK is not None and _QWEN_TOK_KEY == cache_key:
        return _QWEN_TOK
    with _QWEN_TOK_LOCK:
        if _QWEN_TOK is not None and _QWEN_TOK_KEY == cache_key:
            return _QWEN_TOK
        load_prepared_manifest(settings)
        try:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                settings.model,
                revision=settings.revision,
                cache_dir=str(settings.cache_dir),
                local_files_only=True,
            )
            tokens = tokenizer.encode("Shopping tokenizer preflight", add_special_tokens=False)
            if not tokens:
                raise RuntimeError("tokenizer returned no preflight tokens")
        except Exception as exc:
            raise RuntimeError(
                f"search_products: prepared tokenizer is missing or incomplete for "
                f"{settings.model}@{settings.revision} in {settings.cache_dir}. "
                "Run scripts/prepare_shopping_tokenizer.py before the benchmark. "
                f"Offline load error: {exc}"
            ) from exc
        _QWEN_TOK = tokenizer
        _QWEN_TOK_KEY = cache_key
        return _QWEN_TOK


def _resolve_tokenize_fn(language: str) -> Callable[[str], List[str]]:
    """Pick a tokenize function based on the active language's script family.

    Latin/Cyrillic/Arabic/Hebrew/Devanagari/Gurmukhi/Tamil/Telugu all whitespace-
    segment their words, so the legacy `.split()` path is preserved (no behavior
    change for English baseline). CJK/Thai/Khmer/Burmese/Lao have no internal
    whitespace — for those we use Qwen3 BPE subword tokens so compound nouns
    (e.g., ランニングシューズ, 运动鞋) decompose into matchable pieces. The
    tokenizer load is mandatory for those families; no fallback.
    """
    family = None
    if _resolve_language is not None:
        try:
            spec = _resolve_language(language)
            family = spec.script_family if spec is not None else None
        except Exception:
            family = None
    if family in _NON_WHITESPACE_FAMILIES:
        tok = _get_qwen_tokenizer()

        def _bpe_tokenize(text: str) -> List[str]:
            if not text:
                return []
            # NFC first: a few rendered DB cells and translated queries disagree
            # on Unicode normalization form (my/pa), which would otherwise split
            # into different BPE ids for canonically identical text.
            text = unicodedata.normalize('NFC', text)
            # Use raw token IDs (stringified) as BM25 terms. Same encode path
            # for corpus and query → consistent terms, no string-normalization
            # surprises from BPE leading-space markers.
            return [str(i) for i in tok.encode(text, add_special_tokens=False)]
        return _bpe_tokenize
    return lambda text: unicodedata.normalize('NFC', text).lower().split()

@register_tool('search_products')
class SearchProductsTool(BaseShoppingTool):
    """
    Handle open-ended natural language user queries by performing semantic matching
    using the BM25 algorithm on key product fields.
    """

    LANG_FIELDS = {
        'en': {
            'bm25_unavailable': "BM25 index is not available. Check database loading.",
        },
        'zh': {
            'bm25_unavailable': "BM25 索引不可用，请检查数据库加载。",
        },
    }

    def __init__(self, cfg: Dict = None):
        """
        Initialize the tool, load the product database, and prepare for BM25 matching.
        """
        super().__init__(cfg)

        self.products: List[Dict] = []
        self.bm25 = None
        # Resolve tokenizer once per instance — picks Qwen3 BPE for non-whitespace
        # script families, falls back to `.split()` for Latin/etc.
        self._tokenize = _resolve_tokenize_fn(self.language)

        default_db_path = os.path.join(
            os.path.dirname(__file__), '..', 'database', 'case_0', 'products.jsonl'
        )

        if self.cfg and 'database_path' in self.cfg and self.cfg['database_path']:
            db_path = Path(self.cfg['database_path']) / 'products.jsonl'
        else:
            db_path = default_db_path

        self._load_and_prepare_database(db_path)

    def _load_and_prepare_database(self, path: str):
        """Load database and build corpus for BM25 indexing."""
        corpus = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        product = json.loads(line)
                        self.products.append(product)

                        # Create a "rich text" document for each product by concatenating key fields
                        searchable_text = " ".join([
                            product.get('brand', ''),
                            product.get('color', ''),
                            product.get('size', ''),
                            product.get('thickness', ''),
                            product.get('elasticity', ''),
                            product.get('version_type', ''),
                            product.get('collar_type', ''),
                            product.get('suitable_season', ''),
                            product.get('target_demographic', ''),
                            product.get('name', ''),
                        ])
                        corpus.append(searchable_text)

            if corpus:
                tokenized_corpus = [self._tokenize(doc) for doc in corpus]
                self.bm25 = BM25Okapi(tokenized_corpus)
        except FileNotFoundError:
            pass
        except Exception:
            pass

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Main logic for BM25-based product search.
        """
        if not self.bm25:
            return self.format_result_as_json({
                "error": self.fields['bm25_unavailable']
            })

        try:
            params_dict = self._verify_json_format_args(params)
        except ValueError as e:
            return self.format_result_as_json({"error": str(e)})

        query = params_dict.get('query')
        limit = params_dict.get('limit', 20)

        if not query:
            return self.format_result_as_json({"product_ids": []})

        tokenized_query = self._tokenize(query)

        # Calculate BM25 scores for all documents
        doc_scores = self.bm25.get_scores(tokenized_query)

        # Collect products with scores above the threshold
        results_with_scores = []
        for i, score in enumerate(doc_scores):
            if score > BM25_SCORE_THRESHOLD:
                results_with_scores.append({
                    "product_id": self.products[i]['product_id'],
                    "name": self.products[i]['name'],
                    "score": score
                })

        # Sort by score descending, then limit result count
        sorted_results = sorted(results_with_scores, key=lambda x: x['score'], reverse=True)
        limited_results = sorted_results[:limit]

        final_product_ids = [item['product_id'] for item in limited_results]

        return self.format_result_as_json({"product_ids": final_product_ids})
