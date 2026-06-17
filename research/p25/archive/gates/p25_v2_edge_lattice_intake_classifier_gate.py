#!/usr/bin/env python3
"""Classify integer combinations of the four p25 source-graph edges.

The source graph normal form says the current target is one oriented edge of a
quotient-C4 K_{2,2} graph.  This gate records the corresponding edge-lattice
rule: for an integer combination of the four edge rows, the Hilbert-90 boundary
scale is the coefficient sum.  A W-boundary combination is source-closing only
when it is exactly one edge; otherwise it is one edge plus a nonzero
boundary-zero lattice element and remains repair.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path

from p25_v2_source_graph_normal_form_gate import build_normal_form


EDGE_ORDER = (1, 2, 4, 8)
BOUNDED_INTAKE_RANGE = (-1, 0, 1, 2)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class LatticeVector:
    coefficients: tuple[int, int, int, int]
    boundary_scale_w: int
    l1_norm: int
    exact_one_edge: bool
    zero_boundary_nonzero: bool
    w_boundary_nonedge: bool
    scale_two_or_more: bool
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class IntakeDecision:
    name: str
    coefficient_condition: str
    decision: str
    missing: str
    ok: bool


@dataclass(frozen=True)
class EdgeLatticeIntakeClassifier:
    evidence_markers: tuple[EvidenceMarker, ...]
    decisions: tuple[IntakeDecision, ...]
    sample_vectors: tuple[LatticeVector, ...]
    legal_edge_vectors: int
    zero_boundary_nonzero_vectors: int
    w_boundary_nonedge_vectors: int
    scale_two_vectors: int
    all_w_boundary_nonedge_decompose_as_edge_plus_zero: bool
    source_candidate_routes: int
    repair_or_reject_routes: int
    current_source_theorems: int
    submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
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
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
    )


def is_unit_vector(vector: tuple[int, int, int, int]) -> bool:
    return sum(1 for value in vector if value == 1) == 1 and sum(1 for value in vector if value != 0) == 1


def can_decompose_as_edge_plus_zero(vector: tuple[int, int, int, int]) -> bool:
    if sum(vector) != 1 or is_unit_vector(vector):
        return False
    for index in range(len(vector)):
        zero_part = tuple(value - (1 if i == index else 0) for i, value in enumerate(vector))
        if sum(zero_part) == 0 and any(value != 0 for value in zero_part):
            return True
    return False


def classify_vector(vector: tuple[int, int, int, int]) -> LatticeVector:
    boundary_scale = sum(vector)
    exact_edge = is_unit_vector(vector)
    zero_boundary = boundary_scale == 0 and any(value != 0 for value in vector)
    w_boundary_nonedge = boundary_scale == 1 and not exact_edge
    scale_two_or_more = boundary_scale >= 2
    if exact_edge:
        decision = "source_stage_candidate_if_theorem_present"
    elif zero_boundary:
        decision = "repair_boundary_zero_relation"
    elif w_boundary_nonedge:
        decision = "repair_edge_plus_boundary_zero_lattice"
    elif scale_two_or_more:
        decision = "repair_or_reject_scaled_boundary"
    else:
        decision = "reject_wrong_boundary_scale"
    return LatticeVector(
        coefficients=vector,
        boundary_scale_w=boundary_scale,
        l1_norm=sum(abs(value) for value in vector),
        exact_one_edge=exact_edge,
        zero_boundary_nonzero=zero_boundary,
        w_boundary_nonedge=w_boundary_nonedge,
        scale_two_or_more=scale_two_or_more,
        decision=decision,
        row_ok=True,
    )


def intake_decisions() -> tuple[IntakeDecision, ...]:
    return (
        IntakeDecision(
            name="unit_edge_vector",
            coefficient_condition="one coefficient is 1 and the other three are 0",
            decision="source_stage_candidate_if_theorem_present",
            missing="finite value/divisor theorem plus downstream extraction",
            ok=True,
        ),
        IntakeDecision(
            name="nonzero_zero_sum_vector",
            coefficient_condition="sum coefficients = 0, vector nonzero",
            decision="repair_boundary_zero_relation",
            missing="one-edge theorem; quotient/invariant has no W boundary",
            ok=True,
        ),
        IntakeDecision(
            name="w_boundary_nonedge_vector",
            coefficient_condition="sum coefficients = 1, but not a unit edge",
            decision="repair_edge_plus_boundary_zero_lattice",
            missing="finite value for the boundary-zero part or direct one-edge theorem",
            ok=True,
        ),
        IntakeDecision(
            name="scaled_boundary_vector",
            coefficient_condition="sum coefficients != 1",
            decision="repair_or_reject_scaled_boundary",
            missing="root/orientation/value normalization or rewrite to one W-boundary edge",
            ok=True,
        ),
    )


def build_classifier() -> EdgeLatticeIntakeClassifier:
    markers = evidence_markers()
    normal_form = build_normal_form()
    sample_vectors = tuple(
        classify_vector(tuple(vector))
        for vector in product(BOUNDED_INTAKE_RANGE, repeat=len(EDGE_ORDER))
    )
    legal_edges = sum(row.exact_one_edge for row in sample_vectors)
    zero_boundary = sum(row.zero_boundary_nonzero for row in sample_vectors)
    w_nonedge = sum(row.w_boundary_nonedge for row in sample_vectors)
    scale_two = sum(row.boundary_scale_w == 2 for row in sample_vectors)
    all_w_nonedge_decompose = all(
        can_decompose_as_edge_plus_zero(row.coefficients)
        for row in sample_vectors
        if row.w_boundary_nonedge
    )
    decisions = intake_decisions()
    source_candidates = sum(
        row.decision == "source_stage_candidate_if_theorem_present" for row in decisions
    )
    repair_or_reject = len(decisions) - source_candidates
    current_source_theorems = 0
    submission_ready_rows = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and normal_form.row_ok
        and legal_edges == 4
        and zero_boundary > 0
        and w_nonedge > 0
        and scale_two > 0
        and all_w_nonedge_decompose
        and source_candidates == 1
        and repair_or_reject == 3
        and current_source_theorems == 0
        and submission_ready_rows == 0
        and all(row.row_ok for row in sample_vectors)
        and all(row.ok for row in decisions)
    )
    return EdgeLatticeIntakeClassifier(
        evidence_markers=markers,
        decisions=decisions,
        sample_vectors=sample_vectors,
        legal_edge_vectors=legal_edges,
        zero_boundary_nonzero_vectors=zero_boundary,
        w_boundary_nonedge_vectors=w_nonedge,
        scale_two_vectors=scale_two,
        all_w_boundary_nonedge_decompose_as_edge_plus_zero=all_w_nonedge_decompose,
        source_candidate_routes=source_candidates,
        repair_or_reject_routes=repair_or_reject,
        current_source_theorems=current_source_theorems,
        submission_ready_rows=submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    classifier = build_classifier()
    print("p25 v2 edge lattice intake classifier")
    for marker_row in classifier.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"edge_order={EDGE_ORDER}")
    print(f"bounded_intake_range={BOUNDED_INTAKE_RANGE}")
    print("decisions")
    for decision in classifier.decisions:
        print(
            "  "
            f"{decision.name}: condition={decision.coefficient_condition} "
            f"decision={decision.decision} missing={decision.missing} ok={int(decision.ok)}"
        )
    print("checks")
    print(f"  sample_vectors={len(classifier.sample_vectors)}")
    print(f"  legal_edge_vectors={classifier.legal_edge_vectors}")
    print(f"  zero_boundary_nonzero_vectors={classifier.zero_boundary_nonzero_vectors}")
    print(f"  w_boundary_nonedge_vectors={classifier.w_boundary_nonedge_vectors}")
    print(f"  scale_two_vectors={classifier.scale_two_vectors}")
    print(
        "  "
        f"all_w_boundary_nonedge_decompose_as_edge_plus_zero="
        f"{int(classifier.all_w_boundary_nonedge_decompose_as_edge_plus_zero)}"
    )
    print(f"  source_candidate_routes={classifier.source_candidate_routes}")
    print(f"  repair_or_reject_routes={classifier.repair_or_reject_routes}")
    print(f"  current_source_theorems={classifier.current_source_theorems}")
    print(f"  submission_ready_rows={classifier.submission_ready_rows}")
    print(f"p25_v2_edge_lattice_intake_classifier_rows={int(classifier.row_ok)}/1")
    return 0 if classifier.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
