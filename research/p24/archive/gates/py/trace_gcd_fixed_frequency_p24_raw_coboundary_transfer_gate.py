#!/usr/bin/env python3
"""Raw coboundary transfer gate for the p24 nested trace target.

The nested internal-trace theorem target is useful only if we can construct a
potential before checking the desired trace vanishing.  This script records a
positive transfer theorem:

    x = sigma(Y) - epsilon*Y   on the raw p^780 factor-cycle algebra

implies

    Tr_{B/E}(x) = sigma(Tr_{B/E}(Y)) - epsilon*Tr_{B/E}(Y)

on the quotient degree-7 seed after the nested internal trace
Tr_{B/E}=Tr_{C/E} o Tr_{B/C}.

It also records the circularity boundary: solving for Y by applying a
Hilbert-90 inverse after knowing the quotient twisted trace is zero is just a
restatement of the vanishing.  The p24 proof must construct Y from CM/Lang
data before that zero is known.
"""

from __future__ import annotations

import math
import random

import sympy as sp


P24 = 10**24 + 7
M = 66254
N = 3107441
RIGHT = 211
RIGHT_GEN = 2
RHO_EXPONENT = 780
ORDER7 = 7
P24_C_DEGREE = 179
P24_B_OVER_C_DEGREE = 31

FIELD_Q = 43
TOY_QUOTIENT_DEGREE = 7
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3
TOY_TOTAL_DEGREE = TOY_QUOTIENT_DEGREE * TOY_C_DEGREE * TOY_B_OVER_C_DEGREE
SEED = 20260606


Vector = list[int]


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


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def right_log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("2 is not primitive modulo 211")
    return logs


def add(left: Vector, right: Vector) -> Vector:
    return [(a + b) % FIELD_Q for a, b in zip(left, right)]


def sub(left: Vector, right: Vector) -> Vector:
    return [(a - b) % FIELD_Q for a, b in zip(left, right)]


def scalar_mul(scalar: int, vector: Vector) -> Vector:
    return [(scalar * value) % FIELD_Q for value in vector]


def sigma(vector: Vector, power: int = 1) -> Vector:
    shift = power % len(vector)
    if shift == 0:
        return vector[:]
    return vector[-shift:] + vector[:-shift]


def zero() -> Vector:
    return [0] * TOY_TOTAL_DEGREE


def random_vector(rng: random.Random) -> Vector:
    while True:
        vector = [rng.randrange(FIELD_Q) for _index in range(TOY_TOTAL_DEGREE)]
        if any(vector):
            return vector


def trace_over_powers(vector: Vector, step: int, count: int) -> Vector:
    out = zero()
    for index in range(count):
        out = add(out, sigma(vector, step * index))
    return out


def trace_b_over_c(vector: Vector) -> Vector:
    return trace_over_powers(
        vector,
        TOY_QUOTIENT_DEGREE * TOY_C_DEGREE,
        TOY_B_OVER_C_DEGREE,
    )


def trace_c_over_e(vector: Vector) -> Vector:
    return trace_over_powers(vector, TOY_QUOTIENT_DEGREE, TOY_C_DEGREE)


def nested_internal_trace(vector: Vector) -> Vector:
    return trace_c_over_e(trace_b_over_c(vector))


def twisted_coboundary(vector: Vector, eigenvalue: int) -> Vector:
    return sub(sigma(vector), scalar_mul(eigenvalue, vector))


