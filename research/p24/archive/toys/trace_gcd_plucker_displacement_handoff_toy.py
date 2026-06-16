#!/usr/bin/env python3
"""Plucker-chart displacement handoff toy.

This is the finite algebra behind the sharpened block/skew Cauchy route.

Let a full column family be split as `X = [S O]`, with selected square block
`S` invertible and omitted chart `C = S^{-1} O`.  If an arithmetic operator
`T` acts on the ambient column span with known selected/omitted coordinate
operators `A` and `B`, then

    T S = S A + E_s,
    T O = O B + E_o

implies

    A C - C B = S^{-1} (E_o - E_s C).

Thus a low-rank operator boundary for the full `210` columns gives a low-rank
Sylvester displacement for the `156 x 54` Plucker chart.  This is the bridge we
need from the CM/Lang construction: `A` and `B` must be derived before seeing
the chart.  The toy also shows why choosing `A` after seeing a random chart is
not evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_rs_tail_block_skew_cauchy_displacement_toy import (
    block_resolvent_data,
    random_invertible_matrix,
    random_matrix,
)
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import inverse_matrix, matmul


@dataclass(frozen=True)
class HandoffCase:
    label: str
    q: int
    rows: int
    cols: int
    expected_bound: int
    displacement_rank: int
    boundary_rank: int
    handoff_identity: bool
    passes_bound: bool
    postfit_operator: bool


def mat_add(
    left: list[list[int]],
    right: list[list[int]],
    q: int,
    sign: int = 1,
) -> list[list[int]]:
    return [
        [(a + sign * b) % q for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def identity_matrix(dim: int) -> list[list[int]]:
    return [[1 if row == col else 0 for col in range(dim)] for row in range(dim)]


def scalar_mul(scale: int, matrix: list[list[int]], q: int) -> list[list[int]]:
    return [[scale * value % q for value in row] for row in matrix]


def diagonal_matrix(values: list[int]) -> list[list[int]]:
    return [[value if row == col else 0 for col, value in enumerate(values)] for row in range(len(values))]


def columns(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]


def matrix_from_columns(cols: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*cols)]


def displacement(
    chart: list[list[int]],
    left_operator: list[list[int]],
    right_operator: list[list[int]],
    q: int,
) -> list[list[int]]:
    return mat_add(
        matmul(left_operator, chart, q),
        matmul(chart, right_operator, q),
        q,
        sign=-1,
    )


def extend_columns_to_basis(seed_columns: list[list[int]], q: int) -> list[list[int]]:
    dim = len(seed_columns[0])
    basis = [list(col) for col in seed_columns]
    current_rows = matrix_from_columns(basis) if basis else []
    for index in range(dim):
        candidate = [1 if row == index else 0 for row in range(dim)]
        candidate_basis = basis + [candidate]
        candidate_rows = matrix_from_columns(candidate_basis)
        if rank_mod_q(candidate_rows, q) > rank_mod_q(current_rows, q):
            basis.append(candidate)
            current_rows = candidate_rows
        if len(basis) == dim:
            return basis
    raise RuntimeError("could not extend columns to a basis")


def companion_truncation_operator(dim: int) -> list[list[int]]:
    """Multiplication by x on polynomials of degree < dim, dropping x^dim."""
    out = [[0 for _col in range(dim)] for _row in range(dim)]
    for row in range(dim - 1):
        out[row][row + 1] = 1
    return out


def vandermonde_columns(values: list[int], dim: int, q: int) -> list[list[int]]:
    out: list[list[int]] = []
    for value in values:
        power = 1
        col: list[int] = []
        for _row in range(dim):
            col.append(power)
            power = power * value % q
        out.append(col)
    return out


def handoff_case(
    label: str,
    chart: list[list[int]],
    left_operator: list[list[int]],
    right_operator: list[list[int]],
    expected_bound: int,
    q: int,
    rng: random.Random,
    postfit_operator: bool = False,
) -> HandoffCase:
    rows = len(chart)
    selected_basis = random_invertible_matrix(rows, q, rng)
    omitted = matmul(selected_basis, chart, q)
    selected_inv = inverse_matrix(selected_basis, q)
    ambient_operator = matmul(
        matmul(selected_basis, left_operator, q),
        selected_inv,
        q,
    )
    selected_boundary = mat_add(
        matmul(ambient_operator, selected_basis, q),
        matmul(selected_basis, left_operator, q),
        q,
        sign=-1,
    )
    omitted_boundary = mat_add(
        matmul(ambient_operator, omitted, q),
        matmul(omitted, right_operator, q),
        q,
        sign=-1,
    )
    disp = displacement(chart, left_operator, right_operator, q)
    handoff_rhs = matmul(
        selected_inv,
        mat_add(
            omitted_boundary,
            matmul(selected_boundary, chart, q),
            q,
            sign=-1,
        ),
        q,
    )
    return HandoffCase(
        label=label,
        q=q,
        rows=rows,
        cols=len(chart[0]),
        expected_bound=expected_bound,
        displacement_rank=rank_mod_q(disp, q),
        boundary_rank=rank_mod_q(
            mat_add(
                omitted_boundary,
                matmul(selected_boundary, chart, q),
                q,
                sign=-1,
            ),
            q,
        ),
        handoff_identity=(disp == handoff_rhs),
        passes_bound=(rank_mod_q(disp, q) <= expected_bound),
        postfit_operator=postfit_operator,
    )


def scalar_cauchy_handoff(q: int, rng: random.Random) -> HandoffCase:
    dim = 8
    omitted_dim = 4
    x_values = [2, 5, 9, 14, 20, 27, 35, 44]
    y_values = [60, 72, 83, 96]
    selected = matrix_from_columns(vandermonde_columns(x_values, dim, q))
    omitted = matrix_from_columns(vandermonde_columns(y_values, dim, q))
    chart = matmul(inverse_matrix(selected, q), omitted, q)
    left_operator = matmul(
        matmul(inverse_matrix(selected, q), companion_truncation_operator(dim), q),
        selected,
        q,
    )
    right_operator = diagonal_matrix(y_values)
    return handoff_case(
        "scalar_vandermonde_operator_boundary",
        chart,
        left_operator,
        right_operator,
        1,
        q,
        rng,
    )


def random_fixed_operator_rejection(q: int, rng: random.Random) -> HandoffCase:
    rows = 8
    cols = 4
    chart = random_matrix(rows, cols, q, rng)
    while rank_mod_q(chart, q) < cols:
        chart = random_matrix(rows, cols, q, rng)
    left_operator = companion_truncation_operator(rows)
    right_operator = diagonal_matrix([60, 72, 83, 96])
    return handoff_case(
        "random_chart_fixed_arithmetic_operators",
        chart,
        left_operator,
        right_operator,
        1,
        q,
        rng,
    )


def random_postfit_pitfall(q: int, rng: random.Random) -> HandoffCase:
    rows = 8
    cols = 4
    chart = random_matrix(rows, cols, q, rng)
    while rank_mod_q(chart, q) < cols:
        chart = random_matrix(rows, cols, q, rng)
    right_operator = diagonal_matrix([60, 72, 83, 96])
    chart_basis_columns = extend_columns_to_basis(columns(chart), q)
    basis_matrix = matrix_from_columns(chart_basis_columns)
    basis_inv = inverse_matrix(basis_matrix, q)
    target_on_chart = matmul(chart, right_operator, q)
    action_columns = columns(target_on_chart) + [[0] * rows for _ in range(rows - cols)]
    action_matrix = matrix_from_columns(action_columns)
    left_operator = matmul(action_matrix, basis_inv, q)
    return handoff_case(
        "random_chart_postfit_operator_pitfall",
        chart,
        left_operator,
        right_operator,
        1,
        q,
        rng,
        postfit_operator=True,
    )


def block_resolvent_handoff(q: int, rng: random.Random) -> HandoffCase:
    chart, left_operator, right_operator, residual_rank = block_resolvent_data(q, rng)
    return handoff_case(
        "block_resolvent_operator_boundary",
        chart,
        left_operator,
        right_operator,
        residual_rank,
        q,
        rng,
    )


def main() -> None:
    q = 101
    rng = random.Random(20260606)
    rows = [
        scalar_cauchy_handoff(q, rng),
        block_resolvent_handoff(q, rng),
        random_fixed_operator_rejection(q, rng),
        random_postfit_pitfall(q, rng),
    ]

    print("Trace-GCD Plucker displacement handoff toy")
    for row in rows:
        print(
            f"case={row.label} q={row.q} rows={row.rows} cols={row.cols} "
            f"expected_bound={row.expected_bound} "
            f"displacement_rank={row.displacement_rank} "
            f"boundary_rank={row.boundary_rank} "
            f"handoff_identity={int(row.handoff_identity)} "
            f"passes_bound={int(row.passes_bound)} "
            f"postfit_operator={int(row.postfit_operator)}"
        )
    print("p24")
    print("  selected_basis_columns=156")
    print("  omitted_erasure_columns=54")
    print("  full_columns=210")
    print("interpretation")
    print("  low_rank_operator_boundary_implies_low_rank_plucker_displacement=1")
    print("  scalar_vandermonde_boundary_is_rank_one=1")
    print("  block_resolvent_boundary_survives_selected_basis_change=1")
    print("  random_chart_rejected_by_fixed_arithmetic_operators=1")
    print("  postfit_operators_are_not_certificate_evidence=1")
    print("conclusion=reported_trace_gcd_plucker_displacement_handoff_toy")

    required = {
        "scalar_vandermonde_operator_boundary": True,
        "block_resolvent_operator_boundary": True,
        "random_chart_fixed_arithmetic_operators": False,
        "random_chart_postfit_operator_pitfall": True,
    }
    for row in rows:
        if not row.handoff_identity:
            raise SystemExit(1)
        if row.passes_bound != required[row.label]:
            raise SystemExit(1)
        if row.label == "random_chart_postfit_operator_pitfall" and not row.postfit_operator:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
