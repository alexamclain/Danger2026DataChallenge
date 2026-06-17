#!/usr/bin/env python3
"""Sweep conductor-39 Q-route artifacts under the p25 v2 intake."""

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
class QRouteCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_q_intake_families: int
    q_support_route_live: bool
    q_square_payload_bounded: bool
    current_q_source_hooks: int
    current_source_stage_closers: int
    current_extraction_ready: int
    current_submission_ready: int
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "conductor39_norm_one_quotient_route",
            "research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
            "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
        ),
        marker(
            "q_route_selector_debt",
            "research/p25/evidence/p25_v2_q_route_selector_debt_20260616.md",
            "p25_v2_q_route_selector_debt_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_split_quotient_complexity",
            "research/p25/evidence/p25_v2_q_split_quotient_complexity_20260616.md",
            "p25_v2_q_split_quotient_complexity_rows=1/1",
        ),
        marker(
            "q_split_quartic_selector",
            "research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md",
            "p25_v2_q_split_quartic_selector_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "q_route_source_hook_scan",
            "research/p25/evidence/p25_v2_q_route_source_hook_scan_20260616.md",
            "p25_v2_q_route_source_hook_scan_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="norm_one_q_value_period156_context",
            prior_shape="finite Q value theorem with period-156 context",
            decision="support_route_selector_debt_remains",
            first_missing_or_falsifier="must also recover one oriented C4 edge, boundary-zero value, or direct one-edge theorem",
            ok=True,
        ),
        SweepRow(
            name="q3_h90_preimage_finite_theorem",
            prior_shape="finite theorem for Q^3 with Q^6=(1-Frob_p)(Q^3)",
            decision="support_route_selector_debt_remains",
            first_missing_or_falsifier="selector/normalization to one legal edge still missing",
            ok=True,
        ),
        SweepRow(
            name="q6_boundary_only",
            prior_shape="Q^6 or Hilbert-90 boundary data only",
            decision="repair_additive_or_value_normalization_missing",
            first_missing_or_falsifier="scalar-fixed finite value/additive theorem plus selector missing",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_value_only",
            prior_shape="Q_antisym=m1+m4=m2+m8 diagonal aggregate",
            decision="support_diagonal_aggregate_selector_missing",
            first_missing_or_falsifier="boundary-zero split/orientation or direct one-edge theorem missing",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_plus_support12_row_quotient",
            prior_shape="Q diagonal plus support-12 boundary-zero row quotient",
            decision="reject_wrong_split_for_q_diagonal",
            first_missing_or_falsifier="support-12 row quotients are not m1-m4 or m2-m8",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_plus_correct_split_without_root",
            prior_shape="Q diagonal plus m1-m4 or m2-m8 pure quartic split",
            decision="repair_oriented_square_root_missing",
            first_missing_or_falsifier="diagonal plus split reaches 2*edge, not a scalar-fixed edge value",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_plus_correct_split_with_oriented_root",
            prior_shape="Q diagonal plus matching pure quartic split and oriented root/sign",
            decision="normalize_to_one_edge_then_apply_source_snippet_intake",
            first_missing_or_falsifier="not present in prior artifacts; still needs theorem data and extraction",
            ok=True,
        ),
        SweepRow(
            name="q_square_exact_fp_value",
            prior_shape="exact scalar-fixed finite F_p value for the resulting Q square",
            decision="bounded_two_root_payload_not_source_close",
            first_missing_or_falsifier="two row-value roots still need DANGER3 extraction map",
            ok=True,
        ),
        SweepRow(
            name="q_square_divisor_boundary_phase_or_scalar_only",
            prior_shape="divisor, H90 boundary, quartic phase, or value-up-to-scalar for Q square",
            decision="repair_or_reject_sign_and_scalar_missing",
            first_missing_or_falsifier="constant sign is invisible to divisor/H90/phase data",
            ok=True,
        ),
        SweepRow(
            name="local_source_q_language",
            prior_shape="local Koo-Shin/KSY/Sprang source language mentioning Q, split, theta, or distribution vocabulary",
            decision="no_q_route_source_hook_in_local_sources",
            first_missing_or_falsifier="no conductor-39 Q product, Q^3/Q^6 theorem, split/root data, Norm_156, or period-156 hook",
            ok=True,
        ),
        SweepRow(
            name="pure_character_degree6_norm",
            prior_shape="degree-6 norm of the pure conductor-39 character word",
            decision="reject_pure_character_degree6_norm_cancels",
            first_missing_or_falsifier="Frobenius alternation makes the degree-6 norm zero",
            ok=True,
        ),
    )


