#!/usr/bin/env python3
"""Complete 70-factor descent gate for the p24 fixed-frequency packet sum.

The refined p24 target has two logically different inputs.

1. Complete recombination/descent:
   the sum over all 70 E-tensor factors is the original fixed-frequency
   projection S_chi in L=F_p(mu_157).  Since rho=p^780 fixes L, this gives
   rho(S_chi)=S_chi.

2. Factor covariance:
   the individual factor contributions Z_d satisfy

       Z_{d+10} = lambda_chi * rho(Z_d)

   along the ten 7-cycles of factors.

Covariance alone only puts the complete sum in a nontrivial eigenspace and is
usually nonzero.  Complete recombination plus covariance forces zero.  This is
the finite gate for that proof shape; it does not construct the CM
contributions Z_d.
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
    cycles: list[list[int]] = []
    for start in range(FACTOR_COUNT):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value + step) % FACTOR_COUNT
        cycles.append(orbit)
    return cycles


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def is_fixed(value: FpE, field: ExtensionField) -> bool:
    return frobenius(value, field) == value


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = tuple(rng.randrange(field.q) for _ in range(field.degree))
        if value != field.zero:
            return value


def covariant_components(
    rng: random.Random,
    field: ExtensionField,
    factor_step: int,
    character_value: int,
) -> list[FpE]:
    values = [field.zero] * FACTOR_COUNT
    for orbit in factor_cycles(factor_step):
        current = random_element(rng, field)
        for factor_index in orbit:
            values[factor_index] = current
            current = field.scalar_mul(character_value, frobenius(current, field))
    return values


def fill_covariant_orbit(
    values: list[FpE],
    orbit: list[int],
    seed: FpE,
    field: ExtensionField,
    character_value: int,
) -> None:
    current = seed
    for factor_index in orbit:
        values[factor_index] = current
        current = field.scalar_mul(character_value, frobenius(current, field))


def component_sum(values: list[FpE], field: ExtensionField, indices: list[int] | None = None) -> FpE:
    out = field.zero
    iterable = range(len(values)) if indices is None else indices
    for index in iterable:
        out = field.add(out, values[index])
    return out


def covariance_failures(
    values: list[FpE],
    field: ExtensionField,
    factor_step: int,
    character_value: int,
) -> int:
    failures = 0
    for index, value in enumerate(values):
        target = (index + factor_step) % FACTOR_COUNT
        expected = field.scalar_mul(character_value, frobenius(value, field))
        failures += int(values[target] != expected)
    return failures


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
    cycles = factor_cycles(rho_factor_step)
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    characters = [pow(zeta7, k, FIELD_Q) for k in range(1, ORDER7)]

    field = ExtensionField(
        FIELD_Q,
        FIELD_DEGREE,
        find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED),
    )
    rng = random.Random(SEED)

    covariance_failure_count = 0
    complete_sums_nonzero = 0
    complete_sums_not_fixed = 0
    complete_sums_eigen_failures = 0
    one_cycle_sums_nonzero = 0
    one_cycle_sums_not_fixed = 0
    descended_covariant_sums_forced_zero = 0
    constructed_zero_sum_covariance_failures = 0
    constructed_zero_sum_nonzero_components = 0
    constructed_zero_sum_descended = 0
    trials = 0

    for character in characters:
        inverse_character = pow(character, -1, FIELD_Q)
        constructed = [field.zero] * FACTOR_COUNT
        seed = random_element(rng, field)
        fill_covariant_orbit(constructed, cycles[0], seed, field, character)
        fill_covariant_orbit(constructed, cycles[1], field.neg(seed), field, character)
        constructed_sum = component_sum(constructed, field)
        constructed_zero_sum_covariance_failures += covariance_failures(
            constructed,
            field,
            rho_factor_step,
            character,
        )
        constructed_zero_sum_nonzero_components += int(
            any(value != field.zero for value in constructed)
        )
        constructed_zero_sum_descended += int(
            constructed_sum == field.zero and is_fixed(constructed_sum, field)
        )

        for _ in range(6):
            values = covariant_components(rng, field, rho_factor_step, character)
            covariance_failure_count += covariance_failures(
                values,
                field,
                rho_factor_step,
                character,
            )
            total = component_sum(values, field)
            one_cycle_total = component_sum(values, field, cycles[0])

            complete_sums_nonzero += int(total != field.zero)
            complete_sums_not_fixed += int(not is_fixed(total, field))
            complete_sums_eigen_failures += int(
                frobenius(total, field)
                != field.scalar_mul(inverse_character, total)
            )
            one_cycle_sums_nonzero += int(one_cycle_total != field.zero)
            one_cycle_sums_not_fixed += int(not is_fixed(one_cycle_total, field))

            # This is the formal descent step: if complete recombination gives
            # a rho-fixed total, the simultaneous nontrivial eigen relation
            # forces zero.  Random covariant data almost never descends, so we
            # check the implication directly on the fixed cases that occur.
            if is_fixed(total, field):
                descended_covariant_sums_forced_zero += int(total == field.zero)
            trials += 1

    print("Trace-GCD fixed-frequency p24 complete factor descent gate")
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
    print(f"rho_factor_cycle_count={len(cycles)}")
    print(f"rho_factor_cycle_lengths={[len(cycle) for cycle in cycles]}")
    print(f"field_q={FIELD_Q}")
    print(f"field_degree={FIELD_DEGREE}")
    print(f"character_count={len(characters)}")
    print(f"covariant_random_trials={trials}")
    print(f"factor_covariance_failures={covariance_failure_count}")
    print(f"complete_covariant_sums_nonzero={complete_sums_nonzero}/{trials}")
    print(f"complete_covariant_sums_not_fixed={complete_sums_not_fixed}/{trials}")
    print(f"complete_covariant_sums_eigen_failures={complete_sums_eigen_failures}")
    print(f"one_cycle_covariant_sums_nonzero={one_cycle_sums_nonzero}/{trials}")
    print(f"one_cycle_covariant_sums_not_fixed={one_cycle_sums_not_fixed}/{trials}")
    print(
        "descended_covariant_sums_forced_zero="
        f"{descended_covariant_sums_forced_zero}/"
        f"{trials - complete_sums_not_fixed}"
    )
    print(f"constructed_zero_sum_covariance_failures={constructed_zero_sum_covariance_failures}")
    print(
        "constructed_descended_zero_sum_nonzero_components="
        f"{constructed_zero_sum_nonzero_components}/6"
    )
    print(f"constructed_descended_zero_sum_verified={constructed_zero_sum_descended}/6")
    print("interpretation")
    print("  complete_70_factor_recombination_is_the_descent_input=1")
    print("  factor_covariance_alone_does_not_descend=1")
    print("  one_factor_cycle_is_not_a_valid_descended_certificate=1")
    print("  descended_plus_covariant_complete_sum_forces_h_coset_zero=1")
    print("  remaining_arithmetic_is_complete_idempotent_factor_covariance=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_complete_factor_descent_gate")

    if (factor_count, factor_degree, rho_order_on_e) != (70, 5549, ORDER7):
        raise SystemExit(1)
    if not rho_left_fixed or rho_right_log_mod7 == 0:
        raise SystemExit(1)
    if rho_factor_step != 10 or len(cycles) != 10 or {len(cycle) for cycle in cycles} != {7}:
        raise SystemExit(1)
    if covariance_failure_count or complete_sums_eigen_failures:
        raise SystemExit(1)
    if complete_sums_nonzero < trials - 1 or complete_sums_not_fixed < trials - 1:
        raise SystemExit(1)
    if one_cycle_sums_nonzero < trials - 1 or one_cycle_sums_not_fixed < trials - 1:
        raise SystemExit(1)
    if descended_covariant_sums_forced_zero != trials - complete_sums_not_fixed:
        raise SystemExit(1)
    if constructed_zero_sum_covariance_failures:
        raise SystemExit(1)
    if constructed_zero_sum_nonzero_components != 6 or constructed_zero_sum_descended != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
