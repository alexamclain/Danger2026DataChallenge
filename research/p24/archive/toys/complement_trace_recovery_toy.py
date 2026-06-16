#!/usr/bin/env python3
"""Build a complement-trace quotient and recovery relation in a small CM cycle.

This is the toy version of the p24 complement-trace route:

    h = m*n, gcd(m,n)=1,
    Y_k = sum_r j_{n*r + m*k}.

The values Y_k form a degree-n quotient object.  Above each Y_k sits a
degree-m recovery polynomial whose roots are the K-orbit

    {j_{n*r + m*k} : 0 <= r < m}.

The script constructs the quotient polynomial and the interpolated recovery
relation from an embedded CM cycle, then verifies the specializations.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

Y = sp.symbols("Y")
J = sp.symbols("J")


@dataclass(frozen=True)
class ToyResult:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    quotient_values: tuple[int, ...]
    quotient_poly: sp.Poly
    relation_coeffs: tuple[sp.Poly, ...]
    all_specializations_ok: bool
    quotient_values_distinct: bool
    relation_degree_y_max: int


def inv_mod(value: int, q: int) -> int:
    return pow(value % q, -1, q)


def lagrange_interpolate(points: list[tuple[int, int]], q: int) -> sp.Poly:
    total = sp.Poly(0, Y, modulus=q)
    for x_i, y_i in points:
        numer = sp.Poly(1, Y, modulus=q)
        denom = 1
        for x_j, _ in points:
            if x_i == x_j:
                continue
            numer *= sp.Poly(Y - x_j, Y, modulus=q)
            denom = (denom * (x_i - x_j)) % q
        total += (y_i * inv_mod(denom, q)) * numer
    return sp.Poly(total.as_expr(), Y, modulus=q)


def complement_trace_values(cycle: list[int], q: int, m: int) -> list[int]:
    h = len(cycle)
    n = h // m
    if sp.gcd(m, n) != 1:
        raise ValueError("complement trace requires gcd(m,n)=1")
    return [
        sum(cycle[(n * r + m * k) % h] for r in range(m)) % q
        for k in range(n)
    ]


def fiber_poly(cycle: list[int], q: int, m: int, k: int) -> sp.Poly:
    h = len(cycle)
    n = h // m
    poly = sp.Poly(1, J, modulus=q)
    for r in range(m):
        poly *= sp.Poly(J - cycle[(n * r + m * k) % h], J, modulus=q)
    return poly.monic()


def quotient_poly_from_values(values: list[int], q: int) -> sp.Poly:
    poly = sp.Poly(1, Y, modulus=q)
    for value in values:
        poly *= sp.Poly(Y - value, Y, modulus=q)
    return poly.monic()


def build_recovery_relation(
    cycle: list[int],
    q: int,
    m: int,
) -> tuple[list[int], sp.Poly, list[sp.Poly], bool]:
    values = complement_trace_values(cycle, q, m)
    if len(set(values)) != len(values):
        raise ValueError("quotient trace values collide; cannot interpolate")
    h = len(cycle)
    n = h // m
    fiber_polys = [fiber_poly(cycle, q, m, k) for k in range(n)]

    # Coefficients are in ascending J-degree order.
    coeff_tables: list[list[tuple[int, int]]] = [[] for _ in range(m)]
    for y_value, poly in zip(values, fiber_polys):
        coeffs = [0] * (m + 1)
        for (degree,), coeff in poly.as_dict().items():
            coeffs[degree] = int(coeff) % q
        if coeffs[m] != 1:
            raise AssertionError("fiber polynomial was not monic")
        for degree in range(m):
            coeff_tables[degree].append((y_value, coeffs[degree]))

    coeff_polys = [lagrange_interpolate(table, q) for table in coeff_tables]

    ok = True
    for y_value, expected in zip(values, fiber_polys):
        reconstructed = sp.Poly(J**m, J, modulus=q)
        for degree, coeff_poly in enumerate(coeff_polys):
            value = int(coeff_poly.eval(y_value)) % q
            reconstructed += sp.Poly(value * J**degree, J, modulus=q)
        if reconstructed.monic() != expected:
            ok = False
            break
    return values, quotient_poly_from_values(values, q), coeff_polys, ok


def find_case(
    D: int | None,
    q_start: int,
    q_stop: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    preferred_m: int | None,
) -> tuple[int, int, int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [D] if D is not None else [-5000] + [
        disc for disc in range(-200, -max_abs_D - 1, -1)
        if disc % 4 in (0, 1)
    ]
    seen: set[int] = set()
    for disc in discriminants:
        if disc in seen:
            continue
        seen.add(disc)
        try:
            hilbert = pari.polclass(disc)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        if preferred_m is not None:
            if h % preferred_m or sp.gcd(preferred_m, h // preferred_m) != 1:
                continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, disc, q)
        if full is None:
            continue
        ell, cycle = full
        return disc, q, ell, cycle
    raise RuntimeError("no suitable case found")


def choose_m(h: int, preferred_m: int | None) -> int:
    if preferred_m is not None:
        return preferred_m
    candidates = [
        int(d)
        for d in sp.divisors(h)
        if 2 <= d < h and sp.gcd(int(d), h // int(d)) == 1
    ]
    if not candidates:
        raise ValueError("no coprime factor split available")
    return min(candidates, key=lambda d: (abs(d - h // d), d))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=150000)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=90)
    ap.add_argument("--max-abs-D", type=int, default=15000)
    ap.add_argument("--m", type=int)
    args = ap.parse_args()

    D, q, ell, cycle = find_case(
        D=args.D,
        q_start=args.q_start,
        q_stop=args.q_stop,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        preferred_m=args.m,
    )
    h = len(cycle)
    m = choose_m(h, args.m)
    n = h // m
    values, quotient_poly, coeff_polys, ok = build_recovery_relation(cycle, q, m)
    relation_degree_y_max = max(poly.degree() for poly in coeff_polys)

    print("complement trace recovery toy")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"gcd_m_n={sp.gcd(m,n)}")
    print(f"quotient_values_distinct={int(len(set(values)) == len(values))}")
    print(f"all_specializations_ok={int(ok)}")
    print(f"quotient_poly_degree={quotient_poly.degree()}")
    print(f"recovery_degree_in_J={m}")
    print(f"relation_degree_y_max={relation_degree_y_max}")
    print(f"quotient_values={values}")
    print(f"quotient_poly={quotient_poly.as_expr()}")
    print("recovery_relation_coefficients_ascending_J_degree:")
    for degree, coeff_poly in enumerate(coeff_polys):
        print(f"  J^{degree}: {coeff_poly.as_expr()}")
    print()
    print("interpretation")
    print("  complement_trace_polynomial_degree_equals_n=1")
    print("  recovery_specialization_degree_equals_m=1")
    print("  relation_built_from_embedded_cycle_not_abstract_tower=1")
    print("conclusion=reported_complement_trace_recovery_toy")


if __name__ == "__main__":
    main()
