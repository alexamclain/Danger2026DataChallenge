#!/usr/bin/env python3
"""Eliminate the affine offsets by taking right C_7 differences.

The affine quotient-profile target says that for each nonzero relative <p>
coset D,

    M_i(D) = w*b_i + gamma_D,

where i runs over the seven right H-cosets and w=|<p>|.  Taking the cyclic
right difference removes gamma_D:

    M_{i+1}(D) - M_i(D) = w * (b_{i+1} - b_i).

Conversely, because p is not 7, these right-difference identities recover the
offsets explicitly by right averaging.  This gate checks the finite algebra in
a split toy field and prints the p24 counts.
"""

from __future__ import annotations

import random


FIELD_Q = 337
RIGHT_QUOTIENT = 7
RELATIVE_QUOTIENT = 8
TOY_W_ORDER = 29
SEED = 20260607
TRIALS = 96

P24_RELATIVE_W_ORDER = 388430
P24_RIGHT_QUOTIENT = 7
P24_RIGHT_NONTRIVIAL = 6
P24_RELATIVE_QUOTIENT = 8


Vector = list[int]
Matrix = list[list[int]]


def random_vector(rng: random.Random, length: int) -> Vector:
    return [rng.randrange(FIELD_Q) for _index in range(length)]


def random_matrix(rng: random.Random) -> Matrix:
    return [
        [rng.randrange(FIELD_Q) for _col in range(RELATIVE_QUOTIENT)]
        for _row in range(RIGHT_QUOTIENT)
    ]


def residual(matrix: Matrix, base: Vector) -> Matrix:
    return [
        [
            (matrix[row][col] - TOY_W_ORDER * base[row]) % FIELD_Q
            for col in range(RELATIVE_QUOTIENT)
        ]
        for row in range(RIGHT_QUOTIENT)
    ]


def affine_offsets(matrix: Matrix, base: Vector) -> bool:
    diff = residual(matrix, base)
    for col in range(RELATIVE_QUOTIENT):
        if any(diff[row][col] != diff[0][col] for row in range(1, RIGHT_QUOTIENT)):
            return False
    return True


def right_difference_identity(matrix: Matrix, base: Vector) -> bool:
    for row in range(RIGHT_QUOTIENT):
        next_row = (row + 1) % RIGHT_QUOTIENT
        base_delta = (TOY_W_ORDER * (base[next_row] - base[row])) % FIELD_Q
        for col in range(RELATIVE_QUOTIENT):
            matrix_delta = (matrix[next_row][col] - matrix[row][col]) % FIELD_Q
            if matrix_delta != base_delta:
                return False
    return True


def offsets_by_right_average(matrix: Matrix, base: Vector) -> Vector:
    diff = residual(matrix, base)
    inv7 = pow(RIGHT_QUOTIENT, -1, FIELD_Q)
    return [
        inv7 * sum(diff[row][col] for row in range(RIGHT_QUOTIENT)) % FIELD_Q
        for col in range(RELATIVE_QUOTIENT)
    ]


def average_reconstructs_affine(matrix: Matrix, base: Vector) -> bool:
    offsets = offsets_by_right_average(matrix, base)
    for row in range(RIGHT_QUOTIENT):
        for col in range(RELATIVE_QUOTIENT):
            if matrix[row][col] != (TOY_W_ORDER * base[row] + offsets[col]) % FIELD_Q:
                return False
    return True


def force_affine(rng: random.Random) -> tuple[Matrix, Vector]:
    base = random_vector(rng, RIGHT_QUOTIENT)
    offsets = random_vector(rng, RELATIVE_QUOTIENT)
    matrix = [
        [
            (TOY_W_ORDER * base[row] + offsets[col]) % FIELD_Q
            for col in range(RELATIVE_QUOTIENT)
        ]
        for row in range(RIGHT_QUOTIENT)
    ]
    return matrix, base


def force_column_sum_only(rng: random.Random) -> tuple[Matrix, Vector]:
    """Match the right-average offsets but fail at right differences."""
    matrix, base = force_affine(rng)
    col = rng.randrange(RELATIVE_QUOTIENT)
    row = rng.randrange(RIGHT_QUOTIENT)
    next_row = (row + 1) % RIGHT_QUOTIENT
    noise = rng.randrange(1, FIELD_Q)
    matrix[row][col] = (matrix[row][col] + noise) % FIELD_Q
    matrix[next_row][col] = (matrix[next_row][col] - noise) % FIELD_Q
    return matrix, base


