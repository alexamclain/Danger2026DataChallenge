#!/usr/bin/env python3
"""Frobenius orbit law for the p25 conductor-39 period-norm character.

The conductor-39 contract says primitive 39th roots first appear over degree 6.
This gate records a sharper fact: on the pure conductor-39 exponent word,
Frobenius at p flips the quadratic character.  Thus the full degree-6 norm of
the pure character word cancels additively.  A value-side theorem has to use a
twisted trace/ratio or a non-pure lift; a naive norm of the character word is
trivial.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import (
    P25,
    profile_yang_y507_conductor39_frobenius_contract,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import (
    CONDUCTOR,
    chi39,
    profile_yang_y507_period_norm_conductor,
)


@dataclass(frozen=True)
class FrobeniusPowerRow:
    degree: int
    multiplier_mod_39: int
    image_equals_word: bool
    image_equals_negative_word: bool
    support_preserved: bool
    ok: bool


@dataclass(frozen=True)
class UnitOrbitRow:
    orbit: tuple[int, ...]
    coefficients: tuple[int, ...]
    alternating_signs: bool
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39FrobeniusOrbit:
    conductor: int
    p_mod_39: int
    chi39_p: int
    chi39_minus_one: int
    word_mod39: tuple[tuple[int, int], ...]
    frobenius_rows: tuple[FrobeniusPowerRow, ...]
    unit_orbits: tuple[UnitOrbitRow, ...]
    unit_orbit_length_counts: tuple[tuple[int, int], ...]
    two_conjugate_sum_support: int
    three_conjugate_sum_equals_word: bool
    six_conjugate_sum_support: int
    exact_signed_frobenius_period: int
    pure_character_degree6_norm_cancels: bool
    conductor_gate_ok: bool
    frobenius_contract_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def y_period_norm_word_mod39() -> dict[int, int]:
    return {residue: -6 * chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def push_word(word: dict[int, int], multiplier: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = (multiplier * residue) % CONDUCTOR
        out[target] = out.get(target, 0) + coefficient
    return nonzero(out)


def add_words(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for residue, coefficient in right.items():
        out[residue] = out.get(residue, 0) + coefficient
    return nonzero(out)


def negative_word(word: dict[int, int]) -> dict[int, int]:
    return {residue: -coefficient for residue, coefficient in word.items()}


def frobenius_row(word: dict[int, int], degree: int) -> FrobeniusPowerRow:
    multiplier = pow(P25, degree, CONDUCTOR)
    image = push_word(word, multiplier)
    same = image == word
    negative = image == negative_word(word)
    support = set(image) == set(word)
    return FrobeniusPowerRow(
        degree=degree,
        multiplier_mod_39=multiplier,
        image_equals_word=same,
        image_equals_negative_word=negative,
        support_preserved=support,
        ok=support and (same if degree % 2 == 0 else negative),
    )


def conjugate_sum(word: dict[int, int], terms: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for degree in range(terms):
        out = add_words(out, push_word(word, pow(P25, degree, CONDUCTOR)))
    return out


def unit_orbits(word: dict[int, int]) -> tuple[UnitOrbitRow, ...]:
    seen: set[int] = set()
    rows: list[UnitOrbitRow] = []
    for residue in sorted(word):
        if residue in seen:
            continue
        orbit: list[int] = []
        current = residue
        while current not in orbit:
            orbit.append(current)
            seen.add(current)
            current = (P25 * current) % CONDUCTOR
        coefficients = tuple(word[item] for item in orbit)
        alternating = all(coefficients[index] == ((-1) ** index) * coefficients[0] for index in range(len(coefficients)))
        rows.append(
            UnitOrbitRow(
                orbit=tuple(orbit),
                coefficients=coefficients,
                alternating_signs=alternating,
                ok=len(orbit) == 6 and alternating,
            )
        )
    return tuple(rows)


def signed_period(word: dict[int, int]) -> int:
    for period in range(1, 7):
        if push_word(word, pow(P25, period, CONDUCTOR)) == word:
            return period
    raise AssertionError("signed period exceeds six")


def profile_yang_y507_conductor39_frobenius_orbit() -> YangY507Conductor39FrobeniusOrbit:
    conductor = profile_yang_y507_period_norm_conductor()
    contract = profile_yang_y507_conductor39_frobenius_contract()
    word = y_period_norm_word_mod39()
    rows = tuple(frobenius_row(word, degree) for degree in range(1, 7))
    orbits = unit_orbits(word)
    length_counts: dict[int, int] = {}
    for row in orbits:
        length_counts[len(row.orbit)] = length_counts.get(len(row.orbit), 0) + 1
    two_sum = conjugate_sum(word, 2)
    three_sum = conjugate_sum(word, 3)
    six_sum = conjugate_sum(word, 6)
    period = signed_period(word)
    direct_closer = False
    row_ok = (
        conductor.row_ok
        and contract.row_ok
        and CONDUCTOR == 39
        and P25 % 39 == 23
        and chi39(P25) == -1
        and chi39(-1) == -1
        and tuple(row.multiplier_mod_39 for row in rows) == (23, 22, 38, 16, 17, 1)
        and all(row.ok for row in rows)
        and tuple(sorted(length_counts.items())) == ((6, 4),)
        and all(row.ok for row in orbits)
        and not two_sum
        and three_sum == word
        and not six_sum
        and period == 2
        and not direct_closer
    )
    return YangY507Conductor39FrobeniusOrbit(
        conductor=CONDUCTOR,
        p_mod_39=P25 % 39,
        chi39_p=chi39(P25),
        chi39_minus_one=chi39(-1),
        word_mod39=tuple(sorted(word.items())),
        frobenius_rows=rows,
        unit_orbits=orbits,
        unit_orbit_length_counts=tuple(sorted(length_counts.items())),
        two_conjugate_sum_support=len(two_sum),
        three_conjugate_sum_equals_word=three_sum == word,
        six_conjugate_sum_support=len(six_sum),
        exact_signed_frobenius_period=period,
        pure_character_degree6_norm_cancels=not six_sum,
        conductor_gate_ok=conductor.row_ok,
        frobenius_contract_ok=contract.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Frob_p sends the conductor-39 period-norm word to its negative; "
            "the pure character word has signed period 2 and degree-6 norm zero."
        ),
        first_missing_clause=(
            "this Frobenius orbit law is not a finite-field value/divisor theorem "
            "or DANGER3 extraction"
        ),
        recommendation=(
            "reject value-side candidates that simply norm the pure conductor-39 "
            "character down from degree 6; continue only with a twisted trace, "
            "ratio, non-pure lift, or explicit conjugate descent that survives "
            "the alternating Frobenius signs"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_frobenius_orbit()
    print("p25 KSY-y Yang Y_507 conductor-39 Frobenius orbit gate")
    print(f"conductor={profile.conductor}")
    print(f"p_mod_39={profile.p_mod_39}")
    print(f"chi39_p={profile.chi39_p}")
    print(f"chi39_minus_one={profile.chi39_minus_one}")
    print(f"word_mod39={profile.word_mod39}")
    print("frobenius_rows")
    for row in profile.frobenius_rows:
        print(
            "  "
            f"degree={row.degree} multiplier={row.multiplier_mod_39} "
            f"same={int(row.image_equals_word)} negative={int(row.image_equals_negative_word)} "
            f"support={int(row.support_preserved)} ok={int(row.ok)}"
        )
    print("unit_orbits")
    for row in profile.unit_orbits:
        print(
            "  "
            f"orbit={row.orbit} coefficients={row.coefficients} "
            f"alternating={int(row.alternating_signs)} ok={int(row.ok)}"
        )
    print("conjugate_sums")
    print(f"  unit_orbit_length_counts={profile.unit_orbit_length_counts}")
    print(f"  two_conjugate_sum_support={profile.two_conjugate_sum_support}")
    print(f"  three_conjugate_sum_equals_word={int(profile.three_conjugate_sum_equals_word)}")
    print(f"  six_conjugate_sum_support={profile.six_conjugate_sum_support}")
    print(f"  exact_signed_frobenius_period={profile.exact_signed_frobenius_period}")
    print(f"  pure_character_degree6_norm_cancels={int(profile.pure_character_degree6_norm_cancels)}")
    print("checks")
    print(f"  conductor_gate_ok={int(profile.conductor_gate_ok)}")
    print(f"  frobenius_contract_ok={int(profile.frobenius_contract_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  frob_p_flips_the_conductor39_character_word=1")
    print("  naive_degree6_norm_of_pure_character_word_is_trivial=1")
    print("  continue_only_with_twisted_trace_ratio_or_non_pure_lift=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_frobenius_orbit_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 Frobenius orbit regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
