#!/usr/bin/env python3
"""Ray-local modular-unit pullback router for the p25 Lane B moonshot.

The finite Lane B work has two different producer-facing acceptors:

* raw local theta31 vectors, checked by the ray-local pullback falsifier; and
* the smaller square-axis/curved-corner Hilbert-90 payload, checked by the
  corner producer intake.

This router sits one level above those harnesses.  It classifies future
CM-Artin, modular-unit, Robert/Siegel/Kubert-Lang, or related theorem claims
before they are allowed into the raw-vector or curved-corner lanes.  The point
is to reject theorem-shaped false positives early: split-prime-only sources,
separated local units, x-only/even tables, pure C-axis phases, nonprimitive K
traces, and the wrong translated edge.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class PullbackCandidate:
    name: str
    theorem_body_verified: bool
    ray_local_inert_right_source: bool
    split_c_axis_source: bool
    source_coupling_not_separated: bool
    residue_rectangles_constant: bool
    mixed_rank2_non_degenerate: bool
    avoids_degenerate_u_plus_2v: bool
    not_x_only_even_table: bool
    active_c_side_odd_orientation: bool
    orientation_not_plain_c_character: bool
    coupled_d_segment: bool
    primitive_k_trace: bool
    recorded_t_edge_2_113: bool
    raw_kernel_gauge_only: bool
    raw_vector_or_bridge_harness: bool
    curved_corner_shape: bool
    curved_corner_unit_triangle: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    arithmetic_source_theorem: bool
    danger3_framing: bool
    same_j_x18112_bridge: bool
    x16_surface: bool
    concrete_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class PullbackDecision:
    candidate: PullbackCandidate
    decision: str
    finite_shape_reached: bool
    finite_value_reached: bool
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
class RayLocalPullbackRouterProfile:
    cm_artin_marker_present: bool
    local_pullback_marker_present: bool
    residue_coset_marker_present: bool
    source_half_arc_marker_present: bool
    mixed_character_marker_present: bool
    ray_local_theta31_falsifier_marker_present: bool
    bridge_harness_marker_present: bool
    anti_invariant_contract_marker_present: bool
    curved_corner_intake_marker_present: bool
    curved_corner_unit_triangle_marker_present: bool
    dependency_markers_ok: bool
    right_source_prime: int
    c_axis_source_prime: int
    quotient_rectangles: int
    residue_rectangle_size: int
    raw_order: int
    carrying_rectangles: int
    raw_carry_one_positions: int
    bridge_mixed_characters: int
    compact_curved_corner_atoms: int
    required_translated_edge: tuple[int, int]
    rows: tuple[PullbackDecision, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    finite_shape_rows: int
    finite_value_rows: int
    source_closing_rows: int
    danger3_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def regex_marker_present(path: Path, pattern: str) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    return re.search(pattern, path.read_text()) is not None


def classify_candidate(candidate: PullbackCandidate) -> PullbackDecision:
    if candidate.official_vpp and candidate.concrete_A_x0:
        return PullbackDecision(
            candidate=candidate,
            decision="submission_ready",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_or_falsifier="none",
            next_action="archive official vpp.py output, command, environment, and certificate",
            ok=True,
        )

    if not candidate.theorem_body_verified:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_no_theorem_body",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="obtain a theorem body before routing the pullback claim",
            ok=True,
        )

    if not (candidate.ray_local_inert_right_source and candidate.split_c_axis_source):
        return PullbackDecision(
            candidate=candidate,
            decision="reject_not_ray_local_inert_split_source",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="inert/ray-local right source 151 coupled to split C source 677",
            next_action="discard split-prime-only or plain class-quotient producers for this lane",
            ok=True,
        )

    if not candidate.source_coupling_not_separated:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_separated_or_pure_c_source",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="nonseparated inert-right/split-C coupling",
            next_action="kill additive products of independent right and C selectors",
            ok=True,
        )

    if not candidate.residue_rectangles_constant:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_not_residue_rectangle_pullback",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="constancy on 25 x 13 local residue rectangles",
            next_action="check the object on local residue cosets before quotient claims",
            ok=True,
        )

    if not (candidate.mixed_rank2_non_degenerate and candidate.avoids_degenerate_u_plus_2v):
        return PullbackDecision(
            candidate=candidate,
            decision="reject_degenerate_rank1_mixed_module",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="nondegenerate rank-2 mixed right-character module",
            next_action="discard rank-1-only constructions on u+2v=0",
            ok=True,
        )

    if not candidate.not_x_only_even_table:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_x_only_inversion_even_table",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="y/odd-orientation payload, not an x-only even table",
            next_action="route only anti-invariant or odd-oriented objects",
            ok=True,
        )

    if not candidate.active_c_side_odd_orientation:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_missing_active_c_side_odd_orientation",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="active C-side odd orientation",
            next_action="do not accept scalar sign tags without C-side orientation",
            ok=True,
        )

    if not candidate.orientation_not_plain_c_character:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_plain_c_character_or_sign_tag",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="orientation not reducible to a plain C-character phase",
            next_action="require coupled support, not scalar-normalized C-character labels",
            ok=True,
        )

    if not candidate.coupled_d_segment:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_point_quotient_missing_d_segment",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="coupled D segment in the translated odd quotient skeleton",
            next_action="reject point quotients and pure edge controls without D_segment",
            ok=True,
        )

    if not candidate.primitive_k_trace:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_missing_or_nonprimitive_k_trace",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="primitive full K trace",
            next_action="reject missing, collapsed, nonprimitive, or subtrace K payloads",
            ok=True,
        )

    if not candidate.recorded_t_edge_2_113:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_wrong_translated_edge",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="translated quotient edge T=(2,113)",
            next_action="remap to the recorded anti-invariant edge or discard",
            ok=True,
        )

    if not candidate.raw_kernel_gauge_only:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_non_kernel_raw_representative_shift",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="raw representatives normalized only by kernel gauge",
            next_action="reject non-kernel shifts that change the raw source graph",
            ok=True,
        )

    if not (candidate.raw_vector_or_bridge_harness or candidate.curved_corner_shape):
        return PullbackDecision(
            candidate=candidate,
            decision="conditional_no_raw_harness_or_curved_corner_payload",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="raw theta31/bridge vector or curved-corner payload",
            next_action="produce a raw vector for the falsifier or the curved-corner finite shape",
            ok=True,
        )

    if candidate.curved_corner_shape and not candidate.curved_corner_unit_triangle:
        return PullbackDecision(
            candidate=candidate,
            decision="reject_curved_corner_without_unit_triangle_law",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="primitive unit sign and branch coefficient forcing the curved-corner row triangle",
            next_action="reroute through the curved-corner producer intake with --unit-triangle or discard",
            ok=True,
        )

    if not candidate.finite_value_or_divisor_theorem:
        if candidate.curved_corner_shape and not candidate.raw_vector_or_bridge_harness:
            decision = "helper_only_curved_corner_payload_value_theorem_missing"
            missing = "finite value/divisor theorem for the curved K-traced corner payload"
            action = "keep as a 75-atom helper; ask for the value/divisor theorem"
        else:
            decision = "helper_only_raw_bridge_payload_value_theorem_missing"
            missing = "finite value/divisor theorem for the raw theta31 or bridge payload"
            action = "keep as a finite harness hit; ask for the arithmetic value theorem"
        return PullbackDecision(
            candidate=candidate,
            decision=decision,
            finite_shape_reached=True,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier=missing,
            next_action=action,
            ok=True,
        )

    if not candidate.period156_context:
        return PullbackDecision(
            candidate=candidate,
            decision="conditional_missing_period156_context",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="period-156 branch/root/telescoping context",
            next_action="attach period-156 context before trusting the finite value identity",
            ok=True,
        )

    if not candidate.arithmetic_source_theorem:
        return PullbackDecision(
            candidate=candidate,
            decision="conditional_finite_payload_without_source_theorem",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            next_action="keep as finite verifier payload only",
            ok=True,
        )

    if not candidate.danger3_framing:
        return PullbackDecision(
            candidate=candidate,
            decision="source_theorem_closed_policy_or_framing_missing",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=True,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            next_action="settle framing, then seek the same-j X_1(8112) bridge",
            ok=True,
        )

    if not candidate.same_j_x18112_bridge:
        return PullbackDecision(
            candidate=candidate,
            decision="danger3_unblocked_cross_level_bridge_missing",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="same-j X_1(8112) bridge or equivalent cross-level map",
            next_action="derive the bridge to the practical X_1(16) chart",
            ok=True,
        )

    if not candidate.x16_surface:
        return PullbackDecision(
            candidate=candidate,
            decision="cross_level_target_identified_specialization_missing",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="specialized X_1(16) y, A, and xP16 surface",
            next_action="specialize the same-j bridge to X_1(16)",
            ok=True,
        )

    if not candidate.concrete_A_x0:
        return PullbackDecision(
            candidate=candidate,
            decision="x16_surface_reached_halving_or_vpp_missing",
            finite_shape_reached=True,
            finite_value_reached=True,
            source_stage_closed=True,
            danger3_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="halving chain or direct concrete x0",
            next_action="derive x0 and verify with official vpp.py",
            ok=True,
        )

    return PullbackDecision(
        candidate=candidate,
        decision="extraction_ready_vpp_missing",
        finite_shape_reached=True,
        finite_value_reached=True,
        source_stage_closed=True,
        danger3_unblocked=True,
        cross_level_bridge_identified=True,
        x16_surface_reached=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_or_falsifier="official vpp.py verification",
        next_action="run official vpp.py on concrete p25 (p,A,x0)",
        ok=True,
    )


def base_candidate() -> dict[str, bool]:
    return {
        "theorem_body_verified": True,
        "ray_local_inert_right_source": True,
        "split_c_axis_source": True,
        "source_coupling_not_separated": True,
        "residue_rectangles_constant": True,
        "mixed_rank2_non_degenerate": True,
        "avoids_degenerate_u_plus_2v": True,
        "not_x_only_even_table": True,
        "active_c_side_odd_orientation": True,
        "orientation_not_plain_c_character": True,
        "coupled_d_segment": True,
        "primitive_k_trace": True,
        "recorded_t_edge_2_113": True,
        "raw_kernel_gauge_only": True,
        "raw_vector_or_bridge_harness": False,
        "curved_corner_shape": False,
        "curved_corner_unit_triangle": False,
        "finite_value_or_divisor_theorem": False,
        "period156_context": False,
        "arithmetic_source_theorem": False,
        "danger3_framing": False,
        "same_j_x18112_bridge": False,
        "x16_surface": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }


def regression_candidates() -> tuple[PullbackCandidate, ...]:
    base = base_candidate()
    value_ready = {
        **base,
        "raw_vector_or_bridge_harness": True,
        "finite_value_or_divisor_theorem": True,
    }
    source_ready = {
        **value_ready,
        "period156_context": True,
        "arithmetic_source_theorem": True,
    }
    danger3_ready = {**source_ready, "danger3_framing": True}
    same_j_ready = {**danger3_ready, "same_j_x18112_bridge": True}
    x16_ready = {**same_j_ready, "x16_surface": True}
    x0_ready = {**x16_ready, "concrete_A_x0": True}

    return (
        PullbackCandidate("no_theorem_body", **{**base, "theorem_body_verified": False}),
        PullbackCandidate(
            "split_prime_only_source",
            **{**base, "ray_local_inert_right_source": False},
        ),
        PullbackCandidate(
            "separated_source_selector",
            **{**base, "source_coupling_not_separated": False},
        ),
        PullbackCandidate(
            "non_rectangle_pullback",
            **{**base, "residue_rectangles_constant": False},
        ),
        PullbackCandidate(
            "degenerate_rank1_mixed_module",
            **{**base, "mixed_rank2_non_degenerate": False},
        ),
        PullbackCandidate("x_only_even_table", **{**base, "not_x_only_even_table": False}),
        PullbackCandidate(
            "missing_c_odd_orientation",
            **{**base, "active_c_side_odd_orientation": False},
        ),
        PullbackCandidate(
            "plain_c_character_phase",
            **{**base, "orientation_not_plain_c_character": False},
        ),
        PullbackCandidate("point_quotient_no_d_segment", **{**base, "coupled_d_segment": False}),
        PullbackCandidate("missing_k_trace", **{**base, "primitive_k_trace": False}),
        PullbackCandidate("wrong_t_edge", **{**base, "recorded_t_edge_2_113": False}),
        PullbackCandidate("non_kernel_raw_shift", **{**base, "raw_kernel_gauge_only": False}),
        PullbackCandidate("local_pullback_no_payload", **base),
        PullbackCandidate(
            "raw_bridge_payload_helper",
            **{**base, "raw_vector_or_bridge_harness": True},
        ),
        PullbackCandidate(
            "curved_corner_without_unit_triangle",
            **{**base, "curved_corner_shape": True},
        ),
        PullbackCandidate(
            "curved_corner_payload_helper",
            **{**base, "curved_corner_shape": True, "curved_corner_unit_triangle": True},
        ),
        PullbackCandidate("value_no_period156", **value_ready),
        PullbackCandidate(
            "period156_no_source",
            **{**value_ready, "period156_context": True},
        ),
        PullbackCandidate("source_no_framing", **source_ready),
        PullbackCandidate("danger3_no_same_j", **danger3_ready),
        PullbackCandidate("same_j_no_x16", **same_j_ready),
        PullbackCandidate("x16_no_x0", **x16_ready),
        PullbackCandidate("x0_no_vpp", **x0_ready),
        PullbackCandidate("official_vpp_verified", **{**x0_ready, "official_vpp": True}),
    )


def dependency_markers() -> dict[str, bool]:
    return {
        "cm_artin": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_cm_artin_sources.md",
            r"cm_artin_local_source_rows\s*=\s*3\s*/\s*3",
        ),
        "local_pullback": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_local_pullback.md",
            r"local_pullback_rows\s*=\s*3\s*/\s*3",
        ),
        "residue_coset": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_residue_coset_mask.md",
            r"residue_coset_mask_rows\s*=\s*3\s*/\s*3",
        ),
        "source_half_arc": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_source_half_arc_lift.md",
            r"source_half_arc_lift_rows\s*=\s*3\s*/\s*3",
        ),
        "mixed_character": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_mixed_character_module.md",
            r"mixed_character_module_rows\s*=\s*3\s*/\s*3",
        ),
        "ray_local_theta31": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_ray_local_theta31_pullback_falsifier.md",
            r"ray_local_theta31_pullback_rows\s*=\s*1\s*/\s*1",
        ),
        "bridge_harness": regex_marker_present(
            RESEARCH / "run_status.md",
            r"square_axis_bridge_candidate_harness_rows\s*=\s*1\s*/\s*1",
        ),
        "anti_invariant_contract": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract.md",
            r"robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_rows\s*=\s*1\s*/\s*1",
        ),
        "curved_corner_intake": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_corner_producer_intake.md",
            r"square_axis_bridge_hilbert90_corner_producer_intake_rows\s*=\s*1\s*/\s*1",
        ),
        "curved_corner_unit_triangle": regex_marker_present(
            RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle.md",
            r"square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_rows\s*=\s*1\s*/\s*1",
        ),
    }


def profile_ray_local_modular_unit_pullback_router() -> RayLocalPullbackRouterProfile:
    markers = dependency_markers()
    decisions = tuple(classify_candidate(candidate) for candidate in regression_candidates())
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    helper = sum(row.decision.startswith("helper_only_") for row in decisions)
    conditional = sum(row.decision.startswith("conditional_") for row in decisions)
    finite_shape = sum(row.finite_shape_reached for row in decisions)
    finite_value = sum(row.finite_value_reached for row in decisions)
    source_closing = sum(row.source_stage_closed for row in decisions)
    danger3 = sum(row.danger3_unblocked for row in decisions)
    cross_level = sum(row.cross_level_bridge_identified for row in decisions)
    x16_surface = sum(row.x16_surface_reached for row in decisions)
    extraction = sum(row.extraction_ready for row in decisions)
    submission = sum(row.submission_ready for row in decisions)
    expected_decisions = (
        "reject_no_theorem_body",
        "reject_not_ray_local_inert_split_source",
        "reject_separated_or_pure_c_source",
        "reject_not_residue_rectangle_pullback",
        "reject_degenerate_rank1_mixed_module",
        "reject_x_only_inversion_even_table",
        "reject_missing_active_c_side_odd_orientation",
        "reject_plain_c_character_or_sign_tag",
        "reject_point_quotient_missing_d_segment",
        "reject_missing_or_nonprimitive_k_trace",
        "reject_wrong_translated_edge",
        "reject_non_kernel_raw_representative_shift",
        "conditional_no_raw_harness_or_curved_corner_payload",
        "helper_only_raw_bridge_payload_value_theorem_missing",
        "reject_curved_corner_without_unit_triangle_law",
        "helper_only_curved_corner_payload_value_theorem_missing",
        "conditional_missing_period156_context",
        "conditional_finite_payload_without_source_theorem",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    dependency_ok = all(markers.values())
    row_ok = (
        dependency_ok
        and len(decisions) == 24
        and rejected == 13
        and helper == 2
        and conditional == 3
        and finite_shape == 10
        and finite_value == 8
        and source_closing == 6
        and danger3 == 5
        and cross_level == 4
        and x16_surface == 3
        and extraction == 2
        and submission == 1
        and tuple(row.decision for row in decisions) == expected_decisions
        and all(row.ok for row in decisions)
    )
    return RayLocalPullbackRouterProfile(
        cm_artin_marker_present=markers["cm_artin"],
        local_pullback_marker_present=markers["local_pullback"],
        residue_coset_marker_present=markers["residue_coset"],
        source_half_arc_marker_present=markers["source_half_arc"],
        mixed_character_marker_present=markers["mixed_character"],
        ray_local_theta31_falsifier_marker_present=markers["ray_local_theta31"],
        bridge_harness_marker_present=markers["bridge_harness"],
        anti_invariant_contract_marker_present=markers["anti_invariant_contract"],
        curved_corner_intake_marker_present=markers["curved_corner_intake"],
        curved_corner_unit_triangle_marker_present=markers["curved_corner_unit_triangle"],
        dependency_markers_ok=dependency_ok,
        right_source_prime=151,
        c_axis_source_prime=677,
        quotient_rectangles=39,
        residue_rectangle_size=325,
        raw_order=12675,
        carrying_rectangles=18,
        raw_carry_one_positions=5850,
        bridge_mixed_characters=336,
        compact_curved_corner_atoms=75,
        required_translated_edge=(2, 113),
        rows=decisions,
        row_count=len(decisions),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        finite_shape_rows=finite_shape,
        finite_value_rows=finite_value,
        source_closing_rows=source_closing,
        danger3_unblocked_rows=danger3,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> PullbackCandidate:
    return PullbackCandidate(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        ray_local_inert_right_source=args.ray_local,
        split_c_axis_source=args.split_c,
        source_coupling_not_separated=args.coupled,
        residue_rectangles_constant=args.rectangles,
        mixed_rank2_non_degenerate=args.rank2,
        avoids_degenerate_u_plus_2v=args.avoid_degenerate,
        not_x_only_even_table=args.not_x_only,
        active_c_side_odd_orientation=args.c_odd,
        orientation_not_plain_c_character=args.not_c_character,
        coupled_d_segment=args.d_segment,
        primitive_k_trace=args.k_trace,
        recorded_t_edge_2_113=args.t_edge,
        raw_kernel_gauge_only=args.kernel_gauge,
        raw_vector_or_bridge_harness=args.raw_bridge,
        curved_corner_shape=args.curved_corner,
        curved_corner_unit_triangle=args.unit_triangle,
        finite_value_or_divisor_theorem=args.finite_or_divisor,
        period156_context=args.period_156,
        arithmetic_source_theorem=args.arithmetic_source,
        danger3_framing=args.danger3_framing,
        same_j_x18112_bridge=args.same_j,
        x16_surface=args.x16,
        concrete_A_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(decision: PullbackDecision) -> None:
    candidate = decision.candidate
    print(
        "  "
        f"{candidate.name}: theorem={int(candidate.theorem_body_verified)} "
        f"ray_local={int(candidate.ray_local_inert_right_source)} "
        f"split_c={int(candidate.split_c_axis_source)} "
        f"coupled={int(candidate.source_coupling_not_separated)} "
        f"rectangles={int(candidate.residue_rectangles_constant)} "
        f"rank2={int(candidate.mixed_rank2_non_degenerate)} "
        f"avoid_u2v={int(candidate.avoids_degenerate_u_plus_2v)} "
        f"not_x_only={int(candidate.not_x_only_even_table)} "
        f"c_odd={int(candidate.active_c_side_odd_orientation)} "
        f"not_c_character={int(candidate.orientation_not_plain_c_character)} "
        f"d_segment={int(candidate.coupled_d_segment)} "
        f"k_trace={int(candidate.primitive_k_trace)} "
        f"t_edge={int(candidate.recorded_t_edge_2_113)} "
        f"kernel_gauge={int(candidate.raw_kernel_gauge_only)} "
        f"raw_bridge={int(candidate.raw_vector_or_bridge_harness)} "
        f"curved={int(candidate.curved_corner_shape)} "
        f"unit_triangle={int(candidate.curved_corner_unit_triangle)} "
        f"finite={int(candidate.finite_value_or_divisor_theorem)} "
        f"period156={int(candidate.period156_context)} "
        f"source={int(candidate.arithmetic_source_theorem)} "
        f"danger3={int(candidate.danger3_framing)} "
        f"same_j={int(candidate.same_j_x18112_bridge)} "
        f"x16={int(candidate.x16_surface)} "
        f"x0={int(candidate.concrete_A_x0)} "
        f"vpp={int(candidate.official_vpp)} "
        f"decision={decision.decision} "
        f"shape={int(decision.finite_shape_reached)} "
        f"value={int(decision.finite_value_reached)} "
        f"source_closed={int(decision.source_stage_closed)} "
        f"submission={int(decision.submission_ready)} "
        f"missing={decision.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify ray-local modular-unit pullback theorem claims."
    )
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--ray-local", action="store_true")
    parser.add_argument("--split-c", action="store_true")
    parser.add_argument("--coupled", action="store_true")
    parser.add_argument("--rectangles", action="store_true")
    parser.add_argument("--rank2", action="store_true")
    parser.add_argument("--avoid-degenerate", action="store_true")
    parser.add_argument("--not-x-only", action="store_true")
    parser.add_argument("--c-odd", action="store_true")
    parser.add_argument("--not-c-character", action="store_true")
    parser.add_argument("--d-segment", action="store_true")
    parser.add_argument("--k-trace", action="store_true")
    parser.add_argument("--t-edge", action="store_true")
    parser.add_argument("--kernel-gauge", action="store_true")
    parser.add_argument("--raw-bridge", action="store_true")
    parser.add_argument("--curved-corner", action="store_true")
    parser.add_argument("--unit-triangle", action="store_true")
    parser.add_argument("--finite-or-divisor", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--arithmetic-source", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--x16", action="store_true")
    parser.add_argument("--x0", action="store_true")
    parser.add_argument("--vpp", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B ray-local modular-unit pullback router gate")
    if args.candidate:
        decision = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(f"ray_local_modular_unit_pullback_router_candidate_rows={int(decision.ok)}/1")
        return 0 if decision.ok else 1

    profile = profile_ray_local_modular_unit_pullback_router()
    print("dependencies")
    print(f"  cm_artin_marker_present={int(profile.cm_artin_marker_present)}")
    print(f"  local_pullback_marker_present={int(profile.local_pullback_marker_present)}")
    print(f"  residue_coset_marker_present={int(profile.residue_coset_marker_present)}")
    print(f"  source_half_arc_marker_present={int(profile.source_half_arc_marker_present)}")
    print(f"  mixed_character_marker_present={int(profile.mixed_character_marker_present)}")
    print(
        "  ray_local_theta31_falsifier_marker_present="
        f"{int(profile.ray_local_theta31_falsifier_marker_present)}"
    )
    print(f"  bridge_harness_marker_present={int(profile.bridge_harness_marker_present)}")
    print(
        "  anti_invariant_contract_marker_present="
        f"{int(profile.anti_invariant_contract_marker_present)}"
    )
    print(
        "  curved_corner_intake_marker_present="
        f"{int(profile.curved_corner_intake_marker_present)}"
    )
    print(
        "  curved_corner_unit_triangle_marker_present="
        f"{int(profile.curved_corner_unit_triangle_marker_present)}"
    )
    print(f"  dependency_markers_ok={int(profile.dependency_markers_ok)}")
    print("local_target")
    print(f"  right_source_prime={profile.right_source_prime}")
    print(f"  c_axis_source_prime={profile.c_axis_source_prime}")
    print(f"  quotient_rectangles={profile.quotient_rectangles}")
    print(f"  residue_rectangle_size={profile.residue_rectangle_size}")
    print(f"  raw_order={profile.raw_order}")
    print(f"  carrying_rectangles={profile.carrying_rectangles}")
    print(f"  raw_carry_one_positions={profile.raw_carry_one_positions}")
    print(f"  bridge_mixed_characters={profile.bridge_mixed_characters}")
    print(f"  compact_curved_corner_atoms={profile.compact_curved_corner_atoms}")
    print(f"  required_translated_edge={profile.required_translated_edge}")
    print("regression_rows")
    for decision in profile.rows:
        print_decision(decision)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  finite_shape_rows={profile.finite_shape_rows}")
    print(f"  finite_value_rows={profile.finite_value_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  pullback_claims_must_couple_inert_151_to_split_677=1")
    print("  separated_pure_C_rank1_and_x_only_even_claims_are_first_rejects=1")
    print("  curved_corner_payload_must_include_unit_triangle_law=1")
    print("  raw_or_curved_finite_shape_is_helper_only_until_value_theorem=1")
    print("  source_theorem_closure_still_routes_through_DANGER3_and_vpp=1")
    print(f"ray_local_modular_unit_pullback_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("ray-local modular-unit pullback router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
