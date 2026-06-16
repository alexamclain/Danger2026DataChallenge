#!/usr/bin/env python3
"""Source-route packet for p25 exact value theorems with period-156 context.

The value-side queue says a finite-field value theorem is useful only when it
emits the exact p25 product P, preserves the mixed graph, and carries
period-156 branch/root/telescoping context.  This lightweight packet turns that
rule into local candidate commands and downstream acceptance states.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


RESEARCH = Path("research/p25")
P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780


@dataclass(frozen=True)
class Period156ValueRouteRow:
    name: str
    route_type: str
    accepted_payload: str
    router_artifact: Path
    candidate_command: str
    expected_decision: str
    first_missing_clause: str
    closes_value_source_stage: bool
    support_period_root_unique: bool
    rejected_shadow: bool
    still_needs_danger3_framing: bool
    still_needs_extraction: bool
    submission_ready: bool
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class Period156ValueSourceRoutePacket:
    p: int
    support_period: int
    support_root_gcd_fp_star: int
    ambient_period: int
    ambient_root_gcd_fp_star: int
    prerequisite_markers_present: int
    route_rows: tuple[Period156ValueRouteRow, ...]
    route_count: int
    local_candidate_commands: int
    closing_value_rows: int
    rejected_shadow_rows: int
    danger3_remaining_rows: int
    extraction_remaining_rows: int
    submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def source_claim_command(
    name: str,
    *,
    anchor: str = "siegel_robert_value_units",
    exact: bool = False,
    graph: bool = False,
    finite: bool = False,
    period: bool = False,
    output_kind: str = "value",
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--anchor {anchor}",
        f"--output-kind {output_kind}",
    ]
    if exact:
        parts.append("--exact-product")
    if graph:
        parts.append("--mixed-graph")
    if finite:
        parts.append("--finite-field-identity")
    if period:
        parts.append("--period-156")
    return " ".join(parts)


def theorem_hit_command(
    name: str,
    *,
    output_type: str = "raw-value",
    period: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py",
        f"--output-type {output_type}",
        "--center-right 47",
        "--center-c 28",
        "--d-right 22",
        "--d-c 3",
        "--k-multiplier 1",
    ]
    if period:
        parts.append("--period-156-context")
    # The router itself does not take a name; keep the row name in the note/gate.
    _ = name
    return " ".join(parts)


def route_rows() -> tuple[Period156ValueRouteRow, ...]:
    source_router = RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py"
    theorem_router = RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py"
    period_gate = RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py"
    extraction_gate = RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_gate.py"
    return (
        Period156ValueRouteRow(
            name="source_exact_p_value_with_period156",
            route_type="source_claim",
            accepted_payload="exact finite-field value identity for P with mixed graph and period-156 context",
            router_artifact=source_router,
            candidate_command=source_claim_command(
                "source_exact_p_value_with_period156",
                exact=True,
                graph=True,
                finite=True,
                period=True,
            ),
            expected_decision="closing_value_identity_with_period_156",
            first_missing_clause="none in value-source stage",
            closes_value_source_stage=True,
            support_period_root_unique=True,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="not exact P, missing mixed graph, no finite-field identity, or no period-156 context",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="raw_value_theorem_with_period156",
            route_type="theorem_hit_router",
            accepted_payload="raw C/D/K finite-field value theorem with period-156 theta2 context",
            router_artifact=theorem_router,
            candidate_command=theorem_hit_command(
                "raw_value_theorem_with_period156",
                output_type="raw-value",
                period=True,
            ),
            expected_decision="accept",
            first_missing_clause="none in raw value router",
            closes_value_source_stage=True,
            support_period_root_unique=True,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="raw geometry fails C=(47,28), D=(22,3), primitive K, or period context is absent",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="bare_exact_value_without_period156",
            route_type="source_claim",
            accepted_payload="exact P finite-field value but no branch/root/telescoping context",
            router_artifact=source_router,
            candidate_command=source_claim_command(
                "bare_exact_value_without_period156",
                exact=True,
                graph=True,
                finite=True,
            ),
            expected_decision="conditional_missing_period_156_context",
            first_missing_clause="period-156 branch/root/telescoping context",
            closes_value_source_stage=False,
            support_period_root_unique=False,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="value theorem leaves the F_p^* branch/root unspecified",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="period156_context_without_exact_p",
            route_type="source_claim",
            accepted_payload="period-156 vocabulary or telescoping without the exact product P",
            router_artifact=source_router,
            candidate_command=source_claim_command(
                "period156_context_without_exact_p",
                graph=True,
                finite=True,
                period=True,
            ),
            expected_decision="conditional_missing_exact_product",
            first_missing_clause="exact product P with C=(47,28), D=(22,3), K=(57,0)",
            closes_value_source_stage=False,
            support_period_root_unique=True,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="period context is attached to the wrong object or a family rather than P",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="ambient_780_value_only",
            route_type="theorem_hit_router",
            accepted_payload="ambient 780-period value without support-period descent",
            router_artifact=theorem_router,
            candidate_command=theorem_hit_command(
                "ambient_780_value_only",
                output_type="ambient-value",
                period=False,
            ),
            expected_decision="reject",
            first_missing_clause="ambient 780-period value route has mu_11 ambiguity",
            closes_value_source_stage=False,
            support_period_root_unique=False,
            rejected_shadow=True,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="gcd(4^780 - 1, p - 1) = 11",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="finite_verifier_payload_without_source",
            route_type="period_value_upgrade",
            accepted_payload="finite verifier payload with period context but no arithmetic source theorem",
            router_artifact=period_gate,
            candidate_command="run period-value upgrade gate and inspect finite_verifier_without_source_theorem row",
            expected_decision="conditional_finite_verifier_without_arithmetic_producer",
            first_missing_clause="challenge-legal arithmetic producer theorem",
            closes_value_source_stage=False,
            support_period_root_unique=True,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="payload is only a verifier target, not a source theorem",
            ok=True,
        ),
        Period156ValueRouteRow(
            name="downstream_after_value_source_closure",
            route_type="acceptance_ladder",
            accepted_payload="value-source theorem closed; continue to DANGER3 framing, cross-level bridge, X1(16), halving, vpp",
            router_artifact=extraction_gate,
            candidate_command="run conductor-39 to DANGER3 acceptance ladder and inspect non-submission rows",
            expected_decision="source theorem closed but not submission-ready",
            first_missing_clause="DANGER3 framing, X_1(16) extraction, halving chain, and official vpp.py",
            closes_value_source_stage=True,
            support_period_root_unique=True,
            rejected_shadow=False,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_falsifier="claim treats a value theorem as a verified Pomerance triple",
            ok=True,
        ),
    )


def profile_period156_value_source_route_packet() -> Period156ValueSourceRoutePacket:
    rows = route_rows()
    prerequisite_markers = sum(
        (
            marker_present(
                RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade.md",
                "robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md",
                "ksy_y_siegel_robert_period_value_primary_source_scout_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_20260614.md",
                "ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1",
            ),
        )
    )
    support_gcd = gcd(4**SUPPORT_PERIOD - 1, P25 - 1)
    ambient_gcd = gcd(4**AMBIENT_PERIOD - 1, P25 - 1)
    local_commands = sum(" --candidate " in row.candidate_command or "--output-type " in row.candidate_command for row in rows)
    closing = sum(row.closes_value_source_stage for row in rows)
    rejected = sum(row.rejected_shadow for row in rows)
    danger3_remaining = sum(row.still_needs_danger3_framing for row in rows)
    extraction_remaining = sum(row.still_needs_extraction for row in rows)
    submission = sum(row.submission_ready for row in rows)
    row_ok = (
        P25 == 10000000000000000000000013
        and SUPPORT_PERIOD == 156
        and AMBIENT_PERIOD == 780
        and support_gcd == 1
        and ambient_gcd == 11
        and prerequisite_markers == 3
        and len(rows) == 7
        and local_commands == 5
        and closing == 3
        and rejected == 1
        and danger3_remaining == 7
        and extraction_remaining == 7
        and submission == 0
        and tuple(row.expected_decision for row in rows)
        == (
            "closing_value_identity_with_period_156",
            "accept",
            "conditional_missing_period_156_context",
            "conditional_missing_exact_product",
            "reject",
            "conditional_finite_verifier_without_arithmetic_producer",
            "source theorem closed but not submission-ready",
        )
        and all(row.router_artifact.exists() and row.router_artifact.stat().st_size > 0 for row in rows)
        and all(row.ok for row in rows)
    )
    return Period156ValueSourceRoutePacket(
        p=P25,
        support_period=SUPPORT_PERIOD,
        support_root_gcd_fp_star=support_gcd,
        ambient_period=AMBIENT_PERIOD,
        ambient_root_gcd_fp_star=ambient_gcd,
        prerequisite_markers_present=prerequisite_markers,
        route_rows=rows,
        route_count=len(rows),
        local_candidate_commands=local_commands,
        closing_value_rows=closing,
        rejected_shadow_rows=rejected,
        danger3_remaining_rows=danger3_remaining,
        extraction_remaining_rows=extraction_remaining,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_period156_value_source_route_packet()
    print("p25 KSY-y period-156 value source-route packet gate")
    print("denominators")
    print(f"  support_period={profile.support_period}")
    print(f"  support_root_gcd_Fp_star={profile.support_root_gcd_fp_star}")
    print(f"  ambient_period={profile.ambient_period}")
    print(f"  ambient_root_gcd_Fp_star={profile.ambient_root_gcd_fp_star}")
    print(f"prerequisite_markers_present={profile.prerequisite_markers_present}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: type={row.route_type} decision={row.expected_decision} "
            f"closes_value={int(row.closes_value_source_stage)} "
            f"unique_root={int(row.support_period_root_unique)} "
            f"rejected={int(row.rejected_shadow)} "
            f"danger3={int(row.still_needs_danger3_framing)} "
            f"extraction={int(row.still_needs_extraction)} "
            f"submission={int(row.submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    payload={row.accepted_payload}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    router={row.router_artifact}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  route_count={profile.route_count}")
    print(f"  local_candidate_commands={profile.local_candidate_commands}")
    print(f"  closing_value_rows={profile.closing_value_rows}")
    print(f"  rejected_shadow_rows={profile.rejected_shadow_rows}")
    print(f"  danger3_remaining_rows={profile.danger3_remaining_rows}")
    print(f"  extraction_remaining_rows={profile.extraction_remaining_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  exact_value_route_closes_only_with_exact_P_graph_finite_identity_period156=1")
    print("  ambient_780_value_only_has_mu11_ambiguity=1")
    print("  value_source_closure_still_needs_danger3_extraction_and_vpp=1")
    print(f"ksy_y_period156_value_source_route_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("period-156 value source-route packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
