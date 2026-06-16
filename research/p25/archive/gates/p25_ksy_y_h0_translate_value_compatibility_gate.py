#!/usr/bin/env python3
"""Compatibility packet for legal H0 translates.

The H0/Y507 period gate checks the canonical H0 value route.  This gate makes
the translate language precise: the only accepted H0 translates are the four
78-over-78 sparse Yang-fiber products in the conductor-39 doubling orbit.
Everything else remains a theorem target, a conditional verifier payload, or a
rejected formal lookalike.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_period156_value_compatibility_gate import (
    profile_h0_period156_value_compatibility,
)
from p25_ksy_y_h90_value_theorem_intake_gate import (
    H90ValueTheoremClaim,
    classify_claim,
    profile_h90_value_theorem_intake,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    SparseProductNormalFormRow,
    profile_sparse_h90_product_normal_form,
)


@dataclass(frozen=True)
class H0TranslateCompatibilityRow:
    name: str
    target_object: str
    output_kind: str
    selector_name: str
    multiplier_from_canonical: int
    source_constants: tuple[int, ...]
    source_positive_residues: tuple[int, ...]
    source_negative_residues: tuple[int, ...]
    lifted_positive_count: int
    lifted_negative_count: int
    lifted_support: int
    boundary_equals_period_norm: bool
    legal_translate_product: bool
    theorem_body_verified: bool
    exact_target: bool
    bridge_spine_preserved: bool
    legal_yang_or_h90_object: bool
    boundary_context: bool
    period156_context: bool
    arithmetic_source: bool
    expected_decision: str
    actual_decision: str
    expected_missing_clause: str
    actual_missing_clause: str
    source_stage_closed: bool
    value_closing: bool
    divisor_closing: bool
    rejected: bool
    conditional: bool
    ok: bool


@dataclass(frozen=True)
class H0TranslateCompatibilityPacket:
    h90_intake_ok: bool
    h0_period156_compatibility_ok: bool
    sparse_h90_normal_form_ok: bool
    support_period: int
    doubling_subgroup: tuple[int, ...]
    canonical_stabilizer: tuple[int, ...]
    quotient_representatives: tuple[int, ...]
    legal_product_rows: int
    legal_products_form_one_doubling_orbit: bool
    legal_products_are_78_over_78: bool
    formal_one_coset_controls_rejected: bool
    compatibility_rows: tuple[H0TranslateCompatibilityRow, ...]
    row_count: int
    legal_translate_rows: int
    canonical_target_rows: int
    h0_translate_target_rows: int
    source_closing_rows: int
    value_closing_rows: int
    divisor_closing_rows: int
    rejected_rows: int
    conditional_rows: int
    finite_payload_rows: int
    submission_ready_rows: int
    row_ok: bool


def make_claim(
    *,
    name: str,
    target_object: str,
    output_kind: str,
    theorem_body_verified: bool = True,
    exact_target: bool = True,
    bridge_spine_preserved: bool = True,
    legal_yang_or_h90_object: bool = True,
    boundary_context: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H90ValueTheoremClaim:
    return H90ValueTheoremClaim(
        name=name,
        theorem_body_verified=theorem_body_verified,
        target_object=target_object,
        output_kind=output_kind,
        exact_target=exact_target,
        bridge_spine_preserved=bridge_spine_preserved,
        legal_yang_or_h90_object=legal_yang_or_h90_object,
        boundary_or_period_norm_context=boundary_context,
        finite_field_identity_or_divisor=output_kind != "finite-verifier",
        period_156_context=period156,
        arithmetic_source_theorem=arithmetic_source,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def compatibility_row(
    *,
    name: str,
    target_object: str,
    output_kind: str,
    expected_decision: str,
    expected_missing: str,
    product_row: SparseProductNormalFormRow | None = None,
    legal_translate_product: bool = False,
    theorem_body_verified: bool = True,
    exact_target: bool = True,
    bridge_spine_preserved: bool = True,
    legal_yang_or_h90_object: bool = True,
    boundary_context: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H0TranslateCompatibilityRow:
    claim = make_claim(
        name=name,
        target_object=target_object,
        output_kind=output_kind,
        theorem_body_verified=theorem_body_verified,
        exact_target=exact_target,
        bridge_spine_preserved=bridge_spine_preserved,
        legal_yang_or_h90_object=legal_yang_or_h90_object,
        boundary_context=boundary_context,
        period156=period156,
        arithmetic_source=arithmetic_source,
    )
    decision = classify_claim(claim)
    source_stage_closed = decision.theorem_source_closed
    value_closing = source_stage_closed and output_kind == "value"
    divisor_closing = source_stage_closed and output_kind == "divisor-additive"
    rejected = decision.decision.startswith("reject_")
    conditional = decision.decision.startswith(("conditional_", "live_target_identified_"))

    if product_row is None:
        selector_name = "control"
        multiplier = 0
        constants: tuple[int, ...] = ()
        positive: tuple[int, ...] = ()
        negative: tuple[int, ...] = ()
        lifted_positive_count = 0
        lifted_negative_count = 0
        lifted_support = 0
        boundary_norm = False
    else:
        selector_name = product_row.selector_name
        multiplier = product_row.multiplier_from_canonical
        constants = product_row.source_constants
        positive = product_row.source_positive_residues
        negative = product_row.source_negative_residues
        lifted_positive_count = product_row.lifted_positive_count
        lifted_negative_count = product_row.lifted_negative_count
        lifted_support = product_row.lifted_support
        boundary_norm = product_row.boundary_equals_period_norm

    return H0TranslateCompatibilityRow(
        name=name,
        target_object=target_object,
        output_kind=output_kind,
        selector_name=selector_name,
        multiplier_from_canonical=multiplier,
        source_constants=constants,
        source_positive_residues=positive,
        source_negative_residues=negative,
        lifted_positive_count=lifted_positive_count,
        lifted_negative_count=lifted_negative_count,
        lifted_support=lifted_support,
        boundary_equals_period_norm=boundary_norm,
        legal_translate_product=legal_translate_product,
        theorem_body_verified=theorem_body_verified,
        exact_target=exact_target,
        bridge_spine_preserved=bridge_spine_preserved,
        legal_yang_or_h90_object=legal_yang_or_h90_object,
        boundary_context=boundary_context,
        period156_context=period156,
        arithmetic_source=arithmetic_source,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_clause=expected_missing,
        actual_missing_clause=decision.first_missing_clause,
        source_stage_closed=source_stage_closed,
        value_closing=value_closing,
        divisor_closing=divisor_closing,
        rejected=rejected,
        conditional=conditional,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def legal_translate_rows(
    product_rows: tuple[SparseProductNormalFormRow, ...]
) -> tuple[H0TranslateCompatibilityRow, ...]:
    rows: list[H0TranslateCompatibilityRow] = []
    for product_row in product_rows:
        target = "canonical_H0" if product_row.multiplier_from_canonical == 1 else "H0_translate"
        rows.append(
            compatibility_row(
                name=f"legal_h0_translate_m{product_row.multiplier_from_canonical}_value_period156",
                target_object=target,
                output_kind="value",
                product_row=product_row,
                legal_translate_product=True,
                expected_decision="source_theorem_closed_policy_or_framing_missing",
                expected_missing="DANGER3 finite-identity/non-CM framing",
            )
        )
    return tuple(rows)


def control_rows() -> tuple[H0TranslateCompatibilityRow, ...]:
    return (
        compatibility_row(
            name="h0_translate_value_missing_boundary",
            target_object="H0_translate",
            output_kind="value",
            boundary_context=False,
            expected_decision="conditional_h0_missing_boundary_to_norm",
            expected_missing="(1-Frob_p)H0 = Norm_156(Y_507)",
        ),
        compatibility_row(
            name="h0_translate_value_missing_period156",
            target_object="H0_translate",
            output_kind="value",
            period156=False,
            expected_decision="conditional_missing_period_156_context",
            expected_missing="period-156 branch/root/telescoping context",
        ),
        compatibility_row(
            name="h0_translate_divisor_boundary_no_period_value_branch",
            target_object="H0_translate",
            output_kind="divisor-additive",
            period156=False,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        compatibility_row(
            name="h0_translate_finite_payload_without_source",
            target_object="H0_translate",
            output_kind="finite-verifier",
            arithmetic_source=False,
            expected_decision="conditional_finite_payload_without_source_theorem",
            expected_missing="challenge-legal arithmetic source theorem",
        ),
        compatibility_row(
            name="nonlegal_h0_translate_payload",
            target_object="H0_translate",
            output_kind="value",
            legal_yang_or_h90_object=False,
            expected_decision="reject_target_fails_yang_or_h90_legality",
            expected_missing="Yang/Yu legality and legal sparse H90 selector",
        ),
        compatibility_row(
            name="formal_one_coset_h_translate",
            target_object="formal_one_coset_H",
            output_kind="value",
            expected_decision="reject_illegal_or_insufficient_target",
            expected_missing="exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source",
        ),
    )


def profile_h0_translate_value_compatibility() -> H0TranslateCompatibilityPacket:
    h90 = profile_h90_value_theorem_intake()
    h0_period = profile_h0_period156_value_compatibility()
    h0_form = profile_sparse_h90_product_normal_form()
    rows = legal_translate_rows(h0_form.legal_rows) + control_rows()
    legal_rows = tuple(row for row in rows if row.legal_translate_product)
    source_closing = sum(row.source_stage_closed for row in rows)
    value_closing = sum(row.value_closing for row in rows)
    divisor_closing = sum(row.divisor_closing for row in rows)
    rejected = sum(row.rejected for row in rows)
    conditional = sum(row.conditional for row in rows)
    finite_payload = sum(row.output_kind == "finite-verifier" for row in rows)
    submission_ready = 0

    row_ok = (
        h90.row_ok
        and h0_period.row_ok
        and h0_form.row_ok
        and h0_form.support_period == 156
        and h0_form.quotient_representatives == (1, 2, 4, 8)
        and h0_form.canonical_stabilizer == (1, 16, 22)
        and h0_form.legal_rows_form_one_doubling_orbit
        and h0_form.legal_rows_are_78_over_78_products
        and h0_form.formal_one_coset_controls_rejected
        and len(rows) == 10
        and len(legal_rows) == 4
        and sum(row.target_object == "canonical_H0" for row in rows) == 1
        and sum(row.target_object == "H0_translate" for row in rows) == 8
        and all(row.boundary_equals_period_norm for row in legal_rows)
        and all(row.lifted_positive_count == 78 for row in legal_rows)
        and all(row.lifted_negative_count == 78 for row in legal_rows)
        and all(row.lifted_support == 156 for row in legal_rows)
        and source_closing == 5
        and value_closing == 4
        and divisor_closing == 1
        and rejected == 2
        and conditional == 3
        and finite_payload == 1
        and submission_ready == 0
        and all(row.ok for row in rows)
    )
    return H0TranslateCompatibilityPacket(
        h90_intake_ok=h90.row_ok,
        h0_period156_compatibility_ok=h0_period.row_ok,
        sparse_h90_normal_form_ok=h0_form.row_ok,
        support_period=h0_form.support_period,
        doubling_subgroup=h0_form.doubling_subgroup,
        canonical_stabilizer=h0_form.canonical_stabilizer,
        quotient_representatives=h0_form.quotient_representatives,
        legal_product_rows=len(h0_form.legal_rows),
        legal_products_form_one_doubling_orbit=h0_form.legal_rows_form_one_doubling_orbit,
        legal_products_are_78_over_78=h0_form.legal_rows_are_78_over_78_products,
        formal_one_coset_controls_rejected=h0_form.formal_one_coset_controls_rejected,
        compatibility_rows=rows,
        row_count=len(rows),
        legal_translate_rows=len(legal_rows),
        canonical_target_rows=sum(row.target_object == "canonical_H0" for row in rows),
        h0_translate_target_rows=sum(row.target_object == "H0_translate" for row in rows),
        source_closing_rows=source_closing,
        value_closing_rows=value_closing,
        divisor_closing_rows=divisor_closing,
        rejected_rows=rejected,
        conditional_rows=conditional,
        finite_payload_rows=finite_payload,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_value_compatibility()
    print("p25 KSY-y H0 translate value-compatibility gate")
    print("dependencies")
    print(f"  h90_intake_ok={int(profile.h90_intake_ok)}")
    print(f"  h0_period156_compatibility_ok={int(profile.h0_period156_compatibility_ok)}")
    print(f"  sparse_h90_normal_form_ok={int(profile.sparse_h90_normal_form_ok)}")
    print("legal_translate_family")
    print(f"  support_period={profile.support_period}")
    print(f"  doubling_subgroup={profile.doubling_subgroup}")
    print(f"  canonical_stabilizer={profile.canonical_stabilizer}")
    print(f"  quotient_representatives={profile.quotient_representatives}")
    print(f"  legal_product_rows={profile.legal_product_rows}")
    print(
        "  legal_products_form_one_doubling_orbit="
        f"{int(profile.legal_products_form_one_doubling_orbit)}"
    )
    print(f"  legal_products_are_78_over_78={int(profile.legal_products_are_78_over_78)}")
    print(
        "  formal_one_coset_controls_rejected="
        f"{int(profile.formal_one_coset_controls_rejected)}"
    )
    print("compatibility_rows")
    for row in profile.compatibility_rows:
        print(
            "  "
            f"{row.name}: target={row.target_object} kind={row.output_kind} "
            f"multiplier={row.multiplier_from_canonical} "
            f"legal_product={int(row.legal_translate_product)} "
            f"lift=+{row.lifted_positive_count}/-{row.lifted_negative_count} "
            f"support={row.lifted_support} boundary={int(row.boundary_equals_period_norm)} "
            f"period156={int(row.period156_context)} source={int(row.arithmetic_source)} "
            f"legal={int(row.legal_yang_or_h90_object)} "
            f"decision={row.actual_decision} closed={int(row.source_stage_closed)} "
            f"missing={row.actual_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  legal_translate_rows={profile.legal_translate_rows}")
    print(f"  canonical_target_rows={profile.canonical_target_rows}")
    print(f"  h0_translate_target_rows={profile.h0_translate_target_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  value_closing_rows={profile.value_closing_rows}")
    print(f"  divisor_closing_rows={profile.divisor_closing_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  finite_payload_rows={profile.finite_payload_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  H0_translate_means_the_four_legal_78_over_78_products_only=1")
    print("  noncanonical_legal_translates_route_like_canonical_H0=1")
    print("  missing_boundary_or_period156_context_stays_conditional=1")
    print("  formal_or_nonlegal_H_translates_are_rejected=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_value_compatibility_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate value-compatibility regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
