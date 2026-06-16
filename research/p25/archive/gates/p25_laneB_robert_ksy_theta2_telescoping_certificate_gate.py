#!/usr/bin/env python3
"""Compact telescoping certificate for the p25 KSY theta2 route.

The support-period resolvent expands

    sum_{i=0}^{155} 4^(155-i) [2]^i theta2 / (4^156 - 1).

For a compact KSY hit this expansion is unnecessary.  If

    theta2 = (4 - [2]) * B
    [2]^156 B = B,

then the numerator telescopes to `(4^156 - 1) * B`.  This gate records the
small certificate skeleton: compact bridge/theta2 parameters, period-fixing
checks, the orbit decomposition explaining why period 156 is support-specific,
and one expanded-resolvent cross-check against the previous gate.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_resolvent_gate import (
    P25,
    SQRT_FLOOR,
    weighted_resolvent_numerator,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import SUPPORT_PERIOD
from p25_laneB_robert_ksy_y_doubling_distribution_gate import divide_ring_exact
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    route_centers,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import add_rings, scale_ring
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring, scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class OrbitSkeletonProfile:
    touched_doubling_orbits: int
    ambient_orbit_length_counts: tuple[tuple[int, int], ...]
    bridge_points_per_orbit_counts: tuple[tuple[int, int], ...]
    theta2_points_per_orbit_counts: tuple[tuple[int, int], ...]
    ambient_780_orbits_touched: int
    support_156_orbits_touched: int
    global_power_156_is_identity: bool
    support_power_156_is_identity: bool
    row_ok: bool


@dataclass(frozen=True)
class KsyTheta2TelescopingCertificateProfile:
    center_base: Coord
    half_shift: Coord
    support_period: int
    route_center_support: int
    bridge_support: int
    theta2_support: int
    theta2_equals_four_minus_double_bridge: bool
    bridge_fixed_by_support_period: bool
    theta2_fixed_by_support_period: bool
    all_proper_period_divisors_fail_to_fix_theta2: bool
    denominator_bit_length: int
    denominator_nonzero_mod_p25: bool
    denominator_gcd_p25_minus_1: int
    compact_linear_cell_check_budget: int
    expanded_resolvent_term_budget: int
    compact_budget_improvement_factor: int
    expanded_resolvent_crosscheck_recovers_bridge: bool
    compact_telescoping_identity_recovers_bridge: bool
    compact_budget_below_sqrt: bool
    expanded_budget_below_sqrt: bool
    orbit_skeleton: OrbitSkeletonProfile
    row_ok: bool


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def pushforward_power(ring: Ring, exponent: int) -> Ring:
    right_scale = pow(2, exponent, RIGHT_ORDER)
    c_scale = pow(2, exponent, C_ORDER)
    out: Ring = {}
    for coord, coefficient in ring.items():
        pushed = ((right_scale * coord[0]) % RIGHT_ORDER, (c_scale * coord[1]) % C_ORDER)
        add_ring_entry(out, pushed, coefficient)
    return dict(sorted(out.items()))


def double_pushforward_local(ring: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in ring.items():
        add_ring_entry(out, scale_coord(coord, 2), coefficient)
    return dict(sorted(out.items()))


def coord_orbit(coord: Coord) -> tuple[Coord, ...]:
    orbit: list[Coord] = []
    current = coord
    while current not in orbit:
        orbit.append(current)
        current = scale_coord(current, 2)
    return tuple(orbit)


def canonical_orbit_rep(orbit: tuple[Coord, ...]) -> Coord:
    return min(orbit)


def support_orbit_rows(ring: Ring) -> tuple[tuple[Coord, int, int], ...]:
    seen: set[Coord] = set()
    rows: list[tuple[Coord, int, int]] = []
    for coord in sorted(ring):
        if coord in seen:
            continue
        orbit = coord_orbit(coord)
        support_hits = sum(1 for item in orbit if item in ring)
        rows.append((canonical_orbit_rep(orbit), len(orbit), support_hits))
        seen.update(orbit)
    return tuple(sorted(rows, key=lambda row: (row[1], row[0])))


def orbit_skeleton_profile(bridge: Ring, theta2: Ring) -> OrbitSkeletonProfile:
    bridge_rows = support_orbit_rows(bridge)
    theta2_rows = support_orbit_rows(theta2)
    bridge_orbits = tuple((rep, length) for rep, length, _hits in bridge_rows)
    theta2_orbits = tuple((rep, length) for rep, length, _hits in theta2_rows)
    ambient_counts = Counter(row[1] for row in theta2_rows)
    bridge_point_counts = Counter(row[2] for row in bridge_rows)
    theta2_point_counts = Counter(row[2] for row in theta2_rows)
    global_fixed = pushforward_power({(1, 1): 1}, SUPPORT_PERIOD) == {(1, 1): 1}
    support_fixed = pushforward_power(bridge, SUPPORT_PERIOD) == bridge and pushforward_power(
        theta2,
        SUPPORT_PERIOD,
    ) == theta2
    row_ok = (
        len(bridge_rows) == 27
        and bridge_orbits == theta2_orbits
        and tuple(sorted(ambient_counts.items())) == ((156, 15), (780, 12))
        and tuple(sorted(bridge_point_counts.items())) == ((2, 15), (10, 12))
        and tuple(sorted(theta2_point_counts.items())) == ((4, 15), (20, 12))
        and not global_fixed
        and support_fixed
    )
    return OrbitSkeletonProfile(
        touched_doubling_orbits=len(theta2_rows),
        ambient_orbit_length_counts=tuple(sorted(ambient_counts.items())),
        bridge_points_per_orbit_counts=tuple(sorted(bridge_point_counts.items())),
        theta2_points_per_orbit_counts=tuple(sorted(theta2_point_counts.items())),
        ambient_780_orbits_touched=ambient_counts[780],
        support_156_orbits_touched=ambient_counts[156],
        global_power_156_is_identity=global_fixed,
        support_power_156_is_identity=support_fixed,
        row_ok=row_ok,
    )


def proper_divisors(value: int) -> tuple[int, ...]:
    return tuple(candidate for candidate in range(1, value) if value % candidate == 0)


def profile_telescoping_certificate() -> KsyTheta2TelescopingCertificateProfile:
    half_profile = profile_half_edge_footprint()
    centers = route_centers(half_profile.accepted_center_base)
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2_inverse = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2 = scale_ring(theta2_inverse, -1)
    four_minus_double_bridge = add_rings(
        scale_ring(bridge, 4),
        scale_ring(double_pushforward_local(bridge), -1),
    )

    bridge_fixed = pushforward_power(bridge, SUPPORT_PERIOD) == bridge
    theta2_fixed = pushforward_power(theta2, SUPPORT_PERIOD) == theta2
    proper_fail = all(
        pushforward_power(theta2, period) != theta2
        for period in proper_divisors(SUPPORT_PERIOD)
    )

    denominator = 4 ** SUPPORT_PERIOD - 1
    numerator, _union_support, _returns_to_theta2, expanded_term_budget = weighted_resolvent_numerator(
        theta2,
        SUPPORT_PERIOD,
    )
    expanded_recovered = divide_ring_exact(numerator, denominator)
    compact_identity_ok = (
        theta2 == four_minus_double_bridge
        and bridge_fixed
        and divide_ring_exact(
            add_rings(
                scale_ring(bridge, 4 ** SUPPORT_PERIOD),
                scale_ring(pushforward_power(bridge, SUPPORT_PERIOD), -1),
            ),
            denominator,
        )
        == bridge
    )
    orbit_skeleton = orbit_skeleton_profile(bridge, theta2)
    compact_budget = (
        len(centers)
        + len(bridge)
        + len(theta2)
        + len(pushforward_power(bridge, SUPPORT_PERIOD))
        + len(pushforward_power(theta2, SUPPORT_PERIOD))
    )

    row_ok = (
        half_profile.accepted_center_base == (44, 166)
        and half_profile.negative_half_edge == (56, 28)
        and SUPPORT_PERIOD == 156
        and len(centers) == 75
        and len(bridge) == 150
        and len(theta2) == 300
        and theta2 == four_minus_double_bridge
        and bridge_fixed
        and theta2_fixed
        and proper_fail
        and denominator.bit_length() == 312
        and denominator % P25 != 0
        and gcd(denominator, P25 - 1) == 1
        and compact_budget == 975
        and expanded_term_budget == 46800
        and expanded_term_budget // compact_budget == 48
        and expanded_recovered == bridge
        and compact_identity_ok
        and compact_budget < SQRT_FLOOR
        and expanded_term_budget < SQRT_FLOOR
        and orbit_skeleton.row_ok
    )
    return KsyTheta2TelescopingCertificateProfile(
        center_base=half_profile.accepted_center_base,
        half_shift=half_profile.negative_half_edge,
        support_period=SUPPORT_PERIOD,
        route_center_support=len(centers),
        bridge_support=len(bridge),
        theta2_support=len(theta2),
        theta2_equals_four_minus_double_bridge=theta2 == four_minus_double_bridge,
        bridge_fixed_by_support_period=bridge_fixed,
        theta2_fixed_by_support_period=theta2_fixed,
        all_proper_period_divisors_fail_to_fix_theta2=proper_fail,
        denominator_bit_length=denominator.bit_length(),
        denominator_nonzero_mod_p25=denominator % P25 != 0,
        denominator_gcd_p25_minus_1=gcd(denominator, P25 - 1),
        compact_linear_cell_check_budget=compact_budget,
        expanded_resolvent_term_budget=expanded_term_budget,
        compact_budget_improvement_factor=expanded_term_budget // compact_budget,
        expanded_resolvent_crosscheck_recovers_bridge=expanded_recovered == bridge,
        compact_telescoping_identity_recovers_bridge=compact_identity_ok,
        compact_budget_below_sqrt=compact_budget < SQRT_FLOOR,
        expanded_budget_below_sqrt=expanded_term_budget < SQRT_FLOOR,
        orbit_skeleton=orbit_skeleton,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/theta2 telescoping certificate gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_telescoping_certificate()
    print(f"ksy_theta2_telescoping_certificate_profile={profile}")
    print("telescoping_certificate_laws")
    print("  compact_recipe_center_base_44_166_and_half_shift_56_28=1")
    print("  theta2_equals_4_minus_doubling_operator_applied_to_bridge=1")
    print("  bridge_and_theta2_are_fixed_by_doubling_power_156=1")
    print("  all_proper_divisors_of_156_fail_to_fix_theta2=1")
    print("  compact_telescoping_identity_recovers_bridge_without_expanded_resolvent=1")
    print("  expanded_46800_term_resolvent_crosscheck_still_recovers_bridge=1")
    print("orbit_skeleton_laws")
    print("  theta2_support_touches_27_doubling_orbits=1")
    print("  orbit_lengths_are_15_of_156_and_12_of_780=1")
    print("  global_doubling_power_156_is_not_identity_on_C75xC169=1")
    print("  period_156_is_support_specific_not_ambient=1")
    print("interpretation")
    print("  compact_KSY_hit_can_be_checked_by_telescoping_certificate_before_full_resolvent=1")
    print("  this_is_a_certificate_skeleton_not_an_arithmetic_theta2_producer=1")
    print(f"robert_ksy_theta2_telescoping_certificate_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_telescoping_certificate_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
