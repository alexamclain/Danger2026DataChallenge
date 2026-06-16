#!/usr/bin/env python3
"""Boundary-rigidity screen for p25 Hilbert-90 source chains.

The curvature gate showed that the Hilbert-90 antiderivative target is a
curved three-point source graph.  This gate asks whether any sparse first
boundary of that chain could replace the recorded source-boundary direction.

It cannot.  Each three-point chain has six support-four first boundaries,
coming exactly from the six pair-difference directions.  Only the recorded
direction, 197 or 310, gives the signed bridge after the inversion boundary.
All other sparse directions and all support-six directions miss the bridge.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    BoundaryWitness,
    PotentialBoundaryRow,
    boundary,
    coord_from_q,
    inversion_boundary,
    source_boundary_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


PolyItems = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ChainBoundaryRigidityRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_coord: tuple[int, int]
    chain: PolyItems
    support_distribution: tuple[tuple[int, int], ...]
    minimal_boundary_support: int
    sparse_directions: tuple[int, ...]
    sparse_direction_coords: tuple[tuple[int, int], ...]
    potential_hit_directions: tuple[int, ...]
    bridge_hit_directions: tuple[int, ...]
    negative_bridge_hit_directions: tuple[int, ...]
    wrong_sparse_directions: tuple[int, ...]
    recorded_first_boundary: PolyItems


@dataclass(frozen=True)
class ChainBoundaryRigidityProfile:
    row_count: int
    universal_support_distribution: tuple[tuple[int, int], ...]
    universal_sparse_directions: tuple[int, ...]
    universal_sparse_direction_coords: tuple[tuple[int, int], ...]
    all_minimal_support_four: bool
    all_sparse_directions_are_pair_differences: bool
    all_recorded_directions_unique_potential_hits: bool
    all_recorded_directions_unique_bridge_hits: bool
    all_wrong_sparse_directions_miss_bridge: bool
    all_support_six_directions_miss_bridge: bool
    rows: tuple[ChainBoundaryRigidityRow, ...]


def negative(poly: dict[int, int]) -> dict[int, int]:
    return {q_value: -coefficient for q_value, coefficient in poly.items()}


def pair_difference_directions(chain: PolyItems) -> tuple[int, ...]:
    q_values = tuple(q_value for q_value, _coefficient in chain)
    directions = {
        (right - left) % QUOTIENT_ORDER
        for left in q_values
        for right in q_values
        if left != right
    }
    return tuple(sorted(directions))


def scan_chain(row: PotentialBoundaryRow, witness: BoundaryWitness) -> ChainBoundaryRigidityRow:
    chain = witness.antiderivative
    chain_poly = dict(chain)
    potential = dict(row.trace_values)
    bridge = bridge_coefficients()
    negative_bridge = negative(bridge)

    support_counter: Counter[int] = Counter()
    sparse_directions: list[int] = []
    potential_hits: list[int] = []
    bridge_hits: list[int] = []
    negative_bridge_hits: list[int] = []
    first_boundary_by_direction: dict[int, PolyItems] = {}

    for direction in range(1, QUOTIENT_ORDER):
        first_boundary = boundary(chain_poly, direction)
        first_boundary_items = tuple(first_boundary.items())
        first_boundary_by_direction[direction] = first_boundary_items
        support_counter[len(first_boundary)] += 1
        if first_boundary == potential:
            potential_hits.append(direction)
        inverted = inversion_boundary(first_boundary)
        if inverted == bridge:
            bridge_hits.append(direction)
        if inverted == negative_bridge:
            negative_bridge_hits.append(direction)

    minimal_support = min(support_counter)
    sparse_directions = [
        direction
        for direction, first_boundary in first_boundary_by_direction.items()
        if len(first_boundary) == minimal_support
    ]
    wrong_sparse_directions = [
        direction for direction in sparse_directions if direction != witness.direction_q
    ]

    return ChainBoundaryRigidityRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=witness.direction_q,
        recorded_direction_coord=witness.direction_coord,
        chain=chain,
        support_distribution=tuple(sorted(support_counter.items())),
        minimal_boundary_support=minimal_support,
        sparse_directions=tuple(sparse_directions),
        sparse_direction_coords=tuple(coord_from_q(direction) for direction in sparse_directions),
        potential_hit_directions=tuple(potential_hits),
        bridge_hit_directions=tuple(bridge_hits),
        negative_bridge_hit_directions=tuple(negative_bridge_hits),
        wrong_sparse_directions=tuple(wrong_sparse_directions),
        recorded_first_boundary=first_boundary_by_direction[witness.direction_q],
    )


def source_chain_boundary_rigidity_profile() -> ChainBoundaryRigidityProfile:
    boundary_profile = source_boundary_profile()
    rows = tuple(
        scan_chain(row, witness)
        for row in boundary_profile.rows
        if row.bridge_zero_compatible
        for witness in row.best_witnesses
    )
    universal_support_distribution = rows[0].support_distribution
    universal_sparse_directions = rows[0].sparse_directions
    universal_sparse_direction_coords = rows[0].sparse_direction_coords
    return ChainBoundaryRigidityProfile(
        row_count=len(rows),
        universal_support_distribution=universal_support_distribution,
        universal_sparse_directions=universal_sparse_directions,
        universal_sparse_direction_coords=universal_sparse_direction_coords,
        all_minimal_support_four=all(row.minimal_boundary_support == 4 for row in rows),
        all_sparse_directions_are_pair_differences=all(
            row.sparse_directions == pair_difference_directions(row.chain) for row in rows
        ),
        all_recorded_directions_unique_potential_hits=all(
            row.potential_hit_directions == (row.recorded_direction_q,) for row in rows
        ),
        all_recorded_directions_unique_bridge_hits=all(
            row.bridge_hit_directions == (row.recorded_direction_q,) for row in rows
        ),
        all_wrong_sparse_directions_miss_bridge=all(
            direction not in row.bridge_hit_directions
            and direction not in row.negative_bridge_hit_directions
            for row in rows
            for direction in row.wrong_sparse_directions
        ),
        all_support_six_directions_miss_bridge=all(
            set(row.bridge_hit_directions) <= set(row.sparse_directions)
            and set(row.negative_bridge_hit_directions) <= set(row.sparse_directions)
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain boundary-rigidity gate")
    profile = source_chain_boundary_rigidity_profile()
    expected_rows = (
        ChainBoundaryRigidityRow(1, 197, (2, 28), ((0, -1), (172, -1), (482, -1)), ((4, 6), (6, 500)), 4, (25, 172, 197, 310, 335, 482), ((1, 25), (1, 3), (2, 28), (1, 141), (2, 166), (2, 144)), (197,), (197,), (), (25, 172, 310, 335, 482), ((0, -1), (197, 1), (369, 1), (482, -1))),
        ChainBoundaryRigidityRow(1, 310, (1, 141), ((172, 1), (197, 1), (369, 1)), ((4, 6), (6, 500)), 4, (25, 172, 197, 310, 335, 482), ((1, 25), (1, 3), (2, 28), (1, 141), (2, 166), (2, 144)), (310,), (310,), (), (25, 172, 197, 335, 482), ((0, -1), (197, 1), (369, 1), (482, -1))),
        ChainBoundaryRigidityRow(6, 197, (2, 28), ((138, -1), (310, -1), (335, -1)), ((4, 6), (6, 500)), 4, (25, 172, 197, 310, 335, 482), ((1, 25), (1, 3), (2, 28), (1, 141), (2, 166), (2, 144)), (197,), (197,), (), (25, 172, 310, 335, 482), ((0, 1), (25, 1), (138, -1), (310, -1))),
        ChainBoundaryRigidityRow(6, 310, (1, 141), ((0, 1), (25, 1), (335, 1)), ((4, 6), (6, 500)), 4, (25, 172, 197, 310, 335, 482), ((1, 25), (1, 3), (2, 28), (1, 141), (2, 166), (2, 144)), (310,), (310,), (), (25, 172, 197, 335, 482), ((0, 1), (25, 1), (138, -1), (310, -1))),
    )
    row_ok = (
        profile.row_count == 4
        and profile.universal_support_distribution == ((4, 6), (6, 500))
        and profile.universal_sparse_directions == (25, 172, 197, 310, 335, 482)
        and profile.universal_sparse_direction_coords == (
            (1, 25),
            (1, 3),
            (2, 28),
            (1, 141),
            (2, 166),
            (2, 144),
        )
        and profile.all_minimal_support_four
        and profile.all_sparse_directions_are_pair_differences
        and profile.all_recorded_directions_unique_potential_hits
        and profile.all_recorded_directions_unique_bridge_hits
        and profile.all_wrong_sparse_directions_miss_bridge
        and profile.all_support_six_directions_miss_bridge
        and profile.rows == expected_rows
    )

    print(
        "source_chain_boundary_rigidity_summary: "
        f"row_count={profile.row_count} "
        f"support_distribution={profile.universal_support_distribution} "
        f"sparse_directions={profile.universal_sparse_directions} "
        f"sparse_direction_coords={profile.universal_sparse_direction_coords}"
    )
    print("source_chain_boundary_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("interpretation")
    print("  each_curved_chain_has_exactly_six_sparse_first_boundaries=1")
    print("  sparse_first_boundaries_are_exactly_pair_difference_directions=1")
    print("  only_the_recorded_197_or_310_direction_recovers_the_four_block_potential=1")
    print("  only_the_recorded_197_or_310_direction_recovers_the_signed_bridge_after_inversion=1")
    print("  producer_cannot_replace_the_curved_chain_orientation_by_D_endpoint_or_other_sparse_boundary=1")
    print(f"square_axis_bridge_hilbert90_source_chain_boundary_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_boundary_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
