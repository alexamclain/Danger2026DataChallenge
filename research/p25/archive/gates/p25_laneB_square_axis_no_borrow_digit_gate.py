#!/usr/bin/env python3
"""Square-axis no-borrow digit gate for p25 Lane B.

The digit-selector gate shows that the square-axis residual classes are
selected by a base-43 digit rule.  This gate records the tiny carry mechanism
inside that rule.

Write q = 43*m + 9*t with

    m = 4*s + h + 1,  h,t in {0,1,2}.

Then the selector is exactly the no-borrow predicate for h - t:

    selected(h,t) = 1 - floor((t + 2 - h)/3).

This is a compact carry/no-borrow normal form, but not a separable or
low-degree polynomial shortcut in the digit variables: the 3x3 selector has
rank 3, nonzero mixed second difference, and its exact interpolation requires
total degree 4 / bidegree (2,2).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from p25_laneB_divisor_footprint_gate import rank_mod
from p25_laneB_square_axis_digit_selector_gate import (
    BASE_DIGIT,
    ODD_RANK_FIELD,
    digit_rule,
    residual_q_values,
)


@dataclass(frozen=True)
class PolynomialProfile:
    total_degree_min: int
    bidegree_min: tuple[int, int]
    coefficients: tuple[tuple[int, int, Fraction], ...]


def selector_matrix() -> list[list[int]]:
    return [[int(t_value <= h_value) for t_value in range(3)] for h_value in range(3)]


def borrow_matrix() -> list[list[int]]:
    return [
        [(t_value + 2 - h_value) // 3 for t_value in range(3)]
        for h_value in range(3)
    ]


def mixed_second_differences(matrix: list[list[int]]) -> list[int]:
    return [
        matrix[h][t] - matrix[h][0] - matrix[0][t] + matrix[0][0]
        for h in range(1, 3)
        for t in range(1, 3)
    ]


def solve_interpolation(
    monomials: list[tuple[int, int]], values: list[list[int]]
) -> tuple[bool, tuple[Fraction, ...]]:
    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []
    for h_value in range(3):
        for t_value in range(3):
            rows.append(
                [
                    Fraction(h_value) ** h_power * Fraction(t_value) ** t_power
                    for h_power, t_power in monomials
                ]
            )
            rhs.append(Fraction(values[h_value][t_value]))

    augmented = [row + [target] for row, target in zip(rows, rhs)]
    row_count = len(augmented)
    col_count = len(monomials)
    rank = 0
    pivots: list[int] = []
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if augmented[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inverse = augmented[rank][col]
        augmented[rank] = [value / inverse for value in augmented[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            factor = augmented[row][col]
            if factor:
                augmented[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[rank])
                ]
        pivots.append(col)
        rank += 1

    consistent = all(
        any(row[:col_count]) or not row[col_count]
        for row in augmented[rank:]
    )
    if not consistent:
        return False, tuple()
    coefficients = [Fraction(0) for _ in monomials]
    for row, col in enumerate(pivots):
        coefficients[col] = augmented[row][col_count]
    return True, tuple(coefficients)


def polynomial_profile() -> PolynomialProfile:
    matrix = selector_matrix()
    total_degree_min = -1
    final_monomials: list[tuple[int, int]] = []
    final_coefficients: tuple[Fraction, ...] = tuple()
    for total_degree in range(5):
        monomials = [
            (h_power, t_power)
            for h_power in range(3)
            for t_power in range(3)
            if h_power + t_power <= total_degree
        ]
        ok, coefficients = solve_interpolation(monomials, matrix)
        if ok:
            total_degree_min = total_degree
            final_monomials = monomials
            final_coefficients = coefficients
            break
    if total_degree_min < 0:
        raise AssertionError("no interpolation found")

    bidegree_min = (-1, -1)
    for h_degree in range(3):
        for t_degree in range(3):
            monomials = [
                (h_power, t_power)
                for h_power in range(h_degree + 1)
                for t_power in range(t_degree + 1)
            ]
            ok, _coefficients = solve_interpolation(monomials, matrix)
            if ok:
                bidegree_min = (h_degree, t_degree)
                break
        if bidegree_min != (-1, -1):
            break
    nonzero_coefficients = tuple(
        (h_power, t_power, coefficient)
        for (h_power, t_power), coefficient in zip(final_monomials, final_coefficients)
        if coefficient
    )
    return PolynomialProfile(
        total_degree_min=total_degree_min,
        bidegree_min=bidegree_min,
        coefficients=nonzero_coefficients,
    )


def main() -> int:
    print("p25 Lane B square-axis no-borrow digit gate")
    print(f"base_digit={BASE_DIGIT}")
    selector = selector_matrix()
    borrow = borrow_matrix()
    q_values = residual_q_values()
    no_borrow_q_values = sorted(
        BASE_DIGIT * (4 * s_value + h_value + 1) + 9 * t_value
        for s_value in range(3)
        for h_value in range(3)
        for t_value in range(3)
        if selector[h_value][t_value]
    )
    digit_rule_q_values = [q_value for q_value in range(507) if digit_rule(q_value)]
    no_borrow_hits = sum(
        int(selector[h_value][t_value] == 1 - borrow[h_value][t_value])
        for h_value in range(3)
        for t_value in range(3)
    )
    selector_rank_f2 = rank_mod(selector, 2)
    selector_rank_odd = rank_mod(selector, ODD_RANK_FIELD)
    borrow_rank_f2 = rank_mod(borrow, 2)
    borrow_rank_odd = rank_mod(borrow, ODD_RANK_FIELD)
    mixed_differences = mixed_second_differences(selector)
    profile = polynomial_profile()
    expected_coefficients = (
        (0, 0, Fraction(1, 1)),
        (0, 1, Fraction(-3, 2)),
        (0, 2, Fraction(1, 2)),
        (1, 1, Fraction(13, 4)),
        (1, 2, Fraction(-7, 4)),
        (2, 1, Fraction(-5, 4)),
        (2, 2, Fraction(3, 4)),
    )
    row_ok = (
        no_borrow_hits == 9
        and q_values == no_borrow_q_values == digit_rule_q_values
        and selector == [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
        and borrow == [[0, 1, 1], [0, 0, 1], [0, 0, 0]]
        and selector_rank_f2 == 3
        and selector_rank_odd == 3
        and borrow_rank_f2 == 2
        and borrow_rank_odd == 2
        and mixed_differences == [1, 0, 1, 1]
        and profile.total_degree_min == 4
        and profile.bidegree_min == (2, 2)
        and profile.coefficients == expected_coefficients
    )
    print(
        f"no_borrow_selector: "
        f"no_borrow_hits={no_borrow_hits}/9 "
        f"q_count={len(q_values)}/18 "
        f"selector_matrix={selector} "
        f"borrow_matrix={borrow} "
        f"selector_rank_f2={selector_rank_f2} "
        f"selector_rank_odd={selector_rank_odd} "
        f"borrow_rank_f2={borrow_rank_f2} "
        f"borrow_rank_odd={borrow_rank_odd} "
        f"mixed_second_differences={mixed_differences} "
        f"total_degree_min={profile.total_degree_min} "
        f"bidegree_min={profile.bidegree_min} "
        f"ok={int(row_ok)}"
    )
    print("polynomial_normal_form")
    for h_power, t_power, coefficient in profile.coefficients:
        print(f"  h^{h_power} t^{t_power}: {coefficient}")
    print("no_borrow_law")
    print("  m = 4*s + h + 1")
    print("  q = 43*m + 9*t")
    print("  selected = 1 - floor((t + 2 - h)/3)")
    print(f"square_axis_no_borrow_digit_rows={int(row_ok)}/1")
    print("interpretation")
    print("  base43_digit_selector_is_a_base3_no_borrow_predicate=1")
    print("  no_borrow_selector_is_rank3_and_mixed_not_row_column_separable=1")
    print("  exact_polynomial_normal_form_requires_total_degree4_bidegree2_by2=1")
    print("  producer_must_realize_a_tiny_carry_not_a_linear_digit_filter=1")
    print("conclusion=reported_p25_laneB_square_axis_no_borrow_digit_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
