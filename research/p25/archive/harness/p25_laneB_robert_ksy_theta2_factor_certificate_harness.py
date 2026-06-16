#!/usr/bin/env python3
"""Tiny factor-certificate intake for the p25 KSY theta2 route.

The sparse harness accepts 300 theta2 terms, and the compact KSY harness
accepts center/half-edge parameters.  A theorem-side producer may instead
identify the p24-derived bridge factors directly:

    base * K_trace * D_segment * (1 - T).

This harness accepts that tiny factor tuple, derives the KSY half-edge recipe
from `T`, and then reuses the existing bridge, compact theta2, and period
absorption checks.  It is an intake/verifier contract, not the missing
arithmetic theta2 producer.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_compact_harness import (
    KsyTheta2CompactProfile,
    profile_compact_theta2,
)
from p25_laneB_robert_ksy_theta2_factor_period_certificate_gate import (
    coord_delta,
    period_scale,
    proper_divisor_row,
    push_coord,
    push_factor,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import SUPPORT_PERIOD
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    proper_divisors,
    pushforward_power,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    half_step,
    inverse_step,
    normalized_y_exponent_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import scale_ring
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    edge_factor,
    geometric_factor,
    monomial,
    multiply_factors,
    scale_coord,
    source_mask_to_raw,
    translate_ring,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class FactorPeriodAbsorptionProfile:
    period: int
    period_scale: Coord
    k_generator_multiplier: int
    k_generator_multiplier_coprime_to_25: bool
    k_trace_fixed: bool
    base_drift: Coord
    base_drift_k_index: int
    d_drift: Coord
    d_drift_k_index: int
    t_drift: Coord
    t_drift_k_index: int
    base_drift_absorbed: bool
    d_drift_absorbed: bool
    t_drift_absorbed: bool
    product_fixed: bool
    theta2_fixed: bool
    proper_divisors_all_fail_theta2_fixedness: bool
    ok: bool


@dataclass(frozen=True)
class KsyTheta2FactorCertificateProfile:
    name: str
    base: Coord
    k_step: Coord
    d_step: Coord
    t_step: Coord
    derived_half_edge: Coord
    derived_center_base: Coord
    derived_half_shift: Coord
    factor_support_budget: int
    product_support: int
    product_equals_derived_bridge: bool
    bridge_profile: CandidateProfile
    compact_inverse_profile: KsyTheta2CompactProfile
    compact_theta2_profile: KsyTheta2CompactProfile
    period_absorption_profile: FactorPeriodAbsorptionProfile
    ok: bool


def subgroup_index(generator: Coord, length: int, coord: Coord) -> int | None:
    for index in range(length):
        if scale_coord(generator, index) == coord:
            return index
    return None


def coprime(left: int, right: int) -> bool:
    while right:
        left, right = right, left % right
    return abs(left) == 1


def factor_rings(
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
) -> tuple[tuple[str, Ring], ...]:
    return (
        ("base", monomial(base)),
        ("K_trace", geometric_factor(k_step, 25)),
        ("D_segment", geometric_factor(d_step, 3)),
        ("bridge_edge", edge_factor(t_step)),
    )


def factor_product(
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
) -> Ring:
    return multiply_factors(factor_rings(base, k_step, d_step, t_step))


def period_absorption_profile(
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
    product: Ring,
    theta2: Ring,
) -> FactorPeriodAbsorptionProfile:
    k_trace = geometric_factor(k_step, 25)
    pushed_k = push_coord(k_step, SUPPORT_PERIOD)
    k_multiplier = subgroup_index(k_step, 25, pushed_k)
    base_drift = coord_delta(push_coord(base, SUPPORT_PERIOD), base)
    d_drift = coord_delta(push_coord(d_step, SUPPORT_PERIOD), d_step)
    t_drift = coord_delta(push_coord(t_step, SUPPORT_PERIOD), t_step)
    base_drift_index = subgroup_index(k_step, 25, base_drift)
    d_drift_index = subgroup_index(k_step, 25, d_drift)
    t_drift_index = subgroup_index(k_step, 25, t_drift)
    proper_rows = tuple(
        proper_divisor_row(period, product, theta2)
        for period in proper_divisors(SUPPORT_PERIOD)
    )
    k_trace_fixed = push_factor(k_trace, SUPPORT_PERIOD) == k_trace
    base_absorbed = translate_ring(k_trace, base_drift) == k_trace
    d_absorbed = translate_ring(k_trace, d_drift) == k_trace
    t_absorbed = translate_ring(k_trace, t_drift) == k_trace
    product_fixed = pushforward_power(product, SUPPORT_PERIOD) == product
    theta2_fixed = pushforward_power(theta2, SUPPORT_PERIOD) == theta2
    proper_fail = all(not row.theta2_fixed for row in proper_rows)
    row_ok = (
        period_scale(SUPPORT_PERIOD) == (61, 1)
        and k_trace_fixed
        and k_multiplier is not None
        and coprime(k_multiplier, 25)
        and base_drift_index is not None
        and d_drift_index is not None
        and t_drift_index is not None
        and base_absorbed
        and d_absorbed
        and t_absorbed
        and product_fixed
        and theta2_fixed
        and proper_fail
    )
    return FactorPeriodAbsorptionProfile(
        period=SUPPORT_PERIOD,
        period_scale=period_scale(SUPPORT_PERIOD),
        k_generator_multiplier=-1 if k_multiplier is None else k_multiplier,
        k_generator_multiplier_coprime_to_25=(
            False if k_multiplier is None else coprime(k_multiplier, 25)
        ),
        k_trace_fixed=k_trace_fixed,
        base_drift=base_drift,
        base_drift_k_index=-1 if base_drift_index is None else base_drift_index,
        d_drift=d_drift,
        d_drift_k_index=-1 if d_drift_index is None else d_drift_index,
        t_drift=t_drift,
        t_drift_k_index=-1 if t_drift_index is None else t_drift_index,
        base_drift_absorbed=base_absorbed,
        d_drift_absorbed=d_absorbed,
        t_drift_absorbed=t_absorbed,
        product_fixed=product_fixed,
        theta2_fixed=theta2_fixed,
        proper_divisors_all_fail_theta2_fixedness=proper_fail,
        ok=row_ok,
    )


def profile_factor_certificate(
    name: str,
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
) -> KsyTheta2FactorCertificateProfile:
    product = factor_product(base, k_step, d_step, t_step)
    bridge_profile = profile_candidate(name, source_mask_to_raw(product), target_raw_bridge())
    half_edge = half_step(t_step)
    half_shift = inverse_step(half_edge)
    center_base = add_coord(base, half_edge)
    compact_inverse = profile_compact_theta2(
        f"{name}_compact_theta2_inverse",
        center_base,
        half_shift,
        False,
    )
    compact_theta2 = profile_compact_theta2(
        f"{name}_compact_theta2",
        center_base,
        half_shift,
        True,
    )
    derived_bridge = symmetric_edge_ring(center_base, half_shift)
    theta2_inverse = normalized_y_exponent_footprint(center_base, half_shift)
    theta2 = scale_ring(theta2_inverse, -1)
    period_profile = period_absorption_profile(
        base,
        k_step,
        d_step,
        t_step,
        product,
        theta2,
    )
    factor_budget = sum(len(factor) for _name, factor in factor_rings(base, k_step, d_step, t_step))
    row_ok = (
        factor_budget == 31
        and len(product) == 150
        and product == derived_bridge
        and bridge_profile.ok
        and compact_inverse.ok
        and compact_theta2.ok
        and compact_inverse.candidate_profile.exact_theta2_inverse
        and compact_theta2.candidate_profile.exact_theta2
        and period_profile.ok
    )
    return KsyTheta2FactorCertificateProfile(
        name=name,
        base=base,
        k_step=k_step,
        d_step=d_step,
        t_step=t_step,
        derived_half_edge=half_edge,
        derived_center_base=center_base,
        derived_half_shift=half_shift,
        factor_support_budget=factor_budget,
        product_support=len(product),
        product_equals_derived_bridge=product == derived_bridge,
        bridge_profile=bridge_profile,
        compact_inverse_profile=compact_inverse,
        compact_theta2_profile=compact_theta2,
        period_absorption_profile=period_profile,
        ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a tiny p25 KSY factor certificate: base, K, D, and T "
            "coordinates in C_75 x C_169."
        )
    )
    parser.add_argument("--base-right", type=int)
    parser.add_argument("--base-c", type=int)
    parser.add_argument("--k-right", type=int)
    parser.add_argument("--k-c", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--t-right", type=int)
    parser.add_argument("--t-c", type=int)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/theta2 factor-certificate intake harness")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")

    supplied = (
        args.base_right is not None,
        args.base_c is not None,
        args.k_right is not None,
        args.k_c is not None,
        args.d_right is not None,
        args.d_c is not None,
        args.t_right is not None,
        args.t_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all eight factor coordinates must be supplied together")
        profile = profile_factor_certificate(
            "factor_certificate_candidate",
            (args.base_right % RIGHT_ORDER, args.base_c % C_ORDER),
            (args.k_right % RIGHT_ORDER, args.k_c % C_ORDER),
            (args.d_right % RIGHT_ORDER, args.d_c % C_ORDER),
            (args.t_right % RIGHT_ORDER, args.t_c % C_ORDER),
        )
        print("mode=factor_certificate_candidate")
        print(f"factor_certificate_profile={profile}")
        print("candidate_contract")
        print("  pass requires factor product to equal the target bridge")
        print("  pass derives the KSY center/half-edge theta2 recipe from T")
        print("  pass requires period-156 absorption by K_trace")
        print(f"robert_ksy_theta2_factor_certificate_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_factor_certificate_candidate")
        return 0 if profile.ok else 1

    target = profile_factor_certificate(
        "target_factor_certificate",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    base_k_gauge = profile_factor_certificate(
        "base_k_gauge_control",
        add_coord(BASE_POINT, KERNEL_SHIFT),
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    wrong_d = profile_factor_certificate(
        "wrong_d_control",
        BASE_POINT,
        KERNEL_SHIFT,
        add_coord(D_SHIFT, (0, 1)),
        BRIDGE_SHIFT,
    )
    wrong_t = profile_factor_certificate(
        "wrong_t_control",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        scale_coord(BRIDGE_SHIFT, 2),
    )
    collapsed_k = profile_factor_certificate(
        "collapsed_k_control",
        BASE_POINT,
        (0, 0),
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    row_ok = (
        target.ok
        and base_k_gauge.ok
        and not wrong_d.ok
        and not wrong_t.ok
        and not collapsed_k.ok
        and target.derived_center_base == (44, 166)
        and target.derived_half_shift == (56, 28)
        and target.factor_support_budget == 31
        and base_k_gauge.product_equals_derived_bridge
        and base_k_gauge.bridge_profile.ok
    )
    print(f"target_factor_certificate_profile={target}")
    print(f"base_k_gauge_control_profile={base_k_gauge}")
    print(f"wrong_d_control_profile={wrong_d}")
    print(f"wrong_t_control_profile={wrong_t}")
    print(f"collapsed_k_control_profile={collapsed_k}")
    print("factor_certificate_laws")
    print("  theorem_hit_may_emit_only_base_K_D_T_factor_coordinates=1")
    print("  factor_product_must_equal_the_exact_bridge_contract=1")
    print("  KSY_center_and_half_shift_are_derived_from_base_and_T=1")
    print("  compact_theta2_and_theta2_inverse_harnesses_are_reused=1")
    print("  period_156_absorption_must_hold_at_factor_level=1")
    print("  base_K_gauge_is_accepted_but_wrong_D_wrong_T_and_collapsed_K_fail=1")
    print(f"robert_ksy_theta2_factor_certificate_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_factor_certificate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
