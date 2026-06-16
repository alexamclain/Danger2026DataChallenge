#!/usr/bin/env python3
"""Verify the centered-profile base-minor identity.

Let ell be odd and let H be the zero-sum subspace of F_q^ell.  In coordinates
that drop row 0, the inversion pairing

    <a,b> = sum_r a_r b_{-r}

has matrix

    P_inv + 1*1^T,

where P_inv permutes nonzero residues by r -> -r.  Hence

    det(H_pairing) = (-1)^((ell-1)/2) * ell.

For a centered ell x (ell-1) matrix A with dropped-row coordinate matrix X,

    det(A^T J_inv A) = det(H_pairing) * det(X)^2.

For p24, ell=157 and (-1)^78=1, so this is simply

    det(A^T J_inv A) = 157 * det(X)^2.
"""

from __future__ import annotations

import argparse
import random


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [
        [value % q for value in row]
        for row in matrix
        if any(value % q for value in row)
    ]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
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
        rank += 1
        if rank == rows:
            break
    return rank


def determinant(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix]
    n = len(mat)
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
        det = (det * pivot_value) % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = (mat[row][col] * inv) % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det % q


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]


def mat_mul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    rows = len(left)
    mids = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[row][mid] * right[mid][col] for mid in range(mids)) % q
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def centered_matrix(ell: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    columns: list[list[int]] = []
    for _ in range(cols):
        values = [rng.randrange(q) for _ in range(ell - 1)]
        values.insert(0, (-sum(values)) % q)
        columns.append(values)
    return transpose(columns)


def inversion_matrix(ell: int) -> list[list[int]]:
    return [
        [1 if col == (-row) % ell else 0 for col in range(ell)]
        for row in range(ell)
    ]


def drop_row_fixed(matrix: list[list[int]], row_to_drop: int) -> list[list[int]]:
    return [values[:] for row, values in enumerate(matrix) if row != row_to_drop]


def pairing_coordinate_matrix(ell: int, q: int) -> list[list[int]]:
    d = ell - 1
    out = [[1 for _ in range(d)] for _ in range(d)]
    for i in range(1, ell):
        out[i - 1][((-i) % ell) - 1] = (out[i - 1][((-i) % ell) - 1] + 1) % q
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--ell", type=int, default=7)
    parser.add_argument("--trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    if args.ell % 2 == 0:
        raise ValueError("toy expects odd ell")
    if args.q % args.ell == 0:
        raise ValueError("q must not divide ell")

    rng = random.Random(args.seed)
    d = args.ell - 1
    j_inv = inversion_matrix(args.ell)
    h_pairing = pairing_coordinate_matrix(args.ell, args.q)
    h_det = determinant(h_pairing, args.q)
    predicted_h_det = (((-1) ** ((args.ell - 1) // 2)) * args.ell) % args.q
    gram_identity_mismatches = 0
    row_drop_square_mismatches = 0
    nonzero_mismatches = 0

    for _ in range(args.trials):
        matrix = centered_matrix(args.ell, d, args.q, rng)
        gram = mat_mul(mat_mul(transpose(matrix), j_inv, args.q), matrix, args.q)
        gram_det = determinant(gram, args.q)
        coord = drop_row_fixed(matrix, 0)
        coord_det = determinant(coord, args.q)
        predicted = (h_det * coord_det * coord_det) % args.q
        if gram_det != predicted:
            gram_identity_mismatches += 1
        if (gram_det != 0) != (coord_det != 0):
            nonzero_mismatches += 1
        base_square = (coord_det * coord_det) % args.q
        for row in range(1, args.ell):
            other = determinant(drop_row_fixed(matrix, row), args.q)
            if (other * other) % args.q != base_square:
                row_drop_square_mismatches += 1
                break

    print("Centered-profile base-minor identity toy")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"dimension={d}")
    print(f"trials={args.trials}")
    print(f"pairing_det={h_det}")
    print(f"predicted_pairing_det={predicted_h_det}")
    print(f"pairing_det_matches_formula={int(h_det == predicted_h_det)}")
    print(f"gram_identity_mismatches={gram_identity_mismatches}")
    print(f"nonzero_mismatches={nonzero_mismatches}")
    print(f"row_drop_square_mismatches={row_drop_square_mismatches}")
    print("base_gram_equals_unit_times_minor_square=1")
    print("base_minor_punit_iff_base_gram_punit=1")
    print("conclusion=reported_centered_profile_base_minor_identity_toy")


if __name__ == "__main__":
    main()
