#!/usr/bin/env python3
"""Literal Kato/Robert subgroup-support falsifier for the p25 bridge.

The literature gives a promising translated quotient shape

    rho_H(P + T) / rho_H(P - T),

where `rho_H` has divisor `|H|[0] - [H]` for a finite subgroup `H`.  This is
exactly the right odd-quotient orientation, but the p25 finite bridge needs a
one-sided `D_segment = 1 + D + D^2` multiplied by the `K` trace.  This gate
checks whether that positive support can literally be a subgroup/coset support.

It cannot: visible `D=(1,3)` has order 507, raw `D=(22,3)` has order 12675,
and the raw positive layer has three distinct C-coordinates.  Any raw subgroup
of order 75 in `C_75 x C_169` has trivial C-projection because gcd(75,169)=1.
So the literal subgroup divisor is killed; only a Siegel/Klein/y/differential
quotient or another weighted finite-difference mechanism remains live.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


VisibleCoord = tuple[int, int]
RawCoord = tuple[int, int]

VISIBLE_RIGHT_ORDER = 3
VISIBLE_C_ORDER = 169
VISIBLE_BASE = (1, 25)
VISIBLE_D = (1, 3)


@dataclass(frozen=True)
class KatoSubgroupSupportProfile:
    visible_d_order: int
    visible_segment_size: int
    visible_three_d: VisibleCoord
    visible_order3_coset_has_fixed_c: bool
    visible_segment_is_order3_coset: bool
    raw_d_order: int
    raw_positive_support_size: int
    raw_positive_c_support: tuple[int, ...]
    raw_order75_subgroup_c_projection_must_be_trivial: bool
    raw_positive_layer_can_be_order75_coset: bool
    literal_subgroup_divisor_killed: bool


def coord_order(coord: tuple[int, int], orders: tuple[int, int]) -> int:
    left_order, right_order = orders
    left, right = coord
    left_part = 1 if left % left_order == 0 else left_order // gcd(left_order, left)
    right_part = 1 if right % right_order == 0 else right_order // gcd(right_order, right)
    return lcm(left_part, right_part)


def add_coord(left: tuple[int, int], right: tuple[int, int], orders: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % orders[0], (left[1] + right[1]) % orders[1])


def scale_coord(coord: tuple[int, int], scale: int, orders: tuple[int, int]) -> tuple[int, int]:
    return ((coord[0] * scale) % orders[0], (coord[1] * scale) % orders[1])


def visible_segment() -> tuple[VisibleCoord, ...]:
    orders = (VISIBLE_RIGHT_ORDER, VISIBLE_C_ORDER)
    return tuple(add_coord(VISIBLE_BASE, scale_coord(VISIBLE_D, i, orders), orders) for i in range(3))


def raw_positive_layer() -> tuple[RawCoord, ...]:
    orders = (RIGHT_ORDER, C_ORDER)
    points: list[RawCoord] = []
    for kernel_index in range(25):
        kernel = scale_coord(KERNEL_SHIFT, kernel_index, orders)
        for d_index in range(3):
            points.append(
                add_coord(
                    add_coord(BASE_POINT, kernel, orders),
                    scale_coord(D_SHIFT, d_index, orders),
                    orders,
                )
            )
    return tuple(sorted(points))


def kato_subgroup_support_profile() -> KatoSubgroupSupportProfile:
    visible_orders = (VISIBLE_RIGHT_ORDER, VISIBLE_C_ORDER)
    raw_orders = (RIGHT_ORDER, C_ORDER)
    visible_d_order = coord_order(VISIBLE_D, visible_orders)
    visible_three_d = scale_coord(VISIBLE_D, 3, visible_orders)
    segment = visible_segment()
    visible_c_values = {coord[1] for coord in segment}
    visible_order3_coset_has_fixed_c = True
    visible_segment_is_order3_coset = len(visible_c_values) == 1 and visible_d_order == 3

    raw_d_order = coord_order(D_SHIFT, raw_orders)
    raw_layer = raw_positive_layer()
    raw_c_support = tuple(sorted({coord[1] for coord in raw_layer}))
    raw_order75_subgroup_c_projection_must_be_trivial = gcd(75, C_ORDER) == 1
    raw_positive_layer_can_be_order75_coset = (
        len(raw_layer) == 75
        and len(raw_c_support) == 1
        and raw_order75_subgroup_c_projection_must_be_trivial
    )
    literal_killed = (
        visible_d_order != 3
        and not visible_segment_is_order3_coset
        and raw_d_order != 75
        and not raw_positive_layer_can_be_order75_coset
    )
    return KatoSubgroupSupportProfile(
        visible_d_order=visible_d_order,
        visible_segment_size=len(segment),
        visible_three_d=visible_three_d,
        visible_order3_coset_has_fixed_c=visible_order3_coset_has_fixed_c,
        visible_segment_is_order3_coset=visible_segment_is_order3_coset,
        raw_d_order=raw_d_order,
        raw_positive_support_size=len(raw_layer),
        raw_positive_c_support=raw_c_support,
        raw_order75_subgroup_c_projection_must_be_trivial=raw_order75_subgroup_c_projection_must_be_trivial,
        raw_positive_layer_can_be_order75_coset=raw_positive_layer_can_be_order75_coset,
        literal_subgroup_divisor_killed=literal_killed,
    )


def main() -> int:
    print("p25 Lane B Robert/Kato subgroup-support falsifier gate")
    profile = kato_subgroup_support_profile()
    row_ok = (
        profile.visible_d_order == 507
        and profile.visible_three_d == (0, 9)
        and not profile.visible_segment_is_order3_coset
        and profile.raw_d_order == 12675
        and profile.raw_positive_support_size == 75
        and profile.raw_positive_c_support == (25, 28, 31)
        and profile.raw_order75_subgroup_c_projection_must_be_trivial
        and not profile.raw_positive_layer_can_be_order75_coset
        and profile.literal_subgroup_divisor_killed
    )

    print(f"kato_subgroup_support_profile={profile}")
    print("subgroup_support_laws")
    print("  visible_D=(1,3)_has_order_507_not_3=1")
    print("  visible_D_segment_is_not_an_order_3_subgroup_coset=1")
    print("  raw_K_trace_times_D_segment_has_C_support_(25,28,31)=1")
    print("  raw_order_75_subgroups_have_trivial_C_projection=1")
    print("interpretation")
    print("  literal_rho_H_subgroup_divisor_cannot_supply_the_D_segment=1")
    print("  continue_only_with_weighted_Siegel_y_differential_or_finite_difference_quotient=1")
    print(f"robert_kato_subgroup_support_falsifier_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_kato_subgroup_support_falsifier_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
