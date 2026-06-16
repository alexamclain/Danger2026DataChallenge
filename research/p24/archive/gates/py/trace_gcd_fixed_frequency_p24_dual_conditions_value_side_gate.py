#!/usr/bin/env python3
"""Value-side form of the p24 admissible Jacobi dual conditions.

The four Fourier families are useful for the verifier pipeline, but an
arithmetic CM/Lang proof is more likely to see value-side packet identities.
For functions f on C_7 x C_c, with c odd, the dual Fourier system with
lambda_c=-2/(c-1) is equivalent to three value-side conditions:

1. C-row sums are independent of the right coordinate;
2. f vanishes on the C-zero fiber;
3. off the C-zero fiber, f(x)+f(-x) is one global constant.

This gate checks the equivalence in small exact models and confirms every
admissible C-axis Jacobi carry satisfies the value-side identities.
"""

from __future__ import annotations

import random

from trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate import (
    condition_rows,
)
from trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary import dft_rows
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    admissible_c_axis_carry_rows,
    rank_mod,
    split_prime_for,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate import lambda_formula


TRIALS = 24
SEED = 20260607


def dual_conditions_hold(row: list[int], c_degree: int, field_q: int) -> bool:
    dft = dft_rows([row], c_degree, field_q)[0]
    conditions = condition_rows(c_degree, field_q, lambda_formula(c_degree, field_q))
    return all(
        sum(value * coeff for value, coeff in zip(dft, condition)) % field_q == 0
        for condition in conditions
    )


def c_row_sums_independent(row: list[int], c_degree: int, field_q: int) -> bool:
    row_sums = [
        sum(row[right * c_degree : (right + 1) * c_degree]) % field_q
        for right in range(RIGHT_DEGREE)
    ]
    return all(value == row_sums[0] for value in row_sums)


def c_zero_fiber_vanishes(row: list[int], c_degree: int, field_q: int) -> bool:
    return all(row[right * c_degree] % field_q == 0 for right in range(RIGHT_DEGREE))


def inversion_constant_off_c_zero(row: list[int], c_degree: int, field_q: int) -> bool:
    constant: int | None = None
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            value = (
                row[right * c_degree + c_index]
                + row[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
            ) % field_q
            if constant is None:
                constant = value
            elif value != constant:
                return False
    return constant is not None


def value_conditions_hold(row: list[int], c_degree: int, field_q: int) -> bool:
    return (
        c_row_sums_independent(row, c_degree, field_q)
        and c_zero_fiber_vanishes(row, c_degree, field_q)
        and inversion_constant_off_c_zero(row, c_degree, field_q)
    )


def value_condition_rows(c_degree: int, field_q: int) -> list[list[int]]:
    width = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []

    def row_with(entries: list[tuple[int, int]]) -> list[int]:
        row = [0] * width
        for column, value in entries:
            row[column] = (row[column] + value) % field_q
        return row

    # 1. C-row sums equal the row-0 sum.
    for right in range(1, RIGHT_DEGREE):
        entries: list[tuple[int, int]] = []
        for c_index in range(c_degree):
            entries.append((right * c_degree + c_index, 1))
            entries.append((c_index, -1))
        rows.append(row_with(entries))

    # 2. C-zero fiber vanishes.
    for right in range(RIGHT_DEGREE):
        rows.append(row_with([(right * c_degree, 1)]))

    # 3. Off C-zero inversion sums are constant.  Compare every entry to (0,1).
    base_entries = [
        (1, 1),
        (((-0) % RIGHT_DEGREE) * c_degree + ((-1) % c_degree), 1),
    ]
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            if right == 0 and c_index == 1:
                continue
            entries = [
                (right * c_degree + c_index, 1),
                (((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree), 1),
            ]
            for column, value in base_entries:
                entries.append((column, -value))
            rows.append(row_with(entries))

    return rows


def random_row(width: int, field_q: int, rng: random.Random) -> list[int]:
    return [rng.randrange(field_q) for _ in range(width)]


def main() -> None:
    rng = random.Random(SEED)
    equivalence_rows = 0
    rank_rows = 0
    carry_rows = 0
    random_controls = 0
    rows_checked = 0

    print("Trace-GCD fixed-frequency p24 dual-conditions value-side gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES[:3]:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        width = RIGHT_DEGREE * c_degree
        dual_condition_matrix = condition_rows(
            c_degree, field_q, lambda_formula(c_degree, field_q)
        )
        value_condition_matrix = value_condition_rows(c_degree, field_q)
        dual_rank = rank_mod(dual_condition_matrix, field_q)
        value_rank = rank_mod(value_condition_matrix, field_q)
        expected_rank = 6 + 6 * ((c_degree - 1) // 2) + ((c_degree - 1) // 2) + 3
        rank_match = int(dual_rank == value_rank == expected_rank)

        carries = admissible_c_axis_carry_rows(c_degree, field_q)
        carry_value_ok = sum(
            int(value_conditions_hold(row, c_degree, field_q)) for row in carries
        )
        carry_dual_ok = sum(
            int(dual_conditions_hold(row, c_degree, field_q)) for row in carries
        )
        carry_match = int(carry_value_ok == len(carries) and carry_dual_ok == len(carries))

        equivalence_trials = 0
        random_dual_hits = 0
        random_value_hits = 0
        for _ in range(TRIALS):
            row = random_row(width, field_q, rng)
            dual = dual_conditions_hold(row, c_degree, field_q)
            value = value_conditions_hold(row, c_degree, field_q)
            equivalence_trials += int(dual == value)
            random_dual_hits += int(dual)
            random_value_hits += int(value)
        equivalence_match = int(equivalence_trials == TRIALS)
        random_control_match = int(random_dual_hits == 0 and random_value_hits == 0)

        equivalence_rows += equivalence_match
        rank_rows += rank_match
        carry_rows += carry_match
        random_controls += random_control_match
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"dual_rank={dual_rank} value_rank={value_rank} "
            f"expected_rank={expected_rank} "
            f"rank_match={rank_match} "
            f"admissible_carry_value_conditions={carry_value_ok}/{len(carries)} "
            f"admissible_carry_dual_conditions={carry_dual_ok}/{len(carries)} "
            f"carry_match={carry_match} "
            f"random_equivalence_trials={equivalence_trials}/{TRIALS} "
            f"random_dual_hits={random_dual_hits}/{TRIALS} "
            f"random_value_hits={random_value_hits}/{TRIALS} "
            f"random_control_match={random_control_match}"
        )

    print(f"value_dual_equivalence_random_checks={equivalence_rows}/{rows_checked}")
    print(f"value_dual_rank_matches={rank_rows}/{rows_checked}")
    print(f"admissible_carries_satisfy_value_conditions={carry_rows}/{rows_checked}")
    print(f"random_controls_reject_both={random_controls}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("interpretation")
    print("  four_dual_fourier_families_equal_three_value_side_packet_identities=1")
    print("  value_identity_1_C_row_sums_independent=1")
    print("  value_identity_2_C_zero_fiber_vanishes=1")
    print("  value_identity_3_inversion_complement_constant_off_C_zero=1")
    print("  selected_packet_proof_can_target_value_side_identities=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate")

    if equivalence_rows != rows_checked:
        raise SystemExit(1)
    if rank_rows != rows_checked:
        raise SystemExit(1)
    if carry_rows != rows_checked:
        raise SystemExit(1)
    if random_controls != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
