#!/usr/bin/env python3
"""Projective-shape screen for p25 Hilbert-90 source chains.

The curvature and boundary-rigidity gates identify a curved three-point source
graph with a rigid first-boundary orientation.  This gate records the
projective shape of that graph: the cyclic first-difference triple modulo the
product-affine source action.

The C_13 shadow still does not select the C_169 object.  Among primitive
C_169 projective difference shapes, the canonical C_13 shadow has thirteen
distinct lifts.  A producer must realize the specific nonsplit C_169 lift, not
only the mod-13 projective shape.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from math import gcd

from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    source_boundary_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


DiffTriple = tuple[int, int, int]


@dataclass(frozen=True)
class ChainShapeRow:
    orientation_mask: int
    boundary_direction_q: int
    q_values: tuple[int, ...]
    row_values_c169: tuple[int, int, int]
    row_values_c13: tuple[int, int, int]
    cyclic_differences_c169: DiffTriple
    cyclic_differences_c13: DiffTriple
    projective_shape_c169: DiffTriple
    projective_shape_c13: DiffTriple


@dataclass(frozen=True)
class ProjectiveShapeProfile:
    rows: tuple[ChainShapeRow, ...]
    canonical_projective_shape_c169: DiffTriple
    canonical_projective_shape_c13: DiffTriple
    c169_orbit_size: int
    c13_orbit_size: int
    c169_projective_stabilizer_size: int
    c13_projective_stabilizer_size: int
    primitive_c169_projective_shape_count: int
    c13_shadow_distribution: tuple[tuple[DiffTriple, int], ...]
    canonical_c13_lift_count: int
    canonical_c13_lifts: tuple[DiffTriple, ...]
    all_rows_same_c169_shape: bool
    all_rows_same_c13_shape: bool
    c13_shadow_is_not_lift_unique: bool


def units(modulus: int) -> tuple[int, ...]:
    return tuple(value for value in range(1, modulus) if gcd(value, modulus) == 1)


def row_values_from_q(q_values: tuple[int, ...], modulus: int) -> tuple[int, int, int]:
    values = {q_value % RIGHT_DEGREE: q_value % modulus for q_value in q_values}
    if set(values) != {0, 1, 2}:
        raise AssertionError(f"chain is not one point per row: {q_values}")
    return (values[0], values[1], values[2])


def cyclic_differences(values: tuple[int, int, int], modulus: int) -> DiffTriple:
    return (
        (values[1] - values[0]) % modulus,
        (values[2] - values[1]) % modulus,
        (values[0] - values[2]) % modulus,
    )


def permute_differences(differences: DiffTriple, row_permutation: tuple[int, int, int], modulus: int) -> DiffTriple:
    # Reconstruct a row graph with c(0)=0, then permute row labels.
    values = (
        0,
        differences[0] % modulus,
        (differences[0] + differences[1]) % modulus,
    )
    permuted_values = tuple(values[row_permutation[row]] for row in range(RIGHT_DEGREE))
    return cyclic_differences(permuted_values, modulus)


def projective_orbit(differences: DiffTriple, modulus: int) -> tuple[DiffTriple, ...]:
    orbit = {
        tuple((unit * value) % modulus for value in permuted)
        for row_permutation in permutations(range(RIGHT_DEGREE))
        for permuted in (permute_differences(differences, row_permutation, modulus),)
        for unit in units(modulus)
    }
    return tuple(sorted(orbit))


def projective_shape(differences: DiffTriple, modulus: int) -> DiffTriple:
    return projective_orbit(differences, modulus)[0]


def primitive_projective_shapes_c169() -> tuple[DiffTriple, ...]:
    shapes: set[DiffTriple] = set()
    for first in range(SQUARE_C):
        for second in range(SQUARE_C):
            if gcd((second - first) % SQUARE_C, SQUARE_C) != 1:
                continue
            shape = projective_shape((first, second, (-first - second) % SQUARE_C), SQUARE_C)
            shapes.add(shape)
    return tuple(sorted(shapes))


def chain_shape_rows() -> tuple[ChainShapeRow, ...]:
    boundary_profile = source_boundary_profile()
    rows: list[ChainShapeRow] = []
    for row in boundary_profile.rows:
        if not row.bridge_zero_compatible:
            continue
        for witness in row.best_witnesses:
            q_values = tuple(q_value for q_value, _coefficient in witness.antiderivative)
            values_c169 = row_values_from_q(q_values, SQUARE_C)
            values_c13 = row_values_from_q(q_values, 13)
            differences_c169 = cyclic_differences(values_c169, SQUARE_C)
            differences_c13 = cyclic_differences(values_c13, 13)
            rows.append(
                ChainShapeRow(
                    orientation_mask=row.orientation_mask,
                    boundary_direction_q=witness.direction_q,
                    q_values=q_values,
                    row_values_c169=values_c169,
                    row_values_c13=values_c13,
                    cyclic_differences_c169=differences_c169,
                    cyclic_differences_c13=differences_c13,
                    projective_shape_c169=projective_shape(differences_c169, SQUARE_C),
                    projective_shape_c13=projective_shape(differences_c13, 13),
                )
            )
    return tuple(rows)


def projective_shape_profile() -> ProjectiveShapeProfile:
    rows = chain_shape_rows()
    canonical_c169 = rows[0].projective_shape_c169
    canonical_c13 = rows[0].projective_shape_c13
    c169_orbit = projective_orbit(rows[0].cyclic_differences_c169, SQUARE_C)
    c13_orbit = projective_orbit(rows[0].cyclic_differences_c13, 13)
    c169_shapes = primitive_projective_shapes_c169()
    shadow_counter = Counter(projective_shape(tuple(value % 13 for value in shape), 13) for shape in c169_shapes)
    canonical_lifts = tuple(
        shape
        for shape in c169_shapes
        if projective_shape(tuple(value % 13 for value in shape), 13) == canonical_c13
    )
    return ProjectiveShapeProfile(
        rows=rows,
        canonical_projective_shape_c169=canonical_c169,
        canonical_projective_shape_c13=canonical_c13,
        c169_orbit_size=len(c169_orbit),
        c13_orbit_size=len(c13_orbit),
        c169_projective_stabilizer_size=(6 * len(units(SQUARE_C))) // len(c169_orbit),
        c13_projective_stabilizer_size=(6 * len(units(13))) // len(c13_orbit),
        primitive_c169_projective_shape_count=len(c169_shapes),
        c13_shadow_distribution=tuple(sorted(shadow_counter.items())),
        canonical_c13_lift_count=len(canonical_lifts),
        canonical_c13_lifts=canonical_lifts,
        all_rows_same_c169_shape=all(row.projective_shape_c169 == canonical_c169 for row in rows),
        all_rows_same_c13_shape=all(row.projective_shape_c13 == canonical_c13 for row in rows),
        c13_shadow_is_not_lift_unique=len(canonical_lifts) > 1,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain projective-shape gate")
    profile = projective_shape_profile()
    expected_rows = (
        ChainShapeRow(1, 197, (0, 172, 482), (0, 3, 144), (0, 3, 1), (3, 141, 25), (3, 11, 12), (1, 18, 150), (1, 2, 10)),
        ChainShapeRow(1, 310, (172, 197, 369), (31, 3, 28), (5, 3, 2), (141, 25, 3), (11, 12, 3), (1, 18, 150), (1, 2, 10)),
        ChainShapeRow(6, 197, (138, 310, 335), (138, 141, 166), (8, 11, 10), (3, 25, 141), (3, 12, 11), (1, 18, 150), (1, 2, 10)),
        ChainShapeRow(6, 310, (0, 25, 335), (0, 25, 166), (0, 12, 10), (25, 141, 3), (12, 11, 3), (1, 18, 150), (1, 2, 10)),
    )
    expected_lifts = (
        (1, 2, 166),
        (1, 4, 164),
        (1, 5, 163),
        (1, 7, 161),
        (1, 8, 160),
        (1, 10, 158),
        (1, 15, 153),
        (1, 18, 150),
        (1, 30, 138),
        (1, 31, 137),
        (1, 43, 125),
        (1, 49, 119),
        (1, 57, 111),
    )
    row_ok = (
        profile.rows == expected_rows
        and profile.canonical_projective_shape_c169 == (1, 18, 150)
        and profile.canonical_projective_shape_c13 == (1, 2, 10)
        and profile.c169_orbit_size == 936
        and profile.c13_orbit_size == 72
        and profile.c169_projective_stabilizer_size == 1
        and profile.c13_projective_stabilizer_size == 1
        and profile.primitive_c169_projective_shape_count == 32
        and profile.c13_shadow_distribution == (
            ((0, 1, 12), 7),
            ((1, 1, 11), 7),
            ((1, 2, 10), 13),
            ((1, 3, 9), 5),
        )
        and profile.canonical_c13_lift_count == 13
        and profile.canonical_c13_lifts == expected_lifts
        and profile.all_rows_same_c169_shape
        and profile.all_rows_same_c13_shape
        and profile.c13_shadow_is_not_lift_unique
    )

    print(
        "source_chain_projective_shape_summary: "
        f"canonical_c169={profile.canonical_projective_shape_c169} "
        f"canonical_c13={profile.canonical_projective_shape_c13} "
        f"c169_orbit_size={profile.c169_orbit_size} "
        f"c13_orbit_size={profile.c13_orbit_size} "
        f"primitive_c169_projective_shape_count={profile.primitive_c169_projective_shape_count} "
        f"canonical_c13_lift_count={profile.canonical_c13_lift_count}"
    )
    print(f"c13_shadow_distribution={profile.c13_shadow_distribution}")
    print(f"canonical_c13_lifts={profile.canonical_c13_lifts}")
    print("source_chain_projective_shape_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("interpretation")
    print("  all_four_hilbert90_source_chains_have_the_same_projective_C169_shape=1")
    print("  projective_shape_has_trivial_product_affine_stabilizer=1")
    print("  C13_projective_shadow_has_thirteen_primitive_C169_lifts=1")
    print("  producer_must_select_the_specific_nonsplit_C169_projective_shape_not_only_the_C13_shadow=1")
    print(f"square_axis_bridge_hilbert90_source_chain_projective_shape_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
