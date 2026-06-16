#!/usr/bin/env python3
"""Koo-Shin 6.2 screen for the four legal H0 translate products.

The exact-product query packet lists four legal level-507 H0 products.  Their
source words live at conductor 39 with coefficients +6 on P and -6 on N.  This
gate checks the Koo-Shin Theorem 6.2 congruence screen for each exact source
word.

Passing this screen is useful but deliberately not enough: it certifies product
legality at the source level, not a finite-field value/divisor theorem,
DANGER3 framing, X_1(16) extraction, or vpp.py verification.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_ksy_y_h0_translate_exact_product_query_packet_gate import (
    H0ExactProductQueryRow,
    profile_h0_translate_exact_product_query_packet,
)
from p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_gate import (
    FULL_FIBER_LENGTH,
    profile_koo_shin_theorem62_conductor39_unit,
)


@dataclass(frozen=True)
class H0TranslateKooShin62ScreenRow:
    name: str
    exact_product_row: str
    target_object: str
    multiplier_from_canonical: int
    positive_residues_mod39: tuple[int, ...]
    negative_residues_mod39: tuple[int, ...]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum: int
    exponent_sum_mod_12: int
    quadratic_sum_mod_39: int
    theorem62_congruences_ok: bool
    lemma61_full_fiber_cells: int
    boundary_equals_norm156_y507: bool
    source_certified_by_koo_shin62: bool
    source_theorem_closes: bool
    first_missing_clause: str
    row_ok: bool


@dataclass(frozen=True)
class H0TranslateKooShin62ScreenPacket:
    exact_product_query_ok: bool
    koo_shin_62_conductor39_unit_ok: bool
    theorem62_present: bool
    conductor: int
    full_fiber_length: int
    support_period: int
    screen_rows: tuple[H0TranslateKooShin62ScreenRow, ...]
    row_count: int
    theorem62_congruence_rows: int
    source_certified_rows: int
    source_theorem_closing_rows: int
    boundary_norm_rows: int
    canonical_rows: int
    h0_translate_rows: int
    full_fiber_cell_count: int
    source_closing_answer_shapes: int
    submission_ready_rows: int
    row_ok: bool


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(word.values()).items()))


def source_word(row: H0ExactProductQueryRow) -> dict[int, int]:
    word = {residue: 6 for residue in row.positive_residues_mod39}
    word.update({residue: -6 for residue in row.negative_residues_mod39})
    return dict(sorted(word.items()))


def screen_row(row: H0ExactProductQueryRow) -> H0TranslateKooShin62ScreenRow:
    word = source_word(row)
    exponent_sum = sum(word.values())
    quadratic_sum = sum(residue * residue * coefficient for residue, coefficient in word.items())
    congruences_ok = exponent_sum % 12 == 0 and quadratic_sum % 39 == 0
    support = len(word)
    fiber_cells = support * FULL_FIBER_LENGTH
    row_ok = (
        row.row_ok
        and support == 12
        and coefficient_counts(word) == ((-6, 6), (6, 6))
        and exponent_sum == 0
        and congruences_ok
        and fiber_cells == 468
        and row.boundary_equals_norm156_y507
    )
    return H0TranslateKooShin62ScreenRow(
        name=f"koo_shin62_screen_{row.name}",
        exact_product_row=row.name,
        target_object=row.target_object,
        multiplier_from_canonical=row.multiplier_from_canonical,
        positive_residues_mod39=row.positive_residues_mod39,
        negative_residues_mod39=row.negative_residues_mod39,
        support=support,
        coefficient_counts=coefficient_counts(word),
        exponent_sum=exponent_sum,
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum_mod_39=quadratic_sum % 39,
        theorem62_congruences_ok=congruences_ok,
        lemma61_full_fiber_cells=fiber_cells,
        boundary_equals_norm156_y507=row.boundary_equals_norm156_y507,
        source_certified_by_koo_shin62=congruences_ok,
        source_theorem_closes=False,
        first_missing_clause="finite-field value/divisor theorem for this exact H0 product",
        row_ok=row_ok,
    )


def profile_h0_translate_koo_shin62_screen() -> H0TranslateKooShin62ScreenPacket:
    exact = profile_h0_translate_exact_product_query_packet()
    ks62 = profile_koo_shin_theorem62_conductor39_unit()
    rows = tuple(screen_row(row) for row in exact.exact_product_rows)
    congruence_rows = sum(row.theorem62_congruences_ok for row in rows)
    certified = sum(row.source_certified_by_koo_shin62 for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    boundary = sum(row.boundary_equals_norm156_y507 for row in rows)
    canonical = sum(row.target_object == "canonical_H0" for row in rows)
    translates = sum(row.target_object == "H0_translate" for row in rows)
    full_fiber_cell_count = sum(row.lemma61_full_fiber_cells for row in rows)
    row_ok = (
        exact.row_ok
        and ks62.row_ok
        and ks62.theorem62_present
        and exact.conductor == 39
        and FULL_FIBER_LENGTH == 39
        and exact.support_period == 156
        and len(rows) == 4
        and congruence_rows == 4
        and certified == 4
        and source_closing == 0
        and boundary == 4
        and canonical == 1
        and translates == 3
        and full_fiber_cell_count == 1872
        and exact.source_closing_answer_shapes == 8
        and exact.submission_ready_rows == 0
        and tuple(row.multiplier_from_canonical for row in rows) == (1, 2, 4, 8)
        and tuple(row.exponent_sum_mod_12 for row in rows) == (0, 0, 0, 0)
        and tuple(row.quadratic_sum_mod_39 for row in rows) == (0, 0, 0, 0)
        and all(row.row_ok for row in rows)
    )
    return H0TranslateKooShin62ScreenPacket(
        exact_product_query_ok=exact.row_ok,
        koo_shin_62_conductor39_unit_ok=ks62.row_ok,
        theorem62_present=ks62.theorem62_present,
        conductor=exact.conductor,
        full_fiber_length=FULL_FIBER_LENGTH,
        support_period=exact.support_period,
        screen_rows=rows,
        row_count=len(rows),
        theorem62_congruence_rows=congruence_rows,
        source_certified_rows=certified,
        source_theorem_closing_rows=source_closing,
        boundary_norm_rows=boundary,
        canonical_rows=canonical,
        h0_translate_rows=translates,
        full_fiber_cell_count=full_fiber_cell_count,
        source_closing_answer_shapes=exact.source_closing_answer_shapes,
        submission_ready_rows=exact.submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_koo_shin62_screen()
    print("p25 KSY-y H0 translate Koo-Shin 6.2 screen gate")
    print("dependencies")
    print(f"  exact_product_query_ok={int(profile.exact_product_query_ok)}")
    print(f"  koo_shin_62_conductor39_unit_ok={int(profile.koo_shin_62_conductor39_unit_ok)}")
    print(f"  theorem62_present={int(profile.theorem62_present)}")
    print("family")
    print(f"  conductor={profile.conductor}")
    print(f"  full_fiber_length={profile.full_fiber_length}")
    print(f"  support_period={profile.support_period}")
    print("screen_rows")
    for row in profile.screen_rows:
        print(
            "  "
            f"{row.name}: exact={row.exact_product_row} target={row.target_object} "
            f"multiplier={row.multiplier_from_canonical} support={row.support} "
            f"counts={row.coefficient_counts} exp_mod12={row.exponent_sum_mod_12} "
            f"quad_mod39={row.quadratic_sum_mod_39} theorem62={int(row.theorem62_congruences_ok)} "
            f"fiber_cells={row.lemma61_full_fiber_cells} boundary={int(row.boundary_equals_norm156_y507)} "
            f"source_closes={int(row.source_theorem_closes)} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  theorem62_congruence_rows={profile.theorem62_congruence_rows}")
    print(f"  source_certified_rows={profile.source_certified_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  boundary_norm_rows={profile.boundary_norm_rows}")
    print(f"  canonical_rows={profile.canonical_rows}")
    print(f"  h0_translate_rows={profile.h0_translate_rows}")
    print(f"  full_fiber_cell_count={profile.full_fiber_cell_count}")
    print(f"  source_closing_answer_shapes={profile.source_closing_answer_shapes}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  all_four_exact_H0_products_pass_Koo_Shin_6_2_congruence_screen=1")
    print("  Koo_Shin_6_2_certifies_product_legality_not_value_or_divisor_theorem=1")
    print("  source_closure_still_requires_value_period156_or_divisor_identity=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_koo_shin62_screen_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate Koo-Shin 6.2 screen regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
