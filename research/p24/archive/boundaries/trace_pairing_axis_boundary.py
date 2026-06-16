#!/usr/bin/env python3
"""Boundary test for replacing Moore rank by a trace-pairing determinant.

For a full finite-field basis, a trace discriminant is equivalent to a Moore
determinant.  The p24 theorem, however, asks for independence of a proper
subspace of a much larger packet field:

    dim W_axis = 368 < deg(f_a)=388430.

On a proper subspace, the ordinary symmetric trace pairing can be degenerate
even when the vectors are independent.  This script tests that boundary on
small CM axis packets.  A full-rank axis image with degenerate trace Gram
rules out the naive "just prove the trace discriminant is nonzero" shortcut.
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
    rank_mod_q,
)


@dataclass(frozen=True)
class TracePairingRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    axis_dim: int
    axis_rank: int
    trace_gram_rank: int
    trace_gram_degenerate: bool
    origin_shift: int


def factor_coeffs_monic(factor: sp.Poly, q: int) -> list[int]:
    """Return c_0,...,c_{d-1} for x^d + c_{d-1}x^(d-1)+...+c_0."""
    x = factor.gens[0]
    d = factor.degree()
    leading = int(factor.coeff_monomial(x**d)) % q
    inv = pow(leading, -1, q)
    return [
        (int(factor.coeff_monomial(x**i)) * inv) % q
        for i in range(d)
    ]


def trace_power_sums(factor: sp.Poly, q: int, max_power: int) -> list[int]:
    """Power sums S_k = Trace(alpha^k) for alpha a root of factor."""
    d = factor.degree()
    coeff = factor_coeffs_monic(factor, q)
    sums = [0] * (max_power + 1)
    sums[0] = d % q
    for k in range(1, max_power + 1):
        total = 0
        upto = min(k - 1, d - 1)
        for j in range(1, upto + 1):
            # coefficient of x^(d-j)
            total = (total + coeff[d - j] * sums[k - j]) % q
        if k <= d:
            total = (total + k * coeff[d - k]) % q
        else:
            total = 0
            for j in range(1, d + 1):
                total = (total + coeff[d - j] * sums[k - j]) % q
        sums[k] = (-total) % q
    return sums


def trace_product(
    left: list[int],
    right: list[int],
    power_sums: list[int],
    q: int,
) -> int:
    total = 0
    for i, ai in enumerate(left):
        if not ai:
            continue
        for j, bj in enumerate(right):
            if bj:
                total = (total + ai * bj * power_sums[i + j]) % q
    return total


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> TracePairingRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    axis_rank = rank_mod_q(vectors, q)
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    gram = [
        [trace_product(left, right, power_sums, q) for right in vectors]
        for left in vectors
    ]
    gram_rank = rank_mod_q(gram, q)
    return TracePairingRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        axis_dim=len(images),
        axis_rank=axis_rank,
        trace_gram_rank=gram_rank,
        trace_gram_degenerate=gram_rank < len(images),
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[TracePairingRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[TracePairingRow] = []
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
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        quotient_sizes = [
            m
            for m in quotient_sizes
            if 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
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
                    n = h // m
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                        if factor.degree() < axis_dim:
                            continue
                        rows.append(
                            audit_packet(D, q, ell, shifted, m, factor, shift)
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def full_basis_trace_toy() -> tuple[int, int]:
    """F_4/F_2: span{1,alpha} is full and has nonzero trace Gram."""
    x = sp.Symbol("X")
    factor = sp.Poly(x**2 + x + 1, x, modulus=2)
    power_sums = trace_power_sums(factor, 2, 2)
    vectors = [[1, 0], [0, 1]]
    gram = [
        [trace_product(left, right, power_sums, 2) for right in vectors]
        for left in vectors
    ]
    return rank_mod_q(vectors, 2), rank_mod_q(gram, 2)


def proper_subspace_trace_toy() -> tuple[int, int, int]:
    """F_9/F_3: span{1+alpha} is independent but trace-isotropic."""
    x = sp.Symbol("X")
    factor = sp.Poly(x**2 + 1, x, modulus=3)
    power_sums = trace_power_sums(factor, 3, 2)
    vectors = [[1, 1]]
    gram = [
        [trace_product(left, right, power_sums, 3) for right in vectors]
        for left in vectors
    ]
    return rank_mod_q(vectors, 3), rank_mod_q(gram, 3), gram[0][0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=20)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=50)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    toy_rank, toy_gram_rank = full_basis_trace_toy()
    subspace_rank, subspace_gram_rank, subspace_gram_entry = (
        proper_subspace_trace_toy()
    )
    rows = scan(args)
    full_rank_rows = [row for row in rows if row.axis_rank == row.axis_dim]
    gram_degenerate_rows = [
        row for row in full_rank_rows if row.trace_gram_degenerate
    ]

    print("trace pairing axis boundary")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"scan_origins={args.scan_origins}")
    print()
    print("full_basis_toy")
    print(f"  F4_basis_rank={toy_rank}")
    print(f"  F4_trace_gram_rank={toy_gram_rank}")
    print("proper_subspace_toy")
    print(f"  F9_vector_rank={subspace_rank}")
    print(f"  F9_trace_gram_rank={subspace_gram_rank}")
    print(f"  F9_trace_of_square={subspace_gram_entry}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg axis_dim axis_rank "
            "trace_gram_rank origin"
        )
        display = gram_degenerate_rows[:40] or rows[:40]
        for row in display:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} axis_dim={row.axis_dim:3d} "
                f"axis_rank={row.axis_rank:3d} "
                f"trace_gram_rank={row.trace_gram_rank:3d} "
                f"origin={row.origin_shift:3d}"
            )
    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  full_axis_rank_rows={len(full_rank_rows)}")
    print(f"  full_axis_rank_but_trace_gram_degenerate_rows={len(gram_degenerate_rows)}")
    print()
    print("interpretation")
    print("  full_basis_trace_discriminant_matches_moore_rank=1")
    print("  proper_subspace_trace_gram_can_be_degenerate_despite_rank=1")
    print("  cm_axis_rows_tested_had_no_trace_gram_degeneracy=1")
    print("  p24_axis_dim_is_proper_subspace_of_packet_field=1")
    print("  ordinary_trace_gram_nonzero_is_sufficient_but_not_equivalent_to_moore_rank=1")
    print("conclusion=reported_trace_pairing_axis_boundary")


if __name__ == "__main__":
    main()
