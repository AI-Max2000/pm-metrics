#!/usr/bin/env python3
"""Offline arithmetic for explicitly supplied, non-negative product metrics.

No data collection, file modification, forecasting, or significance testing.
All ratios have explicit zero-denominator handling. Requires Python 3.9+.
"""

import argparse
import json
import math
import sys


FIELDS = {
    "ratio": {"numerator", "denominator"},
    "growth": {"current", "previous"},
    "mrr_bridge": {"start", "new", "expansion", "contraction", "churn"},
    "nrr": {"start", "expansion", "contraction", "churn"},
    "cash_runway": {"cash", "monthly_cash_in", "monthly_cash_out"},
}


def finite_nonnegative(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a JSON number, not a string or boolean")
    try:
        valid = math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f"{field} must be finite and non-negative")
    return value


def calculate(data):
    """Return a result dict or raise ValueError for invalid/unsupported input."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    operation = data.get("operation")
    if not isinstance(operation, str) or operation not in FIELDS:
        raise ValueError("operation must be one of: " + ", ".join(FIELDS))
    required = FIELDS[operation]
    missing = required - data.keys()
    extra = data.keys() - required - {"operation"}
    if missing:
        raise ValueError("missing fields: " + ", ".join(sorted(missing)))
    if extra:
        raise ValueError("unexpected fields: " + ", ".join(sorted(extra)))
    v = {key: finite_nonnegative(data[key], key) for key in required}
    result = {"operation": operation, "status": "ok"}

    if operation == "ratio":
        if v["denominator"] == 0:
            result.update(status="undefined", ratio=None, percent=None,
                          reason="zero_denominator")
        else:
            ratio = v["numerator"] / v["denominator"]
            result.update(ratio=ratio, percent=ratio * 100)
    elif operation == "growth":
        delta = v["current"] - v["previous"]
        result["absolute_change"] = delta
        if v["previous"] == 0:
            result.update(status="undefined", growth_fraction=None,
                          growth_percent=None, reason="zero_baseline")
        else:
            growth = delta / v["previous"]
            result.update(growth_fraction=growth, growth_percent=growth * 100)
    elif operation in ("mrr_bridge", "nrr"):
        cohort_end = v["start"] + v["expansion"] - v["contraction"] - v["churn"]
        if cohort_end < 0:
            raise ValueError("ending cohort revenue is negative; check component overlap")
        if operation == "mrr_bridge":
            end = cohort_end + v["new"]
            result.update(end_mrr=end, net_new_mrr=end - v["start"])
        else:
            result["ending_cohort_revenue"] = cohort_end
            if v["start"] == 0:
                result.update(status="undefined", nrr_fraction=None,
                              nrr_percent=None, reason="zero_starting_cohort_revenue")
            else:
                nrr = cohort_end / v["start"]
                result.update(nrr_fraction=nrr, nrr_percent=nrr * 100)
    elif operation == "cash_runway":
        burn = v["monthly_cash_out"] - v["monthly_cash_in"]
        result["net_monthly_burn"] = burn
        if burn <= 0:
            result.update(status="not_burning", runway_months=None,
                          reason="non_positive_net_burn")
        else:
            result["runway_months"] = v["cash"] / burn

    for key, value in result.items():
        if isinstance(value, (int, float)):
            try:
                finite = math.isfinite(value)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError(f"{key} exceeds supported numeric range")
    return result


def reject_constant(value):
    raise ValueError(f"invalid JSON numeric constant: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-",
                        help="JSON file, or - / omitted to read standard input")
    args = parser.parse_args(argv)
    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as handle:
                raw = handle.read()
        data = json.loads(raw, parse_constant=reject_constant,
                          object_pairs_hook=unique_object)
        result = calculate(data)
    except (ValueError, OSError, OverflowError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
