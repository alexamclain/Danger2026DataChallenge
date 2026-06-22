#!/usr/bin/env python3
"""Emit reduced B-line d3 fiber fixtures for CAS normalization.

The B-line fiber invariant probe showed that every legal B in the p27-signature
guard fields has a reduced d3 fiber:

    32 root occurrences -> 8 distinct x roots -> 4 u=x+1/x roots,
    f3(B) = chi(u+2) on every u root.

This packet freezes those rows and polynomial coefficients so CAS can work on
the reduced 4-u / 8-x cover without reconstructing source candidates.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from p27_b_line_fiber_invariant_probe import (
    collect_b_fibers,
    inv,
    poly_roots_coeffs,
)
from p27_kline_reverse_z_relation_probe import parse_ints


DEFAULT_JSON = Path("research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json")


def sign_label(sign: int) -> str:
    if sign == 1:
        return "plus"
    if sign == -1:
        return "minus"
    return "mixed"


def field_fixture(q: int) -> dict[str, Any]:
    groups, signs, setup_stats = collect_b_fibers(q)
    rows = []
    stats: Counter = Counter(setup_stats)
    for B, roots in sorted(groups.items()):
        x_roots = sorted(set(roots))
        u_roots = sorted({(root + inv(root, q)) % q for root in x_roots if root})
        x_poly = poly_roots_coeffs(x_roots, q)
        u_poly = poly_roots_coeffs(u_roots, q)
        sign = signs[B]
        stats[f"sign_{sign_label(sign)}"] += 1
        stats[f"occurrence_roots_{len(roots)}"] += 1
        stats[f"x_roots_{len(x_roots)}"] += 1
        stats[f"u_roots_{len(u_roots)}"] += 1
        rows.append(
            {
                "B": int(B),
                "sign": sign_label(sign),
                "occurrence_root_count": len(roots),
                "x_roots": [int(root) for root in x_roots],
                "u_roots": [int(root) for root in u_roots],
                "x_poly_coeffs_ascending": [int(value) for value in x_poly],
                "u_poly_coeffs_ascending": [int(value) for value in u_poly],
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
        "name": "p27_b_line_reduced_fiber_fixture",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "CAS fixture for the reduced B-line d3 fiber: 8 distinct x roots "
            "or 4 u=x+1/x roots over each legal B."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "coordinates": {
            "B": "8*X^2/(X^2 - 1)^2",
            "x": "next selected x-coordinate after the legal d2 source",
            "u": "x + 1/x",
            "selector": "f3(B) = chi(x) = chi(u + 2) on every reduced-fiber root",
        },
        "fixtures": [field_fixture(q) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Normalize reduced u-cover",
                "compute": [
                    "function field for the 4-root u cover over legal B",
                    "genus and components",
                    "branch divisor degree and support field degrees",
                    "quotients or involutions beyond x -> 1/x",
                ],
                "promote_if": "low-genus/sourceable quotient or recurrence controlling f3 and later gates",
                "kill_if": "generic high-genus cover with no quotient or recurrence",
            },
            {
                "priority": 20,
                "name": "Compare f4 after reduced f3 cover",
                "compute": [
                    "pull back f4 to the reduced f3 cover",
                    "test whether f4/f3 is a coboundary, translate, iterate, or fresh cover",
                ],
                "promote_if": "one class/correspondence controls multiple selected gates",
                "kill_if": "f4 is a fresh independent half-cover on every useful quotient",
            },
        ],
        "acceptance": {
            "promote": "genus <= 1, explicit sampler/sourceable walk, or multi-gate recurrence",
            "kill": "high-genus/generic reduced cover and fresh f4/f5 classes",
        },
        "sentinel": "p27_b_line_reduced_fiber_fixture_rows=1/1",
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 B-line reduced fiber fixture packet")
    print()
    print("Purpose:")
    print("  Freeze the reduced d3 fiber over legal B for CAS normalization.")
    print("  Each row records 8 distinct x-roots, 4 u=x+1/x roots, and")
    print("  polynomial coefficients over the guard field.")
    print()
    for fixture in packet["fixtures"]:
        stats = fixture["stats"]
        print(
            f"q={fixture['field']}: rows={fixture['row_count']} "
            f"plus={stats.get('sign_plus', 0)} minus={stats.get('sign_minus', 0)} "
            f"occ32={stats.get('occurrence_roots_32', 0)} "
            f"x8={stats.get('x_roots_8', 0)} u4={stats.get('u_roots_4', 0)}"
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
