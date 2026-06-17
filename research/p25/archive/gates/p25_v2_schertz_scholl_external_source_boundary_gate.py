#!/usr/bin/env python3
"""External-source boundary for Schertz/Shin/Scholl value-side leads.

The sources are real anchors for ray-class, Siegel-Ramachandra, and
Kato-Siegel/theta distribution language.  This gate keeps that support from
being confused with a p25 source-stage closer.
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
class SourceBoundaryRow:
    name: str
    source_kind: str
    url: str
    provides_value_unit_framework: bool
    provides_period156_value_or_theta2_payload: bool
    provides_h0_y507_boundary_bridge: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class SchertzSchollExternalSourceBoundary:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceBoundaryRow, ...]
    evidence_markers_ok: int
    general_value_unit_framework_rows: int
    period156_payload_rows: int
    h0_y507_bridge_rows: int
    repair_rows: int
    accepted_future_hook_rows: int
    current_period156_value_theorems: int
    current_source_stage_closers: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "period156_value_source_hook",
            "research/p25/evidence/p25_v2_period156_value_source_hook_20260616.md",
            "p25_v2_period156_value_source_hook_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
        marker(
            "theta2_period156_support_contract",
            "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            "p25_v2_theta2_period156_support_contract_rows=1/1",
        ),
        marker(
            "sprang_theta2_source_intake",
            "research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
            "p25_v2_sprang_theta2_source_intake_rows=1/1",
        ),
        marker(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
    )


def source_rows() -> tuple[SourceBoundaryRow, ...]:
    return (
        SourceBoundaryRow(
            name="schertz_1997_ray_class_elliptic_units",
            source_kind="primary source anchor",
            url="https://eudml.org/doc/248002",
            provides_value_unit_framework=True,
            provides_period156_value_or_theta2_payload=False,
            provides_h0_y507_boundary_bridge=False,
            decision="ray_class_generator_anchor_not_period156_hook",
            first_missing_or_falsifier="exact p25 support-156 edge value, H0/Y507 boundary, or theta2 payload",
            ok=True,
        ),
        SourceBoundaryRow(
            name="shin_1009_2253_siegel_ramachandra",
            source_kind="primary arXiv source anchor",
            url="https://arxiv.org/abs/1009.2253",
            provides_value_unit_framework=True,
            provides_period156_value_or_theta2_payload=False,
            provides_h0_y507_boundary_bridge=False,
            decision="siegel_ramachandra_generator_not_p25_value_hook",
            first_missing_or_falsifier="arithmetic finite value theorem for one oriented support-156 row",
            ok=True,
        ),
        SourceBoundaryRow(
            name="scholl_euler_kato_siegel",
            source_kind="source-note anchor",
            url="https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            provides_value_unit_framework=True,
            provides_period156_value_or_theta2_payload=False,
            provides_h0_y507_boundary_bridge=False,
            decision="kato_siegel_norm_relations_not_d2_p25_hook",
            first_missing_or_falsifier="direct D=2 period-156 theta2/divisor payload with branch or additive normalization",
            ok=True,
        ),
        SourceBoundaryRow(
            name="future_period156_value_or_theta2_hit",
            source_kind="required future hook",
            url="local:p25_period156_h0_y507_or_theta2_payload",
            provides_value_unit_framework=True,
            provides_period156_value_or_theta2_payload=True,
            provides_h0_y507_boundary_bridge=True,
            decision="accepted_if_period156_source_theorem_present",
            first_missing_or_falsifier="DANGER3 framing and extraction after theorem hit",
            ok=True,
        ),
    )


def build_boundary() -> SchertzSchollExternalSourceBoundary:
    markers = evidence_markers()
    rows = source_rows()
    framework = sum(row.provides_value_unit_framework for row in rows)
    payload = sum(row.provides_period156_value_or_theta2_payload for row in rows)
    h0_bridge = sum(row.provides_h0_y507_boundary_bridge for row in rows)
    accepted = sum(row.decision == "accepted_if_period156_source_theorem_present" for row in rows)
    repairs = len(rows) - accepted
    current_period156_value_theorems = 0
    current_source_stage_closers = 0
    expected = (
        "ray_class_generator_anchor_not_period156_hook",
        "siegel_ramachandra_generator_not_p25_value_hook",
        "kato_siegel_norm_relations_not_d2_p25_hook",
        "accepted_if_period156_source_theorem_present",
    )
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 4
        and tuple(row.decision for row in rows) == expected
        and framework == 4
        and payload == 1
        and h0_bridge == 1
        and repairs == 3
        and accepted == 1
        and current_period156_value_theorems == 0
        and current_source_stage_closers == 0
        and all(row.ok for row in rows)
    )
    return SchertzSchollExternalSourceBoundary(
        evidence_markers=markers,
        rows=rows,
        evidence_markers_ok=sum(row.ok for row in markers),
        general_value_unit_framework_rows=framework,
        period156_payload_rows=payload,
        h0_y507_bridge_rows=h0_bridge,
        repair_rows=repairs,
        accepted_future_hook_rows=accepted,
        current_period156_value_theorems=current_period156_value_theorems,
        current_source_stage_closers=current_source_stage_closers,
        row_ok=row_ok,
    )


def main() -> int:
    boundary = build_boundary()
    print("p25 v2 Schertz/Shin/Scholl external source boundary")
    for marker_row in boundary.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in boundary.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    source_kind={row.source_kind}")
        print(f"    url={row.url}")
        print(f"    value_unit_framework={int(row.provides_value_unit_framework)}")
        print(f"    period156_value_or_theta2_payload={int(row.provides_period156_value_or_theta2_payload)}")
        print(f"    h0_y507_boundary_bridge={int(row.provides_h0_y507_boundary_bridge)}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={boundary.evidence_markers_ok}/{len(boundary.evidence_markers)}")
    print(f"  general_value_unit_framework_rows={boundary.general_value_unit_framework_rows}")
    print(f"  period156_payload_rows={boundary.period156_payload_rows}")
    print(f"  h0_y507_bridge_rows={boundary.h0_y507_bridge_rows}")
    print(f"  repair_rows={boundary.repair_rows}")
    print(f"  accepted_future_hook_rows={boundary.accepted_future_hook_rows}")
    print(f"  current_period156_value_theorems={boundary.current_period156_value_theorems}")
    print(f"  current_source_stage_closers={boundary.current_source_stage_closers}")
    print("interpretation")
    print("  external_schertz_shin_scholl_sources_are_framework_not_current_p25_hook=1")
    print("  accepted_hook_requires_period156_value_divisor_or_theta2_payload_with_bridge=1")
    print(f"p25_v2_schertz_scholl_external_source_boundary_rows={int(boundary.row_ok)}/1")
    return 0 if boundary.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
