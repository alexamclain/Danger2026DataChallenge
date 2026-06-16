#!/usr/bin/env python3
"""p24 factor-cycle cancellation candidate for the order-7 packet sum.

The class-character expansion reduces the H-coset theorem to packet sums

    sum_a T_{1,0,a} R_{chi,-a}.

After adjoining E=F_p(mu_m), each F_p relative packet splits into 70
degree-5549 E-factors.  The p24 arithmetic has a useful exponent:

    rho = p^780.

It fixes the left 157-character, shifts the right H-quotient by a generator,
and shifts the 70 E-factor labels by 10, hence ten cycles of length 7.  If the
E-factor packet contributions satisfy the corresponding Frobenius covariance,
each 7-cycle has a nontrivial order-7 multiplier and its sum is zero.

This script verifies the finite implication and records the exact p24
arithmetic.  It does not prove the CM covariance theorem; that is the next
arithmetic target.
"""

from __future__ import annotations

import random

import sympy as sp


P24 = 10**24 + 7
M = 66254
N = 3107441
LEFT = 157
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
FIELD_Q = 43  # 42 is divisible by 7.
FACTOR_COUNT = 70


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


def cycles(step: int, modulus: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value + step) % modulus
        out.append(orbit)
    return out


def covariant_contributions(
    rng: random.Random,
    zeta7: int,
    character_index: int,
    factor_step: int,
) -> list[int]:
    values = [0] * FACTOR_COUNT
    multiplier = pow(zeta7, character_index, FIELD_Q)
    for orbit in cycles(factor_step, FACTOR_COUNT):
        seed = rng.randrange(1, FIELD_Q)
        current = seed
        for index in orbit:
            values[index] = current
            current = current * multiplier % FIELD_Q
    return values


def random_contributions(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _ in range(FACTOR_COUNT)]


def main() -> None:
    ord_m = int(sp.n_order(P24 % M, M))
    ord_n = int(sp.n_order(P24 % N, N))
    factor_count = int(sp.igcd(ord_m, ord_n))
    factor_degree = ord_n // factor_count
    logs = right_log_table()
    p_log = logs[P24 % RIGHT]
    rho_right_log_mod7 = (p_log * RHO_EXPONENT) % ORDER7
    rho_factor_step = RHO_EXPONENT % factor_count
    rho_factor_cycles = cycles(rho_factor_step, factor_count)
    rho_left_fixed = pow(P24, RHO_EXPONENT, LEFT) == 1
    rho_order_on_factor_quotient = len(rho_factor_cycles[0])
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    rng = random.Random(20260606)

    covariant_zeroes = 0
    random_nonzeroes = 0
    for character_index in range(1, ORDER7):
        values = covariant_contributions(rng, zeta7, character_index, rho_factor_step)
        covariant_zeroes += int(sum(values) % FIELD_Q == 0)
        random_nonzeroes += int(sum(random_contributions(rng)) % FIELD_Q != 0)

    print("Trace-GCD fixed-frequency p24 factor-cycle cancellation candidate")
    print(f"p24={P24}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m_p={ord_m}")
    print(f"ord_n_p={ord_n}")
    print(f"tensor_factor_count_over_E={factor_count}")
    print(f"tensor_factor_degree_over_E={factor_degree}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_left157_fixed={int(rho_left_fixed)}")
    print(f"rho_right_h_quotient_shift={rho_right_log_mod7}")
    print(f"rho_factor_step_mod_70={rho_factor_step}")
    print(f"rho_factor_cycle_count={len(rho_factor_cycles)}")
    print(f"rho_factor_cycle_length={rho_order_on_factor_quotient}")
    print(f"rho_factor_cycles_cover_70={int(sum(len(orbit) for orbit in rho_factor_cycles) == factor_count)}")
    print(f"field_q={FIELD_Q}")
    print(f"covariant_character_sums_zero={covariant_zeroes}/6")
    print(f"random_character_sums_nonzero={random_nonzeroes}/6")
    print("interpretation")
    print("  p780_fixes_left157_and_cycles_right_order7_quotient=1")
    print("  p780_cycles_70_E_tensor_factors_as_ten_7_cycles=1")
    print("  scalar_covariant_factor_cycle_contributions_cancel=1")
    print("  semilinear_case_requires_descent_gate=1")
    print("  random_factor_contributions_do_not_cancel=1")
    print("  remaining_theorem_is_p24_factor_cycle_covariance_plus_descent=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate")

    if factor_count != FACTOR_COUNT or factor_degree != 5549:
        raise SystemExit(1)
    if not rho_left_fixed or rho_right_log_mod7 == 0:
        raise SystemExit(1)
    if rho_factor_step != 10 or len(rho_factor_cycles) != 10:
        raise SystemExit(1)
    if rho_order_on_factor_quotient != ORDER7:
        raise SystemExit(1)
    if covariant_zeroes != 6 or random_nonzeroes != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
