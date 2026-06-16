#!/usr/bin/env python3
"""Cauchy-Binet audit for centered mixed marginal leading minors.

For left/right CRT components c,d, the centered mixed block has entries

    C(a,b) = <L_a, R_b>_H,

where `L_a` and `R_b` are trace-zero component sums of packet fibers.  In a
packet power basis this is

    C_window = A B R^t,

with `B` the Hermitian trace form.  For a square leading window of size
`r = c-1`, Cauchy-Binet gives

    det(C_window)
      = sum_{|S|=|T|=r} det(A_S) det(B_{S,T}) det(R_T).

This script checks whether that expansion collapses to the leading
coefficient minors, or is dense.  A dense expansion means the visible
`Delta_C_leading` certificate is a genuine mixed exterior trace-form value,
not an immediate product of separate left/right coordinate minors.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components, sum_polys, zero_poly_like
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import centered_double_marginal, double_marginal, kernel_matrix
from hermitian_trace_gram_scan import frobenius_middle_vector
from l1_axis_injectivity_scan import coeff_vector, discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from trace_pairing_axis_boundary import trace_power_sums, trace_product


@dataclass(frozen=True)
class MixedCBAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    window_dim: int
    centered_rank: int
    window_det: int
    cb_sum: int
    leading_left_det: int
    leading_b_det: int
    leading_right_det: int
    leading_term: int
    diagonal_sum: int
    left_pluecker_nonzero: int
    right_pluecker_nonzero: int
    pluecker_total: int
    nonzero_b_on_support: int
    nonzero_terms: int
    off_diagonal_terms: int


def det_mod(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 1
    return int(sp.Matrix(matrix).det()) % q


def column_submatrix(rows: list[list[int]], cols: tuple[int, ...]) -> list[list[int]]:
    return [[row[j] for j in cols] for row in rows]


def submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def hermitian_power_basis_matrix(factor: sp.Poly, q: int) -> list[list[int]]:
    d = factor.degree()
    basis = [[1 if i == j else 0 for i in range(d)] for j in range(d)]
    conjugates = [frobenius_middle_vector(vector, factor, q) for vector in basis]
    power_sums = trace_power_sums(factor, q, 2 * d - 2)
    return [
        [trace_product(left, right, power_sums, q) for right in conjugates]
        for left in basis
    ]


def component_difference_vectors(
    residues: list[sp.Poly],
    component: int,
    q: int,
    factor: sp.Poly,
) -> list[list[int]]:
    zero_terms = [residues[r] for r in range(0, len(residues), component)]
    zero_sum = sum_polys(zero_terms) if zero_terms else zero_poly_like(residues[0])
    out: list[list[int]] = []
    for t in range(1, component):
        terms = [residues[r] for r in range(t, len(residues), component)]
        total = sum_polys(terms) if terms else zero_poly_like(residues[0])
        diff = sp.Poly((total - zero_sum).as_expr(), factor.gens[0], modulus=q)
        out.append(coeff_vector(diff.rem(factor), factor.degree(), q))
    return out


def matmul_mod(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    if not left or not right:
        return []
    inner = len(right)
    cols = len(right[0])
    return [
        [
            sum(row[k] * right[k][col] for k in range(inner)) % q
            for col in range(cols)
        ]
        for row in left
    ]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)] if matrix else []


def audit_pair(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
) -> MixedCBAudit | None:
    h = len(cycle)
    n = h // m
    d = factor.degree()
    if d % 2:
        return None
    if pow(q, d // 2, n) != n - 1:
        return None
    r = left - 1
    if right - 1 < r or d < r:
        return None

    fibers = section_fiber_polynomials(cycle, q, m, "complement")
    residues = [fiber.rem(factor) for fiber in fibers]
    left_vectors = component_difference_vectors(residues, left, q, factor)
    right_vectors_full = component_difference_vectors(residues, right, q, factor)
    right_vectors = right_vectors_full[:r]
    B = hermitian_power_basis_matrix(factor, q)
    window = matmul_mod(matmul_mod(left_vectors, B, q), transpose(right_vectors), q)
    window_det = det_mod(window, q)

    marginal = double_marginal(kernel_matrix(residues, factor, q), left, right, q)
    centered = centered_double_marginal(marginal, q)
    centered_rank = rank_mod_q(centered, q)
    leading_centered = [row[:r] for row in centered]
    if leading_centered != window:
        raise AssertionError("direct centered marginal does not match packet window")

    col_sets = tuple(combinations(range(d), r))
    left_dets = {
        cols: det_mod(column_submatrix(left_vectors, cols), q)
        for cols in col_sets
    }
    right_dets = {
        cols: det_mod(column_submatrix(right_vectors, cols), q)
        for cols in col_sets
    }
    left_support = [cols for cols, det in left_dets.items() if det]
    right_support = [cols for cols, det in right_dets.items() if det]
    leading = tuple(range(r))
    leading_left = left_dets[leading]
    leading_right = right_dets[leading]
    leading_b = det_mod(submatrix(B, leading, leading), q)
    leading_term = leading_left * leading_b * leading_right % q

    cb_sum = 0
    diagonal_sum = 0
    nonzero_b = 0
    nonzero_terms = 0
    off_diag = 0
    for S in left_support:
        det_left = left_dets[S]
        for T in right_support:
            det_b = det_mod(submatrix(B, S, T), q)
            if det_b:
                nonzero_b += 1
            term = det_left * det_b * right_dets[T] % q
            if term:
                nonzero_terms += 1
                if S != T:
                    off_diag += 1
                else:
                    diagonal_sum = (diagonal_sum + term) % q
                cb_sum = (cb_sum + term) % q
    if cb_sum != window_det:
        raise AssertionError("Cauchy-Binet sum did not match determinant")

    return MixedCBAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=d,
        left=left,
        right=right,
        window_dim=r,
        centered_rank=centered_rank,
        window_det=window_det,
        cb_sum=cb_sum,
        leading_left_det=leading_left,
        leading_b_det=leading_b,
        leading_right_det=leading_right,
        leading_term=leading_term,
        diagonal_sum=diagonal_sum,
        left_pluecker_nonzero=len(left_support),
        right_pluecker_nonzero=len(right_support),
        pluecker_total=len(col_sets),
        nonzero_b_on_support=nonzero_b,
        nonzero_terms=nonzero_terms,
        off_diagonal_terms=off_diag,
    )


def scan(args: argparse.Namespace) -> MixedCBAudit | None:
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
            shifted = rotate(cycle, args.origin_shift % h)
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
                            if right - 1 < left - 1:
                                continue
                            row = audit_pair(
                                D, q, ell, shifted, m, factor, left, right
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
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")
    print("Centered marginal mixed Cauchy-Binet audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"window_dim={row.window_dim}")
    print(f"centered_rank={row.centered_rank}")
    print()
    print("determinants")
    print(f"  leading_left_det={row.leading_left_det}")
    print(f"  leading_b_det={row.leading_b_det}")
    print(f"  leading_right_det={row.leading_right_det}")
    print(f"  leading_term={row.leading_term}")
    print(f"  diagonal_sum={row.diagonal_sum}")
    print(f"  window_det={row.window_det}")
    print(f"  cb_sum={row.cb_sum}")
    print()
    print("support")
    print(f"  left_pluecker_nonzero={row.left_pluecker_nonzero}")
    print(f"  right_pluecker_nonzero={row.right_pluecker_nonzero}")
    print(f"  pluecker_total={row.pluecker_total}")
    print(f"  nonzero_b_on_support={row.nonzero_b_on_support}")
    print(f"  nonzero_terms={row.nonzero_terms}")
    print(f"  off_diagonal_terms={row.off_diagonal_terms}")
    print()
    print("interpretation")
    print("  centered_window_equals_A_B_Rt=1")
    print("  mixed_cauchy_binet_expansion_verified=1")
    print("  leading_difference_minor_is_a_mixed_exterior_trace_form=1")
    print("conclusion=reported_centered_marginal_cauchy_binet_audit")


if __name__ == "__main__":
    main()
