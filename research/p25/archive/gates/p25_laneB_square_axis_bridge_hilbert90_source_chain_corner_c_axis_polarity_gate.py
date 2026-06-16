#!/usr/bin/env python3
"""C-axis polarity law for the p25 Hilbert-90 corner skew orientation.

The skew-orientation gate defined the local score by summing centered skew
residuals.  This gate records the simpler producer-facing law behind it.

For every one-cancellation source translation, the three centered skew
residuals telescope to three times the centered C_169 component of the
translation.  Thus

    orientation_score = 3 * chain_coefficient * signed_c(direction).

The recorded branch is exactly the one-cancellation branch with
coefficient-weighted signed C-step -28; the opposite short branch has +28.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_orientation_gate import (
    skew_orientation_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C


Coord = tuple[int, int]


@dataclass(frozen=True)
class CAxisPolarityDirectionRow:
    direction_q: int
    direction_source_step: Coord
    signed_c_step: int
    coefficient_weighted_signed_c_step: int
    orientation_score: int
    score_from_c_polarity: int
    branch_role: str


@dataclass(frozen=True)
class CAxisPolarityRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    chain_coefficient: int
    weighted_signed_c_values: tuple[int, ...]
    recorded_weighted_signed_c_step: int
    opposite_weighted_signed_c_step: int
    recorded_orientation_score: int
    opposite_orientation_score: int
    polarity_direction_rows: tuple[CAxisPolarityDirectionRow, ...]


@dataclass(frozen=True)
class CAxisPolarityProfile:
    row_count: int
    all_orientation_scores_are_triple_c_polarity: bool
    all_weighted_signed_c_sets_are_standard: bool
    all_recorded_branches_are_negative_28_polarity: bool
    all_opposite_short_branches_are_positive_28_polarity: bool
    all_negative_28_polarity_branches_are_recorded: bool
    rows: tuple[CAxisPolarityRow, ...]


def signed_c(value: int) -> int:
    value %= SQUARE_C
    return value if value <= SQUARE_C // 2 else value - SQUARE_C


def polarity_row(orientation_row) -> CAxisPolarityRow:
    direction_rows: list[CAxisPolarityDirectionRow] = []
    for one_cancel in orientation_row.one_cancellation_rows:
        c_step = signed_c(one_cancel.direction_source_step[1])
        weighted_c_step = orientation_row.chain_coefficient * c_step
        direction_rows.append(
            CAxisPolarityDirectionRow(
                direction_q=one_cancel.direction_q,
                direction_source_step=one_cancel.direction_source_step,
                signed_c_step=c_step,
                coefficient_weighted_signed_c_step=weighted_c_step,
                orientation_score=one_cancel.orientation_score,
                score_from_c_polarity=3 * weighted_c_step,
                branch_role=one_cancel.branch_role,
            )
        )
    rows_tuple = tuple(direction_rows)
    recorded = tuple(row for row in rows_tuple if row.direction_q == orientation_row.recorded_direction_q)
    opposite = tuple(row for row in rows_tuple if row.direction_q == orientation_row.opposite_direction_q)
    if len(recorded) != 1 or len(opposite) != 1:
        raise AssertionError("recorded/opposite branch missing from polarity scan")
    return CAxisPolarityRow(
        orientation_mask=orientation_row.orientation_mask,
        recorded_direction_q=orientation_row.recorded_direction_q,
        opposite_direction_q=orientation_row.opposite_direction_q,
        chain_coefficient=orientation_row.chain_coefficient,
        weighted_signed_c_values=tuple(sorted(row.coefficient_weighted_signed_c_step for row in rows_tuple)),
        recorded_weighted_signed_c_step=recorded[0].coefficient_weighted_signed_c_step,
        opposite_weighted_signed_c_step=opposite[0].coefficient_weighted_signed_c_step,
        recorded_orientation_score=recorded[0].orientation_score,
        opposite_orientation_score=opposite[0].orientation_score,
        polarity_direction_rows=rows_tuple,
    )


def c_axis_polarity_profile() -> CAxisPolarityProfile:
    rows = tuple(polarity_row(row) for row in skew_orientation_profile().rows)
    return CAxisPolarityProfile(
        row_count=len(rows),
        all_orientation_scores_are_triple_c_polarity=all(
            direction.orientation_score == direction.score_from_c_polarity
            for row in rows
            for direction in row.polarity_direction_rows
        ),
        all_weighted_signed_c_sets_are_standard=all(
            row.weighted_signed_c_values == (-28, -25, -3, 3, 25, 28)
            for row in rows
        ),
        all_recorded_branches_are_negative_28_polarity=all(
            row.recorded_weighted_signed_c_step == -28
            and row.recorded_orientation_score == -84
            for row in rows
        ),
        all_opposite_short_branches_are_positive_28_polarity=all(
            row.opposite_weighted_signed_c_step == 28
            and row.opposite_orientation_score == 84
            for row in rows
        ),
        all_negative_28_polarity_branches_are_recorded=all(
            tuple(
                direction.direction_q
                for direction in row.polarity_direction_rows
                if direction.coefficient_weighted_signed_c_step == -28
            )
            == (row.recorded_direction_q,)
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner C-axis polarity gate")
    profile = c_axis_polarity_profile()
    expected_rows = (
        CAxisPolarityRow(
            1, 197, 310, -1, (-28, -25, -3, 3, 25, 28), -28, 28, -84, 84,
            (
                CAxisPolarityDirectionRow(25, (1, 25), 25, -25, -75, -75, "other_one_cancellation"),
                CAxisPolarityDirectionRow(172, (1, 3), 3, -3, -9, -9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(197, (2, 28), 28, -28, -84, -84, "recorded"),
                CAxisPolarityDirectionRow(310, (1, 141), -28, 28, 84, 84, "opposite_short"),
                CAxisPolarityDirectionRow(335, (2, 166), -3, 3, 9, 9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(482, (2, 144), -25, 25, 75, 75, "other_one_cancellation"),
            ),
        ),
        CAxisPolarityRow(
            1, 310, 197, 1, (-28, -25, -3, 3, 25, 28), -28, 28, -84, 84,
            (
                CAxisPolarityDirectionRow(25, (1, 25), 25, 25, 75, 75, "other_one_cancellation"),
                CAxisPolarityDirectionRow(172, (1, 3), 3, 3, 9, 9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(197, (2, 28), 28, 28, 84, 84, "opposite_short"),
                CAxisPolarityDirectionRow(310, (1, 141), -28, -28, -84, -84, "recorded"),
                CAxisPolarityDirectionRow(335, (2, 166), -3, -3, -9, -9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(482, (2, 144), -25, -25, -75, -75, "other_one_cancellation"),
            ),
        ),
        CAxisPolarityRow(
            6, 197, 310, -1, (-28, -25, -3, 3, 25, 28), -28, 28, -84, 84,
            (
                CAxisPolarityDirectionRow(25, (1, 25), 25, -25, -75, -75, "other_one_cancellation"),
                CAxisPolarityDirectionRow(172, (1, 3), 3, -3, -9, -9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(197, (2, 28), 28, -28, -84, -84, "recorded"),
                CAxisPolarityDirectionRow(310, (1, 141), -28, 28, 84, 84, "opposite_short"),
                CAxisPolarityDirectionRow(335, (2, 166), -3, 3, 9, 9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(482, (2, 144), -25, 25, 75, 75, "other_one_cancellation"),
            ),
        ),
        CAxisPolarityRow(
            6, 310, 197, 1, (-28, -25, -3, 3, 25, 28), -28, 28, -84, 84,
            (
                CAxisPolarityDirectionRow(25, (1, 25), 25, 25, 75, 75, "other_one_cancellation"),
                CAxisPolarityDirectionRow(172, (1, 3), 3, 3, 9, 9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(197, (2, 28), 28, 28, 84, 84, "opposite_short"),
                CAxisPolarityDirectionRow(310, (1, 141), -28, -28, -84, -84, "recorded"),
                CAxisPolarityDirectionRow(335, (2, 166), -3, -3, -9, -9, "other_one_cancellation"),
                CAxisPolarityDirectionRow(482, (2, 144), -25, -25, -75, -75, "other_one_cancellation"),
            ),
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_orientation_scores_are_triple_c_polarity
        and profile.all_weighted_signed_c_sets_are_standard
        and profile.all_recorded_branches_are_negative_28_polarity
        and profile.all_opposite_short_branches_are_positive_28_polarity
        and profile.all_negative_28_polarity_branches_are_recorded
        and profile.rows == expected_rows
    )

    print(
        "corner_c_axis_polarity_summary: "
        f"weighted_c_sets={tuple(row.weighted_signed_c_values for row in profile.rows)} "
        f"recorded_weighted_c={tuple(row.recorded_weighted_signed_c_step for row in profile.rows)} "
        f"opposite_weighted_c={tuple(row.opposite_weighted_signed_c_step for row in profile.rows)} "
        f"recorded_scores={tuple(row.recorded_orientation_score for row in profile.rows)}"
    )
    print("corner_c_axis_polarity_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("c_axis_polarity_laws")
    print("  orientation_score equals 3 * chain_coefficient * centered_C169_direction_component")
    print("  one-cancellation directions have coefficient-weighted signed C steps {-28,-25,-3,3,25,28}")
    print("  the recorded branch is the unique coefficient-weighted signed C step -28")
    print("interpretation")
    print("  local_skew_orientation_reduces_to_C_axis_polarity_before_inversion=1")
    print("  opposite_197_310_branch_has_C_axis_polarity_plus_28=1")
    print("  producer_can_target_one_cancellation_plus_negative_28_C_polarity=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_c_axis_polarity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c_axis_polarity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
