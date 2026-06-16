#!/usr/bin/env python3
"""Boundary for the p24 matching right-resolvent coboundary.

The product-coboundary route needs a right factor

    R_chi = sigma(V) - epsilon_chi * V.

There is a tempting shortcut: the right multiplicative resolvent already has
formal Frobenius covariance.  This gate records the sign obstruction.  In the
raw convention chi_k(2)=zeta_7^k, Frob_p^780 shifts the right quotient by
6 mod 7, so the coefficient vector of the right resolvent is an eigenvector
with eigenvalue zeta_7^k.  That is exactly the matching twist epsilon_k, so it
lies in the obstruction eigenspace of sigma - epsilon_k rather than in its
image.

The only way this route can still work is if additional CM/Lang arithmetic
kills the obstruction, for example after the internal degree-5549 trace over
the relative packet.  A pure cyclotomic internal trace does not vanish
automatically; its Gaussian periods are nonzero in a small split finite-field
audit.  Thus the missing theorem is real packet/internal-trace cancellation,
not formal right-character covariance.
"""

from __future__ import annotations

import sympy as sp


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
N = 3107441
INTERNAL_DEGREE = 5549
SPLIT_Q_FOR_N = 37289293  # 12*N + 1, prime.
FIELD_Q = 43


Vector = list[int]


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("generator is not primitive")
    return logs


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


def primitive_root_known_factors(q: int, factors: set[int]) -> int:
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root found")


def primitive_root(q: int) -> int:
    return primitive_root_known_factors(q, factor_distinct(q - 1))


def right_character_coefficients(k: int, zeta7: int, logs: dict[int, int]) -> Vector:
    return [
        pow(zeta7, (k * logs[value]) % ORDER7, FIELD_Q)
        for value in range(1, RIGHT)
    ]


def quotient_action(vector: Vector, multiplier: int) -> Vector:
    inverse = pow(multiplier, -1, RIGHT)
    out = [0] * (RIGHT - 1)
    for value in range(1, RIGHT):
        out[value - 1] = vector[(inverse * value % RIGHT) - 1]
    return out


def sub(left: Vector, right: Vector) -> Vector:
    return [(a - b) % FIELD_Q for a, b in zip(left, right)]


def add(left: Vector, right: Vector) -> Vector:
    return [(a + b) % FIELD_Q for a, b in zip(left, right)]


def scalar_mul(scalar: int, vector: Vector) -> Vector:
    return [(scalar * value) % FIELD_Q for value in vector]


def is_zero(vector: Vector) -> bool:
    return all(value % FIELD_Q == 0 for value in vector)


def twisted_trace(vector: Vector, multiplier: int, twist: int) -> Vector:
    out = [0] * (RIGHT - 1)
    coeff = 1
    inverse_twist = pow(twist, -1, FIELD_Q)
    current = vector[:]
    for _index in range(ORDER7):
        out = add(out, scalar_mul(coeff, current))
        coeff = coeff * inverse_twist % FIELD_Q
        current = quotient_action(current, multiplier)
    return out


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
    return rank


def coboundary_matrix(multiplier: int, twist: int) -> list[list[int]]:
    columns: list[Vector] = []
    for index in range(RIGHT - 1):
        basis = [0] * (RIGHT - 1)
        basis[index] = 1
        columns.append(sub(quotient_action(basis, multiplier), scalar_mul(twist, basis)))
    return [[columns[col][row] for col in range(RIGHT - 1)] for row in range(RIGHT - 1)]


def in_column_span(matrix: list[list[int]], target: Vector) -> bool:
    augmented = [row[:] + [target[index]] for index, row in enumerate(matrix)]
    return rank_mod(matrix, FIELD_Q) == rank_mod(augmented, FIELD_Q)


