#!/usr/bin/env python3
"""Product-coboundary gate for the p24 raw trace-resolvent term.

The raw p24 term has product shape

    x = T_left * R_right.

A useful noncircular way to produce the raw full-order coboundary is a
Leibniz-style identity.  If

    sigma(A) = alpha*A
    B = sigma(V) - (epsilon/alpha)*V,

then

    A*B = alpha^(-1) * (sigma(A*V) - epsilon*(A*V)).

So it is enough to construct a matching twisted potential for the right
factor, provided the left factor has a known sigma-eigen/covariance multiplier.
This script checks that algebra over a split cyclic model and records two
failure modes: a wrong twist, or a random right factor, does not generically
produce the needed raw coboundary.
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

FIELD_Q = 421  # 420 is divisible by 105, so the split cyclic model has mu_105.
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


def mul(left: Vector, right: Vector) -> Vector:
    return [(a * b) % FIELD_Q for a, b in zip(left, right)]


def scalar_mul(scalar: int, vector: Vector) -> Vector:
    return [(scalar * value) % FIELD_Q for value in vector]


def sigma(vector: Vector, power: int = 1) -> Vector:
    shift = power % len(vector)
    if shift == 0:
        return vector[:]
    return vector[-shift:] + vector[:-shift]


def zero() -> Vector:
    return [0] * TOY_TOTAL_DEGREE


def is_zero(vector: Vector) -> bool:
    return all(value % FIELD_Q == 0 for value in vector)


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


def nested_internal_trace(vector: Vector) -> Vector:
    b_over_c = trace_over_powers(
        vector,
        TOY_QUOTIENT_DEGREE * TOY_C_DEGREE,
        TOY_B_OVER_C_DEGREE,
    )
    return trace_over_powers(b_over_c, TOY_QUOTIENT_DEGREE, TOY_C_DEGREE)


def quotient_twisted_trace(vector: Vector, eigenvalue: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_eigenvalue = pow(eigenvalue, -1, FIELD_Q)
    for index in range(TOY_QUOTIENT_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_eigenvalue % FIELD_Q
    return out


def twisted_coboundary(vector: Vector, eigenvalue: int) -> Vector:
    return sub(sigma(vector), scalar_mul(eigenvalue, vector))


def full_twisted_trace(vector: Vector, eigenvalue: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_eigenvalue = pow(eigenvalue, -1, FIELD_Q)
    for index in range(TOY_TOTAL_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_eigenvalue % FIELD_Q
    return out


def eigenvector(exponent: int, omega: int) -> tuple[Vector, int]:
    # With sigma implemented as (sigma f)_i=f_{i-1}, omega^(exponent*i)
    # has eigenvalue omega^(-exponent).
    vector = [
        pow(omega, (exponent * index) % TOY_TOTAL_DEGREE, FIELD_Q)
        for index in range(TOY_TOTAL_DEGREE)
    ]
    eigenvalue = pow(omega, (-exponent) % TOY_TOTAL_DEGREE, FIELD_Q)
    return vector, eigenvalue


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    tensor_factor_count = math.gcd(ord_m, ord_n)
    tensor_factor_degree = ord_n // tensor_factor_count
    rho_mod_n = pow(P24, RHO_EXPONENT, N)
    rho_order_mod_n = int(sp.n_order(rho_mod_n, N))
    rho7_mod_n = pow(P24, RHO_EXPONENT * ORDER7, N)
    rho7_order_mod_n = int(sp.n_order(rho7_mod_n, N))
    logs = right_log_table()
    rho_mod_211 = pow(P24, RHO_EXPONENT, RIGHT)
    rho_h_shift = logs[rho_mod_211] % ORDER7

    root = primitive_root(FIELD_Q)
    omega = pow(root, (FIELD_Q - 1) // TOY_TOTAL_DEGREE, FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q)
    epsilon_values = [pow(zeta7, character, FIELD_Q) for character in range(1, ORDER7)]
    rng = random.Random(SEED)

    product_identity_failures = 0
    product_trace_nonzero = 0
    nested_quotient_trace_nonzero = 0
    wrong_twist_trace_zero = 0
    random_right_trace_zero = 0
    eigen_covariance_failures = 0
    trials = 0

    # Use several left eigencharacters, including the fixed case exponent 0.
    left_exponents = [0, 1, 5, 17]
    for epsilon in epsilon_values:
        for exponent in left_exponents:
            left, alpha = eigenvector(exponent, omega)
            eigen_covariance_failures += int(sigma(left) != scalar_mul(alpha, left))
            matching_twist = epsilon * pow(alpha, -1, FIELD_Q) % FIELD_Q
            wrong_twist = matching_twist * zeta7 % FIELD_Q
            for _trial in range(2):
                right_potential = random_vector(rng)
                right_factor = twisted_coboundary(right_potential, matching_twist)
                product = mul(left, right_factor)
                product_potential = scalar_mul(pow(alpha, -1, FIELD_Q), mul(left, right_potential))
                expected_product = twisted_coboundary(product_potential, epsilon)

                product_identity_failures += int(product != expected_product)
                product_trace_nonzero += int(not is_zero(full_twisted_trace(product, epsilon)))
                nested_quotient_trace_nonzero += int(
                    not is_zero(quotient_twisted_trace(nested_internal_trace(product), epsilon))
                )

                wrong_factor = twisted_coboundary(right_potential, wrong_twist)
                wrong_product = mul(left, wrong_factor)
                wrong_twist_trace_zero += int(is_zero(full_twisted_trace(wrong_product, epsilon)))

                random_product = mul(left, random_vector(rng))
                random_right_trace_zero += int(is_zero(full_twisted_trace(random_product, epsilon)))
                trials += 1

    print("Trace-GCD fixed-frequency p24 product coboundary Leibniz gate")
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
    print(f"rho_mod_211={rho_mod_211}")
    print(f"rho_raw_h_quotient_shift={rho_h_shift}")
    print(f"field_q={FIELD_Q}")
    print(f"toy_total_degree={TOY_TOTAL_DEGREE}")
    print(f"toy_quotient_degree={TOY_QUOTIENT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"left_eigen_exponents={left_exponents}")
    print(f"character_count={len(epsilon_values)}")
    print(f"eigen_covariance_failures={eigen_covariance_failures}")
    print(f"product_coboundary_identity_failures={product_identity_failures}")
    print(f"product_full_twisted_trace_nonzero={product_trace_nonzero}/{trials}")
    print(f"nested_quotient_trace_nonzero={nested_quotient_trace_nonzero}/{trials}")
    print(f"wrong_twist_product_trace_zero={wrong_twist_trace_zero}/{trials}")
    print(f"random_right_product_trace_zero={random_right_trace_zero}/{trials}")
    print("interpretation")
    print("  product_coboundary_leibniz_identity_holds=1")
    print("  left_covariance_plus_matching_right_coboundary_suffices=1")
    print("  wrong_twist_does_not_give_required_packet_cancellation=1")
    print("  random_right_factor_does_not_give_required_packet_cancellation=1")
    print("  p24_candidate_source_is_right_resolvent_coboundary_with_matching_twist=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_product_coboundary_leibniz_gate")

    if (tensor_factor_count, tensor_factor_degree) != (70, 5549):
        raise SystemExit(1)
    if rho_order_mod_n != ORDER7 * tensor_factor_degree:
        raise SystemExit(1)
    if rho7_order_mod_n != tensor_factor_degree:
        raise SystemExit(1)
    if rho_h_shift == 0:
        raise SystemExit(1)
    if eigen_covariance_failures or product_identity_failures:
        raise SystemExit(1)
    if product_trace_nonzero or nested_quotient_trace_nonzero:
        raise SystemExit(1)
    if wrong_twist_trace_zero > trials // 4:
        raise SystemExit(1)
    if random_right_trace_zero > trials // 4:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
