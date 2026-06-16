#!/usr/bin/env python3
"""Two-direction boundary rigidity for the p25 square-axis seed.

The seed-boundary gate shows that the only minimal first boundaries are in
the signed X/Y/X+Y directions.  This gate checks the next modular-unit shape:

    (1 - T_a)(1 - T_b) seed.

Exhausting all unordered nonzero direction pairs in C_507, the only minimal
support-8 second boundaries use two distinct signed frame directions.  No
off-frame pair, same-direction pair, or available opposite-direction pair
reaches that support.
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
class SecondBoundaryProfile:
    first_direction: int
    second_direction: int
    first_label: str
    second_label: str
    support_count: int
    coefficient_counts: tuple[tuple[int, int], ...]
    coefficients: tuple[tuple[int, int], ...]


def seed_word() -> dict[int, int]:
    return {point: 1 for point in seed_terms()}


def first_difference(word: dict[int, int], direction: int) -> dict[int, int]:
    out = dict(word)
    for point, coefficient in word.items():
        shifted = (point + direction) % QUOTIENT_ORDER
        out[shifted] = out.get(shifted, 0) - coefficient
    return {point: coefficient for point, coefficient in out.items() if coefficient}


def second_boundary_profile(first_direction: int, second_direction: int) -> SecondBoundaryProfile:
    boundary = first_difference(first_difference(seed_word(), first_direction), second_direction)
    counts = Counter(boundary.values())
    return SecondBoundaryProfile(
        first_direction=first_direction,
        second_direction=second_direction,
        first_label=SIGNED_DIRECTIONS.get(first_direction, "other"),
        second_label=SIGNED_DIRECTIONS.get(second_direction, "other"),
        support_count=len(boundary),
        coefficient_counts=tuple(sorted(counts.items())),
        coefficients=tuple(sorted(boundary.items())),
    )


def expected_minimal_pairs() -> dict[tuple[int, int], tuple[str, str]]:
    return {
        (9, 43): ("+Y", "+X"),
        (9, 52): ("+Y", "+X+Y"),
        (9, 455): ("+Y", "-X-Y"),
        (9, 464): ("+Y", "-X"),
        (43, 52): ("+X", "+X+Y"),
        (43, 455): ("+X", "-X-Y"),
        (43, 498): ("+X", "-Y"),
        (52, 464): ("+X+Y", "-X"),
        (52, 498): ("+X+Y", "-Y"),
        (455, 464): ("-X-Y", "-X"),
        (455, 498): ("-X-Y", "-Y"),
        (464, 498): ("-X", "-Y"),
    }


def expected_same_or_opposite_frame_supports() -> dict[tuple[int, int], int]:
    return {
        (9, 9): 11,
        (9, 498): 11,
        (43, 43): 11,
        (43, 464): 11,
        (52, 52): 11,
        (52, 455): 11,
        (455, 455): 11,
        (464, 464): 11,
        (498, 498): 11,
    }


def main() -> int:
    print("p25 Lane B square-axis seed-second-boundary-rigidity gate")
    print(f"quotient_order={QUOTIENT_ORDER} X={X_STEP} Y={Y_STEP} X_plus_Y={X_STEP + Y_STEP}")
    profiles = [
        second_boundary_profile(first_direction, second_direction)
        for first_direction in range(1, QUOTIENT_ORDER)
        for second_direction in range(first_direction, QUOTIENT_ORDER)
    ]
    support_counts = Counter(profile.support_count for profile in profiles)
    minimal_support = min(profile.support_count for profile in profiles)
    minimal_profiles = [
        profile for profile in profiles if profile.support_count == minimal_support
    ]
    expected_pairs = expected_minimal_pairs()
    minimal_pairs = {
        (profile.first_direction, profile.second_direction)
        for profile in minimal_profiles
    }
    expected_rows = sum(
        int(
            (profile.first_direction, profile.second_direction) in expected_pairs
            and (
                profile.first_label,
                profile.second_label,
            )
            == expected_pairs[(profile.first_direction, profile.second_direction)]
            and profile.coefficient_counts == ((-1, 4), (1, 4))
        )
        for profile in minimal_profiles
    )
    frame_directions = set(SIGNED_DIRECTIONS)
    off_frame_min_support = min(
        profile.support_count
        for profile in profiles
        if profile.first_direction not in frame_directions
        or profile.second_direction not in frame_directions
    )
    same_or_opposite_frame_supports = {
        (profile.first_direction, profile.second_direction): profile.support_count
        for profile in profiles
        if profile.first_direction in frame_directions
        and profile.second_direction in frame_directions
        and (
            profile.first_direction == profile.second_direction
            or (profile.first_direction + profile.second_direction) % QUOTIENT_ORDER == 0
        )
    }
    expected_same_or_opposite = expected_same_or_opposite_frame_supports()
    row_ok = (
        len(profiles) == 128271
        and minimal_support == 8
        and len(minimal_profiles) == 12
        and minimal_pairs == set(expected_pairs)
        and expected_rows == 12
        and off_frame_min_support == 10
        and same_or_opposite_frame_supports == expected_same_or_opposite
        and support_counts[8] == 12
        and support_counts[10] == 24
        and support_counts[11] == 105
        and support_counts[24] == 110076
    )
    print(
        "seed_second_boundary_rigidity: "
        f"pair_count={len(profiles)} "
        f"minimal_support={minimal_support} "
        f"minimal_pair_count={len(minimal_profiles)} "
        f"expected_minimal_rows={expected_rows}/12 "
        f"off_frame_min_support={off_frame_min_support} "
        f"same_or_opposite_frame_supports={dict(sorted(same_or_opposite_frame_supports.items()))} "
        f"ok={int(row_ok)}"
    )
    print(f"support_count_distribution={dict(sorted(support_counts.items()))}")
    print("minimal_second_boundary_profiles")
    for profile in minimal_profiles:
        print(
            f"  directions=({profile.first_direction},{profile.second_direction}) "
            f"labels=({profile.first_label},{profile.second_label}) "
            f"coefficient_counts={dict(profile.coefficient_counts)} "
            f"coefficients={list(profile.coefficients)}"
        )
    print(f"square_axis_seed_second_boundary_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  second_boundary_support_is_minimal_only_for_distinct_signed_frame_pairs=1")
    print("  off_frame_two_direction_boundaries_have_support_at_least_10=1")
    print("  same_or_opposite_frame_direction_pairs_do_not_attain_minimal_support=1")
    print("  two_unit_boundary_explanations_are_forced_onto_the_X_Y_XplusY_frame=1")
    print("conclusion=reported_p25_laneB_square_axis_seed_second_boundary_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
