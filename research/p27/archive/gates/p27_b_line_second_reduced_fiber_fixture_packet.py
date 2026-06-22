#!/usr/bin/env python3
"""Emit CAS fixtures for the second reduced B-line fiber.

This freezes the f4-over-f3-plus reduced fiber:

    x7 roots, v = x7 + 1/x7 roots, and v-polynomial coefficients

for each legal B row with d3=+1.  It is the f4/f3 analogue of
p27_b_line_reduced_fiber_fixture_packet.py.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from p27_b_line_fiber_invariant_probe import inv, poly_roots_coeffs
from p27_b_line_second_reduced_fiber_probe import collect_second_fibers
from p27_kline_reverse_z_relation_probe import parse_ints


DEFAULT_JSON = Path("research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json")


def sign_label(sign: int) -> str:
    if sign == 1:
        return "plus"
    if sign == -1:
        return "minus"
    return "mixed"


def field_fixture(q: int) -> dict[str, Any]:
    groups, signs, setup_stats = collect_second_fibers(q)
    rows = []
    stats: Counter = Counter(setup_stats)
    for B in sorted(signs):
        roots = groups[B]
        x_roots = sorted(set(roots))
        v_roots = sorted({(root + inv(root, q)) % q for root in x_roots if root})
        x_poly = poly_roots_coeffs(x_roots, q)
        v_poly = poly_roots_coeffs(v_roots, q)
        sign = signs[B]
        stats[f"sign_{sign_label(sign)}"] += 1
        stats[f"occurrence_roots_{len(roots)}"] += 1
        stats[f"x_roots_{len(x_roots)}"] += 1
        stats[f"v_roots_{len(v_roots)}"] += 1
        rows.append(
            {
                "B": int(B),
                "sign": sign_label(sign),
                "occurrence_root_count": len(roots),
                "x7_roots": [int(root) for root in x_roots],
                "v_roots": [int(root) for root in v_roots],
                "x7_poly_coeffs_ascending": [int(value) for value in x_poly],
                "v_poly_coeffs_ascending": [int(value) for value in v_poly],
            }
        )
    return {
        "field": q,
        "row_count": len(rows),
        "stats": {str(key): int(value) for key, value in sorted(stats.items(), key=lambda item: str(item[0]))},
        "rows": rows,
    }


def packet_json(fields: list[int]) -> dict[str, Any]:
    return {
        "name": "p27_b_line_second_reduced_fiber_fixture",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "CAS fixture for f4 over the f3-plus B-line domain: 16 distinct "
            "x7 roots or 8 v=x7+1/x7 roots over each active B."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "coordinates": {
            "B": "8*X^2/(X^2 - 1)^2",
            "x7": "next selected x-coordinate after imposing f3=+1",
            "v": "x7 + 1/x7",
            "selector": "f4(B) = chi(x7) = chi(v + 2) on every second-fiber root",
        },
        "fixtures": [field_fixture(q) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Normalize f4 over f3-plus cover",
                "compute": [
                    "function field for the 8-root v cover over the f3-plus B domain",
                    "genus and components",
                    "branch divisor degree and support field degrees",
                    "quotients or relations to the first reduced f3 cover",
                ],
                "promote_if": "f4 is a pullback, translate, coboundary, iterate, or low-genus quotient of f3",
                "kill_if": "f4 is a fresh high-genus/generic independent half-cover",
            }
        ],
        "sentinel": "p27_b_line_second_reduced_fiber_fixture_rows=1/1",
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 B-line second reduced fiber fixture packet")
    print()
    print("Purpose:")
    print("  Freeze the f4-over-f3-plus reduced fiber for CAS class comparison.")
    print("  Each row records 16 distinct x7 roots, 8 v=x7+1/x7 roots,")
    print("  polynomial coefficients, and the descended f4 sign.")
    print()
    for fixture in packet["fixtures"]:
        stats = fixture["stats"]
        print(
            f"q={fixture['field']}: rows={fixture['row_count']} "
            f"plus={stats.get('sign_plus', 0)} minus={stats.get('sign_minus', 0)} "
            f"occ64={stats.get('occurrence_roots_64', 0)} "
            f"x16={stats.get('x_roots_16', 0)} v8={stats.get('v_roots_8', 0)}"
        )
    print()
    print("JSON fixture:")
    print(f"  {DEFAULT_JSON}")
    print()
    print(packet["sentinel"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    packet = packet_json(parse_ints(args.small_primes))
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print_text(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
