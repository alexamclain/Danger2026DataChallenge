#!/usr/bin/env python3
"""Section-choice obstruction for the p24 trace-average anchor route.

The anchor trace-defect profile is

    D_r = Tr_relative(j_{r+m*bullet}) - n * j_r.

This gate tests a tempting compression: perhaps the quotient trace profile
`Tr_relative(j_{r+m*bullet})` already determines the anchor equations, so the
selected child profile `j_r` would not need an embedded producer.  It does
not.  The same quotient trace profile can pass or fail the anchor depending
on which child section is selected.

The second half checks the same sensitivity on the pinned actual-CM
right-combo analogue D=-13319, q=13463, m=28, n=5: globally shifting the child
section changes the anchor defect, and no shift makes the generic analogue
pass.  Thus the p24 proof must produce an embedded section or an equivalent
section-aware defect payload; unordered relative trace coefficients alone are
not enough.
"""

from __future__ import annotations

import random

from trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary import (
    weighted_coefficients,
)
from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    load_actual_packet,
)
from trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate import (
    FIELD_Q,
    LEFT,
    M,
    ORDER7,
    RELATIVE,
    RIGHT,
    TRIALS,
    all_equal,
    h_coset_sums,
    log_table,
    primitive_root_mod_prime,
    random_j_values,
)


P24_M = 66254
P24_SQRT_FLOOR = 10**12
SEED = 20260606


def quotient_trace_profile(j_values: list[int]) -> list[int]:
    profile = [0] * RIGHT
    for residue in range(1, RIGHT):
        total = 0
        for r in range(residue, M, RIGHT):
            total = (
                total
                + sum(j_values[r + M * child] for child in range(RELATIVE))
            ) % FIELD_Q
        profile[residue] = total
    return profile


def selected_child_profile(j_values: list[int], child: int) -> list[int]:
    profile = [0] * RIGHT
    for residue in range(1, RIGHT):
        total = 0
        for r in range(residue, M, RIGHT):
            total = (total + j_values[r + M * child]) % FIELD_Q
        profile[residue] = total
    return profile


def defect_profile_for_child(j_values: list[int], child: int) -> list[int]:
    trace = quotient_trace_profile(j_values)
    selected = selected_child_profile(j_values, child)
    return [
        (trace[residue] - RELATIVE * selected[residue]) % FIELD_Q
        for residue in range(RIGHT)
    ]


def trace_only_counterexample(logs: dict[int, int]) -> tuple[bool, bool, bool]:
    """Build one table where the same trace profile has opposite verdicts.

    For every right residue, put a chosen trace value T into one left slot.
    Choose child 0 to be T/n, child 1 to be 0, and child 2 to carry the
    remaining trace.  Then child 0 has zero defect, while child 1 has defect T.
    """

    rng = random.Random(SEED + 17)
    inv_n = pow(RELATIVE, -1, FIELD_Q)
    j_values = [0] * (M * RELATIVE)
    trace_values = [0] * RIGHT
    while all_equal(h_coset_sums(trace_values, logs)):
        for residue in range(1, RIGHT):
            trace_values[residue] = rng.randrange(FIELD_Q)

    for residue in range(1, RIGHT):
        trace = trace_values[residue]
        j_values[residue] = trace * inv_n % FIELD_Q
        j_values[residue + 2 * M] = (trace - j_values[residue]) % FIELD_Q

    trace_profile = quotient_trace_profile(j_values)
    child0_defect = defect_profile_for_child(j_values, 0)
    child1_defect = defect_profile_for_child(j_values, 1)
    same_trace_profile = trace_profile == trace_values
    child0_passes = all_equal(h_coset_sums(child0_defect, logs))
    child1_passes = all_equal(h_coset_sums(child1_defect, logs))
    return same_trace_profile, child0_passes, child1_passes


def random_child_shift_changes(logs: dict[int, int]) -> int:
    rng = random.Random(SEED + 31)
    changes = 0
    for _trial in range(TRIALS):
        j_values = random_j_values(rng)
        sums0 = h_coset_sums(defect_profile_for_child(j_values, 0), logs)
        sums1 = h_coset_sums(defect_profile_for_child(j_values, 1), logs)
        changes += int(sums0 != sums1)
    return changes


def actual_cm_shift_audit() -> tuple[int, int, int]:
    packet = load_actual_packet()
    field = packet.field
    coefficients = weighted_coefficients(packet)
    total = field.zero
    for coeff in coefficients:
        total = field.add(total, coeff)

    defects = [
        field.sub(total, field.scalar_mul(packet.n, coefficients[child]))
        for child in range(packet.n)
    ]
    zeroes = sum(defect == field.zero for defect in defects)
    distinct_defects = len(set(defects))
    distinct_child_coefficients = len(set(coefficients))
    return zeroes, distinct_defects, distinct_child_coefficients


def main() -> None:
    right_generator = primitive_root_mod_prime(RIGHT)
    logs = log_table(RIGHT, right_generator)

    same_trace_profile, child0_passes, child1_passes = trace_only_counterexample(logs)
    random_changes = random_child_shift_changes(logs)
    actual_zeroes, actual_distinct_defects, actual_distinct_coeffs = actual_cm_shift_audit()

    trace_only_payload = P24_M
    trace_plus_child_payload = 2 * P24_M

    print("Trace-GCD fixed-frequency p24 section-choice obstruction gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_left={LEFT}")
    print(f"toy_right={RIGHT}")
    print(f"toy_right_generator={right_generator}")
    print(f"toy_relative={RELATIVE}")
    print(f"toy_m={M}")
    print(f"toy_h_cosets={ORDER7}")
    print(f"same_trace_profile_counterexample={int(same_trace_profile)}")
    print(f"same_trace_child0_anchor_passes={int(child0_passes)}")
    print(f"same_trace_child1_anchor_passes={int(child1_passes)}")
    print(f"random_child_shift_changes_defect_sums={random_changes}/{TRIALS}")
    print("actual_cm_D=-13319")
    print("actual_cm_q=13463")
    print("actual_cm_m=28")
    print("actual_cm_n=5")
    print(f"actual_cm_global_child_shift_anchor_zeroes={actual_zeroes}/5")
    print(f"actual_cm_global_child_shift_distinct_defects={actual_distinct_defects}/5")
    print(f"actual_cm_distinct_child_coefficients={actual_distinct_coeffs}/5")
    print(f"p24_trace_only_profile_payload={trace_only_payload}")
    print(f"p24_trace_plus_child_profile_payload={trace_plus_child_payload}")
    print(
        "p24_trace_plus_child_profile_payload_over_sqrt="
        f"{trace_plus_child_payload / P24_SQRT_FLOOR:.12e}"
    )
    print("interpretation")
    print("  quotient_trace_profile_alone_does_not_determine_anchor=1")
    print("  selected_child_section_is_arithmetic_data_not_bookkeeping=1")
    print("  unordered_relative_trace_coefficients_do_not_authenticate_defect=1")
    print("  p24_anchor_producer_must_be_section_aware=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate")

    if not same_trace_profile:
        raise SystemExit(1)
    if not child0_passes or child1_passes:
        raise SystemExit(1)
    if random_changes != TRIALS:
        raise SystemExit(1)
    if actual_zeroes != 0:
        raise SystemExit(1)
    if actual_distinct_defects != 5 or actual_distinct_coeffs != 5:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
