#!/usr/bin/env python3
"""Bridge-theorem intake between conductor-39 source and ray-local payload.

The alignment gate proves that U_chi=-chi_3*chi_13 is not the ray-local
theta31 payload.  This gate classifies future claims that try to cross that
gap.  It accepts source/value theorems as real progress, but rejects any claim
that merely renames U_chi as theta31 without an explicit bridge or evaluation
theorem and a finite payload accepted by the ray-local harness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_ray_local_conductor39_alignment_gate import (
    profile_ray_local_conductor39_alignment,
)
from p25_ksy_y_ray_local_conductor39_simple_transform_falsifier_gate import (
    profile_simple_transform_falsifier,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class BridgeTheoremCandidate:
    name: str
    theorem_body_verified: bool
    conductor39_source_certified: bool
    preserves_mixed_tensor: bool
    projection_or_generator_only: bool
    claims_uchi_equals_theta31: bool
    explicit_bridge_or_evaluation: bool
    resolves_alignment_obstruction: bool
    target_raw_theta31_or_bridge: bool
    target_curved_corner: bool
    finite_acceptor_verified: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    arithmetic_source_theorem: bool
    danger3_framing: bool
    same_j_x18112_bridge: bool
    x16_surface: bool
    concrete_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class BridgeTheoremDecision:
    candidate: BridgeTheoremCandidate
    decision: str
    source_stage_closed: bool
    ray_payload_reached: bool
    finite_value_reached: bool
    danger3_unblocked: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class BridgeTheoremIntakeProfile:
    alignment_ok: bool
    unified_router_marker_present: bool
    simple_transform_falsifier_ok: bool
    theta31_support: int
    u_chi_support: int
    raw_signed_dot: int
    theta31_mixed_rank: int
    u_chi_rank: int
    combined_mixed_rank: int
    simple_transform_exact_support_matches: int
    simple_transform_row_column_solvable_rows: int
    simple_transform_rank_ceiling: int
    rows: tuple[BridgeTheoremDecision, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_stage_closed_rows: int
    ray_payload_rows: int
    finite_value_rows: int
    danger3_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def decision(
    candidate: BridgeTheoremCandidate,
    name: str,
    *,
    source_stage_closed: bool = False,
    ray_payload_reached: bool = False,
    finite_value_reached: bool = False,
    danger3_unblocked: bool = False,
    cross_level_bridge_identified: bool = False,
    x16_surface_reached: bool = False,
    extraction_ready: bool = False,
    submission_ready: bool = False,
    first_missing_or_falsifier: str,
    next_action: str,
) -> BridgeTheoremDecision:
    return BridgeTheoremDecision(
        candidate=candidate,
        decision=name,
        source_stage_closed=source_stage_closed,
        ray_payload_reached=ray_payload_reached,
        finite_value_reached=finite_value_reached,
        danger3_unblocked=danger3_unblocked,
        cross_level_bridge_identified=cross_level_bridge_identified,
        x16_surface_reached=x16_surface_reached,
        extraction_ready=extraction_ready,
        submission_ready=submission_ready,
        first_missing_or_falsifier=first_missing_or_falsifier,
        next_action=next_action,
        ok=True,
    )


def classify_candidate(candidate: BridgeTheoremCandidate) -> BridgeTheoremDecision:
    if candidate.official_vpp and candidate.concrete_A_x0:
        return decision(
            candidate,
            "submission_ready",
            source_stage_closed=True,
            ray_payload_reached=True,
            finite_value_reached=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_or_falsifier="none",
            next_action="archive official vpp.py output, command, environment, and certificate",
        )

    if not candidate.theorem_body_verified:
        return decision(
            candidate,
            "reject_no_theorem_body",
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="obtain theorem text before routing the bridge claim",
        )

    if not candidate.conductor39_source_certified:
        return decision(
            candidate,
            "reject_missing_conductor39_source",
            first_missing_or_falsifier="certified U_chi, W, Y_507, H0, or H0 translate source",
            next_action="route through conductor-39 source certificate/intake first",
        )

    if candidate.projection_or_generator_only or not candidate.preserves_mixed_tensor:
        return decision(
            candidate,
            "reject_loses_mixed_tensor",
            first_missing_or_falsifier="mixed chi_3 tensor chi_13 source on X_1(39)",
            next_action="kill projection/generator-only answers unless the mixed tensor is restored",
        )

    if candidate.claims_uchi_equals_theta31 and not candidate.explicit_bridge_or_evaluation:
        return decision(
            candidate,
            "reject_uchi_theta31_renaming",
            first_missing_or_falsifier=(
                "explicit bridge/evaluation theorem; simple-transform falsifier "
                "kills U_chi-to-theta31 shortcuts"
            ),
            next_action="do not infer ray-local payload certification from U_chi source certification",
        )

    if not candidate.explicit_bridge_or_evaluation:
        if candidate.finite_value_or_divisor_theorem:
            if not candidate.period156_context:
                return decision(
                    candidate,
                    "conditional_missing_period156_context",
                    finite_value_reached=True,
                    first_missing_or_falsifier="period-156 branch/root/telescoping context",
                    next_action="ask for period-156 fixedness before treating a value theorem as closed",
                )
            if not candidate.arithmetic_source_theorem:
                return decision(
                    candidate,
                    "conditional_finite_value_without_source_theorem",
                    finite_value_reached=True,
                    first_missing_or_falsifier="challenge-legal arithmetic source theorem",
                    next_action="keep as finite value data only",
                )
            return decision(
                candidate,
                "source_theorem_closed_not_ray_payload_policy_or_framing_missing",
                source_stage_closed=True,
                finite_value_reached=True,
                first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing; no ray-local payload bridge",
                next_action="continue as conductor-39/H0 value route, not as theta31 payload",
            )
        return decision(
            candidate,
            "conditional_conductor39_source_only_no_ray_bridge",
            first_missing_or_falsifier="finite value/divisor theorem or explicit bridge to ray-local payload",
            next_action="keep as source certification; ask for value theorem or bridge theorem",
        )

    if not candidate.resolves_alignment_obstruction:
        return decision(
            candidate,
            "reject_alignment_obstruction_unresolved",
            first_missing_or_falsifier=(
                "support/rank/orthogonality mismatch between U_chi and theta31 "
                "must be resolved explicitly beyond scalar, affine, row/column, "
                "or separated-gauge transforms"
            ),
            next_action="require a map that explains support 24 vs 18, dot 0, and rank 1 vs 2",
        )

    if not (candidate.target_raw_theta31_or_bridge or candidate.target_curved_corner):
        return decision(
            candidate,
            "conditional_bridge_target_payload_unspecified",
            first_missing_or_falsifier="raw theta31/bridge target or curved-corner target",
            next_action="name the finite acceptor before value/extraction routing",
        )

    if not candidate.finite_acceptor_verified:
        return decision(
            candidate,
            "conditional_bridge_no_finite_acceptor",
            first_missing_or_falsifier="ray-local raw/bridge harness or curved-corner intake verification",
            next_action="run the proposed payload through the finite acceptor",
        )

    if not candidate.finite_value_or_divisor_theorem:
        if candidate.target_curved_corner and not candidate.target_raw_theta31_or_bridge:
            return decision(
                candidate,
                "helper_only_curved_corner_bridge_value_theorem_missing",
                ray_payload_reached=True,
                first_missing_or_falsifier="finite value/divisor theorem for the curved K-traced corner payload",
                next_action="keep as 75-atom helper; ask for value/divisor theorem",
            )
        return decision(
            candidate,
            "helper_only_raw_theta31_bridge_value_theorem_missing",
            ray_payload_reached=True,
            first_missing_or_falsifier="finite value/divisor theorem for the raw theta31 or bridge payload",
            next_action="keep as finite helper; ask for value/divisor theorem",
        )

    if not candidate.period156_context:
        return decision(
            candidate,
            "conditional_missing_period156_context",
            ray_payload_reached=True,
            finite_value_reached=True,
            first_missing_or_falsifier="period-156 branch/root/telescoping context",
            next_action="attach period-156 context before source closure",
        )

    if not candidate.arithmetic_source_theorem:
        return decision(
            candidate,
            "conditional_finite_payload_without_source_theorem",
            ray_payload_reached=True,
            finite_value_reached=True,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            next_action="keep as verifier payload only",
        )

    if not candidate.danger3_framing:
        return decision(
            candidate,
            "source_theorem_closed_policy_or_framing_missing",
            source_stage_closed=True,
            ray_payload_reached=True,
            finite_value_reached=True,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            next_action="resolve framing, then route to same-j X_1(8112) bridge",
        )

    if not candidate.same_j_x18112_bridge:
        return decision(
            candidate,
            "danger3_unblocked_cross_level_bridge_missing",
            source_stage_closed=True,
            ray_payload_reached=True,
            finite_value_reached=True,
            danger3_unblocked=True,
            first_missing_or_falsifier="same-j X_1(8112) bridge or equivalent cross-level map",
            next_action="derive the bridge to the practical X_1(16) chart",
        )

    if not candidate.x16_surface:
        return decision(
            candidate,
            "cross_level_target_identified_specialization_missing",
            source_stage_closed=True,
            ray_payload_reached=True,
            finite_value_reached=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            first_missing_or_falsifier="specialized X_1(16) y, A, and xP16 surface",
            next_action="specialize the bridge to X_1(16)",
        )

    if not candidate.concrete_A_x0:
        return decision(
            candidate,
            "x16_surface_reached_halving_or_vpp_missing",
            source_stage_closed=True,
            ray_payload_reached=True,
            finite_value_reached=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            first_missing_or_falsifier="halving chain or direct concrete x0",
            next_action="derive x0 and verify with official vpp.py",
        )

    return decision(
        candidate,
        "extraction_ready_vpp_missing",
        source_stage_closed=True,
        ray_payload_reached=True,
        finite_value_reached=True,
        danger3_unblocked=True,
        cross_level_bridge_identified=True,
        x16_surface_reached=True,
        extraction_ready=True,
        first_missing_or_falsifier="official vpp.py verification",
        next_action="run official vpp.py on concrete p25 (p,A,x0)",
    )


def base_candidate() -> dict[str, bool]:
    return {
        "theorem_body_verified": True,
        "conductor39_source_certified": True,
        "preserves_mixed_tensor": True,
        "projection_or_generator_only": False,
        "claims_uchi_equals_theta31": False,
        "explicit_bridge_or_evaluation": False,
        "resolves_alignment_obstruction": False,
        "target_raw_theta31_or_bridge": False,
        "target_curved_corner": False,
        "finite_acceptor_verified": False,
        "finite_value_or_divisor_theorem": False,
        "period156_context": False,
        "arithmetic_source_theorem": False,
        "danger3_framing": False,
        "same_j_x18112_bridge": False,
        "x16_surface": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }


def regression_candidates() -> tuple[BridgeTheoremCandidate, ...]:
    base = base_candidate()
    bridge = {
        **base,
        "explicit_bridge_or_evaluation": True,
        "resolves_alignment_obstruction": True,
        "target_raw_theta31_or_bridge": True,
        "finite_acceptor_verified": True,
    }
    value_bridge = {**bridge, "finite_value_or_divisor_theorem": True}
    source_bridge = {
        **value_bridge,
        "period156_context": True,
        "arithmetic_source_theorem": True,
    }
    danger3_bridge = {**source_bridge, "danger3_framing": True}
    same_j_bridge = {**danger3_bridge, "same_j_x18112_bridge": True}
    x16_bridge = {**same_j_bridge, "x16_surface": True}
    x0_bridge = {**x16_bridge, "concrete_A_x0": True}
    conductor39_value = {
        **base,
        "finite_value_or_divisor_theorem": True,
        "period156_context": True,
        "arithmetic_source_theorem": True,
    }
    return (
        BridgeTheoremCandidate("no_theorem_body", **{**base, "theorem_body_verified": False}),
        BridgeTheoremCandidate(
            "missing_conductor39_source",
            **{**base, "conductor39_source_certified": False},
        ),
        BridgeTheoremCandidate(
            "projection_generator_only",
            **{**base, "projection_or_generator_only": True, "preserves_mixed_tensor": False},
        ),
        BridgeTheoremCandidate(
            "bare_uchi_theta31_rename",
            **{**base, "claims_uchi_equals_theta31": True},
        ),
        BridgeTheoremCandidate("source_only_no_bridge", **base),
        BridgeTheoremCandidate("conductor39_value_no_ray_bridge", **conductor39_value),
        BridgeTheoremCandidate(
            "bridge_unresolved_alignment",
            **{**base, "explicit_bridge_or_evaluation": True},
        ),
        BridgeTheoremCandidate(
            "bridge_target_unspecified",
            **{
                **base,
                "explicit_bridge_or_evaluation": True,
                "resolves_alignment_obstruction": True,
            },
        ),
        BridgeTheoremCandidate(
            "bridge_no_finite_acceptor",
            **{
                **base,
                "explicit_bridge_or_evaluation": True,
                "resolves_alignment_obstruction": True,
                "target_raw_theta31_or_bridge": True,
            },
        ),
        BridgeTheoremCandidate("raw_theta31_helper", **bridge),
        BridgeTheoremCandidate(
            "curved_corner_helper",
            **{
                **base,
                "explicit_bridge_or_evaluation": True,
                "resolves_alignment_obstruction": True,
                "target_curved_corner": True,
                "finite_acceptor_verified": True,
            },
        ),
        BridgeTheoremCandidate("value_no_period156", **value_bridge),
        BridgeTheoremCandidate(
            "period156_value_no_source",
            **{**value_bridge, "period156_context": True},
        ),
        BridgeTheoremCandidate("source_no_framing", **source_bridge),
        BridgeTheoremCandidate("danger3_no_same_j", **danger3_bridge),
        BridgeTheoremCandidate("same_j_no_x16", **same_j_bridge),
        BridgeTheoremCandidate("x16_no_x0", **x16_bridge),
        BridgeTheoremCandidate("x0_no_vpp", **x0_bridge),
        BridgeTheoremCandidate("official_vpp_verified", **{**x0_bridge, "official_vpp": True}),
    )


def profile_bridge_theorem_intake() -> BridgeTheoremIntakeProfile:
    alignment = profile_ray_local_conductor39_alignment()
    simple = profile_simple_transform_falsifier()
    unified_marker = marker_present(
        RESEARCH / "p25_ksy_y_unified_expert_answer_router_20260614.md",
        "ksy_y_unified_expert_answer_router_rows=1/1",
    )
    rows = tuple(classify_candidate(candidate) for candidate in regression_candidates())
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    helper = sum(row.decision.startswith("helper_only_") for row in rows)
    conditional = sum(row.decision.startswith("conditional_") for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    ray_payload = sum(row.ray_payload_reached for row in rows)
    finite_value = sum(row.finite_value_reached for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    cross_level = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "reject_no_theorem_body",
        "reject_missing_conductor39_source",
        "reject_loses_mixed_tensor",
        "reject_uchi_theta31_renaming",
        "conditional_conductor39_source_only_no_ray_bridge",
        "source_theorem_closed_not_ray_payload_policy_or_framing_missing",
        "reject_alignment_obstruction_unresolved",
        "conditional_bridge_target_payload_unspecified",
        "conditional_bridge_no_finite_acceptor",
        "helper_only_raw_theta31_bridge_value_theorem_missing",
        "helper_only_curved_corner_bridge_value_theorem_missing",
        "conditional_missing_period156_context",
        "conditional_finite_payload_without_source_theorem",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        alignment.row_ok
        and simple.row_ok
        and unified_marker
        and alignment.theta31_support == 18
        and alignment.u_chi_support == 24
        and alignment.raw_signed_dot == 0
        and alignment.theta31_mixed_rank == 2
        and alignment.u_chi_rank == 1
        and alignment.combined_mixed_rank == 3
        and simple.product_affine.exact_theta_support_matches == 0
        and simple.product_affine.exact_theta_mixed_support_matches == 0
        and not simple.raw_row_column_fit.solvable
        and not simple.mixed_row_column_fit.solvable
        and simple.separated_multiplicative_rank_ceiling == 1
        and len(rows) == 19
        and rejected == 5
        and helper == 2
        and conditional == 5
        and source_closed == 7
        and ray_payload == 10
        and finite_value == 9
        and danger3 == 5
        and cross_level == 4
        and x16 == 3
        and extraction == 2
        and submission == 1
        and tuple(row.decision for row in rows) == expected_decisions
        and all(row.ok for row in rows)
    )
    return BridgeTheoremIntakeProfile(
        alignment_ok=alignment.row_ok,
        unified_router_marker_present=unified_marker,
        simple_transform_falsifier_ok=simple.row_ok,
        theta31_support=alignment.theta31_support,
        u_chi_support=alignment.u_chi_support,
        raw_signed_dot=alignment.raw_signed_dot,
        theta31_mixed_rank=alignment.theta31_mixed_rank,
        u_chi_rank=alignment.u_chi_rank,
        combined_mixed_rank=alignment.combined_mixed_rank,
        simple_transform_exact_support_matches=(
            simple.product_affine.exact_theta_support_matches
            + simple.product_affine.exact_theta_mixed_support_matches
        ),
        simple_transform_row_column_solvable_rows=sum(
            (
                simple.raw_row_column_fit.solvable,
                simple.mixed_row_column_fit.solvable,
            )
        ),
        simple_transform_rank_ceiling=simple.separated_multiplicative_rank_ceiling,
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_stage_closed_rows=source_closed,
        ray_payload_rows=ray_payload,
        finite_value_rows=finite_value,
        danger3_unblocked_rows=danger3,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> BridgeTheoremCandidate:
    return BridgeTheoremCandidate(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        conductor39_source_certified=args.conductor39_source,
        preserves_mixed_tensor=args.mixed_tensor,
        projection_or_generator_only=args.projection_only,
        claims_uchi_equals_theta31=args.claims_uchi_equals_theta31,
        explicit_bridge_or_evaluation=args.explicit_bridge,
        resolves_alignment_obstruction=args.resolves_alignment,
        target_raw_theta31_or_bridge=args.raw_theta31_bridge,
        target_curved_corner=args.curved_corner,
        finite_acceptor_verified=args.finite_acceptor,
        finite_value_or_divisor_theorem=args.finite_or_divisor,
        period156_context=args.period_156,
        arithmetic_source_theorem=args.arithmetic_source,
        danger3_framing=args.danger3_framing,
        same_j_x18112_bridge=args.same_j,
        x16_surface=args.x16,
        concrete_A_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(row: BridgeTheoremDecision) -> None:
    candidate = row.candidate
    print(
        "  "
        f"{candidate.name}: theorem={int(candidate.theorem_body_verified)} "
        f"source={int(candidate.conductor39_source_certified)} "
        f"mixed={int(candidate.preserves_mixed_tensor)} "
        f"projection={int(candidate.projection_or_generator_only)} "
        f"renames={int(candidate.claims_uchi_equals_theta31)} "
        f"bridge={int(candidate.explicit_bridge_or_evaluation)} "
        f"resolves={int(candidate.resolves_alignment_obstruction)} "
        f"raw={int(candidate.target_raw_theta31_or_bridge)} "
        f"curved={int(candidate.target_curved_corner)} "
        f"acceptor={int(candidate.finite_acceptor_verified)} "
        f"finite={int(candidate.finite_value_or_divisor_theorem)} "
        f"period156={int(candidate.period156_context)} "
        f"arithmetic={int(candidate.arithmetic_source_theorem)} "
        f"danger3={int(candidate.danger3_framing)} "
        f"same_j={int(candidate.same_j_x18112_bridge)} "
        f"x16={int(candidate.x16_surface)} "
        f"x0={int(candidate.concrete_A_x0)} "
        f"vpp={int(candidate.official_vpp)} "
        f"decision={row.decision} "
        f"source_closed={int(row.source_stage_closed)} "
        f"ray_payload={int(row.ray_payload_reached)} "
        f"finite_value={int(row.finite_value_reached)} "
        f"submission={int(row.submission_ready)} "
        f"missing={row.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify bridge theorem claims from conductor-39 source to ray-local payload."
    )
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--conductor39-source", action="store_true")
    parser.add_argument("--mixed-tensor", action="store_true")
    parser.add_argument("--projection-only", action="store_true")
    parser.add_argument("--claims-uchi-equals-theta31", action="store_true")
    parser.add_argument("--explicit-bridge", action="store_true")
    parser.add_argument("--resolves-alignment", action="store_true")
    parser.add_argument("--raw-theta31-bridge", action="store_true")
    parser.add_argument("--curved-corner", action="store_true")
    parser.add_argument("--finite-acceptor", action="store_true")
    parser.add_argument("--finite-or-divisor", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--arithmetic-source", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--x16", action="store_true")
    parser.add_argument("--x0", action="store_true")
    parser.add_argument("--vpp", action="store_true")
    args = parser.parse_args()

    print("p25 KSY-y ray-local / conductor-39 bridge theorem intake gate")
    if args.candidate:
        row = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(row)
        print(f"ksy_y_ray_local_conductor39_bridge_theorem_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_bridge_theorem_intake()
    print("dependencies")
    print(f"  alignment_ok={int(profile.alignment_ok)}")
    print(f"  unified_router_marker_present={int(profile.unified_router_marker_present)}")
    print(f"  simple_transform_falsifier_ok={int(profile.simple_transform_falsifier_ok)}")
    print("alignment_facts")
    print(f"  theta31_support={profile.theta31_support}")
    print(f"  u_chi_support={profile.u_chi_support}")
    print(f"  raw_signed_dot={profile.raw_signed_dot}")
    print(f"  theta31_mixed_rank={profile.theta31_mixed_rank}")
    print(f"  u_chi_rank={profile.u_chi_rank}")
    print(f"  combined_mixed_rank={profile.combined_mixed_rank}")
    print("simple_transform_falsifier")
    print(f"  exact_support_matches={profile.simple_transform_exact_support_matches}")
    print(
        "  row_column_solvable_rows="
        f"{profile.simple_transform_row_column_solvable_rows}"
    )
    print(f"  separated_rank_ceiling={profile.simple_transform_rank_ceiling}")
    print("regression_rows")
    for row in profile.rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  ray_payload_rows={profile.ray_payload_rows}")
    print(f"  finite_value_rows={profile.finite_value_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  u_chi_source_value_route_is_not_ray_payload_without_bridge=1")
    print("  explicit_bridge_must_resolve_support_rank_orthogonality_mismatch=1")
    print("  simple_transforms_are_first_falsifier_for_uchi_theta31_claims=1")
    print("  finite_ray_payload_is_helper_only_until_value_theorem=1")
    print("  source_closure_still_routes_to_DANGER3_extraction_and_vpp=1")
    print(f"ksy_y_ray_local_conductor39_bridge_theorem_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("ray-local / conductor-39 bridge theorem intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
