#!/usr/bin/env python3
"""First-boundary screen for p25 Hilbert-90 source targets.

The minimal source-edge gate reduced the bridge-compatible Hilbert-90 target
to a four-block source function on C_3 x C_169.  This gate asks the next
producer-facing question: is that four-block potential itself a sparse
first boundary in some source direction?

The answer is a useful positive.  The bridge-zero-compatible masks 1 and 6
are optimal support-3 first boundaries in the primitive quotient/source
directions q=197 and q=310.  The other row-balanced orbit, masks 2 and 5,
does not share this compression: its best first-boundary antiderivative has
support 14.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate import (
    MinimalPotential,
    minimal_potential_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_minimal_potential_structure_gate import (
    structure_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


MODULUS = 2029
Poly = dict[int, int]


@dataclass(frozen=True)
class BoundaryWitness:
    direction_q: int
    direction_coord: tuple[int, int]
    support: int
    nonzero_cycle_count: int
    max_cycle_support: int
    antiderivative: tuple[tuple[int, int], ...]
    antiderivative_coords: tuple[tuple[tuple[int, int], int], ...]


@dataclass(frozen=True)
class PotentialBoundaryRow:
    orientation_mask: int
    trace_values: tuple[tuple[int, int], ...]
    row_balanced: bool
    bridge_zero_compatible: bool
    possible_direction_count: int
    minimal_antiderivative_support: int
    best_directions: tuple[int, ...]
    best_direction_coords: tuple[tuple[int, int], ...]
    best_witnesses: tuple[BoundaryWitness, ...]
    bridge_double_boundary_ok: bool


@dataclass(frozen=True)
class SourceBoundaryProfile:
    best_support_by_mask: tuple[tuple[int, int], ...]
    possible_direction_count_by_mask: tuple[tuple[int, int], ...]
    best_directions_by_mask: tuple[tuple[int, tuple[int, ...]], ...]
    bridge_zero_compatible_masks: tuple[int, ...]
    row_balanced_masks: tuple[int, ...]
    bridge_best_support: int
    bridge_best_directions: tuple[int, ...]
    extra_zero_row_balanced_best_support: int
    all_bridge_best_directions_are_primitive: bool
    all_bridge_targets_are_optimal_three_point_boundaries: bool
    extra_zero_orbit_has_no_three_point_boundary: bool
    bridge_double_boundary_hits: int
    rows: tuple[PotentialBoundaryRow, ...]


def coord_from_q(q_value: int) -> tuple[int, int]:
    return (q_value % RIGHT_DEGREE, q_value % SQUARE_C)


def normalize(poly: Poly) -> Poly:
    return {q_value: value for q_value, value in sorted(poly.items()) if value}


def boundary(poly: Poly, direction: int) -> Poly:
    return normalize(
        {
            q_value: poly.get(q_value, 0) - poly.get((q_value - direction) % QUOTIENT_ORDER, 0)
            for q_value in range(QUOTIENT_ORDER)
        }
    )


def inversion_boundary(poly: Poly) -> Poly:
    return normalize(
        {
            q_value: poly.get(q_value, 0) - poly.get((-q_value) % QUOTIENT_ORDER, 0)
            for q_value in range(QUOTIENT_ORDER)
        }
    )


def cycle_values(direction: int) -> tuple[tuple[int, ...], ...]:
    cycle_count = gcd(direction, QUOTIENT_ORDER)
    cycles: list[tuple[int, ...]] = []
    for start in range(cycle_count):
        cycle: list[int] = []
        q_value = start
        while True:
            cycle.append(q_value)
            q_value = (q_value + direction) % QUOTIENT_ORDER
            if q_value == start:
                break
        cycles.append(tuple(cycle))
    return tuple(cycles)


def antiderivative_stats(target: Poly, direction: int) -> tuple[int, int, int] | None:
    total_support = 0
    nonzero_cycle_count = 0
    max_cycle_support = 0
    for cycle in cycle_values(direction):
        if sum(target.get(q_value, 0) for q_value in cycle) % MODULUS:
            return None
        prefix_values: list[int] = []
        running = 0
        for index, q_value in enumerate(cycle):
            if index:
                running = (running + target.get(q_value, 0)) % MODULUS
            prefix_values.append(running)
        zeroable_count = Counter(prefix_values).most_common(1)[0][1]
        cycle_support = len(cycle) - zeroable_count
        total_support += cycle_support
        if cycle_support:
            nonzero_cycle_count += 1
            max_cycle_support = max(max_cycle_support, cycle_support)
    return total_support, nonzero_cycle_count, max_cycle_support


def signed_mod(value: int) -> int:
    value %= MODULUS
    return value if value <= MODULUS // 2 else value - MODULUS


def minimal_antiderivative(target: Poly, direction: int) -> Poly:
    out: Poly = {}
    for cycle in cycle_values(direction):
        prefix_values: list[int] = []
        running = 0
        for index, q_value in enumerate(cycle):
            if index:
                running = (running + target.get(q_value, 0)) % MODULUS
            prefix_values.append(running)
        most_common_value = Counter(prefix_values).most_common(1)[0][0]
        for q_value, prefix in zip(cycle, prefix_values):
            coefficient = signed_mod(prefix - most_common_value)
            if coefficient:
                out[q_value] = coefficient
    return normalize(out)


def row_balanced(row: MinimalPotential) -> bool:
    return tuple(
        sum(value for q_value, value in row.trace_values if q_value % RIGHT_DEGREE == right)
        for right in range(RIGHT_DEGREE)
    ) == (0, 0, 0)


def scan_row(
    row: MinimalPotential,
    bridge_zero_compatible: bool,
) -> PotentialBoundaryRow:
    target = dict(row.trace_values)
    scan: list[tuple[int, int, int, int]] = []
    for direction in range(1, QUOTIENT_ORDER):
        stats = antiderivative_stats(target, direction)
        if stats is None:
            continue
        support, nonzero_cycle_count, max_cycle_support = stats
        scan.append((support, nonzero_cycle_count, max_cycle_support, direction))

    scan.sort()
    minimal_support = scan[0][0]
    best = tuple(row for row in scan if row[0] == minimal_support)
    witnesses = tuple(
        BoundaryWitness(
            direction_q=direction,
            direction_coord=coord_from_q(direction),
            support=support,
            nonzero_cycle_count=nonzero_cycle_count,
            max_cycle_support=max_cycle_support,
            antiderivative=tuple(minimal_antiderivative(target, direction).items()),
            antiderivative_coords=tuple(
                (coord_from_q(q_value), coefficient)
                for q_value, coefficient in minimal_antiderivative(target, direction).items()
            ),
        )
        for support, nonzero_cycle_count, max_cycle_support, direction in best
    )
    double_boundary_ok = any(
        inversion_boundary(boundary(dict(witness.antiderivative), witness.direction_q))
        == bridge_coefficients()
        for witness in witnesses
    )
    return PotentialBoundaryRow(
        orientation_mask=row.orientation_mask,
        trace_values=row.trace_values,
        row_balanced=row_balanced(row),
        bridge_zero_compatible=bridge_zero_compatible,
        possible_direction_count=len(scan),
        minimal_antiderivative_support=minimal_support,
        best_directions=tuple(witness.direction_q for witness in witnesses),
        best_direction_coords=tuple(witness.direction_coord for witness in witnesses),
        best_witnesses=witnesses,
        bridge_double_boundary_ok=double_boundary_ok,
    )


def source_boundary_profile() -> SourceBoundaryProfile:
    structures = structure_profile()
    zero_match_masks = set(structures.bridge_zero_match_masks)
    minimal = minimal_potential_profile()
    rows = tuple(
        scan_row(row, bridge_zero_compatible=row.orientation_mask in zero_match_masks)
        for row in minimal.potentials
    )
    bridge_rows = tuple(row for row in rows if row.bridge_zero_compatible)
    extra_zero_rows = tuple(row for row in rows if row.row_balanced and not row.bridge_zero_compatible)
    bridge_best_directions = tuple(
        sorted({direction for row in bridge_rows for direction in row.best_directions})
    )
    return SourceBoundaryProfile(
        best_support_by_mask=tuple(
            (row.orientation_mask, row.minimal_antiderivative_support) for row in rows
        ),
        possible_direction_count_by_mask=tuple(
            (row.orientation_mask, row.possible_direction_count) for row in rows
        ),
        best_directions_by_mask=tuple(
            (row.orientation_mask, row.best_directions) for row in rows
        ),
        bridge_zero_compatible_masks=tuple(row.orientation_mask for row in bridge_rows),
        row_balanced_masks=tuple(row.orientation_mask for row in rows if row.row_balanced),
        bridge_best_support=min(row.minimal_antiderivative_support for row in bridge_rows),
        bridge_best_directions=bridge_best_directions,
        extra_zero_row_balanced_best_support=min(
            row.minimal_antiderivative_support for row in extra_zero_rows
        ),
        all_bridge_best_directions_are_primitive=all(
            gcd(direction, QUOTIENT_ORDER) == 1 for direction in bridge_best_directions
        ),
        all_bridge_targets_are_optimal_three_point_boundaries=all(
            row.minimal_antiderivative_support == 3
            and row.best_directions == (197, 310)
            for row in bridge_rows
        ),
        extra_zero_orbit_has_no_three_point_boundary=all(
            row.minimal_antiderivative_support > 3 for row in extra_zero_rows
        ),
        bridge_double_boundary_hits=sum(row.bridge_double_boundary_ok for row in bridge_rows),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-boundary gate")
    profile = source_boundary_profile()
    expected_best_support = (
        (0, 23),
        (1, 3),
        (2, 14),
        (3, 3),
        (4, 3),
        (5, 14),
        (6, 3),
        (7, 23),
    )
    expected_possible_counts = (
        (0, 312),
        (1, 468),
        (2, 468),
        (3, 312),
        (4, 312),
        (5, 468),
        (6, 468),
        (7, 312),
    )
    expected_best_directions = (
        (0, (43, 464)),
        (1, (197, 310)),
        (2, (243, 264)),
        (3, (197, 310)),
        (4, (197, 310)),
        (5, (243, 264)),
        (6, (197, 310)),
        (7, (43, 464)),
    )
    expected_bridge_witnesses = {
        (1, 197): ((0, -1), (172, -1), (482, -1)),
        (1, 310): ((172, 1), (197, 1), (369, 1)),
        (6, 197): ((138, -1), (310, -1), (335, -1)),
        (6, 310): ((0, 1), (25, 1), (335, 1)),
    }
    witness_ok = all(
        witness.antiderivative == expected_bridge_witnesses.get((row.orientation_mask, witness.direction_q), witness.antiderivative)
        for row in profile.rows
        if row.orientation_mask in (1, 6)
        for witness in row.best_witnesses
    )
    row_ok = (
        profile.best_support_by_mask == expected_best_support
        and profile.possible_direction_count_by_mask == expected_possible_counts
        and profile.best_directions_by_mask == expected_best_directions
        and profile.bridge_zero_compatible_masks == (1, 6)
        and profile.row_balanced_masks == (1, 2, 5, 6)
        and profile.bridge_best_support == 3
        and profile.bridge_best_directions == (197, 310)
        and profile.extra_zero_row_balanced_best_support == 14
        and profile.all_bridge_best_directions_are_primitive
        and profile.all_bridge_targets_are_optimal_three_point_boundaries
        and profile.extra_zero_orbit_has_no_three_point_boundary
        and profile.bridge_double_boundary_hits == 2
        and witness_ok
    )

    print(
        "source_boundary_summary: "
        f"best_support_by_mask={profile.best_support_by_mask} "
        f"possible_direction_count_by_mask={profile.possible_direction_count_by_mask} "
        f"best_directions_by_mask={profile.best_directions_by_mask}"
    )
    print(
        "bridge_source_boundary_laws: "
        f"bridge_zero_compatible_masks={profile.bridge_zero_compatible_masks} "
        f"row_balanced_masks={profile.row_balanced_masks} "
        f"bridge_best_support={profile.bridge_best_support} "
        f"bridge_best_directions={profile.bridge_best_directions} "
        f"bridge_best_direction_coords={tuple(coord_from_q(direction) for direction in profile.bridge_best_directions)} "
        f"extra_zero_row_balanced_best_support={profile.extra_zero_row_balanced_best_support} "
        f"all_bridge_best_directions_are_primitive={int(profile.all_bridge_best_directions_are_primitive)} "
        f"bridge_double_boundary_hits={profile.bridge_double_boundary_hits}/2"
    )
    print("source_boundary_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("interpretation")
    print("  bridge_compatible_hilbert90_potentials_are_optimal_three_point_first_boundaries=1")
    print("  best_boundary_directions_are_the_opposite_primitive_source_steps_197_and_310=1")
    print("  bridge_is_exactly_inversion_boundary_of_this_three_point_source_boundary=1")
    print("  extra_zero_row_balanced_orbit_has_no_three_point_boundary_compression=1")
    print("  producer_can_target_a_three_point_skew_source_chain_but_must_still_realize_the_nonsplit_hilbert90_ratio=1")
    print(f"square_axis_bridge_hilbert90_source_boundary_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
