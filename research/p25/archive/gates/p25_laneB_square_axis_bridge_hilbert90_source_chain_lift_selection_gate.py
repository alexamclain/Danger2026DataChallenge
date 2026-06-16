#!/usr/bin/env python3
"""Lift-selection screen for p25 Hilbert-90 source-chain witnesses.

The projective-shape gate shows that the bridge's C_13 projective shadow has
thirteen primitive C_169 lifts.  This gate asks which of those lifts actually
appears in the optimal support-three Hilbert-90 source-boundary witnesses.

Only the nonsplit lift (1,18,150) appears.  The other twelve C_169 lifts with
the same C_13 shadow have no bridge-compatible support-three source-graph
witness in the already classified minimal-potential boundary problem.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    BoundaryWitness,
    PotentialBoundaryRow,
    source_boundary_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate import (
    DiffTriple,
    ProjectiveShapeProfile,
    cyclic_differences,
    projective_shape,
    projective_shape_profile,
    row_values_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


WitnessKey = tuple[int, int, tuple[int, ...], tuple[int, ...]]


@dataclass(frozen=True)
class SupportThreeWitnessProfile:
    orientation_mask: int
    boundary_direction_q: int
    bridge_zero_compatible: bool
    source_graph: bool
    q_values: tuple[int, ...]
    coefficients: tuple[int, ...]
    projective_shape_c169: DiffTriple | None
    projective_shape_c13: DiffTriple | None


@dataclass(frozen=True)
class LiftSelectionRow:
    lift_shape_c169: DiffTriple
    bridge_source_graph_witness_count: int
    bridge_source_graph_witnesses: tuple[WitnessKey, ...]


@dataclass(frozen=True)
class LiftSelectionProfile:
    canonical_c13_shadow: DiffTriple
    canonical_bridge_lift: DiffTriple
    c13_lift_count: int
    rows: tuple[LiftSelectionRow, ...]
    total_support_three_witnesses: int
    support_three_source_graph_witnesses: int
    support_three_bridge_source_graph_witnesses: int
    support_three_nonbridge_nongraph_witnesses: int
    active_lift_count: int
    inactive_lift_count: int
    all_bridge_source_graph_witnesses_use_canonical_lift: bool
    all_other_c13_lifts_inactive: bool
    support_three_profiles: tuple[SupportThreeWitnessProfile, ...]


def one_point_per_row(q_values: tuple[int, ...]) -> bool:
    return len(q_values) == RIGHT_DEGREE and {q_value % RIGHT_DEGREE for q_value in q_values} == {0, 1, 2}


def support_three_profile(row: PotentialBoundaryRow, witness: BoundaryWitness) -> SupportThreeWitnessProfile:
    q_values = tuple(q_value for q_value, _coefficient in witness.antiderivative)
    coefficients = tuple(coefficient for _q_value, coefficient in witness.antiderivative)
    if one_point_per_row(q_values):
        values_c169 = row_values_from_q(q_values, SQUARE_C)
        differences_c169 = cyclic_differences(values_c169, SQUARE_C)
        shape_c169: DiffTriple | None = projective_shape(differences_c169, SQUARE_C)
        shape_c13: DiffTriple | None = projective_shape(tuple(value % 13 for value in differences_c169), 13)
    else:
        shape_c169 = None
        shape_c13 = None
    return SupportThreeWitnessProfile(
        orientation_mask=row.orientation_mask,
        boundary_direction_q=witness.direction_q,
        bridge_zero_compatible=row.bridge_zero_compatible,
        source_graph=one_point_per_row(q_values),
        q_values=q_values,
        coefficients=coefficients,
        projective_shape_c169=shape_c169,
        projective_shape_c13=shape_c13,
    )


def witness_key(profile: SupportThreeWitnessProfile) -> WitnessKey:
    return (
        profile.orientation_mask,
        profile.boundary_direction_q,
        profile.q_values,
        profile.coefficients,
    )


def support_three_profiles() -> tuple[SupportThreeWitnessProfile, ...]:
    boundary_profile = source_boundary_profile()
    return tuple(
        support_three_profile(row, witness)
        for row in boundary_profile.rows
        if row.minimal_antiderivative_support == RIGHT_DEGREE
        for witness in row.best_witnesses
    )


def lift_selection_profile() -> LiftSelectionProfile:
    projective_profile: ProjectiveShapeProfile = projective_shape_profile()
    profiles = support_three_profiles()
    bridge_graph_profiles = tuple(
        profile
        for profile in profiles
        if profile.bridge_zero_compatible and profile.source_graph
    )
    rows = tuple(
        LiftSelectionRow(
            lift_shape_c169=lift,
            bridge_source_graph_witness_count=sum(
                profile.projective_shape_c169 == lift for profile in bridge_graph_profiles
            ),
            bridge_source_graph_witnesses=tuple(
                witness_key(profile)
                for profile in bridge_graph_profiles
                if profile.projective_shape_c169 == lift
            ),
        )
        for lift in projective_profile.canonical_c13_lifts
    )
    active_lifts = tuple(row for row in rows if row.bridge_source_graph_witness_count)
    return LiftSelectionProfile(
        canonical_c13_shadow=projective_profile.canonical_projective_shape_c13,
        canonical_bridge_lift=projective_profile.canonical_projective_shape_c169,
        c13_lift_count=projective_profile.canonical_c13_lift_count,
        rows=rows,
        total_support_three_witnesses=len(profiles),
        support_three_source_graph_witnesses=sum(profile.source_graph for profile in profiles),
        support_three_bridge_source_graph_witnesses=len(bridge_graph_profiles),
        support_three_nonbridge_nongraph_witnesses=sum(
            (not profile.bridge_zero_compatible) and (not profile.source_graph)
            for profile in profiles
        ),
        active_lift_count=len(active_lifts),
        inactive_lift_count=len(rows) - len(active_lifts),
        all_bridge_source_graph_witnesses_use_canonical_lift=all(
            profile.projective_shape_c169 == projective_profile.canonical_projective_shape_c169
            for profile in bridge_graph_profiles
        ),
        all_other_c13_lifts_inactive=all(
            row.lift_shape_c169 == projective_profile.canonical_projective_shape_c169
            or row.bridge_source_graph_witness_count == 0
            for row in rows
        ),
        support_three_profiles=profiles,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain lift-selection gate")
    profile = lift_selection_profile()
    expected_rows = (
        LiftSelectionRow((1, 2, 166), 0, ()),
        LiftSelectionRow((1, 4, 164), 0, ()),
        LiftSelectionRow((1, 5, 163), 0, ()),
        LiftSelectionRow((1, 7, 161), 0, ()),
        LiftSelectionRow((1, 8, 160), 0, ()),
        LiftSelectionRow((1, 10, 158), 0, ()),
        LiftSelectionRow((1, 15, 153), 0, ()),
        LiftSelectionRow(
            (1, 18, 150),
            4,
            (
                (1, 197, (0, 172, 482), (-1, -1, -1)),
                (1, 310, (172, 197, 369), (1, 1, 1)),
                (6, 197, (138, 310, 335), (-1, -1, -1)),
                (6, 310, (0, 25, 335), (1, 1, 1)),
            ),
        ),
        LiftSelectionRow((1, 30, 138), 0, ()),
        LiftSelectionRow((1, 31, 137), 0, ()),
        LiftSelectionRow((1, 43, 125), 0, ()),
        LiftSelectionRow((1, 49, 119), 0, ()),
        LiftSelectionRow((1, 57, 111), 0, ()),
    )
    expected_support_three_profiles = (
        SupportThreeWitnessProfile(1, 197, True, True, (0, 172, 482), (-1, -1, -1), (1, 18, 150), (1, 2, 10)),
        SupportThreeWitnessProfile(1, 310, True, True, (172, 197, 369), (1, 1, 1), (1, 18, 150), (1, 2, 10)),
        SupportThreeWitnessProfile(3, 197, False, False, (172, 310, 482), (-1, -1, -1), None, None),
        SupportThreeWitnessProfile(3, 310, False, False, (0, 172, 369), (1, 1, 1), None, None),
        SupportThreeWitnessProfile(4, 197, False, False, (0, 138, 335), (-1, -1, -1), None, None),
        SupportThreeWitnessProfile(4, 310, False, False, (25, 197, 335), (1, 1, 1), None, None),
        SupportThreeWitnessProfile(6, 197, True, True, (138, 310, 335), (-1, -1, -1), (1, 18, 150), (1, 2, 10)),
        SupportThreeWitnessProfile(6, 310, True, True, (0, 25, 335), (1, 1, 1), (1, 18, 150), (1, 2, 10)),
    )
    row_ok = (
        profile.canonical_c13_shadow == (1, 2, 10)
        and profile.canonical_bridge_lift == (1, 18, 150)
        and profile.c13_lift_count == 13
        and profile.rows == expected_rows
        and profile.total_support_three_witnesses == 8
        and profile.support_three_source_graph_witnesses == 4
        and profile.support_three_bridge_source_graph_witnesses == 4
        and profile.support_three_nonbridge_nongraph_witnesses == 4
        and profile.active_lift_count == 1
        and profile.inactive_lift_count == 12
        and profile.all_bridge_source_graph_witnesses_use_canonical_lift
        and profile.all_other_c13_lifts_inactive
        and profile.support_three_profiles == expected_support_three_profiles
    )

    print(
        "source_chain_lift_selection_summary: "
        f"canonical_c13_shadow={profile.canonical_c13_shadow} "
        f"canonical_bridge_lift={profile.canonical_bridge_lift} "
        f"c13_lift_count={profile.c13_lift_count} "
        f"active_lift_count={profile.active_lift_count} "
        f"inactive_lift_count={profile.inactive_lift_count}"
    )
    print(
        "support_three_witness_counts: "
        f"total={profile.total_support_three_witnesses} "
        f"source_graph={profile.support_three_source_graph_witnesses} "
        f"bridge_source_graph={profile.support_three_bridge_source_graph_witnesses} "
        f"nonbridge_nongraph={profile.support_three_nonbridge_nongraph_witnesses}"
    )
    print("lift_selection_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("support_three_profiles")
    for row in profile.support_three_profiles:
        print(f"  {row}")
    print("interpretation")
    print("  only_one_of_the_thirteen_C13_shadow_lifts_has_bridge_support3_source_graph_witnesses=1")
    print("  the_active_lift_is_the_nonsplit_C169_projective_shape_1_18_150=1")
    print("  nonbridge_support3_controls_are_not_one_point_per_source_row=1")
    print("  producer_must_select_the_active_C169_lift_before_the_rigid_197_310_boundary=1")
    print(f"square_axis_bridge_hilbert90_source_chain_lift_selection_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_lift_selection_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