def quotient_twisted_trace(vector: Vector, eigenvalue: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_eigenvalue = pow(eigenvalue, -1, FIELD_Q)
    for index in range(TOY_QUOTIENT_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_eigenvalue % FIELD_Q
    return out


def is_zero(vector: Vector) -> bool:
    return all(value % FIELD_Q == 0 for value in vector)


def is_fixed_by(vector: Vector, power: int) -> bool:
    return sigma(vector, power) == vector


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if rows[row][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, q)
        rows[rank] = [value * inv % q for value in rows[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def standard_basis(index: int) -> Vector:
    return [1 if i == index else 0 for i in range(TOY_TOTAL_DEGREE)]


def linear_map_matrix(fn) -> list[list[int]]:
    columns = [fn(standard_basis(index)) for index in range(TOY_TOTAL_DEGREE)]
    return [[columns[col][row] for col in range(TOY_TOTAL_DEGREE)] for row in range(TOY_TOTAL_DEGREE)]


def kernel_dimension(matrix: list[list[int]]) -> int:
    return TOY_TOTAL_DEGREE - rank_mod(matrix, FIELD_Q)


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    tensor_factor_count = math.gcd(ord_m, ord_n)
    tensor_factor_degree = ord_n // tensor_factor_count
    rho_mod_n = pow(P24, RHO_EXPONENT, N)
    rho_order_mod_n = int(sp.n_order(rho_mod_n, N))
    rho7_mod_n = pow(P24, RHO_EXPONENT * ORDER7, N)
    rho7_order_mod_n = int(sp.n_order(rho7_mod_n, N))
    trace_subgroup_generator = pow(rho7_mod_n, P24_C_DEGREE, N)
    trace_subgroup_order = int(sp.n_order(trace_subgroup_generator, N))
    logs = right_log_table()
    rho_mod_211 = pow(P24, RHO_EXPONENT, RIGHT)
    rho_h_shift = logs[rho_mod_211] % ORDER7

    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    eigenvalues = [pow(zeta7, character, FIELD_Q) for character in range(1, ORDER7)]
    rng = random.Random(SEED)

    transfer_failures = 0
    quotient_trace_nonzero_after_transfer = 0
    transferred_seed_not_quotient_fixed = 0
    random_raw_seed_quotient_trace_zero = 0
    random_raw_seed_not_transfer_coboundary = 0
    circular_inverse_dimension_checks: list[tuple[int, int]] = []
    trials = 0

    for eigenvalue in eigenvalues:
        coboundary_matrix = linear_map_matrix(
            lambda vector, eigenvalue=eigenvalue: twisted_coboundary(vector, eigenvalue)
        )
        quotient_trace_after_nested_matrix = linear_map_matrix(
            lambda vector, eigenvalue=eigenvalue: quotient_twisted_trace(
                nested_internal_trace(vector),
                eigenvalue,
            )
        )
        circular_inverse_dimension_checks.append(
            (
                rank_mod(coboundary_matrix, FIELD_Q),
                kernel_dimension(quotient_trace_after_nested_matrix),
            )
        )

        for _trial in range(8):
            potential = random_vector(rng)
            raw_coboundary = twisted_coboundary(potential, eigenvalue)
            transferred_seed = nested_internal_trace(raw_coboundary)
            transferred_potential = nested_internal_trace(potential)
            expected_seed = twisted_coboundary(transferred_potential, eigenvalue)

            transfer_failures += int(transferred_seed != expected_seed)
            quotient_trace_nonzero_after_transfer += int(
                not is_zero(quotient_twisted_trace(transferred_seed, eigenvalue))
            )
            transferred_seed_not_quotient_fixed += int(
                not is_fixed_by(transferred_seed, TOY_QUOTIENT_DEGREE)
            )

            random_raw = random_vector(rng)
            random_seed = nested_internal_trace(random_raw)
            random_trace_zero = is_zero(quotient_twisted_trace(random_seed, eigenvalue))
            random_raw_seed_quotient_trace_zero += int(random_trace_zero)
            # In this semisimple cyclic model, quotient trace zero after
            # internal trace is exactly the same linear condition as being a
            # raw full-order coboundary.  Constructing a potential by solving
            # that equation after observing zero would be circular.
            random_raw_seed_not_transfer_coboundary += int(not random_trace_zero)
            trials += 1

    print("Trace-GCD fixed-frequency p24 raw coboundary transfer gate")
    print(f"p24={P24}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m_p={ord_m}")
    print(f"ord_n_p={ord_n}")
    print(f"tensor_factor_count_over_E={tensor_factor_count}")
    print(f"tensor_factor_degree_over_E={tensor_factor_degree}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_order_mod_n={rho_order_mod_n}")
    print(f"rho7_order_mod_n={rho7_order_mod_n}")
    print(f"p24_C_degree_over_E={P24_C_DEGREE}")
    print(f"p24_B_over_C_degree={P24_B_OVER_C_DEGREE}")
    print(f"p24_trace_subgroup_order={trace_subgroup_order}")
    print(f"rho_mod_211={rho_mod_211}")
    print(f"rho_raw_h_quotient_shift={rho_h_shift}")
    print(f"toy_q={FIELD_Q}")
    print(f"toy_quotient_degree={TOY_QUOTIENT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"toy_total_degree={TOY_TOTAL_DEGREE}")
    print(f"toy_character_count={len(eigenvalues)}")
    print(f"raw_coboundary_transfer_failures={transfer_failures}")
    print(f"quotient_trace_nonzero_after_transfer={quotient_trace_nonzero_after_transfer}/{trials}")
    print(f"transferred_seed_not_quotient_fixed={transferred_seed_not_quotient_fixed}/{trials}")
    print(f"random_nested_seed_quotient_trace_zero={random_raw_seed_quotient_trace_zero}/{trials}")
    print(f"random_nested_seed_not_forced_coboundary={random_raw_seed_not_transfer_coboundary}/{trials}")
    print(f"circular_inverse_rank_kernel_checks={circular_inverse_dimension_checks}")
    print("interpretation")
    print("  nested_internal_trace_commutes_with_twisted_coboundary=1")
    print("  raw_cm_lang_coboundary_would_supply_quotient_potential=1")
    print("  transferred_seed_has_zero_quotient_twisted_trace=1")
    print("  random_nested_seed_usually_not_a_coboundary=1")
    print("  solving_potential_after_zero_is_hilbert90_circular=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate")

    if (tensor_factor_count, tensor_factor_degree) != (70, 5549):
        raise SystemExit(1)
    if rho_order_mod_n != ORDER7 * tensor_factor_degree:
        raise SystemExit(1)
    if rho7_order_mod_n != tensor_factor_degree:
        raise SystemExit(1)
    if (P24_C_DEGREE, P24_B_OVER_C_DEGREE, trace_subgroup_order) != (179, 31, 31):
        raise SystemExit(1)
    if rho_h_shift == 0:
        raise SystemExit(1)
    if transfer_failures or quotient_trace_nonzero_after_transfer:
        raise SystemExit(1)
    if transferred_seed_not_quotient_fixed:
        raise SystemExit(1)
    if random_raw_seed_quotient_trace_zero > trials // 4:
        raise SystemExit(1)
    if any(pair[0] != pair[1] for pair in circular_inverse_dimension_checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
