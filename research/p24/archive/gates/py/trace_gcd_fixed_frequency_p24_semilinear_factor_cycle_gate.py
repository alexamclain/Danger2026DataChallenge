#!/usr/bin/env python3
"""Semilinear p24 factor-cycle gate for the order-7 packet sum.

The scalar factor-cycle toy is intentionally too optimistic: if

    Z_{i+1} = lambda * sigma(Z_i)

with sigma a Frobenius of order 7 and lambda a nontrivial 7th root of unity,
then sum_i Z_i is usually not zero.  It is a nontrivial Frobenius eigenvector.

For p24 this is still useful because the original fixed-frequency
class-character projection is L-valued, and rho=p^780 fixes
L=F_p(mu_157).  Thus the real finite implication is:

    semilinear rho-covariance gives sigma(S)=lambda^(-1) S,
    descent gives sigma(S)=S,
    lambda != 1 gives S=0.

This script checks that implication in a small finite-field model and records
the exact p24 arithmetic that makes rho an order-7 semilinear operator.
"""

from __future__ import annotations

import math
import random

import sympy as sp

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus


P24 = 10**24 + 7
M = 66254
N = 3107441
LEFT = 157
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
FIELD_Q = 43
FIELD_DEGREE = 7
SEED = 20260606


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


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
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
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def basis_vector(index: int, degree: int) -> tuple[int, ...]:
    return tuple(1 if i == index else 0 for i in range(degree))


def frobenius(value: tuple[int, ...], field: ExtensionField) -> tuple[int, ...]:
    return field.pow(value, field.q)


def frobenius_power(value: tuple[int, ...], times: int, field: ExtensionField) -> tuple[int, ...]:
    out = value
    for _ in range(times):
        out = frobenius(out, field)
    return out


def linear_map_matrix(field: ExtensionField, fn) -> list[list[int]]:
    columns = [fn(basis_vector(i, field.degree)) for i in range(field.degree)]
    return [[columns[col][row] for col in range(field.degree)] for row in range(field.degree)]


def kernel_dimension(field: ExtensionField, matrix: list[list[int]]) -> int:
    return field.degree - rank_mod(matrix, field.q)


def eigenspace_matrix(field: ExtensionField, eigenvalue: int) -> list[list[int]]:
    return linear_map_matrix(
        field,
        lambda value: field.sub(frobenius(value, field), field.scalar_mul(eigenvalue, value)),
    )


def twisted_projection(
    value: tuple[int, ...],
    character_value: int,
    field: ExtensionField,
) -> tuple[int, ...]:
    out = field.zero
    coeff = 1
    for i in range(ORDER7):
        out = field.add(out, field.scalar_mul(coeff, frobenius_power(value, i, field)))
        coeff = (coeff * character_value) % field.q
    return out


