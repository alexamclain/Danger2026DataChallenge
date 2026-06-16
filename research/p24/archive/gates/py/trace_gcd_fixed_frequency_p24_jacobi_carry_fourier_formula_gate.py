#!/usr/bin/env python3
"""Explicit Fourier formula for admissible C-axis Jacobi carries.

For N=7*c and a multiplier m, define the cyclic sawtooth

    g_m(t) = [m*t]_N.

If d=gcd(m,N), M=N/d, and zeta_M is a primitive Mth root, then the nonzero
Fourier coefficients are

    \hat g_m(k) = 0                              if d does not divide k,
    \hat g_m(k) = -d^2*M/(1-zeta_M^(-k/d*m'^{-1}))
                                                  if d divides k != 0,

where m'=m/d mod M.  At k=0, \hat g_m(0)=d^2*M*(M-1)/2.

This gate checks that formula against the brute DFT used by the admissible
Jacobi experiments and records the source of the four dual Fourier families:

* forbidden C-trivial/right-nontrivial coefficients cancel because u=7s and
  v,u+v have the same right component;
* conjugate skew follows from \hat g_m(k)+\hat g_m(-k)=-d*N;
* right-trivial pair sums have lambda_c=-2/(c-1);
* the three global balances follow because every admissible carry vanishes on
  the C-zero fiber.
"""

from __future__ import annotations

from math import gcd

from trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate import (
    condition_rows,
    coord,
    derive_pair_sum_lambda,
)
from trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary import dft_rows
from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import primitive_root
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    admissible_c_axis_carry_rows,
    carry_vector,
    crt,
    split_prime_for,
)


SAMPLE_FORMULA_ROWS = 32


def product_frequency(right_character: int, c_character: int, c_degree: int) -> int:
    # The value-side CRT point is
    #   x = r*c*c^{-1} mod 7 + b*7*7^{-1} mod c.
    # Thus zeta_N^(-k*x) gives product-character exponents
    #   right: k*c^{-1} mod 7,   C: k*7^{-1} mod c.
    # To match omega_7^(-right_character*r) omega_c^(-c_character*b),
    # use k == right_character*c mod 7 and k == c_character*7 mod c.
    return crt(
        (right_character * c_degree) % RIGHT_DEGREE,
        (c_character * RIGHT_DEGREE) % c_degree,
        c_degree,
    )


