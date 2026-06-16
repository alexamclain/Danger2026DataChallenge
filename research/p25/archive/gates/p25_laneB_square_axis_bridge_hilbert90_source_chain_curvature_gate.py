#!/usr/bin/env python3
"""Curvature screen for p25 Hilbert-90 source-boundary chains.

The source-boundary gate reduced the bridge-compatible Hilbert-90 target to a
three-point antiderivative chain.  This gate asks whether that chain is just a
disguised source line, arithmetic progression, or D-segment.

It is not.  The four best witnesses for masks 1 and 6 are one product-affine
source orbit, but their row graph has unit C_169 curvature.  Equivalently, the
chain is a genuinely curved three-point graph on C_3 x C_169, not a line or a
uniform D-segment.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    BoundaryWitness,
    source_boundary_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Chain = tuple[int, ...]
AffineMap = tuple[int, int, int, int]


@dataclass(frozen=True)
class SourceChainProfile:
    orientation_mask: int
    boundary_direction_q: int
    boundary_direction_coord: tuple[int, int]
    coefficients: tuple[int, ...]
    q_values: Chain
    source_coords: tuple[tuple[int, int], ...]
    row_values: tuple[int, int, int]
    c13_row_values: tuple[int, int, int]
    cyclic_first_differences: tuple[int, int, int]
    cyclic_first_differences_mod13: tuple[int, int, int]
    curvature: int
    curvature_mod13: int
    primitive_curvature: bool
    line_like_over_c169: bool
    line_like_over_c13: bool
    arithmetic_progression_count: int
    d_segment_affine_match_count: int


@dataclass(frozen=True)
class SourceChainCurvatureProfile:
    bridge_chain_count: int
    source_affine_equivalence: tuple[tuple[tuple[int, int], tuple[tuple[int, int, AffineMap], ...]], ...]
    all_chains_one_affine_orbit: bool
    all_curvatures_primitive: bool
    all_c13_curvatures_nonzero: bool
    no_chain_is_line_like_over_c169: bool
    no_chain_is_line_like_over_c13: bool
    no_chain_is_arithmetic_progression: bool
    no_chain_is_affine_d_segment: bool
    canonical_chain: tuple[int, ...]
    canonical_curvature: int
    canonical_quadratic_coefficients: tuple[int, int, int]
    profiles: tuple[SourceChainProfile, ...]


def coord_from_q(q_value: int) -> tuple[int, int]:
    return (q_value % RIGHT_DEGREE, q_value % SQUARE_C)


def q_from_coord(coord: tuple[int, int]) -> int:
    right, c_value = coord
    c_value %= SQUARE_C
    quotient_lift = (right - c_value) % RIGHT_DEGREE
    return c_value + SQUARE_C * quotient_lift


def source_transform(q_values: Chain, alpha: int, beta: int, unit: int, shift: int) -> Chain:
    image = []
    for q_value in q_values:
        right, c_value = coord_from_q(q_value)
        image.append(q_from_coord(((alpha * right + beta) % RIGHT_DEGREE, (unit * c_value + shift) % SQUARE_C)))
    return tuple(sorted(image))


def c_units() -> tuple[int, ...]:
    return tuple(value for value in range(1, SQUARE_C) if gcd(value, SQUARE_C) == 1)


def affine_maps(source: Chain, target: Chain) -> tuple[AffineMap, ...]:
    target_sorted = tuple(sorted(target))
    maps: list[AffineMap] = []
    for alpha in (1, 2):
        for beta in range(RIGHT_DEGREE):
            for unit in c_units():
                for shift in range(SQUARE_C):
                    if source_transform(source, alpha, beta, unit, shift) == target_sorted:
                        maps.append((alpha, beta, unit, shift))
    return tuple(maps)


def arithmetic_progression_count(q_values: Chain) -> int:
    support = set(q_values)
    count = 0
    for base in support:
        for step in range(1, QUOTIENT_ORDER):
            if len({base, (base + step) % QUOTIENT_ORDER, (base + 2 * step) % QUOTIENT_ORDER}) != 3:
                continue
            if {base, (base + step) % QUOTIENT_ORDER, (base + 2 * step) % QUOTIENT_ORDER} == support:
                count += 1
    return count


def row_values(q_values: Chain) -> tuple[int, int, int]:
    values = {q_value % RIGHT_DEGREE: q_value % SQUARE_C for q_value in q_values}
    if set(values) != {0, 1, 2}:
        raise AssertionError(f"chain is not one point per row: {q_values}")
    return (values[0], values[1], values[2])


def first_differences(values: tuple[int, int, int], modulus: int) -> tuple[int, int, int]:
    return (
        (values[1] - values[0]) % modulus,
        (values[2] - values[1]) % modulus,
        (values[0] - values[2]) % modulus,
    )


def curvature(values: tuple[int, int, int], modulus: int) -> int:
    return (values[2] - 2 * values[1] + values[0]) % modulus


def quadratic_coefficients(values: tuple[int, int, int]) -> tuple[int, int, int]:
    # c(r) = a*r^2 + b*r + c over Z/169 for rows r=0,1,2.
    c0 = values[0]
    two_inverse = pow(2, -1, SQUARE_C)
    a = ((values[2] - 2 * values[1] + values[0]) * two_inverse) % SQUARE_C
    b = (values[1] - c0 - a) % SQUARE_C
    return (a, b, c0)


def chain_profile(mask: int, witness: BoundaryWitness) -> SourceChainProfile:
    q_values = tuple(q_value for q_value, _coefficient in witness.antiderivative)
    values = row_values(q_values)
    values_mod13 = tuple(value % 13 for value in values)  # type: ignore[assignment]
    curv = curvature(values, SQUARE_C)
    curv_mod13 = curvature(values_mod13, 13)
    return SourceChainProfile(
        orientation_mask=mask,
        boundary_direction_q=witness.direction_q,
        boundary_direction_coord=witness.direction_coord,
        coefficients=tuple(coefficient for _q_value, coefficient in witness.antiderivative),
        q_values=q_values,
        source_coords=tuple(coord_from_q(q_value) for q_value in q_values),
        row_values=values,
        c13_row_values=values_mod13,
        cyclic_first_differences=first_differences(values, SQUARE_C),
        cyclic_first_differences_mod13=first_differences(values_mod13, 13),
        curvature=curv,
        curvature_mod13=curv_mod13,
        primitive_curvature=gcd(curv, SQUARE_C) == 1,
        line_like_over_c169=curv == 0,
        line_like_over_c13=curv_mod13 == 0,
        arithmetic_progression_count=arithmetic_progression_count(q_values),
        d_segment_affine_match_count=len(affine_maps(q_values, (0, q_from_coord((1, 3)), q_from_coord((2, 6))))),
    )


def source_chain_curvature_profile() -> SourceChainCurvatureProfile:
    boundary_profile = source_boundary_profile()
    profiles = tuple(
        chain_profile(row.orientation_mask, witness)
        for row in boundary_profile.rows
        if row.bridge_zero_compatible
        for witness in row.best_witnesses
    )
    canonical = profiles[0].q_values
    equivalence = tuple(
        (
            (profile.orientation_mask, profile.boundary_direction_q),
            tuple(
                (
                    other.orientation_mask,
                    other.boundary_direction_q,
                    maps[0],
                )
                for other in profiles
                for maps in (affine_maps(canonical, other.q_values),)
                if maps
            ),
        )
        for profile in profiles
    )
    return SourceChainCurvatureProfile(
        bridge_chain_count=len(profiles),
        source_affine_equivalence=equivalence,
        all_chains_one_affine_orbit=all(affine_maps(canonical, profile.q_values) for profile in profiles),
        all_curvatures_primitive=all(profile.primitive_curvature for profile in profiles),
        all_c13_curvatures_nonzero=all(profile.curvature_mod13 != 0 for profile in profiles),
        no_chain_is_line_like_over_c169=all(not profile.line_like_over_c169 for profile in profiles),
        no_chain_is_line_like_over_c13=all(not profile.line_like_over_c13 for profile in profiles),
        no_chain_is_arithmetic_progression=all(profile.arithmetic_progression_count == 0 for profile in profiles),
        no_chain_is_affine_d_segment=all(profile.d_segment_affine_match_count == 0 for profile in profiles),
        canonical_chain=canonical,
        canonical_curvature=profiles[0].curvature,
        canonical_quadratic_coefficients=quadratic_coefficients(profiles[0].row_values),
        profiles=profiles,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain curvature gate")
    profile = source_chain_curvature_profile()
    expected_profiles = (
        SourceChainProfile(1, 197, (2, 28), (-1, -1, -1), (0, 172, 482), ((0, 0), (1, 3), (2, 144)), (0, 3, 144), (0, 3, 1), (3, 141, 25), (3, 11, 12), 138, 8, True, False, False, 0, 0),
        SourceChainProfile(1, 310, (1, 141), (1, 1, 1), (172, 197, 369), ((1, 3), (2, 28), (0, 31)), (31, 3, 28), (5, 3, 2), (141, 25, 3), (11, 12, 3), 53, 1, True, False, False, 0, 0),
        SourceChainProfile(6, 197, (2, 28), (-1, -1, -1), (138, 310, 335), ((0, 138), (1, 141), (2, 166)), (138, 141, 166), (8, 11, 10), (3, 25, 141), (3, 12, 11), 22, 9, True, False, False, 0, 0),
        SourceChainProfile(6, 310, (1, 141), (1, 1, 1), (0, 25, 335), ((0, 0), (1, 25), (2, 166)), (0, 25, 166), (0, 12, 10), (25, 141, 3), (12, 11, 3), 116, 12, True, False, False, 0, 0),
    )
    expected_equivalence = (
        ((1, 197), ((1, 197, (1, 0, 1, 0)), (1, 310, (1, 2, 1, 28)), (6, 197, (2, 1, 168, 141)), (6, 310, (2, 0, 168, 0)))),
        ((1, 310), ((1, 197, (1, 0, 1, 0)), (1, 310, (1, 2, 1, 28)), (6, 197, (2, 1, 168, 141)), (6, 310, (2, 0, 168, 0)))),
        ((6, 197), ((1, 197, (1, 0, 1, 0)), (1, 310, (1, 2, 1, 28)), (6, 197, (2, 1, 168, 141)), (6, 310, (2, 0, 168, 0)))),
        ((6, 310), ((1, 197, (1, 0, 1, 0)), (1, 310, (1, 2, 1, 28)), (6, 197, (2, 1, 168, 141)), (6, 310, (2, 0, 168, 0)))),
    )
    row_ok = (
        profile.bridge_chain_count == 4
        and profile.profiles == expected_profiles
        and profile.source_affine_equivalence == expected_equivalence
        and profile.all_chains_one_affine_orbit
        and profile.all_curvatures_primitive
        and profile.all_c13_curvatures_nonzero
        and profile.no_chain_is_line_like_over_c169
        and profile.no_chain_is_line_like_over_c13
        and profile.no_chain_is_arithmetic_progression
        and profile.no_chain_is_affine_d_segment
        and profile.canonical_chain == (0, 172, 482)
        and profile.canonical_curvature == 138
        and profile.canonical_quadratic_coefficients == (69, 103, 0)
    )

    print(
        "source_chain_curvature_summary: "
        f"bridge_chain_count={profile.bridge_chain_count} "
        f"canonical_chain={profile.canonical_chain} "
        f"canonical_curvature={profile.canonical_curvature} "
        f"canonical_quadratic_coefficients={profile.canonical_quadratic_coefficients} "
        f"all_chains_one_affine_orbit={int(profile.all_chains_one_affine_orbit)} "
        f"all_curvatures_primitive={int(profile.all_curvatures_primitive)} "
        f"all_c13_curvatures_nonzero={int(profile.all_c13_curvatures_nonzero)}"
    )
    print(f"source_affine_equivalence={profile.source_affine_equivalence}")
    print("source_chain_profiles")
    for row in profile.profiles:
        print(f"  {row}")
    print("interpretation")
    print("  three_point_hilbert90_antiderivative_chains_are_one_source_affine_orbit=1")
    print("  canonical_chain_has_unit_C169_curvature_not_a_source_line=1")
    print("  c13_shadow_already_sees_nonzero_curvature=1")
    print("  no_chain_is_a_C507_arithmetic_progression_or_affine_D_segment=1")
    print("  producer_must_realize_a_curved_three_point_source_graph_not_a_line_segment=1")
    print(f"square_axis_bridge_hilbert90_source_chain_curvature_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_curvature_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
