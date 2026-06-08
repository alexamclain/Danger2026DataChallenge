#!/usr/bin/env python3
"""Dual Fourier conditions for the admissible C-axis Jacobi-carry span.

The spectral boundary showed that the p24 admissible Jacobi target has rank

    621 = 1 + 7*88 + 4.

This gate turns that rank statement into explicit equations.  In small exact
models C_7 x C_c, the admissible carry span is exactly the solution space of
four Fourier condition families:

1. C-trivial/right-nontrivial coefficients vanish;
2. nontrivial right coefficients are skew under (a,b) -> (-a,-b);
3. right-trivial conjugate C-pair sums are tied to the global constant
   coefficient by one normalization scalar lambda_c;
4. three global balances over positive C representatives:
      sum_b (F(-a,b) - F(a,b)) = 0,  a=1,2,3.

The scalar lambda_c depends on the chosen Fourier root normalization.  The
condition is intrinsic once that normalization is fixed.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary import dft_rows
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    admissible_c_axis_carry_rows,
    rank_mod,
    split_prime_for,
)


SMALL_C_DEGREES = [5, 11, 13]
P24_C_DEGREE = 179


def coord(c_degree: int, right_character: int, c_character: int) -> int:
    return (right_character % RIGHT_DEGREE) * c_degree + (c_character % c_degree)


def derive_pair_sum_lambda(dft: list[list[int]], c_degree: int, field_q: int) -> int:
    for row in dft:
        global_constant = row[coord(c_degree, 0, 0)] % field_q
        if global_constant:
            pair_sum = (
                row[coord(c_degree, 0, 1)]
                + row[coord(c_degree, 0, -1)]
            ) % field_q
            return pair_sum * pow(global_constant, -1, field_q) % field_q
    raise RuntimeError("no row with nonzero global constant found")


def condition_rows(c_degree: int, field_q: int, pair_sum_lambda: int) -> list[list[int]]:
    rows: list[list[int]] = []
    width = RIGHT_DEGREE * c_degree
    positive_c = range(1, (c_degree + 1) // 2)

    def row_with(entries: list[tuple[int, int]]) -> list[int]:
        row = [0] * width
        for column, value in entries:
            row[column] = (row[column] + value) % field_q
        return row

    # 1. C-trivial/right-nontrivial coefficients vanish.
    for right_character in range(1, RIGHT_DEGREE):
        rows.append(row_with([(coord(c_degree, right_character, 0), 1)]))

    # 2. Nontrivial right coefficients are skew across conjugate C pairs.
    for c_character in positive_c:
        for right_character in range(1, RIGHT_DEGREE):
            rows.append(
                row_with(
                    [
                        (coord(c_degree, right_character, c_character), 1),
                        (coord(c_degree, -right_character, -c_character), 1),
                    ]
                )
            )

    # 3. Right-trivial conjugate C-pair sums share the same constant part.
    for c_character in positive_c:
        rows.append(
            row_with(
                [
                    (coord(c_degree, 0, c_character), 1),
                    (coord(c_degree, 0, -c_character), 1),
                    (coord(c_degree, 0, 0), -pair_sum_lambda),
                ]
            )
        )

    # 4. The three global right-pair balances.
    for right_character in range(1, (RIGHT_DEGREE + 1) // 2):
        entries: list[tuple[int, int]] = []
        for c_character in positive_c:
            entries.append((coord(c_degree, -right_character, c_character), 1))
            entries.append((coord(c_degree, right_character, c_character), -1))
        rows.append(row_with(entries))

    return rows


def row_satisfies_conditions(
    row: list[int], conditions: list[list[int]], field_q: int
) -> bool:
    return all(
        sum(value * coeff for value, coeff in zip(row, condition)) % field_q == 0
        for condition in conditions
    )


def expected_constraint_count(c_degree: int) -> int:
    pair_count = (c_degree - 1) // 2
    return 6 + 6 * pair_count + pair_count + 3


def expected_solution_dimension(c_degree: int) -> int:
    return RIGHT_DEGREE * c_degree - expected_constraint_count(c_degree)


def main() -> None:
    all_rows_match = 0

    print("Trace-GCD fixed-frequency p24 admissible Jacobi dual-conditions gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        rows = admissible_c_axis_carry_rows(c_degree, field_q)
        dft = dft_rows(rows, c_degree, field_q)
        pair_sum_lambda = derive_pair_sum_lambda(dft, c_degree, field_q)
        conditions = condition_rows(c_degree, field_q, pair_sum_lambda)
        admissible_rank = rank_mod(dft, field_q)
        condition_rank = rank_mod(conditions, field_q)
        solution_dim = RIGHT_DEGREE * c_degree - condition_rank
        expected_conditions = expected_constraint_count(c_degree)
        expected_dim = expected_solution_dimension(c_degree)
        rows_satisfy = sum(
            int(row_satisfies_conditions(row, conditions, field_q))
            for row in dft
        )
        match = int(
            rows_satisfy == len(dft)
            and len(conditions) == expected_conditions
            and condition_rank == expected_conditions
            and solution_dim == admissible_rank
            and solution_dim == expected_dim
        )
        all_rows_match += match
        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"pair_sum_lambda={pair_sum_lambda} "
            f"admissible_rank={admissible_rank} "
            f"condition_count={len(conditions)} "
            f"condition_rank={condition_rank} "
            f"solution_dim={solution_dim} "
            f"expected_solution_dim={expected_dim} "
            f"rows_satisfying_conditions={rows_satisfy}/{len(dft)} "
            f"dual_condition_match={match}"
        )

    p24_pair_count = (P24_C_DEGREE - 1) // 2
    p24_condition_count = expected_constraint_count(P24_C_DEGREE)
    p24_solution_dim = expected_solution_dimension(P24_C_DEGREE)
    print(f"dual_condition_matches={all_rows_match}/{len(SMALL_C_DEGREES)}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print(f"p24_conjugate_C_pair_count={p24_pair_count}")
    print(f"p24_dual_condition_count=6+6*89+89+3={p24_condition_count}")
    print(f"p24_dual_solution_dim=1253-632={p24_solution_dim}")
    print("interpretation")
    print("  admissible_span_equals_explicit_four_family_fourier_conditions=1")
    print("  pair_skew_conditions_are_F_a_b_plus_F_minus_a_minus_b_zero=1")
    print("  three_global_balances_are_sum_b_F_minus_a_b_minus_F_a_b_zero=1")
    print("  p24_membership_target_is_explicit_632_equation_fourier_system=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate")

    if all_rows_match != len(SMALL_C_DEGREES):
        raise SystemExit(1)
    if p24_condition_count != 632:
        raise SystemExit(1)
    if p24_solution_dim != 621:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
