#!/usr/bin/env python3
"""Signed S-layer image selector for p25 Hilbert-90 corners.

The image-support gate showed that support size alone does not certify the
bridge: some wrong first boundaries also have support-150 inversion images.
This gate records the next structural selector.  Among all 506 nonzero
first-boundary directions for each active source-chain corner, the recorded
half-boundary is the unique direction whose inversion image is a signed pair of
complete S-orbits with constant coefficients.

Thus the bridge image is selected as

    + (25, 197, 369) - (138, 310, 482),

not merely as an arbitrary six-point anti-invariant image.
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
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Items = tuple[tuple[int, int], ...]
OrbitDecomposition = tuple[tuple[tuple[int, ...], int], ...]


@dataclass(frozen=True)
class SLayerImageRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    chain_q_values: tuple[int, ...]
    support6_image_directions_q: tuple[int, ...]
    support6_image_directions_d: tuple[int, ...]
    support6_first_boundary_raw_support_distribution: tuple[tuple[int, int], ...]
    signed_s_layer_directions_q: tuple[int, ...]
    signed_s_layer_directions_d: tuple[int, ...]
    signed_s_layer_image: Items
    signed_s_layer_decomposition: OrbitDecomposition
    wrong_support6_image_count: int
    wrong_support6_s_layer_count: int


@dataclass(frozen=True)
class SLayerImageProfile:
    row_count: int
    kernel_order: int
    s_step: int
    bridge_image: Items
    bridge_s_layer_decomposition: OrbitDecomposition
    all_rows_have_unique_recorded_s_layer_image: bool
    all_s_layer_images_are_the_bridge: bool
    support6_image_size_is_not_sufficient: bool
    rows: tuple[SLayerImageRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


def s_orbit(q_value: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                q_value % QUOTIENT_ORDER,
                (q_value + S_STEP) % QUOTIENT_ORDER,
                (q_value + 2 * S_STEP) % QUOTIENT_ORDER,
            }
        )
    )


def signed_s_layer_decomposition(poly: dict[int, int]) -> OrbitDecomposition:
    if len(poly) != 6 or set(poly.values()) != {-1, 1}:
        return ()

    support = set(poly)
    used: set[int] = set()
    rows: list[tuple[tuple[int, ...], int]] = []
    for q_value in sorted(support):
        if q_value in used:
            continue
        orbit = s_orbit(q_value)
        if not set(orbit).issubset(support):
            return ()
        coefficients = {poly[point] for point in orbit}
        if len(coefficients) != 1:
            return ()
        rows.append((orbit, next(iter(coefficients))))
        used.update(orbit)

    if used != support or len(rows) != 2:
        return ()
    if sorted(coefficient for _orbit, coefficient in rows) != [-1, 1]:
        return ()
    return tuple(sorted(rows))


def raw_support_distribution(counter: Counter[int], kernel_order: int) -> tuple[tuple[int, int], ...]:
    return tuple((support * kernel_order, count) for support, count in sorted(counter.items()))


def scan_row(row, kernel_order: int) -> SLayerImageRow:
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    bridge = bridge_coefficients()
    support6_directions: list[int] = []
    signed_s_layer_directions: list[int] = []
    support6_first_supports: Counter[int] = Counter()
    signed_s_layer_images: dict[int, dict[int, int]] = {}
    signed_s_layer_decompositions: dict[int, OrbitDecomposition] = {}

    for direction in range(1, QUOTIENT_ORDER):
        first = boundary(chain, direction)
        image = inversion_boundary(first)
        if len(image) == 6:
            support6_directions.append(direction)
            support6_first_supports[len(first)] += 1
        decomposition = signed_s_layer_decomposition(image)
        if decomposition:
            signed_s_layer_directions.append(direction)
            signed_s_layer_images[direction] = image
            signed_s_layer_decompositions[direction] = decomposition

    if len(signed_s_layer_directions) != 1:
        raise AssertionError(f"expected one signed S-layer image, got {signed_s_layer_directions}")
    signed_direction = signed_s_layer_directions[0]
    if signed_s_layer_images[signed_direction] != bridge:
        raise AssertionError("signed S-layer image did not equal the bridge")

    return SLayerImageRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.boundary_direction_q,
        recorded_direction_d=d_residue_from_q(row.boundary_direction_q),
        chain_q_values=row.q_values,
        support6_image_directions_q=tuple(support6_directions),
        support6_image_directions_d=tuple(d_residue_from_q(direction) for direction in support6_directions),
        support6_first_boundary_raw_support_distribution=raw_support_distribution(
            support6_first_supports,
            kernel_order,
        ),
        signed_s_layer_directions_q=tuple(signed_s_layer_directions),
        signed_s_layer_directions_d=tuple(
            d_residue_from_q(direction) for direction in signed_s_layer_directions
        ),
        signed_s_layer_image=as_items(signed_s_layer_images[signed_direction]),
        signed_s_layer_decomposition=signed_s_layer_decompositions[signed_direction],
        wrong_support6_image_count=len(support6_directions) - 1,
        wrong_support6_s_layer_count=sum(
            1 for direction in support6_directions
            if direction != signed_direction
            and signed_s_layer_decomposition(inversion_boundary(boundary(chain, direction)))
        ),
    )


def s_layer_image_profile() -> SLayerImageProfile:
    kernel_order = k_trace_minimality_profile().kernel_order
    bridge = bridge_coefficients()
    rows = tuple(scan_row(row, kernel_order) for row in coefficient_rigidity_profile().rows)
    bridge_decomposition = signed_s_layer_decomposition(bridge)
    return SLayerImageProfile(
        row_count=len(rows),
        kernel_order=kernel_order,
        s_step=S_STEP,
        bridge_image=as_items(bridge),
        bridge_s_layer_decomposition=bridge_decomposition,
        all_rows_have_unique_recorded_s_layer_image=all(
            row.signed_s_layer_directions_q == (row.recorded_direction_q,)
            and row.signed_s_layer_directions_d == (row.recorded_direction_d,)
            for row in rows
        ),
        all_s_layer_images_are_the_bridge=all(
            row.signed_s_layer_image == as_items(bridge)
            and row.signed_s_layer_decomposition == bridge_decomposition
            for row in rows
        ),
        support6_image_size_is_not_sufficient=all(
            row.wrong_support6_image_count > 0
            and row.wrong_support6_s_layer_count == 0
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner S-layer image gate")
    profile = s_layer_image_profile()
    expected_bridge = ((25, 1), (138, -1), (197, 1), (310, -1), (369, 1), (482, -1))
    expected_decomposition = (((25, 197, 369), 1), ((138, 310, 482), -1))
    expected_rows = (
        SLayerImageRow(1, 197, 122, (0, 172, 482), (25, 172, 180, 197, 266, 310, 335, 360, 421, 482), (121, 1, 60, 122, 314, 385, 506, 120, 253, 386), ((100, 6), (150, 4)), (197,), (122,), expected_bridge, expected_decomposition, 9, 0),
        SLayerImageRow(1, 310, 385, (172, 197, 369), (138, 310, 335), (384, 385, 506), ((100, 2), (150, 1)), (310,), (385,), expected_bridge, expected_decomposition, 2, 0),
        SLayerImageRow(6, 197, 122, (138, 310, 335), (172, 197, 369), (1, 122, 123), ((100, 2), (150, 1)), (197,), (122,), expected_bridge, expected_decomposition, 2, 0),
        SLayerImageRow(6, 310, 385, (0, 25, 335), (25, 86, 147, 172, 197, 241, 310, 327, 335, 482), (121, 254, 387, 1, 122, 193, 385, 447, 506, 386), ((100, 6), (150, 4)), (310,), (385,), expected_bridge, expected_decomposition, 9, 0),
    )
    row_ok = (
        profile.row_count == 4
        and profile.kernel_order == 25
        and profile.s_step == 172
        and profile.bridge_image == expected_bridge
        and profile.bridge_s_layer_decomposition == expected_decomposition
        and profile.all_rows_have_unique_recorded_s_layer_image
        and profile.all_s_layer_images_are_the_bridge
        and profile.support6_image_size_is_not_sufficient
        and profile.rows == expected_rows
    )

    print(
        "corner_s_layer_image_summary: "
        f"s_step={profile.s_step} "
        f"bridge_decomposition={profile.bridge_s_layer_decomposition} "
        f"signed_s_layer_hit_q={tuple(row.signed_s_layer_directions_q for row in profile.rows)} "
        f"support6_counts={tuple(len(row.support6_image_directions_q) for row in profile.rows)}"
    )
    print("corner_s_layer_image_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("selector_laws")
    print("  support-six inversion images are not enough to identify the bridge")
    print("  the recorded half-boundary is the unique direction with a signed pair of full S-orbits")
    print("  the selected image is +(25,197,369) -(138,310,482)")
    print("interpretation")
    print("  producer_must_realize_the_signed_S_layer_pair_not_only_a_six_point_image=1")
    print("  wrong_sparse_images_fail_the_constant_S_orbit_selector=1")
    print("  bridge_image_selector_is_now_structural_between_support_and_full_equality=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
