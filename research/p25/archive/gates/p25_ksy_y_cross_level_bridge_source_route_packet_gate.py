#!/usr/bin/env python3
"""Source-route packet for the p25 odd-level to X_1(16) bridge.

The conductor-39 route can produce an odd-level value/divisor theorem, but the
DANGER3 extractor needs the 2-primary X_1(16) Montgomery surface.  This
lightweight gate records which cross-level theorem shapes are useful, how they
are classified locally, and what falsifies them first.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm
from pathlib import Path


RESEARCH = Path("research/p25")
P25 = 10**25 + 13
X16_LEVEL = 16
ODD_LEVEL = 507
CONDUCTOR_LEVEL = 39
CROSS_LEVEL = lcm(X16_LEVEL, ODD_LEVEL)


@dataclass(frozen=True)
class BridgeSourceRouteRow:
    name: str
    theorem_payload: str
    accepted_source_families: tuple[str, ...]
    first_falsifier: str
    router_artifact: Path
    candidate_command: str
    expected_decision: str
    expected_first_missing_clause: str
    closes_odd_value_stage: bool
    identifies_same_j_bridge: bool
    reaches_practical_x16_surface: bool
    supplies_halving_chain: bool
    submission_ready: bool
    discard_condition: str
    ok: bool


@dataclass(frozen=True)
class BridgeSourceRoutePacket:
    p: int
    x16_level: int
    odd_level: int
    conductor_level: int
    cross_level: int
    level_gcd: int
    inv_507_mod_16: int
    inv_16_mod_507: int
    normalized_p16_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    prerequisite_markers_present: int
    route_rows: tuple[BridgeSourceRouteRow, ...]
    route_count: int
    local_candidate_commands: int
    same_j_bridge_rows: int
    practical_x16_surface_rows: int
    halving_rows: int
    submission_ready_rows: int
    non_submission_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


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


def route_rows() -> tuple[BridgeSourceRouteRow, ...]:
    x1_8112_router = RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py"
    chart_gate = RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_gate.py"
    halving_gate = RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_gate.py"
    submission_gate = (
        RESEARCH
        / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py"
    )
    return (
        BridgeSourceRouteRow(
            name="same_curve_p16_q507_pair",
            theorem_payload=(
                "exact p25 odd-level target plus exact P16 and Q507 on the same curve"
            ),
            accepted_source_families=(
                "X_1(16) x_j X_1(507) fiber-product theorem",
                "modular correspondence preserving the same j-invariant",
                "explicit elliptic curve carrying both exact torsion components",
            ),
            first_falsifier="independent level-16 and level-507 data, or no same-j proof",
            router_artifact=x1_8112_router,
            candidate_command=x1_8112_candidate_command(
                "same_curve_p16_q507_pair",
                fiber_product=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            expected_first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=False,
            supplies_halving_chain=False,
            submission_ready=False,
            discard_condition="discard if P16 and Q507 live on unrelated curves or only share field generation",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="order_8112_generator_R",
            theorem_payload=(
                "exact order-8112 point R tied to the p25 odd-level target"
            ),
            accepted_source_families=(
                "single X_1(8112) point theorem",
                "same-curve torsion gluing theorem with R=P16+Q507",
                "explicit normalized projections [1521]R=P16 and [6592]R=Q507",
            ),
            first_falsifier="R does not have exact order 8112 or does not project to the recorded odd target",
            router_artifact=x1_8112_router,
            candidate_command=x1_8112_candidate_command(
                "order_8112_generator_R",
                fiber_product=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            expected_first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=False,
            supplies_halving_chain=False,
            submission_ready=False,
            discard_condition="discard if the theorem only gives broad ray-class generation or unnormalized torsion data",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="x16_y_model_root_surface",
            theorem_payload="same-j bridge specialized to X_1(16) y, model root x, A, and xP16",
            accepted_source_families=(
                "X_1(8112) theorem specialized to the production X_1(16) chart",
                "explicit y and model root x satisfying the recorded quadratic",
                "direct A,xP16 payload derived from the same odd target",
            ),
            first_falsifier="abstract P16 torsion without y-chart or direct A,xP16 data",
            router_artifact=x1_8112_router,
            candidate_command=x1_8112_candidate_command(
                "x16_y_model_root_surface",
                fiber_product=True,
                x16_relation=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            expected_first_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=True,
            supplies_halving_chain=False,
            submission_ready=False,
            discard_condition="discard if the surface is generic X_1(16) data not tied to the odd target",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="active_x16_surface_with_policy",
            theorem_payload="DANGER3-framed X_1(16) A,xP16 surface for active x16halvenonsplit",
            accepted_source_families=(
                "finite-field/non-CM accepted bridge plus production X_1(16) surface",
                "direct A,xP16 output with same-j odd-level provenance",
                "optional d-gate surface only if it also preserves the active A,xP16 payload",
            ),
            first_falsifier="surface lacks challenge framing or only emits optional first-half data",
            router_artifact=x1_8112_router,
            candidate_command=x1_8112_candidate_command(
                "active_x16_surface_with_policy",
                fiber_product=True,
                x16_relation=True,
                danger3_framing=True,
            ),
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            expected_first_missing_clause="valid halving chain from xP16 to concrete x0",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=True,
            supplies_halving_chain=False,
            submission_ready=False,
            discard_condition="discard if it cannot start depth-4 halving from xP16",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="checkable_halving_chain",
            theorem_payload="A, xP16, and x_4=xP16,...,x_42=x0",
            accepted_source_families=(
                "explicit x-coordinate halving certificate",
                "sqrt-witness chain for active branch provenance",
                "direct x0 plus A verified by official vpp.py",
            ),
            first_falsifier="branch word without actual x-values or sqrt witnesses",
            router_artifact=halving_gate,
            candidate_command="run halving-certificate payload gate and inspect x_coordinate_chain row",
            expected_decision="checkable_x_chain_vpp_missing",
            expected_first_missing_clause="official vpp.py verification",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=True,
            supplies_halving_chain=True,
            submission_ready=False,
            discard_condition="discard if xDBL links do not check back to xP16",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="direct_verified_pomerance_triple",
            theorem_payload="concrete p25 (p,A,x0) verified by official vpp.py",
            accepted_source_families=(
                "official vpp.py verified triple",
                "Lean certificate generated from the verified triple",
                "archived command/log/environment bundle",
            ),
            first_falsifier="official vpp.py rejects the triple",
            router_artifact=submission_gate,
            candidate_command=(
                "python3 research/p25/"
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py "
                "--p 10000000000000000000000013 --A <A> --x0 <x0>"
            ),
            expected_decision="closing_vpp_verified_submission",
            expected_first_missing_clause="none",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=True,
            supplies_halving_chain=True,
            submission_ready=True,
            discard_condition="not a submission unless the official verifier accepts it",
            ok=True,
        ),
        BridgeSourceRouteRow(
            name="chart_contract_reference",
            theorem_payload="production X_1(16) chart formulas for y, x, A, and xP16",
            accepted_source_families=(
                "active x16halvenonsplit chart formulas",
                "direct A,xP16 chart bypass",
                "optional x16halvenonsplitdgate first-half data as a strict upgrade",
            ),
            first_falsifier="only an abstract P16 point, or y without model root",
            router_artifact=chart_gate,
            candidate_command="run X_1(16) Montgomery-chart contract gate and inspect route rows",
            expected_decision="active_surface_reached_halving_missing",
            expected_first_missing_clause="halve chain from xP16 at depth 4 to x0",
            closes_odd_value_stage=True,
            identifies_same_j_bridge=True,
            reaches_practical_x16_surface=True,
            supplies_halving_chain=False,
            submission_ready=False,
            discard_condition="discard if it cannot emit the active production A,xP16 surface",
            ok=True,
        ),
    )


def profile_bridge_source_route_packet() -> BridgeSourceRoutePacket:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    projection_sum = (normalized_p16 + normalized_q507) % CROSS_LEVEL
    rows = route_rows()
    prerequisite_markers = sum(
        (
            marker_present(
                RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_20260614.md",
                "ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_x1_8112_torsion_gluing_contract_20260614.md",
                "ksy_y_x1_8112_torsion_gluing_contract_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
                "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
                "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
            ),
        )
    )
    local_commands = sum(" --candidate " in row.candidate_command for row in rows)
    same_j = sum(row.identifies_same_j_bridge for row in rows)
    practical = sum(row.reaches_practical_x16_surface for row in rows)
    halving = sum(row.supplies_halving_chain for row in rows)
    submission = sum(row.submission_ready for row in rows)
    non_submission = len(rows) - submission
    row_ok = (
        P25 == 10000000000000000000000013
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CONDUCTOR_LEVEL == 39
        and CROSS_LEVEL == 8112
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and inv_507 == 3
        and inv_16 == 412
        and normalized_p16 == 1521
        and normalized_q507 == 6592
        and projection_sum == 1
        and prerequisite_markers == 4
        and len(rows) == 7
        and local_commands == 4
        and same_j == 7
        and practical == 5
        and halving == 2
        and submission == 1
        and non_submission == 6
        and tuple(row.expected_decision for row in rows)
        == (
            "cross_level_target_identified_specialization_missing",
            "cross_level_target_identified_specialization_missing",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "checkable_x_chain_vpp_missing",
            "closing_vpp_verified_submission",
            "active_surface_reached_halving_missing",
        )
        and all(row.router_artifact.exists() and row.router_artifact.stat().st_size > 0 for row in rows)
        and all(row.ok for row in rows)
    )
    return BridgeSourceRoutePacket(
        p=P25,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        conductor_level=CONDUCTOR_LEVEL,
        cross_level=CROSS_LEVEL,
        level_gcd=gcd(X16_LEVEL, ODD_LEVEL),
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        normalized_p16_multiplier=normalized_p16,
        normalized_q507_multiplier=normalized_q507,
        normalized_projection_sum_mod_8112=projection_sum,
        prerequisite_markers_present=prerequisite_markers,
        route_rows=rows,
        route_count=len(rows),
        local_candidate_commands=local_commands,
        same_j_bridge_rows=same_j,
        practical_x16_surface_rows=practical,
        halving_rows=halving,
        submission_ready_rows=submission,
        non_submission_rows=non_submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_bridge_source_route_packet()
    print("p25 KSY-y cross-level bridge source-route packet gate")
    print("levels")
    print(f"  p={profile.p}")
    print(f"  conductor_level={profile.conductor_level}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  cross_level={profile.cross_level}")
    print(f"  level_gcd={profile.level_gcd}")
    print("projection_arithmetic")
    print(f"  inv_507_mod_16={profile.inv_507_mod_16}")
    print(f"  inv_16_mod_507={profile.inv_16_mod_507}")
    print(f"  normalized_p16_multiplier={profile.normalized_p16_multiplier}")
    print(f"  normalized_q507_multiplier={profile.normalized_q507_multiplier}")
    print(
        "  normalized_projection_sum_mod_8112="
        f"{profile.normalized_projection_sum_mod_8112}"
    )
    print(f"prerequisite_markers_present={profile.prerequisite_markers_present}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.expected_decision} "
            f"same_j={int(row.identifies_same_j_bridge)} "
            f"x16_surface={int(row.reaches_practical_x16_surface)} "
            f"halving={int(row.supplies_halving_chain)} "
            f"submission={int(row.submission_ready)} "
            f"missing={row.expected_first_missing_clause}"
        )
        print(f"    payload={row.theorem_payload}")
        print(f"    families={row.accepted_source_families}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    discard={row.discard_condition}")
        print(f"    router={row.router_artifact}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  route_count={profile.route_count}")
    print(f"  local_candidate_commands={profile.local_candidate_commands}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  practical_x16_surface_rows={profile.practical_x16_surface_rows}")
    print(f"  halving_rows={profile.halving_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  non_submission_rows={profile.non_submission_rows}")
    print("interpretation")
    print("  odd_value_theorem_must_emit_same_j_bridge_or_direct_triple=1")
    print("  same_j_bridge_must_specialize_to_production_A_xP16_surface=1")
    print("  active_surface_still_needs_depth4_halving_and_vpp=1")
    print(f"ksy_y_cross_level_bridge_source_route_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("cross-level bridge source-route packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
