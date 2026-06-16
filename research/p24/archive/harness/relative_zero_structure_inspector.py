#!/usr/bin/env python3
"""Inspect relative-coordinate zero packets in small CM cycles.

This is a narrow companion to `relative_normality_prime_composite_scan.py`.
When a coordinate `J_u mod f` vanishes, it prints the offending fiber
coefficients and tests whether the length-`n` sequence is pulled back from a
proper quotient period.  Composite failures in the current scans are expected
to have this imprimitive shape.
"""

from __future__ import annotations

import argparse

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from packetized_relative_content_scan import fiber_polynomials, packet_factors


def proper_periods(values: list[int]) -> list[int]:
    n = len(values)
    out: list[int] = []
    for d in sorted(int(x) for x in sp.divisors(n)):
        if d == n:
            continue
        if all(values[k] == values[k % d] for k in range(n)):
            out.append(d)
    return out


def rotate(cycle: list[int], shift: int) -> list[int]:
    if shift == 0:
        return cycle
    return cycle[shift:] + cycle[:shift]


def roots_of_factor(factor: sp.Poly, q: int) -> list[int]:
    roots: list[int] = []
    for x in range(q):
        if int(factor.eval(x)) % q == 0:
            roots.append(x)
    return roots


def inspect_case(D: int, q_start: int, q_stop: int, min_n: int, max_n: int) -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    h = int(pari.poldegree(hilbert))
    split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
    if split is None:
        raise SystemExit("no split prime found")
    q, roots = split
    full = find_full_cycle_prime(roots, D, q)
    if full is None:
        raise SystemExit("no full cycle found")
    ell, cycle = full

    print("relative zero structure inspector")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={h}")
    print(f"min_n={min_n}")
    print(f"max_n={max_n}")
    print()
    print(
        "columns: m n n_prime factor_degree roots shift u proper_periods "
        "coefficients"
    )
    hits = 0
    for n in sorted(int(d) for d in sp.divisors(h)):
        if n < min_n or n > max_n or n >= h:
            continue
        m = h // n
        if m < 2:
            continue
        for factor in packet_factors(n, q):
            for shift in range(h):
                shifted = rotate(cycle, shift)
                fibers = fiber_polynomials(shifted, q, m)
                for u, fiber in enumerate(fibers):
                    if fiber.rem(factor).is_zero:
                        coeffs = [
                            shifted[u + m * k] % q
                            for k in range(n)
                        ]
                        print(
                            f"m={m:3d} n={n:3d} n_prime={int(sp.isprime(n))} "
                            f"deg={factor.degree():2d} roots={roots_of_factor(factor, q)} "
                            f"shift={shift:3d} u={u:3d} "
                            f"proper_periods={proper_periods(coeffs)} "
                            f"coeffs={coeffs}"
                        )
                        hits += 1
    print()
    print(f"zero_coordinate_hits={hits}")
    print("conclusion=reported_relative_zero_structure")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, required=True)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=300000)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=20)
    args = ap.parse_args()
    inspect_case(args.D, args.q_start, args.q_stop, args.min_n, args.max_n)


if __name__ == "__main__":
    main()
