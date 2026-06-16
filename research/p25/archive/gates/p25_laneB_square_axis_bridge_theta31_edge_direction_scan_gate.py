#!/usr/bin/env python3
"""All-direction theta_{3,1} edge scan for the p25 bridge.

The theta31 edge falsifier shows that the natural D and T edges do not produce
the primitive bridge.  This gate strengthens that check: scan every nonzero
finite-difference direction of the square-axis theta_{3,1} quotient and ask
whether any single edge is the bridge up to scalar, sign, and translation.

Only the two signed D directions have bridge-sized six-point support, and both
are disjoint from the bridge support.  The next correction must therefore be a
new mixed combination, not a different single edge of the canonical theta
pullback.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import MODULUS, quotient_trace
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_theta31_edge_falsifier_gate import theta31_raw_packet
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class SmallDirectionProfile:
    direction: int
    support_size: int
    support: tuple[int, ...]
    coefficient_counts: tuple[tuple[int, int], ...]
    bridge_support_overlap: int
    bridge_translation_matches: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class EdgeDirectionScanProfile:
    direction_count: int
    min_support: int
    min_support_directions: tuple[int, ...]
    support_12_directions: tuple[int, ...]
    small_direction_profiles: tuple[SmallDirectionProfile, ...]
    exact_bridge_match_count: int
    exact_bridge_matches: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]
    bridge_sized_disjoint_count: int
    max_support: int
    max_support_count: int
    overlap_distribution: tuple[tuple[int, int], ...]
    support_distribution_key: tuple[tuple[int, int], ...]


def signed(value: int) -> int:
    value %= MODULUS
    if value > MODULUS // 2:
        return value - MODULUS
    return value


def normalize(values: list[int]) -> list[int]:
    nonzero = sorted({value % MODULUS for value in values if value % MODULUS})
    if not nonzero:
        return values
    inverse = pow(nonzero[0], -1, MODULUS)
    return [(value * inverse) % MODULUS for value in values]


def quotient_theta_packet() -> list[int]:
    return [value % MODULUS for value in quotient_trace(theta31_raw_packet())]


def edge_coefficients(packet: list[int], direction: int) -> dict[int, int]:
    raw_edge = [
        (packet[index] - packet[(index - direction) % QUOTIENT_ORDER]) % MODULUS
        for index in range(QUOTIENT_ORDER)
    ]
    normalized = normalize(raw_edge)
    return {
        index: signed(value)
        for index, value in enumerate(normalized)
        if value % MODULUS
    }


def bridge_translation_matches(coefficients: dict[int, int]) -> tuple[tuple[int, int], ...]:
    target = bridge_coefficients()
    matches: list[tuple[int, int]] = []
    for shift in range(QUOTIENT_ORDER):
        for sign in (1, -1):
            translated = {
                (q_value + shift) % QUOTIENT_ORDER: sign * value
                for q_value, value in target.items()
            }
            if translated == coefficients:
                matches.append((shift, sign))
    return tuple(matches)


def scan_profile() -> EdgeDirectionScanProfile:
    packet = quotient_theta_packet()
    target_support = set(bridge_coefficients())
    support_counts: Counter[int] = Counter()
    overlap_counts: Counter[int] = Counter()
    small_profiles: list[SmallDirectionProfile] = []
    exact_matches: list[tuple[int, tuple[tuple[int, int], ...]]] = []

    for direction in range(1, QUOTIENT_ORDER):
        coefficients = edge_coefficients(packet, direction)
        support = tuple(sorted(coefficients))
        support_size = len(support)
        matches = bridge_translation_matches(coefficients)
        support_counts[support_size] += 1
        overlap_counts[len(set(support) & target_support)] += 1
        if support_size <= 12:
            small_profiles.append(
                SmallDirectionProfile(
                    direction=direction,
                    support_size=support_size,
                    support=support,
                    coefficient_counts=tuple(sorted(Counter(coefficients.values()).items())),
                    bridge_support_overlap=len(set(support) & target_support),
                    bridge_translation_matches=matches,
                )
            )
        if matches:
            exact_matches.append((direction, matches))

    min_support = min(support_counts)
    max_support = max(support_counts)
    return EdgeDirectionScanProfile(
        direction_count=QUOTIENT_ORDER - 1,
        min_support=min_support,
        min_support_directions=tuple(
            sorted(
                direction
                for direction in range(1, QUOTIENT_ORDER)
                if len(edge_coefficients(packet, direction)) == min_support
            )
        ),
        support_12_directions=tuple(
            sorted(
                direction
                for direction in range(1, QUOTIENT_ORDER)
                if len(edge_coefficients(packet, direction)) == 12
            )
        ),
        small_direction_profiles=tuple(small_profiles),
        exact_bridge_match_count=len(exact_matches),
        exact_bridge_matches=tuple(exact_matches),
        bridge_sized_disjoint_count=sum(
            1
            for profile in small_profiles
            if profile.support_size == 6 and profile.bridge_support_overlap == 0
        ),
        max_support=max_support,
        max_support_count=support_counts[max_support],
        overlap_distribution=tuple(sorted(overlap_counts.items())),
        support_distribution_key=tuple(
            sorted((support, count) for support, count in support_counts.items() if support <= 24 or support == max_support)
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge theta31 edge direction-scan gate")
    print(f"quotient_order={QUOTIENT_ORDER} modulus={MODULUS} D={S_STEP}")
    profile = scan_profile()
    expected_small = (
        SmallDirectionProfile(163, 12, (163, 166, 206, 249, 292, 332, 335, 378, 421, 464, 501, 504), ((-1, 6), (1, 6)), 0, ()),
        SmallDirectionProfile(172, 6, (0, 43, 86, 129, 169, 338), ((-1, 3), (1, 3)), 0, ()),
        SmallDirectionProfile(335, 6, (166, 335, 378, 421, 464, 504), ((-1, 3), (1, 3)), 0, ()),
        SmallDirectionProfile(344, 12, (0, 3, 43, 86, 129, 169, 172, 215, 258, 301, 338, 341), ((-1, 6), (1, 6)), 0, ()),
    )
    expected = EdgeDirectionScanProfile(
        direction_count=506,
        min_support=6,
        min_support_directions=(172, 335),
        support_12_directions=(163, 344),
        small_direction_profiles=expected_small,
        exact_bridge_match_count=0,
        exact_bridge_matches=(),
        bridge_sized_disjoint_count=2,
        max_support=338,
        max_support_count=88,
        overlap_distribution=((0, 160), (1, 8), (2, 8), (3, 157), (4, 4), (5, 4), (6, 165)),
        support_distribution_key=((6, 2), (12, 2), (18, 2), (24, 2), (338, 88)),
    )
    row_ok = (
        profile == expected
        and profile.min_support_directions == (S_STEP, (-S_STEP) % QUOTIENT_ORDER)
        and profile.exact_bridge_match_count == 0
    )

    print(f"bridge_coefficients={sorted(bridge_coefficients().items())}")
    print(f"edge_direction_scan_profile={profile}")
    print("scan_laws")
    print("  all 506 nonzero finite-difference directions were checked")
    print("  only +/-D have six-point support")
    print("  the two bridge-sized theta edges are disjoint from the primitive bridge")
    print("  no theta edge is the bridge up to scalar, sign, or translation")
    print("interpretation")
    print("  canonical_theta31_has_no_single_edge_equal_to_the_bridge=1")
    print("  theta31_D_edge_near_miss_is_globally_minimal_among_theta_edges=1")
    print("  required_mixed_correction_cannot_be_a_different_single_theta_edge=1")
    print("  next_producer_candidate_must_combine_or_modify_theta_edges=1")
    print(f"square_axis_bridge_theta31_edge_direction_scan_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_theta31_edge_direction_scan_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
