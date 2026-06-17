#!/usr/bin/env python3
"""Sweep prior exact-P artifacts under the p25 v2 heavy-route intake."""

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
class ExactPCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_exactp_intake_families: int
    finite_payload_rigid: bool
    exactp_to_unified_one_way: bool
    current_exactp_source_theorems: int
    current_source_stage_closers: int
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
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
        marker(
            "exactp_finite_geometry_rigidity",
            "research/p25/evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
            "p25_v2_exactp_finite_geometry_rigidity_rows=1/1",
        ),
        marker(
            "exactp_to_unified_target_spine",
            "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
            "p25_v2_exactp_to_unified_target_spine_rows=1/1",
        ),
        marker(
            "reverse_exactp_information_loss",
            "research/p25/evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
            "p25_v2_reverse_exactp_information_loss_rows=1/1",
        ),
        marker(
            "exactp_closure_template_replay_boundary",
            "research/p25/evidence/p25_v2_exactp_closure_template_replay_boundary_20260616.md",
            "p25_v2_exactp_closure_template_replay_boundary_rows=1/1",
        ),
        marker(
            "ksy_source_ingest_scan",
            "research/p25/evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md",
            "decision = continue_as_exactp_vocabulary_not_closer",
        ),
        marker(
            "kubert_lang_selector_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
            "p25_v2_kubert_lang_selector_boundary_rows=1/1",
        ),
        marker(
            "kubert_lang_external_source_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
            "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
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
        marker(
            "value_payload_reality_ledger",
            "research/p25/evidence/p25_v2_value_payload_reality_ledger_20260616.md",
            "p25_v2_value_payload_reality_ledger_rows=1/1",
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
            name="ksy_normalized_y_surface",
            prior_shape="normalized-y torsion/ray-class atom vocabulary on the KSY surface",
            decision="exactp_vocabulary_not_source_theorem",
            first_missing_or_falsifier="exact equal-weight 75-atom selector/product theorem missing",
            ok=True,
        ),
        SweepRow(
            name="finite_75_atom_payload",
            prior_shape="disjoint four-cell supports, forced equal weights, and compact theta2 footprint",
            decision="rigid_finite_payload_not_arithmetic_producer",
            first_missing_or_falsifier="challenge-legal arithmetic theorem selecting the payload missing",
            ok=True,
        ),
        SweepRow(
            name="compact_cdk_orientation",
            prior_shape="C=(47,28), D=(22,3), primitive K=(57,0), orientation",
            decision="accepted_hook_not_prior_theorem",
            first_missing_or_falsifier="no source theorem emits one accepted raw branch with finite identity data",
            ok=True,
        ),
        SweepRow(
            name="branchless_orientation_word",
            prior_shape="C,D,K,orientation stated without one of the four raw branches",
            decision="repair_exactp_orientation_branch_missing",
            first_missing_or_falsifier="must choose forward/reverse branch and theta2/theta2-inverse output",
            ok=True,
        ),
        SweepRow(
            name="kubert_lang_exponent_and_primitive_word",
            prior_shape="KL congruence screen plus primitive word z^121*(1+z+z^2)*(1-z^263)",
            decision="finite_selector_boundary_not_source_closer",
            first_missing_or_falsifier="theorem-legal mixed C3 x C169 selector or primitive-word identity missing",
            ok=True,
        ),
        SweepRow(
            name="theta2_period156_support",
            prior_shape="period-156 theta2/theta2-inverse divisor support and accepted finite interfaces",
            decision="support_payload_not_arithmetic_producer",
            first_missing_or_falsifier="exact theta2/theta2-inverse divisor-additive source theorem missing",
            ok=True,
        ),
        SweepRow(
            name="sprang_d2_support",
            prior_shape="D=2 Poincare/Kronecker/theta machinery and distribution vocabulary",
            decision="support_source_not_theta2_closer",
            first_missing_or_falsifier="sparse p25 theta2 payload, selector, bridge, and branch data missing",
            ok=True,
        ),
        SweepRow(
            name="unified_target_theorem_as_exactp_recovery",
            prior_shape="H0/conductor-39 support-156 theorem treated as reverse exact-P recovery",
            decision="repair_reverse_selector_structure_missing",
            first_missing_or_falsifier="reverse reconstruction to C,D,K,orientation or 75 atoms is not proved",
            ok=True,
        ),
        SweepRow(
            name="period156_value_side_bridge",
            prior_shape="H0/Y507 value theorem or theta2 value without full exact-P selector",
            decision="value_route_may_feed_extraction_not_exactp_close",
            first_missing_or_falsifier="exact-P selector or explicit reverse reconstruction missing",
            ok=True,
        ),
        SweepRow(
            name="finite_packet_without_source",
            prior_shape="local fixture, packet, product, or value payload only",
            decision="repair_arithmetic_source_missing",
            first_missing_or_falsifier="finite payloads are targets and evidence, not source theorems",
            ok=True,
        ),
    )


