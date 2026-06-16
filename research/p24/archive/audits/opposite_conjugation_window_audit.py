#!/usr/bin/env python3
"""Audit the tail-window convention for opposite-orbit conjugation.

For raw mixed DFT seed rows, inversion sends

    H(1, p^k v) -> H(-1, -p^k v).

In p24 the left negation is `-1 = p^78 mod 157`, so this raw seed expression
contains the semilinear right shift `T^78`.  After Lang trivialization,
however, `T^78` acts by coordinatewise Frobenius on the transformed Lang
coordinates.  It does not shift the Lang coordinate index.

This script records the p24 orbit-window offsets and verifies the Lang
coordinate convention in a small finite-field model.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp

from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)


P24 = 10**24 + 7
LEFT = 157
RIGHT = 211
TAIL_LEN = 16


def q_orbits(modulus: int, q: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(1, modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * q) % modulus
        out.append(orbit)
    return out


def first_power_for_value(q: int, modulus: int, target: int) -> int:
    value = 1
    for exponent in range(1, modulus):
        value = (value * q) % modulus
        if value == target % modulus:
            return exponent
    raise ValueError(f"{target} is not in the q-cyclic subgroup modulo {modulus}")


def field_matrix_from_lang_basis(
    q: int,
    orbit_len: int,
    field: ExtensionField,
    seed: int,
) -> list[list[FpE]]:
    basis = subfield_power_basis(q, orbit_len, field, seed)
    return [
        [field.pow(alpha, q**row) for alpha in basis]
        for row in range(orbit_len)
    ]


def semilinear_shift(
    vector: list[FpE],
    shift: int,
    field: ExtensionField,
) -> list[FpE]:
    length = len(vector)
    return [
        field.pow(vector[(index - shift) % length], field.q**shift)
        for index in range(length)
    ]


def random_field_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def lang_shift_mismatches(q: int, orbit_len: int, shift: int, seed: int) -> int:
    extension_degree = orbit_len
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    rng = random.Random(seed)
    lang_matrix = field_matrix_from_lang_basis(q, orbit_len, field, seed + 17)
    lang_inverse = lang_inverse_for_orbit(q, orbit_len, field, seed + 17)
    coords = [random_field_value(field, rng) for _ in range(orbit_len)]
    seed_vector = matrix_vector_mul(lang_matrix, coords, field)
    shifted_seed = semilinear_shift(seed_vector, shift, field)
    shifted_coords = matrix_vector_mul(lang_inverse, shifted_seed, field)
    expected = [field.pow(value, field.q**shift) for value in coords]
    return sum(1 for left, right in zip(shifted_coords, expected) if left != right)


def print_p24_windows() -> None:
    p_mod_left = P24 % LEFT
    p_mod_right = P24 % RIGHT
    left_neg_shift = first_power_for_value(p_mod_left, LEFT, -1)
    right_orbits = q_orbits(RIGHT, p_mod_right)
    print("p24 opposite conjugation window audit")
    print(f"p_mod_157={p_mod_left}")
    print(f"p_mod_211={p_mod_right}")
    print(f"left_neg_shift={left_neg_shift}")
    print(f"left_neg_shift_mod_right_orbit={left_neg_shift % len(right_orbits[0])}")
    for index, orbit in enumerate(right_orbits[:3], start=1):
        partner = next(
            other_index
            for other_index, other_orbit in enumerate(right_orbits, start=1)
            if (-orbit[0]) % RIGHT in other_orbit
        )
        partner_orbit = right_orbits[partner - 1]
        direct_negation = [(-value) % RIGHT for value in orbit[:TAIL_LEN]]
        raw_seed_after_left = [
            (-orbit[(coord - left_neg_shift) % len(orbit)]) % RIGHT
            for coord in range(TAIL_LEN)
        ]
        print(
            f"pair=O{index}/O{partner} "
            f"direct_negation_positions="
            f"{[partner_orbit.index(value) for value in direct_negation]} "
            f"raw_seed_after_left_positions="
            f"{[partner_orbit.index(value) for value in raw_seed_after_left]}"
        )
    print("lang_coordinate_rule=T^a_seed_maps_to_coordinatewise_Frobenius^a")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--orbit-len", type=int, default=5)
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()
    if sp.gcd(args.q, args.orbit_len) != 1:
        raise ValueError("q and orbit length should be coprime")
    print_p24_windows()
    mismatches = lang_shift_mismatches(
        args.q,
        args.orbit_len,
        args.shift,
        args.seed,
    )
    print(
        f"toy_q={args.q} toy_orbit_len={args.orbit_len} "
        f"toy_shift={args.shift}"
    )
    print(f"lang_shift_coordinate_mismatches={mismatches}")
    print("conclusion=reported_opposite_conjugation_window_audit")


if __name__ == "__main__":
    main()