def internal_gaussian_periods_nonzero() -> tuple[int, int, list[int]]:
    if not sp.isprime(SPLIT_Q_FOR_N):
        raise RuntimeError("split q is not prime")
    root = primitive_root_known_factors(SPLIT_Q_FOR_N, {2, 3, N})
    zeta_n = pow(root, (SPLIT_Q_FOR_N - 1) // N, SPLIT_Q_FOR_N)
    q_generator = pow(P24, 5460, N)
    if int(sp.n_order(q_generator, N)) != INTERNAL_DEGREE:
        raise RuntimeError("bad internal generator")
    orbit: list[int] = []
    value = 1
    for _index in range(INTERNAL_DEGREE):
        orbit.append(value)
        value = value * q_generator % N
    samples = [1, 2, 3, 5, 7, 31, 179, 3107440]
    periods = [
        sum(pow(zeta_n, (sample * exponent) % N, SPLIT_Q_FOR_N) for exponent in orbit)
        % SPLIT_Q_FOR_N
        for sample in samples
    ]
    return root, q_generator, periods


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_mod_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_mod_right]
    rho_shift = rho_log % ORDER7
    root = primitive_root(FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q)

    covariance_failures = 0
    matching_trace_zeroes = 0
    matching_coboundary_memberships = 0
    opposite_trace_zeroes = 0
    opposite_coboundary_memberships = 0
    matching_ranks: list[int] = []

    for k in range(1, ORDER7):
        vector = right_character_coefficients(k, zeta7, logs)
        epsilon = pow(zeta7, k, FIELD_Q)
        opposite = pow(epsilon, -1, FIELD_Q)
        acted = quotient_action(vector, rho_mod_right)
        covariance_failures += int(acted != scalar_mul(epsilon, vector))

        matching_matrix = coboundary_matrix(rho_mod_right, epsilon)
        matching_ranks.append(rank_mod(matching_matrix, FIELD_Q))
        matching_trace_zeroes += int(is_zero(twisted_trace(vector, rho_mod_right, epsilon)))
        matching_coboundary_memberships += int(in_column_span(matching_matrix, vector))

        opposite_matrix = coboundary_matrix(rho_mod_right, opposite)
        opposite_trace_zeroes += int(is_zero(twisted_trace(vector, rho_mod_right, opposite)))
        opposite_coboundary_memberships += int(in_column_span(opposite_matrix, vector))

    split_root, q_generator, periods = internal_gaussian_periods_nonzero()
    nonzero_periods = sum(period != 0 for period in periods)

    print("Trace-GCD fixed-frequency p24 right coboundary obstruction gate")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho_mod_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_raw_h_quotient_shift={rho_shift}")
    print(f"field_q={FIELD_Q}")
    print(f"zeta7={zeta7}")
    print(f"right_resolvent_covariance_failures={covariance_failures}")
    print(f"matching_coboundary_ranks={matching_ranks}")
    print(f"matching_twist_trace_zeroes={matching_trace_zeroes}/6")
    print(f"matching_twist_coboundary_memberships={matching_coboundary_memberships}/6")
    print(f"opposite_twist_trace_zeroes={opposite_trace_zeroes}/6")
    print(f"opposite_twist_coboundary_memberships={opposite_coboundary_memberships}/6")
    print(f"split_q_for_internal_n={SPLIT_Q_FOR_N}")
    print(f"split_q_primitive_root={split_root}")
    print(f"internal_q_generator=p^5460_mod_n={q_generator}")
    print(f"internal_gaussian_period_samples={periods}")
    print(f"internal_gaussian_period_nonzeroes={nonzero_periods}/{len(periods)}")
    print("interpretation")
    print("  formal_right_character_covariance_has_matching_eigenvalue=1")
    print("  formal_right_covariance_is_coboundary_obstruction_not_potential=1")
    print("  opposite_twist_would_be_coboundary_but_is_wrong_product_twist=1")
    print("  cyclotomic_internal_trace_does_not_vanish_automatically=1")
    print("  remaining_theorem_needs_cm_lang_internal_trace_cancellation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate")

    if rho_shift != 6:
        raise SystemExit(1)
    if covariance_failures != 0:
        raise SystemExit(1)
    if matching_ranks != [180] * 6:
        raise SystemExit(1)
    if matching_trace_zeroes != 0 or matching_coboundary_memberships != 0:
        raise SystemExit(1)
    if opposite_trace_zeroes != 6 or opposite_coboundary_memberships != 6:
        raise SystemExit(1)
    if nonzero_periods != len(periods):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
