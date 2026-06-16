#!/usr/bin/env python3
"""Multiplicative dictionary for the selected-defect producer theorem.

The raw selected-defect producer target is additive:

    g(r,0)+g(-r,0)=A0
    g(r,c)+g(-r,-c)=A1, c != 0
    sum_c g(r,c)-c_degree*g(r,0)=B.

If U(r,c)=omega^g(r,c) in a cyclic torus, these are exactly:

    U(r,0) U(-r,0) = alpha0
    U(r,c) U(-r,-c) = alpha1, c != 0
    prod_c U(r,c) / U(r,0)^c_degree = beta.

This is the shape a modular-unit, elliptic-unit, or product-formula proof
would naturally supply.  The gate checks the equivalence in small finite
cyclic tori and keeps the same controls as the additive producer gate.
"""

from __future__ import annotations

import random

from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import primitive_root
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate import (
    TRIALS,
    force_affine_balance,
    force_both_conditions,
    force_two_level_inversion,
    random_raw,
    raw_producer_conditions,
    raw_selected_affine_row_balance,
    raw_two_level_inversion_complement,
)


SEED = 20260607


def torus_root(exponent_modulus: int) -> tuple[int, int]:
    torus_field = split_prime_for(exponent_modulus)
    root = primitive_root(torus_field)
    omega = pow(root, (torus_field - 1) // exponent_modulus, torus_field)
    if pow(omega, exponent_modulus, torus_field) != 1 or omega == 1:
        raise RuntimeError("failed to construct requested torus root")
    return torus_field, omega


def exponentiate(raw: list[int], exponent_modulus: int, torus_field: int, omega: int) -> list[int]:
    return [pow(omega, value % exponent_modulus, torus_field) for value in raw]


def multiplicative_two_level_complement(
    values: list[int], c_degree: int, torus_field: int
) -> bool:
    zero_constant: int | None = None
    off_constant: int | None = None
    for right in range(RIGHT_DEGREE):
        zero_value = (
            values[right * c_degree]
            * values[((-right) % RIGHT_DEGREE) * c_degree]
        ) % torus_field
        if zero_constant is None:
            zero_constant = zero_value
        elif zero_value != zero_constant:
            return False

        for c_index in range(1, c_degree):
            value = (
                values[right * c_degree + c_index]
                * values[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
            ) % torus_field
            if off_constant is None:
                off_constant = value
            elif value != off_constant:
                return False
    return zero_constant is not None and off_constant is not None


def multiplicative_selected_row_ratio(
    values: list[int], c_degree: int, torus_field: int
) -> bool:
    ratios: list[int] = []
    for right in range(RIGHT_DEGREE):
        product = 1
        for c_index in range(c_degree):
            product = product * values[right * c_degree + c_index] % torus_field
        denominator = pow(values[right * c_degree], c_degree, torus_field)
        ratios.append(product * pow(denominator, -1, torus_field) % torus_field)
    return all(value == ratios[0] for value in ratios)


def multiplicative_producer_conditions(
    raw: list[int], c_degree: int, exponent_modulus: int, torus_field: int, omega: int
) -> bool:
    values = exponentiate(raw, exponent_modulus, torus_field, omega)
    return multiplicative_two_level_complement(
        values, c_degree, torus_field
    ) and multiplicative_selected_row_ratio(values, c_degree, torus_field)


def main() -> None:
    rng = random.Random(SEED)
    rows_checked = 0
    equivalence_rows = 0
    forced_rows = 0
    inversion_only_rows = 0
    affine_only_rows = 0

    print("Trace-GCD fixed-frequency p24 multiplicative producer dictionary gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES[:3]:
        # Use a prime exponent modulus so the additive checks and the torus
        # checks have the same equality notion.
        exponent_modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        torus_field, omega = torus_root(exponent_modulus)
        width = RIGHT_DEGREE * c_degree
        equivalence_trials = 0
        random_hits = 0
        forced_hits = 0
        inversion_only_controls = 0
        affine_only_controls = 0

        for _ in range(TRIALS):
            raw = random_raw(width, exponent_modulus, rng)
            additive = raw_producer_conditions(raw, c_degree, exponent_modulus)
            multiplicative = multiplicative_producer_conditions(
                raw, c_degree, exponent_modulus, torus_field, omega
            )
            equivalence_trials += int(additive == multiplicative)
            random_hits += int(multiplicative)

            raw_both = force_both_conditions(c_degree, exponent_modulus, rng)
            forced_hits += int(
                raw_producer_conditions(raw_both, c_degree, exponent_modulus)
                and multiplicative_producer_conditions(
                    raw_both, c_degree, exponent_modulus, torus_field, omega
                )
            )

            raw_inversion = force_two_level_inversion(c_degree, exponent_modulus, rng)
            inversion_values = exponentiate(
                raw_inversion, exponent_modulus, torus_field, omega
            )
            inversion_only_controls += int(
                raw_two_level_inversion_complement(
                    raw_inversion, c_degree, exponent_modulus
                )
                and multiplicative_two_level_complement(
                    inversion_values, c_degree, torus_field
                )
                and not raw_selected_affine_row_balance(
                    raw_inversion, c_degree, exponent_modulus
                )
                and not multiplicative_selected_row_ratio(
                    inversion_values, c_degree, torus_field
                )
            )

            raw_affine = force_affine_balance(c_degree, exponent_modulus, rng)
            affine_values = exponentiate(raw_affine, exponent_modulus, torus_field, omega)
            affine_only_controls += int(
                raw_selected_affine_row_balance(
                    raw_affine, c_degree, exponent_modulus
                )
                and multiplicative_selected_row_ratio(
                    affine_values, c_degree, torus_field
                )
                and not raw_two_level_inversion_complement(
                    raw_affine, c_degree, exponent_modulus
                )
                and not multiplicative_two_level_complement(
                    affine_values, c_degree, torus_field
                )
            )

        equivalence_ok = int(equivalence_trials == TRIALS and random_hits == 0)
        forced_ok = int(forced_hits == TRIALS)
        inversion_ok = int(inversion_only_controls == TRIALS)
        affine_ok = int(affine_only_controls == TRIALS)
        equivalence_rows += equivalence_ok
        forced_rows += forced_ok
        inversion_only_rows += inversion_ok
        affine_only_rows += affine_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} exponent_modulus={exponent_modulus} "
            f"torus_field={torus_field} "
            f"equivalence_trials={equivalence_trials}/{TRIALS} "
            f"random_multiplicative_hits={random_hits}/{TRIALS} "
            f"forced_hits={forced_hits}/{TRIALS} "
            f"inversion_only_controls={inversion_only_controls}/{TRIALS} "
            f"affine_only_controls={affine_only_controls}/{TRIALS} "
            f"equivalence_ok={equivalence_ok} "
            f"forced_ok={forced_ok} "
            f"inversion_ok={inversion_ok} "
            f"affine_ok={affine_ok}"
        )

    print(f"multiplicative_additive_equivalence={equivalence_rows}/{rows_checked}")
    print(f"forced_product_formula_hits={forced_rows}/{rows_checked}")
    print(f"inversion_product_without_row_ratio_controls={inversion_only_rows}/{rows_checked}")
    print(f"row_ratio_without_inversion_product_controls={affine_only_rows}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("interpretation")
    print("  raw_complement_law_is_pair_product_constancy=1")
    print("  selected_affine_balance_is_selected_row_product_ratio_constancy=1")
    print("  product_formula_producer_target_matches_additive_selected_defect_target=1")
    print("  product_complement_without_row_ratio_leaks_balances=1")
    print("  row_ratio_without_product_complement_leaks_structural_symmetry=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate")

    if equivalence_rows != rows_checked:
        raise SystemExit(1)
    if forced_rows != rows_checked:
        raise SystemExit(1)
    if inversion_only_rows != rows_checked:
        raise SystemExit(1)
    if affine_only_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
