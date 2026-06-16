#!/usr/bin/env python3
"""Toy audit for the right-unit equivariance/subspace-orbit distinction.

The p24 verifier uses the unit `2 mod 211` to propagate whole deletion-row
certificates.  A tempting shortcut is to infer that, inside one fixed row, the
six trace-coordinate subspaces

    W_j = span_Fq{right Lang coordinates from orbit O_j} subset L

are themselves generated from one W by a single Fq-linear operator on L.

This toy checks the analogous claim in a random finite-field DFT model with
six right Frobenius orbits.  The expected outcome is that unit permutations of
right orbit labels do not force equality of the W_j inside one fixed row.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp

from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_dual_trace_injectivity_toy import random_base_table
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    matrix_vector_mul,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {
        value: index
        for index, orbit in enumerate(orbits)
        for value in orbit
    }


def unit_permutation(unit: int, modulus: int, orbits: list[list[int]]) -> tuple[int, ...]:
    labels = orbit_label_map(orbits)
    return tuple(labels[(unit * orbit[0]) % modulus] for orbit in orbits)


def find_six_cycle_unit(modulus: int, orbits: list[list[int]]) -> tuple[int, tuple[int, ...]]:
    for unit in range(2, modulus):
        if sp.gcd(unit, modulus) != 1:
            continue
        perm = unit_permutation(unit, modulus, orbits)
        seen = set()
        value = 0
        for _ in range(len(orbits)):
            seen.add(value)
            value = perm[value]
        if len(seen) == len(orbits) and value == 0:
            return unit, perm
    raise ValueError("no unit cycling all right orbits")


def transformed_for_orbit(
    dft_matrix,
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbit: list[int],
    q: int,
    field: ExtensionField,
    seed: int,
):
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    inverse = lang_inverse_for_orbit(q, len(right_orbit), field, seed)
    seed_vector = [
        dft_matrix[row_index[left_orbit[0]]][col_index[v]]
        for v in right_orbit
    ]
    return matrix_vector_mul(inverse, seed_vector, field)


def subspace_equal(left_values, right_values, q: int) -> bool:
    left_rank = fq_rank(left_values, q)
    right_rank = fq_rank(right_values, q)
    joined_rank = fq_rank(list(left_values) + list(right_values), q)
    return left_rank == right_rank == joined_rank


def frobenius_block(values, shift: int, field: ExtensionField):
    return [field.pow(value, field.q**shift) for value in values]


def frobenius_equal_shifts(left_values, right_values, left_degree: int, q: int, field):
    return [
        shift
        for shift in range(left_degree)
        if subspace_equal(frobenius_block(left_values, shift, field), right_values, q)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left", type=int, default=11)
    parser.add_argument("--right", type=int, default=31)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    left_degree = int(sp.n_order(args.q % args.left, args.left))
    right_degree = int(sp.n_order(args.q % args.right, args.right))
    extension_degree = int(sp.ilcm(left_degree, right_degree))
    modulus = find_irreducible_modulus(args.q, extension_degree, args.seed)
    field = ExtensionField(args.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, args.left * args.right, args.seed)
    powers = zeta_powers(zeta, args.left * args.right, field)

    rng = random.Random(args.seed)
    table = random_base_table(args.left, args.right, args.q, rng)
    dft_matrix = dft_double_marginal(
        table,
        args.left,
        args.right,
        powers,
        args.left * args.right,
        field,
    )
    left_orbits = q_orbits(args.left, args.q)
    right_orbits = q_orbits(args.right, args.q)
    unit, perm = find_six_cycle_unit(args.right, right_orbits)
    left_orbit = left_orbits[0]

    blocks = [
        transformed_for_orbit(
            dft_matrix,
            args.left,
            args.right,
            left_orbit,
            right_orbit,
            args.q,
            field,
            args.seed,
        )
        for right_orbit in right_orbits
    ]
    ranks = [fq_rank(block, args.q) for block in blocks]
    pair_join_ranks = []
    equal_pairs = 0
    unit_equal_edges = 0
    unit_frobenius_edge_shifts: list[list[int]] = []
    for i, block in enumerate(blocks):
        nxt = perm[i]
        joined = fq_rank(block + blocks[nxt], args.q)
        pair_join_ranks.append(joined)
        if subspace_equal(block, blocks[nxt], args.q):
            unit_equal_edges += 1
        unit_frobenius_edge_shifts.append(
            frobenius_equal_shifts(block, blocks[nxt], left_degree, args.q, field)
        )
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            if subspace_equal(blocks[i], blocks[j], args.q):
                equal_pairs += 1

    print("Right-unit subspace orbit toy")
    print(f"q={args.q}")
    print(f"left={args.left}")
    print(f"right={args.right}")
    print(f"left_degree={left_degree}")
    print(f"right_degree={right_degree}")
    print(f"right_orbit_count={len(right_orbits)}")
    print(f"extension_degree={extension_degree}")
    print(f"unit_cycle={unit}")
    print(f"unit_permutation_1based={[x + 1 for x in perm]}")
    print(f"block_ranks={ranks}")
    print(f"unit_edge_join_ranks={pair_join_ranks}")
    print(f"unit_equal_edges={unit_equal_edges}/{len(blocks)}")
    print(f"unit_frobenius_edge_shifts={unit_frobenius_edge_shifts}")
    print(
        "unit_frobenius_equal_edges="
        f"{sum(1 for shifts in unit_frobenius_edge_shifts if shifts)}/{len(blocks)}"
    )
    print(f"all_equal_pairs={equal_pairs}/{len(blocks) * (len(blocks) - 1) // 2}")
    print(
        "interpretation="
        "unit_permutation_of_labels_does_not_force_fixed_row_subspace_equality"
    )
    print("conclusion=reported_right_unit_subspace_orbit_toy")


if __name__ == "__main__":
    main()
