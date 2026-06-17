#!/usr/bin/env python3
"""Extraction boundary for exact Q-square value data.

The Q-square payload router records that an exact scalar-fixed value for
2*edge has only two square roots in F_p.  This gate checks the downstream
boundary: those are two modular-unit row-value roots, not automatically two
DANGER3 candidates.  vpp.py verifies (p,A,x0), so a row-value root still needs
the DANGER3 framing / same-j / X_1(16) / halving extraction map.
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
class BoundaryRow:
    name: str
    shape: str
    decision: str
    row_value_payload: bool
    extraction_ready: bool
    submission_ready: bool
    repair: bool
    reject: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class QSquareExtractionBoundary:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[BoundaryRow, ...]
    evidence_markers_ok: int
    row_value_payload_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    repair_rows: int
    reject_rows: int
    current_extraction_ready_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
        marker(
            "extraction_minimal_hook",
            "research/p25/evidence/p25_v2_extraction_minimal_hook_20260616.md",
            "p25_v2_extraction_minimal_hook_rows=1/1",
        ),
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "danger3_framing_contract",
            "research/p25/evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
            "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
        ),
    )


def rows() -> tuple[BoundaryRow, ...]:
    return (
        BoundaryRow(
            name="q_square_exact_fp_value_only",
            shape="exact scalar-fixed F_p value for the Q square, hence two row-value roots",
            decision="repair_extraction_map_missing_after_two_root_row_payload",
            row_value_payload=True,
            extraction_ready=False,
            submission_ready=False,
            repair=True,
            reject=False,
            first_missing_or_falsifier="DANGER3 framing plus same-j/X_1(16)/halving or direct A,x0 extraction map",
            ok=True,
        ),
        BoundaryRow(
            name="q_square_roots_plus_same_j_x16_map",
            shape="two row-value roots plus a same-j bridge and practical X_1(16) payload",
            decision="route_mapped_roots_through_extraction_payload_contract",
            row_value_payload=True,
            extraction_ready=False,
            submission_ready=False,
            repair=False,
            reject=False,
            first_missing_or_falsifier="halving chain, direct x0, or vpp.py depending on supplied map",
            ok=True,
        ),
        BoundaryRow(
            name="q_square_roots_plus_direct_A_x0",
            shape="two row-value roots plus an explicit map to concrete A,x0 candidates",
            decision="extraction_ready_vpp_missing",
            row_value_payload=True,
            extraction_ready=True,
            submission_ready=False,
            repair=False,
            reject=False,
            first_missing_or_falsifier="official src/vpp.py verification for each concrete candidate",
            ok=True,
        ),
        BoundaryRow(
            name="q_square_value_up_to_scalar",
            shape="Q-square value known only up to an unspecified F_p^* scalar",
            decision="repair_scalar_and_root_orientation_missing",
            row_value_payload=False,
            extraction_ready=False,
            submission_ready=False,
            repair=True,
            reject=False,
            first_missing_or_falsifier="specified scalar before even the two row roots are concrete",
            ok=True,
        ),
        BoundaryRow(
            name="direct_vpp_on_row_value",
            shape="attempt to feed a modular-unit row-value root directly to vpp.py",
            decision="reject_vpp_requires_A_x0_not_row_value",
            row_value_payload=False,
            extraction_ready=False,
            submission_ready=False,
            repair=False,
            reject=True,
            first_missing_or_falsifier="vpp.py verifies (p,A,x0), not a modular-unit row value",
            ok=True,
        ),
    )


def build_boundary() -> QSquareExtractionBoundary:
    markers = evidence_markers()
    boundary_rows = rows()
    markers_ok = sum(row.ok for row in markers)
    row_value_payloads = sum(row.row_value_payload for row in boundary_rows)
    extraction_ready = sum(row.extraction_ready for row in boundary_rows)
    submission_ready = sum(row.submission_ready for row in boundary_rows)
    repairs = sum(row.repair for row in boundary_rows)
    rejects = sum(row.reject for row in boundary_rows)
    current_extraction_ready = 0
    current_submission_ready = 0
    expected = (
        "repair_extraction_map_missing_after_two_root_row_payload",
        "route_mapped_roots_through_extraction_payload_contract",
        "extraction_ready_vpp_missing",
        "repair_scalar_and_root_orientation_missing",
        "reject_vpp_requires_A_x0_not_row_value",
    )
    row_ok = (
        markers_ok == len(markers)
        and len(boundary_rows) == 5
        and tuple(row.decision for row in boundary_rows) == expected
        and row_value_payloads == 3
        and extraction_ready == 1
        and submission_ready == 0
        and repairs == 2
        and rejects == 1
        and current_extraction_ready == 0
        and current_submission_ready == 0
        and all(row.ok for row in boundary_rows)
    )
    return QSquareExtractionBoundary(
        evidence_markers=markers,
        rows=boundary_rows,
        evidence_markers_ok=markers_ok,
        row_value_payload_rows=row_value_payloads,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        repair_rows=repairs,
        reject_rows=rejects,
        current_extraction_ready_rows=current_extraction_ready,
        current_submission_ready_rows=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    boundary = build_boundary()
    print("p25 v2 Q square extraction boundary")
    for marker_row in boundary.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("boundary_rows")
    for row in boundary.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    row_value_payload={int(row.row_value_payload)} extraction_ready={int(row.extraction_ready)}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={boundary.evidence_markers_ok}/{len(boundary.evidence_markers)}")
    print(f"  row_value_payload_rows={boundary.row_value_payload_rows}")
    print(f"  extraction_ready_rows={boundary.extraction_ready_rows}")
    print(f"  submission_ready_rows={boundary.submission_ready_rows}")
    print(f"  repair_rows={boundary.repair_rows}")
    print(f"  reject_rows={boundary.reject_rows}")
    print(f"  current_extraction_ready_rows={boundary.current_extraction_ready_rows}")
    print(f"  current_submission_ready_rows={boundary.current_submission_ready_rows}")
    print(f"p25_v2_q_square_extraction_boundary_rows={int(boundary.row_ok)}/1")
    return 0 if boundary.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
