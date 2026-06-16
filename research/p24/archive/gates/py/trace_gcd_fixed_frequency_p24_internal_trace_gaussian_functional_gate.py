#!/usr/bin/env python3
"""Gaussian-period functional form of the p24 internal trace target.

The current target is the codimension-one identity

    Tr_{C/E}(Tr_{B/C}(R_obstruction)) = 0.

For a relative packet polynomial P(X), this is an orbit trace

    sum_{r in <Q>} P(zeta_n^(a r)),

where Q=p^5460 mod n has order 5549 for p24.  Expanding
P(X)=sum_k c_k X^k turns the target into a Gaussian-period pairing

    sum_k c_k * eta_{a k},     eta_t = sum_{r in <Q>} zeta_n^(t r).

This gate verifies the identity in a small split cyclotomic model and records
two boundaries:

* primitive/augmentation nonvanishing does not imply this trace zero;
* trace zero does not imply packet vanishing.

So the missing theorem is exactly weighted CM/Lang cancellation against this
Gaussian-period vector.
"""

from __future__ import annotations

import random

import sympy as sp


P24 = 10**24 + 7
P24_N = 3107441
P24_SPLIT_Q = 37289293
P24_INTERNAL_DEGREE = 5549

TOY_N = 31
TOY_Q = 311  # 311 - 1 is divisible by 31.
TOY_INTERNAL_DEGREE = 15
SEED = 20260606


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


def primitive_root_known_factors(q: int, factors: set[int]) -> int:
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def subgroup_order_elements(modulus: int, order: int) -> list[int]:
    generator = primitive_root_mod_prime(modulus)
    step = (modulus - 1) // order
    h_generator = pow(generator, step, modulus)
    out: list[int] = []
    value = 1
    for _index in range(order):
        out.append(value)
        value = value * h_generator % modulus
    if value != 1 or len(set(out)) != order:
        raise RuntimeError("bad subgroup")
    return out


