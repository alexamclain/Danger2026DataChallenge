#!/usr/bin/env python3
"""Corner selector for the p25 Hilbert-90 C_169 lift.

The corner graph-selector gate reduces the source-chain target to:

    half-bridge corner + C_3 row-balance.

This gate asks whether that cleaner corner formulation directly selects the
previously mysterious C_169 lift.  It does.  Among the thirteen primitive
C_169 projective lifts of the same C_13 shadow, the row-balanced half-bridge
corner graphs land only on the nonsplit lift (1,18,150).

This is intentionally narrower than the older minimal-boundary lift-selection
gate: it uses the corner normal form itself, rather than the whole
minimal-potential boundary search, to explain why the active lift is the
corner lift.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_graph_selector_gate import (
    selector_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate import (
    DiffTriple,
    cyclic_differences,
    projective_shape,
    projective_shape_profile,
    row_values_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C


WitnessKey = tuple[int, int, int, tuple[int, ...], tuple[int, int, int], DiffTriple]


@dataclass(frozen=True)
class CornerLiftRow:
    lift_shape_c169: DiffTriple
    corner_graph_witness_count: int
    corner_graph_witnesses: tuple[WitnessKey, ...]


@dataclass(frozen=True)
class CornerC169LiftSelectorProfile:
    canonical_c13_shadow: DiffTriple
    canonical_bridge_lift: DiffTriple
    c13_lift_count: int
    row_balanced_corner_count: int
    corner_graph_count: int
    corner_graph_shapes: tuple[DiffTriple, ...]
    rows: tuple[CornerLiftRow, ...]
    active_lift_count: int
    inactive_lift_count: int
    all_corner_graphs_use_canonical_lift: bool
    all_other_c13_lifts_inactive: bool


def witness_key(row) -> WitnessKey:
    row_values = row_values_from_q(row.chain_q_values, SQUARE_C)
    differences = cyclic_differences(row_values, SQUARE_C)
    return (
        row.center_d,
        row.unit_d,
        row.sign,
        row.chain_q_values,
        row_values,
        differences,
    )


def corner_c169_lift_selector_profile() -> CornerC169LiftSelectorProfile:
    projective = projective_shape_profile()
    selector = selector_profile()
    corner_graph_rows = tuple(row for row in selector.formal_rows if row.source_graph)
    corner_graph_shapes = tuple(
        projective_shape(
            cyclic_differences(row_values_from_q(row.chain_q_values, SQUARE_C), SQUARE_C),
            SQUARE_C,
        )
        for row in corner_graph_rows
    )
    rows = tuple(
        CornerLiftRow(
            lift_shape_c169=lift,
            corner_graph_witness_count=sum(shape == lift for shape in corner_graph_shapes),
            corner_graph_witnesses=tuple(
                witness_key(row)
                for row, shape in zip(corner_graph_rows, corner_graph_shapes)
                if shape == lift
            ),
        )
        for lift in projective.canonical_c13_lifts
    )
    active_rows = tuple(row for row in rows if row.corner_graph_witness_count)
    return CornerC169LiftSelectorProfile(
        canonical_c13_shadow=projective.canonical_projective_shape_c13,
        canonical_bridge_lift=projective.canonical_projective_shape_c169,
        c13_lift_count=projective.canonical_c13_lift_count,
        row_balanced_corner_count=selector.formal_row_balanced_count,
        corner_graph_count=selector.formal_source_graph_count,
        corner_graph_shapes=corner_graph_shapes,
        rows=rows,
        active_lift_count=len(active_rows),
        inactive_lift_count=len(rows) - len(active_rows),
        all_corner_graphs_use_canonical_lift=all(
            shape == projective.canonical_projective_shape_c169
            for shape in corner_graph_shapes
        ),
        all_other_c13_lifts_inactive=all(
            row.lift_shape_c169 == projective.canonical_projective_shape_c169
            or row.corner_graph_witness_count == 0
            for row in rows
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner C169-lift selector gate")
    profile = corner_c169_lift_selector_profile()
    expected_rows = (
        CornerLiftRow((1, 2, 166), 0, ()),
        CornerLiftRow((1, 4, 164), 0, ()),
        CornerLiftRow((1, 5, 163), 0, ()),
        CornerLiftRow((1, 7, 161), 0, ()),
        CornerLiftRow((1, 8, 160), 0, ()),
        CornerLiftRow((1, 10, 158), 0, ()),
        CornerLiftRow((1, 15, 153), 0, ()),
        CornerLiftRow(
            (1, 18, 150),
            2,
            (
                (122, 1, 1, (0, 172, 482), (0, 3, 144), (3, 141, 25)),
                (385, 506, -1, (0, 25, 335), (0, 25, 166), (25, 141, 3)),
            ),
        ),
        CornerLiftRow((1, 30, 138), 0, ()),
        CornerLiftRow((1, 31, 137), 0, ()),
        CornerLiftRow((1, 43, 125), 0, ()),
        CornerLiftRow((1, 49, 119), 0, ()),
        CornerLiftRow((1, 57, 111), 0, ()),
    )
    row_ok = (
        profile.canonical_c13_shadow == (1, 2, 10)
        and profile.canonical_bridge_lift == (1, 18, 150)
        and profile.c13_lift_count == 13
        and profile.row_balanced_corner_count == 2
        and profile.corner_graph_count == 2
        and profile.corner_graph_shapes == ((1, 18, 150), (1, 18, 150))
        and profile.rows == expected_rows
        and profile.active_lift_count == 1
        and profile.inactive_lift_count == 12
        and profile.all_corner_graphs_use_canonical_lift
        and profile.all_other_c13_lifts_inactive
    )

    print(
        "corner_c169_lift_selector_summary: "
        f"canonical_c13_shadow={profile.canonical_c13_shadow} "
        f"canonical_bridge_lift={profile.canonical_bridge_lift} "
        f"c13_lift_count={profile.c13_lift_count} "
        f"row_balanced_corner_count={profile.row_balanced_corner_count} "
        f"corner_graph_count={profile.corner_graph_count} "
        f"active_lift_count={profile.active_lift_count} "
        f"inactive_lift_count={profile.inactive_lift_count}"
    )
    print(f"corner_graph_shapes={profile.corner_graph_shapes}")
    print("corner_lift_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("selector_law")
    print("  row_balanced_half_bridge_corners_have_projective_C169_shape_(1,18,150)")
    print("  all_twelve_other_C13_shadow_lifts_have_zero_corner_graph_witnesses")
    print("interpretation")
    print("  half_bridge_corner_plus_C3_row_balance_selects_the_active_C169_lift=1")
    print("  active_lift_selection_no_longer_requires_the_full_minimal_boundary_search=1")
    print("  raw_K_trace_and_Kummer_cost_remain_unsolved=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
