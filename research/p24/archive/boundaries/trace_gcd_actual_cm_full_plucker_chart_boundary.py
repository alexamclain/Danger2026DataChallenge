#!/usr/bin/env python3
"""Actual-CM boundary audit for the full Plucker-chart invariant.

The p24 full-chart invariant is only meaningful after the selected RS-tail
columns form a basis for the ambient span of all natural right-block columns.
This audit reuses the bounded actual-CM RS-tail rows and measures whether the
selected prefix-plus-tail columns are a basis for the full selected+omitted
column set.  When they are, it computes the Plucker chart and the visible
scalar-GRS Cauchy test from
`trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py`.

Current small rows are expected to be calibration-poor: the full-rank rows are
tail-only, while the nontrivial prefix-plus-tail rows are singular controls.
That is useful information because it prevents overclaiming the full-chart
test from the present actual-CM dataset.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import lang_inverse_for_orbit, matrix_vector_mul
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_actual_cm_gaussian_rs_tail_audit import transformed_kept_blocks
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED
from trace_gcd_residual_prefix_tail_bridge_audit import split_prefix_len
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import (
    entrywise_inverse_rank,
    inverse_matrix,
    matmul,
)


@dataclass(frozen=True)
class ActualChartRow:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    left_orbit: tuple[int, ...]
    omitted: int
    source_dim: int
    right_block_count: int
    right_len: int
    prefix_blocks: int
    tail_dim: int
    selected_count: int
    omitted_count: int
    selected_rank: int
    full_rank: int
    selected_spans_full: bool
    chart_inverse_rank: int | None
    visible_scalar_grs_chart: bool | None
    informative_chart_row: bool


def rank_values(values: list[tuple[int, ...]], q: int) -> int:
    if not values:
        return 0
    return rank_mod_q([list(value) for value in values], q)


def all_transformed_blocks(
    dft_matrix,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    left: int,
    right: int,
    q: int,
    field,
) -> list[list[tuple[int, ...]]]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    blocks: list[list[tuple[int, ...]]] = []
    inverses: dict[int, list[list]] = {}
    for orbit in right_orbits:
        orbit_len = len(orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(q, orbit_len, field, SEED)
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in orbit
        ]
        blocks.append(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return blocks


def selected_and_omitted_columns(
    all_blocks: list[list[tuple[int, ...]]],
    omitted: int,
    source_dim: int,
    right_orbits: list[list[int]],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], int, int, int]:
    kept_indices = [index for index in range(len(all_blocks)) if index != omitted]
    kept_blocks = [all_blocks[index] for index in kept_indices]
    lengths = [len(block) for block in kept_blocks]
    if not lengths or len(set(lengths)) != 1:
        return [], [], 0, 0, 0
    right_len = lengths[0]
    prefix_len = split_prefix_len(right_orbits, omitted, source_dim)
    if prefix_len % right_len:
        return [], [], 0, 0, 0
    prefix_blocks = prefix_len // right_len
    tail_dim = source_dim - prefix_len
    if tail_dim <= 0 or prefix_blocks >= len(kept_blocks):
        return [], [], 0, 0, 0

    selected: list[tuple[int, ...]] = []
    omitted_columns: list[tuple[int, ...]] = []
    for block in kept_blocks[:prefix_blocks]:
        selected.extend(block)
    tail_block = kept_blocks[prefix_blocks]
    selected.extend(tail_block[:tail_dim])
    omitted_columns.extend(tail_block[tail_dim:])
    for block in kept_blocks[prefix_blocks + 1 :]:
        omitted_columns.extend(block)
    omitted_columns.extend(all_blocks[omitted])
    return selected, omitted_columns, right_len, prefix_blocks, tail_dim


def pivot_coordinate_rows(columns: list[tuple[int, ...]], q: int) -> list[int]:
    selected_rows: list[list[int]] = []
    selected_indices: list[int] = []
    for row_index in range(len(columns[0])):
        candidate = [column[row_index] % q for column in columns]
        if rank_mod_q(selected_rows + [candidate], q) > len(selected_rows):
            selected_rows.append(candidate)
            selected_indices.append(row_index)
            if len(selected_indices) == len(columns):
                return selected_indices
    raise ValueError("selected columns do not have full column rank")


def plucker_chart(
    selected: list[tuple[int, ...]],
    omitted: list[tuple[int, ...]],
    q: int,
) -> list[list[int]]:
    pivot_rows = pivot_coordinate_rows(selected, q)
    selected_square = [
        [selected[col][row] % q for col in range(len(selected))]
        for row in pivot_rows
    ]
    omitted_square = [
        [column[row] % q for column in omitted]
        for row in pivot_rows
    ]
    return matmul(inverse_matrix(selected_square, q), omitted_square, q)


def rows_for_case(case: RowspaceCase) -> list[ActualChartRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[ActualChartRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        all_blocks = all_transformed_blocks(
            dft_matrix,
            left_orbit,
            right_orbits,
            case.left,
            case.right,
            case.q,
            field,
        )
        for omitted in range(len(right_orbits)):
            selected, omitted_columns, right_len, prefix_blocks, tail_dim = (
                selected_and_omitted_columns(
                    all_blocks,
                    omitted,
                    source_dim,
                    right_orbits,
                )
            )
            if not selected:
                continue
            selected_rank = rank_values(selected, case.q)
            full_rank = rank_values(selected + omitted_columns, case.q)
            selected_spans_full = selected_rank == full_rank == len(selected)
            inverse_rank = None
            visible_scalar = None
            informative = (
                selected_spans_full
                and len(selected) >= 3
                and len(omitted_columns) >= 3
            )
            if selected_spans_full and omitted_columns:
                chart = plucker_chart(selected, omitted_columns, case.q)
                inverse_rank = entrywise_inverse_rank(chart, case.q)
                visible_scalar = inverse_rank is not None and inverse_rank <= 2
            rows.append(
                ActualChartRow(
                    label=case.label,
                    D=case.D,
                    q=case.q,
                    h=h,
                    m=case.m,
                    n=n,
                    factor_degree=factor.degree(),
                    left=case.left,
                    right=case.right,
                    left_orbit=tuple(left_orbit),
                    omitted=omitted,
                    source_dim=source_dim,
                    right_block_count=len(right_orbits),
                    right_len=right_len,
                    prefix_blocks=prefix_blocks,
                    tail_dim=tail_dim,
                    selected_count=len(selected),
                    omitted_count=len(omitted_columns),
                    selected_rank=selected_rank,
                    full_rank=full_rank,
                    selected_spans_full=selected_spans_full,
                    chart_inverse_rank=inverse_rank,
                    visible_scalar_grs_chart=visible_scalar,
                    informative_chart_row=informative,
                )
            )
    return rows


def main() -> None:
    cases = [
        RowspaceCase("pinned_tail_only_full_rank", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout_tail_only_full_rank", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_tail_only_full_rank", -4319, 4463, 28, 4, 7),
        RowspaceCase("actual_prefix_plus_tail_singular", -15791, 40127, 65, 5, 13),
    ]
    rows = [row for case in cases for row in rows_for_case(case)]
    print("Trace-GCD actual-CM full Plucker-chart boundary")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "source_dim right_blocks right_len prefix_blocks tail_dim "
        "selected_count omitted_count selected_rank full_rank "
        "selected_spans_full chart_inverse_rank visible_scalar_grs_chart "
        "informative_chart_row"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} source_dim={row.source_dim} "
            f"right_blocks={row.right_block_count} right_len={row.right_len} "
            f"prefix_blocks={row.prefix_blocks} tail_dim={row.tail_dim} "
            f"selected_count={row.selected_count} omitted_count={row.omitted_count} "
            f"selected_rank={row.selected_rank} full_rank={row.full_rank} "
            f"selected_spans_full={int(row.selected_spans_full)} "
            f"chart_inverse_rank={row.chart_inverse_rank} "
            f"visible_scalar_grs_chart={row.visible_scalar_grs_chart} "
            f"informative_chart_row={int(row.informative_chart_row)}"
        )
    basis_rows = [row for row in rows if row.selected_spans_full]
    informative_rows = [row for row in rows if row.informative_chart_row]
    singular_controls = [
        row for row in rows
        if row.selected_rank < row.selected_count and row.prefix_blocks > 0
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  selected_basis_for_full_span_rows={len(basis_rows)}/{len(rows)}")
    print(f"  informative_chart_rows={len(informative_rows)}/{len(rows)}")
    print(f"  singular_prefix_tail_controls={len(singular_controls)}")
    print("interpretation")
    print("  actual_cm_full_plucker_chart_columns_measured=1")
    print("  actual_cm_full_chart_has_no_nontrivial_basis_calibration_row=1")
    print("  p24_full_chart_requires_selected_basis_of_ambient=1")
    print("  current_small_actual_rows_do_not_test_visible_scalar_grs_chart=1")
    print("conclusion=reported_trace_gcd_actual_cm_full_plucker_chart_boundary")

    if not rows or informative_rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
