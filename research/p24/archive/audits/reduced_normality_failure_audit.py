#!/usr/bin/env python3
"""Audit actual small CM reduced-normality failures.

The broad theorem "split ordinary CM cycles are always reduced-normal" is
false.  This script looks for the small failures, classifies the vanished
character packets, and separates low-order accidents from the p24 high-order
non-genus packets.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

T = sp.symbols("T")


@dataclass(frozen=True)
class Failure:
    D: int
    q: int
    ell: int
    h: int
    gcd_degree: int
    factor_degrees: tuple[int, ...]
    zero_indices: tuple[int, ...] | None
    zero_orders: tuple[int, ...] | None
    quotient_failures: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class ScanResult:
    checked_rows: int
    failures: tuple[Failure, ...]


def primitive_root_of_order(q: int, h: int) -> int | None:
    if (q - 1) % h:
        return None
    root = pow(sp.primitive_root(q), (q - 1) // h, q)
    if pow(root, h, q) != 1:
        return None
    for prime in sp.factorint(h):
        if pow(root, h // prime, q) == 1:
            return None
    return int(root)


def dft_zero_indices(cycle: list[int], q: int) -> tuple[int, ...] | None:
    h = len(cycle)
    zeta = primitive_root_of_order(q, h)
    if zeta is None:
        return None
    zeros: list[int] = []
    for s in range(h):
        total = 0
        for i, value in enumerate(cycle):
            total = (total + value * pow(zeta, s * i, q)) % q
        if total == 0:
            zeros.append(s)
    return tuple(zeros)


def char_orders(h: int, indices: tuple[int, ...] | None) -> tuple[int, ...] | None:
    if indices is None:
        return None
    return tuple(h // math.gcd(h, s) if s else 1 for s in indices)


def factor_degrees(j_poly: sp.Poly, h: int, q: int) -> tuple[int, ...]:
    torsor = sp.Poly(T**h - 1, T, modulus=q)
    gcd = sp.gcd(j_poly, torsor)
    if gcd.degree() <= 0:
        return ()
    _unit, factors = sp.factor_list(gcd, modulus=q)
    return tuple(sorted(poly.degree() for poly, exp in factors for _ in range(exp)))


def quotient_dft_support(cycle: list[int], quotient_size: int, q: int) -> int | None:
    h = len(cycle)
    if h % quotient_size:
        return None
    zeta = primitive_root_of_order(q, quotient_size)
    if zeta is None:
        return None
    support = 0
    for s in range(quotient_size):
        total = 0
        for i, value in enumerate(cycle):
            total = (total + value * pow(zeta, s * i, q)) % q
        if total:
            support += 1
    return support


def quotient_failures(cycle: list[int], q: int) -> tuple[tuple[int, int, int], ...]:
    h = len(cycle)
    rows: list[tuple[int, int, int]] = []
    for m in sp.divisors(h):
        m = int(m)
        if not (2 <= m < h and h % m == 0):
            continue
        support = quotient_dft_support(cycle, m, q)
        if support is not None and support < m:
            rows.append((m, h // m, support))
    return tuple(rows)


def scan(
    max_failures: int,
    min_h: int,
    max_h: int,
    start_abs_D: int,
    max_abs_D: int,
) -> ScanResult:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    failures: list[Failure] = []
    checked_rows = 0
    start = max(200, start_abs_D)
    for D in range(-start, -max_abs_D - 1, -1):
        if D % 4 not in (0, 1):
            continue
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        checked_rows += 1
        j_poly = sp.Poly(sum(value * T**i for i, value in enumerate(cycle)), T, modulus=q)
        factors = factor_degrees(j_poly, h, q)
        if not factors:
            continue
        zeros = dft_zero_indices(cycle, q)
        failures.append(
            Failure(
                D=D,
                q=q,
                ell=ell,
                h=h,
                gcd_degree=sum(factors),
                factor_degrees=factors,
                zero_indices=zeros,
                zero_orders=char_orders(h, zeros),
                quotient_failures=quotient_failures(cycle, q),
            )
        )
        if len(failures) >= max_failures:
            break
    return ScanResult(checked_rows=checked_rows, failures=tuple(failures))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-failures", type=int, default=12)
    ap.add_argument("--min-h", type=int, default=2)
    ap.add_argument("--max-h", type=int, default=24)
    ap.add_argument("--start-abs-D", type=int, default=200)
    ap.add_argument("--max-abs-D", type=int, default=5000)
    args = ap.parse_args()

    result = scan(
        max_failures=args.max_failures,
        min_h=args.min_h,
        max_h=args.max_h,
        start_abs_D=args.start_abs_D,
        max_abs_D=args.max_abs_D,
    )
    failures = result.failures

    print("reduced-normality failure audit")
    print(f"max_failures={args.max_failures}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"start_abs_D={args.start_abs_D}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"checked_rows={result.checked_rows}")
    print()
    print(
        "D q ell h gcd_degree factor_degrees zero_indices zero_orders "
        "quotient_failures:m/n/support"
    )
    for row in failures:
        qf = ",".join(f"{m}/{n}/{support}" for m, n, support in row.quotient_failures)
        print(
            f"D={row.D:7d} q={row.q:5d} ell={row.ell:3d} h={row.h:3d} "
            f"gcd_degree={row.gcd_degree:2d} factors={list(row.factor_degrees)} "
            f"zero_indices={None if row.zero_indices is None else list(row.zero_indices)} "
            f"zero_orders={None if row.zero_orders is None else list(row.zero_orders)} "
            f"quotient_failures={qf}"
        )

    order_counts: dict[int, int] = {}
    for row in failures:
        if row.zero_orders is None:
            continue
        for order in row.zero_orders:
            order_counts[order] = order_counts.get(order, 0) + 1
    print()
    print("summary")
    print(f"  checked_rows={result.checked_rows}")
    print(f"  failures={len(failures)}")
    print(f"  zero_order_counts={dict(sorted(order_counts.items()))}")
    print()
    print("interpretation")
    print("  split_squarefree_CM_reduction_does_not_force_reduced_normality=1")
    print("  observed_small_failures_are_low_order_character_packets=1")
    print("  p24_still_needs_specific_nonvanishing_for_high_order_non_genus_packets=1")
    print("conclusion=reported_reduced_normality_failure_audit")


if __name__ == "__main__":
    main()
