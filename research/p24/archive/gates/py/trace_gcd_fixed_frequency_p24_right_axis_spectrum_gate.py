#!/usr/bin/env python3
"""Right-axis spectrum form of the p24 weighted-polynomial target.

After the right Gauss-sum reduction, the remaining identity is the vanishing
of all nontrivial order-7 multiplicative character projections on the
right 211-axis of an internally traced profile.

This gate records the exact p24 Frobenius bookkeeping:

* rho=p^780 shifts the right H-quotient by 6 mod 7;
* the internal generator p^5460=rho^7 fixes the right 211-axis completely.

Therefore the B/C and C/E internal traces do not themselves average the
right H-cosets.  The missing theorem is precisely that the internally traced
G_chi profile has no order-7 multiplicative spectrum, equivalently equal
H-coset sums on F_211^*.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
FIELD_Q = 43
RHO_EXPONENT = 780
INTERNAL_EXPONENT = 5460
SEED = 20260606


Vector = list[int]


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


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def character(value: int, zeta7: int, logs: dict[int, int], index: int) -> int:
    value %= RIGHT
    if value == 0:
        return 0
    return pow(zeta7, (index * logs[value]) % ORDER7, FIELD_Q)


def order7_projection(profile: Vector, zeta7: int, logs: dict[int, int], index: int) -> int:
    total = 0
    for residue in range(1, RIGHT):
        weight = pow(character(residue, zeta7, logs, index), -1, FIELD_Q)
        total = (total + weight * profile[residue]) % FIELD_Q
    return total


def h_coset_sums(profile: Vector, logs: dict[int, int]) -> list[int]:
    sums = [0] * ORDER7
    for residue in range(1, RIGHT):
        sums[logs[residue] % ORDER7] = (
            sums[logs[residue] % ORDER7] + profile[residue]
        ) % FIELD_Q
    return sums


def random_profile(rng: random.Random) -> Vector:
    return [rng.randrange(FIELD_Q) for _index in range(RIGHT)]


def force_equal_h_coset_sums(profile: Vector, logs: dict[int, int]) -> Vector:
    adjusted = profile[:]
    sums = h_coset_sums(adjusted, logs)
    target = sums[0]
    representatives = [None] * ORDER7
    for residue in range(1, RIGHT):
        coset = logs[residue] % ORDER7
        if representatives[coset] is None:
            representatives[coset] = residue
    for coset in range(1, ORDER7):
        residue = representatives[coset]
        if residue is None:
            raise RuntimeError("missing coset representative")
        adjusted[residue] = (adjusted[residue] + target - sums[coset]) % FIELD_Q
    return adjusted


def projections_all_zero(profile: Vector, zeta7: int, logs: dict[int, int]) -> bool:
    return all(
        order7_projection(profile, zeta7, logs, index) == 0
        for index in range(1, ORDER7)
    )


def coset_sums_equal(profile: Vector, logs: dict[int, int]) -> bool:
    sums = h_coset_sums(profile, logs)
    return len(set(sums)) == 1


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    root = primitive_root(FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q)
    p_log = logs[P24 % RIGHT]
    rho_log = logs[pow(P24, RHO_EXPONENT, RIGHT)]
    internal_log = logs[pow(P24, INTERNAL_EXPONENT, RIGHT)]

    rng = random.Random(SEED)
    random_projection_leaks = 0
    forced_projection_zeroes = 0
    equivalence_failures = 0
    residue_zero_irrelevant_failures = 0
    trials = 48

    for _trial in range(trials):
        profile = random_profile(rng)
        random_projection_leaks += int(not projections_all_zero(profile, zeta7, logs))
        forced = force_equal_h_coset_sums(profile, logs)
        forced_projection_zeroes += int(
            projections_all_zero(forced, zeta7, logs)
            and coset_sums_equal(forced, logs)
        )
        equivalence_failures += int(
            projections_all_zero(profile, zeta7, logs)
            != coset_sums_equal(profile, logs)
        )
        changed_zero = profile[:]
        changed_zero[0] = (changed_zero[0] + rng.randrange(1, FIELD_Q)) % FIELD_Q
        residue_zero_irrelevant_failures += int(
            [
                order7_projection(profile, zeta7, logs, index)
                for index in range(1, ORDER7)
            ]
            != [
                order7_projection(changed_zero, zeta7, logs, index)
                for index in range(1, ORDER7)
            ]
        )

    print("Trace-GCD fixed-frequency p24 right-axis spectrum gate")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"field_q={FIELD_Q}")
    print(f"zeta7={zeta7}")
    print(f"p24_mod_211={P24 % RIGHT}")
    print(f"p24_log_base2_mod_211={p_log}")
    print(f"p24_log_mod_order7_quotient={p_log % ORDER7}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_log_mod_order7_quotient={rho_log % ORDER7}")
    print(f"internal_exponent={INTERNAL_EXPONENT}")
    print(f"internal_log_base2_mod_211={internal_log}")
    print(f"internal_log_mod_order7_quotient={internal_log % ORDER7}")
    print(f"random_profiles_with_order7_leak={random_projection_leaks}/{trials}")
    print(f"forced_equal_H_coset_sums_projection_zero={forced_projection_zeroes}/{trials}")
    print(f"projection_zero_iff_H_coset_sums_equal_failures={equivalence_failures}")
    print(f"residue_zero_mod_211_irrelevant_failures={residue_zero_irrelevant_failures}")
    print("interpretation")
    print("  p780_shifts_right_order7_quotient_nontrivially=1")
    print("  p5460_internal_trace_fixes_right_211_axis=1")
    print("  internal_trace_does_not_average_right_H_cosets=1")
    print("  target_is_no_order7_multiplicative_spectrum_on_traced_right_axis=1")
    print("  equivalently_H_coset_sums_equal_on_F211_star=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_spectrum_gate")

    if p_log % ORDER7 != 2:
        raise SystemExit(1)
    if rho_log % ORDER7 != 6:
        raise SystemExit(1)
    if internal_log != 0:
        raise SystemExit(1)
    if random_projection_leaks != trials:
        raise SystemExit(1)
    if forced_projection_zeroes != trials:
        raise SystemExit(1)
    if equivalence_failures != 0:
        raise SystemExit(1)
    if residue_zero_irrelevant_failures != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
