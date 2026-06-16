#!/usr/bin/env python3
"""Local orientation selector for the p25 Hilbert-90 corner skew derivative.

The skew-derivative selector leaves a twofold near miss: directions 197 and
310 both give one cancellation and residual short lengths 31 and 53.  Later
gates select the recorded branch by the Hilbert-90 image.  This gate records a
smaller local selector that is visible before the inversion image is taken.

For each one-cancellation direction, sum the signed C_169 skew residuals using
the centered representatives in [-84, 84], then multiply by the constant chain
coefficient.  Among the six one-cancellation directions, the recorded branch
is the unique score -84.  The opposite short branch is the unique score +84.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_gate import (
    chain_by_source_row,
    signed_short_step,
    source_coord,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_gate import (
    skew_derivative_selector_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C


Coord = tuple[int, int]


@dataclass(frozen=True)
class OneCancellationOrientationRow:
    direction_q: int
    direction_d: int
    direction_source_step: Coord
    cancellation_row: int
    signed_deltas: tuple[int, int, int]
    residual_short_steps: tuple[int, ...]
    orientation_score: int
    branch_role: str


@dataclass(frozen=True)
class SkewOrientationRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    chain_q_values: tuple[int, ...]
    chain_coefficient: int
    score_values: tuple[int, ...]
    recorded_orientation_score: int
    opposite_orientation_score: int
    unique_min_direction_q: int
    unique_max_direction_q: int
    one_cancellation_rows: tuple[OneCancellationOrientationRow, ...]


@dataclass(frozen=True)
class SkewOrientationProfile:
    row_count: int
    all_rows_have_six_one_cancellation_directions: bool
    all_score_sets_are_standard: bool
    all_recorded_branches_are_unique_min_score: bool
    all_opposite_short_branches_are_unique_max_score: bool
    all_min_max_branches_are_the_197_310_pair: bool
    rows: tuple[SkewOrientationRow, ...]


def signed_delta(delta: int) -> int:
    delta %= SQUARE_C
    return delta if delta <= SQUARE_C // 2 else delta - SQUARE_C


def constant_chain_coefficient(chain_rows: dict[int, tuple[int, int, int]]) -> int:
    coefficients = {coefficient for _q_value, _c_value, coefficient in chain_rows.values()}
    if len(coefficients) != 1:
        raise AssertionError(f"expected constant chain coefficient, got {coefficients}")
    return next(iter(coefficients))


def orientation_data(chain: dict[int, int], direction_q: int) -> tuple[int, tuple[int, int, int], tuple[int, ...], tuple[int, ...]]:
    chain_rows = chain_by_source_row(chain)
    coefficient = constant_chain_coefficient(chain_rows)
    direction_row, direction_c = source_coord(direction_q)
    signed_deltas: list[int] = []
    cancellation_rows: list[int] = []
    short_steps: list[int] = []
    for target_row in range(3):
        shifted_from_row = (target_row - direction_row) % 3
        _orig_q, original_c, _orig_coeff = chain_rows[target_row]
        _shift_q, shift_c, _shift_coeff = chain_rows[shifted_from_row]
        delta = (shift_c + direction_c - original_c) % SQUARE_C
        signed_deltas.append(signed_delta(delta))
        if delta == 0:
            cancellation_rows.append(target_row)
        else:
            short_steps.append(signed_short_step(delta))
    return (
        coefficient * sum(signed_deltas),
        tuple(signed_deltas),  # type: ignore[return-value]
        tuple(cancellation_rows),
        tuple(sorted(short_steps)),
    )


def scan_row(active_row, opposite_direction_q: int) -> SkewOrientationRow:
    chain = dict(zip(active_row.q_values, active_row.recorded_coefficients))
    chain_rows = chain_by_source_row(chain)
    chain_coefficient = constant_chain_coefficient(chain_rows)
    rows: list[OneCancellationOrientationRow] = []
    for direction_q in range(1, QUOTIENT_ORDER):
        score, signed_deltas, cancellation_rows, short_steps = orientation_data(chain, direction_q)
        if len(cancellation_rows) != 1:
            continue
        if direction_q == active_row.boundary_direction_q:
            role = "recorded"
        elif direction_q == opposite_direction_q:
            role = "opposite_short"
        else:
            role = "other_one_cancellation"
        rows.append(
            OneCancellationOrientationRow(
                direction_q=direction_q,
                direction_d=d_residue_from_q(direction_q),
                direction_source_step=source_coord(direction_q),
                cancellation_row=cancellation_rows[0],
                signed_deltas=signed_deltas,
                residual_short_steps=short_steps,
                orientation_score=score,
                branch_role=role,
            )
        )
    rows_tuple = tuple(rows)
    score_values = tuple(sorted(row.orientation_score for row in rows_tuple))
    min_score = min(score_values)
    max_score = max(score_values)
    min_rows = tuple(row for row in rows_tuple if row.orientation_score == min_score)
    max_rows = tuple(row for row in rows_tuple if row.orientation_score == max_score)
    if len(min_rows) != 1 or len(max_rows) != 1:
        raise AssertionError("orientation score did not have unique extrema")
    recorded_score = tuple(
        row.orientation_score for row in rows_tuple if row.direction_q == active_row.boundary_direction_q
    )
    opposite_score = tuple(
        row.orientation_score for row in rows_tuple if row.direction_q == opposite_direction_q
    )
    if len(recorded_score) != 1 or len(opposite_score) != 1:
        raise AssertionError("recorded/opposite direction was not a one-cancellation row")
    return SkewOrientationRow(
        orientation_mask=active_row.orientation_mask,
        recorded_direction_q=active_row.boundary_direction_q,
        opposite_direction_q=opposite_direction_q,
        chain_q_values=active_row.q_values,
        chain_coefficient=chain_coefficient,
        score_values=score_values,
        recorded_orientation_score=recorded_score[0],
        opposite_orientation_score=opposite_score[0],
        unique_min_direction_q=min_rows[0].direction_q,
        unique_max_direction_q=max_rows[0].direction_q,
        one_cancellation_rows=rows_tuple,
    )


def skew_orientation_profile() -> SkewOrientationProfile:
    opposite_by_key = {
        (row.orientation_mask, row.recorded_direction_q): row.opposite_direction_q
        for row in skew_derivative_selector_profile().rows
    }
    rows = tuple(
        scan_row(active_row, opposite_by_key[(active_row.orientation_mask, active_row.boundary_direction_q)])
        for active_row in coefficient_rigidity_profile().rows
    )
    return SkewOrientationProfile(
        row_count=len(rows),
        all_rows_have_six_one_cancellation_directions=all(
            len(row.one_cancellation_rows) == 6 for row in rows
        ),
        all_score_sets_are_standard=all(
            row.score_values == (-84, -75, -9, 9, 75, 84) for row in rows
        ),
        all_recorded_branches_are_unique_min_score=all(
            row.recorded_orientation_score == -84
            and row.unique_min_direction_q == row.recorded_direction_q
            for row in rows
        ),
        all_opposite_short_branches_are_unique_max_score=all(
            row.opposite_orientation_score == 84
            and row.unique_max_direction_q == row.opposite_direction_q
            for row in rows
        ),
        all_min_max_branches_are_the_197_310_pair=all(
            tuple(sorted((row.unique_min_direction_q, row.unique_max_direction_q))) == (197, 310)
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner skew-orientation gate")
    profile = skew_orientation_profile()
    expected_rows = (
        SkewOrientationRow(
            1, 197, 310, (0, 172, 482), -1, (-84, -75, -9, 9, 75, 84), -84, 84, 197, 310,
            (
                OneCancellationOrientationRow(25, 121, (1, 25), 0, (0, 22, 53), (22, 53), -75, "other_one_cancellation"),
                OneCancellationOrientationRow(172, 1, (1, 3), 1, (-22, 0, 31), (22, 31), -9, "other_one_cancellation"),
                OneCancellationOrientationRow(197, 122, (2, 28), 1, (31, 0, 53), (31, 53), -84, "recorded"),
                OneCancellationOrientationRow(310, 385, (1, 141), 2, (-53, -31, 0), (31, 53), 84, "opposite_short"),
                OneCancellationOrientationRow(335, 506, (2, 166), 0, (0, -31, 22), (22, 31), 9, "other_one_cancellation"),
                OneCancellationOrientationRow(482, 386, (2, 144), 2, (-22, -53, 0), (22, 53), 75, "other_one_cancellation"),
            ),
        ),
        SkewOrientationRow(
            1, 310, 197, (172, 197, 369), 1, (-84, -75, -9, 9, 75, 84), -84, 84, 310, 197,
            (
                OneCancellationOrientationRow(25, 121, (1, 25), 2, (22, 53, 0), (22, 53), 75, "other_one_cancellation"),
                OneCancellationOrientationRow(172, 1, (1, 3), 0, (0, 31, -22), (22, 31), 9, "other_one_cancellation"),
                OneCancellationOrientationRow(197, 122, (2, 28), 0, (0, 53, 31), (31, 53), 84, "opposite_short"),
                OneCancellationOrientationRow(310, 385, (1, 141), 1, (-31, 0, -53), (31, 53), -84, "recorded"),
                OneCancellationOrientationRow(335, 506, (2, 166), 2, (-31, 22, 0), (22, 31), -9, "other_one_cancellation"),
                OneCancellationOrientationRow(482, 386, (2, 144), 1, (-53, 0, -22), (22, 53), -75, "other_one_cancellation"),
            ),
        ),
        SkewOrientationRow(
            6, 197, 310, (138, 310, 335), -1, (-84, -75, -9, 9, 75, 84), -84, 84, 197, 310,
            (
                OneCancellationOrientationRow(25, 121, (1, 25), 2, (53, 22, 0), (22, 53), -75, "other_one_cancellation"),
                OneCancellationOrientationRow(172, 1, (1, 3), 1, (31, 0, -22), (22, 31), -9, "other_one_cancellation"),
                OneCancellationOrientationRow(197, 122, (2, 28), 2, (31, 53, 0), (31, 53), -84, "recorded"),
                OneCancellationOrientationRow(310, 385, (1, 141), 0, (0, -31, -53), (31, 53), 84, "opposite_short"),
                OneCancellationOrientationRow(335, 506, (2, 166), 0, (0, 22, -31), (22, 31), 9, "other_one_cancellation"),
                OneCancellationOrientationRow(482, 386, (2, 144), 1, (-22, 0, -53), (22, 53), 75, "other_one_cancellation"),
            ),
        ),
        SkewOrientationRow(
            6, 310, 197, (0, 25, 335), 1, (-84, -75, -9, 9, 75, 84), -84, 84, 310, 197,
            (
                OneCancellationOrientationRow(25, 121, (1, 25), 1, (22, 0, 53), (22, 53), 75, "other_one_cancellation"),
                OneCancellationOrientationRow(172, 1, (1, 3), 0, (0, -22, 31), (22, 31), 9, "other_one_cancellation"),
                OneCancellationOrientationRow(197, 122, (2, 28), 1, (53, 0, 31), (31, 53), 84, "opposite_short"),
                OneCancellationOrientationRow(310, 385, (1, 141), 2, (-31, -53, 0), (31, 53), -84, "recorded"),
                OneCancellationOrientationRow(335, 506, (2, 166), 2, (22, -31, 0), (22, 31), -9, "other_one_cancellation"),
                OneCancellationOrientationRow(482, 386, (2, 144), 0, (0, -53, -22), (22, 53), -75, "other_one_cancellation"),
            ),
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_have_six_one_cancellation_directions
        and profile.all_score_sets_are_standard
        and profile.all_recorded_branches_are_unique_min_score
        and profile.all_opposite_short_branches_are_unique_max_score
        and profile.all_min_max_branches_are_the_197_310_pair
        and profile.rows == expected_rows
    )

    print(
        "corner_skew_orientation_summary: "
        f"score_sets={tuple(row.score_values for row in profile.rows)} "
        f"recorded_scores={tuple(row.recorded_orientation_score for row in profile.rows)} "
        f"opposite_scores={tuple(row.opposite_orientation_score for row in profile.rows)} "
        f"unique_min_dirs={tuple(row.unique_min_direction_q for row in profile.rows)} "
        f"unique_max_dirs={tuple(row.unique_max_direction_q for row in profile.rows)}"
    )
    print("corner_skew_orientation_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("orientation_laws")
    print("  every active corner has exactly six one-cancellation first-boundary directions")
    print("  coefficient-weighted signed skew residual scores are always {-84,-75,-9,9,75,84}")
    print("  the recorded branch is the unique local minimum score -84")
    print("  the opposite short branch is the unique local maximum score +84")
    print("interpretation")
    print("  producer_can_select_the_recorded_197_310_branch_by_local_skew_orientation_before_inversion=1")
    print("  opposite_197_310_branch_has_the_opposite_local_orientation_score=1")
    print("  q0_endpoint_and_31_53_lengths_are_weaker_than_the_signed_skew_orientation=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_skew_orientation_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_orientation_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
