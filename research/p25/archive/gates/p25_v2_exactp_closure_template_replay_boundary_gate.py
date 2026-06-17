#!/usr/bin/env python3
"""Replay boundary for the archived exact-P closure-template gate.

The old closure-template gate is still useful as provenance, but replaying it
during an active production fleet enters the heavy support-resolvent stack.
This lightweight v2 gate records the boundary and points to the promoted
exact-P contracts that should be used for normal theorem intake.
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
class ReplayBoundaryRow:
    name: str
    status: str
    command_or_surface: str
    observed_or_required: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class ExactPClosureTemplateReplayBoundary:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[ReplayBoundaryRow, ...]
    markers_ok: int
    heavy_replay_rows: int
    lightweight_successor_rows: int
    exactp_source_theorems: int
    submission_ready_rows: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_theorem_interface_contract",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "still_missing = challenge-legal Robert/Siegel/Kubert-Lang/KSY identity",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "theta2_period156_support_contract",
            "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            "p25_v2_theta2_period156_support_contract_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
        marker(
            "source_action_registry",
            "research/p25/evidence/p25_v2_source_action_registry_20260616.md",
            "p25_v2_source_action_registry_rows=1/1",
        ),
    )


def boundary_rows() -> tuple[ReplayBoundaryRow, ...]:
    return (
        ReplayBoundaryRow(
            name="archived_closure_template_gate",
            status="heavy_replay_boundary",
            command_or_surface=(
                "PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness "
                "python3 research/p25/archive/gates/"
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py"
            ),
            observed_or_required=(
                "entered support-resolvent / half-edge footprint stack; interrupted "
                "after more than 60 seconds during active fleet"
            ),
            decision="do_not_use_as_default_short_probe",
            ok=True,
        ),
        ReplayBoundaryRow(
            name="missing_harness_path",
            status="replay_hygiene_boundary",
            command_or_surface="PYTHONPATH=research/p25/archive/gates only",
            observed_or_required="fails before replay because archived harness modules are not on sys.path",
            decision="use_archive_harness_path_if_explicit_heavy_replay_is_needed",
            ok=True,
        ),
        ReplayBoundaryRow(
            name="v2_exactp_theorem_interface_contract",
            status="lightweight_successor",
            command_or_surface="research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            observed_or_required="compact C,D,K,orientation target and accepted equivalent interfaces are already promoted",
            decision="use_for_normal_exactp_intake",
            ok=True,
        ),
        ReplayBoundaryRow(
            name="v2_exactp_minimal_hook",
            status="lightweight_successor",
            command_or_surface="research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            observed_or_required="minimal source ask, repair rows, and current exact-P source theorem count are explicit",
            decision="use_for_source_or_expert_answers",
            ok=True,
        ),
        ReplayBoundaryRow(
            name="v2_theta2_period156_support_contract",
            status="lightweight_successor",
            command_or_surface="research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            observed_or_required="period-156 theta2 support certificate and source obligation are already promoted",
            decision="use_for_theta2_payload_intake",
            ok=True,
        ),
    )


def build_boundary() -> ExactPClosureTemplateReplayBoundary:
    markers = evidence_markers()
    rows = boundary_rows()
    heavy = sum(row.status == "heavy_replay_boundary" for row in rows)
    lightweight = sum(row.status == "lightweight_successor" for row in rows)
    exactp_source_theorems = 0
    submission_ready_rows = 0
    expected_decisions = (
        "do_not_use_as_default_short_probe",
        "use_archive_harness_path_if_explicit_heavy_replay_is_needed",
        "use_for_normal_exactp_intake",
        "use_for_source_or_expert_answers",
        "use_for_theta2_payload_intake",
    )
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and tuple(row.decision for row in rows) == expected_decisions
        and heavy == 1
        and lightweight == 3
        and exactp_source_theorems == 0
        and submission_ready_rows == 0
        and all(row.ok for row in rows)
    )
    return ExactPClosureTemplateReplayBoundary(
        markers=markers,
        rows=rows,
        markers_ok=sum(marker_row.ok for marker_row in markers),
        heavy_replay_rows=heavy,
        lightweight_successor_rows=lightweight,
        exactp_source_theorems=exactp_source_theorems,
        submission_ready_rows=submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    boundary = build_boundary()
    print("p25 v2 exact-P closure-template replay boundary")
    for marker_row in boundary.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in boundary.rows:
        print(f"  {row.name}: status={row.status}")
        print(f"    surface={row.command_or_surface}")
        print(f"    observed_or_required={row.observed_or_required}")
        print(f"    decision={row.decision}")
    print("counts")
    print(f"  markers_ok={boundary.markers_ok}/{len(boundary.markers)}")
    print(f"  heavy_replay_rows={boundary.heavy_replay_rows}")
    print(f"  lightweight_successor_rows={boundary.lightweight_successor_rows}")
    print(f"  exactp_source_theorems={boundary.exactp_source_theorems}")
    print(f"  submission_ready_rows={boundary.submission_ready_rows}")
    print("interpretation")
    print("  exactp_old_closure_template_is_archive_provenance_not_default_probe=1")
    print("  exactp_v2_lightweight_contracts_are_current_intake_surface=1")
    print(f"p25_v2_exactp_closure_template_replay_boundary_rows={int(boundary.row_ok)}/1")
    return 0 if boundary.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
