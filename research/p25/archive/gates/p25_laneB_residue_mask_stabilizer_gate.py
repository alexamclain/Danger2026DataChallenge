#!/usr/bin/env python3
"""Residue-mask stabilizer gate for p25 Lane B.

The residue-mask coupling and character-support gates show that the canonical
carry mask is genuinely two-dimensional and character-rich.  This gate checks
whether the same mask can still be compressed by a hidden symmetry.

It cannot: for the p25 C_3 x C_c half-arc masks tested here, the stabilizer is
trivial under the full product-affine action

    right -> alpha * right + beta mod 3,
    C     -> u * C + v mod c,

with alpha in Aut(C_3), beta in C_3, u in Aut(C_c), and v in C_c.

Thus the producer target is rigid as a residue-coset mask: a candidate cannot
save degree by quotienting the 39-rectangle C_3 x C_13 target by a hidden
right/C translation, diamond, or affine symmetry.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_local_pullback_gate import CASES as PULLBACK_CASES, PullbackCase
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class StabilizerProfile:
    right_translations: tuple[int, ...]
    c_translations: tuple[int, ...]
    c_diamonds: tuple[int, ...]
    linear: tuple[tuple[int, int, int], ...]
    affine: tuple[tuple[int, int, int, int], ...]
    group_size: int
    orbit_size: int


def mask_matrix(c_axis: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(template_bits(c_axis, c_index)[right] for c_index in range(c_axis))
        for right in range(RIGHT_DEGREE)
    )


def units_mod(c_axis: int) -> tuple[int, ...]:
    return tuple(value for value in range(1, c_axis) if gcd(value, c_axis) == 1)


def image_equal(
    matrix: tuple[tuple[int, ...], ...],
    c_axis: int,
    alpha: int,
    beta: int,
    unit: int,
    shift: int,
) -> bool:
    for right in range(RIGHT_DEGREE):
        image_right = (alpha * right + beta) % RIGHT_DEGREE
        for c_index in range(c_axis):
            image_c = (unit * c_index + shift) % c_axis
            if matrix[image_right][image_c] != matrix[right][c_index]:
                return False
    return True


def stabilizer_profile(c_axis: int) -> StabilizerProfile:
    matrix = mask_matrix(c_axis)
    right_automorphisms = tuple(
        value for value in range(1, RIGHT_DEGREE) if gcd(value, RIGHT_DEGREE) == 1
    )
    c_units = units_mod(c_axis)

    right_translations = tuple(
        beta
        for beta in range(RIGHT_DEGREE)
        if image_equal(matrix, c_axis, 1, beta, 1, 0)
    )
    c_translations = tuple(
        shift
        for shift in range(c_axis)
        if image_equal(matrix, c_axis, 1, 0, 1, shift)
    )
    c_diamonds = tuple(
        unit for unit in c_units if image_equal(matrix, c_axis, 1, 0, unit, 0)
    )

    linear: list[tuple[int, int, int]] = []
    affine: list[tuple[int, int, int, int]] = []
    for alpha in right_automorphisms:
        for beta in range(RIGHT_DEGREE):
            for unit in c_units:
                if image_equal(matrix, c_axis, alpha, beta, unit, 0):
                    linear.append((alpha, beta, unit))
                for shift in range(c_axis):
                    if image_equal(matrix, c_axis, alpha, beta, unit, shift):
                        affine.append((alpha, beta, unit, shift))

    group_size = len(right_automorphisms) * RIGHT_DEGREE * len(c_units) * c_axis
    if not affine:
        raise AssertionError("identity affine action was not detected")
    orbit_size = group_size // len(affine)
    return StabilizerProfile(
        right_translations=right_translations,
        c_translations=c_translations,
        c_diamonds=c_diamonds,
        linear=tuple(linear),
        affine=tuple(affine),
        group_size=group_size,
        orbit_size=orbit_size,
    )


def audit_case(case: PullbackCase) -> tuple[list[str], bool]:
    profile = stabilizer_profile(case.c_axis)
    expected_affine = ((1, 0, 1, 0),)
    expected_linear = ((1, 0, 1),)
    row_ok = (
        profile.right_translations == (0,)
        and profile.c_translations == (0,)
        and profile.c_diamonds == (1,)
        and profile.linear == expected_linear
        and profile.affine == expected_affine
        and profile.orbit_size == profile.group_size
    )
    lines = [
        (
            f"case {case.name}: c={case.c_axis} "
            f"right_translation_stabilizers={list(profile.right_translations)} "
            f"c_translation_stabilizers={list(profile.c_translations)} "
            f"c_diamond_stabilizers={list(profile.c_diamonds)} "
            f"linear_stabilizer_count={len(profile.linear)} "
            f"linear_stabilizers={list(profile.linear)} "
            f"affine_stabilizer_count={len(profile.affine)} "
            f"affine_stabilizers={list(profile.affine)} "
            f"group_size={profile.group_size} "
            f"orbit_size={profile.orbit_size} "
            f"ok={int(row_ok)}"
        )
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B residue-mask stabilizer gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in PULLBACK_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"residue_mask_stabilizer_rows={ok_rows}/{len(PULLBACK_CASES)}")
    print("interpretation")
    print("  residue_mask_has_no_nontrivial_right_translation_stabilizer=1")
    print("  residue_mask_has_no_nontrivial_C_translation_stabilizer=1")
    print("  residue_mask_has_no_nontrivial_C_diamond_stabilizer=1")
    print("  residue_mask_has_trivial_full_right_C_affine_stabilizer=1")
    print("  hidden_affine_quotient_compressions_are_ruled_out=1")
    print("conclusion=reported_p25_laneB_residue_mask_stabilizer_gate")
    return 0 if ok_rows == len(PULLBACK_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
