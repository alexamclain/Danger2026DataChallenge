#!/usr/bin/env python3
"""Selector structure of the legal sparse conductor-39 Hilbert-90 gauges.

The legal gauge-family gate found four support-12 sparse gauges.  This gate
records their compact theorem-facing normal form: a sign selector on the
four-class Frobenius quotient, anti-invariant under multiplication by 4.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    character_word,
    frobenius_orbits,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_gate import (
    gauge_word,
    profile_hilbert90_legal_gauge_family,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25


@dataclass(frozen=True)
class SparseSelectorRow:
    name: str
    quotient_signs: tuple[int, int, int, int]
    constants: tuple[int, int, int, int]
    support: int
    positive_support: tuple[int, ...]
    negative_support: tuple[int, ...]
    coefficient_counts: tuple[tuple[int, int], ...]
    formula_v_equals_3_selector_minus_chi: bool
    anti_invariant_under_times4: bool
    mod3_pushforward: tuple[int, int, int]
    mod13_pushforward: tuple[int, ...]
    proper_axis_pushforwards_vanish: bool
    expected_legal_sparse: bool
    ok: bool


@dataclass(frozen=True)
class SparseSelectorStructureProfile:
    conductor: int
    p_mod_39: int
    frobenius_orbits: tuple[tuple[int, ...], ...]
    times2_orbit_map: tuple[int, int, int, int]
    times4_orbit_map: tuple[int, int, int, int]
    times7_orbit_map: tuple[int, int, int, int]
    frobenius_orbit_map: tuple[int, int, int, int]
    legal_sparse_rows: tuple[SparseSelectorRow, ...]
    formal_one_coset_rows: tuple[SparseSelectorRow, ...]
    legal_sparse_count: int
    formal_one_coset_count: int
    all_legal_sparse_have_vanishing_axis_pushforwards: bool
    all_formal_one_cosets_have_nonzero_axis_pushforwards: bool
    legal_gauge_family_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def orbit_index() -> dict[int, int]:
    return {
        residue: index
        for index, orbit in enumerate(frobenius_orbits(character_word()))
        for residue in orbit
    }


def orbit_map(multiplier: int) -> tuple[int, int, int, int]:
    index = orbit_index()
    return tuple(index[(multiplier * orbit[0]) % CONDUCTOR] for orbit in frobenius_orbits(character_word()))


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def pushforward_mod(word: dict[int, int], modulus: int) -> tuple[int, ...]:
    return tuple(
        sum(coefficient for residue, coefficient in word.items() if residue % modulus == target)
        for target in range(modulus)
    )


def selector_formula_ok(word: dict[int, int], signs: tuple[int, int, int, int]) -> bool:
    index = orbit_index()
    for residue in range(CONDUCTOR):
        if not chi39(residue):
            if word.get(residue, 0) != 0:
                return False
            continue
        expected = 3 * (signs[index[residue]] - chi39(residue))
        if expected == 0:
            if word.get(residue, 0) != 0:
                return False
        elif word.get(residue, 0) != expected:
            return False
    return True


def anti_invariant_under_times4(signs: tuple[int, int, int, int]) -> bool:
    times4 = orbit_map(4)
    return all(signs[times4[index]] == -signs[index] for index in range(4))


def selector_row(
    name: str,
    signs: tuple[int, int, int, int],
    expected_legal_sparse: bool,
) -> SparseSelectorRow:
    constants = tuple(3 * sign for sign in signs)
    word = gauge_word(constants)
    mod3 = pushforward_mod(word, 3)
    mod13 = pushforward_mod(word, 13)
    legal_sparse = (
        len(word) == 12
        and coefficient_counts(word) == ((-6, 6), (6, 6))
        and selector_formula_ok(word, signs)
        and anti_invariant_under_times4(signs)
        and all(value == 0 for value in mod3)
        and all(value == 0 for value in mod13)
    )
    formal_one_coset = (
        len(word) == 12
        and coefficient_counts(word) in {((-6, 12),), ((6, 12),)}
        and selector_formula_ok(word, signs)
        and not anti_invariant_under_times4(signs)
        and (any(value != 0 for value in mod3) or any(value != 0 for value in mod13))
    )
    return SparseSelectorRow(
        name=name,
        quotient_signs=signs,
        constants=constants,
        support=len(word),
        positive_support=tuple(sorted(residue for residue, coefficient in word.items() if coefficient > 0)),
        negative_support=tuple(sorted(residue for residue, coefficient in word.items() if coefficient < 0)),
        coefficient_counts=coefficient_counts(word),
        formula_v_equals_3_selector_minus_chi=selector_formula_ok(word, signs),
        anti_invariant_under_times4=anti_invariant_under_times4(signs),
        mod3_pushforward=mod3,
        mod13_pushforward=mod13,
        proper_axis_pushforwards_vanish=all(value == 0 for value in mod3) and all(value == 0 for value in mod13),
        expected_legal_sparse=expected_legal_sparse,
        ok=legal_sparse if expected_legal_sparse else formal_one_coset,
    )


def profile_hilbert90_sparse_selector_structure() -> SparseSelectorStructureProfile:
    family = profile_hilbert90_legal_gauge_family()
    legal_rows = tuple(
        selector_row(
            f"legal_sparse_selector_{index}",
            signs,
            True,
        )
        for index, signs in enumerate(
            (
                (1, 1, -1, -1),
                (1, -1, -1, 1),
                (-1, 1, 1, -1),
                (-1, -1, 1, 1),
            )
        )
    )
    formal_rows = (
        selector_row("formal_positive_one_coset_selector", (1, 1, 1, 1), False),
        selector_row("formal_negative_one_coset_selector", (-1, -1, -1, -1), False),
    )
    direct_closer = False
    legal_axis_zero = all(row.proper_axis_pushforwards_vanish for row in legal_rows)
    formal_axis_nonzero = all(not row.proper_axis_pushforwards_vanish for row in formal_rows)
    row_ok = (
        family.row_ok
        and CONDUCTOR == 39
        and P25 % 39 == 23
        and orbit_map(2) == (1, 2, 3, 0)
        and orbit_map(4) == (2, 3, 0, 1)
        and orbit_map(7) == (1, 2, 3, 0)
        and orbit_map(P25) == (0, 1, 2, 3)
        and len(legal_rows) == 4
        and len(formal_rows) == 2
        and all(row.ok for row in legal_rows)
        and all(row.ok for row in formal_rows)
        and legal_axis_zero
        and formal_axis_nonzero
        and family.support12_legal_sparse_rows == 4
        and family.support12_formal_one_coset_rows == 2
        and not direct_closer
    )
    return SparseSelectorStructureProfile(
        conductor=CONDUCTOR,
        p_mod_39=P25 % 39,
        frobenius_orbits=frobenius_orbits(character_word()),
        times2_orbit_map=orbit_map(2),
        times4_orbit_map=orbit_map(4),
        times7_orbit_map=orbit_map(7),
        frobenius_orbit_map=orbit_map(P25),
        legal_sparse_rows=legal_rows,
        formal_one_coset_rows=formal_rows,
        legal_sparse_count=len(legal_rows),
        formal_one_coset_count=len(formal_rows),
        all_legal_sparse_have_vanishing_axis_pushforwards=legal_axis_zero,
        all_formal_one_cosets_have_nonzero_axis_pushforwards=formal_axis_nonzero,
        legal_gauge_family_ok=family.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The four legal support-12 Hilbert-90 gauges are exactly the "
            "anti-invariant +/- sign selectors on the Frobenius quotient, "
            "V_s(r)=3*(s([r])-chi_39(r)), and their mod-3 and mod-13 "
            "pushforwards vanish."
        ),
        first_missing_clause=(
            "selector structure is a theorem-facing source normal form, not a "
            "finite-field value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask source/value theorems for an anti-invariant quotient sign "
            "selector; reject one-coset sparse gauges and projection-only "
            "explanations"
        ),
        row_ok=row_ok,
    )


def print_row(row: SparseSelectorRow) -> None:
    print(
        "  "
        f"{row.name}: signs={row.quotient_signs} support={row.support} "
        f"counts={row.coefficient_counts} formula={int(row.formula_v_equals_3_selector_minus_chi)} "
        f"anti4={int(row.anti_invariant_under_times4)} "
        f"axis_zero={int(row.proper_axis_pushforwards_vanish)} "
        f"expected_legal={int(row.expected_legal_sparse)} ok={int(row.ok)}"
    )
    print(f"    positive_support={row.positive_support}")
    print(f"    negative_support={row.negative_support}")
    print(f"    mod3_pushforward={row.mod3_pushforward}")
    nonzero_mod13 = tuple((index, value) for index, value in enumerate(row.mod13_pushforward) if value)
    print(f"    mod13_pushforward_nonzero={nonzero_mod13}")


def main() -> int:
    profile = profile_hilbert90_sparse_selector_structure()
    print("p25 KSY-y Yang Y_507 conductor-39 Hilbert-90 sparse selector structure gate")
    print(f"conductor={profile.conductor}")
    print(f"p_mod_39={profile.p_mod_39}")
    print(f"frobenius_orbits={profile.frobenius_orbits}")
    print("quotient_orbit_maps")
    print(f"  times2={profile.times2_orbit_map}")
    print(f"  times4={profile.times4_orbit_map}")
    print(f"  times7={profile.times7_orbit_map}")
    print(f"  frobenius={profile.frobenius_orbit_map}")
    print("legal_sparse_rows")
    for row in profile.legal_sparse_rows:
        print_row(row)
    print("formal_one_coset_rows")
    for row in profile.formal_one_coset_rows:
        print_row(row)
    print("counts")
    print(f"  legal_sparse_count={profile.legal_sparse_count}")
    print(f"  formal_one_coset_count={profile.formal_one_coset_count}")
    print(
        "  all_legal_sparse_have_vanishing_axis_pushforwards="
        f"{int(profile.all_legal_sparse_have_vanishing_axis_pushforwards)}"
    )
    print(
        "  all_formal_one_cosets_have_nonzero_axis_pushforwards="
        f"{int(profile.all_formal_one_cosets_have_nonzero_axis_pushforwards)}"
    )
    print(f"  legal_gauge_family_ok={int(profile.legal_gauge_family_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  legal_sparse_gauges_are_anti_invariant_quotient_sign_selectors=1")
    print("  legal_sparse_gauges_preserve_zero_mod3_and_mod13_pushforwards=1")
    print("  one_coset_sparse_gauges_are_formal_projection_visible_controls=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Hilbert-90 sparse selector structure regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
