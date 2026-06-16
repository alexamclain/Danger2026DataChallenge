#!/usr/bin/env python3
"""Exact trace-CRT construction barrier for p24.

An apparent escape from CM root selection is to impose enough Frobenius
eigenvalue / trace residue data to isolate the strict traces.  As information,
this is easy: trace modulo a product N larger than the Hasse width isolates a
trace.  As construction, however, imposing exact trace residues is modular
level structure.  A Gamma0(N)-style condition has degree at least on the order
of [SL2:Gamma0(N)] ~ N, while oriented X1 data is larger.

For p24 the strict 2-adic condition already uses N=2^40, essentially sqrt(p).
Adding odd CRT residues can improve constants or distinguish the three
representatives, but it cannot change the exponent in this construction model.
"""

from __future__ import annotations

from fractions import Fraction
import math

import sympy as sp

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
K = 40
TWO_LEVEL = 1 << K
TARGET_TRACES = (
    -1178414874616,
    -1020608380936,
    -78903246840,
    78903246840,
    1020608380936,
    1178414874616,
)


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError(value)
    return value.numerator


def hasse_count_for_residues(modulus: int) -> int:
    bound = math.isqrt(4 * P24)
    residues = {t % modulus for t in TARGET_TRACES}
    seen: set[int] = set()
    for residue in residues:
        first = -bound + ((residue + bound) % modulus)
        t = first
        while t <= bound:
            seen.add(t)
            t += modulus
    return len(seen)


def main() -> None:
    print("p24 exact trace-CRT modular-degree barrier")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"k={K}")
    print(f"2^k={TWO_LEVEL}")
    print(f"2^k_over_sqrt={TWO_LEVEL / SQRT_P:.6f}")
    print()
    print("level odd_part level_over_sqrt gamma0_over_sqrt target_residue_count hasse_survivors")
    for odd in (1, 3, 5, 7, 11, 15, 21, 35, 105, 3 * 5 * 7 * 11, 3 * 5 * 7 * 11 * 13):
        level = TWO_LEVEL * odd
        residues = len({t % level for t in TARGET_TRACES})
        survivors = hasse_count_for_residues(level)
        gamma0 = gamma0_index(level)
        print(
            f"{level:18d} {odd:8d} {level / SQRT_P:15.6f} "
            f"{gamma0 / SQRT_P:17.6f} {residues:20d} {survivors:15d}"
        )
    print()
    print("interpretation")
    print("  trace_residue_modulus_above_hasse_width_is_information_sufficient=1")
    print("  imposing_trace_residue_constructively_has_modular_level_cost=1")
    print("  p24_two_adic_level_already_has_gamma0_degree_constant_times_sqrt=1")
    print("  odd_crt_residues_can_improve_constants_but_not_the_exponent=1")
    print(
        "conclusion=exact_trace_crt_construction_repackages_the_sqrt_scale_"
        "modular_degree_barrier"
    )


if __name__ == "__main__":
    main()
