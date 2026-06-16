#!/usr/bin/env python3
"""H0 order-8112 bridge to practical X_1(16) chart specialization.

The H0 X_1(8112) bridge payload contract accepts same-j/order-8112 bridge
data.  This gate records the next concrete requirement: the bridge must
specialize to the practical X_1(16) Montgomery chart used by the p25 search,
or directly emit A/x0 for official vpp.py verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt
from pathlib import Path


P25 = 10**25 + 13
ACTIVE_MODE = "x16halvenonsplit"
OPTIONAL_DGATE_MODE = "x16halvenonsplitdgate"
ACTIVE_START_DEPTH = 4
OPTIONAL_DGATE_START_DEPTH = 5
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class H0Order8112X16FormulaRow:
    name: str
    formula: str
    active_required: bool
    optional_dgate_only: bool
    ok: bool


@dataclass(frozen=True)
class H0Order8112X16RouteRow:
    name: str
    payload_shape: str
    has_order8112_bridge: bool
    has_y_parameter: bool
    has_model_root_x: bool
    has_A_and_xP16: bool
    has_optional_first_half: bool
    has_halving_chain_or_x0: bool
    has_official_vpp: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class H0Order8112X16ChartSpecialization:
    bridge_payload_marker_present: bool
    montgomery_chart_marker_present: bool
    halving_chain_marker_present: bool
    halving_payload_marker_present: bool
    p_mod_8: int
    sqrt_floor: int
    hasse_bound: int
    k: int
    active_mode: str
    active_start_depth: int
    active_halving_steps: int
    optional_dgate_mode: str
    optional_dgate_start_depth: int
    optional_dgate_halving_steps: int
    formula_rows: tuple[H0Order8112X16FormulaRow, ...]
    route_rows: tuple[H0Order8112X16RouteRow, ...]
    formula_count: int
    active_formula_rows: int
    optional_dgate_formula_rows: int
    route_count: int
    order8112_bridge_rows: int
    chart_surface_rows: int
    optional_dgate_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def compute_k_and_bound(p: int) -> tuple[int, int, int]:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return q, bound, bound.bit_length()


def formula_rows() -> tuple[H0Order8112X16FormulaRow, ...]:
    return (
        H0Order8112X16FormulaRow(
            name="chart_denominators",
            formula="y != 0, y != 1, y^2-2y != 0, x-y != 0",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="model_quadratic",
            formula="(y^2-2y)*x^2 + (2y^2-y^3)*x + (1-y) = 0",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="model_discriminant",
            formula="D=(2y^2-y^3)^2 - 4*(y^2-2y)*(1-y) must be square",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="montgomery_A",
            formula=(
                "A=N(y)/(4*(y-1)^4), "
                "N=y^8-8y^7+24y^6-32y^5+8y^4+32y^3-48y^2+32y-8"
            ),
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="marked_xP16",
            formula="xP16=x/(x-y)",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="nonsplit_filter",
            formula="(y^2-2)*(y^2-4y+2) is nonsquare",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="active_depth4_surface",
            formula="x16halvenonsplit starts from (A,xP16) at depth 4",
            active_required=True,
            optional_dgate_only=False,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="optional_first_half_gate",
            formula="(y-1)*(y^2-2)*(y^2-2y+2) is square",
            active_required=False,
            optional_dgate_only=True,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="optional_first_half_sd",
            formula="sd=y*z/(2*(x-y)*(y-1)^2), z^2=(y-1)*(y^2-2)*(y^2-2y+2)",
            active_required=False,
            optional_dgate_only=True,
            ok=True,
        ),
        H0Order8112X16FormulaRow(
            name="optional_dgate_depth5_surface",
            formula="x16halvenonsplitdgate starts from (A,x32) at depth 5",
            active_required=False,
            optional_dgate_only=True,
            ok=True,
        ),
    )


def route_rows() -> tuple[H0Order8112X16RouteRow, ...]:
    return (
        H0Order8112X16RouteRow(
            name="order8112_bridge_only",
            payload_shape="same-j order-8112 bridge R tied to H0",
            has_order8112_bridge=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=False,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_official_vpp=False,
            decision="order8112_bridge_not_practical_chart",
            first_missing_clause="X_1(16) y-chart parameter or direct A,xP16",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="order8112_y_only",
            payload_shape="order-8112 bridge with X_1(16) y only",
            has_order8112_bridge=True,
            has_y_parameter=True,
            has_model_root_x=False,
            has_A_and_xP16=False,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_official_vpp=False,
            decision="y_chart_missing_model_root",
            first_missing_clause="model root x satisfying the X_1(16) quadratic",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="order8112_y_model_root_surface",
            payload_shape="order-8112 bridge with y, model root x, A, and xP16",
            has_order8112_bridge=True,
            has_y_parameter=True,
            has_model_root_x=True,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_official_vpp=False,
            decision="active_surface_reached_halving_missing",
            first_missing_clause="halve chain from xP16 at depth 4 to x0",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="order8112_direct_A_xP16_surface",
            payload_shape="order-8112 bridge with direct A and xP16 but no y witness",
            has_order8112_bridge=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_official_vpp=False,
            decision="active_surface_reached_halving_missing",
            first_missing_clause="halve chain from xP16 at depth 4 to x0",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="order8112_optional_dgate_surface",
            payload_shape="order-8112 bridge with y, x, A, xP16, and first-half d-gate",
            has_order8112_bridge=True,
            has_y_parameter=True,
            has_model_root_x=True,
            has_A_and_xP16=True,
            has_optional_first_half=True,
            has_halving_chain_or_x0=False,
            has_official_vpp=False,
            decision="optional_depth5_surface_reached_halving_missing",
            first_missing_clause="halve chain from x32 at depth 5 to x0",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="order8112_surface_with_x0",
            payload_shape="order-8112 bridge with A, xP16, and concrete x0",
            has_order8112_bridge=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=True,
            has_official_vpp=False,
            decision="extraction_ready_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        H0Order8112X16RouteRow(
            name="verified_pomerance_triple",
            payload_shape="concrete p25 (p,A,x0) triple verified by official vpp.py",
            has_order8112_bridge=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=True,
            has_official_vpp=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_h0_order8112_x16_chart_specialization() -> H0Order8112X16ChartSpecialization:
    bridge_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_x18112_bridge_payload_contract_20260614.md",
        "ksy_y_h0_x18112_bridge_payload_contract_rows=1/1",
    )
    chart_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    )
    halving_chain_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_halving_chain_contract_20260614.md",
        "ksy_y_x1_16_halving_chain_contract_rows=1/1",
    )
    halving_payload_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    )
    sqrt_floor, hasse_bound, k = compute_k_and_bound(P25)
    formulas = formula_rows()
    routes = route_rows()
    active_steps = k - ACTIVE_START_DEPTH
    dgate_steps = k - OPTIONAL_DGATE_START_DEPTH
    active_formulas = sum(row.active_required for row in formulas)
    dgate_formulas = sum(row.optional_dgate_only for row in formulas)
    order8112_bridge_rows = sum(row.has_order8112_bridge for row in routes)
    chart_surface_rows = sum(row.has_A_and_xP16 for row in routes)
    optional_dgate_rows = sum(row.has_optional_first_half for row in routes)
    extraction_rows = sum(row.has_halving_chain_or_x0 for row in routes)
    submission_rows = sum(row.has_official_vpp for row in routes)
    row_ok = (
        bridge_marker
        and chart_marker
        and halving_chain_marker
        and halving_payload_marker
        and P25 % 8 == 5
        and sqrt_floor == 3162277660168
        and k == 42
        and 2**41 <= hasse_bound < 2**42
        and gcd(4, P25) == 1
        and ACTIVE_MODE == "x16halvenonsplit"
        and OPTIONAL_DGATE_MODE == "x16halvenonsplitdgate"
        and ACTIVE_START_DEPTH == 4
        and OPTIONAL_DGATE_START_DEPTH == 5
        and active_steps == 38
        and dgate_steps == 37
        and len(formulas) == 10
        and active_formulas == 7
        and dgate_formulas == 3
        and all(row.ok for row in formulas)
        and len(routes) == 7
        and order8112_bridge_rows == 7
        and chart_surface_rows == 5
        and optional_dgate_rows == 1
        and extraction_rows == 2
        and submission_rows == 1
        and tuple(row.decision for row in routes)
        == (
            "order8112_bridge_not_practical_chart",
            "y_chart_missing_model_root",
            "active_surface_reached_halving_missing",
            "active_surface_reached_halving_missing",
            "optional_depth5_surface_reached_halving_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in routes)
    )
    return H0Order8112X16ChartSpecialization(
        bridge_payload_marker_present=bridge_marker,
        montgomery_chart_marker_present=chart_marker,
        halving_chain_marker_present=halving_chain_marker,
        halving_payload_marker_present=halving_payload_marker,
        p_mod_8=P25 % 8,
        sqrt_floor=sqrt_floor,
        hasse_bound=hasse_bound,
        k=k,
        active_mode=ACTIVE_MODE,
        active_start_depth=ACTIVE_START_DEPTH,
        active_halving_steps=active_steps,
        optional_dgate_mode=OPTIONAL_DGATE_MODE,
        optional_dgate_start_depth=OPTIONAL_DGATE_START_DEPTH,
        optional_dgate_halving_steps=dgate_steps,
        formula_rows=formulas,
        route_rows=routes,
        formula_count=len(formulas),
        active_formula_rows=active_formulas,
        optional_dgate_formula_rows=dgate_formulas,
        route_count=len(routes),
        order8112_bridge_rows=order8112_bridge_rows,
        chart_surface_rows=chart_surface_rows,
        optional_dgate_rows=optional_dgate_rows,
        extraction_ready_rows=extraction_rows,
        submission_ready_rows=submission_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_order8112_x16_chart_specialization()
    print("p25 KSY-y H0 order-8112 to X1(16) chart-specialization gate")
    print("dependencies")
    print(f"  bridge_payload_marker_present={int(profile.bridge_payload_marker_present)}")
    print(f"  montgomery_chart_marker_present={int(profile.montgomery_chart_marker_present)}")
    print(f"  halving_chain_marker_present={int(profile.halving_chain_marker_present)}")
    print(f"  halving_payload_marker_present={int(profile.halving_payload_marker_present)}")
    print("production")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  sqrt_floor={profile.sqrt_floor}")
    print(f"  hasse_bound={profile.hasse_bound}")
    print(f"  k={profile.k}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  active_halving_steps={profile.active_halving_steps}")
    print(f"  optional_dgate_mode={profile.optional_dgate_mode}")
    print(f"  optional_dgate_start_depth={profile.optional_dgate_start_depth}")
    print(f"  optional_dgate_halving_steps={profile.optional_dgate_halving_steps}")
    print("formula_rows")
    for row in profile.formula_rows:
        print(
            "  "
            f"{row.name}: active={int(row.active_required)} "
            f"dgate={int(row.optional_dgate_only)} formula={row.formula}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: R8112={int(row.has_order8112_bridge)} "
            f"y={int(row.has_y_parameter)} x={int(row.has_model_root_x)} "
            f"A_xP16={int(row.has_A_and_xP16)} "
            f"dgate={int(row.has_optional_first_half)} "
            f"x0={int(row.has_halving_chain_or_x0)} "
            f"vpp={int(row.has_official_vpp)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
        print(f"    payload={row.payload_shape}")
    print("counts")
    print(f"  formula_count={profile.formula_count}")
    print(f"  active_formula_rows={profile.active_formula_rows}")
    print(f"  optional_dgate_formula_rows={profile.optional_dgate_formula_rows}")
    print(f"  route_count={profile.route_count}")
    print(f"  order8112_bridge_rows={profile.order8112_bridge_rows}")
    print(f"  chart_surface_rows={profile.chart_surface_rows}")
    print(f"  optional_dgate_rows={profile.optional_dgate_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  order8112_bridge_is_not_practical_until_it_emits_y_x_A_xP16_or_direct_A_xP16=1")
    print("  active_x16halvenonsplit_path_starts_from_xP16_at_depth4_and_needs_38_halvings=1")
    print("  optional_dgate_path_starts_from_x32_at_depth5_and_is_not_required_for_submission=1")
    print("  only_official_vpp_verified_A_x0_is_submission_ready=1")
    print(f"ksy_y_h0_order8112_x16_chart_specialization_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 order-8112 X1(16) chart-specialization regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
