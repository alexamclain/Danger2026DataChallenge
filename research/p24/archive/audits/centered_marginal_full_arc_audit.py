#!/usr/bin/env python3
"""Audit full affine-arc behavior of centered marginal point columns.

The live p24 theorem only needs cyclic consecutive 157-arcs among the 211
right columns.  A stronger possible theorem is that all 157-subsets are
affinely independent.  This script tests that strengthening on small actual-CM
rows where all subsets are enumerable.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd
import random

import sympy as sp
from cypari2 import Pari

from centered_marginal_leading_minor_audit import det_mod
from centered_marginal_cyclic_code_boundary import point_matrix
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    double_marginal,
    kernel_matrix,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class FullArcAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    subset_count: int
    zero_subset_count: int
    consecutive_zero_count: int
    first_zero_subset: tuple[int, ...] | None
    random_trials: int
    random_zero_subset_count_min: int
    random_zero_subset_count_max: int
    random_full_arc_count: int


def affine_det(points: list[list[int]], subset: tuple[int, ...], q: int) -> int:
    dim = len(points)
    base = subset[0]
    matrix = []
    for row in range(dim):
        matrix.append(
            [
                (points[row][col] - points[row][base]) % q
                for col in subset[1:]
            ]
        )
    return det_mod(matrix, q)


def count_zero_affine_subsets(
    points: list[list[int]],
    q: int,
    subset_size: int,
    max_subsets: int,
) -> tuple[int, int, tuple[int, ...] | None]:
    total = comb(len(points[0]), subset_size)
    if total > max_subsets:
        raise ValueError(f"subset count {total} exceeds max_subsets={max_subsets}")
    zero_count = 0
    first_zero = None
    for subset in combinations(range(len(points[0])), subset_size):
        if affine_det(points, subset, q) == 0:
            zero_count += 1
            if first_zero is None:
                first_zero = subset
    return total, zero_count, first_zero


def consecutive_zero_count(points: list[list[int]], q: int, subset_size: int) -> int:
    length = len(points[0])
    zeros = 0
    for start in range(length):
        subset = tuple((start + offset) % length for offset in range(subset_size))
        if affine_det(points, subset, q) == 0:
            zeros += 1
    return zeros


def random_points(dim: int, count: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(count)] for _ in range(dim)]


def random_baseline(
    dim: int,
    count: int,
    q: int,
    subset_size: int,
    max_subsets: int,
    trials: int,
    seed: int,
) -> tuple[int, int, int]:
    rng = random.Random(seed + 10007 * q + 97 * dim + count)
    zero_counts: list[int] = []
    full = 0
    for _ in range(trials):
        points = random_points(dim, count, q, rng)
        _total, zeros, _first = count_zero_affine_subsets(
            points, q, subset_size, max_subsets
        )
        zero_counts.append(zeros)
        if zeros == 0:
            full += 1
    return min(zero_counts), max(zero_counts), full


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
) -> FullArcAudit | None:
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
    subset_size = left
    subset_count, zero_count, first_zero = count_zero_affine_subsets(
        points, q, subset_size, args.max_subsets
    )
    consecutive_zeros = consecutive_zero_count(points, q, subset_size)
    random_min, random_max, random_full = random_baseline(
        left - 1,
        right,
        q,
        subset_size,
        args.max_subsets,
        args.random_trials,
        args.seed,
    )
    return FullArcAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        subset_count=subset_count,
        zero_subset_count=zero_count,
        consecutive_zero_count=consecutive_zeros,
        first_zero_subset=first_zero,
        random_trials=args.random_trials,
        random_zero_subset_count_min=random_min,
        random_zero_subset_count_max=random_max,
        random_full_arc_count=random_full,
    )


def scan(args: argparse.Namespace) -> FullArcAudit | None:
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
    parser.add_argument("--max-subsets", type=int, default=20000)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")
    print("Centered marginal full-arc audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"subset_size={row.left}")
    print(f"subset_count={row.subset_count}")
    print(f"zero_subset_count={row.zero_subset_count}")
    print(f"consecutive_zero_count={row.consecutive_zero_count}")
    print(f"first_zero_subset={row.first_zero_subset}")
    print()
    print("random_baseline")
    print(f"  random_trials={row.random_trials}")
    print(f"  random_zero_subset_count_min={row.random_zero_subset_count_min}")
    print(f"  random_zero_subset_count_max={row.random_zero_subset_count_max}")
    print(f"  random_full_arc_count={row.random_full_arc_count}")
    print()
    print("interpretation")
    print("  full_arc_zero_count_tests_mds_strengthening=1")
    print("  consecutive_arc_is_the_live_p24_requirement=1")
    print("conclusion=reported_centered_marginal_full_arc_audit")


if __name__ == "__main__":
    main()
