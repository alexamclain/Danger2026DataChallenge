#!/usr/bin/env python3
"""Rank compatibility for the order-7 augmentation target.

This is a finite linear-algebra gate for the p24 fixed-frequency route.  The
order-7 augmentation theorem asks for seven coset sums in the 210 nonzero
right-frequency coordinates to vanish.  Ordinary centering is only their total
sum, so augmentation adds six independent equations.

The useful sanity check is that these six extra equations are neither forced
by the existing generic evidence nor too strong for the fixed square: the
augmentation subspace still has dimension 203, comfortably above the 156 rows
needed by the fixed determinant.
"""

from __future__ import annotations

import random


Q = 1009
RIGHT_COORDS = 210
ORDER7 = 7
COSET_SIZE = RIGHT_COORDS // ORDER7
TARGET_RANK = 156


def rank_mod(matrix: list[list[int]], q: int = Q) -> int:
    rows = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for col in range(width):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][col] % q), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % q, -1, q)
        rows[rank] = [value * inv % q for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank:
                continue
            scale = rows[row][col] % q
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def centering_constraint() -> list[list[int]]:
    return [[1] * RIGHT_COORDS]


def augmentation_constraints() -> list[list[int]]:
    return [
        [int(index % ORDER7 == residue) for index in range(RIGHT_COORDS)]
        for residue in range(ORDER7)
    ]


def coset_sums(row: list[int]) -> list[int]:
    sums = [0] * ORDER7
    for index, value in enumerate(row):
        sums[index % ORDER7] = (sums[index % ORDER7] + value) % Q
    return sums


def coset_sum_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [coset_sums(row) for row in matrix]


def all_centered(matrix: list[list[int]]) -> bool:
    return all(sum(row) % Q == 0 for row in matrix)


def all_augmented(matrix: list[list[int]]) -> bool:
    return all(all(value == 0 for value in coset_sums(row)) for row in matrix)


def shifted_by_unit2(matrix: list[list[int]]) -> list[list[int]]:
    shifted = []
    for row in matrix:
        out = [0] * RIGHT_COORDS
        for index, value in enumerate(row):
            out[(index + 1) % RIGHT_COORDS] = value
        shifted.append(out)
    return shifted


def random_centered_row(rng: random.Random) -> list[int]:
    row = [rng.randrange(Q) for _ in range(RIGHT_COORDS - 1)]
    row.append((-sum(row)) % Q)
    return row


def random_augmented_row(rng: random.Random) -> list[int]:
    row = [0] * RIGHT_COORDS
    for residue in range(ORDER7):
        members = [index for index in range(RIGHT_COORDS) if index % ORDER7 == residue]
        partial = 0
        for index in members[:-1]:
            row[index] = rng.randrange(Q)
            partial = (partial + row[index]) % Q
        row[members[-1]] = (-partial) % Q
    return row


def full_rank_rows(
    rng: random.Random,
    row_builder,
    target_rank: int = TARGET_RANK,
    attempts: int = 20,
) -> list[list[int]]:
    for _attempt in range(attempts):
        matrix = [row_builder(rng) for _ in range(target_rank)]
        if rank_mod(matrix) == target_rank:
            return matrix
    raise RuntimeError("failed to sample a full-rank matrix")


def main() -> None:
    rng = random.Random(20260606)
    center = centering_constraint()
    augment = augmentation_constraints()
    center_rank = rank_mod(center)
    augment_rank = rank_mod(augment)
    combined_rank = rank_mod(center + augment)

    centered = full_rank_rows(rng, random_centered_row)
    augmented = full_rank_rows(rng, random_augmented_row)
    shifted_centered = shifted_by_unit2(centered)
    shifted_augmented = shifted_by_unit2(augmented)

    centered_coset_rank = rank_mod(coset_sum_matrix(centered))
    augmented_coset_rank = rank_mod(coset_sum_matrix(augmented))
    shifted_centered_coset_rank = rank_mod(coset_sum_matrix(shifted_centered))

    print("Trace-GCD fixed-frequency order-7 rank compatibility toy")
    print(f"field_q={Q}")
    print(f"right_frequency_coordinates={RIGHT_COORDS}")
    print(f"order7_coset_size={COSET_SIZE}")
    print(f"target_row_rank={TARGET_RANK}")
    print(f"centering_constraints_rank={center_rank}")
    print(f"augmentation_constraints_rank={augment_rank}")
    print(f"augmentation_extra_rank_over_centering={combined_rank - center_rank}")
    print(f"centered_subspace_dimension={RIGHT_COORDS - center_rank}")
    print(f"augmentation_subspace_dimension={RIGHT_COORDS - augment_rank}")
    print(f"augmentation_rank_margin={(RIGHT_COORDS - augment_rank) - TARGET_RANK}")
    print(f"centered_full_rank_possible={int(rank_mod(centered) == TARGET_RANK)}")
    print(f"centered_all_rows_centered={int(all_centered(centered))}")
    print(f"centered_nontrivial_quotient_rank={centered_coset_rank}")
    print(f"centered_random_has_nontrivial_quotient_leak={int(centered_coset_rank == ORDER7 - 1)}")
    print(f"augmentation_zero_full_rank_possible={int(rank_mod(augmented) == TARGET_RANK)}")
    print(f"augmentation_zero_coset_sum_rank={augmented_coset_rank}")
    print(f"augmentation_zero_all_rows_augmented={int(all_augmented(augmented))}")
    print(f"unit2_preserves_augmentation_subspace={int(all_augmented(shifted_augmented))}")
    print(f"unit2_preserves_centering={int(all_centered(shifted_centered))}")
    print(
        "unit2_preserves_centering_but_not_force_augmentation="
        f"{int(shifted_centered_coset_rank == ORDER7 - 1)}"
    )
    print("interpretation")
    print("  order7_augmentation_adds_six_equations_beyond_centering=1")
    print("  order7_augmentation_is_compatible_with_156_rank_fixed_square=1")
    print("  full_rank_and_unit2_transport_do_not_prove_order7_augmentation=1")
    print("  p24_missing_theorem_remains_specific_cm_lang_vanishing=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_rank_compatibility_toy")

    if center_rank != 1 or augment_rank != ORDER7 or combined_rank != ORDER7:
        raise SystemExit(1)
    if rank_mod(centered) != TARGET_RANK or not all_centered(centered):
        raise SystemExit(1)
    if centered_coset_rank != ORDER7 - 1:
        raise SystemExit(1)
    if rank_mod(augmented) != TARGET_RANK or not all_augmented(augmented):
        raise SystemExit(1)
    if augmented_coset_rank != 0:
        raise SystemExit(1)
    if not all_augmented(shifted_augmented) or not all_centered(shifted_centered):
        raise SystemExit(1)
    if shifted_centered_coset_rank != ORDER7 - 1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
