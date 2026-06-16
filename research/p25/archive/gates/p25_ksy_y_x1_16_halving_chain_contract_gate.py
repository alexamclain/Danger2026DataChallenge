#!/usr/bin/env python3
"""X_1(16) halving-chain contract for p25 bridge payloads.

The Montgomery-chart contract stops at A,xP16 for the active production mode.
This gate records the remaining extraction burden: for p25, xP16 starts at
depth 4 and the final verifier needs k=42, so the active route needs 38
successive halvings or a direct x0 that passes official vpp.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt

from p25_ksy_y_cross_level_extraction_gap_gate import P25
from p25_ksy_y_x1_16_montgomery_chart_contract_gate import (
    ACTIVE_PRODUCTION_MODE,
    DGATE_START_DEPTH,
    OPTIONAL_DGATE_MODE,
    X16_START_DEPTH,
    profile_x1_16_montgomery_chart_contract,
)


@dataclass(frozen=True)
class HalvingFormulaRow:
    name: str
    formula: str
    active_first_branch_requirement: bool
    full_backtracking_control: bool
    ok: bool


@dataclass(frozen=True)
class HalvingRouteRow:
    name: str
    has_A_xP16_surface: bool
    has_active_first_branch_chain: bool
    has_any_valid_halving_chain: bool
    has_direct_x0: bool
    has_internal_verify: bool
    has_official_vpp: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class X16HalvingChainContract:
    p: int
    p_mod_8: int
    q_floor_sqrt_p: int
    hasse_bound: int
    k: int
    active_mode: str
    active_start_depth: int
    active_halving_steps: int
    optional_dgate_mode: str
    optional_dgate_start_depth: int
    optional_dgate_halving_steps: int
    chart_contract_ok: bool
    formula_rows: tuple[HalvingFormulaRow, ...]
    route_rows: tuple[HalvingRouteRow, ...]
    active_formula_rows: int
    full_backtracking_formula_rows: int
    active_chain_rows: int
    any_chain_rows: int
    direct_x0_rows: int
    internal_verify_rows: int
    official_vpp_rows: int
    row_ok: bool


def compute_k_and_bound(p: int) -> tuple[int, int, int]:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return q, bound, bound.bit_length()


def formula_rows() -> tuple[HalvingFormulaRow, ...]:
    return (
        HalvingFormulaRow(
            name="halve_step_d_square",
            formula="d=x^2+A*x+1 must be square",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="halve_step_u_branches",
            formula="u=2*x+2*sqrt(d) first, then u=2*x-2*sqrt(d)",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="halve_step_w_square",
            formula="w=u^2-4 must be square for the selected u branch",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="halve_step_candidate_order",
            formula="candidate halves are (u+sqrt(w))/2 first, then (u-sqrt(w))/2",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="active_first_nonzero_choice",
            formula="x16halvenonsplit accepts the first nonzero candidate in C loop order",
            active_first_branch_requirement=True,
            full_backtracking_control=False,
            ok=True,
        ),
        HalvingFormulaRow(
            name="full_backtracking_control",
            formula="x16halvefull explores all distinct halves instead of the first branch",
            active_first_branch_requirement=False,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="final_internal_verify",
            formula="after depth k, verify128 requires no earlier zero Z and final zero Z",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
        HalvingFormulaRow(
            name="official_vpp_acceptance",
            formula="official vpp.py doubles x0 k times and requires Z_k=0 and gcd(Z_{k-1},p)=1",
            active_first_branch_requirement=True,
            full_backtracking_control=True,
            ok=True,
        ),
    )


def route_rows() -> tuple[HalvingRouteRow, ...]:
    return (
        HalvingRouteRow(
            name="A_xP16_surface_only",
            has_A_xP16_surface=True,
            has_active_first_branch_chain=False,
            has_any_valid_halving_chain=False,
            has_direct_x0=False,
            has_internal_verify=False,
            has_official_vpp=False,
            decision="surface_reached_halving_chain_missing",
            first_missing_clause="38 active first-branch halvings or direct x0",
            ok=True,
        ),
        HalvingRouteRow(
            name="active_first_branch_chain_to_x0",
            has_A_xP16_surface=True,
            has_active_first_branch_chain=True,
            has_any_valid_halving_chain=True,
            has_direct_x0=True,
            has_internal_verify=True,
            has_official_vpp=False,
            decision="x0_extracted_official_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        HalvingRouteRow(
            name="any_valid_halving_chain_to_x0",
            has_A_xP16_surface=True,
            has_active_first_branch_chain=False,
            has_any_valid_halving_chain=True,
            has_direct_x0=True,
            has_internal_verify=True,
            has_official_vpp=False,
            decision="x0_extracted_not_active_path_vpp_missing",
            first_missing_clause="official vpp.py verification; active-path provenance optional",
            ok=True,
        ),
        HalvingRouteRow(
            name="direct_A_x0_without_chain",
            has_A_xP16_surface=False,
            has_active_first_branch_chain=False,
            has_any_valid_halving_chain=False,
            has_direct_x0=True,
            has_internal_verify=False,
            has_official_vpp=False,
            decision="direct_x0_official_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        HalvingRouteRow(
            name="internal_verify_only",
            has_A_xP16_surface=True,
            has_active_first_branch_chain=True,
            has_any_valid_halving_chain=True,
            has_direct_x0=True,
            has_internal_verify=True,
            has_official_vpp=False,
            decision="internal_verify_not_submission",
            first_missing_clause="official vpp.py verification and archive",
            ok=True,
        ),
        HalvingRouteRow(
            name="official_vpp_verified_triple",
            has_A_xP16_surface=False,
            has_active_first_branch_chain=False,
            has_any_valid_halving_chain=False,
            has_direct_x0=True,
            has_internal_verify=False,
            has_official_vpp=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_x1_16_halving_chain_contract() -> X16HalvingChainContract:
    chart = profile_x1_16_montgomery_chart_contract()
    q, bound, k = compute_k_and_bound(P25)
    formulas = formula_rows()
    routes = route_rows()
    active_steps = k - X16_START_DEPTH
    dgate_steps = k - DGATE_START_DEPTH
    active_formula_rows = sum(row.active_first_branch_requirement for row in formulas)
    full_formula_rows = sum(row.full_backtracking_control for row in formulas)
    active_chain_rows = sum(row.has_active_first_branch_chain for row in routes)
    any_chain_rows = sum(row.has_any_valid_halving_chain for row in routes)
    direct_x0_rows = sum(row.has_direct_x0 for row in routes)
    internal_rows = sum(row.has_internal_verify for row in routes)
    vpp_rows = sum(row.has_official_vpp for row in routes)
    decisions = tuple(row.decision for row in routes)
    row_ok = (
        P25 == 10**25 + 13
        and P25 % 8 == 5
        and q == 3162277660168
        and k == 42
        and bound.bit_length() == 42
        and 2**41 <= bound < 2**42
        and chart.row_ok
        and ACTIVE_PRODUCTION_MODE == "x16halvenonsplit"
        and OPTIONAL_DGATE_MODE == "x16halvenonsplitdgate"
        and X16_START_DEPTH == 4
        and DGATE_START_DEPTH == 5
        and active_steps == 38
        and dgate_steps == 37
        and gcd(4, P25) == 1
        and len(formulas) == 8
        and active_formula_rows == 7
        and full_formula_rows == 7
        and all(row.ok for row in formulas)
        and len(routes) == 6
        and active_chain_rows == 2
        and any_chain_rows == 3
        and direct_x0_rows == 5
        and internal_rows == 3
        and vpp_rows == 1
        and decisions
        == (
            "surface_reached_halving_chain_missing",
            "x0_extracted_official_vpp_missing",
            "x0_extracted_not_active_path_vpp_missing",
            "direct_x0_official_vpp_missing",
            "internal_verify_not_submission",
            "submission_ready",
        )
        and all(row.ok for row in routes)
    )
    return X16HalvingChainContract(
        p=P25,
        p_mod_8=P25 % 8,
        q_floor_sqrt_p=q,
        hasse_bound=bound,
        k=k,
        active_mode=ACTIVE_PRODUCTION_MODE,
        active_start_depth=X16_START_DEPTH,
        active_halving_steps=active_steps,
        optional_dgate_mode=OPTIONAL_DGATE_MODE,
        optional_dgate_start_depth=DGATE_START_DEPTH,
        optional_dgate_halving_steps=dgate_steps,
        chart_contract_ok=chart.row_ok,
        formula_rows=formulas,
        route_rows=routes,
        active_formula_rows=active_formula_rows,
        full_backtracking_formula_rows=full_formula_rows,
        active_chain_rows=active_chain_rows,
        any_chain_rows=any_chain_rows,
        direct_x0_rows=direct_x0_rows,
        internal_verify_rows=internal_rows,
        official_vpp_rows=vpp_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_x1_16_halving_chain_contract()
    print("p25 KSY-y X1(16) halving-chain contract gate")
    print("production")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  q_floor_sqrt_p={profile.q_floor_sqrt_p}")
    print(f"  hasse_bound={profile.hasse_bound}")
    print(f"  k={profile.k}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  active_halving_steps={profile.active_halving_steps}")
    print(f"  optional_dgate_mode={profile.optional_dgate_mode}")
    print(f"  optional_dgate_start_depth={profile.optional_dgate_start_depth}")
    print(f"  optional_dgate_halving_steps={profile.optional_dgate_halving_steps}")
    print(f"  chart_contract_ok={int(profile.chart_contract_ok)}")
    print("formula_rows")
    for row in profile.formula_rows:
        print(
            "  "
            f"{row.name}: active={int(row.active_first_branch_requirement)} "
            f"full={int(row.full_backtracking_control)} formula={row.formula}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: surface={int(row.has_A_xP16_surface)} "
            f"active_chain={int(row.has_active_first_branch_chain)} "
            f"any_chain={int(row.has_any_valid_halving_chain)} "
            f"x0={int(row.has_direct_x0)} "
            f"internal={int(row.has_internal_verify)} "
            f"vpp={int(row.has_official_vpp)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  active_formula_rows={profile.active_formula_rows}")
    print(f"  full_backtracking_formula_rows={profile.full_backtracking_formula_rows}")
    print(f"  active_chain_rows={profile.active_chain_rows}")
    print(f"  any_chain_rows={profile.any_chain_rows}")
    print(f"  direct_x0_rows={profile.direct_x0_rows}")
    print(f"  internal_verify_rows={profile.internal_verify_rows}")
    print(f"  official_vpp_rows={profile.official_vpp_rows}")
    print("interpretation")
    print("  active_surface_needs_38_first_branch_halvings_or_direct_x0=1")
    print("  any_valid_x0_can_be_accepted_by_official_vpp_even_without_active_path=1")
    print("  internal_verify_is_not_the_submission_boundary=1")
    print(f"ksy_y_x1_16_halving_chain_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(16) halving-chain contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
