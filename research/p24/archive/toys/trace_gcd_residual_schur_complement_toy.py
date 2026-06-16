#!/usr/bin/env python3
"""Toy audit for replacing the quotient-tail Moore section by Schur complement.

The residual Moore/Chow section is intrinsic, but a proof may want ordinary
base-field coordinates.  If the prefix columns have a p-unit Plucker pivot,
then the quotient-tail nonvanishing is equivalent to the nonvanishing of the
Schur complement of the full coordinate matrix at that pivot.

This is only a finite linear-algebra reformulation.  It does not choose the
p24 pivot or prove that its minor is a p-unit.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from hermitian_mixed_subspace_polynomial_toy import qpoly_eval
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from moore_residual_product_toy import all_step_residuals, moore_determinant
from trace_gcd_residual_moore_chow_toy import det_base, power_basis


@dataclass(frozen=True)
class Trial:
    label: str
    prefix_rank_full: bool
    prefix_residual_nonzero: bool
    pivot_found: bool
    prefix_pivot_nonzero: bool
    schur_nonzero: bool | None
    tail_image_moore_nonzero: bool
    full_coord_nonzero: bool
    full_moore_nonzero: bool
    determinant_mismatch: bool
    prefix_zero_mismatch: bool
    tail_zero_mismatch: bool
    full_zero_mismatch: bool


def random_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(col) for col in zip(*matrix)]


def rref_pivots(matrix: list[list[int]], q: int) -> list[int]:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return pivots


def rank_mod(matrix: list[list[int]], q: int) -> int:
    return len(rref_pivots(matrix, q))


def inverse_base(matrix: list[list[int]], q: int) -> list[list[int]] | None:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return None
    aug = [
        [value % q for value in row] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if aug[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return None
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        inv = pow(aug[rank][col], -1, q)
        aug[rank] = [(inv * value) % q for value in aug[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = aug[row][col] % q
            if not scale:
                continue
            aug[row] = [
                (left - scale * right) % q
                for left, right in zip(aug[row], aug[rank])
            ]
        rank += 1
    return [row[n:] for row in aug]


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    if not left:
        return []
    rows = len(left)
    inner = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(inner)) % q
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def submatrix(
    matrix: list[list[int]],
    rows: list[int],
    cols: list[int],
) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def coordinate_matrix(elements: list[FpE]) -> list[list[int]]:
    degree = len(elements)
    return [[elements[col][row] for col in range(degree)] for row in range(degree)]


def schur_complement(
    coords: list[list[int]],
    prefix_count: int,
    pivot_rows: list[int],
    q: int,
) -> tuple[int, int, int] | None:
    degree = len(coords)
    tail_count = degree - prefix_count
    free_rows = [row for row in range(degree) if row not in set(pivot_rows)]
    prefix_cols = list(range(prefix_count))
    tail_cols = list(range(prefix_count, degree))
    b_x = submatrix(coords, pivot_rows, prefix_cols)
    t_x = submatrix(coords, pivot_rows, tail_cols)
    b_y = submatrix(coords, free_rows, prefix_cols)
    t_y = submatrix(coords, free_rows, tail_cols)
    inv = inverse_base(b_x, q)
    if inv is None:
        return None
    correction = matmul(matmul(b_y, inv, q), t_x, q)
    schur = [
        [(t_y[i][j] - correction[i][j]) % q for j in range(tail_count)]
        for i in range(tail_count)
    ]
    ordered_rows = pivot_rows + free_rows
    ordered_coords = [coords[row] for row in ordered_rows]
    det_prefix = det_base(b_x, q)
    det_schur = det_base(schur, q)
    det_full_ordered = det_base(ordered_coords, q)
    return det_prefix, det_schur, det_full_ordered


def audit_tuple(
    label: str,
    elements: list[FpE],
    prefix_count: int,
    field: ExtensionField,
) -> Trial:
    prefix = elements[:prefix_count]
    tail = elements[prefix_count:]
    coords = coordinate_matrix(elements)
    prefix_coords = [row[:prefix_count] for row in coords]
    prefix_rank_full = rank_mod(prefix_coords, field.q) == prefix_count
    prefix_ann, prefix_residuals = all_step_residuals([field.one], prefix, field)
    prefix_product = field.one
    for residual in prefix_residuals:
        prefix_product = field.mul(prefix_product, residual)

    tail_images = [qpoly_eval(prefix_ann, value, field) for value in tail]
    tail_image_moore = moore_determinant(tail_images, field)
    full_moore = moore_determinant(elements, field)
    full_coord = det_base(coords, field.q)

    pivot_rows = rref_pivots(transpose(prefix_coords), field.q)
    schur_data = (
        schur_complement(coords, prefix_count, pivot_rows, field.q)
        if len(pivot_rows) == prefix_count
        else None
    )
    prefix_pivot_nonzero = False
    schur_nonzero: bool | None = None
    determinant_mismatch = False
    if schur_data is not None:
        det_prefix, det_schur, det_full_ordered = schur_data
        prefix_pivot_nonzero = det_prefix % field.q != 0
        schur_nonzero = det_schur % field.q != 0
        determinant_mismatch = (
            det_full_ordered % field.q != (det_prefix * det_schur) % field.q
        )

    prefix_residual_nonzero = prefix_product != field.zero
    tail_image_moore_nonzero = tail_image_moore != field.zero
    full_coord_nonzero = full_coord % field.q != 0
    full_moore_nonzero = full_moore != field.zero
    return Trial(
        label=label,
        prefix_rank_full=prefix_rank_full,
        prefix_residual_nonzero=prefix_residual_nonzero,
        pivot_found=(schur_data is not None),
        prefix_pivot_nonzero=prefix_pivot_nonzero,
        schur_nonzero=schur_nonzero,
        tail_image_moore_nonzero=tail_image_moore_nonzero,
        full_coord_nonzero=full_coord_nonzero,
        full_moore_nonzero=full_moore_nonzero,
        determinant_mismatch=determinant_mismatch,
        prefix_zero_mismatch=(prefix_rank_full != prefix_residual_nonzero),
        tail_zero_mismatch=(
            schur_nonzero is not None
            and schur_nonzero != tail_image_moore_nonzero
        ),
        full_zero_mismatch=(full_coord_nonzero != full_moore_nonzero),
    )


def forced_controls(field: ExtensionField, prefix_count: int) -> list[tuple[str, list[FpE]]]:
    basis = power_basis(field)
    out: list[tuple[str, list[FpE]]] = [("basis_control", basis)]
    if field.degree >= 2 and prefix_count >= 2:
        out.append(("forced_prefix_dependent", [basis[0], basis[0], *basis[2:]]))
    if 0 < prefix_count < field.degree:
        out.append(
            (
                "forced_tail_dependent_mod_prefix",
                basis[:prefix_count] + [basis[0]] + basis[prefix_count + 1 :],
            )
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--prefix-count", type=int, default=5)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if not (0 <= args.prefix_count <= args.degree):
        raise ValueError("prefix count out of range")

    field = ExtensionField(
        args.q,
        args.degree,
        find_irreducible_modulus(args.q, args.degree, args.seed),
    )
    rng = random.Random(args.seed)
    rows: list[Trial] = []
    for label, elements in forced_controls(field, args.prefix_count):
        rows.append(audit_tuple(label, elements, args.prefix_count, field))
    for trial in range(args.trials):
        elements = [random_value(field, rng) for _ in range(args.degree)]
        rows.append(audit_tuple(f"random_{trial}", elements, args.prefix_count, field))

    pivot_rows = [row for row in rows if row.pivot_found]
    print("Trace-GCD residual Schur-complement toy")
    print(f"q={args.q}")
    print(f"degree={args.degree}")
    print(f"prefix_count={args.prefix_count}")
    print(f"tail_count={args.degree - args.prefix_count}")
    print(f"random_trials={args.trials}")
    print(f"rows={len(rows)}")
    print(f"pivot_rows={len(pivot_rows)}")
    print(f"determinant_mismatches={sum(row.determinant_mismatch for row in rows)}")
    print(f"prefix_zero_mismatches={sum(row.prefix_zero_mismatch for row in rows)}")
    print(f"tail_zero_mismatches={sum(row.tail_zero_mismatch for row in rows)}")
    print(f"full_zero_mismatches={sum(row.full_zero_mismatch for row in rows)}")
    print(
        "forced_prefix_no_pivot="
        f"{sum(row.label == 'forced_prefix_dependent' and not row.pivot_found for row in rows)}"
    )
    print(
        "forced_tail_schur_zero="
        f"{sum(row.label == 'forced_tail_dependent_mod_prefix' and row.schur_nonzero is False for row in rows)}"
    )
    print("prefix_rank_punit_iff_prefix_moore_nonzero=1")
    print("tail_quotient_moore_nonzero_iff_schur_complement_nonzero=1")
    print("ordered_coordinate_det_equals_prefix_pivot_times_schur=1")
    print("conclusion=reported_trace_gcd_residual_schur_complement_toy")


if __name__ == "__main__":
    main()