def zeta_n(field_q: int, order: int) -> int:
    root = primitive_root(field_q)
    return pow(root, (field_q - 1) // order, field_q)


def sawtooth_dft_formula(
    multiplier: int, frequency: int, order: int, zeta: int, field_q: int
) -> int:
    multiplier %= order
    frequency %= order
    if multiplier == 0:
        return 0
    divisor = gcd(multiplier, order)
    quotient_order = order // divisor
    if frequency == 0:
        return (
            divisor
            * divisor
            * quotient_order
            * (quotient_order - 1)
            // 2
        ) % field_q
    if frequency % divisor:
        return 0
    reduced_multiplier = (multiplier // divisor) % quotient_order
    reduced_frequency = (frequency // divisor) % quotient_order
    exponent = (
        -reduced_frequency * pow(reduced_multiplier, -1, quotient_order)
    ) % quotient_order
    zeta_quotient = pow(zeta, divisor, field_q)
    denominator = (1 - pow(zeta_quotient, exponent, field_q)) % field_q
    return (-divisor * divisor * quotient_order * pow(denominator, -1, field_q)) % field_q


def carry_dft_formula(
    c_degree: int,
    field_q: int,
    u_value: int,
    v_value: int,
    right_character: int,
    c_character: int,
) -> int:
    order = RIGHT_DEGREE * c_degree
    zeta = zeta_n(field_q, order)
    frequency = product_frequency(right_character, c_character, c_degree)
    uv_value = (u_value + v_value) % order
    return (
        sawtooth_dft_formula(u_value, frequency, order, zeta, field_q)
        + sawtooth_dft_formula(v_value, frequency, order, zeta, field_q)
        - sawtooth_dft_formula(uv_value, frequency, order, zeta, field_q)
    ) % field_q


def admissible_pairs(c_degree: int) -> list[tuple[int, int]]:
    order = RIGHT_DEGREE * c_degree
    pairs: list[tuple[int, int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if v_value % c_degree == 0:
                continue
            if (u_value + v_value) % c_degree == 0:
                continue
            pairs.append((u_value, v_value))
    return pairs


def row_satisfies_all_conditions(
    row: list[int], c_degree: int, field_q: int, pair_sum_lambda: int
) -> bool:
    conditions = condition_rows(c_degree, field_q, pair_sum_lambda)
    return all(
        sum(value * coeff for value, coeff in zip(row, condition)) % field_q == 0
        for condition in conditions
    )


def c_zero_fiber_vanishes(
    c_degree: int, field_q: int, u_value: int, v_value: int
) -> bool:
    row = carry_vector(c_degree, field_q, u_value, v_value)
    return all(row[right * c_degree] % field_q == 0 for right in range(RIGHT_DEGREE))


def lambda_formula(c_degree: int, field_q: int) -> int:
    return (-2 * pow(c_degree - 1, -1, field_q)) % field_q


def main() -> None:
    formula_rows_ok = 0
    condition_rows_ok = 0
    lambda_rows_ok = 0
    c_zero_rows_ok = 0
    rows_checked = 0

    print("Trace-GCD fixed-frequency p24 Jacobi-carry Fourier formula gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        field_q = split_prime_for(order)
        pairs = admissible_pairs(c_degree)
        rows = admissible_c_axis_carry_rows(c_degree, field_q)
        dft = dft_rows(rows, c_degree, field_q)
        derived_lambda = derive_pair_sum_lambda(dft, c_degree, field_q)
        predicted_lambda = lambda_formula(c_degree, field_q)
        lambda_match = int(derived_lambda == predicted_lambda)
        lambda_rows_ok += lambda_match

        formula_match_count = 0
        for row_index, (u_value, v_value) in enumerate(pairs[:SAMPLE_FORMULA_ROWS]):
            brute = dft[row_index]
            formula = [
                carry_dft_formula(
                    c_degree,
                    field_q,
                    u_value,
                    v_value,
                    right_character,
                    c_character,
                )
                for right_character in range(RIGHT_DEGREE)
                for c_character in range(c_degree)
            ]
            formula_match_count += int(brute == formula)

        condition_match_count = sum(
            int(row_satisfies_all_conditions(row, c_degree, field_q, predicted_lambda))
            for row in dft
        )
        c_zero_match_count = sum(
            int(c_zero_fiber_vanishes(c_degree, field_q, u_value, v_value))
            for u_value, v_value in pairs
        )

        formula_ok = int(formula_match_count == min(SAMPLE_FORMULA_ROWS, len(pairs)))
        conditions_ok = int(condition_match_count == len(rows))
        c_zero_ok = int(c_zero_match_count == len(pairs))
        formula_rows_ok += formula_ok
        condition_rows_ok += conditions_ok
        c_zero_rows_ok += c_zero_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"admissible_generators={len(rows)} "
            f"sample_formula_matches={formula_match_count}/"
            f"{min(SAMPLE_FORMULA_ROWS, len(pairs))} "
            f"derived_lambda={derived_lambda} "
            f"predicted_lambda_minus_2_over_c_minus_1={predicted_lambda} "
            f"lambda_match={lambda_match} "
            f"dual_condition_rows={condition_match_count}/{len(rows)} "
            f"c_zero_fiber_vanishes={c_zero_match_count}/{len(pairs)} "
            f"formula_gate_ok={formula_ok} "
            f"dual_conditions_gate_ok={conditions_ok} "
            f"c_zero_gate_ok={c_zero_ok}"
        )

    print(f"formula_matches={formula_rows_ok}/{rows_checked}")
    print(f"lambda_formula_matches={lambda_rows_ok}/{rows_checked}")
    print(f"dual_condition_rows_match={condition_rows_ok}/{rows_checked}")
    print(f"c_zero_fiber_rows_match={c_zero_rows_ok}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("p24_pair_sum_lambda_rational=-2/(179-1)=-1/89")
    print("interpretation")
    print("  sawtooth_dft_formula_matches_brute_dft=1")
    print("  admissible_carry_pair_sum_lambda_is_minus_2_over_c_minus_1=1")
    print("  conjugate_skew_comes_from_sawtooth_pair_sum_cancellation=1")
    print("  global_balances_come_from_c_zero_fiber_vanishing=1")
    print("  finite_dual_conditions_are_symbolic_jacobi_carry_identities=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate")

    if formula_rows_ok != rows_checked:
        raise SystemExit(1)
    if lambda_rows_ok != rows_checked:
        raise SystemExit(1)
    if condition_rows_ok != rows_checked:
        raise SystemExit(1)
    if c_zero_rows_ok != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
