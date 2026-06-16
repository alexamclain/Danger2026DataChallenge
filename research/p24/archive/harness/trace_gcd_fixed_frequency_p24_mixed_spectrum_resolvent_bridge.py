#!/usr/bin/env python3
"""Gauss bridge between mixed spectrum and additive class resolvents.

The recombined target uses multiplicative characters on two additive class
coordinates:

    S(chi,lambda) =
      sum_{r != 0, k != 0} chi^{-1}(r) lambda(k) j_{r+m*k}.

This is not one additive class-character resolvent.  By two finite Gauss
transforms it is a weighted linear combination of the additive resolvents

    R(v,a) = sum_{r,k} zeta_R^(v*r) zeta_N^(a*k) j_{r+m*k}.

Therefore reduced normality, which says the additive resolvents are nonzero,
does not decide the mixed-spectrum theorem.  This toy checks the exact bridge
and constructs both controls:

* all additive resolvents nonzero but mixed spectrum zero;
* one additive resolvent zero but mixed spectrum nonzero.
"""

from __future__ import annotations

import random


FIELD_Q = 55217  # 1 mod lcm(29,17,7,8).
RIGHT = 29
RELATIVE_N = 17
RIGHT_QUOTIENT = 7
RELATIVE_QUOTIENT = 8
M = RIGHT
SEED = 20260606
TRIALS = 24

P24_RIGHT = 211
P24_RELATIVE_N = 3107441


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


