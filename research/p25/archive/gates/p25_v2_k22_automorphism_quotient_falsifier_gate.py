#!/usr/bin/env python3
"""Classify nontrivial K_{2,2} automorphism quotients for the p25 source graph.

The first-pass H0/conductor-39 target is one oriented quotient-C4 edge.  This
gate records the finite combinatorial obstruction to promoting a theorem that
is only invariant under a nontrivial symmetry of the four-edge K_{2,2} graph:
every nontrivial quotient orbit has size two or four, so it carries 2W/4W
boundary as a product aggregate, or boundary zero as a quotient relation.  It
does not isolate one scalar-fixed W-boundary edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EDGES = ("m1", "m2", "m4", "m8")
EDGE_COORDS = {
    "m1": ("7H", "4H"),
    "m2": ("7H", "H"),
    "m4": ("2H", "H"),
    "m8": ("2H", "4H"),
}

AUTOMORPHISMS = {
    "identity": {"m1": "m1", "m2": "m2", "m4": "m4", "m8": "m8"},
    "row_swap": {"m1": "m8", "m8": "m1", "m2": "m4", "m4": "m2"},
    "column_swap": {"m1": "m2", "m2": "m1", "m4": "m8", "m8": "m4"},
    "row_column_swap": {"m1": "m4", "m4": "m1", "m2": "m8", "m8": "m2"},
}

SUBGROUP_GENERATORS = {
    "identity_singletons": (),
    "row_swap_pairs": ("row_swap",),
    "column_swap_pairs": ("column_swap",),
    "diagonal_pairs": ("row_column_swap",),
    "full_k22_symmetry": ("row_swap", "column_swap"),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OrbitRow:
    name: str
    generators: tuple[str, ...]
    orbits: tuple[tuple[str, ...], ...]
    min_orbit_size: int
    max_orbit_size: int
    product_boundary_scales: tuple[int, ...]
    quotient_boundary_scale: int
    decision: str
    source_stage_candidate: bool
    ok: bool


@dataclass(frozen=True)
class IntakeRoute:
    name: str
    provided_shape: str
    decision: str
    first_missing_or_falsifier: str
    source_stage_candidate: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class K22AutomorphismQuotientFalsifier:
    evidence_markers: tuple[EvidenceMarker, ...]
    orbit_rows: tuple[OrbitRow, ...]
    routes: tuple[IntakeRoute, ...]
    automorphism_group_order: int
    subgroup_rows: int
    nontrivial_subgroups: int
    nontrivial_singleton_orbits: int
    accepted_routes: int
    repair_routes: int
    reject_routes: int
    current_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "orbit_tuple_theorem_router",
            "research/p25/evidence/p25_v2_orbit_tuple_theorem_router_20260616.md",
            "p25_v2_orbit_tuple_theorem_router_rows=1/1",
        ),
        marker(
            "edge_lattice_global_minimality",
            "research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
            "p25_v2_edge_lattice_global_minimality_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
    )


def compose(left: dict[str, str], right: dict[str, str]) -> dict[str, str]:
    return {edge: left[right[edge]] for edge in EDGES}


def generated_group(generators: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    group = [AUTOMORPHISMS["identity"]]
    changed = True
    while changed:
        changed = False
        for current in tuple(group):
            for gen_name in generators:
                candidate = compose(AUTOMORPHISMS[gen_name], current)
                if candidate not in group:
                    group.append(candidate)
                    changed = True
    return tuple(group)


def orbits_for(generators: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
    group = generated_group(generators)
    unseen = set(EDGES)
    orbits: list[tuple[str, ...]] = []
    while unseen:
        start = min(unseen, key=EDGES.index)
        orbit = {g[start] for g in group}
        ordered = tuple(edge for edge in EDGES if edge in orbit)
        orbits.append(ordered)
        unseen -= orbit
    return tuple(orbits)


def orbit_rows() -> tuple[OrbitRow, ...]:
    rows: list[OrbitRow] = []
    for name, generators in SUBGROUP_GENERATORS.items():
        orbits = orbits_for(generators)
        sizes = tuple(len(orbit) for orbit in orbits)
        source_candidate = name == "identity_singletons"
        if source_candidate:
            decision = "promote_only_if_one_row_has_scalar_fixed_finite_theorem"
        elif name == "diagonal_pairs":
            decision = "repair_diagonal_pair_selector_or_oriented_root_missing"
        elif name == "full_k22_symmetry":
            decision = "repair_all_four_aggregate_or_fourth_root_missing"
        else:
            decision = "repair_two_edge_selector_or_square_root_missing"
        rows.append(
            OrbitRow(
                name=name,
                generators=generators,
                orbits=orbits,
                min_orbit_size=min(sizes),
                max_orbit_size=max(sizes),
                product_boundary_scales=sizes,
                quotient_boundary_scale=0,
                decision=decision,
                source_stage_candidate=source_candidate,
                ok=(
                    (source_candidate and sizes == (1, 1, 1, 1))
                    or ((not source_candidate) and min(sizes) >= 2)
                ),
            )
        )
    return tuple(rows)


def intake_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute(
            name="identity_or_row_labeled_singleton",
            provided_shape="one oriented edge, or a row-labeled theorem containing one singleton edge",
            decision="source_stage_candidate_if_arithmetic_theorem_and_scalar_data_present",
            first_missing_or_falsifier="finite divisor/additive theorem or period-156 value theorem",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="row_or_column_pair_orbit",
            provided_shape="theorem invariant under row swap or column swap",
            decision="repair_two_edge_selector_missing",
            first_missing_or_falsifier="oriented square root, selected edge, or direct one-edge theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="diagonal_pair_orbit",
            provided_shape="theorem invariant under row-column swap, opposite-edge diagonal, or Q-style diagonal pair",
            decision="repair_diagonal_selector_missing",
            first_missing_or_falsifier="factorization/root down to one W-boundary edge",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="all_four_orbit",
            provided_shape="theorem for product, norm, trace, or symmetric aggregate over all four legal rows",
            decision="repair_fourth_root_or_row_labeling_missing",
            first_missing_or_falsifier="selected fourth root/scalar data or direct row-labeled theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="unlabeled_four_tuple",
            provided_shape="four identities or values with no map to m, edge labels, cosets, or hashes",
            decision="repair_row_labeling_missing",
            first_missing_or_falsifier="assignment to one exact oriented edge R_m",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="automorphism_invariant_value_only",
            provided_shape="value equality only after quotienting by a nontrivial graph symmetry",
            decision="repair_or_reject_selector_and_scalar_data_lost",
            first_missing_or_falsifier="row-antisymmetric C4 phase, mixed tensor sign, and scalar-fixed finite theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        IntakeRoute(
            name="orientation_reversing_or_vertex_projection_symmetry",
            provided_shape="symmetry that swaps source/target sides, projects to a vertex, or forgets the signed column",
            decision="reject_mixed_oriented_edge_not_preserved",
            first_missing_or_falsifier="oriented K22 edge preserving the mixed signed-column fingerprint",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_falsifier() -> K22AutomorphismQuotientFalsifier:
    markers = evidence_markers()
    rows = orbit_rows()
    routes = intake_routes()
    nontrivial = tuple(row for row in rows if row.name != "identity_singletons")
    nontrivial_singletons = sum(
        1 for row in nontrivial for orbit in row.orbits if len(orbit) == 1
    )
    accepted_routes = sum(route.source_stage_candidate for route in routes)
    repair_routes = sum(route.repair for route in routes)
    reject_routes = sum(route.reject for route in routes)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(m.ok for m in markers) == len(markers)
        and set(EDGE_COORDS) == set(EDGES)
        and len(set(EDGE_COORDS.values())) == 4
        and len(AUTOMORPHISMS) == 4
        and len(rows) == 5
        and all(row.ok for row in rows)
        and rows[0].orbits == (("m1",), ("m2",), ("m4",), ("m8",))
        and nontrivial_singletons == 0
        and accepted_routes == 1
        and repair_routes == 5
        and reject_routes == 1
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return K22AutomorphismQuotientFalsifier(
        evidence_markers=markers,
        orbit_rows=rows,
        routes=routes,
        automorphism_group_order=len(AUTOMORPHISMS),
        subgroup_rows=len(rows),
        nontrivial_subgroups=len(nontrivial),
        nontrivial_singleton_orbits=nontrivial_singletons,
        accepted_routes=accepted_routes,
        repair_routes=repair_routes,
        reject_routes=reject_routes,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    falsifier = build_falsifier()
    print("p25 v2 K22 automorphism quotient falsifier")
    for marker_row in falsifier.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("orbit rows")
    for row in falsifier.orbit_rows:
        generators = ",".join(row.generators) if row.generators else "identity"
        orbit_text = " ".join("{" + ",".join(orbit) + "}" for orbit in row.orbits)
        print(f"  {row.name}: generators={generators} orbits={orbit_text}")
        print(
            "    "
            f"product_boundary_scales={row.product_boundary_scales} "
            f"quotient_boundary_scale={row.quotient_boundary_scale} "
            f"decision={row.decision}"
        )
    print("routes")
    for route in falsifier.routes:
        print(f"  {route.name}: decision={route.decision}")
        print(f"    missing={route.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(m.ok for m in falsifier.evidence_markers)}/{len(falsifier.evidence_markers)}")
    print(f"  automorphism_group_order={falsifier.automorphism_group_order}")
    print(f"  subgroup_rows={falsifier.subgroup_rows}")
    print(f"  nontrivial_subgroups={falsifier.nontrivial_subgroups}")
    print(f"  nontrivial_singleton_orbits={falsifier.nontrivial_singleton_orbits}")
    print(f"  accepted_routes={falsifier.accepted_routes}")
    print(f"  repair_routes={falsifier.repair_routes}")
    print(f"  reject_routes={falsifier.reject_routes}")
    print(f"  current_source_theorems={falsifier.current_source_theorems}")
    print(f"  current_submission_ready={falsifier.current_submission_ready}")
    print(f"p25_v2_k22_automorphism_quotient_falsifier_rows={int(falsifier.row_ok)}/1")
    return 0 if falsifier.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
