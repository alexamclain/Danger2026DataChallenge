#!/usr/bin/env python3
"""Validate the boundary-zero lattice transfer contract for p25."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


EDGE_ORDER = ("m1", "m2", "m4", "m8")
UNIT_EDGES = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)
ZERO_BASIS = (
    (-1, 1, 0, 0),  # m2 - m1
    (-1, 0, 1, 0),  # m4 - m1
    (-1, 0, 0, 1),  # m8 - m1
)
PAIR_QUOTIENTS = tuple(
    tuple(right - left for left, right in zip(UNIT_EDGES[i], UNIT_EDGES[j]))
    for i in range(len(UNIT_EDGES))
    for j in range(i + 1, len(UNIT_EDGES))
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class TransferRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    source_stage_candidate_if_data_present: bool
    ok: bool


@dataclass(frozen=True)
class ZeroLatticeTransferContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    routes: tuple[TransferRoute, ...]
    zero_lattice_rank: int
    pair_quotients: int
    pair_quotient_rank: int
    all_zero_basis_boundary_zero: bool
    all_pair_quotients_boundary_zero: bool
    unit_edges: int
    first_pass_normalization_routes: int
    support_only_routes: int
    repair_or_reject_routes: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "edge_lattice_global_minimality",
            "research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
            "p25_v2_edge_lattice_global_minimality_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def coeff_sum(vector: tuple[int, int, int, int]) -> int:
    return sum(vector)


def rank(vectors: tuple[tuple[int, int, int, int], ...]) -> int:
    matrix = [[Fraction(value) for value in row] for row in vectors]
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = None
        for row in range(pivot_row, rows):
            if matrix[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = matrix[row][col]
            if factor:
                matrix[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def transfer_routes() -> tuple[TransferRoute, ...]:
    return (
        TransferRoute(
            name="direct_one_edge_theorem",
            decision="source_stage_candidate_if_theorem_present",
            first_missing_or_falsifier="finite value/divisor theorem plus extraction",
            source_stage_candidate_if_data_present=True,
            ok=True,
        ),
        TransferRoute(
            name="w_boundary_nonedge_plus_exact_zero_lattice_value",
            decision="normalize_to_unit_edge_then_source_intake",
            first_missing_or_falsifier=(
                "exact scalar-fixed finite value for the boundary-zero part"
            ),
            source_stage_candidate_if_data_present=True,
            ok=True,
        ),
        TransferRoute(
            name="one_edge_theorem_plus_exact_row_quotient_value",
            decision="transfer_between_legal_edges_after_source_stage",
            first_missing_or_falsifier=(
                "not a first close; needs one absolute W-boundary edge theorem first"
            ),
            source_stage_candidate_if_data_present=False,
            ok=True,
        ),
        TransferRoute(
            name="zero_lattice_basis_values_only",
            decision="support_transfer_data_not_source_close",
            first_missing_or_falsifier="absolute W-boundary row value/divisor theorem",
            source_stage_candidate_if_data_present=False,
            ok=True,
        ),
        TransferRoute(
            name="zero_lattice_divisor_or_boundary_only",
            decision="repair_scalar_fixed_zero_lattice_value_missing",
            first_missing_or_falsifier=(
                "zero Hilbert-90 boundary does not fix a finite row quotient value"
            ),
            source_stage_candidate_if_data_present=False,
            ok=True,
        ),
        TransferRoute(
            name="w_boundary_nonedge_without_zero_lattice_value",
            decision="repair_boundary_zero_content_missing",
            first_missing_or_falsifier=(
                "nonunit W-boundary vector is edge plus boundary-zero lattice debt"
            ),
            source_stage_candidate_if_data_present=False,
            ok=True,
        ),
    )


def build_contract() -> ZeroLatticeTransferContract:
    markers = evidence_markers()
    routes = transfer_routes()
    zero_rank = rank(ZERO_BASIS)
    quotient_rank = rank(PAIR_QUOTIENTS)
    normalization_routes = sum(row.source_stage_candidate_if_data_present for row in routes)
    support_only_routes = sum("support" in row.decision or "transfer_between" in row.decision for row in routes)
    repair_or_reject_routes = len(routes) - normalization_routes - support_only_routes
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and zero_rank == 3
        and len(PAIR_QUOTIENTS) == 6
        and quotient_rank == 3
        and all(coeff_sum(row) == 0 for row in ZERO_BASIS)
        and all(coeff_sum(row) == 0 for row in PAIR_QUOTIENTS)
        and len(UNIT_EDGES) == 4
        and len(routes) == 6
        and normalization_routes == 2
        and support_only_routes == 2
        and repair_or_reject_routes == 2
        and current_source_stage_closers == 0
        and current_submission_ready == 0
        and all(row.ok for row in routes)
    )
    return ZeroLatticeTransferContract(
        evidence_markers=markers,
        routes=routes,
        zero_lattice_rank=zero_rank,
        pair_quotients=len(PAIR_QUOTIENTS),
        pair_quotient_rank=quotient_rank,
        all_zero_basis_boundary_zero=all(coeff_sum(row) == 0 for row in ZERO_BASIS),
        all_pair_quotients_boundary_zero=all(coeff_sum(row) == 0 for row in PAIR_QUOTIENTS),
        unit_edges=len(UNIT_EDGES),
        first_pass_normalization_routes=normalization_routes,
        support_only_routes=support_only_routes,
        repair_or_reject_routes=repair_or_reject_routes,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    print("p25 v2 zero-lattice transfer contract")
    for marker_row in contract.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("routes")
    for route in contract.routes:
        print(
            f"  {route.name}: decision={route.decision} "
            f"source_stage_if_data={int(route.source_stage_candidate_if_data_present)}"
        )
        print(f"    first_missing_or_falsifier={route.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in contract.evidence_markers)}/{len(contract.evidence_markers)}")
    print(f"  zero_lattice_rank={contract.zero_lattice_rank}")
    print(f"  pair_quotients={contract.pair_quotients}")
    print(f"  pair_quotient_rank={contract.pair_quotient_rank}")
    print(f"  all_zero_basis_boundary_zero={int(contract.all_zero_basis_boundary_zero)}")
    print(f"  all_pair_quotients_boundary_zero={int(contract.all_pair_quotients_boundary_zero)}")
    print(f"  unit_edges={contract.unit_edges}")
    print(f"  first_pass_normalization_routes={contract.first_pass_normalization_routes}")
    print(f"  support_only_routes={contract.support_only_routes}")
    print(f"  repair_or_reject_routes={contract.repair_or_reject_routes}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print(f"  current_submission_ready={contract.current_submission_ready}")
    print(f"p25_v2_zero_lattice_transfer_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
