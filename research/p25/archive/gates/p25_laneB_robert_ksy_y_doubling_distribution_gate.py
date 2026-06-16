#!/usr/bin/env python3
"""Doubling-distribution obstruction for the p25 KSY-y route.

The projection gate shows that the normalized-y footprint is

    double_pushforward(bridge) - 4*bridge.

This gate checks whether the doubled layer can disappear by an ordinary
doubling distribution or orbit average.  It cannot: multiplication by 2 is an
automorphism on C_75 x C_169, with source order 780 and trivial kernel.  The
doubled bridge is another 150-cell bridge-shaped object with wrong trace; the
full doubling orbit expands massively, and exact subtraction of the doubled
layer is the only tested low-complexity way back to the bridge.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd, lcm

from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import (
    add_rings,
    double_pushforward,
    scale_ring,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
)


@dataclass(frozen=True)
class LambdaScanRow:
    lambda_value: int
    support: int
    quotient_support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    trace_correct: bool
    ok: bool


@dataclass(frozen=True)
class KsyYDoublingDistributionProfile:
    right_order_of_2: int
    c_order_of_2: int
    source_order_of_2: int
    doubling_kernel_size: int
    bridge_support: int
    doubled_support: int
    doubled_profile: CandidateProfile
    orbit_unique_support: int
    orbit_sum_support: int
    orbit_sum_coefficient_counts: tuple[tuple[int, int], ...]
    orbit_sum_profile: CandidateProfile
    alternating_orbit_support: int
    lambda_scan: tuple[LambdaScanRow, ...]
    lambda_minus_one_scaled_bridge_ok: bool
    row_ok: bool


def multiplicative_order(value: int, modulus: int) -> int:
    current = value % modulus
    order = 1
    while current != 1:
        current = (current * value) % modulus
        order += 1
    return order


def add_ring_entry(ring: Ring, coord: tuple[int, int], coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def divide_ring_exact(ring: Ring, divisor: int) -> Ring:
    out: Ring = {}
    for coord, coefficient in ring.items():
        if coefficient % divisor:
            raise AssertionError("ring coefficient is not exactly divisible")
        out[coord] = coefficient // divisor
    return dict(sorted(out.items()))


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def orbit_sum(rings: tuple[Ring, ...], alternating: bool = False) -> Ring:
    out: Ring = {}
    for index, ring in enumerate(rings):
        sign = -1 if alternating and index % 2 else 1
        for coord, coefficient in ring.items():
            add_ring_entry(out, coord, sign * coefficient)
    return dict(sorted(out.items()))


def lambda_scan_rows(footprint: Ring, doubled: Ring) -> tuple[LambdaScanRow, ...]:
    rows: list[LambdaScanRow] = []
    for lambda_value in range(-5, 6):
        combo = add_rings(footprint, scale_ring(doubled, lambda_value))
        profile = bridge_profile(f"ksy_y_lambda_{lambda_value}_doubled_combo", combo)
        rows.append(
            LambdaScanRow(
                lambda_value=lambda_value,
                support=len(combo),
                quotient_support=profile.quotient_support,
                coefficient_counts=coefficient_counts(combo),
                trace_correct=profile.trace_correct,
                ok=profile.ok,
            )
        )
    return tuple(rows)


def profile_doubling_distribution() -> KsyYDoublingDistributionProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    footprint = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    doubled = double_pushforward(bridge)

    right_order = multiplicative_order(2, RIGHT_ORDER)
    c_order = multiplicative_order(2, C_ORDER)
    source_order = lcm(right_order, c_order)
    kernel_size = gcd(2, RIGHT_ORDER) * gcd(2, C_ORDER)

    orbit_rings: list[Ring] = []
    current = bridge
    for _index in range(source_order):
        orbit_rings.append(current)
        current = double_pushforward(current)
    orbit_tuple = tuple(orbit_rings)
    unique_support = len(set().union(*(set(ring) for ring in orbit_tuple)))

    orbit_total = orbit_sum(orbit_tuple)
    alternating_total = orbit_sum(orbit_tuple, alternating=True)
    lambda_rows = lambda_scan_rows(footprint, doubled)
    lambda_minus_one = add_rings(footprint, scale_ring(doubled, -1))
    scaled_bridge = divide_ring_exact(lambda_minus_one, -4)

    doubled_profile = bridge_profile("ksy_y_doubled_bridge_distribution_control", doubled)
    orbit_profile = bridge_profile("ksy_y_doubling_orbit_sum_control", orbit_total)
    scaled_profile = bridge_profile("ksy_y_lambda_minus_one_scaled_bridge", scaled_bridge)

    row_ok = (
        right_order == 20
        and c_order == 156
        and source_order == 780
        and kernel_size == 1
        and len(bridge) == 150
        and len(doubled) == 150
        and not doubled_profile.ok
        and doubled_profile.raw_support == 150
        and doubled_profile.quotient_support == 6
        and not doubled_profile.trace_correct
        and unique_support == 11700
        and len(orbit_total) == 7800
        and coefficient_counts(orbit_total) == ((-10, 3900), (10, 3900))
        and not orbit_profile.ok
        and len(alternating_total) == 0
        and tuple(row.lambda_value for row in lambda_rows if row.support == 150) == (-1,)
        and not any(row.ok for row in lambda_rows)
        and scaled_profile.ok
    )
    return KsyYDoublingDistributionProfile(
        right_order_of_2=right_order,
        c_order_of_2=c_order,
        source_order_of_2=source_order,
        doubling_kernel_size=kernel_size,
        bridge_support=len(bridge),
        doubled_support=len(doubled),
        doubled_profile=doubled_profile,
        orbit_unique_support=unique_support,
        orbit_sum_support=len(orbit_total),
        orbit_sum_coefficient_counts=coefficient_counts(orbit_total),
        orbit_sum_profile=orbit_profile,
        alternating_orbit_support=len(alternating_total),
        lambda_scan=lambda_rows,
        lambda_minus_one_scaled_bridge_ok=scaled_profile.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY-y doubling-distribution gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_doubling_distribution()
    print(f"ksy_y_doubling_distribution_profile={profile}")
    print("doubling_laws")
    print("  multiplication_by_2_has_trivial_kernel_on_C75xC169=1")
    print("  order_of_2_on_source_group_is_780=1")
    print("  doubled_bridge_has_support_150_but_wrong_trace=1")
    print("  full_doubling_orbit_union_has_support_11700=1")
    print("  full_orbit_sum_has_support_7800_and_fails_bridge_contract=1")
    print("  alternating_full_orbit_sum_is_zero=1")
    print("  among_lambda_-5_to_5_only_lambda_-1_reduces_support_to_150=1")
    print("  lambda_-1_then_exact_divide_by_-4_recovers_bridge=1")
    print("interpretation")
    print("  ordinary_doubling_distribution_does_not_cancel_the_g2Q_layer=1")
    print("  theorem_route_must_supply_exact_doubled_layer_subtraction_or_equivalent_dlog_cancellation=1")
    print(f"robert_ksy_y_doubling_distribution_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_y_doubling_distribution_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
