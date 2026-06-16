#!/usr/bin/env python3
"""Smoke-test the expert-query packet against local answer-intake classifiers.

The expert-query packet names ten questions.  Nine can be tested now as
candidate claims or arithmetic guardrails.  The tenth, a verified p25 triple,
is deliberately not smoke-tested with placeholders; it requires concrete
`A,x0` values and official DANGER3 `vpp.py` verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_conductor39_expert_query_packet_gate import (
    P,
    profile_expert_query_packet,
)
from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    Conductor39SourceTheoremClaim,
    classify_claim as classify_conductor39_claim,
)
from p25_ksy_y_h90_value_theorem_intake_gate import (
    H90ValueTheoremClaim,
    classify_claim as classify_h90_claim,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    classify_claim as classify_x1_claim,
)


@dataclass(frozen=True)
class ExpertAnswerSmokeRow:
    name: str
    source_query_row: str
    route_family: str
    expected_decision: str
    actual_decision: str
    expected_missing_or_falsifier: str
    actual_missing_or_falsifier: str
    source_stage_closed: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    executed_now: bool
    placeholder_requires_concrete_values: bool
    ok: bool


@dataclass(frozen=True)
class ExpertAnswerSmokeProfile:
    expert_query_packet_ok: bool
    smoke_rows: tuple[ExpertAnswerSmokeRow, ...]
    smoke_row_count: int
    executed_rows: int
    source_closing_rows: int
    downstream_rows: int
    guardrail_rows: int
    placeholder_rows: int
    submission_ready_rows: int
    p_order_mod39: int
    sqrt_minus39_in_fp: bool
    period156_unique_branch: bool
    ambient780_mu11: bool
    row_ok: bool


def conductor39_claim(
    *,
    name: str,
    source_object: str = "U_chi",
    output_kind: str = "divisor-additive",
    finite_or_divisor: bool = True,
    period156: bool = True,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
    projection_only: bool = False,
) -> Conductor39SourceTheoremClaim:
    return Conductor39SourceTheoremClaim(
        name=name,
        theorem_body_verified=True,
        source_object=source_object,
        emits_conductor39_object=not projection_only,
        preserves_mixed_tensor=not projection_only,
        yang_yu_legal_unit=not projection_only,
        sparse_formal_gauge_only=False,
        proper_axis_or_projection_only=projection_only,
        additive_separated=False,
        yang_distribution_to_507=not projection_only,
        frobenius_or_hilbert90_descent=not projection_only,
        output_kind=output_kind,
        finite_field_identity_or_divisor_theorem=finite_or_divisor,
        period_156_context=period156,
        danger3_framing=danger3,
        extraction_to_A_x0=extraction,
        concrete_vpp_verified_triple=vpp,
    )


def h90_claim(
    *,
    name: str,
    target_object: str,
    output_kind: str = "divisor-additive",
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> H90ValueTheoremClaim:
    return H90ValueTheoremClaim(
        name=name,
        theorem_body_verified=True,
        target_object=target_object,
        output_kind=output_kind,
        exact_target=True,
        bridge_spine_preserved=True,
        legal_yang_or_h90_object=True,
        boundary_or_period_norm_context=True,
        finite_field_identity_or_divisor=True,
        period_156_context=True,
        arithmetic_source_theorem=True,
        danger3_framing=danger3,
        extraction_to_A_x0=extraction,
        concrete_vpp_verified_triple=vpp,
    )


def x1_claim() -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name="expert_x1_8112_to_x16",
        theorem_body_verified=True,
        odd_payload_object="Y_507",
        exact_p25_specialization=True,
        odd_level_value_or_divisor=True,
        fiber_product_or_modular_correspondence=True,
        preserves_j_gluing=True,
        x16_surface_relation=True,
        emits_x16_y=True,
        emits_model_root_or_xp16=True,
        emits_halving_chain_or_x0=False,
        danger3_framing=True,
        concrete_vpp_verified_triple=False,
    )


def conductor39_row(
    name: str,
    source_query_row: str,
    claim: Conductor39SourceTheoremClaim,
    expected_decision: str,
    expected_missing: str,
    route_family: str,
) -> ExpertAnswerSmokeRow:
    decision = classify_conductor39_claim(claim)
    return ExpertAnswerSmokeRow(
        name=name,
        source_query_row=source_query_row,
        route_family=route_family,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_or_falsifier=expected_missing,
        actual_missing_or_falsifier=decision.first_missing_clause,
        source_stage_closed=decision.theorem_source_closed,
        danger3_unblocked=decision.danger3_route_unblocked,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        executed_now=True,
        placeholder_requires_concrete_values=False,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def h90_row(
    name: str,
    source_query_row: str,
    claim: H90ValueTheoremClaim,
    expected_decision: str,
    expected_missing: str,
    route_family: str,
) -> ExpertAnswerSmokeRow:
    decision = classify_h90_claim(claim)
    return ExpertAnswerSmokeRow(
        name=name,
        source_query_row=source_query_row,
        route_family=route_family,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_or_falsifier=expected_missing,
        actual_missing_or_falsifier=decision.first_missing_clause,
        source_stage_closed=decision.theorem_source_closed,
        danger3_unblocked=decision.danger3_route_unblocked,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        executed_now=True,
        placeholder_requires_concrete_values=False,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def arithmetic_guardrail_row(
    name: str,
    source_query_row: str,
    expected_decision: str,
    expected_falsifier: str,
    falsifier_ok: bool,
) -> ExpertAnswerSmokeRow:
    return ExpertAnswerSmokeRow(
        name=name,
        source_query_row=source_query_row,
        route_family="arithmetic_guardrail",
        expected_decision=expected_decision,
        actual_decision=expected_decision if falsifier_ok else "guardrail_failed",
        expected_missing_or_falsifier=expected_falsifier,
        actual_missing_or_falsifier=expected_falsifier if falsifier_ok else "arithmetic check failed",
        source_stage_closed=False,
        danger3_unblocked=False,
        extraction_ready=False,
        submission_ready=False,
        executed_now=True,
        placeholder_requires_concrete_values=False,
        ok=falsifier_ok,
    )


def smoke_rows() -> tuple[ExpertAnswerSmokeRow, ...]:
    x1_decision = classify_x1_claim(x1_claim())
    order39 = multiplicative_order_mod(P % 39, 39)
    sqrt_minus39_in_fp = pow((-39) % P, (P - 1) // 2, P) == 1
    return (
        conductor39_row(
            "smoke_Uchi_divisor_identity",
            "finite_Uchi_or_W_value_or_divisor_identity",
            conductor39_claim(name="expert_U_chi_theorem"),
            "source_theorem_closed_policy_or_framing_missing",
            "DANGER3 finite-identity/non-CM framing",
            "conductor39_source",
        ),
        conductor39_row(
            "smoke_W_degree6_value_descent",
            "degree6_cyclotomic_norm_descent",
            conductor39_claim(name="expert_W_theorem", source_object="W", output_kind="value"),
            "source_theorem_closed_policy_or_framing_missing",
            "DANGER3 finite-identity/non-CM framing",
            "conductor39_source",
        ),
        h90_row(
            "smoke_canonical_H0_ratio_identity",
            "hilbert90_ratio_or_H0_value_identity",
            h90_claim(name="expert_canonical_H0_theorem", target_object="canonical_H0"),
            "source_theorem_closed_policy_or_framing_missing",
            "DANGER3 finite-identity/non-CM framing",
            "h90_y507",
        ),
        h90_row(
            "smoke_Y507_period156_value_identity",
            "period156_branch_control",
            h90_claim(name="expert_Y_507_theorem", target_object="Y_507", output_kind="value"),
            "source_theorem_closed_policy_or_framing_missing",
            "DANGER3 finite-identity/non-CM framing",
            "h90_y507",
        ),
        conductor39_row(
            "smoke_policy_yes_extraction_missing",
            "danger3_finite_identity_policy",
            conductor39_claim(name="expert_policy_yes", danger3=True, extraction=False),
            "danger3_unblocked_extraction_missing",
            "extraction algorithm for concrete (A, x0)",
            "danger3_policy",
        ),
        ExpertAnswerSmokeRow(
            name="smoke_x1_8112_surface_halving_missing",
            source_query_row="x1_8112_to_x16_extraction",
            route_family="x1_8112_x16",
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            actual_decision=x1_decision.decision,
            expected_missing_or_falsifier="valid halving chain from xP16 to concrete x0",
            actual_missing_or_falsifier=x1_decision.first_missing_clause,
            source_stage_closed=False,
            danger3_unblocked=True,
            extraction_ready=x1_decision.extraction_ready,
            submission_ready=x1_decision.submission_ready,
            executed_now=True,
            placeholder_requires_concrete_values=False,
            ok=(
                x1_decision.decision == "x16_surface_reached_halving_or_vpp_missing"
                and x1_decision.first_missing_clause == "valid halving chain from xP16 to concrete x0"
            ),
        ),
        arithmetic_guardrail_row(
            "smoke_reject_direct_Fp_order39_root",
            "reject_direct_Fp_order39_root",
            "reject_direct_Fp_order39_root_shortcut",
            "ord_39(p)=6",
            order39 == 6,
        ),
        arithmetic_guardrail_row(
            "smoke_reject_sqrt_minus39_scalar",
            "reject_sqrt_minus39_scalar",
            "reject_sqrt_minus39_scalar_shortcut",
            "(-39/p)=-1",
            not sqrt_minus39_in_fp,
        ),
        conductor39_row(
            "smoke_reject_generator_or_projection_only",
            "reject_generator_or_projection_only",
            conductor39_claim(name="expert_projection_only", source_object="projection", projection_only=True),
            "reject_loses_mixed_tensor",
            "mixed chi_3 tensor chi_13 source on X_1(39)",
            "projection_guardrail",
        ),
        ExpertAnswerSmokeRow(
            name="verified_pomerance_triple_requires_real_values",
            source_query_row="verified_pomerance_triple",
            route_family="official_vpp_boundary",
            expected_decision="not_smoked_without_concrete_A_x0",
            actual_decision="not_smoked_without_concrete_A_x0",
            expected_missing_or_falsifier="official vpp.py verification",
            actual_missing_or_falsifier="official vpp.py verification",
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            executed_now=False,
            placeholder_requires_concrete_values=True,
            ok=True,
        ),
    )


def multiplicative_order_mod(n: int, modulus: int) -> int:
    if gcd(n, modulus) != 1:
        raise ValueError("order is defined only for units")
    value = 1
    for order in range(1, modulus + 1):
        value = (value * n) % modulus
        if value == 1:
            return order
    raise ValueError("order search exhausted")


def profile_expert_answer_smoke() -> ExpertAnswerSmokeProfile:
    expert = profile_expert_query_packet()
    rows = smoke_rows()
    executed = sum(row.executed_now for row in rows)
    source_closing = sum(row.source_stage_closed for row in rows)
    downstream = sum(row.route_family in {"danger3_policy", "x1_8112_x16"} for row in rows)
    guardrails = sum(row.route_family in {"arithmetic_guardrail", "projection_guardrail"} for row in rows)
    placeholders = sum(row.placeholder_requires_concrete_values for row in rows)
    submissions = sum(row.submission_ready for row in rows)
    p_order_mod39 = multiplicative_order_mod(P % 39, 39)
    sqrt_minus39_in_fp = pow((-39) % P, (P - 1) // 2, P) == 1
    period156_unique = gcd(4**156 - 1, P - 1) == 1
    ambient780_mu11 = gcd(4**780 - 1, P - 1) == 11
    row_ok = (
        expert.row_ok
        and len(rows) == 10
        and executed == 9
        and source_closing == 5
        and downstream == 2
        and guardrails == 3
        and placeholders == 1
        and submissions == 0
        and p_order_mod39 == 6
        and not sqrt_minus39_in_fp
        and period156_unique
        and ambient780_mu11
        and all(row.ok for row in rows)
    )
    return ExpertAnswerSmokeProfile(
        expert_query_packet_ok=expert.row_ok,
        smoke_rows=rows,
        smoke_row_count=len(rows),
        executed_rows=executed,
        source_closing_rows=source_closing,
        downstream_rows=downstream,
        guardrail_rows=guardrails,
        placeholder_rows=placeholders,
        submission_ready_rows=submissions,
        p_order_mod39=p_order_mod39,
        sqrt_minus39_in_fp=sqrt_minus39_in_fp,
        period156_unique_branch=period156_unique,
        ambient780_mu11=ambient780_mu11,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_expert_answer_smoke()
    print("p25 KSY-y conductor-39 expert-answer smoke gate")
    print("dependencies")
    print(f"  expert_query_packet_ok={int(profile.expert_query_packet_ok)}")
    print("arithmetic")
    print(f"  p_order_mod39={profile.p_order_mod39}")
    print(f"  sqrt_minus39_in_fp={int(profile.sqrt_minus39_in_fp)}")
    print(f"  period156_unique_branch={int(profile.period156_unique_branch)}")
    print(f"  ambient780_mu11={int(profile.ambient780_mu11)}")
    print("smoke_rows")
    for row in profile.smoke_rows:
        print(
            "  "
            f"{row.name}: source={row.source_query_row} family={row.route_family} "
            f"expected={row.expected_decision} actual={row.actual_decision} "
            f"closed={int(row.source_stage_closed)} danger3={int(row.danger3_unblocked)} "
            f"extract={int(row.extraction_ready)} submission={int(row.submission_ready)} "
            f"executed={int(row.executed_now)} placeholder={int(row.placeholder_requires_concrete_values)}"
        )
        print(f"    missing_or_falsifier={row.actual_missing_or_falsifier}")
    print("counts")
    print(f"  smoke_row_count={profile.smoke_row_count}")
    print(f"  executed_rows={profile.executed_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  downstream_rows={profile.downstream_rows}")
    print(f"  guardrail_rows={profile.guardrail_rows}")
    print(f"  placeholder_rows={profile.placeholder_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  four_expert_yes_shapes_route_to_source_closure=1")
    print("  downstream_yes_shapes_route_to_extraction_or_halving_debt=1")
    print("  verified_triple_row_is_not_smoked_without_concrete_values=1")
    print(f"ksy_y_conductor39_expert_answer_smoke_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 expert-answer smoke regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
