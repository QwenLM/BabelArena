from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SHOPPING_ROOT = ROOT / "shoppingplanning"
TOOLS_ROOT = SHOPPING_ROOT / "tools"
for path in (str(SHOPPING_ROOT), str(TOOLS_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

import tokenizer_config
import tools.search_products_tool as search_products
from shoppingplanning.agent import shopping_agent
from base_shopping_tool import TOOL_REGISTRY


class FakeTokenizer:
    def encode(self, text, add_special_tokens=False):
        return [len(text), 7] if text else []


class ShoppingTokenizerTests(unittest.TestCase):
    def tearDown(self):
        with search_products._QWEN_TOK_LOCK:
            search_products._QWEN_TOK = None
            search_products._QWEN_TOK_KEY = None

    def settings(self, cache_dir: Path):
        return tokenizer_config.resolve_tokenizer_settings(
            "test/tokenizer",
            "0123456789abcdef0123456789abcdef01234567",
            cache_dir,
        )

    def write_manifest(self, settings):
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        settings.manifest_path.write_text(
            json.dumps(
                {
                    "model": settings.model,
                    "revision": settings.revision,
                    "validated_offline": True,
                }
            ),
            encoding="utf-8",
        )

    def tokenizer_env(self, settings):
        return mock.patch.dict(
            os.environ,
            {
                tokenizer_config.TOKENIZER_MODEL_ENV: settings.model,
                tokenizer_config.TOKENIZER_REVISION_ENV: settings.revision,
                tokenizer_config.TOKENIZER_CACHE_ENV: str(settings.cache_dir),
            },
        )

    def test_default_artifact_revision_is_immutable(self):
        self.assertEqual(tokenizer_config.DEFAULT_TOKENIZER_MODEL, "Qwen/Qwen3-8B")
        self.assertRegex(tokenizer_config.DEFAULT_TOKENIZER_REVISION, r"^[0-9a-f]{40}$")
        self.assertNotEqual(tokenizer_config.DEFAULT_TOKENIZER_REVISION, "main")

    def test_model_revision_and_cache_have_independent_environment_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = self.settings(Path(temp_dir))
            with self.tokenizer_env(settings):
                resolved = tokenizer_config.resolve_tokenizer_settings()
            self.assertEqual(resolved, settings)

    def test_requirements_pin_tested_tokenizer_runtime(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        for requirement in (
            "transformers==5.10.2",
            "tokenizers==0.22.1",
            "huggingface-hub==1.18.0",
            "safetensors==0.6.2",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, requirements)

    def test_prepare_downloads_then_validates_offline_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = self.settings(Path(temp_dir))
            calls = []

            def load(current_settings, *, local_files_only):
                self.assertEqual(current_settings, settings)
                calls.append(local_files_only)
                return FakeTokenizer()

            with mock.patch.object(
                tokenizer_config, "_load_auto_tokenizer", side_effect=load
            ):
                tokenizer, changed = tokenizer_config.prepare_tokenizer(settings)
                self.assertTrue(changed)
                self.assertIsInstance(tokenizer, FakeTokenizer)
                self.assertEqual(calls, [False, True, True])
                manifest = tokenizer_config.load_prepared_manifest(settings)
                self.assertEqual(manifest["model"], settings.model)
                self.assertEqual(manifest["revision"], settings.revision)

                calls.clear()
                tokenizer, changed = tokenizer_config.prepare_tokenizer(settings)
                self.assertFalse(changed)
                self.assertIsInstance(tokenizer, FakeTokenizer)
                self.assertEqual(calls, [True])

    def test_missing_manifest_fails_with_setup_command_before_import(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = self.settings(Path(temp_dir))
            with self.tokenizer_env(settings):
                with self.assertRaisesRegex(RuntimeError, "prepare_shopping_tokenizer.py"):
                    search_products._get_qwen_tokenizer()

    def test_runtime_is_local_only_and_covers_every_script_family(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = self.settings(Path(temp_dir))
            self.write_manifest(settings)
            fake = FakeTokenizer()
            with (
                self.tokenizer_env(settings),
                mock.patch(
                    "transformers.AutoTokenizer.from_pretrained", return_value=fake
                ) as from_pretrained,
            ):
                for language in (
                    "chinese",
                    "japanese",
                    "korean",
                    "thai",
                    "khmer",
                    "burmese",
                    "lao",
                ):
                    with self.subTest(language=language):
                        tokens = search_products._resolve_tokenize_fn(language)("商品测试")
                        self.assertTrue(tokens)
                from_pretrained.assert_called_once_with(
                    settings.model,
                    revision=settings.revision,
                    cache_dir=str(settings.cache_dir),
                    local_files_only=True,
                )

            with mock.patch.object(search_products, "_get_qwen_tokenizer") as get_tokenizer:
                self.assertEqual(
                    search_products._resolve_tokenize_fn("english")("Two Shoes"),
                    ["two", "shoes"],
                )
                get_tokenizer.assert_not_called()

    def test_search_tool_stays_registered(self):
        self.assertIs(TOOL_REGISTRY.get("search_products"), search_products.SearchProductsTool)

    def test_concurrent_workers_initialize_one_tokenizer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = self.settings(Path(temp_dir))
            self.write_manifest(settings)
            fake = FakeTokenizer()
            with (
                self.tokenizer_env(settings),
                mock.patch(
                    "transformers.AutoTokenizer.from_pretrained", return_value=fake
                ) as from_pretrained,
                ThreadPoolExecutor(max_workers=16) as executor,
            ):
                tokenizers = list(
                    executor.map(
                        lambda _: search_products._get_qwen_tokenizer(), range(64)
                    )
                )
            self.assertTrue(all(tokenizer is fake for tokenizer in tokenizers))
            self.assertEqual(from_pretrained.call_count, 1)

    def test_missing_setup_aborts_batch_before_any_llm_request(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            settings = self.settings(root / "cache")
            dataset = root / "tasks.json"
            dataset.write_text("[]", encoding="utf-8")
            schema = root / "schema.json"
            schema.write_text("[]", encoding="utf-8")
            with (
                self.tokenizer_env(settings),
                mock.patch.object(shopping_agent, "call_llm") as call_llm,
            ):
                with self.assertRaisesRegex(RuntimeError, "prepare_shopping_tokenizer.py"):
                    shopping_agent.run_agent_inference(
                        model="unused",
                        test_data_path=dataset,
                        database_dir=root,
                        tool_schema_path=schema,
                        system_prompt="prompt",
                        workers=2,
                        language="chinese",
                    )
            call_llm.assert_not_called()


if __name__ == "__main__":
    unittest.main()
