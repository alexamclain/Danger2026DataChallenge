#!/usr/bin/env python3
"""Priority-1 divisor/additive intake for the p25 KSY/Yang/H90 moonshot.

The source-priority selector says to ask first for exact divisor/additive
identities with legal Hilbert-90 boundary.  This gate composes the existing
conductor-39, H0, twisted/H90, and curved-corner classifiers into one
priority-1 intake.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    Conductor39SourceTheoremClaim,
    classify_claim as classify_conductor39_claim,
)
from p25_ksy_y_conductor39_twisted_descent_candidate_router_gate import (
    TwistedDescentCandidate,
    classify_candidate as classify_twisted_candidate,
)
from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    H0SourceTheoremCandidate,
    classify_candidate as classify_h0_candidate,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate import (
    CornerProducerCandidate,
    classify_candidate as classify_curved_corner_candidate,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_source_theorem_priority_selector_20260614.md",
        "ksy_y_source_theorem_priority_selector_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_source_theorem_intake_20260614.md",
        "ksy_y_conductor39_source_theorem_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_source_theorem_candidate_matcher_20260614.md",
        "ksy_y_h0_source_theorem_candidate_matcher_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_twisted_descent_candidate_router_20260614.md",
        "ksy_y_conductor39_twisted_descent_candidate_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_value_payload_reality_check_20260614.md",
        "ksy_y_value_payload_reality_check_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_curved_corner_minimal_closing_ask_packet_20260614.md",
        "ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1",
    ),
)


@dataclass(frozen=True)
class Priority1DivisorAdditiveRow:
    name: str
    lane: str
    classifier: str
    priority_rank: int
    avoids_finite_value_branch: bool
    needs_period156_bridge_context: bool
    current_source_theorem_exists: bool
    expected_decision: str
    actual_decision: str
    source_stage_closes: bool
    helper_only: bool
    conditional: bool
    rejected: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class Priority1DivisorAdditiveIntakeProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    rows: tuple[Priority1DivisorAdditiveRow, ...]
    row_count: int
    priority1_rows: int
    source_closing_rows: int
    current_source_theorem_rows: int
    avoids_value_branch_rows: int
    period156_bridge_context_rows: int
    helper_only_rows: int
    conditional_rows: int
    rejected_rows: int
    row_ok: bool


@dataclass(frozen=True)
class Priority1DivisorAdditivePacket:
    name: str
    lane: str
    claim_is_current_evidence: bool
    theorem_body_verified: bool
    output_kind: str
    arithmetic_source_theorem: bool
    finite_or_divisor: bool
    period156_context: bool
    danger3_framing: bool
    h0_product_multiplier: int | None
    h0_residue_sets_exact: bool
    h0_h90_boundary: bool
    conductor39_source_object: str
    conductor39_emits_object: bool
    conductor39_preserves_mixed_tensor: bool
    conductor39_yang_yu_legal_unit: bool
    conductor39_sparse_formal_gauge_only: bool
    conductor39_projection_or_axis_only: bool
    conductor39_additive_separated: bool
    conductor39_yang_distribution_to_507: bool
    conductor39_frobenius_or_hilbert90_descent: bool
    twisted_uses_degree6_orbit: bool
    twisted_uses_pure_norm: bool
    twisted_uses_pair_sum: bool
    twisted_uses_signed_shadow: bool
    twisted_uses_quotient_or_ratio: bool
    twisted_uses_hilbert90_boundary: bool
    curved_payload_shape_verified: bool
    curved_unit_triangle: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_from_mapping(data: dict[str, Any]) -> Priority1DivisorAdditivePacket:
    fields = Priority1DivisorAdditivePacket.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {name: False for name in allowed}
    defaults.update(
        {
            "name": "candidate",
            "lane": "h0",
            "output_kind": "divisor-additive",
            "h0_product_multiplier": None,
            "conductor39_source_object": "U_chi",
        }
    )
    defaults.update(data)
    return Priority1DivisorAdditivePacket(**{name: defaults[name] for name in fields})


def h0_candidate(
    name: str,
    *,
    multiplier: int | None,
    residue_exact: bool,
    source: bool,
    output_kind: str,
    period156: bool = False,
    h90_boundary: bool = True,
    danger3: bool = False,
) -> H0SourceTheoremCandidate:
    return H0SourceTheoremCandidate(
        name=name,
        product_multiplier=multiplier,
        residue_sets_exact=residue_exact,
        arithmetic_source_theorem=source,
        output_kind=output_kind,
        period156_context=period156,
        h90_boundary=h90_boundary,
        danger3_framing=danger3,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_x0=False,
        official_vpp=False,
    )


def conductor39_claim(
    name: str,
    *,
    source_object: str = "U_chi",
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    proper_axis_projection: bool = False,
    yang_lift: bool = True,
    descent: bool = True,
    output_kind: str = "divisor-additive",
    finite_or_divisor: bool = True,
    period156: bool = False,
    danger3: bool = False,
) -> Conductor39SourceTheoremClaim:
    return Conductor39SourceTheoremClaim(
        name=name,
        theorem_body_verified=True,
        source_object=source_object,
        emits_conductor39_object=emits,
        preserves_mixed_tensor=mixed,
        yang_yu_legal_unit=legal,
        sparse_formal_gauge_only=False,
        proper_axis_or_projection_only=proper_axis_projection,
        additive_separated=False,
        yang_distribution_to_507=yang_lift,
        frobenius_or_hilbert90_descent=descent,
        output_kind=output_kind,
        finite_field_identity_or_divisor_theorem=finite_or_divisor,
        period_156_context=period156,
        danger3_framing=danger3,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def twisted_candidate(
    name: str,
    *,
    finite_or_divisor: bool = True,
    period156: bool = True,
    source: bool = True,
    h90_boundary: bool = True,
    ratio: bool = True,
    danger3: bool = False,
) -> TwistedDescentCandidate:
    return TwistedDescentCandidate(
        name=name,
        theorem_body_verified=True,
        uses_degree6_orbit=True,
        uses_pure_norm=False,
        uses_pair_sum=False,
        uses_signed_shadow=False,
        uses_quotient_or_ratio=ratio,
        uses_hilbert90_boundary=h90_boundary,
        finite_value_or_divisor_theorem=finite_or_divisor,
        period156_context=period156,
        arithmetic_source_theorem=source,
        danger3_framing=danger3,
        extraction_to_A_x0=False,
        official_vpp=False,
    )


def curved_corner_candidate(
    name: str,
    *,
    payload_shape: bool,
    unit_triangle: bool,
    finite_or_divisor: bool = True,
    period156: bool = True,
    source: bool = True,
    danger3: bool = False,
) -> CornerProducerCandidate:
    return CornerProducerCandidate(
        name=name,
        theorem_body_verified=True,
        exact_curved_row_triangle=payload_shape,
        primitive_newton_curvature=payload_shape,
        recorded_half_bridge_edge=payload_shape,
        full_order25_k_trace=payload_shape,
        raw_d3_y_relation=payload_shape,
        raw_kernel_trace_accounted=payload_shape,
        primitive_c169_motion=payload_shape,
        active_c169_lift_selected=payload_shape,
        quadratic_fiber_section=payload_shape,
        nonsplit_c169_carry_transport=payload_shape,
        unit_triangle_law=unit_triangle,
        finite_value_or_divisor_theorem=finite_or_divisor,
        period156_context=period156,
        arithmetic_source_theorem=source,
        danger3_framing=danger3,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_A_x0=False,
        official_vpp=False,
    )


def make_row(
    *,
    name: str,
    lane: str,
    classifier: str,
    priority_rank: int,
    avoids_value_branch: bool,
    needs_period156_bridge_context: bool,
    expected_decision: str,
    decision: Any,
    current_source_theorem_exists: bool = False,
) -> Priority1DivisorAdditiveRow:
    actual = decision.decision
    source_closed = bool(
        getattr(decision, "source_stage_closed", False)
        or getattr(decision, "theorem_source_closed", False)
    )
    missing = str(
        getattr(
            decision,
            "first_missing_or_falsifier",
            getattr(decision, "first_missing_clause", ""),
        )
    )
    next_action = str(getattr(decision, "next_action", ""))
    helper_only = actual.startswith("helper_only_") or actual in {
        "source_certified_value_or_divisor_missing",
        "conductor39_source_identified_value_or_divisor_theorem_missing",
    }
    conditional = actual.startswith(("conditional_", "live_target_identified_"))
    rejected = actual.startswith("reject_")
    return Priority1DivisorAdditiveRow(
        name=name,
        lane=lane,
        classifier=classifier,
        priority_rank=priority_rank,
        avoids_finite_value_branch=avoids_value_branch,
        needs_period156_bridge_context=needs_period156_bridge_context,
        current_source_theorem_exists=current_source_theorem_exists,
        expected_decision=expected_decision,
        actual_decision=actual,
        source_stage_closes=source_closed,
        helper_only=helper_only,
        conditional=conditional,
        rejected=rejected,
        first_missing_or_falsifier=missing,
        next_action=next_action,
        ok=actual == expected_decision and getattr(decision, "ok", getattr(decision, "row_ok", False)),
    )


def manual_packet_row(
    packet: Priority1DivisorAdditivePacket,
    *,
    decision: str,
    classifier: str,
    priority_rank: int,
    avoids_value_branch: bool,
    needs_period156_bridge_context: bool,
    source_stage_closes: bool,
    helper_only: bool,
    conditional: bool,
    rejected: bool,
    first_missing_or_falsifier: str,
    next_action: str,
) -> Priority1DivisorAdditiveRow:
    return Priority1DivisorAdditiveRow(
        name=packet.name,
        lane=packet.lane,
        classifier=classifier,
        priority_rank=priority_rank,
        avoids_finite_value_branch=avoids_value_branch,
        needs_period156_bridge_context=needs_period156_bridge_context,
        current_source_theorem_exists=packet.claim_is_current_evidence and source_stage_closes,
        expected_decision=decision,
        actual_decision=decision,
        source_stage_closes=source_stage_closes,
        helper_only=helper_only,
        conditional=conditional,
        rejected=rejected,
        first_missing_or_falsifier=first_missing_or_falsifier,
        next_action=next_action,
        ok=True,
    )


def classify_packet(packet: Priority1DivisorAdditivePacket) -> Priority1DivisorAdditiveRow:
    if not packet.theorem_body_verified:
        return manual_packet_row(
            packet,
            decision="reject_no_theorem_body",
            classifier="priority1_divisor_additive_packet",
            priority_rank=0,
            avoids_value_branch=False,
            needs_period156_bridge_context=False,
            source_stage_closes=False,
            helper_only=False,
            conditional=False,
            rejected=True,
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="obtain theorem text before routing the claim",
        )

    if packet.lane == "h0":
        decision = classify_h0_candidate(
            h0_candidate(
                packet.name,
                multiplier=packet.h0_product_multiplier,
                residue_exact=packet.h0_residue_sets_exact,
                source=packet.arithmetic_source_theorem,
                output_kind=packet.output_kind,
                period156=packet.period156_context,
                h90_boundary=packet.h0_h90_boundary,
                danger3=packet.danger3_framing,
            )
        )
        return make_row(
            name=packet.name,
            lane=packet.lane,
            classifier="h0_source_theorem_candidate_matcher",
            priority_rank=1 if packet.output_kind == "divisor-additive" else 2 if packet.output_kind == "value" else 0,
            avoids_value_branch=packet.output_kind == "divisor-additive",
            needs_period156_bridge_context=packet.output_kind == "value",
            expected_decision=decision.decision,
            decision=decision,
            current_source_theorem_exists=packet.claim_is_current_evidence and decision.source_stage_closed,
        )

    if packet.lane == "conductor39":
        decision = classify_conductor39_claim(
            Conductor39SourceTheoremClaim(
                name=packet.name,
                theorem_body_verified=packet.theorem_body_verified,
                source_object=packet.conductor39_source_object,
                emits_conductor39_object=packet.conductor39_emits_object,
                preserves_mixed_tensor=packet.conductor39_preserves_mixed_tensor,
                yang_yu_legal_unit=packet.conductor39_yang_yu_legal_unit,
                sparse_formal_gauge_only=packet.conductor39_sparse_formal_gauge_only,
                proper_axis_or_projection_only=packet.conductor39_projection_or_axis_only,
                additive_separated=packet.conductor39_additive_separated,
                yang_distribution_to_507=packet.conductor39_yang_distribution_to_507,
                frobenius_or_hilbert90_descent=packet.conductor39_frobenius_or_hilbert90_descent,
                output_kind=packet.output_kind,
                finite_field_identity_or_divisor_theorem=packet.finite_or_divisor,
                period_156_context=packet.period156_context,
                danger3_framing=packet.danger3_framing,
                extraction_to_A_x0=False,
                concrete_vpp_verified_triple=False,
            )
        )
        return make_row(
            name=packet.name,
            lane=packet.lane,
            classifier="conductor39_source_theorem_intake",
            priority_rank=1 if packet.output_kind == "divisor-additive" else 2 if packet.output_kind == "value" else 0,
            avoids_value_branch=packet.output_kind == "divisor-additive",
            needs_period156_bridge_context=packet.output_kind == "value",
            expected_decision=decision.decision,
            decision=decision,
            current_source_theorem_exists=packet.claim_is_current_evidence and decision.theorem_source_closed,
        )

    if packet.lane == "twisted_h90":
        decision = classify_twisted_candidate(
            TwistedDescentCandidate(
                name=packet.name,
                theorem_body_verified=packet.theorem_body_verified,
                uses_degree6_orbit=packet.twisted_uses_degree6_orbit,
                uses_pure_norm=packet.twisted_uses_pure_norm,
                uses_pair_sum=packet.twisted_uses_pair_sum,
                uses_signed_shadow=packet.twisted_uses_signed_shadow,
                uses_quotient_or_ratio=packet.twisted_uses_quotient_or_ratio,
                uses_hilbert90_boundary=packet.twisted_uses_hilbert90_boundary,
                finite_value_or_divisor_theorem=packet.finite_or_divisor,
                period156_context=packet.period156_context,
                arithmetic_source_theorem=packet.arithmetic_source_theorem,
                danger3_framing=packet.danger3_framing,
                extraction_to_A_x0=False,
                official_vpp=False,
            )
        )
        return make_row(
            name=packet.name,
            lane=packet.lane,
            classifier="twisted_descent_candidate_router",
            priority_rank=1 if packet.output_kind == "divisor-additive" else 2 if packet.output_kind == "value" else 0,
            avoids_value_branch=packet.output_kind == "divisor-additive",
            needs_period156_bridge_context=True,
            expected_decision=decision.decision,
            decision=decision,
            current_source_theorem_exists=packet.claim_is_current_evidence and decision.source_stage_closed,
        )

    if packet.lane == "curved_corner":
        decision = classify_curved_corner_candidate(
            curved_corner_candidate(
                packet.name,
                payload_shape=packet.curved_payload_shape_verified,
                unit_triangle=packet.curved_unit_triangle,
                finite_or_divisor=packet.finite_or_divisor,
                period156=packet.period156_context,
                source=packet.arithmetic_source_theorem,
                danger3=packet.danger3_framing,
            )
        )
        return make_row(
            name=packet.name,
            lane=packet.lane,
            classifier="curved_corner_producer_intake",
            priority_rank=1 if packet.output_kind == "divisor-additive" else 2 if packet.output_kind == "value" else 0,
            avoids_value_branch=packet.output_kind == "divisor-additive",
            needs_period156_bridge_context=True,
            expected_decision=decision.decision,
            decision=decision,
            current_source_theorem_exists=packet.claim_is_current_evidence and decision.source_stage_closed,
        )

    return manual_packet_row(
        packet,
        decision="reject_unknown_priority1_lane",
        classifier="priority1_divisor_additive_packet",
        priority_rank=0,
        avoids_value_branch=False,
        needs_period156_bridge_context=False,
        source_stage_closes=False,
        helper_only=False,
        conditional=False,
        rejected=True,
        first_missing_or_falsifier="lane must be h0, conductor39, twisted_h90, or curved_corner",
        next_action="restate the claim using one of the priority-1 source lanes",
    )


def intake_rows() -> tuple[Priority1DivisorAdditiveRow, ...]:
    h0_closed = classify_h0_candidate(
        h0_candidate(
            "h0_legal_divisor_boundary_identity",
            multiplier=4,
            residue_exact=True,
            source=True,
            output_kind="divisor-additive",
            h90_boundary=True,
        )
    )
    h0_missing_boundary = classify_h0_candidate(
        h0_candidate(
            "h0_divisor_missing_h90_boundary",
            multiplier=4,
            residue_exact=True,
            source=True,
            output_kind="divisor-additive",
            h90_boundary=False,
        )
    )
    h0_source_only = classify_h0_candidate(
        h0_candidate(
            "h0_source_certification_only",
            multiplier=1,
            residue_exact=True,
            source=True,
            output_kind="source-certification",
        )
    )
    conductor_closed = classify_conductor39_claim(
        conductor39_claim("conductor39_legal_divisor_identity")
    )
    conductor_source_only = classify_conductor39_claim(
        conductor39_claim(
            "conductor39_source_certification_only",
            finite_or_divisor=False,
        )
    )
    conductor_value_no_period = classify_conductor39_claim(
        conductor39_claim(
            "conductor39_value_without_period156_control",
            output_kind="value",
            finite_or_divisor=True,
            period156=False,
        )
    )
    twisted_closed = classify_twisted_candidate(
        twisted_candidate("twisted_h90_divisor_with_period_bridge_context")
    )
    twisted_missing_period = classify_twisted_candidate(
        twisted_candidate(
            "twisted_h90_divisor_missing_period_bridge_context",
            period156=False,
        )
    )
    curved_closed = classify_curved_corner_candidate(
        curved_corner_candidate(
            "curved_corner_divisor_with_period156_context",
            payload_shape=True,
            unit_triangle=True,
        )
    )
    curved_missing_period = classify_curved_corner_candidate(
        curved_corner_candidate(
            "curved_corner_divisor_missing_period156_context",
            payload_shape=True,
            unit_triangle=True,
            period156=False,
        )
    )
    finite_payload_no_source = classify_h0_candidate(
        h0_candidate(
            "finite_payload_without_source_control",
            multiplier=1,
            residue_exact=True,
            source=False,
            output_kind="computed-payload",
            period156=True,
            h90_boundary=True,
        )
    )
    projection_reject = classify_conductor39_claim(
        conductor39_claim(
            "prime13_projection_or_axis_control",
            source_object="projection",
            emits=False,
            mixed=False,
            legal=False,
            proper_axis_projection=True,
            yang_lift=False,
            descent=False,
            finite_or_divisor=False,
        )
    )

    return (
        make_row(
            name="h0_legal_divisor_boundary_identity",
            lane="H0/H0_translate",
            classifier="h0_source_theorem_candidate_matcher",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=False,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            decision=h0_closed,
        ),
        make_row(
            name="h0_divisor_missing_h90_boundary",
            lane="H0/H0_translate",
            classifier="h0_source_theorem_candidate_matcher",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=False,
            expected_decision="conditional_divisor_identity_missing_h90_boundary",
            decision=h0_missing_boundary,
        ),
        make_row(
            name="h0_source_certification_only",
            lane="H0/H0_translate",
            classifier="h0_source_theorem_candidate_matcher",
            priority_rank=0,
            avoids_value_branch=False,
            needs_period156_bridge_context=False,
            expected_decision="source_certified_value_or_divisor_missing",
            decision=h0_source_only,
        ),
        make_row(
            name="conductor39_legal_divisor_identity",
            lane="conductor39",
            classifier="conductor39_source_theorem_intake",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=False,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            decision=conductor_closed,
        ),
        make_row(
            name="conductor39_source_certification_only",
            lane="conductor39",
            classifier="conductor39_source_theorem_intake",
            priority_rank=0,
            avoids_value_branch=False,
            needs_period156_bridge_context=False,
            expected_decision="conductor39_source_identified_value_or_divisor_theorem_missing",
            decision=conductor_source_only,
        ),
        make_row(
            name="conductor39_value_without_period156_control",
            lane="conductor39",
            classifier="conductor39_source_theorem_intake",
            priority_rank=2,
            avoids_value_branch=False,
            needs_period156_bridge_context=True,
            expected_decision="conditional_missing_period_156_context",
            decision=conductor_value_no_period,
        ),
        make_row(
            name="twisted_h90_divisor_with_period_bridge_context",
            lane="twisted/H90",
            classifier="twisted_descent_candidate_router",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=True,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            decision=twisted_closed,
        ),
        make_row(
            name="twisted_h90_divisor_missing_period_bridge_context",
            lane="twisted/H90",
            classifier="twisted_descent_candidate_router",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=True,
            expected_decision="conditional_value_theorem_missing_period156_context",
            decision=twisted_missing_period,
        ),
        make_row(
            name="curved_corner_divisor_with_period156_context",
            lane="curved_corner",
            classifier="curved_corner_producer_intake",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=True,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            decision=curved_closed,
        ),
        make_row(
            name="curved_corner_divisor_missing_period156_context",
            lane="curved_corner",
            classifier="curved_corner_producer_intake",
            priority_rank=1,
            avoids_value_branch=True,
            needs_period156_bridge_context=True,
            expected_decision="conditional_missing_period156_context",
            decision=curved_missing_period,
        ),
        make_row(
            name="finite_payload_without_source_control",
            lane="finite_payload",
            classifier="h0_source_theorem_candidate_matcher",
            priority_rank=0,
            avoids_value_branch=False,
            needs_period156_bridge_context=False,
            expected_decision="conditional_finite_payload_without_source_theorem",
            decision=finite_payload_no_source,
        ),
        make_row(
            name="prime13_projection_or_axis_control",
            lane="conductor39",
            classifier="conductor39_source_theorem_intake",
            priority_rank=0,
            avoids_value_branch=False,
            needs_period156_bridge_context=False,
            expected_decision="reject_loses_mixed_tensor",
            decision=projection_reject,
        ),
    )


def profile_priority1_divisor_additive_intake() -> Priority1DivisorAdditiveIntakeProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = intake_rows()
    priority1 = sum(row.priority_rank == 1 for row in rows)
    source_closing = sum(row.source_stage_closes for row in rows)
    current_sources = sum(row.current_source_theorem_exists for row in rows)
    avoids_value = sum(row.avoids_finite_value_branch for row in rows)
    needs_period = sum(row.needs_period156_bridge_context for row in rows)
    helper = sum(row.helper_only for row in rows)
    conditional = sum(row.conditional for row in rows)
    rejected = sum(row.rejected for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 12
        and priority1 == 7
        and source_closing == 4
        and current_sources == 0
        and avoids_value == 7
        and needs_period == 5
        and helper == 2
        and conditional == 5
        and rejected == 1
        and tuple(row.actual_decision for row in rows)
        == (
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_divisor_identity_missing_h90_boundary",
            "source_certified_value_or_divisor_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conductor39_source_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_value_theorem_missing_period156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_missing_period156_context",
            "conditional_finite_payload_without_source_theorem",
            "reject_loses_mixed_tensor",
        )
        and all(row.ok for row in rows)
    )
    return Priority1DivisorAdditiveIntakeProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        rows=rows,
        row_count=len(rows),
        priority1_rows=priority1,
        source_closing_rows=source_closing,
        current_source_theorem_rows=current_sources,
        avoids_value_branch_rows=avoids_value,
        period156_bridge_context_rows=needs_period,
        helper_only_rows=helper,
        conditional_rows=conditional,
        rejected_rows=rejected,
        row_ok=row_ok,
    )


def print_row(row: Priority1DivisorAdditiveRow) -> None:
    print(
        "  "
        f"{row.name}: lane={row.lane} classifier={row.classifier} "
        f"rank={row.priority_rank} avoids_value={int(row.avoids_finite_value_branch)} "
        f"period156_context={int(row.needs_period156_bridge_context)} "
        f"current_source={int(row.current_source_theorem_exists)} "
        f"decision={row.actual_decision} closes={int(row.source_stage_closes)} "
        f"helper={int(row.helper_only)} conditional={int(row.conditional)} "
        f"rejected={int(row.rejected)} missing={row.first_missing_or_falsifier}"
    )
    print(f"    next={row.next_action}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json")
    args = parser.parse_args()

    if args.packet_json:
        with Path(args.packet_json).open() as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise SystemExit("packet JSON must be an object")
        row = classify_packet(packet_from_mapping(data))
        print("p25 KSY-y priority-1 divisor/additive packet intake")
        print_row(row)
        print(f"source_stage_closes={int(row.source_stage_closes)}")
        print(f"current_source_theorem_exists={int(row.current_source_theorem_exists)}")
        print(f"helper_only={int(row.helper_only)}")
        print(f"conditional={int(row.conditional)}")
        print(f"rejected={int(row.rejected)}")
        print(f"ksy_y_priority1_divisor_additive_intake_candidate_rows={int(row.ok)}/1")
        if not row.ok:
            raise SystemExit("priority-1 divisor/additive packet intake failed")
        return 0

    profile = profile_priority1_divisor_additive_intake()
    print("p25 KSY-y priority-1 divisor/additive intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("intake_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  avoids_value_branch_rows={profile.avoids_value_branch_rows}")
    print(f"  period156_bridge_context_rows={profile.period156_bridge_context_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  priority1_divisor_additive_yes_closes_source_but_not_DANGER3=1")
    print("  H0_divisor_claims_need_the_legal_H90_boundary=1")
    print("  conductor39_divisor_claims_need_the_legal_mixed_source_and_descent=1")
    print("  twisted_H90_and_curved_corner_divisor_claims_still_need_period156_context_in_current_router=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_priority1_divisor_additive_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 divisor/additive intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
