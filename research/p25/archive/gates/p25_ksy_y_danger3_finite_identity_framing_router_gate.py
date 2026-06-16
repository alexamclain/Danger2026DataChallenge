#!/usr/bin/env python3
"""Router for DANGER3 finite-identity/non-CM framing claims.

The source-side moonshot now has several ways a theorem could enter the
pipeline: a 75-atom product, Y_507 value, canonical H0 value, or H0 divisor
identity.  This gate classifies what extra framing and extraction data are
needed before such a theorem becomes a DANGER3 submission.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class FiniteIdentityFramingCandidate:
    name: str
    has_source_theorem: bool
    finite_field_identity_for_p: bool
    generic_cm_or_class_field_generation: bool
    explicit_non_cm_finite_field_framing: bool
    danger3_policy_accepts_identity: bool
    same_j_x18112_bridge: bool
    x16_surface_or_A_xP16: bool
    concrete_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class FiniteIdentityFramingDecision:
    candidate: FiniteIdentityFramingCandidate
    decision: str
    source_stage_closed: bool
    danger3_unblocked: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class FiniteIdentityFramingRouter:
    conductor39_acceptance_marker_present: bool
    general_danger3_framing_marker_present: bool
    h0_source_handoff_marker_present: bool
    h0_final_boundary_marker_present: bool
    rows: tuple[FiniteIdentityFramingDecision, ...]
    row_count: int
    rejected_rows: int
    source_shape_missing_rows: int
    policy_or_framing_missing_rows: int
    danger3_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def classify_candidate(
    candidate: FiniteIdentityFramingCandidate,
) -> FiniteIdentityFramingDecision:
    if candidate.official_vpp:
        if candidate.concrete_A_x0:
            return FiniteIdentityFramingDecision(
                candidate=candidate,
                decision="submission_ready",
                source_stage_closed=True,
                danger3_unblocked=True,
                cross_level_bridge_identified=True,
                x16_surface_reached=True,
                extraction_ready=True,
                submission_ready=True,
                first_missing_or_falsifier="none",
                next_action="archive official vpp output, command, environment, and Lean certificate",
                ok=True,
            )
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="reject_vpp_without_concrete_A_x0",
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="concrete A and x0 accompanying the vpp claim",
            next_action="obtain the concrete triple and rerun official vpp.py",
            ok=True,
        )

    if not candidate.has_source_theorem and not candidate.concrete_A_x0:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="reject_no_source_theorem_or_triple",
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="source theorem or concrete vpp-verifiable triple",
            next_action="obtain theorem text, or supply A,x0 and run official vpp.py",
            ok=True,
        )

    generic_only = (
        candidate.generic_cm_or_class_field_generation
        and not candidate.explicit_non_cm_finite_field_framing
        and not candidate.danger3_policy_accepts_identity
        and not candidate.concrete_A_x0
    )
    if generic_only:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="reject_generic_cm_generation_not_framing",
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="explicit non-CM finite-field identity framing or external policy yes",
            next_action="reframe as a finite-field identity for this p, not generic CM/class-field generation",
            ok=True,
        )

    if candidate.has_source_theorem and not candidate.finite_field_identity_for_p:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="source_theorem_value_shape_missing_finite_identity",
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="finite-field value/divisor identity specialized to p25",
            next_action="upgrade the theorem statement to an exact p25 finite identity",
            ok=True,
        )

    framed_or_policy_yes = (
        candidate.explicit_non_cm_finite_field_framing
        or candidate.danger3_policy_accepts_identity
    )
    if not framed_or_policy_yes:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="source_theorem_closed_policy_or_framing_missing",
            source_stage_closed=True,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            next_action="get explicit non-CM finite-field language or an external policy yes",
            ok=True,
        )

    if not candidate.same_j_x18112_bridge:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="danger3_unblocked_cross_level_bridge_missing",
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="same-j X_1(8112) bridge or equivalent cross-level map",
            next_action="derive the bridge from the odd-level identity to the X_1(16) surface",
            ok=True,
        )

    if not candidate.x16_surface_or_A_xP16:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="cross_level_target_identified_specialization_missing",
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="specialized X_1(16) y, Montgomery A, and xP16 surface",
            next_action="specialize the bridge to X_1(16) and expose A,xP16 or equivalent data",
            ok=True,
        )

    if not candidate.concrete_A_x0:
        return FiniteIdentityFramingDecision(
            candidate=candidate,
            decision="x16_surface_reached_halving_or_vpp_missing",
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="halving chain or direct concrete x0",
            next_action="derive x0 from A,xP16, then run official vpp.py",
            ok=True,
        )

    return FiniteIdentityFramingDecision(
        candidate=candidate,
        decision="extraction_ready_vpp_missing",
        source_stage_closed=True,
        danger3_unblocked=True,
        cross_level_bridge_identified=True,
        x16_surface_reached=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_or_falsifier="official vpp.py verification",
        next_action="run official vpp.py on the concrete p25 (p,A,x0) triple",
        ok=True,
    )


def regression_candidates() -> tuple[FiniteIdentityFramingCandidate, ...]:
    base = {
        "has_source_theorem": True,
        "finite_field_identity_for_p": True,
        "generic_cm_or_class_field_generation": False,
        "explicit_non_cm_finite_field_framing": False,
        "danger3_policy_accepts_identity": False,
        "same_j_x18112_bridge": False,
        "x16_surface_or_A_xP16": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }
    return (
        FiniteIdentityFramingCandidate(
            "no_source_no_triple",
            **{**base, "has_source_theorem": False, "finite_field_identity_for_p": False},
        ),
        FiniteIdentityFramingCandidate(
            "source_theorem_no_finite_identity",
            **{**base, "finite_field_identity_for_p": False},
        ),
        FiniteIdentityFramingCandidate(
            "generic_cm_class_field_generation",
            **{**base, "generic_cm_or_class_field_generation": True},
        ),
        FiniteIdentityFramingCandidate("finite_identity_policy_unknown", **base),
        FiniteIdentityFramingCandidate(
            "finite_identity_explicit_non_cm_no_bridge",
            **{**base, "explicit_non_cm_finite_field_framing": True},
        ),
        FiniteIdentityFramingCandidate(
            "finite_identity_policy_yes_no_bridge",
            **{**base, "danger3_policy_accepts_identity": True},
        ),
        FiniteIdentityFramingCandidate(
            "same_j_bridge_no_x16",
            **{
                **base,
                "danger3_policy_accepts_identity": True,
                "same_j_x18112_bridge": True,
            },
        ),
        FiniteIdentityFramingCandidate(
            "x16_surface_no_x0",
            **{
                **base,
                "danger3_policy_accepts_identity": True,
                "same_j_x18112_bridge": True,
                "x16_surface_or_A_xP16": True,
            },
        ),
        FiniteIdentityFramingCandidate(
            "concrete_A_x0_no_vpp",
            **{
                **base,
                "danger3_policy_accepts_identity": True,
                "same_j_x18112_bridge": True,
                "x16_surface_or_A_xP16": True,
                "concrete_A_x0": True,
            },
        ),
        FiniteIdentityFramingCandidate(
            "official_vpp_verified_triple",
            **{
                **base,
                "danger3_policy_accepts_identity": True,
                "same_j_x18112_bridge": True,
                "x16_surface_or_A_xP16": True,
                "concrete_A_x0": True,
                "official_vpp": True,
            },
        ),
    )


def profile_finite_identity_framing_router() -> FiniteIdentityFramingRouter:
    conductor39_marker = marker_present(
        RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_20260614.md",
        "ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1",
    )
    general_framing_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing.md",
        "robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_rows=1/1",
    )
    h0_handoff_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_source_to_danger3_handoff_20260614.md",
        "ksy_y_h0_source_to_danger3_handoff_rows=1/1",
    )
    h0_boundary_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_x16_final_certificate_boundary_20260614.md",
        "ksy_y_h0_x16_final_certificate_boundary_rows=1/1",
    )
    rows = tuple(classify_candidate(candidate) for candidate in regression_candidates())
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    source_shape_missing = sum(
        row.decision == "source_theorem_value_shape_missing_finite_identity"
        for row in rows
    )
    policy_missing = sum(
        row.decision == "source_theorem_closed_policy_or_framing_missing"
        for row in rows
    )
    danger3_unblocked = sum(row.danger3_unblocked for row in rows)
    cross_level = sum(row.cross_level_bridge_identified for row in rows)
    x16_surface = sum(row.x16_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "reject_no_source_theorem_or_triple",
        "source_theorem_value_shape_missing_finite_identity",
        "reject_generic_cm_generation_not_framing",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        conductor39_marker
        and general_framing_marker
        and h0_handoff_marker
        and h0_boundary_marker
        and len(rows) == 10
        and rejected == 2
        and source_shape_missing == 1
        and policy_missing == 1
        and danger3_unblocked == 6
        and cross_level == 4
        and x16_surface == 3
        and extraction == 2
        and submission == 1
        and tuple(row.decision for row in rows) == expected_decisions
        and all(row.ok for row in rows)
    )
    return FiniteIdentityFramingRouter(
        conductor39_acceptance_marker_present=conductor39_marker,
        general_danger3_framing_marker_present=general_framing_marker,
        h0_source_handoff_marker_present=h0_handoff_marker,
        h0_final_boundary_marker_present=h0_boundary_marker,
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        source_shape_missing_rows=source_shape_missing,
        policy_or_framing_missing_rows=policy_missing,
        danger3_unblocked_rows=danger3_unblocked,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> FiniteIdentityFramingCandidate:
    return FiniteIdentityFramingCandidate(
        name=args.name,
        has_source_theorem=args.source_theorem,
        finite_field_identity_for_p=args.finite_identity,
        generic_cm_or_class_field_generation=args.generic_cm,
        explicit_non_cm_finite_field_framing=args.non_cm_framing,
        danger3_policy_accepts_identity=args.policy_yes,
        same_j_x18112_bridge=args.same_j,
        x16_surface_or_A_xP16=args.x16,
        concrete_A_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(decision: FiniteIdentityFramingDecision) -> None:
    candidate = decision.candidate
    print(
        "  "
        f"{candidate.name}: source={int(candidate.has_source_theorem)} "
        f"finite_identity={int(candidate.finite_field_identity_for_p)} "
        f"generic_cm={int(candidate.generic_cm_or_class_field_generation)} "
        f"non_cm_framing={int(candidate.explicit_non_cm_finite_field_framing)} "
        f"policy_yes={int(candidate.danger3_policy_accepts_identity)} "
        f"same_j={int(candidate.same_j_x18112_bridge)} "
        f"x16={int(candidate.x16_surface_or_A_xP16)} "
        f"x0={int(candidate.concrete_A_x0)} "
        f"vpp={int(candidate.official_vpp)} "
        f"decision={decision.decision} "
        f"source_closed={int(decision.source_stage_closed)} "
        f"danger3={int(decision.danger3_unblocked)} "
        f"x8112={int(decision.cross_level_bridge_identified)} "
        f"x16_reached={int(decision.x16_surface_reached)} "
        f"extract={int(decision.extraction_ready)} "
        f"submission={int(decision.submission_ready)} "
        f"missing={decision.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify DANGER3 finite-identity/non-CM framing candidates."
    )
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--source-theorem", action="store_true")
    parser.add_argument("--finite-identity", action="store_true")
    parser.add_argument("--generic-cm", action="store_true")
    parser.add_argument("--non-cm-framing", action="store_true")
    parser.add_argument("--policy-yes", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--x16", action="store_true")
    parser.add_argument("--x0", action="store_true")
    parser.add_argument("--vpp", action="store_true")
    args = parser.parse_args()

    print("p25 KSY-y DANGER3 finite-identity framing router gate")
    if args.candidate:
        decision = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(
            "ksy_y_danger3_finite_identity_framing_router_candidate_rows="
            f"{int(decision.ok)}/1"
        )
        return 0 if decision.ok else 1

    profile = profile_finite_identity_framing_router()
    print("dependencies")
    print(
        "  conductor39_acceptance_marker_present="
        f"{int(profile.conductor39_acceptance_marker_present)}"
    )
    print(
        "  general_danger3_framing_marker_present="
        f"{int(profile.general_danger3_framing_marker_present)}"
    )
    print(
        "  h0_source_handoff_marker_present="
        f"{int(profile.h0_source_handoff_marker_present)}"
    )
    print(
        "  h0_final_boundary_marker_present="
        f"{int(profile.h0_final_boundary_marker_present)}"
    )
    print("regression_rows")
    for decision in profile.rows:
        print_decision(decision)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  source_shape_missing_rows={profile.source_shape_missing_rows}")
    print(f"  policy_or_framing_missing_rows={profile.policy_or_framing_missing_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  generic_cm_generation_is_not_danger3_framing=1")
    print("  explicit_non_cm_finite_identity_or_policy_yes_unblocks_framing=1")
    print("  framing_yes_still_needs_same_j_bridge_x16_extraction_and_vpp=1")
    print("  only_official_vpp_verified_A_x0_is_submission_ready=1")
    print(
        "ksy_y_danger3_finite_identity_framing_router_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("DANGER3 finite-identity framing router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
