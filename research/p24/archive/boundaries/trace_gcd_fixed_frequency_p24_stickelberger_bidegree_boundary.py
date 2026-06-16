#!/usr/bin/env python3
"""Boundary for plain Stickelberger/Jacobi explanations of the bidegree target.

The current p24 fixed-frequency theorem asks for zero support in the six
forbidden Fourier slots

    C_7^nontrivial x {trivial C/E character},

after the B/C trace.  A tempting next proof slogan is that a cyclotomic
Stickelberger or Jacobi-sum annihilator should kill these slots automatically.
This gate checks the finite Fourier shadow of that slogan on the exact
quotient degrees C_7 x C_179.

It does not rule out a bespoke phase-aware CM/Lang determinant product.  It
does rule out the plain cyclic Stickelberger distribution, and the right-axis
Stickelberger distribution, as automatic sources of the needed support
separation: both have nonzero mass in all six forbidden slots.  Only a
deliberately C-centered product avoids the trivial C-character component, so
any successful Stickelberger/Jacobi proof has to explain that C-centering from
the selected weighted packet itself.
"""

from __future__ import annotations

from math import gcd


FIELD_Q = 32579  # 32579 - 1 = 26 * 7 * 179.
RIGHT_DEGREE = 7
C_DEGREE = 179
PRODUCT_DEGREE = RIGHT_DEGREE * C_DEGREE


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


def dft_coefficient(
    values: list[list[int]],
    right_character: int,
    c_character: int,
    omega_right: int,
    omega_c: int,
) -> int:
    total = 0
    for r in range(RIGHT_DEGREE):
        right_weight = pow(omega_right, (-right_character * r) % RIGHT_DEGREE, FIELD_Q)
        for c in range(C_DEGREE):
            c_weight = pow(omega_c, (-c_character * c) % C_DEGREE, FIELD_Q)
            total = (total + values[r][c] * right_weight * c_weight) % FIELD_Q
    return total


def all_forbidden_coefficients(values: list[list[int]], omega_right: int, omega_c: int) -> list[int]:
    return [
        dft_coefficient(values, right_character, 0, omega_right, omega_c)
        for right_character in range(1, RIGHT_DEGREE)
    ]


def cyclic_stickelberger_distribution(centered: bool) -> list[list[int]]:
    """Fractional-part distribution on C_(7*179), pulled back by CRT labels."""
    values = [[0 for _c in range(C_DEGREE)] for _r in range(RIGHT_DEGREE)]
    mean = (PRODUCT_DEGREE - 1) * pow(2, -1, FIELD_Q) % FIELD_Q
    for exponent in range(PRODUCT_DEGREE):
        value = exponent % FIELD_Q
        if centered:
            value = (value - mean) % FIELD_Q
        values[exponent % RIGHT_DEGREE][exponent % C_DEGREE] = value
    return values


def right_axis_stickelberger_distribution(centered: bool) -> list[list[int]]:
    mean = (RIGHT_DEGREE - 1) * pow(2, -1, FIELD_Q) % FIELD_Q
    values = []
    for r in range(RIGHT_DEGREE):
        value = r % FIELD_Q
        if centered:
            value = (value - mean) % FIELD_Q
        values.append([value for _c in range(C_DEGREE)])
    return values


def c_axis_stickelberger_distribution(centered: bool) -> list[list[int]]:
    mean = (C_DEGREE - 1) * pow(2, -1, FIELD_Q) % FIELD_Q
    values = []
    for _r in range(RIGHT_DEGREE):
        row = []
        for c in range(C_DEGREE):
            value = c % FIELD_Q
            if centered:
                value = (value - mean) % FIELD_Q
            row.append(value)
        values.append(row)
    return values


def centered_product_distribution() -> list[list[int]]:
    right_mean = (RIGHT_DEGREE - 1) * pow(2, -1, FIELD_Q) % FIELD_Q
    c_mean = (C_DEGREE - 1) * pow(2, -1, FIELD_Q) % FIELD_Q
    return [
        [
            ((r - right_mean) * (c - c_mean)) % FIELD_Q
            for c in range(C_DEGREE)
        ]
        for r in range(RIGHT_DEGREE)
    ]


def count_nonzero(values: list[int]) -> int:
    return sum(1 for value in values if value % FIELD_Q)


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

    cyclic_raw = all_forbidden_coefficients(
        cyclic_stickelberger_distribution(centered=False), omega_right, omega_c
    )
    cyclic_centered = all_forbidden_coefficients(
        cyclic_stickelberger_distribution(centered=True), omega_right, omega_c
    )
    right_raw = all_forbidden_coefficients(
        right_axis_stickelberger_distribution(centered=False), omega_right, omega_c
    )
    right_centered = all_forbidden_coefficients(
        right_axis_stickelberger_distribution(centered=True), omega_right, omega_c
    )
    c_centered = all_forbidden_coefficients(
        c_axis_stickelberger_distribution(centered=True), omega_right, omega_c
    )
    product_centered = all_forbidden_coefficients(
        centered_product_distribution(), omega_right, omega_c
    )

    print("Trace-GCD fixed-frequency p24 Stickelberger bidegree boundary")
    print(f"field_q={FIELD_Q}")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"c_degree={C_DEGREE}")
    print(f"product_degree={PRODUCT_DEGREE}")
    print(f"gcd_right_c={gcd(RIGHT_DEGREE, C_DEGREE)}")
    print(f"omega_right={omega_right}")
    print(f"omega_c={omega_c}")
    print(f"cyclic_stickelberger_forbidden_coefficients={cyclic_raw}")
    print(f"cyclic_centered_stickelberger_forbidden_coefficients={cyclic_centered}")
    print(f"right_axis_stickelberger_forbidden_coefficients={right_raw}")
    print(f"right_axis_centered_stickelberger_forbidden_coefficients={right_centered}")
    print(f"c_axis_centered_stickelberger_forbidden_coefficients={c_centered}")
    print(f"centered_product_forbidden_coefficients={product_centered}")
    print(f"cyclic_stickelberger_forbidden_nonzero={count_nonzero(cyclic_raw)}/6")
    print(f"cyclic_centered_stickelberger_forbidden_nonzero={count_nonzero(cyclic_centered)}/6")
    print(f"right_axis_stickelberger_forbidden_nonzero={count_nonzero(right_raw)}/6")
    print(f"right_axis_centered_stickelberger_forbidden_nonzero={count_nonzero(right_centered)}/6")
    print(f"c_axis_centered_stickelberger_forbidden_nonzero={count_nonzero(c_centered)}/6")
    print(f"centered_product_forbidden_nonzero={count_nonzero(product_centered)}/6")
    print("interpretation")
    print("  plain_cyclic_stickelberger_leaks_forbidden_bidegrees=1")
    print("  plain_right_axis_stickelberger_leaks_forbidden_bidegrees=1")
    print("  c_centered_factor_is_needed_to_avoid_trivial_C_component=1")
    print("  successful_jacobi_sum_proof_must_explain_C_centering_from_weighted_packet=1")
    print("  generic_stickelberger_slogan_is_not_the_missing_anchor_theorem=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_stickelberger_bidegree_boundary")

    if gcd(RIGHT_DEGREE, C_DEGREE) != 1:
        raise SystemExit(1)
    if count_nonzero(cyclic_raw) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if count_nonzero(cyclic_centered) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if count_nonzero(right_raw) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if count_nonzero(right_centered) != RIGHT_DEGREE - 1:
        raise SystemExit(1)
    if count_nonzero(c_centered) != 0:
        raise SystemExit(1)
    if count_nonzero(product_centered) != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
