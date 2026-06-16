#!/usr/bin/env python3
"""K-gauge normal form for the p25 KSY theta2 factor certificate.

The factor-certificate harness accepts the literal tuple

    base=(25,25), K=(57,0), D=(22,3), T=(38,113).

This gate records the full K-trace gauge freedom behind that tuple.  Any
primitive generator of the same 25-point right subgroup may be used for `K`,
and `base`, `D`, and `T` may be shifted independently by that subgroup.  The
factor product, the derived symmetric bridge, and the normalized-y/theta2
footprint are unchanged.

Thus the real finite theorem-output contract is a quotient normal form plus a
primitive K-subgroup generator, not one rigid eight-coordinate tuple.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_factor_certificate_harness import (
    factor_product,
    profile_factor_certificate,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    half_step,
    inverse_step,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    add_coord,
    geometric_factor,
    scale_coord,
    translate_ring,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class FactorGaugeNormalFormProfile:
    k_subgroup_size: int
    k_subgroup_is_right_mod_3_kernel: bool
    primitive_k_generator_count: int
    quotient_base_class: Coord
    quotient_d_class: Coord
    quotient_t_class: Coord
    inferred_accepted_factor_gauge_count: int
    all_primitive_generators_give_same_k_trace: bool
    all_k_trace_shifts_absorb: bool
    representative_factor_gauges_preserve_bridge: bool
    theta2_base_t_gauge_pairs_checked: int
    all_base_t_gauges_preserve_derived_bridge: bool
    all_base_t_gauges_preserve_theta2_inverse: bool
    target_profile_ok: bool
    primitive_generator_profile_ok: bool
    base_d_t_gauge_profile_ok: bool
    nonprimitive_k_profile_ok: bool
    wrong_quotient_d_profile_ok: bool
    wrong_quotient_t_profile_ok: bool
    row_ok: bool


def quotient_class(coord: Coord) -> Coord:
    return (coord[0] % 3, coord[1] % C_ORDER)


def k_subgroup(generator: Coord = KERNEL_SHIFT) -> set[Coord]:
    return {scale_coord(generator, index) for index in range(25)}


def primitive_k_generators() -> tuple[Coord, ...]:
    return tuple(
        scale_coord(KERNEL_SHIFT, multiplier)
        for multiplier in range(25)
        if gcd(multiplier, 25) == 1
    )


def same_k_trace(generator: Coord) -> bool:
    return geometric_factor(generator, 25) == geometric_factor(KERNEL_SHIFT, 25)


def all_shifts_absorbed(generator: Coord) -> bool:
    trace = geometric_factor(generator, 25)
    return all(translate_ring(trace, shift) == trace for shift in k_subgroup(generator))


def add_k(coord: Coord, generator: Coord, index: int) -> Coord:
    return add_coord(coord, scale_coord(generator, index))


def representative_factor_gauges_preserve_bridge(generator: Coord) -> bool:
    target = raw_source_mask()
    reps = []
    for index in range(25):
        reps.append((add_k(BASE_POINT, generator, index), generator, D_SHIFT, BRIDGE_SHIFT))
        reps.append((BASE_POINT, generator, add_k(D_SHIFT, generator, index), BRIDGE_SHIFT))
        reps.append((BASE_POINT, generator, D_SHIFT, add_k(BRIDGE_SHIFT, generator, index)))
    reps.append(
        (
            add_k(BASE_POINT, generator, 7),
            generator,
            add_k(D_SHIFT, generator, 11),
            add_k(BRIDGE_SHIFT, generator, 19),
        )
    )
    return all(factor_product(base, k_step, d_step, t_step) == target for base, k_step, d_step, t_step in reps)


def base_t_gauge_preserves_theta2() -> tuple[int, bool, bool]:
    half_profile = profile_half_edge_footprint()
    target_inverse = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    target_bridge = raw_source_mask()
    checked = 0
    bridge_ok = True
    theta2_ok = True
    for base_index in range(25):
        for t_index in range(25):
            checked += 1
            base = add_k(BASE_POINT, KERNEL_SHIFT, base_index)
            t_step = add_k(BRIDGE_SHIFT, KERNEL_SHIFT, t_index)
            half_edge = half_step(t_step)
            half_shift = inverse_step(half_edge)
            center_base = add_coord(base, half_edge)
            derived_bridge = symmetric_edge_ring(center_base, half_shift)
            footprint = normalized_y_exponent_footprint(center_base, half_shift)
            bridge_ok = bridge_ok and derived_bridge == target_bridge
            theta2_ok = theta2_ok and footprint == target_inverse
    return checked, bridge_ok, theta2_ok


def profile_gauge_normal_form() -> FactorGaugeNormalFormProfile:
    subgroup = k_subgroup()
    primitive_generators = primitive_k_generators()
    trace_laws_ok = all(same_k_trace(generator) for generator in primitive_generators)
    absorption_ok = all(all_shifts_absorbed(generator) for generator in primitive_generators)
    representative_ok = all(
        representative_factor_gauges_preserve_bridge(generator)
        for generator in primitive_generators
    )
    checked_pairs, derived_bridge_ok, theta2_inverse_ok = base_t_gauge_preserves_theta2()

    target_profile = profile_factor_certificate(
        "target_factor_gauge_normal_form",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    primitive_profile = profile_factor_certificate(
        "primitive_K_generator_control",
        BASE_POINT,
        scale_coord(KERNEL_SHIFT, 2),
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    base_d_t_gauge_profile = profile_factor_certificate(
        "base_D_T_K_gauge_control",
        add_k(BASE_POINT, KERNEL_SHIFT, 7),
        KERNEL_SHIFT,
        add_k(D_SHIFT, KERNEL_SHIFT, 11),
        add_k(BRIDGE_SHIFT, KERNEL_SHIFT, 19),
    )
    nonprimitive_profile = profile_factor_certificate(
        "nonprimitive_K_generator_control",
        BASE_POINT,
        scale_coord(KERNEL_SHIFT, 5),
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    wrong_d_profile = profile_factor_certificate(
        "wrong_D_quotient_class_control",
        BASE_POINT,
        KERNEL_SHIFT,
        add_coord(D_SHIFT, (0, 1)),
        BRIDGE_SHIFT,
    )
    wrong_t_profile = profile_factor_certificate(
        "wrong_T_quotient_class_control",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        add_coord(BRIDGE_SHIFT, (0, 1)),
    )

    right_mod_3_kernel = {(3 * index) % RIGHT_ORDER for index in range(25)}
    subgroup_ok = (
        len(subgroup) == 25
        and all(coord[1] == 0 for coord in subgroup)
        and {coord[0] for coord in subgroup} == right_mod_3_kernel
    )
    inferred_count = len(primitive_generators) * 25 * 25 * 25
    row_ok = (
        subgroup_ok
        and len(primitive_generators) == 20
        and quotient_class(BASE_POINT) == (1, 25)
        and quotient_class(D_SHIFT) == (1, 3)
        and quotient_class(BRIDGE_SHIFT) == (2, 113)
        and inferred_count == 312_500
        and trace_laws_ok
        and absorption_ok
        and representative_ok
        and checked_pairs == 625
        and derived_bridge_ok
        and theta2_inverse_ok
        and target_profile.ok
        and primitive_profile.ok
        and base_d_t_gauge_profile.ok
        and not nonprimitive_profile.ok
        and not wrong_d_profile.ok
        and not wrong_t_profile.ok
    )
    return FactorGaugeNormalFormProfile(
        k_subgroup_size=len(subgroup),
        k_subgroup_is_right_mod_3_kernel=subgroup_ok,
        primitive_k_generator_count=len(primitive_generators),
        quotient_base_class=quotient_class(BASE_POINT),
        quotient_d_class=quotient_class(D_SHIFT),
        quotient_t_class=quotient_class(BRIDGE_SHIFT),
        inferred_accepted_factor_gauge_count=inferred_count,
        all_primitive_generators_give_same_k_trace=trace_laws_ok,
        all_k_trace_shifts_absorb=absorption_ok,
        representative_factor_gauges_preserve_bridge=representative_ok,
        theta2_base_t_gauge_pairs_checked=checked_pairs,
        all_base_t_gauges_preserve_derived_bridge=derived_bridge_ok,
        all_base_t_gauges_preserve_theta2_inverse=theta2_inverse_ok,
        target_profile_ok=target_profile.ok,
        primitive_generator_profile_ok=primitive_profile.ok,
        base_d_t_gauge_profile_ok=base_d_t_gauge_profile.ok,
        nonprimitive_k_profile_ok=nonprimitive_profile.ok,
        wrong_quotient_d_profile_ok=wrong_d_profile.ok,
        wrong_quotient_t_profile_ok=wrong_t_profile.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/theta2 factor-gauge normal-form gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"K_subgroup_generator={KERNEL_SHIFT}"
    )
    profile = profile_gauge_normal_form()
    print(f"ksy_theta2_factor_gauge_normal_form_profile={profile}")
    print("factor_gauge_laws")
    print("  K_trace_subgroup_is_right_mod_3_kernel_of_size_25=1")
    print("  K_may_be_any_of_20_primitive_generators_of_that_subgroup=1")
    print("  base_D_and_T_may_be_shifted_independently_by_K_trace=1")
    print("  inferred_accepted_factor_gauge_count_312500=1")
    print("  quotient_classes_are_base_1_25_D_1_3_T_2_113=1")
    print("  all_625_base_T_gauges_preserve_symmetric_bridge_and_theta2_inverse=1")
    print("  nonprimitive_K_and_wrong_D_or_T_quotient_classes_fail=1")
    print("interpretation")
    print("  theorem_output_can_be_quotient_factor_data_plus_primitive_K_subgroup_generator=1")
    print("  this_is_a_normal_form_for_the_factor_certificate_not_an_arithmetic_producer=1")
    print(f"robert_ksy_theta2_factor_gauge_normal_form_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_factor_gauge_normal_form_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