def force_one_row_difference_defect(rng: random.Random) -> tuple[Matrix, Vector]:
    matrix, base = force_affine(rng)
    row = rng.randrange(RIGHT_QUOTIENT)
    col = rng.randrange(RELATIVE_QUOTIENT)
    matrix[row][col] = (matrix[row][col] + rng.randrange(1, FIELD_Q)) % FIELD_Q
    return matrix, base


def main() -> None:
    rng = random.Random(SEED)

    equivalence_failures = 0
    average_formula_failures = 0
    random_difference_true = 0
    forced_affine_difference_true = 0
    forced_affine_average_reconstructs = 0
    column_sum_only_difference_false = 0
    row_defect_difference_false = 0

    families: list[tuple[Matrix, Vector]] = []
    for _trial in range(TRIALS):
        families.append((random_matrix(rng), random_vector(rng, RIGHT_QUOTIENT)))
        families.append(force_affine(rng))
        families.append(force_column_sum_only(rng))
        families.append(force_one_row_difference_defect(rng))

    for matrix, base in families:
        affine = affine_offsets(matrix, base)
        difference = right_difference_identity(matrix, base)
        average = average_reconstructs_affine(matrix, base)
        equivalence_failures += int(not (affine == difference == average))
        if difference and not average:
            average_formula_failures += 1

    for _trial in range(TRIALS):
        matrix, base = random_matrix(rng), random_vector(rng, RIGHT_QUOTIENT)
        random_difference_true += int(right_difference_identity(matrix, base))

        matrix, base = force_affine(rng)
        forced_affine_difference_true += int(right_difference_identity(matrix, base))
        forced_affine_average_reconstructs += int(average_reconstructs_affine(matrix, base))

        matrix, base = force_column_sum_only(rng)
        column_sum_only_difference_false += int(not right_difference_identity(matrix, base))

        matrix, base = force_one_row_difference_defect(rng)
        row_defect_difference_false += int(not right_difference_identity(matrix, base))

    print("Trace-GCD fixed-frequency p24 right-difference affine gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_right_quotient={RIGHT_QUOTIENT}")
    print(f"toy_relative_quotient={RELATIVE_QUOTIENT}")
    print(f"toy_w_order={TOY_W_ORDER}")
    print(f"right_difference_equivalence_failures={equivalence_failures}")
    print(f"right_average_recovery_failures={average_formula_failures}")
    print(f"random_right_difference_true={random_difference_true}/{TRIALS}")
    print(f"forced_affine_right_difference_true={forced_affine_difference_true}/{TRIALS}")
    print(f"forced_affine_right_average_reconstructs={forced_affine_average_reconstructs}/{TRIALS}")
    print(f"column_sum_only_right_difference_false={column_sum_only_difference_false}/{TRIALS}")
    print(f"row_defect_right_difference_false={row_defect_difference_false}/{TRIALS}")
    print(f"p24_relative_w_order={P24_RELATIVE_W_ORDER}")
    print(f"p24_right_quotient={P24_RIGHT_QUOTIENT}")
    print(f"p24_relative_quotient={P24_RELATIVE_QUOTIENT}")
    print(f"p24_redundant_right_difference_equations={P24_RIGHT_QUOTIENT * P24_RELATIVE_QUOTIENT}")
    print(f"p24_independent_right_difference_equations={P24_RIGHT_NONTRIVIAL * P24_RELATIVE_QUOTIENT}")
    print("interpretation")
    print("  affine_profile_iff_right_difference_matches_selected_child=1")
    print("  offsets_recovered_by_right_average_when_differences_match=1")
    print("  column_sums_or_averages_alone_do_not_force_right_difference=1")
    print("  arithmetic_target_can_be_stated_without_characters_or_offsets=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_gate")

    if equivalence_failures:
        raise SystemExit(1)
    if average_formula_failures:
        raise SystemExit(1)
    if random_difference_true:
        raise SystemExit(1)
    if forced_affine_difference_true != TRIALS:
        raise SystemExit(1)
    if forced_affine_average_reconstructs != TRIALS:
        raise SystemExit(1)
    if column_sum_only_difference_false != TRIALS:
        raise SystemExit(1)
    if row_defect_difference_false != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
