#!/usr/bin/env python3
"""Audit full scalar-MDS behavior of the centered difference rowspace.

The cyclic-difference identity rewrites the live p24 factors as consecutive
minors of

    Q_b = P_b - P_{b-1}.

The p24 theorem only needs the 211 cyclic consecutive `156`-column minors of
`Q` to be nonzero.  A stronger shortcut would be that the `156 x 211`
difference matrix is an ordinary scalar MDS generator: every `156`-column
minor is nonzero, equivalently the rowspace has distance `211-156+1 = 56`.

This script tests that strengthening in small actual-CM rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd
import random

import sympy as sp
from cypari2 import Pari

from centered_marginal_difference_code_audit import (
    consecutive_diff_window_det,
    cyclic_difference_rows,
)
from centered_marginal_cyclic_code_boundary import point_matrix
from centered_marginal_leading_minor_audit import det_mod
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class DifferenceMDSAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    row_dim: int
    diff_rank: int
    subset_count: int
    zero_subset_count: int
    first_zero_subset: tuple[int, ...] | None
    cyclic_zero_count: int
    random_trials: int
    random_zero_subset_count_min: int
    random_zero_subset_count_max: int
    random_mds_count: int


def column_minor(matrix: list[list[int]], cols: tuple[int, ...], q: int) -> int:
    return det_mod([[row[col] for col in cols] for row in matrix], q)


def count_zero_column_subsets(
    matrix: list[list[int]],
    q: int,
    subset_size: int,
    max_subsets: int,
) -> tuple[int, int, tuple[int, ...] | None]:
    total = comb(len(matrix[0]), subset_size)
    if total > max_subsets:
        raise ValueError(f"subset count {total} exceeds max_subsets={max_subsets}")
    zeros = 0
    first_zero = None
    for cols in combinations(range(len(matrix[0])), subset_size):
        if column_minor(matrix, cols, q) == 0:
            zeros += 1
            if first_zero is None:
                first_zero = cols
    return total, zeros, first_zero


def random_matrix(row_dim: int, col_count: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(col_count)] for _ in range(row_dim)]


def random_baseline(
    row_dim: int,
    col_count: int,
    q: int,
    max_subsets: int,
    trials: int,
    seed: int,
) -> tuple[int, int, int]:
    rng = random.Random(seed + 41 * q + 1009 * row_dim + col_count)
    zero_counts: list[int] = []
    mds_count = 0
    for _ in range(trials):
        matrix = random_matrix(row_dim, col_count, q, rng)
        _total, zeros, _first = count_zero_column_subsets(
            matrix, q, row_dim, max_subsets
        )
        zero_counts.append(zeros)
        if zeros == 0:
            mds_count += 1
    return min(zero_counts), max(zero_counts), mds_count


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    args: argparse.Namespace,
) -> DifferenceMDSAudit | None:
    h = len(cycle)
    n = h // m
    if factor.degree() % 2:
        return None
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    if right < left:
        return None
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    marginal = double_marginal(kernel_matrix(residues, factor, q), left, right, q)
    points = point_matrix(marginal, left, right, q)
    diffs = cyclic_difference_rows(points, q)
    row_dim = left - 1
    subset_count, zero_count, first_zero = count_zero_column_subsets(
        diffs, q, row_dim, args.max_subsets
    )
    cyclic_zeros = sum(
        1
        for start in range(right)
        if consecutive_diff_window_det(diffs, start, row_dim, q) == 0
    )
    random_min, random_max, random_mds = random_baseline(
        row_dim,
        right,
        q,
        args.max_subsets,
        args.random_trials,
        args.seed,
    )
    return DifferenceMDSAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        row_dim=row_dim,
        diff_rank=rank_mod_q(diffs, q),
        subset_count=subset_count,
        zero_subset_count=zero_count,
        first_zero_subset=first_zero,
        cyclic_zero_count=cyclic_zeros,
        random_trials=args.random_trials,
        random_zero_subset_count_min=random_min,
        random_zero_subset_count_max=random_max,
        random_mds_count=random_mds,
    )


def scan(args: argparse.Namespace) -> DifferenceMDSAudit | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
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
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([c for c in coprime_components(m) if c > 2]) >= 2
        ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                components = tuple(c for c in coprime_components(m) if c > 2)
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in components:
                        if args.only_left and left != args.only_left:
                            continue
                        for right in components:
                            if args.only_right and right != args.only_right:
                                continue
                            row = audit_case(
                                D, q, ell, cycle, m, factor, left, right, args
                            )
                            if row is not None:
                                return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--max-subsets", type=int, default=500000)
    parser.add_argument("--random-trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered difference-MDS row found")
    print("Centered marginal difference-MDS audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"row_dim={row.row_dim}")
    print(f"diff_rank={row.diff_rank}")
    print(f"subset_count={row.subset_count}")
    print(f"zero_subset_count={row.zero_subset_count}")
    print(f"first_zero_subset={row.first_zero_subset}")
    print(f"cyclic_zero_count={row.cyclic_zero_count}")
    print(f"random_trials={row.random_trials}")
    print(f"random_zero_subset_count_min={row.random_zero_subset_count_min}")
    print(f"random_zero_subset_count_max={row.random_zero_subset_count_max}")
    print(f"random_mds_count={row.random_mds_count}/{row.random_trials}")
    print()
    print("interpretation")
    print("  zero_subset_count=0 means full scalar MDS in the tested row=1")
    print("  if random_mds_count is also high this is generic evidence only=1")
    print("  cyclic_zero_count=0 is the weaker live theorem=1")
    print("conclusion=reported_centered_marginal_difference_mds_audit")


if __name__ == "__main__":
    main()
