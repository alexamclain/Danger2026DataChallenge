#!/usr/bin/env python3
"""Fixed-point half-potential selector for p25 Hilbert-90 corners.

The S-layer image gate selects the signed bridge image as two complete
S-orbits.  This gate records the immediately preceding four-block potential.
For each active source-chain corner, the recorded half-boundary is the unique
first boundary that is a fixed-point half-potential: it contains the q=0 fixed
block and exactly one representative from each of the three bridge inversion
pairs.

This is a structural selector between "support-four first boundary" and
"signed bridge image".  The producer must recover the fixed q=0 repair and the
orientation choice on each inversion pair, not merely any sparse first
boundary whose inversion has six points.
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
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_gate import (
    signed_s_layer_decomposition,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Items = tuple[tuple[int, int], ...]
OrbitDecomposition = tuple[tuple[tuple[int, ...], int], ...]


@dataclass(frozen=True)
class HalfPotentialRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    chain_q_values: tuple[int, ...]
    support4_first_boundary_directions_q: tuple[int, ...]
    support4_first_boundary_directions_d: tuple[int, ...]
    half_potential_directions_q: tuple[int, ...]
    half_potential_directions_d: tuple[int, ...]
    half_potential: Items
    fixed_q0_coefficient: int
    selected_pair_representatives: tuple[int, ...]
    inversion_image: Items
    s_layer_decomposition: OrbitDecomposition
    wrong_support4_first_boundary_count: int
    wrong_support4_half_potential_count: int


@dataclass(frozen=True)
class HalfPotentialProfile:
    row_count: int
    bridge_pairs: tuple[tuple[int, int], ...]
    bridge_image: Items
    bridge_s_layer_decomposition: OrbitDecomposition
    support4_direction_count_values: tuple[int, ...]
    all_rows_have_unique_recorded_half_potential: bool
    all_half_potentials_invert_to_bridge: bool
    support4_first_boundary_is_not_sufficient: bool
    rows: tuple[HalfPotentialRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


def bridge_pairs() -> tuple[tuple[int, int], ...]:
    bridge = bridge_coefficients()
    return tuple(
        (q_value, (-q_value) % QUOTIENT_ORDER)
        for q_value, coefficient in sorted(bridge.items())
        if coefficient == 1
    )


def half_potential_representatives(poly: dict[int, int], pairs: tuple[tuple[int, int], ...]) -> tuple[int, ...] | None:
    bridge = bridge_coefficients()
    allowed = {0} | {q_value for pair in pairs for q_value in pair}
    if len(poly) != 4 or set(poly) - allowed:
        return None
    if poly.get(0) not in (-1, 1):
        return None

    representatives: list[int] = []
    for pair in pairs:
        present = tuple(q_value for q_value in pair if q_value in poly)
        if len(present) != 1:
            return None
        selected = present[0]
        if poly[selected] != bridge[selected]:
            return None
        representatives.append(selected)
    return tuple(representatives)


def scan_row(row, pairs: tuple[tuple[int, int], ...]) -> HalfPotentialRow:
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    support4_directions: list[int] = []
    half_potential_directions: list[int] = []
    half_potential_by_direction: dict[int, dict[int, int]] = {}
    representatives_by_direction: dict[int, tuple[int, ...]] = {}

    for direction in range(1, QUOTIENT_ORDER):
        first = boundary(chain, direction)
        if len(first) == 4:
            support4_directions.append(direction)
        representatives = half_potential_representatives(first, pairs)
        if representatives is not None:
            half_potential_directions.append(direction)
            half_potential_by_direction[direction] = first
            representatives_by_direction[direction] = representatives

    if len(half_potential_directions) != 1:
        raise AssertionError(f"expected one half-potential direction, got {half_potential_directions}")
    half_direction = half_potential_directions[0]
    half_potential = half_potential_by_direction[half_direction]
    image = inversion_boundary(half_potential)
    return HalfPotentialRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.boundary_direction_q,
        recorded_direction_d=d_residue_from_q(row.boundary_direction_q),
        chain_q_values=row.q_values,
        support4_first_boundary_directions_q=tuple(support4_directions),
        support4_first_boundary_directions_d=tuple(
            d_residue_from_q(direction) for direction in support4_directions
        ),
        half_potential_directions_q=tuple(half_potential_directions),
        half_potential_directions_d=tuple(
            d_residue_from_q(direction) for direction in half_potential_directions
        ),
        half_potential=as_items(half_potential),
        fixed_q0_coefficient=half_potential[0],
        selected_pair_representatives=representatives_by_direction[half_direction],
        inversion_image=as_items(image),
        s_layer_decomposition=signed_s_layer_decomposition(image),
        wrong_support4_first_boundary_count=len(support4_directions) - 1,
        wrong_support4_half_potential_count=sum(
            direction != half_direction
            and half_potential_representatives(boundary(chain, direction), pairs) is not None
            for direction in support4_directions
        ),
    )


def half_potential_profile() -> HalfPotentialProfile:
    pairs = bridge_pairs()
    bridge = bridge_coefficients()
    bridge_decomposition = signed_s_layer_decomposition(bridge)
    rows = tuple(scan_row(row, pairs) for row in coefficient_rigidity_profile().rows)
    return HalfPotentialProfile(
        row_count=len(rows),
        bridge_pairs=pairs,
        bridge_image=as_items(bridge),
        bridge_s_layer_decomposition=bridge_decomposition,
        support4_direction_count_values=tuple(sorted({len(row.support4_first_boundary_directions_q) for row in rows})),
        all_rows_have_unique_recorded_half_potential=all(
            row.half_potential_directions_q == (row.recorded_direction_q,)
            and row.half_potential_directions_d == (row.recorded_direction_d,)
            for row in rows
        ),
        all_half_potentials_invert_to_bridge=all(
            row.inversion_image == as_items(bridge)
            and row.s_layer_decomposition == bridge_decomposition
            for row in rows
        ),
        support4_first_boundary_is_not_sufficient=all(
            row.wrong_support4_first_boundary_count > 0
            and row.wrong_support4_half_potential_count == 0
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner half-potential gate")
    profile = half_potential_profile()
    expected_bridge = ((25, 1), (138, -1), (197, 1), (310, -1), (369, 1), (482, -1))
    expected_decomposition = (((25, 197, 369), 1), ((138, 310, 482), -1))
    expected_support4 = (25, 172, 197, 310, 335, 482)
    expected_support4_d = (121, 1, 122, 385, 506, 386)
    expected_rows = (
        HalfPotentialRow(1, 197, 122, (0, 172, 482), expected_support4, expected_support4_d, (197,), (122,), ((0, -1), (197, 1), (369, 1), (482, -1)), -1, (482, 197, 369), expected_bridge, expected_decomposition, 5, 0),
        HalfPotentialRow(1, 310, 385, (172, 197, 369), expected_support4, expected_support4_d, (310,), (385,), ((0, -1), (197, 1), (369, 1), (482, -1)), -1, (482, 197, 369), expected_bridge, expected_decomposition, 5, 0),
        HalfPotentialRow(6, 197, 122, (138, 310, 335), expected_support4, expected_support4_d, (197,), (122,), ((0, 1), (25, 1), (138, -1), (310, -1)), 1, (25, 310, 138), expected_bridge, expected_decomposition, 5, 0),
        HalfPotentialRow(6, 310, 385, (0, 25, 335), expected_support4, expected_support4_d, (310,), (385,), ((0, 1), (25, 1), (138, -1), (310, -1)), 1, (25, 310, 138), expected_bridge, expected_decomposition, 5, 0),
    )
    row_ok = (
        profile.row_count == 4
        and profile.bridge_pairs == ((25, 482), (197, 310), (369, 138))
        and profile.bridge_image == expected_bridge
        and profile.bridge_s_layer_decomposition == expected_decomposition
        and profile.support4_direction_count_values == (6,)
        and profile.all_rows_have_unique_recorded_half_potential
        and profile.all_half_potentials_invert_to_bridge
        and profile.support4_first_boundary_is_not_sufficient
        and profile.rows == expected_rows
    )

    print(
        "corner_half_potential_summary: "
        f"bridge_pairs={profile.bridge_pairs} "
        f"half_potential_hits={tuple(row.half_potential_directions_q for row in profile.rows)} "
        f"fixed_coefficients={tuple(row.fixed_q0_coefficient for row in profile.rows)}"
    )
    print("corner_half_potential_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("selector_laws")
    print("  every active chain has six support-four first boundaries")
    print("  exactly one support-four first boundary is a fixed-point half-potential")
    print("  the half-potential chooses one representative from each bridge inversion pair plus q=0")
    print("  this unique half-potential inverts to the signed S-layer bridge")
    print("interpretation")
    print("  producer_must_realize_the_q0_fixed_block_and_pair_orientation=1")
    print("  sparse_first_boundary_support_alone_does_not_select_the_Hilbert90_potential=1")
    print("  half_potential_selector_links_the_corner_chain_to_the_signed_S_layer_image=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_half_potential_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_potential_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
