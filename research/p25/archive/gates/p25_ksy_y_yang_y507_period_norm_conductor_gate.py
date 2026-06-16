#!/usr/bin/env python3
"""Conductor of the compact p25 Y_507 period-norm character.

The period-norm gate shows that Norm_156(Y_507) is dense on the units of
Z/507Z.  This gate asks whether that dense character is genuinely conductor
507 or an inflation from a smaller modulus.  It is exactly the inflation of the
primitive quadratic character modulo 39, scaled by -6.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_modular_period_certificate_gate import SUPPORT_PERIOD
from p25_ksy_y_yang_y507_period_norm_character_gate import (
    coefficient_counts,
    period_norm,
    profile_yang_y507_period_norm_character,
)
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)


TEST_MODULI = (1, 3, 13, 39, 169, 507)
CONDUCTOR = 39


@dataclass(frozen=True)
class ModulusDescentRow:
    modulus: int
    descends: bool
    first_bad_pair: tuple[int, int] | None
    first_bad_residue: int | None
    first_bad_coefficients: tuple[int, int] | None
    quotient_support: int
    quotient_coefficient_counts: tuple[tuple[int, int], ...]
    ok: bool


@dataclass(frozen=True)
class YangY507PeriodNormConductor:
    level: int
    support_period: int
    conductor: int
    descent_rows: tuple[ModulusDescentRow, ...]
    minimal_conductor_is_39: bool
    y_norm_is_inflated_minus_six_chi39: bool
    u_norm_is_inflated_two_chi39: bool
    plus_six_residues_mod39: tuple[int, ...]
    minus_six_residues_mod39: tuple[int, ...]
    chi39_kernel_residues_mod39: tuple[int, ...]
    chi39_negative_residues_mod39: tuple[int, ...]
    period_norm_character_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def coefficient_at(word: dict[int, int], residue: int) -> int:
    return word.get(residue % QUOTIENT_LEVEL, 0)


def quotient_word_if_descends(word: dict[int, int], modulus: int) -> tuple[bool, dict[int, int], tuple[int, int] | None]:
    quotient: dict[int, int] = {}
    first_bad: tuple[int, int] | None = None
    for residue in range(modulus):
        values = {
            coefficient_at(word, lift)
            for lift in range(residue, QUOTIENT_LEVEL, modulus)
        }
        if len(values) != 1:
            lifts = list(range(residue, QUOTIENT_LEVEL, modulus))
            first = lifts[0]
            for lift in lifts[1:]:
                if coefficient_at(word, lift) != coefficient_at(word, first):
                    first_bad = (first, lift)
                    break
            return False, {}, first_bad
        value = values.pop()
        if value:
            quotient[residue] = value
    return True, dict(sorted(quotient.items())), None


def descent_row(word: dict[int, int], modulus: int, expected_descends: bool) -> ModulusDescentRow:
    descends, quotient, bad_pair = quotient_word_if_descends(word, modulus)
    bad_residue = bad_pair[0] % modulus if bad_pair is not None else None
    bad_coefficients = (
        (coefficient_at(word, bad_pair[0]), coefficient_at(word, bad_pair[1]))
        if bad_pair is not None
        else None
    )
    return ModulusDescentRow(
        modulus=modulus,
        descends=descends,
        first_bad_pair=bad_pair,
        first_bad_residue=bad_residue,
        first_bad_coefficients=bad_coefficients,
        quotient_support=len(quotient),
        quotient_coefficient_counts=coefficient_counts(quotient),
        ok=descends == expected_descends,
    )


def chi3(residue: int) -> int:
    value = residue % 3
    if value == 0:
        return 0
    return 1 if value == 1 else -1


def legendre13(residue: int) -> int:
    value = residue % 13
    if value == 0:
        return 0
    return 1 if pow(value, 6, 13) == 1 else -1


def chi39(residue: int) -> int:
    return chi3(residue) * legendre13(residue)


def inflated_character(scale: int) -> dict[int, int]:
    return {
        residue: scale * chi39(residue)
        for residue in range(QUOTIENT_LEVEL)
        if chi39(residue)
    }


def residues_mod39_with_value(value: int) -> tuple[int, ...]:
    return tuple(residue for residue in range(CONDUCTOR) if chi39(residue) == value)


def profile_yang_y507_period_norm_conductor() -> YangY507PeriodNormConductor:
    primitive = profile_yang_y507_primitive_factor_word()
    period_character = profile_yang_y507_period_norm_character()
    u_norm = period_norm(dict(primitive.u_primitive_word), SUPPORT_PERIOD)
    y_norm = period_norm(dict(primitive.y507_primitive_word), SUPPORT_PERIOD)
    expected_descents = {
        1: False,
        3: False,
        13: False,
        39: True,
        169: False,
        507: True,
    }
    rows = tuple(descent_row(y_norm, modulus, expected_descents[modulus]) for modulus in TEST_MODULI)
    y_is_chi = y_norm == inflated_character(-6)
    u_is_chi = u_norm == inflated_character(2)
    conductor_minimal = (
        tuple(row.modulus for row in rows if row.descends) == (39, 507)
        and all(row.ok for row in rows)
    )
    plus_residues = tuple(residue for residue in range(CONDUCTOR) if y_norm.get(residue, 0) == 6)
    minus_residues = tuple(residue for residue in range(CONDUCTOR) if y_norm.get(residue, 0) == -6)
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and period_character.row_ok
        and QUOTIENT_LEVEL == 507
        and SUPPORT_PERIOD == 156
        and CONDUCTOR == 39
        and conductor_minimal
        and y_is_chi
        and u_is_chi
        and plus_residues == residues_mod39_with_value(-1)
        and minus_residues == residues_mod39_with_value(1)
        and len(plus_residues) == 12
        and len(minus_residues) == 12
        and not direct_closer
    )
    return YangY507PeriodNormConductor(
        level=QUOTIENT_LEVEL,
        support_period=SUPPORT_PERIOD,
        conductor=CONDUCTOR,
        descent_rows=rows,
        minimal_conductor_is_39=conductor_minimal,
        y_norm_is_inflated_minus_six_chi39=y_is_chi,
        u_norm_is_inflated_two_chi39=u_is_chi,
        plus_six_residues_mod39=plus_residues,
        minus_six_residues_mod39=minus_residues,
        chi39_kernel_residues_mod39=residues_mod39_with_value(1),
        chi39_negative_residues_mod39=residues_mod39_with_value(-1),
        period_norm_character_ok=period_character.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Norm_156(Y_507) is the inflation to level 507 of -6 times the "
            "primitive quadratic character chi_3*chi_13 modulo 39."
        ),
        first_missing_clause=(
            "conductor descent is a value-side constraint, not the finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "search value-side sources for a conductor-39 quadratic character "
            "norm/period formula inflated to level 507; reject conductor-3, "
            "conductor-13, conductor-169, or arbitrary conductor-507 readings"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_period_norm_conductor()
    print("p25 KSY-y Yang Y_507 period-norm conductor gate")
    print(f"level={profile.level}")
    print(f"support_period={profile.support_period}")
    print(f"conductor={profile.conductor}")
    print("descent_rows")
    for row in profile.descent_rows:
        print(
            "  "
            f"modulus={row.modulus} descends={int(row.descends)} "
            f"bad_pair={row.first_bad_pair} bad_residue={row.first_bad_residue} "
            f"bad_coefficients={row.first_bad_coefficients} "
            f"quotient_support={row.quotient_support} "
            f"quotient_counts={row.quotient_coefficient_counts} "
            f"ok={int(row.ok)}"
        )
    print("character")
    print(f"  y_norm_is_inflated_minus_six_chi39={int(profile.y_norm_is_inflated_minus_six_chi39)}")
    print(f"  u_norm_is_inflated_two_chi39={int(profile.u_norm_is_inflated_two_chi39)}")
    print(f"  plus_six_residues_mod39={profile.plus_six_residues_mod39}")
    print(f"  minus_six_residues_mod39={profile.minus_six_residues_mod39}")
    print(f"  chi39_kernel_residues_mod39={profile.chi39_kernel_residues_mod39}")
    print(f"  chi39_negative_residues_mod39={profile.chi39_negative_residues_mod39}")
    print("checks")
    print(f"  period_norm_character_ok={int(profile.period_norm_character_ok)}")
    print(f"  minimal_conductor_is_39={int(profile.minimal_conductor_is_39)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  period_norm_descends_exactly_to_conductor_39=1")
    print("  norm_y507_equals_minus_six_chi3_chi13_inflated_to_507=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_period_norm_conductor_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 period-norm conductor regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
