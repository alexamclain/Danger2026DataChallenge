#!/usr/bin/env python3
"""Audit modular-form level costs for non-genus twisted traces.

The split-cycle period route reduces p24 CM-root selection to computing
class-character twisted traces

    T_chi = sum_{a in Cl(O)} chi(a) j(a).

For trivial and genus characters, known singular-moduli trace formulas can
collapse the class sum to coefficients of relatively accessible modular
objects.  For a high-order class group character, the associated automorphic
object is dihedral: a theta series induced from an unramified Hecke/class
character of K.  Its natural level over Q is the discriminant of K (up to the
usual small half-integral-weight factors), not the quotient size 314 or 422.

This script records the resulting level/index/Sturm-bound proxies.  It is an
audit of the modular-form route, not a proof of an unconditional lower bound.
"""

from __future__ import annotations

from fractions import Fraction
import math

import sympy as sp

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
ABS_D = abs(D_K)
SQRT_P = math.isqrt(P24)

QUOTIENTS = (314, 422, 66254)


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for prime in sp.factorint(n):
        value *= Fraction(prime + 1, prime)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def sturm_proxy(level: int, weight_num: int, weight_den: int = 1) -> Fraction:
    """Return the usual k/12 * [SL2Z:Gamma0(N)] proxy."""
    return Fraction(weight_num, weight_den) * gamma0_index(level) / 12


def main() -> None:
    print("p24 non-genus twisted trace modular-level audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"factor_abs_D_K={sp.factorint(ABS_D)}")
    print(f"sqrt_floor_p={SQRT_P}")
    print()

    levels = [
        ("dihedral_weight1_level_abs_D", ABS_D, Fraction(1, 1)),
        ("half_integral_trace_level_4abs_D", 4 * ABS_D, Fraction(3, 2)),
    ]
    print("level_cost_proxies")
    print("  label level gamma0_index sturm_proxy proxy_over_sqrt")
    for label, level, weight in levels:
        index = gamma0_index(level)
        proxy = sturm_proxy(level, weight.numerator, weight.denominator)
        print(
            f"  {label:34s} {level:26d} {index:26d} "
            f"{float(proxy):16.6e} {float(proxy) / SQRT_P:16.6e}"
        )
    print()

    print("quotient_character_orders")
    print("  quotient factorization non_genus_odd_factor required_character_orders")
    for quotient in QUOTIENTS:
        factors = sp.factorint(quotient)
        odd = [q for q in factors if q != 2]
        print(f"  {quotient:8d} {factors!s:24s} {odd!s:20s} all divisors of quotient")
    print()

    print("interpretation")
    print("  genus_characters_factor_through_Cl_over_Cl_squared=1")
    print("  third_target_genus_quotient_size=2")
    print("  quotient_314_or_422_requires_order_157_or_211_characters=1")
    print("  non_genus_dihedral_theta_level_is_abs_D_not_quotient_size=1")
    print("  modular_space_proxy_far_above_sqrt_p=1")
    print(
        "conclusion=standard_modular_form_twisted_trace_route_does_not_"
        "give_the_needed_subsqrt_formula_for_p24"
    )


if __name__ == "__main__":
    main()
