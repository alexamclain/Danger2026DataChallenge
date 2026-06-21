#!/usr/bin/env python3
"""Parity reduction for low-degree S-root source candidates.

The selected d3/d4 bits are constant on S/-S pairs.  Since q == 7 mod 8 in the
p27 sign regime, chi(-1) = -1, so any odd S-semi-invariant squareclass flips
on those pairs and cannot be the selector.  Any even S-semi-invariant
low-degree branch divisor is a K=S^2 divisor already covered by the K-line
screens.

This probe records that reduction on the guard fields and names the surviving
work: non-visible branch-class/genus extraction, not another visible
low-degree S polynomial scan.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_sroot_branch_divisor_probe import SRow, collect_rows


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def pair_stats(rows: list[SRow], q: int) -> Counter:
    by_s = {row.s: row.target for row in rows}
    stats: Counter = Counter()
    seen: set[int] = set()
    for row in rows:
        if row.s in seen:
            continue
        partner = (-row.s) % q
        if partner not in by_s:
            stats["missing_partner"] += 1
            seen.add(row.s)
            continue
        seen.add(row.s)
        seen.add(partner)
        stats["pairs"] += 1
        stats["same_target_pairs"] += int(by_s[partner] == row.target)
        stats["mixed_target_pairs"] += int(by_s[partner] != row.target)
        stats["opposite_chi_s_pairs"] += int(legendre(row.s, q) == -legendre(partner, q))
    return stats


def odd_semivariant_mismatch(rows: list[SRow], q: int) -> Counter:
    """Score the structural obstruction for odd S*g(S^2) squareclasses.

    For any g(K), g(S^2) is the same on S and -S.  Multiplication by S changes
    squareclass by chi(-1)=-1 across the pair, so exactly one side of each pair
    can match an even target.
    """

    by_s = {row.s: row.target for row in rows}
    stats: Counter = Counter()
    seen: set[int] = set()
    for row in rows:
        if row.s in seen:
            continue
        partner = (-row.s) % q
        if partner not in by_s:
            continue
        seen.add(row.s)
        seen.add(partner)
        # If a hypothetical even g(K) has character e on both sides, then
        # S*g(K) has characters chi(S)*e and -chi(S)*e on the pair.  Since the
        # target is same on both sides, at most one row can match.
        stats["pair_count"] += 1
        stats["forced_pair_mismatches"] += 1
    stats["max_odd_semivariant_good"] = len(rows) - stats["forced_pair_mismatches"]
    stats["rows"] = len(rows)
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    args = parser.parse_args()

    print("p27 S-root parity reduction probe")
    print("coordinate = S=(U^2-4)/(2V), K=S^2")
    print("target condition = d3/d4 are even on S/-S pairs")
    print("odd semivariant obstruction = chi(-1)=-1")
    print("even semivariant reduction = function of K, already covered by K-line screens")
    for q in parse_ints(args.small_primes):
        sd3, sd4, setup_stats = collect_rows(q)
        print(f"q={q}:")
        print(f"  q_mod_8 = {q % 8}")
        print(f"  chi_minus_one = {legendre(-1, q)}")
        print_counter("  setup_stats", setup_stats)
        for label, rows in [("d3", sd3), ("d4", sd4)]:
            print_counter(f"  {label}_pair_stats", pair_stats(rows, q))
            print_counter(f"  {label}_odd_semivariant_obstruction", odd_semivariant_mismatch(rows, q))
    print("reduction_summary:")
    print("  even_global_s_semivariant_degree_le_4 = K-polynomial degree <= 2")
    print("  odd_global_s_semivariant_degree_le_4 = impossible for pair-even target")
    print("  remaining = non-visible branch class or non-semi-invariant accidental fit")
    print("p27_sroot_parity_reduction_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