def build_sweep() -> ExactPCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    minimal = read("research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md")
    orientation = read("research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md")
    finite = read("research/p25/evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md")
    spine = read("research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md")
    reverse = read("research/p25/evidence/p25_v2_reverse_exactp_information_loss_20260616.md")
    ksy = read("research/p25/evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md")
    kl = read("research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md")
    kl_ext = read("research/p25/evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md")
    theta2 = read("research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md")
    sprang = read("research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md")
    constructive = read("research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md")
    ledger = read("research/p25/evidence/p25_v2_value_payload_reality_ledger_20260616.md")
    family = read("research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md")
    registry = read("research/p25/evidence/p25_v2_source_action_registry_20260616.md")

    minimal_ok = (
        "current_exactp_source_theorems = 0" in minimal
        and "accepted_routes = 5" in minimal
        and "repair_or_reject_routes = 11" in minimal
    )
    orientation_ok = (
        "accepted_orientation_branches = 4" in orientation
        and "current_exactp_source_theorems = 0" in orientation
    )
    finite_payload_rigid = (
        "atom_count = 75" in finite
        and "linear_nullity_from_disjoint_support = 0" in finite
        and "theta2_inverse_solution = all 75 weights +1" in finite
        and "theta2_solution = all 75 weights -1" in finite
    )
    exactp_to_unified_one_way = (
        "exact-P theorem hit -> unified H0/conductor-39 target" in spine
        and "unified target theorem hit -> exact-P theorem hit is not proved" in spine
        and "reverse_unified_to_exactp = rejected without extra selector structure" in reverse
    )
    ksy_ok = (
        "decision = continue_as_exactp_vocabulary_not_closer" in ksy
        and "missing  = exact 75-atom selector, mixed graph, orientation, period-156 bridge" in ksy
    )
    kl_ok = (
        "finite_selector_rigid_but_kl_source_theorem_missing" in kl
        and "current_kl_source_theorems = 0" in kl_ext
    )
    theta2_ok = (
        "accepted_theta2_interfaces = 7" in theta2
        and "current_arithmetic_producers = 0" in theta2
        and "source_stage_closers = 0" in theta2
    )
    sprang_ok = (
        "exact_theta2_payload_named = no" in sprang
        and "source_stage_closers = 0" in sprang
    )
    constructive_ok = (
        "packetizable_source_payloads = 0" in constructive
        and "source_stage_closers = 0" in constructive
    )
    ledger_ok = (
        "current_source_theorem_rows = 0" in ledger
        and "current_submission_ready_rows = 0" in ledger
    )
    family_registry_ok = (
        "exactp_upstream_theorems = 0" in family
        and "current_source_stage_closers = 0" in registry
    )
    newly_promoted_prior_candidates = 0
    surviving_exactp_intake_families = 4
    current_exactp_source_theorems = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 10
        and all(row.ok for row in rows)
        and minimal_ok
        and orientation_ok
        and finite_payload_rigid
        and exactp_to_unified_one_way
        and ksy_ok
        and kl_ok
        and theta2_ok
        and sprang_ok
        and constructive_ok
        and ledger_ok
        and family_registry_ok
        and newly_promoted_prior_candidates == 0
        and surviving_exactp_intake_families == 4
        and current_exactp_source_theorems == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return ExactPCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_exactp_intake_families=surviving_exactp_intake_families,
        finite_payload_rigid=finite_payload_rigid,
        exactp_to_unified_one_way=exactp_to_unified_one_way,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 exact-P candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_exactp_intake_families={sweep.surviving_exactp_intake_families}")
    print(f"  finite_payload_rigid={int(sweep.finite_payload_rigid)}")
    print(f"  exactp_to_unified_one_way={int(sweep.exactp_to_unified_one_way)}")
    print(f"  current_exactp_source_theorems={sweep.current_exactp_source_theorems}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_exactp_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
