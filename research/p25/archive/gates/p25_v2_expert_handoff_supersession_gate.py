#!/usr/bin/env python3
"""Check the current expert-handoff supersession path."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"


@dataclass(frozen=True)
class EvidenceMarker:
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
    EvidenceMarker(
        "evidence/p25_v2_minimal_expert_ask_20260616.md",
        "p25_v2_minimal_expert_ask_rows=1/1",
    ),
    EvidenceMarker(
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
)


def read(rel_path: str) -> str:
    return (RESEARCH / rel_path).read_text(errors="replace")


def compact(text: str) -> str:
    return " ".join(text.split())


def main() -> int:
    frontier = read("frontier.md")
    h0 = read("lanes/h0.md")
    conductor39 = read("lanes/conductor39.md")
    exactp = read("lanes/exact-p.md")
    frontier_flat = compact(frontier)
    marker_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    stale_preferred_count = sum(
        text.count("minimal expert ask is now the preferred")
        for text in (frontier, h0, conductor39, exactp)
    )
    checks = {
        "frontier_names_current_expert_packet": (
            "The current expert-facing handoff is the Drew kernel review packet"
            in frontier_flat
        ),
        "frontier_names_supporting_minimal_ask": (
            "is now supporting predecessor context for the Drew kernel review packet"
            in frontier
        ),
        "h0_routes_expert_replies_to_drew_packet": (
            "H0 expert replies should be judged against the Drew kernel review packet"
            in h0
        ),
        "conductor39_routes_expert_replies_to_drew_packet": (
            "Conductor-39 expert replies should be judged against the Drew kernel review"
            in conductor39
        ),
        "h0_minimal_ask_supporting_only": (
            "The minimal expert ask is now supporting H0 handoff provenance"
            in h0
        ),
        "conductor39_minimal_ask_supporting_only": (
            "The minimal expert ask is now supporting conductor-39 handoff provenance"
            in conductor39
        ),
        "exactp_drew_packet_boundary_present": (
            "The Drew kernel review packet makes the exact-P boundary expert-facing"
            in exactp
        ),
    }
    current_handoff_headings = (
        "### 1. Scalar-Fixed Row Theorem",
        "### 2. Row-Labeled Unique Power",
        "### 3. Support-Period-156 Value",
    )
    drew_packet = read("evidence/p25_v2_drew_kernel_review_packet_20260617.md")
    handoff_rows_present = all(row in drew_packet for row in current_handoff_headings)
    overall_ok = (
        marker_count == len(EVIDENCE_MARKERS)
        and stale_preferred_count == 0
        and all(checks.values())
        and handoff_rows_present
    )

    print("p25 v2 expert handoff supersession")
    print(f"evidence_markers_ok={marker_count}/{len(EVIDENCE_MARKERS)}")
    print(f"stale_preferred_count={stale_preferred_count}")
    for name, ok in checks.items():
        print(f"{name}={int(ok)}")
    print(f"current_handoff_rows_present={int(handoff_rows_present)}")
    print(f"p25_v2_expert_handoff_supersession_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("expert handoff supersession failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
