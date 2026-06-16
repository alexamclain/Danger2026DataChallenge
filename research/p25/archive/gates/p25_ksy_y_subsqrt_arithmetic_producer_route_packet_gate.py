#!/usr/bin/env python3
"""Arithmetic-producer route packet for the subsqrt p25 moonshot.

The universal producer intake proves that several tiny finite payloads are
equivalent entry points to the KSY/Yang/Hilbert-90 spine.  This packet records
what would make one of those payloads a theorem-producing moonshot checkpoint
rather than a finite replay, and routes each accepted hit to the next DANGER3
obligation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_subsqrt_moonshot_budget_ladder_gate import (
    profile_subsqrt_moonshot_budget_ladder,
)
from p25_ksy_y_curved_corner_minimal_closing_ask_packet_gate import (
    profile_curved_corner_minimal_closing_ask_packet,
)
from p25_laneB_robert_ksy_theta2_universal_producer_intake import (
    default_universal_producer_intake_profile,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    classify_claim,
    ClosingTheoremClaim,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate import (
    SourceClaim,
    classify_claim as classify_source_claim,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate import (
    CornerProducerCandidate,
    classify_candidate as classify_corner_producer_candidate,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class ArithmeticProducerRouteRow:
    name: str
    finite_interface: str
    finite_payload_size: int
    candidate_command: str
    finite_payload_accepts: bool
    theorem_claim_shape: str
    source_theorem_closes_if_proved: bool
    value_route: bool
    danger3_remaining: bool
    extraction_remaining: bool
    submission_ready: bool
    first_missing_clause: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ArithmeticProducerRoutePacket:
    budget_ladder_ok: bool
    universal_intake_ok: bool
    curved_corner_closing_ask_ok: bool
    current_max_budget: int
    current_max_margin_floor: int
    route_rows: tuple[ArithmeticProducerRouteRow, ...]
    route_count: int
    universal_candidate_commands: int
    source_claim_commands: int
    closing_obligation_commands: int
    finite_payload_accept_rows: int
    source_theorem_closing_rows: int
    value_route_rows: int
    producer_theorem_missing_rows: int
    danger3_remaining_rows: int
    extraction_remaining_rows: int
    submission_ready_rows: int
    all_routes_subsqrt: bool
    row_ok: bool


def universal_command(mode: str, args: str) -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py "
        f"--mode {mode} {args}"
    )


def source_claim_command() -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py "
        "--candidate --name subsqrt_period156_value_theorem "
        "--anchor siegel_robert_value_units --output-kind value "
        "--exact-product --mixed-graph --finite-field-identity --period-156"
    )


def curved_corner_command() -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py "
        "--candidate --name curved_corner_source_shape "
        "--theorem-body --triangle --curvature --half-bridge-edge "
        "--full-k-trace --raw-relation --raw-kernel-trace --primitive-c169 "
        "--active-c169-lift --quadratic-fiber --nonsplit-carry --unit-triangle"
    )


def closing_command(name: str, *, output_kind: str, extraction: bool = False, vpp: bool = False) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py",
        "--candidate",
        f"--name {name}",
        "--source-family subsqrt_arithmetic_producer",
        f"--output-kind {output_kind}",
        "--exact-p",
        "--mixed-graph",
        "--equal-weight",
        "--orientation",
        "--arithmetic-source",
        "--finite-identity",
        "--period-156",
    ]
    if extraction:
        parts.extend(("--danger3-framing", "--extraction"))
    if vpp:
        parts.append("--vpp-verified-triple")
    return " ".join(parts)


def route_rows() -> tuple[ArithmeticProducerRouteRow, ...]:
    universal = default_universal_producer_intake_profile()
    accepted = {row.mode: row for row in universal.accepted_rows}

    exact_product_decision = classify_claim(
        ClosingTheoremClaim(
            name="subsqrt_exact_product_policy_unknown",
            source_family="subsqrt_arithmetic_producer",
            emits_exact_p=True,
            preserves_mixed_graph=True,
            equal_weight_atoms=True,
            orientation_recorded=True,
            arithmetic_source_theorem=True,
            output_kind="divisor-additive",
            finite_field_identity_for_p=True,
            period_156_context=True,
            danger3_policy_or_non_cm_framing=False,
            extraction_to_A_x0=False,
            concrete_vpp_verified_triple=False,
        )
    )
    value_decision = classify_source_claim(
        SourceClaim(
            name="subsqrt_period156_value_theorem",
            anchor_name="siegel_robert_value_units",
            output_kind="value",
            exact_product_p=True,
            mixed_graph_selector=True,
            period_156_context=True,
            finite_field_identity=True,
            divisor_or_additive=False,
            policy_accepts_finite_identity=False,
        )
    )
    extraction_decision = classify_claim(
        ClosingTheoremClaim(
            name="subsqrt_extraction_ready_unverified",
            source_family="subsqrt_arithmetic_producer",
            emits_exact_p=True,
            preserves_mixed_graph=True,
            equal_weight_atoms=True,
            orientation_recorded=True,
            arithmetic_source_theorem=True,
            output_kind="period-value",
            finite_field_identity_for_p=True,
            period_156_context=True,
            danger3_policy_or_non_cm_framing=True,
            extraction_to_A_x0=True,
            concrete_vpp_verified_triple=False,
        )
    )
    verified_decision = classify_claim(
        ClosingTheoremClaim(
            name="subsqrt_verified_pomerance_triple",
            source_family="subsqrt_arithmetic_producer",
            emits_exact_p=True,
            preserves_mixed_graph=True,
            equal_weight_atoms=True,
            orientation_recorded=True,
            arithmetic_source_theorem=True,
            output_kind="period-value",
            finite_field_identity_for_p=True,
            period_156_context=True,
            danger3_policy_or_non_cm_framing=True,
            extraction_to_A_x0=True,
            concrete_vpp_verified_triple=True,
        )
    )
    curved_corner_decision = classify_corner_producer_candidate(
        CornerProducerCandidate(
            name="curved_corner_source_shape",
            theorem_body_verified=True,
            exact_curved_row_triangle=True,
            primitive_newton_curvature=True,
            recorded_half_bridge_edge=True,
            full_order25_k_trace=True,
            raw_d3_y_relation=True,
            raw_kernel_trace_accounted=True,
            primitive_c169_motion=True,
            active_c169_lift_selected=True,
            quadratic_fiber_section=True,
            nonsplit_c169_carry_transport=True,
            unit_triangle_law=True,
            finite_value_or_divisor_theorem=False,
            period156_context=False,
            arithmetic_source_theorem=False,
            danger3_framing=False,
            same_j_x18112_bridge=False,
            x16_surface=False,
            concrete_A_x0=False,
            official_vpp=False,
        )
    )

    return (
        ArithmeticProducerRouteRow(
            name="hilbert90_signs_source_theorem",
            finite_interface="hilbert90-signs eps=1 branch=-1",
            finite_payload_size=accepted["hilbert90-signs"].finite_input_size,
            candidate_command=universal_command("hilbert90-signs", "--eps 1 --branch -1"),
            finite_payload_accepts=accepted["hilbert90-signs"].ok,
            theorem_claim_shape="source theorem emits the two Hilbert-90 signs from a legal KSY/Yang/H0 producer",
            source_theorem_closes_if_proved=False,
            value_route=False,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause="arithmetic proof producing the signs, not only a finite replay",
            first_falsifier="signs are asserted without source theorem, or fail universal intake",
            ok=accepted["hilbert90-signs"].ok,
        ),
        ArithmeticProducerRouteRow(
            name="source_packet_source_theorem",
            finite_interface="six signed source-packet cells plus primitive K",
            finite_payload_size=accepted["source-packet"].finite_input_size,
            candidate_command=universal_command(
                "source-packet",
                "--packet research/p25/producer_payload_fixtures/source_packet_target.txt --k-multiplier 1",
            ),
            finite_payload_accepts=accepted["source-packet"].ok,
            theorem_claim_shape="source theorem emits the exact six-cell C3 x C169 packet and primitive K trace",
            source_theorem_closes_if_proved=False,
            value_route=False,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause="challenge-legal arithmetic producer for the packet",
            first_falsifier="q-cycle coordinates, nonprimitive K, wrong D, or no theorem source",
            ok=accepted["source-packet"].ok,
        ),
        ArithmeticProducerRouteRow(
            name="quotient_factor_source_theorem",
            finite_interface="base=(1,25), D=(1,3), T=(2,113), primitive K",
            finite_payload_size=accepted["quotient-factor"].finite_input_size,
            candidate_command=universal_command(
                "quotient-factor",
                "--base-right-class 1 --base-c 25 --d-right-class 1 --d-c 3 "
                "--t-right-class 2 --t-c 113 --k-multiplier 1",
            ),
            finite_payload_accepts=accepted["quotient-factor"].ok,
            theorem_claim_shape="source theorem emits the quotient factor classes that force the finite spine",
            source_theorem_closes_if_proved=False,
            value_route=False,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause="arithmetic theorem selecting these classes with orientation",
            first_falsifier="wrong quotient D, T not tied to reflection center, or primitive K absent",
            ok=accepted["quotient-factor"].ok,
        ),
        ArithmeticProducerRouteRow(
            name="curved_corner_source_theorem",
            finite_interface=(
                "curved Newton triangle, recorded 197/310 edge, full K trace, "
                "raw D^3=Y with kernel trace, active C169 lift, quadratic fiber, nonsplit carry"
                ", unit triangle"
            ),
            finite_payload_size=75,
            candidate_command=curved_corner_command(),
            finite_payload_accepts=curved_corner_decision.finite_shape_reached,
            theorem_claim_shape=(
                "arithmetic theorem emits a finite value/divisor identity for the curved "
                "K-traced Hilbert-90 corner payload"
            ),
            source_theorem_closes_if_proved=False,
            value_route=False,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause=curved_corner_decision.first_missing_or_falsifier,
            first_falsifier=(
                "wrong source triangle, linear/AP graph, wrong half-edge, sparse K subtrace, "
                "raw D^3=Y failure, omitted kernel trace, C13/right-kernel-only lift, "
                "generic primitive C169 lift, affine/Teichmuller fiber shortcut, "
                "split no-carry transport, or passive/wrong unit triangle"
            ),
            ok=(
                curved_corner_decision.decision
                == "helper_only_curved_triangle_value_theorem_missing"
            ),
        ),
        ArithmeticProducerRouteRow(
            name="compact_theta2_exact_product_theorem",
            finite_interface="compact theta2 center_base=(44,166), half_shift=(56,28)",
            finite_payload_size=accepted["compact-theta2"].finite_input_size,
            candidate_command=universal_command(
                "compact-theta2",
                "--center-right 44 --center-c 166 --half-right 56 --half-c 28 --invert",
            ),
            finite_payload_accepts=accepted["compact-theta2"].ok,
            theorem_claim_shape="arithmetic theorem emits exact P/theta2 payload, mixed graph, equal weights, and orientation",
            source_theorem_closes_if_proved=exact_product_decision.source_theorem_closed,
            value_route=False,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause=exact_product_decision.first_missing_clause,
            first_falsifier="finite compact payload without arithmetic source theorem or missing DANGER3 framing",
            ok=accepted["compact-theta2"].ok
            and exact_product_decision.decision == "source_theorem_closed_policy_or_framing_missing",
        ),
        ArithmeticProducerRouteRow(
            name="period156_value_source_theorem",
            finite_interface="exact finite-field value identity for P with period-156 context",
            finite_payload_size=46800,
            candidate_command=source_claim_command(),
            finite_payload_accepts=value_decision.decision == "closing_value_identity_with_period_156",
            theorem_claim_shape="value theorem emits exact P over F_p with mixed graph and support-period branch context",
            source_theorem_closes_if_proved=value_decision.closes_route,
            value_route=True,
            danger3_remaining=True,
            extraction_remaining=True,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing after value-source closure",
            first_falsifier=value_decision.first_missing_clause,
            ok=value_decision.closes_route,
        ),
        ArithmeticProducerRouteRow(
            name="extraction_ready_unverified_triple",
            finite_interface="DANGER3-framed theorem plus concrete A,x0 extraction",
            finite_payload_size=0,
            candidate_command=closing_command(
                "subsqrt_extraction_ready_unverified",
                output_kind="period-value",
                extraction=True,
            ),
            finite_payload_accepts=extraction_decision.extraction_ready,
            theorem_claim_shape="same theorem route has produced concrete A,x0 but vpp.py has not been run",
            source_theorem_closes_if_proved=extraction_decision.source_theorem_closed,
            value_route=True,
            danger3_remaining=False,
            extraction_remaining=False,
            submission_ready=False,
            first_missing_clause=extraction_decision.first_missing_clause,
            first_falsifier="official vpp.py does not verify the triple",
            ok=extraction_decision.decision == "ready_to_extract_and_verify_concrete_triple",
        ),
        ArithmeticProducerRouteRow(
            name="verified_pomerance_triple",
            finite_interface="official p25 (p,A,x0) triple",
            finite_payload_size=0,
            candidate_command=closing_command(
                "subsqrt_verified_pomerance_triple",
                output_kind="period-value",
                extraction=True,
                vpp=True,
            ),
            finite_payload_accepts=verified_decision.submission_ready,
            theorem_claim_shape="official vpp.py verified concrete p25 triple",
            source_theorem_closes_if_proved=verified_decision.source_theorem_closed,
            value_route=True,
            danger3_remaining=False,
            extraction_remaining=False,
            submission_ready=True,
            first_missing_clause=verified_decision.first_missing_clause,
            first_falsifier="none if vpp.py and certificate verify",
            ok=verified_decision.submission_ready,
        ),
    )


def profile_arithmetic_producer_route_packet() -> ArithmeticProducerRoutePacket:
    budget = profile_subsqrt_moonshot_budget_ladder()
    universal = default_universal_producer_intake_profile()
    curved_corner_closing = profile_curved_corner_minimal_closing_ask_packet()
    rows = route_rows()
    universal_commands = sum("universal_producer_intake.py" in row.candidate_command for row in rows)
    source_claim_commands = sum("source_claim_intake_gate.py" in row.candidate_command for row in rows)
    closing_commands = sum("closing_theorem_obligation_gate.py" in row.candidate_command for row in rows)
    curved_corner_commands = sum("corner_producer_intake_gate.py" in row.candidate_command for row in rows)
    finite_accepts = sum(row.finite_payload_accepts for row in rows)
    source_closing = sum(row.source_theorem_closes_if_proved for row in rows)
    value_routes = sum(row.value_route for row in rows)
    producer_missing = sum(
        any(term in row.first_missing_clause.lower() for term in ("theorem", "proof", "producer"))
        for row in rows
    )
    danger3_remaining = sum(row.danger3_remaining for row in rows)
    extraction_remaining = sum(row.extraction_remaining for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    row_ok = (
        budget.row_ok
        and universal.row_ok
        and curved_corner_closing.row_ok
        and budget.current_max_budget == 46800
        and budget.current_max_margin_floor == 67570035
        and len(rows) == 8
        and universal_commands == 4
        and curved_corner_commands == 1
        and source_claim_commands == 1
        and closing_commands == 2
        and finite_accepts == 8
        and source_closing == 4
        and value_routes == 3
        and producer_missing == 4
        and danger3_remaining == 6
        and extraction_remaining == 6
        and submission_ready == 1
        and all(0 <= row.finite_payload_size < budget.sqrt_floor for row in rows)
        and all(row.ok for row in rows)
        and not any(row.submission_ready for row in rows[:-1])
    )
    return ArithmeticProducerRoutePacket(
        budget_ladder_ok=budget.row_ok,
        universal_intake_ok=universal.row_ok,
        curved_corner_closing_ask_ok=curved_corner_closing.row_ok,
        current_max_budget=budget.current_max_budget,
        current_max_margin_floor=budget.current_max_margin_floor,
        route_rows=rows,
        route_count=len(rows),
        universal_candidate_commands=universal_commands,
        source_claim_commands=source_claim_commands,
        closing_obligation_commands=closing_commands,
        finite_payload_accept_rows=finite_accepts,
        source_theorem_closing_rows=source_closing,
        value_route_rows=value_routes,
        producer_theorem_missing_rows=producer_missing,
        danger3_remaining_rows=danger3_remaining,
        extraction_remaining_rows=extraction_remaining,
        submission_ready_rows=submission_ready,
        all_routes_subsqrt=budget.all_current_budgets_below_sqrt,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_arithmetic_producer_route_packet()
    print("p25 KSY-y subsqrt arithmetic-producer route packet gate")
    print("dependencies")
    print(f"  budget_ladder_ok={int(profile.budget_ladder_ok)}")
    print(f"  universal_intake_ok={int(profile.universal_intake_ok)}")
    print(f"  curved_corner_closing_ask_ok={int(profile.curved_corner_closing_ask_ok)}")
    print(f"  current_max_budget={profile.current_max_budget}")
    print(f"  current_max_margin_floor={profile.current_max_margin_floor}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: size={row.finite_payload_size} finite={int(row.finite_payload_accepts)} "
            f"source_closes={int(row.source_theorem_closes_if_proved)} "
            f"value={int(row.value_route)} danger3={int(row.danger3_remaining)} "
            f"extraction={int(row.extraction_remaining)} submission={int(row.submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    interface={row.finite_interface}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  route_count={profile.route_count}")
    print(f"  universal_candidate_commands={profile.universal_candidate_commands}")
    print(f"  source_claim_commands={profile.source_claim_commands}")
    print(f"  closing_obligation_commands={profile.closing_obligation_commands}")
    print(f"  finite_payload_accept_rows={profile.finite_payload_accept_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  value_route_rows={profile.value_route_rows}")
    print(f"  producer_theorem_missing_rows={profile.producer_theorem_missing_rows}")
    print(f"  danger3_remaining_rows={profile.danger3_remaining_rows}")
    print(f"  extraction_remaining_rows={profile.extraction_remaining_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  all_routes_subsqrt={int(profile.all_routes_subsqrt)}")
    print("interpretation")
    print("  universal_intake_pass_is_finite_payload_compatibility_not_a_source_proof=1")
    print("  a_real_moonshot_hit_must_name_an_arithmetic_producer_for_one_tiny_interface=1")
    print("  curved_corner_route_uses_unit_triangle_minimal_closing_ask=1")
    print("  source_theorem_closure_still_routes_to_DANGER3_framing_extraction_and_vpp=1")
    print(f"ksy_y_subsqrt_arithmetic_producer_route_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("subsqrt arithmetic-producer route packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
