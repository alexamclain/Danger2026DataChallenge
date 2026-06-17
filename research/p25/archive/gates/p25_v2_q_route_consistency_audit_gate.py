#!/usr/bin/env python3
"""Cross-check the p25 conductor-39 Q-route support boundary."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


def read(rel_path: str) -> str:
    return (RESEARCH / rel_path).read_text(errors="replace")


def load_gate(name: str) -> ModuleType:
    path = RESEARCH / "archive" / "gates" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "conductor39_norm_one_quotient_route",
        "evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
        "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_selector_debt",
        "evidence/p25_v2_q_route_selector_debt_20260616.md",
        "p25_v2_q_route_selector_debt_rows=1/1",
    ),
    EvidenceMarker(
        "q_diagonal_normalization",
        "evidence/p25_v2_q_diagonal_normalization_20260616.md",
        "p25_v2_q_diagonal_normalization_rows=1/1",
    ),
    EvidenceMarker(
        "q_split_quartic_selector",
        "evidence/p25_v2_q_split_quartic_selector_20260616.md",
        "p25_v2_q_split_quartic_selector_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_payload_router",
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_extraction_boundary",
        "evidence/p25_v2_q_square_extraction_boundary_20260616.md",
        "p25_v2_q_square_extraction_boundary_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_source_hook_scan",
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_candidate_sweep",
        "evidence/p25_v2_q_route_candidate_sweep_20260617.md",
        "p25_v2_q_route_candidate_sweep_rows=1/1",
    ),
    EvidenceMarker(
        "q_yang_lookup_row_status",
        "evidence/p25_v2_q_yang_lookup_row_status_20260617.md",
        "p25_v2_q_yang_lookup_row_status_rows=1/1",
    ),
)


def evidence_text_consistent() -> bool:
    norm = read("evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md")
    selector = read("evidence/p25_v2_q_route_selector_debt_20260616.md")
    sweep = read("evidence/p25_v2_q_route_candidate_sweep_20260617.md")
    lookup = read("evidence/p25_v2_q_yang_lookup_row_status_20260617.md")
    square = read("evidence/p25_v2_q_square_payload_router_20260616.md")
    extraction = read("evidence/p25_v2_q_square_extraction_boundary_20260616.md")
    source = read("evidence/p25_v2_q_route_source_hook_scan_20260616.md")
    return (
        "Q^6 = (1 - Frob_p)(Q^3)" in norm
        and "support_routes = 2" in norm
        and "current_source_theorems = 0" in norm
        and "q_value_period156_context_only" in selector
        and "q3_h90_preimage_finite_theorem_only" in selector
        and "source_candidate_routes = 1" in selector
        and "support_routes = 2" in selector
        and "q6_boundary_only" in sweep
        and "repair_additive_or_value_normalization_missing" in sweep
        and "q_square_exact_fp_value" in sweep
        and "bounded_two_root_payload_not_source_close" in sweep
        and "surviving_q_intake_families = 4" in sweep
        and "current_q_source_hooks = 0" in sweep
        and "current_source_stage_closers = 0" in sweep
        and "q_or_q3_finite_theorem" in lookup
        and "support_only_until_selector_paid" in lookup
        and "q_square_payload" in lookup
        and "payload_not_source_stage" in lookup
        and "bounded_payload_rows = 1" in square
        and "current_source_theorems = 0" in square
        and "current_extraction_ready_rows = 0" in extraction
        and "current_submission_ready_rows = 0" in extraction
        and "accepted_source_hook_rows = 0" in source
        and "source_stage_closers = 0" in source
    )


def canonical_pages_ok() -> bool:
    conductor = " ".join(read("lanes/conductor39.md").split())
    frontier = " ".join(read("frontier.md").split())
    return (
        "Q or Q^3 finite theorem data with selector debt paid" in frontier
        and "Q diagonal plus correct pure quartic split" in conductor
        and "exact scalar-fixed Q-square value plus extraction map" in conductor
    )


def main() -> int:
    sweep_gate = load_gate("p25_v2_q_route_candidate_sweep_gate")
    lookup_gate = load_gate("p25_v2_q_yang_lookup_row_status_gate")
    square_gate = load_gate("p25_v2_q_square_payload_router_gate")

    candidate = sweep_gate.build_sweep()
    lookup_markers, lookup_rows, lookup_ok = lookup_gate.build_check(RESEARCH)
    square = square_gate.build_router()

    marker_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    candidate_consistent = (
        candidate.row_ok
        and candidate.surviving_q_intake_families == 4
        and candidate.current_q_source_hooks == 0
        and candidate.current_source_stage_closers == 0
        and candidate.current_extraction_ready == 0
        and candidate.current_submission_ready == 0
        and any(row.name == "q3_h90_preimage_finite_theorem" and row.decision == "support_route_selector_debt_remains" for row in candidate.rows)
        and any(row.name == "q6_boundary_only" and row.decision == "repair_additive_or_value_normalization_missing" for row in candidate.rows)
        and any(row.name == "q_square_exact_fp_value" and row.decision == "bounded_two_root_payload_not_source_close" for row in candidate.rows)
    )
    lookup_consistent = (
        lookup_ok
        and len(lookup_rows) == 6
        and sum(row.current_status == "support_only_until_selector_paid" for row in lookup_rows) == 1
        and sum(row.current_status == "payload_not_source_stage" for row in lookup_rows) == 1
        and sum(marker.ok for marker in lookup_markers) == len(lookup_markers)
    )
    square_consistent = (
        square.row_ok
        and square.bounded_payload_rows == 1
        and square.current_source_theorems == 0
        and any(row.name == "q_square_exact_fp_value" and row.bounded_operational_payload for row in square.routes)
        and any(row.name == "q_direct_one_edge_theorem" and row.source_stage_candidate for row in square.routes)
    )
    overall_ok = (
        marker_count == len(EVIDENCE_MARKERS)
        and candidate_consistent
        and lookup_consistent
        and square_consistent
        and evidence_text_consistent()
        and canonical_pages_ok()
    )

    print("p25 v2 Q-route consistency audit")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print(f"candidate_consistent={int(candidate_consistent)}")
    print(f"lookup_consistent={int(lookup_consistent)}")
    print(f"square_consistent={int(square_consistent)}")
    print(f"evidence_text_consistent={int(evidence_text_consistent())}")
    print(f"canonical_pages_ok={int(canonical_pages_ok())}")
    print("q_or_q3_status=support_only_until_selector_paid")
    print("q6_boundary_status=repair_additive_or_value_normalization_missing")
    print("q_square_status=bounded_two_root_payload_not_source_close")
    print("surviving_q_intake_families=4")
    print("current_q_source_hooks=0")
    print("current_source_stage_closers=0")
    print("current_extraction_ready=0")
    print("current_submission_ready=0")
    print(f"p25_v2_q_route_consistency_audit_rows={int(overall_ok)}/1")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
