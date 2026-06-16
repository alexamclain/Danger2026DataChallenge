#!/usr/bin/env python3
"""Verify the Hermitian axis Gram autocorrelation formula.

For an axis basis image

    Y_i(X) = sum_k y_{i,k} X^k,

the Hermitian packet Gram entry is

    H_a(i,j) = Tr_{F_q[X]/(f_a)/F_q}(Y_i(X) * Y_j(X^{-1})).

This is equivalent to the middle-Frobenius definition when
q^(deg(f_a)/2) == -1 mod n.  It rewrites the determinant target as a packet
trace of explicit quotient autocorrelation polynomials, which is the finite
identity a future p-adic/divisor proof has to exploit.
"""

from __future__ import annotations

import argparse

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
from crt_partial_moment_projection_scan import coprime_components, scale_poly, sum_polys, zero_poly_like
from l1_axis_injectivity_scan import axis_basis_images, coeff_vector, discriminants, rank_mod_q
from trace_pairing_axis_boundary import trace_power_sums, trace_product
from hermitian_trace_gram_scan import frobenius_middle_vector

X = sp.symbols("X")


def axis_basis_full_polys(
    fibers: list[sp.Poly],
    components: tuple[int, ...],
    q: int,
) -> list[tuple[str, sp.Poly]]:
    images: list[tuple[str, sp.Poly]] = [("1", sum_polys(fibers))]
    for component in components:
        for t in range(1, component):
            terms = [fibers[r] for r in range(t, len(fibers), component)]
            images.append(
                (f"I{component}_{t}", sum_polys(terms) if terms else zero_poly_like(fibers[0]))
            )
    return [(name, sp.Poly(poly.as_expr(), X, modulus=q)) for name, poly in images]


def invert_exponents(poly: sp.Poly, n: int, q: int) -> sp.Poly:
    out = sp.Poly(0, X, modulus=q)
    for (degree,), coeff in poly.terms():
        out += sp.Poly((int(coeff) % q) * X ** ((-degree) % n), X, modulus=q)
    return sp.Poly(out.as_expr(), X, modulus=q)


def trace_poly_mod_factor(poly: sp.Poly, factor: sp.Poly, q: int) -> int:
    reduced = poly.rem(factor)
    vector = coeff_vector(reduced, factor.degree(), q)
    power_sums = trace_power_sums(factor, q, factor.degree() - 1)
    return sum(value * power_sums[i] for i, value in enumerate(vector)) % q


def direct_hermitian_gram(
    images_mod_factor: list[tuple[str, sp.Poly]],
    factor: sp.Poly,
    q: int,
) -> list[list[int]]:
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images_mod_factor]
    conjugates = [frobenius_middle_vector(vector, factor, q) for vector in vectors]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    return [
        [trace_product(left, right, power_sums, q) for right in conjugates]
        for left in vectors
    ]


def autocorrelation_gram(
    images_full: list[tuple[str, sp.Poly]],
    factor: sp.Poly,
    n: int,
    q: int,
) -> list[list[int]]:
    inverted = [invert_exponents(poly, n, q) for _, poly in images_full]
    polys = [poly for _, poly in images_full]
    return [
        [
            trace_poly_mod_factor((left * right).rem(factor), factor, q)
            for right in inverted
        ]
        for left in polys
    ]


def first_case(args: argparse.Namespace):
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen: set[int] = set()
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
            ]
        splits = find_splitting_primes(
            pari, hilbert, h, args.q_start, args.q_stop, args.max_splitting_primes
        )
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                n = h // m
                components = coprime_components(m)
                axis_dim = 1 + sum(c - 1 for c in components)
                if axis_dim > args.max_axis_dim:
                    continue
                for factor_index, factor in enumerate(packet_factors(n, q)):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim or factor.degree() % 2:
                        continue
                    if pow(q, factor.degree() // 2, n) != n - 1:
                        continue
                    fibers = section_fiber_polynomials(shifted, q, m, "complement")
                    images_full = axis_basis_full_polys(fibers, components, q)
                    images_mod = axis_basis_images(
                        [fiber.rem(factor) for fiber in fibers], components, factor
                    )
                    return D, q, ell, h, m, n, factor_index, factor, images_full, images_mod
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-prime-quotients", type=int, default=6)
    parser.add_argument("--max-composite-quotients", type=int, default=6)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=120)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=45)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    args = parser.parse_args()

    case = first_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, h, m, n, factor_index, factor, images_full, images_mod = case
    direct = direct_hermitian_gram(images_mod, factor, q)
    via_corr = autocorrelation_gram(images_full, factor, n, q)
    equal = direct == via_corr

    print("Hermitian axis autocorrelation formula")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"factor_index={factor_index}")
    print(f"factor_degree={factor.degree()}")
    print(f"axis_dim={len(images_mod)}")
    print(f"formula_equal={int(equal)}")
    print(f"direct_rank={rank_mod_q(direct, q)}")
    print(f"autocorrelation_rank={rank_mod_q(via_corr, q)}")
    print()
    print("interpretation")
    print("  hermitian_gram_entries_are_packet_traces_of_Yi_times_Yj_inverse=1")
    print("  p24_determinant_is_phase_aware_axis_autocorrelation_determinant=1")
    print("conclusion=reported_hermitian_axis_autocorrelation_formula")
    if not equal:
        raise AssertionError("autocorrelation formula mismatch")


if __name__ == "__main__":
    main()
