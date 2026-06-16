#!/usr/bin/env python3
"""Audit alpha/beta origin action on leading axis coefficient minors.

For an origin shift `s` with

    s == n*alpha + m*beta mod h,

the packet fibers transform as

    F'_r(X) = X^(-beta) F_{r+alpha}(X).

The alpha part is a translation of the axis coordinate and should act through
a unimodular change of axis basis.  The beta part is multiplication by a
packet monomial before taking leading coordinates, and is the reason leading
coefficient minors are not obviously origin invariant.

This script records leading-minor determinant values grouped by alpha and beta
directions.  It is a consistency check for whether the coefficient-minor route
has a packetwise invariant p-unit status, or remains a selected-coordinate
certificate.
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
from l1_axis_injectivity_scan import discriminants


@dataclass(frozen=True)
class OriginDet:
    shift: int
    alpha: int
    beta: int
    det: int


def crt_coordinates(shift: int, m: int, n: int) -> tuple[int, int]:
    alpha = (shift * pow(n % m, -1, m)) % m
    beta = (shift * pow(m % n, -1, n)) % n
    return alpha, beta


def first_origin_orbit(args: argparse.Namespace) -> tuple[int, int, int, int, int, list[OriginDet]] | None:
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
                    rows: list[OriginDet] = []
                    for shift in range(h):
                        shifted = rotate(cycle, shift)
                        row = audit_packet(D, q, ell, shifted, m, factor, shift)
                        if row.leading_det is None:
                            raise AssertionError("expected determinant for small axis")
                        alpha, beta = crt_coordinates(shift, m, n)
                        rows.append(OriginDet(shift, alpha, beta, row.leading_det))
                    return D, q, ell, m, n, rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def value_summary(values: list[int]) -> str:
    return (
        f"count={len(values)} distinct={len(set(values))} "
        f"zeros={sum(1 for value in values if value == 0)}"
    )


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

    found = first_origin_orbit(args)
    if found is None:
        raise SystemExit("no eligible origin orbit found")
    D, q, ell, m, n, rows = found
    all_values = [row.det for row in rows]
    pure_alpha = [row.det for row in rows if row.beta == 0]
    pure_beta = [row.det for row in rows if row.alpha == 0]

    by_alpha = {
        alpha: [row.det for row in rows if row.alpha == alpha]
        for alpha in sorted({row.alpha for row in rows})
    }
    by_beta = {
        beta: [row.det for row in rows if row.beta == beta]
        for beta in sorted({row.beta for row in rows})
    }
    alpha_distinct_hist: dict[int, int] = {}
    beta_distinct_hist: dict[int, int] = {}
    for values in by_alpha.values():
        alpha_distinct_hist[len(set(values))] = alpha_distinct_hist.get(len(set(values)), 0) + 1
    for values in by_beta.values():
        beta_distinct_hist[len(set(values))] = beta_distinct_hist.get(len(set(values)), 0) + 1

    print("axis leading-minor origin-action audit")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"h={m*n}")
    print()
    print("summaries")
    print(f"  all_origins {value_summary(all_values)}")
    print(f"  pure_alpha_beta0 {value_summary(pure_alpha)}")
    print(f"  pure_beta_alpha0 {value_summary(pure_beta)}")
    print(f"  alpha_fixed_distinct_hist={dict(sorted(alpha_distinct_hist.items()))}")
    print(f"  beta_fixed_distinct_hist={dict(sorted(beta_distinct_hist.items()))}")
    print()
    print("samples")
    for row in rows[: min(24, len(rows))]:
        print(
            f"  shift={row.shift:3d} alpha={row.alpha:3d} "
            f"beta={row.beta:3d} det={row.det}"
        )
    print()
    print("interpretation")
    print("  beta0_tests_axis_translation_only=1")
    print("  alpha0_tests_packet_monomial_multiplication_only=1")
    print("  determinant_value_variation_means_no_literal_origin_invariance=1")
    print("conclusion=reported_axis_minor_origin_action_audit")


if __name__ == "__main__":
    main()
