#!/usr/bin/env python3
"""Affine and lower-level rigidity for the compact p25 Y_507 word.

The primitive-D form

    Y_507 = [2]^*U_507 / U_507^4,
    U_507 = z^121(1+z+z^2)(1-z^263),

has only 12 nonzero exponent residues.  This gate checks whether that compact
word is secretly a lower-level pullback or has an affine symmetry that could
make the theorem target cheaper.  The useful answer is sharp: the exact affine
stabilizer is trivial, and the only support symmetry is inversion, which sends
the word to its negative.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
)


PROPER_DIVISORS = (1, 3, 13, 39, 169)


@dataclass(frozen=True)
class LowerLevelRow:
    level: int
    pullback_from_level: bool
    first_bad_residue: int | None
    first_bad_values: tuple[int, ...]
    pushforward_support: int
    pushforward_word: tuple[tuple[int, int], ...]
    pushforward_zero: bool
    ok: bool


@dataclass(frozen=True)
class YangY507AffineLevelRigidity:
    level: int
    word: tuple[tuple[int, int], ...]
    unit_count: int
    exact_affine_stabilizers: tuple[tuple[int, int], ...]
    negative_affine_stabilizers: tuple[tuple[int, int], ...]
    support_affine_stabilizers: tuple[tuple[int, int], ...]
    exact_translation_stabilizers: tuple[int, ...]
    support_translation_stabilizers: tuple[int, ...]
    exact_multiplicative_stabilizers: tuple[int, ...]
    support_multiplicative_stabilizers: tuple[int, ...]
    lower_level_rows: tuple[LowerLevelRow, ...]
    all_proper_pullbacks_fail: bool
    inversion_is_only_nontrivial_support_symmetry: bool
    exact_stabilizer_is_trivial: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero_word(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def transform(word: dict[int, int], unit: int, shift: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = (unit * residue + shift) % QUOTIENT_LEVEL
        out[target] = out.get(target, 0) + coefficient
    return nonzero_word(out)


def affine_scans(word: dict[int, int]) -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
]:
    units = tuple(unit for unit in range(QUOTIENT_LEVEL) if gcd(unit, QUOTIENT_LEVEL) == 1)
    support = set(word)
    negative_word = {residue: -coefficient for residue, coefficient in word.items()}
    exact: list[tuple[int, int]] = []
    negative: list[tuple[int, int]] = []
    support_only: list[tuple[int, int]] = []
    for unit in units:
        for shift in range(QUOTIENT_LEVEL):
            image = transform(word, unit, shift)
            if image == word:
                exact.append((unit, shift))
            if image == negative_word:
                negative.append((unit, shift))
            if set(image) == support:
                support_only.append((unit, shift))
    return tuple(exact), tuple(negative), tuple(support_only)


def pullback_failure(word: dict[int, int], level: int) -> tuple[bool, int | None, tuple[int, ...]]:
    coefficients = {residue: word.get(residue, 0) for residue in range(QUOTIENT_LEVEL)}
    for residue in range(level):
        values = tuple(sorted({coefficients[x] for x in range(residue, QUOTIENT_LEVEL, level)}))
        if len(values) > 1:
            return False, residue, values
    return True, None, ()


def pushforward(word: dict[int, int], level: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = residue % level
        out[target] = out.get(target, 0) + coefficient
    return nonzero_word(out)


def lower_level_rows(word: dict[int, int]) -> tuple[LowerLevelRow, ...]:
    rows: list[LowerLevelRow] = []
    for level in PROPER_DIVISORS:
        pullback, bad_residue, bad_values = pullback_failure(word, level)
        pushed = pushforward(word, level)
        rows.append(
            LowerLevelRow(
                level=level,
                pullback_from_level=pullback,
                first_bad_residue=bad_residue,
                first_bad_values=bad_values,
                pushforward_support=len(pushed),
                pushforward_word=tuple(sorted(pushed.items())),
                pushforward_zero=not pushed,
                ok=not pullback,
            )
        )
    return tuple(rows)


def profile_yang_y507_affine_level_rigidity() -> YangY507AffineLevelRigidity:
    primitive = profile_yang_y507_primitive_factor_word()
    word = dict(primitive.y507_primitive_word)
    exact, negative, support_only = affine_scans(word)
    rows = lower_level_rows(word)
    exact_translations = tuple(shift for unit, shift in exact if unit == 1)
    support_translations = tuple(shift for unit, shift in support_only if unit == 1)
    exact_multiplicative = tuple(unit for unit, shift in exact if shift == 0)
    support_multiplicative = tuple(unit for unit, shift in support_only if shift == 0)
    exact_trivial = exact == ((1, 0),)
    inversion_only = (
        negative == ((QUOTIENT_LEVEL - 1, 0),)
        and support_only == ((1, 0), (QUOTIENT_LEVEL - 1, 0))
    )
    all_pullbacks_fail = all(row.ok for row in rows)
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and QUOTIENT_LEVEL == 507
        and len(word) == 12
        and exact_trivial
        and inversion_only
        and exact_translations == (0,)
        and support_translations == (0,)
        and exact_multiplicative == (1,)
        and support_multiplicative == (1, QUOTIENT_LEVEL - 1)
        and all_pullbacks_fail
        and tuple(row.pushforward_support for row in rows) == (0, 0, 10, 12, 12)
        and not direct_closer
    )
    return YangY507AffineLevelRigidity(
        level=QUOTIENT_LEVEL,
        word=primitive.y507_primitive_word,
        unit_count=sum(1 for unit in range(QUOTIENT_LEVEL) if gcd(unit, QUOTIENT_LEVEL) == 1),
        exact_affine_stabilizers=exact,
        negative_affine_stabilizers=negative,
        support_affine_stabilizers=support_only,
        exact_translation_stabilizers=exact_translations,
        support_translation_stabilizers=support_translations,
        exact_multiplicative_stabilizers=exact_multiplicative,
        support_multiplicative_stabilizers=support_multiplicative,
        lower_level_rows=rows,
        all_proper_pullbacks_fail=all_pullbacks_fail,
        inversion_is_only_nontrivial_support_symmetry=inversion_only,
        exact_stabilizer_is_trivial=exact_trivial,
        direct_closer=direct_closer,
        positive_payload=(
            "The compact Y_507 word has trivial exact affine stabilizer; "
            "inversion is the only nontrivial support symmetry and sends the "
            "word to its negative."
        ),
        first_missing_clause=(
            "affine/level rigidity is still structural data, not the finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "keep source queries at genuine level 507 and preserve inversion "
            "anti-invariance; do not chase a lower-level pullback shortcut"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_affine_level_rigidity()
    print("p25 KSY-y Yang Y_507 affine/level rigidity gate")
    print(f"level={profile.level}")
    print(f"unit_count={profile.unit_count}")
    print(f"word={profile.word}")
    print("affine_stabilizers")
    print(f"  exact_affine_stabilizers={profile.exact_affine_stabilizers}")
    print(f"  negative_affine_stabilizers={profile.negative_affine_stabilizers}")
    print(f"  support_affine_stabilizers={profile.support_affine_stabilizers}")
    print(f"  exact_translation_stabilizers={profile.exact_translation_stabilizers}")
    print(f"  support_translation_stabilizers={profile.support_translation_stabilizers}")
    print(f"  exact_multiplicative_stabilizers={profile.exact_multiplicative_stabilizers}")
    print(f"  support_multiplicative_stabilizers={profile.support_multiplicative_stabilizers}")
    print("lower_levels")
    for row in profile.lower_level_rows:
        print(
            "  "
            f"level={row.level} pullback={int(row.pullback_from_level)} "
            f"bad_residue={row.first_bad_residue} bad_values={row.first_bad_values} "
            f"push_support={row.pushforward_support} push_zero={int(row.pushforward_zero)} "
            f"ok={int(row.ok)}"
        )
        print(f"    pushforward_word={row.pushforward_word}")
    print("checks")
    print(f"  exact_stabilizer_is_trivial={int(profile.exact_stabilizer_is_trivial)}")
    print(
        "  inversion_is_only_nontrivial_support_symmetry="
        f"{int(profile.inversion_is_only_nontrivial_support_symmetry)}"
    )
    print(f"  all_proper_pullbacks_fail={int(profile.all_proper_pullbacks_fail)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  no_lower_level_pullback_shortcut=1")
    print("  preserve_genuine_level_507_and_inversion_anti_invariance=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_affine_level_rigidity_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 affine/level rigidity regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
