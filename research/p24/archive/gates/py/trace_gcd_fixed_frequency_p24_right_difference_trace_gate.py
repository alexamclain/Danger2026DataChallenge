#!/usr/bin/env python3
"""Bridge right-difference profiles to decomposition-field trace zero.

For adjacent right H-cosets define the relative difference polynomial

    P_i(X) = sum_k (A_{i+1,k} - A_{i,k}) X^k,

where A_{i,k} is the right-coset profile coefficient at relative index k.
The right-difference target is

    sum_{k in D} coeff_k(P_i) = |<p>| * coeff_0(P_i)

for every nonzero relative <p>-coset D.  By Gaussian-period inversion, this is
equivalent to the decomposition trace

    Tr_{K_n/K_n^<p>}(P_i(zeta_n)) = 0.

This script checks the equivalence in a small cyclotomic model with a relative
quotient of order 8 and seven cyclic right differences.
"""

from __future__ import annotations

import random


FIELD_Q = 439  # 439 - 1 = 6 * 73, so F_q contains zeta_73.
RIGHT_QUOTIENT = 7
TOY_N = 73
TOY_RELATIVE_QUOTIENT = 8
TOY_W_ORDER = (TOY_N - 1) // TOY_RELATIVE_QUOTIENT
SEED = 20260607
TRIALS = 72

P24_N = 3107441
P24_W_ORDER = 388430
P24_RIGHT_QUOTIENT = 7
P24_RELATIVE_QUOTIENT = 8
P24_INDEPENDENT_RIGHT_DIFFERENCES = 6


Vector = list[int]
Rows = list[Vector]


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


def subgroup_order_elements(modulus: int, order: int) -> list[int]:
    generator = primitive_root_mod_prime(modulus)
    step = (modulus - 1) // order
    h_generator = pow(generator, step, modulus)
    out: list[int] = []
    value = 1
    for _index in range(order):
        out.append(value)
        value = value * h_generator % modulus
    if value != 1 or len(set(out)) != order:
        raise RuntimeError("bad subgroup")
    return out


def cosets_of_subgroup(modulus: int, subgroup: list[int]) -> list[list[int]]:
    remaining = set(range(1, modulus))
    cosets: list[list[int]] = []
    while remaining:
        rep = min(remaining)
        coset = sorted((rep * u) % modulus for u in subgroup)
        cosets.append(coset)
        remaining.difference_update(coset)
    return cosets


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % q
            if factor:
                mat[row] = [
                    (mat[row][idx] - factor * mat[rank][idx]) % q
                    for idx in range(cols)
                ]
        rank += 1
    return rank


