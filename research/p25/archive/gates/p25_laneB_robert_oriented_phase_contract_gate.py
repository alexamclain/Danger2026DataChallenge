#!/usr/bin/env python3
"""Robert oriented-phase contract for the p25 square-axis bridge.

The x-difference obstruction says that a literal x-only Robert table is too
even.  This gate records the finite sign pattern a successful oriented
Robert/Siegel producer must supply.

On the raw source rectangle C_75 x C_169, the bridge support is already a
coupled D-segment/K-trace object.  Its signs, however, are exactly a C-side
odd orientation on the three active C-pairs:

    positive C-values: 25, 28, 31
    negative C-values: 144, 141, 138 = -25, -28, -31 mod 169.

Thus an oriented C-side phase recovers the signed bridge from the unsigned
coupled bridge hull.  But the same C-side phase applied to a separated
right-trace-times-C hull overproduces by a factor of three and has zero mixed
right/C payload.  A row-only phase is impossible because every raw right row
contains both a positive and a negative bridge point.

Producer consequence: the Robert lane needs both pieces at once:

* a coupled unsigned support/magnitude, not a separated C selector;
* an oriented C-side quotient/unit phase, not an x-only even table.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_source_matrix_harness_gate import (
    raw_from_source_matrix,
    source_matrix_from_raw,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
)


@dataclass(frozen=True)
class PhaseProfile:
    positive_c_values: tuple[int, ...]
    negative_c_values: tuple[int, ...]
    negative_is_c_inversion: bool
    rows_with_both_signs: int
    rows_with_single_sign: int
    c_phase_recovers_target: bool
    c_phase_odd_on_active_pairs: bool


def source_index(right_log: int, c_log: int) -> int:
    return right_log * C_ORDER + c_log


def active_entries(matrix: list[int]) -> list[tuple[int, int, int]]:
    return [
        (right_log, c_log, matrix[source_index(right_log, c_log)])
        for right_log in range(RIGHT_ORDER)
        for c_log in range(C_ORDER)
        if matrix[source_index(right_log, c_log)]
    ]


def active_c_phase(positive_c_values: tuple[int, ...], negative_c_values: tuple[int, ...]) -> list[int]:
    phase = [0] * C_ORDER
    for c_log in positive_c_values:
        phase[c_log] = 1
    for c_log in negative_c_values:
        phase[c_log] = -1
    return phase


def multiply_by_c_phase(unsigned_matrix: list[int], phase: list[int]) -> list[int]:
    out = [0] * (RIGHT_ORDER * C_ORDER)
    for right_log in range(RIGHT_ORDER):
        for c_log in range(C_ORDER):
            out[source_index(right_log, c_log)] = (
                unsigned_matrix[source_index(right_log, c_log)] * phase[c_log]
            )
    return out


def separated_axis_hull(phase: list[int]) -> list[int]:
    out = [0] * (RIGHT_ORDER * C_ORDER)
    for right_log in range(RIGHT_ORDER):
        for c_log, value in enumerate(phase):
            if value:
                out[source_index(right_log, c_log)] = value
    return out


def row_sign_counts(entries: list[tuple[int, int, int]]) -> tuple[int, int]:
    rows_with_both = 0
    rows_with_single = 0
    for right_log in range(RIGHT_ORDER):
        signs = {
            value
            for row, _c_log, value in entries
            if row == right_log
        }
        rows_with_both += int(signs == {-1, 1})
        rows_with_single += int(signs in ({-1}, {1}))
    return rows_with_both, rows_with_single


def c_phase_odd(phase: list[int]) -> bool:
    for c_log, value in enumerate(phase):
        inv_value = phase[(-c_log) % C_ORDER]
        if value or inv_value:
            if inv_value != -value:
                return False
    return True


def phase_profile(target_matrix: list[int]) -> PhaseProfile:
    entries = active_entries(target_matrix)
    positive_c_values = tuple(sorted({c_log for _right, c_log, value in entries if value > 0}))
    negative_c_values = tuple(sorted({c_log for _right, c_log, value in entries if value < 0}))
    unsigned_matrix = [abs(value) for value in target_matrix]
    phase = active_c_phase(positive_c_values, negative_c_values)
    oriented = multiply_by_c_phase(unsigned_matrix, phase)
    rows_with_both, rows_with_single = row_sign_counts(entries)
    return PhaseProfile(
        positive_c_values=positive_c_values,
        negative_c_values=negative_c_values,
        negative_is_c_inversion=tuple(sorted((-c_log) % C_ORDER for c_log in positive_c_values))
        == negative_c_values,
        rows_with_both_signs=rows_with_both,
        rows_with_single_sign=rows_with_single,
        c_phase_recovers_target=oriented == target_matrix,
        c_phase_odd_on_active_pairs=c_phase_odd(phase),
    )


def main() -> int:
    print("p25 Lane B Robert oriented-phase contract gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    target_raw = target_raw_bridge()
    target_matrix = source_matrix_from_raw(target_raw)
    unsigned_matrix = [abs(value) for value in target_matrix]
    profile = phase_profile(target_matrix)
    phase = active_c_phase(profile.positive_c_values, profile.negative_c_values)
    oriented_matrix = multiply_by_c_phase(unsigned_matrix, phase)
    axis_matrix = separated_axis_hull(phase)

    target_candidate = profile_candidate(
        "signed_bridge_target",
        raw_from_source_matrix(target_matrix),
        target_raw,
    )
    unsigned_candidate = profile_candidate(
        "unsigned_coupled_bridge_hull",
        raw_from_source_matrix(unsigned_matrix),
        target_raw,
    )
    oriented_candidate = profile_candidate(
        "c_oriented_unsigned_bridge_hull",
        raw_from_source_matrix(oriented_matrix),
        target_raw,
    )
    axis_candidate = profile_candidate(
        "c_oriented_separated_axis_hull",
        raw_from_source_matrix(axis_matrix),
        target_raw,
    )

    row_ok = (
        target_candidate.ok
        and not unsigned_candidate.ok
        and oriented_candidate.ok
        and not axis_candidate.ok
        and axis_candidate.raw_support == 450
        and axis_candidate.quotient_mixed_nonzero == 0
        and profile.positive_c_values == (25, 28, 31)
        and profile.negative_c_values == (138, 141, 144)
        and profile.negative_is_c_inversion
        and profile.rows_with_both_signs == RIGHT_ORDER
        and profile.rows_with_single_sign == 0
        and profile.c_phase_recovers_target
        and profile.c_phase_odd_on_active_pairs
    )

    print(f"phase_profile={profile}")
    print("candidate_profiles")
    print(f"  target={target_candidate}")
    print(f"  unsigned_coupled_hull={unsigned_candidate}")
    print(f"  c_oriented_coupled_hull={oriented_candidate}")
    print(f"  c_oriented_axis_hull={axis_candidate}")
    print("phase_contract")
    print("  row-only orientation is impossible: every right row has both signs")
    print("  C-side odd orientation recovers the signed bridge from the coupled unsigned hull")
    print("  C-side orientation without the coupled D/K support overproduces and has no mixed payload")
    print(f"robert_oriented_phase_contract_rows={int(row_ok)}/1")
    print("interpretation")
    print("  robert_lane_needs_coupled_unsigned_support_plus_oriented_C_phase=1")
    print("  c_phase_is_necessary_but_not_sufficient_without_D_segment_support=1")
    print("  separated_right_trace_times_oriented_C_selector_is_rejected=1")
    print("conclusion=reported_p25_laneB_robert_oriented_phase_contract_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
