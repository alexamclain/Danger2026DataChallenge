#!/usr/bin/env python3
"""External X_1(16) specialization work order after same-j bridge answers.

The external bridge-answer router says that five live front doors can continue
only to X_1(16) surface specialization.  This gate makes that next ask concrete:
for each bridge-stage yes, the acceptable production payload is either
X_1(16) y plus model root x, hence A,xP16, or direct A,xP16.  Both shapes route
to the active x16halvenonsplit halving boundary, not to submission.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_x18112_bridge_answer_router_gate import (
    ExternalX18112BridgeAnswerRow,
    profile_external_x18112_bridge_answer_router,
)
from p25_ksy_y_post_bridge_x16_surface_intake_gate import (
    PostBridgeX16SurfaceDecision,
    PostBridgeX16SurfacePacket,
    classify_packet,
    profile_post_bridge_x16_surface_intake,
)
from p25_ksy_y_x1_16_halving_chain_contract_gate import (
    profile_x1_16_halving_chain_contract,
)
from p25_ksy_y_x1_16_montgomery_chart_contract_gate import (
    ACTIVE_PRODUCTION_MODE,
    X16_START_DEPTH,
    profile_x1_16_montgomery_chart_contract,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_x18112_bridge_answer_router_20260614.md",
        "ksy_y_external_x18112_bridge_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_post_bridge_x16_surface_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_chain_contract_20260614.md",
        "ksy_y_x1_16_halving_chain_contract_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalX16SpecializationWorkRow:
    name: str
    source_answer_name: str
    source_lane: str
    odd_payload_object: str
    payload_variant: str
    accepted_shape: str
    first_falsifier: str
    surface_decision: PostBridgeX16SurfaceDecision
    active_mode: str
    active_start_depth: int
    exact75: bool
    curved_corner: bool
    optional_dgate_required: bool
    current_evidence: bool
    current_submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExternalX16SpecializationWorkOrder:
    dependency_markers_present: int
    dependency_markers_total: int
    bridge_answer_router_ok: bool
    post_bridge_surface_intake_ok: bool
    montgomery_chart_contract_ok: bool
    halving_chain_contract_ok: bool
    active_mode: str
    active_start_depth: int
    active_halving_steps: int
    rows: tuple[ExternalX16SpecializationWorkRow, ...]
    row_count: int
    frontdoor_count: int
    y_model_root_rows: int
    direct_A_xP16_rows: int
    active_surface_rows: int
    continue_to_halving_rows: int
    exact75_rows: int
    curved_corner_rows: int
    optional_dgate_required_rows: int
    current_evidence_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def surface_packet(
    name: str,
    *,
    y_model_root: bool,
    direct_A_xP16: bool,
) -> PostBridgeX16SurfacePacket:
    return PostBridgeX16SurfacePacket(
        name=name,
        current_evidence=False,
        same_j_bridge_accepted=True,
        same_curve_p16=True,
        y_parameter=y_model_root,
        model_root_x=y_model_root,
        A_and_xP16=direct_A_xP16 or y_model_root,
        optional_first_half_dgate=False,
        active_first_branch_chain=False,
        any_valid_halving_chain=False,
        direct_x0=False,
        internal_verify=False,
        official_vpp=False,
    )


def work_row(
    answer: ExternalX18112BridgeAnswerRow,
    *,
    payload_variant: str,
) -> ExternalX16SpecializationWorkRow:
    y_model_root = payload_variant == "y_model_root"
    direct_A_xP16 = payload_variant == "direct_A_xP16"
    decision = classify_packet(
        surface_packet(
            f"{answer.source_query_name}_{payload_variant}",
            y_model_root=y_model_root,
            direct_A_xP16=direct_A_xP16,
        )
    )
    accepted_shape = (
        "same-j bridge emits X_1(16) y, model root x, Montgomery A, and xP16"
        if y_model_root
        else "same-j bridge directly emits Montgomery A and xP16"
    )
    first_falsifier = (
        "model root x or induced A,xP16 missing"
        if y_model_root
        else "direct A,xP16 not on the production Montgomery chart"
    )
    ok = (
        answer.ok
        and answer.continue_to_x16
        and not answer.current_evidence
        and decision.ok
        and decision.bridge_established
        and decision.active_x16_surface_reached
        and not decision.optional_dgate_surface_reached
        and not decision.extraction_ready
        and not decision.submission_ready
        and decision.decision == "active_surface_reached_halving_missing"
    )
    return ExternalX16SpecializationWorkRow(
        name=f"{answer.source_query_name}_{payload_variant}",
        source_answer_name=answer.name,
        source_lane=answer.source_lane,
        odd_payload_object=answer.odd_payload_object,
        payload_variant=payload_variant,
        accepted_shape=accepted_shape,
        first_falsifier=first_falsifier,
        surface_decision=decision,
        active_mode=ACTIVE_PRODUCTION_MODE,
        active_start_depth=X16_START_DEPTH,
        exact75=answer.exact75,
        curved_corner=answer.curved_corner,
        optional_dgate_required=False,
        current_evidence=False,
        current_submission_ready=False,
        ok=ok,
    )


def work_rows(
    answer_rows: tuple[ExternalX18112BridgeAnswerRow, ...],
) -> tuple[ExternalX16SpecializationWorkRow, ...]:
    bridge_answers = tuple(row for row in answer_rows if row.continue_to_x16)
    rows: list[ExternalX16SpecializationWorkRow] = []
    for answer in bridge_answers:
        rows.append(work_row(answer, payload_variant="y_model_root"))
        rows.append(work_row(answer, payload_variant="direct_A_xP16"))
    return tuple(rows)


def profile_external_x16_specialization_work_order() -> ExternalX16SpecializationWorkOrder:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    answer_router = profile_external_x18112_bridge_answer_router()
    post_bridge = profile_post_bridge_x16_surface_intake()
    chart = profile_x1_16_montgomery_chart_contract()
    halving = profile_x1_16_halving_chain_contract()
    rows = work_rows(answer_router.rows)
    frontdoors = len({row.source_answer_name for row in rows})
    y_model = sum(row.payload_variant == "y_model_root" for row in rows)
    direct = sum(row.payload_variant == "direct_A_xP16" for row in rows)
    active = sum(row.surface_decision.active_x16_surface_reached for row in rows)
    halving_rows = sum(
        row.surface_decision.decision == "active_surface_reached_halving_missing"
        for row in rows
    )
    exact75 = sum(row.exact75 for row in rows)
    curved = sum(row.curved_corner for row in rows)
    dgate_required = sum(row.optional_dgate_required for row in rows)
    current = sum(row.current_evidence for row in rows)
    submission = sum(row.current_submission_ready for row in rows)
    source_answers = tuple(row.source_answer_name for row in rows[::2])
    expected_sources = (
        "answer_ask_h0_same_j_x18112_bridge",
        "answer_ask_conductor39_same_j_x18112_bridge",
        "answer_ask_twisted_h90_same_j_x18112_bridge",
        "answer_ask_curved_corner_same_j_x18112_bridge",
        "answer_ask_exactP_same_j_x18112_bridge",
    )
    variants = tuple(row.payload_variant for row in rows)
    expected_variants = (
        "y_model_root",
        "direct_A_xP16",
        "y_model_root",
        "direct_A_xP16",
        "y_model_root",
        "direct_A_xP16",
        "y_model_root",
        "direct_A_xP16",
        "y_model_root",
        "direct_A_xP16",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and answer_router.row_ok
        and answer_router.continue_to_x16_rows == 5
        and post_bridge.row_ok
        and chart.row_ok
        and halving.row_ok
        and ACTIVE_PRODUCTION_MODE == "x16halvenonsplit"
        and X16_START_DEPTH == 4
        and halving.active_halving_steps == 38
        and len(rows) == 10
        and frontdoors == 5
        and y_model == 5
        and direct == 5
        and active == 10
        and halving_rows == 10
        and exact75 == 2
        and curved == 2
        and dgate_required == 0
        and current == 0
        and submission == 0
        and source_answers == expected_sources
        and variants == expected_variants
        and all(row.ok for row in rows)
    )
    return ExternalX16SpecializationWorkOrder(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        bridge_answer_router_ok=answer_router.row_ok,
        post_bridge_surface_intake_ok=post_bridge.row_ok,
        montgomery_chart_contract_ok=chart.row_ok,
        halving_chain_contract_ok=halving.row_ok,
        active_mode=ACTIVE_PRODUCTION_MODE,
        active_start_depth=X16_START_DEPTH,
        active_halving_steps=halving.active_halving_steps,
        rows=rows,
        row_count=len(rows),
        frontdoor_count=frontdoors,
        y_model_root_rows=y_model,
        direct_A_xP16_rows=direct,
        active_surface_rows=active,
        continue_to_halving_rows=halving_rows,
        exact75_rows=exact75,
        curved_corner_rows=curved,
        optional_dgate_required_rows=dgate_required,
        current_evidence_rows=current,
        current_submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_x16_specialization_work_order()
    print("p25 KSY-y external X1(16) specialization work-order gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  bridge_answer_router_ok={int(profile.bridge_answer_router_ok)}")
    print(f"  post_bridge_surface_intake_ok={int(profile.post_bridge_surface_intake_ok)}")
    print(f"  montgomery_chart_contract_ok={int(profile.montgomery_chart_contract_ok)}")
    print(f"  halving_chain_contract_ok={int(profile.halving_chain_contract_ok)}")
    print("production")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  active_halving_steps={profile.active_halving_steps}")
    print("work_order_rows")
    for row in profile.rows:
        surface = row.surface_decision
        print(
            "  "
            f"{row.name}: lane={row.source_lane} odd={row.odd_payload_object} "
            f"variant={row.payload_variant} decision={surface.decision} "
            f"active_surface={int(surface.active_x16_surface_reached)} "
            f"extract={int(surface.extraction_ready)} "
            f"submission={int(surface.submission_ready)} "
            f"exact75={int(row.exact75)} curved={int(row.curved_corner)} "
            f"dgate_required={int(row.optional_dgate_required)} "
            f"current={int(row.current_evidence)}"
        )
        print(f"    accepted={row.accepted_shape}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    next={surface.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  frontdoor_count={profile.frontdoor_count}")
    print(f"  y_model_root_rows={profile.y_model_root_rows}")
    print(f"  direct_A_xP16_rows={profile.direct_A_xP16_rows}")
    print(f"  active_surface_rows={profile.active_surface_rows}")
    print(f"  continue_to_halving_rows={profile.continue_to_halving_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  curved_corner_rows={profile.curved_corner_rows}")
    print(f"  optional_dgate_required_rows={profile.optional_dgate_required_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  each_live_external_bridge_frontdoor_has_two_X16_surface_acceptance_shapes=1")
    print("  accepted_X16_surface_routes_to_active_depth4_halving_not_submission=1")
    print("  optional_dgate_is_not_required_for_the_active_production_mode=1")
    print("  current_submission_ready_rows_remain_zero=1")
    print(
        "ksy_y_external_x16_specialization_work_order_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external X1(16) specialization work-order regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
