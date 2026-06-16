#!/usr/bin/env python3
"""Audit Atkin-Lehner/Fricke quotient limits for the smooth p24 CM lead.

The smooth third target tempts one to use odd-level modular invariants.  A
function on an Atkin-Lehner quotient X0(N)/W can have a smaller map to the
j-line than X0(N), and known class invariants often exploit these symmetries.

This script quantifies the maximum possible saving from the obvious normalizer
symmetries.  For squarefree N, the Atkin-Lehner group has size 2^omega(N).
Even granting the full quotient, this is tiny compared with the desired class
stabilizers 157, 211, or 3107441.  It can improve constants and heights, but
it cannot manufacture the large odd class-field quotient by itself.
"""

from __future__ import annotations

from fractions import Fraction
import math

import sympy as sp


P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014

LEVELS = [
    23,
    157,
    211,
    677,
    2897,
    7349,
    14057,
    3107441,
    157 * 211,
    157 * 3107441,
    211 * 3107441,
    157 * 211 * 3107441,
]


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def atkin_lehner_size(n: int) -> int:
    # Upper bound for squarefree N; enough for these squarefree levels.
    return 1 << len(sp.factorint(n))


def main() -> None:
    print("p24 Atkin-Lehner quotient limit audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"factor_class_number={sp.factorint(CLASS_NUMBER)}")
    print()
    print(
        "level split gamma0_index full_AL_size quotient_degree_lb "
        "quotient_degree_over_sqrt desired_class_stabilizer_gap"
    )

    desired_stabilizers = [157, 211, 3107441, 66254, 157 * 211, 157 * 211 * 3107441]
    for level in LEVELS:
        idx = gamma0_index(level)
        al = atkin_lehner_size(level)
        quotient_lb = math.ceil(idx / al)
        split = sp.kronecker_symbol(D_K, level) if math.gcd(D_K, level) == 1 else 0
        gap = min(stab / al for stab in desired_stabilizers if stab >= al)
        print(
            f"{level:15d} {int(split):5d} {idx:12d} {al:12d} "
            f"{quotient_lb:18d} {quotient_lb / SQRT_P:25.6e} "
            f"{gap:28.6e}"
        )

    print()
    print("desired_class_stabilizers")
    for stabilizer in desired_stabilizers:
        quotient_degree = CLASS_NUMBER // stabilizer if CLASS_NUMBER % stabilizer == 0 else None
        print(
            f"  stabilizer={stabilizer:12d} "
            f"quotient_degree={quotient_degree if quotient_degree is not None else 'n/a'} "
            f"stabilizer_bits={math.log2(stabilizer):.3f}"
        )

    print()
    print("interpretation")
    print("  full_Atkin_Lehner_quotient_available_only_saves_2^omega_N=1")
    print("  required_smooth_class_stabilizer_can_be_3107441_or_66254=1")
    print("  normalizer_symmetry_is_not_the_same_as_class_subgroup_stabilizer=1")
    print(
        "conclusion=Atkin_Lehner_or_Fricke_quotients_change_constants_but_do_"
        "not_supply_the_large_odd_class_field_quotient_needed_for_p24"
    )


if __name__ == "__main__":
    main()
