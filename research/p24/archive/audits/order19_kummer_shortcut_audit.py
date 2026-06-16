#!/usr/bin/env python3
"""Audit the order-19 Kummer shortcut for the first strict p24 trace.

The first strict trace has the smallest clean quotient found so far:

    h = 2 * 19 * 7335098083,
    ell = 19,
    Cl/<ell> has order 19.

Also p == -1 mod 19, so primitive 19th roots of unity live in F_{p^2}.
This script records exactly what that buys.  The answer is useful but narrow:
the Fourier/Kummer diagonalization of the quotient is cheap once the embedded
order-19 character traces are known, but the congruence does not construct
those traces or pair an abstract class-field generator with j.
"""

from __future__ import annotations

import math

import sympy as sp


P = 10**24 + 7
TRACE = 1020608380936
D_K = -739589633190799177940983
CLASS_NUMBER = 278733727154
QUOTIENT_ORDER = 19
RECOVERY_ORDER = CLASS_NUMBER // QUOTIENT_ORDER
SQRT_P = math.isqrt(P)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def multiplicative_order(a: int, modulus: int) -> int | None:
    if math.gcd(a, modulus) != 1:
        return None
    return int(sp.n_order(a % modulus, modulus))


def row(label: str, modulus: int) -> None:
    order = multiplicative_order(P, modulus)
    print(
        f"  {label:18s} modulus={modulus:15d} "
        f"p_mod={P % modulus:15d} ord_p={str(order):>12s} "
        f"divides_p_minus_1={int((P - 1) % modulus == 0)} "
        f"divides_p_plus_1={int((P + 1) % modulus == 0)}"
    )


def main() -> None:
    curve_order = P + 1 - TRACE
    twist_order = P + 1 + TRACE

    print("order-19 Kummer shortcut audit")
    print(f"p={P}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factor={sp.factorint(CLASS_NUMBER)}")
    print(f"quotient_order={QUOTIENT_ORDER}")
    print(f"recovery_order={RECOVERY_ORDER}")
    print(f"recovery_order_factor={sp.factorint(RECOVERY_ORDER)}")
    print(f"recovery_order_over_sqrt={RECOVERY_ORDER / SQRT_P:.6e}")
    print()

    print("finite_field_congruences")
    print(f"  p_minus_1_factor={sp.factorint(P - 1)}")
    print(f"  p_plus_1_factor={sp.factorint(P + 1)}")
    print(f"  curve_order_factor={sp.factorint(curve_order)}")
    print(f"  twist_order_factor={sp.factorint(twist_order)}")
    print(f"  v2_curve_order={v2(curve_order)}")
    print(f"  v2_twist_order={v2(twist_order)}")
    print()

    print("cyclotomic_table")
    row("quotient_zeta", QUOTIENT_ORDER)
    row("recovery_prime", 7335098083)
    row("recovery_order", RECOVERY_ORDER)
    print()

    print("gcds_with_class_number")
    for label, value in (
        ("p-1", P - 1),
        ("p+1", P + 1),
        ("curve_order", curve_order),
        ("twist_order", twist_order),
        ("abs_D_K", abs(D_K)),
    ):
        g = math.gcd(value, CLASS_NUMBER)
        print(f"  {label:14s} gcd={g:15d} factors={sp.factorint(g)}")
    print()

    print("order_19_period_accounting")
    print("  quotient_periods y_r lie in F_p because the CM roots split in F_p")
    print("  primitive_zeta_19_in_Fp=0")
    print("  primitive_zeta_19_in_Fp2=1")
    print("  Frobenius_on_zeta_19=sends_zeta_to_zeta_inverse")
    print("  Frobenius_pairs_twisted_traces=T_s_with_T_19_minus_s")
    print("  inverse_DFT_cost_after_traces_known=O(19^2)_field_ops")
    print("  direct_Kummer_radical_over_Fp_available=0")
    print("  direct_Kummer_radical_over_Fp2_formally_available=1")
    print("  embedded_character_traces_constructed=0")
    print("  abstract_quotient_to_j_pairing_constructed=0")
    print()

    print("standard_trace_formula_scale")
    print(f"  natural_dihedral_theta_level_abs_D={abs(D_K)}")
    print(f"  abs_D_over_sqrt={abs(D_K) / SQRT_P:.6e}")
    print("  quotient_order_over_sqrt=1.900000e-11")
    print("  level_is_not_reduced_by_zeta_extension_degree=1")
    print()

    print("interpretation")
    print("  p_congruent_minus_1_mod_19_gives_quadratic_cyclotomic_descent=1")
    print("  this_diagonalizes_the_known_period_vector_but_does_not_create_it=1")
    print("  missing_input=embedded_order_19_class_character_trace_or_equivalent")
    print(
        "conclusion=order19_kummer_is_a_good_normal_form_for_the_missing_"
        "theorem_not_a_seedless_selector"
    )


if __name__ == "__main__":
    main()
