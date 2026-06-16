#!/usr/bin/env python3
"""Source-theorem obligation packet for legal H0 translates.

Koo-Shin 6.2 now certifies the compact conductor-39 source, and the H0
translate gates certify the four legal support-156 targets.  This packet keeps
those two positives separated from the still-missing theorem: an exact
finite-field value identity or divisor/additive identity for one legal H0
product, with the required Hilbert-90 boundary and period discipline.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_translate_value_compatibility_gate import (
    H0TranslateCompatibilityRow,
    profile_h0_translate_value_compatibility,
)
from p25_ksy_y_h90_value_theorem_intake_gate import (
    H90ValueTheoremClaim,
    classify_claim,
)
from p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_gate import (
    profile_koo_shin_theorem62_conductor39_unit,
)


@dataclass(frozen=True)
class H0TranslateSourceObligationRow:
    name: str
    source_anchor: str
    target_object: str
    output_kind: str
    multiplier_from_canonical: int
    legal_translate_product: bool
    theorem_body_verified: bool
    exact_target: bool
    legal_yang_or_h90_object: bool
    boundary_context: bool
    period156_context: bool
    arithmetic_source: bool
    expected_decision: str
    actual_decision: str
    expected_missing_clause: str
    actual_missing_clause: str
    source_certified_only: bool
    live_target_identified: bool
    source_theorem_closes: bool
    rejected: bool
    conditional: bool
    ok: bool


@dataclass(frozen=True)
class H0TranslateSourceObligationPacket:
    h0_translate_compatibility_ok: bool
    koo_shin_62_conductor39_unit_ok: bool
    legal_product_rows: int
    noncanonical_legal_translate_rows: int
    canonical_legal_rows: int
    legal_products_are_78_over_78: bool
    support_period: int
    source_rows: tuple[H0TranslateSourceObligationRow, ...]
    row_count: int
    source_certified_only_rows: int
    live_target_rows: int
    source_theorem_closing_rows: int
    rejected_rows: int
    conditional_rows: int
    policy_or_framing_missing_rows: int
    submission_ready_rows: int
    row_ok: bool


def h90_claim(
    *,
    name: str,
    target_object: str,
    output_kind: str,
    theorem_body: bool = True,
    exact_target: bool = True,
    legal_yang_or_h90: bool = True,
    boundary_context: bool = True,
    finite_or_divisor: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H90ValueTheoremClaim:
    return H90ValueTheoremClaim(
        name=name,
        theorem_body_verified=theorem_body,
        target_object=target_object,
        output_kind=output_kind,
        exact_target=exact_target,
        bridge_spine_preserved=True,
        legal_yang_or_h90_object=legal_yang_or_h90,
        boundary_or_period_norm_context=boundary_context,
        finite_field_identity_or_divisor=finite_or_divisor,
        period_156_context=period156,
        arithmetic_source_theorem=arithmetic_source,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def h90_row(
    *,
    name: str,
    source_anchor: str,
    source_row: H0TranslateCompatibilityRow,
    output_kind: str,
    expected_decision: str,
    expected_missing: str,
    theorem_body: bool = True,
    exact_target: bool = True,
    legal_yang_or_h90: bool = True,
    boundary_context: bool = True,
    finite_or_divisor: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H0TranslateSourceObligationRow:
    decision = classify_claim(
        h90_claim(
            name=name,
            target_object=source_row.target_object,
            output_kind=output_kind,
            theorem_body=theorem_body,
            exact_target=exact_target,
            legal_yang_or_h90=legal_yang_or_h90,
            boundary_context=boundary_context,
            finite_or_divisor=finite_or_divisor,
            period156=period156,
            arithmetic_source=arithmetic_source,
        )
    )
    rejected = decision.decision.startswith("reject_")
    conditional = decision.decision.startswith(("conditional_", "live_target_identified_"))
    return H0TranslateSourceObligationRow(
        name=name,
        source_anchor=source_anchor,
        target_object=source_row.target_object,
        output_kind=output_kind,
        multiplier_from_canonical=source_row.multiplier_from_canonical,
        legal_translate_product=source_row.legal_translate_product,
        theorem_body_verified=theorem_body,
        exact_target=exact_target,
        legal_yang_or_h90_object=legal_yang_or_h90,
        boundary_context=boundary_context,
        period156_context=period156,
        arithmetic_source=arithmetic_source,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_clause=expected_missing,
        actual_missing_clause=decision.first_missing_clause,
        source_certified_only=False,
        live_target_identified=decision.live_target_identified,
        source_theorem_closes=decision.theorem_source_closed,
        rejected=rejected,
        conditional=conditional,
        ok=(
            decision.decision == expected_decision
            and decision.first_missing_clause == expected_missing
            and (source_row.legal_translate_product or rejected)
        ),
    )


def certified_only_row(
    *,
    name: str,
    source_anchor: str,
    actual_decision: str,
    actual_missing: str,
) -> H0TranslateSourceObligationRow:
    return H0TranslateSourceObligationRow(
        name=name,
        source_anchor=source_anchor,
        target_object="conductor39_W",
        output_kind="source-certification",
        multiplier_from_canonical=0,
        legal_translate_product=False,
        theorem_body_verified=True,
        exact_target=True,
        legal_yang_or_h90_object=True,
        boundary_context=False,
        period156_context=False,
        arithmetic_source=True,
        expected_decision=actual_decision,
        actual_decision=actual_decision,
        expected_missing_clause=actual_missing,
        actual_missing_clause=actual_missing,
        source_certified_only=True,
        live_target_identified=False,
        source_theorem_closes=False,
        rejected=False,
        conditional=True,
        ok=True,
    )


def source_rows(
    legal_rows: tuple[H0TranslateCompatibilityRow, ...],
    nonlegal_row: H0TranslateCompatibilityRow,
    formal_row: H0TranslateCompatibilityRow,
    theorem62,
) -> tuple[H0TranslateSourceObligationRow, ...]:
    representative_translate = next(
        row
        for row in legal_rows
        if row.target_object == "H0_translate" and row.multiplier_from_canonical == 2
    )
    ks62_period_norm = next(row for row in theorem62.route_rows if row.name == "w_then_yang_distribution_lift")
    return (
        certified_only_row(
            name="koo_shin_62_certifies_w_source_only",
            source_anchor="Koo-Shin 2010 Theorem 6.2 plus Yang distribution",
            actual_decision=ks62_period_norm.decision,
            actual_missing=ks62_period_norm.first_missing_clause,
        ),
        h90_row(
            name="legal_h0_translate_boundary_only",
            source_anchor="legal H0 translate plus Hilbert-90 boundary",
            source_row=representative_translate,
            output_kind="source-object",
            finite_or_divisor=False,
            expected_decision="live_target_identified_value_or_divisor_theorem_missing",
            expected_missing="finite-field value identity or divisor/additive theorem",
        ),
        h90_row(
            name="legal_h0_translate_value_missing_period156",
            source_anchor="candidate finite value theorem without branch control",
            source_row=representative_translate,
            output_kind="value",
            period156=False,
            expected_decision="conditional_missing_period_156_context",
            expected_missing="period-156 branch/root/telescoping context",
        ),
        h90_row(
            name="legal_h0_translate_value_period156",
            source_anchor="candidate finite value theorem with branch control",
            source_row=representative_translate,
            output_kind="value",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        h90_row(
            name="legal_h0_translate_divisor_boundary",
            source_anchor="candidate divisor/additive theorem for legal H0 translate",
            source_row=representative_translate,
            output_kind="divisor-additive",
            period156=False,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        h90_row(
            name="legal_h0_translate_finite_payload_no_source",
            source_anchor="finite verifier payload without arithmetic theorem",
            source_row=representative_translate,
            output_kind="finite-verifier",
            arithmetic_source=False,
            expected_decision="conditional_finite_payload_without_source_theorem",
            expected_missing="challenge-legal arithmetic source theorem",
        ),
        h90_row(
            name="nonlegal_h0_translate_source_claim",
            source_anchor="nonlegal H0 translate control",
            source_row=nonlegal_row,
            output_kind="value",
            legal_yang_or_h90=False,
            expected_decision="reject_target_fails_yang_or_h90_legality",
            expected_missing="Yang/Yu legality and legal sparse H90 selector",
        ),
        h90_row(
            name="formal_one_coset_h_source_claim",
            source_anchor="formal one-coset H control",
            source_row=formal_row,
            output_kind="value",
            expected_decision="reject_illegal_or_insufficient_target",
            expected_missing="exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source",
        ),
    )


def profile_h0_translate_source_obligation() -> H0TranslateSourceObligationPacket:
    translate = profile_h0_translate_value_compatibility()
    theorem62 = profile_koo_shin_theorem62_conductor39_unit()
    legal_rows = tuple(row for row in translate.compatibility_rows if row.legal_translate_product)
    nonlegal_row = next(row for row in translate.compatibility_rows if row.name == "nonlegal_h0_translate_payload")
    formal_row = next(row for row in translate.compatibility_rows if row.name == "formal_one_coset_h_translate")
    rows = source_rows(legal_rows, nonlegal_row, formal_row, theorem62)
    source_certified_only = sum(row.source_certified_only for row in rows)
    live_target = sum(row.live_target_identified for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    rejected = sum(row.rejected for row in rows)
    conditional = sum(row.conditional for row in rows)
    policy_missing = sum(row.actual_decision == "source_theorem_closed_policy_or_framing_missing" for row in rows)
    submission_ready = 0
    row_ok = (
        translate.row_ok
        and theorem62.row_ok
        and translate.support_period == 156
        and len(legal_rows) == 4
        and sum(row.target_object == "canonical_H0" for row in legal_rows) == 1
        and sum(row.target_object == "H0_translate" for row in legal_rows) == 3
        and translate.legal_products_are_78_over_78
        and len(rows) == 8
        and source_certified_only == 1
        and live_target == 5
        and source_closing == 2
        and rejected == 2
        and conditional == 4
        and policy_missing == 2
        and submission_ready == 0
        and tuple(row.actual_decision for row in rows)
        == (
            "period_norm_source_certified_theorem_missing",
            "live_target_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_finite_payload_without_source_theorem",
            "reject_target_fails_yang_or_h90_legality",
            "reject_illegal_or_insufficient_target",
        )
        and all(row.ok for row in rows)
    )
    return H0TranslateSourceObligationPacket(
        h0_translate_compatibility_ok=translate.row_ok,
        koo_shin_62_conductor39_unit_ok=theorem62.row_ok,
        legal_product_rows=len(legal_rows),
        noncanonical_legal_translate_rows=sum(row.target_object == "H0_translate" for row in legal_rows),
        canonical_legal_rows=sum(row.target_object == "canonical_H0" for row in legal_rows),
        legal_products_are_78_over_78=translate.legal_products_are_78_over_78,
        support_period=translate.support_period,
        source_rows=rows,
        row_count=len(rows),
        source_certified_only_rows=source_certified_only,
        live_target_rows=live_target,
        source_theorem_closing_rows=source_closing,
        rejected_rows=rejected,
        conditional_rows=conditional,
        policy_or_framing_missing_rows=policy_missing,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_source_obligation()
    print("p25 KSY-y H0 translate source-obligation gate")
    print("dependencies")
    print(f"  h0_translate_compatibility_ok={int(profile.h0_translate_compatibility_ok)}")
    print(f"  koo_shin_62_conductor39_unit_ok={int(profile.koo_shin_62_conductor39_unit_ok)}")
    print("legal_target_family")
    print(f"  support_period={profile.support_period}")
    print(f"  legal_product_rows={profile.legal_product_rows}")
    print(f"  canonical_legal_rows={profile.canonical_legal_rows}")
    print(f"  noncanonical_legal_translate_rows={profile.noncanonical_legal_translate_rows}")
    print(f"  legal_products_are_78_over_78={int(profile.legal_products_are_78_over_78)}")
    print("source_rows")
    for row in profile.source_rows:
        print(
            "  "
            f"{row.name}: anchor={row.source_anchor} target={row.target_object} "
            f"kind={row.output_kind} multiplier={row.multiplier_from_canonical} "
            f"legal={int(row.legal_translate_product)} boundary={int(row.boundary_context)} "
            f"period156={int(row.period156_context)} source={int(row.arithmetic_source)} "
            f"decision={row.actual_decision} source_only={int(row.source_certified_only)} "
            f"live={int(row.live_target_identified)} closes={int(row.source_theorem_closes)} "
            f"missing={row.actual_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  live_target_rows={profile.live_target_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  policy_or_framing_missing_rows={profile.policy_or_framing_missing_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  Koo_Shin_6_2_certifies_the_conductor39_source_but_not_the_H0_value_theorem=1")
    print("  boundary_only_H0_translate_claims_still_need_value_or_divisor_theorem=1")
    print("  value_claims_need_period156_context=1")
    print("  value_or_divisor_theorem_for_any_legal_H0_translate_closes_source_stage=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_source_obligation_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate source-obligation regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
