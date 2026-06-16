#!/usr/bin/env python3
"""Robert C-phase character obstruction for the p25 square-axis bridge.

The oriented-phase contract identifies the needed C-side phase on the active
C-values:

    + on 25, 28, 31
    - on 138, 141, 144 = -31, -28, -25 mod 169.

This gate checks whether that phase can be a plain character/tag on C_169.  It
cannot.  Since C_169 has odd order, there is no nontrivial homomorphism
C_169 -> {+/-1}.  More generally, for any 169th-root character chi_b(c), an
odd phase would require

    chi_b(-c) = -chi_b(c)

on an active pair, i.e. chi_b(2c) = -1.  But -1 is not a 169th root of unity.

So the Robert/Siegel orientation cannot be a plain C-character, Legendre-style
tag, or scalar-shifted C-character.  It has to come from an oriented divisor,
quotient of conjugate units, y/differential data, or another non-character
finite identity.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_robert_oriented_phase_contract_gate import (
    active_c_phase,
    phase_profile,
)
from p25_laneB_robert_source_matrix_harness_gate import source_matrix_from_raw
from p25_laneB_square_axis_bridge_candidate_harness_gate import target_raw_bridge
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, MODULUS


@dataclass(frozen=True)
class CharacterScanProfile:
    character_count: int
    exact_phase_matches: int
    odd_on_active_pairs: int
    constant_on_positive_arc: int
    exact_negative_after_positive_normalization: int
    minus_one_in_c169_roots: bool
    sign_homomorphism_count: int
    nontrivial_sign_homomorphism_count: int


def c169_roots() -> tuple[int, ...]:
    root = primitive_root(MODULUS)
    zeta = pow(root, (MODULUS - 1) // C_ORDER, MODULUS)
    roots = tuple(pow(zeta, exponent, MODULUS) for exponent in range(C_ORDER))
    if len(set(roots)) != C_ORDER:
        raise AssertionError("failed to enumerate C169 roots")
    return roots


def character_values(exponent: int, roots: tuple[int, ...]) -> list[int]:
    return [roots[(exponent * c_log) % C_ORDER] for c_log in range(C_ORDER)]


def phase_values() -> tuple[tuple[int, ...], tuple[int, ...], list[int]]:
    target_matrix = source_matrix_from_raw(target_raw_bridge())
    profile = phase_profile(target_matrix)
    phase = active_c_phase(profile.positive_c_values, profile.negative_c_values)
    return profile.positive_c_values, profile.negative_c_values, phase


def scan_characters() -> CharacterScanProfile:
    positive_c_values, negative_c_values, phase = phase_values()
    roots = c169_roots()
    exact_phase_matches = 0
    odd_on_active_pairs = 0
    constant_on_positive_arc = 0
    exact_negative_after_positive_normalization = 0

    for exponent in range(C_ORDER):
        values = character_values(exponent, roots)
        normalizer = pow(values[positive_c_values[0]], -1, MODULUS)
        normalized = [(normalizer * value) % MODULUS for value in values]

        exact_phase_matches += int(
            all(normalized[c_log] == phase[c_log] % MODULUS for c_log in positive_c_values)
            and all(normalized[c_log] == phase[c_log] % MODULUS for c_log in negative_c_values)
        )
        odd_on_active_pairs += int(
            all(values[(-c_log) % C_ORDER] == (-values[c_log]) % MODULUS for c_log in positive_c_values)
        )
        positive_constant = all(
            normalized[c_log] == 1 for c_log in positive_c_values
        )
        constant_on_positive_arc += int(positive_constant)
        exact_negative_after_positive_normalization += int(
            positive_constant
            and all(normalized[c_log] == MODULUS - 1 for c_log in negative_c_values)
        )

    # A homomorphism from C_169 to {+/-1} is determined by the generator image.
    sign_homomorphism_count = sum(1 for image in (1, -1) if image**C_ORDER == 1)
    nontrivial_sign_homomorphism_count = sum(
        1 for image in (-1,) if image**C_ORDER == 1
    )

    return CharacterScanProfile(
        character_count=C_ORDER,
        exact_phase_matches=exact_phase_matches,
        odd_on_active_pairs=odd_on_active_pairs,
        constant_on_positive_arc=constant_on_positive_arc,
        exact_negative_after_positive_normalization=exact_negative_after_positive_normalization,
        minus_one_in_c169_roots=(MODULUS - 1) in set(roots),
        sign_homomorphism_count=sign_homomorphism_count,
        nontrivial_sign_homomorphism_count=nontrivial_sign_homomorphism_count,
    )


def main() -> int:
    print("p25 Lane B Robert C-phase character obstruction gate")
    print(f"c_order={C_ORDER} modulus={MODULUS}")
    positive_c_values, negative_c_values, phase = phase_values()
    scan = scan_characters()
    active_phase_support = tuple(
        c_log for c_log, value in enumerate(phase) if value
    )
    row_ok = (
        positive_c_values == (25, 28, 31)
        and negative_c_values == (138, 141, 144)
        and active_phase_support == (25, 28, 31, 138, 141, 144)
        and scan.character_count == 169
        and scan.exact_phase_matches == 0
        and scan.odd_on_active_pairs == 0
        and scan.constant_on_positive_arc == 1
        and scan.exact_negative_after_positive_normalization == 0
        and not scan.minus_one_in_c169_roots
        and scan.sign_homomorphism_count == 1
        and scan.nontrivial_sign_homomorphism_count == 0
    )

    print(
        "active_phase: "
        f"positive={positive_c_values} "
        f"negative={negative_c_values} "
        f"support={active_phase_support}"
    )
    print(f"character_scan={scan}")
    print("character_obstruction_law")
    print("  C169 has odd order, so no nontrivial +/-1 character exists")
    print("  169th-root characters cannot satisfy chi(-c)=-chi(c), because -1 is not a 169th root")
    print("  scalar shifts/normalizations of C-characters do not recover the active +/- phase")
    print(f"robert_c_phase_character_obstruction_rows={int(row_ok)}/1")
    print("interpretation")
    print("  robert_phase_cannot_be_a_plain_C169_character_or_sign_tag=1")
    print("  orientation_must_come_from_divisor_quotient_y_data_or_unit_phase_identity=1")
    print("conclusion=reported_p25_laneB_robert_c_phase_character_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
