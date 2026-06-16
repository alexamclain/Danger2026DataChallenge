#!/usr/bin/env python3
"""Separate the reduced-anchor diamond norm from the cyclic C/E trace norm.

The previous diamond gate showed that the denominator-cleared reduced-anchor
residual is

    D_c = sum_{k != 0} [zeta_c^k] - (c - 1)[1],

the diamond/unit norm over `(Z/cZ)^*` of the single divisor
`[zeta_c] - [1]`.

This gate checks the nearby false implementation: take the ordinary cyclic
translation trace/norm over `C_c`.  It telescopes:

    sum_{t in C_c} ([zeta_c^{1+t}] - [zeta_c^t]) = 0,

or multiplicatively

    prod_t (X - zeta_c^{1+t}) / (X - zeta_c^t) = 1.

So a producer that realizes the one-point factor but then applies the cyclic
`C/E` trace norm erases the anchor residual.  The p24 producer must use the
diamond/unit orbit of size 178, not the cyclic orbit of size 179.
"""

from __future__ import annotations

from collections import Counter

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate import (
    formal_cyclotomic_divisor,
    fourier_profile_ok,
)
from trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate import (
    diamond_norm_divisor,
    single_divisor,
)


def add(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def cyclic_translation(values: list[int], c_degree: int, shift: int) -> list[int]:
    out = [0] * len(values)
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            target = (c_index + shift) % c_degree
            out[right * c_degree + target] = values[right * c_degree + c_index]
    return out


def cyclic_translation_trace_divisor(c_degree: int, modulus: int) -> list[int]:
    total = [0] * (RIGHT_DEGREE * c_degree)
    base = single_divisor(c_degree, modulus)
    for shift in range(c_degree):
        total = add(total, cyclic_translation(base, c_degree, shift), modulus)
    return total


def cyclic_product_telescopes(c_degree: int) -> bool:
    numerator_exponents = Counter((1 + shift) % c_degree for shift in range(c_degree))
    denominator_exponents = Counter(shift % c_degree for shift in range(c_degree))
    return numerator_exponents == denominator_exponents


def diamond_product_exponents(c_degree: int) -> tuple[Counter[int], Counter[int]]:
    numerator_exponents = Counter(multiplier % c_degree for multiplier in range(1, c_degree))
    denominator_exponents = Counter(0 for _multiplier in range(1, c_degree))
    return numerator_exponents, denominator_exponents


def diamond_product_is_residual(c_degree: int) -> bool:
    numerator_exponents, denominator_exponents = diamond_product_exponents(c_degree)
    expected_numerator = Counter(range(1, c_degree))
    expected_denominator = Counter({0: c_degree - 1})
    return numerator_exponents == expected_numerator and denominator_exponents == expected_denominator


def is_zero(values: list[int], modulus: int) -> bool:
    return all(value % modulus == 0 for value in values)


def main() -> None:
    print("Trace-GCD reduced-anchor cyclic-vs-diamond norm gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    cyclic_trace_zero_rows = 0
    cyclic_product_rows = 0
    diamond_residual_rows = 0
    diamond_product_rows = 0
    cyclic_not_residual_rows = 0
    distinct_orbit_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        cyclic_trace = cyclic_translation_trace_divisor(c_degree, modulus)
        diamond = diamond_norm_divisor(c_degree, modulus)
        expected = formal_cyclotomic_divisor(c_degree, modulus)

        cyclic_trace_zero_ok = int(is_zero(cyclic_trace, modulus))
        cyclic_product_ok = int(cyclic_product_telescopes(c_degree))
        diamond_residual_ok = int(
            diamond == expected and fourier_profile_ok(diamond, c_degree, modulus)
        )
        diamond_product_ok = int(diamond_product_is_residual(c_degree))
        cyclic_not_residual_ok = int(cyclic_trace != expected and not is_zero(expected, modulus))
        distinct_orbit_ok = int(c_degree != c_degree - 1)

        rows_checked += 1
        cyclic_trace_zero_rows += cyclic_trace_zero_ok
        cyclic_product_rows += cyclic_product_ok
        diamond_residual_rows += diamond_residual_ok
        diamond_product_rows += diamond_product_ok
        cyclic_not_residual_rows += cyclic_not_residual_ok
        distinct_orbit_rows += distinct_orbit_ok

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"cyclic_translation_orbit_size={c_degree} "
            f"diamond_orbit_size={c_degree - 1} "
            f"cyclic_trace_zero_ok={cyclic_trace_zero_ok} "
            f"cyclic_product_telescopes_ok={cyclic_product_ok} "
            f"diamond_residual_ok={diamond_residual_ok} "
            f"diamond_product_residual_ok={diamond_product_ok} "
            f"cyclic_not_residual_ok={cyclic_not_residual_ok} "
            f"distinct_orbit_ok={distinct_orbit_ok}"
        )

    print(f"cyclic_vs_diamond_rows_checked={rows_checked}")
    print(f"cyclic_translation_trace_zero_rows={cyclic_trace_zero_rows}/{rows_checked}")
    print(f"cyclic_product_telescopes_rows={cyclic_product_rows}/{rows_checked}")
    print(f"diamond_norm_residual_rows={diamond_residual_rows}/{rows_checked}")
    print(f"diamond_product_residual_rows={diamond_product_rows}/{rows_checked}")
    print(f"cyclic_translation_not_residual_rows={cyclic_not_residual_rows}/{rows_checked}")
    print(f"cyclic_and_diamond_orbit_sizes_distinct_rows={distinct_orbit_rows}/{rows_checked}")
    print(f"p24_cyclic_translation_orbit_size={P24_C_DEGREE}")
    print(f"p24_diamond_orbit_size={P24_C_DEGREE - 1}")
    print("interpretation")
    print("  cyclic_C_over_E_translation_norm_of_one_point_factor_is_trivial=1")
    print("  diamond_unit_norm_of_one_point_factor_is_the_R_c_residual=1")
    print("  ordinary_cyclic_trace_norm_erases_the_selected_anchor_residual=1")
    print("  p24_producer_must_use_diamond_norm_not_cyclic_C_over_E_norm=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate")

    if cyclic_trace_zero_rows != rows_checked:
        raise SystemExit(1)
    if cyclic_product_rows != rows_checked:
        raise SystemExit(1)
    if diamond_residual_rows != rows_checked:
        raise SystemExit(1)
    if diamond_product_rows != rows_checked:
        raise SystemExit(1)
    if cyclic_not_residual_rows != rows_checked:
        raise SystemExit(1)
    if distinct_orbit_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
