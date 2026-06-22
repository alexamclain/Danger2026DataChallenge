#!/usr/bin/env python3
"""Emit machine-readable targets for the B-line quartic GPU screen.

The quartic screen is meant to be run outside the Python research harness,
probably on GPU.  This packet freezes the finite-field B rows and target signs
so an implementation can test the exact same rows without reconstructing the
label-2 source pipeline.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps
from p27_b_line_prefix_cubic_support_probe import b_prefix_rows
from p27_kline_reverse_z_relation_probe import parse_ints


def sign_counts(rows: list[dict[str, int]]) -> Counter:
    stats: Counter = Counter()
    for row in rows:
        stats["rows"] += 1
        if row["sign"] == 1:
            stats["plus"] += 1
        elif row["sign"] == -1:
            stats["minus"] += 1
        else:
            stats["other"] += 1
    return stats


def d3_rows(q: int) -> tuple[list[dict[str, int]], Counter]:
    d3, _d4, stats = legal_b_maps(q)
    rows = [{"B": B, "sign": value} for B, value in sorted(d3.items())]
    return rows, Counter(stats)


def gate_prefix_rows(q: int, gate: int) -> tuple[list[dict[str, int]], Counter]:
    rows_by_gate, stats = b_prefix_rows(q, gate)
    rows = [
        {"B": B, "sign": 1 if bit == 0 else -1}
        for B, bit in rows_by_gate[gate]
    ]
    return rows, Counter(stats)


def legal_core_rows(q: int) -> tuple[list[dict[str, int]], Counter]:
    d3, _d4, stats = legal_b_maps(q)
    legal = set(d3)
    core = core_b_values(q)
    rows = [
        {"B": B, "sign": 1 if B in legal else -1}
        for B in sorted(core)
    ]
    out_stats = Counter(stats)
    out_stats["core_B"] = len(core)
    out_stats["legal_B_in_core"] = len(legal & core)
    out_stats["legal_B_missing_core"] = len(legal - core)
    return rows, out_stats


def family_payload(q: int, family: str) -> dict[str, Any]:
    if family == "d3_on_legalB":
        rows, source_stats = d3_rows(q)
    elif family == "gate4_prefix_on_legalB":
        rows, source_stats = gate_prefix_rows(q, 4)
    elif family == "legal_on_coreB":
        rows, source_stats = legal_core_rows(q)
    else:
        raise ValueError(f"unknown family {family!r}")

    counts = sign_counts(rows)
    return {
        "field": q,
        "family": family,
        "sign_convention": "+1 means target/square side; -1 means complement",
        "row_count": counts["rows"],
        "plus_count": counts["plus"],
        "minus_count": counts["minus"],
        "source_stats": dict(sorted(source_stats.items())),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument(
        "--families",
        default="d3_on_legalB,gate4_prefix_on_legalB,legal_on_coreB",
    )
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    families = [part.strip() for part in args.families.split(",") if part.strip()]
    packet = {
        "name": "p27_b_line_quartic_targets",
        "purpose": "Exact finite-field B rows for monic quartic GPU support screen",
        "quartic_family": "chi(B^4+aB^3+bB^2+cB+d), global polarity allowed",
        "zero_policy": "exclude quartics that vanish on any listed B row",
        "fields": parse_ints(args.small_primes),
        "families": families,
        "targets": [
            family_payload(q, family)
            for q in parse_ints(args.small_primes)
            for family in families
        ],
        "sentinel": "p27_b_line_quartic_target_packet_rows=1/1",
    }
    print(json.dumps(packet, indent=args.indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
