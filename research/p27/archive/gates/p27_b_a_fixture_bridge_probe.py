#!/usr/bin/env python3
"""Bridge the frozen B-line and A-level Kummer fixture packets.

The B-line packet records conditional classes f3(B), f4(B), ...
The A-level packet records d3(A), d4(A), ... after the selected tower has
descended to A-fibers.  This probe checks whether those frozen fixtures are
literally the same rows through

    A = B^2 - 2.

If they match row-by-row with signs, the A-level CAS task should be folded
into the B/K/Sroot normalized-class task instead of treated as independent.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any


DEFAULT_A_PACKET = Path("research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json")
DEFAULT_B_PACKET = Path("research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json")


def load_packet(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def fixture_by_field(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(fixture["field"]): fixture for fixture in packet["fixtures"]}


def a_gate_map(fixture: dict[str, Any]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for gate in fixture["gates"]:
        name = str(gate["gate"])
        if not name.startswith("d"):
            continue
        out[int(name[1:])] = gate
    return out


def b_family_map(fixture: dict[str, Any]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for family in fixture["families"]:
        name = str(family["name"])
        if not (name.startswith("f") and name.endswith("_conditional")):
            continue
        gate = int(name.removeprefix("f").removesuffix("_conditional"))
        out[gate] = family
    return out


def signed_rows(rows: list[dict[str, Any]], key: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for row in rows:
        value = int(row[key])
        sign = str(row["sign"])
        if sign not in {"plus", "minus"}:
            continue
        if value in out and out[value] != sign:
            raise ValueError(f"mixed sign for {key}={value}: {out[value]} vs {sign}")
        out[value] = sign
    return out


def compare_gate(q: int, gate: int, a_gate: dict[str, Any], b_family: dict[str, Any]) -> Counter:
    stats: Counter = Counter()
    a_rows = signed_rows(a_gate["rows"], "A")
    b_rows = signed_rows(b_family["rows"], "B")
    preimages: defaultdict[int, list[tuple[int, str]]] = defaultdict(list)

    stats["A_rows"] = len(a_rows)
    stats["B_rows"] = len(b_rows)

    for B, b_sign in sorted(b_rows.items()):
        stats["B_checked"] += 1
        A = (B * B - 2) % q
        preimages[A].append((B, b_sign))
        a_sign = a_rows.get(A)
        if a_sign is None:
            stats["B_to_A_missing"] += 1
        elif a_sign == b_sign:
            stats["B_to_A_sign_match"] += 1
        else:
            stats["B_to_A_sign_mismatch"] += 1

    for A, a_sign in sorted(a_rows.items()):
        rows = preimages.get(A, [])
        stats[f"A_preimages_{len(rows)}"] += 1
        if not rows:
            stats["A_uncovered"] += 1
            continue
        if len(rows) > 1:
            stats["A_collision_values"] += 1
            if len({sign for _B, sign in rows}) > 1:
                stats["A_collision_mixed_signs"] += 1
        if any(sign == a_sign for _B, sign in rows):
            stats["A_has_matching_B_sign"] += 1
        else:
            stats["A_no_matching_B_sign"] += 1

    if (
        stats["A_rows"] == stats["B_rows"]
        and stats["B_to_A_missing"] == 0
        and stats["B_to_A_sign_mismatch"] == 0
        and stats["A_uncovered"] == 0
        and stats["A_collision_values"] == 0
    ):
        stats["exact_signed_bijection"] = 1
    else:
        stats["exact_signed_bijection"] = 0

    stats[f"gate{gate}_rows"] = stats["B_rows"]
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a-packet", type=Path, default=DEFAULT_A_PACKET)
    parser.add_argument("--b-packet", type=Path, default=DEFAULT_B_PACKET)
    args = parser.parse_args()

    a_packet = load_packet(args.a_packet)
    b_packet = load_packet(args.b_packet)
    a_fields = fixture_by_field(a_packet)
    b_fields = fixture_by_field(b_packet)
    fields = sorted(set(a_fields) & set(b_fields))

    print("p27 B/A fixture bridge probe")
    print("relation = A - (B^2 - 2)")
    print(f"fields = {fields}")

    total: Counter = Counter()
    for q in fields:
        a_gates = a_gate_map(a_fields[q])
        b_families = b_family_map(b_fields[q])
        gates = sorted(set(a_gates) & set(b_families))
        print(f"q={q}:")
        print(f"  gates = {gates}")
        for gate in gates:
            stats = compare_gate(q, gate, a_gates[gate], b_families[gate])
            print_counter(f"  gate{gate}_bridge", stats)
            total.update({f"{key}": value for key, value in stats.items()})

    print_counter("total_bridge", total)
    print("p27_b_a_fixture_bridge_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
