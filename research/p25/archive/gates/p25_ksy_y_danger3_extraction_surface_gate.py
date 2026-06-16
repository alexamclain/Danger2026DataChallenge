#!/usr/bin/env python3
"""DANGER3 extraction surface for KSY/Y507/H0 theorem hits.

The H0/Y507 value-theorem intake tells us what counts as a live arithmetic
theorem target.  DANGER3 still needs a concrete Montgomery triple `(p,A,x0)`.
This gate records the exact extraction surface supplied by the practical
X_1(16) code and separates it from the current KSY/Yang/H0 finite payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt

from p25_ksy_y_h90_value_theorem_intake_gate import (
    profile_h90_value_theorem_intake,
)


P25 = 10**25 + 13


@dataclass(frozen=True)
class X16MontgomerySurface:
    p: int
    p_mod_8: int
    p_supports_x16_fast_sqrt: bool
    k: int
    a_numerator_coefficients_desc: tuple[int, ...]
    a_formula: str
    x_model_quadratic: str
    xP16_formula: str
    nonsplit_filter_formula: str
    first_half_gate_formula: str
    first_half_sd_formula: str
    halving_chain_requirement: str
    formula_count: int
    row_ok: bool


@dataclass(frozen=True)
class ExtractionRouteRow:
    name: str
    finite_payload: str
    supplies_x16_y_or_montgomery_surface: bool
    supplies_halving_chain_or_x0: bool
    supplies_concrete_vpp_triple: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class Danger3ExtractionSurfaceProfile:
    h90_value_intake_ok: bool
    x16_surface: X16MontgomerySurface
    route_rows: tuple[ExtractionRouteRow, ...]
    x16_surface_rows: int
    direct_triple_rows: int
    unresolved_finite_payload_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def compute_k(p: int) -> int:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return bound.bit_length()


def x16_surface() -> X16MontgomerySurface:
    coeffs = (1, -8, 24, -32, 8, 32, -48, 32, -8)
    p_mod_8 = P25 % 8
    k = compute_k(P25)
    row_ok = (
        P25 % 8 == 5
        and k == 42
        and coeffs == (1, -8, 24, -32, 8, 32, -48, 32, -8)
        and gcd(4, P25) == 1
    )
    return X16MontgomerySurface(
        p=P25,
        p_mod_8=p_mod_8,
        p_supports_x16_fast_sqrt=p_mod_8 == 5,
        k=k,
        a_numerator_coefficients_desc=coeffs,
        a_formula=(
            "A = N(y) / (4*(y-1)^4), "
            "N=y^8-8y^7+24y^6-32y^5+8y^4+32y^3-48y^2+32y-8"
        ),
        x_model_quadratic=(
            "(y^2-2y)*x^2 + (2y^2-y^3)*x + (1-y) = 0"
        ),
        xP16_formula="xP16 = x / (x-y)",
        nonsplit_filter_formula="(y^2-2) * (y^2-4y+2) is nonsquare",
        first_half_gate_formula="(y-1) * (y^2-2) * (y^2-2y+2) is square",
        first_half_sd_formula=(
            "sd = y*z / (2*(x-y)*(y-1)^2), where z^2=(y-1)*(y^2-2)*(y^2-2y+2)"
        ),
        halving_chain_requirement=(
            "starting at xP16, repeatedly choose valid Montgomery halves until "
            "a point x0 has exact 2^k doubling-to-zero behavior under vpp.py"
        ),
        formula_count=7,
        row_ok=row_ok,
    )


def route_rows() -> tuple[ExtractionRouteRow, ...]:
    return (
        ExtractionRouteRow(
            name="exact_P_or_theta2_divisor_payload",
            finite_payload="exact P / theta2 / bridge divisor data",
            supplies_x16_y_or_montgomery_surface=False,
            supplies_halving_chain_or_x0=False,
            supplies_concrete_vpp_triple=False,
            decision="finite_payload_not_extraction",
            first_missing_clause="map from bridge/theta2 data to Montgomery A and x0",
            ok=True,
        ),
        ExtractionRouteRow(
            name="Y507_or_canonical_H0_value_payload",
            finite_payload="Y_507 or canonical H0 value/divisor identity",
            supplies_x16_y_or_montgomery_surface=False,
            supplies_halving_chain_or_x0=False,
            supplies_concrete_vpp_triple=False,
            decision="finite_payload_not_extraction",
            first_missing_clause="map from Y507/H0 value to X1(16) y, A, xP16, or x0",
            ok=True,
        ),
        ExtractionRouteRow(
            name="x16_y_A_xP16_payload",
            finite_payload="X1(16) parameter y plus model root x giving A and xP16",
            supplies_x16_y_or_montgomery_surface=True,
            supplies_halving_chain_or_x0=False,
            supplies_concrete_vpp_triple=False,
            decision="extraction_surface_identified_halving_missing",
            first_missing_clause="valid halving chain from xP16 to concrete x0",
            ok=True,
        ),
        ExtractionRouteRow(
            name="x16_y_A_x0_payload",
            finite_payload="X1(16) parameter y, A, and halved x0",
            supplies_x16_y_or_montgomery_surface=True,
            supplies_halving_chain_or_x0=True,
            supplies_concrete_vpp_triple=False,
            decision="extraction_ready_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        ExtractionRouteRow(
            name="direct_verified_pomerance_triple",
            finite_payload="concrete (p,A,x0) verified by official vpp.py",
            supplies_x16_y_or_montgomery_surface=True,
            supplies_halving_chain_or_x0=True,
            supplies_concrete_vpp_triple=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_danger3_extraction_surface() -> Danger3ExtractionSurfaceProfile:
    intake = profile_h90_value_theorem_intake()
    surface = x16_surface()
    rows = route_rows()
    x16_rows = sum(row.supplies_x16_y_or_montgomery_surface for row in rows)
    direct_rows = sum(row.supplies_concrete_vpp_triple for row in rows)
    unresolved = sum(row.decision == "finite_payload_not_extraction" for row in rows)
    extraction_ready = sum(row.decision in {"extraction_ready_vpp_missing", "submission_ready"} for row in rows)
    submission_ready = sum(row.decision == "submission_ready" for row in rows)
    row_ok = (
        intake.row_ok
        and surface.row_ok
        and len(rows) == 5
        and x16_rows == 3
        and direct_rows == 1
        and unresolved == 2
        and extraction_ready == 2
        and submission_ready == 1
        and tuple(row.decision for row in rows)
        == (
            "finite_payload_not_extraction",
            "finite_payload_not_extraction",
            "extraction_surface_identified_halving_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in rows)
    )
    return Danger3ExtractionSurfaceProfile(
        h90_value_intake_ok=intake.row_ok,
        x16_surface=surface,
        route_rows=rows,
        x16_surface_rows=x16_rows,
        direct_triple_rows=direct_rows,
        unresolved_finite_payload_rows=unresolved,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_danger3_extraction_surface()
    print("p25 KSY-y DANGER3 extraction-surface gate")
    print("dependency_gates")
    print(f"  h90_value_intake_ok={int(profile.h90_value_intake_ok)}")
    print("x16_montgomery_surface")
    surface = profile.x16_surface
    print(f"  p_mod_8={surface.p_mod_8}")
    print(f"  p_supports_x16_fast_sqrt={int(surface.p_supports_x16_fast_sqrt)}")
    print(f"  k={surface.k}")
    print(f"  A_numerator_coefficients_desc={surface.a_numerator_coefficients_desc}")
    print(f"  A_formula={surface.a_formula}")
    print(f"  x_model_quadratic={surface.x_model_quadratic}")
    print(f"  xP16_formula={surface.xP16_formula}")
    print(f"  nonsplit_filter_formula={surface.nonsplit_filter_formula}")
    print(f"  first_half_gate_formula={surface.first_half_gate_formula}")
    print(f"  first_half_sd_formula={surface.first_half_sd_formula}")
    print(f"  halving_chain_requirement={surface.halving_chain_requirement}")
    print(f"  formula_count={surface.formula_count}")
    print(f"  ok={int(surface.row_ok)}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: x16={int(row.supplies_x16_y_or_montgomery_surface)} "
            f"halving_or_x0={int(row.supplies_halving_chain_or_x0)} "
            f"vpp={int(row.supplies_concrete_vpp_triple)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  direct_triple_rows={profile.direct_triple_rows}")
    print(f"  unresolved_finite_payload_rows={profile.unresolved_finite_payload_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  H0_Y507_theta2_payloads_are_not_DANGER3_extractions_by_themselves=1")
    print("  theorem_hit_must_map_to_x16_surface_or_direct_verified_triple=1")
    print("  x16_surface_equations_are_recorded_from_practical_search_path=1")
    print("  still_missing_actual_map_from_KSY_Yang_H0_value_to_A_x0=1")
    print(f"ksy_y_danger3_extraction_surface_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("DANGER3 extraction-surface regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
