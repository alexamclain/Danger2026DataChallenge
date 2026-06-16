#!/usr/bin/env python3
"""Split the recombined p24 balance into mixed spectrum plus anchor.

For one nontrivial right order-7 character, the recombined coefficient target is

    sum_{k in D} c_k = |W| c_0

for every nonzero W=<p>-coset D in F_n^*.  Since F_n^*/W has order 8 for p24,
Fourier inversion on this quotient says this is equivalent to:

    1. seven nontrivial octic quotient-character sums vanish;
    2. the trivial quotient sum satisfies sum_{k != 0} c_k = (n-1)c_0.

After expanding

    c_k = sum_r chi^{-1}(r mod 211) j_{r+m*k},

the seven nontrivial equations are mixed right-order-7 / relative-octic
character sums of the ordered embedded CM sequence.  The trivial quotient
equation is the already named trace-defect anchor.  This script checks that
finite algebra in a split toy model and prints the p24 equation counts.
"""

from __future__ import annotations

import random


FIELD_Q = 337  # 337 - 1 is divisible by 7 and 8.
RIGHT = 43  # RIGHT - 1 = 42, quotient by a size-6 subgroup has order 7.
RIGHT_QUOTIENT = 7
RELATIVE_N = 73  # RELATIVE_N - 1 = 72, quotient by W of order 9 has order 8.
RELATIVE_QUOTIENT = 8
RELATIVE_W_ORDER = (RELATIVE_N - 1) // RELATIVE_QUOTIENT
LEFT_DUMMY = 3
M = LEFT_DUMMY * RIGHT
SEED = 20260606
TRIALS = 48

P24_RIGHT = 211
P24_RELATIVE_N = 3107441
P24_RECOMBINED_W_ORDER = 388430
P24_RIGHT_NONTRIVIAL = 6
P24_RELATIVE_QUOTIENT = 8


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


def subgroup_cosets(modulus: int, quotient_order: int) -> list[list[int]]:
    generator = primitive_root_mod_prime(modulus)
    logs = log_table(modulus, generator)
    cosets: list[list[int]] = [[] for _ in range(quotient_order)]
    for value in range(1, modulus):
        cosets[logs[value] % quotient_order].append(value)
    return cosets


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


def random_j_values(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _ in range(M * RELATIVE_N)]


def coefficients(
    j_values: list[int],
    right_logs: dict[int, int],
    zeta7: int,
    right_character: int,
) -> list[int]:
    out = [0] * RELATIVE_N
    for k in range(RELATIVE_N):
        total = 0
        for r in range(M):
            residue = r % RIGHT
            if residue == 0:
                continue
            weight = character_value(
                residue,
                RIGHT,
                RIGHT_QUOTIENT,
                zeta7,
                right_logs,
                -right_character,
            )
            total = (total + weight * j_values[r + M * k]) % FIELD_Q
        out[k] = total
    return out


def coset_sums(coeffs: list[int], cosets: list[list[int]]) -> list[int]:
    return [sum(coeffs[index] for index in coset) % FIELD_Q for coset in cosets]


def balanced(coeffs: list[int], cosets: list[list[int]]) -> bool:
    target = (RELATIVE_W_ORDER * coeffs[0]) % FIELD_Q
    return all(value == target for value in coset_sums(coeffs, cosets))


def octic_spectrum(
    coeffs: list[int],
    rel_logs: dict[int, int],
    zeta8: int,
) -> list[int]:
    values: list[int] = []
    for character in range(RELATIVE_QUOTIENT):
        total = 0
        for k in range(1, RELATIVE_N):
            total = (
                total
                + character_value(k, RELATIVE_N, RELATIVE_QUOTIENT, zeta8, rel_logs, character)
                * coeffs[k]
            ) % FIELD_Q
        values.append(total)
    return values


