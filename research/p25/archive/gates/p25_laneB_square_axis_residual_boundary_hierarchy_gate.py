#!/usr/bin/env python3
"""First-boundary hierarchy for the full p25 square-axis residual.

The seed boundary gates isolate the X/Y/X+Y no-borrow frame inside the
six-term seed.  The full 18-point residual also contains the three-term
S-orbit factor.  This gate checks the first-difference hierarchy on the full
residual, so the producer contract distinguishes the outer S orbit from the
inner seed frame.

On the full residual, the only support-6 first boundaries are the S-orbit
directions +/-D = +/-172.  The signed seed-frame directions appear at support
18, not at the absolute minimum.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
    residual_q_values,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


SIGNED_S_DIRECTIONS = {
    S_STEP % QUOTIENT_ORDER: "+D",
    (-S_STEP) % QUOTIENT_ORDER: "-D",
}

SIGNED_TWO_S_DIRECTIONS = {
    (2 * S_STEP) % QUOTIENT_ORDER: "+2D",
    (-2 * S_STEP) % QUOTIENT_ORDER: "-2D",
}

SIGNED_FRAME_DIRECTIONS = {
    Y_STEP % QUOTIENT_ORDER: "+Y",
    (-Y_STEP) % QUOTIENT_ORDER: "-Y",
    X_STEP % QUOTIENT_ORDER: "+X",
    (-X_STEP) % QUOTIENT_ORDER: "-X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "+X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "-X-Y",
}


@dataclass(frozen=True)
class BoundaryProfile:
    direction: int
    label: str
    support_count: int
    coefficient_counts: tuple[tuple[int, int], ...]
    positive: tuple[int, ...]
    negative: tuple[int, ...]


def direction_label(direction: int) -> str:
    if direction in SIGNED_S_DIRECTIONS:
        return SIGNED_S_DIRECTIONS[direction]
    if direction in SIGNED_TWO_S_DIRECTIONS:
        return SIGNED_TWO_S_DIRECTIONS[direction]
    if direction in SIGNED_FRAME_DIRECTIONS:
        return SIGNED_FRAME_DIRECTIONS[direction]
    return "other"


def first_boundary_profile(direction: int) -> BoundaryProfile:
    coefficients: dict[int, int] = {}
    for point in residual_q_values():
        coefficients[point] = coefficients.get(point, 0) + 1
        shifted = (point + direction) % QUOTIENT_ORDER
        coefficients[shifted] = coefficients.get(shifted, 0) - 1
    coefficients = {point: coefficient for point, coefficient in coefficients.items() if coefficient}
    return BoundaryProfile(
        direction=direction,
        label=direction_label(direction),
        support_count=len(coefficients),
        coefficient_counts=tuple(sorted(Counter(coefficients.values()).items())),
        positive=tuple(sorted(point for point, coefficient in coefficients.items() if coefficient > 0)),
        negative=tuple(sorted(point for point, coefficient in coefficients.items() if coefficient < 0)),
    )


def expected_distribution() -> Counter[int]:
    return Counter({
        6: 2,
        12: 2,
        18: 10,
        22: 6,
        26: 8,
        28: 2,
        30: 16,
        32: 8,
        34: 8,
        36: 444,
    })


def main() -> int:
    print("p25 Lane B square-axis residual-boundary-hierarchy gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} D={S_STEP} "
        f"X={X_STEP} Y={Y_STEP} X_plus_Y={X_STEP + Y_STEP}"
    )
    profiles = [
        first_boundary_profile(direction)
        for direction in range(1, QUOTIENT_ORDER)
    ]
    support_counts = Counter(profile.support_count for profile in profiles)
    by_support: dict[int, list[BoundaryProfile]] = {}
    for profile in profiles:
        by_support.setdefault(profile.support_count, []).append(profile)

    support6 = by_support.get(6, [])
    support12 = by_support.get(12, [])
    support18 = by_support.get(18, [])
    support18_directions = {profile.direction for profile in support18}
    signed_frame_hits = support18_directions & set(SIGNED_FRAME_DIRECTIONS)
    cross_layer_support18 = support18_directions - set(SIGNED_FRAME_DIRECTIONS)
    expected_support18 = {9, 43, 52, 120, 215, 292, 387, 455, 464, 498}
    row_ok = (
        len(profiles) == 506
        and support_counts == expected_distribution()
        and {profile.direction for profile in support6} == set(SIGNED_S_DIRECTIONS)
        and {profile.direction for profile in support12} == set(SIGNED_TWO_S_DIRECTIONS)
        and support18_directions == expected_support18
        and signed_frame_hits == set(SIGNED_FRAME_DIRECTIONS)
        and cross_layer_support18 == {120, 215, 292, 387}
        and all(profile.coefficient_counts == ((-1, profile.support_count // 2), (1, profile.support_count // 2)) for profile in support6 + support12 + support18)
    )
    print(
        "residual_boundary_hierarchy: "
        f"direction_count={len(profiles)} "
        f"support_distribution={dict(sorted(support_counts.items()))} "
        f"support6={[profile.direction for profile in support6]} "
        f"support12={[profile.direction for profile in support12]} "
        f"support18={sorted(support18_directions)} "
        f"signed_frame_support18={sorted(signed_frame_hits)} "
        f"cross_layer_support18={sorted(cross_layer_support18)} "
        f"ok={int(row_ok)}"
    )
    print("support6_profiles")
    for profile in support6:
        print(
            f"  direction={profile.direction} label={profile.label} "
            f"positive={list(profile.positive)} negative={list(profile.negative)}"
        )
    print("support12_profiles")
    for profile in support12:
        print(
            f"  direction={profile.direction} label={profile.label} "
            f"positive={list(profile.positive)} negative={list(profile.negative)}"
        )
    print("support18_profiles")
    for profile in support18:
        print(
            f"  direction={profile.direction} label={profile.label} "
            f"positive={list(profile.positive)} negative={list(profile.negative)}"
        )
    print(f"square_axis_residual_boundary_hierarchy_rows={int(row_ok)}/1")
    print("interpretation")
    print("  full_residual_minimal_first_boundary_is_the_S_orbit_direction=1")
    print("  seed_frame_directions_are_support18_on_the_full_residual_not_support6=1")
    print("  producer_must_explain_outer_S_orbit_before_inner_no_borrow_seed_frame=1")
    print("  full_residual_boundary_arguments_must_not_apply_seed_only_minimality_directly=1")
    print("conclusion=reported_p25_laneB_square_axis_residual_boundary_hierarchy_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
