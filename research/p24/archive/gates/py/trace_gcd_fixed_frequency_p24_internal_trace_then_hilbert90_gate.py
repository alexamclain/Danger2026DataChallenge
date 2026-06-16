#!/usr/bin/env python3
"""Internal-trace boundary for the p24 twisted Hilbert-90 target.

The p^780 action does two things at once:

* it shifts the 70 E-factors by +10, giving ten visible cycles of length 7;
* after seven steps, p^5460 returns to the same factor and acts internally
  with order 5549 = 31*179.

So a length-7 twisted Hilbert-90 potential is valid only after the
degree-5549 internal factor contribution has been traced/normed down to an
E-valued seed.  On raw factor components the relevant Frobenius has order
38843 = 7*5549, and the correct trace is the full twisted trace.

This script checks the finite identity in a small model with total order
21 = 7*3:

    Tr_full,epsilon(x)
      = Tr_quot,epsilon(Tr_internal(x)),

where Tr_internal sums the sigma^7 orbit.  It also records the failure mode:
the naive length-7 quotient trace of a raw, not internally descended element
is not the full trace.
"""

from __future__ import annotations

import math
import random

import sympy as sp

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus


P24 = 10**24 + 7
M = 66254
N = 3107441
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
TOY_Q = 43
TOY_INTERNAL_DEGREE = 3
TOY_DEGREE = ORDER7 * TOY_INTERNAL_DEGREE
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


def kernel_dimension(field: ExtensionField, matrix: list[list[int]]) -> int:
    return field.degree - rank_mod(matrix, field.q)


def internal_trace(value: FpE, field: ExtensionField) -> FpE:
    out = field.zero
    for step in range(TOY_INTERNAL_DEGREE):
        out = field.add(out, frobenius_power(value, ORDER7 * step, field))
    return out


def quotient_twisted_trace(value: FpE, eigenvalue: int, field: ExtensionField) -> FpE:
    out = field.zero
    coeff = 1
    inv_eigen = pow(eigenvalue, -1, field.q)
    for step in range(ORDER7):
        out = field.add(
            out,
            field.scalar_mul(coeff, frobenius_power(value, step, field)),
        )
        coeff = coeff * inv_eigen % field.q
    return out


def full_twisted_trace(value: FpE, eigenvalue: int, field: ExtensionField) -> FpE:
    out = field.zero
    coeff = 1
    inv_eigen = pow(eigenvalue, -1, field.q)
    for step in range(TOY_DEGREE):
        out = field.add(
            out,
            field.scalar_mul(coeff, frobenius_power(value, step, field)),
        )
        coeff = coeff * inv_eigen % field.q
    return out


def full_coboundary(value: FpE, eigenvalue: int, field: ExtensionField) -> FpE:
    return field.sub(frobenius(value, field), field.scalar_mul(eigenvalue, value))


