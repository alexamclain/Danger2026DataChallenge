#!/usr/bin/env python3
"""Inversion-image support law for K-traced p25 Hilbert-90 corners.

The first-boundary support gate made the K-orbit ladder visible through the
first boundary: support 75 corners have support 100 minimal first boundaries.
This gate records the next producer-facing step.  The recorded support-100
half-boundary expands under the inversion boundary to the support-150 signed
bridge, and it is the unique first-boundary direction that does so.

There is a small trap here: some wrong support-100 first boundaries also have
support-150 inversion images.  The image support count is necessary but not a
certificate; the signed bridge image is the actual gate.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    boundary,
    inversion_boundary,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_gate import (
    k_trace_minimality_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Items = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class Support100ImageRow:
    direction_q: int
    direction_d: int
    image_raw_support: int
    image_is_bridge: bool


@dataclass(frozen=True)
class CornerImageSupportRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    chain_q_values: tuple[int, ...]
    chain_raw_support: int
    first_boundary_raw_support_distribution: tuple[tuple[int, int], ...]
    image_raw_support_distribution: tuple[tuple[int, int], ...]
    support100_image_raw_support_distribution: tuple[tuple[int, int], ...]
    support100_image_rows: tuple[Support100ImageRow, ...]
    recorded_first_boundary_raw_support: int
    recorded_image_raw_support: int
    recorded_image_q_items: Items
    recorded_image_d_items: Items
    bridge_hit_directions: tuple[int, ...]
    bridge_hit_d_directions: tuple[int, ...]
    bridge_hit_is_recorded_support100: bool
    wrong_support100_directions: tuple[int, ...]
    wrong_support100_support150_count: int
    wrong_support100_support200_count: int


@dataclass(frozen=True)
class CornerImageSupportProfile:
    row_count: int
    kernel_order: int
    forced_corner_raw_support: int
    recorded_first_boundary_raw_support: int
    bridge_raw_support: int
    bridge_q_items: Items
    bridge_d_items: Items
    all_rows_have_ladder_75_100_150: bool
    all_rows_have_unique_recorded_bridge_hit: bool
    all_support100_sets_are_pair_difference_sixpacks: bool
    support150_image_is_not_sufficient: bool
    rows: tuple[CornerImageSupportRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


def d_items(poly: dict[int, int]) -> Items:
    return tuple(
        sorted((d_residue_from_q(q_value), coefficient) for q_value, coefficient in poly.items())
    )


def raw_support_distribution(counter: Counter[int], kernel_order: int) -> tuple[tuple[int, int], ...]:
    return tuple((support * kernel_order, count) for support, count in sorted(counter.items()))


def pair_difference_directions(q_values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                (right - left) % QUOTIENT_ORDER
                for left in q_values
                for right in q_values
                if left != right
            }
        )
    )


def scan_row(row, kernel_order: int) -> CornerImageSupportRow:
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    bridge = bridge_coefficients()

    first_counter: Counter[int] = Counter()
    image_counter: Counter[int] = Counter()
    support100_image_counter: Counter[int] = Counter()
    support100_rows: list[Support100ImageRow] = []
    bridge_hits: list[int] = []

    recorded_first: dict[int, int] | None = None
    recorded_image: dict[int, int] | None = None

    for direction in range(1, QUOTIENT_ORDER):
        first = boundary(chain, direction)
        image = inversion_boundary(first)
        first_counter[len(first)] += 1
        image_counter[len(image)] += 1
        if image == bridge:
            bridge_hits.append(direction)
        if direction == row.boundary_direction_q:
            recorded_first = first
            recorded_image = image
        if len(first) * kernel_order == 100:
            support100_image_counter[len(image)] += 1
            support100_rows.append(
                Support100ImageRow(
                    direction_q=direction,
                    direction_d=d_residue_from_q(direction),
                    image_raw_support=len(image) * kernel_order,
                    image_is_bridge=image == bridge,
                )
            )

    if recorded_first is None or recorded_image is None:
        raise AssertionError("recorded direction was not scanned")

    wrong_support100_rows = tuple(row for row in support100_rows if not row.image_is_bridge)
    return CornerImageSupportRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.boundary_direction_q,
        recorded_direction_d=d_residue_from_q(row.boundary_direction_q),
        chain_q_values=row.q_values,
        chain_raw_support=len(chain) * kernel_order,
        first_boundary_raw_support_distribution=raw_support_distribution(first_counter, kernel_order),
        image_raw_support_distribution=raw_support_distribution(image_counter, kernel_order),
        support100_image_raw_support_distribution=raw_support_distribution(
            support100_image_counter,
            kernel_order,
        ),
        support100_image_rows=tuple(support100_rows),
        recorded_first_boundary_raw_support=len(recorded_first) * kernel_order,
        recorded_image_raw_support=len(recorded_image) * kernel_order,
        recorded_image_q_items=as_items(recorded_image),
        recorded_image_d_items=d_items(recorded_image),
        bridge_hit_directions=tuple(bridge_hits),
        bridge_hit_d_directions=tuple(d_residue_from_q(direction) for direction in bridge_hits),
        bridge_hit_is_recorded_support100=(
            tuple(bridge_hits) == (row.boundary_direction_q,)
            and len(recorded_first) * kernel_order == 100
        ),
        wrong_support100_directions=tuple(row.direction_q for row in wrong_support100_rows),
        wrong_support100_support150_count=sum(
            row.image_raw_support == 150 for row in wrong_support100_rows
        ),
        wrong_support100_support200_count=sum(
            row.image_raw_support == 200 for row in wrong_support100_rows
        ),
    )


def corner_image_support_profile() -> CornerImageSupportProfile:
    kernel_order = k_trace_minimality_profile().kernel_order
    bridge = bridge_coefficients()
    rows = tuple(scan_row(row, kernel_order) for row in coefficient_rigidity_profile().rows)
    return CornerImageSupportProfile(
        row_count=len(rows),
        kernel_order=kernel_order,
        forced_corner_raw_support=75,
        recorded_first_boundary_raw_support=100,
        bridge_raw_support=len(bridge) * kernel_order,
        bridge_q_items=as_items(bridge),
        bridge_d_items=d_items(bridge),
        all_rows_have_ladder_75_100_150=all(
            row.chain_raw_support == 75
            and row.recorded_first_boundary_raw_support == 100
            and row.recorded_image_raw_support == 150
            and row.recorded_image_q_items == as_items(bridge)
            for row in rows
        ),
        all_rows_have_unique_recorded_bridge_hit=all(
            row.bridge_hit_is_recorded_support100 for row in rows
        ),
        all_support100_sets_are_pair_difference_sixpacks=all(
            tuple(row.direction_q for row in profile_row.support100_image_rows)
            == pair_difference_directions(profile_row.chain_q_values)
            for profile_row in rows
        ),
        support150_image_is_not_sufficient=all(
            row.wrong_support100_support150_count >= 1 for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner image-support gate")
    profile = corner_image_support_profile()
    expected_bridge_q = ((25, 1), (138, -1), (197, 1), (310, -1), (369, 1), (482, -1))
    expected_bridge_d = ((121, 1), (122, 1), (123, 1), (384, -1), (385, -1), (386, -1))
    expected_support100_a = (
        Support100ImageRow(25, 121, 150, False),
        Support100ImageRow(172, 1, 150, False),
        Support100ImageRow(197, 122, 150, True),
        Support100ImageRow(310, 385, 150, False),
        Support100ImageRow(335, 506, 150, False),
        Support100ImageRow(482, 386, 150, False),
    )
    expected_support100_b = (
        Support100ImageRow(25, 121, 200, False),
        Support100ImageRow(172, 1, 200, False),
        Support100ImageRow(197, 122, 200, False),
        Support100ImageRow(310, 385, 150, True),
        Support100ImageRow(335, 506, 150, False),
        Support100ImageRow(482, 386, 200, False),
    )
    expected_support100_c = (
        Support100ImageRow(25, 121, 200, False),
        Support100ImageRow(172, 1, 150, False),
        Support100ImageRow(197, 122, 150, True),
        Support100ImageRow(310, 385, 200, False),
        Support100ImageRow(335, 506, 200, False),
        Support100ImageRow(482, 386, 200, False),
    )
    expected_support100_d = (
        Support100ImageRow(25, 121, 150, False),
        Support100ImageRow(172, 1, 150, False),
        Support100ImageRow(197, 122, 150, False),
        Support100ImageRow(310, 385, 150, True),
        Support100ImageRow(335, 506, 150, False),
        Support100ImageRow(482, 386, 150, False),
    )
    expected_rows = (
        CornerImageSupportRow(1, 197, 122, (0, 172, 482), 75, ((100, 6), (150, 500)), ((150, 10), (200, 2), (250, 494)), ((150, 6),), expected_support100_a, 100, 150, expected_bridge_q, expected_bridge_d, (197,), (122,), True, (25, 172, 310, 335, 482), 5, 0),
        CornerImageSupportRow(1, 310, 385, (172, 197, 369), 75, ((100, 6), (150, 500)), ((150, 3), (200, 9), (250, 3), (300, 491)), ((150, 2), (200, 4)), expected_support100_b, 100, 150, expected_bridge_q, expected_bridge_d, (310,), (385,), True, (25, 172, 197, 335, 482), 1, 4),
        CornerImageSupportRow(6, 197, 122, (138, 310, 335), 75, ((100, 6), (150, 500)), ((150, 3), (200, 9), (250, 3), (300, 491)), ((150, 2), (200, 4)), expected_support100_c, 100, 150, expected_bridge_q, expected_bridge_d, (197,), (122,), True, (25, 172, 310, 335, 482), 1, 4),
        CornerImageSupportRow(6, 310, 385, (0, 25, 335), 75, ((100, 6), (150, 500)), ((150, 10), (200, 2), (250, 494)), ((150, 6),), expected_support100_d, 100, 150, expected_bridge_q, expected_bridge_d, (310,), (385,), True, (25, 172, 197, 335, 482), 5, 0),
    )
    row_ok = (
        profile.row_count == 4
        and profile.kernel_order == 25
        and profile.forced_corner_raw_support == 75
        and profile.recorded_first_boundary_raw_support == 100
        and profile.bridge_raw_support == 150
        and profile.bridge_q_items == expected_bridge_q
        and profile.bridge_d_items == expected_bridge_d
        and profile.all_rows_have_ladder_75_100_150
        and profile.all_rows_have_unique_recorded_bridge_hit
        and profile.all_support100_sets_are_pair_difference_sixpacks
        and profile.support150_image_is_not_sufficient
        and profile.rows == expected_rows
    )

    print(
        "corner_image_support_summary: "
        f"kernel_order={profile.kernel_order} "
        f"forced_corner_raw_support={profile.forced_corner_raw_support} "
        f"recorded_first_boundary_raw_support={profile.recorded_first_boundary_raw_support} "
        f"bridge_raw_support={profile.bridge_raw_support} "
        f"bridge_hit_q_directions={tuple(row.bridge_hit_directions for row in profile.rows)}"
    )
    print("corner_image_support_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("support_laws")
    print("  recorded K-traced source chain has raw support 75")
    print("  recorded first boundary cancels one K orbit and has raw support 100")
    print("  recorded inversion image is the signed bridge and has raw support 150")
    print("  some wrong support-100 first boundaries also have support-150 images")
    print("interpretation")
    print("  support_ladder_75_100_150_is_necessary_for_the_bridge_source_chain=1")
    print("  support_150_image_size_alone_is_not_a_bridge_certificate=1")
    print("  producer_must_match_the_recorded_half_boundary_image_not_only_the_support_counts=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_image_support_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_image_support_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
