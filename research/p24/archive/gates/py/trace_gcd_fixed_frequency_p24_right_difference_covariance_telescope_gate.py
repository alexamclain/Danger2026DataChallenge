#!/usr/bin/env python3
"""Covariance plus one descended anchor kills adjacent right-difference traces.

Let T_i be the seven adjacent right-difference trace values

    T_i = Tr_{K_n/K_n^<p>}(P_i(zeta_n)).

The adjacent differences telescope, so sum_i T_i = 0.  If the p^780 action
rho shifts the right H-quotient by 6 and the packet satisfies

    T_{i+6} = rho(T_i),

then one descended anchor rho(T_0)=T_0 makes all seven T_i equal.  Since
7 is invertible modulo p and their sum is zero, every T_i is zero.

This script checks that finite implication and the negative controls:
covariance plus telescoping can be nonzero, and descent plus telescoping can
be nonzero without covariance.
"""

from __future__ import annotations

import random


FIELD_Q = 43
RHO_ORDER = 7
SHIFT = 6
SEED = 20260607
TRIALS = 96

P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
RHO_EXPONENT = 780


Vector = tuple[int, ...]
Profile = list[Vector]


def zero() -> Vector:
    return (0,) * RHO_ORDER


def add(left: Vector, right: Vector) -> Vector:
    return tuple((left[index] + right[index]) % FIELD_Q for index in range(RHO_ORDER))


def sub(left: Vector, right: Vector) -> Vector:
    return tuple((left[index] - right[index]) % FIELD_Q for index in range(RHO_ORDER))


def scalar_mul(scalar: int, value: Vector) -> Vector:
    return tuple((scalar * entry) % FIELD_Q for entry in value)


def rho(value: Vector) -> Vector:
    return value[1:] + value[:1]


def rho_power(value: Vector, exponent: int) -> Vector:
    out = value
    for _step in range(exponent % RHO_ORDER):
        out = rho(out)
    return out


def random_vector(rng: random.Random) -> Vector:
    return tuple(rng.randrange(FIELD_Q) for _index in range(RHO_ORDER))


def random_fixed_vector(rng: random.Random) -> Vector:
    value = rng.randrange(FIELD_Q)
    return (value,) * RHO_ORDER


def random_nonzero_fixed_vector(rng: random.Random) -> Vector:
    value = rng.randrange(1, FIELD_Q)
    return (value,) * RHO_ORDER


def trace_to_fixed(value: Vector) -> Vector:
    total = zero()
    orbit = value
    for _step in range(RHO_ORDER):
        total = add(total, orbit)
        orbit = rho(orbit)
    return total


def force_trace_zero_seed(rng: random.Random) -> Vector:
    values = [rng.randrange(FIELD_Q) for _index in range(RHO_ORDER - 1)]
    values.append((-sum(values)) % FIELD_Q)
    return tuple(values)


def profile_from_seed(seed: Vector) -> Profile:
    profile = [zero() for _index in range(RHO_ORDER)]
    for step in range(RHO_ORDER):
        profile[(step * SHIFT) % RHO_ORDER] = rho_power(seed, step)
    return profile


def random_sum_zero_profile_with_fixed_anchor(rng: random.Random) -> Profile:
    profile = [random_vector(rng) for _index in range(RHO_ORDER)]
    profile[0] = random_fixed_vector(rng)
    running = zero()
    for index in range(RHO_ORDER - 1):
        running = add(running, profile[index])
    profile[-1] = scalar_mul(-1, running)
    if profile[-1] == zero():
        profile[-1] = add(profile[-1], (1,) + (0,) * (RHO_ORDER - 1))
        profile[-2] = sub(profile[-2], (1,) + (0,) * (RHO_ORDER - 1))
    return profile


def profile_sum(profile: Profile) -> Vector:
    total = zero()
    for value in profile:
        total = add(total, value)
    return total


def covariance_failures(profile: Profile) -> int:
    failures = 0
    for index, value in enumerate(profile):
        failures += int(profile[(index + SHIFT) % RHO_ORDER] != rho(value))
    return failures


def anchor_descended(profile: Profile) -> bool:
    return rho(profile[0]) == profile[0]


def all_zero(profile: Profile) -> bool:
    return all(value == zero() for value in profile)


