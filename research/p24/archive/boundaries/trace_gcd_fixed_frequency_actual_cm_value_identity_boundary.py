#!/usr/bin/env python3
"""Actual-CM boundary for the value-side admissible-packet identities.

The p24 target has three value-side packet identities after B/C trace:

  1. C-row sums independent of the right coordinate;
  2. C-zero fiber vanishes;
  3. inversion-complement is constant off the C-zero fiber.

This boundary diagnoses nearby actual-CM rows by these three identities.  It
answers whether the new split proof target is generic.  It is not: the pinned
actual-CM projector/right-combo/coefficient packets fail the structural
identities before the final three balances become the issue.  The only partial
exception is tautological: selected-defect coefficients vanish on the C-zero
fiber by construction, but still fail inversion-complement and row sums.
"""

from __future__ import annotations

from dataclasses import replace

from trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary import (
    H,
    PROJECTOR_Q,
    TOY_C_DEGREE,
    TOP_QUOTIENT,
    coefficient_projected_distribution,
    defect_projected_distribution,
    load_projector_cycle,
    load_right_combo_packet,
    projector_projected_distribution,
    right_combo_projected_distribution,
)
from trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary import (
    weighted_coefficients,
)
from relative_moment_projection_scan import rotate as rotate_tuple
from trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary import (
    rotate as rotate_list,
)


def int_row_sum_independent(
    row: list[int], right_degree: int, c_degree: int, modulus: int
) -> bool:
    row_sums = [
        sum(row[right * c_degree : (right + 1) * c_degree]) % modulus
        for right in range(right_degree)
    ]
    return all(value == row_sums[0] for value in row_sums)


def int_c_zero(row: list[int], right_degree: int, c_degree: int, modulus: int) -> bool:
    return all(row[right * c_degree] % modulus == 0 for right in range(right_degree))


def int_inversion_constant(
    row: list[int], right_degree: int, c_degree: int, modulus: int
) -> bool:
    constant: int | None = None
    for right in range(right_degree):
        for c_index in range(1, c_degree):
            value = (
                row[right * c_degree + c_index]
                + row[((-right) % right_degree) * c_degree + ((-c_index) % c_degree)]
            ) % modulus
            if constant is None:
                constant = value
            elif value != constant:
                return False
    return constant is not None


def ext_row_sum_independent(row, right_degree: int, c_degree: int, field) -> bool:
    row_sums = []
    for right in range(right_degree):
        total = field.zero
        for value in row[right * c_degree : (right + 1) * c_degree]:
            total = field.add(total, value)
        row_sums.append(total)
    return all(value == row_sums[0] for value in row_sums)


def ext_c_zero(row, right_degree: int, c_degree: int, field) -> bool:
    return all(row[right * c_degree] == field.zero for right in range(right_degree))


def ext_inversion_constant(row, right_degree: int, c_degree: int, field) -> bool:
    constant = None
    for right in range(right_degree):
        for c_index in range(1, c_degree):
            value = field.add(
                row[right * c_degree + c_index],
                row[((-right) % right_degree) * c_degree + ((-c_index) % c_degree)],
            )
            if constant is None:
                constant = value
            elif value != constant:
                return False
    return constant is not None


def count_projector_profiles() -> tuple[int, int, int, int, int]:
    cycle = load_projector_cycle()
    row_sum = 0
    c_zero = 0
    inversion = 0
    structural = 0
    all_three = 0
    for shift in range(H):
        target = projector_projected_distribution(rotate_list(cycle, shift))
        row_ok = int_row_sum_independent(
            target, TOP_QUOTIENT, TOY_C_DEGREE, PROJECTOR_Q
        )
        zero_ok = int_c_zero(target, TOP_QUOTIENT, TOY_C_DEGREE, PROJECTOR_Q)
        inv_ok = int_inversion_constant(
            target, TOP_QUOTIENT, TOY_C_DEGREE, PROJECTOR_Q
        )
        row_sum += int(row_ok)
        c_zero += int(zero_ok)
        inversion += int(inv_ok)
        structural += int(zero_ok and inv_ok)
        all_three += int(row_ok and zero_ok and inv_ok)
    return row_sum, c_zero, inversion, structural, all_three


