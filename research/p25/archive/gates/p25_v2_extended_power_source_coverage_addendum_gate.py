#!/usr/bin/env python3
"""Guard the extended row-power intake against reopening broad source search."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
EXTENDED_EXACT_ROW_POWERS = (75, 169, 507)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


@dataclass(frozen=True)
class AddendumRow:
    name: str
    object_basis: str
    accepted_if: str
    local_coverage: str
    decision: str
    first_falsifier: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "extended_unique_power_intake",
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    EvidenceMarker(
        "local_source_hook_coverage_audit",
        "evidence/p25_v2_local_source_hook_coverage_audit_20260617.md",
        "p25_v2_local_source_hook_coverage_audit_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "drew_kernel_review_packet",
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_75_anchor_bridge_filter",
        "evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md",
        "p25_v2_exactp_75_anchor_bridge_filter_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_spine_payload_separation",
        "evidence/p25_v2_exactp_spine_payload_separation_20260617.md",
        "p25_v2_exactp_spine_payload_separation_rows=1/1",
    ),
    EvidenceMarker(
        "kl_source_split_local_scan",
        "evidence/p25_v2_kl_source_split_local_scan_20260617.md",
        "p25_v2_kl_source_split_local_scan_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_theta2_lookup_row_status",
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
)


def read(rel_path: str) -> str:
    return (RESEARCH / rel_path).read_text(errors="replace")


def source_text_consistent() -> bool:
    extended = read("evidence/p25_v2_extended_unique_power_intake_20260617.md")
    local = read("evidence/p25_v2_local_source_hook_coverage_audit_20260617.md")
    anchor = read("evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md")
    spine = read("evidence/p25_v2_exactp_spine_payload_separation_20260617.md")
    kl_scan = read("evidence/p25_v2_kl_source_split_local_scan_20260617.md")
    return (
        "R_m^75" in extended
        and "R_m^169" in extended
        and "R_m^507" in extended
        and "Do not open a broad search for arbitrary unique powers" in extended
        and "The local corpus is exhausted for the current live hooks" in local
        and "positive_local_source_hooks = 0" in local
        and "row_power_Rm75" in anchor
        and "exact-P 75 atoms" in anchor
        and "current_row_power_75_theorems = 0" in anchor
        and "exactp_75_not_row_power_75" in spine
        and "current_kl_source_theorems = 0" in kl_scan
    )


def build_rows() -> tuple[AddendumRow, ...]:
    return (
        AddendumRow(
            name="extended_row_power_intake",
            object_basis="one labeled legal row R_m with e in {75,169,507}",
            accepted_if=(
                "an arithmetic source theorem gives an exact finite F_p value "
                "for R_m^e plus the boundary or accepted period bridge"
            ),
            local_coverage="covered by local source-hook audit and extended intake",
            decision="intake_only_if_exact_row_labeled_theorem_arrives",
            first_falsifier="rowless power value, boundary-only powered divisor, or value up to scalar",
            ok=all(gcd(exponent, P25 - 1) == 1 for exponent in EXTENDED_EXACT_ROW_POWERS),
        ),
        AddendumRow(
            name="exactp_75_atom_not_row_power",
            object_basis="exact-P normalized-y/theta2 atoms",
            accepted_if=(
                "a challenge-legal exact-P theorem emits the compact packet, "
                "orientation, and 75->300->12->312->156 bridge"
            ),
            local_coverage="covered by exact-P spine separation and local KL scan",
            decision="heavy_upstream_not_first_pass_row_power_shortcut",
            first_falsifier="75 vocabulary, atom count, or finite fixture without arithmetic source theorem",
            ok=True,
        ),
        AddendumRow(
            name="c169_507_context_not_power_hook",
            object_basis="KL/Sprang/Koo-Shin source vocabulary mentioning 169 or 507",
            accepted_if=(
                "the source supplies either a row-labeled R_m^169/R_m^507 theorem "
                "or the accepted exact-P/KL/theta2 payload"
            ),
            local_coverage="covered by KL source-split local scan and exact-P/theta2 lookup",
            decision="support_or_repair_until_exact_hook",
            first_falsifier="C_169, level-507, Y_507, or primitive-word vocabulary without exact payload",
            ok=True,
        ),
        AddendumRow(
            name="no_local_reread_unlocked",
            object_basis="local Koo-Shin/KSY/Koo-Shin II/Sprang extracts",
            accepted_if="a new snippet names one of the exact accepted hooks",
            local_coverage="local corpus already exhausted for current live hooks",
            decision="external_theorem_new_snippet_or_proof_attempt_only",
            first_falsifier="broad reread request driven only by expanded unique-power list",
            ok=True,
        ),
    )


def canonical_pages_ok() -> bool:
    required = (
        ("frontier.md", "extended power-source coverage addendum"),
        ("lanes/h0.md", "extended power-source coverage addendum"),
        ("lanes/conductor39.md", "extended power-source coverage addendum"),
        ("lanes/exact-p.md", "extended power-source coverage addendum"),
    )
    return all((RESEARCH / rel).exists() and needle in read(rel) for rel, needle in required)


def main() -> int:
    rows = build_rows()
    marker_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    source_text_ok = source_text_consistent()
    canonical_ok = canonical_pages_ok()
    current_extended_power_source_theorems = 0
    current_exactp_source_theorems = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    broad_reread_unlocked = 0
    overall_ok = (
        marker_count == len(EVIDENCE_MARKERS)
        and source_text_ok
        and canonical_ok
        and all(row.ok for row in rows)
        and current_extended_power_source_theorems == 0
        and current_exactp_source_theorems == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
        and broad_reread_unlocked == 0
    )

    print("p25 v2 extended power source coverage addendum")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print(f"source_text_consistent={int(source_text_ok)}")
    print(f"canonical_pages_ok={int(canonical_ok)}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: ok={int(row.ok)}")
        print(f"    object_basis={row.object_basis}")
        print(f"    accepted_if={row.accepted_if}")
        print(f"    local_coverage={row.local_coverage}")
        print(f"    decision={row.decision}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("extended_power_inverses")
    for exponent in EXTENDED_EXACT_ROW_POWERS:
        print(f"  e={exponent}: inverse={pow(exponent, -1, P25 - 1)}")
    print("counts")
    print(f"evidence_markers_ok={marker_count}/{len(EVIDENCE_MARKERS)}")
    print(f"extended_exact_row_power_hooks={len(EXTENDED_EXACT_ROW_POWERS)}")
    print(f"addendum_rows={len(rows)}")
    print(f"broad_local_reread_unlocked={broad_reread_unlocked}")
    print(f"current_extended_power_source_theorems={current_extended_power_source_theorems}")
    print(f"current_exactp_source_theorems={current_exactp_source_theorems}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"p25_v2_extended_power_source_coverage_addendum_rows={int(overall_ok)}/1")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
