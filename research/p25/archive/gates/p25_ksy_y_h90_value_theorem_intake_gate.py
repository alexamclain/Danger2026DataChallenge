#!/usr/bin/env python3
"""Intake gate for exact Y_507 / H0 value-theorem claims.

The bridge-spine gate proves that the KSY-y target can be routed through

    exact P -> Y_507 -> Norm_156(Y_507) -> legal sparse H0.

This gate classifies future theorem hits against that narrowed interface.  It
does not prove a new value identity; it prevents weaker claims from being
mistaken for closure.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
BRIDGE_SPINE = REPO / "research" / "p25" / "p25_ksy_y_yang_ksy_product_h90_bridge_spine_20260614.md"
BRIDGE_SPINE_MARKER = "ksy_y_yang_ksy_product_h90_bridge_spine_rows=1/1"
ATOM_COUNT = 75
RAW_SIEGEL_TERM_COUNT = 300
QUOTIENT_Y507_SUPPORT = 12
PERIOD_NORM_SUPPORT = 312
H90_POTENTIAL_SUPPORT = 156
CANONICAL_H90_POSITIVE_RESIDUES_MOD39 = (7, 17, 23, 34, 37, 38)
CANONICAL_H90_NEGATIVE_RESIDUES_MOD39 = (4, 8, 10, 11, 20, 25)
H90_POSITIVE_FACTOR_COUNT = 78
H90_NEGATIVE_FACTOR_COUNT = 78
H90_BOUNDARY_OK = True


LIVE_TARGET_OBJECTS = frozenset(
    {
        "exact_P",
        "Y_507",
        "canonical_H0",
        "H0_translate",
        "conductor39_U_chi",
    }
)

ILLEGAL_OR_INSUFFICIENT_TARGETS = frozenset(
    {
        "formal_one_coset_H",
        "prime13_projection",
        "c169_projection",
        "ambient_780_value",
    }
)


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


@dataclass(frozen=True)
class H90ValueTheoremClaim:
    name: str
    theorem_body_verified: bool
    target_object: str
    output_kind: str
    exact_target: bool
    bridge_spine_preserved: bool
    legal_yang_or_h90_object: bool
    boundary_or_period_norm_context: bool
    finite_field_identity_or_divisor: bool
    period_156_context: bool
    arithmetic_source_theorem: bool
    danger3_framing: bool
    extraction_to_A_x0: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class H90ValueTheoremDecision:
    claim: H90ValueTheoremClaim
    decision: str
    live_target_identified: bool
    theorem_source_closed: bool
    danger3_route_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class H90ValueTheoremIntakeProfile:
    bridge_spine_ok: bool
    conductor39_contract_referenced: bool
    submission_extraction_contract_referenced: bool
    canonical_positive_residues_mod39: tuple[int, ...]
    canonical_negative_residues_mod39: tuple[int, ...]
    h90_positive_factor_count: int
    h90_negative_factor_count: int
    h90_boundary_equals_period_norm: bool
    regression_rows: tuple[H90ValueTheoremDecision, ...]
    live_target_rows: int
    theorem_source_closed_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_rows: int
    conditional_rows: int
    row_ok: bool


def classify_claim(claim: H90ValueTheoremClaim) -> H90ValueTheoremDecision:
    if claim.concrete_vpp_verified_triple:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="submission_ready_verified_triple",
            live_target_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_clause="none",
            next_action="archive certificate, logs, environment, and submit",
            row_ok=True,
        )

    if not claim.theorem_body_verified:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="reject_no_theorem_body",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="verified theorem statement or proof body",
            next_action="obtain theorem text before routing it through H0/Y507 intake",
            row_ok=True,
        )

    if claim.target_object in ILLEGAL_OR_INSUFFICIENT_TARGETS:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="reject_illegal_or_insufficient_target",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact P, Y_507, canonical H0, H0 translate, or conductor-39 mixed source",
            next_action="reject projection, ambient-period, or formal one-coset claims",
            row_ok=True,
        )

    if claim.output_kind == "field-generation":
        return H90ValueTheoremDecision(
            claim=claim,
            decision="reject_field_generation_not_value_or_divisor_theorem",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact finite-field value or divisor/additive identity",
            next_action="discard unless reframed as exact P/Y507/H0 identity",
            row_ok=True,
        )

    if claim.output_kind == "finite-verifier":
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_finite_payload_without_source_theorem",
            live_target_identified=claim.target_object in LIVE_TARGET_OBJECTS,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="challenge-legal arithmetic source theorem",
            next_action="keep as verifier payload only after a real source theorem emits it",
            row_ok=True,
        )

    if claim.target_object not in LIVE_TARGET_OBJECTS:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_unknown_or_unrouted_target",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="target object on the KSY/Yang/H0 bridge spine",
            next_action="map the claim to exact P, Y_507, canonical H0, H0 translate, or U_chi",
            row_ok=True,
        )

    if not claim.exact_target:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_missing_exact_target",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact residues/product, not a nearby family",
            next_action="specialize the theorem to the recorded p25 target object",
            row_ok=True,
        )

    if not claim.bridge_spine_preserved:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_missing_bridge_spine",
            live_target_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="75->300->12->312->156 KSY/Yang/H90 bridge context",
            next_action="attach the bridge-spine normalization before treating the theorem as p25 progress",
            row_ok=True,
        )

    if not claim.legal_yang_or_h90_object:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="reject_target_fails_yang_or_h90_legality",
            live_target_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="Yang/Yu legality and legal sparse H90 selector",
            next_action="run the target through Y507/H0 legality and product-normal-form gates",
            row_ok=True,
        )

    if claim.target_object in {"canonical_H0", "H0_translate"} and not claim.boundary_or_period_norm_context:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_h0_missing_boundary_to_norm",
            live_target_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="(1-Frob_p)H0 = Norm_156(Y_507)",
            next_action="attach the Hilbert-90 boundary before using the H0 value",
            row_ok=True,
        )

    if claim.output_kind == "value" and not claim.period_156_context:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_missing_period_156_context",
            live_target_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="period-156 branch/root/telescoping context",
            next_action="ask for support-period fixedness before trusting the F_p value branch",
            row_ok=True,
        )

    if not claim.finite_field_identity_or_divisor:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="live_target_identified_value_or_divisor_theorem_missing",
            live_target_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value identity or divisor/additive theorem",
            next_action="continue from the exact target object to a theorem that can feed extraction",
            row_ok=True,
        )

    if not claim.arithmetic_source_theorem:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="conditional_finite_identity_without_arithmetic_source",
            live_target_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="challenge-legal arithmetic source theorem",
            next_action="treat as finite verifier payload until an arithmetic source theorem emits it",
            row_ok=True,
        )

    if not claim.danger3_framing:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="source_theorem_closed_policy_or_framing_missing",
            live_target_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            next_action="settle challenge framing, then derive concrete A and x0",
            row_ok=True,
        )

    if not claim.extraction_to_A_x0:
        return H90ValueTheoremDecision(
            claim=claim,
            decision="danger3_unblocked_extraction_missing",
            live_target_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="extraction algorithm for concrete (A,x0)",
            next_action="derive the DANGER3 triple and run official vpp.py",
            row_ok=True,
        )

    return H90ValueTheoremDecision(
        claim=claim,
        decision="ready_to_extract_and_verify_concrete_triple",
        live_target_identified=True,
        theorem_source_closed=True,
        danger3_route_unblocked=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_clause="official vpp.py verification of concrete (A,x0)",
        next_action="run extraction and official verification",
        row_ok=True,
    )


def regression_claims() -> tuple[H90ValueTheoremClaim, ...]:
    base = {
        "theorem_body_verified": True,
        "target_object": "canonical_H0",
        "output_kind": "divisor-additive",
        "exact_target": True,
        "bridge_spine_preserved": True,
        "legal_yang_or_h90_object": True,
        "boundary_or_period_norm_context": True,
        "finite_field_identity_or_divisor": True,
        "period_156_context": True,
        "arithmetic_source_theorem": True,
        "danger3_framing": True,
        "extraction_to_A_x0": True,
        "concrete_vpp_verified_triple": False,
    }
    return (
        H90ValueTheoremClaim(
            "snippet_only",
            False,
            "unknown",
            "source-object",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        H90ValueTheoremClaim(
            "formal_one_coset_same_boundary",
            **{**base, "target_object": "formal_one_coset_H", "finite_field_identity_or_divisor": False},
        ),
        H90ValueTheoremClaim(
            "prime13_projection_value",
            **{**base, "target_object": "prime13_projection", "output_kind": "value"},
        ),
        H90ValueTheoremClaim(
            "generic_ray_class_generation",
            **{
                **base,
                "target_object": "Y_507",
                "output_kind": "field-generation",
                "finite_field_identity_or_divisor": False,
            },
        ),
        H90ValueTheoremClaim(
            "finite_y507_payload_without_source",
            **{
                **base,
                "target_object": "Y_507",
                "output_kind": "finite-verifier",
                "arithmetic_source_theorem": False,
            },
        ),
        H90ValueTheoremClaim(
            "canonical_h0_target_no_value_theorem",
            **{**base, "finite_field_identity_or_divisor": False},
        ),
        H90ValueTheoremClaim(
            "canonical_h0_missing_boundary",
            **{**base, "boundary_or_period_norm_context": False, "finite_field_identity_or_divisor": False},
        ),
        H90ValueTheoremClaim(
            "exact_y507_value_without_period156",
            **{**base, "target_object": "Y_507", "output_kind": "value", "period_156_context": False},
        ),
        H90ValueTheoremClaim(
            "canonical_h0_finite_identity_without_source",
            **{**base, "arithmetic_source_theorem": False},
        ),
        H90ValueTheoremClaim(
            "canonical_h0_divisor_theorem_policy_missing",
            **{**base, "danger3_framing": False, "extraction_to_A_x0": False},
        ),
        H90ValueTheoremClaim(
            "h0_translate_divisor_theorem_extraction_missing",
            **{**base, "target_object": "H0_translate", "extraction_to_A_x0": False},
        ),
        H90ValueTheoremClaim(
            "exact_p_value_ready_to_verify",
            **{**base, "target_object": "exact_P", "output_kind": "value"},
        ),
        H90ValueTheoremClaim(
            "submission_ready_control",
            **{**base, "concrete_vpp_verified_triple": True},
        ),
    )


def profile_h90_value_theorem_intake() -> H90ValueTheoremIntakeProfile:
    bridge_ok = marker_present(BRIDGE_SPINE, BRIDGE_SPINE_MARKER)
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    conditional = sum(
        row.decision.startswith(("conditional_", "live_target_identified_"))
        for row in decisions
    )
    row_ok = (
        bridge_ok
        and ATOM_COUNT == 75
        and RAW_SIEGEL_TERM_COUNT == 300
        and QUOTIENT_Y507_SUPPORT == 12
        and PERIOD_NORM_SUPPORT == 312
        and H90_POTENTIAL_SUPPORT == 156
        and CANONICAL_H90_POSITIVE_RESIDUES_MOD39 == (7, 17, 23, 34, 37, 38)
        and CANONICAL_H90_NEGATIVE_RESIDUES_MOD39 == (4, 8, 10, 11, 20, 25)
        and H90_POSITIVE_FACTOR_COUNT == 78
        and H90_NEGATIVE_FACTOR_COUNT == 78
        and H90_BOUNDARY_OK
        and tuple(row.decision for row in decisions)
        == (
            "reject_no_theorem_body",
            "reject_illegal_or_insufficient_target",
            "reject_illegal_or_insufficient_target",
            "reject_field_generation_not_value_or_divisor_theorem",
            "conditional_finite_payload_without_source_theorem",
            "live_target_identified_value_or_divisor_theorem_missing",
            "conditional_h0_missing_boundary_to_norm",
            "conditional_missing_period_156_context",
            "conditional_finite_identity_without_arithmetic_source",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "ready_to_extract_and_verify_concrete_triple",
            "submission_ready_verified_triple",
        )
        and rejected == 4
        and conditional == 5
        and sum(row.live_target_identified for row in decisions) == 9
        and sum(row.theorem_source_closed for row in decisions) == 4
        and sum(row.danger3_route_unblocked for row in decisions) == 3
        and sum(row.extraction_ready for row in decisions) == 2
        and sum(row.submission_ready for row in decisions) == 1
        and all(row.row_ok for row in decisions)
    )
    return H90ValueTheoremIntakeProfile(
        bridge_spine_ok=bridge_ok,
        conductor39_contract_referenced=True,
        submission_extraction_contract_referenced=True,
        canonical_positive_residues_mod39=CANONICAL_H90_POSITIVE_RESIDUES_MOD39,
        canonical_negative_residues_mod39=CANONICAL_H90_NEGATIVE_RESIDUES_MOD39,
        h90_positive_factor_count=H90_POSITIVE_FACTOR_COUNT,
        h90_negative_factor_count=H90_NEGATIVE_FACTOR_COUNT,
        h90_boundary_equals_period_norm=H90_BOUNDARY_OK,
        regression_rows=decisions,
        live_target_rows=sum(row.live_target_identified for row in decisions),
        theorem_source_closed_rows=sum(row.theorem_source_closed for row in decisions),
        danger3_unblocked_rows=sum(row.danger3_route_unblocked for row in decisions),
        extraction_ready_rows=sum(row.extraction_ready for row in decisions),
        submission_ready_rows=sum(row.submission_ready for row in decisions),
        rejected_rows=rejected,
        conditional_rows=conditional,
        row_ok=row_ok,
    )


def print_decision(row: H90ValueTheoremDecision) -> None:
    claim = row.claim
    print(
        "  "
        f"{claim.name}: target={claim.target_object} kind={claim.output_kind} "
        f"exact={int(claim.exact_target)} bridge={int(claim.bridge_spine_preserved)} "
        f"legal={int(claim.legal_yang_or_h90_object)} "
        f"boundary={int(claim.boundary_or_period_norm_context)} "
        f"finite={int(claim.finite_field_identity_or_divisor)} "
        f"period156={int(claim.period_156_context)} "
        f"source={int(claim.arithmetic_source_theorem)} "
        f"danger3={int(claim.danger3_framing)} "
        f"extract={int(claim.extraction_to_A_x0)} "
        f"vpp={int(claim.concrete_vpp_verified_triple)} "
        f"decision={row.decision} "
        f"missing={row.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--target-object", default="canonical_H0")
    parser.add_argument("--output-kind", default="divisor-additive")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--exact-target", action="store_true")
    parser.add_argument("--bridge-spine", action="store_true")
    parser.add_argument("--legal-yang-h90", action="store_true")
    parser.add_argument("--boundary-context", action="store_true")
    parser.add_argument("--finite-or-divisor", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--arithmetic-source", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--extraction", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        decision = classify_claim(
            H90ValueTheoremClaim(
                name=args.name,
                theorem_body_verified=args.theorem_body,
                target_object=args.target_object,
                output_kind=args.output_kind,
                exact_target=args.exact_target,
                bridge_spine_preserved=args.bridge_spine,
                legal_yang_or_h90_object=args.legal_yang_h90,
                boundary_or_period_norm_context=args.boundary_context,
                finite_field_identity_or_divisor=args.finite_or_divisor,
                period_156_context=args.period_156,
                arithmetic_source_theorem=args.arithmetic_source,
                danger3_framing=args.danger3_framing,
                extraction_to_A_x0=args.extraction,
                concrete_vpp_verified_triple=args.vpp_verified,
            )
        )
        print("p25 KSY-y H90/Y507 value-theorem intake candidate")
        print_decision(decision)
        print(f"live_target_identified={int(decision.live_target_identified)}")
        print(f"theorem_source_closed={int(decision.theorem_source_closed)}")
        print(f"danger3_route_unblocked={int(decision.danger3_route_unblocked)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"next_action={decision.next_action}")
        print(f"ksy_y_h90_value_theorem_intake_candidate_rows={int(decision.row_ok)}/1")
        if not decision.row_ok:
            raise SystemExit("H90/Y507 value-theorem candidate intake failed")
        return 0

    profile = profile_h90_value_theorem_intake()
    print("p25 KSY-y H90/Y507 value-theorem intake gate")
    print("dependency_gates")
    print(f"  bridge_spine_ok={int(profile.bridge_spine_ok)}")
    print(f"  conductor39_contract_referenced={int(profile.conductor39_contract_referenced)}")
    print(
        "  submission_extraction_contract_referenced="
        f"{int(profile.submission_extraction_contract_referenced)}"
    )
    print("canonical_H0")
    print(f"  positive_residues_mod39={profile.canonical_positive_residues_mod39}")
    print(f"  negative_residues_mod39={profile.canonical_negative_residues_mod39}")
    print(f"  positive_factor_count={profile.h90_positive_factor_count}")
    print(f"  negative_factor_count={profile.h90_negative_factor_count}")
    print(f"  boundary_equals_period_norm={int(profile.h90_boundary_equals_period_norm)}")
    print("regression_claims")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  live_target_rows={profile.live_target_rows}")
    print(f"  theorem_source_closed_rows={profile.theorem_source_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  exact_P_Y507_and_legal_H0_are_live_value_theorem_targets=1")
    print("  formal_one_coset_projection_generation_and_ambient780_claims_are_rejected=1")
    print("  H0_value_claims_need_boundary_period156_source_policy_and_extraction=1")
    print("  still_missing_actual_value_or_divisor_theorem_and_vpp_verified_triple=1")
    print(f"ksy_y_h90_value_theorem_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H90/Y507 value-theorem intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
