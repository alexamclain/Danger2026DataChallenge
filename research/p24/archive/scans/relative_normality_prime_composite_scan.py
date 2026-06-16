#!/usr/bin/env python3
"""Prime-vs-composite relative normality scan for small CM cycles.

The p24 product-certificate refinement asks whether prime recovery length
behaves better than the composite examples that killed the universal product
theorem.  For a quotient `h=m*n`, this scan tests primitive relative packets:

    J_u(X) = sum_k j_{u+m*k} X^k  mod f(X),  f | Phi_n.

For prime `n`, these packets are exactly the nontrivial relative characters.
For composite `n`, they are only primitive relative characters, but they still
include the known `n=6` counterexample.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from packetized_relative_content_scan import (
    fiber_polynomials,
    hermitian_energy_poly,
    packet_factors,
)


@dataclass(frozen=True)
class PacketRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    coord_zero_count: int
    content_zero: bool
    hermitian_zero: bool
    origin_tests: int
    origin_coord_zero_count: int
    origin_zero_sample: tuple[int, ...]


def rotate(cycle: list[int], shift: int) -> list[int]:
    if shift == 0:
        return cycle
    return cycle[shift:] + cycle[:shift]


def quotient_sizes_any(
    h: int,
    max_prime: int,
    max_composite: int,
    min_n: int,
    max_n: int,
) -> list[int]:
    prime_ms: list[int] = []
    composite_ms: list[int] = []
    for n in sorted(int(d) for d in sp.divisors(h)):
        if n < min_n or n > max_n or n >= h:
            continue
        m = h // n
        if m < 2:
            continue
        if sp.isprime(n):
            prime_ms.append(m)
        elif n > 2:
            composite_ms.append(m)
    prime_ms = sorted(prime_ms, key=lambda m: (h // m, m))[:max_prime]
    composite_ms = sorted(composite_ms, key=lambda m: (h // m, m))[:max_composite]
    return sorted(set(prime_ms + composite_ms), key=lambda m: (h // m, m))


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    scan_origins: bool,
) -> PacketRow:
    h = len(cycle)
    n = h // m
    residues = [fiber.rem(factor) for fiber in fiber_polynomials(cycle, q, m)]
    coord_zero_count = sum(residue.is_zero for residue in residues)
    hermitian_zero = hermitian_energy_poly(cycle, q, m).rem(factor).is_zero
    origin_zero_sample: list[int] = []
    if scan_origins:
        for shift in range(h):
            shifted_residues = [
                fiber.rem(factor)
                for fiber in fiber_polynomials(rotate(cycle, shift), q, m)
            ]
            if any(residue.is_zero for residue in shifted_residues):
                origin_zero_sample.append(shift)
    return PacketRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        coord_zero_count=coord_zero_count,
        content_zero=(coord_zero_count == m),
        hermitian_zero=hermitian_zero,
        origin_tests=(h if scan_origins else 0),
        origin_coord_zero_count=len(origin_zero_sample),
        origin_zero_sample=tuple(origin_zero_sample[:12]),
    )


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_prime_quotients: int,
    max_composite_quotients: int,
    min_n: int,
    max_n: int,
    q_start: int,
    q_stop: int,
    include_linear: bool,
    only_D: int | None,
    scan_origins: bool,
) -> list[PacketRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    if only_D is None:
        discriminants = [-5000] + [
            D for D in range(-200, -max_abs_D - 1, -1)
            if D % 4 in (0, 1)
        ]
    else:
        discriminants = [only_D]
    rows: list[PacketRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=max_prime_quotients,
            max_composite=max_composite_quotients,
            min_n=min_n,
            max_n=max_n,
        )
        if not quotient_sizes:
            continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        for m in quotient_sizes:
            n = h // m
            for factor in packet_factors(n, q):
                if factor.degree() == 1 and not include_linear:
                    continue
                rows.append(audit_packet(D, q, ell, cycle, m, factor, scan_origins))
        cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=40)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=120)
    ap.add_argument("--max-abs-D", type=int, default=30000)
    ap.add_argument("--max-prime-quotients", type=int, default=4)
    ap.add_argument("--max-composite-quotients", type=int, default=4)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=200)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=300000)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--only-D", type=int)
    ap.add_argument("--scan-origins", action="store_true")
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_prime_quotients=args.max_prime_quotients,
        max_composite_quotients=args.max_composite_quotients,
        min_n=args.min_n,
        max_n=args.max_n,
        q_start=args.q_start,
        q_stop=args.q_stop,
        include_linear=args.include_linear,
        only_D=args.only_D,
        scan_origins=args.scan_origins,
    )

    print("relative normality prime/composite packet scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"max_n={args.max_n}")
    print(f"q_stop={args.q_stop}")
    print(f"include_linear={args.include_linear}")
    print(f"only_D={args.only_D}")
    print(f"scan_origins={args.scan_origins}")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg coord_zero content_zero "
            "hermitian_zero"
        )
        for row in rows:
            if (
                row.coord_zero_count
                or row.content_zero
                or row.hermitian_zero
                or row.origin_coord_zero_count
            ):
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                    f"deg={row.factor_degree:3d} coord_zero={row.coord_zero_count:3d} "
                    f"content_zero={int(row.content_zero)} "
                    f"hermitian_zero={int(row.hermitian_zero)} "
                    f"origin_zero_count={row.origin_coord_zero_count:3d} "
                    f"origin_zero_sample={list(row.origin_zero_sample)}"
                )

    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    prime_coord_failures = [row for row in prime_rows if row.coord_zero_count]
    composite_coord_failures = [row for row in composite_rows if row.coord_zero_count]
    prime_content_failures = [row for row in prime_rows if row.content_zero]
    composite_content_failures = [row for row in composite_rows if row.content_zero]
    prime_hermitian_failures = [row for row in prime_rows if row.hermitian_zero]
    composite_hermitian_failures = [row for row in composite_rows if row.hermitian_zero]
    prime_origin_failures = [row for row in prime_rows if row.origin_coord_zero_count]
    composite_origin_failures = [row for row in composite_rows if row.origin_coord_zero_count]
    prime_expected_coord = sum(row.m / (row.q ** row.factor_degree) for row in prime_rows)
    composite_expected_coord = sum(row.m / (row.q ** row.factor_degree) for row in composite_rows)
    prime_expected_origin = sum(
        row.origin_tests * row.m / (row.q ** row.factor_degree)
        for row in prime_rows
    )
    composite_expected_origin = sum(
        row.origin_tests * row.m / (row.q ** row.factor_degree)
        for row in composite_rows
    )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  prime_packet_rows={len(prime_rows)}")
    print(f"  composite_packet_rows={len(composite_rows)}")
    print(f"  prime_coord_zero_packets={len(prime_coord_failures)}")
    print(f"  composite_coord_zero_packets={len(composite_coord_failures)}")
    print(f"  prime_content_zero_packets={len(prime_content_failures)}")
    print(f"  composite_content_zero_packets={len(composite_content_failures)}")
    print(f"  prime_hermitian_zero_packets={len(prime_hermitian_failures)}")
    print(f"  composite_hermitian_zero_packets={len(composite_hermitian_failures)}")
    print(f"  prime_packets_with_some_origin_coord_zero={len(prime_origin_failures)}")
    print(f"  composite_packets_with_some_origin_coord_zero={len(composite_origin_failures)}")
    print(f"  selected_origin_tests={sum(row.origin_tests for row in rows)}")
    print(f"  selected_origin_coord_zeros={sum(row.origin_coord_zero_count for row in rows)}")
    print(f"  expected_prime_coord_zero_packets_random={prime_expected_coord:.6f}")
    print(f"  expected_composite_coord_zero_packets_random={composite_expected_coord:.6f}")
    print(f"  expected_prime_origin_coord_zeros_random={prime_expected_origin:.6f}")
    print(f"  expected_composite_origin_coord_zeros_random={composite_expected_origin:.6f}")
    print(f"  max_prime_coord_zero_count={max((row.coord_zero_count for row in prime_rows), default=0)}")
    print(f"  max_composite_coord_zero_count={max((row.coord_zero_count for row in composite_rows), default=0)}")
    if composite_coord_failures[:8]:
        print("  composite_coord_zero_samples=")
        for row in composite_coord_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} coord_zero={row.coord_zero_count}"
            )
    if prime_coord_failures[:8]:
        print("  prime_coord_zero_samples=")
        for row in prime_coord_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} coord_zero={row.coord_zero_count}"
            )
    if prime_origin_failures[:8]:
        print("  prime_some_origin_zero_samples=")
        for row in prime_origin_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin_zero_count={row.origin_coord_zero_count} "
                f"origins={list(row.origin_zero_sample)}"
            )
    if composite_origin_failures[:8]:
        print("  composite_some_origin_zero_samples=")
        for row in composite_origin_failures[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin_zero_count={row.origin_coord_zero_count} "
                f"origins={list(row.origin_zero_sample)}"
            )
    print()
    print("interpretation")
    print("  coordinate_zero_is_failure_of_the_strong_product_certificate=1")
    print("  content_zero_is_the_exact_harmful_packet_condition=1")
    print("  prime_n_rows_model_the_p24_recovery_subgroup_more_closely=1")
    print("  origin_scan_models_selected_prime_rotation_when_enabled=1")
    print("conclusion=reported_relative_normality_prime_composite_scan")


if __name__ == "__main__":
    main()
