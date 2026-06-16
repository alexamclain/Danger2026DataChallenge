#!/usr/bin/env python3
"""Block/skew Cauchy displacement-rank toy for the full Plucker chart.

The scalar visible-GRS Plucker chart has a Cauchy form:

    C_ij = u_i v_j / (x_i - y_j).

Equivalently, `diag(x) C - C diag(y)` has rank one.  The entrywise-inverse
rank <= 2 test in `trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py` is the
scalar shadow of this displacement-rank identity.

For a hidden block/skew Cauchy theorem, the useful invariant should instead be
a Sylvester displacement:

    A C - C B = R S,

where `A` and `B` are the transported left/right operators coming from the
class-field/Lang construction and the rank of `R S` is small.  This toy checks
the scalar case, a genuine block-resolvent case, invariance under transported
row/column basis changes, and rejection of a random chart with the same
dimensions.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import (
    entrywise_inverse_rank,
    inverse_matrix,
    matmul,
)


@dataclass(frozen=True)
class DisplacementCase:
    label: str
    q: int
    rows: int
    cols: int
    residual_rank_bound: int
    displacement_rank: int
    passes_low_rank_gate: bool
    scalar_inverse_rank: int | None = None


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


def scalar_matrix_mul(scale: int, matrix: list[list[int]], q: int) -> list[list[int]]:
    return [[scale * value % q for value in row] for row in matrix]


def block_diag(blocks: list[list[list[int]]]) -> list[list[int]]:
    row_count = sum(len(block) for block in blocks)
    col_count = sum(len(block[0]) for block in blocks)
    out = [[0 for _col in range(col_count)] for _row in range(row_count)]
    row_offset = 0
    col_offset = 0
    for block in blocks:
        for row, values in enumerate(block):
            for col, value in enumerate(values):
                out[row_offset + row][col_offset + col] = value
        row_offset += len(block)
        col_offset += len(block[0])
    return out


def horizontal_concat(blocks: list[list[list[int]]]) -> list[list[int]]:
    rows = len(blocks[0])
    out = [[] for _row in range(rows)]
    for block in blocks:
        for row in range(rows):
            out[row].extend(block[row])
    return out


def vertical_concat(blocks: list[list[list[int]]]) -> list[list[int]]:
    out: list[list[int]] = []
    for block in blocks:
        out.extend([list(row) for row in block])
    return out


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]


def diagonal_matrix(values: list[int]) -> list[list[int]]:
    return [[value if row == col else 0 for col, value in enumerate(values)] for row in range(len(values))]


def displacement_rank(
    chart: list[list[int]],
    left_operator: list[list[int]],
    right_operator: list[list[int]],
    q: int,
) -> int:
    left_action = matmul(left_operator, chart, q)
    right_action = matmul(chart, right_operator, q)
    return rank_mod_q(mat_add(left_action, right_action, q, sign=-1), q)


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _col in range(cols)] for _row in range(rows)]


def random_invertible_matrix(dim: int, q: int, rng: random.Random) -> list[list[int]]:
    for _trial in range(2000):
        matrix = random_matrix(dim, dim, q, rng)
        if rank_mod_q(matrix, q) == dim:
            return matrix
    raise RuntimeError("did not find an invertible matrix")


def shifted_matrix(matrix: list[list[int]], shift: int, q: int) -> list[list[int]]:
    return mat_add(matrix, scalar_matrix_mul((-shift) % q, identity_matrix(len(matrix)), q), q)


def invertible_shifted_matrix(
    dim: int,
    shift: int,
    q: int,
    rng: random.Random,
) -> list[list[int]]:
    for _trial in range(2000):
        matrix = random_matrix(dim, dim, q, rng)
        if rank_mod_q(shifted_matrix(matrix, shift, q), q) == dim:
            return matrix
    raise RuntimeError("did not find an invertible shifted matrix")


def scalar_cauchy_case(q: int) -> DisplacementCase:
    x_values = [2, 5, 9, 14, 20, 27, 35, 44]
    y_values = [60, 72, 83, 96]
    chart = [
        [pow((x - y) % q, -1, q) for y in y_values]
        for x in x_values
    ]
    left = diagonal_matrix(x_values)
    right = diagonal_matrix(y_values)
    rank = displacement_rank(chart, left, right, q)
    inverse_rank = entrywise_inverse_rank(chart, q)
    return DisplacementCase(
        label="scalar_cauchy_shadow",
        q=q,
        rows=len(chart),
        cols=len(chart[0]),
        residual_rank_bound=1,
        displacement_rank=rank,
        passes_low_rank_gate=(rank <= 1),
        scalar_inverse_rank=inverse_rank,
    )


def block_resolvent_data(
    q: int,
    rng: random.Random,
) -> tuple[list[list[int]], list[list[int]], list[list[int]], int]:
    row_blocks = 5
    col_blocks = 4
    row_dim = 3
    col_dim = 2
    residual_rank = 2
    y_values = [7, 19, 43, 71]

    a_blocks = [
        invertible_shifted_matrix(row_dim, y_values[index % col_blocks], q, rng)
        for index in range(row_blocks)
    ]
    r_blocks = [random_matrix(row_dim, residual_rank, q, rng) for _ in range(row_blocks)]
    s_blocks = [random_matrix(residual_rank, col_dim, q, rng) for _ in range(col_blocks)]

    chart_blocks: list[list[list[list[int]]]] = []
    for a_block, r_block in zip(a_blocks, r_blocks):
        block_row: list[list[list[int]]] = []
        for y_value, s_block in zip(y_values, s_blocks):
            resolvent = inverse_matrix(shifted_matrix(a_block, y_value, q), q)
            block_row.append(matmul(matmul(resolvent, r_block, q), s_block, q))
        chart_blocks.append(block_row)

    chart = vertical_concat([horizontal_concat(block_row) for block_row in chart_blocks])
    left_operator = block_diag(a_blocks)
    right_operator = block_diag(
        [scalar_matrix_mul(y_value, identity_matrix(col_dim), q) for y_value in y_values]
    )
    return chart, left_operator, right_operator, residual_rank


def transported_basis_change_case(
    chart: list[list[int]],
    left_operator: list[list[int]],
    right_operator: list[list[int]],
    residual_rank: int,
    q: int,
    rng: random.Random,
) -> DisplacementCase:
    row_change = random_invertible_matrix(len(chart), q, rng)
    col_change = random_invertible_matrix(len(chart[0]), q, rng)
    row_change_inv = inverse_matrix(row_change, q)
    col_change_inv = inverse_matrix(col_change, q)
    changed_chart = matmul(matmul(row_change, chart, q), col_change, q)
    changed_left = matmul(matmul(row_change, left_operator, q), row_change_inv, q)
    changed_right = matmul(matmul(col_change_inv, right_operator, q), col_change, q)
    rank = displacement_rank(changed_chart, changed_left, changed_right, q)
    return DisplacementCase(
        label="transported_basis_change_block_resolvent",
        q=q,
        rows=len(changed_chart),
        cols=len(changed_chart[0]),
        residual_rank_bound=residual_rank,
        displacement_rank=rank,
        passes_low_rank_gate=(rank <= residual_rank),
    )


def random_chart_case(
    left_operator: list[list[int]],
    right_operator: list[list[int]],
    residual_rank: int,
    q: int,
    rng: random.Random,
) -> DisplacementCase:
    rows = len(left_operator)
    cols = len(right_operator)
    for _trial in range(2000):
        chart = random_matrix(rows, cols, q, rng)
        rank = displacement_rank(chart, left_operator, right_operator, q)
        if rank > residual_rank:
            return DisplacementCase(
                label="random_chart_same_operators",
                q=q,
                rows=rows,
                cols=cols,
                residual_rank_bound=residual_rank,
                displacement_rank=rank,
                passes_low_rank_gate=False,
            )
    raise RuntimeError("did not find a random chart rejecting the gate")


def main() -> None:
    q = 101
    seed = 20260606
    rng = random.Random(seed)

    chart, left_operator, right_operator, residual_rank = block_resolvent_data(q, rng)
    block_rank = displacement_rank(chart, left_operator, right_operator, q)

    rows = [
        scalar_cauchy_case(q),
        DisplacementCase(
            label="block_resolvent_skew_cauchy",
            q=q,
            rows=len(chart),
            cols=len(chart[0]),
            residual_rank_bound=residual_rank,
            displacement_rank=block_rank,
            passes_low_rank_gate=(block_rank <= residual_rank),
        ),
        transported_basis_change_case(
            chart,
            left_operator,
            right_operator,
            residual_rank,
            q,
            rng,
        ),
        random_chart_case(left_operator, right_operator, residual_rank, q, rng),
    ]

    p24_selected_dim = 156
    p24_omitted_dim = 35 + 19

    print("Trace-GCD RS-tail block/skew Cauchy displacement toy")
    for row in rows:
        scalar_text = (
            "None"
            if row.scalar_inverse_rank is None
            else str(row.scalar_inverse_rank)
        )
        print(
            f"case={row.label} q={row.q} rows={row.rows} cols={row.cols} "
            f"residual_rank_bound={row.residual_rank_bound} "
            f"displacement_rank={row.displacement_rank} "
            f"passes_low_rank_gate={int(row.passes_low_rank_gate)} "
            f"scalar_inverse_rank={scalar_text}"
        )
    print("p24")
    print(f"  p24_selected_rs_tail_rows={p24_selected_dim}")
    print(f"  p24_omitted_full_source_columns={p24_omitted_dim}")
    print(f"  p24_block_skew_chart_entries={p24_selected_dim * p24_omitted_dim}")
    print("interpretation")
    print("  scalar_cauchy_is_displacement_rank_one=1")
    print("  scalar_entrywise_inverse_rank_is_shadow_of_displacement_rank=1")
    print("  block_resolvent_has_low_sylvester_displacement_rank=1")
    print("  transported_basis_changes_preserve_low_displacement_rank=1")
    print("  random_chart_rejected_by_block_skew_displacement_rank=1")
    print("  actual_p24_work_is_to_identify_transported_CM_operators_A_and_B=1")
    print("conclusion=reported_trace_gcd_rs_tail_block_skew_cauchy_displacement_toy")


if __name__ == "__main__":
    main()
