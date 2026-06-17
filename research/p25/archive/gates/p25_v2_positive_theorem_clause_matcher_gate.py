#!/usr/bin/env python3
"""Positive-clause matcher for the p25 H0/Y507 theorem front door.

This gate is deliberately narrower than the full expert-response rubric.  It
records the exact clauses a future expert/source answer must contain before it
can be promoted from "interesting" to "source-stage theorem candidate" for the
current H0/conductor-39/H0-Y507 target.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class PositiveRoute:
    name: str
    lane: str
    required_clauses: tuple[str, ...]
    first_downstream_missing: str
    source_stage_shape: bool
    currently_in_hand: bool
    ok: bool


@dataclass(frozen=True)
class NearMiss:
    name: str
    provided_shape: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class PositiveTheoremClauseMatcher:
    evidence_markers: tuple[EvidenceMarker, ...]
    positive_routes: tuple[PositiveRoute, ...]
    near_misses: tuple[NearMiss, ...]
    evidence_markers_ok: int
    h0_y507_frontdoor_routes: int
    exactp_heavy_routes: int
    source_stage_shapes: int
    current_source_theorems: int
    current_submission_ready: int
    near_miss_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "unified_submission_extraction",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
    )


def positive_routes() -> tuple[PositiveRoute, ...]:
    return (
        PositiveRoute(
            name="canonical_h0_divisor_additive_identity",
            lane="H0/conductor39",
            required_clauses=(
                "one_exact_oriented_edge_R_m",
                "arithmetic_source_theorem",
                "Norm_156_Y_507_boundary",
                "scalar_fixed_finite_divisor_additive_identity",
            ),
            first_downstream_missing="DANGER3 finite-identity / non-CM framing",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
        PositiveRoute(
            name="quartic_character_finite_theorem",
            lane="H0/conductor39",
            required_clauses=(
                "Norm_156_Y_507_or_W_boundary",
                "exact_row_antisymmetric_C4_1_phase",
                "mixed_tensor_row_sign",
                "arithmetic_source_theorem",
                "scalar_fixed_finite_divisor_additive_identity",
            ),
            first_downstream_missing="DANGER3 finite-identity / non-CM framing",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
        PositiveRoute(
            name="canonical_h0_period156_value_identity",
            lane="H0/Y507 value route",
            required_clauses=(
                "canonical_H0_value",
                "one_exact_oriented_edge_R_m",
                "arithmetic_source_theorem",
                "Norm_156_Y_507_boundary",
                "period156_branch_root_telescoping_context",
            ),
            first_downstream_missing="DANGER3 finite-identity / non-CM framing",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
        PositiveRoute(
            name="Y_507_period156_value_identity",
            lane="H0/Y507 value route",
            required_clauses=(
                "Y_507_value",
                "arithmetic_source_theorem",
                "period156_branch_root_telescoping_context",
                "H0_Y507_compatibility_bridge",
            ),
            first_downstream_missing="DANGER3 finite-identity / non-CM framing",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
        PositiveRoute(
            name="power_normalized_row_value_theorem",
            lane="H0/conductor39",
            required_clauses=(
                "one_exact_oriented_edge_R_m",
                "arithmetic_source_theorem",
                "exact_finite_Fp_value_for_R_m_power_e_with_e_in_3_5_13_39_75_169_507",
                "inverse_exponent_recovery_mod_pminus1",
                "Norm_156_Y_507_boundary_or_accepted_period156_bridge",
            ),
            first_downstream_missing="DANGER3 finite-identity / non-CM framing",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
        PositiveRoute(
            name="exactp_upstream_bridge_theorem",
            lane="exact-P",
            required_clauses=(
                "exact_75_atom_or_theta2_payload",
                "orientation_and_bridge_data",
                "arithmetic_source_theorem",
                "bridge_75_300_12_312_156",
            ),
            first_downstream_missing="DANGER3 framing and extraction after upstream theorem",
            source_stage_shape=True,
            currently_in_hand=False,
            ok=True,
        ),
    )


def near_misses() -> tuple[NearMiss, ...]:
    return (
        NearMiss(
            name="source_legality_only",
            provided_shape="Koo-Shin/Yang source certificate or class-field generation",
            decision="repair_finite_theorem_missing",
            first_missing_or_falsifier="finite scalar-fixed value/divisor theorem",
            ok=True,
        ),
        NearMiss(
            name="boundary_only",
            provided_shape="Norm_156(Y_507) or Hilbert-90 boundary without a row identity",
            decision="repair_identity_for_one_edge_missing",
            first_missing_or_falsifier="finite identity for one exact oriented edge",
            ok=True,
        ),
        NearMiss(
            name="h0_value_without_boundary",
            provided_shape="H0 value theorem but no Norm_156(Y_507) boundary",
            decision="repair_boundary_missing",
            first_missing_or_falsifier="H0/Y507 boundary compatibility",
            ok=True,
        ),
        NearMiss(
            name="h0_or_y507_value_without_period156_context",
            provided_shape="bare H0/Y507 value theorem",
            decision="repair_period156_branch_context_missing",
            first_missing_or_falsifier="period-156 branch/root/telescoping context",
            ok=True,
        ),
        NearMiss(
            name="ambient780_or_mu11_value",
            provided_shape="ambient period-780 value, 11th power, or mu_11 quotient",
            decision="repair_period156_value_selection_missing",
            first_missing_or_falsifier="one selected F_p value on the support-period-156 branch",
            ok=True,
        ),
        NearMiss(
            name="ambiguous_power_value_without_selector",
            provided_shape="R_m^2, R_m^4, R_m^11, R_m^22, R_m^44, R_m^156, or R_m^780 value without branch/orientation/scalar data",
            decision="repair_power_root_selection_missing",
            first_missing_or_falsifier="kernel root selector or one of the bijective exponents 3, 5, 13, 39, 75, 169, 507",
            ok=True,
        ),
        NearMiss(
            name="formal_one_coset_value",
            provided_shape="formal one-coset H value with matching boundary",
            decision="reject_boundary_control_not_source_object",
            first_missing_or_falsifier="proper-axis pushforward and mixed-source fingerprint",
            ok=True,
        ),
        NearMiss(
            name="projector_or_two_edge_value",
            provided_shape="projector, row-pair, column-pair, or diagonal-pair value",
            decision="repair_oriented_edge_selection_missing",
            first_missing_or_falsifier="fourth-root or oriented-square-root selector for one edge",
            ok=True,
        ),
        NearMiss(
            name="exact_quartic_selector_without_finite_theorem",
            provided_shape="exact row-antisymmetric C4_1 phase selecting one legal edge",
            decision="repair_value_divisor_theorem_missing",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem for the selected row",
            ok=True,
        ),
        NearMiss(
            name="coarse_quartic_phase_or_magnitude_only",
            provided_shape="one quartic sign, quartic magnitude, quadratic component, or boundary-visible component",
            decision="repair_quartic_edge_selection_missing",
            first_missing_or_falsifier="exact row-antisymmetric C4_1 phase selecting one legal edge",
            ok=True,
        ),
        NearMiss(
            name="quartic_phase_without_row_sign",
            provided_shape="quotient-C4 phase data without mixed tensor row sign",
            decision="repair_mixed_tensor_missing",
            first_missing_or_falsifier="row-antisymmetric mixed tensor structure for the conductor-39 source row",
            ok=True,
        ),
        NearMiss(
            name="same_parity_quartic_phase",
            provided_shape="same-parity quartic character edge",
            decision="reject_zero_boundary_wrong_edge",
            first_missing_or_falsifier="same-parity edges have zero W boundary or the wrong mixed tensor target",
            ok=True,
        ),
        NearMiss(
            name="finite_payload_without_source",
            provided_shape="local finite product, hash match, or computed payload",
            decision="repair_arithmetic_source_missing",
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            ok=True,
        ),
        NearMiss(
            name="exactp_vocabulary_only",
            provided_shape="normalized-y, KL exponent, or theta vocabulary without exact packet theorem",
            decision="repair_exactp_theorem_missing",
            first_missing_or_falsifier="exact 75-atom/theta2 payload with bridge and orientation",
            ok=True,
        ),
    )


def build_matcher() -> PositiveTheoremClauseMatcher:
    markers = evidence_markers()
    routes = positive_routes()
    misses = near_misses()
    evidence_ok = sum(row.ok for row in markers)
    h0_y507 = sum(route.lane != "exact-P" for route in routes)
    exactp = sum(route.lane == "exact-P" for route in routes)
    source_stage_shapes = sum(route.source_stage_shape for route in routes)
    current_source_theorems = sum(route.currently_in_hand for route in routes)
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(routes) == 6
        and h0_y507 == 5
        and exactp == 1
        and source_stage_shapes == 6
        and current_source_theorems == 0
        and current_submission_ready == 0
        and len(misses) == 14
        and all(route.ok and route.required_clauses for route in routes)
        and all(miss.ok and miss.first_missing_or_falsifier for miss in misses)
    )
    return PositiveTheoremClauseMatcher(
        evidence_markers=markers,
        positive_routes=routes,
        near_misses=misses,
        evidence_markers_ok=evidence_ok,
        h0_y507_frontdoor_routes=h0_y507,
        exactp_heavy_routes=exactp,
        source_stage_shapes=source_stage_shapes,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        near_miss_rows=len(misses),
        row_ok=row_ok,
    )


def main() -> int:
    matcher = build_matcher()
    print("p25 v2 positive theorem clause matcher")
    for marker_row in matcher.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("positive_routes")
    for route in matcher.positive_routes:
        print(
            f"  {route.name}: lane={route.lane} "
            f"clauses={len(route.required_clauses)} in_hand={int(route.currently_in_hand)}"
        )
        for clause in route.required_clauses:
            print(f"    requires={clause}")
        print(f"    first_downstream_missing={route.first_downstream_missing}")
    print("near_misses")
    for miss in matcher.near_misses:
        print(f"  {miss.name}: decision={miss.decision}")
        print(f"    shape={miss.provided_shape}")
        print(f"    missing_or_falsifier={miss.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={matcher.evidence_markers_ok}/{len(matcher.evidence_markers)}")
    print(f"  h0_y507_frontdoor_routes={matcher.h0_y507_frontdoor_routes}")
    print(f"  exactp_heavy_routes={matcher.exactp_heavy_routes}")
    print(f"  source_stage_shapes={matcher.source_stage_shapes}")
    print(f"  current_source_theorems={matcher.current_source_theorems}")
    print(f"  current_submission_ready={matcher.current_submission_ready}")
    print(f"  near_miss_rows={matcher.near_miss_rows}")
    print(f"p25_v2_positive_theorem_clause_matcher_rows={int(matcher.row_ok)}/1")
    return 0 if matcher.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
