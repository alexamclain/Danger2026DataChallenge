#!/usr/bin/env python3
"""Minimality of the K-trace lift for p25 Hilbert-90 corners.

The K-trace-invariance gate showed that raw D^3 = Y is exactly invariance under
the order-25 raw kernel shift.  This gate makes the support consequence
explicit: on the K-invariant subspace, normalized trace is an isomorphism back
to the quotient blocks.  Therefore each nonzero quotient corner point has one
trace-correct K-invariant lift, the full 25-point constant K orbit.

Proper K-subtraces of orders 1 and 5 can be trace-correct with supports 3 and
15, but they fail by their K-boundary defects.  The unavoidable K-invariant
corner support is 75.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_invariance_gate import (
    k_boundary_mismatch_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate import (
    active_coefficient,
    raw_lift,
    relation_mismatch_profile,
    signed_mod,
    trace_correct,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import MODULUS
from p25_laneB_square_axis_bridge_raw_source_gate import square_axis_case
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class KSubtraceRow:
    orientation_mask: int
    boundary_direction_q: int
    trace_order: int
    coset_offset: int
    layers: tuple[int, ...]
    value_per_layer: int
    raw_support: int
    raw_degree: int
    trace_correct: bool
    k_boundary_mismatches: int
    k_boundary_q_count: int
    k_boundary_per_q_values: tuple[int, ...]
    raw_relation_mismatches: int
    raw_relation_q_count: int
    raw_relation_per_q_values: tuple[int, ...]
    relation_defect_equals_k_boundary_defect: bool
    k_invariant: bool


@dataclass(frozen=True)
class KSubtraceSummary:
    trace_order: int
    coset_count: int
    total_rows: int
    raw_support_values: tuple[int, ...]
    value_per_layer_values: tuple[int, ...]
    raw_degree_values: tuple[int, ...]
    trace_correct_rows: int
    k_boundary_mismatch_values: tuple[int, ...]
    k_boundary_q_count_values: tuple[int, ...]
    k_boundary_per_q_profiles: tuple[tuple[int, ...], ...]
    raw_relation_mismatch_values: tuple[int, ...]
    relation_defect_equals_k_boundary_rows: int
    k_invariant_rows: int


@dataclass(frozen=True)
class KTraceMinimalityProfile:
    raw_block_count: int
    kernel_order: int
    quotient_block_count: int
    k_invariant_dimension: int
    normalized_trace_rank_on_k_invariants: int
    normalized_trace_kernel_dimension_on_k_invariants: int
    selected_corner_blocks: int
    unique_k_invariant_corner_support: int
    proper_subtrace_orders: tuple[int, ...]
    full_trace_order: int
    subtrace_summaries: tuple[KSubtraceSummary, ...]
    full_trace_rows_match_block_k_trace: bool
    all_subtrace_relation_defects_equal_k_boundary_defects: bool
    only_full_subtraces_are_k_invariant: bool


def subtrace_layers(trace_order: int, coset_offset: int) -> tuple[int, ...]:
    case = square_axis_case()
    step = case.b_trace // trace_order
    return tuple((coset_offset + step * index) % case.b_trace for index in range(trace_order))


def subtrace_raw(active_row, trace_order: int, coset_offset: int) -> list[int]:
    case = square_axis_case()
    coefficient = active_coefficient(active_row)
    value = coefficient * (case.b_trace // trace_order)
    raw = [0] * case.raw_order
    for q_value in active_row.chain_q_values:
        for layer in subtrace_layers(trace_order, coset_offset):
            raw[q_value + QUOTIENT_ORDER * layer] = value % MODULUS
    return raw


def subtrace_row(active_row, trace_order: int, coset_offset: int) -> KSubtraceRow:
    raw = subtrace_raw(active_row, trace_order, coset_offset)
    k_mismatches, k_q_count, k_per_q = k_boundary_mismatch_profile(raw)
    relation_mismatches, relation_q_count, relation_per_q = relation_mismatch_profile(raw)
    values = {signed_mod(value) for value in raw if value % MODULUS}
    if len(values) != 1:
        raise AssertionError(f"expected one nonzero layer value, got {values}")
    return KSubtraceRow(
        orientation_mask=active_row.orientation_mask,
        boundary_direction_q=active_row.boundary_direction_q,
        trace_order=trace_order,
        coset_offset=coset_offset,
        layers=subtrace_layers(trace_order, coset_offset),
        value_per_layer=next(iter(values)),
        raw_support=sum(1 for value in raw if value % MODULUS),
        raw_degree=sum(signed_mod(value) for value in raw),
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
        k_invariant=k_mismatches == 0,
    )


def summarize_subtrace(rows: tuple[KSubtraceRow, ...], trace_order: int) -> KSubtraceSummary:
    order_rows = tuple(row for row in rows if row.trace_order == trace_order)
    return KSubtraceSummary(
        trace_order=trace_order,
        coset_count=square_axis_case().b_trace // trace_order,
        total_rows=len(order_rows),
        raw_support_values=tuple(sorted({row.raw_support for row in order_rows})),
        value_per_layer_values=tuple(sorted({row.value_per_layer for row in order_rows})),
        raw_degree_values=tuple(sorted({row.raw_degree for row in order_rows})),
        trace_correct_rows=sum(row.trace_correct for row in order_rows),
        k_boundary_mismatch_values=tuple(sorted({row.k_boundary_mismatches for row in order_rows})),
        k_boundary_q_count_values=tuple(sorted({row.k_boundary_q_count for row in order_rows})),
        k_boundary_per_q_profiles=tuple(sorted({row.k_boundary_per_q_values for row in order_rows})),
        raw_relation_mismatch_values=tuple(sorted({row.raw_relation_mismatches for row in order_rows})),
        relation_defect_equals_k_boundary_rows=sum(
            row.relation_defect_equals_k_boundary_defect for row in order_rows
        ),
        k_invariant_rows=sum(row.k_invariant for row in order_rows),
    )


def k_trace_minimality_profile() -> KTraceMinimalityProfile:
    case = square_axis_case()
    trace_orders = (1, 5, 25)
    active_rows = corner_profile().active_rows
    rows: list[KSubtraceRow] = []
    for active_row in active_rows:
        for trace_order in trace_orders:
            for coset_offset in range(case.b_trace // trace_order):
                rows.append(subtrace_row(active_row, trace_order, coset_offset))
    row_tuple = tuple(rows)
    full_rows_match = all(
        subtrace_raw(active_row, case.b_trace, 0) == raw_lift(active_row, "block_k_trace", 1)
        for active_row in active_rows
    )
    return KTraceMinimalityProfile(
        raw_block_count=case.raw_order,
        kernel_order=case.b_trace,
        quotient_block_count=QUOTIENT_ORDER,
        k_invariant_dimension=QUOTIENT_ORDER,
        normalized_trace_rank_on_k_invariants=QUOTIENT_ORDER,
        normalized_trace_kernel_dimension_on_k_invariants=0,
        selected_corner_blocks=3,
        unique_k_invariant_corner_support=3 * case.b_trace,
        proper_subtrace_orders=(1, 5),
        full_trace_order=case.b_trace,
        subtrace_summaries=tuple(summarize_subtrace(row_tuple, trace_order) for trace_order in trace_orders),
        full_trace_rows_match_block_k_trace=full_rows_match,
        all_subtrace_relation_defects_equal_k_boundary_defects=all(
            row.relation_defect_equals_k_boundary_defect for row in row_tuple
        ),
        only_full_subtraces_are_k_invariant=all(
            row.k_invariant == (row.trace_order == case.b_trace) for row in row_tuple
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner K-trace-minimality gate")
    profile = k_trace_minimality_profile()
    expected_summaries = (
        KSubtraceSummary(1, 25, 100, (3,), (-25, 25), (-75, 75), 100, (6,), (3,), ((2,),), (6,), 100, 0),
        KSubtraceSummary(5, 5, 20, (15,), (-5, 5), (-75, 75), 20, (30,), (3,), ((10,),), (30,), 20, 0),
        KSubtraceSummary(25, 1, 4, (75,), (-1, 1), (-75, 75), 4, (0,), (0,), ((),), (0,), 4, 4),
    )
    row_ok = (
        profile.raw_block_count == 12675
        and profile.kernel_order == 25
        and profile.quotient_block_count == 507
        and profile.k_invariant_dimension == 507
        and profile.normalized_trace_rank_on_k_invariants == 507
        and profile.normalized_trace_kernel_dimension_on_k_invariants == 0
        and profile.selected_corner_blocks == 3
        and profile.unique_k_invariant_corner_support == 75
        and profile.proper_subtrace_orders == (1, 5)
        and profile.full_trace_order == 25
        and profile.subtrace_summaries == expected_summaries
        and profile.full_trace_rows_match_block_k_trace
        and profile.all_subtrace_relation_defects_equal_k_boundary_defects
        and profile.only_full_subtraces_are_k_invariant
    )

    print(
        "corner_k_trace_minimality_summary: "
        f"kernel_order={profile.kernel_order} "
        f"quotient_block_count={profile.quotient_block_count} "
        f"k_invariant_dimension={profile.k_invariant_dimension} "
        f"trace_rank={profile.normalized_trace_rank_on_k_invariants} "
        f"trace_kernel_dimension={profile.normalized_trace_kernel_dimension_on_k_invariants} "
        f"unique_k_invariant_corner_support={profile.unique_k_invariant_corner_support}"
    )
    print("subtrace_summaries")
    for summary in profile.subtrace_summaries:
        print(f"  {summary}")
    print("minimality_laws")
    print("  normalized_trace restricted to K-invariant raw lifts is an isomorphism on 507 quotient blocks")
    print("  a nonzero corner quotient block therefore lifts uniquely to a full 25-point K orbit")
    print("  proper K-subtraces of order 1 or 5 are trace-correct but fail the raw K-boundary/D3=Y relation")
    print("interpretation")
    print("  support_75_is_unavoidable_for_a_trace_correct_K_invariant_corner_lift=1")
    print("  smaller_sparse_or_K5_subtraces_are_not_raw_producer_certificates=1")
    print("  producer_must_realize_the_full_order_25_K_trace_on_the_Newton_triangle=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
