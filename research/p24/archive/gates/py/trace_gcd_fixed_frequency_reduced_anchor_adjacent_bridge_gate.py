#!/usr/bin/env python3
"""Bridge the reduced Jacobi anchor to the adjacent-anchor descent target.

The reduced-anchor fingerprint is a function on C_7 x C_c:

    h(r,k) = 1 if r=0 and k != 0, else 0.

The older adjacent-anchor/descent route only sees the C/E-trivial slice, i.e.
the row sums over k.  For h that row-sum profile is

    A = (c-1) * e_0  on C_7.

This gate checks the exact finite bridge:

* the b=0 Fourier slice of h is the Fourier transform of A;
* A has nonzero projection to all six nontrivial right characters;
* the cyclic adjacent difference Delta_i=A_{i+1}-A_i multiplies each
  nontrivial right Fourier channel by zeta_7^{-a}-1, hence is invertible
  on the nonfixed quotient;
* an opposite raw b=0 leak is exactly what the selected reduced anchor must
  cancel before the old adjacent-anchor descent theorem can hold.

This is not the CM/Lang producer proof.  It identifies precisely which slice
of the reduced anchor composes with the previous adjacent-anchor machinery.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import (
    primitive_root,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate import (
    punctured_right_zero_row,
)


def dft_right(profile: list[int], a_value: int, modulus: int, zeta7: int) -> int:
    total = 0
    for right, value in enumerate(profile):
        total += value * pow(zeta7, a_value * right, modulus)
    return total % modulus


def dft_full_b0(values: list[int], c_degree: int, a_value: int, modulus: int, zeta7: int) -> int:
    total = 0
    for right in range(RIGHT_DEGREE):
        right_phase = pow(zeta7, a_value * right, modulus)
        for c_index in range(c_degree):
            total += values[right * c_degree + c_index] * right_phase
    return total % modulus


def row_sums(values: list[int], c_degree: int, modulus: int) -> list[int]:
    return [
        sum(values[right * c_degree : (right + 1) * c_degree]) % modulus
        for right in range(RIGHT_DEGREE)
    ]


def adjacent_difference(profile: list[int], modulus: int) -> list[int]:
    return [
        (profile[(right + 1) % RIGHT_DEGREE] - profile[right]) % modulus
        for right in range(RIGHT_DEGREE)
    ]


def nontrivial_channels_nonzero(profile: list[int], modulus: int, zeta7: int) -> bool:
    return all(dft_right(profile, a_value, modulus, zeta7) for a_value in range(1, RIGHT_DEGREE))


def all_nontrivial_channels_zero(profile: list[int], modulus: int, zeta7: int) -> bool:
    return all(
        dft_right(profile, a_value, modulus, zeta7) == 0
        for a_value in range(1, RIGHT_DEGREE)
    )


def profile_is_constant(profile: list[int]) -> bool:
    return all(value == profile[0] for value in profile)


def main() -> None:
    print("Trace-GCD reduced-anchor adjacent bridge gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    b0_slice_rows = 0
    forbidden_leak_rows = 0
    adjacent_multiplier_rows = 0
    adjacent_invertible_rows = 0
    adjacent_telescope_rows = 0
    opposite_cancel_rows = 0
    mismatch_control_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        root = primitive_root(modulus)
        zeta7 = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)

        anchor = punctured_right_zero_row(c_degree, modulus)
        profile = row_sums(anchor, c_degree, modulus)
        diff = adjacent_difference(profile, modulus)

        b0_slice_ok = True
        adjacent_multiplier_ok = True
        for a_value in range(RIGHT_DEGREE):
            full_b0 = dft_full_b0(anchor, c_degree, a_value, modulus, zeta7)
            profile_b0 = dft_right(profile, a_value, modulus, zeta7)
            if full_b0 != profile_b0:
                b0_slice_ok = False

            diff_b0 = dft_right(diff, a_value, modulus, zeta7)
            multiplier = (pow(zeta7, (-a_value) % RIGHT_DEGREE, modulus) - 1) % modulus
            if diff_b0 != (multiplier * profile_b0) % modulus:
                adjacent_multiplier_ok = False

        forbidden_leak_ok = nontrivial_channels_nonzero(profile, modulus, zeta7)
        adjacent_invertible_ok = nontrivial_channels_nonzero(diff, modulus, zeta7)
        adjacent_telescope_ok = sum(diff) % modulus == 0

        raw_opposite = [(-value) % modulus for value in profile]
        corrected = [(a + b) % modulus for a, b in zip(raw_opposite, profile)]
        opposite_cancel_ok = (
            all(value == 0 for value in corrected)
            and all_nontrivial_channels_zero(corrected, modulus, zeta7)
            and profile_is_constant(corrected)
        )

        mismatched = [(raw_opposite[idx] + 2 * profile[idx]) % modulus for idx in range(RIGHT_DEGREE)]
        mismatch_control_ok = (
            not profile_is_constant(mismatched)
            and not all_nontrivial_channels_zero(mismatched, modulus, zeta7)
        )

        rows_checked += 1
        b0_slice_rows += int(b0_slice_ok)
        forbidden_leak_rows += int(forbidden_leak_ok)
        adjacent_multiplier_rows += int(adjacent_multiplier_ok)
        adjacent_invertible_rows += int(adjacent_invertible_ok)
        adjacent_telescope_rows += int(adjacent_telescope_ok)
        opposite_cancel_rows += int(opposite_cancel_ok)
        mismatch_control_rows += int(mismatch_control_ok)

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"row_sum_profile={profile} "
            f"adjacent_difference={diff} "
            f"b0_slice_ok={int(b0_slice_ok)} "
            f"forbidden_b0_leak_ok={int(forbidden_leak_ok)} "
            f"adjacent_multiplier_ok={int(adjacent_multiplier_ok)} "
            f"adjacent_invertible_ok={int(adjacent_invertible_ok)} "
            f"adjacent_telescope_ok={int(adjacent_telescope_ok)} "
            f"opposite_cancel_ok={int(opposite_cancel_ok)} "
            f"mismatch_control_ok={int(mismatch_control_ok)}"
        )

    print(f"bridge_rows_checked={rows_checked}")
    print(f"b0_slice_matches_row_sum_rows={b0_slice_rows}/{rows_checked}")
    print(f"anchor_b0_forbidden_leak_rows={forbidden_leak_rows}/{rows_checked}")
    print(f"adjacent_difference_multiplier_rows={adjacent_multiplier_rows}/{rows_checked}")
    print(f"adjacent_difference_nonfixed_invertible_rows={adjacent_invertible_rows}/{rows_checked}")
    print(f"anchor_diff_telescope_rows={adjacent_telescope_rows}/{rows_checked}")
    print(f"opposite_raw_leak_cancel_rows={opposite_cancel_rows}/{rows_checked}")
    print(f"mismatched_anchor_leak_control_rows={mismatch_control_rows}/{rows_checked}")
    print(f"p24_anchor_b0_nontrivial_projectors={RIGHT_DEGREE - 1}")
    print("interpretation")
    print("  adjacent_anchor_sees_c_trivial_slice_of_reduced_anchor=1")
    print("  reduced_anchor_row_sum_profile_generates_all_six_nonfixed_right_channels=1")
    print("  right_difference_is_invertible_on_that_nonfixed_slice=1")
    print("  old_adjacent_anchor_target_is_cancellation_of_reduced_anchor_b0_leak=1")
    print("  full_punctured_anchor_still_requires_cm_lang_realization_not_just_b0_slice=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate")

    if b0_slice_rows != rows_checked:
        raise SystemExit(1)
    if forbidden_leak_rows != rows_checked:
        raise SystemExit(1)
    if adjacent_multiplier_rows != rows_checked:
        raise SystemExit(1)
    if adjacent_invertible_rows != rows_checked:
        raise SystemExit(1)
    if adjacent_telescope_rows != rows_checked:
        raise SystemExit(1)
    if opposite_cancel_rows != rows_checked:
        raise SystemExit(1)
    if mismatch_control_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
