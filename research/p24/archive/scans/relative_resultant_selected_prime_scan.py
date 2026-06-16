#!/usr/bin/env python3
"""Multi-splitting-prime scan for primitive relative resultants.

For h=m*n and a fiber

    J_u(X)=sum_k j_{u+m*k} X^k,

the p24 prime-relative-normality target is

    Res(Phi_n, J_u) != 0 mod p

for every u.  This is stronger than exact packet content, but p24 has prime
recovery length n=3107441, so it is a clean sufficient theorem target.

This scan tests the selected-prime shape in small CM cycles across several
splitting primes q and optional selected-origin rotations.  It distinguishes
prime n from composite controls, where known coordinate failures occur.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import fiber_polynomials, packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class ResultantPacketRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    factor_label: str
    origin: int
    distinguished_zero: bool
    coord_zero_count: int
    content_zero: bool


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin: int,
) -> ResultantPacketRow:
    shifted = rotate(cycle, origin)
    residues = [fiber.rem(factor) for fiber in fiber_polynomials(shifted, q, m)]
    coord_zero_count = sum(residue.is_zero for residue in residues)
    h = len(cycle)
    n = h // m
    return ResultantPacketRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        factor_label=str(factor.as_expr()),
        origin=origin,
        distinguished_zero=residues[0].is_zero,
        coord_zero_count=coord_zero_count,
        content_zero=(coord_zero_count == m),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[ResultantPacketRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ResultantPacketRow] = []
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
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        rows.append(audit_packet(D, q, ell, cycle, m, factor, origin))
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


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
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    failures = [row for row in rows if row.coord_zero_count]
    distinguished_failures = [row for row in rows if row.distinguished_zero]
    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    prime_failures = [row for row in prime_rows if row.coord_zero_count]
    composite_failures = [row for row in composite_rows if row.coord_zero_count]
    prime_distinguished_failures = [row for row in prime_rows if row.distinguished_zero]
    composite_distinguished_failures = [
        row for row in composite_rows if row.distinguished_zero
    ]
    unique_rows = {
        (
            row.D,
            row.q,
            row.ell,
            row.h,
            row.m,
            row.n,
            row.factor_degree,
            row.factor_label,
        )
        for row in rows
    }
    unique_failures = {
        (
            row.D,
            row.q,
            row.ell,
            row.h,
            row.m,
            row.n,
            row.factor_degree,
            row.factor_label,
        )
        for row in failures
    }
    unique_distinguished_failures = {
        (
            row.D,
            row.q,
            row.ell,
            row.h,
            row.m,
            row.n,
            row.factor_degree,
            row.factor_label,
            row.origin,
        )
        for row in distinguished_failures
    }

    print("relative resultant selected-prime scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"scan_origins={args.scan_origins}")
    print(f"max_origins={args.max_origins}")
    print(f"include_linear={args.include_linear}")
    print("origin_shifts_are_coordinate_zero_symmetries=1")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin distinguished_zero "
            "coord_zero content_zero"
        )
        for row in failures:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                f"deg={row.factor_degree:3d} origin={row.origin:3d} "
                f"distinguished_zero={int(row.distinguished_zero)} "
                f"coord_zero={row.coord_zero_count:3d} "
                f"content_zero={int(row.content_zero)}"
            )

    expected_prime = sum(row.m / (row.q ** row.factor_degree) for row in prime_rows)
    expected_composite = sum(row.m / (row.q ** row.factor_degree) for row in composite_rows)
    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  unique_packet_rows_ignoring_origin={len(unique_rows)}")
    print(f"  prime_packet_rows={len(prime_rows)}")
    print(f"  composite_packet_rows={len(composite_rows)}")
    print(f"  coord_zero_packets={len(failures)}")
    print(f"  unique_coord_zero_packets_ignoring_origin={len(unique_failures)}")
    print(f"  distinguished_zero_packets={len(distinguished_failures)}")
    print(
        "  unique_distinguished_zero_packets_with_origin="
        f"{len(unique_distinguished_failures)}"
    )
    print(f"  prime_coord_zero_packets={len(prime_failures)}")
    print(f"  composite_coord_zero_packets={len(composite_failures)}")
    print(f"  prime_distinguished_zero_packets={len(prime_distinguished_failures)}")
    print(
        "  composite_distinguished_zero_packets="
        f"{len(composite_distinguished_failures)}"
    )
    print(f"  content_zero_packets={sum(row.content_zero for row in rows)}")
    print(f"  expected_prime_coord_zero_packets_random={expected_prime:.6f}")
    print(f"  expected_composite_coord_zero_packets_random={expected_composite:.6f}")
    if prime_failures:
        print("  prime_failure_samples:")
        for row in prime_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin={row.origin} "
                f"coord_zero={row.coord_zero_count}"
            )
    if composite_failures:
        print("  composite_failure_samples:")
        for row in composite_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin={row.origin} "
                f"coord_zero={row.coord_zero_count}"
            )
    print()
    print("interpretation")
    print("  coord_zero_packet_means_some primitive resultant vanishes mod selected prime=1")
    print("  distinguished_zero_packet_means the u=0/principal-fiber coordinate vanishes=1")
    print("  prime_n_failures_would_falsify the broad prime-relative-normality hope=1")
    print("  content_zero_packet_is_the exact harmful condition=1")
    print("conclusion=reported_relative_resultant_selected_prime_scan")


if __name__ == "__main__":
    main()
