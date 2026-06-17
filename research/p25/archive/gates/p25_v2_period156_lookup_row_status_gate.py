#!/usr/bin/env python3
"""Validate the period-156 lookup-row status artifact."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class StatusRow:
    name: str
    accepted_hook: str
    current_status: str
    first_falsifier: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "priority1_source_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "period156_value_branch_contract",
        "evidence/p25_v2_period156_value_branch_contract_20260616.md",
        "p25_v2_period156_value_branch_contract_rows=1/1",
    ),
    (
        "period156_value_source_hook",
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    (
        "period156_value_candidate_sweep",
        "evidence/p25_v2_period156_value_candidate_sweep_20260617.md",
        "p25_v2_period156_value_candidate_sweep_rows=1/1",
    ),
    (
        "h0_y507_period156_compatibility",
        "evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
        "p25_v2_h0_y507_period156_compatibility_rows=1/1",
    ),
    (
        "schertz_scholl_external_source_boundary",
        "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
        "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
    ),
    (
        "theta2_period156_support_contract",
        "evidence/p25_v2_theta2_period156_support_contract_20260616.md",
        "p25_v2_theta2_period156_support_contract_rows=1/1",
    ),
    (
        "sprang_theta2_source_intake",
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
    (
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    (
        "source_action_registry",
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        text = read(root / rel)
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def status_rows() -> tuple[StatusRow, ...]:
    return (
        StatusRow(
            "canonical_h0_period156_value",
            "arithmetic finite F_p value theorem for canonical H0 with Norm_156(Y_507) boundary and period-156 branch/root/telescoping data",
            "live_not_in_hand",
            "ambient-period-780 value, mu_11 quotient, value up to scalar, or source vocabulary without exact H0 row",
            "continue_only_on_exact_value_theorem",
        ),
        StatusRow(
            "y507_period156_value",
            "arithmetic finite F_p value theorem for Y_507 with period-156 context and bridge to one legal support-156 row",
            "live_not_in_hand",
            "Y_507 name, norm identity, or boundary-only statement without finite value and legal-row bridge",
            "continue_only_on_exact_value_theorem",
        ),
        StatusRow(
            "canonical_h0_divisor_additive_backup",
            "scalar-fixed finite divisor/additive identity for canonical H0 with Norm_156(Y_507) boundary",
            "same_branch_free_backup_as_priority1",
            "divisor class, H90 boundary, or up-to-scalar value without additive/basepoint/telescoping normalization",
            "route_back_to_priority1_divisor_additive",
        ),
        StatusRow(
            "theta2_or_theta2_inverse_payload",
            "exact theta2/theta2-inverse divisor/additive payload with period-156 bridge into the support-156 target",
            "support_confirmed_but_no_arithmetic_producer",
            "theta2 support certificate, Sprang D=2 support, or branchless theta value without sparse payload and bridge",
            "continue_only_on_exact_theta2_payload",
        ),
        StatusRow(
            "schertz_shin_scholl_framework_sources",
            "source theorem specializing framework/value-unit language to the exact p25 H0/Y507/theta2 hook",
            "framework_not_current_hook",
            "ray-class generation, Siegel-Ramachandra generator language, generic norm relation, or direct Scholl D=2 import",
            "ask_narrow_source_question_only",
        ),
        StatusRow(
            "ambient_or_shortcut_values",
            "none",
            "repair_or_reject",
            "ambient 780 branch ambiguity, degree-6 value without F_p descent, direct order-39 root, or sqrt(-39) scalar shortcut",
            "discard_without_new_branch_descent_data",
        ),
    )


def evidence_consistency(root: Path) -> bool:
    candidate = read(root / "evidence/p25_v2_period156_value_candidate_sweep_20260617.md")
    hook = read(root / "evidence/p25_v2_period156_value_source_hook_20260616.md")
    boundary = read(root / "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md")
    return (
        "current_period156_value_theorems = 0" in candidate
        and "surviving_value_intake_families = 3" in candidate
        and "current_period156_value_theorems = 0" in hook
        and "accepted_routes = 2" in hook
        and "current_source_stage_closers = 0" in boundary
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[StatusRow, ...], bool]:
    markers = evidence_markers(root)
    rows = status_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and evidence_consistency(root)
        and len(rows) == 6
        and sum(row.current_status == "live_not_in_hand" for row in rows) == 2
        and sum("priority1" in row.decision for row in rows) == 1
        and sum("theta2" in row.name for row in rows) == 1
        and sum(row.current_status == "repair_or_reject" for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 period-156 lookup-row status")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"evidence_consistency={int(evidence_consistency(root))}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    current_status={row.current_status}")
        print(f"    accepted_hook={row.accepted_hook}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"status_rows={len(rows)}")
    print("surviving_value_intake_families=3")
    print("current_period156_value_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_period156_lookup_row_status_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