def mixed_spectrum_direct(
    j_values: list[int],
    right_logs: dict[int, int],
    rel_logs: dict[int, int],
    zeta7: int,
    zeta8: int,
    right_character: int,
    relative_character: int,
) -> int:
    total = 0
    for k in range(1, RELATIVE_N):
        rel_weight = character_value(
            k,
            RELATIVE_N,
            RELATIVE_QUOTIENT,
            zeta8,
            rel_logs,
            relative_character,
        )
        for r in range(M):
            residue = r % RIGHT
            if residue == 0:
                continue
            right_weight = character_value(
                residue,
                RIGHT,
                RIGHT_QUOTIENT,
                zeta7,
                right_logs,
                -right_character,
            )
            total = (total + right_weight * rel_weight * j_values[r + M * k]) % FIELD_Q
    return total


def anchor(coeffs: list[int]) -> int:
    return (sum(coeffs[1:]) - (RELATIVE_N - 1) * coeffs[0]) % FIELD_Q


def trace_defect_anchor_direct(
    j_values: list[int],
    right_logs: dict[int, int],
    zeta7: int,
    right_character: int,
) -> int:
    total = 0
    for r in range(M):
        residue = r % RIGHT
        if residue == 0:
            continue
        right_weight = character_value(
            residue,
            RIGHT,
            RIGHT_QUOTIENT,
            zeta7,
            right_logs,
            -right_character,
        )
        relative_trace = sum(j_values[r + M * k] for k in range(RELATIVE_N)) % FIELD_Q
        defect = (relative_trace - RELATIVE_N * j_values[r]) % FIELD_Q
        total = (total + right_weight * defect) % FIELD_Q
    return total


def force_balanced_coefficients(rng: random.Random, cosets: list[list[int]]) -> list[int]:
    coeffs = [0] * RELATIVE_N
    coeffs[0] = rng.randrange(FIELD_Q)
    target = (RELATIVE_W_ORDER * coeffs[0]) % FIELD_Q
    for coset in cosets:
        running = 0
        for index in coset[:-1]:
            coeffs[index] = rng.randrange(FIELD_Q)
            running = (running + coeffs[index]) % FIELD_Q
        coeffs[coset[-1]] = (target - running) % FIELD_Q
    return coeffs


def coeffs_to_j_values(
    coeffs: list[int],
    right_logs: dict[int, int],
    zeta7: int,
    right_character: int,
) -> list[int]:
    """Embed requested coefficients into one right residue.

    Pick a nonzero residue whose inverse right-character weight is invertible,
    then put all coefficient mass there.  This is only a toy realization to
    check the equivalence between balanced coefficients and expanded mixed
    spectrum equations.
    """
    residue = 1
    weight = character_value(
        residue,
        RIGHT,
        RIGHT_QUOTIENT,
        zeta7,
        right_logs,
        -right_character,
    )
    inv_weight = pow(weight, -1, FIELD_Q)
    values = [0] * (M * RELATIVE_N)
    for k, coeff in enumerate(coeffs):
        values[residue + M * k] = coeff * inv_weight % FIELD_Q
    return values