def polynomial_eval(coefficients: list[int], point: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coefficients:
        total = (total + coeff * power) % q
        power = power * point % q
    return total


def gaussian_periods(n: int, q: int, subgroup: list[int]) -> tuple[int, list[int]]:
    root = primitive_root_known_factors(q, factor_distinct(q - 1))
    zeta = pow(root, (q - 1) // n, q)
    periods = [
        sum(pow(zeta, (t * exponent) % n, q) for exponent in subgroup) % q
        for t in range(n)
    ]
    return zeta, periods


def orbit_trace_direct(coefficients: list[int], zeta: int, subgroup: list[int], a: int, n: int, q: int) -> int:
    return sum(
        polynomial_eval(coefficients, pow(zeta, (a * exponent) % n, q), q)
        for exponent in subgroup
    ) % q


def orbit_trace_pairing(coefficients: list[int], periods: list[int], a: int, n: int, q: int) -> int:
    return sum(
        coeff * periods[(a * index) % n]
        for index, coeff in enumerate(coefficients)
    ) % q


def all_primitive_evaluations_nonzero(coefficients: list[int], zeta: int, n: int, q: int) -> bool:
    return all(
        polynomial_eval(coefficients, pow(zeta, exponent, q), q) != 0
        for exponent in range(1, n)
    )


def random_coefficients(rng: random.Random, n: int, q: int) -> list[int]:
    while True:
        coeffs = [rng.randrange(q) for _index in range(n)]
        coeffs[0] = 0  # augmentation-only model, ignore the trivial coordinate.
        if any(coeffs[1:]):
            return coeffs


def force_trace_zero(coefficients: list[int], periods: list[int], a: int, n: int, q: int) -> list[int]:
    adjusted = coefficients[:]
    pivot = next(index for index in range(1, n) if periods[(a * index) % n] % q)
    current = orbit_trace_pairing(adjusted, periods, a, n, q)
    adjusted[pivot] = (adjusted[pivot] - current * pow(periods[(a * pivot) % n], -1, q)) % q
    return adjusted


def p24_period_sample() -> tuple[int, list[int]]:
    q_generator = pow(P24, 5460, P24_N)
    if int(sp.n_order(q_generator, P24_N)) != P24_INTERNAL_DEGREE:
        raise RuntimeError("bad p24 internal order")
    root = primitive_root_known_factors(P24_SPLIT_Q, {2, 3, P24_N})
    zeta = pow(root, (P24_SPLIT_Q - 1) // P24_N, P24_SPLIT_Q)
    subgroup: list[int] = []
    value = 1
    for _index in range(P24_INTERNAL_DEGREE):
        subgroup.append(value)
        value = value * q_generator % P24_N
    samples = [1, 2, 3, 5, 7, 31, 179, P24_N - 1]
    periods = [
        sum(pow(zeta, (sample * exponent) % P24_N, P24_SPLIT_Q) for exponent in subgroup)
        % P24_SPLIT_Q
        for sample in samples
    ]
    return q_generator, periods


def main() -> None:
    subgroup = subgroup_order_elements(TOY_N, TOY_INTERNAL_DEGREE)
    zeta, periods = gaussian_periods(TOY_N, TOY_Q, subgroup)
    rng = random.Random(SEED)

    identity_failures = 0
    random_all_nonzero_trace_nonzero = 0
    forced_trace_zero_all_nonzero = 0
    trials = 0
    a_values = [1, 3, 11]
    for a in a_values:
        for _trial in range(12):
            coeffs = random_coefficients(rng, TOY_N, TOY_Q)
            direct = orbit_trace_direct(coeffs, zeta, subgroup, a, TOY_N, TOY_Q)
            pairing = orbit_trace_pairing(coeffs, periods, a, TOY_N, TOY_Q)
            identity_failures += int(direct != pairing)
            random_all_nonzero_trace_nonzero += int(
                all_primitive_evaluations_nonzero(coeffs, zeta, TOY_N, TOY_Q)
                and pairing != 0
            )

            # Retry a few random points until trace zero coexists with all
            # primitive evaluations nonzero.
            found_forced = False
            for _retry in range(20):
                forced = force_trace_zero(
                    random_coefficients(rng, TOY_N, TOY_Q),
                    periods,
                    a,
                    TOY_N,
                    TOY_Q,
                )
                if (
                    orbit_trace_pairing(forced, periods, a, TOY_N, TOY_Q) == 0
                    and all_primitive_evaluations_nonzero(forced, zeta, TOY_N, TOY_Q)
                ):
                    found_forced = True
                    break
            forced_trace_zero_all_nonzero += int(found_forced)
            trials += 1

    p24_q_generator, p24_periods = p24_period_sample()
    p24_nonzero_periods = sum(period != 0 for period in p24_periods)

    print("Trace-GCD fixed-frequency p24 internal trace Gaussian functional gate")
    print(f"toy_n={TOY_N}")
    print(f"toy_q={TOY_Q}")
    print(f"toy_zeta={zeta}")
    print(f"toy_internal_degree={TOY_INTERNAL_DEGREE}")
    print(f"toy_subgroup={subgroup}")
    print(f"toy_period_nonzeroes={sum(period != 0 for period in periods[1:])}/{TOY_N - 1}")
    print(f"orbit_trace_pairing_identity_failures={identity_failures}")
    print(f"random_all_primitive_evals_nonzero_trace_nonzero={random_all_nonzero_trace_nonzero}/{trials}")
    print(f"forced_trace_zero_and_all_primitive_evals_nonzero={forced_trace_zero_all_nonzero}/{trials}")
    print(f"p24_n={P24_N}")
    print(f"p24_split_q={P24_SPLIT_Q}")
    print(f"p24_internal_q_generator=p^5460_mod_n={p24_q_generator}")
    print(f"p24_internal_degree={P24_INTERNAL_DEGREE}")
    print(f"p24_sample_gaussian_periods={p24_periods}")
    print(f"p24_sample_gaussian_period_nonzeroes={p24_nonzero_periods}/{len(p24_periods)}")
    print("interpretation")
    print("  nested_internal_trace_is_gaussian_period_pairing=1")
    print("  augmentation_nonvanishing_does_not_imply_internal_trace_zero=1")
    print("  internal_trace_zero_does_not_imply_packet_vanishing=1")
    print("  p24_gaussian_period_weights_are_not_formally_zero=1")
    print("  remaining_theorem_is_cm_lang_weighted_period_cancellation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_gaussian_functional_gate")

    if identity_failures:
        raise SystemExit(1)
    if random_all_nonzero_trace_nonzero == 0:
        raise SystemExit(1)
    if forced_trace_zero_all_nonzero != trials:
        raise SystemExit(1)
    if p24_nonzero_periods != len(p24_periods):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
