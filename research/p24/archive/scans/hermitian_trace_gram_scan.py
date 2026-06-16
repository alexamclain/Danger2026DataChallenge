#!/usr/bin/env python3
"""Hermitian trace-Gram scan for axis packets.

For p24 the packet degree is even:

    ord_3107441(p)=388430.

The middle Frobenius power sends a primitive H-character to its inverse.  This
suggests replacing the ordinary trace pairing

    Tr(x*y)

by the Hermitian trace pairing

    Tr(x * y^(q^(d/2))).

This script compares ordinary and Hermitian trace-Gram ranks on small CM axis
packets.  The key test is whether Hermitian Gram rank survives rows where the
ordinary trace Gram is degenerate despite axis injectivity.
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
from trace_pairing_axis_boundary import trace_power_sums, trace_product

X = sp.symbols("X")


@dataclass(frozen=True)
class HermitianGramRow:
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
    ordinary_gram_rank: int
    hermitian_gram_rank: int | None
    origin_shift: int


def vector_to_poly(vector: list[int], q: int) -> sp.Poly:
    return sp.Poly(sum(value * X**i for i, value in enumerate(vector)), X, modulus=q)


def poly_pow_mod(base: sp.Poly, exponent: int, modulus: sp.Poly) -> sp.Poly:
    result = sp.Poly(1, X, modulus=base.get_modulus())
    power = base.rem(modulus)
    n = exponent
    while n:
        if n & 1:
            result = (result * power).rem(modulus)
        power = (power * power).rem(modulus)
        n >>= 1
    return result


def frobenius_middle_vector(vector: list[int], factor: sp.Poly, q: int) -> list[int]:
    """Return coefficients of poly^(q^(d/2)) mod factor for even d."""
    d = factor.degree()
    if d % 2:
        raise ValueError("Hermitian middle Frobenius requires even degree")
    x_image = poly_pow_mod(sp.Poly(X, X, modulus=q), q ** (d // 2), factor)
    total = sp.Poly(0, X, modulus=q)
    power = sp.Poly(1, X, modulus=q)
    for coeff in vector:
        if coeff:
            total = (total + coeff * power).rem(factor)
        power = (power * x_image).rem(factor)
    return coeff_vector(total.rem(factor), d, q)


def gram_rank(
    vectors: list[list[int]],
    power_sums: list[int],
    q: int,
    right_vectors: list[list[int]] | None = None,
) -> int:
    right = vectors if right_vectors is None else right_vectors
    matrix = [
        [trace_product(left, other, power_sums, q) for other in right]
        for left in vectors
    ]
    return rank_mod_q(matrix, q)


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> HermitianGramRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    ordinary_rank = gram_rank(vectors, power_sums, q)
    hermitian_rank: int | None = None
    if factor.degree() % 2 == 0:
        conjugates = [
            frobenius_middle_vector(vector, factor, q) for vector in vectors
        ]
        hermitian_rank = gram_rank(vectors, power_sums, q, conjugates)
    return HermitianGramRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(vectors),
        axis_rank=rank_mod_q(vectors, q),
        ordinary_gram_rank=ordinary_rank,
        hermitian_gram_rank=hermitian_rank,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[HermitianGramRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[HermitianGramRow] = []
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
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
    parser.add_argument("--max-axis-dim", type=int, default=75)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_axis_rows = [row for row in rows if row.axis_rank == row.axis_dim]
    ordinary_failures = [
        row for row in full_axis_rows if row.ordinary_gram_rank < row.axis_dim
    ]
    hermitian_possible = [
        row for row in full_axis_rows if row.hermitian_gram_rank is not None
    ]
    hermitian_failures = [
        row
        for row in hermitian_possible
        if row.hermitian_gram_rank is not None
        and row.hermitian_gram_rank < row.axis_dim
    ]
    ordinary_failed_hermitian_rescued = [
        row
        for row in ordinary_failures
        if row.hermitian_gram_rank == row.axis_dim
    ]

    print("Hermitian trace-Gram scan")
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
            "ordinary_gram hermitian_gram origin"
        )
        display = ordinary_failures + hermitian_failures
        if not display:
            display = rows[:50]
        for row in display[:100]:
            herm = -1 if row.hermitian_gram_rank is None else row.hermitian_gram_rank
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:3d} axis_rank={row.axis_rank:3d} "
                f"ordinary_gram={row.ordinary_gram_rank:3d} "
                f"hermitian_gram={herm:3d} origin={row.origin_shift:3d}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  full_axis_rank_rows={len(full_axis_rows)}")
    print(f"  ordinary_gram_failure_rows={len(ordinary_failures)}")
    print(f"  hermitian_possible_rows={len(hermitian_possible)}")
    print(f"  hermitian_gram_failure_rows={len(hermitian_failures)}")
    print(
        "  ordinary_failed_hermitian_rescued_rows="
        f"{len(ordinary_failed_hermitian_rescued)}"
    )
    print()
    print("interpretation")
    print("  p24_packet_degree_even_so_middle_frobenius_is_available=1")
    print("  hermitian_gram_nonzero_would_imply_axis_injectivity=1")
    print("  hermitian_pairing_matches_inverse_H_character_autocorrelation=1")
    print("conclusion=reported_hermitian_trace_gram_scan")


if __name__ == "__main__":
    main()
