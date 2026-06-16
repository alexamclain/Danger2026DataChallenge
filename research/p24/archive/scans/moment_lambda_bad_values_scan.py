#!/usr/bin/env python3
"""Forbidden base-field lambdas for the two-moment content certificate.

For a packet factor `f | Phi_n`, let

    M0 = sum_u J_u mod f,
    M1 = sum_u u J_u mod f.

If the content vector is nonzero, a scalar projection

    L_lambda = M0 + lambda*M1

can vanish for at most one base-field value `lambda`, unless both moments
already vanish.  This scan computes that forbidden value when it exists.

The point is certificate packaging: for p24 there are eight packet factors, so
after proving `{M0,M1}` content nonzero, one small lambda outside the forbidden
set would reduce the finite-field certificate to one resultant.  This script
tests the same phenomenon in selected-prime small CM rows.
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


@dataclass(frozen=True)
class LambdaRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    origin: int
    section: str
    content_zero: bool
    m0_zero: bool
    m1_zero: bool
    pair_zero: bool
    bad_lambda: int | None
    small_lambda_hit: int | None


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def moment_residue(
    residues: list[sp.Poly],
    factor: sp.Poly,
    q: int,
    degree: int,
) -> sp.Poly:
    var = factor.gens[0]
    total = sp.Poly(0, var, modulus=q)
    for u, residue in enumerate(residues):
        coeff = pow(u % q, degree, q)
        if coeff:
            total = (total + coeff * residue).rem(factor)
    return total.rem(factor)


def coeffs(poly: sp.Poly, degree: int, q: int) -> list[int]:
    return [int(poly.nth(i)) % q for i in range(degree)]


def forbidden_lambda(m0: sp.Poly, m1: sp.Poly, factor: sp.Poly, q: int) -> int | None:
    """Return lambda in F_q with m0 + lambda*m1 == 0, if it exists."""
    d = factor.degree()
    a = coeffs(m0, d, q)
    b = coeffs(m1, d, q)
    lam: int | None = None
    for left, right in zip(a, b):
        if right == 0:
            if left != 0:
                return None
            continue
        candidate = (-left * pow(right, -1, q)) % q
        if lam is None:
            lam = candidate
        elif lam != candidate:
            return None
    return lam


def small_lambda_hit(
    m0: sp.Poly,
    m1: sp.Poly,
    factor: sp.Poly,
    q: int,
    bound: int,
) -> int | None:
    for signed in range(-bound, bound + 1):
        lam = signed % q
        if (m0 + lam * m1).rem(factor).is_zero:
            return signed
    return None


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin: int,
    section: str,
    lambda_bound: int,
) -> LambdaRow:
    shifted = rotate(cycle, origin)
    fibers = section_fiber_polynomials(shifted, q, m, section)
    residues = [fiber.rem(factor) for fiber in fibers]
    content_zero = all(residue.is_zero for residue in residues)
    m0 = moment_residue(residues, factor, q, 0)
    m1 = moment_residue(residues, factor, q, 1)
    h = len(cycle)
    n = h // m
    bad = forbidden_lambda(m0, m1, factor, q)
    return LambdaRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        origin=origin,
        section=section,
        content_zero=content_zero,
        m0_zero=m0.is_zero,
        m1_zero=m1.is_zero,
        pair_zero=(m0.is_zero and m1.is_zero),
        bad_lambda=bad,
        small_lambda_hit=small_lambda_hit(m0, m1, factor, q, lambda_bound),
    )


def scan(args: argparse.Namespace) -> list[LambdaRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[LambdaRow] = []
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
            if args.scan_origins:
                step = max(1, h // args.max_origins) if args.max_origins else 1
                origins = list(range(0, h, step))[: args.max_origins or h]
            else:
                origins = [0]
            for origin in origins:
                for m in quotient_sizes:
                    n = h // m
                    if args.section == "complement" and sp.gcd(m, n) != 1:
                        continue
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        rows.append(
                            audit_packet(
                                D,
                                q,
                                ell,
                                cycle,
                                m,
                                factor,
                                origin,
                                args.section,
                                args.lambda_bound,
                            )
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def print_samples(title: str, rows: list[LambdaRow]) -> None:
    if not rows:
        return
    print(f"  {title}:")
    for row in rows[:8]:
        print(
            f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
            f"deg={row.factor_degree} origin={row.origin} "
            f"m0_zero={int(row.m0_zero)} m1_zero={int(row.m1_zero)} "
            f"bad_lambda={row.bad_lambda} small_hit={row.small_lambda_hit}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-abs-D", type=int, default=30000)
    parser.add_argument("--max-prime-quotients", type=int, default=5)
    parser.add_argument("--max-composite-quotients", type=int, default=5)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=120)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=300000)
    parser.add_argument("--max-splitting-primes", type=int, default=3)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--max-origins", type=int, default=12)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--section", choices=("contiguous", "complement"), default="complement")
    parser.add_argument("--lambda-bound", type=int, default=16)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    content_failures = [row for row in rows if row.content_zero]
    pair_failures = [row for row in rows if row.pair_zero and not row.content_zero]
    m0_failures = [row for row in rows if row.m0_zero and not row.content_zero]
    bad_lambda_rows = [
        row for row in rows
        if row.bad_lambda is not None and not row.content_zero
    ]
    small_lambda_rows = [
        row for row in rows
        if row.small_lambda_hit is not None and not row.content_zero
    ]
    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    small_hits_by_lambda: dict[int, int] = {}
    for row in small_lambda_rows:
        assert row.small_lambda_hit is not None
        small_hits_by_lambda[row.small_lambda_hit] = (
            small_hits_by_lambda.get(row.small_lambda_hit, 0) + 1
        )

    print("moment lambda bad-values scan")
    print(f"section={args.section}")
    print(f"max_cases={args.max_cases}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"lambda_bound={args.lambda_bound}")
    print(f"scan_origins={args.scan_origins}")
    print(f"include_linear={args.include_linear}")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin section content_zero "
            "m0_zero m1_zero pair_zero bad_lambda small_lambda_hit"
        )
        for row in rows:
            if (
                row.content_zero
                or row.pair_zero
                or row.m0_zero
                or row.small_lambda_hit is not None
            ):
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} "
                    f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                    f"n_prime={int(row.n_is_prime)} deg={row.factor_degree:3d} "
                    f"origin={row.origin:3d} section={row.section:10s} "
                    f"content_zero={int(row.content_zero)} "
                    f"m0_zero={int(row.m0_zero)} m1_zero={int(row.m1_zero)} "
                    f"pair_zero={int(row.pair_zero)} "
                    f"bad_lambda={row.bad_lambda} "
                    f"small_lambda_hit={row.small_lambda_hit}"
                )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  prime_packet_rows={len(prime_rows)}")
    print(f"  composite_packet_rows={len(composite_rows)}")
    print(f"  content_failures={len(content_failures)}")
    print(f"  m0_failures={len(m0_failures)}")
    print(f"  pair_failures={len(pair_failures)}")
    print(f"  rows_with_base_field_bad_lambda={len(bad_lambda_rows)}")
    print(f"  rows_with_small_lambda_hit={len(small_lambda_rows)}")
    print(f"  small_hits_by_lambda={dict(sorted(small_hits_by_lambda.items()))}")
    print_samples("m0_failure_samples", m0_failures)
    print_samples("pair_failure_samples", pair_failures)
    print_samples("small_lambda_hit_samples", small_lambda_rows)
    print()
    print("interpretation")
    print("  pair_failure_would_falsify_the_M0_M1_content_certificate=1")
    print("  small_lambda_hit_means_that_signed_lambda_would_fail_one_packet=1")
    print("  a_fixed_lambda_outside_observed_hits_packages_content_as_one_resultant=1")
    print("conclusion=reported_moment_lambda_bad_values_scan")


if __name__ == "__main__":
    main()
