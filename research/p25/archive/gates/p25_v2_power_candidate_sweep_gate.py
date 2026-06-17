#!/usr/bin/env python3
"""Sweep prior power-shaped artifacts under the p25 v2 power intake."""

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
class SweepRow:
    name: str
    prior_shape: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class PowerCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_future_power_intakes: int
    current_source_stage_closers: int
    current_submission_ready: int
    lane_b_kernel_monodromy_confirmed: bool
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
        marker(
            "power_projector_extraction_boundary",
            "research/p25/evidence/p25_v2_power_projector_extraction_boundary_20260616.md",
            "p25_v2_power_projector_extraction_boundary_rows=1/1",
        ),
        marker(
            "coefficient6_root_normalization",
            "research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md",
            "p25_v2_coefficient6_root_normalization_rows=1/1",
        ),
        marker(
            "primitive_character_power_recheck",
            "research/p25/evidence/p25_v2_primitive_character_power_recheck_20260617.md",
            "p25_v2_primitive_character_power_recheck_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="router_exact_power_templates",
            prior_shape="exact_value_power3/exact_value_power39 and exact_R3_value/exact_R39_value rows",
            decision="intake_templates_not_source_discoveries",
            first_missing_or_falsifier="the router pages classify hypothetical snippets and record current source theorem count zero",
            ok=True,
        ),
        SweepRow(
            name="coefficient_root_shapes",
            prior_shape="coefficient-1/2/3 exact root rows powering to coefficient 6",
            decision="conditional_power_back_shape_not_prior_candidate",
            first_missing_or_falsifier="the page states it is an arithmetic screen, not a source theorem",
            ok=True,
        ),
        SweepRow(
            name="primitive_character_power_relation",
            prior_shape="V_bal=U_chi^3 and W=U_chi^6",
            decision="support_identity_not_exact_Fp_row_power_value",
            first_missing_or_falsifier="primitive-character recheck classifies it as exponent-word/source-unit support",
            ok=True,
        ),
        SweepRow(
            name="lane_b_d_cubed_relation",
            prior_shape="Lane B D^3=Y after quotienting or trace-down",
            decision="quotient_kernel_monodromy_not_legal_row_value_theorem",
            first_missing_or_falsifier="raw D^3 and Y differ by one B=25 trace-kernel layer and nontrivial kernel characters trace to zero",
            ok=True,
        ),
        SweepRow(
            name="source_family_prior_scan",
            prior_shape="inspected Koo-Shin/Sprang/Kubert-Lang/Schertz source families",
            decision="no_prior_exact_power_source_theorem_found",
            first_missing_or_falsifier="source-family gap matrix still has scalar_fixed_finite_theorems=0 and first_pass_closers=0",
            ok=True,
        ),
        SweepRow(
            name="surviving_future_power_intake",
            prior_shape="future exact F_p theorem for R_m^e with e in {3,5,13,39,75,169,507}",
            decision="keep_as_live_expert_ask",
            first_missing_or_falsifier="must name one legal row or row-labeled theorem and the Norm_156(Y_507) boundary/period bridge",
            ok=True,
        ),
    )


def build_sweep() -> PowerCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    power_router = read("research/p25/evidence/p25_v2_power_output_kind_router_20260616.md")
    power_projector = read("research/p25/evidence/p25_v2_power_projector_extraction_boundary_20260616.md")
    coefficient = read("research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md")
    primitive = read("research/p25/evidence/p25_v2_primitive_character_power_recheck_20260617.md")
    source_family = read("research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md")
    raw_shift = read("research/p25/archive/notes/subsqrt_moonshot_laneB_square_axis_raw_shift_lift.md")
    factor_kummer = read("research/p25/archive/notes/subsqrt_moonshot_laneB_square_axis_bridge_factor_kummer.md")
    kernel_trace = read("research/p25/archive/notes/subsqrt_moonshot_laneB_square_axis_kernel_character_trace.md")

    router_ok = (
        "exact_value_power3" in power_router
        and "current_source_stage_closers = 0" in power_router
        and "exact_R3_value" in power_projector
        and "current_source_theorem = no" in power_projector
    )
    coefficient_ok = (
        "This is a p25 arithmetic screen, not a source theorem." in coefficient
        and "coefficient2_exact_root_value" in coefficient
        and "current_source_stage_closers = 0" in coefficient
    )
    primitive_ok = (
        "support_identity_not_power_value_theorem" in primitive
        and "current_source_stage_closers = 0" in primitive
    )
    lane_b_kernel_monodromy_confirmed = (
        "same quotient coordinate" in raw_shift
        and "one raw trace-kernel layer" in raw_shift
        and "becomes true only after the `25`-kernel trace has been collapsed" in factor_kummer
        and "every nontrivial `C_25` kernel character has zero trace" in kernel_trace
    )
    source_scan_ok = (
        "scalar_fixed_finite_theorems = 0" in source_family
        and "first_pass_closers = 0" in source_family
    )
    current_source_stage_closers = 0
    current_submission_ready = 0
    newly_promoted_prior_candidates = 0
    surviving_future_power_intakes = 1
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 6
        and all(row.ok for row in rows)
        and router_ok
        and coefficient_ok
        and primitive_ok
        and lane_b_kernel_monodromy_confirmed
        and source_scan_ok
        and newly_promoted_prior_candidates == 0
        and surviving_future_power_intakes == 1
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return PowerCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_future_power_intakes=surviving_future_power_intakes,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        lane_b_kernel_monodromy_confirmed=lane_b_kernel_monodromy_confirmed,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 power candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_future_power_intakes={sweep.surviving_future_power_intakes}")
    print(f"  lane_b_kernel_monodromy_confirmed={int(sweep.lane_b_kernel_monodromy_confirmed)}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_power_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
