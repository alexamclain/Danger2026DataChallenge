#!/usr/bin/env python3
"""Validate the v2 demotion of twisted-H90 and curved-corner lanes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SOURCE_MARKERS = (
    (
        "evidence/p25_v2_support_lane_router_20260616.md",
        "p25_v2_support_lane_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
    (
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
)

LANE_REQUIREMENTS = (
    (
        "lanes/twisted-h90.md",
        (
            "status: background",
            "support surface, not a first-pass front door",
            "period-156 value source hook",
            "source-snippet intake",
        ),
    ),
    (
        "lanes/curved-corner.md",
        (
            "status: background",
            "support surface, not a first-pass front door",
            "period-156 value source hook",
            "source-snippet intake",
        ),
    ),
)

FRONTIER_REQUIREMENTS = (
    "## Support Lanes",
    "support surfaces, not independent first-pass fronts",
    "currently add zero independent front-door closers",
)

INDEX_REQUIREMENTS = (
    "background support surface routed",
    "through period-156 value intake",
    "background support route with",
    "period-156 requirements",
)

PACKET_REQUIRED_LINES = (
    "support_lanes_demoted = 2/2",
    "frontdoor_support_lanes = 0",
    "current_source_theorems = 0",
    "submission_ready_rows = 0",
    "p25_v2_support_lane_status_demotion_rows=1/1",
)


@dataclass(frozen=True)
class SupportLaneDemotionCheck:
    source_markers_ok: int
    source_markers_total: int
    lane_requirements_ok: int
    lane_requirements_total: int
    frontier_requirements_ok: int
    frontier_requirements_total: int
    index_requirements_ok: int
    index_requirements_total: int
    packet_lines_ok: int
    packet_lines_total: int
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def text(root: Path, rel: str) -> str:
    return (root / rel).read_text()


def build_check(root: Path) -> SupportLaneDemotionCheck:
    source_markers_ok = 0
    for rel, marker in SOURCE_MARKERS:
        path = root / rel
        source_markers_ok += int(path.exists() and marker in path.read_text())

    lane_requirements_total = sum(len(reqs) for _rel, reqs in LANE_REQUIREMENTS)
    lane_requirements_ok = 0
    for rel, requirements in LANE_REQUIREMENTS:
        lane_text = text(root, rel)
        lane_requirements_ok += sum(requirement in lane_text for requirement in requirements)

    frontier_text = text(root, "frontier.md")
    frontier_requirements_ok = sum(req in frontier_text for req in FRONTIER_REQUIREMENTS)

    index_text = text(root, "index.md")
    index_requirements_ok = sum(req in index_text for req in INDEX_REQUIREMENTS)

    packet_text = text(root, "evidence/p25_v2_support_lane_status_demotion_20260616.md")
    packet_lines_ok = sum(line in packet_text for line in PACKET_REQUIRED_LINES)

    row_ok = (
        source_markers_ok == len(SOURCE_MARKERS)
        and lane_requirements_ok == lane_requirements_total
        and frontier_requirements_ok == len(FRONTIER_REQUIREMENTS)
        and index_requirements_ok == len(INDEX_REQUIREMENTS)
        and packet_lines_ok == len(PACKET_REQUIRED_LINES)
    )

    return SupportLaneDemotionCheck(
        source_markers_ok=source_markers_ok,
        source_markers_total=len(SOURCE_MARKERS),
        lane_requirements_ok=lane_requirements_ok,
        lane_requirements_total=lane_requirements_total,
        frontier_requirements_ok=frontier_requirements_ok,
        frontier_requirements_total=len(FRONTIER_REQUIREMENTS),
        index_requirements_ok=index_requirements_ok,
        index_requirements_total=len(INDEX_REQUIREMENTS),
        packet_lines_ok=packet_lines_ok,
        packet_lines_total=len(PACKET_REQUIRED_LINES),
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(research_root())
    print("p25 v2 support lane status demotion")
    print(f"source_markers_ok={check.source_markers_ok}/{check.source_markers_total}")
    print(
        "lane_requirements_ok="
        f"{check.lane_requirements_ok}/{check.lane_requirements_total}"
    )
    print(
        "frontier_requirements_ok="
        f"{check.frontier_requirements_ok}/{check.frontier_requirements_total}"
    )
    print(
        "index_requirements_ok="
        f"{check.index_requirements_ok}/{check.index_requirements_total}"
    )
    print(f"packet_lines_ok={check.packet_lines_ok}/{check.packet_lines_total}")
    print(f"p25_v2_support_lane_status_demotion_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
