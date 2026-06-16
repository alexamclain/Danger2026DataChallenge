#!/usr/bin/env python3
"""Order-7 augmentation as a right-character projection.

This is a finite-field bookkeeping check for the p24 fixed-frequency route.
It does not model the CM packet.  It proves that the proposed order-7
augmentation identity is exactly a multiplicative-character projection
statement for the centered right profile.

Let

    S_v = sum_s zeta_211^(v*s) G_s,     1 <= v < 211.

The six p24 right Frobenius orbits are indexed by

    v = 2^(35*label + 198*position) mod 211.

For a nontrivial order-7 quotient character chi_k with

    chi_k(2^e) = zeta_7^(k * 198^(-1) * e),

the order-7 orbit-position augmentation

    A_k = sum_{label,position} zeta_7^(k*position) S_v

equals

    tau(chi_k) * sum_{s != 0} chi_k(s)^(-1) G_s.

Thus the missing order-7 augmentation theorem is not ordinary centering.  It
is the vanishing of six specific right multiplicative-character projections
of the actual CM/Lang Hermitian profile.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
FIELD_Q = 8863  # 8863 - 1 = 42 * 211, so F_q contains mu_211 and mu_7.
ORBIT_COUNT = 6
ORBIT_LEN = 35
ORDER7 = 7


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


def log_table_mod_211() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("2 is not primitive modulo 211")
    return logs


def orbit_frequency(label: int, position: int, p_log: int) -> int:
    exponent = (35 * label + p_log * position) % (RIGHT - 1)
    return pow(RIGHT_GEN, exponent, RIGHT)


def roots() -> tuple[int, int, int]:
    root = primitive_root(FIELD_Q)
    return (
        root,
        pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q),
        pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q),
    )


def right_dft(profile: list[int], zeta211: int) -> list[int]:
    periods = [0] * RIGHT
    for v in range(1, RIGHT):
        periods[v] = sum(
            profile[s] * pow(zeta211, (v * s) % RIGHT, FIELD_Q)
            for s in range(RIGHT)
        ) % FIELD_Q
    return periods


def character(value: int, k: int, logs: dict[int, int], zeta7: int, p_log_inv: int) -> int:
    exponent = (k * p_log_inv * logs[value]) % ORDER7
    return pow(zeta7, exponent, FIELD_Q)


def orbit_augmentation(periods: list[int], k: int, zeta7: int, p_log: int) -> int:
    total = 0
    for label in range(ORBIT_COUNT):
        for position in range(ORBIT_LEN):
            v = orbit_frequency(label, position, p_log)
            weight = pow(zeta7, (k * position) % ORDER7, FIELD_Q)
            total = (total + weight * periods[v]) % FIELD_Q
    return total


def character_period_sum(
    periods: list[int],
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    return sum(
        character(v, k, logs, zeta7, p_log_inv) * periods[v]
        for v in range(1, RIGHT)
    ) % FIELD_Q


def gauss_sum_formula(
    profile: list[int],
    k: int,
    logs: dict[int, int],
    zeta211: int,
    zeta7: int,
    p_log_inv: int,
) -> tuple[int, int, int]:
    tau = sum(
        character(v, k, logs, zeta7, p_log_inv) * pow(zeta211, v, FIELD_Q)
        for v in range(1, RIGHT)
    ) % FIELD_Q
    projection = sum(
        pow(character(s, k, logs, zeta7, p_log_inv), -1, FIELD_Q) * profile[s]
        for s in range(1, RIGHT)
    ) % FIELD_Q
    return tau, projection, tau * projection % FIELD_Q


def random_profile(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _ in range(RIGHT)]


def force_trivial_augmentation_zero(profile: list[int], zeta211: int, zeta7: int, p_log: int) -> list[int]:
    adjusted = profile[:]
    periods = right_dft(adjusted, zeta211)
    a0 = orbit_augmentation(periods, 0, zeta7, p_log)
    adjusted[0] = (adjusted[0] - a0 * pow(RIGHT - 1, -1, FIELD_Q)) % FIELD_Q
    return adjusted


def quotient_index(value: int, logs: dict[int, int], p_log_inv: int) -> int:
    return (p_log_inv * logs[value]) % ORDER7


def force_all_order7_quotient_sums_zero(
    profile: list[int],
    logs: dict[int, int],
    p_log_inv: int,
) -> list[int]:
    adjusted = profile[:]
    for residue in range(ORDER7):
        members = [
            s
            for s in range(1, RIGHT)
            if quotient_index(s, logs, p_log_inv) == residue
        ]
        total = sum(adjusted[s] for s in members) % FIELD_Q
        adjusted[members[0]] = (adjusted[members[0]] - total) % FIELD_Q
    return adjusted


def nontrivial_zero_count(profile: list[int], zeta211: int, zeta7: int, p_log: int) -> int:
    periods = right_dft(profile, zeta211)
    return sum(
        int(orbit_augmentation(periods, k, zeta7, p_log) == 0)
        for k in range(1, ORDER7)
    )


def main() -> None:
    p_mod = P24 % RIGHT
    logs = log_table_mod_211()
    p_log = logs[p_mod]
    p_log_inv = pow(p_log % ORDER7, -1, ORDER7)
    root, zeta211, zeta7 = roots()
    rng = random.Random(20260606)

    orbit_weight_mismatches = 0
    gauss_sum_mismatches = 0
    gauss_sum_zeroes = 0
    for _trial in range(12):
        profile = random_profile(rng)
        periods = right_dft(profile, zeta211)
        for k in range(1, ORDER7):
            orbit_value = orbit_augmentation(periods, k, zeta7, p_log)
            character_value = character_period_sum(periods, k, logs, zeta7, p_log_inv)
            tau, projection, formula_value = gauss_sum_formula(
                profile,
                k,
                logs,
                zeta211,
                zeta7,
                p_log_inv,
            )
            orbit_weight_mismatches += int(orbit_value != character_value)
            gauss_sum_mismatches += int(orbit_value != formula_value)
            gauss_sum_zeroes += int(tau == 0 or projection == 0)

    centered_only = force_trivial_augmentation_zero(random_profile(rng), zeta211, zeta7, p_log)
    centered_periods = right_dft(centered_only, zeta211)
    centered_a0_zero = orbit_augmentation(centered_periods, 0, zeta7, p_log) == 0
    centered_nontrivial_zeroes = nontrivial_zero_count(centered_only, zeta211, zeta7, p_log)

    forced = force_all_order7_quotient_sums_zero(random_profile(rng), logs, p_log_inv)
    forced_nontrivial_zeroes = nontrivial_zero_count(forced, zeta211, zeta7, p_log)

    print("Trace-GCD fixed-frequency order-7 character-projection toy")
    print(f"field_q={FIELD_Q}")
    print(f"field_primitive_root={root}")
    print(f"p24_p_mod_211={p_mod}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p_log_mod_7={p_log % ORDER7}")
    print(f"p_log_inverse_mod_7={p_log_inv}")
    print(f"orbit_character_weight_mismatches={orbit_weight_mismatches}")
    print(f"gauss_sum_equivalence_mismatches={gauss_sum_mismatches}")
    print(f"nonzero_gauss_sum_and_random_projection_checks={72 - gauss_sum_zeroes}/72")
    print(f"ordinary_centering_trivial_component_zero={int(centered_a0_zero)}")
    print(f"ordinary_centering_only_nontrivial_zeroes={centered_nontrivial_zeroes}/6")
    print(f"forced_projection_zeroes={forced_nontrivial_zeroes}/6")
    print("interpretation")
    print("  order7_augmentation_is_character_projection_vanishing=1")
    print("  generic_centering_does_not_prove_order7_augmentation=1")
    print("  p24_missing_theorem_is_a_right_order7_profile_vanishing=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_character_projection_toy")

    if (p_mod, p_log, p_log_inv) != (114, 198, 4):
        raise SystemExit(1)
    if orbit_weight_mismatches or gauss_sum_mismatches or gauss_sum_zeroes:
        raise SystemExit(1)
    if not centered_a0_zero or centered_nontrivial_zeroes != 0:
        raise SystemExit(1)
    if forced_nontrivial_zeroes != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
