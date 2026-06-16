#!/usr/bin/env python3
"""Augmentation-order scan for relative CM packets.

For a packet factor f | Phi_n, write the relative-content vector as

    V(Y) = sum_u J_u(zeta) Y^u.

The two-moment certificate {M0,M1} is the statement that no nonzero packet
vector has a double zero at Y=1.  This script tests the sharper invariant:
the first nonzero Hasse derivative of V at Y=1, i.e. the largest power of the
augmentation ideal (Y-1) containing the packet vector.

For e=0,1 the Hasse derivatives agree with M0 and M1 up to the harmless
coefficient convention used in relative_moment_projection_scan.py.  Higher
orders are useful diagnostics for whether pair failures should be expected
randomly or whether CM packets avoid the square of the augmentation ideal.
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
class AugmentationRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    content_zero: bool
    first_nonzero_hasse: int | None
    zero_prefix: int
    origin_shift: int
    section: str


def first_nonzero_hasse_order(
    residues: list[sp.Poly],
    factor: sp.Poly,
    q: int,
    max_order: int,
) -> tuple[int | None, int]:
    """Return the first nonzero Hasse derivative at Y=1."""
    zero_prefix = 0
    var = factor.gens[0]
    for order in range(max_order + 1):
        total = sp.Poly(0, var, modulus=q)
        for u, residue in enumerate(residues):
            coeff = int(sp.binomial(u, order)) % q
            if coeff:
                total = (total + coeff * residue).rem(factor)
        if not total.is_zero:
            return order, zero_prefix
        zero_prefix += 1
    return None, zero_prefix


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    max_order: int,
    origin_shift: int,
    section: str,
) -> AugmentationRow:
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, section)
    ]
    content_zero = all(residue.is_zero for residue in residues)
    first, prefix = first_nonzero_hasse_order(residues, factor, q, max_order)
    h = len(cycle)
    n = h // m
    return AugmentationRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        content_zero=content_zero,
        first_nonzero_hasse=first,
        zero_prefix=prefix,
        origin_shift=origin_shift,
        section=section,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[AugmentationRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[AugmentationRow] = []
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

        case_had_full_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_full_cycle = True
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
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
                                shifted,
                                m,
                                factor,
                                args.max_order,
                                shift,
                                args.section,
                            )
                        )
        if case_had_full_cycle:
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
    parser.add_argument("--section", choices=("contiguous", "complement"), default="complement")
    parser.add_argument("--max-order", type=int, default=4)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    nonzero_rows = [row for row in rows if not row.content_zero]
    content_failures = [row for row in rows if row.content_zero]
    hist: dict[str, int] = {}
    for row in rows:
        key = "content_zero" if row.content_zero else (
            f">{args.max_order}"
            if row.first_nonzero_hasse is None
            else str(row.first_nonzero_hasse)
        )
        hist[key] = hist.get(key, 0) + 1

    pair_failures = [
        row for row in nonzero_rows
        if row.first_nonzero_hasse is None or row.first_nonzero_hasse > 1
    ]
    first_order_failures = [
        row for row in nonzero_rows
        if row.first_nonzero_hasse is None or row.first_nonzero_hasse > 0
    ]
    expected_prefix = {
        r: sum(row.q ** (-r * row.factor_degree) for row in nonzero_rows)
        for r in range(1, min(args.max_order, 4) + 1)
    }

    print("relative augmentation-order scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"section={args.section}")
    print(f"scan_origins={args.scan_origins}")
    print(f"include_linear={args.include_linear}")
    print(f"max_order={args.max_order}")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin content_zero "
            "first_nonzero_hasse zero_prefix section"
        )
        for row in rows:
            interesting = (
                row.content_zero
                or row.first_nonzero_hasse is None
                or row.first_nonzero_hasse > 0
            )
            if interesting:
                first = (
                    "NA"
                    if row.first_nonzero_hasse is None
                    else str(row.first_nonzero_hasse)
                )
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                    f"deg={row.factor_degree:3d} origin={row.origin_shift:3d} "
                    f"content_zero={int(row.content_zero)} "
                    f"first_nonzero_hasse={first:>2s} "
                    f"zero_prefix={row.zero_prefix:2d} section={row.section}"
                )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  nonzero_packet_rows={len(nonzero_rows)}")
    print(f"  content_failures={len(content_failures)}")
    print(f"  first_order_failures={len(first_order_failures)}")
    print(f"  pair_failures={len(pair_failures)}")
    print(f"  augmentation_histogram={dict(sorted(hist.items()))}")
    for r, value in expected_prefix.items():
        print(f"  expected_prefix_{r}_zeros_random={value:.6f}")
    if pair_failures:
        print("  pair_failure_samples:")
        for row in pair_failures[:8]:
            first = (
                "NA"
                if row.first_nonzero_hasse is None
                else str(row.first_nonzero_hasse)
            )
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin={row.origin_shift} "
                f"first={first} section={row.section}"
            )
    print()
    print("interpretation")
    print("  first_order_failure means M0 vanishes but the packet is nonzero")
    print("  pair_failure means the {M0,M1} certificate misses a nonzero packet")
    print("  no pair failures supports relative augmentation order < 2")
    print("conclusion=reported_relative_augmentation_order_scan")


if __name__ == "__main__":
    main()
