#!/usr/bin/env python3
"""Scan tower-native CRT partial moments for relative-content packets.

The first complement Hasse derivative

    M1 = sum_r r J_r

uses integer representatives and has a CRT carry term when m is composite.
For p24, m=2*157*211.  This script tests the tower-native replacement:

    M0 = sum_r J_r,
    P_c = sum_t t * sum_{r == t mod c} J_r

for the coprime prime-power components c | m.  Each P_c is a partial first
moment after tracing out all other K factors, so it lives at intermediate
degree n*c rather than in a dense order-m recovery table.

The certificate condition tested here is only finite-field linear algebra:
if any of M0 or the P_c is nonzero in a packet, exact content is certified.
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
class CrtMomentRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    components: tuple[int, ...]
    content_zero: bool
    m0_zero: bool
    crt_linear_zero: bool
    partial_all_zero: bool
    first_nonzero_projection: str | None
    origin_shift: int


def coprime_components(m: int) -> tuple[int, ...]:
    return tuple(int(p) ** int(e) for p, e in sp.factorint(m).items())


def crt_idempotent(m: int, component: int) -> int:
    rest = m // component
    return (rest * pow(rest % component, -1, component)) % m


def zero_poly_like(poly: sp.Poly) -> sp.Poly:
    return sp.Poly(0, poly.gens[0], modulus=poly.get_modulus())


def sum_polys(polys: list[sp.Poly]) -> sp.Poly:
    total = zero_poly_like(polys[0])
    for poly in polys:
        total += poly
    return sp.Poly(total.as_expr(), total.gens[0], modulus=total.get_modulus())


def scale_poly(poly: sp.Poly, coeff: int) -> sp.Poly:
    q = poly.get_modulus()
    return sp.Poly((coeff % q) * poly.as_expr(), poly.gens[0], modulus=q)


def partial_moment(residues: list[sp.Poly], component: int) -> sp.Poly:
    total = zero_poly_like(residues[0])
    for t in range(component):
        subtotal = zero_poly_like(residues[0])
        for r in range(t, len(residues), component):
            subtotal += residues[r]
        total += scale_poly(subtotal, t)
    return sp.Poly(total.as_expr(), total.gens[0], modulus=total.get_modulus())


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> CrtMomentRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    m0 = sum_polys(residues).rem(factor)
    partials = tuple(partial_moment(residues, component).rem(factor) for component in components)
    crt_linear = zero_poly_like(m0)
    for component, partial in zip(components, partials):
        crt_linear += scale_poly(partial, crt_idempotent(m, component))
    crt_linear = crt_linear.rem(factor)

    projections: list[tuple[str, sp.Poly]] = [("M0", m0)]
    projections.extend((f"P{component}", partial) for component, partial in zip(components, partials))
    first = next((name for name, value in projections if not value.is_zero), None)
    content_zero = all(residue.is_zero for residue in residues)
    return CrtMomentRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        components=components,
        content_zero=content_zero,
        m0_zero=m0.is_zero,
        crt_linear_zero=crt_linear.is_zero,
        partial_all_zero=all(partial.is_zero for partial in partials),
        first_nonzero_projection=first,
        origin_shift=origin_shift,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[CrtMomentRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[CrtMomentRow] = []
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
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        rows.append(audit_packet(D, q, ell, shifted, m, factor, shift))
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
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    nonzero_rows = [row for row in rows if not row.content_zero]
    content_failures = [row for row in rows if row.content_zero]
    m0_failures = [row for row in nonzero_rows if row.m0_zero]
    crt_pair_failures = [
        row for row in nonzero_rows
        if row.m0_zero and row.crt_linear_zero
    ]
    partial_family_failures = [
        row for row in nonzero_rows
        if row.m0_zero and row.partial_all_zero
    ]
    hist: dict[str, int] = {}
    for row in nonzero_rows:
        key = row.first_nonzero_projection or "none"
        hist[key] = hist.get(key, 0) + 1

    print("CRT partial-moment projection scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin components content_zero "
            "M0_zero CRT_linear_zero partial_all_zero first"
        )
        for row in rows:
            interesting = (
                row.content_zero
                or row.m0_zero
                or row.crt_linear_zero
                or row.partial_all_zero
            )
            if interesting:
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                    f"deg={row.factor_degree:3d} origin={row.origin_shift:3d} "
                    f"components={list(row.components)} "
                    f"content_zero={int(row.content_zero)} "
                    f"M0_zero={int(row.m0_zero)} "
                    f"CRT_linear_zero={int(row.crt_linear_zero)} "
                    f"partial_all_zero={int(row.partial_all_zero)} "
                    f"first={row.first_nonzero_projection}"
                )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  nonzero_packet_rows={len(nonzero_rows)}")
    print(f"  content_failures={len(content_failures)}")
    print(f"  m0_failures={len(m0_failures)}")
    print(f"  m0_crt_linear_pair_failures={len(crt_pair_failures)}")
    print(f"  m0_partial_family_failures={len(partial_family_failures)}")
    print(f"  first_projection_histogram={dict(sorted(hist.items()))}")
    if partial_family_failures:
        print("  partial_family_failure_samples:")
        for row in partial_family_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} components={list(row.components)}"
            )
    print()
    print("interpretation")
    print("  CRT_linear_is_tower_native_but_not_the_integer_Hasse_derivative=1")
    print("  partial_family_uses_all_component_moments_without_CRT_carry=1")
    print("  no_partial_family_failures_supports_a_compressed_tower_projection_target=1")
    print("conclusion=reported_crt_partial_moment_projection_scan")


if __name__ == "__main__":
    main()
