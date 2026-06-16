#!/usr/bin/env python3
"""K-trace invariance mechanism for p25 Hilbert-90 source-chain corners.

The raw K-trace gate established empirically that block K-trace lifts are the
only tested trace-correct lifts satisfying the raw D^3 = Y relation.  This gate
records the mechanism:

    3*S_STEP - Y_STEP = 507,

the raw kernel shift.  Therefore raw D^3 = Y on a corner lift is exactly
invariance under the C_25 kernel shift.  Sparse sections and hidden modes fail
the raw relation by precisely their K-boundary defect.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_gate import (
    row_newton_triangle_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate import (
    LiftKind,
    raw_lift,
    relation_mismatch_profile,
    trace_correct,
)
from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import (
    solve_d_exponent,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    KERNEL_SHIFT,
    MODULUS,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_bridge_raw_source_gate import square_axis_case
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class LiftInvarianceRow:
    orientation_mask: int
    boundary_direction_q: int
    lift_kind: LiftKind
    raw_support: int
    trace_correct: bool
    k_boundary_mismatches: int
    k_boundary_q_count: int
    k_boundary_per_q_values: tuple[int, ...]
    raw_relation_mismatches: int
    raw_relation_q_count: int
    raw_relation_per_q_values: tuple[int, ...]
    relation_defect_equals_k_boundary_defect: bool
    d_residue_classes: tuple[int, ...]


@dataclass(frozen=True)
class LiftKindSummary:
    lift_kind: LiftKind
    row_count: int
    trace_correct_rows: int
    k_boundary_mismatch_values: tuple[int, ...]
    raw_relation_mismatch_values: tuple[int, ...]
    k_boundary_q_count_values: tuple[int, ...]
    per_q_mismatch_profiles: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class KTraceInvarianceProfile:
    kernel_raw_shift: int
    d3_minus_y_raw_shift: int
    primitive_d_kernel_exponent: int
    canonical_d_residue_classes: tuple[int, ...]
    block_k_trace_d_residue_classes: tuple[tuple[int, ...], ...]
    rows: tuple[LiftInvarianceRow, ...]
    summaries: tuple[LiftKindSummary, ...]
    all_relation_defects_equal_k_boundary_defects: bool
    only_block_k_trace_is_trace_correct_and_k_invariant: bool
    sparse_section_failure_is_two_kernel_edges_per_corner_point: bool
    hidden_mode_failure_is_full_kernel_cycle_per_corner_point: bool


def k_boundary_mismatch_profile(raw: list[int]) -> tuple[int, int, tuple[int, ...]]:
    by_q: dict[int, int] = {}
    for index in range(len(raw)):
        if raw[(index + QUOTIENT_ORDER) % len(raw)] % MODULUS != raw[index] % MODULUS:
            q_value = index % QUOTIENT_ORDER
            by_q[q_value] = by_q.get(q_value, 0) + 1
    return sum(by_q.values()), len(by_q), tuple(sorted(set(by_q.values())))


def d_residue_classes(raw: list[int]) -> tuple[int, ...]:
    residues: set[int] = set()
    for index, value in enumerate(raw):
        if not value % MODULUS:
            continue
        source_coord = (index % RIGHT_ORDER, index % C_ORDER)
        residues.add(solve_d_exponent(source_coord) % QUOTIENT_ORDER)
    return tuple(sorted(residues))


def lift_row(active_row, lift_kind: LiftKind, zeta_b: int) -> LiftInvarianceRow:
    raw = raw_lift(active_row, lift_kind, zeta_b)
    k_mismatches, k_q_count, k_per_q = k_boundary_mismatch_profile(raw)
    relation_mismatches, relation_q_count, relation_per_q = relation_mismatch_profile(raw)
    return LiftInvarianceRow(
        orientation_mask=active_row.orientation_mask,
        boundary_direction_q=active_row.boundary_direction_q,
        lift_kind=lift_kind,
        raw_support=sum(1 for value in raw if value % MODULUS),
        trace_correct=trace_correct(active_row, raw),
        k_boundary_mismatches=k_mismatches,
        k_boundary_q_count=k_q_count,
        k_boundary_per_q_values=k_per_q,
        raw_relation_mismatches=relation_mismatches,
        raw_relation_q_count=relation_q_count,
        raw_relation_per_q_values=relation_per_q,
        relation_defect_equals_k_boundary_defect=(
            (k_mismatches, k_q_count, k_per_q)
            == (relation_mismatches, relation_q_count, relation_per_q)
        ),
        d_residue_classes=d_residue_classes(raw),
    )


def summarize_kind(rows: tuple[LiftInvarianceRow, ...], lift_kind: LiftKind) -> LiftKindSummary:
    kind_rows = tuple(row for row in rows if row.lift_kind == lift_kind)
    return LiftKindSummary(
        lift_kind=lift_kind,
        row_count=len(kind_rows),
        trace_correct_rows=sum(row.trace_correct for row in kind_rows),
        k_boundary_mismatch_values=tuple(sorted({row.k_boundary_mismatches for row in kind_rows})),
        raw_relation_mismatch_values=tuple(sorted({row.raw_relation_mismatches for row in kind_rows})),
        k_boundary_q_count_values=tuple(sorted({row.k_boundary_q_count for row in kind_rows})),
        per_q_mismatch_profiles=tuple(sorted({row.k_boundary_per_q_values for row in kind_rows})),
    )


def k_trace_invariance_profile() -> KTraceInvarianceProfile:
    case = square_axis_case()
    root = primitive_root(MODULUS)
    zeta_b = pow(root, (MODULUS - 1) // case.b_trace, MODULUS)
    lift_kinds: tuple[LiftKind, ...] = (
        "block_k_trace",
        "sparse_section",
        "block_plus_hidden_mode",
        "hidden_mode_only",
    )
    rows = tuple(
        lift_row(active_row, lift_kind, zeta_b)
        for active_row in corner_profile().active_rows
        for lift_kind in lift_kinds
    )
    summaries = tuple(summarize_kind(rows, lift_kind) for lift_kind in lift_kinds)
    block_rows = tuple(row for row in rows if row.lift_kind == "block_k_trace")
    sparse_rows = tuple(row for row in rows if row.lift_kind == "sparse_section")
    hidden_rows = tuple(
        row for row in rows if row.lift_kind in {"block_plus_hidden_mode", "hidden_mode_only"}
    )
    return KTraceInvarianceProfile(
        kernel_raw_shift=QUOTIENT_ORDER,
        d3_minus_y_raw_shift=(3 * S_STEP - Y_STEP) % case.raw_order,
        primitive_d_kernel_exponent=solve_d_exponent(KERNEL_SHIFT),
        canonical_d_residue_classes=row_newton_triangle_profile().rows[0].d_by_source_row,
        block_k_trace_d_residue_classes=tuple(row.d_residue_classes for row in block_rows),
        rows=rows,
        summaries=summaries,
        all_relation_defects_equal_k_boundary_defects=all(
            row.relation_defect_equals_k_boundary_defect for row in rows
        ),
        only_block_k_trace_is_trace_correct_and_k_invariant=(
            sum(row.trace_correct and row.k_boundary_mismatches == 0 for row in rows) == len(block_rows)
            and all(row.trace_correct and row.k_boundary_mismatches == 0 for row in block_rows)
        ),
        sparse_section_failure_is_two_kernel_edges_per_corner_point=all(
            row.k_boundary_mismatches == 6
            and row.k_boundary_q_count == 3
            and row.k_boundary_per_q_values == (2,)
            for row in sparse_rows
        ),
        hidden_mode_failure_is_full_kernel_cycle_per_corner_point=all(
            row.k_boundary_mismatches == 75
            and row.k_boundary_q_count == 3
            and row.k_boundary_per_q_values == (25,)
            for row in hidden_rows
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner K-trace-invariance gate")
    profile = k_trace_invariance_profile()
    expected_summaries = (
        LiftKindSummary("block_k_trace", 4, 4, (0,), (0,), (0,), ((),)),
        LiftKindSummary("sparse_section", 4, 4, (6,), (6,), (3,), ((2,),)),
        LiftKindSummary("block_plus_hidden_mode", 4, 4, (75,), (75,), (3,), ((25,),)),
        LiftKindSummary("hidden_mode_only", 4, 0, (75,), (75,), (3,), ((25,),)),
    )
    row_ok = (
        profile.kernel_raw_shift == 507
        and profile.d3_minus_y_raw_shift == 507
        and profile.primitive_d_kernel_exponent == 4056
        and profile.canonical_d_residue_classes == (0, 1, 386)
        and profile.block_k_trace_d_residue_classes
        == ((0, 1, 386), (1, 122, 123), (384, 385, 506), (0, 121, 506))
        and profile.summaries == expected_summaries
        and profile.all_relation_defects_equal_k_boundary_defects
        and profile.only_block_k_trace_is_trace_correct_and_k_invariant
        and profile.sparse_section_failure_is_two_kernel_edges_per_corner_point
        and profile.hidden_mode_failure_is_full_kernel_cycle_per_corner_point
    )

    print(
        "corner_k_trace_invariance_summary: "
        f"kernel_raw_shift={profile.kernel_raw_shift} "
        f"d3_minus_y_raw_shift={profile.d3_minus_y_raw_shift} "
        f"primitive_d_kernel_exponent={profile.primitive_d_kernel_exponent} "
        f"canonical_d_residue_classes={profile.canonical_d_residue_classes} "
        f"block_d_residue_classes={profile.block_k_trace_d_residue_classes}"
    )
    print("lift_kind_summaries")
    for summary in profile.summaries:
        print(f"  {summary}")
    print("k_trace_invariance_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("mechanism")
    print("  3*S_STEP - Y_STEP is exactly the raw kernel shift 507")
    print("  raw D^3=Y failures are exactly K-boundary failures on every tested lift")
    print("  sparse sections fail by two K-boundary edges on each of the three corner points")
    print("  nontrivial hidden modes fail around the full 25-point kernel cycle")
    print("interpretation")
    print("  raw_K_trace_is_the_mechanism_that_restores_D3_equals_Y=1")
    print("  quotient_or_sparse_corner_lifts_fail_because_they_are_not_K_invariant=1")
    print("  producer_must_realize_the_K_invariant_row_triangle_not_only_the_quotient_triangle=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_k_trace_invariance_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_invariance_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
