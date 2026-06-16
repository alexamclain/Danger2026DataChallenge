#!/usr/bin/env python3
"""Residue-mask character-support gate for p25 Lane B.

The residue-mask coupling gate rules out separated row/column masks.  This gate
checks the full character footprint of the binary canonical carry mask on
C_3 x C_c.

The support is maximal subject to equal row sums:

    scalar:      present;
    pure right:  absent;
    pure C:      every nontrivial C character present;
    mixed:       every nontrivial right and nontrivial C character present.

Thus a producer cannot hide in a small character set.  It must supply the full
two-dimensional C_3 x C_c character payload of the residue mask.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import CASES as PULLBACK_CASES, PullbackCase
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class CharacterProfile:
    nonzero: int
    scalar: int
    pure_right: int
    pure_c: int
    mixed: int


def character_coefficients(c_axis: int, modulus: int) -> list[int]:
    root = primitive_root(modulus)
    zeta_right = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zeta_c = pow(root, (modulus - 1) // c_axis, modulus)
    coeffs: list[int] = []
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(c_axis):
            total = 0
            for right in range(RIGHT_DEGREE):
                for c_index in range(c_axis):
                    total += (
                        template_bits(c_axis, c_index)[right]
                        * pow(zeta_right, right_frequency * right, modulus)
                        * pow(zeta_c, c_frequency * c_index, modulus)
                    )
            coeffs.append(total % modulus)
    return coeffs


def character_profile(c_axis: int, modulus: int) -> CharacterProfile:
    coeffs = character_coefficients(c_axis, modulus)
    nonzero = 0
    scalar = 0
    pure_right = 0
    pure_c = 0
    mixed = 0
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(c_axis):
            value = coeffs[right_frequency * c_axis + c_frequency]
            if not value:
                continue
            nonzero += 1
            if right_frequency == 0 and c_frequency == 0:
                scalar += 1
            elif right_frequency != 0 and c_frequency == 0:
                pure_right += 1
            elif right_frequency == 0 and c_frequency != 0:
                pure_c += 1
            else:
                mixed += 1
    return CharacterProfile(nonzero, scalar, pure_right, pure_c, mixed)


def audit_case(case: PullbackCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    profile = character_profile(case.c_axis, modulus)
    expected_nonzero = 1 + (case.c_axis - 1) + (RIGHT_DEGREE - 1) * (case.c_axis - 1)
    row_ok = (
        profile.nonzero == expected_nonzero
        and profile.scalar == 1
        and profile.pure_right == 0
        and profile.pure_c == case.c_axis - 1
        and profile.mixed == (RIGHT_DEGREE - 1) * (case.c_axis - 1)
    )
    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"nonzero={profile.nonzero} expected_nonzero={expected_nonzero} "
            f"scalar={profile.scalar} pure_right={profile.pure_right} "
            f"pure_c={profile.pure_c}/{case.c_axis - 1} "
            f"mixed={profile.mixed}/{(RIGHT_DEGREE - 1) * (case.c_axis - 1)} "
            f"ok={int(row_ok)}"
        )
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B residue-mask character-support gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in PULLBACK_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"residue_mask_character_support_rows={ok_rows}/{len(PULLBACK_CASES)}")
    print("interpretation")
    print("  residue_mask_has_no_pure_right_character_support=1")
    print("  residue_mask_has_every_nontrivial_pure_C_character=1")
    print("  residue_mask_has_every_mixed_right_C_character=1")
    print("  sparse_character_support_producers_are_ruled_out=1")
    print("conclusion=reported_p25_laneB_residue_mask_character_support_gate")
    return 0 if ok_rows == len(PULLBACK_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
