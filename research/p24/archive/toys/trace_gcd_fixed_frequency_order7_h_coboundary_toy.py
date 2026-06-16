#!/usr/bin/env python3
"""Order-7 augmentation as an H-coboundary theorem.

For p24, the missing fixed-frequency identity is that the right profile has
zero relative trace from `(Z/211Z)^*` to the quotient by

    H = <2^7>,        |H| = 30,        (Z/211Z)^*/H ~= C_7.

This toy records the finite additive Hilbert-90 form of that target.  On each
H-coset, relative trace zero is equivalent to being a cyclic coboundary:

    G_s = Y_s - Y_{gamma*s},        gamma = 2^7 mod 211.

So a tower-native proof can aim to construct the potential `Y` for the actual
CM/Lang right profile, rather than proving six multiplicative character sums
one by one.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
Q = 1009


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("generator is not primitive")
    return logs


def h_cosets(logs: dict[int, int]) -> list[list[int]]:
    cosets: list[list[int]] = []
    for residue in range(H_STEP):
        members = [
            value
            for value in range(1, RIGHT)
            if logs[value] % H_STEP == residue
        ]
        cosets.append(sorted(members, key=logs.__getitem__))
    return cosets


def relative_trace(profile: list[int], cosets: list[list[int]]) -> list[int]:
    return [sum(profile[value] for value in coset) % Q for coset in cosets]


def coboundary(potential: list[int], gamma: int) -> list[int]:
    profile = [0] * RIGHT
    for value in range(1, RIGHT):
        profile[value] = (potential[value] - potential[gamma * value % RIGHT]) % Q
    return profile


def potential_from_trace_zero(profile: list[int], cosets: list[list[int]], gamma: int) -> list[int]:
    potential = [0] * RIGHT
    for coset in cosets:
        start = coset[0]
        value = start
        running = 0
        for _index in range(len(coset) - 1):
            running = (running - profile[value]) % Q
            value = gamma * value % RIGHT
            potential[value] = running
        if gamma * value % RIGHT != start:
            raise RuntimeError("bad H-cycle ordering")
    return potential


def random_profile(rng: random.Random) -> list[int]:
    profile = [0] * RIGHT
    for value in range(1, RIGHT):
        profile[value] = rng.randrange(Q)
    return profile


def force_global_centering(profile: list[int]) -> list[int]:
    adjusted = profile[:]
    adjusted[1] = (adjusted[1] - sum(adjusted[1:])) % Q
    return adjusted


def force_h_trace_zero(profile: list[int], cosets: list[list[int]]) -> list[int]:
    adjusted = profile[:]
    for coset in cosets:
        adjusted[coset[0]] = (adjusted[coset[0]] - sum(adjusted[value] for value in coset)) % Q
    return adjusted


def same_profile(left: list[int], right: list[int]) -> bool:
    return all((left[value] - right[value]) % Q == 0 for value in range(1, RIGHT))


def main() -> None:
    logs = log_table()
    gamma = pow(GEN, H_STEP, RIGHT)
    cosets = h_cosets(logs)
    rng = random.Random(20260606)

    potential = random_profile(rng)
    exact_coboundary = coboundary(potential, gamma)
    exact_trace = relative_trace(exact_coboundary, cosets)

    trace_zero = force_h_trace_zero(random_profile(rng), cosets)
    reconstructed = coboundary(potential_from_trace_zero(trace_zero, cosets, gamma), gamma)

    centered_only = force_global_centering(random_profile(rng))
    centered_trace = relative_trace(centered_only, cosets)
    centered_reconstructed = coboundary(
        potential_from_trace_zero(force_h_trace_zero(centered_only, cosets), cosets, gamma),
        gamma,
    )

    p_mod = P24 % RIGHT
    p_log = logs[p_mod]
    subgroup_logs = sorted(logs[value] for value in cosets[0])

    print("Trace-GCD fixed-frequency order-7 H-coboundary toy")
    print(f"field_q={Q}")
    print(f"right={RIGHT}")
    print(f"primitive_root={GEN}")
    print(f"p24_p_mod_211={p_mod}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"h_generator=2^{H_STEP}_mod_211={gamma}")
    print(f"h_subgroup_order={len(cosets[0])}")
    print(f"quotient_order={len(cosets)}")
    print(f"h_subgroup_logs_are_multiples_of_7={int(all(log % H_STEP == 0 for log in subgroup_logs))}")
    print(f"coboundary_relative_trace_zero={int(all(value == 0 for value in exact_trace))}")
    print(f"trace_zero_reconstructs_coboundary={int(same_profile(trace_zero, reconstructed))}")
    print(f"centered_only_global_sum_zero={int(sum(centered_only[1:]) % Q == 0)}")
    print(f"centered_only_h_trace_zero={int(all(value == 0 for value in centered_trace))}")
    print(f"centered_control_has_h_trace_leak={int(any(value != 0 for value in centered_trace))}")
    print(f"forced_centered_h_trace_part_is_coboundary={int(same_profile(force_h_trace_zero(centered_only, cosets), centered_reconstructed))}")
    print("interpretation")
    print("  h_coboundary_implies_order7_augmentation=1")
    print("  order7_augmentation_equivalent_to_h_coboundary_potential=1")
    print("  ordinary_centering_is_not_an_h_coboundary_condition=1")
    print("  p24_sufficient_theorem_is_explicit_H_potential_for_right_profile=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_h_coboundary_toy")

    if (p_mod, p_log, gamma, len(cosets), len(cosets[0])) != (114, 198, 128, 7, 30):
        raise SystemExit(1)
    if any(value != 0 for value in exact_trace):
        raise SystemExit(1)
    if not same_profile(trace_zero, reconstructed):
        raise SystemExit(1)
    if sum(centered_only[1:]) % Q != 0:
        raise SystemExit(1)
    if all(value == 0 for value in centered_trace):
        raise SystemExit(1)
    if not same_profile(force_h_trace_zero(centered_only, cosets), centered_reconstructed):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