def quotient_fixed_space_matrix(field: ExtensionField) -> list[list[int]]:
    return linear_map_matrix(
        field,
        lambda value: field.sub(frobenius_power(value, ORDER7, field), value),
    )


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = tuple(rng.randrange(field.q) for _ in range(field.degree))
        if value != field.zero:
            return value


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    factor_count = math.gcd(ord_m, ord_n)
    factor_degree = ord_n // factor_count
    rho_mod_n = pow(P24, RHO_EXPONENT, N)
    rho_order_mod_n = int(sp.n_order(rho_mod_n, N))
    rho7_mod_n = pow(P24, RHO_EXPONENT * ORDER7, N)
    rho7_order_mod_n = int(sp.n_order(rho7_mod_n, N))
    rho_factor_step = RHO_EXPONENT % factor_count
    rho_factor_cycle_count = math.gcd(factor_count, rho_factor_step)
    rho_factor_cycle_length = factor_count // rho_factor_cycle_count
    logs = right_log_table()
    rho_mod_211 = pow(P24, RHO_EXPONENT, RIGHT)
    rho_h_shift = logs[rho_mod_211] % ORDER7

    field = ExtensionField(
        TOY_Q,
        TOY_DEGREE,
        find_irreducible_modulus(TOY_Q, TOY_DEGREE, SEED),
    )
    zeta7 = pow(primitive_root(TOY_Q), (TOY_Q - 1) // ORDER7, TOY_Q)
    eigenvalues = [pow(zeta7, character, TOY_Q) for character in range(1, ORDER7)]
    rng = random.Random(SEED)

    factorization_failures = 0
    naive_quotient_mismatches = 0
    internal_trace_not_fixed = 0
    full_trace_ranks: list[int] = []
    full_coboundary_ranks: list[int] = []
    full_trace_kernel_dims: list[int] = []
    quotient_fixed_dim = kernel_dimension(field, quotient_fixed_space_matrix(field))
    internal_trace_ranks = rank_mod(
        linear_map_matrix(field, lambda value: internal_trace(value, field)),
        TOY_Q,
    )
    random_trials = 0

    for eigenvalue in eigenvalues:
        full_trace_matrix = linear_map_matrix(
            field,
            lambda value, eigenvalue=eigenvalue: full_twisted_trace(value, eigenvalue, field),
        )
        full_coboundary_matrix = linear_map_matrix(
            field,
            lambda value, eigenvalue=eigenvalue: full_coboundary(value, eigenvalue, field),
        )
        full_trace_ranks.append(rank_mod(full_trace_matrix, TOY_Q))
        full_coboundary_ranks.append(rank_mod(full_coboundary_matrix, TOY_Q))
        full_trace_kernel_dims.append(kernel_dimension(field, full_trace_matrix))

        for _trial in range(8):
            value = random_element(rng, field)
            traced = internal_trace(value, field)
            factorized = quotient_twisted_trace(traced, eigenvalue, field)
            full = full_twisted_trace(value, eigenvalue, field)
            naive = quotient_twisted_trace(value, eigenvalue, field)
            factorization_failures += int(factorized != full)
            naive_quotient_mismatches += int(naive != full)
            internal_trace_not_fixed += int(
                frobenius_power(traced, ORDER7, field) != traced
            )
            random_trials += 1

    print("Trace-GCD fixed-frequency p24 internal-trace then Hilbert-90 gate")
    print(f"p24={P24}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m_p={ord_m}")
    print(f"ord_n_p={ord_n}")
    print(f"tensor_factor_count_over_E={factor_count}")
    print(f"tensor_factor_degree_over_E={factor_degree}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_n={rho_mod_n}")
    print(f"rho_order_mod_n={rho_order_mod_n}")
    print(f"rho7_mod_n={rho7_mod_n}")
    print(f"rho7_order_mod_n={rho7_order_mod_n}")
    print(f"rho_mod_211={rho_mod_211}")
    print(f"rho_raw_h_quotient_shift={rho_h_shift}")
    print(f"rho_factor_step_mod_70={rho_factor_step}")
    print(f"rho_factor_cycle_count={rho_factor_cycle_count}")
    print(f"rho_factor_cycle_length={rho_factor_cycle_length}")
    print(f"toy_q={TOY_Q}")
    print(f"toy_internal_degree={TOY_INTERNAL_DEGREE}")
    print(f"toy_total_degree={TOY_DEGREE}")
    print(f"toy_character_count={len(eigenvalues)}")
    print(f"quotient_fixed_space_dimension={quotient_fixed_dim}")
    print(f"internal_trace_rank={internal_trace_ranks}")
    print(f"full_twisted_trace_ranks={full_trace_ranks}")
    print(f"full_coboundary_ranks={full_coboundary_ranks}")
    print(f"full_twisted_trace_kernel_dimensions={full_trace_kernel_dims}")
    print(f"full_trace_equals_quotient_trace_after_internal_trace_failures={factorization_failures}")
    print(f"naive_quotient_trace_on_raw_seed_mismatches={naive_quotient_mismatches}/{random_trials}")
    print(f"internal_trace_not_fixed_by_sigma7={internal_trace_not_fixed}/{random_trials}")
    print("interpretation")
    print("  p780_raw_factor_action_has_order_38843_not_7=1")
    print("  seven_cycle_hilbert90_requires_internal_trace_to_E_seed=1")
    print("  full_twisted_trace_factors_as_internal_trace_then_quotient_trace=1")
    print("  naive_length7_trace_on_raw_factor_component_is_invalid=1")
    print("  cm_lang_target_must_supply_internal_trace_or_full_order_coboundary=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate")

    if (factor_count, factor_degree) != (70, 5549):
        raise SystemExit(1)
    if rho_order_mod_n != ORDER7 * factor_degree:
        raise SystemExit(1)
    if rho7_order_mod_n != factor_degree:
        raise SystemExit(1)
    if (rho_factor_cycle_count, rho_factor_cycle_length, rho_factor_step) != (10, 7, 10):
        raise SystemExit(1)
    if rho_h_shift == 0:
        raise SystemExit(1)
    if quotient_fixed_dim != ORDER7 or internal_trace_ranks != ORDER7:
        raise SystemExit(1)
    if full_trace_ranks != [1] * (ORDER7 - 1):
        raise SystemExit(1)
    if full_coboundary_ranks != [TOY_DEGREE - 1] * (ORDER7 - 1):
        raise SystemExit(1)
    if full_trace_kernel_dims != [TOY_DEGREE - 1] * (ORDER7 - 1):
        raise SystemExit(1)
    if factorization_failures or internal_trace_not_fixed:
        raise SystemExit(1)
    if naive_quotient_mismatches < random_trials // 2:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
