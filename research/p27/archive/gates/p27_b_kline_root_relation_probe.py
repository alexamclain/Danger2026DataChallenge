#!/usr/bin/env python3
"""Low-degree relation screen for the B/K signed-root selector.

The B/K bridge gives a two-sheet cover

    K^2 = (B - 2)^4 / (8*B*(B + 2)^2).

For each legal B target row, only one of the two K roots appears in the
signed-doubling K-line target packet.  This probe asks whether that selected
sheet has an additional low-degree plane relation in `(B,K)` beyond the full
two-sheet cover.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_kline_bridge_probe import b_to_l, sqrt_table
from p27_b_line_branch_support_probe import legal_b_maps
from p27_conic_pair_invariant_relation_probe import relation_stats_for_system
from p27_k_belyi_involution_probe import collect_rows, parse_ints


def selected_and_cover_rows(q: int, family: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]], Counter]:
    b_d3, b_d4, b_stats = legal_b_maps(q)
    k_d3_rows, k_d4_rows, _s_d3, _s_d4, k_stats = collect_rows(q)
    roots = sqrt_table(q)
    b_targets = b_d3 if family == "d3" else b_d4
    k_targets = {row.k: row.target for row in (k_d3_rows if family == "d3" else k_d4_rows)}
    stats: Counter = Counter()
    stats.update({f"B_{key}": value for key, value in b_stats.items()})
    stats.update({f"K_{key}": value for key, value in k_stats.items()})

    cover: list[tuple[int, int]] = []
    selected: list[tuple[int, int]] = []
    for B in sorted(b_targets):
        L = b_to_l(B, q)
        if L is None:
            stats["B_degenerate"] += 1
            continue
        ks = roots[L]
        stats[f"K_roots_{len(ks)}"] += 1
        for K in ks:
            cover.append((B, K))
            if K in k_targets:
                selected.append((B, K))
    stats["cover_rows"] = len(cover)
    stats["cover_unique"] = len(set(cover))
    stats["selected_rows"] = len(selected)
    stats["selected_unique"] = len(set(selected))
    return cover, selected, stats


def compare(label: str, q: int, cover: list[tuple[int, int]], selected: list[tuple[int, int]], degrees: list[int]) -> None:
    cover_stats = relation_stats_for_system(cover, q, degrees)
    selected_stats = relation_stats_for_system(selected, q, degrees)
    print(f"{label}:")
    print(f"  cover_rows = {len(cover)}")
    print(f"  cover_unique = {len(set(cover))}")
    print(f"  selected_rows = {len(selected)}")
    print(f"  selected_unique = {len(set(selected))}")
    for degree in degrees:
        prefix = f"deg{degree}"
        ce = cover_stats[f"{prefix}_extra_nullity"]
        se = selected_stats[f"{prefix}_extra_nullity"]
        print(
            "  "
            f"{prefix}: cover_rank={cover_stats[f'{prefix}_rank']} "
            f"cover_extra={ce} "
            f"selected_rank={selected_stats[f'{prefix}_rank']} "
            f"selected_extra={se} "
            f"selected_minus_cover_extra={se - ce}"
        )


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847,2087")
    parser.add_argument("--families", default="d3,d4")
    parser.add_argument("--degrees", default="2,4,6,8,10,12")
    args = parser.parse_args()

    degrees = parse_ints(args.degrees)
    families = [part.strip() for part in args.families.split(",") if part.strip()]
    print("p27 B/K signed-root relation probe")
    print("cover = K^2 - (B-2)^4/(8*B*(B+2)^2)")
    print(f"degrees = {degrees}")
    for q in parse_ints(args.small_primes):
        for family in families:
            cover, selected, stats = selected_and_cover_rows(q, family)
            print_counter(f"q{q}_{family}_setup", stats)
            compare(f"q{q}_{family}_B_K", q, cover, selected, degrees)
    print("p27_b_kline_root_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
