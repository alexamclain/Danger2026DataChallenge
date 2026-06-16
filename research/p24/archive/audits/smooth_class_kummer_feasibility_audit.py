#!/usr/bin/env python3
"""Audit Kummer/radical feasibility for the smooth third p24 class group.

The third strict target has cyclic class group order

    h = 2 * 157 * 211 * 3107441.

It is natural to ask whether the smoothness lets us compute one CM root by a
radical tower rather than by enumerating the full class group.  This script
checks the finite-field side of that idea.

If a cyclic degree-l class subextension were available by an explicit defining
polynomial, then solving a split degree-l polynomial over F_p is cheap for
small l.  But a Kummer/radical expression over F_p itself needs l-th roots of
unity, i.e. l | p-1.  Otherwise the radicals live over F_{p^ord_l(p)}.  For
the large factor this extension degree is already large, and in every case
the hard missing input is the explicit embedded subfield/relative polynomial.
"""

from __future__ import annotations

import math

import sympy as sp


P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
CLASS_FACTORS = [2, 157, 211, 3107441]
CLASS_ODD_PART = CLASS_NUMBER // 2
SQRT_P = math.isqrt(P24)


def multiplicative_order_mod_prime(a: int, ell: int) -> int:
    if math.gcd(a, ell) != 1:
        return 0
    return int(sp.n_order(a % ell, ell))


def main() -> None:
    print("p24 smooth-class Kummer feasibility audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"factor_class_number={sp.factorint(CLASS_NUMBER)}")
    print(f"p_minus_1_factors={sp.factorint(P24 - 1)}")
    print(f"p_plus_1_factors={sp.factorint(P24 + 1)}")
    print()

    print("cyclic_factor_kummer_table")
    print(
        "  ell divides_p_minus_1 p_mod_ell ord_p_mod_ell "
        "extension_degree_for_zeta ell_times_ord over_sqrt"
    )
    for ell in CLASS_FACTORS:
        if ell == 2:
            ord_p = 1
        else:
            ord_p = multiplicative_order_mod_prime(P24, ell)
        work_proxy = ell * ord_p
        print(
            f"  {ell:8d} {str((P24 - 1) % ell == 0):16s} "
            f"{P24 % ell:9d} {ord_p:13d} {ord_p:25d} "
            f"{work_proxy:13d} {work_proxy / SQRT_P:9.6e}"
        )
    odd_part_order = int(sp.n_order(P24 % CLASS_ODD_PART, CLASS_ODD_PART))
    print(
        f"  {'oddpart':>8s} {str((P24 - 1) % CLASS_ODD_PART == 0):16s} "
        f"{P24 % CLASS_ODD_PART:9d} {odd_part_order:13d} "
        f"{odd_part_order:25d} "
        f"{CLASS_ODD_PART * odd_part_order:13d} "
        f"{CLASS_ODD_PART * odd_part_order / SQRT_P:9.6e}"
    )
    print()

    print("tower_degree_accounting")
    remaining = CLASS_NUMBER
    for ell in CLASS_FACTORS:
        remaining //= ell
        print(
            f"  after_solving_factor={ell:8d} remaining_class_degree={remaining:15d} "
            f"remaining_over_sqrt={remaining / SQRT_P:.6e}"
        )
    print()

    print("field_interaction_gcds")
    for label, value in (
        ("p-1", P24 - 1),
        ("p+1", P24 + 1),
        ("curve_odd_order", (P24 + 1 - TRACE) >> 41),
        ("abs_DK", abs(D_K)),
    ):
        g = math.gcd(value, CLASS_NUMBER)
        print(f"  {label:16s} gcd_with_h={g:12d} factors={sp.factorint(g)}")
    print()

    print("interpretation")
    print("  class_group_smooth=1")
    print("  lth_roots_of_unity_in_Fp_for_odd_class_factors=0")
    print("  Kummer_radicals_over_Fp_directly_available=0")
    print("  defining_subfield_polynomials_available=0")
    print("  if_subfield_polynomials_were_available_then_small_factors_are_easy=1")
    print("  large_factor_radical_requires_zeta_extension_degree=388430")
    print(f"  full_odd_part_zeta_extension_degree={odd_part_order}")
    print(
        "conclusion=smooth_class_group_does_not_by_itself_give_an_embedded_"
        "Fp_radical_descent_to_a_CM_root"
    )


if __name__ == "__main__":
    main()
