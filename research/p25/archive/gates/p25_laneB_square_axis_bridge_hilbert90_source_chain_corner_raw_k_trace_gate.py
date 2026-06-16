#!/usr/bin/env python3
"""Raw K-trace selector for p25 Hilbert-90 source-chain corners.

The corner C_169-lift selector leaves the producer debt at the raw block lift:
the source-chain corner must be realized with the 25-point right-kernel trace
factor, not merely as a quotient or sparse raw section.

This gate checks that statement directly on the four active half-bridge
corner chains.  For each chain, the kernel-trivial K-trace lift is the only
tested trace-correct lift satisfying the raw D^3 = Y relation.  Sparse
sections are trace-correct but expose all C_25 kernel modes and break the raw
relation; trace-zero hidden modes do not repair this.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    ActiveCornerRow,
    corner_profile,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import MODULUS
from p25_laneB_square_axis_bridge_raw_source_gate import (
    kernel_mode_support,
    normalized_trace,
    square_axis_case,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


LiftKind = str


@dataclass(frozen=True)
class CornerRawLiftRow:
    orientation_mask: int
    boundary_step_d: int
    boundary_direction_q: int
    chain_q_values: tuple[int, ...]
    coefficient: int
    lift_kind: LiftKind
    raw_support: int
    raw_degree: int
    trace_correct: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    kernel_mode_counts: tuple[int, ...]
    raw_relation_mismatches: int
    mismatch_q_count: int
    mismatch_per_q_values: tuple[int, ...]


@dataclass(frozen=True)
class CornerRawKTraceProfile:
    row_count: int
    active_corner_count: int
    trace_correct_rows: int
    trace_correct_raw_relation_rows: int
    trace_correct_kernel_trivial_rows: int
    block_k_trace_rows: tuple[CornerRawLiftRow, ...]
    sparse_section_rows: tuple[CornerRawLiftRow, ...]
    block_plus_hidden_rows: tuple[CornerRawLiftRow, ...]
    hidden_only_rows: tuple[CornerRawLiftRow, ...]
    all_block_k_trace_rows_pass: bool
    all_sparse_sections_are_trace_correct_but_relation_bad: bool
    all_block_plus_hidden_rows_are_trace_correct_but_relation_bad: bool
    all_hidden_only_rows_are_degree_zero_but_trace_bad: bool
    rows: tuple[CornerRawLiftRow, ...]


def signed_mod(value: int) -> int:
    value %= MODULUS
    return value if value <= MODULUS // 2 else value - MODULUS


def active_coefficient(row: ActiveCornerRow) -> int:
    coefficients = {coefficient for _point, coefficient in row.chain_word}
    if len(coefficients) != 1:
        raise AssertionError(f"active row does not have constant coefficients: {row}")
    return next(iter(coefficients))


def raw_lift(row: ActiveCornerRow, lift_kind: LiftKind, zeta_b: int) -> list[int]:
    case = square_axis_case()
    coefficient = active_coefficient(row)
    raw = [0] * case.raw_order
    for q_value in row.chain_q_values:
        for layer in range(case.b_trace):
            index = q_value + QUOTIENT_ORDER * layer
            if lift_kind == "block_k_trace":
                value = coefficient
            elif lift_kind == "sparse_section":
                value = coefficient * case.b_trace if layer == 0 else 0
            elif lift_kind == "block_plus_hidden_mode":
                value = coefficient * (1 + pow(zeta_b, layer, MODULUS))
            elif lift_kind == "hidden_mode_only":
                value = coefficient * pow(zeta_b, layer, MODULUS)
            else:
                raise AssertionError(f"unknown lift kind: {lift_kind}")
            raw[index] = value % MODULUS
    return raw


def trace_correct(row: ActiveCornerRow, raw: list[int]) -> bool:
    case = square_axis_case()
    coefficient = active_coefficient(row) % MODULUS
    expected = [0 for _ in range(QUOTIENT_ORDER)]
    for q_value in row.chain_q_values:
        expected[q_value] = coefficient
    trace = normalized_trace(raw, case, MODULUS)
    return all((value - target) % MODULUS == 0 for value, target in zip(trace, expected))


def block_constancy_hits(raw: list[int]) -> int:
    case = square_axis_case()
    hits = 0
    for q_value in range(QUOTIENT_ORDER):
        values = {
            raw[q_value + QUOTIENT_ORDER * layer] % MODULUS
            for layer in range(case.b_trace)
        }
        hits += int(len(values) == 1)
    return hits


def relation_mismatch_profile(raw: list[int]) -> tuple[int, int, tuple[int, ...]]:
    mismatch_by_q: dict[int, int] = {}
    for e_value in range(len(raw)):
        if raw[(e_value + 3 * S_STEP) % len(raw)] % MODULUS != raw[(e_value + Y_STEP) % len(raw)] % MODULUS:
            q_value = e_value % QUOTIENT_ORDER
            mismatch_by_q[q_value] = mismatch_by_q.get(q_value, 0) + 1
    return (
        sum(mismatch_by_q.values()),
        len(mismatch_by_q),
        tuple(sorted(set(mismatch_by_q.values()))),
    )


def lift_row(row: ActiveCornerRow, lift_kind: LiftKind, zeta_b: int) -> CornerRawLiftRow:
    case = square_axis_case()
    raw = raw_lift(row, lift_kind, zeta_b)
    modes, mode_counts = kernel_mode_support(raw, case, MODULUS, zeta_b)
    mismatches, mismatch_q_count, mismatch_per_q_values = relation_mismatch_profile(raw)
    return CornerRawLiftRow(
        orientation_mask=row.orientation_mask,
        boundary_step_d=row.boundary_step_d,
        boundary_direction_q=row.boundary_direction_q,
        chain_q_values=row.chain_q_values,
        coefficient=active_coefficient(row),
        lift_kind=lift_kind,
        raw_support=sum(1 for value in raw if value % MODULUS),
        raw_degree=sum(signed_mod(value) for value in raw),
        trace_correct=trace_correct(row, raw),
        block_constancy_hits=block_constancy_hits(raw),
        kernel_modes=modes,
        kernel_mode_counts=mode_counts,
        raw_relation_mismatches=mismatches,
        mismatch_q_count=mismatch_q_count,
        mismatch_per_q_values=mismatch_per_q_values,
    )


def profile() -> CornerRawKTraceProfile:
    case = square_axis_case()
    root = primitive_root(MODULUS)
    zeta_b = pow(root, (MODULUS - 1) // case.b_trace, MODULUS)
    kinds = (
        "block_k_trace",
        "sparse_section",
        "block_plus_hidden_mode",
        "hidden_mode_only",
    )
    rows = tuple(
        lift_row(active, kind, zeta_b)
        for active in corner_profile().active_rows
        for kind in kinds
    )
    block_rows = tuple(row for row in rows if row.lift_kind == "block_k_trace")
    sparse_rows = tuple(row for row in rows if row.lift_kind == "sparse_section")
    block_hidden_rows = tuple(row for row in rows if row.lift_kind == "block_plus_hidden_mode")
    hidden_rows = tuple(row for row in rows if row.lift_kind == "hidden_mode_only")
    return CornerRawKTraceProfile(
        row_count=len(rows),
        active_corner_count=len(corner_profile().active_rows),
        trace_correct_rows=sum(row.trace_correct for row in rows),
        trace_correct_raw_relation_rows=sum(row.trace_correct and row.raw_relation_mismatches == 0 for row in rows),
        trace_correct_kernel_trivial_rows=sum(row.trace_correct and row.kernel_modes == (0,) for row in rows),
        block_k_trace_rows=block_rows,
        sparse_section_rows=sparse_rows,
        block_plus_hidden_rows=block_hidden_rows,
        hidden_only_rows=hidden_rows,
        all_block_k_trace_rows_pass=all(
            row.raw_support == 75
            and row.raw_degree == 25 * 3 * row.coefficient
            and row.trace_correct
            and row.block_constancy_hits == QUOTIENT_ORDER
            and row.kernel_modes == (0,)
            and row.kernel_mode_counts == (3,) + (0,) * 24
            and row.raw_relation_mismatches == 0
            for row in block_rows
        ),
        all_sparse_sections_are_trace_correct_but_relation_bad=all(
            row.raw_support == 3
            and row.raw_degree == 25 * 3 * row.coefficient
            and row.trace_correct
            and row.block_constancy_hits == QUOTIENT_ORDER - 3
            and row.kernel_modes == tuple(range(25))
            and row.kernel_mode_counts == (3,) * 25
            and row.raw_relation_mismatches == 6
            and row.mismatch_q_count == 3
            and row.mismatch_per_q_values == (2,)
            for row in sparse_rows
        ),
        all_block_plus_hidden_rows_are_trace_correct_but_relation_bad=all(
            row.raw_support == 75
            and row.raw_degree == 25 * 3 * row.coefficient
            and row.trace_correct
            and row.block_constancy_hits == QUOTIENT_ORDER - 3
            and row.kernel_modes == (0, 1)
            and row.kernel_mode_counts == (3, 3) + (0,) * 23
            and row.raw_relation_mismatches == 75
            and row.mismatch_q_count == 3
            and row.mismatch_per_q_values == (25,)
            for row in block_hidden_rows
        ),
        all_hidden_only_rows_are_degree_zero_but_trace_bad=all(
            row.raw_support == 75
            and row.raw_degree == 0
            and not row.trace_correct
            and row.block_constancy_hits == QUOTIENT_ORDER - 3
            and row.kernel_modes == (1,)
            and row.kernel_mode_counts == (0, 3) + (0,) * 23
            and row.raw_relation_mismatches == 75
            and row.mismatch_q_count == 3
            and row.mismatch_per_q_values == (25,)
            for row in hidden_rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner raw K-trace gate")
    result = profile()
    row_ok = (
        result.row_count == 16
        and result.active_corner_count == 4
        and result.trace_correct_rows == 12
        and result.trace_correct_raw_relation_rows == 4
        and result.trace_correct_kernel_trivial_rows == 4
        and result.all_block_k_trace_rows_pass
        and result.all_sparse_sections_are_trace_correct_but_relation_bad
        and result.all_block_plus_hidden_rows_are_trace_correct_but_relation_bad
        and result.all_hidden_only_rows_are_degree_zero_but_trace_bad
    )

    print(
        "corner_raw_k_trace_summary: "
        f"active_corner_count={result.active_corner_count} "
        f"row_count={result.row_count} "
        f"trace_correct_rows={result.trace_correct_rows} "
        f"trace_correct_raw_relation_rows={result.trace_correct_raw_relation_rows} "
        f"trace_correct_kernel_trivial_rows={result.trace_correct_kernel_trivial_rows}"
    )
    print("corner_raw_lift_rows")
    for row in result.rows:
        print(f"  {row}")
    print("selector_law")
    print("  block_K_trace_lifts_are_trace_correct_kernel_trivial_and_raw_D3_equals_Y_compatible")
    print("  sparse_sections_are_trace_correct_but_have_all_C25_kernel_modes_and_break_raw_D3_equals_Y")
    print("  trace_zero_hidden_modes_do_not_repair_the_raw_relation_or_trace_contract")
    print("interpretation")
    print("  half_bridge_corner_requires_the_25_point_K_trace_block_lift=1")
    print("  quotient_corner_or_sparse_raw_section_is_not_a_producer_certificate=1")
    print("  raw_chain_degree_remains_plusminus_75_before_the_first_boundary=1")
    print("  remaining_arithmetic_debt_is_realizing_this_K_trace_with_the_recorded_Kummer_cost=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
