#!/usr/bin/env python3
"""Cross-level extraction gap for the p25 KSY/Yang/H90 moonshot.

The current value-side target lives at odd level 507 (and conductor 39), while
the practical DANGER3 extractor is the 2-primary X_1(16) surface.  Since
gcd(16,507)=1, an odd-level modular-unit or H90 value theorem is not by itself
an extraction theorem.  This gate records the precise interface we still need:
either a real cross-level/fiber-product theorem that reaches the X_1(16)
Montgomery surface, or a direct official vpp.py-verified triple.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

from p25_ksy_y_danger3_extraction_surface_gate import (
    P25,
    profile_danger3_extraction_surface,
)
from p25_ksy_y_h90_value_theorem_intake_gate import (
    profile_h90_value_theorem_intake,
)
from p25_ksy_y_yang_x1_507_modular_unit_certificate_gate import (
    profile_yang_x1_507_modular_unit_certificate,
)


X16_LEVEL = 16
ODD_LEVEL = 507
CONDUCTOR_LEVEL = 39
CROSS_LEVEL = lcm(X16_LEVEL, ODD_LEVEL)


@dataclass(frozen=True)
class CrossLevelRouteRow:
    name: str
    payload: str
    has_odd_level_source: bool
    has_two_primary_source: bool
    has_cross_level_relation: bool
    supplies_x16_surface_data: bool
    supplies_concrete_vpp_triple: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class CrossLevelExtractionGapProfile:
    p: int
    odd_level: int
    x16_level: int
    conductor_level: int
    cross_level: int
    level_gcd: int
    levels_are_coprime: bool
    x1507_modular_unit_ok: bool
    h90_value_intake_ok: bool
    danger3_extraction_surface_ok: bool
    odd_payload_objects: tuple[str, ...]
    x16_required_fields: tuple[str, ...]
    route_rows: tuple[CrossLevelRouteRow, ...]
    pure_odd_payload_rows: int
    cross_level_relation_rows: int
    x16_surface_rows: int
    direct_triple_rows: int
    unsupported_auto_projection_rows: int
    row_ok: bool


def route_rows() -> tuple[CrossLevelRouteRow, ...]:
    return (
        CrossLevelRouteRow(
            name="y507_or_h0_value_identity_only",
            payload="exact Y_507 / canonical H0 / conductor-39 value or divisor theorem",
            has_odd_level_source=True,
            has_two_primary_source=False,
            has_cross_level_relation=False,
            supplies_x16_surface_data=False,
            supplies_concrete_vpp_triple=False,
            decision="odd_level_value_not_x16_extraction",
            first_missing_clause="cross-level relation to X_1(16), or direct (A,x0)",
            ok=True,
        ),
        CrossLevelRouteRow(
            name="x1507_modular_unit_provenance",
            payload="U_507 modular-unit provenance on X_1(507)",
            has_odd_level_source=True,
            has_two_primary_source=False,
            has_cross_level_relation=False,
            supplies_x16_surface_data=False,
            supplies_concrete_vpp_triple=False,
            decision="odd_level_unit_not_x16_extraction",
            first_missing_clause="theorem selecting the p25 value and a 2-primary extraction map",
            ok=True,
        ),
        CrossLevelRouteRow(
            name="x1_8112_fiber_product_theorem",
            payload="theorem on the X_1(16) x_j X_1(507) fiber product",
            has_odd_level_source=True,
            has_two_primary_source=True,
            has_cross_level_relation=True,
            supplies_x16_surface_data=False,
            supplies_concrete_vpp_triple=False,
            decision="cross_level_target_identified_specialization_missing",
            first_missing_clause="specialized p25 relation yielding y, A, xP16, or x0",
            ok=True,
        ),
        CrossLevelRouteRow(
            name="specialized_x16_surface_payload",
            payload="p25 theorem emits X_1(16) y plus model root data for A and xP16",
            has_odd_level_source=True,
            has_two_primary_source=True,
            has_cross_level_relation=True,
            supplies_x16_surface_data=True,
            supplies_concrete_vpp_triple=False,
            decision="x16_surface_reached_halving_or_vpp_missing",
            first_missing_clause="valid halving chain and official vpp.py verification",
            ok=True,
        ),
        CrossLevelRouteRow(
            name="direct_verified_pomerance_triple",
            payload="concrete (p,A,x0) verified by official vpp.py",
            has_odd_level_source=True,
            has_two_primary_source=True,
            has_cross_level_relation=True,
            supplies_x16_surface_data=True,
            supplies_concrete_vpp_triple=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_cross_level_extraction_gap() -> CrossLevelExtractionGapProfile:
    x1507 = profile_yang_x1_507_modular_unit_certificate()
    h90 = profile_h90_value_theorem_intake()
    extraction = profile_danger3_extraction_surface()
    rows = route_rows()

    level_gcd = gcd(X16_LEVEL, ODD_LEVEL)
    pure_odd = sum(
        row.has_odd_level_source
        and not row.has_two_primary_source
        and not row.has_cross_level_relation
        for row in rows
    )
    cross_rows = sum(row.has_cross_level_relation for row in rows)
    x16_rows = sum(row.supplies_x16_surface_data for row in rows)
    direct_rows = sum(row.supplies_concrete_vpp_triple for row in rows)
    unsupported_auto = sum(
        row.has_odd_level_source
        and not row.has_two_primary_source
        and row.decision.endswith("not_x16_extraction")
        for row in rows
    )

    row_ok = (
        P25 == 10**25 + 13
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CONDUCTOR_LEVEL == 39
        and CROSS_LEVEL == 8112
        and level_gcd == 1
        and x1507.row_ok
        and x1507.level == ODD_LEVEL
        and not x1507.direct_closer
        and h90.row_ok
        and h90.h90_positive_factor_count == 78
        and h90.h90_negative_factor_count == 78
        and extraction.row_ok
        and extraction.x16_surface.k == 42
        and extraction.x16_surface.p_mod_8 == 5
        and pure_odd == 2
        and cross_rows == 3
        and x16_rows == 2
        and direct_rows == 1
        and unsupported_auto == 2
        and tuple(row.decision for row in rows)
        == (
            "odd_level_value_not_x16_extraction",
            "odd_level_unit_not_x16_extraction",
            "cross_level_target_identified_specialization_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in rows)
    )

    return CrossLevelExtractionGapProfile(
        p=P25,
        odd_level=ODD_LEVEL,
        x16_level=X16_LEVEL,
        conductor_level=CONDUCTOR_LEVEL,
        cross_level=CROSS_LEVEL,
        level_gcd=level_gcd,
        levels_are_coprime=level_gcd == 1,
        x1507_modular_unit_ok=x1507.row_ok,
        h90_value_intake_ok=h90.row_ok,
        danger3_extraction_surface_ok=extraction.row_ok,
        odd_payload_objects=(
            "U_507 on X_1(507)",
            "Y_507=[2]^*U_507/U_507^4",
            "Norm_156(Y_507)",
            "canonical H0 78-over-78 Yang-fiber product",
            "conductor-39 mixed source",
        ),
        x16_required_fields=(
            "X_1(16) parameter y",
            "model root x",
            "Montgomery parameter A",
            "marked coordinate xP16",
            "valid halving chain to x0",
            "official vpp.py verification",
        ),
        route_rows=rows,
        pure_odd_payload_rows=pure_odd,
        cross_level_relation_rows=cross_rows,
        x16_surface_rows=x16_rows,
        direct_triple_rows=direct_rows,
        unsupported_auto_projection_rows=unsupported_auto,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_cross_level_extraction_gap()
    print("p25 KSY-y cross-level extraction-gap gate")
    print("levels")
    print(f"  odd_level={profile.odd_level}")
    print(f"  conductor_level={profile.conductor_level}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  level_gcd={profile.level_gcd}")
    print(f"  cross_level_lcm={profile.cross_level}")
    print(f"  levels_are_coprime={int(profile.levels_are_coprime)}")
    print("dependency_gates")
    print(f"  x1507_modular_unit_ok={int(profile.x1507_modular_unit_ok)}")
    print(f"  h90_value_intake_ok={int(profile.h90_value_intake_ok)}")
    print(f"  danger3_extraction_surface_ok={int(profile.danger3_extraction_surface_ok)}")
    print("odd_payload_objects")
    for obj in profile.odd_payload_objects:
        print(f"  {obj}")
    print("x16_required_fields")
    for field in profile.x16_required_fields:
        print(f"  {field}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: odd={int(row.has_odd_level_source)} "
            f"two_primary={int(row.has_two_primary_source)} "
            f"cross={int(row.has_cross_level_relation)} "
            f"x16_surface={int(row.supplies_x16_surface_data)} "
            f"vpp={int(row.supplies_concrete_vpp_triple)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  pure_odd_payload_rows={profile.pure_odd_payload_rows}")
    print(f"  cross_level_relation_rows={profile.cross_level_relation_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  direct_triple_rows={profile.direct_triple_rows}")
    print(f"  unsupported_auto_projection_rows={profile.unsupported_auto_projection_rows}")
    print("interpretation")
    print("  odd_level_KSY_Yang_H90_value_is_not_automatically_X1_16_data=1")
    print("  positive_moonshot_artifact_must_live_on_X1_8112_or_emit_verified_triple=1")
    print("  extraction_gap_is_cross_level_not_a_75_atom_enumeration=1")
    print(f"ksy_y_cross_level_extraction_gap_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("cross-level extraction-gap regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
