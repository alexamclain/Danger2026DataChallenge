#!/usr/bin/env python3
"""C-trivial / C-nontrivial decomposition of the reduced Jacobi anchor.

The reduced anchor selected-defect fingerprint is the punctured right-zero row

    h(r,k) = 1 if r=0 and k != 0, else 0

on C_7 x C_c.  The adjacent-anchor bridge accounts only for the C-trivial
row-sum slice of h.  This gate splits h into

    h = h_triv + h_nontriv

where h_triv is constant in the C-coordinate on each right row, and h_nontriv
has C-row sums zero.  The exact profiles are:

    h_triv Fourier:    H(a,0)=c-1, H(a,b)=0 for b != 0;
    h_nontriv Fourier: H(a,0)=0,   H(a,b)=-1 for b != 0.

Thus the old adjacent-anchor route handles only the six nonfixed right
channels in h_triv.  The remaining CM/Lang unit realization must still supply
the full C-nontrivial slice, which for p24 has 7*(179-1)=1246 nonzero Fourier
channels.
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


def c_trivial_projection(values: list[int], c_degree: int, modulus: int) -> list[int]:
    inv_c = pow(c_degree, -1, modulus)
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        row = values[right * c_degree : (right + 1) * c_degree]
        average = (sum(row) * inv_c) % modulus
        out.extend([average] * c_degree)
    return out


def subtract(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a - b) % modulus for a, b in zip(left, right)]


def add(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def dft(values: list[int], c_degree: int, a_value: int, b_value: int, modulus: int) -> int:
    root = primitive_root(modulus)
    zeta7 = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zetac = pow(root, (modulus - 1) // c_degree, modulus)
    total = 0
    for right in range(RIGHT_DEGREE):
        right_phase = pow(zeta7, a_value * right, modulus)
        for c_index in range(c_degree):
            total += (
                values[right * c_degree + c_index]
                * right_phase
                * pow(zetac, b_value * c_index, modulus)
            )
    return total % modulus


def row_sums_zero(values: list[int], c_degree: int, modulus: int) -> bool:
    return all(
        sum(values[right * c_degree : (right + 1) * c_degree]) % modulus == 0
        for right in range(RIGHT_DEGREE)
    )


def trivial_slice_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    expected_b0 = (c_degree - 1) % modulus
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            expected = expected_b0 if b_value == 0 else 0
            if dft(values, c_degree, a_value, b_value, modulus) != expected:
                return False
    return True


def nontrivial_slice_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            expected = 0 if b_value == 0 else (-1) % modulus
            if dft(values, c_degree, a_value, b_value, modulus) != expected:
                return False
    return True


def nontrivial_spatial_formula_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    inv_c = pow(c_degree, -1, modulus)
    zero_value = (-(c_degree - 1) * inv_c) % modulus
    nonzero_value = inv_c
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            value = values[right * c_degree + c_index]
            if right == 0 and c_index == 0:
                expected = zero_value
            elif right == 0:
                expected = nonzero_value
            else:
                expected = 0
            if value != expected:
                return False
    return True


def nonzero_fourier_count(values: list[int], c_degree: int, modulus: int) -> int:
    count = 0
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            count += int(dft(values, c_degree, a_value, b_value, modulus) != 0)
    return count


def main() -> None:
    print("Trace-GCD reduced-anchor C-slice decomposition gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    reconstruction_rows = 0
    trivial_profile_rows = 0
    nontrivial_profile_rows = 0
    nontrivial_rowsum_rows = 0
    nontrivial_spatial_rows = 0
    old_anchor_invisible_rows = 0
    full_remaining_channel_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        anchor = punctured_right_zero_row(c_degree, modulus)
        trivial = c_trivial_projection(anchor, c_degree, modulus)
        nontrivial = subtract(anchor, trivial, modulus)

        reconstruction_ok = int(add(trivial, nontrivial, modulus) == anchor)
        trivial_profile_ok = int(trivial_slice_profile_ok(trivial, c_degree, modulus))
        nontrivial_profile_ok = int(nontrivial_slice_profile_ok(nontrivial, c_degree, modulus))
        nontrivial_rowsum_ok = int(row_sums_zero(nontrivial, c_degree, modulus))
        nontrivial_spatial_ok = int(nontrivial_spatial_formula_ok(nontrivial, c_degree, modulus))
        old_anchor_invisible_ok = int(
            row_sums_zero(nontrivial, c_degree, modulus)
            and all(dft(nontrivial, c_degree, a_value, 0, modulus) == 0 for a_value in range(1, RIGHT_DEGREE))
        )
        remaining_channels = nonzero_fourier_count(nontrivial, c_degree, modulus)
        full_remaining_channel_ok = int(remaining_channels == RIGHT_DEGREE * (c_degree - 1))

        rows_checked += 1
        reconstruction_rows += reconstruction_ok
        trivial_profile_rows += trivial_profile_ok
        nontrivial_profile_rows += nontrivial_profile_ok
        nontrivial_rowsum_rows += nontrivial_rowsum_ok
        nontrivial_spatial_rows += nontrivial_spatial_ok
        old_anchor_invisible_rows += old_anchor_invisible_ok
        full_remaining_channel_rows += full_remaining_channel_ok

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"remaining_nontrivial_fourier_channels={remaining_channels} "
            f"expected_remaining={RIGHT_DEGREE * (c_degree - 1)} "
            f"reconstruction_ok={reconstruction_ok} "
            f"trivial_profile_ok={trivial_profile_ok} "
            f"nontrivial_profile_ok={nontrivial_profile_ok} "
            f"nontrivial_rowsum_ok={nontrivial_rowsum_ok} "
            f"nontrivial_spatial_formula_ok={nontrivial_spatial_ok} "
            f"old_anchor_invisible_ok={old_anchor_invisible_ok} "
            f"full_remaining_channel_ok={full_remaining_channel_ok}"
        )

    print(f"slice_rows_checked={rows_checked}")
    print(f"slice_reconstruction_rows={reconstruction_rows}/{rows_checked}")
    print(f"c_trivial_slice_profile_rows={trivial_profile_rows}/{rows_checked}")
    print(f"c_nontrivial_slice_profile_rows={nontrivial_profile_rows}/{rows_checked}")
    print(f"c_nontrivial_rowsum_zero_rows={nontrivial_rowsum_rows}/{rows_checked}")
    print(f"c_nontrivial_spatial_formula_rows={nontrivial_spatial_rows}/{rows_checked}")
    print(f"old_adjacent_anchor_invisible_c_nontrivial_rows={old_anchor_invisible_rows}/{rows_checked}")
    print(f"full_remaining_nontrivial_channel_rows={full_remaining_channel_rows}/{rows_checked}")
    print(f"p24_remaining_c_nontrivial_fourier_channels={RIGHT_DEGREE * (P24_C_DEGREE - 1)}")
    print("interpretation")
    print("  adjacent_bridge_accounts_only_for_c_trivial_row_sum_slice=1")
    print("  c_nontrivial_slice_has_zero_row_sums_and_is_invisible_to_old_adjacent_anchor=1")
    print("  cm_lang_unit_must_realize_full_punctured_row_not_only_b0_slice=1")
    print("  remaining_p24_anchor_realization_has_1246_c_nontrivial_fourier_channels=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate")

    if reconstruction_rows != rows_checked:
        raise SystemExit(1)
    if trivial_profile_rows != rows_checked:
        raise SystemExit(1)
    if nontrivial_profile_rows != rows_checked:
        raise SystemExit(1)
    if nontrivial_rowsum_rows != rows_checked:
        raise SystemExit(1)
    if nontrivial_spatial_rows != rows_checked:
        raise SystemExit(1)
    if old_anchor_invisible_rows != rows_checked:
        raise SystemExit(1)
    if full_remaining_channel_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
