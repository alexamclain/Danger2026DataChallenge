#!/usr/bin/env python3
"""External post-policy X_1(8112) bridge work order.

After an external Drew policy yes, the exact 75-atom product and curved-corner
front door must enter the same cross-level bridge work as H0/Yang/H90.  This
gate makes that explicit by routing the accepted odd targets through the
X_1(8112) intake.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_drew_policy_answer_router_gate import (
    profile_external_drew_policy_answer_router,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    X18112BridgeTheoremDecision,
    classify_claim,
    profile_x1_8112_bridge_theorem_intake,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_drew_policy_answer_router_20260614.md",
        "ksy_y_external_drew_policy_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_post_source_danger3_handoff_20260614.md",
        "ksy_y_external_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_20260614.md",
        "ksy_y_x1_8112_bridge_theorem_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_8112_torsion_gluing_contract_20260614.md",
        "ksy_y_x1_8112_torsion_gluing_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalPostPolicyX18112WorkOrderRow:
    name: str
    work_item: str
    accepted_shape: str
    first_falsifier: str
    candidate_command: str
    decision: X18112BridgeTheoremDecision
    current_evidence: bool
    continue_route: bool
    kill_route: bool
    boundary_row: bool
    exact_p_payload: bool
    ok: bool


@dataclass(frozen=True)
class ExternalPostPolicyX18112WorkOrder:
    dependency_markers_present: int
    dependency_markers_total: int
    external_drew_answer_router_ok: bool
    x18112_intake_ok: bool
    rows: tuple[ExternalPostPolicyX18112WorkOrderRow, ...]
    row_count: int
    current_evidence_rows: int
    work_order_rows: int
    exact_p_payload_rows: int
    bridge_target_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    boundary_rows: int
    continue_rows: int
    kill_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def claim(
    name: str,
    *,
    theorem_body: bool = True,
    odd_payload_object: str = "exact_P",
    exact_p25: bool = True,
    odd_value_or_divisor: bool = True,
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3_framing: bool = True,
    vpp_verified: bool = False,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=name,
        theorem_body_verified=theorem_body,
        odd_payload_object=odd_payload_object,
        exact_p25_specialization=exact_p25,
        odd_level_value_or_divisor=odd_value_or_divisor,
        fiber_product_or_modular_correspondence=fiber_product,
        preserves_j_gluing=j_gluing,
        x16_surface_relation=x16_relation,
        emits_x16_y=emit_y,
        emits_model_root_or_xp16=emit_model_root_xp16,
        emits_halving_chain_or_x0=emit_x0,
        danger3_framing=danger3_framing,
        concrete_vpp_verified_triple=vpp_verified,
    )


def candidate_command(
    *,
    name: str,
    odd_payload_object: str = "exact_P",
    theorem_body: bool = True,
    exact_p25: bool = True,
    odd_value_or_divisor: bool = True,
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3_framing: bool = True,
    vpp_verified: bool = False,
) -> str:
    flags = [
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3",
        "research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--odd-payload-object {odd_payload_object}",
    ]
    for enabled, flag in (
        (theorem_body, "--theorem-body"),
        (exact_p25, "--exact-p25"),
        (odd_value_or_divisor, "--odd-value-or-divisor"),
        (fiber_product, "--fiber-product"),
        (j_gluing, "--j-gluing"),
        (x16_relation, "--x16-relation"),
        (emit_y, "--emit-y"),
        (emit_model_root_xp16, "--emit-model-root-xp16"),
        (emit_x0, "--emit-x0"),
        (danger3_framing, "--danger3-framing"),
        (vpp_verified, "--vpp-verified"),
    ):
        if enabled:
            flags.append(flag)
    return " ".join(flags)


def work_row(
    *,
    name: str,
    work_item: str,
    accepted_shape: str,
    first_falsifier: str,
    expected_decision: str,
    claim_kwargs: dict[str, bool | str],
    current_evidence: bool = False,
    continue_route: bool = False,
    kill_route: bool = False,
    boundary_row: bool = False,
) -> ExternalPostPolicyX18112WorkOrderRow:
    decision = classify_claim(claim(name, **claim_kwargs))
    command = candidate_command(name=name, **claim_kwargs)
    exact_p_payload = decision.claim.odd_payload_object == "exact_P"
    return ExternalPostPolicyX18112WorkOrderRow(
        name=name,
        work_item=work_item,
        accepted_shape=accepted_shape,
        first_falsifier=first_falsifier,
        candidate_command=command,
        decision=decision,
        current_evidence=current_evidence,
        continue_route=continue_route,
        kill_route=kill_route,
        boundary_row=boundary_row,
        exact_p_payload=exact_p_payload,
        ok=decision.row_ok
        and decision.decision == expected_decision
        and not current_evidence,
    )


def work_rows() -> tuple[ExternalPostPolicyX18112WorkOrderRow, ...]:
    return (
        work_row(
            name="exactP_odd_theorem_only_control",
            work_item="Do not confuse an exact P source theorem with extraction.",
            accepted_shape="exact 75-atom P value/divisor theorem with no cross-level bridge",
            first_falsifier="no X_1(16) relation or X_1(8112) fiber-product theorem",
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            claim_kwargs={"fiber_product": False, "j_gluing": False},
        ),
        work_row(
            name="exactP_unglued_level16_level507_falsifier",
            work_item="Reject independent level-16 and exact-P facts.",
            accepted_shape="fiber product or modular correspondence over the same j-invariant",
            first_falsifier="independent level data without same-j gluing",
            expected_decision="reject_unvalidated_fiber_product_gluing",
            claim_kwargs={"fiber_product": True, "j_gluing": False},
            kill_route=True,
        ),
        work_row(
            name="exactP_same_curve_P16_odd_bridge",
            work_item="Find same-curve exact P16 and exact-P odd target data.",
            accepted_shape="same elliptic curve with exact 16-torsion and exact_P odd payload over the same j",
            first_falsifier="same-j proof missing or odd target not exact_P/Yang/H90 compatible",
            expected_decision="cross_level_target_identified_specialization_missing",
            claim_kwargs={"fiber_product": True, "j_gluing": True},
            continue_route=True,
        ),
        work_row(
            name="exactP_order8112_generator_bridge",
            work_item="Find an exact order-8112 generator whose projections are P16 and exact_P.",
            accepted_shape="R of order 8112 with normalized projections to P16 and the exact_P odd target",
            first_falsifier="R not exact order 8112 or projections not normalized to exact_P",
            expected_decision="cross_level_target_identified_specialization_missing",
            claim_kwargs={"fiber_product": True, "j_gluing": True},
            continue_route=True,
        ),
        work_row(
            name="exactP_bridge_plus_x16_surface_no_halving",
            work_item="Specialize the exact-P bridge to the production X_1(16) Montgomery payload.",
            accepted_shape="same-j exact_P bridge emits y and model root x, or directly emits A,xP16",
            first_falsifier="abstract P16 torsion without practical y/x/A/xP16 data",
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            claim_kwargs={
                "fiber_product": True,
                "j_gluing": True,
                "x16_relation": True,
                "emit_y": True,
                "emit_model_root_xp16": True,
            },
            continue_route=True,
        ),
        work_row(
            name="exactP_x0_payload_vpp_missing",
            work_item="Finish extraction only after the exact-P halving payload is present.",
            accepted_shape="exact-P bridge emits concrete A,x0 or a checkable halving chain from xP16",
            first_falsifier="no official DANGER3 vpp.py verification",
            expected_decision="extraction_ready_vpp_missing",
            claim_kwargs={
                "fiber_product": True,
                "j_gluing": True,
                "x16_relation": True,
                "emit_y": True,
                "emit_model_root_xp16": True,
                "emit_x0": True,
            },
            continue_route=True,
        ),
        work_row(
            name="canonical_H0_bridge_control",
            work_item="Keep non-exact-P front doors on the same post-policy bridge ladder.",
            accepted_shape="same-j bridge for canonical_H0/Yang/H90 source paths",
            first_falsifier="front-door path not tied to an accepted KSY/Yang/H90 odd target",
            expected_decision="cross_level_target_identified_specialization_missing",
            claim_kwargs={
                "odd_payload_object": "canonical_H0",
                "fiber_product": True,
                "j_gluing": True,
            },
            continue_route=True,
        ),
        work_row(
            name="curved_corner_bridge_control",
            work_item="Keep the curved-corner front door on the same post-policy bridge ladder.",
            accepted_shape="same-j bridge for the unit-triangle curved K-traced corner source path",
            first_falsifier="curved-corner path not tied to an accepted odd target over the same j",
            expected_decision="cross_level_target_identified_specialization_missing",
            claim_kwargs={
                "odd_payload_object": "curved_corner",
                "fiber_product": True,
                "j_gluing": True,
            },
            continue_route=True,
        ),
        work_row(
            name="official_vpp_verified_boundary",
            work_item="Submission boundary.",
            accepted_shape="official DANGER3 vpp.py verifies concrete p25 A,x0",
            first_falsifier="official vpp.py rejects or has not been run",
            expected_decision="submission_ready_verified_triple",
            claim_kwargs={
                "odd_payload_object": "vpp_boundary",
                "theorem_body": False,
                "exact_p25": False,
                "odd_value_or_divisor": False,
                "vpp_verified": True,
            },
            boundary_row=True,
        ),
    )


def profile_external_post_policy_x18112_work_order() -> ExternalPostPolicyX18112WorkOrder:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    drew = profile_external_drew_policy_answer_router()
    intake = profile_x1_8112_bridge_theorem_intake()
    rows = work_rows()
    current = sum(row.current_evidence for row in rows)
    work_order = sum(not row.boundary_row for row in rows)
    exact_p = sum(row.exact_p_payload for row in rows)
    bridge_target = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16_surface = sum(row.decision.x16_surface_reached for row in rows)
    extraction = sum(row.decision.extraction_ready for row in rows)
    boundary = sum(row.boundary_row for row in rows)
    continue_rows = sum(row.continue_route for row in rows)
    kill_rows = sum(row.kill_route for row in rows)
    decisions = tuple(row.decision.decision for row in rows)
    expected_decisions = (
        "upstream_odd_value_no_cross_level_bridge",
        "reject_unvalidated_fiber_product_gluing",
        "cross_level_target_identified_specialization_missing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "cross_level_target_identified_specialization_missing",
            "cross_level_target_identified_specialization_missing",
            "submission_ready_verified_triple",
        )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and drew.row_ok
        and drew.exact75_policy_rows == 3
        and intake.row_ok
        and len(rows) == 9
        and current == 0
        and work_order == 8
        and exact_p == 6
        and bridge_target == 7
        and x16_surface == 3
        and extraction == 2
        and boundary == 1
        and continue_rows == 6
        and kill_rows == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalPostPolicyX18112WorkOrder(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_drew_answer_router_ok=drew.row_ok,
        x18112_intake_ok=intake.row_ok,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        work_order_rows=work_order,
        exact_p_payload_rows=exact_p,
        bridge_target_rows=bridge_target,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction,
        boundary_rows=boundary,
        continue_rows=continue_rows,
        kill_rows=kill_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_post_policy_x18112_work_order()
    print("p25 KSY-y external post-policy X1(8112) work-order gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_drew_answer_router_ok={int(profile.external_drew_answer_router_ok)}")
    print(f"  x18112_intake_ok={int(profile.x18112_intake_ok)}")
    print("work_order_rows")
    for row in profile.rows:
        decision = row.decision
        print(
            "  "
            f"{row.name}: odd={decision.claim.odd_payload_object} "
            f"decision={decision.decision} "
            f"bridge={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"extract={int(decision.extraction_ready)} "
            f"continue={int(row.continue_route)} kill={int(row.kill_route)} "
            f"boundary={int(row.boundary_row)} exactP={int(row.exact_p_payload)} "
            f"current={int(row.current_evidence)}"
        )
        print(f"    work={row.work_item}")
        print(f"    accepted={row.accepted_shape}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  work_order_rows={profile.work_order_rows}")
    print(f"  exact_p_payload_rows={profile.exact_p_payload_rows}")
    print(f"  bridge_target_rows={profile.bridge_target_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  boundary_rows={profile.boundary_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  kill_rows={profile.kill_rows}")
    print("interpretation")
    print("  exact75_policy_yes_starts_with_exact_P_same_j_x18112_bridge=1")
    print("  unglued_level16_exactP_data_is_killed=1")
    print("  exactP_bridge_without_x16_surface_is_not_extraction=1")
    print("  official_vpp_verified_triple_is_boundary_not_current_evidence=1")
    print(
        "ksy_y_external_post_policy_x18112_work_order_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external post-policy X1(8112) work-order regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
