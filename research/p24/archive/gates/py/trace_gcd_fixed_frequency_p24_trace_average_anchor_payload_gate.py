#!/usr/bin/env python3
"""Anchor verifier accounting from quotient trace averages.

The anchor trace-defect target can be checked in two equivalent ways:

1. supply the seven H-coset sums of the relative trace defect profile;
2. supply the quotient trace-average profile and selected child profile, then
   compute those seven sums.

This is a verifier/accounting gate, not a producer theorem.  The seven defect
sums are tiny, but they are useful only if an embedded CM/Lang construction
proves they are the honest sums for

    D_r = Tr_relative(j_{r+m*bullet}) - n*j_r.
"""

from __future__ import annotations

import random


FIELD_Q = 337
LEFT = 3
RIGHT = 43
RELATIVE = 5
M = LEFT * RIGHT
ORDER7 = 7
SEED = 20260606
TRIALS = 48

P24_SQRT_FLOOR = 10**12
P24_M = 66254
P24_N = 3107441
P24_RIGHT = 211
P24_H_COSETS = 7
P24_RIGHT_NONTRIVIAL_CHARACTERS = 6


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


def random_j_values(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _index in range(M * RELATIVE)]


def selected_child_profile(j_values: list[int]) -> list[int]:
    out = [0] * RIGHT
    for residue in range(1, RIGHT):
        total = 0
        for r in range(residue, M, RIGHT):
            total = (total + j_values[r]) % FIELD_Q
        out[residue] = total
    return out


def quotient_trace_profile(j_values: list[int]) -> list[int]:
    out = [0] * RIGHT
    for residue in range(1, RIGHT):
        total = 0
        for r in range(residue, M, RIGHT):
            total = (
                total
                + sum(j_values[r + M * k] for k in range(RELATIVE))
            ) % FIELD_Q
        out[residue] = total
    return out


def defect_profile_from_profiles(trace_profile: list[int], child_profile: list[int]) -> list[int]:
    out = [0] * RIGHT
    for residue in range(1, RIGHT):
        out[residue] = (trace_profile[residue] - RELATIVE * child_profile[residue]) % FIELD_Q
    return out


def defect_profile_direct(j_values: list[int]) -> list[int]:
    return defect_profile_from_profiles(quotient_trace_profile(j_values), selected_child_profile(j_values))


def h_coset_sums(profile: list[int], logs: dict[int, int]) -> list[int]:
    sums = [0] * ORDER7
    for residue in range(1, RIGHT):
        sums[logs[residue] % ORDER7] = (
            sums[logs[residue] % ORDER7] + profile[residue]
        ) % FIELD_Q
    return sums


def all_equal(values: list[int]) -> bool:
    return all(value == values[0] for value in values)


def random_equal_h_sums_profile(rng: random.Random, logs: dict[int, int]) -> list[int]:
    profile = [0] * RIGHT
    target = rng.randrange(FIELD_Q)
    cosets: list[list[int]] = [[] for _index in range(ORDER7)]
    for residue in range(1, RIGHT):
        cosets[logs[residue] % ORDER7].append(residue)
    for coset in cosets:
        running = 0
        for residue in coset[:-1]:
            profile[residue] = rng.randrange(FIELD_Q)
            running = (running + profile[residue]) % FIELD_Q
        profile[coset[-1]] = (target - running) % FIELD_Q
    return profile


def main() -> None:
    rng = random.Random(SEED)
    right_generator = primitive_root_mod_prime(RIGHT)
    logs = log_table(RIGHT, right_generator)

    profile_decomposition_failures = 0
    random_equal_h_sums = 0
    forced_equal_h_sums = 0
    fake_equal_sum_payloads_pass = 0

    for _trial in range(TRIALS):
        j_values = random_j_values(rng)
        trace_profile = quotient_trace_profile(j_values)
        child_profile = selected_child_profile(j_values)
        from_profiles = defect_profile_from_profiles(trace_profile, child_profile)
        direct = defect_profile_direct(j_values)
        profile_decomposition_failures += int(from_profiles != direct)
        random_equal_h_sums += int(all_equal(h_coset_sums(direct, logs)))

        forced_profile = random_equal_h_sums_profile(rng, logs)
        forced_equal_h_sums += int(all_equal(h_coset_sums(forced_profile, logs)))
        fake_equal_sum_payloads_pass += int(all_equal([rng.randrange(FIELD_Q)] * ORDER7))

    full_profile_payload = 2 * P24_M
    print("Trace-GCD fixed-frequency p24 trace-average anchor payload gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_left={LEFT}")
    print(f"toy_right={RIGHT}")
    print(f"toy_right_generator={right_generator}")
    print(f"toy_relative={RELATIVE}")
    print(f"toy_m={M}")
    print(f"toy_h_cosets={ORDER7}")
    print(f"profile_decomposition_failures={profile_decomposition_failures}")
    print(f"random_trace_average_anchor_passes={random_equal_h_sums}/{TRIALS}")
    print(f"forced_defect_h_sums_equal={forced_equal_h_sums}/{TRIALS}")
    print(f"fake_equal_h_sum_payloads_pass={fake_equal_sum_payloads_pass}/{TRIALS}")
    print(f"p24_m={P24_M}")
    print(f"p24_n={P24_N}")
    print(f"p24_right={P24_RIGHT}")
    print(f"p24_anchor_equations={P24_RIGHT_NONTRIVIAL_CHARACTERS}")
    print(f"p24_defect_hcoset_sum_payload={P24_H_COSETS}")
    print(f"p24_full_trace_average_plus_child_payload={full_profile_payload}")
    print(
        "p24_full_trace_average_plus_child_payload_over_sqrt="
        f"{full_profile_payload / P24_SQRT_FLOOR:.12e}"
    )
    print("interpretation")
    print("  anchor_can_be_verified_from_seven_defect_H_coset_sums=1")
    print("  full_trace_average_plus_child_profile_is_subsqrt_for_p24=1")
    print("  equal_sum_payload_requires_producer_honesty=1")
    print("  trace_average_route_still_needs_embedded_child_or_morphism=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate")

    if profile_decomposition_failures:
        raise SystemExit(1)
    if random_equal_h_sums:
        raise SystemExit(1)
    if forced_equal_h_sums != TRIALS:
        raise SystemExit(1)
    if fake_equal_sum_payloads_pass != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
