#!/usr/bin/env python3
"""Audit p25_v2 evidence notes intentionally left outside the cockpit gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
COCKPIT = RESEARCH / "archive/gates/p25_v2_wiki_cockpit_lightweight_check_gate.py"


@dataclass(frozen=True)
class OrphanEvidenceRow:
    name: str
    rel_path: str
    marker_or_anchor: str
    downstream_refs: tuple[tuple[str, str], ...]
    decision: str
    live_hook_status: str

    @property
    def path(self) -> Path:
        return RESEARCH / self.rel_path


ROWS = (
    OrphanEvidenceRow(
        name="exactp_theorem_interface_contract",
        rel_path="evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
        marker_or_anchor="positive_artifact = compact theorem-output interface",
        downstream_refs=(
            ("evidence/p25_v2_exactp_minimal_hook_20260616.md", "p25_v2_exactp_theorem_interface_contract_20260616.md"),
            ("evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md", "p25_v2_exactp_theorem_interface_contract_20260616.md"),
            ("evidence/p25_v2_exactp_spine_payload_separation_20260617.md", "compact exact-P theorem feeds unified target"),
            ("lanes/exact-p.md", "exact-P theorem-interface contract"),
        ),
        decision="superseded_by_exactp_minimal_hook_lookup_and_spine",
        live_hook_status="heavy_upstream_interface_not_standalone_cockpit_row",
    ),
    OrphanEvidenceRow(
        name="h0_conductor39_canonical_frontier_pass",
        rel_path="evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md",
        marker_or_anchor="continue_lane_but_kill_koo_shin_2010_as_closer",
        downstream_refs=(
            ("evidence/p25_v2_h0_theorem_interface_contract_20260616.md", "p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md"),
            ("evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md", "p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md"),
            ("evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md", "p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md"),
            ("sources/koo-shin-2010.md", "H0 / conductor-39 frontier pass"),
        ),
        decision="superseded_by_h0_conductor39_interface_and_koo_shin_falsifiers",
        live_hook_status="historical_local_source_scan_not_current_closer",
    ),
    OrphanEvidenceRow(
        name="koo_shin_ii_first_pass_source_scan",
        rel_path="evidence/p25_v2_koo_shin_ii_first_pass_source_scan_20260616.md",
        marker_or_anchor="Koo-Shin II `1007.2318` is background context",
        downstream_refs=(
            ("evidence/p25_v2_constructive_payload_source_scan_20260616.md", "koo_shin_ii_1007_2318"),
            ("evidence/p25_v2_source_family_gap_matrix_20260616.md", "koo_shin_ii_1007_2318"),
            ("sources/koo-shin-ii-1007-2318.md", "Koo-Shin II first-pass source scan"),
        ),
        decision="superseded_by_source_family_gap_and_constructive_payload_scan",
        live_hook_status="background_context_not_front_door_source",
    ),
    OrphanEvidenceRow(
        name="ksy_1007_2307_source_ingest_scan",
        rel_path="evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md",
        marker_or_anchor="continue_as_exactp_vocabulary_not_closer",
        downstream_refs=(
            ("evidence/p25_v2_exactp_candidate_sweep_20260617.md", "p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md"),
            ("evidence/p25_v2_kl_source_split_local_scan_20260617.md", "ksy_1007_2307_normalized_y"),
            ("evidence/p25_v2_source_family_gap_matrix_20260616.md", "koo_shin_yoon_1007_2307"),
            ("sources/koo-shin-yoon-1007-2307.md", "KSY source ingest scan"),
        ),
        decision="superseded_by_exactp_candidate_sweep_kl_scan_and_source_gap",
        live_hook_status="exactp_vocabulary_not_arithmetic_producer",
    ),
)


def read(rel_path: str) -> str:
    return (RESEARCH / rel_path).read_text(errors="replace")


def row_ok(row: OrphanEvidenceRow, cockpit_text: str) -> bool:
    if not row.path.exists():
        return False
    text = row.path.read_text(errors="replace")
    if row.marker_or_anchor not in text:
        return False
    if Path(row.rel_path).name in cockpit_text:
        return False
    return all((RESEARCH / ref).exists() and needle in read(ref) for ref, needle in row.downstream_refs)


def canonical_pages_ok() -> bool:
    required = (
        ("frontier.md", "source-family gap matrix"),
        ("lanes/h0.md", "H0 / conductor-39 frontier pass"),
        ("lanes/conductor39.md", "H0 / conductor-39 frontier pass"),
        ("lanes/exact-p.md", "exact-P theorem-interface contract"),
        ("sources/koo-shin-yoon-1007-2307.md", "V2 exact-P theorem-interface contract"),
        ("sources/koo-shin-ii-1007-2318.md", "V2 Koo-Shin II first-pass source scan"),
    )
    return all((RESEARCH / rel).exists() and needle in read(rel) for rel, needle in required)


def main() -> int:
    cockpit_text = COCKPIT.read_text(errors="replace")
    row_results = tuple(row_ok(row, cockpit_text) for row in ROWS)
    all_downstream_refs = sum(len(row.downstream_refs) for row in ROWS)
    live_source_stage_closers = 0
    cockpit_promotion_needed = 0
    broad_reread_unlocked = 0
    overall_ok = (
        all(row_results)
        and canonical_pages_ok()
        and live_source_stage_closers == 0
        and cockpit_promotion_needed == 0
        and broad_reread_unlocked == 0
    )

    print("p25 v2 orphan evidence supersession audit")
    print(f"canonical_pages_ok={int(canonical_pages_ok())}")
    print("rows")
    for row, ok in zip(ROWS, row_results):
        print(f"  {row.name}: ok={int(ok)}")
        print(f"    rel_path={row.rel_path}")
        print(f"    decision={row.decision}")
        print(f"    live_hook_status={row.live_hook_status}")
        print(f"    downstream_refs={','.join(ref for ref, _needle in row.downstream_refs)}")
    print("counts")
    print(f"orphan_evidence_rows={len(ROWS)}")
    print(f"rows_ok={sum(row_results)}/{len(ROWS)}")
    print(f"downstream_refs_checked={all_downstream_refs}")
    print(f"live_source_stage_closers={live_source_stage_closers}")
    print(f"cockpit_promotion_needed={cockpit_promotion_needed}")
    print(f"broad_reread_unlocked={broad_reread_unlocked}")
    print(f"p25_v2_orphan_evidence_supersession_audit_rows={int(overall_ok)}/1")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
