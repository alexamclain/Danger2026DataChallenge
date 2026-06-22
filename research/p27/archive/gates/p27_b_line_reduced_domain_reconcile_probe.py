#!/usr/bin/env python3
"""Reconcile reduced-cover point-count B fibers with frozen legal B fixtures.

The reduced-cover point count enumerates a larger eta=+1 chart than the frozen
selected-source B fixture.  This probe compares the domains and checks whether
the selector-lift profile agrees with the known d3 sign on the actual legal
B-domain.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps
from p27_b_line_reduced_cover_pointcount_probe import field_rows, parse_ints


DEFAULT_FIXTURE = Path("research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json")


def load_fixture(path: Path) -> dict[int, dict[int, str]]:
    packet = json.loads(path.read_text())
    out: dict[int, dict[int, str]] = {}
    for fixture in packet["fixtures"]:
        q = int(fixture["field"])
        out[q] = {int(row["B"]): str(row["sign"]) for row in fixture["rows"]}
    return out


def lift_units(row: Counter, unit: int) -> int | str:
    plus = row["selector_chi_1"]
    if plus % unit:
        return "nonintegral"
    return plus // unit


def sign_to_lift(sign: str) -> int | None:
    if sign == "plus":
        return 2
    if sign == "minus":
        return 0
    return None


def lift_hist(by_b: dict[int, Counter], values: set[int], unit: int) -> Counter:
    hist: Counter = Counter()
    for b in values:
        row = by_b.get(b)
        if row is None:
            hist["missing_pointcount_row"] += 1
            continue
        hist[f"lift_units_{lift_units(row, unit)}"] += 1
    return hist


def check_fixture_lifts(by_b: dict[int, Counter], fixture: dict[int, str], unit: int) -> Counter:
    stats: Counter = Counter()
    for b, sign in sorted(fixture.items()):
        row = by_b.get(b)
        if row is None:
            stats["fixture_missing_pointcount"] += 1
            continue
        observed = lift_units(row, unit)
        expected = sign_to_lift(sign)
        stats[f"fixture_sign_{sign}_rows"] += 1
        stats[f"fixture_observed_lift_{observed}"] += 1
        if expected is None:
            stats["fixture_unknown_sign"] += 1
        elif observed != expected:
            stats["fixture_lift_sign_mismatch"] += 1
    return stats


def print_counter(prefix: str, stats: Counter | dict[str, Any]) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, fixture_by_field: dict[int, dict[int, str]], unit: int) -> None:
    point_stats, by_b = field_rows(q)
    point_b = set(by_b)
    fixture = fixture_by_field[q]
    fixture_b = set(fixture)
    d3, _d4, legal_stats = legal_b_maps(q)
    legal_b = set(d3)
    core_b = core_b_values(q)

    print(f"q={q}:")
    print_counter(
        "domain_sizes",
        {
            "pointcount_B": len(point_b),
            "fixture_B": len(fixture_b),
            "legal_b_maps_B": len(legal_b),
            "core_B": len(core_b),
            "fixture_equals_legal_b_maps": int(fixture_b == legal_b),
        },
    )
    print_counter(
        "domain_intersections",
        {
            "pointcount_cap_fixture": len(point_b & fixture_b),
            "fixture_minus_pointcount": len(fixture_b - point_b),
            "pointcount_minus_fixture": len(point_b - fixture_b),
            "pointcount_cap_core": len(point_b & core_b),
            "pointcount_minus_core": len(point_b - core_b),
            "core_minus_pointcount": len(core_b - point_b),
            "pointcount_core_minus_fixture": len((point_b & core_b) - fixture_b),
        },
    )
    print_counter("pointcount_setup_stats", point_stats)
    print_counter("legal_b_maps_setup_stats", legal_stats)
    for label, values in [
        ("pointcount_all", point_b),
        ("fixture", fixture_b),
        ("pointcount_minus_fixture", point_b - fixture_b),
        ("pointcount_not_core", point_b - core_b),
        ("pointcount_core_not_fixture", (point_b & core_b) - fixture_b),
    ]:
        print_counter(f"{label}_lift_hist", lift_hist(by_b, values, unit))
    print_counter("fixture_lift_sign_check", check_fixture_lifts(by_b, fixture, unit))
    extra_core = sorted((point_b & core_b) - fixture_b)
    print(f"pointcount_core_not_fixture_values = {extra_core}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--unit", type=int, default=16)
    args = parser.parse_args()

    fixture_by_field = load_fixture(args.fixture)
    print("p27 B-line reduced-domain reconciliation probe")
    print("question = does the reduced point-count B-domain match the frozen legal B-domain?")
    print(f"fixture = {args.fixture}")
    print(f"small_primes = {args.small_primes}")
    print(f"unit = {args.unit}")
    for q in parse_ints(args.small_primes):
        run_field(q, fixture_by_field, args.unit)
    print("p27_b_line_reduced_domain_reconcile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
