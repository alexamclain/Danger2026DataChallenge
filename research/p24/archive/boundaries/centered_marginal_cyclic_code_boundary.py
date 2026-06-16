#!/usr/bin/env python3
"""Boundary audit for cyclic-code shortcuts on centered marginals.

The reduced product `Pi_C,right` is a cyclic product of consecutive minors.
It is tempting to treat the row space as a cyclic code and invoke BCH/MDS
intuition.  This script checks that temptation on small actual-CM rows.

It builds the point matrix

    P_b(a) = M(a,b) - M(a,0) - M(0,b) + M(0,0),  b mod right,

with `P_0=0`, and tests whether the row space is stable under cyclic shifts
of the right coordinate.  It also recomputes the affine consecutive-window
determinants

    det(P_{t+1}-P_t, ..., P_{t+left-1}-P_t).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

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
class CyclicBoundary:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    row_rank: int
    max_shift_span_rank: int
    shift_stable_count: int
    shift_tests: int
    window_zero_count: int
    window_distinct_count: int
    window_values: tuple[int, ...]


def shift_row(row: list[int], shift: int) -> list[int]:
    n = len(row)
    shift %= n
    return [row[(index - shift) % n] for index in range(n)]


def cyclic_shift_rows(matrix: list[list[int]], shift: int) -> list[list[int]]:
    return [shift_row(row, shift) for row in matrix]


def point_matrix(
    marginal: list[list[int]],
    left: int,
    right: int,
    q: int,
) -> list[list[int]]:
    centered = centered_double_marginal(marginal, q)
    rows = left - 1
    out = [[0 for _ in range(right)] for _ in range(rows)]
    for row in range(rows):
        for col in range(1, right):
            out[row][col] = centered[row][col - 1]
    return out


def affine_window_det(points: list[list[int]], start: int, width: int, q: int) -> int:
    rows = len(points)
    matrix = []
    for row in range(rows):
        base = points[row][start % len(points[row])]
        matrix.append(
            [
                (points[row][(start + offset) % len(points[row])] - base) % q
                for offset in range(1, width + 1)
            ]
        )
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
) -> CyclicBoundary | None:
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
    row_rank = rank_mod_q(points, q)
    shift_span_ranks = []
    stable_count = 0
    for shift in range(1, right):
        shifted = cyclic_shift_rows(points, shift)
        span_rank = rank_mod_q(points + shifted, q)
        shift_span_ranks.append(span_rank)
        if span_rank == row_rank:
            stable_count += 1
    width = left - 1
    windows = [affine_window_det(points, start, width, q) for start in range(right)]
    return CyclicBoundary(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        row_rank=row_rank,
        max_shift_span_rank=max(shift_span_ranks) if shift_span_ranks else row_rank,
        shift_stable_count=stable_count,
        shift_tests=right - 1,
        window_zero_count=sum(1 for value in windows if value == 0),
        window_distinct_count=len(set(windows)),
        window_values=tuple(windows),
    )


def scan(args: argparse.Namespace) -> CyclicBoundary | None:
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
        raise SystemExit("no eligible case found")
    print("Centered marginal cyclic-code boundary")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"row_rank={row.row_rank}")
    print(f"max_shift_span_rank={row.max_shift_span_rank}")
    print(f"shift_stable_count={row.shift_stable_count}/{row.shift_tests}")
    print(f"window_zero_count={row.window_zero_count}")
    print(f"window_distinct_count={row.window_distinct_count}")
    print(f"window_values_prefix={list(row.window_values[:40])}")
    print()
    print("interpretation")
    print("  cyclic_minor_sequence_does_not_imply_rowspace_is_cyclic_code=1")
    print("  shift_stable_count_zero_demotes_bch_cyclic_code_shortcut=1")
    print("conclusion=reported_centered_marginal_cyclic_code_boundary")


if __name__ == "__main__":
    main()
