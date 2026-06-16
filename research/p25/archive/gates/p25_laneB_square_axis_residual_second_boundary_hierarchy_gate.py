#!/usr/bin/env python3
"""Two-direction boundary hierarchy for the full p25 square-axis residual.

The residual-boundary hierarchy gate shows that the full 18-point residual
first sees the outer S-orbit direction D.  This gate checks the next layer:

    (1 - T_a)(1 - T_b) residual.

Exhausting all unordered nonzero direction pairs in C_507, support 8 occurs
only for one outer direction +/-D paired with one non-Y seed-frame direction
+/-X or +/-(X+Y).  The signed Y direction is exceptional here because the
outer relation D^3 = Y has already collapsed the D boundary to a Y boundary
on the seed.
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


SIGNED_D_DIRECTIONS = {
    S_STEP % QUOTIENT_ORDER: "+D",
    (-S_STEP) % QUOTIENT_ORDER: "-D",
}

SIGNED_FRAME_DIRECTIONS = {
    Y_STEP % QUOTIENT_ORDER: "+Y",
    (-Y_STEP) % QUOTIENT_ORDER: "-Y",
    X_STEP % QUOTIENT_ORDER: "+X",
    (-X_STEP) % QUOTIENT_ORDER: "-X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "+X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "-X-Y",
}

SIGNED_NON_Y_FRAME_DIRECTIONS = {
    X_STEP % QUOTIENT_ORDER: "+X",
    (-X_STEP) % QUOTIENT_ORDER: "-X",
    (X_STEP + Y_STEP) % QUOTIENT_ORDER: "+X+Y",
    (-(X_STEP + Y_STEP)) % QUOTIENT_ORDER: "-X-Y",
}

SIGNED_Y_DIRECTIONS = {
    Y_STEP % QUOTIENT_ORDER: "+Y",
    (-Y_STEP) % QUOTIENT_ORDER: "-Y",
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


def direction_label(direction: int) -> str:
    if direction in SIGNED_D_DIRECTIONS:
        return SIGNED_D_DIRECTIONS[direction]
    if direction in SIGNED_FRAME_DIRECTIONS:
        return SIGNED_FRAME_DIRECTIONS[direction]
    return "other"


def residual_word() -> dict[int, int]:
    return {point: 1 for point in residual_q_values()}


def first_difference(word: dict[int, int], direction: int) -> dict[int, int]:
    out = dict(word)
    for point, coefficient in word.items():
        shifted = (point + direction) % QUOTIENT_ORDER
        out[shifted] = out.get(shifted, 0) - coefficient
    return {point: coefficient for point, coefficient in out.items() if coefficient}


def second_boundary_profile(first_direction: int, second_direction: int) -> SecondBoundaryProfile:
    boundary = first_difference(first_difference(residual_word(), first_direction), second_direction)
    return SecondBoundaryProfile(
        first_direction=first_direction,
        second_direction=second_direction,
        first_label=direction_label(first_direction),
        second_label=direction_label(second_direction),
        support_count=len(boundary),
        coefficient_counts=tuple(sorted(Counter(boundary.values()).items())),
        coefficients=tuple(sorted(boundary.items())),
    )


def expected_minimal_pairs() -> dict[tuple[int, int], tuple[str, str]]:
    return {
        (43, 172): ("+X", "+D"),
        (43, 335): ("+X", "-D"),
        (52, 172): ("+X+Y", "+D"),
        (52, 335): ("+X+Y", "-D"),
        (172, 455): ("+D", "-X-Y"),
        (172, 464): ("+D", "-X"),
        (335, 455): ("-D", "-X-Y"),
        (335, 464): ("-D", "-X"),
    }


def expected_distribution() -> Counter[int]:
    return Counter({
        8: 8,
        10: 8,
        11: 36,
        12: 959,
        16: 8,
        18: 4,
        20: 20,
        21: 4,
        22: 44,
        23: 67,
        24: 888,
        25: 4,
        26: 24,
        27: 16,
        28: 28,
        29: 35,
        30: 100,
        31: 59,
        32: 92,
        33: 236,
        34: 88,
        35: 80,
        36: 4327,
        37: 43,
        38: 52,
        39: 110,
        40: 40,
        41: 115,
        42: 64,
        43: 91,
        44: 2566,
        45: 87,
        46: 35,
        47: 78,
        48: 106,
        49: 138,
        50: 137,
        51: 206,
        52: 3394,
        53: 142,
        54: 696,
        55: 156,
        56: 936,
        57: 1056,
        58: 184,
        59: 272,
        60: 7452,
        61: 212,
        62: 180,
        63: 4152,
        64: 3248,
        65: 2548,
        66: 148,
        67: 3316,
        68: 3972,
        69: 6352,
        70: 3112,
        71: 3064,
        72: 72676,
    })


def main() -> int:
    print("p25 Lane B square-axis residual-second-boundary-hierarchy gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} D={S_STEP} "
        f"X={X_STEP} Y={Y_STEP} X_plus_Y={X_STEP + Y_STEP}"
    )
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
    minimal_pairs = {
        (profile.first_direction, profile.second_direction)
        for profile in minimal_profiles
    }
    expected_pairs = expected_minimal_pairs()
    expected_rows = sum(
        int(
            (profile.first_direction, profile.second_direction) in expected_pairs
            and (profile.first_label, profile.second_label)
            == expected_pairs[(profile.first_direction, profile.second_direction)]
            and profile.coefficient_counts == ((-1, 4), (1, 4))
        )
        for profile in minimal_profiles
    )

    d_frame_pairs = [
        profile
        for profile in profiles
        if (
            profile.first_direction in SIGNED_D_DIRECTIONS
            and profile.second_direction in SIGNED_FRAME_DIRECTIONS
        )
        or (
            profile.second_direction in SIGNED_D_DIRECTIONS
            and profile.first_direction in SIGNED_FRAME_DIRECTIONS
        )
    ]
    d_non_y_frame_minimal = [
        profile
        for profile in d_frame_pairs
        if (
            profile.first_direction in SIGNED_NON_Y_FRAME_DIRECTIONS
            or profile.second_direction in SIGNED_NON_Y_FRAME_DIRECTIONS
        )
        and profile.support_count == 8
    ]
    d_y_supports = {
        (profile.first_direction, profile.second_direction): profile.support_count
        for profile in d_frame_pairs
        if (
            profile.first_direction in SIGNED_Y_DIRECTIONS
            or profile.second_direction in SIGNED_Y_DIRECTIONS
        )
    }
    off_d_non_y_min_support = min(
        profile.support_count
        for profile in profiles
        if (profile.first_direction, profile.second_direction) not in expected_pairs
    )
    row_ok = (
        len(profiles) == 128271
        and support_counts == expected_distribution()
        and minimal_support == 8
        and len(minimal_profiles) == 8
        and minimal_pairs == set(expected_pairs)
        and expected_rows == 8
        and len(d_non_y_frame_minimal) == 8
        and d_y_supports == {
            (9, 172): 11,
            (9, 335): 11,
            (172, 498): 11,
            (335, 498): 11,
        }
        and off_d_non_y_min_support == 10
    )
    print(
        "residual_second_boundary_hierarchy: "
        f"pair_count={len(profiles)} "
        f"minimal_support={minimal_support} "
        f"minimal_pair_count={len(minimal_profiles)} "
        f"expected_minimal_rows={expected_rows}/8 "
        f"d_non_y_frame_minimal={len(d_non_y_frame_minimal)}/8 "
        f"d_y_supports={dict(sorted(d_y_supports.items()))} "
        f"off_d_non_y_min_support={off_d_non_y_min_support} "
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
    print(f"square_axis_residual_second_boundary_hierarchy_rows={int(row_ok)}/1")
    print("interpretation")
    print("  full_residual_minimal_second_boundaries_pair_outer_D_with_non_Y_seed_frame=1")
    print("  Y_direction_is_not_minimal_because_D_cubed_already_collapses_to_Y=1")
    print("  off_outer_or_off_frame_two_direction_boundaries_have_support_at_least_10=1")
    print("  producer_must_explain_outer_S_then_non_Y_seed_frame_boundaries=1")
    print("conclusion=reported_p25_laneB_square_axis_residual_second_boundary_hierarchy_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