def zeta_n_in_split_field(n: int, q: int) -> int:
    return pow(primitive_root_mod_prime(q), (q - 1) // n, q)


def polynomial_eval(coefficients: Vector, point: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coefficients:
        total = (total + coeff * power) % q
        power = power * point % q
    return total


def gaussian_periods(n: int, q: int, zeta: int, subgroup: list[int]) -> list[int]:
    return [
        sum(pow(zeta, (index * exponent) % n, q) for exponent in subgroup) % q
        for index in range(n)
    ]


def trace_vector(coefficients: Vector, zeta: int, subgroup: list[int], cosets: list[list[int]]) -> Vector:
    return [
        sum(
            polynomial_eval(coefficients, pow(zeta, (coset[0] * u) % TOY_N, FIELD_Q), FIELD_Q)
            for u in subgroup
        )
        % FIELD_Q
        for coset in cosets
    ]


def random_rows(rng: random.Random) -> Rows:
    return [
        [rng.randrange(FIELD_Q) for _index in range(TOY_N)]
        for _row in range(RIGHT_QUOTIENT)
    ]


def difference_coefficients(rows: Rows, right_index: int) -> Vector:
    next_index = (right_index + 1) % RIGHT_QUOTIENT
    return [
        (rows[next_index][index] - rows[right_index][index]) % FIELD_Q
        for index in range(TOY_N)
    ]


def coset_balanced(coefficients: Vector, cosets: list[list[int]]) -> bool:
    target = (TOY_W_ORDER * coefficients[0]) % FIELD_Q
    return all(
        sum(coefficients[index] for index in coset) % FIELD_Q == target
        for coset in cosets
    )


def all_right_differences_balanced(rows: Rows, cosets: list[list[int]]) -> bool:
    return all(
        coset_balanced(difference_coefficients(rows, index), cosets)
        for index in range(RIGHT_QUOTIENT)
    )


def all_right_difference_traces_zero(
    rows: Rows,
    zeta: int,
    subgroup: list[int],
    cosets: list[list[int]],
) -> bool:
    return all(
        all(value == 0 for value in trace_vector(difference_coefficients(rows, index), zeta, subgroup, cosets))
        for index in range(RIGHT_QUOTIENT)
    )


def forced_balanced_coefficients(rng: random.Random, cosets: list[list[int]]) -> Vector:
    coefficients = [0] * TOY_N
    coefficients[0] = rng.randrange(FIELD_Q)
    target = (TOY_W_ORDER * coefficients[0]) % FIELD_Q
    for coset in cosets:
        running = 0
        for index in coset[:-1]:
            coefficients[index] = rng.randrange(FIELD_Q)
            running = (running + coefficients[index]) % FIELD_Q
        coefficients[coset[-1]] = (target - running) % FIELD_Q
    return coefficients


def force_trace_zero_differences(rng: random.Random, cosets: list[list[int]]) -> Rows:
    rows: Rows = [[rng.randrange(FIELD_Q) for _index in range(TOY_N)]]
    deltas = [forced_balanced_coefficients(rng, cosets) for _index in range(RIGHT_QUOTIENT - 1)]
    for delta in deltas:
        rows.append([(rows[-1][index] + delta[index]) % FIELD_Q for index in range(TOY_N)])
    return rows


def force_single_difference_defect(rng: random.Random, cosets: list[list[int]]) -> Rows:
    rows = force_trace_zero_differences(rng, cosets)
    right_index = rng.randrange(RIGHT_QUOTIENT)
    next_index = (right_index + 1) % RIGHT_QUOTIENT
    coeff_index = rng.randrange(1, TOY_N)
    rows[next_index][coeff_index] = (rows[next_index][coeff_index] + rng.randrange(1, FIELD_Q)) % FIELD_Q
    return rows


def main() -> None:
    rng = random.Random(SEED)
    subgroup = subgroup_order_elements(TOY_N, TOY_W_ORDER)
    cosets = cosets_of_subgroup(TOY_N, subgroup)
    zeta = zeta_n_in_split_field(TOY_N, FIELD_Q)
    periods = gaussian_periods(TOY_N, FIELD_Q, zeta, subgroup)
    period_matrix = [
        [periods[(a_coset[0] * d_coset[0]) % TOY_N] for d_coset in cosets]
        for a_coset in cosets
    ]
    period_rank = rank_mod_q(period_matrix, FIELD_Q)

    equivalence_failures = 0
    random_trace_zero = 0
    forced_trace_zero = 0
    forced_balanced = 0
    single_defect_trace_nonzero = 0
    single_defect_balance_false = 0

    families: list[Rows] = []
    for _trial in range(TRIALS):
        families.append(random_rows(rng))
        families.append(force_trace_zero_differences(rng, cosets))
        families.append(force_single_difference_defect(rng, cosets))

    for rows in families:
        trace_zero = all_right_difference_traces_zero(rows, zeta, subgroup, cosets)
        balanced = all_right_differences_balanced(rows, cosets)
        equivalence_failures += int(trace_zero != balanced)

    for _trial in range(TRIALS):
        rows = random_rows(rng)
        random_trace_zero += int(all_right_difference_traces_zero(rows, zeta, subgroup, cosets))

        rows = force_trace_zero_differences(rng, cosets)
        forced_trace_zero += int(all_right_difference_traces_zero(rows, zeta, subgroup, cosets))
        forced_balanced += int(all_right_differences_balanced(rows, cosets))

        rows = force_single_difference_defect(rng, cosets)
        single_defect_trace_nonzero += int(not all_right_difference_traces_zero(rows, zeta, subgroup, cosets))
        single_defect_balance_false += int(not all_right_differences_balanced(rows, cosets))

    print("Trace-GCD fixed-frequency p24 right-difference trace gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_n={TOY_N}")
    print(f"toy_w_order={TOY_W_ORDER}")
    print(f"toy_relative_quotient={TOY_RELATIVE_QUOTIENT}")
    print(f"toy_right_quotient={RIGHT_QUOTIENT}")
    print(f"toy_period_matrix_rank={period_rank}/{TOY_RELATIVE_QUOTIENT}")
    print(f"right_difference_trace_equivalence_failures={equivalence_failures}")
    print(f"random_right_difference_trace_zero={random_trace_zero}/{TRIALS}")
    print(f"forced_right_difference_trace_zero={forced_trace_zero}/{TRIALS}")
    print(f"forced_right_difference_balanced={forced_balanced}/{TRIALS}")
    print(f"single_defect_trace_nonzero={single_defect_trace_nonzero}/{TRIALS}")
    print(f"single_defect_balance_false={single_defect_balance_false}/{TRIALS}")
    print(f"p24_n={P24_N}")
    print(f"p24_w_order={P24_W_ORDER}")
    print(f"p24_right_quotient={P24_RIGHT_QUOTIENT}")
    print(f"p24_relative_quotient={P24_RELATIVE_QUOTIENT}")
    print(f"p24_redundant_adjacent_trace_equations={P24_RIGHT_QUOTIENT * P24_RELATIVE_QUOTIENT}")
    print(f"p24_independent_adjacent_trace_equations={P24_INDEPENDENT_RIGHT_DIFFERENCES * P24_RELATIVE_QUOTIENT}")
    print("interpretation")
    print("  adjacent_right_difference_balance_iff_decomposition_trace_zero=1")
    print("  right_difference_polynomials_are_the_new_trace_zero_targets=1")
    print("  single_coefficient_defect_breaks_trace_and_balance=1")
    print("  proof_target_is_explicit_degree8_trace_zero_for_each_adjacent_right_difference=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_trace_gate")

    if period_rank != TOY_RELATIVE_QUOTIENT:
        raise SystemExit(1)
    if equivalence_failures:
        raise SystemExit(1)
    if random_trace_zero:
        raise SystemExit(1)
    if forced_trace_zero != TRIALS or forced_balanced != TRIALS:
        raise SystemExit(1)
    if single_defect_trace_nonzero != TRIALS or single_defect_balance_false != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
