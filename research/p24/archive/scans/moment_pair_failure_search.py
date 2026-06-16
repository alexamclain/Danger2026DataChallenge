#!/usr/bin/env python3
"""Early-exit search for failures of the {M0,M1} packet certificate.

The relative moment scan aggregates all rows before printing.  This script is
for quick falsification attempts: it stops as soon as it finds a nonzero
relative-content packet where both M0 and M1 vanish modulo a Frobenius factor.
"""

from __future__ import annotations

import argparse

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_decomposition_calibration import pari_linear_roots
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    audit_packet,
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [D for D in range(-200, -max_abs_D - 1, -1) if D % 4 in (0, 1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--section", choices=("contiguous", "complement"), default="complement")
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    tested = 0
    cases = 0
    m0_failures = 0
    seen: set[int] = set()

    print("moment pair failure search")
    print(f"section={args.section}")
    print(f"max_cases={args.max_cases}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"scan_origins={args.scan_origins}")
    print()

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
                        row = audit_packet(
                            D,
                            q,
                            ell,
                            shifted,
                            m,
                            factor,
                            1,
                            shift,
                            args.section,
                        )
                        tested += 1
                        if not row.content_zero and (
                            row.first_nonzero_moment is None
                            or row.first_nonzero_moment > 0
                        ):
                            m0_failures += 1
                        if not row.content_zero and (
                            row.first_nonzero_moment is None
                            or row.first_nonzero_moment > 1
                        ):
                            print("found_moment_pair_failure=1")
                            print(
                                f"D={row.D} q={row.q} ell={row.ell} h={row.h} "
                                f"m={row.m} n={row.n} n_prime={int(row.n_is_prime)} "
                                f"factor_degree={row.factor_degree} origin={row.origin_shift} "
                                f"coord_zero={row.coord_zero_count} section={row.section}"
                            )
                            print(f"tested_packets={tested}")
                            print(f"m0_failures_before_hit={m0_failures}")
                            print("conclusion=moment_pair_failure_found")
                            return
        if case_had_full_cycle:
            cases += 1
            if cases >= args.max_cases:
                break

    print("found_moment_pair_failure=0")
    print(f"cases={cases}")
    print(f"tested_packets={tested}")
    print(f"m0_failures={m0_failures}")
    print("conclusion=no_moment_pair_failure_in_search_window")


if __name__ == "__main__":
    main()
