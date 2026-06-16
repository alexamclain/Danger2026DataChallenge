#!/usr/bin/env python3
"""Koo-Shin 2010 Theorem 6.2 applied to the conductor-39 source.

The full-paper screen says Theorem 6.2 is not a direct producer for the p25
75-atom product: it builds complete one-axis X_1(N) products.  This gate keeps
the positive part too.  At N=39, the primitive source U_chi=-chi_39, its cube
V_bal, and its sixth-power word W all satisfy the Theorem 6.2 congruences.

Thus Koo-Shin 6.2 can certify the compact X_1(39) modular-unit source, but it
still does not provide the finite-field value/divisor theorem, cross-level
X_1(16) surface, halving payload, or vpp.py triple.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_ksy_y_koo_shin_2010_full_surface_screen_gate import (
    profile_koo_shin_2010_full_surface_screen,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39


FULL_FIBER_LENGTH = CONDUCTOR


@dataclass(frozen=True)
class Theorem62SourceRow:
    name: str
    scale_from_u_chi: int
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_sum_mod_level: int
    theorem62_congruences_ok: bool
    lemma61_full_fiber_cells: int
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class Theorem62RouteRow:
    name: str
    claim: str
    decision: str
    source_certified: bool
    direct_product_closer: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class KooShinTheorem62Conductor39UnitProfile:
    level: int
    theorem62_present: bool
    primitive_unit_ok: bool
    distribution_lift_ok: bool
    source_rows: tuple[Theorem62SourceRow, ...]
    route_rows: tuple[Theorem62RouteRow, ...]
    theorem62_congruence_rows: int
    source_certified_rows: int
    direct_product_closer_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_route_rows: int
    full_fiber_length: int
    yang_lift_length: int
    yang_lifted_w_support: int
    positive_payload: str
    remaining_upgrade: str
    row_ok: bool


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(word.values()).items()))


def scaled_u_chi(scale: int) -> dict[int, int]:
    return {
        residue: -scale * chi39(residue)
        for residue in range(1, CONDUCTOR)
        if chi39(residue)
    }


def theorem62_source_row(
    name: str,
    scale: int,
    decision: str,
    first_missing_clause: str,
) -> Theorem62SourceRow:
    word = scaled_u_chi(scale)
    exponent_sum = sum(word.values())
    quadratic_sum = sum(residue * residue * coefficient for residue, coefficient in word.items())
    congruences_ok = exponent_sum % 12 == 0 and quadratic_sum % CONDUCTOR == 0
    return Theorem62SourceRow(
        name=name,
        scale_from_u_chi=scale,
        support=len(word),
        coefficient_counts=coefficient_counts(word),
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum_mod_level=quadratic_sum % CONDUCTOR,
        theorem62_congruences_ok=congruences_ok,
        lemma61_full_fiber_cells=len(word) * FULL_FIBER_LENGTH,
        decision=decision,
        first_missing_clause=first_missing_clause,
        ok=(
            congruences_ok
            and len(word) == 24
            and len(word) * FULL_FIBER_LENGTH == 936
        ),
    )


def route_rows() -> tuple[Theorem62RouteRow, ...]:
    return (
        Theorem62RouteRow(
            name="primitive_u_chi_source",
            claim="Koo-Shin 6.2 certifies U_chi=-chi_39 as an X_1(39) one-axis product",
            decision="source_certified_value_theorem_missing",
            source_certified=True,
            direct_product_closer=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value/divisor theorem and Yang/Hilbert-90 descent",
            ok=True,
        ),
        Theorem62RouteRow(
            name="w_then_yang_distribution_lift",
            claim="Koo-Shin 6.2 certifies W=6*U_chi before the 13-fiber Yang lift",
            decision="period_norm_source_certified_theorem_missing",
            source_certified=True,
            direct_product_closer=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="the theorem that evaluates or identifies Norm_156(Y_507)",
            ok=True,
        ),
        Theorem62RouteRow(
            name="theorem62_as_exact_75_atom_product",
            claim="Use Theorem 6.2 directly as the p25 75-atom product producer",
            decision="reject_one_axis_full_fiber_not_mixed_product",
            source_certified=False,
            direct_product_closer=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="mixed C3 x C169 row graph, T edge, equal 75 atoms, and orientation",
            ok=True,
        ),
        Theorem62RouteRow(
            name="theorem62_as_danger3_extraction",
            claim="Use Theorem 6.2 as the DANGER3 X_1(16) extraction path",
            decision="reject_no_x16_surface_or_halving_payload",
            source_certified=False,
            direct_product_closer=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="A,xP16 surface plus x-chain, sqrt-witness chain, or vpp-verified x0",
            ok=True,
        ),
    )


def profile_koo_shin_theorem62_conductor39_unit() -> KooShinTheorem62Conductor39UnitProfile:
    full_screen = profile_koo_shin_2010_full_surface_screen()
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    lift = profile_yang_y507_conductor39_distribution_lift()

    sources = (
        theorem62_source_row(
            "primitive_character_unit_U_chi",
            1,
            "certifies_X1_39_source_not_value",
            "finite-field value/divisor theorem",
        ),
        theorem62_source_row(
            "balanced_hilbert90_potential_V_bal",
            3,
            "certifies_balanced_source_not_h90_boundary",
            "Hilbert-90 descent boundary and value theorem",
        ),
        theorem62_source_row(
            "period_norm_word_W",
            6,
            "certifies_period_norm_source_not_y507_value",
            "Yang 13-fiber value/divisor theorem for Norm_156(Y_507)",
        ),
    )
    routes = route_rows()
    theorem62_rows = sum(row.theorem62_congruences_ok for row in sources)
    source_certified = sum(row.source_certified for row in routes)
    direct_closers = sum(row.direct_product_closer for row in routes)
    extraction_ready = sum(row.extraction_ready for row in routes)
    submission_ready = sum(row.submission_ready for row in routes)
    rejected_routes = sum(row.decision.startswith("reject_") for row in routes)
    row_ok = (
        full_screen.row_ok
        and full_screen.text_scan.has_theorem_6_2
        and primitive.row_ok
        and lift.row_ok
        and CONDUCTOR == 39
        and lift.lift_length == 13
        and lift.period_norm_support == 312
        and theorem62_rows == 3
        and source_certified == 2
        and direct_closers == 0
        and extraction_ready == 0
        and submission_ready == 0
        and rejected_routes == 2
        and all(row.ok for row in sources)
        and all(row.ok for row in routes)
        and sources[0].coefficient_counts == ((-1, 12), (1, 12))
        and sources[1].coefficient_counts == ((-3, 12), (3, 12))
        and sources[2].coefficient_counts == ((-6, 12), (6, 12))
    )
    return KooShinTheorem62Conductor39UnitProfile(
        level=CONDUCTOR,
        theorem62_present=full_screen.text_scan.has_theorem_6_2,
        primitive_unit_ok=primitive.row_ok,
        distribution_lift_ok=lift.row_ok,
        source_rows=sources,
        route_rows=routes,
        theorem62_congruence_rows=theorem62_rows,
        source_certified_rows=source_certified,
        direct_product_closer_rows=direct_closers,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        rejected_route_rows=rejected_routes,
        full_fiber_length=FULL_FIBER_LENGTH,
        yang_lift_length=lift.lift_length,
        yang_lifted_w_support=lift.period_norm_support,
        positive_payload=(
            "Koo-Shin 2010 Theorem 6.2 certifies U_chi, V_bal, and W as "
            "level-39 one-axis X_1(39) products satisfying the modularity "
            "congruences."
        ),
        remaining_upgrade=(
            "a finite-field value/divisor theorem for the source, Yang/Hilbert-90 "
            "descent, cross-level X_1(16) surface, halving payload, and vpp.py "
            "verification"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_koo_shin_theorem62_conductor39_unit()
    print("p25 KSY-y Koo-Shin 2010 Theorem 6.2 conductor-39 unit gate")
    print("inputs")
    print(f"  level={profile.level}")
    print(f"  theorem62_present={int(profile.theorem62_present)}")
    print(f"  primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"  distribution_lift_ok={int(profile.distribution_lift_ok)}")
    print("source_rows")
    for row in profile.source_rows:
        print(
            "  "
            f"{row.name}: scale={row.scale_from_u_chi} support={row.support} "
            f"counts={row.coefficient_counts} sum_mod12={row.exponent_sum_mod_12} "
            f"quad_mod39={row.quadratic_sum_mod_level} "
            f"theorem62={int(row.theorem62_congruences_ok)} "
            f"lemma61_full_fiber_cells={row.lemma61_full_fiber_cells} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} source={int(row.source_certified)} "
            f"direct_product={int(row.direct_product_closer)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  theorem62_congruence_rows={profile.theorem62_congruence_rows}")
    print(f"  source_certified_rows={profile.source_certified_rows}")
    print(f"  direct_product_closer_rows={profile.direct_product_closer_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_route_rows={profile.rejected_route_rows}")
    print(f"  full_fiber_length={profile.full_fiber_length}")
    print(f"  yang_lift_length={profile.yang_lift_length}")
    print(f"  yang_lifted_w_support={profile.yang_lifted_w_support}")
    print("interpretation")
    print("  koo_shin_6_2_certifies_conductor39_unit_source=1")
    print("  theorem_6_2_is_not_the_75_atom_mixed_product=1")
    print("  theorem_6_2_is_not_danger3_x16_extraction=1")
    print(f"  remaining_upgrade={profile.remaining_upgrade}")
    print(f"ksy_y_koo_shin_2010_theorem62_conductor39_unit_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin 2010 Theorem 6.2 conductor-39 unit regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
