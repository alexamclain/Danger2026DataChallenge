#!/usr/bin/env python3
"""Repackage the p24 48-equation target as an affine quotient-profile identity.

For each nonzero relative <p>-coset D, let M[:,D] be its seven right
H=<2^7>-coset sums, and let b be the selected-child right H-profile.  The
recombined p24 target says that every nontrivial right order-7 character sees

    M[:,D] = |<p>| * b

for all eight relative cosets.  Equivalently,

    M[i,D] = |<p>| * b[i] + gamma_D

for some column offsets gamma_D independent of the right H-coset i.

This script checks, in a split toy field with 7th and 8th roots of unity, that
this affine section identity is equivalent to the older mixed-spectrum plus
anchor split:

    42 mixed C_7 x C_8 equations + 6 anchors.
"""

from __future__ import annotations

import random


FIELD_Q = 337  # 337 - 1 is divisible by 7 and 8.
RIGHT_QUOTIENT = 7
RELATIVE_QUOTIENT = 8
TOY_W_ORDER = 29
SEED = 20260607
TRIALS = 96

P24_RELATIVE_W_ORDER = 388430
P24_RIGHT_NONTRIVIAL = 6
P24_RELATIVE_QUOTIENT = 8


Vector = list[int]
Matrix = list[list[int]]


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root_mod_prime(modulus: int) -> int:
    factors = factor_distinct(modulus - 1)
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def root_of_order(order: int) -> int:
    generator = primitive_root_mod_prime(FIELD_Q)
    root = pow(generator, (FIELD_Q - 1) // order, FIELD_Q)
    if root == 1 or pow(root, order, FIELD_Q) != 1:
        raise RuntimeError("bad root")
    return root


def random_vector(rng: random.Random, length: int) -> Vector:
    return [rng.randrange(FIELD_Q) for _index in range(length)]


def random_matrix(rng: random.Random) -> Matrix:
    return [
        [rng.randrange(FIELD_Q) for _col in range(RELATIVE_QUOTIENT)]
        for _row in range(RIGHT_QUOTIENT)
    ]


def row_projection(values: Vector, zeta7: int, character: int) -> int:
    total = 0
    for row, value in enumerate(values):
        total = (
            total
            + pow(zeta7, (-character * row) % RIGHT_QUOTIENT, FIELD_Q) * value
        ) % FIELD_Q
    return total


def mixed_projection(matrix: Matrix, zeta7: int, zeta8: int, right_char: int, rel_char: int) -> int:
    total = 0
    for row in range(RIGHT_QUOTIENT):
        row_weight = pow(zeta7, (-right_char * row) % RIGHT_QUOTIENT, FIELD_Q)
        for col in range(RELATIVE_QUOTIENT):
            col_weight = pow(zeta8, (-rel_char * col) % RELATIVE_QUOTIENT, FIELD_Q)
            total = (total + row_weight * col_weight * matrix[row][col]) % FIELD_Q
    return total


def direct_recombined_payload(matrix: Matrix, base: Vector, zeta7: int) -> bool:
    for col in range(RELATIVE_QUOTIENT):
        diff = [
            (matrix[row][col] - TOY_W_ORDER * base[row]) % FIELD_Q
            for row in range(RIGHT_QUOTIENT)
        ]
        for right_char in range(1, RIGHT_QUOTIENT):
            if row_projection(diff, zeta7, right_char):
                return False
    return True


def affine_section_profile(matrix: Matrix, base: Vector) -> bool:
    for col in range(RELATIVE_QUOTIENT):
        diff = [
            (matrix[row][col] - TOY_W_ORDER * base[row]) % FIELD_Q
            for row in range(RIGHT_QUOTIENT)
        ]
        if any(value != diff[0] for value in diff[1:]):
            return False
    return True


def mixed_spectrum_zero(matrix: Matrix, zeta7: int, zeta8: int) -> bool:
    for right_char in range(1, RIGHT_QUOTIENT):
        for rel_char in range(1, RELATIVE_QUOTIENT):
            if mixed_projection(matrix, zeta7, zeta8, right_char, rel_char):
                return False
    return True


def anchor_zero(matrix: Matrix, base: Vector, zeta7: int) -> bool:
    defect = [
        (
            sum(matrix[row])
            - RELATIVE_QUOTIENT * TOY_W_ORDER * base[row]
        )
        % FIELD_Q
        for row in range(RIGHT_QUOTIENT)
    ]
    for right_char in range(1, RIGHT_QUOTIENT):
        if row_projection(defect, zeta7, right_char):
            return False
    return True


def mixed_plus_anchor(matrix: Matrix, base: Vector, zeta7: int, zeta8: int) -> bool:
    return mixed_spectrum_zero(matrix, zeta7, zeta8) and anchor_zero(matrix, base, zeta7)


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


def force_mixed_only(rng: random.Random) -> tuple[Matrix, Vector]:
    """No mixed interaction, but the row effect is not tied to the base."""
    row_effect = random_vector(rng, RIGHT_QUOTIENT)
    offsets = random_vector(rng, RELATIVE_QUOTIENT)
    base = random_vector(rng, RIGHT_QUOTIENT)
    matrix = [
        [
            (row_effect[row] + offsets[col]) % FIELD_Q
            for col in range(RELATIVE_QUOTIENT)
        ]
        for row in range(RIGHT_QUOTIENT)
    ]
    return matrix, base


def force_anchor_only(rng: random.Random) -> tuple[Matrix, Vector]:
    """Make the anchor true while leaving generic mixed spectrum."""
    base = random_vector(rng, RIGHT_QUOTIENT)
    common_defect = rng.randrange(FIELD_Q)
    matrix = [
        [rng.randrange(FIELD_Q) for _col in range(RELATIVE_QUOTIENT)]
        for _row in range(RIGHT_QUOTIENT)
    ]
    for row in range(RIGHT_QUOTIENT):
        target_sum = (
            RELATIVE_QUOTIENT * TOY_W_ORDER * base[row] + common_defect
        ) % FIELD_Q
        running = sum(matrix[row][:-1]) % FIELD_Q
        matrix[row][-1] = (target_sum - running) % FIELD_Q
    return matrix, base


def main() -> None:
    rng = random.Random(SEED)
    zeta7 = root_of_order(RIGHT_QUOTIENT)
    zeta8 = root_of_order(RELATIVE_QUOTIENT)

    equivalence_failures = 0
    random_direct_true = 0
    forced_affine_direct_true = 0
    forced_affine_mixed_anchor_true = 0
    mixed_only_anchor_false = 0
    mixed_only_direct_false = 0
    anchor_only_mixed_false = 0
    anchor_only_direct_false = 0

    families: list[tuple[Matrix, Vector]] = []
    for _trial in range(TRIALS):
        families.append((random_matrix(rng), random_vector(rng, RIGHT_QUOTIENT)))
        families.append(force_affine(rng))
        families.append(force_mixed_only(rng))
        families.append(force_anchor_only(rng))

    for matrix, base in families:
        direct = direct_recombined_payload(matrix, base, zeta7)
        affine = affine_section_profile(matrix, base)
        split = mixed_plus_anchor(matrix, base, zeta7, zeta8)
        equivalence_failures += int(not (direct == affine == split))

    for _trial in range(TRIALS):
        matrix, base = random_matrix(rng), random_vector(rng, RIGHT_QUOTIENT)
        random_direct_true += int(direct_recombined_payload(matrix, base, zeta7))

        matrix, base = force_affine(rng)
        forced_affine_direct_true += int(direct_recombined_payload(matrix, base, zeta7))
        forced_affine_mixed_anchor_true += int(mixed_plus_anchor(matrix, base, zeta7, zeta8))

        matrix, base = force_mixed_only(rng)
        mixed_only_anchor_false += int(
            mixed_spectrum_zero(matrix, zeta7, zeta8)
            and not anchor_zero(matrix, base, zeta7)
        )
        mixed_only_direct_false += int(not direct_recombined_payload(matrix, base, zeta7))

        matrix, base = force_anchor_only(rng)
        anchor_only_mixed_false += int(
            anchor_zero(matrix, base, zeta7)
            and not mixed_spectrum_zero(matrix, zeta7, zeta8)
        )
        anchor_only_direct_false += int(not direct_recombined_payload(matrix, base, zeta7))

    print("Trace-GCD fixed-frequency p24 affine quotient-profile gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_right_quotient={RIGHT_QUOTIENT}")
    print(f"toy_relative_quotient={RELATIVE_QUOTIENT}")
    print(f"toy_w_order={TOY_W_ORDER}")
    print(f"affine_equivalence_failures={equivalence_failures}")
    print(f"random_direct_payload_true={random_direct_true}/{TRIALS}")
    print(f"forced_affine_direct_payload_true={forced_affine_direct_true}/{TRIALS}")
    print(f"forced_affine_mixed_plus_anchor_true={forced_affine_mixed_anchor_true}/{TRIALS}")
    print(f"mixed_only_anchor_false={mixed_only_anchor_false}/{TRIALS}")
    print(f"mixed_only_direct_payload_false={mixed_only_direct_false}/{TRIALS}")
    print(f"anchor_only_mixed_false={anchor_only_mixed_false}/{TRIALS}")
    print(f"anchor_only_direct_payload_false={anchor_only_direct_false}/{TRIALS}")
    print(f"p24_relative_w_order={P24_RELATIVE_W_ORDER}")
    print(f"p24_right_nontrivial_characters={P24_RIGHT_NONTRIVIAL}")
    print(f"p24_relative_quotient={P24_RELATIVE_QUOTIENT}")
    print(f"p24_affine_direct_equations={P24_RIGHT_NONTRIVIAL * P24_RELATIVE_QUOTIENT}")
    print(f"p24_mixed_equations={P24_RIGHT_NONTRIVIAL * (P24_RELATIVE_QUOTIENT - 1)}")
    print(f"p24_anchor_equations={P24_RIGHT_NONTRIVIAL}")
    print("interpretation")
    print("  direct_48_payload_iff_affine_right_profile_decomposition=1")
    print("  direct_48_payload_iff_mixed_spectrum_plus_anchor=1")
    print("  mixed_zero_without_anchor_does_not_tie_profiles_to_selected_child=1")
    print("  anchor_without_mixed_zero_does_not_remove_row_column_interaction=1")
    print("  arithmetic_target_is_column_offsets_independent_of_right_H_coset=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_affine_profile_gate")

    if equivalence_failures:
        raise SystemExit(1)
    if random_direct_true:
        raise SystemExit(1)
    if forced_affine_direct_true != TRIALS:
        raise SystemExit(1)
    if forced_affine_mixed_anchor_true != TRIALS:
        raise SystemExit(1)
    if mixed_only_anchor_false != TRIALS or mixed_only_direct_false != TRIALS:
        raise SystemExit(1)
    if anchor_only_mixed_false != TRIALS or anchor_only_direct_false != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
