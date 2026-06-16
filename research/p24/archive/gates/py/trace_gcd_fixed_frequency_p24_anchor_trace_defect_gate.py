#!/usr/bin/env python3
"""Rephrase the p24 anchor equations as relative trace-defect spectrum.

For the recombined period-coset target, one right character has the anchor
equation

    sum_{k != 0} c_k(chi) = (n - 1) c_0(chi),

equivalently

    sum_k c_k(chi) = n c_0(chi).

With

    c_k(chi) = sum_r chi^(-1)(r mod right) j_{r+m*k},

this says the right quotient character projection of

    D_r = Tr_relative(j_{r+m*bullet}) - n*j_r

vanishes.  Thus the six p24 anchor equations are not a constant-term
bookkeeping detail: they are exactly the six nontrivial order-7 right-spectrum
equations for the relative trace defect of the chosen embedded child section.
"""

from __future__ import annotations

import random


FIELD_Q = 337  # 337 - 1 is divisible by 7.
LEFT = 3
RIGHT = 43  # RIGHT - 1 = 42, so quotient by a size-6 H has order 7.
RELATIVE = 5
M = LEFT * RIGHT
ORDER7 = 7
SEED = 20260606
TRIALS = 48

P24_RIGHT = 211
P24_RELATIVE = 3107441
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


def character_inverse(residue: int, zeta7: int, logs: dict[int, int], index: int) -> int:
    if residue % RIGHT == 0:
        return 0
    return pow(zeta7, (-index * logs[residue % RIGHT]) % ORDER7, FIELD_Q)


def random_j_values(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _index in range(M * RELATIVE)]


def coefficients(j_values: list[int], zeta7: int, logs: dict[int, int], index: int) -> list[int]:
    out = [0] * RELATIVE
    for k in range(RELATIVE):
        total = 0
        for r in range(M):
            residue = r % RIGHT
            if residue == 0:
                continue
            total = (
                total
                + character_inverse(residue, zeta7, logs, index)
                * j_values[r + M * k]
            ) % FIELD_Q
        out[k] = total
    return out


def anchor_value(j_values: list[int], zeta7: int, logs: dict[int, int], index: int) -> int:
    coeffs = coefficients(j_values, zeta7, logs, index)
    return (sum(coeffs) - RELATIVE * coeffs[0]) % FIELD_Q


def trace_defect_profile(j_values: list[int]) -> list[int]:
    profile = [0] * RIGHT
    for residue in range(1, RIGHT):
        total = 0
        for r in range(residue, M, RIGHT):
            relative_trace = sum(j_values[r + M * k] for k in range(RELATIVE)) % FIELD_Q
            chosen_child = j_values[r]
            total = (total + relative_trace - RELATIVE * chosen_child) % FIELD_Q
        profile[residue] = total
    return profile


def anchor_from_defect(profile: list[int], zeta7: int, logs: dict[int, int], index: int) -> int:
    return sum(
        character_inverse(residue, zeta7, logs, index) * profile[residue]
        for residue in range(1, RIGHT)
    ) % FIELD_Q


def h_coset_sums(profile: list[int], logs: dict[int, int]) -> list[int]:
    sums = [0] * ORDER7
    for residue in range(1, RIGHT):
        sums[logs[residue] % ORDER7] = (
            sums[logs[residue] % ORDER7] + profile[residue]
        ) % FIELD_Q
    return sums


def all_equal(values: list[int]) -> bool:
    return all(value == values[0] for value in values)


def anchors_zero(j_values: list[int], zeta7: int, logs: dict[int, int]) -> bool:
    return all(anchor_value(j_values, zeta7, logs, index) == 0 for index in range(1, ORDER7))


def j_values_with_defect_profile(profile: list[int]) -> list[int]:
    out = [0] * (M * RELATIVE)
    for residue in range(1, RIGHT):
        # Put the whole requested defect in one relative-trace slot.  Since
        # j_{r,0}=0, the defect is exactly j_{r,1}.
        out[residue + M] = profile[residue] % FIELD_Q
    return out


def random_equal_h_coset_profile(rng: random.Random, logs: dict[int, int]) -> list[int]:
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
    field_generator = primitive_root_mod_prime(FIELD_Q)
    zeta7 = pow(field_generator, (FIELD_Q - 1) // ORDER7, FIELD_Q)

    anchor_defect_mismatches = 0
    anchor_zero_coset_equivalence_failures = 0
    random_anchor_nonzero = 0
    forced_anchor_zero = 0
    forced_equal_cosets = 0

    for _trial in range(TRIALS):
        j_values = random_j_values(rng)
        profile = trace_defect_profile(j_values)
        anchors = [anchor_value(j_values, zeta7, logs, index) for index in range(1, ORDER7)]
        defect_anchors = [
            anchor_from_defect(profile, zeta7, logs, index)
            for index in range(1, ORDER7)
        ]
        anchor_defect_mismatches += int(anchors != defect_anchors)
        zero = all(value == 0 for value in anchors)
        equal = all_equal(h_coset_sums(profile, logs))
        anchor_zero_coset_equivalence_failures += int(zero != equal)
        random_anchor_nonzero += int(not zero)

        forced_profile = random_equal_h_coset_profile(rng, logs)
        forced_j = j_values_with_defect_profile(forced_profile)
        forced_anchor_zero += int(anchors_zero(forced_j, zeta7, logs))
        forced_equal_cosets += int(all_equal(h_coset_sums(forced_profile, logs)))

    print("Trace-GCD fixed-frequency p24 anchor trace-defect gate")
    print(f"field_q={FIELD_Q}")
    print(f"field_zeta7={zeta7}")
    print(f"toy_left={LEFT}")
    print(f"toy_right={RIGHT}")
    print(f"toy_right_generator={right_generator}")
    print(f"toy_relative={RELATIVE}")
    print(f"toy_m={M}")
    print(f"toy_h_coset_size={(RIGHT - 1) // ORDER7}")
    print(f"toy_order7_cosets={ORDER7}")
    print(f"anchor_defect_projection_mismatches={anchor_defect_mismatches}")
    print(f"anchor_zero_iff_trace_defect_h_coset_equal_failures={anchor_zero_coset_equivalence_failures}")
    print(f"random_anchor_nonzero={random_anchor_nonzero}/{TRIALS}")
    print(f"forced_trace_defect_equal_cosets={forced_equal_cosets}/{TRIALS}")
    print(f"forced_anchor_zero={forced_anchor_zero}/{TRIALS}")
    print(f"p24_right={P24_RIGHT}")
    print(f"p24_relative_n={P24_RELATIVE}")
    print(f"p24_anchor_equations={P24_RIGHT_NONTRIVIAL_CHARACTERS}")
    print("interpretation")
    print("  anchor_equation_equals_relative_trace_defect_character_projection=1")
    print("  six_anchors_zero_iff_trace_defect_has_equal_H_coset_sums=1")
    print("  p24_anchor_is_not_constant_term_bookkeeping=1")
    print("  p24_anchor_target_is_relative_trace_defect_order7_spectrum_zero=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate")

    if anchor_defect_mismatches:
        raise SystemExit(1)
    if anchor_zero_coset_equivalence_failures:
        raise SystemExit(1)
    if random_anchor_nonzero != TRIALS:
        raise SystemExit(1)
    if forced_equal_cosets != TRIALS or forced_anchor_zero != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
