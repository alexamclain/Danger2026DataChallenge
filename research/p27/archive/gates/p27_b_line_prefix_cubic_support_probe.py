#!/usr/bin/env python3
"""Exact cubic support for B-line all-plus prefixes.

Earlier screens killed visible low-degree support for the legal B-domain,
d3(B), and unstable d4(B) local fits.  A different beat-sqrt possibility is
that a *combined* all-plus prefix, such as d3=d4=+1, has a single low-genus
source even though the individual characters look generic.

This probe tests whether the prefix subset inside legal B is the squareclass
of a monic cubic

    B^3 + aB^2 + bB + c

over p27-signature finite fields.  A positive for gate4 would be a genus-1
source candidate that enforces two selected gates at once.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_line_cubic_support_probe import exact_monic_cubic_search, print_counter
from p27_b_line_deep_descent_probe import collect_b_groups
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


def b_prefix_rows(q: int, max_gate: int) -> tuple[dict[int, list[tuple[int, int]]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    groups, group_stats = collect_b_groups(candidates, q, max_gate)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"group_{key}": value for key, value in group_stats.items()})

    rows_by_gate: dict[int, list[tuple[int, int]]] = {}
    for gate in range(3, max_gate + 1):
        rows: list[tuple[int, int]] = []
        plus = 0
        minus = 0
        mixed = 0
        missing = 0
        for B, bit_tuples in sorted(groups.items()):
            active = True
            for index in range(gate - 2):
                bit = normalize(bits[index] for bits in bit_tuples)
                if bit == 1:
                    continue
                active = False
                if bit == -1:
                    minus += 1
                elif bit == 0:
                    mixed += 1
                else:
                    missing += 1
                break
            if active:
                plus += 1
            rows.append((B, 0 if active else 1))
        stats[f"gate{gate}_prefix_plus_B"] = plus
        stats[f"gate{gate}_prefix_notplus_B"] = len(rows) - plus
        stats[f"gate{gate}_first_stop_minus_B"] = minus
        stats[f"gate{gate}_first_stop_mixed_B"] = mixed
        stats[f"gate{gate}_first_stop_missing_B"] = missing
        rows_by_gate[gate] = rows
    return rows_by_gate, stats


def run_field(q: int, max_gate: int, sample_limit: int) -> None:
    rows_by_gate, stats = b_prefix_rows(q, max_gate)
    print_counter(f"q{q}_b_line_prefix_source_stats", stats)
    for gate in range(3, max_gate + 1):
        rows = rows_by_gate[gate]
        search_stats, hits = exact_monic_cubic_search(q, rows, sample_limit)
        print_counter(f"q{q}_gate{gate}_prefix_monic_cubic_support_stats", search_stats)
        print(f"q{q}_gate{gate}_prefix_monic_cubic_support_samples:")
        for hit in hits[:sample_limit]:
            a, b, c = hit.coeffs
            print(f"  polarity={hit.polarity} cubic=B^3+{a}*B^2+{b}*B+{c}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--max-gate", type=int, default=5)
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line all-plus prefix cubic support probe")
    print("target = legal B subset with d3..d_gate all plus")
    print("family = chi(B^3+aB^2+bB+c), global polarity allowed")
    print(f"small_primes = {args.small_primes}")
    print(f"max_gate = {args.max_gate}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.max_gate, args.sample_limit)
    print("p27_b_line_prefix_cubic_support_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
