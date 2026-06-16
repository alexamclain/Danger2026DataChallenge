#!/usr/bin/env python3
"""H0 X_1(8112) bridge-component claim intake.

The H0 source theorem lane now has exact product fixtures and source-stage
classifiers.  This intake is for the next downstream claim shape: someone may
hand us level-16 and level-507 torsion data, or an order-8112 point, and say it
extracts the H0/Y507 value into the DANGER3 X_1(16) surface.

This gate rejects unglued components and records the normalized projections
that an order-8112 bridge must use:

    P16  = [1521]R
    Q507 = [6592]R
    1521 + 6592 = 1 mod 8112
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_ksy_y_h0_x18112_bridge_payload_contract_gate import (
    CROSS_LEVEL,
    ODD_LEVEL,
    P25,
    X16_LEVEL,
    profile_h0_x18112_bridge_payload_contract,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    X18112BridgeTheoremDecision,
    classify_claim,
)


@dataclass(frozen=True)
class H0X18112BridgeComponentClaim:
    name: str
    theorem_body_verified: bool
    h0_source_payload: bool
    same_curve_p16: bool
    same_curve_q507: bool
    same_j_or_curve: bool
    order8112_generator: bool
    x16_surface_relation: bool
    emits_x16_y: bool
    emits_model_root_or_xp16: bool
    emits_halving_chain_or_x0: bool
    danger3_framing: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class H0X18112BridgeComponentDecision:
    claim: H0X18112BridgeComponentClaim
    normalized_p16_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    order8112_constructible: bool
    x1_decision: X18112BridgeTheoremDecision | None
    decision: str
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0X18112BridgeComponentClaimIntakeProfile:
    bridge_payload_contract_ok: bool
    p: int
    x16_level: int
    odd_level: int
    cross_level: int
    normalized_p16_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    regression_rows: tuple[H0X18112BridgeComponentDecision, ...]
    row_count: int
    rejected_rows: int
    upstream_only_rows: int
    incomplete_component_rows: int
    order8112_constructible_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def normalized_projection_arithmetic() -> tuple[int, int, int]:
    p16 = (ODD_LEVEL * pow(ODD_LEVEL, -1, X16_LEVEL)) % CROSS_LEVEL
    q507 = (X16_LEVEL * pow(X16_LEVEL, -1, ODD_LEVEL)) % CROSS_LEVEL
    return p16, q507, (p16 + q507) % CROSS_LEVEL


def component_pair_constructible(claim: H0X18112BridgeComponentClaim) -> bool:
    same_curve_pair = (
        claim.same_curve_p16
        and claim.same_curve_q507
        and claim.same_j_or_curve
    )
    return claim.order8112_generator or same_curve_pair


def x1_claim_from_component(
    claim: H0X18112BridgeComponentClaim,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=claim.name,
        theorem_body_verified=claim.theorem_body_verified,
        odd_payload_object="H0_translate",
        exact_p25_specialization=True,
        odd_level_value_or_divisor=claim.h0_source_payload,
        fiber_product_or_modular_correspondence=component_pair_constructible(claim),
        preserves_j_gluing=claim.same_j_or_curve,
        x16_surface_relation=claim.x16_surface_relation,
        emits_x16_y=claim.emits_x16_y,
        emits_model_root_or_xp16=claim.emits_model_root_or_xp16,
        emits_halving_chain_or_x0=claim.emits_halving_chain_or_x0,
        danger3_framing=claim.danger3_framing,
        concrete_vpp_verified_triple=claim.concrete_vpp_verified_triple,
    )


def decision_from_values(
    claim: H0X18112BridgeComponentClaim,
    *,
    x1_decision: X18112BridgeTheoremDecision | None,
    decision: str,
    cross_level_bridge_identified: bool,
    x16_surface_reached: bool,
    extraction_ready: bool,
    submission_ready: bool,
    first_missing_or_falsifier: str,
    next_action: str,
) -> H0X18112BridgeComponentDecision:
    p16, q507, projection_sum = normalized_projection_arithmetic()
    return H0X18112BridgeComponentDecision(
        claim=claim,
        normalized_p16_multiplier=p16,
        normalized_q507_multiplier=q507,
        normalized_projection_sum_mod_8112=projection_sum,
        order8112_constructible=component_pair_constructible(claim),
        x1_decision=x1_decision,
        decision=decision,
        cross_level_bridge_identified=cross_level_bridge_identified,
        x16_surface_reached=x16_surface_reached,
        extraction_ready=extraction_ready,
        submission_ready=submission_ready,
        first_missing_or_falsifier=first_missing_or_falsifier,
        next_action=next_action,
        ok=True,
    )


def classify_component_claim(
    claim: H0X18112BridgeComponentClaim,
) -> H0X18112BridgeComponentDecision:
    if claim.concrete_vpp_verified_triple:
        x1_decision = classify_claim(x1_claim_from_component(claim))
        return decision_from_values(
            claim,
            x1_decision=x1_decision,
            decision=x1_decision.decision,
            cross_level_bridge_identified=x1_decision.cross_level_bridge_identified,
            x16_surface_reached=x1_decision.x16_surface_reached,
            extraction_ready=x1_decision.extraction_ready,
            submission_ready=x1_decision.submission_ready,
            first_missing_or_falsifier=x1_decision.first_missing_clause,
            next_action=x1_decision.next_action,
        )

    if not claim.theorem_body_verified:
        return decision_from_values(
            claim,
            x1_decision=None,
            decision="reject_no_theorem_body",
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="obtain theorem text before routing bridge components",
        )

    if not claim.h0_source_payload:
        return decision_from_values(
            claim,
            x1_decision=None,
            decision="reject_no_h0_source_payload",
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="exact H0/Y507 value or divisor payload",
            next_action="tie the X_1(16) data to the recorded odd-level H0/Y507 target",
        )

    has_partial_component = claim.same_curve_p16 != claim.same_curve_q507
    if has_partial_component and not claim.order8112_generator:
        return decision_from_values(
            claim,
            x1_decision=None,
            decision="conditional_incomplete_component_pair",
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="both same-curve P16 and H0-tied Q507, or an order-8112 generator R",
            next_action="supply the missing torsion component and same-j evidence",
        )

    if (
        claim.same_curve_p16
        and claim.same_curve_q507
        and not claim.same_j_or_curve
        and not claim.order8112_generator
    ):
        return decision_from_values(
            claim,
            x1_decision=None,
            decision="reject_unglued_components",
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="same j-invariant or same elliptic curve",
            next_action="reject independent level-16 and level-507 statements that are not glued",
        )

    if not component_pair_constructible(claim):
        x1_decision = classify_claim(x1_claim_from_component(claim))
        return decision_from_values(
            claim,
            x1_decision=x1_decision,
            decision=x1_decision.decision,
            cross_level_bridge_identified=x1_decision.cross_level_bridge_identified,
            x16_surface_reached=x1_decision.x16_surface_reached,
            extraction_ready=x1_decision.extraction_ready,
            submission_ready=x1_decision.submission_ready,
            first_missing_or_falsifier=x1_decision.first_missing_clause,
            next_action=x1_decision.next_action,
        )

    if (
        claim.same_curve_p16
        and claim.same_curve_q507
        and claim.same_j_or_curve
        and not claim.order8112_generator
        and not claim.x16_surface_relation
    ):
        return decision_from_values(
            claim,
            x1_decision=None,
            decision="construct_order_8112_generator_then_specialize_x16",
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="practical y, model root, A, and xP16 extraction data",
            next_action="construct R=P16+Q507 using normalized projections, then specialize to X_1(16)",
        )

    x1_decision = classify_claim(x1_claim_from_component(claim))
    return decision_from_values(
        claim,
        x1_decision=x1_decision,
        decision=x1_decision.decision,
        cross_level_bridge_identified=x1_decision.cross_level_bridge_identified,
        x16_surface_reached=x1_decision.x16_surface_reached,
        extraction_ready=x1_decision.extraction_ready,
        submission_ready=x1_decision.submission_ready,
        first_missing_or_falsifier=x1_decision.first_missing_clause,
        next_action=x1_decision.next_action,
    )


def base_claim(name: str, **overrides: object) -> H0X18112BridgeComponentClaim:
    values = {
        "theorem_body_verified": True,
        "h0_source_payload": True,
        "same_curve_p16": False,
        "same_curve_q507": False,
        "same_j_or_curve": False,
        "order8112_generator": False,
        "x16_surface_relation": False,
        "emits_x16_y": False,
        "emits_model_root_or_xp16": False,
        "emits_halving_chain_or_x0": False,
        "danger3_framing": False,
        "concrete_vpp_verified_triple": False,
    }
    values.update(overrides)
    return H0X18112BridgeComponentClaim(name=name, **values)


def regression_claims() -> tuple[H0X18112BridgeComponentClaim, ...]:
    return (
        base_claim("snippet_only_no_theorem", theorem_body_verified=False),
        base_claim("h0_source_only"),
        base_claim(
            "generic_x16_no_h0_payload",
            h0_source_payload=False,
            x16_surface_relation=True,
            emits_x16_y=True,
            emits_model_root_or_xp16=True,
        ),
        base_claim("same_curve_p16_only", same_curve_p16=True, same_j_or_curve=True),
        base_claim("independent_p16_q507", same_curve_p16=True, same_curve_q507=True),
        base_claim(
            "same_curve_p16_q507_pair",
            same_curve_p16=True,
            same_curve_q507=True,
            same_j_or_curve=True,
        ),
        base_claim(
            "order8112_generator_no_x16_specialization",
            order8112_generator=True,
            same_j_or_curve=True,
        ),
        base_claim(
            "order8112_x16_relation_without_y",
            order8112_generator=True,
            same_j_or_curve=True,
            x16_surface_relation=True,
        ),
        base_claim(
            "order8112_x16_y_without_surface",
            order8112_generator=True,
            same_j_or_curve=True,
            x16_surface_relation=True,
            emits_x16_y=True,
        ),
        base_claim(
            "order8112_x16_surface_policy_missing",
            order8112_generator=True,
            same_j_or_curve=True,
            x16_surface_relation=True,
            emits_x16_y=True,
            emits_model_root_or_xp16=True,
        ),
        base_claim(
            "order8112_x16_surface_halving_missing",
            order8112_generator=True,
            same_j_or_curve=True,
            x16_surface_relation=True,
            emits_x16_y=True,
            emits_model_root_or_xp16=True,
            danger3_framing=True,
        ),
        base_claim(
            "order8112_x0_payload_vpp_missing",
            order8112_generator=True,
            same_j_or_curve=True,
            x16_surface_relation=True,
            emits_x16_y=True,
            emits_model_root_or_xp16=True,
            emits_halving_chain_or_x0=True,
            danger3_framing=True,
        ),
        base_claim(
            "verified_pomerance_triple",
            h0_source_payload=False,
            concrete_vpp_verified_triple=True,
        ),
    )


def profile_h0_x18112_bridge_component_claim_intake() -> H0X18112BridgeComponentClaimIntakeProfile:
    contract = profile_h0_x18112_bridge_payload_contract()
    p16, q507, projection_sum = normalized_projection_arithmetic()
    rows = tuple(classify_component_claim(claim) for claim in regression_claims())
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    upstream = sum(row.decision == "upstream_odd_value_no_cross_level_bridge" for row in rows)
    incomplete = sum(row.decision == "conditional_incomplete_component_pair" for row in rows)
    order8112 = sum(row.order8112_constructible for row in rows)
    cross_level = sum(row.cross_level_bridge_identified for row in rows)
    x16_surface = sum(row.x16_surface_reached for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "reject_no_theorem_body",
        "upstream_odd_value_no_cross_level_bridge",
        "reject_no_h0_source_payload",
        "conditional_incomplete_component_pair",
        "reject_unglued_components",
        "construct_order_8112_generator_then_specialize_x16",
        "cross_level_target_identified_specialization_missing",
        "conditional_x16_relation_without_y",
        "conditional_y_without_montgomery_surface",
        "cross_level_surface_policy_or_framing_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready_verified_triple",
    )
    row_ok = (
        contract.row_ok
        and P25 == 10**25 + 13
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CROSS_LEVEL == 8112
        and p16 == 1521
        and q507 == 6592
        and projection_sum == 1
        and len(rows) == 13
        and rejected == 3
        and upstream == 1
        and incomplete == 1
        and order8112 == 7
        and cross_level == 8
        and x16_surface == 4
        and extraction_ready == 2
        and submission_ready == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return H0X18112BridgeComponentClaimIntakeProfile(
        bridge_payload_contract_ok=contract.row_ok,
        p=P25,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        cross_level=CROSS_LEVEL,
        normalized_p16_multiplier=p16,
        normalized_q507_multiplier=q507,
        normalized_projection_sum_mod_8112=projection_sum,
        regression_rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        upstream_only_rows=upstream,
        incomplete_component_rows=incomplete,
        order8112_constructible_rows=order8112,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def claim_from_args(args: argparse.Namespace) -> H0X18112BridgeComponentClaim:
    return H0X18112BridgeComponentClaim(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        h0_source_payload=args.h0_source_payload,
        same_curve_p16=args.same_curve_p16,
        same_curve_q507=args.same_curve_q507,
        same_j_or_curve=args.same_j,
        order8112_generator=args.order_8112_generator,
        x16_surface_relation=args.x16_relation,
        emits_x16_y=args.emit_y,
        emits_model_root_or_xp16=args.emit_model_root_xp16,
        emits_halving_chain_or_x0=args.emit_x0,
        danger3_framing=args.danger3_framing,
        concrete_vpp_verified_triple=args.vpp_verified,
    )


def print_decision(row: H0X18112BridgeComponentDecision) -> None:
    claim = row.claim
    print(
        "  "
        f"{claim.name}: theorem={int(claim.theorem_body_verified)} "
        f"h0_payload={int(claim.h0_source_payload)} "
        f"P16={int(claim.same_curve_p16)} Q507={int(claim.same_curve_q507)} "
        f"same_j={int(claim.same_j_or_curve)} R8112={int(claim.order8112_generator)} "
        f"x16_relation={int(claim.x16_surface_relation)} y={int(claim.emits_x16_y)} "
        f"model_xp16={int(claim.emits_model_root_or_xp16)} "
        f"x0={int(claim.emits_halving_chain_or_x0)} "
        f"danger3={int(claim.danger3_framing)} vpp={int(claim.concrete_vpp_verified_triple)} "
        f"constructible={int(row.order8112_constructible)} "
        f"x16={int(row.x16_surface_reached)} extract={int(row.extraction_ready)} "
        f"submission={int(row.submission_ready)} decision={row.decision} "
        f"missing={row.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="component_claim")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--h0-source-payload", action="store_true")
    parser.add_argument("--same-curve-p16", action="store_true")
    parser.add_argument("--same-curve-q507", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--order-8112-generator", action="store_true")
    parser.add_argument("--x16-relation", action="store_true")
    parser.add_argument("--emit-y", action="store_true")
    parser.add_argument("--emit-model-root-xp16", action="store_true")
    parser.add_argument("--emit-x0", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        row = classify_component_claim(claim_from_args(args))
        print("p25 KSY-y H0 X1(8112) bridge-component claim intake candidate")
        print("projection_arithmetic")
        print(f"  normalized_p16_multiplier={row.normalized_p16_multiplier}")
        print(f"  normalized_q507_multiplier={row.normalized_q507_multiplier}")
        print(f"  normalized_projection_sum_mod_8112={row.normalized_projection_sum_mod_8112}")
        print("candidate_decision")
        print_decision(row)
        print(f"next_action={row.next_action}")
        print(f"ksy_y_h0_x18112_bridge_component_claim_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_h0_x18112_bridge_component_claim_intake()
    print("p25 KSY-y H0 X1(8112) bridge-component claim intake gate")
    print("dependencies")
    print(f"  bridge_payload_contract_ok={int(profile.bridge_payload_contract_ok)}")
    print("projection_arithmetic")
    print(f"  p={profile.p}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  cross_level={profile.cross_level}")
    print(f"  normalized_p16_multiplier={profile.normalized_p16_multiplier}")
    print(f"  normalized_q507_multiplier={profile.normalized_q507_multiplier}")
    print(f"  normalized_projection_sum_mod_8112={profile.normalized_projection_sum_mod_8112}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  incomplete_component_rows={profile.incomplete_component_rows}")
    print(f"  order8112_constructible_rows={profile.order8112_constructible_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  same_curve_P16_Q507_components_can_construct_order8112_R=1")
    print("  independent_P16_Q507_components_are_rejected_without_same_j=1")
    print("  order8112_bridge_still_needs_X1_16_specialization_and_vpp=1")
    print(f"ksy_y_h0_x18112_bridge_component_claim_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 X1(8112) bridge-component claim intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
