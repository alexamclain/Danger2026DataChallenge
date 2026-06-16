#!/usr/bin/env python3
"""Affine obstruction for the p25 Hilbert-90 corner skew near miss.

The skew image-orbit gate shows that the recorded 197/310 short skew
derivative lands on the signed S=172 bridge image, while the opposite short
branch has the wrong image-orbit geometry.  This gate rules out a softer
escape: the opposite image is not an affine reindexing of the bridge, either
on the cyclic quotient C_507 or in the actual source coordinates C_3 x C_169.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_gate import (
    source_coord,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_image_orbit_gate import (
    skew_image_orbit_profile,
)
from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import (
    c_units,
    source_bridge_mask,
    transform as source_affine_transform,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_selected_defect_value_gate import RIGHT_DEGREE


Items = tuple[tuple[int, int], ...]
SourceMask = dict[tuple[int, int], int]


@dataclass(frozen=True)
class AffineScan:
    maps_scanned: int
    support_hits: int
    exact_hits: int
    signed_exact_hits: int


@dataclass(frozen=True)
class SkewImageAffineRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    opposite_image_support: int
    opposite_image_items: Items
    q_affine_scan: AffineScan
    source_affine_scan: AffineScan


@dataclass(frozen=True)
class SkewImageAffineProfile:
    row_count: int
    q_affine_maps_per_row: int
    source_affine_maps_per_row: int
    all_opposite_branches_have_no_q_affine_bridge_disguise: bool
    all_opposite_branches_have_no_source_affine_bridge_disguise: bool
    rows: tuple[SkewImageAffineRow, ...]


def q_units() -> tuple[int, ...]:
    return tuple(value for value in range(1, QUOTIENT_ORDER) if gcd(value, QUOTIENT_ORDER) == 1)


def q_affine_transform(poly: dict[int, int], unit: int, shift: int, scale: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for q_value, coefficient in poly.items():
        out[(unit * q_value + shift) % QUOTIENT_ORDER] = scale * coefficient
    return dict(sorted(out.items()))


def source_mask_from_q_items(items: Items) -> SourceMask:
    return dict(sorted((source_coord(q_value), coefficient) for q_value, coefficient in items))


def scaled_source_mask(mask: SourceMask, scale: int) -> SourceMask:
    return dict(sorted((coord, scale * coefficient) for coord, coefficient in mask.items()))


def q_affine_scan(poly: dict[int, int], target: dict[int, int]) -> AffineScan:
    maps_scanned = 0
    support_hits = 0
    exact_hits = 0
    signed_exact_hits = 0
    for unit in q_units():
        for shift in range(QUOTIENT_ORDER):
            maps_scanned += 1
            image = q_affine_transform(poly, unit, shift, 1)
            if set(image) == set(target):
                support_hits += 1
            if image == target:
                exact_hits += 1
            if q_affine_transform(poly, unit, shift, -1) == target:
                signed_exact_hits += 1
    return AffineScan(maps_scanned, support_hits, exact_hits, signed_exact_hits)


def source_affine_scan(mask: SourceMask, target: SourceMask) -> AffineScan:
    maps_scanned = 0
    support_hits = 0
    exact_hits = 0
    signed_exact_hits = 0
    right_units = tuple(value for value in range(1, RIGHT_DEGREE) if gcd(value, RIGHT_DEGREE) == 1)
    negative_target = scaled_source_mask(target, -1)
    for alpha in right_units:
        for beta in range(RIGHT_DEGREE):
            for unit in c_units():
                for shift in range(169):
                    maps_scanned += 1
                    image = source_affine_transform(mask, alpha, beta, unit, shift)
                    if set(image) == set(target):
                        support_hits += 1
                    if image == target:
                        exact_hits += 1
                    if image == negative_target:
                        signed_exact_hits += 1
    return AffineScan(maps_scanned, support_hits, exact_hits, signed_exact_hits)


def skew_image_affine_profile() -> SkewImageAffineProfile:
    bridge = bridge_coefficients()
    source_bridge = source_bridge_mask()
    rows: list[SkewImageAffineRow] = []
    for row in skew_image_orbit_profile().rows:
        opposite = dict(row.opposite_branch.image_items)
        source_opposite = source_mask_from_q_items(row.opposite_branch.image_items)
        rows.append(
            SkewImageAffineRow(
                orientation_mask=row.orientation_mask,
                recorded_direction_q=row.recorded_direction_q,
                opposite_direction_q=row.opposite_direction_q,
                opposite_image_support=row.opposite_branch.image_support,
                opposite_image_items=row.opposite_branch.image_items,
                q_affine_scan=q_affine_scan(opposite, bridge),
                source_affine_scan=source_affine_scan(source_opposite, source_bridge),
            )
        )
    rows_tuple = tuple(rows)
    q_maps = len(q_units()) * QUOTIENT_ORDER
    source_maps = 2 * RIGHT_DEGREE * len(c_units()) * 169
    return SkewImageAffineProfile(
        row_count=len(rows_tuple),
        q_affine_maps_per_row=q_maps,
        source_affine_maps_per_row=source_maps,
        all_opposite_branches_have_no_q_affine_bridge_disguise=all(
            row.q_affine_scan.support_hits == 0
            and row.q_affine_scan.exact_hits == 0
            and row.q_affine_scan.signed_exact_hits == 0
            for row in rows_tuple
        ),
        all_opposite_branches_have_no_source_affine_bridge_disguise=all(
            row.source_affine_scan.support_hits == 0
            and row.source_affine_scan.exact_hits == 0
            and row.source_affine_scan.signed_exact_hits == 0
            for row in rows_tuple
        ),
        rows=rows_tuple,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner skew image affine-obstruction gate")
    profile = skew_image_affine_profile()
    zero_scan = AffineScan(158184, 0, 0, 0)
    wrong6_items = ((172, -1), (197, -1), (222, -1), (285, 1), (310, 1), (335, 1))
    wrong8_items = ((59, -1), (113, 1), (172, 1), (197, 1), (310, -1), (335, -1), (394, -1), (448, 1))
    expected_rows = (
        SkewImageAffineRow(1, 197, 310, 6, wrong6_items, zero_scan, zero_scan),
        SkewImageAffineRow(1, 310, 197, 8, wrong8_items, zero_scan, zero_scan),
        SkewImageAffineRow(6, 197, 310, 8, wrong8_items, zero_scan, zero_scan),
        SkewImageAffineRow(6, 310, 197, 6, wrong6_items, zero_scan, zero_scan),
    )
    row_ok = (
        profile.row_count == 4
        and profile.q_affine_maps_per_row == 158184
        and profile.source_affine_maps_per_row == 158184
        and profile.all_opposite_branches_have_no_q_affine_bridge_disguise
        and profile.all_opposite_branches_have_no_source_affine_bridge_disguise
        and profile.rows == expected_rows
    )

    print(
        "corner_skew_image_affine_summary: "
        f"q_maps_per_row={profile.q_affine_maps_per_row} "
        f"source_maps_per_row={profile.source_affine_maps_per_row} "
        f"opposite_supports={tuple(row.opposite_image_support for row in profile.rows)} "
        f"q_support_hits={tuple(row.q_affine_scan.support_hits for row in profile.rows)} "
        f"source_support_hits={tuple(row.source_affine_scan.support_hits for row in profile.rows)}"
    )
    print("corner_skew_image_affine_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("affine_obstruction_laws")
    print("  no affine unit map q -> a*q+b on C_507 sends an opposite image support to the bridge support")
    print("  no signed affine unit map on C_507 sends an opposite image exactly to the bridge")
    print("  no product-affine source map on C_3 x C_169 sends an opposite image support to the source bridge support")
    print("  no signed product-affine source map sends an opposite image exactly to the source bridge")
    print("interpretation")
    print("  opposite_short_skew_branch_is_not_a_quotient_affine_disguise_of_the_bridge=1")
    print("  opposite_short_skew_branch_is_not_a_source_affine_disguise_of_the_bridge=1")
    print("  producer_cannot_recover_the_wrong_branch_by_diamond_Frobenius_or_source_coordinate_reindexing=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_skew_image_affine_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_image_affine_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
