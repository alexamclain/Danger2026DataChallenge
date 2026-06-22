#!/usr/bin/env python3
"""Combined A-line prefix support screen for the p27 selected tower.

The individual A-line gate screen asks whether a selected bit has a visible
low-degree character:

    d_j(A) = chi(f_j(A)).

This probe asks the sharper source-shrink question: can a single low-degree
A-line character select an all-plus multi-gate prefix such as d3&d4 or
d3&d4&d5 in one shot?  A positive result would fuse several independent
half-losses into one source condition; a negative result keeps the live route
on normalized Kummer/divisor-class extraction rather than GPU buckets.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import add_significance, print_counter, verdict
from p27_a_projection_prefix_profile_probe import auto_primes
from p27_b_line_branch_support_probe import (
    exact_linear_factor_search,
    irreducible_quadratic_pair_search,
    irreducible_quadratic_plus_linear_search,
)
from p27_legal_conic_tower_depth_probe import selected_gate_bits


def parse_set(raw: str) -> set[int]:
    return {int(part) for part in raw.split(",") if part.strip()}


def prefix_class(bits: list[int | None], prefix_depth: int) -> int | None:
    """Classify an all-plus prefix.

    Return convention:
      1  = all selected bits through prefix_depth are +1
     -1  = a selected bit fails before the prefix is complete
    None = a non-PM1/mixed/unknown bit appears before any decisive failure
    """

    for bit in bits[:prefix_depth]:
        if bit == 1:
            continue
        if bit == -1:
            return -1
        return None
    return 1


def prefix_rows(
    ax_points: set[tuple[int, int]],
    p: int,
    selected_depth: int,
    prefix_depth: int,
) -> tuple[list[tuple[int, int]], Counter]:
    """Return A rows for an all-plus selected prefix.

    Row bit convention follows the branch-support probes:
      0 = prefix passes
      1 = prefix fails
    """

    bits_by_ax = {
        (A, x): selected_gate_bits(A, x, p, selected_depth)
        for A, x in sorted(ax_points)
    }
    groups: defaultdict[int, Counter] = defaultdict(Counter)
    stats: Counter = Counter()
    for (A, _x), bits in bits_by_ax.items():
        cls = prefix_class(bits, prefix_depth)
        if cls is None:
            stats["bad_or_mixed_bit_rows"] += 1
            continue
        groups[A][cls] += 1
        groups[A]["rows"] += 1

    rows: list[tuple[int, int]] = []
    for A, counter in sorted(groups.items()):
        if counter[1] and counter[-1]:
            stats["mixed_A_groups"] += 1
            stats["mixed_A_rows"] += counter["rows"]
            continue
        if counter[1]:
            rows.append((A, 0))
            stats["prefix_plus_A"] += 1
        elif counter[-1]:
            rows.append((A, 1))
            stats["prefix_fail_A"] += 1

    stats["prefix_depth"] = prefix_depth
    stats["last_gate_d"] = prefix_depth + 2
    stats["groups"] = len(groups)
    stats["rows"] = len(rows)
    stats["domain_points"] = len(ax_points)
    stats["domain_A"] = len({A for A, _x in ax_points})
    return rows, stats


def screen_prefix(
    q: int,
    rows: list[tuple[int, int]],
    row_stats: Counter,
    min_rows: int,
    max_weight: int,
    quadratic: bool,
) -> None:
    prefix_depth = row_stats["prefix_depth"]
    label = f"q{q}_prefix{prefix_depth}_through_d{prefix_depth + 2}"
    add_significance(row_stats, q, len(rows), max_weight)
    print_counter(f"{label}_target_stats", row_stats)

    if len(rows) < min_rows:
        print(f"{label}_split_support_result: skipped_rows_lt_{min_rows}")
        return
    if row_stats["prefix_plus_A"] == 0 or row_stats["prefix_fail_A"] == 0:
        print(f"{label}_split_support_result: skipped_one_sided")
        return

    split_stats, split_solution = exact_linear_factor_search(q, rows, max_weight)
    print_counter(f"{label}_split_support_stats", split_stats)
    if split_solution is None:
        print(f"{label}_split_support_result: none_weight_le_{max_weight}")
    else:
        weight, factors, polarity = split_solution
        print(
            f"{label}_split_support_result: "
            f"weight={weight} polarity={polarity} factors={','.join(str(f) for f in factors)} "
            f"significance={verdict(row_stats['split_expected_exact_x1e12'] / 1_000_000_000_000)}"
        )

    if not quadratic:
        return

    quad_stats, quad_solution = irreducible_quadratic_plus_linear_search(q, rows, 2)
    print_counter(f"{label}_quad_plus_linear_stats", quad_stats)
    if quad_solution is None:
        print(f"{label}_quad_plus_linear_result: none_quad_plus_le_2_linear")
    else:
        u, v, factors, polarity = quad_solution
        print(
            f"{label}_quad_plus_linear_result: "
            f"quadratic=A^2+{u}A+{v} polarity={polarity} "
            f"linear_factors={','.join(str(f) for f in factors) if factors else 'none'}"
        )

    pair_stats, pair_solution = irreducible_quadratic_pair_search(q, rows)
    print_counter(f"{label}_two_quadratic_stats", pair_stats)
    if pair_solution is None:
        print(f"{label}_two_quadratic_result: none_two_irreducible_quadratics")
    else:
        q0, q1, polarity = pair_solution
        q1_label = "single" if q1 == (-1, -1) else f"A^2+{q1[0]}A+{q1[1]}"
        print(
            f"{label}_two_quadratic_result: "
            f"polarity={polarity} quadratic0=A^2+{q0[0]}A+{q0[1]} quadratic1={q1_label}"
        )


def run_field(
    q: int,
    selected_depth: int,
    prefix_depths: list[int],
    min_rows: int,
    max_weight: int,
    quadratic_prefixes: set[int],
) -> None:
    ax_points, base_stats = collect_field_ax(q)
    base_stats["sqrt_q_floor"] = math.isqrt(q)
    print_counter(f"q{q}_base", base_stats)

    for prefix_depth in prefix_depths:
        if prefix_depth > selected_depth:
            print(f"q{q}_prefix{prefix_depth}: skipped_gt_selected_depth")
            continue
        rows, row_stats = prefix_rows(ax_points, q, selected_depth, prefix_depth)
        screen_prefix(
            q=q,
            rows=rows,
            row_stats=row_stats,
            min_rows=min_rows,
            max_weight=max_weight,
            quadratic=prefix_depth in quadratic_prefixes,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--auto-start", type=int, default=0)
    parser.add_argument("--auto-count", type=int, default=0)
    parser.add_argument("--selected-depth", type=int, default=6)
    parser.add_argument("--prefix-depths", default="2,3,4")
    parser.add_argument("--min-rows", type=int, default=40)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--quadratic-prefixes", default="2,3")
    args = parser.parse_args()

    primes = parse_ints(args.small_primes)
    if args.auto_count:
        primes.extend(auto_primes(args.auto_start, args.auto_count))
    prefix_depths = parse_ints(args.prefix_depths)
    quadratic_prefixes = parse_set(args.quadratic_prefixes)

    print("p27 A-line combined prefix support probe")
    print("screen = all-plus selected prefix as chi(low-degree branch support on P1_A)")
    print(f"selected_depth = {args.selected_depth}")
    print(f"prefix_depths = {','.join(str(depth) for depth in prefix_depths)}")
    print(f"min_rows = {args.min_rows}")
    print(f"max_split_weight = {args.max_weight}")
    print(f"quadratic_prefixes = {','.join(str(depth) for depth in sorted(quadratic_prefixes)) or 'none'}")
    for q in dict.fromkeys(primes):
        run_field(
            q=q,
            selected_depth=args.selected_depth,
            prefix_depths=prefix_depths,
            min_rows=args.min_rows,
            max_weight=args.max_weight,
            quadratic_prefixes=quadratic_prefixes,
        )
    print("p27_a_line_prefix_support_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
