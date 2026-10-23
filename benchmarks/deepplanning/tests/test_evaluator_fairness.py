"""Fairness fixes in the travel evaluator and baseline tool labels (v7).

Three defects the 2026-08-10 translation review found:

1. Entity-name matching was byte-exact, so a plan name that is canonically
   equivalent to the scored anchor but differently Unicode-normalized failed
   the hard constraint. This is real in the shipped data: `my` id_64 stores
   the attraction anchor with U+1025 U+102E where NFC uses U+1026, and `pa`
   id_16 stores the restaurant anchor with precomposed U+0A36 where NFC uses
   U+0A38 U+0A3C. The agent copies the name verbatim from the rendered DB,
   so a normalization mismatch is data noise, not model error.
2. `mode` word lists were exact membership, so a converter emitting an
   unlisted-but-correct variant (ko "flight" as a native word) silently
   emptied the flight/train extraction and force-failed the transport
   constraints.
3. The en/zh `not_found` label lambdas in `flight_query_tool` took 4 args
   while the call site passes 3, so baseline runs raised TypeError instead of
   returning "no flights found" on an empty flight query.
"""
from __future__ import annotations

import sys
import types
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from travelplanning.evaluation.constraints_hard import eval_hard


# Substrings of real shipped anchors, spelled as \u escapes so the fixtures
# survive any editor or tool that would silently NFC-normalize this file.
# my id_64 attraction anchor: U+1025 U+102E composes to U+1026 under NFC.
MY_ATTRACTION_SHIPPED = "\u1014\u103d\u1031\u1025\u102e\u1038\u1021\u101b\u102f\u100f\u103a"
# pa id_16 restaurant anchor: precomposed U+0A36 decomposes to U+0A38 U+0A3C
# under NFC (Unicode composition exclusion).
PA_RESTAURANT_SHIPPED = "\u0a2f\u0a41\u0a35\u0a47\u0a08 \u0a2b\u0a3f\u0a36"
# pa id_77 hotel anchor shape, same U+0A36 issue.
PA_HOTEL_SHIPPED = "\u0a13\u0a30\u0a47\u0a02\u0a1c \u0a36\u0a3e\u0a16\u0a3e"

KO_FLIGHT = "\ube44\ud589\uae30"  # 비행기
KO_TRAIN = "\uae30\ucc28"          # 기차


def _plan_with(activities=None, accommodation=None):
    day = {"day_number": 1, "activities": activities or []}
    if accommodation is not None:
        day["accommodation"] = accommodation
    return {"daily_plans": [day]}


class NfcEntityMatchingTests(unittest.TestCase):
    """Anchor and plan name differ only by Unicode normalization form."""

    def test_fixtures_really_are_non_nfc(self):
        for name in (
            MY_ATTRACTION_SHIPPED,
            PA_RESTAURANT_SHIPPED,
            PA_HOTEL_SHIPPED,
        ):
            self.assertNotEqual(unicodedata.normalize("NFC", name), name)

    def test_attraction_names_match_across_normalization_forms(self):
        meta = {
            "hard_constraints": {
                "attraction_must_visit_named": {
                    "attraction_names": [MY_ATTRACTION_SHIPPED]
                }
            }
        }
        plan = _plan_with(
            activities=[
                {
                    "type": "attraction",
                    "details": {
                        "name": unicodedata.normalize("NFC", MY_ATTRACTION_SHIPPED)
                    },
                }
            ]
        )
        ok, msg = eval_hard(plan, meta)["attraction_must_visit_named"]
        self.assertTrue(ok, msg)

    def test_restaurant_name_matches_across_normalization_forms(self):
        meta = {
            "hard_constraints": {
                "restaurant_must_eat_named": {
                    "restaurant_name": PA_RESTAURANT_SHIPPED
                }
            }
        }
        plan = _plan_with(
            activities=[
                {
                    "type": "meal",
                    "details": {
                        "name": unicodedata.normalize("NFC", PA_RESTAURANT_SHIPPED)
                    },
                }
            ]
        )
        ok, msg = eval_hard(plan, meta)["restaurant_must_eat_named"]
        self.assertTrue(ok, msg)

    def test_hotel_name_matches_across_normalization_forms(self):
        meta = {
            "hard_constraints": {
                "hotel_cheapest_star": {
                    "hotel_name": PA_HOTEL_SHIPPED,
                    "hotel_star": 4,
                }
            }
        }
        plan = _plan_with(
            accommodation={
                "name": unicodedata.normalize("NFC", PA_HOTEL_SHIPPED),
                "price_per_night": 100,
            }
        )
        ok, msg = eval_hard(plan, meta)["hotel_cheapest_star"]
        self.assertTrue(ok, msg)

    def test_genuinely_different_name_still_fails(self):
        meta = {
            "hard_constraints": {
                "restaurant_must_eat_named": {
                    "restaurant_name": "Ru Zhuo Western Restaurant"
                }
            }
        }
        plan = _plan_with(
            activities=[{"type": "meal", "details": {"name": "Some Other Place"}}]
        )
        ok, _ = eval_hard(plan, meta)["restaurant_must_eat_named"]
        self.assertFalse(ok)