def main() -> None:
    rng = random.Random(SEED)
    right_generator = primitive_root_mod_prime(RIGHT)
    relative_generator = primitive_root_mod_prime(RELATIVE_N)
    right_logs = log_table(RIGHT, right_generator)
    rel_logs = log_table(RELATIVE_N, relative_generator)
    zeta7 = root_of_order(RIGHT_QUOTIENT)
    zeta8 = root_of_order(RELATIVE_QUOTIENT)
    rel_cosets = subgroup_cosets(RELATIVE_N, RELATIVE_QUOTIENT)

    balance_equivalence_failures = 0
    mixed_expansion_failures = 0
    anchor_expansion_failures = 0
    random_balanced_count = 0
    forced_balanced_count = 0
    forced_mixed_zero_count = 0
    forced_anchor_zero_count = 0

    for _trial in range(TRIALS):
        j_values = random_j_values(rng)
        coeffs = coefficients(j_values, right_logs, zeta7, 1)
        spectrum = octic_spectrum(coeffs, rel_logs, zeta8)
        anchor_value = anchor(coeffs)
        finite_balanced = balanced(coeffs, rel_cosets)
        spectrum_balanced = (
            all(value == 0 for value in spectrum[1:])
            and anchor_value == 0
        )
        balance_equivalence_failures += int(finite_balanced != spectrum_balanced)
        random_balanced_count += int(finite_balanced)
        for relative_character in range(1, RELATIVE_QUOTIENT):
            direct = mixed_spectrum_direct(
                j_values,
                right_logs,
                rel_logs,
                zeta7,
                zeta8,
                1,
                relative_character,
            )
            mixed_expansion_failures += int(direct != spectrum[relative_character])
        anchor_expansion_failures += int(
            trace_defect_anchor_direct(j_values, right_logs, zeta7, 1) != anchor_value
        )

        forced_coeffs = force_balanced_coefficients(rng, rel_cosets)
        forced_j_values = coeffs_to_j_values(forced_coeffs, right_logs, zeta7, 1)
        forced_spectrum = octic_spectrum(forced_coeffs, rel_logs, zeta8)
        forced_anchor = anchor(forced_coeffs)
        forced_balanced_count += int(balanced(forced_coeffs, rel_cosets))
        forced_mixed_zero_count += int(all(value == 0 for value in forced_spectrum[1:]))
        forced_anchor_zero_count += int(forced_anchor == 0)
        if coefficients(forced_j_values, right_logs, zeta7, 1) != forced_coeffs:
            raise RuntimeError("forced toy coefficients did not embed")

    print("Trace-GCD fixed-frequency p24 recombined mixed-spectrum gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_right={RIGHT}")
    print(f"toy_right_generator={right_generator}")
    print(f"toy_right_quotient={RIGHT_QUOTIENT}")
    print(f"toy_relative_n={RELATIVE_N}")
    print(f"toy_relative_generator={relative_generator}")
    print(f"toy_relative_w_order={RELATIVE_W_ORDER}")
    print(f"toy_relative_quotient={RELATIVE_QUOTIENT}")
    print(f"balance_equivalence_failures={balance_equivalence_failures}")
    print(f"mixed_expansion_failures={mixed_expansion_failures}")
    print(f"anchor_expansion_failures={anchor_expansion_failures}")
    print(f"random_balanced_count={random_balanced_count}/{TRIALS}")
    print(f"forced_balanced_count={forced_balanced_count}/{TRIALS}")
    print(f"forced_mixed_spectrum_zero={forced_mixed_zero_count}/{TRIALS}")
    print(f"forced_anchor_zero={forced_anchor_zero_count}/{TRIALS}")
    print(f"p24_right={P24_RIGHT}")
    print(f"p24_relative_n={P24_RELATIVE_N}")
    print(f"p24_recombined_w_order={P24_RECOMBINED_W_ORDER}")
    print(f"p24_relative_quotient={P24_RELATIVE_QUOTIENT}")
    print(f"p24_equations_per_right_character={P24_RELATIVE_QUOTIENT}")
    print(f"p24_right_nontrivial_characters={P24_RIGHT_NONTRIVIAL}")
    print(f"p24_mixed_octic_equations={P24_RIGHT_NONTRIVIAL * (P24_RELATIVE_QUOTIENT - 1)}")
    print(f"p24_anchor_equations={P24_RIGHT_NONTRIVIAL}")
    print(f"p24_recombined_scalar_equations={P24_RIGHT_NONTRIVIAL * P24_RELATIVE_QUOTIENT}")
    print("interpretation")
    print("  recombined_balance_iff_mixed_octic_spectrum_plus_anchor=1")
    print("  nontrivial_octic_equations_are_right_order7_by_relative_octic_mixed_sums=1")
    print("  trivial_octic_equations_are_trace_defect_anchors=1")
    print("  random_ordered_sequences_do_not_satisfy_the_balance=1")
    print("  remaining_theorem_is_specific_cm_lang_mixed_spectrum_vanishing=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_recombined_mixed_spectrum_gate")

    if balance_equivalence_failures:
        raise SystemExit(1)
    if mixed_expansion_failures:
        raise SystemExit(1)
    if anchor_expansion_failures:
        raise SystemExit(1)
    if random_balanced_count:
        raise SystemExit(1)
    if forced_balanced_count != TRIALS:
        raise SystemExit(1)
    if forced_mixed_zero_count != TRIALS or forced_anchor_zero_count != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
