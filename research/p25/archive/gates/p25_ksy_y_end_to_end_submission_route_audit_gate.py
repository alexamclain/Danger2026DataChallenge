#!/usr/bin/env python3
"""End-to-end submission-route audit for the p25 KSY-y moonshot.

This gate is intentionally a compact composition layer.  It does not re-run
the entire source/bridge/extraction stack; it requires the recorded markers
for the already-audited layers, then records the first missing item at each
hypothetical state between the current evidence and a submission bundle.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")
P25 = 10**25 + 13
ACTIVE_MODE = "x16halvenonsplit"
START_DEPTH = 4
FINAL_DEPTH = 42
HALVING_LINKS = FINAL_DEPTH - START_DEPTH

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_value_payload_reality_check_20260614.md",
        "ksy_y_value_payload_reality_check_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_source_theorem_priority_selector_20260614.md",
        "ksy_y_source_theorem_priority_selector_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_source_answer_router_20260614.md",
        "ksy_y_priority1_source_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_post_source_danger3_handoff_20260614.md",
        "ksy_y_priority1_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_drew_policy_answer_router_20260614.md",
        "ksy_y_drew_policy_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_policy_x18112_work_order_20260614.md",
        "ksy_y_post_policy_x18112_work_order_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x18112_bridge_claim_packet_fixture_export_20260614.md",
        "ksy_y_x18112_bridge_claim_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_post_bridge_x16_surface_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_surface_halving_vpp_intake_20260614.md",
        "ksy_y_post_surface_halving_vpp_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_official_vpp_submission_archive_contract_20260614.md",
        "ksy_y_official_vpp_submission_archive_contract_rows=1/1",
    ),
)


@dataclass(frozen=True)
class SubmissionRouteAuditRow:
    name: str
    route_family: str
    decision: str
    current_evidence: bool
    source_theorem_closed: bool
    danger3_unblocked: bool
    same_j_bridge: bool
    x16_surface: bool
    extraction_ready: bool
    official_vpp_verified: bool
    archive_complete: bool
    submission_ready: bool
    current_submission_ready: bool
    rejected_or_kill: bool
    practical_bypass: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class SubmissionRouteAuditProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    p: int
    active_mode: str
    start_depth: int
    final_depth: int
    halving_links: int
    rows: tuple[SubmissionRouteAuditRow, ...]
    row_count: int
    current_evidence_rows: int
    source_closed_rows: int
    danger3_unblocked_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    official_vpp_verified_rows: int
    archive_complete_rows: int
    submission_ready_rows: int
    current_submission_ready_rows: int
    rejected_or_kill_rows: int
    practical_bypass_rows: int
    archive_incomplete_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def route_rows() -> tuple[SubmissionRouteAuditRow, ...]:
    return (
        SubmissionRouteAuditRow(
            name="current_state_no_source_theorem",
            route_family="current",
            decision="current_first_missing_priority1_source_theorem",
            current_evidence=True,
            source_theorem_closed=False,
            danger3_unblocked=False,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier=(
                "exact priority-1 value/divisor source theorem: exact P, "
                "H0/Y507, H0 translate, or twisted/H90 period-156 payload"
            ),
            next_action="continue source-theorem/literature/expert intake; keep production fleet running",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="practical_vpp_hit_archive_missing",
            route_family="production_bypass",
            decision="official_vpp_true_archive_missing",
            current_evidence=False,
            source_theorem_closed=False,
            danger3_unblocked=False,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=True,
            official_vpp_verified=True,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=True,
            first_missing_or_falsifier="archive command/logs/environment/triple/Lean bundle",
            next_action="if fleet finds A,x0 and official vpp.py is True, bypass moonshot proof work and archive immediately",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="source_yes_no_policy",
            route_family="moonshot",
            decision="source_theorem_closed_policy_or_framing_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=False,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing or Drew policy yes",
            next_action="route the theorem through the finite-identity policy/framing router",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="generic_cm_rewrite_or_kill",
            route_family="moonshot_rewrite",
            decision="reject_generic_cm_generation_not_framing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=False,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=True,
            practical_bypass=False,
            first_missing_or_falsifier="explicit p-specialized finite-field identity",
            next_action="rewrite generic CM/class-field provenance as a finite identity for this p or kill the route",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="policy_yes_no_bridge",
            route_family="moonshot",
            decision="danger3_unblocked_cross_level_bridge_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="same-j X_1(8112) bridge tied to the odd KSY/Yang/H90 target",
            next_action="prove same-curve P16/Q507 data or exact order-8112 generator bridge",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="bridge_yes_no_x16",
            route_family="moonshot",
            decision="cross_level_target_identified_specialization_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=True,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="practical X_1(16) y/x chart or direct A,xP16 payload",
            next_action="specialize the bridge to the active x16halvenonsplit Montgomery surface",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="x16_surface_no_x0",
            route_family="moonshot",
            decision="x16_surface_reached_halving_or_vpp_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=True,
            x16_surface=True,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="full 38-link halving chain from depth 4 to x0, or direct A,x0",
            next_action="derive x-chain/x0 and then run official vpp.py",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="x0_no_vpp",
            route_family="moonshot",
            decision="extraction_ready_vpp_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=True,
            x16_surface=True,
            extraction_ready=True,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="official DANGER3 vpp.py stdout True on concrete p,A,x0",
            next_action="run official vpp.py immediately; reject if it is not True",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="vpp_true_archive_incomplete",
            route_family="moonshot",
            decision="official_vpp_true_archive_missing",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=True,
            x16_surface=True,
            extraction_ready=True,
            official_vpp_verified=True,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="archive command/logs/environment/triple/Lean bundle",
            next_action="complete the official submission archive contract before calling victory",
            ok=True,
        ),
        SubmissionRouteAuditRow(
            name="complete_archive_boundary",
            route_family="boundary",
            decision="submission_archive_complete",
            current_evidence=False,
            source_theorem_closed=True,
            danger3_unblocked=True,
            same_j_bridge=True,
            x16_surface=True,
            extraction_ready=True,
            official_vpp_verified=True,
            archive_complete=True,
            submission_ready=True,
            current_submission_ready=False,
            rejected_or_kill=False,
            practical_bypass=False,
            first_missing_or_falsifier="none",
            next_action="submit/report the p25 triple and preserve the archive bundle",
            ok=True,
        ),
    )


def profile_end_to_end_submission_route_audit() -> SubmissionRouteAuditProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = route_rows()
    current = sum(row.current_evidence for row in rows)
    source = sum(row.source_theorem_closed for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    bridge = sum(row.same_j_bridge for row in rows)
    x16 = sum(row.x16_surface for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    vpp = sum(row.official_vpp_verified for row in rows)
    archive = sum(row.archive_complete for row in rows)
    submission = sum(row.submission_ready for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.rejected_or_kill for row in rows)
    bypass = sum(row.practical_bypass for row in rows)
    archive_incomplete = sum(row.official_vpp_verified and not row.archive_complete for row in rows)
    decisions = tuple(row.decision for row in rows)
    expected = (
        "current_first_missing_priority1_source_theorem",
        "official_vpp_true_archive_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "reject_generic_cm_generation_not_framing",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "official_vpp_true_archive_missing",
        "submission_archive_complete",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and P25 == 10**25 + 13
        and ACTIVE_MODE == "x16halvenonsplit"
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and HALVING_LINKS == 38
        and len(rows) == 10
        and current == 1
        and source == 8
        and danger3 == 6
        and bridge == 5
        and x16 == 4
        and extraction == 4
        and vpp == 3
        and archive == 1
        and submission == 1
        and current_submission == 0
        and rejected == 1
        and bypass == 1
        and archive_incomplete == 2
        and decisions == expected
        and all(row.ok for row in rows)
    )
    return SubmissionRouteAuditProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        p=P25,
        active_mode=ACTIVE_MODE,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        source_closed_rows=source,
        danger3_unblocked_rows=danger3,
        same_j_bridge_rows=bridge,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        official_vpp_verified_rows=vpp,
        archive_complete_rows=archive,
        submission_ready_rows=submission,
        current_submission_ready_rows=current_submission,
        rejected_or_kill_rows=rejected,
        practical_bypass_rows=bypass,
        archive_incomplete_rows=archive_incomplete,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_end_to_end_submission_route_audit()
    print("p25 KSY-y end-to-end submission-route audit gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("invariants")
    print(f"  p={profile.p}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print("route_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: family={row.route_family} decision={row.decision} "
            f"current={int(row.current_evidence)} "
            f"source={int(row.source_theorem_closed)} "
            f"danger3={int(row.danger3_unblocked)} "
            f"bridge={int(row.same_j_bridge)} "
            f"x16={int(row.x16_surface)} "
            f"extract={int(row.extraction_ready)} "
            f"vpp={int(row.official_vpp_verified)} "
            f"archive={int(row.archive_complete)} "
            f"submission={int(row.submission_ready)} "
            f"bypass={int(row.practical_bypass)} "
            f"kill={int(row.rejected_or_kill)}"
        )
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  source_closed_rows={profile.source_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  official_vpp_verified_rows={profile.official_vpp_verified_rows}")
    print(f"  archive_complete_rows={profile.archive_complete_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print(f"  rejected_or_kill_rows={profile.rejected_or_kill_rows}")
    print(f"  practical_bypass_rows={profile.practical_bypass_rows}")
    print(f"  archive_incomplete_rows={profile.archive_incomplete_rows}")
    print("interpretation")
    print("  current_first_missing_item_is_priority1_source_theorem=1")
    print("  production_vpp_hit_bypasses_source_theorem_but_not_archive=1")
    print("  moonshot_route_next_gates_are_policy_bridge_x16_halving_vpp_archive=1")
    print("  current_submission_ready_rows_remain_zero=1")
    print(f"ksy_y_end_to_end_submission_route_audit_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("end-to-end submission-route audit regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
