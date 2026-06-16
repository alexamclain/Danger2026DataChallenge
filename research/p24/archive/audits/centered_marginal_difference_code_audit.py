#!/usr/bin/env python3
"""Audit the cyclic-difference form of centered marginal windows.

For centered point columns `P_b`, set

    Q_b = P_b - P_{b-1}.

Then

    P_{t+i} - P_t = Q_{t+1} + ... + Q_{t+i},

so the affine window determinant equals the consecutive `Q`-window
determinant up to a unit triangular change of basis.  In dual language a
plateau word becomes a sparse-support word after the cyclic difference map.

This script tests whether this sharper support formulation secretly turns the
actual small-CM centered row spaces into cyclic/MDS codes.  If the difference
rowspace is not shift-stable, BCH/cyclic-code imports still do not apply.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from centered_marginal_cyclic_code_boundary import (
    affine_window_det,
    cyclic_shift_rows,
    point_matrix,
)
from centered_marginal_leading_minor_audit import det_mod
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
)
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class DifferenceCodeAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    point_row_rank: int
    diff_row_rank: int
    diff_rows_sum_zero_count: int
    diff_max_shift_span_rank: int
    diff_shift_stable_count: int
    shift_tests: int
    determinant_mismatches: int
    window_zero_count: int
    window_distinct_count: int
    diff_window_values: tuple[int, ...]


def cyclic_difference_rows(points: list[list[int]], q: int) -> list[list[int]]:
    if not points:
        return []
    right = len(points[0])
    return [
        [
            (row[col] - row[(col - 1) % right]) % q
            for col in range(right)
        ]
        for row in points
    ]


def consecutive_diff_window_det(
    diffs: list[list[int]], start: int, width: int, q: int
) -> int:
    matrix = []
    right = len(diffs[0])
    for row in diffs:
        matrix.append([row[(start + offset) % right] for offset in range(1, width + 1)])
    return det_mod(matrix, q)


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
) -> DifferenceCodeAudit | None:
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
    _centered = centered_double_marginal(marginal, q)
    points = point_matrix(marginal, left, right, q)
    diffs = cyclic_difference_rows(points, q)
    point_rank = rank_mod_q(points, q)
    diff_rank = rank_mod_q(diffs, q)
    diff_shift_span_ranks = []
    stable_count = 0
    for shift in range(1, right):
        shifted = cyclic_shift_rows(diffs, shift)
        span_rank = rank_mod_q(diffs + shifted, q)
        diff_shift_span_ranks.append(span_rank)
        if span_rank == diff_rank:
            stable_count += 1

    width = left - 1
    affine_windows = [
        affine_window_det(points, start, width, q) for start in range(right)
    ]
    diff_windows = [
        consecutive_diff_window_det(diffs, start, width, q)
        for start in range(right)
    ]
    mismatches = sum(
        1 for left_value, right_value in zip(affine_windows, diff_windows)
        if left_value != right_value
    )

    return DifferenceCodeAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        point_row_rank=point_rank,
        diff_row_rank=diff_rank,
        diff_rows_sum_zero_count=sum(
            1 for row in diffs if sum(row) % q == 0
        ),
        diff_max_shift_span_rank=max(diff_shift_span_ranks)
        if diff_shift_span_ranks else diff_rank,
        diff_shift_stable_count=stable_count,
        shift_tests=right - 1,
        determinant_mismatches=mismatches,
        window_zero_count=sum(1 for value in diff_windows if value == 0),
        window_distinct_count=len(set(diff_windows)),
        diff_window_values=tuple(diff_windows),
    )


def scan(args: argparse.Namespace) -> DifferenceCodeAudit | None:
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
                                D, q, ell, cycle, m, factor, left, right
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
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered difference-code row found")
    print("Centered marginal difference-code audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"point_row_rank={row.point_row_rank}")
    print(f"diff_row_rank={row.diff_row_rank}")
    print(f"diff_rows_sum_zero_count={row.diff_rows_sum_zero_count}/{row.left - 1}")
    print(f"diff_max_shift_span_rank={row.diff_max_shift_span_rank}")
    print(f"diff_shift_stable_count={row.diff_shift_stable_count}/{row.shift_tests}")
    print(f"determinant_mismatches={row.determinant_mismatches}")
    print(f"window_zero_count={row.window_zero_count}")
    print(f"window_distinct_count={row.window_distinct_count}")
    print(f"diff_window_values_prefix={list(row.diff_window_values[:40])}")
    print()
    print("interpretation")
    print("  affine_windows_equal_consecutive_difference_windows=1")
    print("  cyclic_difference_turns_plateaus_into_coordinate_erasure_support=1")
    print("  shift_stable_difference_rowspace_would_enable_cyclic_code_import=1")
    print("  nonstable_difference_rowspace_keeps_schubert_fitting_target_live=1")
    print("conclusion=reported_centered_marginal_difference_code_audit")


if __name__ == "__main__":
    main()
