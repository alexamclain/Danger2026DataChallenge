#!/usr/bin/env python3
"""Jacobi-carry C/E-centering gate for the p24 bidegree target.

The plain Stickelberger distribution leaks in the forbidden bidegrees

    C_7^nontrivial x {trivial C_179 character}.

But a Jacobi sum divisor is a carry/coboundary

    theta_{u,v}(t) = [ut]_N + [vt]_N - [(u+v)t]_N,    N=7*179,

not a single Stickelberger distribution.  This gate checks the exact finite
Fourier support of that carry.  The positive finding is narrow but real:
when one Jacobi input is right-trivial and C-nontrivial, and the other input
does not make the C-character disappear, the carry has zero forbidden
bidegrees.  Generic Jacobi carries still leak.

Thus a Jacobi-sum proof is not ruled out; it must realize the weighted
trace-GCD obstruction as a combination of C-axis Jacobi carries, not as a
plain or generic Stickelberger element.
"""

from __future__ import annotations

import random


FIELD_Q = 32579  # 32579 - 1 = 26 * 7 * 179.
RIGHT_DEGREE = 7
C_DEGREE = 179
N = RIGHT_DEGREE * C_DEGREE
TRIALS = 48
SEED = 20260607


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


def crt(right_index: int, c_index: int) -> int:
    return (
        right_index * C_DEGREE * pow(C_DEGREE, -1, RIGHT_DEGREE)
        + c_index * RIGHT_DEGREE * pow(RIGHT_DEGREE, -1, C_DEGREE)
    ) % N


POINTS = [
    [crt(right_index, c_index) for c_index in range(C_DEGREE)]
    for right_index in range(RIGHT_DEGREE)
]


def stickelberger_values(multiplier: int) -> list[list[int]]:
    return [
        [(multiplier * POINTS[right][c_pos]) % N for c_pos in range(C_DEGREE)]
        for right in range(RIGHT_DEGREE)
    ]


def jacobi_carry_values(u_value: int, v_value: int) -> list[list[int]]:
    return [
        [
            (
                (u_value * POINTS[right][c_pos]) % N
                + (v_value * POINTS[right][c_pos]) % N
                - ((u_value + v_value) * POINTS[right][c_pos]) % N
            )
            % FIELD_Q
            for c_pos in range(C_DEGREE)
        ]
        for right in range(RIGHT_DEGREE)
    ]


def forbidden_coefficients(values: list[list[int]], omega_right: int) -> list[int]:
    row_sums = [sum(row) % FIELD_Q for row in values]
    return [
        sum(
            row_sums[right] * pow(omega_right, (-character * right) % RIGHT_DEGREE, FIELD_Q)
            for right in range(RIGHT_DEGREE)
        )
        % FIELD_Q
        for character in range(1, RIGHT_DEGREE)
    ]


def forbidden_zero(values: list[list[int]], omega_right: int) -> bool:
    return all(value == 0 for value in forbidden_coefficients(values, omega_right))


def random_c_axis(rng: random.Random) -> int:
    return RIGHT_DEGREE * rng.randrange(1, C_DEGREE)


def random_pure_right(rng: random.Random) -> int:
    return C_DEGREE * rng.randrange(1, RIGHT_DEGREE)


def random_generic(rng: random.Random) -> int:
    while True:
        value = rng.randrange(1, N)
        if value % RIGHT_DEGREE and value % C_DEGREE:
            return value


def random_generic_avoiding_c_cancel(rng: random.Random, c_axis: int) -> int:
    while True:
        value = random_generic(rng)
        if (value + c_axis) % C_DEGREE:
            return value


def random_generic_forcing_c_cancel(rng: random.Random, c_axis: int) -> int:
    target_c = (-c_axis) % C_DEGREE
    while True:
        right = rng.randrange(1, RIGHT_DEGREE)
        value = crt(right, target_c)
        if value % RIGHT_DEGREE and value % C_DEGREE and (value + c_axis) % C_DEGREE == 0:
            return value


def count_nonzero(values: list[int]) -> int:
    return sum(1 for value in values if value)


