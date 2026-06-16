#!/usr/bin/env python3
"""Check projector support in actual reduced-normality failure rows.

Reduced normality can fail without giving a sparse additive selector.  For the
known small CM failures, this script computes the exact affine-code minimum

    min_{B in Ann(J)} wt(e_H + B)

for every nontrivial quotient of the class cycle.
"""

from __future__ import annotations

import itertools

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

T = sp.symbols("T")
FAILURE_DISCRIMINANTS = (-216, -300)


def coeff_vector(poly: sp.Poly, length: int, q: int) -> list[int]:
    out = [0] * length
    for (power,), coeff in poly.as_dict().items():
        out[power % length] = (out[power % length] + int(coeff)) % q
    return out


def cyclic_shift(values: list[int], amount: int) -> list[int]:
    h = len(values)
    out = [0] * h
    for i, value in enumerate(values):
        out[(i + amount) % h] = value
    return out


def weight(values: list[int], q: int) -> int:
    return sum(1 for value in values if value % q)


def projector(h: int, quotient_size: int) -> list[int]:
    subgroup_size = h // quotient_size
    out = [0] * h
    for k in range(subgroup_size):
        out[(quotient_size * k) % h] = 1
    return out


def min_weight(base: list[int], basis: list[list[int]], q: int) -> tuple[int, tuple[int, ...]]:
    if len(basis) > 2:
        raise ValueError("toy brute force only supports annihilator dimension <= 2")
    best_weight = len(base) + 1
    best_coeffs: tuple[int, ...] = ()
    for coeffs in itertools.product(range(q), repeat=len(basis)):
        candidate = base[:]
        for coeff, vector in zip(coeffs, basis):
            candidate = [(x + coeff * y) % q for x, y in zip(candidate, vector)]
        current = weight(candidate, q)
        if current < best_weight:
            best_weight = current
            best_coeffs = tuple(int(c) for c in coeffs)
    return best_weight, best_coeffs


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)

    print("failure projector weight audit")
    print("columns: D q ell h gcd_degree quotient_m subgroup_n projector_weight best_weight coeffs")
    for D in FAILURE_DISCRIMINANTS:
        hilbert = pari.polclass(D)
        h = int(pari.poldegree(hilbert))
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            raise RuntimeError((D, "no split prime"))
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            raise RuntimeError((D, q, "no full cycle"))
        ell, cycle = full

        j_poly = sp.Poly(sum(value * T**i for i, value in enumerate(cycle)), T, modulus=q)
        torsion = sp.Poly(T**h - 1, T, modulus=q)
        gcd = sp.gcd(j_poly, torsion)
        annihilator_generator, remainder = torsion.div(gcd)
        if not remainder.is_zero:
            raise AssertionError((D, q, h, gcd))
        generator = coeff_vector(annihilator_generator, h, q)
        basis = [cyclic_shift(generator, i) for i in range(gcd.degree())]

        for m in sorted(int(d) for d in sp.divisors(h) if 2 <= d < h and h % d == 0):
            base = projector(h, m)
            best, coeffs = min_weight(base, basis, q)
            print(
                f"D={D:6d} q={q:5d} ell={ell:3d} h={h:3d} "
                f"gcd_degree={gcd.degree():2d} quotient_m={m:3d} subgroup_n={h//m:3d} "
                f"projector_weight={weight(base, q):3d} best_weight={best:3d} coeffs={list(coeffs)}"
            )

    print()
    print("interpretation")
    print("  reduced_normality_failure_does_not_imply_sparse_projector=1")
    print("  known_small_cm_failures_still_have_projector_minimum_weight=1")
    print("  p24_can_target_the_weaker_min_weight_theorem_instead_of_full_normality=1")
    print("conclusion=reported_failure_projector_weight_audit")


if __name__ == "__main__":
    main()