def primitive_root_mod_prime(modulus: int) -> int:
    factors = factor_distinct(modulus - 1)
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_table(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def root_of_order(order: int) -> int:
    generator = primitive_root_mod_prime(FIELD_Q)
    root = pow(generator, (FIELD_Q - 1) // order, FIELD_Q)
    if root == 1 or pow(root, order, FIELD_Q) != 1:
        raise RuntimeError("bad root of unity")
    return root


def character_value(
    value: int,
    modulus: int,
    quotient_order: int,
    zeta: int,
    logs: dict[int, int],
    character_index: int,
) -> int:
    if value % modulus == 0:
        return 0
    return pow(zeta, (character_index * logs[value % modulus]) % quotient_order, FIELD_Q)


def index(r: int, k: int) -> int:
    return r + M * k


def random_values(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _ in range(M * RELATIVE_N)]


def additive_resolvent(
    values: list[int],
    zeta_right: int,
    zeta_relative: int,
    v: int,
    a: int,
) -> int:
    total = 0
    for k in range(RELATIVE_N):
        rel_weight = pow(zeta_relative, (a * k) % RELATIVE_N, FIELD_Q)
        for r in range(RIGHT):
            right_weight = pow(zeta_right, (v * r) % RIGHT, FIELD_Q)
            total = (total + right_weight * rel_weight * values[index(r, k)]) % FIELD_Q
    return total


def all_additive_resolvents(
    values: list[int],
    zeta_right: int,
    zeta_relative: int,
) -> list[int]:
    return [
        additive_resolvent(values, zeta_right, zeta_relative, v, a)
        for v in range(1, RIGHT)
        for a in range(1, RELATIVE_N)
    ]


def mixed_spectrum(
    values: list[int],
    right_logs: dict[int, int],
    relative_logs: dict[int, int],
    zeta7: int,
    zeta8: int,
    chi_index: int,
    lambda_index: int,
) -> int:
    total = 0
    for k in range(1, RELATIVE_N):
        rel_weight = character_value(
            k,
            RELATIVE_N,
            RELATIVE_QUOTIENT,
            zeta8,
            relative_logs,
            lambda_index,
        )
        for r in range(1, RIGHT):
            right_weight = character_value(
                r,
                RIGHT,
                RIGHT_QUOTIENT,
                zeta7,
                right_logs,
                -chi_index,
            )
            total = (total + right_weight * rel_weight * values[index(r, k)]) % FIELD_Q
    return total


def gauss_sum(
    modulus: int,
    quotient_order: int,
    zeta_quotient: int,
    logs: dict[int, int],
    character_index: int,
    zeta_additive: int,
) -> int:
    return sum(
        character_value(x, modulus, quotient_order, zeta_quotient, logs, character_index)
        * pow(zeta_additive, x, FIELD_Q)
        for x in range(1, modulus)
    ) % FIELD_Q


def mixed_from_additive_resolvents(
    values: list[int],
    right_logs: dict[int, int],
    relative_logs: dict[int, int],
    zeta7: int,
    zeta8: int,
    zeta_right: int,
    zeta_relative: int,
    chi_index: int,
    lambda_index: int,
) -> int:
    tau_right = gauss_sum(
        RIGHT,
        RIGHT_QUOTIENT,
        zeta7,
        right_logs,
        chi_index,
        zeta_right,
    )
    tau_relative_inverse = gauss_sum(
        RELATIVE_N,
        RELATIVE_QUOTIENT,
        zeta8,
        relative_logs,
        -lambda_index,
        zeta_relative,
    )
    total = 0
    for a in range(1, RELATIVE_N):
        rel_weight = character_value(
            a,
            RELATIVE_N,
            RELATIVE_QUOTIENT,
            zeta8,
            relative_logs,
            -lambda_index,
        )
        for v in range(1, RIGHT):
            right_weight = character_value(
                v,
                RIGHT,
                RIGHT_QUOTIENT,
                zeta7,
                right_logs,
                chi_index,
            )
            total = (
                total
                + right_weight
                * rel_weight
                * additive_resolvent(values, zeta_right, zeta_relative, v, a)
            ) % FIELD_Q
    return total * pow(tau_right * tau_relative_inverse % FIELD_Q, -1, FIELD_Q) % FIELD_Q


def force_linear_functional_zero(
    rng: random.Random,
    functional,
    pivot_index: int,
) -> list[int]:
    values = random_values(rng)
    values[pivot_index] = 0
    current = functional(values)
    values[pivot_index] = 1
    with_one = functional(values)
    coefficient = (with_one - current) % FIELD_Q
    if coefficient == 0:
        raise RuntimeError("bad pivot")
    values[pivot_index] = (-current * pow(coefficient, -1, FIELD_Q)) % FIELD_Q
    if functional(values) != 0:
        raise RuntimeError("forcing failed")
    return values


def find_forced_case(
    rng: random.Random,
    functional,
    pivot_index: int,
    predicate,
) -> list[int]:
    for _attempt in range(200):
        values = force_linear_functional_zero(rng, functional, pivot_index)
        if predicate(values):
            return values
    raise RuntimeError("failed to find forced case")


def main() -> None:
    rng = random.Random(SEED)
    right_generator = primitive_root_mod_prime(RIGHT)
    relative_generator = primitive_root_mod_prime(RELATIVE_N)
    right_logs = log_table(RIGHT, right_generator)
    relative_logs = log_table(RELATIVE_N, relative_generator)
    zeta7 = root_of_order(RIGHT_QUOTIENT)
    zeta8 = root_of_order(RELATIVE_QUOTIENT)
    zeta_right = root_of_order(RIGHT)
    zeta_relative = root_of_order(RELATIVE_N)

    def mixed(values: list[int]) -> int:
        return mixed_spectrum(values, right_logs, relative_logs, zeta7, zeta8, 1, 1)

    def first_additive(values: list[int]) -> int:
        return additive_resolvent(values, zeta_right, zeta_relative, 1, 1)

    gauss_bridge_failures = 0
    random_all_resolvents_nonzero = 0
    random_normal_like_mixed_nonzero = 0
    forced_mixed_zero_normal_like = 0
    forced_additive_zero_mixed_nonzero = 0

    for _trial in range(TRIALS):
        values = random_values(rng)
        additive_values = all_additive_resolvents(values, zeta_right, zeta_relative)
        mixed_direct = mixed(values)
        mixed_gauss = mixed_from_additive_resolvents(
            values,
            right_logs,
            relative_logs,
            zeta7,
            zeta8,
            zeta_right,
            zeta_relative,
            1,
            1,
        )
        gauss_bridge_failures += int(mixed_direct != mixed_gauss)
        all_nonzero = all(value != 0 for value in additive_values)
        random_all_resolvents_nonzero += int(all_nonzero)
        random_normal_like_mixed_nonzero += int(all_nonzero and mixed_direct != 0)

        forced_mixed = find_forced_case(
            rng,
            mixed,
            index(1, 1),
            lambda row: all(
                value != 0
                for value in all_additive_resolvents(row, zeta_right, zeta_relative)
            ),
        )
        forced_mixed_zero_normal_like += int(
            mixed(forced_mixed) == 0
            and all(
                value != 0
                for value in all_additive_resolvents(
                    forced_mixed, zeta_right, zeta_relative
                )
            )
        )

        forced_additive = find_forced_case(
            rng,
            first_additive,
            index(0, 0),
            lambda row: mixed(row) != 0,
        )
        forced_additive_zero_mixed_nonzero += int(
            first_additive(forced_additive) == 0 and mixed(forced_additive) != 0
        )

    print("Trace-GCD fixed-frequency p24 mixed-spectrum resolvent bridge")
    print(f"field_q={FIELD_Q}")
    print(f"toy_right={RIGHT}")
    print(f"toy_right_generator={right_generator}")
    print(f"toy_relative_n={RELATIVE_N}")
    print(f"toy_relative_generator={relative_generator}")
    print(f"toy_additive_resolvent_count={(RIGHT - 1) * (RELATIVE_N - 1)}")
    print(f"gauss_bridge_failures={gauss_bridge_failures}")
    print(f"random_all_additive_resolvents_nonzero={random_all_resolvents_nonzero}/{TRIALS}")
    print(f"random_normal_like_mixed_nonzero={random_normal_like_mixed_nonzero}/{TRIALS}")
    print(f"forced_mixed_zero_with_all_additive_resolvents_nonzero={forced_mixed_zero_normal_like}/{TRIALS}")
    print(f"forced_additive_resolvent_zero_with_mixed_nonzero={forced_additive_zero_mixed_nonzero}/{TRIALS}")
    print(f"p24_right={P24_RIGHT}")
    print(f"p24_relative_n={P24_RELATIVE_N}")
    print("interpretation")
    print("  mixed_spectrum_is_gauss_weighted_additive_resolvent_combination=1")
    print("  mixed_spectrum_is_not_a_single_class_character_resolvent=1")
    print("  additive_reduced_normality_does_not_imply_mixed_spectrum_nonzero=1")
    print("  additive_reduced_normality_does_not_imply_mixed_spectrum_zero=1")
    print("  remaining_theorem_needs_stickelberger_or_cm_lang_relation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_mixed_spectrum_resolvent_bridge")

    if gauss_bridge_failures:
        raise SystemExit(1)
    if random_all_resolvents_nonzero != TRIALS:
        raise SystemExit(1)
    if random_normal_like_mixed_nonzero != TRIALS:
        raise SystemExit(1)
    if forced_mixed_zero_normal_like != TRIALS:
        raise SystemExit(1)
    if forced_additive_zero_mixed_nonzero != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
