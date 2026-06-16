#!/usr/bin/env python3
"""Sparse Hilbert-90 Yang lift for the p25 conductor-39 source.

The legal sparse Hilbert-90 gauges on X_1(39) have support 12.  Yang's
13-fiber distribution sends each of them to a support-156 potential on level
507.  Applying (1 - Frob_p) to that lifted potential recovers the full
312-cell period norm of Y_507.

This is a sharper value-side theorem target: prove or source a legal sparse
Hilbert-90 potential, not merely the larger period-norm boundary.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    LIFT_LENGTH,
    distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25
from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import character_word
from p25_ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_gate import gauge_word
from p25_ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_gate import (
    SparseSelectorRow,
    profile_hilbert90_sparse_selector_structure,
)
from p25_ksy_y_yang_y507_modular_period_certificate_gate import SUPPORT_PERIOD
from p25_ksy_y_yang_y507_period_norm_character_gate import period_norm
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import QUOTIENT_LEVEL


Word = dict[int, int]


@dataclass(frozen=True)
class SparseYangLiftRow:
    name: str
    expected_legal_sparse: bool
    source_constants: tuple[int, int, int, int]
    source_support: int
    source_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_support: int
    lifted_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_mod3_pushforward: tuple[int, int, int]
    lifted_mod13_pushforward: tuple[int, ...]
    lifted_axis_pushforwards_vanish: bool
    boundary_support: int
    boundary_coefficient_counts: tuple[tuple[int, int], ...]
    boundary_equals_lifted_character_word: bool
    boundary_equals_period_norm: bool
    selector_axis_pushforwards_vanish: bool
    row_ok: bool


@dataclass(frozen=True)
class SparseHilbert90YangLiftProfile:
    target_level: int
    lift_length: int
    support_period: int
    period_norm_support: int
    period_norm_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_character_support: int
    lifted_character_coefficient_counts: tuple[tuple[int, int], ...]
    lifted_character_equals_period_norm: bool
    legal_sparse_rows: tuple[SparseYangLiftRow, ...]
    formal_one_coset_rows: tuple[SparseYangLiftRow, ...]
    legal_sparse_lift_count: int
    formal_one_coset_lift_count: int
    min_legal_lifted_potential_support: int
    balanced_lifted_potential_support: int
    sparse_lift_halves_boundary_support: bool
    all_legal_lifts_have_vanishing_axis_pushforwards: bool
    all_formal_lifts_have_nonzero_axis_pushforwards: bool
    selector_structure_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero(word: Word) -> Word:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def coefficient_counts(word: Word) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(word.values()).items()))


def push_frobenius_507(word: Word) -> Word:
    out: Word = {}
    for residue, coefficient in word.items():
        target = (P25 * residue) % QUOTIENT_LEVEL
        out[target] = out.get(target, 0) + coefficient
    return nonzero(out)


def subtract_words(left: Word, right: Word) -> Word:
    out = dict(left)
    for residue, coefficient in right.items():
        out[residue] = out.get(residue, 0) - coefficient
    return nonzero(out)


def boundary_507(potential: Word) -> Word:
    return subtract_words(potential, push_frobenius_507(potential))


def pushforward_mod(word: Word, modulus: int) -> tuple[int, ...]:
    return tuple(
        sum(coefficient for residue, coefficient in word.items() if residue % modulus == target)
        for target in range(modulus)
    )


def sparse_lift_row(
    selector: SparseSelectorRow,
    period_norm_word: Word,
    lifted_character: Word,
) -> SparseYangLiftRow:
    source = gauge_word(selector.constants)
    lifted = distribution_lift(source)
    boundary = boundary_507(lifted)
    mod3 = pushforward_mod(lifted, 3)
    mod13 = pushforward_mod(lifted, 13)
    lifted_axis_zero = all(value == 0 for value in mod3) and all(value == 0 for value in mod13)
    boundary_ok = boundary == lifted_character == period_norm_word
    legal_ok = (
        selector.expected_legal_sparse
        and selector.ok
        and selector.proper_axis_pushforwards_vanish
        and len(source) == 12
        and coefficient_counts(source) == ((-6, 6), (6, 6))
        and len(lifted) == 156
        and coefficient_counts(lifted) == ((-6, 78), (6, 78))
        and lifted_axis_zero
        and boundary_ok
    )
    formal_ok = (
        not selector.expected_legal_sparse
        and selector.ok
        and not selector.proper_axis_pushforwards_vanish
        and len(source) == 12
        and coefficient_counts(source) in {((-6, 12),), ((6, 12),)}
        and len(lifted) == 156
        and coefficient_counts(lifted) in {((-6, 156),), ((6, 156),)}
        and not lifted_axis_zero
        and boundary_ok
    )
    return SparseYangLiftRow(
        name=selector.name,
        expected_legal_sparse=selector.expected_legal_sparse,
        source_constants=selector.constants,
        source_support=len(source),
        source_coefficient_counts=coefficient_counts(source),
        lifted_support=len(lifted),
        lifted_coefficient_counts=coefficient_counts(lifted),
        lifted_mod3_pushforward=mod3,
        lifted_mod13_pushforward=mod13,
        lifted_axis_pushforwards_vanish=lifted_axis_zero,
        boundary_support=len(boundary),
        boundary_coefficient_counts=coefficient_counts(boundary),
        boundary_equals_lifted_character_word=boundary == lifted_character,
        boundary_equals_period_norm=boundary == period_norm_word,
        selector_axis_pushforwards_vanish=selector.proper_axis_pushforwards_vanish,
        row_ok=legal_ok if selector.expected_legal_sparse else formal_ok,
    )


def profile_sparse_hilbert90_yang_lift() -> SparseHilbert90YangLiftProfile:
    selector_profile = profile_hilbert90_sparse_selector_structure()
    y507 = profile_yang_y507_primitive_factor_word()
    period_norm_word = period_norm(dict(y507.y507_primitive_word), SUPPORT_PERIOD)
    lifted_character = distribution_lift(character_word())
    legal_rows = tuple(
        sparse_lift_row(row, period_norm_word, lifted_character)
        for row in selector_profile.legal_sparse_rows
    )
    formal_rows = tuple(
        sparse_lift_row(row, period_norm_word, lifted_character)
        for row in selector_profile.formal_one_coset_rows
    )
    balanced_lift = distribution_lift(gauge_word((0, 0, 0, 0)))
    direct_closer = False
    legal_axis_zero = all(row.lifted_axis_pushforwards_vanish for row in legal_rows)
    formal_axis_nonzero = all(not row.lifted_axis_pushforwards_vanish for row in formal_rows)
    min_legal_lift = min(row.lifted_support for row in legal_rows)
    sparse_halves_boundary = 2 * min_legal_lift == len(period_norm_word)
    row_ok = (
        selector_profile.row_ok
        and y507.row_ok
        and QUOTIENT_LEVEL == 507
        and LIFT_LENGTH == 13
        and SUPPORT_PERIOD == 156
        and len(period_norm_word) == 312
        and coefficient_counts(period_norm_word) == ((-6, 156), (6, 156))
        and lifted_character == period_norm_word
        and len(lifted_character) == 312
        and len(legal_rows) == 4
        and len(formal_rows) == 2
        and all(row.row_ok for row in legal_rows)
        and all(row.row_ok for row in formal_rows)
        and legal_axis_zero
        and formal_axis_nonzero
        and min_legal_lift == 156
        and len(balanced_lift) == 312
        and coefficient_counts(balanced_lift) == ((-3, 156), (3, 156))
        and sparse_halves_boundary
        and not direct_closer
    )
    return SparseHilbert90YangLiftProfile(
        target_level=QUOTIENT_LEVEL,
        lift_length=LIFT_LENGTH,
        support_period=SUPPORT_PERIOD,
        period_norm_support=len(period_norm_word),
        period_norm_coefficient_counts=coefficient_counts(period_norm_word),
        lifted_character_support=len(lifted_character),
        lifted_character_coefficient_counts=coefficient_counts(lifted_character),
        lifted_character_equals_period_norm=lifted_character == period_norm_word,
        legal_sparse_rows=legal_rows,
        formal_one_coset_rows=formal_rows,
        legal_sparse_lift_count=len(legal_rows),
        formal_one_coset_lift_count=len(formal_rows),
        min_legal_lifted_potential_support=min_legal_lift,
        balanced_lifted_potential_support=len(balanced_lift),
        sparse_lift_halves_boundary_support=sparse_halves_boundary,
        all_legal_lifts_have_vanishing_axis_pushforwards=legal_axis_zero,
        all_formal_lifts_have_nonzero_axis_pushforwards=formal_axis_nonzero,
        selector_structure_ok=selector_profile.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Each legal support-12 Hilbert-90 selector on X_1(39) lifts to a "
            "support-156 level-507 potential H_s with (1-Frob_p)H_s equal to "
            "Norm_156(Y_507)."
        ),
        first_missing_clause=(
            "the support-156 potential is a sharper value-side theorem target, "
            "not yet a finite-field value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "prefer theorem hits that emit a legal sparse Hilbert-90 potential "
            "or its value; reject one-coset sparse lifts even though their "
            "formal Frobenius boundary matches the period norm"
        ),
        row_ok=row_ok,
    )


def print_row(row: SparseYangLiftRow) -> None:
    nonzero_mod13 = tuple((index, value) for index, value in enumerate(row.lifted_mod13_pushforward) if value)
    print(
        "  "
        f"{row.name}: legal={int(row.expected_legal_sparse)} "
        f"source_support={row.source_support} source_counts={row.source_coefficient_counts} "
        f"lift_support={row.lifted_support} lift_counts={row.lifted_coefficient_counts} "
        f"axis_zero={int(row.lifted_axis_pushforwards_vanish)} "
        f"boundary_support={row.boundary_support} "
        f"boundary_counts={row.boundary_coefficient_counts} "
        f"boundary_norm={int(row.boundary_equals_period_norm)} ok={int(row.row_ok)}"
    )
    print(f"    constants={row.source_constants}")
    print(f"    lifted_mod3_pushforward={row.lifted_mod3_pushforward}")
    print(f"    lifted_mod13_pushforward_nonzero={nonzero_mod13}")


def main() -> int:
    profile = profile_sparse_hilbert90_yang_lift()
    print("p25 KSY-y Yang Y_507 sparse Hilbert-90 Yang-lift gate")
    print(f"target_level={profile.target_level}")
    print(f"lift_length={profile.lift_length}")
    print(f"support_period={profile.support_period}")
    print("period_norm")
    print(f"  support={profile.period_norm_support}")
    print(f"  counts={profile.period_norm_coefficient_counts}")
    print(f"  lifted_character_support={profile.lifted_character_support}")
    print(f"  lifted_character_counts={profile.lifted_character_coefficient_counts}")
    print(f"  lifted_character_equals_period_norm={int(profile.lifted_character_equals_period_norm)}")
    print("legal_sparse_lifts")
    for row in profile.legal_sparse_rows:
        print_row(row)
    print("formal_one_coset_controls")
    for row in profile.formal_one_coset_rows:
        print_row(row)
    print("counts")
    print(f"  legal_sparse_lift_count={profile.legal_sparse_lift_count}")
    print(f"  formal_one_coset_lift_count={profile.formal_one_coset_lift_count}")
    print(f"  min_legal_lifted_potential_support={profile.min_legal_lifted_potential_support}")
    print(f"  balanced_lifted_potential_support={profile.balanced_lifted_potential_support}")
    print(f"  sparse_lift_halves_boundary_support={int(profile.sparse_lift_halves_boundary_support)}")
    print(
        "  all_legal_lifts_have_vanishing_axis_pushforwards="
        f"{int(profile.all_legal_lifts_have_vanishing_axis_pushforwards)}"
    )
    print(
        "  all_formal_lifts_have_nonzero_axis_pushforwards="
        f"{int(profile.all_formal_lifts_have_nonzero_axis_pushforwards)}"
    )
    print(f"  selector_structure_ok={int(profile.selector_structure_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  legal_sparse_H90_gauge_lifts_to_support156_period_potential=1")
    print("  frobenius_boundary_of_support156_potential_is_Norm156_Y507=1")
    print("  formal_one_coset_lifts_have_same_boundary_but_fail_mixed_axis_tests=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("sparse Hilbert-90 Yang-lift regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
