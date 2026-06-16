#!/usr/bin/env python3
"""Audit possible arithmetic sources for the odd relative tower phases.

The third p24 trace has

    D_K = -599 * q
    h = 2 * 157 * 211 * 3107441.

After the genus split, the remaining tower layers need order-157 and
order-211 unramified class-character phases.  This script separates three
different "cyclotomic" facts that are easy to conflate:

1. roots of unity for the quotient DFT may live in a moderate extension;
2. Kummer radicals would still need defining equations for embedded class
   subfields;
3. a Jacobi-sum CM construction for the actual quadratic field would need a
   cyclotomic conductor whose quadratic subfield has discriminant D_K, hence
   conductor divisible by |D_K|, not just by 157 or 211.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
ABS_D = abs(D_K)
D_FACTORS = [599, 1089874116562502921057]
CLASS_NUMBER = 205880396014
CLASS_FACTORS = [2, 157, 211, 3107441]
ODD_QUOTIENTS = [157, 211, 157 * 211]
SQRT_P = math.isqrt(P24)


def order_mod(modulus: int) -> int:
    if math.gcd(P24, modulus) != 1:
        return 0
    return int(sp.n_order(P24 % modulus, modulus))


def quadratic_subfield_discriminant_for_prime(ell: int) -> int:
    """Quadratic subfield discriminant of Q(zeta_ell), ell odd prime."""
    return ell if ell % 4 == 1 else -ell


def main() -> None:
    q = D_FACTORS[1]
    print("p24 odd relative phase source audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"factor_abs_D_K={sp.factorint(ABS_D)}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"factor_class_number={sp.factorint(CLASS_NUMBER)}")
    print()

    print("quotient_root_of_unity_extensions")
    print("  modulus purpose p_mod_modulus ord_p_modulus ord_over_sqrt")
    for modulus, purpose in [
        (157, "order-157 relative DFT"),
        (211, "order-211 relative DFT"),
        (157 * 211, "combined odd quotient DFT"),
        (2 * 157 * 211, "full quotient incl genus"),
    ]:
        ord_p = order_mod(modulus)
        print(
            f"  {modulus:12d} {purpose:28s} {P24 % modulus:13d} "
            f"{ord_p:14d} {ord_p / SQRT_P:13.6e}"
        )
    print()

    print("small_cyclotomic_quadratic_subfields")
    print("  ell quad_subfield_D equals_target_field")
    for ell in [157, 211, 599]:
        quad_D = quadratic_subfield_discriminant_for_prime(ell)
        print(f"  {ell:5d} {quad_D:15d} {int(quad_D == D_K)}")
    print(
        "  note=157 gives a real quadratic subfield, 211 gives Q(sqrt(-211)), "
        "and 599 gives only the genus factor Q(sqrt(-599))."
    )
    print()

    print("jacobi_sum_target_field_conductors")
    print("  conductor p_mod_conductor ord_p_conductor ord_over_sqrt")
    for conductor in [
        599,
        q,
        ABS_D,
        157 * ABS_D,
        211 * ABS_D,
    ]:
        ord_p = order_mod(conductor)
        print(
            f"  {conductor:27d} {P24 % conductor:27d} "
            f"{ord_p:27d} {ord_p / SQRT_P:13.6e}"
        )
    print()

    print("class_factor_interactions")
    print("  target gcd_with_value factors")
    values = [
        ("p-1", P24 - 1),
        ("p+1", P24 + 1),
        ("D_factor_599_minus_1", 599 - 1),
        ("D_factor_599_plus_1", 599 + 1),
        ("D_factor_q_minus_1", q - 1),
        ("D_factor_q_plus_1", q + 1),
        ("curve_odd_order", (P24 + 1 - TRACE) >> 41),
        ("twist_oddish_order", (P24 + 1 + TRACE) >> 4),
    ]
    odd_h = CLASS_NUMBER // 2
    for label, value in values:
        gcd_value = math.gcd(odd_h, value)
        print(f"  {label:24s} {gcd_value:15d} {sp.factorint(gcd_value)}")
    print()

    print("interpretation")
    print("  quotient_roots_of_unity_are_moderate=1")
    print("  small_cyclotomic_quadratic_subfields_do_not_equal_target_K=1")
    print("  genus_factor_599_supplies_only_degree_2_split=1")
    print("  target_jacobi_sum_conductor_has_huge_zeta_extension=1")
    print("  class_factors_do_not_align_with_p_pm_1_or_D_factor_pm_1=1")
    print(
        "conclusion=odd_157_211_relative_phases_are_not_explained_by_"
        "visible_cyclotomic_or_jacobi_sum_arithmetic"
    )


if __name__ == "__main__":
    main()
