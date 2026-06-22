#!/usr/bin/env python3
"""Emit finite-field fixtures for the p27 B-line Kummer sequence.

The formula packet gives the source equations for the B-line cover.  This
packet gives the descended guard-field rows for the conditional sequence

    f3(B), f4(B), f5(B), ...

where f_j is the selected gate character on the B values that survived the
previous all-plus prefix.  These rows are the compact CAS/expert handoff for
class comparison: recover the normalized Kummer class for f3, then decide
whether f4/f5 are pullbacks, translates, coboundaries, iterates, or fresh
independent half-covers.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps
from p27_b_line_deep_descent_probe import collect_b_groups
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


def sign_label(sign: int) -> str:
    return "plus" if sign == 1 else "minus"


def counter_json(stats: Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(stats.items(), key=lambda item: str(item[0]))}


def legal_core_payload(q: int) -> tuple[dict[str, Any], Counter]:
    d3, _d4, source_stats = legal_b_maps(q)
    legal = set(d3)
    core = core_b_values(q)
    rows = [
        {"B": int(B), "sign": "legal" if B in legal else "not_legal"}
        for B in sorted(core)
    ]
    stats = Counter(source_stats)
    stats["core_B"] = len(core)
    stats["legal_B_in_core"] = len(legal & core)
    stats["legal_B_missing_core"] = len(legal - core)
    stats["core_B_without_legal"] = len(core - legal)
    return {
        "name": "legal_on_coreB",
        "domain": "core B bucket",
        "meaning": "which core B values are legal selected-source values",
        "row_count": len(rows),
        "legal_count": len(legal & core),
        "not_legal_count": len(core - legal),
        "rows": rows,
    }, stats


def conditional_gate_payloads(q: int, max_gate: int) -> tuple[list[dict[str, Any]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    groups, group_stats = collect_b_groups(candidates, q, max_gate)
    stats = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"group_{key}": value for key, value in group_stats.items()})

    payloads: list[dict[str, Any]] = []
    active = set(groups)
    for index, gate in enumerate(range(3, max_gate + 1)):
        rows: list[dict[str, Any]] = []
        next_active: set[int] = set()
        gate_stats: Counter = Counter()
        for B in sorted(active):
            bit = normalize(bits[index] for bits in groups[B])
            if bit in (-1, 1):
                rows.append({"B": int(B), "sign": sign_label(bit)})
                gate_stats[f"gate{gate}_{sign_label(bit)}"] += 1
                if bit == 1:
                    next_active.add(B)
            elif bit == 0:
                rows.append({"B": int(B), "sign": "mixed"})
                gate_stats[f"gate{gate}_mixed"] += 1
            else:
                rows.append({"B": int(B), "sign": "missing"})
                gate_stats[f"gate{gate}_missing"] += 1

        plus = gate_stats[f"gate{gate}_plus"]
        minus = gate_stats[f"gate{gate}_minus"]
        mixed = gate_stats[f"gate{gate}_mixed"]
        missing = gate_stats[f"gate{gate}_missing"]
        payloads.append(
            {
                "name": f"f{gate}_conditional",
                "gate": f"d{gate}",
                "domain": "legal B" if gate == 3 else f"all-plus prefix through d{gate - 1}",
                "meaning": f"selected gate d{gate} character on the active B domain",
                "row_count": len(rows),
                "plus_count": plus,
                "minus_count": minus,
                "mixed_count": mixed,
                "missing_count": missing,
                "rows": rows,
            }
        )
        active = next_active
    return payloads, stats


def field_payload(q: int, max_gate: int) -> dict[str, Any]:
    legal_payload, legal_stats = legal_core_payload(q)
    gate_payloads, gate_stats = conditional_gate_payloads(q, max_gate)
    return {
        "field": q,
        "base": {
            "core_B": legal_stats["core_B"],
            "legal_B": legal_stats["legal_B"],
            "legal_B_in_core": legal_stats["legal_B_in_core"],
            "legal_B_missing_core": legal_stats["legal_B_missing_core"],
        },
        "families": [legal_payload, *gate_payloads],
        "source_stats": {
            "legal_core": counter_json(legal_stats),
            "conditional_gates": counter_json(gate_stats),
        },
    }


def packet_json(fields: list[int], max_gate: int) -> dict[str, Any]:
    return {
        "name": "p27_b_line_kummer_fixture_packet",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "Compact guard-field fixtures for extracting and comparing the "
            "B-line Kummer sequence f3(B), f4(B), f5(B), ... after visible "
            "low-degree B supports and simple B recurrences were killed."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "source_coordinate": {
            "B": "8*X^2/(X^2 - 1)^2",
            "identity": "A + 2 = B^2",
            "branch_resultant": "16384*B^3*(B + 2)^2",
        },
        "fields": fields,
        "max_gate": max_gate,
        "fixtures": [field_payload(q, max_gate) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Recover normalized B-line class for f3",
                "compute": [
                    "branch divisor degree and support field degrees",
                    "normalization genus and component count",
                    "projection degree over P1_B",
                    "visible involutions or quotients after saturation",
                ],
                "promote_if": "stable low-genus/sourceable B-line class across guard fields",
                "kill_if": "high/generic f3 branch class with no quotient or source",
            },
            {
                "priority": 20,
                "name": "Compare conditional classes f4/f3 and f5/f4",
                "compute": [
                    "pullback/translate/coboundary/iterate relation among successive classes",
                    "whether a single source/correspondence controls multiple selected gates",
                    "first falsifier showing f4/f5 are fresh independent half-covers",
                ],
                "promote_if": "one extracted class or correspondence enforces multiple gates",
                "kill_if": "successive conditional classes are unrelated fresh Kummer covers",
            },
        ],
        "do_not_run": [
            "more B bucket scoring without a class or source law",
            "large GPU production from Bplus alone",
            "degree-one B recurrence restarts",
            "visible monic cubic/quartic scans already killed in q1847",
        ],
        "acceptance": {
            "promote": "low-genus/sourceable/recurrent B-line class improving source-normalized half-loss",
            "kill": "generic high-genus f3 plus independent fresh f4/f5 half-covers",
        },
        "sentinel": "p27_b_line_kummer_fixture_packet_rows=1/1",
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 B-line Kummer fixture packet")
    print()
    print("Purpose:")
    print("  Freeze the guard-field rows for conditional B-line classes")
    print("  f3(B), f4(B), f5(B), ... so CAS can compare actual Kummer")
    print("  classes instead of running another bucket scan.")
    print()
    print("Guard fields:")
    for fixture in packet["fixtures"]:
        base = fixture["base"]
        print(
            f"  q={fixture['field']}: core_B={base['core_B']} "
            f"legal_B={base['legal_B']} missing_core={base['legal_B_missing_core']}"
        )
        for family in fixture["families"]:
            if not family["name"].startswith("f"):
                continue
            print(
                "    "
                f"{family['name']}: rows={family['row_count']} "
                f"plus={family['plus_count']} minus={family['minus_count']} "
                f"mixed={family['mixed_count']} missing={family['missing_count']}"
            )
    print()
    print("CAS task:")
    print("  1. Recover the normalized B-line Kummer/divisor class for f3.")
    print("  2. Compute branch degree, support field degrees, genus, components, and quotients.")
    print("  3. Compare f4/f3 and f5/f4 as pullbacks/translates/coboundaries/iterates.")
    print("  4. Promote only a sourceable/recurrent class that controls multiple gates.")
    print("  5. Kill if f3 is generic and f4/f5 are fresh independent half-covers.")
    print()
    print("Fixture JSON:")
    print("  research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json")
    print()
    print(packet["sentinel"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--max-gate", type=int, default=6)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    fields = parse_ints(args.small_primes)
    packet = packet_json(fields, args.max_gate)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print_text(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