def random_element(rng: random.Random, field: ExtensionField) -> tuple[int, ...]:
    while True:
        value = tuple(rng.randrange(field.q) for _ in range(field.degree))
        if value != field.zero:
            return value


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    factor_count = math.gcd(ord_m, ord_n)
    factor_degree = ord_n // factor_count
    rho_order_on_e = ord_m // math.gcd(ord_m, RHO_EXPONENT)
    rho_left_fixed = pow(P24, RHO_EXPONENT, LEFT) == 1
    logs = right_log_table()
    p_log = logs[P24 % RIGHT]
    rho_right_log_mod7 = (p_log * RHO_EXPONENT) % ORDER7
    rho_factor_step = RHO_EXPONENT % factor_count
    rho_factor_cycle_length = factor_count // math.gcd(factor_count, rho_factor_step)

    modulus = find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED)
    field = ExtensionField(FIELD_Q, FIELD_DEGREE, modulus)
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    characters = [pow(zeta7, k, FIELD_Q) for k in range(1, ORDER7)]
    rng = random.Random(SEED)

    fixed_matrix = eigenspace_matrix(field, 1)
    fixed_kernel_dim = kernel_dimension(field, fixed_matrix)
    twisted_ranks: list[int] = []
    twisted_eigenspace_dims: list[int] = []
    fixed_intersection_dims: list[int] = []
    eigen_failures = 0
    random_nonzeroes = 0
    random_trials = 8 * len(characters)
    fixed_seed_zeroes = 0

    for character in characters:
        inverse_character = pow(character, -1, FIELD_Q)
        projection_matrix = linear_map_matrix(
            field,
            lambda value, character=character: twisted_projection(value, character, field),
        )
        twisted_ranks.append(rank_mod(projection_matrix, FIELD_Q))
        eig_matrix = eigenspace_matrix(field, inverse_character)
        twisted_eigenspace_dims.append(kernel_dimension(field, eig_matrix))
        fixed_intersection_dims.append(
            kernel_dimension(field, fixed_matrix + eig_matrix)
        )
        for column_index in range(field.degree):
            value = basis_vector(column_index, field.degree)
            projected = twisted_projection(value, character, field)
            if frobenius(projected, field) != field.scalar_mul(inverse_character, projected):
                eigen_failures += 1
        for _ in range(8):
            value = random_element(rng, field)
            random_nonzeroes += int(twisted_projection(value, character, field) != field.zero)
        fixed_seed = field.embed(rng.randrange(1, FIELD_Q))
        fixed_seed_zeroes += int(twisted_projection(fixed_seed, character, field) == field.zero)

    print("Trace-GCD fixed-frequency p24 semilinear factor-cycle gate")
    print(f"p24={P24}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m_p={ord_m}")
    print(f"ord_n_p={ord_n}")
    print(f"tensor_factor_count_over_E={factor_count}")
    print(f"tensor_factor_degree_over_E={factor_degree}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_order_on_E={rho_order_on_e}")
    print(f"rho_left157_fixed={int(rho_left_fixed)}")
    print(f"rho_right_h_quotient_shift={rho_right_log_mod7}")
    print(f"rho_factor_step_mod_70={rho_factor_step}")
    print(f"rho_factor_cycle_length={rho_factor_cycle_length}")
    print(f"field_q={FIELD_Q}")
    print(f"field_degree={FIELD_DEGREE}")
    print(f"field_modulus={modulus}")
    print(f"zeta7={zeta7}")
    print(f"fixed_eigenspace_dimension={fixed_kernel_dim}")
    print(f"twisted_projection_ranks={twisted_ranks}")
    print(f"twisted_eigenspace_dimensions={twisted_eigenspace_dims}")
    print(f"twisted_fixed_intersection_dimensions={fixed_intersection_dims}")
    print(f"twisted_projection_eigen_failures={eigen_failures}")
    print(f"random_twisted_projection_nonzero={random_nonzeroes}/{random_trials}")
    print(f"fixed_seed_twisted_projection_zero={fixed_seed_zeroes}/6")
    print("interpretation")
    print("  semilinear_covariance_alone_does_not_force_zero=1")
    print("  semilinear_covariance_places_sum_in_nontrivial_frobenius_eigenspace=1")
    print("  descent_to_rho_fixed_left_field_forces_zero=1")
    print("  p24_remaining_theorem_is_covariance_plus_descent_of_packet_product_sum=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate")

    if (factor_count, factor_degree, rho_order_on_e) != (70, 5549, ORDER7):
        raise SystemExit(1)
    if not rho_left_fixed or rho_right_log_mod7 == 0 or rho_factor_step != 10:
        raise SystemExit(1)
    if fixed_kernel_dim != 1:
        raise SystemExit(1)
    if twisted_ranks != [1] * 6 or twisted_eigenspace_dims != [1] * 6:
        raise SystemExit(1)
    if fixed_intersection_dims != [0] * 6:
        raise SystemExit(1)
    if eigen_failures != 0:
        raise SystemExit(1)
    if random_nonzeroes == 0 or fixed_seed_zeroes != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