class TransportModeMatchingTests(unittest.TestCase):
    def _intercity(self, mode: str, number: str):
        return _plan_with(
            activities=[
                {
                    "type": "travel_intercity_public",
                    "details": {"mode": mode, "number": number, "cost": 500},
                }
            ]
        )

    def test_korean_flight_variant_is_recognized(self):
        meta = {
            "hard_constraints": {
                "flight_cheapest_direct": {"outbound_flight_no": "MU5137"}
            }
        }
        ok, msg = eval_hard(self._intercity(KO_FLIGHT, "MU5137"), meta)[
            "flight_cheapest_direct"
        ]
        self.assertTrue(ok, msg)

    def test_mode_matching_ignores_surrounding_whitespace_and_case(self):
        meta = {
            "hard_constraints": {
                "flight_cheapest_direct": {"outbound_flight_no": "MU5137"}
            }
        }
        ok, msg = eval_hard(self._intercity("  Flight  ", "MU5137"), meta)[
            "flight_cheapest_direct"
        ]
        self.assertTrue(ok, msg)

    def test_korean_train_variant_is_recognized(self):
        meta = {
            "hard_constraints": {
                "train_cheapest_direct": {"outbound_train_no": "G7554"}
            }
        }
        ok, msg = eval_hard(self._intercity(KO_TRAIN, "G7554"), meta)[
            "train_cheapest_direct"
        ]
        self.assertTrue(ok, msg)

    def test_unrelated_mode_is_not_a_flight(self):
        meta = {
            "hard_constraints": {
                "flight_cheapest_direct": {"outbound_flight_no": "MU5137"}
            }
        }
        ok, _ = eval_hard(self._intercity("taxi", "MU5137"), meta)[
            "flight_cheapest_direct"
        ]
        self.assertFalse(ok)


class BaselineFlightLabelTests(unittest.TestCase):
    """qwen_agent is not installed in the test env; stub the base it needs."""

    def _load_flight_tool_labels(self):
        if "qwen_agent" not in sys.modules:
            base = types.ModuleType("qwen_agent.tools.base")
            base.BaseTool = type("BaseTool", (), {})
            base.register_tool = lambda name: (lambda cls: cls)
            base.TOOL_REGISTRY = {}
            tools_mod = types.ModuleType("qwen_agent.tools")
            tools_mod.base = base
            root = types.ModuleType("qwen_agent")
            root.tools = tools_mod
            sys.modules.update(
                {
                    "qwen_agent": root,
                    "qwen_agent.tools": tools_mod,
                    "qwen_agent.tools.base": base,
                }
            )
        from travelplanning.tools.flight_query_tool import FlightQueryTool

        return FlightQueryTool.LANG_FIELDS

    def test_not_found_label_accepts_the_three_args_the_caller_passes(self):
        lang_fields = self._load_flight_tool_labels()
        for lang in ("zh", "en"):
            with self.subTest(lang=lang):
                text = lang_fields[lang]["not_found"](
                    "Hefei", "Nanjing", "2024-05-01"
                )
                self.assertIn("Hefei", text)
                self.assertIn("Nanjing", text)
                self.assertIn("2024-05-01", text)


class DbIndexNormalizationTests(unittest.TestCase):
    """The sandbox-compliance indexes must answer for either NFC form.

    `constraints_commonsense.py` looks plan names up in these indexes; some
    shipped DB cells are non-NFC while the converter emits NFC.
    """

    def _write_csv(self, tmpdir, filename, header, name):
        path = Path(tmpdir) / filename
        path.write_text(
            f"{header}\n{name},1,08:00,18:00\n", encoding="utf-8"
        )
        return str(path)

    def test_attraction_index_resolves_both_forms(self):
        import tempfile

        from travelplanning.evaluation.utils import load_attraction_index

        raw = MY_ATTRACTION_SHIPPED
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "attractions.csv"
            csv_path.write_text(
                "attraction_name,ticket_price,opening_time,closing_time\n"
                f"{raw},50,08:00,18:00\n",
                encoding="utf-8",
            )
            index = load_attraction_index(str(csv_path))
        self.assertIn(raw, index)
        self.assertIn(unicodedata.normalize("NFC", raw), index)

    def test_hotel_index_resolves_both_forms(self):
        import tempfile

        from travelplanning.evaluation.utils import load_hotel_index

        raw = PA_HOTEL_SHIPPED
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "hotels.csv"
            csv_path.write_text(
                f"name,price,city\n{raw},300,Hefei\n", encoding="utf-8"
            )
            index = load_hotel_index(str(csv_path))
        self.assertIn(raw, index)
        self.assertIn(unicodedata.normalize("NFC", raw), index)

    def test_restaurant_index_resolves_both_forms(self):
        import tempfile

        from travelplanning.evaluation.utils import load_restaurant_index

        raw = PA_RESTAURANT_SHIPPED
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "restaurants.csv"
            csv_path.write_text(
                "restaurant_name,price_per_person,opening_time,closing_time\n"
                f"{raw},80,10:00,22:00\n",
                encoding="utf-8",
            )
            index = load_restaurant_index(str(csv_path))
        self.assertIn(raw, index)
        self.assertIn(unicodedata.normalize("NFC", raw), index)


if __name__ == "__main__":
    unittest.main()

