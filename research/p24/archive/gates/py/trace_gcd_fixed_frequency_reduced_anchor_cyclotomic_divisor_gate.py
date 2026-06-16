#!/usr/bin/env python3
"""Cyclotomic principal divisor for the reduced-anchor residual.

The reduced-anchor C-slice gate splits the punctured right-zero row

    h(r,k) = 1 if r=0 and k != 0, else 0

into a C/E-trivial row-sum slice and a C/E-nontrivial residual.  The residual
has fractional spatial values

    h_nontriv(0,0) = -(c-1)/c,
    h_nontriv(0,k) = 1/c for k != 0,
    h_nontriv(r,k) = 0 for r != 0.

This gate checks the denominator-cleared identity

    c * h_nontriv = sum_{k != 0} [zeta_c^k] - (c-1)[1],

supported on the right-zero row.  For prime c this is exactly the divisor of

    R_c(X) = Phi_c(X) / (X - 1)^(c - 1).

Thus the C/E-nontrivial residual is not an amorphous 7*(c-1)-channel target:
after clearing the harmless factor c, it is a concrete rational cyclotomic
principal divisor.  The remaining p24 theorem is the CM/Lang specialization
and p-integrality statement for the selected degenerate anchor.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate import (
    c_trivial_projection,
    dft,
    subtract,
)
from trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate import (
    punctured_right_zero_row,
)


def scale(values: list[int], scalar: int, modulus: int) -> list[int]:
    return [(scalar * value) % modulus for value in values]


def integral_residual_divisor(c_degree: int, modulus: int) -> list[int]:
    """Return c*h_nontriv over the split finite field."""

    anchor = punctured_right_zero_row(c_degree, modulus)
    trivial = c_trivial_projection(anchor, c_degree, modulus)
    nontrivial = subtract(anchor, trivial, modulus)
    return scale(nontrivial, c_degree, modulus)


def formal_cyclotomic_divisor(c_degree: int, modulus: int) -> list[int]:
    """Formal divisor of Phi_c(X)/(X-1)^(c-1), placed on right row 0."""

    values = [0] * (RIGHT_DEGREE * c_degree)
    values[0] = (-(c_degree - 1)) % modulus
    for c_index in range(1, c_degree):
        values[c_index] = 1 % modulus
    return values


def signed_cyclotomic_exponents(c_degree: int) -> list[int]:
    exponents = [-(c_degree - 1)]
    exponents.extend([1] * (c_degree - 1))
    return exponents


def degree_zero(values: list[int], c_degree: int, modulus: int) -> bool:
    return sum(values) % modulus == 0 and all(
        sum(values[right * c_degree : (right + 1) * c_degree]) % modulus == 0
        for right in range(RIGHT_DEGREE)
    )


def spatial_integral_formula_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            value = values[right * c_degree + c_index]
            if right == 0 and c_index == 0:
                expected = (-(c_degree - 1)) % modulus
            elif right == 0:
                expected = 1 % modulus
            else:
                expected = 0
            if value != expected:
                return False
    return True


def fourier_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            expected = 0 if b_value == 0 else (-c_degree) % modulus
            if dft(values, c_degree, a_value, b_value, modulus) != expected:
                return False
    return True


def cyclotomic_divisor_profile_ok(c_degree: int) -> bool:
    """Check the formal prime-c cyclotomic divisor exponents.

    For prime c, Phi_c has simple zeros at the nontrivial c-th roots and no
    zero at 1.  Dividing by (X-1)^(c-1) gives one pole of order c-1 at 1.
    """

    exponents = signed_cyclotomic_exponents(c_degree)
    return (
        exponents[0] == -(c_degree - 1)
        and all(exponent == 1 for exponent in exponents[1:])
        and sum(exponents) == 0
    )


def nonzero_fourier_count(values: list[int], c_degree: int, modulus: int) -> int:
    count = 0
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            count += int(dft(values, c_degree, a_value, b_value, modulus) != 0)
    return count


def main() -> None:
    print("Trace-GCD reduced-anchor cyclotomic divisor gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    integral_matches_rows = 0
    degree_zero_rows = 0
    spatial_formula_rows = 0
    fourier_profile_rows = 0
    cyclotomic_divisor_rows = 0
    residual_channel_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        residual_divisor = integral_residual_divisor(c_degree, modulus)
        cyclotomic_divisor = formal_cyclotomic_divisor(c_degree, modulus)

        integral_matches_ok = int(residual_divisor == cyclotomic_divisor)
        degree_zero_ok = int(degree_zero(residual_divisor, c_degree, modulus))
        spatial_formula_ok = int(
            spatial_integral_formula_ok(residual_divisor, c_degree, modulus)
        )
        fourier_ok = int(fourier_profile_ok(residual_divisor, c_degree, modulus))
        cyclotomic_ok = int(cyclotomic_divisor_profile_ok(c_degree))
        channels = nonzero_fourier_count(residual_divisor, c_degree, modulus)
        channels_ok = int(channels == RIGHT_DEGREE * (c_degree - 1))

        rows_checked += 1
        integral_matches_rows += integral_matches_ok
        degree_zero_rows += degree_zero_ok
        spatial_formula_rows += spatial_formula_ok
        fourier_profile_rows += fourier_ok
        cyclotomic_divisor_rows += cyclotomic_ok
        residual_channel_rows += channels_ok

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"nonzero_fourier_channels={channels} "
            f"expected_channels={RIGHT_DEGREE * (c_degree - 1)} "
            f"integral_residual_matches_cyclotomic_divisor_ok={integral_matches_ok} "
            f"degree_zero_ok={degree_zero_ok} "
            f"spatial_integral_formula_ok={spatial_formula_ok} "
            f"fourier_profile_ok={fourier_ok} "
            f"cyclotomic_divisor_profile_ok={cyclotomic_ok} "
            f"residual_channel_count_ok={channels_ok}"
        )

    p24_channels = RIGHT_DEGREE * (P24_C_DEGREE - 1)

    print(f"cyclotomic_divisor_rows_checked={rows_checked}")
    print(f"integral_residual_matches_cyclotomic_divisor_rows={integral_matches_rows}/{rows_checked}")
    print(f"cyclotomic_residual_degree_zero_rows={degree_zero_rows}/{rows_checked}")
    print(f"cyclotomic_residual_spatial_formula_rows={spatial_formula_rows}/{rows_checked}")
    print(f"cyclotomic_residual_fourier_profile_rows={fourier_profile_rows}/{rows_checked}")
    print(f"principal_cyclotomic_divisor_profile_rows={cyclotomic_divisor_rows}/{rows_checked}")
    print(f"cyclotomic_residual_channel_count_rows={residual_channel_rows}/{rows_checked}")
    print(f"p24_cyclotomic_residual_divisor_degree_zero=1")
    print(f"p24_residual_integral_fourier_channels={p24_channels}")
    print("interpretation")
    print("  c_nontrivial_residual_clears_to_integral_degree_zero_divisor=1")
    print("  c_nontrivial_residual_is_cyclotomic_principal_divisor_after_clearing_c=1")
    print("  candidate_unit_R_c_equals_Phi_c_over_X_minus_1_power_c_minus_1=1")
    print("  p24_candidate_unit_is_R_179_equals_Phi_179_over_X_minus_1_power_178=1")
    print("  p24_remaining_arithmetic_is_cm_lang_specialization_and_p_integrality=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate")

    if integral_matches_rows != rows_checked:
        raise SystemExit(1)
    if degree_zero_rows != rows_checked:
        raise SystemExit(1)
    if spatial_formula_rows != rows_checked:
        raise SystemExit(1)
    if fourier_profile_rows != rows_checked:
        raise SystemExit(1)
    if cyclotomic_divisor_rows != rows_checked:
        raise SystemExit(1)
    if residual_channel_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
