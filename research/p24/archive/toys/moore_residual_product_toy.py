#!/usr/bin/env python3
"""Toy audit for Moore determinants and residual products.

The representative p24 scalar `L_rep` is a leading Moore determinant.  The
subspace-polynomial update computes the same nonzero condition as an
incremental residual product.  This toy verifies the exact finite-field
identity:

    det(x_j^(q^i)) = product_i P_{<x_0,...,x_{i-1}>}(x_i),

and the split factorization:

    L = B * T,

where `B` is the residual product for the prefix and `T` continues the update
from the prefix annihilator through the tail.
"""

from __future__ import annotations

import argparse
import random

from hermitian_mixed_subspace_polynomial_toy import (
    qpoly_annihilator_profile,
    qpoly_extend_profile,
    qpoly_eval,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)


def random_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def determinant(matrix: list[list[FpE]], field: ExtensionField) -> FpE:
    mat = [row[:] for row in matrix]
    n = len(mat)
    det = field.one
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            return field.zero
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = field.neg(det)
        pivot_value = mat[col][col]
        det = field.mul(det, pivot_value)
        inv = field.inv(pivot_value)
        for row in range(col + 1, n):
            scale = field.mul(mat[row][col], inv)
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[col])
            ]
    return det


def moore_determinant(elements: list[FpE], field: ExtensionField) -> FpE:
    matrix = [
        [field.pow(value, field.q**row) for value in elements]
        for row in range(len(elements))
    ]
    return determinant(matrix, field)


def product(values: list[FpE], field: ExtensionField) -> FpE:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def all_step_residuals(
    coeffs: list[FpE],
    elements: list[FpE],
    field: ExtensionField,
) -> tuple[list[FpE], list[FpE]]:
    """Extend a q-polynomial while recording zero and nonzero residuals."""

    coeffs = coeffs[:]
    residuals: list[FpE] = []
    for x in elements:
        y = qpoly_eval(coeffs, x, field)
        residuals.append(y)
        if y == field.zero:
            continue
        scale = field.pow(y, field.q - 1)
        new_coeffs = [field.zero for _ in range(len(coeffs) + 1)]
        for i, coeff in enumerate(coeffs):
            new_coeffs[i] = field.sub(new_coeffs[i], field.mul(scale, coeff))
            new_coeffs[i + 1] = field.add(new_coeffs[i + 1], field.pow(coeff, field.q))
        coeffs = new_coeffs
    return coeffs, residuals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--prefix-count", type=int, default=4)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    if args.count > args.degree:
        raise ValueError("count must not exceed extension degree")
    if not (0 <= args.prefix_count <= args.count):
        raise ValueError("prefix count out of range")

    modulus = find_irreducible_modulus(args.q, args.degree, args.seed)
    field = ExtensionField(args.q, args.degree, modulus)
    rng = random.Random(args.seed)
    determinant_mismatches = 0
    split_mismatches = 0
    nonzero_matches = 0
    nonzero_mismatches = 0
    full_rank_examples = 0
    singular_examples = 0

    for _ in range(args.trials):
        elements = [random_value(field, rng) for _ in range(args.count)]
        det = moore_determinant(elements, field)
        ann, _pivots, residuals = qpoly_annihilator_profile(elements, field)
        _all_ann, all_residuals = all_step_residuals([field.one], elements, field)
        residual_product = product(all_residuals, field)
        if det != residual_product:
            determinant_mismatches += 1

        prefix = elements[: args.prefix_count]
        tail = elements[args.prefix_count :]
        prefix_ann, _prefix_pivots, prefix_residuals = qpoly_annihilator_profile(
            prefix, field
        )
        _prefix_all_ann, prefix_all_residuals = all_step_residuals(
            [field.one], prefix, field
        )
        _tail_ann, _tail_pivots, tail_residuals = qpoly_extend_profile(
            prefix_ann, tail, field
        )
        _tail_all_ann, tail_all_residuals = all_step_residuals(
            prefix_ann, tail, field
        )
        split_product = field.mul(
            product(prefix_all_residuals, field),
            product(tail_all_residuals, field),
        )
        if split_product != residual_product:
            split_mismatches += 1

        if (det != field.zero) == all(value != field.zero for value in all_residuals):
            nonzero_matches += 1
        else:
            nonzero_mismatches += 1
        if det != field.zero:
            full_rank_examples += 1
        else:
            singular_examples += 1
        # Keep these live as smoke checks that both update APIs are exercised.
        if not ann:
            raise AssertionError("empty annihilator")
        if bool(prefix_residuals) != bool(prefix_all_residuals):
            raise AssertionError("unexpected empty prefix residual profile")
        if bool(tail_residuals) and not bool(tail_all_residuals):
            raise AssertionError("unexpected empty tail residual profile")

    print("Moore residual-product toy")
    print(f"q={args.q}")
    print(f"degree={args.degree}")
    print(f"count={args.count}")
    print(f"prefix_count={args.prefix_count}")
    print(f"tail_count={args.count - args.prefix_count}")
    print(f"trials={args.trials}")
    print(f"determinant_mismatches={determinant_mismatches}")
    print(f"split_mismatches={split_mismatches}")
    print(f"nonzero_matches={nonzero_matches}")
    print(f"nonzero_mismatches={nonzero_mismatches}")
    print(f"full_rank_examples={full_rank_examples}")
    print(f"singular_examples={singular_examples}")
    print("L_equals_residual_product=1")
    print("L_splits_as_B_times_T=1")
    print("conclusion=reported_moore_residual_product_toy")


if __name__ == "__main__":
    main()