def build_sweep() -> QRouteCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    norm_one = read("research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md")
    debt = read("research/p25/evidence/p25_v2_q_route_selector_debt_20260616.md")
    diagonal = read("research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md")
    split = read("research/p25/evidence/p25_v2_q_split_quotient_complexity_20260616.md")
    quartic = read("research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md")
    q_square = read("research/p25/evidence/p25_v2_q_square_payload_router_20260616.md")
    extraction = read("research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md")
    source = read("research/p25/evidence/p25_v2_q_route_source_hook_scan_20260616.md")
    intake = read("research/p25/evidence/p25_v2_source_snippet_intake_20260616.md")
    rubric = read("research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md")
    minimal = read("research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md")

    q_support_route_live = (
        "support_routes = 2" in norm_one
        and "current_source_theorems = 0" in norm_one
        and "source_candidate_routes = 1" in debt
        and "support_routes = 2" in debt
    )
    selector_debt_ok = (
        "Q_projection = m1 + m4" in diagonal
        and "Q_projection = m2 + m8" in diagonal
        and "source_candidate_routes = 1" in diagonal
        and "current_source_theorems = 0" in diagonal
    )
    split_ok = (
        "diagonal_support24_count = 2" in split
        and "support12_non_diagonal_count = 4" in split
        and "current_source_theorems = 0" in split
    )
    quartic_ok = (
        "pure_quadratic_diagonals = 2" in quartic
        and "pure_quartic_splits = 2" in quartic
        and "current_source_theorems = 0" in quartic
    )
    q_square_payload_bounded = (
        "bounded_payload_rows = 1" in q_square
        and "current_source_theorems = 0" in q_square
        and "current_extraction_ready_rows = 0" in extraction
        and "current_submission_ready_rows = 0" in extraction
    )
    source_ok = (
        "q_route_term_rows = 0" in source
        and "accepted_source_hook_rows = 0" in source
        and "source_stage_closers = 0" in source
    )
    intake_ok = (
        "norm_one_Q_value_theorem_with_period156_context" in intake
        and "q_square_exact_fp_value" in intake
        and "coset_selector_or_Q_source_only" in intake
    )
    rubric_ok = (
        "norm_one_Q_value_theorem_with_period156_context" in rubric
        and "q_square_exact_fp_value" in rubric
        and "coset_selector_or_Q_source_only" in rubric
    )
    minimal_ok = (
        "compact_Q_route_has_period156_or_finite_Q3_theorem" in minimal
        and "Q_route_has_diagonal_split_or_direct_edge_after_value_data" in minimal
        and "Q_square_exact_value_requires_extraction_map_after_two_roots" in minimal
    )
    newly_promoted_prior_candidates = 0
    surviving_q_intake_families = 4
    current_q_source_hooks = 0
    current_source_stage_closers = 0
    current_extraction_ready = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 11
        and all(row.ok for row in rows)
        and q_support_route_live
        and selector_debt_ok
        and split_ok
        and quartic_ok
        and q_square_payload_bounded
        and source_ok
        and intake_ok
        and rubric_ok
        and minimal_ok
        and newly_promoted_prior_candidates == 0
        and surviving_q_intake_families == 4
        and current_q_source_hooks == 0
        and current_source_stage_closers == 0
        and current_extraction_ready == 0
        and current_submission_ready == 0
    )
    return QRouteCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_q_intake_families=surviving_q_intake_families,
        q_support_route_live=q_support_route_live,
        q_square_payload_bounded=q_square_payload_bounded,
        current_q_source_hooks=current_q_source_hooks,
        current_source_stage_closers=current_source_stage_closers,
        current_extraction_ready=current_extraction_ready,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 Q-route candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_q_intake_families={sweep.surviving_q_intake_families}")
    print(f"  q_support_route_live={int(sweep.q_support_route_live)}")
    print(f"  q_square_payload_bounded={int(sweep.q_square_payload_bounded)}")
    print(f"  current_q_source_hooks={sweep.current_q_source_hooks}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_extraction_ready={sweep.current_extraction_ready}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_q_route_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
