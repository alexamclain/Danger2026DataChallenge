#!/usr/bin/env python3
"""Nested internal-trace gate for the p24 quotient Hilbert-90 target.

The previous internal-trace gate showed that a length-7 quotient Hilbert-90
potential applies only after tracing a raw p^780 factor cycle through the
internal degree 5549 action.  For p24 this internal degree is not featureless:

    5549 = 31 * 179,
    B/E degree = 5549,
    C/E degree = 179,
    B/C degree = 31.

This script checks the exact operator factorization in a small cyclic vector
model with the same three-stage shape 7 * 5 * 3:

    Tr_full,epsilon
      = Tr_quot,epsilon o Tr_C/E o Tr_B/C.

It also records the failure modes: applying the length-7 quotient trace after
only one partial internal trace is not the p24 theorem.  The CM/Lang proof
must produce the nested internal trace/norm stage, then the quotient
Hilbert-90 potential.
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
    tau_step = TOY_QUOTIENT_DEGREE * TOY_C_DEGREE
    return trace_over_powers(vector, tau_step, TOY_B_OVER_C_DEGREE)


def trace_c_over_e(vector: Vector) -> Vector:
    tau_step = TOY_QUOTIENT_DEGREE
    return trace_over_powers(vector, tau_step, TOY_C_DEGREE)


def trace_internal_direct(vector: Vector) -> Vector:
    tau_step = TOY_QUOTIENT_DEGREE
    return trace_over_powers(
        vector,
        tau_step,
        TOY_C_DEGREE * TOY_B_OVER_C_DEGREE,
    )


def quotient_twisted_trace(vector: Vector, eigenvalue: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_eigenvalue = pow(eigenvalue, -1, FIELD_Q)
    for index in range(TOY_QUOTIENT_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_eigenvalue % FIELD_Q
    return out


def full_twisted_trace(vector: Vector, eigenvalue: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_eigenvalue = pow(eigenvalue, -1, FIELD_Q)
    for index in range(TOY_TOTAL_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_eigenvalue % FIELD_Q
    return out


def is_fixed_by(vector: Vector, power: int) -> bool:
    return sigma(vector, power) == vector


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

    nested_internal_failures = 0
    full_factorization_failures = 0
    b_only_quotient_mismatches = 0
    c_only_quotient_mismatches = 0
    direct_internal_not_tau_fixed = 0
    b_trace_not_tau_c_fixed = 0
    b_trace_not_tau_fixed = 0
    c_trace_not_tau_fixed = 0
    trials = 0

    for eigenvalue in eigenvalues:
        for _trial in range(8):
            vector = random_vector(rng)
            b_trace = trace_b_over_c(vector)
            c_trace = trace_c_over_e(vector)
            nested_internal = trace_c_over_e(b_trace)
            direct_internal = trace_internal_direct(vector)
            full_trace = full_twisted_trace(vector, eigenvalue)
            quotient_after_nested = quotient_twisted_trace(nested_internal, eigenvalue)
            quotient_after_b_only = quotient_twisted_trace(b_trace, eigenvalue)
            quotient_after_c_only = quotient_twisted_trace(c_trace, eigenvalue)

            nested_internal_failures += int(nested_internal != direct_internal)
            full_factorization_failures += int(quotient_after_nested != full_trace)
            b_only_quotient_mismatches += int(quotient_after_b_only != full_trace)
            c_only_quotient_mismatches += int(quotient_after_c_only != full_trace)
            direct_internal_not_tau_fixed += int(
                not is_fixed_by(direct_internal, TOY_QUOTIENT_DEGREE)
            )
            b_trace_not_tau_c_fixed += int(
                not is_fixed_by(
                    b_trace,
                    TOY_QUOTIENT_DEGREE * TOY_C_DEGREE,
                )
            )
            b_trace_not_tau_fixed += int(not is_fixed_by(b_trace, TOY_QUOTIENT_DEGREE))
            c_trace_not_tau_fixed += int(not is_fixed_by(c_trace, TOY_QUOTIENT_DEGREE))
            trials += 1

    print("Trace-GCD fixed-frequency p24 nested internal-trace gate")
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
    print(f"p24_trace_subgroup_generator={trace_subgroup_generator}")
    print(f"p24_trace_subgroup_order={trace_subgroup_order}")
    print(f"rho_mod_211={rho_mod_211}")
    print(f"rho_raw_h_quotient_shift={rho_h_shift}")
    print(f"toy_q={FIELD_Q}")
    print(f"toy_quotient_degree={TOY_QUOTIENT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"toy_total_degree={TOY_TOTAL_DEGREE}")
    print(f"toy_character_count={len(eigenvalues)}")
    print(f"nested_internal_trace_equals_direct_failures={nested_internal_failures}")
    print(f"full_trace_equals_quotient_after_nested_internal_failures={full_factorization_failures}")
    print(f"quotient_after_B_over_C_only_mismatches={b_only_quotient_mismatches}/{trials}")
    print(f"quotient_after_C_over_E_only_mismatches={c_only_quotient_mismatches}/{trials}")
    print(f"direct_internal_trace_not_tau_fixed={direct_internal_not_tau_fixed}/{trials}")
    print(f"B_over_C_trace_not_tau_C_fixed={b_trace_not_tau_c_fixed}/{trials}")
    print(f"B_over_C_trace_not_tau_fixed={b_trace_not_tau_fixed}/{trials}")
    print(f"C_over_E_trace_not_tau_fixed={c_trace_not_tau_fixed}/{trials}")
    print("interpretation")
    print("  p24_internal_degree_5549_splits_as_31_times_179=1")
    print("  internal_trace_factors_as_C_over_E_after_B_over_C=1")
    print("  quotient_hilbert90_applies_after_nested_internal_trace=1")
    print("  partial_internal_trace_is_not_enough_for_quotient_hilbert90=1")
    print("  cm_lang_target_is_nested_internal_trace_then_quotient_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_nested_internal_trace_gate")

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
    if nested_internal_failures or full_factorization_failures:
        raise SystemExit(1)
    if direct_internal_not_tau_fixed or b_trace_not_tau_c_fixed:
        raise SystemExit(1)
    if b_only_quotient_mismatches < trials // 2:
        raise SystemExit(1)
    if c_only_quotient_mismatches < trials // 2:
        raise SystemExit(1)
    if b_trace_not_tau_fixed < trials // 2:
        raise SystemExit(1)
    if c_trace_not_tau_fixed < trials // 2:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
