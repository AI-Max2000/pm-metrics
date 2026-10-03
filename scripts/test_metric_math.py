#!/usr/bin/env python3
"""Regression tests for business arithmetic and the JSON CLI contract."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from metric_math import calculate


class MetricMathTests(unittest.TestCase):
    def test_cash_burn_sign_and_runway(self):
        r = calculate(dict(operation="cash_runway", cash=360000,
                           monthly_cash_in=20000, monthly_cash_out=80000))
        self.assertEqual(r["net_monthly_burn"], 60000)
        self.assertEqual(r["runway_months"], 6)

    def test_break_even_is_not_infinite_runway(self):
        r = calculate(dict(operation="cash_runway", cash=360000,
                           monthly_cash_in=80000, monthly_cash_out=80000))
        self.assertEqual(r["status"], "not_burning")
        self.assertIsNone(r["runway_months"])

    def test_positive_cash_flow_is_not_negative_runway(self):
        r = calculate(dict(operation="cash_runway", cash=360000,
                           monthly_cash_in=90000, monthly_cash_out=80000))
        self.assertEqual(r["net_monthly_burn"], -10000)
        self.assertIsNone(r["runway_months"])

    def test_zero_cash(self):
        r = calculate(dict(operation="cash_runway", cash=0,
                           monthly_cash_in=0, monthly_cash_out=10))
        self.assertEqual(r["runway_months"], 0)

    def test_ratio(self):
        r = calculate(dict(operation="ratio", numerator=12, denominator=100))
        self.assertAlmostEqual(r["ratio"], .12)
        self.assertAlmostEqual(r["percent"], 12)

    def test_zero_denominator(self):
        for numerator in (0, 10):
            with self.subTest(numerator=numerator):
                r = calculate(dict(operation="ratio", numerator=numerator, denominator=0))
                self.assertEqual(r["status"], "undefined")
                self.assertIsNone(r["percent"])

    def test_growth_and_decline(self):
        for current, expected in ((120, 20), (80, -20), (0, -100)):
            with self.subTest(current=current):
                r = calculate(dict(operation="growth", current=current, previous=100))
                self.assertAlmostEqual(r["growth_percent"], expected)

    def test_zero_baseline(self):
        r = calculate(dict(operation="growth", current=20, previous=0))
        self.assertIsNone(r["growth_percent"])
        self.assertEqual(r["absolute_change"], 20)

    def test_mrr_bridge(self):
        r = calculate(dict(operation="mrr_bridge", start=100, new=20,
                           expansion=10, contraction=5, churn=15))
        self.assertEqual(r["end_mrr"], 110)
        self.assertEqual(r["net_new_mrr"], 10)

    def test_nrr_excludes_new_revenue(self):
        r = calculate(dict(operation="nrr", start=100, expansion=10,
                           contraction=5, churn=15))
        self.assertEqual(r["nrr_percent"], 90)
        with self.assertRaisesRegex(ValueError, "unexpected"):
            calculate(dict(operation="nrr", start=100, new=20, expansion=10,
                           contraction=5, churn=15))

    def test_nrr_above_one_hundred_is_valid(self):
        r = calculate(dict(operation="nrr", start=100, expansion=50,
                           contraction=0, churn=0))
        self.assertEqual(r["nrr_percent"], 150)

    def test_nrr_zero_cohort(self):
        r = calculate(dict(operation="nrr", start=0, expansion=0,
                           contraction=0, churn=0))
        self.assertEqual(r["status"], "undefined")

    def test_negative_cohort_is_rejected_even_if_new_mrr_offsets_it(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            calculate(dict(operation="mrr_bridge", start=100, new=100,
                           expansion=0, contraction=50, churn=60))

    def test_bad_numeric_inputs(self):
        for value in (None, True, "20", -1, float("nan"), float("inf"), 10 ** 1000):
            with self.subTest(type=type(value).__name__):
                with self.assertRaises(ValueError):
                    calculate(dict(operation="ratio", numerator=value, denominator=10))

    def test_overflow_rejected(self):
        with self.assertRaisesRegex(ValueError, "numeric range"):
            calculate(dict(operation="ratio", numerator=1e308, denominator=1e-308))

    def test_missing_extra_and_invalid_operation(self):
        for payload in ({}, [], {"operation": []}, {"operation": "unknown"},
                        {"operation": "growth", "current": 1},
                        {"operation": "growth", "current": 1, "previous": 2, "prevoius": 3}):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    calculate(payload)

    def cli(self, raw):
        return subprocess.run([sys.executable, str(Path(__file__).with_name("metric_math.py"))],
                              input=raw, text=True, capture_output=True, check=False)

    def test_cli_json_success(self):
        p = self.cli('{"operation":"ratio","numerator":1,"denominator":4}')
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["percent"], 25)
        self.assertEqual(p.stderr, "")

    def test_cli_rejects_invalid_json_constants_and_duplicate_keys(self):
        for raw in ('{"operation":"ratio","numerator":NaN,"denominator":4}',
                    '{"operation":"ratio","numerator":1,"numerator":2,"denominator":4}',
                    'not json'):
            with self.subTest(raw=raw):
                p = self.cli(raw)
                self.assertEqual(p.returncode, 2)
                self.assertEqual(p.stdout, "")
                self.assertEqual(json.loads(p.stderr)["status"], "error")

    def test_cli_file_example(self):
        root = Path(__file__).resolve().parents[1]
        p = subprocess.run([sys.executable, str(root / "scripts/metric_math.py"),
                            str(root / "examples/cash-burn.json")],
                           text=True, capture_output=True, check=False)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["runway_months"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
