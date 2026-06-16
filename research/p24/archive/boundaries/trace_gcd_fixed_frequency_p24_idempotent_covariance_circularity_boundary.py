#!/usr/bin/env python3
"""Circularity boundary for descended p24 idempotent covariance.

Let Z_delta be the complete 70-idempotent decomposition of an already
descended L-valued projection S.  Since rho=p^780 fixes L and shifts factors
by +10, the formal idempotent action gives

    Z_{delta+10} = rho(Z_delta).

The desired nontrivial covariance

    Z_{delta+10} = lambda * rho(Z_delta),  lambda != 1,

is therefore equivalent to Z_delta=0 for every delta.  So this covariance is
not a consequence of scalar extension plus descent; it is a restatement of the
vanishing unless proved directly from the CM trace-resolvent terms before
complete recombination.
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
FACTOR_COUNT = 70
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


def factor_cycles(step: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(FACTOR_COUNT):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value + step) % FACTOR_COUNT
        out.append(orbit)
    return out


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = tuple(rng.randrange(field.q) for _ in range(field.degree))
        if value != field.zero:
            return value


def descended_components(
    seeds: list[FpE],
    field: ExtensionField,
    factor_step: int,
) -> list[FpE]:
    values = [field.zero] * FACTOR_COUNT
    for seed, orbit in zip(seeds, factor_cycles(factor_step)):
        current = seed
        for factor_index in orbit:
            values[factor_index] = current
            current = frobenius(current, field)
    return values


def covariance_failures(
    values: list[FpE],
    field: ExtensionField,
    factor_step: int,
    scalar: int,
) -> int:
    failures = 0
    for index, value in enumerate(values):
        target = (index + factor_step) % FACTOR_COUNT
        expected = field.scalar_mul(scalar, frobenius(value, field))
        failures += int(values[target] != expected)
    return failures


def nonzero_components(values: list[FpE], field: ExtensionField) -> int:
    return sum(value != field.zero for value in values)


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
    rho_raw_log_shift = logs[rho] % ORDER7
    rho_factor_step = RHO_EXPONENT % factor_count
    cycles = factor_cycles(rho_factor_step)

    field = ExtensionField(
        FIELD_Q,
        FIELD_DEGREE,
        find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED),
    )
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    characters = [pow(zeta7, k, FIELD_Q) for k in range(1, ORDER7)]
    rng = random.Random(SEED)

    descent_failures = 0
    nontrivial_covariance_failures = 0
    random_descended_nonzero = 0
    zero_intersection_successes = 0
    trials = 0
    for character in characters:
        for _ in range(4):
            seeds = [random_element(rng, field) for _orbit in cycles]
            values = descended_components(seeds, field, rho_factor_step)
            descent_failures += covariance_failures(
                values,
                field,
                rho_factor_step,
                1,
            )
            nontrivial_covariance_failures += int(
                covariance_failures(values, field, rho_factor_step, character) > 0
            )
            random_descended_nonzero += int(nonzero_components(values, field) > 0)

            zero_values = [field.zero] * FACTOR_COUNT
            zero_intersection_successes += int(
                covariance_failures(zero_values, field, rho_factor_step, 1) == 0
                and covariance_failures(zero_values, field, rho_factor_step, character) == 0
            )
            trials += 1

    print("Trace-GCD fixed-frequency p24 idempotent covariance circularity boundary")
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
    print(f"rho_raw_h_quotient_shift={rho_raw_log_shift}")
    print(f"rho_factor_step_mod_70={rho_factor_step}")
    print(f"rho_factor_cycle_count={len(cycles)}")
    print(f"rho_factor_cycle_lengths={[len(orbit) for orbit in cycles]}")
    print(f"field_q={FIELD_Q}")
    print(f"field_degree={FIELD_DEGREE}")
    print(f"character_count={len(characters)}")
    print(f"random_descended_trials={trials}")
    print(f"descended_eigenvalue1_failures={descent_failures}")
    print(f"random_descended_nonzero={random_descended_nonzero}/{trials}")
    print(f"random_descended_fail_nontrivial_covariance={nontrivial_covariance_failures}/{trials}")
    print(f"zero_components_satisfy_both_covariances={zero_intersection_successes}/{trials}")
    print("interpretation")
    print("  descended_idempotent_components_have_trivial_factor_eigenvalue=1")
    print("  nontrivial_idempotent_covariance_is_equivalent_to_vanishing_after_descent=1")
    print("  scalar_extension_idempotent_action_alone_is_circular=1")
    print("  noncircular_proof_must_establish_covariance_on_trace_terms_before_recombination=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary")

    if (factor_count, factor_degree, rho_order_on_e) != (70, 5549, ORDER7):
        raise SystemExit(1)
    if not rho_left_fixed or rho_raw_log_shift == 0:
        raise SystemExit(1)
    if rho_factor_step != 10 or len(cycles) != 10 or {len(orbit) for orbit in cycles} != {7}:
        raise SystemExit(1)
    if descent_failures:
        raise SystemExit(1)
    if random_descended_nonzero != trials:
        raise SystemExit(1)
    if nontrivial_covariance_failures != trials:
        raise SystemExit(1)
    if zero_intersection_successes != trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
