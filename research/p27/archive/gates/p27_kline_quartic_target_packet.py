#!/usr/bin/env python3
"""Emit machine-readable targets for the K-line quartic screen.

This freezes the signed-doubling Kummer-line rows

    K = x([2]P) on E': V^2 = U^3 + 4U

for exact monic quartic support tests.  The goal is a bounded GPU/CAS screen
for a genus-1 source candidate, not another visible-factor fit.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from p27_k_belyi_involution_probe import collect_rows, parse_ints


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


def k_rows(q: int, family: str) -> tuple[list[dict[str, int]], Counter]:
    kd3, kd4, _sd3, _sd4, stats = collect_rows(q)
    if family == "d3_on_K":
        rows = [{"K": row.k, "sign": row.target} for row in kd3]
    elif family == "d4_on_K_after_d3":
        rows = [{"K": row.k, "sign": row.target} for row in kd4]
    else:
        raise ValueError(f"unknown family {family!r}")
    return rows, Counter(stats)


def family_payload(q: int, family: str) -> dict[str, Any]:
    rows, source_stats = k_rows(q, family)
    counts = sign_counts(rows)
    return {
        "field": q,
        "family": family,
        "coordinate": "K",
        "sign_convention": "+1 means target/square side; -1 means complement",
        "row_count": counts["rows"],
        "plus_count": counts["plus"],
        "minus_count": counts["minus"],
        "source_stats": dict(sorted(source_stats.items())),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--families", default="d3_on_K,d4_on_K_after_d3")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    families = [part.strip() for part in args.families.split(",") if part.strip()]
    fields = parse_ints(args.small_primes)
    packet = {
        "name": "p27_kline_quartic_targets",
        "purpose": "Exact finite-field K rows for monic quartic support screen",
        "quartic_family": "chi(K^4+aK^3+bK^2+cK+d), global polarity allowed",
        "zero_policy": "exclude quartics that vanish on any listed K row",
        "fields": fields,
        "families": families,
        "targets": [
            family_payload(q, family)
            for q in fields
            for family in families
        ],
        "sentinel": "p27_kline_quartic_target_packet_rows=1/1",
    }
    print(json.dumps(packet, indent=args.indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
