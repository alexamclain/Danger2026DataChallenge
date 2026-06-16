#!/usr/bin/env python3
"""Sweep small embedded CM towers for low-moment child selection.

The current p24 low-moment hypothesis says that a small number of power sums
could pair the selected child fiber without reconstructing the whole child
polynomial.  This script tests that shape on many small cyclic CM cycles where
the embedded roots are available.

For a quotient refinement

    parent_count = m, child_count = m*r,

the true child above parent a is

    {Y_a, Y_{a+m}, ..., Y_{a+(r-1)m}}.

For each degree d we count unordered r-subsets of all child_count fine periods
with the same power sums sum(x), ..., sum(x^d).  The p24 theorem candidate
would need an intrinsic way to construct these moments and an anti-collision
proof; this sweep only asks whether the finite-field collision behavior is
encouraging in actual embedded CM controls.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
import math

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import (
    find_full_cycle_prime,
    find_splitting_prime,
    period_sequence,
)


PINNED_D = -5000


@dataclass(frozen=True)
class SweepRow:
    D: int
    q: int
    ell: int
    h: int
    parent_count: int
    child_count: int
    child_factor: int
    subset_count: int
    random_unique_degree: int
    first_all_unique_degree: int | None
    max_matches_at_first_unique: int | None
    counts_by_degree: tuple[tuple[int, ...], ...]


def signature(values: list[int], degree: int, q: int) -> tuple[int, ...]:
    return tuple(
        sum(pow(value, exponent, q) for value in values) % q
        for exponent in range(1, degree + 1)
    )


def count_matching_subsets(
    values: list[int],
    child_size: int,
    target_values: list[int],
    degree: int,
    q: int,
) -> int:
    target = signature(target_values, degree, q)
    count = 0
    for indices in combinations(range(len(values)), child_size):
        candidate = [values[index] for index in indices]
        if signature(candidate, degree, q) == target:
            count += 1
    return count


def log10_choose(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    ) / math.log(10)


def moments_for_random_unique(subset_count: int, q: int) -> int:
    if subset_count <= 1:
        return 0
    return math.floor(math.log(subset_count, q)) + 1


def candidate_refinements(
    h: int,
    max_child_count: int,
    max_combinations: int,
) -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    for child_count in sorted(int(d) for d in sp.divisors(h)):
        if child_count < 4 or child_count > max_child_count:
            continue
        for parent_count in sorted(int(d) for d in sp.divisors(child_count)):
            if parent_count <= 1 or parent_count >= child_count:
                continue
            child_factor = child_count // parent_count
            subset_count = math.comb(child_count, child_factor)
            if subset_count > max_combinations:
                continue
            out.append((parent_count, child_count, child_factor, subset_count))
    return out


def audit_refinement(
    D: int,
    q: int,
    ell: int,
    h: int,
    cycle: list[int],
    parent_count: int,
    child_count: int,
    child_factor: int,
    subset_count: int,
    max_degree: int,
) -> SweepRow:
    fine_periods = period_sequence(cycle, child_count, q)
    counts_by_degree: list[tuple[int, ...]] = []
    first_all_unique: int | None = None
    max_at_first: int | None = None

    for degree in range(1, max_degree + 1):
        counts = tuple(
            count_matching_subsets(
                fine_periods,
                child_factor,
                [fine_periods[index] for index in range(parent, child_count, parent_count)],
                degree,
                q,
            )
            for parent in range(parent_count)
        )
        counts_by_degree.append(counts)
        if first_all_unique is None and all(count == 1 for count in counts):
            first_all_unique = degree
            max_at_first = max(counts)

    return SweepRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        parent_count=parent_count,
        child_count=child_count,
        child_factor=child_factor,
        subset_count=subset_count,
        random_unique_degree=moments_for_random_unique(subset_count, q),
        first_all_unique_degree=first_all_unique,
        max_matches_at_first_unique=max_at_first,
        counts_by_degree=tuple(counts_by_degree),
    )


def discriminant_stream(max_abs_D: int) -> list[int]:
    return [PINNED_D] + [
        D
        for D in range(-200, -max_abs_D - 1, -1)
        if D != PINNED_D and D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[SweepRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[SweepRow] = []
    cases = 0
    seen: set[int] = set()

    for D in discriminant_stream(args.max_abs_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        split = find_splitting_prime(pari, hilbert, h, args.q_start, args.q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q, args.ell_bound)
        if full is None:
            continue
        ell, cycle = full
        refinements = candidate_refinements(
            h,
            max_child_count=args.max_child_count,
            max_combinations=args.max_combinations,
        )
        if not refinements:
            continue
        for parent_count, child_count, child_factor, subset_count in refinements[
            : args.max_refinements_per_case
        ]:
            rows.append(
                audit_refinement(
                    D=D,
                    q=q,
                    ell=ell,
                    h=h,
                    cycle=cycle,
                    parent_count=parent_count,
                    child_count=child_count,
                    child_factor=child_factor,
                    subset_count=subset_count,
                    max_degree=args.max_degree,
                )
            )
        cases += 1
        if cases >= args.max_cases:
            break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=6)
    parser.add_argument("--max-h", type=int, default=60)
    parser.add_argument("--max-abs-D", type=int, default=12000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=5000)
    parser.add_argument("--ell-bound", type=int, default=43)
    parser.add_argument("--max-child-count", type=int, default=18)
    parser.add_argument("--max-combinations", type=int, default=250000)
    parser.add_argument("--max-refinements-per-case", type=int, default=8)
    parser.add_argument("--max-degree", type=int, default=5)
    args = parser.parse_args()

    rows = scan(args)
    unique_rows = [row for row in rows if row.first_all_unique_degree is not None]
    degree_one_rows = [row for row in unique_rows if row.first_all_unique_degree == 1]
    within_random_rows = [
        row
        for row in unique_rows
        if row.first_all_unique_degree is not None
        and row.first_all_unique_degree <= max(1, row.random_unique_degree)
    ]

    print("trace-GCD low-moment CM selector sweep")
    print(f"max_cases={args.max_cases}")
    print(f"rows={len(rows)}")
    print(f"rows_all_unique_within_degree_bound={len(unique_rows)}")
    print(f"rows_unique_at_degree_one={len(degree_one_rows)}")
    print(f"rows_unique_no_later_than_random_entropy={len(within_random_rows)}")
    print()
    print("columns: D q ell h m child_count r subsets random_d first_unique counts_by_degree")
    for row in rows:
        first = "NA" if row.first_all_unique_degree is None else str(row.first_all_unique_degree)
        print(
            f"D={row.D:6d} q={row.q:5d} ell={row.ell:2d} h={row.h:3d} "
            f"m={row.parent_count:2d} child_count={row.child_count:2d} "
            f"r={row.child_factor:2d} subsets={row.subset_count:7d} "
            f"random_d={row.random_unique_degree:2d} first_unique={first:>2s} "
            f"counts={row.counts_by_degree}"
        )

    print()
    print("p24_entropy_reference")
    first_log = log10_choose(314, 157)
    second_log = log10_choose(66254, 211)
    print(f"first_layer_log10_subsets={first_log:.6f}")
    print("first_layer_random_unique_moments=4")
    print(f"second_layer_log10_subsets={second_log:.6f}")
    print("second_layer_random_unique_moments=26")
    print("total_low_moment_pairing_constraints=30")
    print()
    print("interpretation")
    print("  actual_cm_towers_can_be_tested_for_low_moment_child_selection=1")
    print("  low_moment_collision_behavior_is_a_theorem_microscope_not_a_certificate=1")
    print("  intrinsic_moment_construction_and_cm_anti_collision_remain_required=1")
    print("conclusion=reported_trace_gcd_low_moment_cm_selector_sweep")

    if not rows:
        raise SystemExit(1)
    if not unique_rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
