#!/usr/bin/env python3
"""CS-structure audit for CRT marginal top-coefficient matrices.

The p24 proof target now says that several CRT marginal matrices have full
rank over E.  Coding-theory language suggests possible stronger structures:

* MDS / superregular generator matrices;
* Toeplitz/Hankel/cyclic low-displacement-rank matrices;
* a random-looking rank condenser with no small deterministic structure.

This script tests those signatures on small tensor-factor rows, and compares
the actual CM marginal matrix with random tensor-factor controls of the same
shape.  It is intentionally a hypothesis filter, not a large computation.
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections import Counter

from k_character_tensor_rank_scan import ExtensionField, rank_over_extension
from tensor_factor_dual_basis_window_audit import top_window_coords
from tensor_factor_marginal_origin_action_audit import determinant
from tensor_factor_marginal_random_support_audit import (
    PreparedCase,
    combined_rows,
    prepare_case,
    random_b_element,
)


Matrix = list[list[tuple[int, ...]]]


def zero_matrix(rows: int, cols: int, field: ExtensionField) -> Matrix:
    return [[field.zero for _ in range(cols)] for _ in range(rows)]


def matrix_sub(left: Matrix, right: Matrix, field: ExtensionField) -> Matrix:
    return [
        [field.sub(a, b) for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def shift_rows_down(matrix: Matrix, field: ExtensionField, cyclic: bool) -> Matrix:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    if rows == 0:
        return []
    out = zero_matrix(rows, cols, field)
    for row in range(rows):
        source = (row - 1) % rows if cyclic else row - 1
        if source >= 0:
            out[row] = matrix[source][:]
    return out


def shift_cols_right(matrix: Matrix, field: ExtensionField, cyclic: bool) -> Matrix:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    out = zero_matrix(rows, cols, field)
    for row in range(rows):
        for col in range(cols):
            source = (col - 1) % cols if cyclic else col - 1
            if source >= 0:
                out[row][col] = matrix[row][source]
    return out


def shift_cols_left(matrix: Matrix, field: ExtensionField, cyclic: bool) -> Matrix:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    out = zero_matrix(rows, cols, field)
    for row in range(rows):
        for col in range(cols):
            source = (col + 1) % cols if cyclic else col + 1
            if source < cols:
                out[row][col] = matrix[row][source]
    return out


def rank(matrix: Matrix, field: ExtensionField) -> int:
    return rank_over_extension(matrix, field)


def displacement_ranks(matrix: Matrix, field: ExtensionField) -> dict[str, int]:
    """Return standard low-displacement-rank diagnostics.

    Toeplitz-like matrices have low rank for Z_r M - M Z_c.  Hankel-like
    matrices have low rank for Z_r M - M Z_c^T.  The cyclic variants test the
    same idea with wrap-around shifts.
    """
    zr = shift_rows_down(matrix, field, cyclic=False)
    cr = shift_cols_right(matrix, field, cyclic=False)
    cl = shift_cols_left(matrix, field, cyclic=False)
    czr = shift_rows_down(matrix, field, cyclic=True)
    ccr = shift_cols_right(matrix, field, cyclic=True)
    ccl = shift_cols_left(matrix, field, cyclic=True)
    return {
        "toeplitz": rank(matrix_sub(zr, cr, field), field),
        "hankel": rank(matrix_sub(zr, cl, field), field),
        "cyclic_toeplitz": rank(matrix_sub(czr, ccr, field), field),
        "cyclic_hankel": rank(matrix_sub(czr, ccl, field), field),
    }


def submatrix_by_cols(matrix: Matrix, cols: tuple[int, ...]) -> Matrix:
    return [[row[col] for col in cols] for row in matrix]


def submatrix_by_rows(matrix: Matrix, rows: tuple[int, ...]) -> Matrix:
    return [matrix[row][:] for row in rows]


def maximal_minor_summary(
    matrix: Matrix,
    field: ExtensionField,
    max_minors: int,
) -> dict[str, int | str]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    size = min(rows, cols)
    if size == 0:
        return {
            "minor_size": 0,
            "tested": 0,
            "zero": 0,
            "mode": "empty",
            "truncated": 0,
        }
    if rows <= cols:
        combos = itertools.combinations(range(cols), rows)
        total = 0
        zero = 0
        truncated = 0
        for cols_choice in combos:
            if total >= max_minors:
                truncated = 1
                break
            total += 1
            det = determinant(submatrix_by_cols(matrix, cols_choice), field)
            zero += int(det == field.zero)
        return {
            "minor_size": rows,
            "tested": total,
            "zero": zero,
            "mode": "column",
            "truncated": truncated,
        }
    combos = itertools.combinations(range(rows), cols)
    total = 0
    zero = 0
    truncated = 0
    for rows_choice in combos:
        if total >= max_minors:
            truncated = 1
            break
        total += 1
        det = determinant(submatrix_by_rows(matrix, rows_choice), field)
        zero += int(det == field.zero)
    return {
        "minor_size": cols,
        "tested": total,
        "zero": zero,
        "mode": "row",
        "truncated": truncated,
    }


def sequence_for_values(values, prepared: PreparedCase):
    return [
        top_window_coords(
            value,
            prepared.windows,
            prepared.subdegree,
            prepared.relative_degree,
            prepared.gprime_theta,
            prepared.basis_columns,
            prepared.selected_factor,
            prepared.field,
        )
        for value in values
    ]


def matrix_for_values(values, prepared: PreparedCase) -> Matrix:
    sequence = sequence_for_values(values, prepared)
    return combined_rows(
        sequence,
        prepared.components,
        prepared.include_constant,
        prepared.field,
    )


def structure_summary(matrix: Matrix, field: ExtensionField, max_minors: int) -> dict[str, object]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    disp = displacement_ranks(matrix, field)
    minors = maximal_minor_summary(matrix, field, max_minors)
    return {
        "rows": rows,
        "cols": cols,
        "rank": rank(matrix, field),
        "capacity": min(rows, cols),
        "displacement": disp,
        "minors": minors,
    }


def random_summaries(args: argparse.Namespace, prepared: PreparedCase) -> list[dict[str, object]]:
    rng = random.Random(args.seed + 9173)
    out = []
    for _ in range(args.random_trials):
        values = [
            random_b_element(rng, prepared)
            for _ in range(prepared.m)
        ]
        matrix = matrix_for_values(values, prepared)
        out.append(structure_summary(matrix, prepared.field, args.max_minors))
    return out


def rank_histogram(summaries: list[dict[str, object]], key: str) -> dict[int, int]:
    return dict(sorted(Counter(int(summary[key]) for summary in summaries).items()))


def displacement_histograms(summaries: list[dict[str, object]]) -> dict[str, dict[int, int]]:
    names = ("toeplitz", "hankel", "cyclic_toeplitz", "cyclic_hankel")
    out = {}
    for name in names:
        out[name] = dict(
            sorted(
                Counter(
                    int(summary["displacement"][name])  # type: ignore[index]
                    for summary in summaries
                ).items()
            )
        )
    return out


def minor_zero_histogram(summaries: list[dict[str, object]]) -> dict[int, int]:
    return dict(
        sorted(
            Counter(
                int(summary["minors"]["zero"])  # type: ignore[index]
                for summary in summaries
            ).items()
        )
    )


def print_summary(label: str, summary: dict[str, object]) -> None:
    print(label)
    print(f"  rows={summary['rows']}")
    print(f"  cols={summary['cols']}")
    print(f"  rank={summary['rank']}/{summary['capacity']}")
    disp = summary["displacement"]
    assert isinstance(disp, dict)
    print(
        "  displacement="
        + ",".join(f"{name}:{value}" for name, value in sorted(disp.items()))
    )
    minors = summary["minors"]
    assert isinstance(minors, dict)
    print(
        "  maximal_minors="
        f"mode:{minors['mode']},size:{minors['minor_size']},"
        f"tested:{minors['tested']},zero:{minors['zero']},"
        f"truncated:{minors['truncated']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=100)
    parser.add_argument("--max-minors", type=int, default=20000)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=3)
    parser.add_argument("--windows", type=int, default=2)
    parser.add_argument("--target", default="full")
    parser.add_argument("--without-constant", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    prepared = prepare_case(args)
    cm_matrix = matrix_for_values(prepared.cm_values, prepared)
    cm_summary = structure_summary(cm_matrix, prepared.field, args.max_minors)
    controls = random_summaries(args, prepared)

    print("tensor factor marginal CS-structure audit")
    print(f"D={prepared.D}")
    print(f"q={prepared.q}")
    print(f"ell={prepared.ell}")
    print(f"h={prepared.h}")
    print(f"m={prepared.m}")
    print(f"n={prepared.n}")
    print(f"factor_degree={prepared.factor_degree}")
    print(f"extension_degree={prepared.extension_degree}")
    print(f"tensor_factor_degree={prepared.tensor_factor_degree}")
    print(f"subdegree={prepared.subdegree}")
    print(f"windows={prepared.windows}")
    print(f"target_components={prepared.components}")
    print(f"include_constant={int(prepared.include_constant)}")
    print()

    print_summary("cm_matrix", cm_summary)
    print()
    print("random_controls")
    print(f"  trials={args.random_trials}")
    print(f"  rank_hist={rank_histogram(controls, 'rank')}")
    print(f"  displacement_hists={displacement_histograms(controls)}")
    print(f"  maximal_minor_zero_hist={minor_zero_histogram(controls)}")
    print()
    print("interpretation")
    print("  full_rank_is_rank_condenser_evidence=1")
    print("  low_displacement_would_indicate_toeplitz_hankel_cyclic_structure=1")
    print("  matching_random_controls_means_structure_is_generic_not_a_certificate=1")
    print("conclusion=reported_tensor_factor_marginal_cs_structure_audit")


if __name__ == "__main__":
    main()
