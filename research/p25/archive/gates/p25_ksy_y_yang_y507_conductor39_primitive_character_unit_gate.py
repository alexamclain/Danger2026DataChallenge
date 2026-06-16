#!/usr/bin/env python3
"""Primitive conductor-39 character unit for the p25 Y_507 value-side target.

The modular-unit legality gate shows that W=-6*chi_39 and V_bal=-3*chi_39 are
legal X_1(39) modular-unit words.  This gate records the primitive legal unit
underneath them:

    U_chi = -chi_39.

Then V_bal = 3*U_chi and W = 6*U_chi in exponent notation.  This matters for
value-side source claims: a theorem may target the primitive character unit and
then power it, rather than producing W directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25
from p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate import (
    legality_row,
    profile_yang_y507_conductor39_modular_unit_legality,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39


@dataclass(frozen=True)
class PrimitiveCharacterPowerRow:
    name: str
    scale_from_primitive: int
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    equals_scaled_primitive: bool
    yang_yu_modular_unit_ok: bool
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39PrimitiveCharacterUnit:
    level: int
    primitive_word: tuple[tuple[int, int], ...]
    primitive_support: int
    primitive_coefficient_counts: tuple[tuple[int, int], ...]
    primitive_yang_yu_modular_unit_ok: bool
    primitive_not_integral_power: bool
    primitive_frobenius_image_is_negative: bool
    power_rows: tuple[PrimitiveCharacterPowerRow, ...]
    cube_root_unique_in_fp_star_if_value_lands_in_fp: bool
    sixth_root_has_sign_ambiguity_in_fp_star: bool
    modular_unit_legality_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def primitive_word() -> dict[int, int]:
    return {residue: -chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def scaled_word(scale: int) -> dict[int, int]:
    return {residue: scale * coefficient for residue, coefficient in primitive_word().items()}


def push_frobenius(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = (P25 * residue) % CONDUCTOR
        out[target] = out.get(target, 0) + coefficient
    return dict(sorted((residue, coefficient) for residue, coefficient in out.items() if coefficient))


def negative_word(word: dict[int, int]) -> dict[int, int]:
    return {residue: -coefficient for residue, coefficient in word.items()}


def power_row(name: str, scale: int, expected_ok: bool) -> PrimitiveCharacterPowerRow:
    word = scaled_word(scale)
    legal = legality_row(
        name,
        word,
        expected_ok,
        "none; scaled primitive character is a legal Yang/Yu modular-unit word",
    )
    return PrimitiveCharacterPowerRow(
        name=name,
        scale_from_primitive=scale,
        support=len(word),
        coefficient_counts=coefficient_counts(word),
        equals_scaled_primitive=word == scaled_word(scale),
        yang_yu_modular_unit_ok=legal.yang_yu_modular_unit_ok,
        ok=legal.yang_yu_modular_unit_ok == expected_ok,
    )


def profile_yang_y507_conductor39_primitive_character_unit() -> YangY507Conductor39PrimitiveCharacterUnit:
    legality = profile_yang_y507_conductor39_modular_unit_legality()
    primitive = primitive_word()
    primitive_legal = legality_row(
        "primitive_character_unit_U_chi",
        primitive,
        True,
        "none; U_chi is a valid primitive X_1(39) Yang/Yu modular-unit word",
    )
    rows = (
        power_row("primitive_character_unit_U_chi", 1, True),
        power_row("balanced_potential_V_bal_equals_U_chi_cubed", 3, True),
        power_row("period_norm_word_W_equals_U_chi_sixth", 6, True),
    )
    direct_closer = False
    row_ok = (
        legality.row_ok
        and CONDUCTOR == 39
        and primitive_legal.yang_yu_modular_unit_ok
        and len(primitive) == 24
        and coefficient_counts(primitive) == ((-1, 12), (1, 12))
        and push_frobenius(primitive) == negative_word(primitive)
        and all(row.ok for row in rows)
        and rows[0].coefficient_counts == ((-1, 12), (1, 12))
        and rows[1].coefficient_counts == ((-3, 12), (3, 12))
        and rows[2].coefficient_counts == ((-6, 12), (6, 12))
        and gcd(3, P25 - 1) == 1
        and gcd(6, P25 - 1) == 2
        and not direct_closer
    )
    return YangY507Conductor39PrimitiveCharacterUnit(
        level=CONDUCTOR,
        primitive_word=tuple(sorted(primitive.items())),
        primitive_support=len(primitive),
        primitive_coefficient_counts=coefficient_counts(primitive),
        primitive_yang_yu_modular_unit_ok=primitive_legal.yang_yu_modular_unit_ok,
        primitive_not_integral_power=True,
        primitive_frobenius_image_is_negative=push_frobenius(primitive) == negative_word(primitive),
        power_rows=rows,
        cube_root_unique_in_fp_star_if_value_lands_in_fp=gcd(3, P25 - 1) == 1,
        sixth_root_has_sign_ambiguity_in_fp_star=gcd(6, P25 - 1) == 2,
        modular_unit_legality_ok=legality.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The legal conductor-39 target has a primitive unit U_chi=-chi_39; "
            "V_bal is its cube and W is its sixth power in exponent notation."
        ),
        first_missing_clause=(
            "primitive modular-unit normalization is not the finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "allow source theorems to emit U_chi, V_bal, or W, but require the "
            "same Frobenius/Hilbert-90 descent data; cube-root normalization in "
            "F_p^* has no branch if the value is already in F_p"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_primitive_character_unit()
    print("p25 KSY-y Yang Y_507 conductor-39 primitive character unit gate")
    print(f"level={profile.level}")
    print(f"primitive_word={profile.primitive_word}")
    print(f"primitive_support={profile.primitive_support}")
    print(f"primitive_coefficient_counts={profile.primitive_coefficient_counts}")
    print(f"primitive_yang_yu_modular_unit_ok={int(profile.primitive_yang_yu_modular_unit_ok)}")
    print(f"primitive_not_integral_power={int(profile.primitive_not_integral_power)}")
    print(f"primitive_frobenius_image_is_negative={int(profile.primitive_frobenius_image_is_negative)}")
    print("power_rows")
    for row in profile.power_rows:
        print(
            "  "
            f"{row.name}: scale={row.scale_from_primitive} support={row.support} "
            f"counts={row.coefficient_counts} "
            f"equals_scaled={int(row.equals_scaled_primitive)} "
            f"yang_yu_ok={int(row.yang_yu_modular_unit_ok)} ok={int(row.ok)}"
        )
    print("root_controls")
    print(
        "  cube_root_unique_in_Fp_star_if_value_lands_in_Fp="
        f"{int(profile.cube_root_unique_in_fp_star_if_value_lands_in_fp)}"
    )
    print(
        "  sixth_root_has_sign_ambiguity_in_Fp_star="
        f"{int(profile.sixth_root_has_sign_ambiguity_in_fp_star)}"
    )
    print("checks")
    print(f"  modular_unit_legality_ok={int(profile.modular_unit_legality_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  primitive_character_unit_U_chi_is_legal_X1_39_modular_unit=1")
    print("  V_bal_is_cube_and_W_is_sixth_power_of_U_chi=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_primitive_character_unit_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 primitive character unit regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
