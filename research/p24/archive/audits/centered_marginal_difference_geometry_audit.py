#!/usr/bin/env python3
"""Projective-geometry audit for centered difference columns.

The difference-MDS audit asks whether the columns

    Q_b = P_b - P_{b-1}

form an ordinary scalar MDS generator.  A stronger and more structured route
would identify these columns, up to p-unit row/column changes, with a
generalized Reed-Solomon/rational-normal-curve model.  In small row dimension
this predicts excess low-degree projective equations; for row dimension 3 it
predicts a conic through the projective columns.

This script compares low-degree homogeneous equations for the actual
difference columns against random controls.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from centered_marginal_cyclic_code_boundary import point_matrix
from centered_marginal_difference_code_audit import cyclic_difference_rows
from centered_marginal_projective_geometry_audit import (
    coordinate_complexities,
    histogram,
    nullity_of_forms,
)
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class DifferenceGeometryAudit:
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
    degree: int
    monomial_count: int
    form_rank: int
    form_nullity: int
    random_nullity_min: int
    random_nullity_max: int
    random_nullity_histogram: tuple[tuple[int, int], ...]
    coordinate_complexities: tuple[int, ...]
    random_complexity_min: int
    random_complexity_max: int


def random_zero_sum_points(
    dim: int,
    count: int,
    q: int,
    rng,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for _ in range(dim):
        prefix = [rng.randrange(q) for _ in range(count - 1)]
        rows.append(prefix + [(-sum(prefix)) % q])
    return rows


def audit_diffs(
    D: int,
    q: int,
    ell: int,
    h: int,
    m: int,
    factor_degree: int,
    left: int,
    right: int,
    diffs: list[list[int]],
    args: argparse.Namespace,
) -> DifferenceGeometryAudit:
    monomial_count, form_rank, form_nullity = nullity_of_forms(
        diffs, args.degree, q
    )
    rng_seed = args.seed + 1009 * q + 17 * left + 131 * right + args.degree
    import random

    rng = random.Random(rng_seed)
    random_nullities: list[int] = []
    random_complexities: list[int] = []
    for _ in range(args.random_trials):
        random_set = random_zero_sum_points(left - 1, right, q, rng)
        _mono, _rank, nullity = nullity_of_forms(random_set, args.degree, q)
        random_nullities.append(nullity)
        random_complexities.extend(coordinate_complexities(random_set, q))
    complexities = coordinate_complexities(diffs, q)
    return DifferenceGeometryAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=h // m,
        factor_degree=factor_degree,
        left=left,
        right=right,
        row_dim=left - 1,
        degree=args.degree,
        monomial_count=monomial_count,
        form_rank=form_rank,
        form_nullity=form_nullity,
        random_nullity_min=min(random_nullities),
        random_nullity_max=max(random_nullities),
        random_nullity_histogram=histogram(random_nullities),
        coordinate_complexities=complexities,
        random_complexity_min=min(random_complexities),
        random_complexity_max=max(random_complexities),
    )


def scan(args: argparse.Namespace) -> DifferenceGeometryAudit | None:
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
                    if factor.degree() % 2 or pow(q, factor.degree() // 2, n) != n - 1:
                        continue
                    residues = [
                        fiber.rem(factor)
                        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
                    ]
                    for left in components:
                        if args.only_left and left != args.only_left:
                            continue
                        for right in components:
                            if args.only_right and right != args.only_right:
                                continue
                            if right < left:
                                continue
                            marginal = double_marginal(
                                kernel_matrix(residues, factor, q), left, right, q
                            )
                            points = point_matrix(marginal, left, right, q)
                            diffs = cyclic_difference_rows(points, q)
                            return audit_diffs(
                                D,
                                q,
                                ell,
                                h,
                                m,
                                factor.degree(),
                                left,
                                right,
                                diffs,
                                args,
                            )
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
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered difference-geometry row found")
    print("Centered marginal difference-geometry audit")
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
    print(f"homogeneous_degree={row.degree}")
    print(f"monomial_count={row.monomial_count}")
    print(f"form_rank={row.form_rank}")
    print(f"form_nullity={row.form_nullity}")
    print(f"random_nullity_min={row.random_nullity_min}")
    print(f"random_nullity_max={row.random_nullity_max}")
    print(f"random_nullity_histogram={dict(row.random_nullity_histogram)}")
    print(f"coordinate_complexities={list(row.coordinate_complexities)}")
    print(f"random_coordinate_complexity_min={row.random_complexity_min}")
    print(f"random_coordinate_complexity_max={row.random_complexity_max}")
    print()
    print("interpretation")
    print("  excess_low_degree_equations_would_support_grs_or_rational_normal_route=1")
    print("  random_like_nullity_demotes_visible_grs_equivalence=1")
    print("conclusion=reported_centered_marginal_difference_geometry_audit")


if __name__ == "__main__":
    main()
