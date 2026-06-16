#!/usr/bin/env python3
"""Source-route packet for the conductor-39 value-theorem targets.

The value-theorem target packet names four finite targets.  This lightweight
gate tells a theorem scout or expert conversation where to route each target:
allowed source families, first falsifier, local candidate command, and the
expected intake decision before DANGER3 framing/extraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class SourceRouteRow:
    name: str
    target_row: str
    accepted_source_families: tuple[str, ...]
    first_falsifier: str
    router_artifact: Path
    candidate_command: str
    expected_pre_danger3_decision: str
    expected_first_missing_clause: str
    closes_value_stage: bool
    still_needs_danger3: bool
    still_needs_extraction: bool
    ok: bool


@dataclass(frozen=True)
class SourceRoutePacket:
    target_packet_artifact: Path
    source_routes: tuple[SourceRouteRow, ...]
    router_artifacts_present: int
    route_rows: int
    value_closing_routes: int
    danger3_remaining_rows: int
    extraction_remaining_rows: int
    local_candidate_commands: int
    row_ok: bool


def conductor39_candidate_command(source_object: str, output_kind: str = "divisor-additive") -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py "
        f"--candidate --name {source_object}_value_theorem_hit "
        f"--source-object {source_object} --output-kind {output_kind} "
        "--theorem-body --emits-conductor39 --mixed-tensor --legal-unit "
        "--yang-lift --descent --finite-or-divisor --period-156"
    )


def h90_candidate_command(target_object: str, output_kind: str = "divisor-additive") -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py "
        f"--candidate --name {target_object}_value_theorem_hit "
        f"--target-object {target_object} --output-kind {output_kind} "
        "--theorem-body --exact-target --bridge-spine --legal-yang-h90 "
        "--boundary-context --finite-or-divisor --period-156 --arithmetic-source"
    )


def source_routes() -> tuple[SourceRouteRow, ...]:
    conductor_router = RESEARCH / "p25_ksy_y_conductor39_source_theorem_intake_gate.py"
    h90_router = RESEARCH / "p25_ksy_y_h90_value_theorem_intake_gate.py"
    return (
        SourceRouteRow(
            name="uchi_value_or_divisor_route",
            target_row="conductor39_U_chi_value_or_divisor",
            accepted_source_families=(
                "Yang/Yu X_1(39) modular-unit identity",
                "Hilbert-90 or twisted-trace descent for U_chi",
                "finite-field identity reframing of a CM/unit theorem",
            ),
            first_falsifier=(
                "source product legality, ray-class generation, projection, or "
                "formal unit vocabulary without finite-field value/divisor identity"
            ),
            router_artifact=conductor_router,
            candidate_command=conductor39_candidate_command("U_chi"),
            expected_pre_danger3_decision="source_theorem_closed_policy_or_framing_missing",
            expected_first_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_value_stage=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            ok=True,
        ),
        SourceRouteRow(
            name="period_norm_w_route",
            target_row="period_norm_W_or_Norm156_Y507",
            accepted_source_families=(
                "Yang 13-fiber distribution identity",
                "period-norm value/divisor theorem for Y_507",
                "conductor-39 W=6*U_chi theorem with period-156 context",
            ),
            first_falsifier=(
                "level-507 statement without conductor-39 descent, Yang lift, "
                "or period-156 branch/telescoping context"
            ),
            router_artifact=conductor_router,
            candidate_command=conductor39_candidate_command("W"),
            expected_pre_danger3_decision="source_theorem_closed_policy_or_framing_missing",
            expected_first_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_value_stage=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            ok=True,
        ),
        SourceRouteRow(
            name="canonical_h0_route",
            target_row="canonical_H0_or_translate",
            accepted_source_families=(
                "Hilbert-90 ratio identity",
                "legal sparse Yang-fiber product theorem",
                "finite-field divisor/additive identity for H0 or a <2>-translate",
            ),
            first_falsifier=(
                "formal one-coset H, missing (1-Frob_p) boundary, or ambient-period value"
            ),
            router_artifact=h90_router,
            candidate_command=h90_candidate_command("canonical_H0"),
            expected_pre_danger3_decision="source_theorem_closed_policy_or_framing_missing",
            expected_first_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_value_stage=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            ok=True,
        ),
        SourceRouteRow(
            name="exact_p_or_y507_route",
            target_row="exact_P_or_Y507_bridge_identity",
            accepted_source_families=(
                "KSY normalized-y exact product/distribution theorem",
                "Kubert-Lang exact mixed row-labeled product",
                "finite-field value identity for Y_507 with 75->300->12 bridge",
            ),
            first_falsifier=(
                "formula language, field generation, C169 projection, wrong C/D/K geometry, "
                "or value theorem without period-156 context"
            ),
            router_artifact=h90_router,
            candidate_command=h90_candidate_command("Y_507", output_kind="value"),
            expected_pre_danger3_decision="source_theorem_closed_policy_or_framing_missing",
            expected_first_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_value_stage=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            ok=True,
        ),
    )


def profile_source_route_packet() -> SourceRoutePacket:
    target_packet = RESEARCH / "p25_ksy_y_conductor39_value_theorem_target_packet_20260614.md"
    routes = source_routes()
    present = sum(row.router_artifact.exists() and row.router_artifact.stat().st_size > 0 for row in routes)
    value_closing = sum(row.closes_value_stage for row in routes)
    danger3_remaining = sum(row.still_needs_danger3 for row in routes)
    extraction_remaining = sum(row.still_needs_extraction for row in routes)
    local_commands = sum(" --candidate " in row.candidate_command for row in routes)
    row_ok = (
        target_packet.exists()
        and target_packet.stat().st_size > 0
        and len(routes) == 4
        and present == 4
        and value_closing == 4
        and danger3_remaining == 4
        and extraction_remaining == 4
        and local_commands == 4
        and all(row.expected_pre_danger3_decision == "source_theorem_closed_policy_or_framing_missing" for row in routes)
        and all(row.expected_first_missing_clause == "DANGER3 finite-identity/non-CM framing" for row in routes)
        and all(row.ok for row in routes)
    )
    return SourceRoutePacket(
        target_packet_artifact=target_packet,
        source_routes=routes,
        router_artifacts_present=present,
        route_rows=len(routes),
        value_closing_routes=value_closing,
        danger3_remaining_rows=danger3_remaining,
        extraction_remaining_rows=extraction_remaining,
        local_candidate_commands=local_commands,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_source_route_packet()
    print("p25 KSY-y conductor-39 value-theorem source-route packet gate")
    print(f"target_packet_artifact={profile.target_packet_artifact}")
    print("source_routes")
    for row in profile.source_routes:
        print(
            "  "
            f"{row.name}: target={row.target_row} closes_value={int(row.closes_value_stage)} "
            f"danger3={int(row.still_needs_danger3)} extraction={int(row.still_needs_extraction)}"
        )
        print(f"    families={row.accepted_source_families}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    router={row.router_artifact}")
        print(f"    expected={row.expected_pre_danger3_decision}")
        print(f"    missing={row.expected_first_missing_clause}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  route_rows={profile.route_rows}")
    print(f"  router_artifacts_present={profile.router_artifacts_present}")
    print(f"  value_closing_routes={profile.value_closing_routes}")
    print(f"  danger3_remaining_rows={profile.danger3_remaining_rows}")
    print(f"  extraction_remaining_rows={profile.extraction_remaining_rows}")
    print(f"  local_candidate_commands={profile.local_candidate_commands}")
    print("interpretation")
    print("  every_value_theorem_target_has_a_local_candidate_router=1")
    print("  successful_source_route_still_needs_danger3_and_extraction=1")
    print(f"ksy_y_conductor39_value_theorem_source_route_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 value-theorem source-route packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
