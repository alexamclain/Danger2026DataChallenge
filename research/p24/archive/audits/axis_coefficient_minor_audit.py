#!/usr/bin/env python3
"""Audit coefficient-minor certificates for the p24 axis map.

Axis injectivity for a packet factor follows if some `axis_dim x axis_dim`
coefficient minor of the axis images is nonzero.  This is a smaller-looking
certificate than the Hermitian trace-Gram determinant:

    rank(coefficients of Y_i) = axis_dim.

The question is whether a canonical minor, such as the leading coefficient
minor, is robust enough to become a theorem target.  This script compares:

* full coefficient rank of the axis images;
* leading minor rank on columns `0..axis_dim-1`;
* the greedy pivot columns from row reduction;
* stability of these ranks under origin shifts.

Unlike the Hermitian determinant, coefficient minors are not expected to be
origin-invariant.  A small all-origin failure is enough to demote "leading
minor p-unit" to a selected-origin heuristic rather than a packet theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import (
    axis_basis_images,
    coeff_vector,
    discriminants,
    pivot_columns_mod_q,
    rank_mod_q,
)


@dataclass(frozen=True)
class MinorRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    axis_rank: int
    leading_rank: int
    leading_det: int | None
    pivot_max: int | None
    pivot_columns: tuple[int, ...]
    origin_shift: int


def column_submatrix_rank(vectors: list[list[int]], columns: list[int], q: int) -> int:
    return rank_mod_q([[row[col] % q for col in columns] for row in vectors], q)


def square_det_mod_q(matrix: list[list[int]], q: int) -> int:
    return int(sp.Matrix(matrix).det()) % q


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> MinorRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    axis_dim = len(vectors)
    pivots = tuple(pivot_columns_mod_q(vectors, q))
    leading_columns = list(range(min(axis_dim, factor.degree())))
    leading_matrix = [
        [row[col] % q for col in leading_columns] for row in vectors
    ]
    return MinorRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=axis_dim,
        axis_rank=len(pivots),
        leading_rank=rank_mod_q(leading_matrix, q),
        leading_det=(
            square_det_mod_q(leading_matrix, q)
            if len(leading_columns) == axis_dim and axis_dim <= 12
            else None
        ),
        pivot_max=max(pivots) if pivots else None,
        pivot_columns=pivots,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[MinorRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[MinorRow] = []
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
            if sp.gcd(m, h // m) == 1
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
        ]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
            ]
        if not quotient_sizes:
            continue

        splits = find_splitting_primes(
            pari, hilbert, h, args.q_start, args.q_stop, args.max_splitting_primes
        )
        if not splits:
            continue

        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                    for factor in packet_factors(h // m, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        if factor.degree() < axis_dim:
                            continue
                        row = audit_packet(D, q, ell, shifted, m, factor, shift)
                        rows.append(row)
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=5000)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=75)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_axis = [row for row in rows if row.axis_rank == row.axis_dim]
    leading_full = [row for row in rows if row.leading_rank == row.axis_dim]
    full_axis_leading_failures = [
        row for row in full_axis if row.leading_rank < row.axis_dim
    ]
    pivot_max_values = [
        row.pivot_max for row in full_axis if row.pivot_max is not None
    ]
    determinant_values = [
        row.leading_det for row in rows if row.leading_det is not None
    ]

    print("axis coefficient-minor audit")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg components axis_dim axis_rank "
            "leading_rank leading_det pivot_max origin pivots"
        )
        display = full_axis_leading_failures[:80] or rows[:80]
        for row in display:
            pivots = ",".join(str(value) for value in row.pivot_columns[:20])
            if len(row.pivot_columns) > 20:
                pivots += ",..."
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:3d} axis_rank={row.axis_rank:3d} "
                f"leading_rank={row.leading_rank:3d} "
                f"leading_det={row.leading_det if row.leading_det is not None else 'NA':>6} "
                f"pivot_max={row.pivot_max if row.pivot_max is not None else 'NA':>3} "
                f"origin={row.origin_shift:3d} pivots={pivots}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  full_axis_rows={len(full_axis)}")
    print(f"  leading_full_rows={len(leading_full)}")
    print(f"  full_axis_leading_failure_rows={len(full_axis_leading_failures)}")
    if pivot_max_values:
        print(f"  max_pivot_max={max(pivot_max_values)}")
        print(
            "  pivot_max_over_axis_dim_max="
            f"{max(row.pivot_max / row.axis_dim for row in full_axis if row.pivot_max is not None):.6f}"
        )
    if determinant_values:
        print(f"  leading_det_values_seen={len(determinant_values)}")
        print(f"  distinct_leading_det_values={len(set(determinant_values))}")
        print(f"  zero_leading_det_values={sum(1 for value in determinant_values if value == 0)}")
    print()
    print("interpretation")
    print("  leading_minor_full_implies_axis_injectivity_for_that_origin=1")
    print("  leading_minor_is_not_origin_invariant_like_hermitian_gram=1")
    print("  leading_failures_demote_prefix_minor_to_selected_origin_heuristic=1")
    print("conclusion=reported_axis_coefficient_minor_audit")


if __name__ == "__main__":
    main()
