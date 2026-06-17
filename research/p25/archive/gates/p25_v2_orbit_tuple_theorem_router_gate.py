#!/usr/bin/env python3
"""Route row-labeled orbit theorems versus symmetric orbit aggregates.

The first-pass H0/conductor-39 target needs one oriented quotient-C4 edge.
A source theorem may naturally state a result for the whole four-row doubling
orbit.  This gate records the distinction that matters: a row-labeled tuple of
four scalar-fixed edge identities contains one-edge theorems and can be
promoted; an unordered or symmetric orbit aggregate does not select an edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROWS = (
    (
        1,
        "7H -> 4H",
        "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e",
    ),
    (
        2,
        "7H -> H",
        "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9",
    ),
    (
        4,
        "2H -> H",
        "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6",
    ),
    (
        8,
        "2H -> 4H",
        "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87",
    ),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RowPayload:
    multiplier: int
    edge: str
    sha256: str
    boundary: str
    row_ok: bool


@dataclass(frozen=True)
class Route:
    name: str
    provided_shape: str
    decision: str
    first_missing_or_next: str
    source_stage_candidate: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class OrbitTupleTheoremRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    row_payloads: tuple[RowPayload, ...]
    routes: tuple[Route, ...]
    evidence_markers_ok: int
    row_payloads_ok: int
    accepted_routes: int
    repair_rows: int
    reject_rows: int
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
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
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
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "current_source_stage_closers = 0",
        ),
    )


def row_payloads() -> tuple[RowPayload, ...]:
    seen_hashes: set[str] = set()
    payloads: list[RowPayload] = []
    for multiplier, edge, digest in ROWS:
        row_ok = (
            multiplier in {1, 2, 4, 8}
            and "->" in edge
            and len(digest) == 64
            and digest not in seen_hashes
        )
        seen_hashes.add(digest)
        payloads.append(
            RowPayload(
                multiplier=multiplier,
                edge=edge,
                sha256=digest,
                boundary="Norm_156(Y_507)",
                row_ok=row_ok,
            )
        )
    return tuple(payloads)


def routes() -> tuple[Route, ...]:
    return (
        Route(
            name="single_labeled_edge_divisor_additive",
            provided_shape="scalar-fixed divisor/additive identity for one row m with hash or edge label",
            decision="source_stage_candidate_if_arithmetic_source_theorem",
            first_missing_or_next="DANGER3 framing and extraction after the theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="row_labeled_four_edge_divisor_additive_tuple",
            provided_shape="four scalar-fixed divisor/additive identities labeled by m in {1,2,4,8}",
            decision="choose_any_labeled_row_then_route_to_extraction_contract",
            first_missing_or_next="DANGER3 framing and extraction after the theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="row_labeled_four_edge_period156_value_tuple",
            provided_shape="four period-156 values labeled by row, each with branch/root/telescoping context",
            decision="choose_any_labeled_row_then_route_to_extraction_contract",
            first_missing_or_next="DANGER3 framing and extraction after the theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="parametric_doubling_orbit_theorem",
            provided_shape="uniform theorem for m in the four legal doubling-orbit representatives",
            decision="normalize_m_then_apply_positive_clause_matcher",
            first_missing_or_next="one normalized row plus scalar-fixed finite identity",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="unordered_four_values_no_row_labels",
            provided_shape="four values or identities with no map to m, edge labels, row hashes, or cosets",
            decision="repair_row_labeling_missing",
            first_missing_or_next="assignment to one exact oriented edge R_m",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="symmetric_all_four_product_or_norm",
            provided_shape="product, norm, trace, or symmetric aggregate over all four rows",
            decision="repair_oriented_edge_selection_missing",
            first_missing_or_next="selected fourth root/scalar data or direct row-labeled theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="diagonal_or_pair_tuple_only",
            provided_shape="two-edge pair, diagonal pair, or complement pair data",
            decision="repair_square_root_or_pair_selector_missing",
            first_missing_or_next="oriented square root or direct one-edge theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="row_quotient_or_boundary_zero_tuple",
            provided_shape="quotients between row labels or boundary-zero orbit relations",
            decision="repair_one_edge_value_missing",
            first_missing_or_next="finite value/divisor theorem for one W-boundary edge",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="orbit_source_legality_only",
            provided_shape="orbit-level source certificate, distribution relation, or class-field generation",
            decision="repair_finite_theorem_missing",
            first_missing_or_next="scalar-fixed finite value/divisor theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="orbit_values_up_to_scalar",
            provided_shape="row-labeled orbit values only up to unspecified F_p^* constants",
            decision="repair_scalar_normalization_missing",
            first_missing_or_next="finite additive/value/basepoint/branch/telescoping normalization",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="outside_doubling_orbit_tuple",
            provided_shape="tuple labeled by units outside the legal doubling orbit",
            decision="reject_not_current_legal_four_row_target",
            first_missing_or_next="one of the four normalized rows or a newly justified target",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_router() -> OrbitTupleTheoremRouter:
    markers = evidence_markers()
    payloads = row_payloads()
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    payload_ok = sum(row.row_ok and row.boundary == "Norm_156(Y_507)" for row in payloads)
    accepted = sum(row.source_stage_candidate for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(payloads) == 4
        and payload_ok == 4
        and {row.multiplier for row in payloads} == {1, 2, 4, 8}
        and len({row.sha256 for row in payloads}) == 4
        and accepted == 4
        and repairs == 6
        and rejects == 1
        and current_source_theorems == 0
        and current_submission_ready == 0
        and all(row.ok for row in route_rows)
    )
    return OrbitTupleTheoremRouter(
        evidence_markers=markers,
        row_payloads=payloads,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        row_payloads_ok=payload_ok,
        accepted_routes=accepted,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    print("p25 v2 orbit tuple theorem router")
    print("evidence")
    for row in router.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} marker={row.marker}")
    print("rows")
    for row in router.row_payloads:
        print(
            f"  m={row.multiplier}: edge={row.edge} "
            f"boundary={row.boundary} sha256={row.sha256} ok={int(row.row_ok)}"
        )
    print("routes")
    for row in router.routes:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source_stage={int(row.source_stage_candidate)} "
            f"repair={int(row.repair)} reject={int(row.reject)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={router.evidence_markers_ok}/{len(router.evidence_markers)}")
    print(f"  row_payloads_ok={router.row_payloads_ok}/{len(router.row_payloads)}")
    print(f"  accepted_routes={router.accepted_routes}")
    print(f"  repair_rows={router.repair_rows}")
    print(f"  reject_rows={router.reject_rows}")
    print(f"  current_source_theorems={router.current_source_theorems}")
    print(f"  current_submission_ready={router.current_submission_ready}")
    print(f"p25_v2_orbit_tuple_theorem_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
