#!/usr/bin/env python3
"""Mixed tensor structure of the p25 conductor-39 primitive character unit.

The primitive character unit U_chi=-chi_39 is legal on X_1(39).  This gate
checks that it is not a disguised conductor-3 or conductor-13 pullback.  Its
proper pushforwards vanish, proper pullback tests fail, and the surviving
structure is exactly the mixed tensor -chi_3 * chi_13.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import (
    CONDUCTOR,
    chi3,
    chi39,
    legendre13,
)


@dataclass(frozen=True)
class PullbackFailure:
    modulus: int
    is_pullback: bool
    first_bad_pair: tuple[int, int] | None
    first_bad_residue: int | None
    first_bad_coefficients: tuple[int, int] | None
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39MixedTensorCharacter:
    level: int
    primitive_unit_ok: bool
    primitive_word: tuple[tuple[int, int], ...]
    pushforward_mod3: tuple[tuple[int, int], ...]
    pushforward_mod13: tuple[tuple[int, int], ...]
    proper_pushforwards_vanish: bool
    pullback_failures: tuple[PullbackFailure, ...]
    tensor_factorization_ok: bool
    units_mod13: tuple[int, ...]
    row_mod3_1: tuple[int, ...]
    row_mod3_2: tuple[int, ...]
    row2_is_negative_row1: bool
    row_sums: tuple[int, int]
    column_sums: tuple[int, ...]
    additive_row_differences: tuple[int, ...]
    additive_separable: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def primitive_word() -> dict[int, int]:
    return {residue: -chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def pushforward(word: dict[int, int], modulus: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = residue % modulus
        out[target] = out.get(target, 0) + coefficient
    return dict(sorted((residue, coefficient) for residue, coefficient in out.items() if coefficient))


def pullback_failure(word: dict[int, int], modulus: int) -> PullbackFailure:
    for left, left_coefficient in sorted(word.items()):
        for right, right_coefficient in sorted(word.items()):
            if left >= right:
                continue
            if left % modulus == right % modulus and left_coefficient != right_coefficient:
                return PullbackFailure(
                    modulus=modulus,
                    is_pullback=False,
                    first_bad_pair=(left, right),
                    first_bad_residue=left % modulus,
                    first_bad_coefficients=(left_coefficient, right_coefficient),
                    ok=True,
                )
    return PullbackFailure(
        modulus=modulus,
        is_pullback=True,
        first_bad_pair=None,
        first_bad_residue=None,
        first_bad_coefficients=None,
        ok=False,
    )


def crt_mod3_mod13(mod3_value: int, mod13_value: int) -> int:
    for residue in range(CONDUCTOR):
        if residue % 3 == mod3_value and residue % 13 == mod13_value:
            return residue
    raise AssertionError("CRT search failed")


def tensor_factorization(word: dict[int, int]) -> bool:
    return all(
        coefficient == -chi3(residue) * legendre13(residue)
        for residue, coefficient in word.items()
    )


def row_for_mod3(word: dict[int, int], mod3_value: int, units13: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(word[crt_mod3_mod13(mod3_value, mod13_value)] for mod13_value in units13)


def profile_yang_y507_conductor39_mixed_tensor_character() -> YangY507Conductor39MixedTensorCharacter:
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    word = primitive_word()
    units13 = tuple(range(1, 13))
    row1 = row_for_mod3(word, 1, units13)
    row2 = row_for_mod3(word, 2, units13)
    row_differences = tuple(right - left for left, right in zip(row1, row2))
    column_sums = tuple(left + right for left, right in zip(row1, row2))
    pullbacks = (pullback_failure(word, 3), pullback_failure(word, 13))
    direct_closer = False
    row_ok = (
        primitive.row_ok
        and CONDUCTOR == 39
        and tuple(sorted(word.items())) == primitive.primitive_word
        and not pushforward(word, 3)
        and not pushforward(word, 13)
        and pullbacks[0].first_bad_pair == (1, 7)
        and pullbacks[1].first_bad_pair == (1, 14)
        and all(row.ok for row in pullbacks)
        and tensor_factorization(word)
        and row2 == tuple(-value for value in row1)
        and sum(row1) == 0
        and sum(row2) == 0
        and all(value == 0 for value in column_sums)
        and len(set(row_differences)) > 1
        and not direct_closer
    )
    return YangY507Conductor39MixedTensorCharacter(
        level=CONDUCTOR,
        primitive_unit_ok=primitive.row_ok,
        primitive_word=tuple(sorted(word.items())),
        pushforward_mod3=tuple(pushforward(word, 3).items()),
        pushforward_mod13=tuple(pushforward(word, 13).items()),
        proper_pushforwards_vanish=not pushforward(word, 3) and not pushforward(word, 13),
        pullback_failures=pullbacks,
        tensor_factorization_ok=tensor_factorization(word),
        units_mod13=units13,
        row_mod3_1=row1,
        row_mod3_2=row2,
        row2_is_negative_row1=row2 == tuple(-value for value in row1),
        row_sums=(sum(row1), sum(row2)),
        column_sums=column_sums,
        additive_row_differences=row_differences,
        additive_separable=len(set(row_differences)) == 1,
        direct_closer=direct_closer,
        positive_payload=(
            "U_chi is a genuine mixed conductor-39 tensor -chi_3*chi_13: "
            "proper pushforwards vanish and proper pullbacks fail."
        ),
        first_missing_clause=(
            "mixed tensor structure is still not the finite-field value/divisor "
            "theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask source theorems for a mixed chi_3 tensor chi_13 character unit; "
            "reject conductor-3-only, conductor-13-only, or additive separated "
            "explanations"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_mixed_tensor_character()
    print("p25 KSY-y Yang Y_507 conductor-39 mixed tensor character gate")
    print(f"level={profile.level}")
    print(f"primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"primitive_word={profile.primitive_word}")
    print(f"pushforward_mod3={profile.pushforward_mod3}")
    print(f"pushforward_mod13={profile.pushforward_mod13}")
    print(f"proper_pushforwards_vanish={int(profile.proper_pushforwards_vanish)}")
    print("pullback_failures")
    for row in profile.pullback_failures:
        print(
            "  "
            f"modulus={row.modulus} is_pullback={int(row.is_pullback)} "
            f"first_bad_pair={row.first_bad_pair} "
            f"first_bad_residue={row.first_bad_residue} "
            f"first_bad_coefficients={row.first_bad_coefficients} ok={int(row.ok)}"
        )
    print("tensor_table")
    print(f"  tensor_factorization_ok={int(profile.tensor_factorization_ok)}")
    print(f"  units_mod13={profile.units_mod13}")
    print(f"  row_mod3_1={profile.row_mod3_1}")
    print(f"  row_mod3_2={profile.row_mod3_2}")
    print(f"  row2_is_negative_row1={int(profile.row2_is_negative_row1)}")
    print(f"  row_sums={profile.row_sums}")
    print(f"  column_sums={profile.column_sums}")
    print(f"  additive_row_differences={profile.additive_row_differences}")
    print(f"  additive_separable={int(profile.additive_separable)}")
    print("checks")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  U_chi_is_genuine_mixed_chi3_tensor_chi13_character=1")
    print("  proper_axis_pushforwards_vanish_and_pullbacks_fail=1")
    print("  reject_conductor3_conductor13_or_additive_separated_explanations=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_mixed_tensor_character_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 mixed tensor character regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