def all_equal(profile: Profile) -> bool:
    return all(value == profile[0] for value in profile)


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


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def main() -> None:
    rng = random.Random(SEED)
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_shift = logs[rho_right] % RHO_ORDER

    positive_zero = 0
    positive_equal = 0
    positive_covariance_failures = 0
    positive_sum_zero = 0
    covariance_telescope_nonzero = 0
    covariance_telescope_anchor_not_descended = 0
    descent_telescope_nonzero = 0
    descent_telescope_covariance_fails = 0
    covariance_descended_without_telescope_nonzero_equal = 0

    for _trial in range(TRIALS):
        positive = profile_from_seed(random_fixed_vector(rng))
        correction = scalar_mul(pow(RHO_ORDER, -1, FIELD_Q), profile_sum(positive))
        positive = [sub(value, correction) for value in positive]
        positive_zero += int(all_zero(positive))
        positive_equal += int(all_equal(positive))
        positive_covariance_failures += covariance_failures(positive)
        positive_sum_zero += int(profile_sum(positive) == zero())

        covariant_nonzero = profile_from_seed(force_trace_zero_seed(rng))
        covariance_telescope_nonzero += int(
            profile_sum(covariant_nonzero) == zero()
            and covariance_failures(covariant_nonzero) == 0
            and not all_zero(covariant_nonzero)
        )
        covariance_telescope_anchor_not_descended += int(
            not anchor_descended(covariant_nonzero)
        )

        descent_only = random_sum_zero_profile_with_fixed_anchor(rng)
        descent_telescope_nonzero += int(
            profile_sum(descent_only) == zero()
            and anchor_descended(descent_only)
            and not all_zero(descent_only)
        )
        descent_telescope_covariance_fails += int(covariance_failures(descent_only) > 0)

        covariant_descended = profile_from_seed(random_nonzero_fixed_vector(rng))
        covariance_descended_without_telescope_nonzero_equal += int(
            covariance_failures(covariant_descended) == 0
            and anchor_descended(covariant_descended)
            and all_equal(covariant_descended)
            and not all_zero(covariant_descended)
            and profile_sum(covariant_descended) != zero()
        )

    print("Trace-GCD fixed-frequency p24 right-difference covariance telescope gate")
    print(f"field_q={FIELD_Q}")
    print(f"model_rho_order={RHO_ORDER}")
    print(f"model_shift={SHIFT}")
    print(f"p24_rho_mod_211={rho_right}")
    print(f"p24_rho_right_shift_mod7={rho_shift}")
    print(f"positive_covariance_failures={positive_covariance_failures}")
    print(f"positive_sum_zero={positive_sum_zero}/{TRIALS}")
    print(f"positive_all_equal={positive_equal}/{TRIALS}")
    print(f"positive_all_zero={positive_zero}/{TRIALS}")
    print(f"covariance_plus_telescope_nonzero={covariance_telescope_nonzero}/{TRIALS}")
    print(
        "covariance_plus_telescope_anchor_not_descended="
        f"{covariance_telescope_anchor_not_descended}/{TRIALS}"
    )
    print(f"descent_plus_telescope_nonzero={descent_telescope_nonzero}/{TRIALS}")
    print(f"descent_plus_telescope_covariance_fails={descent_telescope_covariance_fails}/{TRIALS}")
    print(
        "covariance_plus_descent_without_telescope_nonzero_equal="
        f"{covariance_descended_without_telescope_nonzero_equal}/{TRIALS}"
    )
    print("interpretation")
    print("  covariance_plus_anchor_descent_plus_telescope_forces_trace_zero=1")
    print("  covariance_plus_telescope_alone_does_not_force_zero=1")
    print("  descent_plus_telescope_alone_does_not_force_zero=1")
    print("  covariance_plus_descent_only_gives_equal_values_until_telescope_is_used=1")
    print("  p24_shift6_is_coprime_to_7_and_cycles_adjacent_differences=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_covariance_telescope_gate")

    if rho_shift != SHIFT:
        raise SystemExit(1)
    if positive_covariance_failures:
        raise SystemExit(1)
    if positive_sum_zero != TRIALS or positive_equal != TRIALS or positive_zero != TRIALS:
        raise SystemExit(1)
    if covariance_telescope_nonzero != TRIALS:
        raise SystemExit(1)
    if covariance_telescope_anchor_not_descended != TRIALS:
        raise SystemExit(1)
    if descent_telescope_nonzero != TRIALS:
        raise SystemExit(1)
    if descent_telescope_covariance_fails != TRIALS:
        raise SystemExit(1)
    if covariance_descended_without_telescope_nonzero_equal != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
