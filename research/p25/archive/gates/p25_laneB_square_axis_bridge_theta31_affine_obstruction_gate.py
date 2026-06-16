#!/usr/bin/env python3
"""Affine obstruction for theta_{3,1} bridge near-misses.

The theta_{3,1} D-edge has the right size and several harness-adjacent
invariants, but its support is disjoint from the primitive bridge.  The prior
gates rule out translations and sparse translated-edge sums.  This gate checks
the remaining cheap coordinate escape: could a diamond, Frobenius, or affine
reindexing of the canonical theta edges turn the near miss into the bridge?

No.  Scanning every affine endomorphism of C_507 gives no support match for
any support <= 12 theta edge, so signs and scalars never even get a chance.
For affine automorphisms the obstruction is visible in the difference profile:
the six-point theta D-edges contain six ordered differences with gcd 169, while
the primitive bridge contains none.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_theta31_edge_direction_scan_gate import (
    edge_coefficients,
    quotient_theta_packet,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class DifferenceProfile:
    name: str
    support_size: int
    gcd_difference_counts: tuple[tuple[int, int], ...]
    affine_unit_stabilizer_count: int


@dataclass(frozen=True)
class AffineEdgeProfile:
    direction: int
    support_size: int
    affine_endomorphism_support_matches: int
    affine_unit_support_matches: int
    affine_unit_coefficient_matches: int
    affine_unit_signed_layer_matches: int
    difference_profile: DifferenceProfile


@dataclass(frozen=True)
class AffineObstructionProfile:
    unit_count: int
    small_directions: tuple[int, ...]
    bridge_profile: DifferenceProfile
    edge_profiles: tuple[AffineEdgeProfile, ...]
    total_endomorphism_support_matches: int
    total_unit_support_matches: int
    total_unit_coefficient_matches: int
    theta_d_has_gcd169_differences: bool
    bridge_has_gcd169_differences: bool


def units() -> tuple[int, ...]:
    return tuple(value for value in range(QUOTIENT_ORDER) if gcd(value, QUOTIENT_ORDER) == 1)


def affine_support(support: set[int], multiplier: int, shift: int) -> set[int]:
    return {
        (multiplier * q_value + shift) % QUOTIENT_ORDER
        for q_value in support
    }


def affine_coefficients(coefficients: dict[int, int], multiplier: int, shift: int, sign: int) -> dict[int, int]:
    return {
        (multiplier * q_value + shift) % QUOTIENT_ORDER: sign * value
        for q_value, value in coefficients.items()
    }


def difference_profile(name: str, support: set[int]) -> DifferenceProfile:
    ordered_differences: Counter[int] = Counter()
    for left in support:
        for right in support:
            if left != right:
                ordered_differences[gcd((right - left) % QUOTIENT_ORDER, QUOTIENT_ORDER)] += 1
    unit_stabilizer_count = sum(
        1
        for multiplier in units()
        if {multiplier * q_value % QUOTIENT_ORDER for q_value in support} == support
    )
    return DifferenceProfile(
        name=name,
        support_size=len(support),
        gcd_difference_counts=tuple(sorted(ordered_differences.items())),
        affine_unit_stabilizer_count=unit_stabilizer_count,
    )


def signed_layer_match(coefficients: dict[int, int], target: dict[int, int], multiplier: int, shift: int) -> bool:
    positive = {q_value for q_value, value in coefficients.items() if value == 1}
    negative = {q_value for q_value, value in coefficients.items() if value == -1}
    target_positive = {q_value for q_value, value in target.items() if value == 1}
    target_negative = {q_value for q_value, value in target.items() if value == -1}
    positive_image = affine_support(positive, multiplier, shift)
    negative_image = affine_support(negative, multiplier, shift)
    return (
        (positive_image, negative_image) == (target_positive, target_negative)
        or (positive_image, negative_image) == (target_negative, target_positive)
    )


def edge_profile(direction: int, coefficients: dict[int, int], target: dict[int, int]) -> AffineEdgeProfile:
    support = set(coefficients)
    target_support = set(target)
    unit_values = units()
    endomorphism_support_matches = 0
    unit_support_matches = 0
    unit_coefficient_matches = 0
    unit_signed_layer_matches = 0

    for multiplier in range(QUOTIENT_ORDER):
        for shift in range(QUOTIENT_ORDER):
            if affine_support(support, multiplier, shift) == target_support:
                endomorphism_support_matches += 1

    for multiplier in unit_values:
        for shift in range(QUOTIENT_ORDER):
            if affine_support(support, multiplier, shift) != target_support:
                continue
            unit_support_matches += 1
            if signed_layer_match(coefficients, target, multiplier, shift):
                unit_signed_layer_matches += 1
            if any(
                affine_coefficients(coefficients, multiplier, shift, sign) == target
                for sign in (1, -1)
            ):
                unit_coefficient_matches += 1

    return AffineEdgeProfile(
        direction=direction,
        support_size=len(support),
        affine_endomorphism_support_matches=endomorphism_support_matches,
        affine_unit_support_matches=unit_support_matches,
        affine_unit_coefficient_matches=unit_coefficient_matches,
        affine_unit_signed_layer_matches=unit_signed_layer_matches,
        difference_profile=difference_profile(f"theta_dir_{direction}", support),
    )


def obstruction_profile() -> AffineObstructionProfile:
    packet = quotient_theta_packet()
    target = bridge_coefficients()
    small_directions = tuple(
        direction
        for direction in range(1, QUOTIENT_ORDER)
        if len(edge_coefficients(packet, direction)) <= 12
    )
    edge_profiles = tuple(
        edge_profile(direction, edge_coefficients(packet, direction), target)
        for direction in small_directions
    )
    bridge_profile = difference_profile("bridge", set(target))
    d_profile = next(profile for profile in edge_profiles if profile.direction == S_STEP)
    return AffineObstructionProfile(
        unit_count=len(units()),
        small_directions=small_directions,
        bridge_profile=bridge_profile,
        edge_profiles=edge_profiles,
        total_endomorphism_support_matches=sum(profile.affine_endomorphism_support_matches for profile in edge_profiles),
        total_unit_support_matches=sum(profile.affine_unit_support_matches for profile in edge_profiles),
        total_unit_coefficient_matches=sum(profile.affine_unit_coefficient_matches for profile in edge_profiles),
        theta_d_has_gcd169_differences=any(gcd_value == 169 for gcd_value, _ in d_profile.difference_profile.gcd_difference_counts),
        bridge_has_gcd169_differences=any(gcd_value == 169 for gcd_value, _ in bridge_profile.gcd_difference_counts),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge theta31 affine-obstruction gate")
    print(f"quotient_order={QUOTIENT_ORDER} D={S_STEP}")
    profile = obstruction_profile()
    expected = AffineObstructionProfile(
        unit_count=312,
        small_directions=(163, 172, 335, 344),
        bridge_profile=DifferenceProfile("bridge", 6, ((1, 24), (3, 6)), 2),
        edge_profiles=(
            AffineEdgeProfile(163, 12, 0, 0, 0, 0, DifferenceProfile("theta_dir_163", 12, ((1, 84), (3, 36), (169, 12)), 1)),
            AffineEdgeProfile(172, 6, 0, 0, 0, 0, DifferenceProfile("theta_dir_172", 6, ((1, 18), (3, 6), (169, 6)), 1)),
            AffineEdgeProfile(335, 6, 0, 0, 0, 0, DifferenceProfile("theta_dir_335", 6, ((1, 18), (3, 6), (169, 6)), 1)),
            AffineEdgeProfile(344, 12, 0, 0, 0, 0, DifferenceProfile("theta_dir_344", 12, ((1, 84), (3, 36), (169, 12)), 1)),
        ),
        total_endomorphism_support_matches=0,
        total_unit_support_matches=0,
        total_unit_coefficient_matches=0,
        theta_d_has_gcd169_differences=True,
        bridge_has_gcd169_differences=False,
    )
    row_ok = profile == expected

    print(f"bridge_coefficients={sorted(bridge_coefficients().items())}")
    print(f"affine_obstruction_profile={profile}")
    print("affine_laws")
    print("  every affine endomorphism of C507 was checked for support matches")
    print("  no support <= 12 theta edge has an affine image equal to the bridge support")
    print("  hence no diamond/Frobenius/affine unit can repair signs or coefficients")
    print("  theta D edges have gcd-169 internal differences; the bridge has none")
    print("interpretation")
    print("  theta31_near_miss_is_not_an_affine_or_diamond_reindexing_of_the_bridge=1")
    print("  quotient_coordinate_change_cannot_turn_the_canonical_theta_edge_into_the_bridge=1")
    print("  affine_support_invariants_strengthen_the_sparse_combination_obstruction=1")
    print("  next_theta_route_must_change_the_packet_not_only_relabel_C507=1")
    print(f"square_axis_bridge_theta31_affine_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_theta31_affine_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
