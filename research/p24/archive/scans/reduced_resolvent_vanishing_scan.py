#!/usr/bin/env python3
"""Scan reduced CM cycles for class-character resolvent vanishing.

For a cyclic embedded CM torsor

    j_i = g^i(j_0),  0 <= i < h,

form

    J(T) = sum_i j_i T^i in F_q[T]/(T^h - 1).

Over an algebraic closure, evaluating J at h-th roots of unity gives the
class-character resolvents.  Thus

    gcd(J(T), T^h - 1)

records exactly which character packets vanish after reduction.  A zero gcd
degree means the reduced CM element is normal and every additive subgroup
projector support lower bound is faithful.

This is a toy-scale analogue of the p24 reduced-normality gap.  It does not
prove the p24 target, but it checks whether p-specific character collapses are
common in complete small embedded CM cycles, especially non-genus quotient
layers.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

T = sp.symbols("T")


@dataclass(frozen=True)
class VanishingRow:
    D: int
    q: int
    ell: int
    h: int
    gcd_degree: int
    vanished_factor_degrees: tuple[int, ...]
    quotient_rows: tuple[tuple[int, int, int | None], ...]


def poly_from_cycle(cycle: list[int], q: int) -> sp.Poly:
    return sp.Poly(sum(value * T**i for i, value in enumerate(cycle)), T, modulus=q)


def vanished_factor_degrees(j_poly: sp.Poly, h: int, q: int) -> tuple[int, ...]:
    torsor = sp.Poly(T**h - 1, T, modulus=q)
    gcd = sp.gcd(j_poly, torsor)
    if gcd.degree() <= 0:
        return ()
    coeff, factors = sp.factor_list(gcd, modulus=q)
    return tuple(sorted(poly.degree() for poly, exp in factors for _ in range(exp)))


def primitive_root_of_order(q: int, order: int) -> int | None:
    if (q - 1) % order:
        return None
    root = pow(sp.primitive_root(q), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        return None
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            return None
    return int(root)


def quotient_dft_support(cycle: list[int], quotient: int, q: int) -> int | None:
    """Return support of quotient character traces when mu_quotient <= F_q."""
    h = len(cycle)
    if h % quotient:
        return None
    zeta = primitive_root_of_order(q, quotient)
    if zeta is None:
        return None
    support = 0
    for s in range(quotient):
        total = 0
        for i, value in enumerate(cycle):
            total = (total + value * pow(zeta, s * i, q)) % q
        if total:
            support += 1
    return support


def quotient_rows(cycle: list[int], q: int) -> tuple[tuple[int, int, int | None], ...]:
    h = len(cycle)
    rows: list[tuple[int, int, int | None]] = []
    for m in sorted(sp.divisors(h)):
        if 2 <= m <= min(30, h // 2) and h % m == 0:
            n = h // m
            rows.append((int(m), int(n), quotient_dft_support(cycle, int(m), q)))
    return tuple(rows[:6])


def scan(max_cases: int, min_h: int, max_h: int, max_abs_D: int) -> list[VanishingRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]

    rows: list[VanishingRow] = []
    seen: set[int] = set()
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
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        j_poly = poly_from_cycle(cycle, q)
        factors = vanished_factor_degrees(j_poly, h, q)
        rows.append(
            VanishingRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                gcd_degree=sum(factors),
                vanished_factor_degrees=factors,
                quotient_rows=quotient_rows(cycle, q),
            )
        )
        if len(rows) >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=12)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=96)
    ap.add_argument("--max-abs-D", type=int, default=12000)
    args = ap.parse_args()

    rows = scan(args.max_cases, args.min_h, args.max_h, args.max_abs_D)

    print("reduced resolvent vanishing scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print()
    print("columns: D q ell h gcd_degree vanished_factor_degrees quotient:m/n/support")
    for row in rows:
        quotient_text = ",".join(
            f"{m}/{n}/{'NA' if support is None else support}"
            for m, n, support in row.quotient_rows
        )
        print(
            f"D={row.D:7d} q={row.q:5d} ell={row.ell:2d} h={row.h:3d} "
            f"gcd_degree={row.gcd_degree:2d} vanished_factors={list(row.vanished_factor_degrees)} "
            f"quotients={quotient_text}"
        )

    normal_count = sum(1 for row in rows if row.gcd_degree == 0)
    q_support_rows = [
        (m, support)
        for row in rows
        for m, _n, support in row.quotient_rows
        if support is not None
    ]
    full_support_rows = sum(1 for m, support in q_support_rows if support == m)
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  normal_rows={normal_count}")
    print(f"  nonnormal_rows={len(rows) - normal_count}")
    print(f"  quotient_dft_rows_with_roots={len(q_support_rows)}")
    print(f"  quotient_dft_full_support_rows={full_support_rows}")
    print()
    print("interpretation")
    print("  gcd_degree_zero_means_no_class_character_resolvent_vanishes_mod_q=1")
    print("  quotient_support_m_means_all_m_quotient_character_traces_are_nonzero=1")
    print("  toy_scan_tests_p_specific_reduced_normality_failures_at_small_scale=1")
    print("conclusion=reported_reduced_resolvent_vanishing_scan")


if __name__ == "__main__":
    main()
