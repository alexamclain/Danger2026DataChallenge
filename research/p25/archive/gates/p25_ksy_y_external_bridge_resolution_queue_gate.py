#!/usr/bin/env python3
"""Current external source/bridge resolution queue for the p25 KSY-y moonshot.

Older external scouting left a few named source hits to resolve.  Those are now
closed as context-only.  The live external queue is broader: five front-door
source families can close the source stage, and each must then enter the same
DANGER3 policy plus same-j X_1(8112) bridge ladder.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_frontdoor_answer_router_gate import (
    profile_external_frontdoor_answer_router,
)
from p25_ksy_y_external_post_policy_x18112_work_order_gate import (
    profile_external_post_policy_x18112_work_order,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    profile_x1_8112_bridge_theorem_intake,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_answer_router_20260614.md",
        "ksy_y_external_frontdoor_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_post_policy_x18112_work_order_20260614.md",
        "ksy_y_external_post_policy_x18112_work_order_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_20260614.md",
        "ksy_y_x1_8112_bridge_theorem_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_20260614.md",
        "ksy_y_koo_shin_2010_theorem52_actual_verdict_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalBridgeResolutionRow:
    name: str
    lane: str
    prior_artifact: Path
    resolution_artifact: Path
    resolution_status: str
    source_frontdoor_active: bool
    post_policy_bridge_active: bool
    killed_as_direct_closer: bool
    context_only: bool
    exact75: bool
    curved_corner: bool
    accepted_odd_target: str
    first_acceptable_upgrade: str
    first_bridge_ask: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ExternalBridgeResolutionQueue:
    dependency_markers_present: int
    dependency_markers_total: int
    external_frontdoor_answer_ok: bool
    external_post_policy_ok: bool
    x18112_intake_ok: bool
    rows: tuple[ExternalBridgeResolutionRow, ...]
    row_count: int
    resolved_source_rows: int
    killed_direct_rows: int
    context_only_rows: int
    active_frontdoor_rows: int
    active_post_policy_bridge_rows: int
    exact75_rows: int
    curved_corner_rows: int
    stale_access_blocked_rows: int
    direct_closing_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def resolved_row(
    *,
    name: str,
    lane: str,
    prior_artifact: Path,
    resolution_artifact: Path,
    resolution_status: str,
    first_acceptable_upgrade: str,
    first_falsifier: str,
) -> ExternalBridgeResolutionRow:
    return ExternalBridgeResolutionRow(
        name=name,
        lane=lane,
        prior_artifact=prior_artifact,
        resolution_artifact=resolution_artifact,
        resolution_status=resolution_status,
        source_frontdoor_active=False,
        post_policy_bridge_active=False,
        killed_as_direct_closer=True,
        context_only=True,
        exact75=False,
        curved_corner=False,
        accepted_odd_target="none",
        first_acceptable_upgrade=first_acceptable_upgrade,
        first_bridge_ask="not active; context only",
        first_falsifier=first_falsifier,
        ok=True,
    )


def active_row(
    *,
    name: str,
    lane: str,
    accepted_odd_target: str,
    first_acceptable_upgrade: str,
    first_bridge_ask: str,
    first_falsifier: str,
    exact75: bool = False,
    curved_corner: bool = False,
) -> ExternalBridgeResolutionRow:
    frontdoor = RESEARCH / "p25_ksy_y_external_frontdoor_answer_router_20260614.md"
    post_policy = RESEARCH / "p25_ksy_y_external_post_policy_x18112_work_order_20260614.md"
    return ExternalBridgeResolutionRow(
        name=name,
        lane=lane,
        prior_artifact=frontdoor,
        resolution_artifact=post_policy,
        resolution_status="active_frontdoor_source_yes_then_policy_and_bridge",
        source_frontdoor_active=True,
        post_policy_bridge_active=True,
        killed_as_direct_closer=False,
        context_only=False,
        exact75=exact75,
        curved_corner=curved_corner,
        accepted_odd_target=accepted_odd_target,
        first_acceptable_upgrade=first_acceptable_upgrade,
        first_bridge_ask=first_bridge_ask,
        first_falsifier=first_falsifier,
        ok=True,
    )


def resolution_rows() -> tuple[ExternalBridgeResolutionRow, ...]:
    external_scout = RESEARCH / "p25_ksy_y_external_exact_product_bridge_scout_20260613.md"
    koo_shin_verdict = RESEARCH / "p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_20260614.md"
    primary_verdict = RESEARCH / "p25_ksy_y_priority1_primary_source_verdict_20260613.md"
    return (
        resolved_row(
            name="koo_shin_2010_pdf_candidate_resolved",
            lane="Koo-Shin 2010",
            prior_artifact=external_scout,
            resolution_artifact=koo_shin_verdict,
            resolution_status="pdf_retrieved_theorem52_reject_prime_power_only_missing_mixed_lift",
            first_acceptable_upgrade="mixed-level theorem preserving the C3 row graph and T=(2,113) edge",
            first_falsifier="prime-level or C169 projection product without the mixed lift",
        ),
        resolved_row(
            name="bannai_kobayashi_distribution_ancestor",
            lane="Bannai-Kobayashi distribution",
            prior_artifact=external_scout,
            resolution_artifact=primary_verdict,
            resolution_status="verified_additive_theta_distribution_not_product_bridge",
            first_acceptable_upgrade="specialization to the exact K-traced normalized-y product P",
            first_falsifier="additive Kronecker theta distribution without finite multiplicative P",
        ),
        resolved_row(
            name="scholl_kato_siegel_odd_d_control",
            lane="Scholl/Kato-Siegel odd-D control",
            prior_artifact=external_scout,
            resolution_artifact=primary_verdict,
            resolution_status="verified_multiplicative_distribution_but_D2_ineligible",
            first_acceptable_upgrade="even-D or normalized-y theorem avoiding the (6,D)=1 obstruction",
            first_falsifier="odd-D Kato-Siegel norm relation imported directly into the D=2 target",
        ),
        active_row(
            name="active_h0_divisor_boundary_identity",
            lane="H0/Yang/Kubert-Lang",
            accepted_odd_target="canonical_H0/H0_translate/Y_507",
            first_acceptable_upgrade=(
                "exact legal H0 divisor/additive identity with Hilbert-90 boundary to Norm_156(Y_507)"
            ),
            first_bridge_ask=(
                "same-j X_1(8112) bridge tying the H0/Y_507 odd target to production X_1(16)"
            ),
            first_falsifier="H0 theorem missing the Hilbert-90 boundary, or projection-only data",
        ),
        active_row(
            name="active_conductor39_divisor_identity",
            lane="mixed conductor-39 unit / Yang distribution",
            accepted_odd_target="conductor39_U_chi",
            first_acceptable_upgrade=(
                "exact U_chi/W divisor/additive theorem preserving chi_3 tensor chi_13, Yang lift, and descent"
            ),
            first_bridge_ask=(
                "same-j X_1(8112) bridge for the conductor39_U_chi odd payload and production X_1(16)"
            ),
            first_falsifier="prime projection, axis-only statement, or source certification without finite theorem",
        ),
        active_row(
            name="active_twisted_h90_divisor_identity",
            lane="twisted ratio / Hilbert-90",
            accepted_odd_target="U_507/Y_507",
            first_acceptable_upgrade=(
                "finite divisor/additive theorem for the twisted ratio/Hilbert-90 object with period-156 context"
            ),
            first_bridge_ask=(
                "same-j X_1(8112) bridge for the twisted U_507/Y_507 odd target and production X_1(16)"
            ),
            first_falsifier="H90 vocabulary without finite theorem and period-156 bridge context",
        ),
        active_row(
            name="active_curved_corner_divisor_identity",
            lane="unit-triangle curved K-traced corner",
            accepted_odd_target="curved_corner",
            first_acceptable_upgrade=(
                "finite divisor/additive theorem for the unit-triangle curved K-traced corner with period-156 context"
            ),
            first_bridge_ask=(
                "same-j X_1(8112) bridge for curved_corner and production X_1(16)"
            ),
            first_falsifier="curved helper only, wrong unit triangle, or theorem without period-156 context",
            curved_corner=True,
        ),
        active_row(
            name="active_exact75_product_divisor_theorem",
            lane="Kubert-Lang / KSY exact normalized-y product",
            accepted_odd_target="exact_P",
            first_acceptable_upgrade=(
                "exact P divisor/additive theorem with mixed C3 x C169 graph, all 75 equal atoms, and orientation"
            ),
            first_bridge_ask="same-j X_1(8112) bridge for exact_P and production X_1(16)",
            first_falsifier="field generation, one y-value, subset/nonuniform atom product, or missing orientation",
            exact75=True,
        ),
    )


def accepted_target_covered(target: str, accepted_targets: set[str]) -> bool:
    return all(part in accepted_targets for part in target.split("/") if part != "none")


def profile_external_bridge_resolution_queue() -> ExternalBridgeResolutionQueue:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    frontdoor = profile_external_frontdoor_answer_router()
    post_policy = profile_external_post_policy_x18112_work_order()
    intake = profile_x1_8112_bridge_theorem_intake()
    rows = resolution_rows()
    accepted_targets = set(intake.accepted_odd_targets)
    resolved = sum(not row.source_frontdoor_active for row in rows)
    killed = sum(row.killed_as_direct_closer for row in rows)
    context = sum(row.context_only for row in rows)
    active_frontdoor = sum(row.source_frontdoor_active for row in rows)
    active_bridge = sum(row.post_policy_bridge_active for row in rows)
    exact75 = sum(row.exact75 for row in rows)
    curved = sum(row.curved_corner for row in rows)
    stale_access_blocked = sum(
        row.resolution_status == "candidate_needs_pdf_or_ocr_before_theorem_use"
        for row in rows
    )
    direct_closing = 0
    artifacts_present = all(
        row.prior_artifact.exists()
        and row.prior_artifact.stat().st_size > 0
        and row.resolution_artifact.exists()
        and row.resolution_artifact.stat().st_size > 0
        for row in rows
    )
    active_targets_covered = all(
        accepted_target_covered(row.accepted_odd_target, accepted_targets)
        for row in rows
        if row.source_frontdoor_active
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and artifacts_present
        and frontdoor.row_ok
        and frontdoor.source_closing_rows == 5
        and frontdoor.continue_to_danger3_rows == 5
        and frontdoor.current_source_theorem_rows == 0
        and post_policy.row_ok
        and post_policy.bridge_target_rows == 7
        and intake.row_ok
        and active_targets_covered
        and len(rows) == 8
        and resolved == 3
        and killed == 3
        and context == 3
        and active_frontdoor == 5
        and active_bridge == 5
        and exact75 == 1
        and curved == 1
        and stale_access_blocked == 0
        and direct_closing == 0
        and all(row.ok for row in rows)
    )
    return ExternalBridgeResolutionQueue(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_frontdoor_answer_ok=frontdoor.row_ok,
        external_post_policy_ok=post_policy.row_ok,
        x18112_intake_ok=intake.row_ok,
        rows=rows,
        row_count=len(rows),
        resolved_source_rows=resolved,
        killed_direct_rows=killed,
        context_only_rows=context,
        active_frontdoor_rows=active_frontdoor,
        active_post_policy_bridge_rows=active_bridge,
        exact75_rows=exact75,
        curved_corner_rows=curved,
        stale_access_blocked_rows=stale_access_blocked,
        direct_closing_rows=direct_closing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_bridge_resolution_queue()
    print("p25 KSY-y external bridge resolution queue gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_frontdoor_answer_ok={int(profile.external_frontdoor_answer_ok)}")
    print(f"  external_post_policy_ok={int(profile.external_post_policy_ok)}")
    print(f"  x18112_intake_ok={int(profile.x18112_intake_ok)}")
    print("resolution_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: lane={row.lane} active_source={int(row.source_frontdoor_active)} "
            f"bridge={int(row.post_policy_bridge_active)} killed={int(row.killed_as_direct_closer)} "
            f"context={int(row.context_only)} exact75={int(row.exact75)} "
            f"curved={int(row.curved_corner)} odd_target={row.accepted_odd_target}"
        )
        print(f"    status={row.resolution_status}")
        print(f"    prior={row.prior_artifact}")
        print(f"    resolution={row.resolution_artifact}")
        print(f"    upgrade={row.first_acceptable_upgrade}")
        print(f"    bridge_ask={row.first_bridge_ask}")
        print(f"    falsifier={row.first_falsifier}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  resolved_source_rows={profile.resolved_source_rows}")
    print(f"  killed_direct_rows={profile.killed_direct_rows}")
    print(f"  context_only_rows={profile.context_only_rows}")
    print(f"  active_frontdoor_rows={profile.active_frontdoor_rows}")
    print(f"  active_post_policy_bridge_rows={profile.active_post_policy_bridge_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  curved_corner_rows={profile.curved_corner_rows}")
    print(f"  stale_access_blocked_rows={profile.stale_access_blocked_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print("interpretation")
    print("  old_pdf_or_broad_external_access_actions_are_closed=1")
    print("  five_external_frontdoors_remain_live_but_no_current_source_theorem_exists=1")
    print("  every_live_frontdoor_routes_to_policy_then_same_j_x18112_bridge=1")
    print("  direct_external_closers_seen_so_far=0")
    print(
        "ksy_y_external_bridge_resolution_queue_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external bridge resolution queue regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
