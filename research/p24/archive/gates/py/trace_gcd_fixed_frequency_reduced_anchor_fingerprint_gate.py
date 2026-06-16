#!/usr/bin/env python3
"""Additive fingerprint of the reduced Jacobi anchor.

Multiplicatively, the reduced Jacobi packet changes only

    U(0,0) = J(1,1) = q-2

by multiplying it by (q-2)^(-1).  Additively, write that correction as
`-e_(0,0)` in the raw packet g.  The selected defect is

    f(r,k) = g(r,k) - g(r,0).

Therefore the anchor correction contributes exactly the punctured right-zero
row

    h(r,k) = 1 if r=0 and k != 0, else 0.

This gate records the Fourier and right-difference fingerprints of h.  It is
not a new proof of p24; it names the exact additive object that the selected
CM/Lang anchor unit has to supply.
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


def raw_anchor_correction(c_degree: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_degree)
    values[0] = (-1) % modulus
    return values


def selected_defect(raw: list[int], c_degree: int, modulus: int) -> list[int]:
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        base = raw[right * c_degree]
        for c_index in range(c_degree):
            out.append((raw[right * c_degree + c_index] - base) % modulus)
    return out


def punctured_right_zero_row(c_degree: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_degree)
    for c_index in range(1, c_degree):
        values[c_index] = 1 % modulus
    return values


def fourier_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    order = RIGHT_DEGREE * c_degree
    root = primitive_root(modulus)
    zeta7 = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zetac = pow(root, (modulus - 1) // c_degree, modulus)
    expected_b0 = (c_degree - 1) % modulus
    expected_b_nonzero = (-1) % modulus
    for a_value in range(RIGHT_DEGREE):
        for b_value in range(c_degree):
            total = 0
            for right in range(RIGHT_DEGREE):
                right_phase = pow(zeta7, a_value * right, modulus)
                for c_index in range(c_degree):
                    total += (
                        values[right * c_degree + c_index]
                        * right_phase
                        * pow(zetac, b_value * c_index, modulus)
                    )
            total %= modulus
            expected = expected_b0 if b_value == 0 else expected_b_nonzero
            if total != expected:
                return False
    return order > 0


def forbidden_c_trivial_leaks(values: list[int], c_degree: int, modulus: int) -> bool:
    root = primitive_root(modulus)
    zeta7 = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    expected = (c_degree - 1) % modulus
    for a_value in range(1, RIGHT_DEGREE):
        total = 0
        for right in range(RIGHT_DEGREE):
            right_phase = pow(zeta7, a_value * right, modulus)
            for c_index in range(c_degree):
                total += values[right * c_degree + c_index] * right_phase
        if total % modulus != expected:
            return False
    return True


def right_difference_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    punctured = [0] + [1 % modulus] * (c_degree - 1)
    negative_punctured = [(-value) % modulus for value in punctured]
    for right in range(RIGHT_DEGREE):
        diff = []
        for c_index in range(c_degree):
            diff.append(
                (
                    values[((right + 1) % RIGHT_DEGREE) * c_degree + c_index]
                    - values[right * c_degree + c_index]
                )
                % modulus
            )
        if right == 0:
            expected = negative_punctured
        elif right == RIGHT_DEGREE - 1:
            expected = punctured
        else:
            expected = [0] * c_degree
        if diff != expected:
            return False
    return True


def row_sum_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    sums = [
        sum(values[right * c_degree : (right + 1) * c_degree]) % modulus
        for right in range(RIGHT_DEGREE)
    ]
    return sums[0] == (c_degree - 1) % modulus and all(value == 0 for value in sums[1:])


def main() -> None:
    print("Trace-GCD fixed-frequency reduced-anchor fingerprint gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    selected_defect_rows = 0
    support_rows = 0
    fourier_rows = 0
    forbidden_leak_rows = 0
    right_difference_rows = 0
    row_sum_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        raw = raw_anchor_correction(c_degree, modulus)
        defect = selected_defect(raw, c_degree, modulus)
        expected = punctured_right_zero_row(c_degree, modulus)

        selected_defect_ok = int(defect == expected)
        support_size = sum(1 for value in defect if value % modulus)
        support_ok = int(support_size == c_degree - 1)
        fourier_ok = int(fourier_profile_ok(defect, c_degree, modulus))
        forbidden_leak_ok = int(forbidden_c_trivial_leaks(defect, c_degree, modulus))
        right_difference_ok = int(right_difference_profile_ok(defect, c_degree, modulus))
        row_sum_ok = int(row_sum_profile_ok(defect, c_degree, modulus))

        selected_defect_rows += selected_defect_ok
        support_rows += support_ok
        fourier_rows += fourier_ok
        forbidden_leak_rows += forbidden_leak_ok
        right_difference_rows += right_difference_ok
        row_sum_rows += row_sum_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"support_size={support_size} "
            f"expected_support={c_degree - 1} "
            f"selected_defect_ok={selected_defect_ok} "
            f"support_ok={support_ok} "
            f"fourier_profile_ok={fourier_ok} "
            f"forbidden_c_trivial_leak_ok={forbidden_leak_ok} "
            f"right_difference_profile_ok={right_difference_ok} "
            f"row_sum_profile_ok={row_sum_ok}"
        )

    print(f"anchor_fingerprint_rows_checked={rows_checked}")
    print(f"anchor_selected_defect_rows={selected_defect_rows}/{rows_checked}")
    print(f"anchor_support_rows={support_rows}/{rows_checked}")
    print(f"anchor_fourier_profile_rows={fourier_rows}/{rows_checked}")
    print(f"anchor_forbidden_c_trivial_leak_rows={forbidden_leak_rows}/{rows_checked}")
    print(f"anchor_right_difference_profile_rows={right_difference_rows}/{rows_checked}")
    print(f"anchor_row_sum_profile_rows={row_sum_rows}/{rows_checked}")
    print(f"p24_anchor_nonzero_entries={P24_C_DEGREE - 1}")
    print("interpretation")
    print("  single_anchor_correction_becomes_punctured_right_zero_row=1")
    print("  anchor_fingerprint_has_all_right_frequencies_and_fixed_c_profile=1")
    print("  anchor_fingerprint_alone_leaks_forbidden_c_trivial_bidegrees=1")
    print("  anchor_fingerprint_right_difference_is_two_adjacent_punctured_rows=1")
    print("  p24_cm_lang_anchor_must_supply_this_selected_defect_fingerprint=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate")

    if selected_defect_rows != rows_checked:
        raise SystemExit(1)
    if support_rows != rows_checked:
        raise SystemExit(1)
    if fourier_rows != rows_checked:
        raise SystemExit(1)
    if forbidden_leak_rows != rows_checked:
        raise SystemExit(1)
    if right_difference_rows != rows_checked:
        raise SystemExit(1)
    if row_sum_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
