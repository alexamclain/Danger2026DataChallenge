#!/usr/bin/env python3
"""Selected-prime stress scan for exact relative content.

This is the multi-splitting-prime companion to
`packetized_relative_content_scan.py`.  The exact p24 target is

    gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1,

for each Frobenius packet factor `f_a | Phi_n`.  The product/resultant
shortcut can fail when one coordinate `J_u mod f_a` vanishes; this scan keeps
that stronger failure visible while testing whether the exact content vector
or Hermitian scalar also fails across several selected splitting primes.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import (
    X,
    autocorrelation_energy_poly,
    content_gcd_degree,
    fiber_polynomials,
    hermitian_energy_poly,
    packet_factors,
)
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class ContentPacketRow:
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
    coord_zero_count: int
    distinguished_zero: bool
    content_gcd_degree: int
    energy_zero: bool
    energy_norm_zero: bool
    hermitian_zero: bool
    hermitian_norm_zero: bool

    @property
    def content_zero(self) -> bool:
        return self.content_gcd_degree > 0


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin: int,
) -> ContentPacketRow:
    shifted = rotate(cycle, origin)
    fibers = fiber_polynomials(shifted, q, m)
    residues = [fiber.rem(factor) for fiber in fibers]
    coord_zero_count = sum(residue.is_zero for residue in residues)
    content_degree = content_gcd_degree(factor, fibers)

    energy_poly = autocorrelation_energy_poly(shifted, q, m)
    energy_remainder = energy_poly.rem(factor)
    energy_norm = int(sp.resultant(factor.as_expr(), energy_poly.as_expr(), X)) % q

    hermitian_poly = hermitian_energy_poly(shifted, q, m)
    hermitian_remainder = hermitian_poly.rem(factor)
    hermitian_norm = (
        int(sp.resultant(factor.as_expr(), hermitian_poly.as_expr(), X)) % q
    )

    h = len(cycle)
    n = h // m
    return ContentPacketRow(
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
        coord_zero_count=coord_zero_count,
        distinguished_zero=residues[0].is_zero,
        content_gcd_degree=content_degree,
        energy_zero=energy_remainder.is_zero,
        energy_norm_zero=(energy_norm == 0),
        hermitian_zero=hermitian_remainder.is_zero,
        hermitian_norm_zero=(hermitian_norm == 0),
    )


def scan(args: argparse.Namespace) -> list[ContentPacketRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ContentPacketRow] = []
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


def key_ignoring_origin(row: ContentPacketRow) -> tuple[object, ...]:
    return (
        row.D,
        row.q,
        row.ell,
        row.h,
        row.m,
        row.n,
        row.factor_degree,
        row.factor_label,
    )


def interesting(row: ContentPacketRow) -> bool:
    return (
        row.coord_zero_count > 0
        or row.content_zero
        or row.energy_zero
        or row.energy_norm_zero
        or row.hermitian_zero
        or row.hermitian_norm_zero
    )


def print_sample(title: str, rows: list[ContentPacketRow]) -> None:
    if not rows:
        return
    print(f"  {title}:")
    for row in rows[:8]:
        print(
            f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
            f"deg={row.factor_degree} origin={row.origin} "
            f"coord_zero={row.coord_zero_count} "
            f"content_gcd_degree={row.content_gcd_degree} "
            f"energy_zero={int(row.energy_zero)} "
            f"energy_norm_zero={int(row.energy_norm_zero)} "
            f"hermitian_zero={int(row.hermitian_zero)} "
            f"hermitian_norm_zero={int(row.hermitian_norm_zero)}"
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
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    coord_zero_rows = [row for row in rows if row.coord_zero_count > 0]
    content_failures = [row for row in rows if row.content_zero]
    energy_zero_rows = [row for row in rows if row.energy_zero]
    energy_norm_zero_rows = [row for row in rows if row.energy_norm_zero]
    hermitian_zero_rows = [row for row in rows if row.hermitian_zero]
    hermitian_norm_zero_rows = [row for row in rows if row.hermitian_norm_zero]
    interesting_rows = [row for row in rows if interesting(row)]

    unique_rows = {key_ignoring_origin(row) for row in rows}
    unique_content_failures = {
        key_ignoring_origin(row) for row in content_failures
    }
    unique_hermitian_zero = {
        key_ignoring_origin(row)
        for row in rows
        if row.hermitian_zero or row.hermitian_norm_zero
    }

    print("packetized content selected-prime scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"max_n={args.max_n}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"scan_origins={args.scan_origins}")
    print(f"max_origins={args.max_origins}")
    print(f"include_linear={args.include_linear}")
    print("origin_shifts_are_coordinate_zero_symmetries=1")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin coord_zero "
            "content_gcd_degree energy_zero energy_norm_zero "
            "hermitian_zero hermitian_norm_zero"
        )
        for row in interesting_rows:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                f"deg={row.factor_degree:3d} origin={row.origin:3d} "
                f"coord_zero={row.coord_zero_count:3d} "
                f"content_gcd_degree={row.content_gcd_degree:3d} "
                f"energy_zero={int(row.energy_zero)} "
                f"energy_norm_zero={int(row.energy_norm_zero)} "
                f"hermitian_zero={int(row.hermitian_zero)} "
                f"hermitian_norm_zero={int(row.hermitian_norm_zero)}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  unique_packet_rows_ignoring_origin={len(unique_rows)}")
    print(f"  prime_packet_rows={len(prime_rows)}")
    print(f"  composite_packet_rows={len(composite_rows)}")
    print(f"  coord_zero_packets={len(coord_zero_rows)}")
    print(f"  prime_coord_zero_packets={sum(row.coord_zero_count > 0 for row in prime_rows)}")
    print(
        "  composite_coord_zero_packets="
        f"{sum(row.coord_zero_count > 0 for row in composite_rows)}"
    )
    print(f"  content_failures={len(content_failures)}")
    print(
        "  unique_content_failures_ignoring_origin="
        f"{len(unique_content_failures)}"
    )
    print(f"  energy_zero_packets={len(energy_zero_rows)}")
    print(f"  energy_norm_zero_packets={len(energy_norm_zero_rows)}")
    print(f"  hermitian_zero_packets={len(hermitian_zero_rows)}")
    print(f"  hermitian_norm_zero_packets={len(hermitian_norm_zero_rows)}")
    print(
        "  unique_hermitian_zero_or_norm_zero="
        f"{len(unique_hermitian_zero)}"
    )

    print_sample("coord_zero_samples", coord_zero_rows)
    print_sample("content_failure_samples", content_failures)
    print_sample("hermitian_failure_samples", hermitian_zero_rows + hermitian_norm_zero_rows)

    print()
    print("interpretation")
    print("  coord_zero_is_failure_of_the_strong_product_certificate=1")
    print("  content_gcd_degree_positive_is_exact_packet_failure=1")
    print("  hermitian_zero_or_norm_zero_is_failure_of_scalar_sufficient_certificate=1")
    print("  selected_splitting_primes_model_different_primes_above_the_CM_prime=1")
    print("conclusion=reported_packetized_content_selected_prime_scan")


if __name__ == "__main__":
    main()
