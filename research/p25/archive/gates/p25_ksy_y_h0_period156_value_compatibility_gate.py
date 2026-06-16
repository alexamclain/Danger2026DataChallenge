#!/usr/bin/env python3
"""Period-156 compatibility packet for H0/Y507 value-theorem claims.

The twisted-descent packet leaves one live value route: a ratio/Hilbert-90
theorem with period-156 context.  This gate pins down the H0/Y507 side of that
claim.  H0 is useful only when its boundary is the period norm of Y_507; value
claims need support-period branch context, while divisor/additive identities
can close the source stage without a multiplicative value branch.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h90_value_theorem_intake_gate import (
    H90ValueTheoremClaim,
    classify_claim,
    profile_h90_value_theorem_intake,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)
from p25_ksy_y_yang_y507_modular_period_certificate_gate import (
    profile_yang_y507_modular_period_certificate,
)


@dataclass(frozen=True)
class H0Period156CompatibilityRow:
    name: str
    target_object: str
    output_kind: str
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
class H0Period156CompatibilityPacket:
    h90_intake_ok: bool
    y507_period_certificate_ok: bool
    sparse_h90_normal_form_ok: bool
    y507_minimum_doubling_period: int
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    h0_support_period: int
    canonical_h0_positive_count: int
    canonical_h0_negative_count: int
    canonical_h0_boundary_equals_norm: bool
    legal_h0_orbit_count: int
    legal_h0_stabilizer_size: int
    compatibility_rows: tuple[H0Period156CompatibilityRow, ...]
    row_count: int
    source_closing_rows: int
    value_closing_rows: int
    divisor_closing_rows: int
    rejected_rows: int
    conditional_rows: int
    finite_payload_rows: int
    row_ok: bool


def make_claim(
    *,
    name: str,
    target_object: str,
    output_kind: str,
    boundary_context: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H90ValueTheoremClaim:
    return H90ValueTheoremClaim(
        name=name,
        theorem_body_verified=True,
        target_object=target_object,
        output_kind=output_kind,
        exact_target=True,
        bridge_spine_preserved=True,
        legal_yang_or_h90_object=True,
        boundary_or_period_norm_context=boundary_context,
        finite_field_identity_or_divisor=output_kind != "finite-verifier",
        period_156_context=period156,
        arithmetic_source_theorem=arithmetic_source,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def row(
    *,
    name: str,
    target_object: str,
    output_kind: str,
    expected_decision: str,
    expected_missing: str,
    boundary_context: bool = True,
    period156: bool = True,
    arithmetic_source: bool = True,
) -> H0Period156CompatibilityRow:
    claim = make_claim(
        name=name,
        target_object=target_object,
        output_kind=output_kind,
        boundary_context=boundary_context,
        period156=period156,
        arithmetic_source=arithmetic_source,
    )
    decision = classify_claim(claim)
    source_closed = decision.theorem_source_closed
    value_closing = source_closed and output_kind == "value"
    divisor_closing = source_closed and output_kind == "divisor-additive"
    rejected = decision.decision.startswith("reject_")
    conditional = decision.decision.startswith(("conditional_", "live_target_identified_"))
    return H0Period156CompatibilityRow(
        name=name,
        target_object=target_object,
        output_kind=output_kind,
        boundary_context=boundary_context,
        period156_context=period156,
        arithmetic_source=arithmetic_source,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_clause=expected_missing,
        actual_missing_clause=decision.first_missing_clause,
        source_stage_closed=source_closed,
        value_closing=value_closing,
        divisor_closing=divisor_closing,
        rejected=rejected,
        conditional=conditional,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def compatibility_rows() -> tuple[H0Period156CompatibilityRow, ...]:
    return (
        row(
            name="canonical_h0_value_with_boundary_period156",
            target_object="canonical_H0",
            output_kind="value",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        row(
            name="canonical_h0_value_missing_boundary",
            target_object="canonical_H0",
            output_kind="value",
            boundary_context=False,
            expected_decision="conditional_h0_missing_boundary_to_norm",
            expected_missing="(1-Frob_p)H0 = Norm_156(Y_507)",
        ),
        row(
            name="canonical_h0_value_missing_period156",
            target_object="canonical_H0",
            output_kind="value",
            period156=False,
            expected_decision="conditional_missing_period_156_context",
            expected_missing="period-156 branch/root/telescoping context",
        ),
        row(
            name="canonical_h0_divisor_boundary_no_period_value_branch",
            target_object="canonical_H0",
            output_kind="divisor-additive",
            period156=False,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        row(
            name="y507_value_with_period156",
            target_object="Y_507",
            output_kind="value",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        row(
            name="formal_one_coset_h_value",
            target_object="formal_one_coset_H",
            output_kind="value",
            expected_decision="reject_illegal_or_insufficient_target",
            expected_missing="exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source",
        ),
        row(
            name="ambient_780_value",
            target_object="ambient_780_value",
            output_kind="value",
            expected_decision="reject_illegal_or_insufficient_target",
            expected_missing="exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source",
        ),
        row(
            name="h0_finite_payload_without_source",
            target_object="canonical_H0",
            output_kind="finite-verifier",
            arithmetic_source=False,
            expected_decision="conditional_finite_payload_without_source_theorem",
            expected_missing="challenge-legal arithmetic source theorem",
        ),
        row(
            name="h0_finite_identity_without_arithmetic_source",
            target_object="canonical_H0",
            output_kind="value",
            arithmetic_source=False,
            expected_decision="conditional_finite_identity_without_arithmetic_source",
            expected_missing="challenge-legal arithmetic source theorem",
        ),
    )


def profile_h0_period156_value_compatibility() -> H0Period156CompatibilityPacket:
    h90 = profile_h90_value_theorem_intake()
    y_period = profile_yang_y507_modular_period_certificate()
    h0_form = profile_sparse_h90_product_normal_form()
    rows = compatibility_rows()
    source_closing = sum(row.source_stage_closed for row in rows)
    value_closing = sum(row.value_closing for row in rows)
    divisor_closing = sum(row.divisor_closing for row in rows)
    rejected = sum(row.rejected for row in rows)
    conditional = sum(row.conditional for row in rows)
    finite_payload = sum(row.output_kind == "finite-verifier" for row in rows)
    row_ok = (
        h90.row_ok
        and y_period.row_ok
        and h0_form.row_ok
        and y_period.minimum_doubling_period == 156
        and y_period.support_period_root_gcd_fp_star == 1
        and y_period.ambient_period_root_gcd_fp_star == 11
        and h0_form.support_period == 156
        and h0_form.canonical_positive_lift_count == 78
        and h0_form.canonical_negative_lift_count == 78
        and h0_form.legal_rows[0].boundary_equals_period_norm
        and len(h0_form.legal_rows) == 4
        and len(h0_form.canonical_stabilizer) == 3
        and len(rows) == 9
        and source_closing == 3
        and value_closing == 2
        and divisor_closing == 1
        and rejected == 2
        and conditional == 4
        and finite_payload == 1
        and all(row.ok for row in rows)
    )
    return H0Period156CompatibilityPacket(
        h90_intake_ok=h90.row_ok,
        y507_period_certificate_ok=y_period.row_ok,
        sparse_h90_normal_form_ok=h0_form.row_ok,
        y507_minimum_doubling_period=y_period.minimum_doubling_period,
        support_period_root_gcd=y_period.support_period_root_gcd_fp_star,
        ambient_period_root_gcd=y_period.ambient_period_root_gcd_fp_star,
        h0_support_period=h0_form.support_period,
        canonical_h0_positive_count=h0_form.canonical_positive_lift_count,
        canonical_h0_negative_count=h0_form.canonical_negative_lift_count,
        canonical_h0_boundary_equals_norm=h0_form.legal_rows[0].boundary_equals_period_norm,
        legal_h0_orbit_count=len(h0_form.legal_rows),
        legal_h0_stabilizer_size=len(h0_form.canonical_stabilizer),
        compatibility_rows=rows,
        row_count=len(rows),
        source_closing_rows=source_closing,
        value_closing_rows=value_closing,
        divisor_closing_rows=divisor_closing,
        rejected_rows=rejected,
        conditional_rows=conditional,
        finite_payload_rows=finite_payload,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_period156_value_compatibility()
    print("p25 KSY-y H0/Y507 period-156 value-compatibility gate")
    print("dependencies")
    print(f"  h90_intake_ok={int(profile.h90_intake_ok)}")
    print(f"  y507_period_certificate_ok={int(profile.y507_period_certificate_ok)}")
    print(f"  sparse_h90_normal_form_ok={int(profile.sparse_h90_normal_form_ok)}")
    print("period_and_h0")
    print(f"  y507_minimum_doubling_period={profile.y507_minimum_doubling_period}")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print(f"  h0_support_period={profile.h0_support_period}")
    print(f"  canonical_h0_positive_count={profile.canonical_h0_positive_count}")
    print(f"  canonical_h0_negative_count={profile.canonical_h0_negative_count}")
    print(f"  canonical_h0_boundary_equals_norm={int(profile.canonical_h0_boundary_equals_norm)}")
    print(f"  legal_h0_orbit_count={profile.legal_h0_orbit_count}")
    print(f"  legal_h0_stabilizer_size={profile.legal_h0_stabilizer_size}")
    print("compatibility_rows")
    for row_profile in profile.compatibility_rows:
        print(
            "  "
            f"{row_profile.name}: target={row_profile.target_object} kind={row_profile.output_kind} "
            f"boundary={int(row_profile.boundary_context)} "
            f"period156={int(row_profile.period156_context)} "
            f"source={int(row_profile.arithmetic_source)} "
            f"decision={row_profile.actual_decision} "
            f"closed={int(row_profile.source_stage_closed)} "
            f"value={int(row_profile.value_closing)} "
            f"divisor={int(row_profile.divisor_closing)} "
            f"missing={row_profile.actual_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  value_closing_rows={profile.value_closing_rows}")
    print(f"  divisor_closing_rows={profile.divisor_closing_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  finite_payload_rows={profile.finite_payload_rows}")
    print("interpretation")
    print("  H0_value_claims_need_boundary_to_Norm156_Y507_and_period156_context=1")
    print("  H0_divisor_additive_identity_closes_source_without_value_branch=1")
    print("  formal_one_coset_and_ambient780_H_claims_are_rejected=1")
    print("  source_closure_still_needs_DANGER3_framing_extraction_and_vpp=1")
    print(f"ksy_y_h0_period156_value_compatibility_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0/Y507 period-156 compatibility regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
