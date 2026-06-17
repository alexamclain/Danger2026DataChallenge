#!/usr/bin/env python3
"""Validate the quotient-C4 source graph normal form for p25.

The self-contained theorem statement gives the exact finite products.  This
gate gives the matching source-side graph: the four legal rows are exactly the
edges of a K_{2,2} graph from odd quotient-C4 cosets to even quotient-C4 cosets.
This is a routing artifact for source theorems, not the missing theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_v2_quotient_h90_idempotent_mechanism_gate import build_profile as build_h90_profile
from p25_v2_rectangle_diagonal_aggregate_gate import build_profile as build_diagonal_profile
from p25_v2_row_quotient_invariant_bridge_gate import build_bridge
from p25_v2_unified_group_ring_payload_gate import build_payload


COSETS = {
    0: "H=(1,3,9)",
    1: "2H=(2,5,6)",
    2: "4H=(4,10,12)",
    3: "7H=(7,8,11)",
}
ODD_VERTICES = (1, 3)
EVEN_VERTICES = (0, 2)
EDGE_ROWS = {
    1: (3, 2),
    2: (3, 0),
    4: (1, 0),
    8: (1, 2),
}
OPPOSITE_EDGE_PAIRS = ((1, 4), (2, 8))
ADJACENT_EDGE_PAIRS = ((1, 2), (1, 8), (2, 4), (4, 8))


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceGraphEdge:
    multiplier: int
    odd_vertex: int
    even_vertex: int
    odd_label: str
    even_label: str
    payload_sha256: str
    support_ok: bool
    boundary_w_ok: bool
    row_ok: bool


@dataclass(frozen=True)
class GraphRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    accepted_if_theorem_present: bool
    ok: bool


@dataclass(frozen=True)
class SourceGraphNormalForm:
    evidence_markers: tuple[EvidenceMarker, ...]
    edges: tuple[SourceGraphEdge, ...]
    routes: tuple[GraphRoute, ...]
    odd_vertices: tuple[int, ...]
    even_vertices: tuple[int, ...]
    edge_graph_is_k22: bool
    opposite_edge_pairs: tuple[tuple[int, int], ...]
    adjacent_edge_pairs: tuple[tuple[int, int], ...]
    diagonal_aggregates_ok: int
    quotient_bridges_ok: int
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
            "self_contained_theorem_statement",
            "research/p25/evidence/p25_v2_self_contained_theorem_statement_20260616.md",
            "p25_v2_self_contained_theorem_statement_rows=1/1",
        ),
        marker(
            "quotient_h90_idempotent_mechanism",
            "research/p25/evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "mixed_signed_column_fingerprint",
            "research/p25/evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
            "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
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
    )


def graph_routes() -> tuple[GraphRoute, ...]:
    return (
        GraphRoute(
            name="one_oriented_k22_edge",
            decision="source_stage_candidate_if_theorem_present",
            first_missing_or_falsifier="finite divisor/additive or period-156 value theorem",
            accepted_if_theorem_present=True,
            ok=True,
        ),
        GraphRoute(
            name="opposite_edge_diagonal_aggregate",
            decision="repair_boundary_2w",
            first_missing_or_falsifier="selector or factorization down to one W-boundary edge",
            accepted_if_theorem_present=False,
            ok=True,
        ),
        GraphRoute(
            name="edge_quotient_only",
            decision="repair_boundary_zero_relation",
            first_missing_or_falsifier="one-edge value/divisor theorem",
            accepted_if_theorem_present=False,
            ok=True,
        ),
        GraphRoute(
            name="aggregate_plus_quotient",
            decision="repair_row_square_halving_missing",
            first_missing_or_falsifier="oriented root or direct one-edge theorem",
            accepted_if_theorem_present=False,
            ok=True,
        ),
        GraphRoute(
            name="vertex_projection_or_one_coset",
            decision="reject_mixed_fingerprint_lost",
            first_missing_or_falsifier="full signed-column edge preserving both axes",
            accepted_if_theorem_present=False,
            ok=True,
        ),
    )


def build_normal_form() -> SourceGraphNormalForm:
    markers = evidence_markers()
    payload = build_payload()
    h90 = build_h90_profile()
    diagonal = build_diagonal_profile()
    quotient_bridge = build_bridge()
    payload_rows = {row.multiplier: row for row in payload.legal_product_rows}
    h90_rows = {row.multiplier: row for row in h90.legal_rows}

    edges: list[SourceGraphEdge] = []
    for multiplier, (odd_vertex, even_vertex) in EDGE_ROWS.items():
        payload_row = payload_rows[multiplier]
        h90_row = h90_rows[multiplier]
        support_ok = (
            len(payload_row.positive_mod39) == 6
            and len(payload_row.negative_mod39) == 6
            and len(payload_row.lifted_positive_entries) == 78
            and len(payload_row.lifted_negative_entries) == 78
        )
        boundary_ok = (
            h90_row.odd_plus_coset == odd_vertex
            and h90_row.even_minus_coset == even_vertex
            and h90_row.boundary_equals_w
        )
        edges.append(
            SourceGraphEdge(
                multiplier=multiplier,
                odd_vertex=odd_vertex,
                even_vertex=even_vertex,
                odd_label=COSETS[odd_vertex],
                even_label=COSETS[even_vertex],
                payload_sha256=payload_row.payload_sha256,
                support_ok=support_ok,
                boundary_w_ok=boundary_ok,
                row_ok=support_ok and boundary_ok and payload_row.row_ok and h90_row.row_ok,
            )
        )

    vertex_degrees = {vertex: 0 for vertex in ODD_VERTICES + EVEN_VERTICES}
    for edge in edges:
        vertex_degrees[edge.odd_vertex] += 1
        vertex_degrees[edge.even_vertex] += 1
    edge_graph_is_k22 = (
        {edge.multiplier for edge in edges} == set(EDGE_ROWS)
        and {(edge.odd_vertex, edge.even_vertex) for edge in edges}
        == {(odd, even) for odd in ODD_VERTICES for even in EVEN_VERTICES}
        and all(vertex_degrees[vertex] == 2 for vertex in vertex_degrees)
    )
    routes = graph_routes()
    source_candidates = sum(route.accepted_if_theorem_present for route in routes)
    repair_or_reject = sum(not route.accepted_if_theorem_present for route in routes)
    diagonal_ok = int(
        diagonal.row_ok
        and diagonal.diagonals_equal
        and diagonal.diagonal_m1_m4.boundary_scale_w == 2
        and diagonal.diagonal_m2_m8.boundary_scale_w == 2
    )
    quotient_ok = int(
        quotient_bridge.row_ok
        and quotient_bridge.boundary_zero_quotients == 6
        and quotient_bridge.row_square_bridges == 4
    )
    current_source_theorems = 0
    submission_ready_rows = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and payload.row_ok
        and h90.row_ok
        and all(edge.row_ok for edge in edges)
        and len(edges) == 4
        and edge_graph_is_k22
        and OPPOSITE_EDGE_PAIRS == ((1, 4), (2, 8))
        and ADJACENT_EDGE_PAIRS == ((1, 2), (1, 8), (2, 4), (4, 8))
        and diagonal_ok == 1
        and quotient_ok == 1
        and len(routes) == 5
        and source_candidates == 1
        and repair_or_reject == 4
        and current_source_theorems == 0
        and submission_ready_rows == 0
        and all(route.ok for route in routes)
    )
    return SourceGraphNormalForm(
        evidence_markers=markers,
        edges=tuple(edges),
        routes=routes,
        odd_vertices=ODD_VERTICES,
        even_vertices=EVEN_VERTICES,
        edge_graph_is_k22=edge_graph_is_k22,
        opposite_edge_pairs=OPPOSITE_EDGE_PAIRS,
        adjacent_edge_pairs=ADJACENT_EDGE_PAIRS,
        diagonal_aggregates_ok=diagonal_ok,
        quotient_bridges_ok=quotient_ok,
        source_candidate_routes=source_candidates,
        repair_or_reject_routes=repair_or_reject,
        current_source_theorems=current_source_theorems,
        submission_ready_rows=submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    normal = build_normal_form()
    print("p25 v2 source graph normal form")
    for marker_row in normal.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"odd_vertices={normal.odd_vertices}")
    print(f"even_vertices={normal.even_vertices}")
    print("edges")
    for edge in normal.edges:
        print(
            "  "
            f"m={edge.multiplier} odd={edge.odd_vertex}:{edge.odd_label} "
            f"even={edge.even_vertex}:{edge.even_label} "
            f"support_ok={int(edge.support_ok)} boundary_w_ok={int(edge.boundary_w_ok)} "
            f"sha256={edge.payload_sha256} ok={int(edge.row_ok)}"
        )
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in normal.evidence_markers)}/{len(normal.evidence_markers)}")
    print(f"  legal_edges_ok={sum(edge.row_ok for edge in normal.edges)}/{len(normal.edges)}")
    print(f"  edge_graph_is_k22={int(normal.edge_graph_is_k22)}")
    print(f"  opposite_edge_pairs={normal.opposite_edge_pairs}")
    print(f"  adjacent_edge_pairs={normal.adjacent_edge_pairs}")
    print(f"  diagonal_aggregates_ok={normal.diagonal_aggregates_ok}/1")
    print(f"  quotient_bridges_ok={normal.quotient_bridges_ok}/1")
    print(f"  source_candidate_routes={normal.source_candidate_routes}")
    print(f"  repair_or_reject_routes={normal.repair_or_reject_routes}")
    print(f"  current_source_theorems={normal.current_source_theorems}")
    print(f"  submission_ready_rows={normal.submission_ready_rows}")
    print(f"p25_v2_source_graph_normal_form_rows={int(normal.row_ok)}/1")
    return 0 if normal.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
