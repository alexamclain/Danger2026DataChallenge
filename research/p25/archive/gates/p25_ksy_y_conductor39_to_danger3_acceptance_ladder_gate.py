#!/usr/bin/env python3
"""Acceptance ladder from conductor-39 theorem hits to DANGER3 submission.

The conductor-39 source-route packet says where an exact value/divisor theorem
would enter the moonshot.  This gate says what happens after that: policy
framing, cross-level X_1(8112) gluing, X_1(16) specialization, halving payload,
and official vpp.py verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_conductor39_value_theorem_source_route_packet_gate import (
    profile_source_route_packet,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class AcceptanceLadderRow:
    name: str
    accepted_input: str
    gate_artifact: Path
    candidate_command: str
    expected_decision: str
    first_missing_clause: str
    value_stage_closed: bool
    policy_unblocked: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    must_not_accept_as_submission: bool
    ok: bool


@dataclass(frozen=True)
class AcceptanceLadderProfile:
    source_route_packet_ok: bool
    target_packet_marker_present: bool
    danger3_framing_gate_present: bool
    submission_extraction_gate_present: bool
    extraction_surface_gate_present: bool
    x1_8112_intake_gate_present: bool
    halving_payload_marker_present: bool
    count_ladder: tuple[int, int, int, int, int]
    ladder_rows: tuple[AcceptanceLadderRow, ...]
    source_route_candidate_commands: int
    x1_8112_candidate_commands: int
    non_submission_rows: int
    value_stage_closed_rows: int
    policy_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def x1_8112_candidate_command(
    name: str,
    *,
    odd_object: str = "Y_507",
    fiber_product: bool = False,
    x16_relation: bool = False,
    danger3_framing: bool = False,
    emit_x0: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--odd-payload-object {odd_object}",
        "--theorem-body",
        "--exact-p25",
        "--odd-value-or-divisor",
    ]
    if fiber_product:
        parts.extend(("--fiber-product", "--j-gluing"))
    if x16_relation:
        parts.extend(("--x16-relation", "--emit-y", "--emit-model-root-xp16"))
    if danger3_framing:
        parts.append("--danger3-framing")
    if emit_x0:
        parts.append("--emit-x0")
    return " ".join(parts)


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def ladder_rows() -> tuple[AcceptanceLadderRow, ...]:
    source_route_gate = RESEARCH / "p25_ksy_y_conductor39_value_theorem_source_route_packet_gate.py"
    x1_8112_gate = RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py"
    halving_gate = RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_gate.py"
    submission_gate = (
        RESEARCH
        / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py"
    )
    return (
        AcceptanceLadderRow(
            name="source_value_theorem_pre_policy",
            accepted_input=(
                "exact U_chi, W, canonical H0, or Y_507 value/divisor theorem "
                "from the conductor-39 source-route packet"
            ),
            gate_artifact=source_route_gate,
            candidate_command="use one of the four source-route packet candidate commands",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            value_stage_closed=True,
            policy_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="odd_value_theorem_policy_yes_no_cross_level",
            accepted_input="policy-accepted finite identity for an odd-level KSY/Yang/H90 target",
            gate_artifact=x1_8112_gate,
            candidate_command=x1_8112_candidate_command("odd_value_policy_yes_no_cross_level"),
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            first_missing_clause="X_1(16) relation or X_1(8112) fiber-product theorem",
            value_stage_closed=True,
            policy_unblocked=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="x1_8112_bridge_no_x16_specialization",
            accepted_input="j-glued X_1(8112) bridge theorem for the odd-level target",
            gate_artifact=x1_8112_gate,
            candidate_command=x1_8112_candidate_command(
                "x1_8112_bridge_no_x16_specialization",
                fiber_product=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            value_stage_closed=True,
            policy_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="x16_surface_policy_missing",
            accepted_input="X_1(8112) theorem specialized to X_1(16) y, A, and xP16",
            gate_artifact=x1_8112_gate,
            candidate_command=x1_8112_candidate_command(
                "x16_surface_policy_missing",
                fiber_product=True,
                x16_relation=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            value_stage_closed=True,
            policy_unblocked=False,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="x16_surface_halving_missing",
            accepted_input="DANGER3-framed X_1(16) y, A, and xP16 surface",
            gate_artifact=x1_8112_gate,
            candidate_command=x1_8112_candidate_command(
                "x16_surface_halving_missing",
                fiber_product=True,
                x16_relation=True,
                danger3_framing=True,
            ),
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            first_missing_clause="valid halving chain from xP16 to concrete x0",
            value_stage_closed=True,
            policy_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=False,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="x_coordinate_chain_vpp_missing",
            accepted_input="A, xP16, and checkable x_4..x_42 halving chain",
            gate_artifact=halving_gate,
            candidate_command="run the halving-certificate payload gate and inspect x_coordinate_chain row",
            expected_decision="checkable_x_chain_vpp_missing",
            first_missing_clause="official vpp.py verification",
            value_stage_closed=True,
            policy_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=True,
            submission_ready=False,
            must_not_accept_as_submission=True,
            ok=True,
        ),
        AcceptanceLadderRow(
            name="verified_pomerance_triple",
            accepted_input="concrete p25 (p,A,x0) triple verified by official vpp.py",
            gate_artifact=submission_gate,
            candidate_command=(
                "python3 research/p25/"
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py "
                "--p 10000000000000000000000013 --A <A> --x0 <x0>"
            ),
            expected_decision="closing_vpp_verified_submission",
            first_missing_clause="none",
            value_stage_closed=True,
            policy_unblocked=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=True,
            extraction_ready=True,
            submission_ready=True,
            must_not_accept_as_submission=False,
            ok=True,
        ),
    )


def profile_acceptance_ladder() -> AcceptanceLadderProfile:
    source_route = profile_source_route_packet()
    rows = ladder_rows()
    target_note = RESEARCH / "p25_ksy_y_conductor39_value_theorem_target_packet_20260614.md"
    halving_note = RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md"
    danger3_gate = (
        RESEARCH
        / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate.py"
    )
    extraction_gate = RESEARCH / "p25_ksy_y_danger3_extraction_surface_gate.py"
    x1_8112_gate = RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py"
    submission_gate = (
        RESEARCH
        / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py"
    )
    target_marker = marker_present(
        target_note,
        "ksy_y_conductor39_value_theorem_target_packet_rows=1/1",
    )
    halving_marker = marker_present(
        halving_note,
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    )
    danger3_present = artifact_present(danger3_gate)
    extraction_present = artifact_present(extraction_gate)
    x1_8112_present = artifact_present(x1_8112_gate)
    submission_present = artifact_present(submission_gate)
    count_ladder = (75, 300, 12, 312, 156)
    source_commands = source_route.local_candidate_commands
    x1_commands = sum("p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py" in row.candidate_command for row in rows)
    non_submission = sum(row.must_not_accept_as_submission for row in rows)
    value_closed = sum(row.value_stage_closed for row in rows)
    policy_unblocked = sum(row.policy_unblocked for row in rows)
    cross_level = sum(row.cross_level_bridge_identified for row in rows)
    x16_surface = sum(row.x16_surface_reached for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    row_ok = (
        source_route.row_ok
        and target_marker
        and danger3_present
        and submission_present
        and extraction_present
        and x1_8112_present
        and halving_marker
        and len(rows) == 7
        and source_commands == 4
        and x1_commands == 4
        and non_submission == 6
        and value_closed == 7
        and policy_unblocked == 5
        and cross_level == 5
        and x16_surface == 4
        and extraction_ready == 2
        and submission_ready == 1
        and tuple(row.expected_decision for row in rows)
        == (
            "source_theorem_closed_policy_or_framing_missing",
            "upstream_odd_value_no_cross_level_bridge",
            "cross_level_target_identified_specialization_missing",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "checkable_x_chain_vpp_missing",
            "closing_vpp_verified_submission",
        )
        and all(row.gate_artifact.exists() and row.gate_artifact.stat().st_size > 0 for row in rows)
        and all(row.ok for row in rows)
        and count_ladder == (75, 300, 12, 312, 156)
    )
    return AcceptanceLadderProfile(
        source_route_packet_ok=source_route.row_ok,
        target_packet_marker_present=target_marker,
        danger3_framing_gate_present=danger3_present,
        submission_extraction_gate_present=submission_present,
        extraction_surface_gate_present=extraction_present,
        x1_8112_intake_gate_present=x1_8112_present,
        halving_payload_marker_present=halving_marker,
        count_ladder=count_ladder,
        ladder_rows=rows,
        source_route_candidate_commands=source_commands,
        x1_8112_candidate_commands=x1_commands,
        non_submission_rows=non_submission,
        value_stage_closed_rows=value_closed,
        policy_unblocked_rows=policy_unblocked,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_acceptance_ladder()
    print("p25 KSY-y conductor-39 to DANGER3 acceptance-ladder gate")
    print("dependency_gates")
    print(f"  source_route_packet_ok={int(profile.source_route_packet_ok)}")
    print(f"  target_packet_marker_present={int(profile.target_packet_marker_present)}")
    print(f"  danger3_framing_gate_present={int(profile.danger3_framing_gate_present)}")
    print(f"  submission_extraction_gate_present={int(profile.submission_extraction_gate_present)}")
    print(f"  extraction_surface_gate_present={int(profile.extraction_surface_gate_present)}")
    print(f"  x1_8112_intake_gate_present={int(profile.x1_8112_intake_gate_present)}")
    print(f"  halving_payload_marker_present={int(profile.halving_payload_marker_present)}")
    print(f"  count_ladder={profile.count_ladder}")
    print("ladder_rows")
    for row in profile.ladder_rows:
        print(
            "  "
            f"{row.name}: decision={row.expected_decision} "
            f"value={int(row.value_stage_closed)} policy={int(row.policy_unblocked)} "
            f"x8112={int(row.cross_level_bridge_identified)} "
            f"x16={int(row.x16_surface_reached)} "
            f"extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    input={row.accepted_input}")
        print(f"    gate={row.gate_artifact}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  source_route_candidate_commands={profile.source_route_candidate_commands}")
    print(f"  x1_8112_candidate_commands={profile.x1_8112_candidate_commands}")
    print(f"  non_submission_rows={profile.non_submission_rows}")
    print(f"  value_stage_closed_rows={profile.value_stage_closed_rows}")
    print(f"  policy_unblocked_rows={profile.policy_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  value_theorem_win_is_real_but_not_submission=1")
    print("  policy_yes_still_needs_x1_8112_and_x16_extraction=1")
    print("  x_chain_certificate_still_needs_official_vpp=1")
    print("  only_vpp_verified_triple_is_submission_ready=1")
    print(f"ksy_y_conductor39_to_danger3_acceptance_ladder_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 to DANGER3 acceptance ladder regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
