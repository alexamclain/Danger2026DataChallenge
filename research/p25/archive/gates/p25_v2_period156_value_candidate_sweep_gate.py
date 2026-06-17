#!/usr/bin/env python3
"""Sweep prior period-156 value-side artifacts under the p25 v2 intake."""

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
class Period156ValueCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_value_intake_families: int
    current_period156_value_theorems: int
    current_source_stage_closers: int
    current_submission_ready: int
    theta2_support_confirmed: bool
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
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
            "schertz_scholl_external_source_boundary",
            "research/p25/evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
            "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
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
            "degree6_value_descent_ambiguity",
            "research/p25/evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
            "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
        ),
        marker(
            "norm_only_descent_ambiguity",
            "research/p25/evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
            "p25_v2_norm_only_descent_ambiguity_rows=1/1",
        ),
        marker(
            "value_divisor_source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "source_action_registry",
            "research/p25/evidence/p25_v2_source_action_registry_20260616.md",
            "p25_v2_source_action_registry_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="canonical_h0_period156_value",
            prior_shape="canonical H0 value with Norm_156(Y_507) boundary and period-156 branch context",
            decision="live_value_route_not_prior_theorem",
            first_missing_or_falsifier="no current arithmetic source theorem emits this finite value",
            ok=True,
        ),
        SweepRow(
            name="y507_period156_value",
            prior_shape="Y_507 value theorem with period-156 context",
            decision="live_value_route_not_prior_theorem",
            first_missing_or_falsifier="no current arithmetic source theorem emits the p25 Y_507 value",
            ok=True,
        ),
        SweepRow(
            name="canonical_h0_divisor_additive",
            prior_shape="canonical H0 divisor/additive identity with boundary",
            decision="live_branch_free_route_not_prior_theorem",
            first_missing_or_falsifier="scalar-fixed finite divisor/additive identity still missing",
            ok=True,
        ),
        SweepRow(
            name="ambient780_or_mu11_value",
            prior_shape="ambient-period-780 value, eleventh power, or mu_11 quotient",
            decision="repair_period156_branch_selection_missing",
            first_missing_or_falsifier="ambient route leaves 11 F_p branches and does not select one value",
            ok=True,
        ),
        SweepRow(
            name="degree6_value_without_fp_descent",
            prior_shape="degree-6 primitive-root expression, value orbit, or norm without selected F_p row",
            decision="repair_fp_descent_and_row_selection_missing",
            first_missing_or_falsifier="needs descent to F_p plus selected legal support-156 row",
            ok=True,
        ),
        SweepRow(
            name="norm_only_or_boundary_only",
            prior_shape="Norm_156(Y_507), dense period norm value, or H90 boundary only",
            decision="repair_legal_h90_descent_and_finite_theorem_missing",
            first_missing_or_falsifier="boundary/norm data does not choose one legal preimage row",
            ok=True,
        ),
        SweepRow(
            name="schertz_shin_scholl_framework",
            prior_shape="ray-class generation, Siegel-Ramachandra generator, Kato-Siegel norm vocabulary",
            decision="support_source_not_period156_hook",
            first_missing_or_falsifier="exact p25 support-156 value/divisor theorem or theta2 payload missing",
            ok=True,
        ),
        SweepRow(
            name="theta2_factor_certificate",
            prior_shape="period-156 theta2/theta2-inverse finite support contract",
            decision="support_payload_not_arithmetic_producer",
            first_missing_or_falsifier="challenge-legal arithmetic identity emitting exact theta2 divisor/additive data missing",
            ok=True,
        ),
        SweepRow(
            name="sprang_d2_theta_support",
            prior_shape="D=2 Poincare/Kronecker/theta source machinery",
            decision="support_source_not_theta2_closer",
            first_missing_or_falsifier="p25 theta2 payload, bridge, and branch/telescoping data missing",
            ok=True,
        ),
        SweepRow(
            name="direct_order39_or_sqrt_minus39_shortcuts",
            prior_shape="direct F_p order-39 root or sqrt(-39) scalar shortcut",
            decision="reject_arithmetic_shortcut",
            first_missing_or_falsifier="ord_39(p)=6 and sqrt(-39) is not in F_p",
            ok=True,
        ),
    )


def build_sweep() -> Period156ValueCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    branch = read("research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md")
    hook = read("research/p25/evidence/p25_v2_period156_value_source_hook_20260616.md")
    h0_y507 = read("research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md")
    schertz = read("research/p25/evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md")
    theta2 = read("research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md")
    sprang = read("research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md")
    degree6 = read("research/p25/evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md")
    norm_only = read("research/p25/evidence/p25_v2_norm_only_descent_ambiguity_20260616.md")
    router = read("research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md")
    gap = read("research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md")
    registry = read("research/p25/evidence/p25_v2_source_action_registry_20260616.md")

    branch_ok = (
        "accepted_source_stage_shapes = 2" in branch
        and "current_source_stage_closers = 0" in branch
        and "gcd(4^780 - 1, p - 1) = 11" in branch
    )
    hook_ok = (
        "current_period156_value_theorems = 0" in hook
        and "accepted_routes = 2" in hook
    )
    h0_y507_ok = (
        "current period-156 value theorems = 0" in h0_y507
        and "period156_h0_y507_value_route_live_but_no_current_theorem" in h0_y507
    )
    schertz_ok = (
        "current_period156_value_theorems = 0" in schertz
        and "current_source_stage_closers = 0" in schertz
    )
    theta2_support_confirmed = (
        "current_arithmetic_producers = 0" in theta2
        and "source_stage_closers = 0" in theta2
        and "accepted_theta2_interfaces = 7" in theta2
    )
    sprang_ok = (
        "exact_theta2_payload_named = no" in sprang
        and "source_stage_closers = 0" in sprang
    )
    degree6_ok = (
        "current_source_stage_closers = 0" in degree6
        and "degree6_value_orbit_without_descent" in degree6
    )
    norm_ok = (
        "current_source_stage_closers = 0" in norm_only
        and "norm_plus_explicit_legal_h90_descent" in norm_only
    )
    router_ok = (
        "period156_value_route" in router
        and "direct_closer_rows = 0" in router
        and "broad_reading_allowed_rows = 0" in router
    )
    gap_ok = (
        "period156_value_theorems = 0" in gap
        and "first_pass_closers = 0" in gap
    )
    registry_ok = (
        "period156_h0_y507_value" in registry
        and "current_source_stage_closers = 0" in registry
    )
    newly_promoted_prior_candidates = 0
    surviving_value_intake_families = 3
    current_period156_value_theorems = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 10
        and all(row.ok for row in rows)
        and branch_ok
        and hook_ok
        and h0_y507_ok
        and schertz_ok
        and theta2_support_confirmed
        and sprang_ok
        and degree6_ok
        and norm_ok
        and router_ok
        and gap_ok
        and registry_ok
        and newly_promoted_prior_candidates == 0
        and surviving_value_intake_families == 3
        and current_period156_value_theorems == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return Period156ValueCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_value_intake_families=surviving_value_intake_families,
        current_period156_value_theorems=current_period156_value_theorems,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        theta2_support_confirmed=theta2_support_confirmed,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 period-156 value candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_value_intake_families={sweep.surviving_value_intake_families}")
    print(f"  theta2_support_confirmed={int(sweep.theta2_support_confirmed)}")
    print(f"  current_period156_value_theorems={sweep.current_period156_value_theorems}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_period156_value_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
