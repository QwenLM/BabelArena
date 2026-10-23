"""Carrier words glued onto intercity transport numbers (v7).

The evaluator exact-matches `details.number` against the flight/train DB
index. On some languages the conversion LLM emits the localized mode word
inside the number field ("Vol MU5137", the Russian for "train G7554"), which
force-failed every transport hard constraint for those languages even when the
plan was correct. `normalize_transport_numbers` keeps only the bare number
when exactly one token qualifies, and leaves anything ambiguous alone.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from travelplanning.evaluation.convert_report import normalize_transport_numbers

RU_TRAIN = "поезд"  # поезд
KO_FLIGHT = "비행기"             # 비행기


def _plan(number, mode="flight"):
    return {
        "daily_plans": [
            {
                "day_number": 1,
                "activities": [
                    {
                        "type": "travel_intercity_public",
                        "details": {"mode": mode, "number": number, "cost": 500},
                    }
                ],
            }
        ]
    }


def _number(plan):
    return plan["daily_plans"][0]["activities"][0]["details"]["number"]


class NormalizeTransportNumbersTests(unittest.TestCase):
    def test_french_carrier_word_is_stripped(self):
        plan = _plan("Vol MU5137")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(_number(plan), "MU5137")

    def test_russian_carrier_word_is_stripped(self):
        plan = _plan(f"{RU_TRAIN} G7554", mode="train")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(_number(plan), "G7554")

    def test_korean_carrier_word_is_stripped(self):
        plan = _plan(f"{KO_FLIGHT} MU5137")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(_number(plan), "MU5137")

    def test_parenthesized_number_is_recovered(self):
        plan = _plan("Flight (MU5137)")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(_number(plan), "MU5137")

    def test_digit_prefixed_carrier_code_survives(self):
        plan = _plan("Vol 9C8888")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(_number(plan), "9C8888")

    def test_already_bare_number_is_untouched(self):
        for bare in ("MU5137", "G7554", "9C8888", "1462", "KTX101"):
            with self.subTest(bare=bare):
                plan = _plan(bare)
                self.assertEqual(normalize_transport_numbers(plan), 0)
                self.assertEqual(_number(plan), bare)

    def test_two_candidate_numbers_are_left_alone(self):
        plan = _plan("MU5137 / MU5138")
        self.assertEqual(normalize_transport_numbers(plan), 0)
        self.assertEqual(_number(plan), "MU5137 / MU5138")

    def test_no_candidate_leaves_value_verbatim(self):
        plan = _plan("morning express")
        self.assertEqual(normalize_transport_numbers(plan), 0)
        self.assertEqual(_number(plan), "morning express")

    def test_plans_key_variant_is_handled(self):
        plan = _plan("Vol MU5137")
        plan["plans"] = plan.pop("daily_plans")
        self.assertEqual(normalize_transport_numbers(plan), 1)
        self.assertEqual(
            plan["plans"][0]["activities"][0]["details"]["number"], "MU5137"
        )

    def test_non_transport_activities_are_ignored(self):
        plan = {
            "daily_plans": [
                {
                    "day_number": 1,
                    "activities": [
                        {
                            "type": "attraction",
                            "details": {"name": "Vol MU5137", "number": "Vol MU5137"},
                        }
                    ],
                }
            ]
        }
        self.assertEqual(normalize_transport_numbers(plan), 0)

    def test_malformed_plan_shapes_do_not_raise(self):
        for bad in ({}, {"daily_plans": None}, {"daily_plans": [None]},
                    {"daily_plans": [{"activities": None}]},
                    {"daily_plans": [{"activities": [{"type": "travel_intercity_public",
                                                      "details": None}]}]}):
            with self.subTest(bad=bad):
                self.assertEqual(normalize_transport_numbers(bad), 0)


if __name__ == "__main__":
    unittest.main()
