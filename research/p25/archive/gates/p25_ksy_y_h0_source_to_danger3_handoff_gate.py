#!/usr/bin/env python3
"""H0 source-closed theorem to DANGER3 handoff contract.

The boundary/value ambiguity gate leaves two H0 source-closing exits:
period-156 value identity or divisor/additive identity.  This gate records the
minimum downstream payload needed after either exit before we can call the
moonshot a DANGER3 win.  It intentionally reads existing markers and uses the
X_1(8112) classifier without replaying the full H0 proof stack.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path

from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    classify_claim,
)


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class H0SourceToDanger3HandoffRow:
    name: str
    accepted_input: str
    source_closing_kind: str
    source_stage_closed: bool
    x1_claim_executed: bool
    decision: str
    first_missing_clause: str
    policy_unblocked: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    must_not_accept_as_submission: bool
    ok: bool


@dataclass(frozen=True)
class H0SourceToDanger3HandoffPacket:
    boundary_value_marker_present: bool
    x16_route_marker_present: bool
    halving_payload_marker_present: bool
    danger3_extraction_marker_present: bool
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    handoff_rows: tuple[H0SourceToDanger3HandoffRow, ...]
    row_count: int
    source_closing_input_rows: int
    x1_classifier_rows: int
    non_submission_rows: int
    policy_missing_rows: int
    policy_unblocked_rows: int
    upstream_only_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def x1_claim(
    name: str,
    *,
    odd_payload_object: str = "H0_translate",
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3: bool = False,
    concrete_vpp: bool = False,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=name,
        theorem_body_verified=True,
        odd_payload_object=odd_payload_object,
        exact_p25_specialization=True,
        odd_level_value_or_divisor=True,
        fiber_product_or_modular_correspondence=fiber_product,
        preserves_j_gluing=j_gluing,
        x16_surface_relation=x16_relation,
        emits_x16_y=emit_y,
        emits_model_root_or_xp16=emit_model_root_xp16,
        emits_halving_chain_or_x0=emit_x0,
        danger3_framing=danger3,
        concrete_vpp_verified_triple=concrete_vpp,
    )


def pre_x1_row(
    *,
    name: str,
    accepted_input: str,
    source_closing_kind: str,
) -> H0SourceToDanger3HandoffRow:
    return H0SourceToDanger3HandoffRow(
        name=name,
        accepted_input=accepted_input,
        source_closing_kind=source_closing_kind,
        source_stage_closed=True,
        x1_claim_executed=False,
        decision="source_theorem_closed_policy_or_framing_missing",
        first_missing_clause="DANGER3 finite-identity/non-CM framing",
        policy_unblocked=False,
        cross_level_bridge_identified=False,
        x16_surface_reached=False,
        extraction_ready=False,
        submission_ready=False,
        must_not_accept_as_submission=True,
        ok=True,
    )


def x1_row(
    *,
    name: str,
    accepted_input: str,
    source_closing_kind: str,
    claim: X18112BridgeTheoremClaim,
    expected_decision: str,
    expected_missing: str,
    policy_unblocked: bool,
) -> H0SourceToDanger3HandoffRow:
    decision = classify_claim(claim)
    return H0SourceToDanger3HandoffRow(
        name=name,
        accepted_input=accepted_input,
        source_closing_kind=source_closing_kind,
        source_stage_closed=True,
        x1_claim_executed=True,
        decision=decision.decision,
        first_missing_clause=decision.first_missing_clause,
        policy_unblocked=policy_unblocked,
        cross_level_bridge_identified=decision.cross_level_bridge_identified,
        x16_surface_reached=decision.x16_surface_reached,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        must_not_accept_as_submission=not decision.submission_ready,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def handoff_rows() -> tuple[H0SourceToDanger3HandoffRow, ...]:
    return (
        pre_x1_row(
            name="h0_period156_value_source_closed_pre_policy",
            accepted_input="exact finite H0 value identity with period-156 context",
            source_closing_kind="period156_value",
        ),
        pre_x1_row(
            name="h0_divisor_additive_source_closed_pre_policy",
            accepted_input="exact H0 divisor/additive identity with Hilbert-90 boundary",
            source_closing_kind="divisor_additive",
        ),
        x1_row(
            name="h0_policy_yes_no_cross_level",
            accepted_input="DANGER3-accepted odd-level H0 theorem, no cross-level map",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim("h0_policy_yes_no_cross_level"),
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            expected_missing="X_1(16) relation or X_1(8112) fiber-product theorem",
            policy_unblocked=True,
        ),
        x1_row(
            name="h0_x18112_bridge_no_x16_specialization",
            accepted_input="same-j X_1(8112) bridge for the H0 theorem payload",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x18112_bridge_no_x16_specialization",
                fiber_product=True,
                j_gluing=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            expected_missing="specialized relation yielding X_1(16) y, A, xP16, or x0",
            policy_unblocked=True,
        ),
        x1_row(
            name="h0_x16_relation_without_y",
            accepted_input="X_1(8112) theorem specialized only to an X_1(16) relation",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x16_relation_without_y",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
            ),
            expected_decision="conditional_x16_relation_without_y",
            expected_missing="actual X_1(16) parameter y",
            policy_unblocked=True,
        ),
        x1_row(
            name="h0_x16_y_without_montgomery_surface",
            accepted_input="X_1(16) y emitted without model root, A, and xP16",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x16_y_without_montgomery_surface",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
            ),
            expected_decision="conditional_y_without_montgomery_surface",
            expected_missing="model root x, Montgomery A, and marked xP16",
            policy_unblocked=True,
        ),
        x1_row(
            name="h0_x16_surface_policy_missing",
            accepted_input="X_1(16) y, A, and xP16 without DANGER3 framing",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x16_surface_policy_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
            policy_unblocked=False,
        ),
        x1_row(
            name="h0_x16_surface_halving_missing",
            accepted_input="DANGER3-framed X_1(16) y, A, and xP16 surface",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x16_surface_halving_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
                danger3=True,
            ),
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            expected_missing="valid halving chain from xP16 to concrete x0",
            policy_unblocked=True,
        ),
        x1_row(
            name="h0_x0_payload_vpp_missing",
            accepted_input="DANGER3-framed H0 bridge with concrete A and x0",
            source_closing_kind="shared_after_source_close",
            claim=x1_claim(
                "h0_x0_payload_vpp_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
                emit_x0=True,
                danger3=True,
            ),
            expected_decision="extraction_ready_vpp_missing",
            expected_missing="official vpp.py verification",
            policy_unblocked=True,
        ),
        x1_row(
            name="verified_pomerance_triple",
            accepted_input="concrete p25 (p,A,x0) triple verified by official vpp.py",
            source_closing_kind="final_submission",
            claim=x1_claim("verified_pomerance_triple", concrete_vpp=True),
            expected_decision="submission_ready_verified_triple",
            expected_missing="none",
            policy_unblocked=True,
        ),
    )


def profile_h0_source_to_danger3_handoff() -> H0SourceToDanger3HandoffPacket:
    boundary_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_boundary_value_ambiguity_20260614.md",
        "ksy_y_h0_translate_boundary_value_ambiguity_rows=1/1",
    )
    x16_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_x16_route_propagation_20260614.md",
        "ksy_y_h0_translate_x16_route_propagation_rows=1/1",
    )
    halving_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    )
    danger3_marker = marker_present(
        RESEARCH / "p25_ksy_y_danger3_extraction_surface_20260614.md",
        "ksy_y_danger3_extraction_surface_rows=1/1",
    )
    support_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    rows = handoff_rows()
    source_inputs = sum(row.source_closing_kind in {"period156_value", "divisor_additive"} for row in rows)
    x1_rows = sum(row.x1_claim_executed for row in rows)
    non_submission = sum(row.must_not_accept_as_submission for row in rows)
    policy_missing = sum(row.first_missing_clause == "DANGER3 finite-identity/non-CM framing" for row in rows)
    policy_unblocked = sum(row.policy_unblocked for row in rows)
    upstream = sum(row.decision == "upstream_odd_value_no_cross_level_bridge" for row in rows)
    cross = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    row_ok = (
        boundary_marker
        and x16_marker
        and halving_marker
        and danger3_marker
        and support_gcd == 1
        and ambient_gcd == 11
        and len(rows) == 10
        and source_inputs == 2
        and x1_rows == 8
        and non_submission == 9
        and policy_missing == 3
        and policy_unblocked == 7
        and upstream == 1
        and cross == 7
        and x16 == 4
        and extraction == 2
        and submission == 1
        and tuple(row.decision for row in rows)
        == (
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "upstream_odd_value_no_cross_level_bridge",
            "cross_level_target_identified_specialization_missing",
            "conditional_x16_relation_without_y",
            "conditional_y_without_montgomery_surface",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready_verified_triple",
        )
        and all(row.ok for row in rows)
    )
    return H0SourceToDanger3HandoffPacket(
        boundary_value_marker_present=boundary_marker,
        x16_route_marker_present=x16_marker,
        halving_payload_marker_present=halving_marker,
        danger3_extraction_marker_present=danger3_marker,
        support_period_root_gcd=support_gcd,
        ambient_period_root_gcd=ambient_gcd,
        handoff_rows=rows,
        row_count=len(rows),
        source_closing_input_rows=source_inputs,
        x1_classifier_rows=x1_rows,
        non_submission_rows=non_submission,
        policy_missing_rows=policy_missing,
        policy_unblocked_rows=policy_unblocked,
        upstream_only_rows=upstream,
        cross_level_bridge_rows=cross,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_source_to_danger3_handoff()
    print("p25 KSY-y H0 source-to-DANGER3 handoff gate")
    print("dependencies")
    print(f"  boundary_value_marker_present={int(profile.boundary_value_marker_present)}")
    print(f"  x16_route_marker_present={int(profile.x16_route_marker_present)}")
    print(f"  halving_payload_marker_present={int(profile.halving_payload_marker_present)}")
    print(f"  danger3_extraction_marker_present={int(profile.danger3_extraction_marker_present)}")
    print("arithmetic")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print("handoff_rows")
    for row in profile.handoff_rows:
        print(
            "  "
            f"{row.name}: kind={row.source_closing_kind} x1={int(row.x1_claim_executed)} "
            f"decision={row.decision} policy={int(row.policy_unblocked)} "
            f"cross={int(row.cross_level_bridge_identified)} "
            f"x16={int(row.x16_surface_reached)} extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} missing={row.first_missing_clause}"
        )
        print(f"    input={row.accepted_input}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_input_rows={profile.source_closing_input_rows}")
    print(f"  x1_classifier_rows={profile.x1_classifier_rows}")
    print(f"  non_submission_rows={profile.non_submission_rows}")
    print(f"  policy_missing_rows={profile.policy_missing_rows}")
    print(f"  policy_unblocked_rows={profile.policy_unblocked_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  either_H0_source_closing_exit_is_real_but_not_a_submission=1")
    print("  handoff_requires_DANGER3_framing_same_j_X1_8112_bridge_and_X1_16_surface=1")
    print("  x16_surface_still_needs_halving_chain_or_direct_x0_and_official_vpp=1")
    print("  only_vpp_verified_pomerance_triple_is_submission_ready=1")
    print(f"ksy_y_h0_source_to_danger3_handoff_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 source-to-DANGER3 handoff regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
