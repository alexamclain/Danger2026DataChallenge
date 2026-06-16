#!/usr/bin/env python3
"""Source-shear obstruction for theta_{3,1} bridge near-misses.

The affine theta31 obstruction rules out quotient maps q -> a*q+b.  The next
cheap mixed repair would be a source-coordinate shear: keep the right axis
affine, multiply the C169 coordinate by a unit, and allow row-dependent C
offsets.  This includes product-affine maps, row-affine shears, and even
arbitrary per-row C offsets.

This gate shows that the support-<=12 theta edge family still cannot become
the primitive bridge.  The support-12 edges are killed by injectivity.  For the
two six-point +/-D edges, the row-pair differences require incompatible C169
unit multipliers before offsets or signs can help.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import (
    c_units,
    source_bridge_mask,
)
from p25_laneB_square_axis_bridge_theta31_edge_direction_scan_gate import (
    edge_coefficients,
    quotient_theta_packet,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
from p25_selected_defect_value_gate import RIGHT_DEGREE


SourceMask = dict[tuple[int, int], int]
RowItems = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ShearHitCounts:
    free_row_offset_support_maps: int
    row_affine_support_maps: int
    free_row_offset_exact_maps: int
    row_affine_exact_maps: int
    free_row_offset_signed_maps: int
    row_affine_signed_maps: int


@dataclass(frozen=True)
class SourceShearDirectionProfile:
    direction: int
    support_size: int
    row_sizes: tuple[int, int, int]
    row_pair_signed_deltas: tuple[tuple[int, int], ...]
    injective_support_size_possible: bool
    row_affine_cases: int
    c_units_checked: int
    unit_difference_support_hits: int
    hit_counts: ShearHitCounts


@dataclass(frozen=True)
class SourceShearObstructionProfile:
    target_row_pair_signed_deltas: tuple[tuple[int, int], ...]
    small_directions: tuple[int, ...]
    direction_profiles: tuple[SourceShearDirectionProfile, ...]
    total_free_row_offset_support_maps: int
    total_row_affine_support_maps: int
    total_exact_maps: int
    total_signed_maps: int


def source_mask_from_coefficients(coefficients: dict[int, int]) -> SourceMask:
    return dict(sorted((coord_from_q(q_value), value) for q_value, value in coefficients.items()))


def rows(mask: SourceMask) -> tuple[RowItems, RowItems, RowItems]:
    return tuple(
        tuple(sorted((c_value, value) for (right, c_value), value in mask.items() if right == row))
        for row in range(RIGHT_DEGREE)
    )  # type: ignore[return-value]


def row_pair_signed_deltas(mask: SourceMask) -> tuple[tuple[int, int], ...]:
    deltas: list[tuple[int, int]] = []
    for row, items in enumerate(rows(mask)):
        if len(items) != 2:
            continue
        positives = [c_value for c_value, value in items if value == 1]
        negatives = [c_value for c_value, value in items if value == -1]
        if len(positives) == 1 and len(negatives) == 1:
            deltas.append((row, (negatives[0] - positives[0]) % 169))
    return tuple(deltas)


def row_delta_options(
    source_items: RowItems,
    target_items: RowItems,
    unit: int,
    coefficient_scale: int | None,
) -> set[int]:
    if len(source_items) != len(target_items):
        return set()

    target_support = {c_value for c_value, _value in target_items}
    target_values = {c_value: coefficient_scale * value for c_value, value in target_items} if coefficient_scale is not None else {}
    options: set[int] = set()
    for source_c, _source_value in source_items:
        for target_c, _target_value in target_items:
            delta = (target_c - unit * source_c) % 169
            image: dict[int, int] = {}
            for c_value, value in source_items:
                image_c = (unit * c_value + delta) % 169
                image[image_c] = value
            if len(image) != len(source_items):
                continue
            if coefficient_scale is None:
                if set(image) == target_support:
                    options.add(delta)
            elif image == target_values:
                options.add(delta)
    return options


def count_row_affine_delta_tuples(delta_options: tuple[set[int], set[int], set[int]]) -> int:
    count = 0
    for delta0, delta1, delta2 in product(*delta_options):
        if (delta1 - delta0) % 169 == (delta2 - delta1) % 169:
            count += 1
    return count


def shear_hit_counts(mask: SourceMask, target: SourceMask) -> tuple[int, ShearHitCounts]:
    source_rows = rows(mask)
    target_rows = rows(target)
    if len(mask) != len(target):
        return 0, ShearHitCounts(0, 0, 0, 0, 0, 0)

    free_support_maps = 0
    row_affine_support_maps = 0
    free_exact_maps = 0
    row_affine_exact_maps = 0
    free_signed_maps = 0
    row_affine_signed_maps = 0
    unit_difference_support_hits = 0
    for alpha in (1, 2):
        for beta in range(RIGHT_DEGREE):
            for unit in c_units():
                support_options: list[set[int]] = []
                exact_options: list[set[int]] = []
                signed_options: list[set[int]] = []
                for source_row in range(RIGHT_DEGREE):
                    target_row = (alpha * source_row + beta) % RIGHT_DEGREE
                    support_options.append(
                        row_delta_options(source_rows[source_row], target_rows[target_row], unit, None)
                    )
                    exact_options.append(
                        row_delta_options(source_rows[source_row], target_rows[target_row], unit, 1)
                    )
                    signed_options.append(
                        row_delta_options(source_rows[source_row], target_rows[target_row], unit, -1)
                    )

                support_tuple = tuple(support_options)  # type: ignore[assignment]
                exact_tuple = tuple(exact_options)  # type: ignore[assignment]
                signed_tuple = tuple(signed_options)  # type: ignore[assignment]
                if all(support_tuple):
                    unit_difference_support_hits += 1
                    support_product = 1
                    for options in support_tuple:
                        support_product *= len(options)
                    free_support_maps += support_product
                    row_affine_support_maps += count_row_affine_delta_tuples(support_tuple)
                if all(exact_tuple):
                    exact_product = 1
                    for options in exact_tuple:
                        exact_product *= len(options)
                    free_exact_maps += exact_product
                    row_affine_exact_maps += count_row_affine_delta_tuples(exact_tuple)
                if all(signed_tuple):
                    signed_product = 1
                    for options in signed_tuple:
                        signed_product *= len(options)
                    free_signed_maps += signed_product
                    row_affine_signed_maps += count_row_affine_delta_tuples(signed_tuple)

    return unit_difference_support_hits, ShearHitCounts(
        free_row_offset_support_maps=free_support_maps,
        row_affine_support_maps=row_affine_support_maps,
        free_row_offset_exact_maps=free_exact_maps,
        row_affine_exact_maps=row_affine_exact_maps,
        free_row_offset_signed_maps=free_signed_maps,
        row_affine_signed_maps=row_affine_signed_maps,
    )


def direction_profile(direction: int, target: SourceMask) -> SourceShearDirectionProfile:
    mask = source_mask_from_coefficients(edge_coefficients(quotient_theta_packet(), direction))
    unit_hits, hit_counts = shear_hit_counts(mask, target)
    return SourceShearDirectionProfile(
        direction=direction,
        support_size=len(mask),
        row_sizes=tuple(len(row) for row in rows(mask)),  # type: ignore[arg-type]
        row_pair_signed_deltas=row_pair_signed_deltas(mask),
        injective_support_size_possible=len(mask) == len(target),
        row_affine_cases=6,
        c_units_checked=len(c_units()),
        unit_difference_support_hits=unit_hits,
        hit_counts=hit_counts,
    )


def obstruction_profile() -> SourceShearObstructionProfile:
    target = source_bridge_mask()
    packet = quotient_theta_packet()
    small_directions = tuple(
        direction
        for direction in range(1, QUOTIENT_ORDER)
        if len(edge_coefficients(packet, direction)) <= 12
    )
    profiles = tuple(direction_profile(direction, target) for direction in small_directions)
    return SourceShearObstructionProfile(
        target_row_pair_signed_deltas=row_pair_signed_deltas(target),
        small_directions=small_directions,
        direction_profiles=profiles,
        total_free_row_offset_support_maps=sum(
            profile.hit_counts.free_row_offset_support_maps for profile in profiles
        ),
        total_row_affine_support_maps=sum(
            profile.hit_counts.row_affine_support_maps for profile in profiles
        ),
        total_exact_maps=sum(
            profile.hit_counts.free_row_offset_exact_maps
            + profile.hit_counts.row_affine_exact_maps
            for profile in profiles
        ),
        total_signed_maps=sum(
            profile.hit_counts.free_row_offset_signed_maps
            + profile.hit_counts.row_affine_signed_maps
            for profile in profiles
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge theta31 source-shear obstruction gate")
    profile = obstruction_profile()
    zero_hits = ShearHitCounts(0, 0, 0, 0, 0, 0)
    expected = SourceShearObstructionProfile(
        target_row_pair_signed_deltas=((0, 107), (1, 116), (2, 116)),
        small_directions=(163, 172, 335, 344),
        direction_profiles=(
            SourceShearDirectionProfile(163, 12, (4, 4, 4), (), False, 6, 156, 0, zero_hits),
            SourceShearDirectionProfile(172, 6, (2, 2, 2), ((0, 43), (1, 127), (2, 85)), True, 6, 156, 0, zero_hits),
            SourceShearDirectionProfile(335, 6, (2, 2, 2), ((0, 42), (1, 84), (2, 126)), True, 6, 156, 0, zero_hits),
            SourceShearDirectionProfile(344, 12, (4, 4, 4), (), False, 6, 156, 0, zero_hits),
        ),
        total_free_row_offset_support_maps=0,
        total_row_affine_support_maps=0,
        total_exact_maps=0,
        total_signed_maps=0,
    )
    row_ok = profile == expected

    print(f"target_row_pair_signed_deltas={profile.target_row_pair_signed_deltas}")
    print("source_shear_direction_profiles")
    for row in profile.direction_profiles:
        print(f"  {row}")
    print("source_shear_laws")
    print("  source shears tested: right -> alpha*right+beta, C -> unit*C + row_offset[right]")
    print("  row-affine shears are the subcase row_offset[right]=shift+gamma*right")
    print("  support-12 theta edges cannot map to the six-point bridge under any injective source shear")
    print("  support-6 theta edges fail before offsets: no C169 unit matches all row-pair differences")
    print("interpretation")
    print("  theta31_near_miss_is_not_a_source_row_shear_of_the_bridge=1")
    print("  arbitrary_per_row_C_offsets_do_not_repair_the_theta31_D_edge=1")
    print("  next_theta_route_must_change_the_packet_or_add_a_new_arithmetic_mixed_factor=1")
    print(
        f"square_axis_bridge_theta31_source_shear_obstruction_rows={int(row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_square_axis_bridge_theta31_source_shear_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
