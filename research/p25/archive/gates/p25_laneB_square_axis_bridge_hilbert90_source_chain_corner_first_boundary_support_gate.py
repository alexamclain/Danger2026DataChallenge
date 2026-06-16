#!/usr/bin/env python3
"""First-boundary support law for K-traced p25 Hilbert-90 corners.

The K-trace minimality gate forces each active three-point quotient corner to
lift to three full K orbits, raw support 75.  This gate records the next support
step: after applying a nonzero first boundary to that K-invariant lift, the raw
support is at least 100.  Exactly the six pair-difference directions achieve
that minimum by cancelling one whole K orbit; all other directions have raw
support 150.

Among the six support-100 boundaries, only the recorded half-boundary direction
197 or 310 gives the bridge after inversion.
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
class FirstBoundarySupportRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_q_values: tuple[int, ...]
    chain_d_values: tuple[int, ...]
    chain_raw_support: int
    quotient_support_distribution: tuple[tuple[int, int], ...]
    raw_support_distribution: tuple[tuple[int, int], ...]
    minimal_raw_support: int
    minimal_directions: tuple[int, ...]
    cancellation_q_values_for_minimal_directions: tuple[int, ...]
    cancellation_d_values_for_minimal_directions: tuple[int, ...]
    recorded_cancellation_q: int
    recorded_cancellation_d: int
    recorded_first_boundary: Items
    recorded_first_boundary_d: Items
    recorded_raw_support: int
    recorded_raw_degree: int
    bridge_hit_directions: tuple[int, ...]
    wrong_minimal_directions: tuple[int, ...]


@dataclass(frozen=True)
class FirstBoundarySupportProfile:
    row_count: int
    kernel_order: int
    forced_chain_raw_support: int
    minimum_first_boundary_raw_support: int
    universal_raw_support_distribution: tuple[tuple[int, int], ...]
    universal_minimal_directions: tuple[int, ...]
    all_rows_have_forced_chain_support: bool
    all_rows_have_minimum_support_100: bool
    all_minimal_directions_are_pair_differences: bool
    all_recorded_boundaries_are_support_100_degree_zero: bool
    all_recorded_directions_unique_bridge_hits: bool
    rows: tuple[FirstBoundarySupportRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


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


def overlap_for_direction(q_values: tuple[int, ...], direction: int) -> tuple[int, ...]:
    shifted = {(q_value + direction) % QUOTIENT_ORDER for q_value in q_values}
    return tuple(sorted(set(q_values) & shifted))


def scan_row(row) -> FirstBoundarySupportRow:
    kernel_order = k_trace_minimality_profile().kernel_order
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    bridge = bridge_coefficients()
    quotient_counter: Counter[int] = Counter()
    bridge_hits: list[int] = []
    minimal_directions: list[int] = []
    cancellation_q_values: list[int] = []
    cancellation_d_values: list[int] = []
    first_boundary_by_direction: dict[int, dict[int, int]] = {}

    for direction in range(1, QUOTIENT_ORDER):
        first_boundary = boundary(chain, direction)
        first_boundary_by_direction[direction] = first_boundary
        quotient_counter[len(first_boundary)] += 1
        if inversion_boundary(first_boundary) == bridge:
            bridge_hits.append(direction)

    minimal_quotient_support = min(quotient_counter)
    for direction, first_boundary in first_boundary_by_direction.items():
        if len(first_boundary) != minimal_quotient_support:
            continue
        minimal_directions.append(direction)
        overlap = overlap_for_direction(row.q_values, direction)
        if len(overlap) != 1:
            raise AssertionError(f"expected one cancellation point, got {overlap}")
        cancellation_q_values.append(overlap[0])
        cancellation_d_values.append(d_residue_from_q(overlap[0]))

    recorded = first_boundary_by_direction[row.boundary_direction_q]
    recorded_overlap = overlap_for_direction(row.q_values, row.boundary_direction_q)
    if len(recorded_overlap) != 1:
        raise AssertionError(f"recorded boundary expected one cancellation, got {recorded_overlap}")
    return FirstBoundarySupportRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.boundary_direction_q,
        chain_q_values=row.q_values,
        chain_d_values=tuple(d_residue_from_q(q_value) for q_value in row.q_values),
        chain_raw_support=len(chain) * kernel_order,
        quotient_support_distribution=tuple(sorted(quotient_counter.items())),
        raw_support_distribution=tuple(
            (quotient_support * kernel_order, count)
            for quotient_support, count in sorted(quotient_counter.items())
        ),
        minimal_raw_support=minimal_quotient_support * kernel_order,
        minimal_directions=tuple(minimal_directions),
        cancellation_q_values_for_minimal_directions=tuple(cancellation_q_values),
        cancellation_d_values_for_minimal_directions=tuple(cancellation_d_values),
        recorded_cancellation_q=recorded_overlap[0],
        recorded_cancellation_d=d_residue_from_q(recorded_overlap[0]),
        recorded_first_boundary=as_items(recorded),
        recorded_first_boundary_d=tuple(
            sorted((d_residue_from_q(q_value), coefficient) for q_value, coefficient in recorded.items())
        ),
        recorded_raw_support=len(recorded) * kernel_order,
        recorded_raw_degree=sum(recorded.values()) * kernel_order,
        bridge_hit_directions=tuple(bridge_hits),
        wrong_minimal_directions=tuple(
            direction for direction in minimal_directions if direction != row.boundary_direction_q
        ),
    )


def first_boundary_support_profile() -> FirstBoundarySupportProfile:
    minimality = k_trace_minimality_profile()
    rows = tuple(scan_row(row) for row in coefficient_rigidity_profile().rows)
    return FirstBoundarySupportProfile(
        row_count=len(rows),
        kernel_order=minimality.kernel_order,
        forced_chain_raw_support=minimality.unique_k_invariant_corner_support,
        minimum_first_boundary_raw_support=100,
        universal_raw_support_distribution=rows[0].raw_support_distribution,
        universal_minimal_directions=rows[0].minimal_directions,
        all_rows_have_forced_chain_support=all(
            row.chain_raw_support == minimality.unique_k_invariant_corner_support for row in rows
        ),
        all_rows_have_minimum_support_100=all(row.minimal_raw_support == 100 for row in rows),
        all_minimal_directions_are_pair_differences=all(
            row.minimal_directions == pair_difference_directions(row.chain_q_values) for row in rows
        ),
        all_recorded_boundaries_are_support_100_degree_zero=all(
            row.recorded_raw_support == 100 and row.recorded_raw_degree == 0 for row in rows
        ),
        all_recorded_directions_unique_bridge_hits=all(
            row.bridge_hit_directions == (row.recorded_direction_q,) for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner first-boundary-support gate")
    profile = first_boundary_support_profile()
    expected_rows = (
        FirstBoundarySupportRow(1, 197, (0, 172, 482), (0, 1, 386), 75, ((4, 6), (6, 500)), ((100, 6), (150, 500)), 100, (25, 172, 197, 310, 335, 482), (0, 172, 172, 482, 0, 482), (0, 1, 1, 386, 0, 386), 172, 1, ((0, -1), (197, 1), (369, 1), (482, -1)), ((0, -1), (122, 1), (123, 1), (386, -1)), 100, 0, (197,), (25, 172, 310, 335, 482)),
        FirstBoundarySupportRow(1, 310, (172, 197, 369), (1, 122, 123), 75, ((4, 6), (6, 500)), ((100, 6), (150, 500)), 100, (25, 172, 197, 310, 335, 482), (197, 369, 369, 172, 197, 172), (122, 123, 123, 1, 122, 1), 172, 1, ((0, -1), (197, 1), (369, 1), (482, -1)), ((0, -1), (122, 1), (123, 1), (386, -1)), 100, 0, (310,), (25, 172, 197, 335, 482)),
        FirstBoundarySupportRow(6, 197, (138, 310, 335), (384, 385, 506), 75, ((4, 6), (6, 500)), ((100, 6), (150, 500)), 100, (25, 172, 197, 310, 335, 482), (335, 310, 335, 138, 138, 310), (506, 385, 506, 384, 384, 385), 335, 506, ((0, 1), (25, 1), (138, -1), (310, -1)), ((0, 1), (121, 1), (384, -1), (385, -1)), 100, 0, (197,), (25, 172, 310, 335, 482)),
        FirstBoundarySupportRow(6, 310, (0, 25, 335), (0, 121, 506), 75, ((4, 6), (6, 500)), ((100, 6), (150, 500)), 100, (25, 172, 197, 310, 335, 482), (25, 0, 25, 335, 335, 0), (121, 0, 121, 506, 506, 0), 335, 506, ((0, 1), (25, 1), (138, -1), (310, -1)), ((0, 1), (121, 1), (384, -1), (385, -1)), 100, 0, (310,), (25, 172, 197, 335, 482)),
    )
    row_ok = (
        profile.row_count == 4
        and profile.kernel_order == 25
        and profile.forced_chain_raw_support == 75
        and profile.minimum_first_boundary_raw_support == 100
        and profile.universal_raw_support_distribution == ((100, 6), (150, 500))
        and profile.universal_minimal_directions == (25, 172, 197, 310, 335, 482)
        and profile.all_rows_have_forced_chain_support
        and profile.all_rows_have_minimum_support_100
        and profile.all_minimal_directions_are_pair_differences
        and profile.all_recorded_boundaries_are_support_100_degree_zero
        and profile.all_recorded_directions_unique_bridge_hits
        and profile.rows == expected_rows
    )

    print(
        "corner_first_boundary_support_summary: "
        f"forced_chain_raw_support={profile.forced_chain_raw_support} "
        f"minimum_first_boundary_raw_support={profile.minimum_first_boundary_raw_support} "
        f"raw_support_distribution={profile.universal_raw_support_distribution} "
        f"minimal_directions={profile.universal_minimal_directions}"
    )
    print("corner_first_boundary_support_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("support_laws")
    print("  K-traced active corners have forced raw support 75")
    print("  every nonzero first boundary has raw support at least 100")
    print("  support 100 occurs exactly for the six pair-difference directions")
    print("  only the recorded half-boundary direction gives the bridge after inversion")
    print("interpretation")
    print("  first_boundary_support_100_is_forced_by_one_K_orbit_cancellation=1")
    print("  producer_must_realize_the_recorded_half_boundary_not_only_any_sparse_boundary=1")
    print("  the_support_ladder_75_to_100_is_now_explicit_on_K_orbits=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_first_boundary_support_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_first_boundary_support_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
