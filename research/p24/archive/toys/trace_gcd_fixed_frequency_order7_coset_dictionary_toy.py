#!/usr/bin/env python3
"""Coset dictionary for the p24 order-7 augmentation target.

This is a finite group bookkeeping gate for the fixed-frequency theorem.  Let
`2` be the primitive root modulo 211.  For p24,

    p = 2^198 mod 211,

so the Frobenius right orbits are the six cosets of `<p>` and the Gaussian
coset representatives can be taken as `2^(35*j)`, `0 <= j < 6`.

At fixed frequencies the length-35 orbit collapses by summing positions
`s+7t`.  Across the six Gaussian labels, those collapsed sums are exactly the
coset sums for the order-30 subgroup of `(Z/211Z)^*` whose discrete logarithms
are multiples of 7.  Thus the order-7 augmentation identity is not ordinary
centering: it kills all seven quotient-character components, while ordinary
centering kills only the trivial one.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
Q = 29
ORBIT_COUNT = 6
ORBIT_LEN = 35
FIXED_COUNT = 7
ORDER5_COUNT = 5


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_base_2_mod_211(value: int) -> int:
    current = 1
    for exponent in range(RIGHT - 1):
        if current == value:
            return exponent
        current = current * GEN % RIGHT
    raise ValueError("value is not a nonzero residue")


def orbit_exponent(label: int, position: int, p_log: int) -> int:
    return (35 * label + p_log * position) % (RIGHT - 1)


def collapsed_six_orbit_sums(values: list[list[int]]) -> list[int]:
    return [
        sum(
            values[label][s + FIXED_COUNT * t]
            for label in range(ORBIT_COUNT)
            for t in range(ORDER5_COUNT)
        ) % Q
        for s in range(FIXED_COUNT)
    ]


def exponent_coset_sums(values: list[list[int]], p_log: int) -> list[int]:
    sums = [0] * FIXED_COUNT
    for label in range(ORBIT_COUNT):
        for position in range(ORBIT_LEN):
            residue = orbit_exponent(label, position, p_log) % FIXED_COUNT
            sums[residue] = (sums[residue] + values[label][position]) % Q
    return sums


def dft7(values: list[int]) -> list[int]:
    root = primitive_root(Q)
    zeta = pow(root, (Q - 1) // FIXED_COUNT, Q)
    return [
        sum(value * pow(zeta, frequency * index, Q) for index, value in enumerate(values)) % Q
        for frequency in range(FIXED_COUNT)
    ]


def random_values(rng: random.Random) -> list[list[int]]:
    return [
        [rng.randrange(Q) for _ in range(ORBIT_LEN)]
        for _label in range(ORBIT_COUNT)
    ]


def augmentation_zero_values() -> list[list[int]]:
    values = [[0 for _ in range(ORBIT_LEN)] for _label in range(ORBIT_COUNT)]
    for s in range(FIXED_COUNT):
        values[0][s] = 1
        values[1][s] = Q - 1
    return values


def centering_only_values() -> list[list[int]]:
    values = [[0 for _ in range(ORBIT_LEN)] for _label in range(ORBIT_COUNT)]
    values[0][0] = 1
    values[0][1] = Q - 1
    return values


def summarize_case(label: str, values: list[list[int]], p_log: int) -> tuple[int, int, int, int]:
    collapsed = collapsed_six_orbit_sums(values)
    coset = exponent_coset_sums(values, p_log)
    remapped = [0] * FIXED_COUNT
    for s, value in enumerate(collapsed):
        remapped[(p_log * s) % FIXED_COUNT] = value
    evals = dft7(collapsed)
    dictionary_ok = remapped == coset
    coefficient_zeroes = sum(int(value == 0) for value in collapsed)
    quotient_character_zeroes = sum(int(value == 0) for value in evals)
    centering = evals[0] == 0
    print(
        f"case={label} dictionary_ok={int(dictionary_ok)} "
        f"centering_at_y1={int(centering)} "
        f"augmentation_coeff_zeroes={coefficient_zeroes}/7 "
        f"quotient_character_zeroes={quotient_character_zeroes}/7 "
        f"nontrivial_quotient_character_zeroes={quotient_character_zeroes - int(centering)}/6"
    )
    return int(dictionary_ok), int(centering), coefficient_zeroes, quotient_character_zeroes


def main() -> None:
    p_mod = P24 % RIGHT
    p_log = log_base_2_mod_211(p_mod)
    subgroup_exponents = sorted({(35 * a + 7 * p_log * b) % (RIGHT - 1) for a in range(ORBIT_COUNT) for b in range(ORDER5_COUNT)})
    rng = random.Random(20260606)
    cases = [
        ("augmentation_zero", augmentation_zero_values()),
        ("ordinary_centering_only", centering_only_values()),
        ("random_control", random_values(rng)),
    ]

    print("Trace-GCD fixed-frequency order-7 coset dictionary toy")
    print(f"right={RIGHT}")
    print(f"primitive_root={GEN}")
    print(f"p24_p_mod_211={p_mod}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p_log_mod_7={p_log % FIXED_COUNT}")
    print(f"order30_subgroup_size={len(subgroup_exponents)}")
    print(
        "order30_subgroup_exponents_are_multiples_of_7="
        f"{int(all(exponent % FIXED_COUNT == 0 for exponent in subgroup_exponents))}"
    )
    summaries = [summarize_case(label, values, p_log) for label, values in cases]
    print("interpretation")
    print("  order5_collapsed_six_orbit_sums_are_order7_coset_sums=1")
    print("  ordinary_centering_is_only_the_trivial_quotient_character=1")
    print("  order7_augmentation_kills_all_C7_quotient_characters=1")
    print("  p24_augmentation_theorem_is_a_gaussian_period_vanishing_statement=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_coset_dictionary_toy")

    if p_log != 198 or len(subgroup_exponents) != 30:
        raise SystemExit(1)
    if not all(summary[0] for summary in summaries):
        raise SystemExit(1)
    augmentation, centering_only, _random = summaries
    if augmentation[2:] != (7, 7):
        raise SystemExit(1)
    if centering_only[1:] != (1, 5, 1):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
