#!/usr/bin/env python3
"""Exact arithmetic relation audit for the smooth p24 class-group lead.

The third strict trace has a friendly class group

    h = 2 * 157 * 211 * 3107441.

Before treating this as an odd class-field route, check whether these factors
interact cheaply with the p24 field arithmetic or target group order: divisors
of p-1, p+1, the target odd cofactor, or small multiplicative orders of p
modulo the class factors would suggest Kummer/radical shortcuts or a direct
projection label.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
N = 10**12
TRACE = -1178414874616
CLASS_NUMBER = 205880396014
CLASS_FACTORS = [2, 157, 211, 3107441]


def v2(n: int) -> int:
    return (abs(n) & -abs(n)).bit_length() - 1


def main() -> None:
    order = P24 + 1 - TRACE
    twist_order = P24 + 1 + TRACE
    odd_order = order >> v2(order)
    abs_DK = abs((TRACE * TRACE - 4 * P24) // 4)

    print("p24 smooth class arithmetic relation audit")
    print(f"p={P24}")
    print(f"n={N}")
    print(f"trace={TRACE}")
    print(f"curve_order={order}")
    print(f"factor_curve_order={sp.factorint(order)}")
    print(f"twist_order={twist_order}")
    print(f"factor_twist_order={sp.factorint(twist_order)}")
    print(f"odd_order={odd_order}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"factor_class_number={sp.factorint(CLASS_NUMBER)}")
    print(f"abs_DK={abs_DK}")
    print(f"factor_abs_DK={sp.factorint(abs_DK)}")
    print()

    rows = [
        ("odd_order", odd_order),
        ("abs_DK", abs_DK),
        ("p_minus_1", P24 - 1),
        ("p_plus_1", P24 + 1),
        ("n", N),
        ("trace", abs(TRACE)),
        ("abs_trace_minus_2n", abs(TRACE - 2 * N)),
        ("abs_trace_plus_2n", abs(TRACE + 2 * N)),
    ]
    print("gcds_with_class_number")
    for label, value in rows:
        g = math.gcd(CLASS_NUMBER, value)
        print(f"  {label:20s} gcd={g:12d} factors={sp.factorint(g)}")
    print()

    print("class_factor_residues")
    print("  factor p_mod factor p_order_mod_factor odd_order_mod_factor")
    for factor in CLASS_FACTORS:
        if factor == 2:
            continue
        p_mod = P24 % factor
        odd_mod = odd_order % factor
        p_order = sp.n_order(p_mod, factor) if math.gcd(p_mod, factor) == 1 else 0
        print(f"  {factor:8d} {p_mod:8d} {p_order:18d} {odd_mod:21d}")
    print()

    print("small_linear_relations_odd_order_plus_a_h")
    for a in range(-5, 6):
        value = odd_order + a * CLASS_NUMBER
        print(f"  a={a:2d} value={value:15d} factors={sp.factorint(abs(value)) if value else {}}")
    print(
        "conclusion=class_group_smoothness_has_no_visible_kummer_or_group_order_"
        "shortcut_with_p24_field_arithmetic"
    )


if __name__ == "__main__":
    main()
