#!/usr/bin/env python3
"""Qfbclassno-only shortlist for centered-marginal holdout rows.

The heavier centered candidate index has to build Hilbert class polynomials
and find splitting primes.  That is the right second stage, but broad scans
can stall there.  This script performs only the cheap first stage:

* class number by qfbclassno;
* quotient shapes h = m*n with coprime m,n;
* CRT component pairs with enough possible right orbit structure.

It deliberately does not claim that a splitting prime q with the displayed
orbit lengths exists.  It produces a small shape shortlist for targeted
polclass/splitting follow-up.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import discriminants
from relative_moment_projection_scan import quotient_sizes_any


@dataclass(frozen=True)
class ShapeRow:
    D: int
    h: int
    m: int
    n: int
    components: tuple[int, ...]
    left: int
    right: int
    possible_left_orbit_max: int
    possible_right_orbit_min: int
    possible_right_orbit_max: int
    axis_dim: int


def possible_orders(modulus: int) -> list[int]:
    if modulus <= 2:
        return []
    group_exponent = int(sp.functions.combinatorial.numbers.reduced_totient(modulus))
    return sorted(d for d in sp.divisors(group_exponent) if d > 1)


def possible_right_orbit_counts(modulus: int) -> list[int]:
    counts: set[int] = set()
    for order in possible_orders(modulus):
        if (modulus - 1) % order == 0:
            counts.add((modulus - 1) // order)
    return sorted(counts)


def scan(args: argparse.Namespace) -> list[ShapeRow]:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    rows: list[ShapeRow] = []
    seen: set[int] = set()
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            h = int(pari.qfbclassno(D))
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
        for m in quotient_sizes:
            n = h // m
            if gcd(m, n) != 1 or m > args.max_m:
                continue
            components = tuple(coprime_components(m))
            components_gt2 = tuple(c for c in components if c > 2)
            if len(components_gt2) < 2:
                continue
            axis_dim = 1 + sum(c - 1 for c in components)
            if axis_dim > args.max_axis_dim:
                continue
            for left in components_gt2:
                left_orders = possible_orders(left)
                if not left_orders:
                    continue
                left_max = max(left_orders)
                if left_max < args.min_possible_left_orbit:
                    continue
                for right in components_gt2:
                    right_counts = [
                        count
                        for count in possible_right_orbit_counts(right)
                        if args.min_possible_right_orbits
                        <= count
                        <= args.max_possible_right_orbits
                    ]
                    if not right_counts:
                        continue
                    rows.append(
                        ShapeRow(
                            D=D,
                            h=h,
                            m=m,
                            n=n,
                            components=components,
                            left=left,
                            right=right,
                            possible_left_orbit_max=left_max,
                            possible_right_orbit_min=min(right_counts),
                            possible_right_orbit_max=max(right_counts),
                            axis_dim=axis_dim,
                        )
                    )
                    if len(rows) >= args.max_rows:
                        return rows
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=80)
    parser.add_argument("--max-h", type=int, default=2000)
    parser.add_argument("--max-abs-D", type=int, default=500000)
    parser.add_argument("--max-prime-quotients", type=int, default=40)
    parser.add_argument("--max-composite-quotients", type=int, default=160)
    parser.add_argument("--min-n", type=int, default=5)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--max-m", type=int, default=800)
    parser.add_argument("--max-axis-dim", type=int, default=220)
    parser.add_argument("--min-possible-left-orbit", type=int, default=4)
    parser.add_argument("--min-possible-right-orbits", type=int, default=2)
    parser.add_argument("--max-possible-right-orbits", type=int, default=24)
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    rows = scan(args)
    print("Centered marginal shape shortlist")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"max_h={args.max_h}")
    print(f"max_rows={args.max_rows}")
    print()
    for row in rows:
        print(
            f"D={row.D} h={row.h} m={row.m} n={row.n} "
            f"components={list(row.components)} left={row.left}"
            f":Lmax{row.possible_left_orbit_max} right={row.right}"
            f":Rcount{row.possible_right_orbit_min}-{row.possible_right_orbit_max} "
            f"axis_dim={row.axis_dim}"
        )
    print()
    print("summary")
    print(f"  shape_rows={len(rows)}")
    if rows:
        print(f"  max_h={max(row.h for row in rows)}")
        print(f"  max_axis_dim={max(row.axis_dim for row in rows)}")
        print(f"  max_possible_left_orbit={max(row.possible_left_orbit_max for row in rows)}")
        print(f"  max_possible_right_orbits={max(row.possible_right_orbit_max for row in rows)}")
    print("conclusion=reported_centered_marginal_shape_shortlist")


if __name__ == "__main__":
    main()
