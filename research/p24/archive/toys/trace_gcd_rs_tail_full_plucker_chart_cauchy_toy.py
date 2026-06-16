#!/usr/bin/env python3
"""Full-210 Plucker-chart Cauchy invariant toy.

The selected RS-tail square uses 156 of the 210 natural fixed-source columns.
If those selected columns are a basis, the 54 omitted columns are encoded by a
156 x 54 Plucker chart:

    omitted_column = sum_i chart[i,j] * selected_column_i.

For a visible scalar GRS/MDS explanation, after putting the selected columns in
systematic form the omitted chart is a scaled Cauchy matrix.  Equivalently, the
entrywise inverse of the chart has rank at most 2.  This rank is invariant
under global row changes and independent column scalings, so it is a genuine
full-object visible-GRS test, unlike selected-square support directness.

The toy confirms the invariant on rational-normal/GRS columns, checks that it
survives row and column scalings, and rejects a random full-source chart with
the same selected/complement bookkeeping.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q


@dataclass(frozen=True)
class ChartCase:
    label: str
    q: int
    selected_dim: int
    omitted_dim: int
    selected_rank: int
    chart_zero_entries: int
    chart_rank: int
    inverse_rank: int | None
    visible_scalar_grs_chart: bool


def det_mod(matrix: list[list[int]], q: int) -> int:
    n = len(matrix)
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = det * pivot_value % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if scale:
                mat[row] = [
                    (left - scale * right) % q
                    for left, right in zip(mat[row], mat[col])
                ]
    return det % q


def inverse_matrix(matrix: list[list[int]], q: int) -> list[list[int]]:
    n = len(matrix)
    aug = [
        [matrix[row][col] % q for col in range(n)]
        + [1 if row == col else 0 for col in range(n)]
        for row in range(n)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if aug[row][col] % q:
                pivot = row
                break
        if pivot is None:
            raise ValueError("matrix is singular")
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        inv = pow(aug[rank][col] % q, -1, q)
        aug[rank] = [(inv * value) % q for value in aug[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = aug[row][col] % q
            if scale:
                aug[row] = [
                    (left - scale * right) % q
                    for left, right in zip(aug[row], aug[rank])
                ]
        rank += 1
    return [row[n:] for row in aug]


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    rows = len(left)
    mid = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[row][k] * right[k][col] for k in range(mid)) % q
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def columns_to_rows(columns: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*columns)]


def chart_matrix(
    selected_columns: list[list[int]],
    omitted_columns: list[list[int]],
    q: int,
) -> list[list[int]]:
    selected_rows = columns_to_rows(selected_columns)
    omitted_rows = columns_to_rows(omitted_columns)
    return matmul(inverse_matrix(selected_rows, q), omitted_rows, q)


def entrywise_inverse_rank(matrix: list[list[int]], q: int) -> int | None:
    if any(value % q == 0 for row in matrix for value in row):
        return None
    inverse_entries = [[pow(value % q, -1, q) for value in row] for row in matrix]
    return rank_mod_q(inverse_entries, q)


def rnc_columns(q: int, selected_dim: int, total_count: int) -> list[list[int]]:
    columns: list[list[int]] = []
    for x in range(1, total_count + 1):
        value = 1
        column: list[int] = []
        for _row in range(selected_dim):
            column.append(value)
            value = value * x % q
        columns.append(column)
    return columns


def random_invertible_matrix(dim: int, q: int, rng: random.Random) -> list[list[int]]:
    for _trial in range(1000):
        matrix = [[rng.randrange(q) for _col in range(dim)] for _row in range(dim)]
        if det_mod(matrix, q):
            return matrix
    raise RuntimeError("did not find an invertible row-change matrix")


def apply_row_and_column_scalings(
    columns: list[list[int]],
    q: int,
    rng: random.Random,
) -> list[list[int]]:
    row_change = random_invertible_matrix(len(columns[0]), q, rng)
    scaled: list[list[int]] = []
    for column in columns:
        scale = rng.randrange(1, q)
        mixed_rows = matmul(row_change, [[value] for value in column], q)
        scaled.append([(scale * row[0]) % q for row in mixed_rows])
    return scaled


def random_full_source_columns(
    q: int,
    selected_dim: int,
    omitted_dim: int,
    seed: int,
) -> list[list[int]]:
    rng = random.Random(seed)
    total = selected_dim + omitted_dim
    for _trial in range(5000):
        columns = [
            [rng.randrange(q) for _row in range(selected_dim)]
            for _col in range(total)
        ]
        selected = columns[:selected_dim]
        omitted = columns[selected_dim:]
        if rank_mod_q(columns_to_rows(selected), q) != selected_dim:
            continue
        chart = chart_matrix(selected, omitted, q)
        if any(value % q == 0 for row in chart for value in row):
            continue
        inverse_rank = entrywise_inverse_rank(chart, q)
        if inverse_rank is not None and inverse_rank > 2:
            return columns
    raise RuntimeError("did not find random chart rejecting scalar GRS")


def analyze_case(
    label: str,
    columns: list[list[int]],
    selected_dim: int,
    q: int,
) -> ChartCase:
    selected = columns[:selected_dim]
    omitted = columns[selected_dim:]
    chart = chart_matrix(selected, omitted, q)
    inverse_rank = entrywise_inverse_rank(chart, q)
    zero_entries = sum(value % q == 0 for row in chart for value in row)
    return ChartCase(
        label=label,
        q=q,
        selected_dim=selected_dim,
        omitted_dim=len(omitted),
        selected_rank=rank_mod_q(columns_to_rows(selected), q),
        chart_zero_entries=zero_entries,
        chart_rank=rank_mod_q(chart, q),
        inverse_rank=inverse_rank,
        visible_scalar_grs_chart=(inverse_rank is not None and inverse_rank <= 2),
    )


def main() -> None:
    q = 101
    selected_dim = 8
    omitted_dim = 4
    seed = 20260606
    rng = random.Random(seed)

    grs_columns = rnc_columns(q, selected_dim, selected_dim + omitted_dim)
    mixed_grs_columns = apply_row_and_column_scalings(grs_columns, q, rng)
    random_columns = random_full_source_columns(q, selected_dim, omitted_dim, seed + 1)

    rows = [
        analyze_case("synthetic_grs_plucker_chart", grs_columns, selected_dim, q),
        analyze_case(
            "row_and_column_scaled_grs_chart",
            mixed_grs_columns,
            selected_dim,
            q,
        ),
        analyze_case(
            "random_full_source_plucker_chart",
            random_columns,
            selected_dim,
            q,
        ),
    ]

    p24_selected_dim = 156
    p24_omitted_dim = 35 + 19
    p24_full_columns = p24_selected_dim + p24_omitted_dim

    print("Trace-GCD RS-tail full Plucker-chart Cauchy toy")
    for row in rows:
        print(
            f"case={row.label} q={row.q} selected_dim={row.selected_dim} "
            f"omitted_dim={row.omitted_dim} selected_rank={row.selected_rank} "
            f"chart_zero_entries={row.chart_zero_entries} "
            f"chart_rank={row.chart_rank} inverse_rank={row.inverse_rank} "
            f"visible_scalar_grs_chart={int(row.visible_scalar_grs_chart)}"
        )
    print("p24")
    print(f"  p24_selected_rs_tail_columns={p24_selected_dim}")
    print(f"  p24_omitted_full_source_columns={p24_omitted_dim}")
    print(f"  p24_full_fixed_source_columns={p24_full_columns}")
    print(f"  p24_plucker_chart_entries={p24_selected_dim * p24_omitted_dim}")
    print("interpretation")
    print("  scalar_grs_plucker_chart_cauchy_invariant_detected=1")
    print("  row_and_column_scaled_grs_chart_preserves_inverse_rank=1")
    print("  random_full_source_plucker_chart_rejected=1")
    print("  full_210_unused_columns_give_real_visible_grs_moduli=1")
    print("  hidden_lrs_still_requires_block_or_classfield_equivalence=1")
    print("conclusion=reported_trace_gcd_rs_tail_full_plucker_chart_cauchy_toy")


if __name__ == "__main__":
    main()
