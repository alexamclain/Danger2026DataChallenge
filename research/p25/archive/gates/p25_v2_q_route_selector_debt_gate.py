#!/usr/bin/env python3
"""Classify the selector debt left by the compact conductor-39 Q route.

The norm-one quotient Q is useful because Q^6 has the current Hilbert-90
boundary.  This gate records the remaining debt: Q-boundary data is still
downstream of the quotient-C4 edge selector.  A Q theorem is a support route
unless it also supplies the edge selector/value theorem or a normalization
that recovers one legal edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_v2_conductor39_norm_one_quotient_route_gate import build_route as build_q_route
from p25_v2_edge_lattice_intake_classifier_gate import build_classifier
from p25_v2_frobenius_tensor_eigenboundary_gate import build_screen
from p25_v2_minimal_expert_ask_gate import build_ask


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class DebtInvariant:
    name: str
    statement: str
    ok: bool


@dataclass(frozen=True)
class DebtRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    source_candidate: bool
    support: bool
    normalize: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class QRouteSelectorDebt:
    evidence_markers: tuple[EvidenceMarker, ...]
    invariants: tuple[DebtInvariant, ...]
    routes: tuple[DebtRoute, ...]
    evidence_markers_ok: int
    invariants_ok: int
    source_candidate_routes: int
    support_routes: int
    normalize_routes: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "conductor39_norm_one_quotient_route",
            "research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
            "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
        ),
        marker(
            "frobenius_tensor_eigenboundary",
            "research/p25/evidence/p25_v2_frobenius_tensor_eigenboundary_20260616.md",
            "p25_v2_frobenius_tensor_eigenboundary_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "current_source_stage_closers = 0",
        ),
    )


def debt_invariants() -> tuple[DebtInvariant, ...]:
    q_route = build_q_route()
    eigen = build_screen()
    lattice = build_classifier()
    ask = build_ask()
    return (
        DebtInvariant(
            "q_boundary_is_current_w",
            "Q^6=(1-Frob_p)(Q^3) has the current W boundary, but Q route source theorems are still zero",
            q_route.row_ok and q_route.support_routes == 2 and q_route.current_source_theorems == 0,
        ),
        DebtInvariant(
            "frobenius_erases_edge_phase",
            "The Hilbert-90 boundary map kills the order-4 C4 selector phases for all four legal rows",
            eigen.row_ok
            and eigen.rows_with_order4_components_killed == 4
            and eigen.common_boundary_rows == 4,
        ),
        DebtInvariant(
            "one_edge_is_the_intake_target",
            "The edge lattice has exactly one source-candidate intake route: a unit edge vector",
            lattice.row_ok
            and lattice.source_candidate_routes == 1
            and lattice.all_w_boundary_nonedge_decompose_as_edge_plus_zero,
        ),
        DebtInvariant(
            "expert_ask_has_q_near_misses",
            "The minimal expert ask now includes Q support rows and Q repair/reject rows",
            ask.row_ok
            and len(ask.accepted_routes) == 6
            and len(ask.repair_or_reject_routes) == 26,
        ),
    )


def debt_routes() -> tuple[DebtRoute, ...]:
    return (
        DebtRoute(
            "q_value_period156_context_only",
            "support_route_selector_debt_remains",
            "edge-selecting order-4 C4 phase, boundary-zero value, or direct one-edge theorem",
            source_candidate=False,
            support=True,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "q3_h90_preimage_finite_theorem_only",
            "support_route_selector_debt_remains",
            "theorem data that recovers one oriented quotient-C4 edge before source-stage promotion",
            source_candidate=False,
            support=True,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "q_with_order4_selector_and_finite_edge_theorem",
            "source_stage_candidate_if_scalar_fixed_theorem_present",
            "DANGER3 framing and extraction after theorem hit",
            source_candidate=True,
            support=False,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "q_plus_boundary_zero_value_or_selector",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            "same theorem data after subtracting the boundary-zero lattice content or selecting one edge",
            source_candidate=False,
            support=False,
            normalize=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "q_source_or_coset_selector_only",
            "repair_finite_value_divisor_theorem_missing",
            "finite value/divisor theorem for Q, Q^3, Q^6, or the selected Yang lift",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "q6_boundary_only",
            "repair_additive_or_value_normalization_missing",
            "scalar-fixed finite value/additive data plus edge selector, not just Hilbert-90 boundary",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        DebtRoute(
            "pure_character_degree6_norm",
            "reject_pure_character_degree6_norm_cancels",
            "Frobenius alternation makes the degree-6 norm zero",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_debt() -> QRouteSelectorDebt:
    markers = evidence_markers()
    invariants = debt_invariants()
    routes = debt_routes()
    evidence_ok = sum(row.ok for row in markers)
    invariants_ok = sum(row.ok for row in invariants)
    source_candidates = sum(row.source_candidate for row in routes)
    support = sum(row.support for row in routes)
    normalize = sum(row.normalize for row in routes)
    repairs = sum(row.repair for row in routes)
    rejects = sum(row.reject for row in routes)
    current_source_theorems = 0
    expected = (
        "support_route_selector_debt_remains",
        "support_route_selector_debt_remains",
        "source_stage_candidate_if_scalar_fixed_theorem_present",
        "normalize_to_one_edge_then_apply_source_snippet_intake",
        "repair_finite_value_divisor_theorem_missing",
        "repair_additive_or_value_normalization_missing",
        "reject_pure_character_degree6_norm_cancels",
    )
    row_ok = (
        evidence_ok == len(markers)
        and len(invariants) == 4
        and invariants_ok == 4
        and len(routes) == 7
        and tuple(row.decision for row in routes) == expected
        and source_candidates == 1
        and support == 2
        and normalize == 1
        and repairs == 2
        and rejects == 1
        and current_source_theorems == 0
        and all(row.ok for row in routes)
    )
    return QRouteSelectorDebt(
        evidence_markers=markers,
        invariants=invariants,
        routes=routes,
        evidence_markers_ok=evidence_ok,
        invariants_ok=invariants_ok,
        source_candidate_routes=source_candidates,
        support_routes=support,
        normalize_routes=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    debt = build_debt()
    print("p25 v2 Q-route selector debt")
    for marker_row in debt.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("invariants")
    for invariant in debt.invariants:
        print(f"  {invariant.name}: ok={int(invariant.ok)}")
        print(f"    {invariant.statement}")
    print("routes")
    for route in debt.routes:
        print(f"  {route.name}: decision={route.decision}")
        print(f"    missing_or_falsifier={route.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={debt.evidence_markers_ok}/{len(debt.evidence_markers)}")
    print(f"  invariants_ok={debt.invariants_ok}/{len(debt.invariants)}")
    print(f"  source_candidate_routes={debt.source_candidate_routes}")
    print(f"  support_routes={debt.support_routes}")
    print(f"  normalize_routes={debt.normalize_routes}")
    print(f"  repair_rows={debt.repair_rows}")
    print(f"  reject_rows={debt.reject_rows}")
    print(f"  current_source_theorems={debt.current_source_theorems}")
    print(f"p25_v2_q_route_selector_debt_rows={int(debt.row_ok)}/1")
    return 0 if debt.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
