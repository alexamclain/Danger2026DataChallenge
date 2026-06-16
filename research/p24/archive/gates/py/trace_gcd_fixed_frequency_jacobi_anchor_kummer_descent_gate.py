#!/usr/bin/env python3
"""Auxiliary Kummer descent for the Jacobi anchor residual.

The residual-factor search shows that the C/E-trivial row-sum slice and the
R_c residual do not split as separate multiplicative factors in the small
Jacobi value fields.  The obstruction is exactly the missing c-th root of the
selected anchor scalar.

This gate records the positive replacement.  Work in a formal Kummer extension
with

    beta^c = s,

where `s=(q-2)/x` and the scalar search left only `x=+/-1`.

For the `R_c^e` family, define on the right-zero row:

    row-sum slice exponent:       (c-1)e       at every C coordinate;
    residual exponent:          -(c-1)e       at k=0;
    residual exponent:              e         at k != 0.

Their product is:

    beta^0      = 1      at k=0;
    beta^(ce)   = s^e    at k != 0.

Therefore the product descends to the base field.  The selected correction
requires `s^e=s`, hence the formal exponent is e=1.  For p24, this is the
precise auxiliary-extension version of the R_179 anchor target.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe import make_context
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def has_power_root(value: int, exponent: int, modulus: int) -> bool:
    if value % modulus == 0:
        return True
    return pow(value, (modulus - 1) // gcd(exponent, modulus - 1), modulus) == 1


def normalize_beta_power(exponent: int, c_degree: int) -> tuple[int, int]:
    """Return (base_s_exponent, beta_exponent) with 0 <= beta_exponent < c."""

    base_exponent = exponent // c_degree
    beta_exponent = exponent % c_degree
    return base_exponent, beta_exponent


def product_profile(c_degree: int, e_value: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return normalized product at k=0 and k!=0.

    The pair `(a,b)` means `s^a * beta^b`.
    """

    row_sum_exponent = (c_degree - 1) * e_value
    residual_zero_exponent = -(c_degree - 1) * e_value
    residual_nonzero_exponent = e_value
    zero = normalize_beta_power(row_sum_exponent + residual_zero_exponent, c_degree)
    nonzero = normalize_beta_power(
        row_sum_exponent + residual_nonzero_exponent, c_degree
    )
    return zero, nonzero


def descends_to_selected_correction(c_degree: int, e_value: int) -> bool:
    zero, nonzero = product_profile(c_degree, e_value)
    return zero == (0, 0) and nonzero == (1, 0)


def descends_to_base(c_degree: int, e_value: int) -> bool:
    zero, nonzero = product_profile(c_degree, e_value)
    return zero[1] == 0 and nonzero[1] == 0


def row_sum_and_residual_are_nonbase(c_degree: int, e_value: int) -> bool:
    row_sum_exponent = (c_degree - 1) * e_value
    residual_zero_exponent = -(c_degree - 1) * e_value
    residual_nonzero_exponent = e_value
    return (
        normalize_beta_power(row_sum_exponent, c_degree)[1] != 0
        and normalize_beta_power(residual_zero_exponent, c_degree)[1] != 0
        and normalize_beta_power(residual_nonzero_exponent, c_degree)[1] != 0
    )


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi anchor Kummer descent gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    unique_e_rows = 0
    selected_descent_rows = 0
    nonbase_slice_rows = 0
    no_base_split_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
        sign_scalars = {
            "plus": q_minus_2,
            "minus": (-q_minus_2) % ctx.value_field_l,
        }

        for sign, selected_scalar in sign_scalars.items():
            valid_exponents = [
                e_value
                for e_value in range(c_degree)
                if descends_to_selected_correction(c_degree, e_value)
            ]
            selected_descent_ok = int(descends_to_selected_correction(c_degree, 1))
            unique_e_ok = int(valid_exponents == [1])
            nonbase_slice_ok = int(row_sum_and_residual_are_nonbase(c_degree, 1))
            base_split_exists = has_power_root(
                selected_scalar, c_degree, ctx.value_field_l
            )
            no_base_split_ok = int(not base_split_exists)
            zero_profile, nonzero_profile = product_profile(c_degree, 1)

            rows_checked += 1
            unique_e_rows += unique_e_ok
            selected_descent_rows += selected_descent_ok
            nonbase_slice_rows += nonbase_slice_ok
            no_base_split_rows += no_base_split_ok

            print(
                "row "
                f"c_degree={c_degree} sign={sign} order={order} "
                f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
                f"selected_scalar={selected_scalar} "
                f"valid_formal_Rc_exponents={valid_exponents} "
                f"e1_zero_profile={zero_profile} "
                f"e1_nonzero_profile={nonzero_profile} "
                f"selected_descent_ok={selected_descent_ok} "
                f"unique_e_ok={unique_e_ok} "
                f"nonbase_slice_ok={nonbase_slice_ok} "
                f"base_field_c_root_exists={int(base_split_exists)} "
                f"no_base_split_ok={no_base_split_ok}"
            )

    print(f"kummer_descent_rows_checked={rows_checked}")
    print(f"kummer_selected_descent_rows={selected_descent_rows}/{rows_checked}")
    print(f"kummer_Rc_exponent_unique_e_one_rows={unique_e_rows}/{rows_checked}")
    print(f"kummer_row_sum_and_residual_nonbase_rows={nonbase_slice_rows}/{rows_checked}")
    print(f"kummer_no_base_field_split_rows={no_base_split_rows}/{rows_checked}")
    print(f"p24_kummer_auxiliary_degree={P24_C_DEGREE}")
    print(f"p24_R179_exponent_for_selected_correction=1")
    print("interpretation")
    print("  adjoining_beta_with_beta_c_equals_selected_scalar_splits_anchor_slices=1")
    print("  row_sum_slice_and_R_c_residual_product_descends_to_base_correction=1")
    print("  selected_correction_forces_R_c_exponent_e_equals_1=1")
    print("  separate_slices_are_nonbase_even_though_their_product_descends=1")
    print("  p24_target_is_auxiliary_kummer_or_norm_descent_for_R_179_with_sign=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate")

    if selected_descent_rows != rows_checked:
        raise SystemExit(1)
    if unique_e_rows != rows_checked:
        raise SystemExit(1)
    if nonbase_slice_rows != rows_checked:
        raise SystemExit(1)
    if no_base_split_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
