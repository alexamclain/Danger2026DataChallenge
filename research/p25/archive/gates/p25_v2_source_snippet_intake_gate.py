#!/usr/bin/env python3
"""Classify future source snippets against the p25 v2 theorem target.

This gate is an intake checklist for paper snippets, expert replies, or
subagent reports.  It does not prove the missing theorem.  It says what kind
of snippet would close source stage, what is partial progress, and what should
be rejected immediately, including the promoted H0/Y507 period-156 value
compatibility screen and the H90 support lower bound.
Exact-P snippets also route through the minimal exact-P hook.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


LEGAL_MULTIPLIERS = (1, 2, 4, 8)
LEGAL_PAYLOAD_HASHES = {
    1: "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e",
    2: "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9",
    4: "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6",
    8: "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87",
}
RECIPROCAL_PAYLOAD_HASHES = {
    1: "b056476e79e03adbda534247a5bccc34efeb3dcaee0f17c60d1cc837add44fb1",
    2: "9bc545cc5aa5616b8d5a452ffdfe3ffe6e3842d619836510e165730243de3d89",
    4: "0668d9f9cefc9d7e784a3a022d55ff3b3f147221f82d8ee17ccec3c20747d47e",
    8: "c0d88010bc8b3e05bb90badb95a50439e184efd4352197a3ae032f29d875d77d",
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SnippetCandidate:
    name: str
    source_family: str
    multiplier: int | None
    payload_hash: str | None
    arithmetic_source_theorem: bool
    output_kind: str
    has_h90_boundary: bool
    has_period156_context: bool
    feeds_exactp_bridge: bool
    has_danger3_framing: bool
    has_same_j_bridge: bool
    has_x16_surface: bool
    has_halving_or_x0: bool
    has_vpp: bool


@dataclass(frozen=True)
class SnippetDecision:
    name: str
    source_family: str
    legal_row: bool
    source_stage_closed: bool
    post_theorem_stage: str
    decision: str
    first_missing: str
    continue_lane: bool
    submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class SourceSnippetIntake:
    evidence_markers: tuple[EvidenceMarker, ...]
    candidates: tuple[SnippetCandidate, ...]
    decisions: tuple[SnippetDecision, ...]
    evidence_markers_ok: int
    source_stage_closing_shapes: int
    direct_submission_shapes: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
        marker(
            "post_theorem_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "row_orientation_reciprocal_normalizer",
            "research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
            "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
        ),
        marker(
            "koo_shin_distribution_noncloser",
            "research/p25/evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
            "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
        ),
        marker(
            "theorem52_constant_span_obstruction",
            "research/p25/evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
            "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
        ),
        marker(
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "norm_only_descent_ambiguity",
            "research/p25/evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
            "p25_v2_norm_only_descent_ambiguity_rows=1/1",
        ),
        marker(
            "degree6_value_descent_ambiguity",
            "research/p25/evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
            "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
        ),
        marker(
            "yang_lift_descent_boundary_contract",
            "research/p25/evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md",
            "p25_v2_yang_lift_descent_boundary_contract_rows=1/1",
        ),
        marker(
            "conductor39_norm_one_quotient_route",
            "research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
            "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "coefficient6_root_normalization",
            "research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md",
            "p25_v2_coefficient6_root_normalization_rows=1/1",
        ),
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "quartic_reciprocal_orientation",
            "research/p25/evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
            "p25_v2_quartic_reciprocal_orientation_rows=1/1",
        ),
        marker(
            "h90_support_lower_bound",
            "research/p25/evidence/p25_v2_h90_support_lower_bound_20260616.md",
            "p25_v2_h90_support_lower_bound_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
    )


def candidate_rows() -> tuple[SnippetCandidate, ...]:
    return (
        SnippetCandidate(
            name="exact_divisor_additive_m1",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="divisor-additive",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="period156_h0_y507_value_m2",
            source_family="H0/Y507 value route",
            multiplier=2,
            payload_hash=LEGAL_PAYLOAD_HASHES[2],
            arithmetic_source_theorem=True,
            output_kind="value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exactp_upstream",
            source_family="exact-P",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-upstream",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=True,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="source_legality_only",
            source_family="Koo-Shin/Yang",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="source-legality",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="reciprocal_m8_minus_boundary",
            source_family="H0/conductor-39",
            multiplier=7,
            payload_hash=RECIPROCAL_PAYLOAD_HASHES[8],
            arithmetic_source_theorem=True,
            output_kind="reciprocal-minus-boundary",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="reciprocal_orientation_unspecified",
            source_family="H0/conductor-39",
            multiplier=7,
            payload_hash=RECIPROCAL_PAYLOAD_HASHES[8],
            arithmetic_source_theorem=True,
            output_kind="reciprocal-orientation-unspecified",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="reciprocal_plus_boundary",
            source_family="H0/conductor-39",
            multiplier=7,
            payload_hash=RECIPROCAL_PAYLOAD_HASHES[8],
            arithmetic_source_theorem=True,
            output_kind="reciprocal-plus-boundary",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="theorem52_constant_product_repair",
            source_family="Koo-Shin 2010",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="theorem52-constant-repair",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="broad_quadratic_aggregate_boundary_2w",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="broad-quadratic-aggregate",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="all_four_rows_product_boundary_4w",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="all-four-rows-product",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="row_quotient_boundary_zero",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="row-quotient-boundary-zero",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="aggregate_plus_quotient_row_square",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="row-square-bridge",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="row_square_value_theorem",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="row-square-value",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="row_square_with_h90_boundary_2w",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="row-square-boundary-2w",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="divisor_only_with_h90_boundary",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="divisor-only-h90-boundary",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="value_up_to_fp_scalar",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="value-up-to-fp-scalar",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="period_norm_identity_only",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="period-norm-only",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="dense_unit_character_norm_value",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="dense-unit-character-norm",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="norm_with_formal_one_coset_descent",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="formal-one-coset-norm-descent",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="norm_one_Q_value_theorem_with_period156_context",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="norm-one-q-value-period156",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="explicit_Q3_hilbert90_preimage_with_finite_theorem",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q3-h90-preimage-finite-theorem",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coset_selector_or_Q_source_only",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coset-selector-or-q-source-only",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="Q6_boundary_only",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q6-boundary-only",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="primitive_U_chi_power_only",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="primitive-u-chi-power-only",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="pure_character_degree6_norm",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="pure-character-degree6-norm",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="boundary_only",
            source_family="Hilbert-90",
            multiplier=4,
            payload_hash=LEGAL_PAYLOAD_HASHES[4],
            arithmetic_source_theorem=True,
            output_kind="boundary",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="ambient_value_no_period156",
            source_family="Schertz/Scholl",
            multiplier=8,
            payload_hash=LEGAL_PAYLOAD_HASHES[8],
            arithmetic_source_theorem=True,
            output_kind="value",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="ambient780_mu11_power_only",
            source_family="Schertz/Scholl",
            multiplier=8,
            payload_hash=LEGAL_PAYLOAD_HASHES[8],
            arithmetic_source_theorem=True,
            output_kind="ambient780-mu11-power",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="degree6_value_orbit_without_descent",
            source_family="Schertz/Shin/Siegel-Robert",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="degree6-value-orbit-without-descent",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="primitive_root_expression_degree6_only",
            source_family="Schertz/Shin/Siegel-Robert",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="degree6-primitive-root-expression",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="degree6_norm_without_selected_row",
            source_family="Schertz/Shin/Siegel-Robert",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="degree6-norm-without-selected-row",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="mixed_unit_without_yang_lift",
            source_family="Koo-Shin/Yang",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="mixed-unit-without-yang-lift",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="mixed_yang_without_h90_descent",
            source_family="Koo-Shin/Yang",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="mixed-yang-without-h90-descent",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="yang_h90_source_without_finite_theorem",
            source_family="Koo-Shin/Yang",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="yang-h90-source-without-finite-theorem",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="yang_lift_wrong_boundary",
            source_family="Koo-Shin/Yang",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="yang-lift-wrong-boundary",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coefficient2_exact_root_value",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coefficient2-exact-root-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coefficient3_exact_root_value",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coefficient3-exact-root-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coefficient1_exact_root_value",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coefficient1-exact-root-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coefficient6_root_without_orientation",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coefficient6-root-without-orientation",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="scaled_boundary_as_current_target",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="scaled-boundary-as-current-target",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_power3_value",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-power3-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_power5_value",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-power5-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_power13_value",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-power13-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_power39_value",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-power39-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="square_power_value_without_branch",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="ambiguous-power-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="eleventh_power_value_without_branch",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="mu11-power-ambiguity",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="mu11_scalar_unspecified",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="mu11-scalar-unspecified",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="mu39_scalar_as_fp",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="mu39-scalar-as-fp",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_power11_value_with_branch",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-power11-value-with-branch",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="power_divisor3_with_value_normalization",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="power-divisor-with-value-normalization",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="power_divisor3_without_value",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="power-divisor-without-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="power_boundary3_as_current",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="power-boundary-as-current-target",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="divisor_h90_no_additive_normalization",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="divisor-h90-no-additive-normalization",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="additive_relation_without_selected_row",
            source_family="dense norm or family average",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="additive-relation-without-selected-row",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="normalized_additive_after_basepoint",
            source_family="H0/conductor-39",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="additive-normalized-after-basepoint",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="w_boundary_nonunit_edge_combination",
            source_family="H0/conductor-39",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="w-boundary-nonunit-edge-combination",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="wrong_product_row",
            source_family="unknown",
            multiplier=3,
            payload_hash="wrong",
            arithmetic_source_theorem=True,
            output_kind="divisor-additive",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="finite_payload_no_source",
            source_family="local computation",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=False,
            output_kind="divisor-additive",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="legal_minimal_h90_preimage_only",
            source_family="conductor-39 H90",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="legal-minimal-h90-preimage-only",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="support12_h90_preimage_boundary_control",
            source_family="conductor-39 H90",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="support12-h90-boundary-control",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="support_below_12_h90_selector",
            source_family="conductor-39 H90",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="support-below-12-h90-selector",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="ksy_normalized_y_vocabulary_only",
            source_family="KSY exact-P",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-ksy-vocabulary-only",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="raw_kubert_lang_exponent_balance_only",
            source_family="Kubert-Lang exact-P",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-raw-kl-balance-only",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exactp_branchless_orientation_word",
            source_family="exact-P heavy route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-branchless-orientation-word",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=True,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exactp_theta2_value_without_period156_context",
            source_family="exact-P value route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-theta2-value-without-period156-context",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=True,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="wrong_exactp_packet",
            source_family="exact-P",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-wrong-packet",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="nonuniform_or_missing_exactp_atoms",
            source_family="exact-P",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-nonuniform-or-missing-atoms",
            has_h90_boundary=False,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exactp_ambient_period780_value_only",
            source_family="exact-P value route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="exactp-ambient-period780-value-only",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=True,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="unified_theorem_as_exactp_recovery",
            source_family="H0/conductor-39 claimed as exact-P",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="unified-theorem-as-exactp-recovery",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="quartic_selector_finite_theorem",
            source_family="H0/conductor-39 character route",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="quartic-selector-finite-theorem",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="exact_quartic_selector_without_value_theorem",
            source_family="H0/conductor-39 character route",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="exact-quartic-selector-without-value-theorem",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="coarse_quartic_phase_or_magnitude_only",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="coarse-quartic-phase-or-magnitude-only",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="quartic_phase_without_row_sign",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="quartic-phase-without-row-sign",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="same_parity_quartic_phase",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="same-parity-quartic-phase",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="quartic_phase_boundary_sign_unspecified",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="quartic-phase-boundary-sign-unspecified",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="quartic_phase_collision_as_different_edge",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="quartic-phase-collision-as-different-edge",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="quartic_reciprocal_phase_plus_boundary",
            source_family="H0/conductor-39 character route",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="quartic-reciprocal-phase-plus-boundary",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_diagonal_value_only",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-diagonal-value-only",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_plus_row_quotient_without_root",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-plus-row-quotient-without-root",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_plus_explicit_oriented_diagonal_split",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-plus-oriented-diagonal-split",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_wrong_zero_boundary_split",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-wrong-zero-boundary-split",
            has_h90_boundary=False,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_square_exact_fp_value",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-square-exact-fp-value",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_square_value_up_to_scalar",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-square-value-up-to-scalar",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="q_square_sign_from_divisor_h90_or_phase",
            source_family="conductor-39 norm-one quotient",
            multiplier=None,
            payload_hash=None,
            arithmetic_source_theorem=True,
            output_kind="q-square-sign-from-invariants",
            has_h90_boundary=True,
            has_period156_context=True,
            feeds_exactp_bridge=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
        ),
        SnippetCandidate(
            name="full_submission",
            source_family="hypothetical complete extraction",
            multiplier=1,
            payload_hash=LEGAL_PAYLOAD_HASHES[1],
            arithmetic_source_theorem=True,
            output_kind="divisor-additive",
            has_h90_boundary=True,
            has_period156_context=False,
            feeds_exactp_bridge=False,
            has_danger3_framing=True,
            has_same_j_bridge=True,
            has_x16_surface=True,
            has_halving_or_x0=True,
            has_vpp=True,
        ),
    )


def legal_row(candidate: SnippetCandidate) -> bool:
    return (
        candidate.multiplier in LEGAL_MULTIPLIERS
        and candidate.payload_hash == LEGAL_PAYLOAD_HASHES.get(candidate.multiplier)
    )


def source_stage_closed(candidate: SnippetCandidate, legal: bool) -> bool:
    if candidate.output_kind == "exactp-upstream":
        return candidate.arithmetic_source_theorem and candidate.feeds_exactp_bridge
    if candidate.output_kind == "reciprocal-minus-boundary":
        return candidate.arithmetic_source_theorem and candidate.has_h90_boundary
    if candidate.output_kind == "quartic-selector-finite-theorem":
        return candidate.arithmetic_source_theorem and candidate.has_h90_boundary
    if not legal or not candidate.arithmetic_source_theorem:
        return False
    if candidate.output_kind == "divisor-additive":
        return candidate.has_h90_boundary
    if candidate.output_kind == "value":
        return candidate.has_h90_boundary and candidate.has_period156_context
    return False


def post_theorem_stage(candidate: SnippetCandidate) -> str:
    if not candidate.has_danger3_framing:
        return "source_stage_win_danger3_framing_missing"
    if not candidate.has_same_j_bridge:
        return "framed_source_same_j_bridge_missing"
    if not candidate.has_x16_surface:
        return "same_j_bridge_x16_surface_missing"
    if not candidate.has_halving_or_x0:
        return "active_surface_reached_halving_missing"
    if not candidate.has_vpp:
        return "extraction_ready_vpp_missing"
    return "submission_ready"


def classify(candidate: SnippetCandidate) -> SnippetDecision:
    legal = legal_row(candidate)
    closed = source_stage_closed(candidate, legal)
    if closed:
        stage = post_theorem_stage(candidate)
        first_missing = {
            "source_stage_win_danger3_framing_missing": "DANGER3 finite-identity / non-CM framing",
            "framed_source_same_j_bridge_missing": "same-j X_1(8112) bridge",
            "same_j_bridge_x16_surface_missing": "X_1(16) y/x/A/xP16 surface or direct A,xP16",
            "active_surface_reached_halving_missing": "38-link halving chain or direct x0",
            "extraction_ready_vpp_missing": "official src/vpp.py verification",
            "submission_ready": "none",
        }[stage]
        return SnippetDecision(
            name=candidate.name,
            source_family=candidate.source_family,
            legal_row=legal,
            source_stage_closed=True,
            post_theorem_stage=stage,
            decision=stage,
            first_missing=first_missing,
            continue_lane=True,
            submission_ready=stage == "submission_ready",
            ok=True,
        )

    if candidate.output_kind == "reciprocal-orientation-unspecified":
        decision = "repair_reciprocal_orientation_or_boundary_sign_missing"
        missing = "explicit reciprocal orientation and -Norm_156 boundary, or rewrite as the oriented legal row"
    elif candidate.output_kind == "reciprocal-plus-boundary":
        decision = "reject_orientation_boundary_mismatch"
        missing = "reciprocal product should carry the opposite Hilbert-90 boundary sign"
    elif candidate.output_kind == "broad-quadratic-aggregate":
        decision = "repair_broad_quadratic_aggregate_boundary_2w"
        missing = "selector/factorization to one sparse edge with W boundary"
    elif candidate.output_kind == "all-four-rows-product":
        decision = "repair_overdemand_square_of_broad_quadratic"
        missing = "one legal support-156 row with W boundary is enough and still missing"
    elif candidate.output_kind == "row-quotient-boundary-zero":
        decision = "repair_boundary_zero_quotient_only"
        missing = "one-row value/divisor theorem; quotient has zero H90 boundary"
    elif candidate.output_kind == "row-square-bridge":
        decision = "repair_row_square_bridge_halving_missing"
        missing = "halving/root/orientation data selecting the legal row, or direct one-row theorem"
    elif candidate.output_kind == "row-square-value":
        decision = "repair_row_square_root_sign_missing"
        missing = "explicit root/sign/orientation data selecting R rather than -R, or direct one-row theorem"
    elif candidate.output_kind == "row-square-boundary-2w":
        decision = "repair_boundary_scale_and_root_sign_missing"
        missing = "one-row W-boundary theorem plus explicit root/sign/orientation"
    elif candidate.output_kind == "divisor-only-h90-boundary":
        decision = "repair_constant_normalization_missing"
        missing = "additive/value normalization or finite framing fixing the F_p^* scalar"
    elif candidate.output_kind == "value-up-to-fp-scalar":
        decision = "repair_constant_normalization_missing"
        missing = "specified scalar, branch/root/telescoping context, or normalized value"
    elif candidate.output_kind == "period-norm-only":
        decision = "repair_norm_only_h90_descent_missing"
        missing = "legal support-156 Hilbert-90 descent selecting one row"
    elif candidate.output_kind == "dense-unit-character-norm":
        decision = "repair_norm_only_row_selection_missing"
        missing = "selected legal 78-over-78 product row and finite theorem for that row"
    elif candidate.output_kind == "formal-one-coset-norm-descent":
        decision = "reject_boundary_control_not_source_object"
        missing = "proper-axis pushforward failure; not the mixed conductor-39 source object"
    elif candidate.output_kind == "norm-one-q-value-period156":
        decision = "route_through_period156_value_source_hook"
        missing = "period-156 value source hook, then downstream DANGER3 framing and extraction"
    elif candidate.output_kind == "q3-h90-preimage-finite-theorem":
        decision = "normalize_h90_preimage_then_apply_source_snippet_intake"
        missing = "same theorem data after legal Hilbert-90 descent normalization"
    elif candidate.output_kind == "q-diagonal-value-only":
        decision = "support_diagonal_aggregate_selector_missing"
        missing = "boundary-zero split/orientation data or direct one-edge theorem"
    elif candidate.output_kind == "q-plus-row-quotient-without-root":
        decision = "repair_oriented_square_root_missing"
        missing = "halving/root/orientation data after reaching twice one edge"
    elif candidate.output_kind == "q-plus-oriented-diagonal-split":
        decision = "normalize_to_one_edge_then_apply_source_snippet_intake"
        missing = "same theorem data after explicit oriented diagonal-split normalization"
    elif candidate.output_kind == "q-wrong-zero-boundary-split":
        decision = "reject_zero_boundary_wrong_edge"
        missing = "split data must recover one of m1,m2,m4,m8 with the current oriented boundary"
    elif candidate.output_kind == "q-square-exact-fp-value":
        decision = "repair_extraction_map_missing_after_two_root_row_payload"
        missing = "two F_p row roots exist; DANGER3 framing and same-j/X_1(16)/halving or direct A,x0 extraction map still missing"
    elif candidate.output_kind == "q-square-value-up-to-scalar":
        decision = "repair_scalar_and_root_orientation_missing"
        missing = "specified scalar before the two-root payload is concrete"
    elif candidate.output_kind == "q-square-sign-from-invariants":
        decision = "reject_sign_invisible_to_current_invariants"
        missing = "constant sign has zero divisor/H90 boundary and does not alter exponent-character data"
    elif candidate.output_kind == "coset-selector-or-q-source-only":
        decision = "repair_finite_value_divisor_theorem_missing"
        missing = "finite value/divisor theorem for Q, Q^3, Q^6, or the selected Yang lift"
    elif candidate.output_kind == "q6-boundary-only":
        decision = "repair_additive_or_value_normalization_missing"
        missing = "scalar-fixed finite value/additive data, not just the Hilbert-90 boundary"
    elif candidate.output_kind == "primitive-u-chi-power-only":
        decision = "repair_yang_lift_descent_and_finite_theorem_missing"
        missing = "Yang lift, Hilbert-90 descent, and finite theorem for the selected row"
    elif candidate.output_kind == "pure-character-degree6-norm":
        decision = "reject_pure_character_degree6_norm_cancels"
        missing = "Frobenius alternation makes the degree-6 norm zero"
    elif candidate.output_kind == "degree6-value-orbit-without-descent":
        decision = "repair_degree6_orbit_without_descent"
        missing = "conjugate/norm descent back to F_p or Hilbert-90 ratio boundary"
    elif candidate.output_kind == "degree6-primitive-root-expression":
        decision = "repair_degree6_orbit_without_descent"
        missing = "conjugate/norm descent back to F_p or Hilbert-90 ratio boundary"
    elif candidate.output_kind == "degree6-norm-without-selected-row":
        decision = "repair_descent_without_selected_legal_row"
        missing = "legal support-156 row selection after descent"
    elif candidate.output_kind == "mixed-unit-without-yang-lift":
        decision = "repair_yang_lift_missing"
        missing = "level-507 Yang lift to the support-156 product"
    elif candidate.output_kind == "mixed-yang-without-h90-descent":
        decision = "repair_h90_descent_boundary_missing"
        missing = "Hilbert-90 descent with boundary Norm_156(Y_507)"
    elif candidate.output_kind == "yang-h90-source-without-finite-theorem":
        decision = "repair_value_divisor_theorem_missing"
        missing = "finite value/divisor theorem for the selected support-156 row"
    elif candidate.output_kind == "yang-lift-wrong-boundary":
        decision = "reject_yang_lift_boundary_or_target_mismatch"
        missing = "legal mixed conductor-39 target with Norm_156(Y_507) boundary"
    elif candidate.output_kind == "coefficient2-exact-root-value":
        decision = "normalize_cube_power_then_apply_source_snippet_intake"
        missing = "same theorem data after cubing to coefficient 6"
    elif candidate.output_kind == "coefficient3-exact-root-value":
        decision = "normalize_square_power_then_apply_source_snippet_intake"
        missing = "same theorem data after squaring to coefficient 6"
    elif candidate.output_kind == "coefficient1-exact-root-value":
        decision = "normalize_sixth_power_then_apply_source_snippet_intake"
        missing = "same theorem data after taking the sixth power to coefficient 6"
    elif candidate.output_kind == "coefficient6-root-without-orientation":
        decision = "repair_coefficient6_root_orientation_missing"
        missing = "explicit oriented root/sign data; square and sixth roots have a two-element kernel"
    elif candidate.output_kind == "scaled-boundary-as-current-target":
        decision = "reject_boundary_scale_mismatch"
        missing = "power back to the coefficient-6 row or prove the current boundary directly"
    elif candidate.output_kind == "exact-power3-value":
        decision = "normalize_unique_3rd_root_then_apply_source_snippet_intake"
        missing = "same theorem data after unique cube-root recovery in F_p^*"
    elif candidate.output_kind == "exact-power5-value":
        decision = "normalize_unique_5th_root_then_apply_source_snippet_intake"
        missing = "same theorem data after unique fifth-root recovery in F_p^*"
    elif candidate.output_kind == "exact-power13-value":
        decision = "normalize_unique_13th_root_then_apply_source_snippet_intake"
        missing = "same theorem data after unique thirteenth-root recovery in F_p^*"
    elif candidate.output_kind == "exact-power39-value":
        decision = "normalize_unique_39th_root_then_apply_source_snippet_intake"
        missing = "same theorem data after unique 39th-root recovery in F_p^*"
    elif candidate.output_kind == "ambiguous-power-value":
        decision = "repair_power_kernel_orientation_or_branch_missing"
        missing = "explicit orientation, branch, or scalar data selecting one root"
    elif candidate.output_kind == "mu11-power-ambiguity":
        decision = "repair_mu11_power_or_quotient_not_value"
        missing = "actual period-156 branch/root/telescoping data selecting one F_p value"
    elif candidate.output_kind == "mu11-scalar-unspecified":
        decision = "repair_root_of_unity_scalar_missing"
        missing = "explicit mu_11 scalar or branch data fixing the value"
    elif candidate.output_kind == "mu39-scalar-as-fp":
        decision = "reject_root_of_unity_not_in_fp"
        missing = "mu_39 is not contained in F_p^* for p25"
    elif candidate.output_kind == "exact-power11-value-with-branch":
        decision = "normalize_selected_power_value_then_apply_source_snippet_intake"
        missing = "same theorem data after branch/scalar-selected eleventh-root recovery"
    elif candidate.output_kind == "power-divisor-with-value-normalization":
        decision = "normalize_power_divisor_with_value_data_then_apply_source_snippet_intake"
        missing = "same theorem data after finite normalization and unique root recovery"
    elif candidate.output_kind == "power-divisor-without-value":
        decision = "repair_power_divisor_value_normalization_missing"
        missing = "finite value/additive normalization fixing the powered value before rooting"
    elif candidate.output_kind == "power-boundary-as-current-target":
        decision = "reject_scaled_boundary_as_current_target"
        missing = "powered boundary eW is not the current W boundary unless it powers back to the row"
    elif candidate.output_kind == "divisor-h90-no-additive-normalization":
        decision = "repair_additive_normalization_missing"
        missing = "finite additive/value/basepoint/telescoping normalization fixing the F_p^* scalar"
    elif candidate.output_kind == "additive-relation-without-selected-row":
        decision = "repair_selected_row_missing"
        missing = "legal support-156 row selection before applying the additive normalization"
    elif candidate.output_kind == "additive-normalized-after-basepoint":
        decision = "normalize_additive_value_then_apply_source_snippet_intake"
        missing = "same theorem data after additive/value normalization"
    elif candidate.output_kind == "w-boundary-nonunit-edge-combination":
        decision = "repair_edge_plus_boundary_zero_lattice"
        missing = "finite value for the boundary-zero lattice part or direct one-edge theorem"
    elif candidate.output_kind == "legal-minimal-h90-preimage-only":
        decision = "repair_selector_only"
        missing = "finite value/divisor theorem for the corresponding support-156 Yang product"
    elif candidate.output_kind == "support12-h90-boundary-control":
        decision = "reject_boundary_control_not_source_object"
        missing = "proper-axis pushforward failure; only the four mixed support-12 minimizers are legal"
    elif candidate.output_kind == "support-below-12-h90-selector":
        decision = "reject_h90_support_below_lower_bound"
        missing = "orbitwise Hilbert-90 lower bound forces support at least 12"
    elif candidate.output_kind == "exactp-ksy-vocabulary-only":
        decision = "repair_exact_selector_theorem_missing"
        missing = "compact C,D,K,orientation packet or exact equal-weight 75-atom theorem"
    elif candidate.output_kind == "exactp-raw-kl-balance-only":
        decision = "repair_theta2_intake_missing"
        missing = "accepted theta2/theta2-inverse divisor-additive payload or compact KSY theta2 certificate"
    elif candidate.output_kind == "exactp-branchless-orientation-word":
        decision = "repair_exactp_orientation_branch_missing"
        missing = "one of the four raw center/reverse branches and theta2/theta2^-1 output"
    elif candidate.output_kind == "exactp-theta2-value-without-period156-context":
        decision = "repair_period156_branch_selection_missing"
        missing = "period-156 theta2 fixedness, branch/root, or telescoping context"
    elif candidate.output_kind == "exactp-wrong-packet":
        decision = "reject_wrong_exactp_payload"
        missing = "compact exact-P packet C=(47,28), D=(22,3), primitive K=(57,0), with accepted orientation"
    elif candidate.output_kind == "exactp-nonuniform-or-missing-atoms":
        decision = "reject_by_finite_geometry_rigidity"
        missing = "finite geometry forces the exact equal-weight 75-atom payload"
    elif candidate.output_kind == "exactp-ambient-period780-value-only":
        decision = "repair_period156_branch_selection_missing"
        missing = "period-156 branch/root/telescoping context or divisor/additive normalization"
    elif candidate.output_kind == "unified-theorem-as-exactp-recovery":
        decision = "repair_reverse_selector_structure_missing"
        missing = "exact-P C,D,K,orientation, equal-weight 75-atom selector theorem, period-156 theta2 payload, or explicit reverse reconstruction theorem"
    elif candidate.output_kind == "exact-quartic-selector-without-value-theorem":
        decision = "repair_value_divisor_theorem_missing"
        missing = "scalar-fixed finite value/divisor theorem for the selected row"
    elif candidate.output_kind == "coarse-quartic-phase-or-magnitude-only":
        decision = "repair_quartic_edge_selection_missing"
        missing = "exact row-antisymmetric C4_1 phase selecting one legal edge"
    elif candidate.output_kind == "quartic-phase-without-row-sign":
        decision = "repair_mixed_tensor_missing"
        missing = "row-antisymmetric mixed tensor structure for the conductor-39 source row"
    elif candidate.output_kind == "same-parity-quartic-phase":
        decision = "reject_zero_boundary_wrong_edge"
        missing = "same-parity edges have zero W boundary or the wrong mixed tensor target"
    elif candidate.output_kind == "quartic-phase-boundary-sign-unspecified":
        decision = "repair_reciprocal_orientation_or_boundary_sign_missing"
        missing = "oriented row data or reciprocal row with -Norm_156 boundary"
    elif candidate.output_kind == "quartic-phase-collision-as-different-edge":
        decision = "repair_phase_orientation_collision"
        missing = "boundary sign/orientation data distinguishing reciprocal row from opposite edge"
    elif candidate.output_kind == "quartic-reciprocal-phase-plus-boundary":
        decision = "reject_orientation_boundary_mismatch"
        missing = "reciprocal phase carries -Norm_156 boundary, not the positive boundary"
    elif not legal and candidate.output_kind != "exactp-upstream":
        decision = "reject_wrong_or_nonlegal_product_row"
        missing = "one of the four legal payload hashes"
    elif not candidate.arithmetic_source_theorem:
        decision = "repair_missing_arithmetic_source_theorem"
        missing = "arithmetic source theorem"
    elif candidate.output_kind == "source-legality":
        decision = "repair_source_legality_only"
        missing = "finite value/divisor theorem"
    elif candidate.output_kind == "theorem52-constant-repair":
        decision = "reject_theorem52_constant_span_repair"
        missing = "nonzero constant-exponent vector in the legal quotient-C4 span"
    elif candidate.output_kind == "boundary":
        decision = "repair_boundary_only"
        missing = "finite value/divisor identity for one legal row"
    elif candidate.output_kind == "value" and not candidate.has_period156_context:
        decision = "repair_value_without_period156_context"
        missing = "canonical H0/Y507 period-156 branch/root/telescoping context"
    elif candidate.output_kind == "ambient780-mu11-power":
        decision = "repair_mu11_power_or_quotient_not_value"
        missing = "actual period-156 branch/root/telescoping data selecting one F_p value"
    else:
        decision = "reject_not_matching_current_intake"
        missing = "accepted source-stage theorem shape"
    return SnippetDecision(
        name=candidate.name,
        source_family=candidate.source_family,
        legal_row=legal,
        source_stage_closed=False,
        post_theorem_stage="not_reached",
        decision=decision,
        first_missing=missing,
        continue_lane=decision.startswith("repair"),
        submission_ready=False,
        ok=True,
    )


def build_intake() -> SourceSnippetIntake:
    markers = evidence_markers()
    candidates = candidate_rows()
    decisions = tuple(classify(candidate) for candidate in candidates)
    evidence_ok = sum(m.ok for m in markers)
    source_closing = sum(d.source_stage_closed for d in decisions)
    submission = sum(d.submission_ready for d in decisions)
    current_source_stage = 0
    current_submission = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(candidates) == 85
        and len(decisions) == 85
        and source_closing == 6
        and submission == 1
        and current_source_stage == 0
        and current_submission == 0
        and decisions[0].decision == "source_stage_win_danger3_framing_missing"
        and decisions[1].decision == "source_stage_win_danger3_framing_missing"
        and decisions[2].decision == "source_stage_win_danger3_framing_missing"
        and decisions[3].decision == "repair_source_legality_only"
        and decisions[4].decision == "source_stage_win_danger3_framing_missing"
        and decisions[5].decision == "repair_reciprocal_orientation_or_boundary_sign_missing"
        and decisions[6].decision == "reject_orientation_boundary_mismatch"
        and decisions[7].decision == "reject_theorem52_constant_span_repair"
        and decisions[8].decision == "repair_broad_quadratic_aggregate_boundary_2w"
        and decisions[9].decision == "repair_overdemand_square_of_broad_quadratic"
        and decisions[10].decision == "repair_boundary_zero_quotient_only"
        and decisions[11].decision == "repair_row_square_bridge_halving_missing"
        and decisions[12].decision == "repair_row_square_root_sign_missing"
        and decisions[13].decision == "repair_boundary_scale_and_root_sign_missing"
        and decisions[14].decision == "repair_constant_normalization_missing"
        and decisions[15].decision == "repair_constant_normalization_missing"
        and decisions[16].decision == "repair_norm_only_h90_descent_missing"
        and decisions[17].decision == "repair_norm_only_row_selection_missing"
        and decisions[18].decision == "reject_boundary_control_not_source_object"
        and decisions[19].decision == "route_through_period156_value_source_hook"
        and decisions[20].decision == "normalize_h90_preimage_then_apply_source_snippet_intake"
        and decisions[21].decision == "repair_finite_value_divisor_theorem_missing"
        and decisions[22].decision == "repair_additive_or_value_normalization_missing"
        and decisions[23].decision == "repair_yang_lift_descent_and_finite_theorem_missing"
        and decisions[24].decision == "reject_pure_character_degree6_norm_cancels"
        and decisions[25].decision == "repair_boundary_only"
        and decisions[26].decision == "repair_value_without_period156_context"
        and decisions[27].decision == "repair_mu11_power_or_quotient_not_value"
        and decisions[28].decision == "repair_degree6_orbit_without_descent"
        and decisions[29].decision == "repair_degree6_orbit_without_descent"
        and decisions[30].decision == "repair_descent_without_selected_legal_row"
        and decisions[31].decision == "repair_yang_lift_missing"
        and decisions[32].decision == "repair_h90_descent_boundary_missing"
        and decisions[33].decision == "repair_value_divisor_theorem_missing"
        and decisions[34].decision == "reject_yang_lift_boundary_or_target_mismatch"
        and decisions[35].decision == "normalize_cube_power_then_apply_source_snippet_intake"
        and decisions[36].decision == "normalize_square_power_then_apply_source_snippet_intake"
        and decisions[37].decision == "normalize_sixth_power_then_apply_source_snippet_intake"
        and decisions[38].decision == "repair_coefficient6_root_orientation_missing"
        and decisions[39].decision == "reject_boundary_scale_mismatch"
        and decisions[40].decision == "normalize_unique_3rd_root_then_apply_source_snippet_intake"
        and decisions[41].decision == "normalize_unique_5th_root_then_apply_source_snippet_intake"
        and decisions[42].decision == "normalize_unique_13th_root_then_apply_source_snippet_intake"
        and decisions[43].decision == "normalize_unique_39th_root_then_apply_source_snippet_intake"
        and decisions[44].decision == "repair_power_kernel_orientation_or_branch_missing"
        and decisions[45].decision == "repair_mu11_power_or_quotient_not_value"
        and decisions[46].decision == "repair_root_of_unity_scalar_missing"
        and decisions[47].decision == "reject_root_of_unity_not_in_fp"
        and decisions[48].decision == "normalize_selected_power_value_then_apply_source_snippet_intake"
        and decisions[49].decision == "normalize_power_divisor_with_value_data_then_apply_source_snippet_intake"
        and decisions[50].decision == "repair_power_divisor_value_normalization_missing"
        and decisions[51].decision == "reject_scaled_boundary_as_current_target"
        and decisions[52].decision == "repair_additive_normalization_missing"
        and decisions[53].decision == "repair_selected_row_missing"
        and decisions[54].decision == "normalize_additive_value_then_apply_source_snippet_intake"
        and decisions[55].decision == "repair_edge_plus_boundary_zero_lattice"
        and decisions[56].decision == "reject_wrong_or_nonlegal_product_row"
        and decisions[57].decision == "repair_missing_arithmetic_source_theorem"
        and decisions[58].decision == "repair_selector_only"
        and decisions[59].decision == "reject_boundary_control_not_source_object"
        and decisions[60].decision == "reject_h90_support_below_lower_bound"
        and decisions[61].decision == "repair_exact_selector_theorem_missing"
        and decisions[62].decision == "repair_theta2_intake_missing"
        and decisions[63].decision == "repair_exactp_orientation_branch_missing"
        and decisions[64].decision == "repair_period156_branch_selection_missing"
        and decisions[65].decision == "reject_wrong_exactp_payload"
        and decisions[66].decision == "reject_by_finite_geometry_rigidity"
        and decisions[67].decision == "repair_period156_branch_selection_missing"
        and decisions[68].decision == "repair_reverse_selector_structure_missing"
        and decisions[69].decision == "source_stage_win_danger3_framing_missing"
        and decisions[70].decision == "repair_value_divisor_theorem_missing"
        and decisions[71].decision == "repair_quartic_edge_selection_missing"
        and decisions[72].decision == "repair_mixed_tensor_missing"
        and decisions[73].decision == "reject_zero_boundary_wrong_edge"
        and decisions[74].decision == "repair_reciprocal_orientation_or_boundary_sign_missing"
        and decisions[75].decision == "repair_phase_orientation_collision"
        and decisions[76].decision == "reject_orientation_boundary_mismatch"
        and decisions[77].decision == "support_diagonal_aggregate_selector_missing"
        and decisions[78].decision == "repair_oriented_square_root_missing"
        and decisions[79].decision == "normalize_to_one_edge_then_apply_source_snippet_intake"
        and decisions[80].decision == "reject_zero_boundary_wrong_edge"
        and decisions[81].decision == "repair_extraction_map_missing_after_two_root_row_payload"
        and decisions[82].decision == "repair_scalar_and_root_orientation_missing"
        and decisions[83].decision == "reject_sign_invisible_to_current_invariants"
        and decisions[84].decision == "submission_ready"
        and all(d.ok for d in decisions)
    )
    return SourceSnippetIntake(
        evidence_markers=markers,
        candidates=candidates,
        decisions=decisions,
        evidence_markers_ok=evidence_ok,
        source_stage_closing_shapes=source_closing,
        direct_submission_shapes=submission,
        current_source_stage_closers=current_source_stage,
        current_submission_ready=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    intake = build_intake()
    for marker_row in intake.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("snippet_decisions")
    for decision in intake.decisions:
        print(
            "  "
            f"{decision.name}: decision={decision.decision} "
            f"legal={int(decision.legal_row)} source_closed={int(decision.source_stage_closed)} "
            f"missing={decision.first_missing} submission={int(decision.submission_ready)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={intake.evidence_markers_ok}/{len(intake.evidence_markers)}")
    print(f"  source_stage_closing_shapes={intake.source_stage_closing_shapes}")
    print(f"  direct_submission_shapes={intake.direct_submission_shapes}")
    print(f"  current_source_stage_closers={intake.current_source_stage_closers}")
    print(f"  current_submission_ready={intake.current_submission_ready}")
    print(f"p25_v2_source_snippet_intake_rows={int(intake.row_ok)}/1")
    return 0 if intake.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
