#!/usr/bin/env python3
"""Source-edge screen for p25 bridge Hilbert-90 minimal potentials.

The quotient structure gate showed that the four-block Hilbert-90 potentials
do not give a sparse quotient-circulant bridge ratio.  This gate moves those
same eight potentials to the actual square-axis source coordinates
C_3 x C_169:

    q  ->  (q mod 3, q mod 169).

It classifies the source-affine orbits and identifies the only remaining
best-looking orbit.  The bridge-zero-compatible minima are masks 1 and 6; they
are the same source-affine object up to inversion plus sign, and they are
row-balanced rank-two sums of two primitive C_169 row edges with unequal
C-steps 31 and 53.  The other row-balanced orbit, masks 2 and 5, has an extra
primitive Fourier zero and is not bridge-ratio compatible.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate import (
    MinimalPotential,
    minimal_potential_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_minimal_potential_structure_gate import (
    structure_profile,
)
from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import rank_mod
from p25_laneB_square_axis_local_graph_residue_gate import BASE_C, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]
SourceMask = dict[Coord, int]
AffineMap = tuple[int, int, int, int, int]


@dataclass(frozen=True)
class RowEdge:
    row: int
    positive_c: int
    negative_c: int
    positive_to_negative_step: int
    negative_to_positive_step: int
    positive_to_negative_step_mod13: int
    negative_to_positive_step_mod13: int
    primitive_c169_steps: bool


@dataclass(frozen=True)
class SourcePotentialProfile:
    orientation_mask: int
    source_values: tuple[tuple[Coord, int], ...]
    c13_projection: tuple[tuple[Coord, int], ...]
    row_sums: tuple[int, int, int]
    rank_f2: int
    rank_f2029: int
    row_balanced: bool
    row_edge_count: int
    row_edges: tuple[RowEdge, ...]
    row_edge_short_steps: tuple[int, ...]
    row_edge_short_steps_mod13: tuple[int, ...]
    common_c_step: bool
    bridge_zero_compatible: bool
    ratio_possible: bool
    extra_ratio_obstruction_zeros: tuple[int, ...]


@dataclass(frozen=True)
class SourceEdgeProfile:
    affine_equivalence: tuple[tuple[int, tuple[tuple[int, AffineMap], ...]], ...]
    source_affine_orbits: tuple[tuple[int, ...], ...]
    row_balanced_masks: tuple[int, ...]
    rank_two_masks: tuple[int, ...]
    bridge_zero_compatible_masks: tuple[int, ...]
    best_orbit: tuple[int, ...]
    extra_zero_row_balanced_orbit: tuple[int, ...]
    all_unit_row_balanced_are_two_edges: bool
    all_row_edges_are_primitive_c169: bool
    no_row_balanced_minimum_has_common_c_step: bool
    potentials: tuple[SourcePotentialProfile, ...]


def source_mask(row: MinimalPotential) -> SourceMask:
    return {
        (q_value % RIGHT_DEGREE, q_value % SQUARE_C): coefficient
        for q_value, coefficient in row.trace_values
    }


def matrix(mask: SourceMask) -> list[list[int]]:
    return [
        [mask.get((right, c_value), 0) for c_value in range(SQUARE_C)]
        for right in range(RIGHT_DEGREE)
    ]


def c13_projection(mask: SourceMask) -> tuple[tuple[Coord, int], ...]:
    projected: dict[Coord, int] = {}
    for (right, c_value), coefficient in mask.items():
        coord = (right, c_value % BASE_C)
        projected[coord] = projected.get(coord, 0) + coefficient
    return tuple(sorted((coord, value) for coord, value in projected.items() if value))


def row_sums(mask: SourceMask) -> tuple[int, int, int]:
    return tuple(
        sum(value for (row, _c_value), value in mask.items() if row == right)
        for right in range(RIGHT_DEGREE)
    )  # type: ignore[return-value]


def row_edges(mask: SourceMask) -> tuple[RowEdge, ...]:
    by_row: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for (right, c_value), coefficient in mask.items():
        by_row[right].append((c_value, coefficient))

    edges: list[RowEdge] = []
    for right, entries in sorted(by_row.items()):
        if len(entries) != 2 or sum(coefficient for _c_value, coefficient in entries) != 0:
            continue
        positives = [c_value for c_value, coefficient in entries if coefficient == 1]
        negatives = [c_value for c_value, coefficient in entries if coefficient == -1]
        if len(positives) != 1 or len(negatives) != 1:
            continue
        positive = positives[0]
        negative = negatives[0]
        pos_to_neg = (negative - positive) % SQUARE_C
        neg_to_pos = (positive - negative) % SQUARE_C
        edges.append(
            RowEdge(
                row=right,
                positive_c=positive,
                negative_c=negative,
                positive_to_negative_step=pos_to_neg,
                negative_to_positive_step=neg_to_pos,
                positive_to_negative_step_mod13=pos_to_neg % BASE_C,
                negative_to_positive_step_mod13=neg_to_pos % BASE_C,
                primitive_c169_steps=(
                    gcd(pos_to_neg, SQUARE_C) == 1
                    and gcd(neg_to_pos, SQUARE_C) == 1
                ),
            )
        )
    return tuple(edges)


def source_potential_profile(
    row: MinimalPotential,
    bridge_zero_compatible: bool,
    ratio_possible: bool,
    obstruction_zeros: tuple[int, ...],
) -> SourcePotentialProfile:
    mask = source_mask(row)
    mat = matrix(mask)
    edges = row_edges(mask)
    short_steps = tuple(sorted(min(edge.positive_to_negative_step, edge.negative_to_positive_step) for edge in edges))
    short_steps_mod13 = tuple(sorted(step % BASE_C for step in short_steps))
    return SourcePotentialProfile(
        orientation_mask=row.orientation_mask,
        source_values=tuple(sorted(mask.items())),
        c13_projection=c13_projection(mask),
        row_sums=row_sums(mask),
        rank_f2=rank_mod([[value % 2 for value in row_values] for row_values in mat], 2),
        rank_f2029=rank_mod([[value % 2029 for value in row_values] for row_values in mat], 2029),
        row_balanced=row_sums(mask) == (0, 0, 0),
        row_edge_count=len(edges),
        row_edges=edges,
        row_edge_short_steps=short_steps,
        row_edge_short_steps_mod13=short_steps_mod13,
        common_c_step=len({edge.positive_to_negative_step for edge in edges}) <= 1
        or len({edge.negative_to_positive_step for edge in edges}) <= 1,
        bridge_zero_compatible=bridge_zero_compatible,
        ratio_possible=ratio_possible,
        extra_ratio_obstruction_zeros=obstruction_zeros,
    )


def c_units() -> tuple[int, ...]:
    return tuple(value for value in range(1, SQUARE_C) if gcd(value, SQUARE_C) == 1)


def transform(mask: SourceMask, alpha: int, beta: int, unit: int, shift: int, scale: int) -> SourceMask:
    return {
        ((alpha * right + beta) % RIGHT_DEGREE, (unit * c_value + shift) % SQUARE_C): scale * coefficient
        for (right, c_value), coefficient in mask.items()
    }


def affine_equivalence(masks: dict[int, SourceMask]) -> tuple[tuple[int, tuple[tuple[int, AffineMap], ...]], ...]:
    rows: list[tuple[int, tuple[tuple[int, AffineMap], ...]]] = []
    units = c_units()
    for source_index, source in sorted(masks.items()):
        matches: list[tuple[int, AffineMap]] = []
        for target_index, target in sorted(masks.items()):
            found: AffineMap | None = None
            for alpha in (1, 2):
                if found is not None:
                    break
                for beta in range(RIGHT_DEGREE):
                    if found is not None:
                        break
                    for unit in units:
                        if found is not None:
                            break
                        for shift in range(SQUARE_C):
                            for scale in (1, -1):
                                if transform(source, alpha, beta, unit, shift, scale) == target:
                                    found = (alpha, beta, unit, shift, scale)
                                    break
                            if found is not None:
                                break
            if found is not None:
                matches.append((target_index, found))
        rows.append((source_index, tuple(matches)))
    return tuple(rows)


def source_affine_orbits(equivalence: tuple[tuple[int, tuple[tuple[int, AffineMap], ...]], ...]) -> tuple[tuple[int, ...], ...]:
    seen: set[int] = set()
    orbits: list[tuple[int, ...]] = []
    adjacency = {
        source: {target for target, _map in matches}
        for source, matches in equivalence
    }
    for source in sorted(adjacency):
        if source in seen:
            continue
        stack = [source]
        orbit: set[int] = set()
        while stack:
            current = stack.pop()
            if current in orbit:
                continue
            orbit.add(current)
            stack.extend(adjacency[current] - orbit)
        seen.update(orbit)
        orbits.append(tuple(sorted(orbit)))
    return tuple(sorted(orbits))


def source_edge_profile() -> SourceEdgeProfile:
    minimal = minimal_potential_profile()
    structure = structure_profile()
    structure_by_mask = {row.orientation_mask: row for row in structure.structures}
    masks = {row.orientation_mask: source_mask(row) for row in minimal.potentials}
    potentials = tuple(
        source_potential_profile(
            row,
            bridge_zero_compatible=structure_by_mask[row.orientation_mask].fourier_zeros == structure.bridge_zeros,
            ratio_possible=structure_by_mask[row.orientation_mask].bridge_ratio.possible,
            obstruction_zeros=structure_by_mask[row.orientation_mask].bridge_ratio.obstruction_zeros,
        )
        for row in minimal.potentials
    )
    equivalence = affine_equivalence(masks)
    orbits = source_affine_orbits(equivalence)
    row_balanced = tuple(row.orientation_mask for row in potentials if row.row_balanced)
    rank_two = tuple(row.orientation_mask for row in potentials if row.rank_f2029 == 2)
    bridge_zero_compatible = tuple(row.orientation_mask for row in potentials if row.bridge_zero_compatible)
    best_orbit = next(orbit for orbit in orbits if set(orbit) == set(bridge_zero_compatible))
    extra_zero_orbit = next(
        orbit
        for orbit in orbits
        if any(p.extra_ratio_obstruction_zeros for p in potentials if p.orientation_mask in orbit)
    )
    return SourceEdgeProfile(
        affine_equivalence=equivalence,
        source_affine_orbits=orbits,
        row_balanced_masks=row_balanced,
        rank_two_masks=rank_two,
        bridge_zero_compatible_masks=bridge_zero_compatible,
        best_orbit=best_orbit,
        extra_zero_row_balanced_orbit=extra_zero_orbit,
        all_unit_row_balanced_are_two_edges=all(
            row.row_edge_count == 2 and row.row_edge_short_steps == (31, 53)
            for row in potentials
            if row.row_balanced
        ),
        all_row_edges_are_primitive_c169=all(
            edge.primitive_c169_steps
            for row in potentials
            for edge in row.row_edges
        ),
        no_row_balanced_minimum_has_common_c_step=all(
            not row.common_c_step
            for row in potentials
            if row.row_balanced
        ),
        potentials=potentials,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 minimal source-edge gate")
    profile = source_edge_profile()
    expected_equivalence = (
        (0, ((0, (1, 0, 1, 0, 1)), (7, (2, 0, 168, 0, -1)))),
        (1, ((1, (1, 0, 1, 0, 1)), (6, (2, 0, 168, 0, -1)))),
        (2, ((2, (1, 0, 1, 0, 1)), (5, (2, 0, 168, 0, -1)))),
        (3, ((3, (1, 0, 1, 0, 1)), (4, (2, 0, 168, 0, -1)))),
        (4, ((3, (2, 0, 168, 0, -1)), (4, (1, 0, 1, 0, 1)))),
        (5, ((2, (2, 0, 168, 0, -1)), (5, (1, 0, 1, 0, 1)))),
        (6, ((1, (2, 0, 168, 0, -1)), (6, (1, 0, 1, 0, 1)))),
        (7, ((0, (2, 0, 168, 0, -1)), (7, (1, 0, 1, 0, 1)))),
    )
    row_ok = (
        profile.affine_equivalence == expected_equivalence
        and profile.source_affine_orbits == ((0, 7), (1, 6), (2, 5), (3, 4))
        and profile.row_balanced_masks == (1, 2, 5, 6)
        and profile.rank_two_masks == (1, 2, 5, 6)
        and profile.bridge_zero_compatible_masks == (1, 6)
        and profile.best_orbit == (1, 6)
        and profile.extra_zero_row_balanced_orbit == (2, 5)
        and profile.all_unit_row_balanced_are_two_edges
        and profile.all_row_edges_are_primitive_c169
        and profile.no_row_balanced_minimum_has_common_c_step
    )

    print(f"source_affine_orbits={profile.source_affine_orbits}")
    print(f"affine_equivalence={profile.affine_equivalence}")
    print(
        "source_edge_summary: "
        f"row_balanced_masks={profile.row_balanced_masks} "
        f"rank_two_masks={profile.rank_two_masks} "
        f"bridge_zero_compatible_masks={profile.bridge_zero_compatible_masks} "
        f"best_orbit={profile.best_orbit} "
        f"extra_zero_row_balanced_orbit={profile.extra_zero_row_balanced_orbit} "
        f"all_unit_row_balanced_are_two_edges={int(profile.all_unit_row_balanced_are_two_edges)} "
        f"all_row_edges_are_primitive_c169={int(profile.all_row_edges_are_primitive_c169)} "
        f"no_row_balanced_minimum_has_common_c_step={int(profile.no_row_balanced_minimum_has_common_c_step)}"
    )
    print("source_potential_profiles")
    for row in profile.potentials:
        print(f"  {row}")
    print("interpretation")
    print("  eight_minimal_potentials_collapse_to_four_source_affine_orbits_under_inversion_plus_sign=1")
    print("  row_balanced_rank_two_minima_are_exactly_masks_1_2_5_6=1")
    print("  bridge_zero_compatible_source_orbit_is_masks_1_and_6=1")
    print("  extra_zero_row_balanced_source_orbit_is_masks_2_and_5=1")
    print("  best_orbit_is_two_primitive_C169_row_edges_with_short_steps_31_and_53=1")
    print("  no_best_source_edge_target_has_a_common_C_step_or_axis_rectangle=1")
    print("  producer_must_realize_a_two_row_two_primitive_edge_source_function_not_a_single_axis_edge=1")
    print(f"square_axis_bridge_hilbert90_minimal_source_edge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_minimal_source_edge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