def count_right_combo_profiles():
    packet = load_right_combo_packet()
    profiles = {
        "right_combo_resolvent": [0, 0, 0, 0, 0],
        "weighted_coefficients": [0, 0, 0, 0, 0],
        "selected_defect_coefficients": [0, 0, 0, 0, 0],
    }
    right_degree = 2
    c_degree = packet.n
    for shift in range(packet.h):
        shifted = replace(packet, cycle=tuple(rotate_tuple(packet.cycle, shift)))
        coefficients = weighted_coefficients(shifted)
        targets = {
            "right_combo_resolvent": right_combo_projected_distribution(shifted),
            "weighted_coefficients": coefficient_projected_distribution(
                coefficients, packet.field
            ),
            "selected_defect_coefficients": defect_projected_distribution(
                coefficients, packet.field
            ),
        }
        for name, target in targets.items():
            row_ok = ext_row_sum_independent(
                target, right_degree, c_degree, packet.field
            )
            zero_ok = ext_c_zero(target, right_degree, c_degree, packet.field)
            inv_ok = ext_inversion_constant(
                target, right_degree, c_degree, packet.field
            )
            profiles[name][0] += int(row_ok)
            profiles[name][1] += int(zero_ok)
            profiles[name][2] += int(inv_ok)
            profiles[name][3] += int(zero_ok and inv_ok)
            profiles[name][4] += int(row_ok and zero_ok and inv_ok)
    return profiles, packet.h


def main() -> None:
    projector_counts = count_projector_profiles()
    right_combo_profiles, right_combo_rows = count_right_combo_profiles()

    print("Trace-GCD fixed-frequency actual-CM value-identity boundary")
    print("projector_row")
    print("  D=-5000")
    print(f"  q={PROJECTOR_Q}")
    print(f"  h={H}")
    print(f"  right_degree={TOP_QUOTIENT}")
    print(f"  c_degree={TOY_C_DEGREE}")
    print(f"  row_sum_independent_origins={projector_counts[0]}/{H}")
    print(f"  c_zero_fiber_origins={projector_counts[1]}/{H}")
    print(f"  inversion_constant_origins={projector_counts[2]}/{H}")
    print(f"  structural_zero_plus_inversion_origins={projector_counts[3]}/{H}")
    print(f"  all_three_value_identities_origins={projector_counts[4]}/{H}")
    print("right_combo_row")
    print("  D=-13319")
    print("  q=13463")
    print(f"  h={right_combo_rows}")
    print("  right_degree=2")
    print("  c_degree=5")
    for name, counts in right_combo_profiles.items():
        print(f"  profile={name}")
        print(f"    row_sum_independent_origins={counts[0]}/{right_combo_rows}")
        print(f"    c_zero_fiber_origins={counts[1]}/{right_combo_rows}")
        print(f"    inversion_constant_origins={counts[2]}/{right_combo_rows}")
        print(f"    structural_zero_plus_inversion_origins={counts[3]}/{right_combo_rows}")
        print(f"    all_three_value_identities_origins={counts[4]}/{right_combo_rows}")
    print("interpretation")
    print("  actual_cm_projector_fails_value_identities_generically=1")
    print("  actual_cm_right_combo_fails_value_identities_generically=1")
    print("  actual_cm_weighted_coefficients_fail_value_identities_generically=1")
    print("  actual_cm_selected_defects_fail_value_identities_generically=1")
    print("  selected_defects_only_force_c_zero_fiber_not_inversion_or_row_balance=1")
    print("  p24_needs_selected_weighted_packet_not_generic_actual_cm_value_symmetry=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_value_identity_boundary")

    if any(projector_counts):
        raise SystemExit(1)
    if any(right_combo_profiles["right_combo_resolvent"]):
        raise SystemExit(1)
    if any(right_combo_profiles["weighted_coefficients"]):
        raise SystemExit(1)
    selected_defects = right_combo_profiles["selected_defect_coefficients"]
    if selected_defects != [0, right_combo_rows, 0, 0, 0]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
