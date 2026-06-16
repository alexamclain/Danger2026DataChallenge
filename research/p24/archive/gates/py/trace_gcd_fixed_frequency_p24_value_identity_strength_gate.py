#!/usr/bin/env python3
"""Strength accounting for the value-side admissible-packet identities.

The verifier only needs C-row sums independent of the right coordinate
(`final internal trace zero`).  The admissible-Jacobi proof target adds two
structural value-side identities:

  Z: f(r,0)=0 on the C-zero fiber;
  I: f(r,c)+f(-r,-c) is constant for c != 0.

This gate computes how these identities interact.  The useful finding is:
Z+I already has the "pair compatibility" shape, and only three independent
row-sum/global-balance equations remain to reach the full rank-621 admissible
target.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate import (
    RIGHT_DEGREE,
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    lambda_formula,
    value_condition_rows,
)
from trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate import (
    condition_rows,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    rank_mod,
    split_prime_for,
)


def row_sum_condition_rows(c_degree: int, field_q: int) -> list[list[int]]:
    width = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []
    for right in range(1, RIGHT_DEGREE):
        row = [0] * width
        for c_index in range(c_degree):
            row[right * c_degree + c_index] = 1
            row[c_index] = (row[c_index] - 1) % field_q
        rows.append(row)
    return rows


def c_zero_condition_rows(c_degree: int, field_q: int) -> list[list[int]]:
    width = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []
    for right in range(RIGHT_DEGREE):
        row = [0] * width
        row[right * c_degree] = 1
        rows.append(row)
    return rows


def inversion_constant_condition_rows(c_degree: int, field_q: int) -> list[list[int]]:
    width = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []
    base_columns = [1, c_degree - 1]
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            if right == 0 and c_index == 1:
                continue
            row = [0] * width
            row[right * c_degree + c_index] = 1
            row[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)] = (
                row[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
                + 1
            ) % field_q
            for column in base_columns:
                row[column] = (row[column] - 1) % field_q
            rows.append(row)
    return rows


def expected_pair_count(c_degree: int) -> int:
    return (c_degree - 1) // 2


def main() -> None:
    rows_checked = 0
    all_rank_matches = 0

    print("Trace-GCD fixed-frequency p24 value-identity strength gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES[:3]:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        ambient_dim = RIGHT_DEGREE * c_degree
        pair_count = expected_pair_count(c_degree)
        row_rows = row_sum_condition_rows(c_degree, field_q)
        zero_rows = c_zero_condition_rows(c_degree, field_q)
        inversion_rows = inversion_constant_condition_rows(c_degree, field_q)
        full_value_rows = value_condition_rows(c_degree, field_q)
        dual_rows = condition_rows(c_degree, field_q, lambda_formula(c_degree, field_q))

        row_rank = rank_mod(row_rows, field_q)
        zero_rank = rank_mod(zero_rows, field_q)
        inversion_rank = rank_mod(inversion_rows, field_q)
        zero_inversion_rank = rank_mod(zero_rows + inversion_rows, field_q)
        full_value_rank = rank_mod(full_value_rows, field_q)
        dual_rank = rank_mod(dual_rows, field_q)
        row_extra_after_zero_inversion = full_value_rank - zero_inversion_rank

        expected_zero_inversion_rank = RIGHT_DEGREE * pair_count + 6
        expected_full_rank = RIGHT_DEGREE * pair_count + 9
        expected_solution_dim = ambient_dim - expected_full_rank
        rank_match = int(
            row_rank == 6
            and zero_rank == 7
            and inversion_rank == RIGHT_DEGREE * pair_count - 1
            and zero_inversion_rank == expected_zero_inversion_rank
            and full_value_rank == dual_rank == expected_full_rank
            and row_extra_after_zero_inversion == 3
            and expected_solution_dim == RIGHT_DEGREE * pair_count - 2
        )
        all_rank_matches += rank_match
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"ambient_dim={ambient_dim} "
            f"pair_count={pair_count} "
            f"row_sum_rank={row_rank} "
            f"c_zero_rank={zero_rank} "
            f"inversion_constant_rank={inversion_rank} "
            f"zero_plus_inversion_rank={zero_inversion_rank} "
            f"expected_zero_plus_inversion_rank={expected_zero_inversion_rank} "
            f"full_value_rank={full_value_rank} "
            f"dual_rank={dual_rank} "
            f"expected_full_rank={expected_full_rank} "
            f"row_extra_after_zero_inversion={row_extra_after_zero_inversion} "
            f"expected_solution_dim={expected_solution_dim} "
            f"rank_match={rank_match}"
        )

    p24_pair_count = expected_pair_count(P24_C_DEGREE)
    p24_zero_inversion_rank = RIGHT_DEGREE * p24_pair_count + 6
    p24_full_rank = RIGHT_DEGREE * p24_pair_count + 9
    p24_solution_dim = RIGHT_DEGREE * P24_C_DEGREE - p24_full_rank
    print(f"rank_matches={all_rank_matches}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print(f"p24_pair_count={p24_pair_count}")
    print(f"p24_zero_plus_inversion_rank=7*89+6={p24_zero_inversion_rank}")
    print(f"p24_full_value_rank=7*89+9={p24_full_rank}")
    print(f"p24_row_sum_extra_after_zero_plus_inversion=3")
    print(f"p24_value_solution_dim=1253-632={p24_solution_dim}")
    print("interpretation")
    print("  verifier_minimal_row_sum_identity_has_rank_6=1")
    print("  c_zero_plus_inversion_constant_leave_three_global_balances=1")
    print("  value_side_identities_are_stronger_than_verifier_minimal_trace_zero=1")
    print("  arithmetic_proof_can_split_into_structural_symmetry_plus_three_balances=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_value_identity_strength_gate")

    if all_rank_matches != rows_checked:
        raise SystemExit(1)
    if p24_zero_inversion_rank != 629:
        raise SystemExit(1)
    if p24_full_rank != 632:
        raise SystemExit(1)
    if p24_solution_dim != 621:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
