#!/usr/bin/env python3
"""External same-j X_1(8112) bridge query packet for live p25 front doors.

The external bridge resolution queue now has five live source front doors.  A
source-stage yes is still not extraction: after DANGER3 policy/framing, each
odd target must be glued to the production X_1(16) side over the same
j-invariant.  This packet turns that bridge need into exact expert/literature
questions and shortcut falsifiers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_bridge_resolution_queue_gate import (
    profile_external_bridge_resolution_queue,
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
        RESEARCH / "p25_ksy_y_external_bridge_resolution_queue_20260614.md",
        "ksy_y_external_bridge_resolution_queue_rows=1/1",
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
class ExternalX18112BridgeQueryRow:
    name: str
    query_kind: str
    source_lane: str
    odd_payload_object: str
    question_for_source: str
    accepted_answer_shape: str
    first_falsifier: str
    candidate_command: str
    expected_decision: str
    decision: X18112BridgeTheoremDecision
    active_frontdoor: bool
    continue_route: bool
    repair_or_rewrite: bool
    kill_route: bool
    exact75: bool
    curved_corner: bool
    ok: bool


@dataclass(frozen=True)
class ExternalX18112BridgeQueryPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    resolution_queue_ok: bool
    x18112_intake_ok: bool
    rows: tuple[ExternalX18112BridgeQueryRow, ...]
    row_count: int
    bridge_query_rows: int
    falsifier_rows: int
    downstream_rows: int
    active_frontdoor_rows: int
    accepted_odd_target_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    continue_rows: int
    repair_or_rewrite_rows: int
    kill_rows: int
    exact75_rows: int
    curved_corner_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def claim(
    name: str,
    *,
    theorem_body: bool = True,
    odd_payload_object: str,
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
    odd_payload_object: str,
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


def query_row(
    *,
    name: str,
    query_kind: str,
    source_lane: str,
    odd_payload_object: str,
    question: str,
    accepted_shape: str,
    falsifier: str,
    expected_decision: str,
    claim_kwargs: dict[str, bool | str],
    active_frontdoor: bool = False,
    continue_route: bool = False,
    repair_or_rewrite: bool = False,
    kill_route: bool = False,
    exact75: bool = False,
    curved_corner: bool = False,
) -> ExternalX18112BridgeQueryRow:
    kwargs = {"odd_payload_object": odd_payload_object, **claim_kwargs}
    decision = classify_claim(claim(name, **kwargs))
    command = candidate_command(name=name, **kwargs)
    return ExternalX18112BridgeQueryRow(
        name=name,
        query_kind=query_kind,
        source_lane=source_lane,
        odd_payload_object=odd_payload_object,
        question_for_source=question,
        accepted_answer_shape=accepted_shape,
        first_falsifier=falsifier,
        candidate_command=command,
        expected_decision=expected_decision,
        decision=decision,
        active_frontdoor=active_frontdoor,
        continue_route=continue_route,
        repair_or_rewrite=repair_or_rewrite,
        kill_route=kill_route,
        exact75=exact75,
        curved_corner=curved_corner,
        ok=decision.row_ok and decision.decision == expected_decision,
    )


def bridge_question(
    *,
    name: str,
    source_lane: str,
    odd_payload_object: str,
    positive: str,
    falsifier: str,
    exact75: bool = False,
    curved_corner: bool = False,
) -> ExternalX18112BridgeQueryRow:
    return query_row(
        name=name,
        query_kind="bridge_query",
        source_lane=source_lane,
        odd_payload_object=odd_payload_object,
        question=(
            "After the source theorem and DANGER3 policy/framing yes, does the "
            "source or expert answer prove a same-j X_1(8112) bridge, or exact "
            "order-8112 generator, tying this odd target to the production X_1(16) side?"
        ),
        accepted_shape=positive,
        falsifier=falsifier,
        expected_decision="cross_level_target_identified_specialization_missing",
        claim_kwargs={"fiber_product": True, "j_gluing": True},
        active_frontdoor=True,
        continue_route=True,
        exact75=exact75,
        curved_corner=curved_corner,
    )


def query_rows() -> tuple[ExternalX18112BridgeQueryRow, ...]:
    return (
        bridge_question(
            name="ask_h0_same_j_x18112_bridge",
            source_lane="H0/Yang/Kubert-Lang",
            odd_payload_object="canonical_H0",
            positive="same-curve exact P16 plus canonical_H0/Y_507 odd payload, or normalized order-8112 R",
            falsifier="H0 source theorem remains upstream-only or level-16 data is independent",
        ),
        bridge_question(
            name="ask_conductor39_same_j_x18112_bridge",
            source_lane="mixed conductor-39 unit / Yang distribution",
            odd_payload_object="conductor39_U_chi",
            positive="same-j bridge for conductor39_U_chi and production X_1(16)",
            falsifier="conductor-39 theorem gives only source certification or ungrafted projection data",
        ),
        bridge_question(
            name="ask_twisted_h90_same_j_x18112_bridge",
            source_lane="twisted ratio / Hilbert-90",
            odd_payload_object="U_507",
            positive="same-j bridge for the twisted U_507/Y_507 odd target and production X_1(16)",
            falsifier="H90 finite theorem has no same-j level-16/level-507 gluing",
        ),
        bridge_question(
            name="ask_curved_corner_same_j_x18112_bridge",
            source_lane="unit-triangle curved K-traced corner",
            odd_payload_object="curved_corner",
            positive="same-j bridge for curved_corner and production X_1(16)",
            falsifier="curved-corner theorem is helper-only or not tied to an accepted odd target over the same j",
            curved_corner=True,
        ),
        bridge_question(
            name="ask_exactP_same_j_x18112_bridge",
            source_lane="Kubert-Lang / KSY exact normalized-y product",
            odd_payload_object="exact_P",
            positive="same-j bridge for exact_P and production X_1(16)",
            falsifier="exact P theorem remains an upstream odd value/product theorem with no cross-level bridge",
            exact75=True,
        ),
        query_row(
            name="falsify_odd_theorem_only_no_bridge",
            query_kind="falsifier",
            source_lane="any accepted odd target",
            odd_payload_object="exact_P",
            question="Does the answer only prove the odd target identity, with no X_1(16) relation or X_1(8112) fiber product?",
            accepted_shape="upstream source progress only; do not call it extraction",
            falsifier="X_1(16) relation or X_1(8112) bridge is missing",
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            claim_kwargs={"fiber_product": False, "j_gluing": False},
            repair_or_rewrite=True,
            exact75=True,
        ),
        query_row(
            name="falsify_unglued_level16_level507_components",
            query_kind="falsifier",
            source_lane="any accepted odd target",
            odd_payload_object="exact_P",
            question="Are the level-16 and odd-level facts independent rather than glued over the same j-invariant?",
            accepted_shape="reject independent level data without same-j gluing",
            falsifier="fiber product is not over the same j-invariant",
            expected_decision="reject_unvalidated_fiber_product_gluing",
            claim_kwargs={"fiber_product": True, "j_gluing": False},
            kill_route=True,
            exact75=True,
        ),
        query_row(
            name="falsify_unknown_odd_target",
            query_kind="falsifier",
            source_lane="ambient or unmapped external target",
            odd_payload_object="ambient_value_only",
            question="Does the answer give a value or product that is not mapped onto an accepted p25 odd target?",
            accepted_shape="rewrite onto exact_P, U_507, Y_507, canonical_H0, conductor39_U_chi, or curved_corner",
            falsifier="unknown odd target is not on the recorded KSY/Yang/H90/curved-corner spine",
            expected_decision="conditional_unknown_odd_target",
            claim_kwargs={"fiber_product": True, "j_gluing": True},
            repair_or_rewrite=True,
        ),
        query_row(
            name="falsify_generic_x16_without_odd_payload",
            query_kind="falsifier",
            source_lane="generic X_1(16)",
            odd_payload_object="canonical_H0",
            question="Does the answer only construct generic X_1(16) data without an odd-level source payload?",
            accepted_shape="reject generic X_1(16) data unless tied to the p25 odd target",
            falsifier="odd-level KSY/Yang/H90/curved-corner value or divisor payload is missing",
            expected_decision="reject_generic_x16_not_ksy_bridge",
            claim_kwargs={
                "odd_value_or_divisor": False,
                "fiber_product": False,
                "j_gluing": True,
                "x16_relation": True,
                "emit_y": True,
                "emit_model_root_xp16": True,
            },
            kill_route=True,
        ),
        query_row(
            name="downstream_x16_surface_no_halving",
            query_kind="downstream",
            source_lane="post-bridge X_1(16) surface",
            odd_payload_object="exact_P",
            question="If the bridge emits production y/x or A,xP16, what is still missing before submission?",
            accepted_shape="X_1(16) surface reached; derive halving chain or direct x0, then official vpp.py",
            falsifier="abstract surface payload without a valid halving chain or direct x0",
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            claim_kwargs={
                "fiber_product": True,
                "j_gluing": True,
                "x16_relation": True,
                "emit_y": True,
                "emit_model_root_xp16": True,
            },
            continue_route=True,
            exact75=True,
        ),
    )


def profile_external_x18112_bridge_query_packet() -> ExternalX18112BridgeQueryPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    resolution = profile_external_bridge_resolution_queue()
    intake = profile_x1_8112_bridge_theorem_intake()
    rows = query_rows()
    bridge_queries = sum(row.query_kind == "bridge_query" for row in rows)
    falsifiers = sum(row.query_kind == "falsifier" for row in rows)
    downstream = sum(row.query_kind == "downstream" for row in rows)
    active_frontdoor = sum(row.active_frontdoor for row in rows)
    accepted_odd = sum(row.decision.odd_target_identified for row in rows)
    same_j = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16 = sum(row.decision.x16_surface_reached for row in rows)
    continue_rows = sum(row.continue_route for row in rows)
    repair = sum(row.repair_or_rewrite for row in rows)
    kill = sum(row.kill_route for row in rows)
    exact75 = sum(row.exact75 for row in rows)
    curved = sum(row.curved_corner for row in rows)
    decisions = tuple(row.decision.decision for row in rows)
    expected_decisions = (
        "cross_level_target_identified_specialization_missing",
        "cross_level_target_identified_specialization_missing",
        "cross_level_target_identified_specialization_missing",
        "cross_level_target_identified_specialization_missing",
        "cross_level_target_identified_specialization_missing",
        "upstream_odd_value_no_cross_level_bridge",
        "reject_unvalidated_fiber_product_gluing",
        "conditional_unknown_odd_target",
        "reject_generic_x16_not_ksy_bridge",
        "x16_surface_reached_halving_or_vpp_missing",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and resolution.row_ok
        and resolution.active_frontdoor_rows == 5
        and resolution.active_post_policy_bridge_rows == 5
        and intake.row_ok
        and len(rows) == 10
        and bridge_queries == 5
        and falsifiers == 4
        and downstream == 1
        and active_frontdoor == 5
        and accepted_odd == 8
        and same_j == 6
        and x16 == 1
        and continue_rows == 6
        and repair == 2
        and kill == 2
        and exact75 == 4
        and curved == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalX18112BridgeQueryPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        resolution_queue_ok=resolution.row_ok,
        x18112_intake_ok=intake.row_ok,
        rows=rows,
        row_count=len(rows),
        bridge_query_rows=bridge_queries,
        falsifier_rows=falsifiers,
        downstream_rows=downstream,
        active_frontdoor_rows=active_frontdoor,
        accepted_odd_target_rows=accepted_odd,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        continue_rows=continue_rows,
        repair_or_rewrite_rows=repair,
        kill_rows=kill,
        exact75_rows=exact75,
        curved_corner_rows=curved,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_x18112_bridge_query_packet()
    print("p25 KSY-y external same-j X1(8112) bridge query packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  resolution_queue_ok={int(profile.resolution_queue_ok)}")
    print(f"  x18112_intake_ok={int(profile.x18112_intake_ok)}")
    print("query_rows")
    for row in profile.rows:
        decision = row.decision
        print(
            "  "
            f"{row.name}: kind={row.query_kind} lane={row.source_lane} "
            f"odd={row.odd_payload_object} decision={decision.decision} "
            f"odd_target={int(decision.odd_target_identified)} "
            f"bridge={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"continue={int(row.continue_route)} repair={int(row.repair_or_rewrite)} "
            f"kill={int(row.kill_route)} exact75={int(row.exact75)} "
            f"curved={int(row.curved_corner)}"
        )
        print(f"    question={row.question_for_source}")
        print(f"    accepted={row.accepted_answer_shape}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  bridge_query_rows={profile.bridge_query_rows}")
    print(f"  falsifier_rows={profile.falsifier_rows}")
    print(f"  downstream_rows={profile.downstream_rows}")
    print(f"  active_frontdoor_rows={profile.active_frontdoor_rows}")
    print(f"  accepted_odd_target_rows={profile.accepted_odd_target_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  repair_or_rewrite_rows={profile.repair_or_rewrite_rows}")
    print(f"  kill_rows={profile.kill_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  curved_corner_rows={profile.curved_corner_rows}")
    print("interpretation")
    print("  five_live_frontdoors_have_same_j_x18112_bridge_questions=1")
    print("  odd_theorem_without_bridge_is_upstream_only=1")
    print("  unglued_or_generic_x16_shortcuts_are_killed=1")
    print("  x16_surface_still_needs_halving_or_vpp=1")
    print(
        "ksy_y_external_x18112_bridge_query_packet_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external X1(8112) bridge query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
