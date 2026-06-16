#!/usr/bin/env python3
"""Invert the p24 Gaussian-period internal trace into coset balance.

The internal trace target for a relative packet polynomial

    P(X) = sum_k c_k X^k

with U=<Q>, Q=p^5460 mod n, is

    Tr_U(P)(a) = sum_{u in U} P(zeta_n^(a u)).

Expanding in Gaussian periods shows this trace depends only on:

    c_0, and the sums C_D = sum_{k in D} c_k

over the nonzero U-cosets D in F_n^*.  The quotient period matrix is
invertible because its Fourier eigenvalues are nonzero Gauss sums.  Therefore
all internal traces vanish if and only if

    C_D = |U| * c_0

for every nonzero U-coset D.

This gate checks the equivalence in a small split cyclotomic model and prints
the p24 counts for the weighted CM/Lang coefficient theorem.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
P24_N = 3107441
P24_INTERNAL_ORDER = 5549
P24_RECOMBINED_ORDER = 388430
P24_RIGHT_NONTRIVIAL_CHARACTERS = 6
SEED = 20260606

TOY_N = 43
TOY_Q = 173
TOY_INTERNAL_ORDER = 7
TOY_RECOMBINED_ORDER = 21


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


def polynomial_eval(coefficients: list[int], point: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coefficients:
        total = (total + coeff * power) % q
        power = power * point % q
    return total


def zeta_n_in_split_field(n: int, q: int) -> int:
    root = primitive_root_mod_prime(q)
    return pow(root, (q - 1) // n, q)


def gaussian_periods(n: int, q: int, zeta: int, subgroup: list[int]) -> list[int]:
    return [
        sum(pow(zeta, (index * exponent) % n, q) for exponent in subgroup) % q
        for index in range(n)
    ]


def orbit_trace_vector(
    coefficients: list[int],
    zeta: int,
    subgroup: list[int],
    cosets: list[list[int]],
    n: int,
    q: int,
) -> list[int]:
    return [
        sum(
            polynomial_eval(coefficients, pow(zeta, (coset[0] * u) % n, q), q)
            for u in subgroup
        )
        % q
        for coset in cosets
    ]


def coset_sums(coefficients: list[int], cosets: list[list[int]], q: int) -> list[int]:
    return [sum(coefficients[index] for index in coset) % q for coset in cosets]


def is_balanced(coefficients: list[int], cosets: list[list[int]], subgroup_order: int, q: int) -> bool:
    target = (subgroup_order * coefficients[0]) % q
    return all(value == target for value in coset_sums(coefficients, cosets, q))


def random_coefficients(rng: random.Random, n: int, q: int) -> list[int]:
    return [rng.randrange(q) for _index in range(n)]


def forced_balanced_coefficients(
    rng: random.Random,
    n: int,
    q: int,
    cosets: list[list[int]],
    subgroup_order: int,
) -> list[int]:
    coefficients = [0] * n
    coefficients[0] = rng.randrange(q)
    target = (subgroup_order * coefficients[0]) % q
    for coset in cosets:
        running = 0
        for index in coset[:-1]:
            coefficients[index] = rng.randrange(q)
            running = (running + coefficients[index]) % q
        coefficients[coset[-1]] = (target - running) % q
    return coefficients


def main() -> None:
    subgroup = subgroup_order_elements(TOY_N, TOY_INTERNAL_ORDER)
    recombined_subgroup = subgroup_order_elements(TOY_N, TOY_RECOMBINED_ORDER)
    cosets = cosets_of_subgroup(TOY_N, subgroup)
    recombined_cosets = cosets_of_subgroup(TOY_N, recombined_subgroup)
    zeta = zeta_n_in_split_field(TOY_N, TOY_Q)
    periods = gaussian_periods(TOY_N, TOY_Q, zeta, subgroup)
    recombined_periods = gaussian_periods(TOY_N, TOY_Q, zeta, recombined_subgroup)
    period_matrix = [
        [periods[(a_coset[0] * d_coset[0]) % TOY_N] for d_coset in cosets]
        for a_coset in cosets
    ]
    recombined_period_matrix = [
        [
            recombined_periods[(a_coset[0] * d_coset[0]) % TOY_N]
            for d_coset in recombined_cosets
        ]
        for a_coset in recombined_cosets
    ]
    period_rank = rank_mod_q(period_matrix, TOY_Q)
    recombined_period_rank = rank_mod_q(recombined_period_matrix, TOY_Q)
    period_row_sum_values = {
        sum(periods[(a_coset[0] * d_coset[0]) % TOY_N] for d_coset in cosets) % TOY_Q
        for a_coset in cosets
    }
    recombined_row_sum_values = {
        sum(
            recombined_periods[(a_coset[0] * d_coset[0]) % TOY_N]
            for d_coset in recombined_cosets
        )
        % TOY_Q
        for a_coset in recombined_cosets
    }

    rng = random.Random(SEED)
    equivalence_failures = 0
    recombined_equivalence_failures = 0
    random_unbalanced_trace_nonzero = 0
    recombined_random_unbalanced_trace_nonzero = 0
    forced_balanced_trace_zero = 0
    recombined_forced_balanced_trace_zero = 0
    trials = 48
    for _trial in range(trials):
        random_coeffs = random_coefficients(rng, TOY_N, TOY_Q)
        random_traces = orbit_trace_vector(random_coeffs, zeta, subgroup, cosets, TOY_N, TOY_Q)
        random_zero = all(trace == 0 for trace in random_traces)
        random_balanced = is_balanced(random_coeffs, cosets, TOY_INTERNAL_ORDER, TOY_Q)
        equivalence_failures += int(random_zero != random_balanced)
        random_unbalanced_trace_nonzero += int((not random_balanced) and (not random_zero))
        recombined_random_traces = orbit_trace_vector(
            random_coeffs,
            zeta,
            recombined_subgroup,
            recombined_cosets,
            TOY_N,
            TOY_Q,
        )
        recombined_random_zero = all(trace == 0 for trace in recombined_random_traces)
        recombined_random_balanced = is_balanced(
            random_coeffs,
            recombined_cosets,
            TOY_RECOMBINED_ORDER,
            TOY_Q,
        )
        recombined_equivalence_failures += int(
            recombined_random_zero != recombined_random_balanced
        )
        recombined_random_unbalanced_trace_nonzero += int(
            (not recombined_random_balanced) and (not recombined_random_zero)
        )

        balanced_coeffs = forced_balanced_coefficients(
            rng, TOY_N, TOY_Q, cosets, TOY_INTERNAL_ORDER
        )
        balanced_traces = orbit_trace_vector(balanced_coeffs, zeta, subgroup, cosets, TOY_N, TOY_Q)
        balanced_zero = all(trace == 0 for trace in balanced_traces)
        balanced_condition = is_balanced(balanced_coeffs, cosets, TOY_INTERNAL_ORDER, TOY_Q)
        equivalence_failures += int(balanced_zero != balanced_condition)
        forced_balanced_trace_zero += int(balanced_zero)

        recombined_balanced_coeffs = forced_balanced_coefficients(
            rng, TOY_N, TOY_Q, recombined_cosets, TOY_RECOMBINED_ORDER
        )
        recombined_balanced_traces = orbit_trace_vector(
            recombined_balanced_coeffs,
            zeta,
            recombined_subgroup,
            recombined_cosets,
            TOY_N,
            TOY_Q,
        )
        recombined_balanced_zero = all(trace == 0 for trace in recombined_balanced_traces)
        recombined_balanced_condition = is_balanced(
            recombined_balanced_coeffs,
            recombined_cosets,
            TOY_RECOMBINED_ORDER,
            TOY_Q,
        )
        recombined_equivalence_failures += int(
            recombined_balanced_zero != recombined_balanced_condition
        )
        recombined_forced_balanced_trace_zero += int(recombined_balanced_zero)

    p24_q_generator = pow(P24, 5460, P24_N)
    p24_internal_order_check = 1
    value = p24_q_generator
    while value != 1:
        value = value * p24_q_generator % P24_N
        p24_internal_order_check += 1
        if p24_internal_order_check > P24_INTERNAL_ORDER:
            break
    p24_coset_count = (P24_N - 1) // P24_INTERNAL_ORDER
    p24_recombined_coset_count = (P24_N - 1) // P24_RECOMBINED_ORDER

    print("Trace-GCD fixed-frequency p24 period-coset balance gate")
    print(f"toy_n={TOY_N}")
    print(f"toy_q={TOY_Q}")
    print(f"toy_zeta={zeta}")
    print(f"toy_internal_order={TOY_INTERNAL_ORDER}")
    print(f"toy_coset_count={len(cosets)}")
    print(f"toy_period_matrix_rank={period_rank}/{len(cosets)}")
    print(f"toy_period_row_sum_values={sorted(period_row_sum_values)}")
    print(f"trace_zero_iff_U_coset_balanced_failures={equivalence_failures}")
    print(f"random_unbalanced_trace_nonzero={random_unbalanced_trace_nonzero}/{trials}")
    print(f"forced_balanced_trace_zero={forced_balanced_trace_zero}/{trials}")
    print(f"toy_recombined_order={TOY_RECOMBINED_ORDER}")
    print(f"toy_recombined_coset_count={len(recombined_cosets)}")
    print(f"toy_recombined_period_matrix_rank={recombined_period_rank}/{len(recombined_cosets)}")
    print(f"toy_recombined_period_row_sum_values={sorted(recombined_row_sum_values)}")
    print(
        "recombined_trace_zero_iff_W_coset_balanced_failures="
        f"{recombined_equivalence_failures}"
    )
    print(
        "recombined_random_unbalanced_trace_nonzero="
        f"{recombined_random_unbalanced_trace_nonzero}/{trials}"
    )
    print(
        "recombined_forced_balanced_trace_zero="
        f"{recombined_forced_balanced_trace_zero}/{trials}"
    )
    print(f"p24_internal_q_generator=p^5460_mod_n={p24_q_generator}")
    print(f"p24_internal_order_check={p24_internal_order_check}")
    print(f"p24_internal_coset_count={p24_coset_count}")
    print(f"p24_internal_subgroup_order={P24_INTERNAL_ORDER}")
    print(f"p24_recombined_subgroup_order=ord_n(p)={P24_RECOMBINED_ORDER}")
    print(f"p24_recombined_coset_count={p24_recombined_coset_count}")
    print(f"p24_E_idempotents_per_Fp_factor={P24_RECOMBINED_ORDER // P24_INTERNAL_ORDER}")
    print(
        "p24_recombined_scalar_equations="
        f"{P24_RIGHT_NONTRIVIAL_CHARACTERS * p24_recombined_coset_count}"
    )
    print(
        "p24_recombined_nontrivial_octic_equations="
        f"{P24_RIGHT_NONTRIVIAL_CHARACTERS * (p24_recombined_coset_count - 1)}"
    )
    print(f"p24_recombined_anchor_equations={P24_RIGHT_NONTRIVIAL_CHARACTERS}")
    print(
        "p24_recombined_compressed_values_with_c0="
        f"{P24_RIGHT_NONTRIVIAL_CHARACTERS * (p24_recombined_coset_count + 1)}"
    )
    print("interpretation")
    print("  quotient_gaussian_period_matrix_is_full_rank=1")
    print("  internal_trace_zero_iff_nonzero_U_coset_sums_equal_U_times_constant=1")
    print("  p24_per_factor_trace_target_equiv_to_560_coset_balance=1")
    print("  complete_recombination_reduces_balance_cosets_560_to_8=1")
    print("  p24_recombined_trace_target_equiv_to_8_coset_balance=1")
    print("  recombined_balance_splits_into_42_octic_plus_6_anchor_equations=1")
    print("  weighted_coefficients_are_c_k_chi=sum_r_chi_inverse_r_j_r_plus_mk=1")
    print("  remaining_theorem_is_weighted_CM_sequence_U_coset_balance=1")
    print("  recombined_theorem_is_weighted_CM_sequence_p_coset_balance=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_period_coset_balance_gate")

    if period_rank != len(cosets):
        raise SystemExit(1)
    if recombined_period_rank != len(recombined_cosets):
        raise SystemExit(1)
    if period_row_sum_values != {TOY_Q - 1}:
        raise SystemExit(1)
    if recombined_row_sum_values != {TOY_Q - 1}:
        raise SystemExit(1)
    if equivalence_failures:
        raise SystemExit(1)
    if recombined_equivalence_failures:
        raise SystemExit(1)
    if random_unbalanced_trace_nonzero != trials:
        raise SystemExit(1)
    if recombined_random_unbalanced_trace_nonzero != trials:
        raise SystemExit(1)
    if forced_balanced_trace_zero != trials:
        raise SystemExit(1)
    if recombined_forced_balanced_trace_zero != trials:
        raise SystemExit(1)
    if p24_internal_order_check != P24_INTERNAL_ORDER:
        raise SystemExit(1)
    if p24_recombined_coset_count != 8:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
