#!/usr/bin/env python3
"""End-to-end route audit for the external p25 KSY-y moonshot ladder.

The external moonshot ladder now has executable checkpoints from source
front doors through the final pre-verifier extraction payloads.  This gate
composes those checkpoints into one first-missing audit, without reclassifying
the underlying mathematics or treating hypothetical boundary rows as current
evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_bridge_resolution_queue_gate import (
    profile_external_bridge_resolution_queue,
)
from p25_ksy_y_external_drew_policy_answer_router_gate import (
    profile_external_drew_policy_answer_router,
)
from p25_ksy_y_external_halving_extraction_work_order_gate import (
    profile_external_halving_extraction_work_order,
)
from p25_ksy_y_external_post_source_danger3_handoff_gate import (
    profile_external_post_source_danger3_handoff,
)
from p25_ksy_y_external_x16_specialization_work_order_gate import (
    profile_external_x16_specialization_work_order,
)
from p25_ksy_y_external_x18112_bridge_answer_router_gate import (
    profile_external_x18112_bridge_answer_router,
)
from p25_ksy_y_official_vpp_submission_archive_contract_gate import (
    profile_vpp_submission_archive_contract,
)


RESEARCH = Path("research/p25")
P25 = 10**25 + 13
ACTIVE_MODE = "x16halvenonsplit"
START_DEPTH = 4
FINAL_DEPTH = 42
HALVING_LINKS = FINAL_DEPTH - START_DEPTH

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_bridge_resolution_queue_20260614.md",
        "ksy_y_external_bridge_resolution_queue_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_post_source_danger3_handoff_20260614.md",
        "ksy_y_external_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_drew_policy_answer_router_20260614.md",
        "ksy_y_external_drew_policy_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_x18112_bridge_answer_router_20260614.md",
        "ksy_y_external_x18112_bridge_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_x16_specialization_work_order_20260614.md",
        "ksy_y_external_x16_specialization_work_order_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_halving_extraction_work_order_20260614.md",
        "ksy_y_external_halving_extraction_work_order_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_official_vpp_submission_archive_contract_20260614.md",
        "ksy_y_official_vpp_submission_archive_contract_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalEndToEndRouteAuditRow:
    name: str
    route_family: str
    decision: str
    support_rows: int
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
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class ExternalEndToEndRouteAudit:
    dependency_markers_present: int
    dependency_markers_total: int
    p: int
    active_mode: str
    start_depth: int
    final_depth: int
    halving_links: int
    external_resolution_ok: bool
    post_source_handoff_ok: bool
    drew_policy_answer_ok: bool
    bridge_answer_router_ok: bool
    x16_specialization_work_order_ok: bool
    halving_extraction_work_order_ok: bool
    vpp_archive_contract_ok: bool
    rows: tuple[ExternalEndToEndRouteAuditRow, ...]
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
    active_frontdoor_rows: int
    policy_unblock_answer_rows: int
    bridge_answer_rows: int
    x16_surface_variant_rows: int
    extraction_payload_rows: int
    shortcut_kill_support_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def route_rows(
    *,
    active_frontdoors: int,
    source_policy_missing: int,
    policy_unblocks: int,
    bridge_answers: int,
    x16_variants: int,
    extraction_payloads: int,
    shortcut_kills: int,
) -> tuple[ExternalEndToEndRouteAuditRow, ...]:
    return (
        ExternalEndToEndRouteAuditRow(
            name="current_external_source_theorem_missing",
            route_family="current",
            decision="current_first_missing_external_source_theorem",
            support_rows=active_frontdoors,
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
            first_missing_or_falsifier=(
                "one source-stage theorem for H0, conductor-39, twisted/H90, "
                "curved-corner, or exact-P"
            ),
            next_action="continue targeted source theorem / expert / literature work while the fleet runs",
            ok=active_frontdoors == 5,
        ),
        ExternalEndToEndRouteAuditRow(
            name="source_yes_policy_missing",
            route_family="external_moonshot",
            decision="source_theorem_closed_policy_or_framing_missing",
            support_rows=source_policy_missing,
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
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing or Drew policy yes",
            next_action="route the source theorem through the external Drew policy/framing answer packet",
            ok=source_policy_missing == 5,
        ),
        ExternalEndToEndRouteAuditRow(
            name="shortcut_controls_killed",
            route_family="external_guardrail",
            decision="reject_shortcuts_without_finite_identity_same_j_or_odd_payload",
            support_rows=shortcut_kills,
            current_evidence=False,
            source_theorem_closed=False,
            danger3_unblocked=False,
            same_j_bridge=False,
            x16_surface=False,
            extraction_ready=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            rejected_or_kill=True,
            first_missing_or_falsifier=(
                "explicit p-specialized finite identity, same-j gluing, and p25 odd payload"
            ),
            next_action="kill or rewrite generic CM, unglued level data, and generic X_1(16) shortcuts",
            ok=shortcut_kills == 3,
        ),
        ExternalEndToEndRouteAuditRow(
            name="policy_yes_no_same_j_bridge",
            route_family="external_moonshot",
            decision="danger3_unblocked_cross_level_bridge_missing",
            support_rows=policy_unblocks,
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
            first_missing_or_falsifier="same-j X_1(8112) bridge for the accepted odd target",
            next_action="prove same-curve P16/odd-target gluing or an exact order-8112 generator",
            ok=policy_unblocks == 3,
        ),
        ExternalEndToEndRouteAuditRow(
            name="bridge_yes_no_x16_specialization",
            route_family="external_moonshot",
            decision="cross_level_target_identified_specialization_missing",
            support_rows=bridge_answers,
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
            first_missing_or_falsifier="production X_1(16) y/model-root/A,xP16 payload",
            next_action="specialize the bridge to active x16halvenonsplit Montgomery chart data",
            ok=bridge_answers == 5,
        ),
        ExternalEndToEndRouteAuditRow(
            name="x16_surface_no_extraction_payload",
            route_family="external_moonshot",
            decision="active_surface_reached_halving_missing",
            support_rows=x16_variants,
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
            first_missing_or_falsifier="38-link halving x-chain, active sqrt witnesses, or direct A,x0",
            next_action="derive x_4..x_42, active-path witnesses, or direct concrete A,x0",
            ok=x16_variants == 10,
        ),
        ExternalEndToEndRouteAuditRow(
            name="extraction_payload_no_vpp",
            route_family="external_moonshot",
            decision="extraction_ready_vpp_missing",
            support_rows=extraction_payloads,
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
            first_missing_or_falsifier="official DANGER3 vpp.py stdout True",
            next_action="run official vpp.py on the concrete p25 A,x0 payload and reject if not True",
            ok=extraction_payloads == 30,
        ),
        ExternalEndToEndRouteAuditRow(
            name="vpp_true_archive_incomplete",
            route_family="external_moonshot",
            decision="official_vpp_true_archive_missing",
            support_rows=1,
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
            first_missing_or_falsifier="archive command/logs/environment/triple/Lean bundle",
            next_action="complete the official submission archive contract before calling victory",
            ok=True,
        ),
        ExternalEndToEndRouteAuditRow(
            name="complete_archive_boundary",
            route_family="boundary",
            decision="submission_archive_complete",
            support_rows=1,
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
            first_missing_or_falsifier="none",
            next_action="submit/report the p25 triple and preserve the archive bundle",
            ok=True,
        ),
    )


def profile_external_end_to_end_route_audit() -> ExternalEndToEndRouteAudit:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    resolution = profile_external_bridge_resolution_queue()
    post_source = profile_external_post_source_danger3_handoff()
    drew = profile_external_drew_policy_answer_router()
    bridge = profile_external_x18112_bridge_answer_router()
    x16 = profile_external_x16_specialization_work_order()
    halving = profile_external_halving_extraction_work_order()
    archive = profile_vpp_submission_archive_contract()
    shortcut_kills = drew.rejected_rows + bridge.kill_rows
    rows = route_rows(
        active_frontdoors=resolution.active_frontdoor_rows,
        source_policy_missing=post_source.policy_or_framing_missing_rows,
        policy_unblocks=drew.policy_unblocks_rows,
        bridge_answers=bridge.continue_to_x16_rows,
        x16_variants=x16.active_surface_rows,
        extraction_payloads=halving.extraction_ready_rows,
        shortcut_kills=shortcut_kills,
    )
    current = sum(row.current_evidence for row in rows)
    source = sum(row.source_theorem_closed for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    same_j = sum(row.same_j_bridge for row in rows)
    x16_surface = sum(row.x16_surface for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    vpp = sum(row.official_vpp_verified for row in rows)
    archive_complete = sum(row.archive_complete for row in rows)
    submission = sum(row.submission_ready for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.rejected_or_kill for row in rows)
    decisions = tuple(row.decision for row in rows)
    expected_decisions = (
        "current_first_missing_external_source_theorem",
        "source_theorem_closed_policy_or_framing_missing",
        "reject_shortcuts_without_finite_identity_same_j_or_odd_payload",
        "danger3_unblocked_cross_level_bridge_missing",
        "cross_level_target_identified_specialization_missing",
        "active_surface_reached_halving_missing",
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
        and resolution.row_ok
        and resolution.active_frontdoor_rows == 5
        and resolution.direct_closing_rows == 0
        and post_source.row_ok
        and post_source.external_source_yes_rows == 5
        and post_source.current_submission_ready_rows == 0
        and drew.row_ok
        and drew.policy_unblocks_rows == 3
        and bridge.row_ok
        and bridge.continue_to_x16_rows == 5
        and bridge.current_submission_ready_rows == 0
        and x16.row_ok
        and x16.frontdoor_count == 5
        and x16.active_surface_rows == 10
        and halving.row_ok
        and halving.frontdoor_count == 5
        and halving.extraction_ready_rows == 30
        and archive.row_ok
        and archive.current_submission_ready_rows == 0
        and len(rows) == 9
        and current == 1
        and source == 7
        and danger3 == 6
        and same_j == 5
        and x16_surface == 4
        and extraction == 3
        and vpp == 2
        and archive_complete == 1
        and submission == 1
        and current_submission == 0
        and rejected == 1
        and shortcut_kills == 3
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalEndToEndRouteAudit(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        p=P25,
        active_mode=ACTIVE_MODE,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        external_resolution_ok=resolution.row_ok,
        post_source_handoff_ok=post_source.row_ok,
        drew_policy_answer_ok=drew.row_ok,
        bridge_answer_router_ok=bridge.row_ok,
        x16_specialization_work_order_ok=x16.row_ok,
        halving_extraction_work_order_ok=halving.row_ok,
        vpp_archive_contract_ok=archive.row_ok,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        source_closed_rows=source,
        danger3_unblocked_rows=danger3,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction,
        official_vpp_verified_rows=vpp,
        archive_complete_rows=archive_complete,
        submission_ready_rows=submission,
        current_submission_ready_rows=current_submission,
        rejected_or_kill_rows=rejected,
        active_frontdoor_rows=resolution.active_frontdoor_rows,
        policy_unblock_answer_rows=drew.policy_unblocks_rows,
        bridge_answer_rows=bridge.continue_to_x16_rows,
        x16_surface_variant_rows=x16.active_surface_rows,
        extraction_payload_rows=halving.extraction_ready_rows,
        shortcut_kill_support_rows=shortcut_kills,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_end_to_end_route_audit()
    print("p25 KSY-y external end-to-end route audit gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_resolution_ok={int(profile.external_resolution_ok)}")
    print(f"  post_source_handoff_ok={int(profile.post_source_handoff_ok)}")
    print(f"  drew_policy_answer_ok={int(profile.drew_policy_answer_ok)}")
    print(f"  bridge_answer_router_ok={int(profile.bridge_answer_router_ok)}")
    print(f"  x16_specialization_work_order_ok={int(profile.x16_specialization_work_order_ok)}")
    print(f"  halving_extraction_work_order_ok={int(profile.halving_extraction_work_order_ok)}")
    print(f"  vpp_archive_contract_ok={int(profile.vpp_archive_contract_ok)}")
    print("route")
    print(f"  p={profile.p}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print("audit_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: family={row.route_family} decision={row.decision} "
            f"support={row.support_rows} current={int(row.current_evidence)} "
            f"source={int(row.source_theorem_closed)} "
            f"danger3={int(row.danger3_unblocked)} "
            f"same_j={int(row.same_j_bridge)} x16={int(row.x16_surface)} "
            f"extract={int(row.extraction_ready)} vpp={int(row.official_vpp_verified)} "
            f"archive={int(row.archive_complete)} submission={int(row.submission_ready)} "
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
    print("support_counts")
    print(f"  active_frontdoor_rows={profile.active_frontdoor_rows}")
    print(f"  policy_unblock_answer_rows={profile.policy_unblock_answer_rows}")
    print(f"  bridge_answer_rows={profile.bridge_answer_rows}")
    print(f"  x16_surface_variant_rows={profile.x16_surface_variant_rows}")
    print(f"  extraction_payload_rows={profile.extraction_payload_rows}")
    print(f"  shortcut_kill_support_rows={profile.shortcut_kill_support_rows}")
    print("interpretation")
    print("  external_ladder_is_continuous_from_source_frontdoor_to_archive_boundary=1")
    print("  current_first_missing_external_source_theorem_remains=1")
    print("  bridge_X16_halving_payload_counts_are_propagated=1")
    print("  current_submission_ready_rows_remain_zero=1")
    print(
        "ksy_y_external_end_to_end_route_audit_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external end-to-end route audit regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