def main() -> None:
    root = primitive_root(FIELD_Q)
    omega_right = pow(root, (FIELD_Q - 1) // RIGHT_DEGREE, FIELD_Q)
    omega_c = pow(root, (FIELD_Q - 1) // C_DEGREE, FIELD_Q)
    if pow(omega_right, RIGHT_DEGREE, FIELD_Q) != 1 or omega_right == 1:
        raise RuntimeError("right root does not have order 7")
    if pow(omega_c, C_DEGREE, FIELD_Q) != 1 or omega_c == 1:
        raise RuntimeError("C root does not have order 179")
    if sum(pow(omega_right, i, FIELD_Q) for i in range(RIGHT_DEGREE)) % FIELD_Q:
        raise RuntimeError("right root is not cyclotomic")
    if sum(pow(omega_c, i, FIELD_Q) for i in range(C_DEGREE)) % FIELD_Q:
        raise RuntimeError("C root is not cyclotomic")

    rng = random.Random(SEED)

    plain_stickelberger_leaks = count_nonzero(
        forbidden_coefficients(stickelberger_values(1), omega_right)
    )
    c_axis_jacobi_forbidden_zero = 0
    both_c_axis_forbidden_zero = 0
    generic_jacobi_forbidden_leaks = 0
    c_axis_pure_right_partner_leaks = 0
    c_axis_sum_pure_right_leaks = 0

    for _trial in range(TRIALS):
        c_axis = random_c_axis(rng)
        generic = random_generic_avoiding_c_cancel(rng, c_axis)
        c_axis_jacobi_forbidden_zero += int(
            forbidden_zero(jacobi_carry_values(c_axis, generic), omega_right)
        )

        another_c_axis = random_c_axis(rng)
        both_c_axis_forbidden_zero += int(
            forbidden_zero(jacobi_carry_values(c_axis, another_c_axis), omega_right)
        )

        u_generic = random_generic(rng)
        v_generic = random_generic_avoiding_c_cancel(rng, u_generic)
        generic_jacobi_forbidden_leaks += int(
            not forbidden_zero(jacobi_carry_values(u_generic, v_generic), omega_right)
        )

        pure_right = random_pure_right(rng)
        c_axis_pure_right_partner_leaks += int(
            not forbidden_zero(jacobi_carry_values(c_axis, pure_right), omega_right)
        )

        c_cancel = random_generic_forcing_c_cancel(rng, c_axis)
        c_axis_sum_pure_right_leaks += int(
            not forbidden_zero(jacobi_carry_values(c_axis, c_cancel), omega_right)
        )

    sample_positive = forbidden_coefficients(jacobi_carry_values(7, 1), omega_right)
    sample_generic = forbidden_coefficients(jacobi_carry_values(1, 1), omega_right)
    sample_pure_right = forbidden_coefficients(jacobi_carry_values(7, 179), omega_right)

    print("Trace-GCD fixed-frequency p24 Jacobi-carry C-centering gate")
    print(f"field_q={FIELD_Q}")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"c_degree={C_DEGREE}")
    print(f"product_degree={N}")
    print(f"omega_right={omega_right}")
    print(f"omega_c={omega_c}")
    print(f"plain_stickelberger_forbidden_nonzero={plain_stickelberger_leaks}/6")
    print(f"sample_c_axis_jacobi_forbidden_coefficients={sample_positive}")
    print(f"sample_generic_jacobi_forbidden_coefficients={sample_generic}")
    print(f"sample_c_axis_pure_right_forbidden_coefficients={sample_pure_right}")
    print(f"c_axis_jacobi_forbidden_zero={c_axis_jacobi_forbidden_zero}/{TRIALS}")
    print(f"both_c_axis_jacobi_forbidden_zero={both_c_axis_forbidden_zero}/{TRIALS}")
    print(f"generic_jacobi_forbidden_leaks={generic_jacobi_forbidden_leaks}/{TRIALS}")
    print(f"c_axis_pure_right_partner_leaks={c_axis_pure_right_partner_leaks}/{TRIALS}")
    print(f"c_axis_sum_pure_right_leaks={c_axis_sum_pure_right_leaks}/{TRIALS}")
    print("interpretation")
    print("  jacobi_carry_with_C_axis_input_kills_forbidden_bidegrees=1")
    print("  generic_jacobi_carry_still_leaks_forbidden_bidegrees=1")
    print("  pure_right_partner_destroys_C_axis_cancellation=1")
    print("  jacobi_sum_route_must_use_C_axis_character_support=1")
    print("  positive_proof_target_is_C_axis_jacobi_carry_decomposition=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate")

    if plain_stickelberger_leaks != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if any(sample_positive):
        raise SystemExit(1)
    if count_nonzero(sample_generic) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if count_nonzero(sample_pure_right) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if c_axis_jacobi_forbidden_zero != TRIALS:
        raise SystemExit(1)
    if both_c_axis_forbidden_zero != TRIALS:
        raise SystemExit(1)
    if generic_jacobi_forbidden_leaks != TRIALS:
        raise SystemExit(1)
    if c_axis_pure_right_partner_leaks != TRIALS:
        raise SystemExit(1)
    if c_axis_sum_pure_right_leaks != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
