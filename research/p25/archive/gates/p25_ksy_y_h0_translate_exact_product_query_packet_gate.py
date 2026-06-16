#!/usr/bin/env python3
"""Exact-product query packet for legal H0 translate theorem hunts.

The theorem-query packet says what answer shape closes the H0 source stage.
This packet supplies the exact four product targets that such a theorem may
hit.  It is meant for paper/expert matching: each row records the multiplier,
conductor-39 residue sets, lifted support, boundary check, and accepted answer
shapes.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    SparseProductNormalFormRow,
    profile_sparse_h90_product_normal_form,
)


@dataclass(frozen=True)
class H0ExactProductQueryRow:
    name: str
    target_object: str
    multiplier_from_canonical: int
    selector_name: str
    source_constants: tuple[int, ...]
    positive_residues_mod39: tuple[int, ...]
    negative_residues_mod39: tuple[int, ...]
    positive_residue_count: int
    negative_residue_count: int
    lifted_positive_count: int
    lifted_negative_count: int
    lifted_support: int
    boundary_equals_norm156_y507: bool
    product_formula: str
    accepted_value_answer_shape: str
    accepted_divisor_answer_shape: str
    first_falsifier: str
    row_ok: bool


@dataclass(frozen=True)
class H0ExactProductQueryPacket:
    sparse_h90_product_normal_form_ok: bool
    conductor: int
    target_level: int
    lift_length: int
    support_period: int
    canonical_stabilizer: tuple[int, ...]
    quotient_representatives: tuple[int, ...]
    exact_product_rows: tuple[H0ExactProductQueryRow, ...]
    row_count: int
    canonical_rows: int
    h0_translate_rows: int
    value_answer_shape_rows: int
    divisor_answer_shape_rows: int
    boundary_norm_rows: int
    all_78_over_78: bool
    all_formula_lift_13_fibers: bool
    source_closing_answer_shapes: int
    submission_ready_rows: int
    row_ok: bool


VALUE_ANSWER_SHAPE = (
    "exact finite-field value identity for this product with period-156 "
    "branch/root/telescoping context"
)

DIVISOR_ANSWER_SHAPE = (
    "exact divisor/additive identity for this product with the Hilbert-90 "
    "boundary to Norm_156(Y_507)"
)


def query_row(product_row: SparseProductNormalFormRow) -> H0ExactProductQueryRow:
    target = "canonical_H0" if product_row.multiplier_from_canonical == 1 else "H0_translate"
    row_ok = (
        product_row.row_ok
        and product_row.source_positive_count == 6
        and product_row.source_negative_count == 6
        and product_row.lifted_positive_count == 78
        and product_row.lifted_negative_count == 78
        and product_row.lifted_support == 156
        and product_row.boundary_equals_period_norm
        and "k=0..12" in product_row.product_formula
        and product_row.lifted_coefficient_counts == ((-6, 78), (6, 78))
    )
    return H0ExactProductQueryRow(
        name=f"exact_h0_product_m{product_row.multiplier_from_canonical}",
        target_object=target,
        multiplier_from_canonical=product_row.multiplier_from_canonical,
        selector_name=product_row.selector_name,
        source_constants=product_row.source_constants,
        positive_residues_mod39=product_row.source_positive_residues,
        negative_residues_mod39=product_row.source_negative_residues,
        positive_residue_count=product_row.source_positive_count,
        negative_residue_count=product_row.source_negative_count,
        lifted_positive_count=product_row.lifted_positive_count,
        lifted_negative_count=product_row.lifted_negative_count,
        lifted_support=product_row.lifted_support,
        boundary_equals_norm156_y507=product_row.boundary_equals_period_norm,
        product_formula=product_row.product_formula,
        accepted_value_answer_shape=VALUE_ANSWER_SHAPE,
        accepted_divisor_answer_shape=DIVISOR_ANSWER_SHAPE,
        first_falsifier=(
            "wrong residue sets, nonlegal sparse gauge, formal one-coset H, "
            "missing boundary, or missing period-156 context for value claims"
        ),
        row_ok=row_ok,
    )


def profile_h0_translate_exact_product_query_packet() -> H0ExactProductQueryPacket:
    normal = profile_sparse_h90_product_normal_form()
    rows = tuple(query_row(row) for row in normal.legal_rows)
    canonical = sum(row.target_object == "canonical_H0" for row in rows)
    translates = sum(row.target_object == "H0_translate" for row in rows)
    value_shapes = sum(bool(row.accepted_value_answer_shape) for row in rows)
    divisor_shapes = sum(bool(row.accepted_divisor_answer_shape) for row in rows)
    boundary_rows = sum(row.boundary_equals_norm156_y507 for row in rows)
    all_78 = all(
        row.lifted_positive_count == 78
        and row.lifted_negative_count == 78
        and row.lifted_support == 156
        for row in rows
    )
    all_lift = all("k=0..12" in row.product_formula for row in rows)
    source_closing_shapes = value_shapes + divisor_shapes
    submission_ready = 0
    row_ok = (
        normal.row_ok
        and normal.conductor == 39
        and normal.target_level == 507
        and normal.lift_length == 13
        and normal.support_period == 156
        and normal.canonical_stabilizer == (1, 16, 22)
        and normal.quotient_representatives == (1, 2, 4, 8)
        and len(rows) == 4
        and canonical == 1
        and translates == 3
        and value_shapes == 4
        and divisor_shapes == 4
        and boundary_rows == 4
        and all_78
        and all_lift
        and source_closing_shapes == 8
        and submission_ready == 0
        and tuple(row.multiplier_from_canonical for row in rows) == (1, 2, 4, 8)
        and tuple(row.positive_residues_mod39 for row in rows)
        == (
            (7, 17, 23, 34, 37, 38),
            (7, 14, 29, 34, 35, 37),
            (14, 19, 28, 29, 31, 35),
            (17, 19, 23, 28, 31, 38),
        )
        and tuple(row.negative_residues_mod39 for row in rows)
        == (
            (4, 8, 10, 11, 20, 25),
            (1, 8, 11, 16, 20, 22),
            (1, 2, 5, 16, 22, 32),
            (2, 4, 5, 10, 25, 32),
        )
        and all(row.row_ok for row in rows)
    )
    return H0ExactProductQueryPacket(
        sparse_h90_product_normal_form_ok=normal.row_ok,
        conductor=normal.conductor,
        target_level=normal.target_level,
        lift_length=normal.lift_length,
        support_period=normal.support_period,
        canonical_stabilizer=normal.canonical_stabilizer,
        quotient_representatives=normal.quotient_representatives,
        exact_product_rows=rows,
        row_count=len(rows),
        canonical_rows=canonical,
        h0_translate_rows=translates,
        value_answer_shape_rows=value_shapes,
        divisor_answer_shape_rows=divisor_shapes,
        boundary_norm_rows=boundary_rows,
        all_78_over_78=all_78,
        all_formula_lift_13_fibers=all_lift,
        source_closing_answer_shapes=source_closing_shapes,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_exact_product_query_packet()
    print("p25 KSY-y H0 translate exact-product query packet gate")
    print("dependencies")
    print(f"  sparse_h90_product_normal_form_ok={int(profile.sparse_h90_product_normal_form_ok)}")
    print("family")
    print(f"  conductor={profile.conductor}")
    print(f"  target_level={profile.target_level}")
    print(f"  lift_length={profile.lift_length}")
    print(f"  support_period={profile.support_period}")
    print(f"  canonical_stabilizer={profile.canonical_stabilizer}")
    print(f"  quotient_representatives={profile.quotient_representatives}")
    print("exact_product_rows")
    for row in profile.exact_product_rows:
        print(
            "  "
            f"{row.name}: target={row.target_object} "
            f"multiplier={row.multiplier_from_canonical} selector={row.selector_name} "
            f"constants={row.source_constants} pos={row.positive_residues_mod39} "
            f"neg={row.negative_residues_mod39} lift=+{row.lifted_positive_count}/"
            f"-{row.lifted_negative_count} support={row.lifted_support} "
            f"boundary={int(row.boundary_equals_norm156_y507)}"
        )
        print(f"    formula={row.product_formula}")
        print(f"    accepts_value={row.accepted_value_answer_shape}")
        print(f"    accepts_divisor={row.accepted_divisor_answer_shape}")
        print(f"    falsifier={row.first_falsifier}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  canonical_rows={profile.canonical_rows}")
    print(f"  h0_translate_rows={profile.h0_translate_rows}")
    print(f"  value_answer_shape_rows={profile.value_answer_shape_rows}")
    print(f"  divisor_answer_shape_rows={profile.divisor_answer_shape_rows}")
    print(f"  boundary_norm_rows={profile.boundary_norm_rows}")
    print(f"  all_78_over_78={int(profile.all_78_over_78)}")
    print(f"  all_formula_lift_13_fibers={int(profile.all_formula_lift_13_fibers)}")
    print(f"  source_closing_answer_shapes={profile.source_closing_answer_shapes}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  theorem_hunt_has_four_exact_legal_H0_product_targets=1")
    print("  accepted_yes_is_value_period156_or_divisor_identity_for_one_target=1")
    print("  boundary_only_or_formal_one_coset_H_is_not_enough=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_exact_product_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate exact-product query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
