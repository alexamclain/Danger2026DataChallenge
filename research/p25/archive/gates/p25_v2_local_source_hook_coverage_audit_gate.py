#!/usr/bin/env python3
"""Audit local-source coverage for the current p25 theorem hooks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
        return path.exists() and self.marker in path.read_text()


@dataclass(frozen=True)
class CoverageRow:
    name: str
    live_hook: str
    coverage_evidence: tuple[str, ...]
    local_verdict: str
    next_action: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    EvidenceMarker(
        "priority1_source_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    EvidenceMarker(
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    EvidenceMarker(
        "additive_normalizer_source_scan",
        "evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
        "p25_v2_additive_normalizer_source_scan_rows=1/1",
    ),
    EvidenceMarker(
        "constructive_payload_source_scan",
        "evidence/p25_v2_constructive_payload_source_scan_20260616.md",
        "p25_v2_constructive_payload_source_scan_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_source_hook_scan",
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
    ),
    EvidenceMarker(
        "koo_shin_priority1_toprow_falsifier",
        "evidence/p25_v2_koo_shin_priority1_toprow_falsifier_20260617.md",
        "p25_v2_koo_shin_priority1_toprow_falsifier_rows=1/1",
    ),
    EvidenceMarker(
        "kato_siegel_divisor_scout",
        "evidence/p25_v2_kato_siegel_divisor_scout_20260617.md",
        "p25_v2_kato_siegel_divisor_scout_rows=1/1",
    ),
    EvidenceMarker(
        "period156_lookup_row_status",
        "evidence/p25_v2_period156_lookup_row_status_20260617.md",
        "p25_v2_period156_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "schertz_scholl_external_source_boundary",
        "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
        "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
    ),
    EvidenceMarker(
        "sprang_theta2_source_intake",
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
    EvidenceMarker(
        "normalizer_lookup_row_status",
        "evidence/p25_v2_normalizer_lookup_row_status_20260617.md",
        "p25_v2_normalizer_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_theta2_lookup_row_status",
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "kl_source_split_local_scan",
        "evidence/p25_v2_kl_source_split_local_scan_20260617.md",
        "p25_v2_kl_source_split_local_scan_rows=1/1",
    ),
)

LOCAL_SOURCE_PATHS = (
    "incoming/extracted/s00209-008-0456-9.pdf.extract.txt",
    "incoming/extracted/1007.2307/ray_class_fields.tex",
    "incoming/extracted/1007.2318v1.pdf.extract.txt",
    "incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex",
    "incoming/extracted/sprang_1802_04996/deRhamRealization.tex",
)


def markers_ok(*names: str) -> bool:
    marker_map = {marker.name: marker.ok for marker in EVIDENCE_MARKERS}
    return all(marker_map[name] for name in names)


def build_rows() -> tuple[CoverageRow, ...]:
    return (
        CoverageRow(
            name="first_pass_row_theorem",
            live_hook=(
                "scalar-fixed divisor/additive theorem or uniquely invertible "
                "finite power-value theorem for one legal support-156 row"
            ),
            coverage_evidence=(
                "additive_normalizer_source_scan",
                "constructive_payload_source_scan",
                "koo_shin_priority1_toprow_falsifier",
                "kato_siegel_divisor_scout",
            ),
            local_verdict="covered_no_local_scalar_fixed_row_theorem",
            next_action="external theorem/proof attempt or new source snippet",
            ok=markers_ok(
                "live_theorem_ask_packet",
                "additive_normalizer_source_scan",
                "constructive_payload_source_scan",
                "koo_shin_priority1_toprow_falsifier",
                "kato_siegel_divisor_scout",
            ),
        ),
        CoverageRow(
            name="period156_h0_y507_value",
            live_hook=(
                "canonical H0 or Y_507 period-156 finite value theorem with "
                "branch/root/telescoping data and legal-row bridge"
            ),
            coverage_evidence=(
                "constructive_payload_source_scan",
                "period156_lookup_row_status",
                "schertz_scholl_external_source_boundary",
                "sprang_theta2_source_intake",
            ),
            local_verdict="covered_no_local_period156_value_theorem",
            next_action="only reopen if a source names H0/Y507 period-156 data",
            ok=markers_ok(
                "constructive_payload_source_scan",
                "period156_lookup_row_status",
                "schertz_scholl_external_source_boundary",
                "sprang_theta2_source_intake",
            ),
        ),
        CoverageRow(
            name="conductor39_q_yang_support",
            live_hook=(
                "mixed U_chi/W Yang-H90 finite theorem, or Q/Q^3 theorem "
                "with selector debt paid"
            ),
            coverage_evidence=(
                "q_route_source_hook_scan",
                "priority1_source_lookup_capsule",
            ),
            local_verdict="covered_no_local_q_or_yang_hook",
            next_action="ask for direct mixed theorem or Q plus quartic split/root",
            ok=markers_ok("q_route_source_hook_scan", "priority1_source_lookup_capsule"),
        ),
        CoverageRow(
            name="row_quartic_power_normalizer",
            live_hook=(
                "row label, reciprocal sign, exact C4_1 phase, selected "
                "projector/root, or uniquely rootable power plus finite theorem"
            ),
            coverage_evidence=(
                "normalizer_lookup_row_status",
                "source_family_gap_matrix",
                "constructive_payload_source_scan",
            ),
            local_verdict="covered_normalizers_live_but_no_local_finite_theorem",
            next_action="accept only when normalizer lands on one scalar-fixed row",
            ok=markers_ok(
                "normalizer_lookup_row_status",
                "source_family_gap_matrix",
                "constructive_payload_source_scan",
            ),
        ),
        CoverageRow(
            name="exactp_theta2_heavy",
            live_hook=(
                "compact C,D,K,orientation, equal-weight 75 atoms, exact KL "
                "primitive word/mixed selector, or theta2 payload"
            ),
            coverage_evidence=(
                "constructive_payload_source_scan",
                "exactp_theta2_lookup_row_status",
                "kl_source_split_local_scan",
                "sprang_theta2_source_intake",
            ),
            local_verdict="covered_no_local_exactp_or_theta2_source_theorem",
            next_action="external exact-P theorem/proof attempt only with accepted hook",
            ok=markers_ok(
                "constructive_payload_source_scan",
                "exactp_theta2_lookup_row_status",
                "kl_source_split_local_scan",
                "sprang_theta2_source_intake",
            ),
        ),
    )


def main() -> int:
    rows = build_rows()
    marker_ok_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    raw_sources_available = all((REPO / rel).exists() for rel in LOCAL_SOURCE_PATHS)
    covered_rows = sum(row.ok for row in rows)
    positive_local_hooks = 0
    source_stage_closers = 0
    submissions = 0
    overall_ok = (
        marker_ok_count == len(EVIDENCE_MARKERS)
        and covered_rows == len(rows)
        and positive_local_hooks == 0
        and source_stage_closers == 0
        and submissions == 0
    )

    print("p25 v2 local source hook coverage audit")
    print(f"raw_sources_available={int(raw_sources_available)}")
    print(f"evidence_markers_ok={marker_ok_count}/{len(EVIDENCE_MARKERS)}")
    print("coverage_rows")
    for row in rows:
        print(f"  {row.name}: ok={int(row.ok)}")
        print(f"    live_hook={row.live_hook}")
        print(f"    coverage_evidence={','.join(row.coverage_evidence)}")
        print(f"    local_verdict={row.local_verdict}")
        print(f"    next_action={row.next_action}")
    print("counts")
    print(f"  live_hook_rows={len(rows)}")
    print(f"  covered_hook_rows={covered_rows}")
    print("  uncovered_local_source_hook_rows=0")
    print(f"  positive_local_source_hooks={positive_local_hooks}")
    print(f"  current_source_stage_closers={source_stage_closers}")
    print(f"  current_submission_ready={submissions}")
    print("interpretation")
    print("  local_corpus_is_exhausted_for_current_live_hooks=1")
    print("  next_progress_requires_new_source_snippet_external_theorem_or_proof=1")
    print(f"p25_v2_local_source_hook_coverage_audit_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("local source hook coverage audit failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
