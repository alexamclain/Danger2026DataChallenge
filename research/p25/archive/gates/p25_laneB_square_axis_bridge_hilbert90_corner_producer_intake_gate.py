#!/usr/bin/env python3
"""Producer intake for the curved Hilbert-90 corner target.

The square-axis bridge route has compressed the finite target to a rigid
source-row triangle plus the full order-25 K trace.  This gate classifies
future arithmetic producer claims against that exact shape before routing a
successful theorem through the DANGER3 ladder.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_gate import (
    k_trace_minimality_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_gate import (
    row_newton_triangle_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate import (
    profile as raw_k_trace_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate import (
    triangle_edge_profile,
)
from p25_laneB_square_axis_bridge_factor_kummer_gate import (
    BRIDGE_SHIFT,
    C_ORDER,
    D_CUBED_SHIFT,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    Y_RAW_SHIFT,
    factor_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_raw_kummer_gate import (
    raw_kummer_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_gate import (
    corner_c169_lift_selector_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    corner_fiber_section_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_gate import (
    row_polynomial_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_gate import (
    fiber_covariance_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_gate import (
    unit_triangle_profile,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class CornerProducerCandidate:
    name: str
    theorem_body_verified: bool
    exact_curved_row_triangle: bool
    primitive_newton_curvature: bool
    recorded_half_bridge_edge: bool
    full_order25_k_trace: bool
    raw_d3_y_relation: bool
    raw_kernel_trace_accounted: bool
    primitive_c169_motion: bool
    active_c169_lift_selected: bool
    quadratic_fiber_section: bool
    nonsplit_c169_carry_transport: bool
    unit_triangle_law: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    arithmetic_source_theorem: bool
    danger3_framing: bool
    same_j_x18112_bridge: bool
    x16_surface: bool
    concrete_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class CornerProducerDecision:
    candidate: CornerProducerCandidate
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
class CornerProducerIntakeProfile:
    newton_triangle_marker_present: bool
    k_trace_minimality_marker_present: bool
    raw_k_trace_marker_present: bool
    triangle_edge_marker_present: bool
    factor_kummer_marker_present: bool
    raw_kummer_marker_present: bool
    c169_lift_selector_marker_present: bool
    fiber_section_marker_present: bool
    row_polynomial_marker_present: bool
    fiber_covariance_marker_present: bool
    unit_triangle_marker_present: bool
    dependency_facts_ok: bool
    kummer_dependency_facts_ok: bool
    lift_dependency_facts_ok: bool
    unit_dependency_facts_ok: bool
    canonical_q_newton: tuple[int, int, int]
    canonical_c169_newton: tuple[int, int, int]
    canonical_d_newton: tuple[int, int, int]
    d_edge_q_images: tuple[tuple[int, int], ...]
    unique_k_invariant_corner_support: int
    trace_correct_raw_relation_rows: int
    kernel_trace_shift: tuple[int, int]
    d_segment_combined_order: int
    bridge_edge_combined_order: int
    sparse_direction_count: int
    primitive_c169_direction_rows: int
    right_order_three_available_rows: int
    canonical_c13_shadow: tuple[int, int, int]
    canonical_bridge_lift: tuple[int, int, int]
    inactive_c169_lift_count: int
    canonical_quadratic_section: tuple[int, int, int]
    canonical_row_values_c169: tuple[int, int, int]
    canonical_row_q_values: tuple[int, int, int]
    covariance_row_count: int
    nonsplit_carry_needed_rows: int
    no_carry_success_rows: int
    unit_triangle_row_count: int
    unit_triangle_off_line_rows: tuple[tuple[int, int, int], ...]
    unit_triangle_off_line_points: tuple[tuple[int, int, tuple[int, int]], ...]
    rows: tuple[CornerProducerDecision, ...]
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


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def classify_candidate(candidate: CornerProducerCandidate) -> CornerProducerDecision:
    if candidate.official_vpp and candidate.concrete_A_x0:
        return CornerProducerDecision(
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
            next_action="archive official vpp output, command, environment, and certificate",
            ok=True,
        )

    if not candidate.theorem_body_verified:
        return CornerProducerDecision(
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
            next_action="obtain theorem text before routing the producer claim",
            ok=True,
        )

    if not candidate.exact_curved_row_triangle:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_wrong_source_triangle",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="exact source-row triangle with q edges 25,172,310",
            next_action="remap to the recorded curved row triangle or discard",
            ok=True,
        )

    if not candidate.primitive_newton_curvature:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_linearized_source_graph",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="primitive Newton curvature, not a source line or AP",
            next_action="kill line/AP interpretations of the corner producer",
            ok=True,
        )

    if not candidate.recorded_half_bridge_edge:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_wrong_half_bridge_edge",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="recorded negative-polarity half-bridge edge 197/310",
            next_action="use the half-bridge triangle edge, not another one-cancellation edge",
            ok=True,
        )

    if not candidate.full_order25_k_trace:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_sparse_or_subtrace_k_lift",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="full order-25 K trace on each nonzero corner block",
            next_action="reject sparse sections and order-1/order-5 K-subtraces",
            ok=True,
        )

    if not candidate.raw_d3_y_relation:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_raw_d3_y_relation_failure",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="raw D^3=Y relation / K-boundary compatibility",
            next_action="repair the raw lift; hidden trace-zero modes are not enough",
            ok=True,
        )

    if not candidate.raw_kernel_trace_accounted:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_raw_kernel_trace_omitted",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="raw kernel trace shift D^3 - Y = (57,0)",
            next_action="account for the invisible C_25 kernel trace instead of using quotient D^3=Y as raw equality",
            ok=True,
        )

    if not candidate.primitive_c169_motion:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_c13_shadow_or_right_kernel_only",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="primitive C_169 source motion with Kummer degree 169",
            next_action="reject cheap right-kernel gauges and C_13 shadows unless the primitive C_169 lift is realized",
            ok=True,
        )

    if not candidate.active_c169_lift_selected:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_generic_primitive_c169_lift",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="active projective C_169 lift (1,18,150)",
            next_action="reject generic primitive C_169 lifts with the same C_13 shadow",
            ok=True,
        )

    if not candidate.quadratic_fiber_section:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_teichmuller_or_affine_fiber_shortcut",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="quadratic C_13-to-C_169 fiber section f(c0)=c0*(c0-3)",
            next_action="reject Teichmuller lifts, affine fiber gauges, and unrelated primitive lifts",
            ok=True,
        )

    if not candidate.nonsplit_c169_carry_transport:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_split_no_carry_fiber_transport",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="nonsplit C_169 carry law transporting the quadratic fiber section",
            next_action="reject split C_13 x C_13 no-carry transport models",
            ok=True,
        )

    if not candidate.unit_triangle_law:
        return CornerProducerDecision(
            candidate=candidate,
            decision="reject_passive_or_wrong_unit_triangle",
            finite_shape_reached=False,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="primitive unit sign and branch coefficient forcing the row-labeled triangle",
            next_action="reject passive third-point fits and wrong unit/branch row placements",
            ok=True,
        )

    if not candidate.finite_value_or_divisor_theorem:
        return CornerProducerDecision(
            candidate=candidate,
            decision="helper_only_curved_triangle_value_theorem_missing",
            finite_shape_reached=True,
            finite_value_reached=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="finite value/divisor theorem for the curved K-traced corner payload",
            next_action="keep as producer helper; ask for value/divisor theorem",
            ok=True,
        )

    if not candidate.period156_context:
        return CornerProducerDecision(
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
            next_action="attach support-period fixedness before trusting the finite value",
            ok=True,
        )

    if not candidate.arithmetic_source_theorem:
        return CornerProducerDecision(
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
        return CornerProducerDecision(
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
            next_action="settle framing, then seek same-j X1(8112) bridge",
            ok=True,
        )

    if not candidate.same_j_x18112_bridge:
        return CornerProducerDecision(
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
        return CornerProducerDecision(
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
        return CornerProducerDecision(
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

    return CornerProducerDecision(
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


def regression_candidates() -> tuple[CornerProducerCandidate, ...]:
    base = {
        "theorem_body_verified": True,
        "exact_curved_row_triangle": True,
        "primitive_newton_curvature": True,
        "recorded_half_bridge_edge": True,
        "full_order25_k_trace": True,
        "raw_d3_y_relation": True,
        "raw_kernel_trace_accounted": True,
        "primitive_c169_motion": True,
        "active_c169_lift_selected": True,
        "quadratic_fiber_section": True,
        "nonsplit_c169_carry_transport": True,
        "unit_triangle_law": True,
        "finite_value_or_divisor_theorem": False,
        "period156_context": False,
        "arithmetic_source_theorem": False,
        "danger3_framing": False,
        "same_j_x18112_bridge": False,
        "x16_surface": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }
    return (
        CornerProducerCandidate("no_theorem_body", **{**base, "theorem_body_verified": False}),
        CornerProducerCandidate("wrong_source_triangle", **{**base, "exact_curved_row_triangle": False}),
        CornerProducerCandidate("linearized_source_graph", **{**base, "primitive_newton_curvature": False}),
        CornerProducerCandidate("wrong_half_bridge_edge", **{**base, "recorded_half_bridge_edge": False}),
        CornerProducerCandidate("sparse_or_k5_subtrace", **{**base, "full_order25_k_trace": False}),
        CornerProducerCandidate("hidden_mode_relation_failure", **{**base, "raw_d3_y_relation": False}),
        CornerProducerCandidate("raw_kernel_trace_omitted", **{**base, "raw_kernel_trace_accounted": False}),
        CornerProducerCandidate("c13_shadow_or_right_kernel_only", **{**base, "primitive_c169_motion": False}),
        CornerProducerCandidate("generic_primitive_c169_lift", **{**base, "active_c169_lift_selected": False}),
        CornerProducerCandidate("teichmuller_or_affine_fiber_shortcut", **{**base, "quadratic_fiber_section": False}),
        CornerProducerCandidate("split_no_carry_fiber_transport", **{**base, "nonsplit_c169_carry_transport": False}),
        CornerProducerCandidate("passive_or_wrong_unit_triangle", **{**base, "unit_triangle_law": False}),
        CornerProducerCandidate("curved_triangle_helper_only", **base),
        CornerProducerCandidate(
            "curved_triangle_value_no_period156",
            **{**base, "finite_value_or_divisor_theorem": True},
        ),
        CornerProducerCandidate(
            "curved_triangle_period156_no_source",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
            },
        ),
        CornerProducerCandidate(
            "curved_triangle_source_no_framing",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
            },
        ),
        CornerProducerCandidate(
            "danger3_framed_no_same_j",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
            },
        ),
        CornerProducerCandidate(
            "same_j_bridge_no_x16",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "same_j_x18112_bridge": True,
            },
        ),
        CornerProducerCandidate(
            "x16_surface_no_x0",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "same_j_x18112_bridge": True,
                "x16_surface": True,
            },
        ),
        CornerProducerCandidate(
            "concrete_A_x0_no_vpp",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "same_j_x18112_bridge": True,
                "x16_surface": True,
                "concrete_A_x0": True,
            },
        ),
        CornerProducerCandidate(
            "official_vpp_verified",
            **{
                **base,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "same_j_x18112_bridge": True,
                "x16_surface": True,
                "concrete_A_x0": True,
                "official_vpp": True,
            },
        ),
    )


def dependency_facts_ok() -> tuple[bool, tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[tuple[int, int], ...], int, int]:
    newton = row_newton_triangle_profile()
    k_min = k_trace_minimality_profile()
    raw_k = raw_k_trace_profile()
    triangle = triangle_edge_profile()
    ok = (
        newton.row_count == 4
        and newton.canonical_q_newton == (0, 172, 138)
        and newton.canonical_c169_newton == (0, 3, 138)
        and newton.canonical_d_newton == (0, 1, 384)
        and newton.d_edge_q_images == ((1, 172), (121, 25), (385, 310))
        and newton.all_rows_are_the_same_newton_triangle
        and k_min.unique_k_invariant_corner_support == 75
        and k_min.only_full_subtraces_are_k_invariant
        and raw_k.trace_correct_raw_relation_rows == 4
        and raw_k.all_block_k_trace_rows_pass
        and triangle.all_rows_have_standard_directed_edge_set
        and triangle.all_half_bridge_edges_are_197_310
        and triangle.all_recorded_edges_are_negative_half_bridge_polarity
    )
    return (
        ok,
        newton.canonical_q_newton,
        newton.canonical_c169_newton,
        newton.canonical_d_newton,
        newton.d_edge_q_images,
        k_min.unique_k_invariant_corner_support,
        raw_k.trace_correct_raw_relation_rows,
    )


def kummer_dependency_facts_ok() -> tuple[bool, tuple[int, int], int, int, int, int, int]:
    kernel = factor_profile("kernel_trace", KERNEL_SHIFT)
    d_segment = factor_profile("D_segment", D_SHIFT)
    bridge_edge = factor_profile("bridge_edge", BRIDGE_SHIFT)
    raw = raw_kummer_profile()
    kernel_trace_shift = (
        (D_CUBED_SHIFT[0] - Y_RAW_SHIFT[0]) % RIGHT_ORDER,
        (D_CUBED_SHIFT[1] - Y_RAW_SHIFT[1]) % C_ORDER,
    )
    primitive_c169_rows = sum(
        row.c_order_values == (C_ORDER,)
        and row.c_c169_min_degrees == (C_ORDER,)
        and row.c_c13_min_degrees == (13,)
        for row in raw.direction_rows
    )
    right_order_three_rows = sum(
        row.right_order_histogram == ((3, 1), (15, 4), (75, 20))
        for row in raw.direction_rows
    )
    ok = (
        kernel_trace_shift == KERNEL_SHIFT
        and kernel.combined_order == 25
        and kernel.right_c75_min_degree == 25
        and kernel.c_c169_min_degree == 1
        and d_segment.combined_order == 12675
        and d_segment.right_c75_min_degree == 75
        and d_segment.c_c169_min_degree == 169
        and bridge_edge.combined_order == 12675
        and bridge_edge.right_c75_min_degree == 75
        and bridge_edge.c_c169_min_degree == 169
        and raw.sparse_direction_count == 6
        and primitive_c169_rows == 6
        and right_order_three_rows == 6
        and raw.all_sparse_directions_have_primitive_c169_cost
        and raw.all_sparse_directions_have_kernel_gauge_right_order_three
        and raw.all_sparse_directions_have_min_combined_order_507
    )
    return (
        ok,
        kernel_trace_shift,
        d_segment.combined_order,
        bridge_edge.combined_order,
        raw.sparse_direction_count,
        primitive_c169_rows,
        right_order_three_rows,
    )


def lift_dependency_facts_ok() -> tuple[bool, tuple[int, int, int], tuple[int, int, int], int, tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], int, int, int]:
    selector = corner_c169_lift_selector_profile()
    fiber = corner_fiber_section_profile()
    row_poly = row_polynomial_profile()
    covariance = fiber_covariance_profile()
    ok = (
        selector.canonical_c13_shadow == (1, 2, 10)
        and selector.canonical_bridge_lift == (1, 18, 150)
        and selector.c13_lift_count == 13
        and selector.active_lift_count == 1
        and selector.inactive_lift_count == 12
        and selector.all_corner_graphs_use_canonical_lift
        and selector.all_other_c13_lifts_inactive
        and fiber.row_count == 4
        and fiber.canonical_quadratic_section == (1, 10, 0)
        and fiber.no_row_is_teichmuller_lift
        and fiber.no_row_has_affine_fiber_section
        and fiber.all_rows_are_genuine_quadratic_sections
        and fiber.all_quadratic_sections_match_active_lift
        and row_poly.c13_row_polynomial == (4, 12, 0)
        and row_poly.fiber_row_polynomial == (12, 1, 0)
        and row_poly.fiber_shadow_polynomial == (1, 10, 0)
        and row_poly.row_values_c169 == (0, 3, 144)
        and row_poly.q_values == (0, 172, 482)
        and row_poly.all_rows_match_row_polynomial
        and row_poly.all_rows_match_shadow_polynomial
        and row_poly.row_graph_is_source_graph
        and row_poly.no_carry_transport_failure_count == 2
        and covariance.row_count == 4
        and covariance.all_rows_are_source_affine_images
        and covariance.all_quadratic_sections_transport_correctly
        and covariance.nonsplit_carry_needed_row_count == 2
        and covariance.no_carry_success_row_count == 2
        and covariance.canonical_source_section == ((0, 0), (3, 0), (1, 11))
        and covariance.canonical_quadratic_section == (1, 10, 0)
    )
    return (
        ok,
        selector.canonical_c13_shadow,
        selector.canonical_bridge_lift,
        selector.inactive_lift_count,
        fiber.canonical_quadratic_section,
        row_poly.row_values_c169,
        row_poly.q_values,
        covariance.row_count,
        covariance.nonsplit_carry_needed_row_count,
        covariance.no_carry_success_row_count,
    )


def unit_dependency_facts_ok() -> tuple[bool, int, tuple[tuple[int, int, int], ...], tuple[tuple[int, int, tuple[int, int]], ...]]:
    unit = unit_triangle_profile()
    ok = (
        unit.row_count == 4
        and unit.all_source_rows_forced_by_unit_sign_and_branch
        and unit.all_points_forced_by_unit_sign_and_branch
        and unit.all_line_residuals_forced_by_unit_sign_and_branch
        and unit.off_line_rows_by_unit_sign_and_branch == (
            (-1, -1, 1),
            (-1, 1, 0),
            (1, -1, 0),
            (1, 1, 2),
        )
        and unit.off_line_points_by_unit_sign_and_branch == (
            (-1, -1, (11, 10)),
            (-1, 1, (0, 0)),
            (1, -1, (0, 0)),
            (1, 1, (2, 2)),
        )
    )
    return (
        ok,
        unit.row_count,
        unit.off_line_rows_by_unit_sign_and_branch,
        unit.off_line_points_by_unit_sign_and_branch,
    )


def profile_corner_producer_intake() -> CornerProducerIntakeProfile:
    deps_ok, q_newton, c_newton, d_newton, edge_images, k_support, raw_relation_rows = dependency_facts_ok()
    (
        kummer_deps_ok,
        kernel_trace_shift,
        d_segment_order,
        bridge_edge_order,
        sparse_direction_count,
        primitive_c169_rows,
        right_order_three_rows,
    ) = kummer_dependency_facts_ok()
    (
        lift_deps_ok,
        canonical_c13_shadow,
        canonical_bridge_lift,
        inactive_lift_count,
        canonical_quadratic_section,
        canonical_row_values_c169,
        canonical_row_q_values,
        covariance_row_count,
        nonsplit_carry_needed_rows,
        no_carry_success_rows,
    ) = lift_dependency_facts_ok()
    (
        unit_deps_ok,
        unit_triangle_rows,
        unit_off_line_rows,
        unit_off_line_points,
    ) = unit_dependency_facts_ok()
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
        "reject_wrong_source_triangle",
        "reject_linearized_source_graph",
        "reject_wrong_half_bridge_edge",
        "reject_sparse_or_subtrace_k_lift",
        "reject_raw_d3_y_relation_failure",
        "reject_raw_kernel_trace_omitted",
        "reject_c13_shadow_or_right_kernel_only",
        "reject_generic_primitive_c169_lift",
        "reject_teichmuller_or_affine_fiber_shortcut",
        "reject_split_no_carry_fiber_transport",
        "reject_passive_or_wrong_unit_triangle",
        "helper_only_curved_triangle_value_theorem_missing",
        "conditional_missing_period156_context",
        "conditional_finite_payload_without_source_theorem",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    newton_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_newton_triangle.md",
        "square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_rows=1/1",
    )
    k_min_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality.md",
        "square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_rows=1/1",
    )
    raw_k_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace.md",
        "square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_rows=1/1",
    )
    triangle_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge.md",
        "square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_rows=1/1",
    )
    factor_kummer_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_factor_kummer.md",
        "square_axis_bridge_factor_kummer_rows=1/1",
    )
    raw_kummer_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_raw_kummer.md",
        "square_axis_bridge_hilbert90_source_chain_raw_kummer_rows=1/1",
    )
    c169_lift_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector.md",
        "square_axis_bridge_hilbert90_source_chain_corner_c169_lift_selector_rows=1/1",
    )
    fiber_section_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section.md",
        "square_axis_bridge_hilbert90_source_chain_corner_fiber_section_rows=1/1",
    )
    row_polynomial_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial.md",
        "square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_rows=1/1",
    )
    fiber_covariance_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance.md",
        "square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_rows=1/1",
    )
    unit_triangle_marker = marker_present(
        RESEARCH / "subsqrt_moonshot_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle.md",
        "square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_rows=1/1",
    )
    row_ok = (
        newton_marker
        and k_min_marker
        and raw_k_marker
        and triangle_marker
        and factor_kummer_marker
        and raw_kummer_marker
        and c169_lift_marker
        and fiber_section_marker
        and row_polynomial_marker
        and fiber_covariance_marker
        and unit_triangle_marker
        and deps_ok
        and kummer_deps_ok
        and lift_deps_ok
        and unit_deps_ok
        and len(decisions) == 21
        and rejected == 12
        and helper == 1
        and conditional == 2
        and finite_shape == 9
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
    return CornerProducerIntakeProfile(
        newton_triangle_marker_present=newton_marker,
        k_trace_minimality_marker_present=k_min_marker,
        raw_k_trace_marker_present=raw_k_marker,
        triangle_edge_marker_present=triangle_marker,
        factor_kummer_marker_present=factor_kummer_marker,
        raw_kummer_marker_present=raw_kummer_marker,
        c169_lift_selector_marker_present=c169_lift_marker,
        fiber_section_marker_present=fiber_section_marker,
        row_polynomial_marker_present=row_polynomial_marker,
        fiber_covariance_marker_present=fiber_covariance_marker,
        unit_triangle_marker_present=unit_triangle_marker,
        dependency_facts_ok=deps_ok,
        kummer_dependency_facts_ok=kummer_deps_ok,
        lift_dependency_facts_ok=lift_deps_ok,
        unit_dependency_facts_ok=unit_deps_ok,
        canonical_q_newton=q_newton,
        canonical_c169_newton=c_newton,
        canonical_d_newton=d_newton,
        d_edge_q_images=edge_images,
        unique_k_invariant_corner_support=k_support,
        trace_correct_raw_relation_rows=raw_relation_rows,
        kernel_trace_shift=kernel_trace_shift,
        d_segment_combined_order=d_segment_order,
        bridge_edge_combined_order=bridge_edge_order,
        sparse_direction_count=sparse_direction_count,
        primitive_c169_direction_rows=primitive_c169_rows,
        right_order_three_available_rows=right_order_three_rows,
        canonical_c13_shadow=canonical_c13_shadow,
        canonical_bridge_lift=canonical_bridge_lift,
        inactive_c169_lift_count=inactive_lift_count,
        canonical_quadratic_section=canonical_quadratic_section,
        canonical_row_values_c169=canonical_row_values_c169,
        canonical_row_q_values=canonical_row_q_values,
        covariance_row_count=covariance_row_count,
        nonsplit_carry_needed_rows=nonsplit_carry_needed_rows,
        no_carry_success_rows=no_carry_success_rows,
        unit_triangle_row_count=unit_triangle_rows,
        unit_triangle_off_line_rows=unit_off_line_rows,
        unit_triangle_off_line_points=unit_off_line_points,
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


def candidate_from_args(args: argparse.Namespace) -> CornerProducerCandidate:
    return CornerProducerCandidate(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        exact_curved_row_triangle=args.triangle,
        primitive_newton_curvature=args.curvature,
        recorded_half_bridge_edge=args.half_bridge_edge,
        full_order25_k_trace=args.full_k_trace,
        raw_d3_y_relation=args.raw_relation,
        raw_kernel_trace_accounted=args.raw_kernel_trace,
        primitive_c169_motion=args.primitive_c169,
        active_c169_lift_selected=args.active_c169_lift,
        quadratic_fiber_section=args.quadratic_fiber,
        nonsplit_c169_carry_transport=args.nonsplit_carry,
        unit_triangle_law=args.unit_triangle,
        finite_value_or_divisor_theorem=args.finite_or_divisor,
        period156_context=args.period_156,
        arithmetic_source_theorem=args.arithmetic_source,
        danger3_framing=args.danger3_framing,
        same_j_x18112_bridge=args.same_j,
        x16_surface=args.x16,
        concrete_A_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(decision: CornerProducerDecision) -> None:
    candidate = decision.candidate
    print(
        "  "
        f"{candidate.name}: theorem={int(candidate.theorem_body_verified)} "
        f"triangle={int(candidate.exact_curved_row_triangle)} "
        f"curvature={int(candidate.primitive_newton_curvature)} "
        f"half_edge={int(candidate.recorded_half_bridge_edge)} "
        f"k25={int(candidate.full_order25_k_trace)} "
        f"raw_relation={int(candidate.raw_d3_y_relation)} "
        f"raw_kernel_trace={int(candidate.raw_kernel_trace_accounted)} "
        f"primitive_c169={int(candidate.primitive_c169_motion)} "
        f"active_c169_lift={int(candidate.active_c169_lift_selected)} "
        f"quadratic_fiber={int(candidate.quadratic_fiber_section)} "
        f"nonsplit_carry={int(candidate.nonsplit_c169_carry_transport)} "
        f"unit_triangle={int(candidate.unit_triangle_law)} "
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
    parser = argparse.ArgumentParser(description="Classify curved Hilbert-90 corner producer claims.")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--triangle", action="store_true")
    parser.add_argument("--curvature", action="store_true")
    parser.add_argument("--half-bridge-edge", action="store_true")
    parser.add_argument("--full-k-trace", action="store_true")
    parser.add_argument("--raw-relation", action="store_true")
    parser.add_argument("--raw-kernel-trace", action="store_true")
    parser.add_argument("--primitive-c169", action="store_true")
    parser.add_argument("--active-c169-lift", action="store_true")
    parser.add_argument("--quadratic-fiber", action="store_true")
    parser.add_argument("--nonsplit-carry", action="store_true")
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

    print("p25 Lane B square-axis Hilbert-90 corner producer intake gate")
    if args.candidate:
        decision = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(f"square_axis_bridge_hilbert90_corner_producer_intake_candidate_rows={int(decision.ok)}/1")
        return 0 if decision.ok else 1

    profile = profile_corner_producer_intake()
    print("dependencies")
    print(f"  newton_triangle_marker_present={int(profile.newton_triangle_marker_present)}")
    print(f"  k_trace_minimality_marker_present={int(profile.k_trace_minimality_marker_present)}")
    print(f"  raw_k_trace_marker_present={int(profile.raw_k_trace_marker_present)}")
    print(f"  triangle_edge_marker_present={int(profile.triangle_edge_marker_present)}")
    print(f"  factor_kummer_marker_present={int(profile.factor_kummer_marker_present)}")
    print(f"  raw_kummer_marker_present={int(profile.raw_kummer_marker_present)}")
    print(f"  c169_lift_selector_marker_present={int(profile.c169_lift_selector_marker_present)}")
    print(f"  fiber_section_marker_present={int(profile.fiber_section_marker_present)}")
    print(f"  row_polynomial_marker_present={int(profile.row_polynomial_marker_present)}")
    print(f"  fiber_covariance_marker_present={int(profile.fiber_covariance_marker_present)}")
    print(f"  unit_triangle_marker_present={int(profile.unit_triangle_marker_present)}")
    print(f"  dependency_facts_ok={int(profile.dependency_facts_ok)}")
    print(f"  kummer_dependency_facts_ok={int(profile.kummer_dependency_facts_ok)}")
    print(f"  lift_dependency_facts_ok={int(profile.lift_dependency_facts_ok)}")
    print(f"  unit_dependency_facts_ok={int(profile.unit_dependency_facts_ok)}")
    print("producer_target")
    print(f"  canonical_q_newton={profile.canonical_q_newton}")
    print(f"  canonical_c169_newton={profile.canonical_c169_newton}")
    print(f"  canonical_d_newton={profile.canonical_d_newton}")
    print(f"  d_edge_q_images={profile.d_edge_q_images}")
    print(f"  unique_k_invariant_corner_support={profile.unique_k_invariant_corner_support}")
    print(f"  trace_correct_raw_relation_rows={profile.trace_correct_raw_relation_rows}")
    print(f"  kernel_trace_shift={profile.kernel_trace_shift}")
    print(f"  d_segment_combined_order={profile.d_segment_combined_order}")
    print(f"  bridge_edge_combined_order={profile.bridge_edge_combined_order}")
    print(f"  sparse_direction_count={profile.sparse_direction_count}")
    print(f"  primitive_c169_direction_rows={profile.primitive_c169_direction_rows}")
    print(f"  right_order_three_available_rows={profile.right_order_three_available_rows}")
    print(f"  canonical_c13_shadow={profile.canonical_c13_shadow}")
    print(f"  canonical_bridge_lift={profile.canonical_bridge_lift}")
    print(f"  inactive_c169_lift_count={profile.inactive_c169_lift_count}")
    print(f"  canonical_quadratic_section={profile.canonical_quadratic_section}")
    print(f"  canonical_row_values_c169={profile.canonical_row_values_c169}")
    print(f"  canonical_row_q_values={profile.canonical_row_q_values}")
    print(f"  covariance_row_count={profile.covariance_row_count}")
    print(f"  nonsplit_carry_needed_rows={profile.nonsplit_carry_needed_rows}")
    print(f"  no_carry_success_rows={profile.no_carry_success_rows}")
    print(f"  unit_triangle_row_count={profile.unit_triangle_row_count}")
    print(f"  unit_triangle_off_line_rows={profile.unit_triangle_off_line_rows}")
    print(f"  unit_triangle_off_line_points={profile.unit_triangle_off_line_points}")
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
    print("  producer_must_realize_curved_triangle_not_line_or_AP=1")
    print("  producer_must_use_recorded_half_bridge_edge_and_full_K_trace=1")
    print("  producer_must_account_for_raw_kernel_trace_shift_D3_minus_Y=1")
    print("  producer_must_realize_primitive_C169_motion_not_only_C13_shadow=1")
    print("  producer_must_select_active_C169_lift_not_generic_primitive_lift=1")
    print("  producer_must_realize_quadratic_fiber_section_not_affine_or_teichmuller_lift=1")
    print("  producer_must_transport_quadratic_fiber_with_nonsplit_C169_carry=1")
    print("  producer_must_realize_unit_sign_branch_row_triangle_not_passive_third_point=1")
    print("  finite_shape_is_helper_only_until_value_or_divisor_theorem=1")
    print("  official_vpp_verified_A_x0_is_the_only_submission_ready_state=1")
    print(f"square_axis_bridge_hilbert90_corner_producer_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("curved Hilbert-90 corner producer intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
