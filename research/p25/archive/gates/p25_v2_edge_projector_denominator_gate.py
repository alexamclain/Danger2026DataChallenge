#!/usr/bin/env python3
"""Validate the quotient-C4 edge projector denominator screen for p25."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P25 = 10000000000000000000000013
EDGE_ORDER = ("m1", "m2", "m4", "m8")

PROJECTORS = {
    "constant": (1, 1, 1, 1),
    "odd_row": (1, 1, -1, -1),
    "even_column": (1, -1, -1, 1),
    "checkerboard": (1, -1, 1, -1),
}

EDGE_EXPANSIONS = {
    "m1": ("constant", "odd_row", "even_column", "checkerboard"),
    "m2": ("constant", "odd_row", "-even_column", "-checkerboard"),
    "m4": ("constant", "-odd_row", "-even_column", "checkerboard"),
    "m8": ("constant", "-odd_row", "even_column", "-checkerboard"),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ProjectorIdentity:
    edge: str
    four_edge_vector: tuple[int, int, int, int]
    expansion_terms: tuple[str, str, str, str]
    expansion_vector: tuple[int, int, int, int]
    ok: bool


@dataclass(frozen=True)
class IntakeRoute:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class EdgeProjectorDenominator:
    evidence_markers: tuple[EvidenceMarker, ...]
    projector_boundary_scales: dict[str, int]
    identities: tuple[ProjectorIdentity, ...]
    p_mod_4: int
    gcd_4_p_minus_1: int
    accepted_routes: tuple[IntakeRoute, ...]
    repair_routes: tuple[IntakeRoute, ...]
    current_source_theorems: int
    current_submission_ready: int
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
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
    )


def signed_projector(term: str) -> tuple[int, int, int, int]:
    if term.startswith("-"):
        vector = PROJECTORS[term[1:]]
        return tuple(-value for value in vector)
    return PROJECTORS[term]


def add_vectors(vectors: tuple[tuple[int, int, int, int], ...]) -> tuple[int, int, int, int]:
    return tuple(sum(vector[index] for vector in vectors) for index in range(4))


def four_edge(edge: str) -> tuple[int, int, int, int]:
    return tuple(4 if name == edge else 0 for name in EDGE_ORDER)


def projector_boundary_scales() -> dict[str, int]:
    return {name: sum(vector) for name, vector in PROJECTORS.items()}


def projector_identities() -> tuple[ProjectorIdentity, ...]:
    identities = []
    for edge, terms in EDGE_EXPANSIONS.items():
        expansion = add_vectors(tuple(signed_projector(term) for term in terms))
        target = four_edge(edge)
        identities.append(
            ProjectorIdentity(
                edge=edge,
                four_edge_vector=target,
                expansion_terms=terms,
                expansion_vector=expansion,
                ok=target == expansion,
            )
        )
    return tuple(identities)


def accepted_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("direct_one_edge_theorem", "source_stage_candidate_if_theorem_present", True),
        IntakeRoute("projector_theorem_with_explicit_fourth_root", "normalize_selected_root_then_intake", True),
    )


def repair_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("constant_component_only", "repair_all_four_or_4W_boundary_not_one_edge", True),
        IntakeRoute("row_or_column_component_only", "repair_boundary_zero_selector_missing", True),
        IntakeRoute("checkerboard_component_only", "repair_boundary_zero_selector_missing", True),
        IntakeRoute("all_projector_values_without_root", "repair_mu4_root_or_scalar_missing", True),
        IntakeRoute("fourth_power_value_only", "repair_mu4_root_selection_missing", True),
    )


def build_screen() -> EdgeProjectorDenominator:
    markers = evidence_markers()
    scales = projector_boundary_scales()
    identities = projector_identities()
    p_mod_4 = P25 % 4
    gcd_4 = 4 if (P25 - 1) % 4 == 0 else 2 if (P25 - 1) % 2 == 0 else 1
    accepted = accepted_routes()
    repairs = repair_routes()
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and scales == {
            "constant": 4,
            "odd_row": 0,
            "even_column": 0,
            "checkerboard": 0,
        }
        and len(identities) == 4
        and all(row.ok for row in identities)
        and p_mod_4 == 1
        and gcd_4 == 4
        and len(accepted) == 2
        and all(row.ok for row in accepted)
        and len(repairs) == 5
        and all(row.ok for row in repairs)
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return EdgeProjectorDenominator(
        evidence_markers=markers,
        projector_boundary_scales=scales,
        identities=identities,
        p_mod_4=p_mod_4,
        gcd_4_p_minus_1=gcd_4,
        accepted_routes=accepted,
        repair_routes=repairs,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_screen()
    print("p25 v2 edge projector denominator")
    for marker_row in screen.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"edge_order={EDGE_ORDER}")
    print("projector_boundary_scales")
    for name, scale in screen.projector_boundary_scales.items():
        print(f"  {name}: {scale}W")
    print("edge_projector_identities")
    for identity in screen.identities:
        terms = " + ".join(identity.expansion_terms)
        print(f"  4*{identity.edge} = {terms}: {'ok' if identity.ok else 'FAIL'}")
    print("p25_power_data")
    print(f"  p_mod_4={screen.p_mod_4}")
    print(f"  gcd_4_p_minus_1={screen.gcd_4_p_minus_1}")
    print("accepted_routes")
    for route in screen.accepted_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("repair_routes")
    for route in screen.repair_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in screen.evidence_markers)}/{len(screen.evidence_markers)}")
    print(f"  projector_identities_ok={sum(row.ok for row in screen.identities)}/{len(screen.identities)}")
    print(f"  accepted_routes={len(screen.accepted_routes)}")
    print(f"  repair_routes={len(screen.repair_routes)}")
    print(f"  current_source_theorems={screen.current_source_theorems}")
    print(f"  current_submission_ready={screen.current_submission_ready}")
    print(f"p25_v2_edge_projector_denominator_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
