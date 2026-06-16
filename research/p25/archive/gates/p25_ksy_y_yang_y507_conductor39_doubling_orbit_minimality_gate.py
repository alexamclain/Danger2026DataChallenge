#!/usr/bin/env python3
"""Minimality of the 12-step doubling-orbit norm on X_1(39).

The doubling-orbit norm gate proves that Q is the full <2>-orbit norm of the
seed ratio E_7/E_1.  This gate checks all proper doubling suborbit norms and
records the obstruction: every proper suborbit fails Yang/Yu modular-unit
legality.  Some pass the elementary congruences, but all fail the signed orbit
condition at the prime 3.  The full length-12 orbit is therefore forced.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_doubling_orbit_norm_gate import (
    COSET_REPRESENTATIVE,
    GENERATOR,
    ORBIT_LENGTH,
    add_words,
    multiply_word,
    profile_yang_y507_conductor39_doubling_orbit_norm,
    seed_word,
)
from p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate import (
    legality_row,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    primitive_word,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR


SUBORBIT_LENGTHS = (1, 2, 3, 4, 6, 12)


@dataclass(frozen=True)
class SuborbitNormRow:
    length: int
    offset: int
    step: int
    support: int
    word: tuple[tuple[int, int], ...]
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_sum_mod_level: int
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    yang_yu_modular_unit_ok: bool
    equals_full_primitive: bool
    expected_ok: bool
    first_failing_clause: str
    ok: bool


@dataclass(frozen=True)
class Conductor39DoublingOrbitMinimality:
    level: int
    generator: int
    coset_representative: int
    rows: tuple[SuborbitNormRow, ...]
    full_rows: int
    proper_rows: int
    legal_rows: int
    proper_legal_rows: int
    proper_elementary_congruence_rows: int
    proper_signed_orbit_failure_rows: int
    full_orbit_forced_by_yang_yu: bool
    doubling_orbit_norm_ok: bool
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


def suborbit_word(length: int, offset: int) -> dict[int, int]:
    step = ORBIT_LENGTH // length
    out: dict[int, int] = {}
    for index in range(length):
        multiplier = pow(GENERATOR, offset + step * index, CONDUCTOR)
        out = add_words(out, multiply_word(seed_word(), multiplier))
    return out


def first_failing_clause(row) -> str:
    if row.yang_yu_modular_unit_ok:
        return "none"
    if row.quadratic_sum_mod_level != 0:
        return "quadratic congruence modulo 39 fails"
    if any(count for _prime, count in row.signed_orbit_bad_counts):
        return "Yang/Yu signed orbit condition fails at prime 3"
    return "unknown legality failure"


def suborbit_row(length: int, offset: int) -> SuborbitNormRow:
    word = suborbit_word(length, offset)
    expected_ok = length == ORBIT_LENGTH and offset == 0
    legal = legality_row(
        f"doubling_orbit_length_{length}_offset_{offset}",
        word,
        expected_ok,
        "proper suborbit is not a standalone X_1(39) Yang/Yu modular unit",
    )
    return SuborbitNormRow(
        length=length,
        offset=offset,
        step=ORBIT_LENGTH // length,
        support=len(word),
        word=tuple(sorted(word.items())),
        coefficient_counts=coefficient_counts(word),
        exponent_sum_mod_12=legal.exponent_sum_mod_12,
        quadratic_sum_mod_level=legal.quadratic_sum_mod_level,
        signed_orbit_bad_counts=legal.signed_orbit_bad_counts,
        yang_yu_modular_unit_ok=legal.yang_yu_modular_unit_ok,
        equals_full_primitive=word == primitive_word(),
        expected_ok=expected_ok,
        first_failing_clause=first_failing_clause(legal),
        ok=legal.yang_yu_modular_unit_ok == expected_ok,
    )


def suborbit_rows() -> tuple[SuborbitNormRow, ...]:
    rows: list[SuborbitNormRow] = []
    for length in SUBORBIT_LENGTHS:
        step = ORBIT_LENGTH // length
        for offset in range(step):
            rows.append(suborbit_row(length, offset))
    return tuple(rows)


def profile_yang_y507_conductor39_doubling_orbit_minimality() -> Conductor39DoublingOrbitMinimality:
    norm = profile_yang_y507_conductor39_doubling_orbit_norm()
    rows = suborbit_rows()
    full_rows = sum(row.length == ORBIT_LENGTH for row in rows)
    proper_rows = sum(row.length < ORBIT_LENGTH for row in rows)
    legal_rows = sum(row.yang_yu_modular_unit_ok for row in rows)
    proper_legal_rows = sum(row.length < ORBIT_LENGTH and row.yang_yu_modular_unit_ok for row in rows)
    proper_elementary = sum(
        row.length < ORBIT_LENGTH and row.exponent_sum_mod_12 == 0 and row.quadratic_sum_mod_level == 0
        for row in rows
    )
    proper_signed_failures = sum(
        row.length < ORBIT_LENGTH
        and row.exponent_sum_mod_12 == 0
        and row.quadratic_sum_mod_level == 0
        and any(count for _prime, count in row.signed_orbit_bad_counts)
        for row in rows
    )
    direct_closer = False
    row_ok = (
        norm.row_ok
        and CONDUCTOR == 39
        and GENERATOR == 2
        and COSET_REPRESENTATIVE == 7
        and ORBIT_LENGTH == 12
        and len(rows) == 28
        and full_rows == 1
        and proper_rows == 27
        and legal_rows == 1
        and proper_legal_rows == 0
        and proper_elementary == 9
        and proper_signed_failures == 9
        and rows[-1].length == 12
        and rows[-1].offset == 0
        and rows[-1].yang_yu_modular_unit_ok
        and rows[-1].equals_full_primitive
        and all(row.ok for row in rows)
        and not direct_closer
    )
    return Conductor39DoublingOrbitMinimality(
        level=CONDUCTOR,
        generator=GENERATOR,
        coset_representative=COSET_REPRESENTATIVE,
        rows=rows,
        full_rows=full_rows,
        proper_rows=proper_rows,
        legal_rows=legal_rows,
        proper_legal_rows=proper_legal_rows,
        proper_elementary_congruence_rows=proper_elementary,
        proper_signed_orbit_failure_rows=proper_signed_failures,
        full_orbit_forced_by_yang_yu=proper_legal_rows == 0 and legal_rows == 1,
        doubling_orbit_norm_ok=norm.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Among all doubling suborbit norms of E_7/E_1, only the full "
            "length-12 orbit is a legal X_1(39) Yang/Yu modular unit."
        ),
        first_missing_clause=(
            "minimality is a source guardrail, not the finite-field value/divisor "
            "theorem or DANGER3 extraction"
        ),
        recommendation=(
            "reject source claims that emit the seed ratio or a proper doubling "
            "suborbit as a standalone modular unit; require the full 12-step norm "
            "or an explicit boundary repairing the Yang/Yu failure"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_doubling_orbit_minimality()
    print("p25 KSY-y Yang Y_507 conductor-39 doubling-orbit minimality gate")
    print(f"level={profile.level}")
    print(f"generator={profile.generator}")
    print(f"coset_representative={profile.coset_representative}")
    print("summary")
    print(f"  full_rows={profile.full_rows}")
    print(f"  proper_rows={profile.proper_rows}")
    print(f"  legal_rows={profile.legal_rows}")
    print(f"  proper_legal_rows={profile.proper_legal_rows}")
    print(f"  proper_elementary_congruence_rows={profile.proper_elementary_congruence_rows}")
    print(f"  proper_signed_orbit_failure_rows={profile.proper_signed_orbit_failure_rows}")
    print(f"  full_orbit_forced_by_yang_yu={int(profile.full_orbit_forced_by_yang_yu)}")
    print("sample_rows")
    for row in profile.rows[:6] + profile.rows[-3:]:
        print(
            "  "
            f"length={row.length} offset={row.offset} step={row.step} "
            f"support={row.support} quad={row.quadratic_sum_mod_level} "
            f"signed_bad={row.signed_orbit_bad_counts} "
            f"yang_yu_ok={int(row.yang_yu_modular_unit_ok)} "
            f"expected={int(row.expected_ok)} ok={int(row.ok)} "
            f"fail={row.first_failing_clause}"
        )
    print("checks")
    print(f"  doubling_orbit_norm_ok={int(profile.doubling_orbit_norm_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  full_12_step_doubling_norm_is_Yang_Yu_minimal=1")
    print("  proper_suborbit_norms_are_not_standalone_X1_39_units=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_doubling_orbit_minimality_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 doubling-orbit minimality regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
