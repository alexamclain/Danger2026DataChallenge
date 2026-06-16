#!/usr/bin/env python3
"""Boundary rigidity for the p25 square-axis no-borrow seed.

The seed-frame gate shows that the AP rectangles containing the six-term seed
use only the signed X/Y/X+Y directions.  This gate gives the same fact a
modular-unit style formulation: apply the first-difference operator

    (1 - T_d)

to the seed word in Z[C_507].  The only directions with minimal boundary
support are the signed frame directions

    +/-Y, +/-X, +/-(X+Y).

Every other nonzero direction has first-difference support at least 10.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import X_STEP, Y_STEP, seed_terms
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


SIGNED_DIRECTIONS = {
    Y_STEP % QUOTIENT_ORDER: "+Y",
    (-Y_STEP) % QUOTIENT_ORDER: "-Y",
    X_STEP % QUOTIENT_ORDER: "+X",
    (-X_STEP) % QUOTIENT_ORDER: "-X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "+X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "-X-Y",
}


@dataclass(frozen=True)
class DifferenceProfile:
    direction: int
    label: str
    support_count: int
    positive: tuple[int, ...]
    negative: tuple[int, ...]


def first_difference_profile(direction: int) -> DifferenceProfile:
    coefficients: dict[int, int] = {}
    for point in seed_terms():
        coefficients[point] = coefficients.get(point, 0) + 1
        shifted = (point + direction) % QUOTIENT_ORDER
        coefficients[shifted] = coefficients.get(shifted, 0) - 1
    coefficients = {point: coeff for point, coeff in coefficients.items() if coeff}
    positive = tuple(sorted(point for point, coeff in coefficients.items() if coeff > 0))
    negative = tuple(sorted(point for point, coeff in coefficients.items() if coeff < 0))
    return DifferenceProfile(
        direction=direction,
        label=SIGNED_DIRECTIONS.get(direction, "other"),
        support_count=len(coefficients),
        positive=positive,
        negative=negative,
    )


def expected_minimal_profiles() -> dict[int, tuple[str, tuple[int, ...], tuple[int, ...]]]:
    return {
        9: ("+Y", (43, 86, 129), (52, 104, 156)),
        43: ("+X", (43, 95, 147), (172, 181, 190)),
        52: ("+X+Y", (43, 86, 129), (181, 190, 199)),
        455: ("-X-Y", (129, 138, 147), (34, 77, 498)),
        464: ("-X", (129, 138, 147), (0, 52, 104)),
        498: ("-Y", (43, 95, 147), (34, 77, 120)),
    }


def main() -> int:
    print("p25 Lane B square-axis seed-boundary-rigidity gate")
    print(f"quotient_order={QUOTIENT_ORDER} X={X_STEP} Y={Y_STEP} X_plus_Y={X_STEP + Y_STEP}")
    profiles = [
        first_difference_profile(direction)
        for direction in range(1, QUOTIENT_ORDER)
    ]
    support_counts = Counter(profile.support_count for profile in profiles)
    minimal_support = min(profile.support_count for profile in profiles)
    minimal_profiles = [
        profile for profile in profiles if profile.support_count == minimal_support
    ]
    expected = expected_minimal_profiles()
    expected_rows = 0
    for profile in minimal_profiles:
        expected_label, expected_positive, expected_negative = expected.get(
            profile.direction,
            ("missing", (), ()),
        )
        if (
            profile.label == expected_label
            and profile.positive == expected_positive
            and profile.negative == expected_negative
        ):
            expected_rows += 1
    non_frame_min_support = min(
        profile.support_count
        for profile in profiles
        if profile.direction not in SIGNED_DIRECTIONS
    )
    next_support_directions = [
        profile.direction
        for profile in profiles
        if profile.support_count == non_frame_min_support
    ]
    row_ok = (
        minimal_support == 6
        and len(minimal_profiles) == 6
        and {profile.direction for profile in minimal_profiles} == set(SIGNED_DIRECTIONS)
        and expected_rows == 6
        and non_frame_min_support == 10
        and support_counts == Counter({12: 488, 10: 12, 6: 6})
    )
    print(
        "seed_boundary_rigidity: "
        f"minimal_support={minimal_support} "
        f"minimal_direction_count={len(minimal_profiles)} "
        f"expected_minimal_rows={expected_rows}/6 "
        f"non_frame_min_support={non_frame_min_support} "
        f"support_count_distribution={dict(sorted(support_counts.items()))} "
        f"ok={int(row_ok)}"
    )
    print("minimal_first_difference_profiles")
    for profile in sorted(minimal_profiles, key=lambda item: item.direction):
        print(
            f"  direction={profile.direction} label={profile.label} "
            f"positive={list(profile.positive)} "
            f"negative={list(profile.negative)}"
        )
    print(f"next_support_directions={next_support_directions}")
    print(f"square_axis_seed_boundary_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  first_difference_boundary_is_minimal_only_in_signed_X_Y_XplusY_directions=1")
    print("  every_other_direction_has_boundary_support_at_least_10=1")
    print("  modular_unit_style_single_direction_boundaries_must_use_the_seed_frame=1")
    print("  producer_cannot_use_an_unrelated_small_boundary_direction=1")
    print("conclusion=reported_p25_laneB_square_axis_seed_boundary_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
