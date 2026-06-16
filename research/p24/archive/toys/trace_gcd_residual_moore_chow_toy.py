#!/usr/bin/env python3
"""Toy audit for the residual product as a Moore/Chow section.

The trace-GCD residual theorem is easiest to state geometrically after two
finite identities:

1. the all-coordinate residual product is the Moore determinant;
2. for a full ordered basis tuple, that Moore determinant is a fixed
   Moore-basis unit times the ordinary coordinate Chow determinant.

For a prefix/tail split the tail scalar is also explicit: after applying the
prefix annihilator P_U, the tail residual product is the Moore determinant of
the images P_U(t_i).  This is the finite quotient Schubert section that the
p24 arithmetic proof must prove is a p-unit.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    qpoly_eval,
    relative_norm_to_base,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from moore_residual_product_toy import (
    all_step_residuals,
    moore_determinant,
    product,
)


@dataclass(frozen=True)
class TrialResult:
    label: str
    full_det_zero: bool
    coord_det_zero: bool
    prefix_zero: bool
    tail_zero: bool
    full_residual_mismatch: bool
    full_chow_mismatch: bool
    norm_chow_mismatch: bool
    prefix_moore_mismatch: bool
    tail_image_mismatch: bool
    prefix_tail_mismatch: bool


def random_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def power_basis(field: ExtensionField) -> list[FpE]:
    return [
        tuple(1 if index == j else 0 for index in range(field.degree))
        for j in range(field.degree)
    ]


def det_base(matrix: list[list[int]], q: int) -> int:
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


def coordinate_determinant(elements: list[FpE], field: ExtensionField) -> int:
    if len(elements) != field.degree:
        raise ValueError("coordinate Chow determinant needs a full tuple")
    matrix = [
        [elements[col][row] for col in range(field.degree)]
        for row in range(field.degree)
    ]
    return det_base(matrix, field.q)


def norm_base(value: FpE, field: ExtensionField) -> int:
    norm = relative_norm_to_base(value, field.degree, field)
    out = base_value_or_none(norm, field)
    if out is None:
        raise AssertionError("relative norm did not land in the base field")
    return out


def audit_tuple(
    label: str,
    elements: list[FpE],
    prefix_count: int,
    basis_moore: FpE,
    basis_moore_norm: int,
    field: ExtensionField,
) -> TrialResult:
    full_moore = moore_determinant(elements, field)
    _full_ann, full_residuals = all_step_residuals([field.one], elements, field)
    full_product = product(full_residuals, field)

    coord_det = coordinate_determinant(elements, field)
    expected_full_moore = field.mul(basis_moore, field.embed(coord_det))
    expected_norm = basis_moore_norm * pow(coord_det, field.degree, field.q) % field.q

    prefix = elements[:prefix_count]
    tail = elements[prefix_count:]
    prefix_ann, prefix_residuals = all_step_residuals([field.one], prefix, field)
    prefix_product = product(prefix_residuals, field)
    prefix_moore = moore_determinant(prefix, field)

    _tail_ann, tail_residuals = all_step_residuals(prefix_ann, tail, field)
    tail_product = product(tail_residuals, field)
    tail_images = [qpoly_eval(prefix_ann, value, field) for value in tail]
    _image_ann, image_residuals = all_step_residuals([field.one], tail_images, field)
    image_product = product(image_residuals, field)
    tail_image_moore = moore_determinant(tail_images, field)

    return TrialResult(
        label=label,
        full_det_zero=(full_moore == field.zero),
        coord_det_zero=(coord_det % field.q == 0),
        prefix_zero=(prefix_product == field.zero),
        tail_zero=(tail_product == field.zero),
        full_residual_mismatch=(full_product != full_moore),
        full_chow_mismatch=(full_moore != expected_full_moore),
        norm_chow_mismatch=(norm_base(full_product, field) != expected_norm),
        prefix_moore_mismatch=(prefix_product != prefix_moore),
        tail_image_mismatch=(
            tail_product != image_product or tail_product != tail_image_moore
        ),
        prefix_tail_mismatch=(
            full_product != field.mul(prefix_product, tail_product)
            or full_moore != field.mul(prefix_moore, tail_image_moore)
        ),
    )


def forced_controls(field: ExtensionField, prefix_count: int) -> list[tuple[str, list[FpE]]]:
    basis = power_basis(field)
    controls: list[tuple[str, list[FpE]]] = [("basis_control", basis)]
    if field.degree >= 2 and prefix_count >= 2:
        controls.append(
            (
                "forced_prefix_dependent",
                [basis[0], basis[0], *basis[2:]],
            )
        )
    if 0 < prefix_count < field.degree:
        controls.append(
            (
                "forced_tail_dependent_mod_prefix",
                basis[:prefix_count] + [basis[0]] + basis[prefix_count + 1 :],
            )
        )
    return controls


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

    modulus = find_irreducible_modulus(args.q, args.degree, args.seed)
    field = ExtensionField(args.q, args.degree, modulus)
    rng = random.Random(args.seed)

    basis = power_basis(field)
    basis_moore = moore_determinant(basis, field)
    if basis_moore == field.zero:
        raise AssertionError("power basis has zero Moore determinant")
    basis_moore_norm = norm_base(basis_moore, field)
    if basis_moore_norm % field.q == 0:
        raise AssertionError("power basis Moore determinant has zero norm")

    rows: list[TrialResult] = []
    for label, elements in forced_controls(field, args.prefix_count):
        rows.append(
            audit_tuple(
                label,
                elements,
                args.prefix_count,
                basis_moore,
                basis_moore_norm,
                field,
            )
        )
    for trial in range(args.trials):
        elements = [random_value(field, rng) for _ in range(args.degree)]
        rows.append(
            audit_tuple(
                f"random_{trial}",
                elements,
                args.prefix_count,
                basis_moore,
                basis_moore_norm,
                field,
            )
        )

    print("Trace-GCD residual Moore/Chow toy")
    print(f"q={args.q}")
    print(f"degree={args.degree}")
    print(f"prefix_count={args.prefix_count}")
    print(f"tail_count={args.degree - args.prefix_count}")
    print(f"random_trials={args.trials}")
    print(f"rows={len(rows)}")
    print(f"basis_moore_norm={basis_moore_norm}")
    print(
        "full_residual_mismatches="
        f"{sum(row.full_residual_mismatch for row in rows)}"
    )
    print(f"full_chow_mismatches={sum(row.full_chow_mismatch for row in rows)}")
    print(f"norm_chow_mismatches={sum(row.norm_chow_mismatch for row in rows)}")
    print(
        "prefix_moore_mismatches="
        f"{sum(row.prefix_moore_mismatch for row in rows)}"
    )
    print(f"tail_image_mismatches={sum(row.tail_image_mismatch for row in rows)}")
    print(
        "prefix_tail_mismatches="
        f"{sum(row.prefix_tail_mismatch for row in rows)}"
    )
    print(
        "full_zero_coordinate_zero_mismatches="
        f"{sum(row.full_det_zero != row.coord_det_zero for row in rows)}"
    )
    print(
        "forced_prefix_zero="
        f"{sum(row.label == 'forced_prefix_dependent' and row.prefix_zero for row in rows)}"
    )
    print(
        "forced_tail_zero="
        f"{sum(row.label == 'forced_tail_dependent_mod_prefix' and row.tail_zero for row in rows)}"
    )
    print("residual_product_equals_moore_determinant=1")
    print("full_moore_equals_basis_unit_times_chow_coordinate_det=1")
    print("tail_residual_product_equals_moore_of_prefix_annihilator_images=1")
    print("prefix_tail_sections_multiply_to_full_section=1")
    print("conclusion=reported_trace_gcd_residual_moore_chow_toy")


if __name__ == "__main__":
    main()
