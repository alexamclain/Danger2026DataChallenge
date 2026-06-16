#!/usr/bin/env python3
"""Constructive torsion-gluing contract for the p25 X_1(8112) bridge.

The bridge-theorem intake says that a useful claim must glue the odd-level
KSY/Yang/H90 target to the X_1(16) extraction surface over the same j-line.
This gate records the elementary coprime-torsion arithmetic behind that
requirement.  If R has exact order 8112 = 16 * 507, then normalized projections
recover exact level-16 and level-507 points on the same curve.  Conversely, an
exact 16-point and exact 507-point on the same curve combine to an 8112-point.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

from p25_ksy_y_cross_level_extraction_gap_gate import (
    CROSS_LEVEL,
    ODD_LEVEL,
    P25,
    X16_LEVEL,
)


@dataclass(frozen=True)
class ProjectionRow:
    name: str
    multiplier: int
    exact_order: int
    annihilator: int
    role: str
    ok: bool


@dataclass(frozen=True)
class GluingRouteRow:
    name: str
    supplies_odd_component: bool
    supplies_x16_component: bool
    same_curve_or_same_j: bool
    supplies_order_8112_generator: bool
    supplies_practical_x16_surface: bool
    supplies_halving_or_x0: bool
    supplies_vpp_triple: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class X18112TorsionGluingContract:
    p: int
    x16_level: int
    odd_level: int
    cross_level: int
    levels_are_coprime: bool
    inv_507_mod_16: int
    inv_16_mod_507: int
    raw_p16_multiplier: int
    normalized_p16_multiplier: int
    raw_q507_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    projection_rows: tuple[ProjectionRow, ...]
    route_rows: tuple[GluingRouteRow, ...]
    normalized_projections_recombine_to_R: bool
    exact_projection_rows: int
    same_curve_bridge_rows: int
    generator_bridge_rows: int
    practical_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def order_of_multiple(order: int, multiplier: int) -> int:
    return order // gcd(order, multiplier)


def projection_rows() -> tuple[ProjectionRow, ...]:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    raw_p16 = ODD_LEVEL
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    raw_q507 = X16_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    return (
        ProjectionRow(
            name="raw_16_component_from_R",
            multiplier=raw_p16,
            exact_order=order_of_multiple(CROSS_LEVEL, raw_p16),
            annihilator=X16_LEVEL,
            role="[507]R has exact order 16, but is scaled by 507 mod 16",
            ok=order_of_multiple(CROSS_LEVEL, raw_p16) == X16_LEVEL,
        ),
        ProjectionRow(
            name="normalized_16_component_from_R",
            multiplier=normalized_p16,
            exact_order=order_of_multiple(CROSS_LEVEL, normalized_p16),
            annihilator=X16_LEVEL,
            role="[3*507]R is the normalized X_1(16) component P16",
            ok=(
                inv_507 == 3
                and normalized_p16 == 1521
                and order_of_multiple(CROSS_LEVEL, normalized_p16) == X16_LEVEL
                and (X16_LEVEL * normalized_p16) % CROSS_LEVEL == 0
            ),
        ),
        ProjectionRow(
            name="raw_507_component_from_R",
            multiplier=raw_q507,
            exact_order=order_of_multiple(CROSS_LEVEL, raw_q507),
            annihilator=ODD_LEVEL,
            role="[16]R has exact order 507, but is scaled by 16 mod 507",
            ok=order_of_multiple(CROSS_LEVEL, raw_q507) == ODD_LEVEL,
        ),
        ProjectionRow(
            name="normalized_507_component_from_R",
            multiplier=normalized_q507,
            exact_order=order_of_multiple(CROSS_LEVEL, normalized_q507),
            annihilator=ODD_LEVEL,
            role="[16*16^-1 mod 507]R is the normalized X_1(507) component Q507",
            ok=(
                (X16_LEVEL * inv_16) % ODD_LEVEL == 1
                and order_of_multiple(CROSS_LEVEL, normalized_q507) == ODD_LEVEL
                and (ODD_LEVEL * normalized_q507) % CROSS_LEVEL == 0
            ),
        ),
    )


def route_rows() -> tuple[GluingRouteRow, ...]:
    return (
        GluingRouteRow(
            name="odd_level_value_only",
            supplies_odd_component=True,
            supplies_x16_component=False,
            same_curve_or_same_j=False,
            supplies_order_8112_generator=False,
            supplies_practical_x16_surface=False,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="odd_component_not_extraction",
            first_missing_clause="same-curve X_1(16) component or order-8112 generator",
            ok=True,
        ),
        GluingRouteRow(
            name="generic_x16_surface_only",
            supplies_odd_component=False,
            supplies_x16_component=True,
            same_curve_or_same_j=False,
            supplies_order_8112_generator=False,
            supplies_practical_x16_surface=True,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="x16_component_not_ksy_bridge",
            first_missing_clause="exact odd KSY/Yang/H90 component on the same curve",
            ok=True,
        ),
        GluingRouteRow(
            name="independent_level16_and_level507_data",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=False,
            supplies_order_8112_generator=False,
            supplies_practical_x16_surface=False,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="reject_unglued_components",
            first_missing_clause="same j-invariant or same elliptic curve",
            ok=True,
        ),
        GluingRouteRow(
            name="same_curve_P16_Q507_pair",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=True,
            supplies_order_8112_generator=False,
            supplies_practical_x16_surface=False,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="construct_order_8112_generator_then_specialize_x16",
            first_missing_clause="practical y, model root, A, and xP16 extraction data",
            ok=True,
        ),
        GluingRouteRow(
            name="order_8112_generator_R",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=True,
            supplies_order_8112_generator=True,
            supplies_practical_x16_surface=False,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="project_R_to_P16_and_Q507_then_specialize",
            first_missing_clause="practical X_1(16) y, model root, A, and xP16",
            ok=True,
        ),
        GluingRouteRow(
            name="order_8112_bridge_with_x16_surface",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=True,
            supplies_order_8112_generator=True,
            supplies_practical_x16_surface=True,
            supplies_halving_or_x0=False,
            supplies_vpp_triple=False,
            decision="x16_surface_reached_halving_or_vpp_missing",
            first_missing_clause="valid halving chain from xP16 to x0",
            ok=True,
        ),
        GluingRouteRow(
            name="order_8112_bridge_with_x0",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=True,
            supplies_order_8112_generator=True,
            supplies_practical_x16_surface=True,
            supplies_halving_or_x0=True,
            supplies_vpp_triple=False,
            decision="extraction_ready_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        GluingRouteRow(
            name="direct_verified_p25_triple",
            supplies_odd_component=True,
            supplies_x16_component=True,
            same_curve_or_same_j=True,
            supplies_order_8112_generator=True,
            supplies_practical_x16_surface=True,
            supplies_halving_or_x0=True,
            supplies_vpp_triple=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_x1_8112_torsion_gluing_contract() -> X18112TorsionGluingContract:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    raw_p16 = ODD_LEVEL
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    raw_q507 = X16_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    projection_sum = (normalized_p16 + normalized_q507) % CROSS_LEVEL
    projections = projection_rows()
    routes = route_rows()
    same_curve_rows = sum(
        row.supplies_odd_component and row.supplies_x16_component and row.same_curve_or_same_j
        for row in routes
    )
    generator_rows = sum(row.supplies_order_8112_generator for row in routes)
    practical_rows = sum(row.supplies_practical_x16_surface for row in routes)
    extraction_rows = sum(row.supplies_halving_or_x0 for row in routes)
    submission_rows = sum(row.supplies_vpp_triple for row in routes)
    row_ok = (
        P25 == 10**25 + 13
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CROSS_LEVEL == 8112
        and lcm(X16_LEVEL, ODD_LEVEL) == CROSS_LEVEL
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and inv_507 == 3
        and (ODD_LEVEL * inv_507) % X16_LEVEL == 1
        and (X16_LEVEL * inv_16) % ODD_LEVEL == 1
        and raw_p16 == 507
        and normalized_p16 == 1521
        and raw_q507 == 16
        and order_of_multiple(CROSS_LEVEL, raw_p16) == 16
        and order_of_multiple(CROSS_LEVEL, normalized_p16) == 16
        and order_of_multiple(CROSS_LEVEL, raw_q507) == 507
        and order_of_multiple(CROSS_LEVEL, normalized_q507) == 507
        and projection_sum == 1
        and all(row.ok for row in projections)
        and len(routes) == 8
        and same_curve_rows == 5
        and generator_rows == 4
        and practical_rows == 4
        and extraction_rows == 2
        and submission_rows == 1
        and tuple(row.decision for row in routes)
        == (
            "odd_component_not_extraction",
            "x16_component_not_ksy_bridge",
            "reject_unglued_components",
            "construct_order_8112_generator_then_specialize_x16",
            "project_R_to_P16_and_Q507_then_specialize",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in routes)
    )
    return X18112TorsionGluingContract(
        p=P25,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        cross_level=CROSS_LEVEL,
        levels_are_coprime=gcd(X16_LEVEL, ODD_LEVEL) == 1,
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        raw_p16_multiplier=raw_p16,
        normalized_p16_multiplier=normalized_p16,
        raw_q507_multiplier=raw_q507,
        normalized_q507_multiplier=normalized_q507,
        normalized_projection_sum_mod_8112=projection_sum,
        projection_rows=projections,
        route_rows=routes,
        normalized_projections_recombine_to_R=projection_sum == 1,
        exact_projection_rows=sum(row.ok for row in projections),
        same_curve_bridge_rows=same_curve_rows,
        generator_bridge_rows=generator_rows,
        practical_surface_rows=practical_rows,
        extraction_ready_rows=extraction_rows,
        submission_ready_rows=submission_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_x1_8112_torsion_gluing_contract()
    print("p25 KSY-y X1(8112) torsion-gluing contract gate")
    print("levels")
    print(f"  p={profile.p}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  cross_level={profile.cross_level}")
    print(f"  levels_are_coprime={int(profile.levels_are_coprime)}")
    print("projection_arithmetic")
    print(f"  inv_507_mod_16={profile.inv_507_mod_16}")
    print(f"  inv_16_mod_507={profile.inv_16_mod_507}")
    print(f"  raw_p16_multiplier={profile.raw_p16_multiplier}")
    print(f"  normalized_p16_multiplier={profile.normalized_p16_multiplier}")
    print(f"  raw_q507_multiplier={profile.raw_q507_multiplier}")
    print(f"  normalized_q507_multiplier={profile.normalized_q507_multiplier}")
    print(
        "  normalized_projection_sum_mod_8112="
        f"{profile.normalized_projection_sum_mod_8112}"
    )
    print("projection_rows")
    for row in profile.projection_rows:
        print(
            "  "
            f"{row.name}: multiplier={row.multiplier} exact_order={row.exact_order} "
            f"annihilator={row.annihilator} role={row.role}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: odd={int(row.supplies_odd_component)} "
            f"x16={int(row.supplies_x16_component)} "
            f"same_j={int(row.same_curve_or_same_j)} "
            f"R8112={int(row.supplies_order_8112_generator)} "
            f"surface={int(row.supplies_practical_x16_surface)} "
            f"x0={int(row.supplies_halving_or_x0)} "
            f"vpp={int(row.supplies_vpp_triple)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  exact_projection_rows={profile.exact_projection_rows}")
    print(f"  same_curve_bridge_rows={profile.same_curve_bridge_rows}")
    print(f"  generator_bridge_rows={profile.generator_bridge_rows}")
    print(f"  practical_surface_rows={profile.practical_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  same_curve_exact_16_and_507_torsion_recombine_to_order_8112=1")
    print("  order_8112_generator_projects_to_x16_and_x507_components=1")
    print("  projection_arithmetic_is_not_yet_the_x16_montgomery_surface=1")
    print(f"ksy_y_x1_8112_torsion_gluing_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(8112) torsion-gluing contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
