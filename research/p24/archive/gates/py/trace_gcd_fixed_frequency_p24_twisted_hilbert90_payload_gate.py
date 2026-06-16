#!/usr/bin/env python3
"""Twisted Hilbert-90 payload gate for the p24 factor-cycle theorem.

The current p24 route says that a Gauss-normalized order-7 packet contribution
has nontrivial Frobenius eigenvalue after summing a 7-cycle of E-factors.  This
script records the equivalent potential form on one factor cycle.

For sigma of order 7 and a nontrivial seventh root eigen != 1, define

    Tr_eigen(x) = sum_{i=0}^6 eigen^(-i) sigma^i(x)
    D_eigen(y)  = sigma(y) - eigen*y.

Then

    im(D_eigen) = ker(Tr_eigen).

So the p24 arithmetic theorem can be sharpened to: for each nontrivial right
quotient character and each of the ten p^780 factor cycles, the
Gauss-normalized seed contribution is a D_eigen-coboundary in the embedded
degree-7 factor-cycle algebra.  Equivalently, its twisted trace descends to
the p^780-fixed left field, hence vanishes because the eigenvalue is
nontrivial.

This is finite linear algebra only; it does not prove the CM/Lang coboundary.
It records the exact potential identity that would be enough.
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


FpE = tuple[int, ...]


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


def basis_vector(index: int, degree: int) -> FpE:
    return tuple(1 if i == index else 0 for i in range(degree))


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def frobenius_power(value: FpE, times: int, field: ExtensionField) -> FpE:
    out = value
    for _ in range(times):
        out = frobenius(out, field)
    return out


def linear_map_matrix(field: ExtensionField, fn) -> list[list[int]]:
    columns = [fn(basis_vector(index, field.degree)) for index in range(field.degree)]
    return [[columns[col][row] for col in range(field.degree)] for row in range(field.degree)]


def subtract_matrices(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    return [
        [(left_value - right_value) % q for left_value, right_value in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def mat_vec(matrix: list[list[int]], vector: FpE, q: int) -> FpE:
    return tuple(
        sum(value * vector[col] for col, value in enumerate(row)) % q
        for row in matrix
    )


def kernel_dimension(field: ExtensionField, matrix: list[list[int]]) -> int:
    return field.degree - rank_mod(matrix, field.q)


def twisted_trace(value: FpE, eigenvalue: int, field: ExtensionField) -> FpE:
    out = field.zero
    coeff = 1
    inv_eigen = pow(eigenvalue, -1, field.q)
    for power in range(ORDER7):
        out = field.add(
            out,
            field.scalar_mul(coeff, frobenius_power(value, power, field)),
        )
        coeff = coeff * inv_eigen % field.q
    return out


def twisted_coboundary(value: FpE, eigenvalue: int, field: ExtensionField) -> FpE:
    return field.sub(frobenius(value, field), field.scalar_mul(eigenvalue, value))


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = tuple(rng.randrange(field.q) for _ in range(field.degree))
        if value != field.zero:
            return value


def is_fixed(value: FpE, field: ExtensionField) -> bool:
    return frobenius(value, field) == value


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    factor_count = math.gcd(ord_m, ord_n)
    factor_degree = ord_n // factor_count
    rho_order_on_e = ord_m // math.gcd(ord_m, RHO_EXPONENT)
    rho_left_fixed = pow(P24, RHO_EXPONENT, LEFT) == 1
    logs = right_log_table()
    p_log = logs[P24 % RIGHT]
    rho = pow(P24, RHO_EXPONENT, RIGHT)
    rho_raw_h_shift = logs[rho] % ORDER7
    rho_factor_step = RHO_EXPONENT % factor_count
    rho_factor_cycle_count = math.gcd(factor_count, rho_factor_step)
    rho_factor_cycle_length = factor_count // rho_factor_cycle_count

    field = ExtensionField(
        FIELD_Q,
        FIELD_DEGREE,
        find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED),
    )
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    # The theorem can use either orientation; using inverse characters here
    # matches the convention sigma(Tr_eigen(x)) = eigen * Tr_eigen(x).
    eigenvalues = [pow(pow(zeta7, character, FIELD_Q), -1, FIELD_Q) for character in range(1, ORDER7)]
    rng = random.Random(SEED)

    trace_ranks: list[int] = []
    coboundary_ranks: list[int] = []
    trace_kernel_dims: list[int] = []
    coboundary_kernel_dims: list[int] = []
    image_subset_kernel_failures = 0
    image_equals_kernel_failures = 0
    trace_eigen_failures = 0
    random_trace_nonzero = 0
    random_trace_zero = 0
    random_trace_fixed_nonzero = 0
    coboundary_trace_zero = 0
    trials = 0

    for eigenvalue in eigenvalues:
        trace_matrix = linear_map_matrix(
            field,
            lambda value, eigenvalue=eigenvalue: twisted_trace(value, eigenvalue, field),
        )
        coboundary_matrix = linear_map_matrix(
            field,
            lambda value, eigenvalue=eigenvalue: twisted_coboundary(value, eigenvalue, field),
        )
        trace_rank = rank_mod(trace_matrix, FIELD_Q)
        coboundary_rank = rank_mod(coboundary_matrix, FIELD_Q)
        trace_kernel_dim = kernel_dimension(field, trace_matrix)
        coboundary_kernel_dim = kernel_dimension(field, coboundary_matrix)
        trace_ranks.append(trace_rank)
        coboundary_ranks.append(coboundary_rank)
        trace_kernel_dims.append(trace_kernel_dim)
        coboundary_kernel_dims.append(coboundary_kernel_dim)

        for basis_index in range(field.degree):
            vector = basis_vector(basis_index, field.degree)
            trace_value = twisted_trace(vector, eigenvalue, field)
            if frobenius(trace_value, field) != field.scalar_mul(eigenvalue, trace_value):
                trace_eigen_failures += 1
            coboundary_value = twisted_coboundary(vector, eigenvalue, field)
            if twisted_trace(coboundary_value, eigenvalue, field) != field.zero:
                image_subset_kernel_failures += 1

        if trace_kernel_dim != coboundary_rank:
            image_equals_kernel_failures += 1

        for _trial in range(8):
            seed = random_element(rng, field)
            trace_value = twisted_trace(seed, eigenvalue, field)
            trace_is_zero = trace_value == field.zero
            random_trace_nonzero += int(not trace_is_zero)
            random_trace_zero += int(trace_is_zero)
            random_trace_fixed_nonzero += int(
                (not trace_is_zero) and is_fixed(trace_value, field)
            )

            potential = random_element(rng, field)
            coboundary_seed = twisted_coboundary(potential, eigenvalue, field)
            coboundary_trace_zero += int(
                twisted_trace(coboundary_seed, eigenvalue, field) == field.zero
            )
            trials += 1

    print("Trace-GCD fixed-frequency p24 twisted Hilbert-90 payload gate")
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
    print(f"rho_mod_211={rho}")
    print(f"rho_raw_h_quotient_shift={rho_raw_h_shift}")
    print(f"rho_factor_step_mod_70={rho_factor_step}")
    print(f"rho_factor_cycle_count={rho_factor_cycle_count}")
    print(f"rho_factor_cycle_length={rho_factor_cycle_length}")
    print(f"field_q={FIELD_Q}")
    print(f"field_degree={FIELD_DEGREE}")
    print(f"character_count={len(eigenvalues)}")
    print(f"twisted_trace_ranks={trace_ranks}")
    print(f"twisted_coboundary_ranks={coboundary_ranks}")
    print(f"twisted_trace_kernel_dimensions={trace_kernel_dims}")
    print(f"twisted_coboundary_kernel_dimensions={coboundary_kernel_dims}")
    print(f"trace_eigen_failures={trace_eigen_failures}")
    print(f"image_subset_kernel_failures={image_subset_kernel_failures}")
    print(f"image_equals_kernel_failures={image_equals_kernel_failures}")
    print(f"random_twisted_traces_nonzero={random_trace_nonzero}/{trials}")
    print(f"random_twisted_traces_zero={random_trace_zero}/{trials}")
    print(f"random_twisted_traces_fixed_nonzero={random_trace_fixed_nonzero}/{trials}")
    print(f"coboundary_seeds_have_zero_twisted_trace={coboundary_trace_zero}/{trials}")
    print("interpretation")
    print("  twisted_trace_has_rank_one_nontrivial_eigenspace=1")
    print("  twisted_hilbert90_image_equals_trace_kernel=1")
    print("  descended_twisted_trace_would_force_zero=1")
    print("  p24_payload_can_be_stated_as_factor_cycle_coboundary=1")
    print("  cm_lang_work_is_constructing_the_coboundary_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate")

    if (factor_count, factor_degree, rho_order_on_e) != (70, 5549, ORDER7):
        raise SystemExit(1)
    if not rho_left_fixed:
        raise SystemExit(1)
    if (rho_raw_h_shift, rho_factor_step, rho_factor_cycle_count, rho_factor_cycle_length) != (6, 10, 10, 7):
        raise SystemExit(1)
    if trace_ranks != [1] * (ORDER7 - 1):
        raise SystemExit(1)
    if coboundary_ranks != [FIELD_DEGREE - 1] * (ORDER7 - 1):
        raise SystemExit(1)
    if trace_kernel_dims != [FIELD_DEGREE - 1] * (ORDER7 - 1):
        raise SystemExit(1)
    if coboundary_kernel_dims != [1] * (ORDER7 - 1):
        raise SystemExit(1)
    if trace_eigen_failures or image_subset_kernel_failures or image_equals_kernel_failures:
        raise SystemExit(1)
    if random_trace_nonzero < (3 * trials) // 4:
        raise SystemExit(1)
    if random_trace_fixed_nonzero:
        raise SystemExit(1)
    if coboundary_trace_zero != trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
