#!/usr/bin/env python3
"""Search small scalar combinations of CRT partial moments.

For complement fibers F_r and coprime components c | m, define

    M0 = sum_r F_r,
    P_c = sum_t t * sum_{r == t mod c} F_r.

This script tests one-resultant packaging of the tower-native projection
family:

    L_lambda = M0 + sum_c lambda_c P_c.

The principal coefficient of L_lambda is always 1, so the usual complex
principal-term dominance survives for small integer lambdas.  The scan checks
whether small lambda tuples avoid finite-field packet zeros in toy CM data.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools

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
from crt_partial_moment_projection_scan import (
    coprime_components,
    partial_moment,
    scale_poly,
    sum_polys,
    zero_poly_like,
)


@dataclass(frozen=True)
class ComboRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    components: tuple[int, ...]
    origin_shift: int
    content_zero: bool
    family_zero: bool
    all_candidate_zero: bool
    first_good_lambda: tuple[int, ...] | None
    lambda_ones_zero: bool


def parse_tuple(text: str) -> tuple[int, ...]:
    if not text:
        return ()
    return tuple(int(part) for part in text.split(","))


def candidate_lambdas(component_count: int, bound: int, fixed: tuple[int, ...] | None) -> list[tuple[int, ...]]:
    if fixed is not None:
        if len(fixed) == 1 and component_count != 1:
            return [tuple(fixed[0] for _ in range(component_count))]
        if len(fixed) != component_count:
            raise ValueError("fixed lambda tuple length does not match component count")
        return [fixed]
    return [
        tuple(values)
        for values in itertools.product(range(bound + 1), repeat=component_count)
    ]


def linear_combo(m0: sp.Poly, partials: tuple[sp.Poly, ...], lambdas: tuple[int, ...]) -> sp.Poly:
    total = m0
    for coeff, partial in zip(lambdas, partials):
        total += scale_poly(partial, coeff)
    return sp.Poly(total.as_expr(), m0.gens[0], modulus=m0.get_modulus())


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    lambdas: list[tuple[int, ...]],
) -> ComboRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    m0 = sum_polys(residues).rem(factor)
    partials = tuple(partial_moment(residues, component).rem(factor) for component in components)
    projections = (m0,) + partials
    content_zero = all(residue.is_zero for residue in residues)
    family_zero = all(projection.is_zero for projection in projections)

    first_good: tuple[int, ...] | None = None
    all_zero = True
    for lamb in lambdas:
        value = linear_combo(m0, partials, lamb).rem(factor)
        if not value.is_zero:
            first_good = lamb
            all_zero = False
            break
    ones = tuple(1 for _ in components)
    lambda_ones_zero = linear_combo(m0, partials, ones).rem(factor).is_zero

    return ComboRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        components=components,
        origin_shift=origin_shift,
        content_zero=content_zero,
        family_zero=family_zero,
        all_candidate_zero=all_zero,
        first_good_lambda=first_good,
        lambda_ones_zero=lambda_ones_zero,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[ComboRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ComboRow] = []
    seen: set[int] = set()
    cases = 0

    fixed = parse_tuple(args.fixed_lambdas) if args.fixed_lambdas is not None else None

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
            quotient_sizes = [m for m in quotient_sizes if len(coprime_components(m)) >= 2]
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
                    comps = coprime_components(m)
                    lambdas = candidate_lambdas(len(comps), args.lambda_bound, fixed)
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        rows.append(audit_packet(D, q, ell, shifted, m, factor, shift, lambdas))
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--lambda-bound", type=int, default=3)
    parser.add_argument("--fixed-lambdas")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    nonzero_rows = [row for row in rows if not row.content_zero]
    family_failures = [row for row in nonzero_rows if row.family_zero]
    candidate_failures = [row for row in nonzero_rows if row.all_candidate_zero]
    ones_failures = [row for row in nonzero_rows if row.lambda_ones_zero]
    hist: dict[str, int] = {}
    for row in nonzero_rows:
        key = "none" if row.first_good_lambda is None else str(row.first_good_lambda)
        hist[key] = hist.get(key, 0) + 1

    print("CRT partial-moment linear-combo scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"require_composite_m={args.require_composite_m}")
    print(f"lambda_bound={args.lambda_bound}")
    print(f"fixed_lambdas={args.fixed_lambdas}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin components content_zero "
            "family_zero all_candidate_zero lambda_ones_zero first_good"
        )
        for row in rows:
            interesting = (
                row.content_zero
                or row.family_zero
                or row.all_candidate_zero
                or row.lambda_ones_zero
            )
            if interesting:
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                    f"deg={row.factor_degree:3d} origin={row.origin_shift:3d} "
                    f"components={list(row.components)} "
                    f"content_zero={int(row.content_zero)} "
                    f"family_zero={int(row.family_zero)} "
                    f"all_candidate_zero={int(row.all_candidate_zero)} "
                    f"lambda_ones_zero={int(row.lambda_ones_zero)} "
                    f"first_good={row.first_good_lambda}"
                )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  nonzero_packet_rows={len(nonzero_rows)}")
    print(f"  family_failures={len(family_failures)}")
    print(f"  candidate_failures={len(candidate_failures)}")
    print(f"  lambda_ones_failures={len(ones_failures)}")
    print(f"  first_good_lambda_histogram={dict(sorted(hist.items()))}")
    if candidate_failures:
        print("  candidate_failure_samples:")
        for row in candidate_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} components={list(row.components)}"
            )
    print()
    print("interpretation")
    print("  L_lambda_has_principal_coefficient_one_for_every_lambda=1")
    print("  finite_bad_lambdas_are_packet_hyperplanes_when_projection_family_nonzero=1")
    print("  one_good_small_lambda_would_package_the_tower_family_as_one_resultant=1")
    print("conclusion=reported_crt_partial_moment_linear_combo_scan")


if __name__ == "__main__":
    main()
