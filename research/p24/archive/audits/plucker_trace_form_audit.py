#!/usr/bin/env python3
"""Cauchy-Binet audit for the axis Pluecker/minor route.

Let V be the axis coefficient matrix in the packet power basis and B the
Hermitian trace form in that basis.  The Hermitian axis determinant is

    det(V B V^t).

Cauchy-Binet expands it as

    sum_{|S|=|T|=r} det(V_S) det(B_{S,T}) det(V_T).

The leading coefficient minor is one Pluecker coordinate `det(V_S0)`.  This
script checks whether the Hermitian determinant is controlled by that single
coordinate, or whether many Pluecker coordinates and trace-form minors
contribute.  A dense expansion means the coefficient-minor certificate is a
separate rank certificate, not an immediate proof of the Hermitian p-unit
theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations

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
    rank_mod_q,
)
from trace_pairing_axis_boundary import trace_power_sums, trace_product
from hermitian_trace_gram_scan import frobenius_middle_vector


@dataclass(frozen=True)
class PlueckerAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    axis_dim: int
    components: tuple[int, ...]
    leading_v_det: int
    leading_b_det: int
    leading_term: int
    gram_det: int
    cb_sum: int
    pluecker_nonzero: int
    pluecker_total: int
    nonzero_b_minors_on_pluecker_support: int
    off_diagonal_nonzero_terms: int
    diagonal_sum: int


def det_mod(matrix: list[list[int]], q: int) -> int:
    return int(sp.Matrix(matrix).det()) % q


def submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[matrix[i][j] for j in cols] for i in rows]


def column_submatrix(
    rows: list[list[int]],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[row[j] for j in cols] for row in rows]


def hermitian_power_basis_matrix(factor: sp.Poly, q: int) -> list[list[int]]:
    d = factor.degree()
    basis = [[1 if i == j else 0 for i in range(d)] for j in range(d)]
    conjugates = [frobenius_middle_vector(vector, factor, q) for vector in basis]
    power_sums = trace_power_sums(factor, q, 2 * d - 2)
    return [
        [trace_product(left, right, power_sums, q) for right in conjugates]
        for left in basis
    ]


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> PlueckerAudit | None:
    h = len(cycle)
    n = h // m
    if factor.degree() % 2:
        return None
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    components = coprime_components(m)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    r = len(vectors)
    d = factor.degree()
    if r > d:
        return None
    B = hermitian_power_basis_matrix(factor, q)
    gram = [
        [
            sum(vectors[i][u] * B[u][v] * vectors[j][v] for u in range(d) for v in range(d)) % q
            for j in range(r)
        ]
        for i in range(r)
    ]
    gram_det = det_mod(gram, q)

    all_cols = tuple(combinations(range(d), r))
    v_dets = {
        cols: det_mod(column_submatrix(vectors, cols), q)
        for cols in all_cols
    }
    nz_cols = [cols for cols, det in v_dets.items() if det]
    leading = tuple(range(r))
    leading_v = v_dets[leading]
    leading_b = det_mod(submatrix(B, leading, leading), q)
    leading_term = (leading_v * leading_b * leading_v) % q

    cb_sum = 0
    diagonal_sum = 0
    b_support_count = 0
    offdiag_terms = 0
    for S in nz_cols:
        det_s = v_dets[S]
        for T in nz_cols:
            det_b = det_mod(submatrix(B, S, T), q)
            if det_b:
                b_support_count += 1
            term = det_s * det_b * v_dets[T]
            if term % q:
                if S != T:
                    offdiag_terms += 1
                cb_sum = (cb_sum + term) % q
                if S == T:
                    diagonal_sum = (diagonal_sum + term) % q

    return PlueckerAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=d,
        axis_dim=r,
        components=components,
        leading_v_det=leading_v,
        leading_b_det=leading_b,
        leading_term=leading_term,
        gram_det=gram_det,
        cb_sum=cb_sum,
        pluecker_nonzero=len(nz_cols),
        pluecker_total=len(all_cols),
        nonzero_b_minors_on_pluecker_support=b_support_count,
        off_diagonal_nonzero_terms=offdiag_terms,
        diagonal_sum=diagonal_sum,
    )


def first_case(args: argparse.Namespace) -> PlueckerAudit | None:
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
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    row = audit_case(D, q, ell, shifted, m, factor, args.origin_shift)
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
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=6)
    parser.add_argument("--max-factor-degree", type=int, default=10)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--origin-shift", type=int, default=0)
    args = parser.parse_args()

    row = first_case(args)
    if row is None:
        raise SystemExit("no eligible case found")
    if row.cb_sum != row.gram_det:
        raise AssertionError("Cauchy-Binet sum did not match Gram determinant")

    print("Pluecker trace-form Cauchy-Binet audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"components={list(row.components)}")
    print(f"axis_dim={row.axis_dim}")
    print()
    print("determinants")
    print(f"  leading_v_det={row.leading_v_det}")
    print(f"  leading_b_det={row.leading_b_det}")
    print(f"  leading_term={row.leading_term}")
    print(f"  diagonal_sum={row.diagonal_sum}")
    print(f"  gram_det={row.gram_det}")
    print(f"  cb_sum={row.cb_sum}")
    print()
    print("support")
    print(f"  pluecker_nonzero={row.pluecker_nonzero}")
    print(f"  pluecker_total={row.pluecker_total}")
    print(f"  nonzero_b_minors_on_pluecker_support={row.nonzero_b_minors_on_pluecker_support}")
    print(f"  off_diagonal_nonzero_terms={row.off_diagonal_nonzero_terms}")
    print()
    print("interpretation")
    print("  cauchy_binet_expansion_verified=1")
    print("  leading_pluecker_coordinate_nonzero_is_only_one_term=1")
    print("  off_diagonal_terms_nonzero_means_no_single_minor_bridge_to_hermitian=1")
    print("conclusion=reported_pluecker_trace_form_audit")


if __name__ == "__main__":
    main()
