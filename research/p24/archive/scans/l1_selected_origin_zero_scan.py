#!/usr/bin/env python3
"""Selected-origin zero scan for M0 and L1 partial-moment scalars.

Rotating a complete split CM cycle models selecting a different prime/root
above the same split rational prime.  This scan compares the K-trivial M0
scalar with the tower-native but K-origin-dependent L1 scalar.
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
from crt_partial_moment_projection_scan import (
    coprime_components,
    partial_moment,
    scale_poly,
    sum_polys,
)


@dataclass(frozen=True)
class OriginScalarRow:
    scalar: str
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    components: tuple[int, ...]
    zero_count: int
    zero_origins_sample: tuple[int, ...]


def scalar_value(cycle: list[int], q: int, m: int, factor: sp.Poly, scalar: str) -> sp.Poly:
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    m0 = sum_polys(residues).rem(factor)
    if scalar == "M0":
        return m0
    if scalar == "L1":
        total = m0
        for component in coprime_components(m):
            total += partial_moment(residues, component).rem(factor)
        return total.rem(factor)
    raise ValueError(f"unknown scalar {scalar}")


def audit_scalar(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> OriginScalarRow:
    h = len(cycle)
    zero_origins: list[int] = []
    for shift in range(h):
        shifted = rotate(cycle, shift)
        if scalar_value(shifted, q, m, factor, scalar).is_zero:
            zero_origins.append(shift)
    return OriginScalarRow(
        scalar=scalar,
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=h // m,
        n_is_prime=bool(sp.isprime(h // m)),
        factor_degree=factor.degree(),
        components=coprime_components(m),
        zero_count=len(zero_origins),
        zero_origins_sample=tuple(zero_origins[:16]),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[OriginScalarRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[OriginScalarRow] = []
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
            for m in quotient_sizes:
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    rows.append(audit_scalar(D, q, ell, cycle, m, factor, "M0"))
                    rows.append(audit_scalar(D, q, ell, cycle, m, factor, "L1"))
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=100)
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--max-prime-quotients", type=int, default=5)
    parser.add_argument("--max-composite-quotients", type=int, default=5)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=100)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    zero_rows = [row for row in rows if row.zero_count]
    m0_rows = [row for row in rows if row.scalar == "M0"]
    l1_rows = [row for row in rows if row.scalar == "L1"]

    print("L1 selected-origin zero scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: scalar D q ell h m n n_prime deg components zero_count "
            "zero_origins_sample"
        )
        for row in zero_rows:
            print(
                f"scalar={row.scalar:2s} D={row.D:7d} q={row.q:6d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"n_prime={int(row.n_is_prime)} deg={row.factor_degree:3d} "
                f"components={list(row.components)} zero_count={row.zero_count:3d} "
                f"zero_origins_sample={list(row.zero_origins_sample)}"
            )

    print()
    print("summary")
    print(f"  scalar_rows={len(rows)}")
    print(f"  m0_rows={len(m0_rows)}")
    print(f"  l1_rows={len(l1_rows)}")
    print(f"  m0_zero_rows={sum(row.zero_count > 0 for row in m0_rows)}")
    print(f"  l1_zero_rows={sum(row.zero_count > 0 for row in l1_rows)}")
    print(f"  m0_selected_origin_zeros={sum(row.zero_count for row in m0_rows)}")
    print(f"  l1_selected_origin_zeros={sum(row.zero_count for row in l1_rows)}")
    print()
    print("interpretation")
    print("  origin_rotation_models_selected_prime_or_CM_root_choice=1")
    print("  M0_is_K_trivial_but_can_have_selected_origin_packet_zeros=1")
    print("  L1_is_K_origin_dependent_but_no_toy_selected_zeros_seen_if_count_is_0=1")
    print("conclusion=reported_l1_selected_origin_zero_scan")


if __name__ == "__main__":
    main()
