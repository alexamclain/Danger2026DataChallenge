#!/usr/bin/env python3
"""Exact KSY normalized-y Siegel formula instantiation for p25.

Koo-Shin-Yoon's normalized y-coordinate has the Siegel-function shape

    y(Q) = -g(2Q) / g(Q)^4.

For the p25 anti-invariant product this gives a concrete four-layer
Siegel-exponent payload for every atom A in the accepted K trace:

    y(A)/y(-A) = g(2A) * g(A)^-4 * g(-2A)^-1 * g(-A)^4.

This gate is the exact formula instantiation promised by the source-exactness
map.  It checks that the four layers are disjoint, recover the accepted theta2
footprint, pass the elementary KL congruence hygiene, and still route as a
divisor/additive payload unless a value theorem also supplies period-156 theta2
context.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    anti_invariant_y_footprint,
    centered_source_trace,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    RAW_LEVEL,
    kl_profile,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate import (
    route_raw_orientation,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate import (
    profile_raw_orientation_value_route,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord, scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class KsyYSiegelLayer:
    name: str
    coefficient: int
    support: int
    sample: tuple[Coord, ...]


@dataclass(frozen=True)
class KsyYSiegelFormulaProfile:
    raw_center: Coord
    raw_d_step: Coord
    raw_k_step: Coord
    source_atom_support: int
    formula_layers: tuple[KsyYSiegelLayer, ...]
    layer_supports_disjoint: bool
    footprint_support: int
    footprint_coefficient_counts: tuple[tuple[int, int], ...]
    footprint_matches_anti_invariant_product: bool
    kl_exponent_screen_ok: bool
    raw_divisor_route_ok: bool
    raw_divisor_emits: str
    raw_value_route_period: int
    raw_value_route_unique_fp_root: bool
    raw_value_route_needs_period_context: bool
    generic_single_y_value_rejected: bool
    exact_formula_contract: str
    row_ok: bool


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % RIGHT_ORDER, (-coord[1]) % C_ORDER)


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def ksy_y_siegel_layers(centers: Ring) -> tuple[tuple[str, int, set[Coord]], ...]:
    positive = set(centers)
    negative = {inverse_coord(point) for point in centers}
    doubled_positive = {scale_coord(point, 2) for point in centers}
    doubled_negative = {scale_coord(inverse_coord(point), 2) for point in centers}
    return (
        ("g(2A)", 1, doubled_positive),
        ("g(A)^-4", -4, positive),
        ("g(-2A)^-1", -1, doubled_negative),
        ("g(-A)^4", 4, negative),
    )


def layer_profiles(layers: tuple[tuple[str, int, set[Coord]], ...]) -> tuple[KsyYSiegelLayer, ...]:
    return tuple(
        KsyYSiegelLayer(
            name=name,
            coefficient=coefficient,
            support=len(points),
            sample=tuple(sorted(points)[:3]),
        )
        for name, coefficient, points in layers
    )


def formula_footprint_from_layers(layers: tuple[tuple[str, int, set[Coord]], ...]) -> Ring:
    footprint: Ring = {}
    for _name, coefficient, points in layers:
        for point in points:
            add_ring_entry(footprint, point, coefficient)
    return dict(sorted(footprint.items()))


def layer_sets_are_disjoint(layers: tuple[tuple[str, int, set[Coord]], ...]) -> bool:
    seen: set[Coord] = set()
    for _name, _coefficient, points in layers:
        if seen.intersection(points):
            return False
        seen.update(points)
    return True


def profile_ksy_y_siegel_formula() -> KsyYSiegelFormulaProfile:
    raw_center = add_coord(BASE_POINT, D_SHIFT)
    centers = centered_source_trace(raw_center, KERNEL_SHIFT, D_SHIFT)
    layers = ksy_y_siegel_layers(centers)
    formula_footprint = formula_footprint_from_layers(layers)
    _expected_centers, expected_footprint = anti_invariant_y_footprint(
        raw_center,
        KERNEL_SHIFT,
        D_SHIFT,
    )
    kl = kl_profile(
        "ksy_y_siegel_formula_theta2_inverse_raw_level",
        formula_footprint,
        RAW_LEVEL,
        C_ORDER,
        RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation=(
            "exact KSY y=-g(2Q)/g(Q)^4 formula instantiation; still needs "
            "challenge-legal theorem or period-156 context for value output"
        ),
    )
    route = route_raw_orientation(
        "ksy_y_siegel_formula_raw_divisor_route",
        raw_center,
        D_SHIFT,
        1,
        False,
    )
    value_route = profile_raw_orientation_value_route()
    generic_single_y_value_rejected = (
        len(centers) == 75
        and value_route.ambient_value_route_has_mu11_ambiguity
        and value_route.proper_period_shortcuts_all_fail
    )
    layer_disjoint = layer_sets_are_disjoint(layers)
    formula_matches = formula_footprint == expected_footprint
    row_ok = (
        raw_center == (47, 28)
        and len(centers) == 75
        and layer_disjoint
        and tuple(layer.support for layer in layer_profiles(layers)) == (75, 75, 75, 75)
        and len(formula_footprint) == 300
        and coefficient_counts(formula_footprint) == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and formula_matches
        and kl.quadratic_relations_ok
        and kl.exponent_sum_mod_12 == 0
        and route.certificate_path_ok
        and route.emitted_payload == "theta2_inverse"
        and route.theta2_candidate_profile.recovered_sign == -1
        and value_route.support_period == 156
        and value_route.support_value_root_unique_fp_star
        and value_route.ambient_value_branch_count_fp_star == 11
        and generic_single_y_value_rejected
    )
    return KsyYSiegelFormulaProfile(
        raw_center=raw_center,
        raw_d_step=D_SHIFT,
        raw_k_step=KERNEL_SHIFT,
        source_atom_support=len(centers),
        formula_layers=layer_profiles(layers),
        layer_supports_disjoint=layer_disjoint,
        footprint_support=len(formula_footprint),
        footprint_coefficient_counts=coefficient_counts(formula_footprint),
        footprint_matches_anti_invariant_product=formula_matches,
        kl_exponent_screen_ok=kl.quadratic_relations_ok,
        raw_divisor_route_ok=route.certificate_path_ok,
        raw_divisor_emits=route.emitted_payload,
        raw_value_route_period=value_route.support_period,
        raw_value_route_unique_fp_root=value_route.support_value_root_unique_fp_star,
        raw_value_route_needs_period_context=True,
        generic_single_y_value_rejected=generic_single_y_value_rejected,
        exact_formula_contract=(
            "instantiate KSY y(Q)=-g(2Q)/g(Q)^4 on all 75 atoms "
            "A=C+jD+kK; divisor/additive output routes immediately, while "
            "value output must carry period-156 theta2 context"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y Siegel formula gate")
    profile = profile_ksy_y_siegel_formula()
    print(f"ksy_y_siegel_formula_profile={profile}")
    print("formula_layers")
    for layer in profile.formula_layers:
        print(
            "  "
            f"{layer.name}: coeff={layer.coefficient} "
            f"support={layer.support} sample={layer.sample}"
        )
    print("formula_checks")
    print(f"  source_atom_support={profile.source_atom_support}")
    print(f"  layer_supports_disjoint={int(profile.layer_supports_disjoint)}")
    print(f"  footprint_support={profile.footprint_support}")
    print(f"  coefficient_counts={profile.footprint_coefficient_counts}")
    print(f"  footprint_matches_anti_invariant_product={int(profile.footprint_matches_anti_invariant_product)}")
    print(f"  KL_exponent_screen_ok={int(profile.kl_exponent_screen_ok)}")
    print("router_checks")
    print(f"  raw_divisor_route_ok={int(profile.raw_divisor_route_ok)}")
    print(f"  raw_divisor_emits={profile.raw_divisor_emits}")
    print(f"  raw_value_route_period={profile.raw_value_route_period}")
    print(f"  raw_value_route_unique_Fp_root={int(profile.raw_value_route_unique_fp_root)}")
    print(f"  raw_value_route_needs_period_context={int(profile.raw_value_route_needs_period_context)}")
    print(f"  generic_single_y_value_rejected={int(profile.generic_single_y_value_rejected)}")
    print("interpretation")
    print("  KSY_normalized_y_formula_instantiates_exact_four_layer_Siegel_payload=1")
    print("  divisor_or_additive_formula_output_routes_to_theta2_inverse_certificate=1")
    print("  value_formula_output_needs_period_156_theta2_context=1")
    print("  generic_KSY_ray_class_generation_is_not_a_certificate_payload=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
