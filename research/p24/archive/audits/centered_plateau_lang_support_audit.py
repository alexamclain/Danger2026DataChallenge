#!/usr/bin/env python3
"""Audit plateau subspaces after right Fourier/Lang normalization.

The centered consecutive-arc bad event is not a coordinate-erasure event in
the right Fourier/Lang basis.  A plateau subspace is sparse in the time basis,
but the Fourier/Lang transform spreads it across right-orbit coordinates.

Centered dual words also satisfy `w_0=0`, because the centered point column
`P_0` is zero.  The relevant bad subspace is therefore the plateau subspace
intersected with the hyperplane `w_0=0`.

This script computes the exact transformed support profile in small prime
right lengths.  It is a finite linear-algebra boundary for importing ordinary
MDS or LRS/MSRD distance theorems: such theorems apply directly to
coordinate/rank-support subspaces, while the centered bad subspaces may become
dense Schubert subspaces after the natural normalization.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q


def extension_zero(field: ExtensionField) -> FpE:
    return field.zero


def ext_to_base(value: FpE, field: ExtensionField) -> int:
    if any(coeff % field.q for coeff in value[1:]):
        raise ValueError(f"expected base-field element, got {value}")
    return value[0] % field.q


def dft_value(word: list[int], frequency: int, zeta: FpE, field: ExtensionField) -> FpE:
    total = field.zero
    power = field.one
    zeta_frequency = field.pow(zeta, frequency % len(word))
    for value in word:
        total = field.add(total, field.scalar_mul(value, power))
        power = field.mul(power, zeta_frequency)
    return total


def lang_transform_word(
    word: list[int],
    q: int,
    right: int,
    field: ExtensionField,
    zeta: FpE,
    seed: int,
) -> tuple[list[int], list[tuple[str, tuple[int, ...]]]]:
    out = [sum(word) % q]
    blocks: list[tuple[str, tuple[int, ...]]] = [("zero", (0,))]
    offset = 1
    for orbit in q_orbits(right, q):
        inverse = lang_inverse_for_orbit(q, len(orbit), field, seed)
        values = [dft_value(word, frequency, zeta, field) for frequency in orbit]
        coords = [ext_to_base(value, field) for value in matrix_vector_mul(inverse, values, field)]
        out.extend(coords)
        blocks.append((f"orbit:{orbit[0]}", tuple(range(offset, offset + len(coords)))))
        offset += len(coords)
    if len(out) != right:
        raise AssertionError("right Fourier/Lang transform should have right coordinates")
    return out, blocks


def plateau_basis(
    right: int,
    left: int,
    start: int,
    zero_position: int,
) -> list[list[int]]:
    """Basis for words constant on the plateau and zero at zero_position."""

    plateau = {(start + offset) % right for offset in range(left)}
    basis: list[list[int]] = []
    if zero_position % right not in plateau:
        constant = [0 for _ in range(right)]
        for index in plateau:
            constant[index] = 1
        basis.append(constant)
    for index in range(right):
        if index in plateau or index == zero_position % right:
            continue
        vector = [0 for _ in range(right)]
        vector[index] = 1
        basis.append(vector)
    return basis


def support_size(row: list[int], q: int) -> int:
    return sum(1 for value in row if value % q)


def active_columns(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 0
    return sum(
        1
        for col in range(len(matrix[0]))
        if any(row[col] % q for row in matrix)
    )


def min_support(matrix: list[list[int]], q: int) -> tuple[int, tuple[int, ...] | None]:
    """Minimum Hamming support of a nonzero word in rowspace(matrix)."""

    rank = rank_mod_q(matrix, q)
    width = len(matrix[0]) if matrix else 0
    columns = tuple(range(width))
    for size in range(1, width + 1):
        for support in combinations(columns, size):
            support_set = set(support)
            complement = [col for col in columns if col not in support_set]
            projected = [[row[col] for col in complement] for row in matrix]
            if rank_mod_q(projected, q) < rank:
                return size, support
    return 0, None


def min_block_support(
    matrix: list[list[int]],
    blocks: list[tuple[str, tuple[int, ...]]],
    q: int,
) -> tuple[int, tuple[str, ...] | None]:
    rank = rank_mod_q(matrix, q)
    block_indices = tuple(range(len(blocks)))
    for size in range(1, len(blocks) + 1):
        for support in combinations(block_indices, size):
            support_set = set(support)
            complement_cols = [
                col
                for block_index, (_name, cols) in enumerate(blocks)
                if block_index not in support_set
                for col in cols
            ]
            projected = [[row[col] for col in complement_cols] for row in matrix]
            if rank_mod_q(projected, q) < rank:
                return size, tuple(blocks[index][0] for index in support)
    return 0, None


def block_rank_profile(
    matrix: list[list[int]],
    blocks: list[tuple[str, tuple[int, ...]]],
    q: int,
) -> list[tuple[str, int, int]]:
    profile: list[tuple[str, int, int]] = []
    for name, cols in blocks:
        projected = [[row[col] for col in cols] for row in matrix]
        profile.append((name, len(cols), rank_mod_q(projected, q)))
    return profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, required=True)
    parser.add_argument("--right", type=int, required=True)
    parser.add_argument("--left", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--zero-position", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument(
        "--skip-min-support",
        action="store_true",
        help="Skip exhaustive transformed Hamming minimum-support search.",
    )
    args = parser.parse_args()

    degree = 1
    if args.right > 1:
        import sympy as sp

        degree = int(sp.n_order(args.q % args.right, args.right))
    modulus = find_irreducible_modulus(args.q, degree, args.seed)
    field = ExtensionField(args.q, degree, modulus)
    zeta = primitive_root_of_order(field, args.right, args.seed)
    basis = plateau_basis(args.right, args.left, args.start, args.zero_position)
    transformed_rows: list[list[int]] = []
    blocks: list[tuple[str, tuple[int, ...]]] | None = None
    for word in basis:
        transformed, word_blocks = lang_transform_word(
            word, args.q, args.right, field, zeta, args.seed
        )
        transformed_rows.append(transformed)
        if blocks is None:
            blocks = word_blocks
    if blocks is None:
        raise RuntimeError("empty basis")

    original_rank = rank_mod_q(basis, args.q)
    transformed_rank = rank_mod_q(transformed_rows, args.q)
    min_time = min(support_size(row, args.q) for row in basis if any(v % args.q for v in row))
    min_lang, min_lang_support = (
        (-1, None)
        if args.skip_min_support
        else min_support(transformed_rows, args.q)
    )
    min_blocks, min_block_names = min_block_support(transformed_rows, blocks, args.q)

    print("Centered plateau Fourier/Lang support audit")
    print(f"q={args.q}")
    print(f"right={args.right}")
    print(f"left_plateau_length={args.left}")
    print(f"start={args.start}")
    print(f"zero_position={args.zero_position % args.right}")
    print(f"ord_right_q={degree}")
    print(f"plateau_subspace_dim={len(basis)}")
    print(f"original_rank={original_rank}")
    print(f"transformed_rank={transformed_rank}")
    print(f"minimum_basis_time_support={min_time}")
    print(f"transformed_active_columns={active_columns(transformed_rows, args.q)}/{args.right}")
    if args.skip_min_support:
        print("transformed_min_hamming_support=skipped")
        print("transformed_min_hamming_support_example=skipped")
    else:
        print(f"transformed_min_hamming_support={min_lang}")
        print(f"transformed_min_hamming_support_example={min_lang_support}")
    print(f"block_count={len(blocks)}")
    print(f"block_rank_profile={block_rank_profile(transformed_rows, blocks, args.q)}")
    print(f"transformed_min_block_support={min_blocks}")
    print(f"transformed_min_block_support_example={min_block_names}")
    print()
    print("interpretation")
    print("  plateau_subspace_is_sparse_in_time_coordinates=1")
    print("  fourier_lang_transform_spreads_plateau_subspace=1")
    print("  coordinate_support_distance_theorems_do_not_directly_apply_after_lang=1")
    print("conclusion=reported_centered_plateau_lang_support_audit")


if __name__ == "__main__":
    main()
