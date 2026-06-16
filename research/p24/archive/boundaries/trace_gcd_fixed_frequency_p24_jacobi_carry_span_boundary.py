#!/usr/bin/env python3
"""Rank boundary for the admissible C-axis Jacobi-carry proof target.

The support gate shows that C-axis Jacobi carries kill the forbidden

    C_7^nontrivial x {C-trivial}

bidegrees only for the admissible subfamily: one input is right-trivial and
C-nontrivial, while the partner and the sum keep nontrivial C-component.  If
the partner is pure-right, or the C-components cancel, the individual carry
leaks in the forbidden slots.

This gate checks the next guardrail: the admissible clean span is much smaller
than the entire no-forbidden-bidegree subspace.  Therefore support agreement
does not make the Jacobi decomposition automatic.

For small exact models C_7 x C_c the C-axis carry span has rank

    broad C-axis family:      7*(c-1)/2 + 2,
    admissible clean family:  7*(c-1)/2 - 2,

while the no-forbidden space has dimension 7*c - 6, and the
origin-normalized part has dimension 7*c - 7.  The p24 admissible-rank
extrapolation is 621.  The older broad rank 625 matches the slow exploratory
p24 rank probe, but includes four leaky directions and is not the termwise-safe
Jacobi theorem target.
"""

from __future__ import annotations


