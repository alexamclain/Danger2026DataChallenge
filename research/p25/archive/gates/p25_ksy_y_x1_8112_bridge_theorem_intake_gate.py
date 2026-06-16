#!/usr/bin/env python3
"""X_1(8112) bridge-theorem intake for the p25 KSY-y moonshot.

The cross-level extraction-gap gate says what is missing: the odd-level
KSY/Yang/H90/curved-corner target must be connected to the 2-primary X_1(16) extraction
surface.  This gate turns that into a theorem-intake classifier.  A future
claim is useful only if it glues the p25 odd-level target to the X_1(16)
surface over the j-line, or directly emits a vpp.py-verified triple.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_ksy_y_cross_level_extraction_gap_gate import (
    CONDUCTOR_LEVEL,
    CROSS_LEVEL,
    ODD_LEVEL,
    P25,
    X16_LEVEL,
    profile_cross_level_extraction_gap,
)


ACCEPTED_ODD_TARGETS = frozenset(
    {
        "exact_P",
        "U_507",
        "Y_507",
        "canonical_H0",
        "H0_translate",
        "conductor39_U_chi",
        "curved_corner",
    }
)


@dataclass(frozen=True)
class X18112BridgeTheoremClaim:
    name: str
    theorem_body_verified: bool
    odd_payload_object: str
    exact_p25_specialization: bool
    odd_level_value_or_divisor: bool
    fiber_product_or_modular_correspondence: bool
    preserves_j_gluing: bool
    x16_surface_relation: bool
    emits_x16_y: bool
    emits_model_root_or_xp16: bool
    emits_halving_chain_or_x0: bool
    danger3_framing: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class X18112BridgeTheoremDecision:
    claim: X18112BridgeTheoremClaim
    decision: str
    odd_target_identified: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class X18112BridgeTheoremIntakeProfile:
    cross_level_gap_ok: bool
    p: int
    x16_level: int
    odd_level: int
    conductor_level: int
    cross_level: int
    accepted_odd_targets: tuple[str, ...]
    regression_rows: tuple[X18112BridgeTheoremDecision, ...]
    odd_target_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    upstream_only_rows: int
    rejected_rows: int
    conditional_rows: int
    row_ok: bool


def odd_target_identified(claim: X18112BridgeTheoremClaim) -> bool:
    return (
        claim.odd_payload_object in ACCEPTED_ODD_TARGETS
        and claim.exact_p25_specialization
        and claim.odd_level_value_or_divisor
    )


def x16_surface_reached(claim: X18112BridgeTheoremClaim) -> bool:
    return (
        claim.x16_surface_relation
        and claim.emits_x16_y
        and claim.emits_model_root_or_xp16
    )


def classify_claim(claim: X18112BridgeTheoremClaim) -> X18112BridgeTheoremDecision:
    if claim.concrete_vpp_verified_triple:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="submission_ready_verified_triple",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_clause="none",
            next_action="archive vpp output, command log, environment, and certificate",
            row_ok=True,
        )

    if not claim.theorem_body_verified:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="reject_no_theorem_body",
            odd_target_identified=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="verified theorem statement or proof body",
            next_action="obtain theorem text before routing it through X1(8112) intake",
            row_ok=True,
        )

    if claim.odd_payload_object not in ACCEPTED_ODD_TARGETS:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="conditional_unknown_odd_target",
            odd_target_identified=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=(
                "exact_P, U_507, Y_507, canonical_H0, H0 translate, conductor39_U_chi, "
                "or curved_corner"
            ),
            next_action="map the claim onto the recorded KSY/Yang/H90/curved-corner bridge spine",
            row_ok=True,
        )

    if not claim.exact_p25_specialization:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="conditional_missing_exact_p25_specialization",
            odd_target_identified=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="p25-specialized target, not a family-level possibility",
            next_action="specialize the theorem to p=10^25+13 and the recorded p25 payload",
            row_ok=True,
        )

    if not claim.odd_level_value_or_divisor:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="reject_generic_x16_not_ksy_bridge",
            odd_target_identified=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="odd-level KSY/Yang/H90 value or divisor payload",
            next_action="reject generic X_1(16) extraction data unless it is tied to the p25 odd target",
            row_ok=True,
        )

    if not claim.fiber_product_or_modular_correspondence and not claim.x16_surface_relation:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="upstream_odd_value_no_cross_level_bridge",
            odd_target_identified=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="X_1(16) relation or X_1(8112) fiber-product theorem",
            next_action="keep as upstream theorem progress; do not call it extraction",
            row_ok=True,
        )

    if claim.fiber_product_or_modular_correspondence and not claim.preserves_j_gluing:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="reject_unvalidated_fiber_product_gluing",
            odd_target_identified=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="fiber product over the same j-invariant",
            next_action="reject independent level-16 and level-507 statements that are not glued",
            row_ok=True,
        )

    if not claim.fiber_product_or_modular_correspondence:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="conditional_missing_x1_8112_bridge",
            odd_target_identified=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="explicit cross-level map, correspondence, or fiber-product relation",
            next_action="upgrade the X_1(16) relation to a p25 KSY/Yang/H90 bridge",
            row_ok=True,
        )

    if not claim.x16_surface_relation:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="cross_level_target_identified_specialization_missing",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            next_action="derive the p25 X_1(16) extraction variables from the fiber-product theorem",
            row_ok=True,
        )

    if not claim.emits_x16_y:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="conditional_x16_relation_without_y",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="actual X_1(16) parameter y",
            next_action="specialize the relation to the practical y-parameter used by the search",
            row_ok=True,
        )

    if not claim.emits_model_root_or_xp16:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="conditional_y_without_montgomery_surface",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="model root x, Montgomery A, and marked xP16",
            next_action="derive the recorded X_1(16) Montgomery surface equations",
            row_ok=True,
        )

    if not claim.danger3_framing:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="cross_level_surface_policy_or_framing_missing",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            next_action="settle challenge framing before treating the bridge as submission progress",
            row_ok=True,
        )

    if not claim.emits_halving_chain_or_x0:
        return X18112BridgeTheoremDecision(
            claim=claim,
            decision="x16_surface_reached_halving_or_vpp_missing",
            odd_target_identified=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="valid halving chain from xP16 to concrete x0",
            next_action="run or derive the halving chain, then official vpp.py",
            row_ok=True,
        )

    return X18112BridgeTheoremDecision(
        claim=claim,
        decision="extraction_ready_vpp_missing",
        odd_target_identified=True,
        cross_level_bridge_identified=True,
        x16_surface_reached=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_clause="official vpp.py verification",
        next_action="verify the concrete (p,A,x0) with official vpp.py",
        row_ok=True,
    )


def regression_claims() -> tuple[X18112BridgeTheoremClaim, ...]:
    base = {
        "theorem_body_verified": True,
        "odd_payload_object": "canonical_H0",
        "exact_p25_specialization": True,
        "odd_level_value_or_divisor": True,
        "fiber_product_or_modular_correspondence": True,
        "preserves_j_gluing": True,
        "x16_surface_relation": True,
        "emits_x16_y": True,
        "emits_model_root_or_xp16": True,
        "emits_halving_chain_or_x0": True,
        "danger3_framing": True,
        "concrete_vpp_verified_triple": False,
    }
    return (
        X18112BridgeTheoremClaim(
            "snippet_only",
            False,
            "unknown",
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
        X18112BridgeTheoremClaim(
            "pure_y507_value_theorem",
            **{
                **base,
                "odd_payload_object": "Y_507",
                "fiber_product_or_modular_correspondence": False,
                "x16_surface_relation": False,
                "emits_x16_y": False,
                "emits_model_root_or_xp16": False,
                "emits_halving_chain_or_x0": False,
            },
        ),
        X18112BridgeTheoremClaim(
            "generic_x16_surface_no_odd_payload",
            **{
                **base,
                "odd_level_value_or_divisor": False,
                "fiber_product_or_modular_correspondence": False,
                "x16_surface_relation": True,
                "emits_halving_chain_or_x0": False,
            },
        ),
        X18112BridgeTheoremClaim(
            "unglued_level16_and_level507_statements",
            **{**base, "preserves_j_gluing": False},
        ),
        X18112BridgeTheoremClaim(
            "x1_8112_bridge_no_x16_specialization",
            **{
                **base,
                "x16_surface_relation": False,
                "emits_x16_y": False,
                "emits_model_root_or_xp16": False,
                "emits_halving_chain_or_x0": False,
            },
        ),
        X18112BridgeTheoremClaim(
            "curved_corner_bridge_no_x16_specialization",
            **{
                **base,
                "odd_payload_object": "curved_corner",
                "x16_surface_relation": False,
                "emits_x16_y": False,
                "emits_model_root_or_xp16": False,
                "emits_halving_chain_or_x0": False,
            },
        ),
        X18112BridgeTheoremClaim(
            "specialized_relation_without_y",
            **{
                **base,
                "emits_x16_y": False,
                "emits_model_root_or_xp16": False,
                "emits_halving_chain_or_x0": False,
            },
        ),
        X18112BridgeTheoremClaim(
            "x16_y_without_montgomery_surface",
            **{**base, "emits_model_root_or_xp16": False, "emits_halving_chain_or_x0": False},
        ),
        X18112BridgeTheoremClaim(
            "surface_payload_policy_missing",
            **{**base, "danger3_framing": False, "emits_halving_chain_or_x0": False},
        ),
        X18112BridgeTheoremClaim(
            "surface_payload_halving_missing",
            **{**base, "emits_halving_chain_or_x0": False},
        ),
        X18112BridgeTheoremClaim("x0_payload_vpp_missing", **base),
        X18112BridgeTheoremClaim(
            "verified_p25_triple",
            **{**base, "concrete_vpp_verified_triple": True},
        ),
    )


def profile_x1_8112_bridge_theorem_intake() -> X18112BridgeTheoremIntakeProfile:
    gap = profile_cross_level_extraction_gap()
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    conditional = sum(
        row.decision.startswith(
            (
                "conditional_",
                "upstream_",
                "cross_level_",
                "x16_surface_",
                "extraction_",
            )
        )
        for row in decisions
    )
    upstream_only = sum(row.decision == "upstream_odd_value_no_cross_level_bridge" for row in decisions)
    row_ok = (
        gap.row_ok
        and P25 == 10**25 + 13
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CONDUCTOR_LEVEL == 39
        and CROSS_LEVEL == 8112
        and tuple(row.decision for row in decisions)
        == (
            "reject_no_theorem_body",
            "upstream_odd_value_no_cross_level_bridge",
            "reject_generic_x16_not_ksy_bridge",
            "reject_unvalidated_fiber_product_gluing",
            "cross_level_target_identified_specialization_missing",
            "cross_level_target_identified_specialization_missing",
            "conditional_x16_relation_without_y",
            "conditional_y_without_montgomery_surface",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready_verified_triple",
        )
        and sum(row.odd_target_identified for row in decisions) == 10
        and sum(row.cross_level_bridge_identified for row in decisions) == 8
        and sum(row.x16_surface_reached for row in decisions) == 4
        and sum(row.extraction_ready for row in decisions) == 2
        and sum(row.submission_ready for row in decisions) == 1
        and upstream_only == 1
        and rejected == 3
        and conditional == 8
        and all(row.row_ok for row in decisions)
    )
    return X18112BridgeTheoremIntakeProfile(
        cross_level_gap_ok=gap.row_ok,
        p=P25,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        conductor_level=CONDUCTOR_LEVEL,
        cross_level=CROSS_LEVEL,
        accepted_odd_targets=tuple(sorted(ACCEPTED_ODD_TARGETS)),
        regression_rows=decisions,
        odd_target_rows=sum(row.odd_target_identified for row in decisions),
        cross_level_bridge_rows=sum(row.cross_level_bridge_identified for row in decisions),
        x16_surface_rows=sum(row.x16_surface_reached for row in decisions),
        extraction_ready_rows=sum(row.extraction_ready for row in decisions),
        submission_ready_rows=sum(row.submission_ready for row in decisions),
        upstream_only_rows=upstream_only,
        rejected_rows=rejected,
        conditional_rows=conditional,
        row_ok=row_ok,
    )


def build_candidate(args: argparse.Namespace) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        odd_payload_object=args.odd_payload_object,
        exact_p25_specialization=args.exact_p25,
        odd_level_value_or_divisor=args.odd_value_or_divisor,
        fiber_product_or_modular_correspondence=args.fiber_product,
        preserves_j_gluing=args.j_gluing,
        x16_surface_relation=args.x16_relation,
        emits_x16_y=args.emit_y,
        emits_model_root_or_xp16=args.emit_model_root_xp16,
        emits_halving_chain_or_x0=args.emit_x0,
        danger3_framing=args.danger3_framing,
        concrete_vpp_verified_triple=args.vpp_verified,
    )


def print_decision(row: X18112BridgeTheoremDecision) -> None:
    claim = row.claim
    print(
        "  "
        f"{claim.name}: odd_object={claim.odd_payload_object} "
        f"exact_p25={int(claim.exact_p25_specialization)} "
        f"odd_value={int(claim.odd_level_value_or_divisor)} "
        f"fiber={int(claim.fiber_product_or_modular_correspondence)} "
        f"j_gluing={int(claim.preserves_j_gluing)} "
        f"x16_relation={int(claim.x16_surface_relation)} "
        f"y={int(claim.emits_x16_y)} "
        f"model_xp16={int(claim.emits_model_root_or_xp16)} "
        f"x0={int(claim.emits_halving_chain_or_x0)} "
        f"danger3={int(claim.danger3_framing)} "
        f"vpp={int(claim.concrete_vpp_verified_triple)} "
        f"decision={row.decision} missing={row.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--odd-payload-object", default="Y_507")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--exact-p25", action="store_true")
    parser.add_argument("--odd-value-or-divisor", action="store_true")
    parser.add_argument("--fiber-product", action="store_true")
    parser.add_argument("--j-gluing", action="store_true")
    parser.add_argument("--x16-relation", action="store_true")
    parser.add_argument("--emit-y", action="store_true")
    parser.add_argument("--emit-model-root-xp16", action="store_true")
    parser.add_argument("--emit-x0", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        decision = classify_claim(build_candidate(args))
        print("p25 KSY-y X1(8112) bridge-theorem intake candidate")
        print_decision(decision)
        print(f"odd_target_identified={int(decision.odd_target_identified)}")
        print(f"cross_level_bridge_identified={int(decision.cross_level_bridge_identified)}")
        print(f"x16_surface_reached={int(decision.x16_surface_reached)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"next_action={decision.next_action}")
        print(f"ksy_y_x1_8112_bridge_theorem_intake_candidate_rows={int(decision.row_ok)}/1")
        if not decision.row_ok:
            raise SystemExit("X1(8112) bridge-theorem candidate intake failed")
        return 0

    profile = profile_x1_8112_bridge_theorem_intake()
    print("p25 KSY-y X1(8112) bridge-theorem intake gate")
    print("levels")
    print(f"  p={profile.p}")
    print(f"  conductor_level={profile.conductor_level}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  cross_level={profile.cross_level}")
    print("dependency_gates")
    print(f"  cross_level_gap_ok={int(profile.cross_level_gap_ok)}")
    print(f"accepted_odd_targets={profile.accepted_odd_targets}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  odd_target_rows={profile.odd_target_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  pure_odd_value_theorem_is_upstream_only=1")
    print("  generic_x16_surface_without_odd_target_is_rejected=1")
    print("  x1_8112_claim_must_preserve_j_gluing_and_emit_x16_surface=1")
    print(f"ksy_y_x1_8112_bridge_theorem_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(8112) bridge-theorem intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
