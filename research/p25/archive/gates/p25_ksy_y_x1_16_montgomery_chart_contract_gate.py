#!/usr/bin/env python3
"""X_1(16) Montgomery-chart contract for p25 bridge payloads.

The X_1(8112) torsion-gluing contract can produce an exact 16-torsion
component P16 on the same curve as the odd KSY/Yang/H90 target.  The practical
search, however, uses a specific X_1(16) Montgomery chart: a y-parameter, a
model root x, the Montgomery coefficient A, and the marked x-coordinate xP16.

This gate records the exact chart ladder and separates the active production
surface (`x16halvenonsplit`, halving starts from xP16 at depth 4) from the
stronger optional first-half d-gate surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt

from p25_ksy_y_cross_level_extraction_gap_gate import P25
from p25_ksy_y_x1_8112_torsion_gluing_contract_gate import (
    profile_x1_8112_torsion_gluing_contract,
)


ACTIVE_PRODUCTION_MODE = "x16halvenonsplit"
OPTIONAL_DGATE_MODE = "x16halvenonsplitdgate"
X16_START_DEPTH = 4
DGATE_START_DEPTH = 5


@dataclass(frozen=True)
class X16ChartFormulaRow:
    name: str
    formula: str
    active_production_requirement: bool
    dgate_only_requirement: bool
    ok: bool


@dataclass(frozen=True)
class X16ChartRouteRow:
    name: str
    has_same_curve_p16: bool
    has_y_parameter: bool
    has_model_root_x: bool
    has_A_and_xP16: bool
    has_optional_first_half: bool
    has_halving_chain_or_x0: bool
    has_vpp_triple: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class X16MontgomeryChartContract:
    p: int
    p_mod_8: int
    k: int
    active_mode: str
    active_start_depth: int
    optional_dgate_mode: str
    optional_dgate_start_depth: int
    torsion_gluing_ok: bool
    formula_rows: tuple[X16ChartFormulaRow, ...]
    route_rows: tuple[X16ChartRouteRow, ...]
    active_formula_rows: int
    dgate_formula_rows: int
    chart_surface_rows: int
    optional_first_half_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def compute_k(p: int) -> int:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return bound.bit_length()


def formula_rows() -> tuple[X16ChartFormulaRow, ...]:
    return (
        X16ChartFormulaRow(
            name="chart_denominators",
            formula="y != 0, y != 1, y^2-2y != 0, x-y != 0",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="model_quadratic",
            formula="(y^2-2y)*x^2 + (2y^2-y^3)*x + (1-y) = 0",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="model_discriminant",
            formula="D=(2y^2-y^3)^2 - 4*(y^2-2y)*(1-y) must be square",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="montgomery_A",
            formula=(
                "A=N(y)/(4*(y-1)^4), "
                "N=y^8-8y^7+24y^6-32y^5+8y^4+32y^3-48y^2+32y-8"
            ),
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="marked_xP16",
            formula="xP16 = x/(x-y)",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="nonsplit_filter",
            formula="(y^2-2)*(y^2-4y+2) is nonsquare",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="active_halving_start",
            formula="x16halvenonsplit starts halve_chain_from_depth(A,xP16,depth=4,k)",
            active_production_requirement=True,
            dgate_only_requirement=False,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="optional_first_half_gate",
            formula="(y-1)*(y^2-2)*(y^2-2y+2) is square",
            active_production_requirement=False,
            dgate_only_requirement=True,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="optional_first_half_sd",
            formula="sd=y*z/(2*(x-y)*(y-1)^2), z^2=(y-1)*(y^2-2)*(y^2-2y+2)",
            active_production_requirement=False,
            dgate_only_requirement=True,
            ok=True,
        ),
        X16ChartFormulaRow(
            name="optional_dgate_halving_start",
            formula="x16halvenonsplitdgate starts halve_chain_from_depth(A,x32,depth=5,k)",
            active_production_requirement=False,
            dgate_only_requirement=True,
            ok=True,
        ),
    )


def route_rows() -> tuple[X16ChartRouteRow, ...]:
    return (
        X16ChartRouteRow(
            name="same_curve_abstract_P16",
            has_same_curve_p16=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=False,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_vpp_triple=False,
            decision="abstract_p16_not_practical_chart",
            first_missing_clause="X_1(16) y-chart parameter or direct A,xP16",
            ok=True,
        ),
        X16ChartRouteRow(
            name="x16_y_only",
            has_same_curve_p16=True,
            has_y_parameter=True,
            has_model_root_x=False,
            has_A_and_xP16=False,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_vpp_triple=False,
            decision="y_chart_missing_model_root",
            first_missing_clause="model root x satisfying the X_1(16) quadratic",
            ok=True,
        ),
        X16ChartRouteRow(
            name="x16_y_and_model_root",
            has_same_curve_p16=True,
            has_y_parameter=True,
            has_model_root_x=True,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_vpp_triple=False,
            decision="active_surface_reached_halving_missing",
            first_missing_clause="halve chain from xP16 at depth 4 to x0",
            ok=True,
        ),
        X16ChartRouteRow(
            name="direct_A_xP16_surface",
            has_same_curve_p16=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=False,
            has_vpp_triple=False,
            decision="active_surface_reached_halving_missing",
            first_missing_clause="halve chain from xP16 at depth 4 to x0",
            ok=True,
        ),
        X16ChartRouteRow(
            name="dgate_first_half_surface",
            has_same_curve_p16=True,
            has_y_parameter=True,
            has_model_root_x=True,
            has_A_and_xP16=True,
            has_optional_first_half=True,
            has_halving_chain_or_x0=False,
            has_vpp_triple=False,
            decision="optional_depth5_surface_reached_halving_missing",
            first_missing_clause="halve chain from x32 at depth 5 to x0",
            ok=True,
        ),
        X16ChartRouteRow(
            name="surface_with_x0",
            has_same_curve_p16=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=True,
            has_vpp_triple=False,
            decision="extraction_ready_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        X16ChartRouteRow(
            name="direct_verified_p25_triple",
            has_same_curve_p16=True,
            has_y_parameter=False,
            has_model_root_x=False,
            has_A_and_xP16=True,
            has_optional_first_half=False,
            has_halving_chain_or_x0=True,
            has_vpp_triple=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_x1_16_montgomery_chart_contract() -> X16MontgomeryChartContract:
    gluing = profile_x1_8112_torsion_gluing_contract()
    formulas = formula_rows()
    routes = route_rows()
    active_rows = sum(row.active_production_requirement for row in formulas)
    dgate_rows = sum(row.dgate_only_requirement for row in formulas)
    chart_rows = sum(row.has_A_and_xP16 for row in routes)
    optional_first_half_rows = sum(row.has_optional_first_half for row in routes)
    extraction_rows = sum(row.has_halving_chain_or_x0 for row in routes)
    submission_rows = sum(row.has_vpp_triple for row in routes)
    decisions = tuple(row.decision for row in routes)
    row_ok = (
        P25 == 10**25 + 13
        and P25 % 8 == 5
        and compute_k(P25) == 42
        and gcd(4, P25) == 1
        and gluing.row_ok
        and ACTIVE_PRODUCTION_MODE == "x16halvenonsplit"
        and OPTIONAL_DGATE_MODE == "x16halvenonsplitdgate"
        and X16_START_DEPTH == 4
        and DGATE_START_DEPTH == 5
        and len(formulas) == 10
        and active_rows == 7
        and dgate_rows == 3
        and all(row.ok for row in formulas)
        and len(routes) == 7
        and chart_rows == 5
        and optional_first_half_rows == 1
        and extraction_rows == 2
        and submission_rows == 1
        and decisions
        == (
            "abstract_p16_not_practical_chart",
            "y_chart_missing_model_root",
            "active_surface_reached_halving_missing",
            "active_surface_reached_halving_missing",
            "optional_depth5_surface_reached_halving_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in routes)
    )
    return X16MontgomeryChartContract(
        p=P25,
        p_mod_8=P25 % 8,
        k=compute_k(P25),
        active_mode=ACTIVE_PRODUCTION_MODE,
        active_start_depth=X16_START_DEPTH,
        optional_dgate_mode=OPTIONAL_DGATE_MODE,
        optional_dgate_start_depth=DGATE_START_DEPTH,
        torsion_gluing_ok=gluing.row_ok,
        formula_rows=formulas,
        route_rows=routes,
        active_formula_rows=active_rows,
        dgate_formula_rows=dgate_rows,
        chart_surface_rows=chart_rows,
        optional_first_half_rows=optional_first_half_rows,
        extraction_ready_rows=extraction_rows,
        submission_ready_rows=submission_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_x1_16_montgomery_chart_contract()
    print("p25 KSY-y X1(16) Montgomery-chart contract gate")
    print("production")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  k={profile.k}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  optional_dgate_mode={profile.optional_dgate_mode}")
    print(f"  optional_dgate_start_depth={profile.optional_dgate_start_depth}")
    print(f"  torsion_gluing_ok={int(profile.torsion_gluing_ok)}")
    print("formula_rows")
    for row in profile.formula_rows:
        print(
            "  "
            f"{row.name}: active={int(row.active_production_requirement)} "
            f"dgate={int(row.dgate_only_requirement)} formula={row.formula}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: P16={int(row.has_same_curve_p16)} "
            f"y={int(row.has_y_parameter)} "
            f"x={int(row.has_model_root_x)} "
            f"A_xP16={int(row.has_A_and_xP16)} "
            f"first_half={int(row.has_optional_first_half)} "
            f"x0={int(row.has_halving_chain_or_x0)} "
            f"vpp={int(row.has_vpp_triple)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  active_formula_rows={profile.active_formula_rows}")
    print(f"  dgate_formula_rows={profile.dgate_formula_rows}")
    print(f"  chart_surface_rows={profile.chart_surface_rows}")
    print(f"  optional_first_half_rows={profile.optional_first_half_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  abstract_P16_torsion_is_not_yet_the_practical_montgomery_chart=1")
    print("  active_x16halvenonsplit_surface_is_A_xP16_with_depth4_halving=1")
    print("  first_half_z_sd_gate_is_optional_dgate_depth5_surface=1")
    print(f"ksy_y_x1_16_montgomery_chart_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(16) Montgomery-chart contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
