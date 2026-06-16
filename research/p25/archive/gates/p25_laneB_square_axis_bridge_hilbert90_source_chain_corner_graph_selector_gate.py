#!/usr/bin/env python3
"""Row-character selector for p25 Hilbert-90 source-chain corners.

The corner-normal-form gate leaves a small ambiguity: the cyclic C_507 corner
has four formal antiderivatives that recover the bridge, but only two are
source graphs.  This gate checks whether that source-graph condition is a new
mysterious selector or the already-seen C_3 row-balance condition.

On the four formal corners, these are equivalent:

* one point in each C_3 source row,
* equal row sums,
* vanishing nontrivial C_3 row characters.

Thus the corner target can be stated as a half-bridge corner plus C_3
row-balance.  This still does not select the C_169 lift or produce the raw
K-trace; it only eliminates the two cyclic antiderivatives that collapse
source rows.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import MODULUS
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    CornerAntiderivative,
    ActiveCornerRow,
    corner_profile,
)
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class CornerSelectorRow:
    center_d: int
    unit_d: int
    sign: int
    chain_q_values: tuple[int, ...]
    source_coords: tuple[tuple[int, int], ...]
    source_rows: tuple[int, ...]
    row_sums: tuple[int, int, int]
    signed_row_character_values: tuple[int, int, int]
    source_graph: bool
    row_balanced: bool
    nontrivial_row_characters_vanish: bool
    recovers_bridge: bool


@dataclass(frozen=True)
class ActiveSelectorRow:
    orientation_mask: int
    boundary_step_d: int
    boundary_direction_q: int
    chain_q_values: tuple[int, ...]
    source_coords: tuple[tuple[int, int], ...]
    row_sums: tuple[int, int, int]
    signed_row_character_values: tuple[int, int, int]
    source_graph: bool
    row_balanced: bool
    nontrivial_row_characters_vanish: bool
    recovers_bridge: bool


@dataclass(frozen=True)
class CornerGraphSelectorProfile:
    formal_rows: tuple[CornerSelectorRow, ...]
    active_rows: tuple[ActiveSelectorRow, ...]
    formal_row_count: int
    formal_source_graph_count: int
    formal_row_balanced_count: int
    formal_nontrivial_row_zero_count: int
    formal_source_graph_iff_row_balanced: bool
    formal_source_graph_iff_nontrivial_row_zero: bool
    all_formal_corners_recover_bridge: bool
    all_active_rows_source_graphs: bool
    all_active_rows_row_balanced: bool
    all_active_rows_have_nontrivial_row_zeros: bool
    active_row_sums: tuple[tuple[int, int, int], ...]


def signed_mod(value: int) -> int:
    value %= MODULUS
    return value if value <= MODULUS // 2 else value - MODULUS


def row_character_values(row_sums: tuple[int, int, int]) -> tuple[int, int, int]:
    root = primitive_root(MODULUS)
    zeta_3 = pow(root, (MODULUS - 1) // RIGHT_DEGREE, MODULUS)
    return tuple(
        signed_mod(
            sum(
                row_sums[row] * pow(zeta_3, character * row, MODULUS)
                for row in range(RIGHT_DEGREE)
            )
        )
        for character in range(RIGHT_DEGREE)
    )  # type: ignore[return-value]


def row_sums_for(q_values: tuple[int, ...], coefficient: int) -> tuple[int, int, int]:
    return tuple(
        sum(coefficient for q_value in q_values if q_value % RIGHT_DEGREE == row)
        for row in range(RIGHT_DEGREE)
    )  # type: ignore[return-value]


def row_balanced(row_sums: tuple[int, int, int]) -> bool:
    return len(set(row_sums)) == 1


def nontrivial_zeros(values: tuple[int, int, int]) -> bool:
    return values[1:] == (0, 0)


def formal_selector_row(corner: CornerAntiderivative) -> CornerSelectorRow:
    coefficients = {coefficient for _point, coefficient in corner.chain_word}
    if len(coefficients) != 1:
        raise AssertionError(f"corner coefficients are not constant: {corner}")
    coefficient = next(iter(coefficients))
    sums = row_sums_for(corner.chain_q_values, coefficient)
    chars = row_character_values(sums)
    return CornerSelectorRow(
        center_d=corner.center_d,
        unit_d=corner.unit_d,
        sign=corner.sign,
        chain_q_values=corner.chain_q_values,
        source_coords=tuple(coord_from_q(q_value) for q_value in corner.chain_q_values),
        source_rows=corner.source_rows,
        row_sums=sums,
        signed_row_character_values=chars,
        source_graph=corner.source_graph,
        row_balanced=row_balanced(sums),
        nontrivial_row_characters_vanish=nontrivial_zeros(chars),
        recovers_bridge=corner.recovers_bridge,
    )


def active_selector_row(active: ActiveCornerRow) -> ActiveSelectorRow:
    coefficients = {coefficient for _point, coefficient in active.chain_word}
    if len(coefficients) != 1:
        raise AssertionError(f"active coefficients are not constant: {active}")
    coefficient = next(iter(coefficients))
    sums = row_sums_for(active.chain_q_values, coefficient)
    chars = row_character_values(sums)
    return ActiveSelectorRow(
        orientation_mask=active.orientation_mask,
        boundary_step_d=active.boundary_step_d,
        boundary_direction_q=active.boundary_direction_q,
        chain_q_values=active.chain_q_values,
        source_coords=tuple(coord_from_q(q_value) for q_value in active.chain_q_values),
        row_sums=sums,
        signed_row_character_values=chars,
        source_graph=active.source_graph,
        row_balanced=row_balanced(sums),
        nontrivial_row_characters_vanish=nontrivial_zeros(chars),
        recovers_bridge=active.recovers_bridge,
    )


def selector_profile() -> CornerGraphSelectorProfile:
    profile = corner_profile()
    formal_rows = tuple(formal_selector_row(row) for row in profile.corner_antiderivatives)
    active_rows = tuple(active_selector_row(row) for row in profile.active_rows)
    return CornerGraphSelectorProfile(
        formal_rows=formal_rows,
        active_rows=active_rows,
        formal_row_count=len(formal_rows),
        formal_source_graph_count=sum(row.source_graph for row in formal_rows),
        formal_row_balanced_count=sum(row.row_balanced for row in formal_rows),
        formal_nontrivial_row_zero_count=sum(row.nontrivial_row_characters_vanish for row in formal_rows),
        formal_source_graph_iff_row_balanced=all(
            row.source_graph == row.row_balanced for row in formal_rows
        ),
        formal_source_graph_iff_nontrivial_row_zero=all(
            row.source_graph == row.nontrivial_row_characters_vanish for row in formal_rows
        ),
        all_formal_corners_recover_bridge=all(row.recovers_bridge for row in formal_rows),
        all_active_rows_source_graphs=all(row.source_graph for row in active_rows),
        all_active_rows_row_balanced=all(row.row_balanced for row in active_rows),
        all_active_rows_have_nontrivial_row_zeros=all(
            row.nontrivial_row_characters_vanish for row in active_rows
        ),
        active_row_sums=tuple(row.row_sums for row in active_rows),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner graph-selector gate")
    profile = selector_profile()
    expected_formal = (
        CornerSelectorRow(122, 1, 1, (0, 172, 482), ((0, 0), (1, 1), (2, 48)), (0, 1, 2), (-1, -1, -1), (-3, 0, 0), True, True, True, True),
        CornerSelectorRow(122, 506, 1, (0, 138, 335), ((0, 0), (0, 46), (2, 168)), (0, 0, 2), (-2, 0, -1), (-3, 974, -977), False, False, False, True),
        CornerSelectorRow(385, 1, -1, (0, 172, 369), ((0, 0), (1, 1), (0, 123)), (0, 0, 1), (2, 1, 0), (3, 977, -974), False, False, False, True),
        CornerSelectorRow(385, 506, -1, (0, 25, 335), ((0, 0), (1, 121), (2, 168)), (0, 1, 2), (1, 1, 1), (3, 0, 0), True, True, True, True),
    )
    expected_active = (
        ActiveSelectorRow(1, 122, 197, (0, 172, 482), ((0, 0), (1, 1), (2, 48)), (-1, -1, -1), (-3, 0, 0), True, True, True, True),
        ActiveSelectorRow(1, 385, 310, (172, 197, 369), ((1, 1), (2, 122), (0, 123)), (1, 1, 1), (3, 0, 0), True, True, True, True),
        ActiveSelectorRow(6, 122, 197, (138, 310, 335), ((0, 46), (1, 47), (2, 168)), (-1, -1, -1), (-3, 0, 0), True, True, True, True),
        ActiveSelectorRow(6, 385, 310, (0, 25, 335), ((0, 0), (1, 121), (2, 168)), (1, 1, 1), (3, 0, 0), True, True, True, True),
    )
    row_ok = (
        profile.formal_rows == expected_formal
        and profile.active_rows == expected_active
        and profile.formal_row_count == 4
        and profile.formal_source_graph_count == 2
        and profile.formal_row_balanced_count == 2
        and profile.formal_nontrivial_row_zero_count == 2
        and profile.formal_source_graph_iff_row_balanced
        and profile.formal_source_graph_iff_nontrivial_row_zero
        and profile.all_formal_corners_recover_bridge
        and profile.all_active_rows_source_graphs
        and profile.all_active_rows_row_balanced
        and profile.all_active_rows_have_nontrivial_row_zeros
        and profile.active_row_sums == ((-1, -1, -1), (1, 1, 1), (-1, -1, -1), (1, 1, 1))
    )

    print(
        "corner_graph_selector_summary: "
        f"formal_row_count={profile.formal_row_count} "
        f"formal_source_graph_count={profile.formal_source_graph_count} "
        f"formal_row_balanced_count={profile.formal_row_balanced_count} "
        f"formal_nontrivial_row_zero_count={profile.formal_nontrivial_row_zero_count} "
        f"source_graph_iff_row_balanced={int(profile.formal_source_graph_iff_row_balanced)} "
        f"source_graph_iff_nontrivial_row_zero={int(profile.formal_source_graph_iff_nontrivial_row_zero)} "
        f"all_active_rows_row_balanced={int(profile.all_active_rows_row_balanced)}"
    )
    print("formal_corner_selector_rows")
    for row in profile.formal_rows:
        print(f"  {row}")
    print("active_corner_selector_rows")
    for row in profile.active_rows:
        print(f"  {row}")
    print("selector_law")
    print("  among bridge-recovering cyclic corners, source_graph <=> equal C3 row sums")
    print("  equal C3 row sums <=> nontrivial C3 row characters vanish")
    print("  active source-chain rows are exactly row-balanced half-bridge corners")
    print("interpretation")
    print("  source_graph_condition_is_the_forced_C3_row_zero_condition_on_corners=1")
    print("  cyclic_C507_corner_alone_is_too_weak_because_non_graph_controls_recover_bridge=1")
    print("  row_balance_selects_the_graph_controls_but_not_the_C169_lift_or_raw_K_trace=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_graph_selector_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_graph_selector_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
