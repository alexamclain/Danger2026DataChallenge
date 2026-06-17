#!/usr/bin/env python3
"""Boundary between powered/projector row values and DANGER3 extraction.

Exact values for powers of a legal row can be useful finite payloads.  When
the power map has a nontrivial kernel, however, those payloads are bounded
row-value candidates, not concrete DANGER3 `(A,x0)` candidates.  This gate
keeps the power/projector screens aligned with the stricter Q-square
extraction boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class BoundaryRow:
    name: str
    exponent: int
    exact_finite_value: bool
    selected_root: bool
    divisor_or_boundary_only: bool
    kernel_size: int
    row_value_payload_count: int
    source_stage_candidate: bool
    extraction_ready: bool
    submission_ready: bool
    decision: str
    missing_or_falsifier: str
    row_ok: bool


@dataclass(frozen=True)
class PowerProjectorExtractionBoundary:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[BoundaryRow, ...]
    unique_root_rows: int
    bounded_row_value_payload_rows: int
    selected_root_normalize_rows: int
    repair_rows: int
    reject_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    current_extraction_ready_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
    )


def boundary_row(
    name: str,
    exponent: int,
    *,
    exact_value: bool,
    selected_root: bool = False,
    divisor_only: bool = False,
    direct_vpp_on_row_value: bool = False,
) -> BoundaryRow:
    kernel = gcd(exponent, P25 - 1)
    if direct_vpp_on_row_value:
        return BoundaryRow(
            name=name,
            exponent=exponent,
            exact_finite_value=exact_value,
            selected_root=selected_root,
            divisor_or_boundary_only=divisor_only,
            kernel_size=kernel,
            row_value_payload_count=0,
            source_stage_candidate=False,
            extraction_ready=False,
            submission_ready=False,
            decision="reject_vpp_requires_A_x0_not_row_value",
            missing_or_falsifier="vpp.py verifies (p,A,x0), not a modular-unit row value",
            row_ok=True,
        )
    if divisor_only:
        return BoundaryRow(
            name=name,
            exponent=exponent,
            exact_finite_value=exact_value,
            selected_root=selected_root,
            divisor_or_boundary_only=divisor_only,
            kernel_size=kernel,
            row_value_payload_count=0,
            source_stage_candidate=False,
            extraction_ready=False,
            submission_ready=False,
            decision="repair_exact_finite_value_or_additive_normalization_missing",
            missing_or_falsifier="divisor/H90/projector data alone does not fix a finite row value",
            row_ok=True,
        )
    if exact_value and kernel == 1:
        return BoundaryRow(
            name=name,
            exponent=exponent,
            exact_finite_value=exact_value,
            selected_root=selected_root,
            divisor_or_boundary_only=divisor_only,
            kernel_size=kernel,
            row_value_payload_count=1,
            source_stage_candidate=True,
            extraction_ready=False,
            submission_ready=False,
            decision="normalize_unique_power_value_then_source_intake",
            missing_or_falsifier="source-snippet intake, then DANGER3 framing and extraction",
            row_ok=True,
        )
    if exact_value and selected_root:
        return BoundaryRow(
            name=name,
            exponent=exponent,
            exact_finite_value=exact_value,
            selected_root=selected_root,
            divisor_or_boundary_only=divisor_only,
            kernel_size=kernel,
            row_value_payload_count=1,
            source_stage_candidate=True,
            extraction_ready=False,
            submission_ready=False,
            decision="normalize_selected_power_value_then_source_intake",
            missing_or_falsifier="source-snippet intake, then DANGER3 framing and extraction",
            row_ok=True,
        )
    if exact_value:
        return BoundaryRow(
            name=name,
            exponent=exponent,
            exact_finite_value=exact_value,
            selected_root=selected_root,
            divisor_or_boundary_only=divisor_only,
            kernel_size=kernel,
            row_value_payload_count=kernel,
            source_stage_candidate=False,
            extraction_ready=False,
            submission_ready=False,
            decision="repair_power_root_selector_missing_after_bounded_row_payload",
            missing_or_falsifier=(
                f"{kernel} F_p row roots exist; orientation/branch/scalar and "
                "DANGER3 same-j/X_1(16)/halving or direct A,x0 map still missing"
            ),
            row_ok=True,
        )
    return BoundaryRow(
        name=name,
        exponent=exponent,
        exact_finite_value=exact_value,
        selected_root=selected_root,
        divisor_or_boundary_only=divisor_only,
        kernel_size=kernel,
        row_value_payload_count=0,
        source_stage_candidate=False,
        extraction_ready=False,
        submission_ready=False,
        decision="repair_exact_value_missing",
        missing_or_falsifier="exact scalar-fixed finite value missing",
        row_ok=True,
    )


def build_rows() -> tuple[BoundaryRow, ...]:
    return (
        boundary_row("exact_R3_value", 3, exact_value=True),
        boundary_row("exact_R39_value", 39, exact_value=True),
        boundary_row("exact_R2_value_no_sign", 2, exact_value=True),
        boundary_row("exact_R4_projector_value_no_branch", 4, exact_value=True),
        boundary_row("exact_R11_value_no_branch", 11, exact_value=True),
        boundary_row("exact_R156_value_no_branch", 156, exact_value=True),
        boundary_row("exact_R4_projector_value_with_selected_root", 4, exact_value=True, selected_root=True),
        boundary_row("projector_components_divisor_only", 4, exact_value=False, divisor_only=True),
        boundary_row("direct_vpp_on_power_row_root", 4, exact_value=True, direct_vpp_on_row_value=True),
    )


def build_profile() -> PowerProjectorExtractionBoundary:
    markers = evidence_markers()
    rows = build_rows()
    unique = sum(row.decision == "normalize_unique_power_value_then_source_intake" for row in rows)
    bounded = sum(row.decision == "repair_power_root_selector_missing_after_bounded_row_payload" for row in rows)
    selected = sum(row.decision == "normalize_selected_power_value_then_source_intake" for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    rejects = sum(row.decision.startswith("reject_") for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    current_extraction_ready = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and tuple((row.name, row.kernel_size, row.row_value_payload_count, row.decision) for row in rows)
        == (
            ("exact_R3_value", 1, 1, "normalize_unique_power_value_then_source_intake"),
            ("exact_R39_value", 1, 1, "normalize_unique_power_value_then_source_intake"),
            ("exact_R2_value_no_sign", 2, 2, "repair_power_root_selector_missing_after_bounded_row_payload"),
            ("exact_R4_projector_value_no_branch", 4, 4, "repair_power_root_selector_missing_after_bounded_row_payload"),
            ("exact_R11_value_no_branch", 11, 11, "repair_power_root_selector_missing_after_bounded_row_payload"),
            ("exact_R156_value_no_branch", 4, 4, "repair_power_root_selector_missing_after_bounded_row_payload"),
            ("exact_R4_projector_value_with_selected_root", 4, 1, "normalize_selected_power_value_then_source_intake"),
            ("projector_components_divisor_only", 4, 0, "repair_exact_finite_value_or_additive_normalization_missing"),
            ("direct_vpp_on_power_row_root", 4, 0, "reject_vpp_requires_A_x0_not_row_value"),
        )
        and unique == 2
        and bounded == 4
        and selected == 1
        and repairs == 5
        and rejects == 1
        and extraction_ready == 0
        and submission_ready == 0
        and current_extraction_ready == 0
        and current_submission_ready == 0
        and all(row.row_ok for row in rows)
    )
    return PowerProjectorExtractionBoundary(
        evidence_markers=markers,
        rows=rows,
        unique_root_rows=unique,
        bounded_row_value_payload_rows=bounded,
        selected_root_normalize_rows=selected,
        repair_rows=repairs,
        reject_rows=rejects,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        current_extraction_ready_rows=current_extraction_ready,
        current_submission_ready_rows=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 power/projector extraction boundary")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("boundary_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: e={row.exponent} kernel={row.kernel_size} "
            f"row_payload={row.row_value_payload_count} "
            f"source={int(row.source_stage_candidate)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} decision={row.decision}"
        )
        print(f"    missing_or_falsifier={row.missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in profile.evidence_markers)}/{len(profile.evidence_markers)}")
    print(f"  unique_root_rows={profile.unique_root_rows}")
    print(f"  bounded_row_value_payload_rows={profile.bounded_row_value_payload_rows}")
    print(f"  selected_root_normalize_rows={profile.selected_root_normalize_rows}")
    print(f"  repair_rows={profile.repair_rows}")
    print(f"  reject_rows={profile.reject_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  current_extraction_ready_rows={profile.current_extraction_ready_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  bounded_power_roots_are_row_values_not_vpp_candidates=1")
    print("  selected_or_unique_power_roots_still_route_through_source_intake=1")
    print("  direct_vpp_requires_A_x0_not_modular_unit_row_value=1")
    print(f"p25_v2_power_projector_extraction_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("power/projector extraction boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
