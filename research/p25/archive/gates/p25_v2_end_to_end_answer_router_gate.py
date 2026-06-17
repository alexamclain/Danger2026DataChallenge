#!/usr/bin/env python3
"""Validate the end-to-end p25 answer router.

This gate keeps future expert/source/practical answers from being overpromoted.
It checks that the new router is aligned with the promoted source-intake,
DANGER3 framing, extraction, and verifier-boundary artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SOURCE_MARKERS = (
    (
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
        "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_extraction_minimal_hook_20260616.md",
        "p25_v2_extraction_minimal_hook_rows=1/1",
    ),
    (
        "evidence/p25_v2_extraction_payload_contract_20260616.md",
        "p25_v2_extraction_payload_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
        "p25_v2_unified_submission_extraction_contract_rows=1/1",
    ),
)

VPP_BOUNDARY_MARKERS = (
    (
        "evidence/p25_v2_extraction_minimal_hook_20260616.md",
        "official_vpp_verified",
    ),
    (
        "evidence/p25_v2_extraction_payload_contract_20260616.md",
        "official_vpp_verified_triple",
    ),
    (
        "evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
        "official vpp.py verification",
    ),
)

ROUTER_STAGES = (
    "stage_0_reject_or_repair",
    "stage_1_source_stage_candidate",
    "stage_2_danger3_framed_theorem",
    "stage_3_same_j_bridge",
    "stage_4_practical_x1_16_surface",
    "stage_5_x0_or_x_chain",
    "stage_6_official_vpp_verified",
)

REPAIR_OR_REJECT_EXAMPLES = (
    "source_legality_only",
    "boundary_only",
    "generic_cm_or_class_field_generation",
    "same_j_invariant_only",
    "independent_p16_q507",
    "branch_word_without_values",
    "x0_extracted_vpp_missing",
)

PACKET_REQUIRED_LINES = (
    "router_stages = 7/7",
    "current_source_theorems = 0",
    "current_danger3_framed_theorems = 0",
    "current_extraction_ready_rows = 0",
    "submission_ready_rows = 0",
    "p25_v2_end_to_end_answer_router_rows=1/1",
)


@dataclass(frozen=True)
class EndToEndRouterCheck:
    source_markers_ok: int
    source_markers_total: int
    vpp_boundary_ok: int
    vpp_boundary_total: int
    stages_ok: int
    stages_total: int
    repair_rows_ok: int
    repair_rows_total: int
    packet_lines_ok: int
    packet_lines_total: int
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text()


def build_check(root: Path) -> EndToEndRouterCheck:
    source_markers_ok = 0
    source_texts: dict[str, str] = {}
    for rel, marker in SOURCE_MARKERS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        source_texts[rel] = text
        source_markers_ok += int(marker in text)

    vpp_boundary_ok = 0
    for rel, marker in VPP_BOUNDARY_MARKERS:
        text = source_texts.get(rel)
        if text is None:
            text = read(root, rel)
        vpp_boundary_ok += int(marker in text)

    packet_text = read(root, "evidence/p25_v2_end_to_end_answer_router_20260616.md")
    combined = packet_text + "\n" + "\n".join(source_texts.values())

    stages_ok = sum(stage in packet_text for stage in ROUTER_STAGES)
    repair_rows_ok = sum(row in combined for row in REPAIR_OR_REJECT_EXAMPLES)
    packet_lines_ok = sum(line in packet_text for line in PACKET_REQUIRED_LINES)

    row_ok = (
        source_markers_ok == len(SOURCE_MARKERS)
        and vpp_boundary_ok == len(VPP_BOUNDARY_MARKERS)
        and stages_ok == len(ROUTER_STAGES)
        and repair_rows_ok == len(REPAIR_OR_REJECT_EXAMPLES)
        and packet_lines_ok == len(PACKET_REQUIRED_LINES)
    )

    return EndToEndRouterCheck(
        source_markers_ok=source_markers_ok,
        source_markers_total=len(SOURCE_MARKERS),
        vpp_boundary_ok=vpp_boundary_ok,
        vpp_boundary_total=len(VPP_BOUNDARY_MARKERS),
        stages_ok=stages_ok,
        stages_total=len(ROUTER_STAGES),
        repair_rows_ok=repair_rows_ok,
        repair_rows_total=len(REPAIR_OR_REJECT_EXAMPLES),
        packet_lines_ok=packet_lines_ok,
        packet_lines_total=len(PACKET_REQUIRED_LINES),
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(research_root())
    print("p25 v2 end-to-end answer router")
    print(f"source_markers_ok={check.source_markers_ok}/{check.source_markers_total}")
    print(f"vpp_boundary_ok={check.vpp_boundary_ok}/{check.vpp_boundary_total}")
    print(f"router_stages_ok={check.stages_ok}/{check.stages_total}")
    print(f"repair_or_reject_examples_ok={check.repair_rows_ok}/{check.repair_rows_total}")
    print(f"packet_lines_ok={check.packet_lines_ok}/{check.packet_lines_total}")
    print(f"p25_v2_end_to_end_answer_router_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
