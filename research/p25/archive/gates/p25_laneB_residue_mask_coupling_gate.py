#!/usr/bin/env python3
"""Residue-mask coupling gate for p25 Lane B.

The residue-coset mask gate says the canonical theta_{3,1} target is a union of
actual local residue rectangles.  This gate asks whether that rectangle mask
could come from separated right-only/C-only data.

It cannot.  The C_3 x C_c carry mask has rank 3 over both F_2 and an odd field,
has nonzero mixed second differences, and has the required four-level column
profile.  A separated local-unit producer would give a row-only, column-only,
rank-1, or row-plus-column rank <= 2 mask; all of those are ruled out.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import rank_mod
from p25_laneB_local_pullback_gate import CASES as PULLBACK_CASES, PullbackCase
from p25_selected_defect_value_gate import RIGHT_DEGREE


ODD_RANK_FIELD = 1_000_003


@dataclass(frozen=True)
class CouplingProfile:
    row_sums: tuple[int, ...]
    column_sum_histogram: dict[int, int]
    rank_f2: int
    rank_odd: int
    mixed_second_differences_z: int
    mixed_second_differences_f2: int
    right_only: bool
    c_only: bool
    additive_separable_z: bool
    additive_separable_f2: bool


def mask_matrix(c_axis: int) -> list[list[int]]:
    return [
        [template_bits(c_axis, c_index)[right] for c_index in range(c_axis)]
        for right in range(RIGHT_DEGREE)
    ]


def column_sum_histogram(matrix: list[list[int]]) -> dict[int, int]:
    c_axis = len(matrix[0])
    histogram: dict[int, int] = {}
    for c_index in range(c_axis):
        column_sum = sum(matrix[right][c_index] for right in range(RIGHT_DEGREE))
        histogram[column_sum] = histogram.get(column_sum, 0) + 1
    return dict(sorted(histogram.items()))


def mixed_second_difference_counts(matrix: list[list[int]]) -> tuple[int, int]:
    c_axis = len(matrix[0])
    integer_count = 0
    f2_count = 0
    for right_a in range(RIGHT_DEGREE):
        for right_b in range(right_a + 1, RIGHT_DEGREE):
            for c_a in range(c_axis):
                for c_b in range(c_a + 1, c_axis):
                    value = (
                        matrix[right_a][c_a]
                        + matrix[right_b][c_b]
                        - matrix[right_a][c_b]
                        - matrix[right_b][c_a]
                    )
                    integer_count += int(value != 0)
                    f2_count += int(value % 2 != 0)
    return integer_count, f2_count


def is_right_only(matrix: list[list[int]]) -> bool:
    return all(len(set(row)) == 1 for row in matrix)


def is_c_only(matrix: list[list[int]]) -> bool:
    c_axis = len(matrix[0])
    return all(
        len({matrix[right][c_index] for right in range(RIGHT_DEGREE)}) == 1
        for c_index in range(c_axis)
    )


def profile(case: PullbackCase) -> CouplingProfile:
    matrix = mask_matrix(case.c_axis)
    mixed_z, mixed_f2 = mixed_second_difference_counts(matrix)
    return CouplingProfile(
        row_sums=tuple(sum(row) for row in matrix),
        column_sum_histogram=column_sum_histogram(matrix),
        rank_f2=rank_mod(matrix, 2),
        rank_odd=rank_mod(matrix, ODD_RANK_FIELD),
        mixed_second_differences_z=mixed_z,
        mixed_second_differences_f2=mixed_f2,
        right_only=is_right_only(matrix),
        c_only=is_c_only(matrix),
        additive_separable_z=mixed_z == 0,
        additive_separable_f2=mixed_f2 == 0,
    )


def expected_column_histogram(c_axis: int) -> dict[int, int]:
    m_value = (c_axis - 1) // 4
    return {0: m_value + 1, 1: m_value, 2: m_value, 3: m_value}


def audit_case(case: PullbackCase) -> tuple[list[str], bool]:
    current = profile(case)
    m_value = (case.c_axis - 1) // 4
    expected_row_sum = 2 * m_value
    expected_histogram = expected_column_histogram(case.c_axis)
    row_ok = (
        current.row_sums == (expected_row_sum,) * RIGHT_DEGREE
        and current.column_sum_histogram == expected_histogram
        and current.rank_f2 == RIGHT_DEGREE
        and current.rank_odd == RIGHT_DEGREE
        and current.mixed_second_differences_z > 0
        and current.mixed_second_differences_f2 > 0
        and not current.right_only
        and not current.c_only
        and not current.additive_separable_z
        and not current.additive_separable_f2
    )
    lines = [
        (
            f"case {case.name}: c={case.c_axis} m={m_value} "
            f"row_sums={list(current.row_sums)} "
            f"expected_row_sum={expected_row_sum} "
            f"column_sum_histogram={current.column_sum_histogram} "
            f"expected_column_sum_histogram={expected_histogram} "
            f"rank_f2={current.rank_f2} rank_odd={current.rank_odd} "
            f"mixed_second_differences_z={current.mixed_second_differences_z} "
            f"mixed_second_differences_f2={current.mixed_second_differences_f2} "
            f"right_only={int(current.right_only)} "
            f"c_only={int(current.c_only)} "
            f"additive_separable_z={int(current.additive_separable_z)} "
            f"additive_separable_f2={int(current.additive_separable_f2)} "
            f"ok={int(row_ok)}"
        )
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B residue-mask coupling gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in PULLBACK_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"residue_mask_coupling_rows={ok_rows}/{len(PULLBACK_CASES)}")
    print("interpretation")
    print("  residue_mask_has_full_right_rank_over_F2_and_odd_fields=1")
    print("  residue_mask_has_nonzero_mixed_second_differences=1")
    print("  separated_right_only_or_C_only_local_units_are_ruled_out=1")
    print("  row_plus_column_separable_masks_are_ruled_out=1")
    print("conclusion=reported_p25_laneB_residue_mask_coupling_gate")
    return 0 if ok_rows == len(PULLBACK_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
