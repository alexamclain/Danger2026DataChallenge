#!/usr/bin/env python3
"""Audit the product over beta-shifted leading axis minors.

A single leading coefficient minor is not origin invariant.  But the product
over all packet monomial shifts

    Pi_alpha = prod_beta det(P_0 X^(-beta) V_alpha)

should have origin-independent zero/nonzero status: changing beta permutes the
factors, while changing alpha acts by a unimodular axis-basis change.

This script computes that product in small CM packets by grouping all origin
shifts according to their CRT alpha coordinate.
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
)
from crt_partial_moment_projection_scan import coprime_components
from axis_coefficient_minor_audit import audit_packet
from axis_minor_origin_action_audit import crt_coordinates
from l1_axis_injectivity_scan import discriminants


@dataclass(frozen=True)
class OriginValue:
    shift: int
    alpha: int
    beta: int
    det: int


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % q)) % q
    return out


def first_rows(args: argparse.Namespace) -> tuple[int, int, int, int, int, int, list[OriginValue]] | None:
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
            for m in quotient_sizes:
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim or axis_dim > 12:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    rows: list[OriginValue] = []
                    for shift in range(h):
                        shifted = rotate(cycle, shift)
                        row = audit_packet(D, q, ell, shifted, m, factor, shift)
                        if row.leading_det is None:
                            raise AssertionError("expected small leading determinant")
                        alpha, beta = crt_coordinates(shift, m, n)
                        rows.append(OriginValue(shift, alpha, beta, row.leading_det))
                    return D, q, ell, m, n, factor.degree(), rows
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
    parser.add_argument("--max-axis-dim", type=int, default=12)
    parser.add_argument("--max-factor-degree", type=int, default=20)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    found = first_rows(args)
    if found is None:
        raise SystemExit("no eligible packet found")
    D, q, ell, m, n, degree, rows = found
    by_alpha = {
        alpha: [row.det for row in rows if row.alpha == alpha]
        for alpha in sorted({row.alpha for row in rows})
    }
    alpha_products = {
        alpha: product_mod(values, q)
        for alpha, values in by_alpha.items()
    }
    zero_alphas = [alpha for alpha, value in alpha_products.items() if value == 0]
    squareclasses = {
        alpha: 0 if value == 0 else pow(value, (q - 1) // 2, q)
        for alpha, value in alpha_products.items()
    }

    print("axis sliding-window product audit")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"h={m*n}")
    print(f"factor_degree={degree}")
    print()
    print("alpha_products")
    for alpha, value in list(alpha_products.items())[:40]:
        sc = squareclasses[alpha]
        sc_label = "zero" if sc == 0 else ("square" if sc == 1 else "nonsquare")
        print(f"  alpha={alpha:3d} product={value:8d} squareclass={sc_label}")
    print()
    print("summary")
    print(f"  alpha_count={len(alpha_products)}")
    print(f"  distinct_alpha_products={len(set(alpha_products.values()))}")
    print(f"  zero_alpha_products={len(zero_alphas)}")
    print(f"  distinct_squareclasses={len(set(squareclasses.values()))}")
    print()
    print("interpretation")
    print("  product_over_beta_packages_all_sliding_window_minors=1")
    print("  zero_status_should_be_alpha_invariant_up_to_unimodular_axis_change=1")
    print("  product_value_may_vary_by_axis_basis_unit=1")
    print("conclusion=reported_axis_sliding_window_product_audit")


if __name__ == "__main__":
    main()