RIGHT_DEGREE = 7
SMALL_C_DEGREES = [5, 11, 13, 17, 19]
P24_C_DEGREE = 179


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def split_prime_for(order: int) -> int:
    multiplier = 2
    while True:
        candidate = multiplier * order + 1
        if is_prime(candidate):
            return candidate
        multiplier += 1


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % modulus, -1, modulus)
        mat[rank] = [(value * inv) % modulus for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % modulus
            if factor:
                mat[row] = [
                    (value - factor * pivot_value) % modulus
                    for value, pivot_value in zip(mat[row], mat[rank])
                ]
        rank += 1
    return rank


def crt(right_index: int, c_index: int, c_degree: int) -> int:
    order = RIGHT_DEGREE * c_degree
    return (
        right_index * c_degree * pow(c_degree, -1, RIGHT_DEGREE)
        + c_index * RIGHT_DEGREE * pow(RIGHT_DEGREE, -1, c_degree)
    ) % order


def carry_vector(c_degree: int, modulus: int, u_value: int, v_value: int) -> list[int]:
    order = RIGHT_DEGREE * c_degree
    uv_value = (u_value + v_value) % order
    points = [
        crt(right_index, c_index, c_degree)
        for right_index in range(RIGHT_DEGREE)
        for c_index in range(c_degree)
    ]
    return [
        ((u_value * point) % order + (v_value * point) % order - (uv_value * point) % order)
        % modulus
        for point in points
    ]


def broad_c_axis_carry_rows(c_degree: int, modulus: int) -> list[list[int]]:
    order = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order:
                rows.append(carry_vector(c_degree, modulus, u_value, v_value))
    return rows


def admissible_c_axis_carry_rows(c_degree: int, modulus: int) -> list[list[int]]:
    order = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if v_value % c_degree == 0:
                continue
            if (u_value + v_value) % c_degree == 0:
                continue
            rows.append(carry_vector(c_degree, modulus, u_value, v_value))
    return rows


def no_forbidden_right_nontrivial_c_trivial(
    row: list[int], c_degree: int, modulus: int
) -> bool:
    row_sums = [
        sum(row[right * c_degree : (right + 1) * c_degree]) % modulus
        for right in range(RIGHT_DEGREE)
    ]
    return all(row_sum == row_sums[0] for row_sum in row_sums)


def c_cancel_partner(c_degree: int, u_value: int) -> int:
    order = RIGHT_DEGREE * c_degree
    for v_value in range(1, order):
        if v_value % c_degree == 0:
            continue
        if (u_value + v_value) % order == 0:
            continue
        if (u_value + v_value) % c_degree == 0:
            return v_value
    raise RuntimeError("no C-cancel partner found")


def expected_broad_rank(c_degree: int) -> int:
    return RIGHT_DEGREE * ((c_degree - 1) // 2) + 2


def expected_admissible_rank(c_degree: int) -> int:
    return RIGHT_DEGREE * ((c_degree - 1) // 2) - 2


def main() -> None:
    broad_rank_formula_matches = 0
    admissible_rank_formula_matches = 0
    admissible_support_rows = 0
    leaky_control_rows = 0
    strict_subspace_rows = 0
    rows_checked = 0

    print("Trace-GCD fixed-frequency p24 Jacobi-carry span boundary")
    print(f"right_degree={RIGHT_DEGREE}")
    for c_degree in SMALL_C_DEGREES:
        order = RIGHT_DEGREE * c_degree
        field_q = split_prime_for(order)
        broad_rows = broad_c_axis_carry_rows(c_degree, field_q)
        admissible_rows = admissible_c_axis_carry_rows(c_degree, field_q)
        broad_rank = rank_mod(broad_rows, field_q)
        admissible_rank = rank_mod(admissible_rows, field_q)
        allowed_dim = order - (RIGHT_DEGREE - 1)
        origin_normalized_allowed_dim = allowed_dim - 1
        broad_formula = expected_broad_rank(c_degree)
        admissible_formula = expected_admissible_rank(c_degree)
        broad_formula_match = int(broad_rank == broad_formula)
        admissible_formula_match = int(admissible_rank == admissible_formula)
        admissible_support_ok = int(
            all(
                no_forbidden_right_nontrivial_c_trivial(row, c_degree, field_q)
                for row in admissible_rows
            )
        )
        u_value = RIGHT_DEGREE
        pure_right_row = carry_vector(c_degree, field_q, u_value, c_degree)
        c_cancel_row = carry_vector(
            c_degree, field_q, u_value, c_cancel_partner(c_degree, u_value)
        )
        leaky_controls_ok = int(
            not no_forbidden_right_nontrivial_c_trivial(
                pure_right_row, c_degree, field_q
            )
            and not no_forbidden_right_nontrivial_c_trivial(
                c_cancel_row, c_degree, field_q
            )
        )
        strict = int(admissible_rank < origin_normalized_allowed_dim)
        broad_rank_formula_matches += broad_formula_match
        admissible_rank_formula_matches += admissible_formula_match
        admissible_support_rows += admissible_support_ok
        leaky_control_rows += leaky_controls_ok
        strict_subspace_rows += strict
        rows_checked += 1
        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"broad_generators={len(broad_rows)} "
            f"admissible_generators={len(admissible_rows)} "
            f"broad_carry_rank={broad_rank} expected_broad_rank={broad_formula} "
            f"admissible_carry_rank={admissible_rank} "
            f"expected_admissible_rank={admissible_formula} "
            f"no_forbidden_dim={allowed_dim} "
            f"origin_normalized_no_forbidden_dim={origin_normalized_allowed_dim} "
            f"broad_formula_match={broad_formula_match} "
            f"admissible_formula_match={admissible_formula_match} "
            f"admissible_support_ok={admissible_support_ok} "
            f"leaky_controls_ok={leaky_controls_ok} "
            f"strict_subspace={strict}"
        )

    p24_broad_formula_rank = expected_broad_rank(P24_C_DEGREE)
    p24_admissible_formula_rank = expected_admissible_rank(P24_C_DEGREE)
    p24_no_forbidden_dim = RIGHT_DEGREE * P24_C_DEGREE - (RIGHT_DEGREE - 1)
    p24_origin_normalized_no_forbidden_dim = p24_no_forbidden_dim - 1

    print(f"broad_rank_formula_matches={broad_rank_formula_matches}/{rows_checked}")
    print(
        "admissible_rank_formula_matches="
        f"{admissible_rank_formula_matches}/{rows_checked}"
    )
    print(f"admissible_support_zero={admissible_support_rows}/{rows_checked}")
    print(f"leaky_controls_forbidden_nonzero={leaky_control_rows}/{rows_checked}")
    print(f"admissible_carry_span_strict_subspace={strict_subspace_rows}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print(f"p24_broad_c_axis_carry_rank_formula={p24_broad_formula_rank}")
    print(f"p24_admissible_c_axis_carry_rank_formula={p24_admissible_formula_rank}")
    print("p24_broad_minus_admissible_rank=4")
    print(f"p24_no_forbidden_bidegree_dim={p24_no_forbidden_dim}")
    print(f"p24_origin_normalized_no_forbidden_dim={p24_origin_normalized_no_forbidden_dim}")
    print("interpretation")
    print("  admissible_C_axis_carry_span_is_strictly_smaller_than_no_forbidden_space=1")
    print("  support_vanishing_does_not_make_jacobi_decomposition_automatic=1")
    print("  broad_C_axis_rank_625_includes_leaky_directions=1")
    print("  p24_positive_target_is_rank_621_admissible_C_axis_carry_subspace=1")
    print("  weighted_packet_must_land_in_specific_admissible_jacobi_carry_span=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary")

    if broad_rank_formula_matches != rows_checked:
        raise SystemExit(1)
    if admissible_rank_formula_matches != rows_checked:
        raise SystemExit(1)
    if admissible_support_rows != rows_checked:
        raise SystemExit(1)
    if leaky_control_rows != rows_checked:
        raise SystemExit(1)
    if strict_subspace_rows != rows_checked:
        raise SystemExit(1)
    if p24_broad_formula_rank != 625:
        raise SystemExit(1)
    if p24_admissible_formula_rank != 621:
        raise SystemExit(1)
    if p24_origin_normalized_no_forbidden_dim != 1246:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
