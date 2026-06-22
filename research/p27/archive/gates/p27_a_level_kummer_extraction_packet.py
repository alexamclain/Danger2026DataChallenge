#!/usr/bin/env python3
"""Emit the p27 A-level Kummer extraction packet.

The selected tower descends to A-fibers, while visible degree <=4 branch
support on P1_A is killed.  This packet gives CAS code concrete finite-field
fixtures for extracting the actual A-line Kummer/divisor classes.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import target_rows


def row_label(bit: int) -> str:
    return "plus" if bit == 0 else "minus"


def gate_fixture(ax_points: set[tuple[int, int]], q: int, gate: int, depth: int) -> dict[str, Any]:
    rows, stats = target_rows(ax_points, q, gate, depth)
    return {
        "gate": f"d{gate}",
        "row_count": len(rows),
        "plus_count": stats["plus_A"],
        "minus_count": stats["minus_A"],
        "mixed_A_groups": stats["mixed_A_groups"],
        "mixed_A_rows": stats["mixed_A_rows"],
        "rows": [{"A": A, "sign": row_label(bit)} for A, bit in rows],
    }


def field_fixture(q: int, depth: int, min_rows: int) -> dict[str, Any]:
    ax_points, base_stats = collect_field_ax(q)
    gates = []
    for gate in range(3, depth + 3):
        fixture = gate_fixture(ax_points, q, gate, depth)
        if fixture["row_count"] >= min_rows or gate <= 4:
            gates.append(fixture)
    return {
        "field": q,
        "base": {
            "unique_A": base_stats["unique_A"],
            "unique_ax": base_stats["unique_ax"],
            "enum_no_label2_candidate": base_stats["enum_no_label2_candidate"],
            "enum_compact_not_target": base_stats["enum_compact_not_target"],
        },
        "gates": gates,
    }


def packet_json(fields: list[int], depth: int, min_rows: int) -> dict[str, Any]:
    return {
        "name": "p27_a_level_kummer_extraction_packet",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "Finite-field fixtures and CAS acceptance criteria for extracting "
            "the normalized A-line Kummer/divisor classes behind selected "
            "gates d3..d10."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "source_coordinate": {
            "A": "Montgomery A parameter after legal label-2/compactD source",
            "fact": "selected gates descend to whole A-fibers in p27 samples",
            "negative": "visible degree <=4 branch support on P1_A is killed for d3 in q1607/q1847/q2087",
        },
        "fixtures": [field_fixture(q, depth, min_rows) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Recover normalized A-cover for d3",
                "compute": [
                    "A-line function field or correspondence carrying the d3 character",
                    "branch divisor degree and support field degrees",
                    "normalization genus and component count",
                    "whether d3 is sourceable despite no visible degree <=4 support",
                ],
                "promote_if": "stable low-genus/sourceable class or named correspondence across guard fields",
                "kill_if": "high/generic branch degree with no quotient or recurrence",
            },
            {
                "priority": 20,
                "name": "Compare successive A-line classes",
                "compute": [
                    "d4 class on d3-plus prefix",
                    "d5/d6 classes when enough guard-field rows exist",
                    "pullback/translate/coboundary/iterate relation among successive classes",
                    "first p27-relevant recurrence candidate for d3..d10",
                ],
                "promote_if": "one class/correspondence controls multiple selected gates",
                "kill_if": "successive characters are independent fresh half-covers",
            },
        ],
        "do_not_run": [
            "blind low-degree A polynomial scans",
            "visible degree <=4 branch support without a new divisor reason",
            "GPU A-bucket production before a source law exists",
        ],
        "acceptance": {
            "promote": "low-genus/sourceable/recurrent A-line class that improves source-normalized half-loss",
            "kill": "independent fresh half-covers for d3..d10 on the normalized A-level object",
        },
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 A-level Kummer extraction packet")
    print()
    print("Purpose:")
    print("  Extract the actual A-line Kummer/divisor classes for selected gates.")
    print("  The A-prefix descent is real, but visible degree <=4 branch support")
    print("  is killed; this packet is for normalized-cover/class extraction.")
    print()
    print("Guard fields:")
    for field in packet["fixtures"]:
        base = field["base"]
        print(
            f"  q={field['field']}: "
            f"unique_A={base['unique_A']} unique_ax={base['unique_ax']}"
        )
        for gate in field["gates"]:
            if gate["row_count"] == 0:
                continue
            print(
                "    "
                f"{gate['gate']}: rows={gate['row_count']} "
                f"plus={gate['plus_count']} minus={gate['minus_count']} "
                f"mixed={gate['mixed_A_groups']}"
            )
    print()
    print("Known kills:")
    print("  - d3 has no visible degree <=4 A-line branch support in q1607/q1847/q2087")
    print("  - q1847 d4 also has no visible degree <=4 A-line branch support")
    print("  - nearby 7 mod 8 fields reject split degree <=4 support for d3")
    print("  - A-prefix counts remain geometric in p27 train/heldout")
    print()
    print("CAS task:")
    print("  1. Recover the normalized A-cover carrying d3.")
    print("  2. Compute branch divisor degree, support field degrees, genus, and components.")
    print("  3. Compare d4/d5/d6 classes as pullbacks/translates/coboundaries/iterates.")
    print("  4. Promote only a low-genus/sourceable class or recurrence controlling multiple gates.")
    print("  5. Kill if d3..d10 are independent fresh half-covers.")
    print()
    print("Fixture JSON:")
    print("  research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json")
    print()
    print("p27_a_level_kummer_extraction_packet_rows=1/1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    fields = parse_ints(args.small_primes)
    packet = packet_json(fields, args.depth, args.min_rows)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print_text(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
