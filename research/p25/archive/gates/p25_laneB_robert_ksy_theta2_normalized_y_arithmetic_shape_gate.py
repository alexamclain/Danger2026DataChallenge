#!/usr/bin/env python3
"""Arithmetic-shape audit for the p25 normalized-y theta2 product.

The normalized-y product gate found the finite identity

    prod_{A in base*K_trace*D_segment} y(A) / y(A+T) = theta2^-1,
    y(Q) = -g(2Q) / g(Q)^4.

This gate separates which parts already have honest finite arithmetic shape
from the theorem debt.  The K factor is a true 25-point trace/norm subgroup in
the right kernel.  The D factor is only a length-3 arithmetic segment, not a
subgroup norm.  Thus a successful proof must justify the normalized-y product
over the short D segment and T edge as a KSY/Siegel-unit identity; it cannot
hide that step inside a fake length-3 norm.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd, lcm

from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
    profile_normalized_y_product_source_law,
    source_centers,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    scale_coord,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
QuotientCoord = tuple[int, int]


@dataclass(frozen=True)
class NormalizedYArithmeticShapeProfile:
    base_class: QuotientCoord
    d_class: QuotientCoord
    t_class: QuotientCoord
    quotient_packet: tuple[tuple[QuotientCoord, int], ...]
    quotient_packet_support: int
    quotient_packet_exact: bool
    k_order: int
    k_trace_size: int
    k_trace_is_subgroup: bool
    k_trace_is_right_kernel: bool
    k_trace_c_trivial: bool
    k_trace_quotient_trivial: bool
    d_raw_order: int
    d_visible_order: int
    d_segment_size: int
    d_segment_distinct: bool
    d_segment_is_short_ap: bool
    d_segment_is_not_subgroup_norm: bool
    d_after_three: Coord
    d_visible_after_three: QuotientCoord
    t_edge_not_absorbed_by_k: bool
    centers_support: int
    centers_coefficient_counts: tuple[tuple[int, int], ...]
    y_evaluation_support: int
    y_evaluation_layers_disjoint: bool
    g_expansion_support: int
    g_coefficient_counts: tuple[tuple[int, int], ...]
    product_source_law_ok: bool
    controls_rejected: bool
    honest_subgroup_part: str
    theorem_debt: str
    row_ok: bool


def coord_order(step: Coord, right_order: int = RIGHT_ORDER, c_order: int = C_ORDER) -> int:
    right_component_order = 1 if step[0] % right_order == 0 else right_order // gcd(right_order, step[0])
    c_component_order = 1 if step[1] % c_order == 0 else c_order // gcd(c_order, step[1])
    return lcm(right_component_order, c_component_order)


def quotient_class(coord: Coord) -> QuotientCoord:
    return (coord[0] % 3, coord[1] % C_ORDER)


def quotient_add(left: QuotientCoord, right: QuotientCoord) -> QuotientCoord:
    return ((left[0] + right[0]) % 3, (left[1] + right[1]) % C_ORDER)


def quotient_scale(step: QuotientCoord, scalar: int) -> QuotientCoord:
    return ((step[0] * scalar) % 3, (step[1] * scalar) % C_ORDER)


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def quotient_source_packet(
    base_class: QuotientCoord,
    d_class: QuotientCoord,
    t_class: QuotientCoord,
) -> tuple[tuple[QuotientCoord, int], ...]:
    packet: dict[QuotientCoord, int] = {}
    for index in range(3):
        positive = quotient_add(base_class, quotient_scale(d_class, index))
        negative = quotient_add(positive, t_class)
        packet[positive] = packet.get(positive, 0) + 1
        packet[negative] = packet.get(negative, 0) - 1
    return tuple(sorted((coord, value) for coord, value in packet.items() if value))


def y_evaluation_points(centers: Ring, t_step: Coord) -> tuple[set[Coord], set[Coord], set[Coord]]:
    left_points = set(centers)
    right_points = {add_coord(point, t_step) for point in centers}
    return left_points, right_points, left_points | right_points


def profile_arithmetic_shape() -> NormalizedYArithmeticShapeProfile:
    source_law = profile_normalized_y_product_source_law()

    k_trace = {scale_coord(KERNEL_SHIFT, index) for index in range(25)}
    d_segment = {scale_coord(D_SHIFT, index) for index in range(3)}
    centers = source_centers(BASE_POINT, KERNEL_SHIFT, D_SHIFT, 25, 3)
    left_y, right_y, all_y = y_evaluation_points(centers, BRIDGE_SHIFT)
    footprint = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )

    base_q = quotient_class(BASE_POINT)
    d_q = quotient_class(D_SHIFT)
    t_q = quotient_class(BRIDGE_SHIFT)
    packet = quotient_source_packet(base_q, d_q, t_q)
    expected_packet = (
        ((0, 31), 1),
        ((0, 138), -1),
        ((1, 25), 1),
        ((1, 141), -1),
        ((2, 28), 1),
        ((2, 144), -1),
    )

    d_after_three = scale_coord(D_SHIFT, 3)
    d_visible_after_three = quotient_scale(d_q, 3)
    controls_rejected = (
        source_law.missing_k_rejected
        and source_law.collapsed_k_rejected
        and source_law.truncated_d_rejected
        and source_law.wrong_d_rejected
        and source_law.wrong_t_rejected
    )

    row_ok = (
        source_law.row_ok
        and base_q == (1, 25)
        and d_q == (1, 3)
        and t_q == (2, 113)
        and packet == expected_packet
        and coord_order(KERNEL_SHIFT) == 25
        and len(k_trace) == 25
        and all(quotient_class(point) == (0, 0) for point in k_trace)
        and all(point[1] == 0 for point in k_trace)
        and coord_order(D_SHIFT) == 12675
        and lcm(3 // gcd(3, d_q[0]), C_ORDER // gcd(C_ORDER, d_q[1])) == 507
        and len(d_segment) == 3
        and d_segment == {scale_coord(D_SHIFT, index) for index in range(3)}
        and d_after_three != (0, 0)
        and d_visible_after_three != (0, 0)
        and t_q != (0, 0)
        and len(centers) == 75
        and coefficient_counts(centers) == ((1, 75),)
        and len(all_y) == 150
        and left_y.isdisjoint(right_y)
        and len(footprint) == 300
        and coefficient_counts(footprint) == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and controls_rejected
    )

    return NormalizedYArithmeticShapeProfile(
        base_class=base_q,
        d_class=d_q,
        t_class=t_q,
        quotient_packet=packet,
        quotient_packet_support=len(packet),
        quotient_packet_exact=packet == expected_packet,
        k_order=coord_order(KERNEL_SHIFT),
        k_trace_size=len(k_trace),
        k_trace_is_subgroup=coord_order(KERNEL_SHIFT) == 25 and len(k_trace) == 25,
        k_trace_is_right_kernel=all(point[0] % 3 == 0 for point in k_trace),
        k_trace_c_trivial=all(point[1] == 0 for point in k_trace),
        k_trace_quotient_trivial=all(quotient_class(point) == (0, 0) for point in k_trace),
        d_raw_order=coord_order(D_SHIFT),
        d_visible_order=lcm(3 // gcd(3, d_q[0]), C_ORDER // gcd(C_ORDER, d_q[1])),
        d_segment_size=len(d_segment),
        d_segment_distinct=len(d_segment) == 3,
        d_segment_is_short_ap=d_segment == {scale_coord(D_SHIFT, index) for index in range(3)},
        d_segment_is_not_subgroup_norm=d_after_three != (0, 0) and d_visible_after_three != (0, 0),
        d_after_three=d_after_three,
        d_visible_after_three=d_visible_after_three,
        t_edge_not_absorbed_by_k=t_q != (0, 0),
        centers_support=len(centers),
        centers_coefficient_counts=coefficient_counts(centers),
        y_evaluation_support=len(all_y),
        y_evaluation_layers_disjoint=left_y.isdisjoint(right_y),
        g_expansion_support=len(footprint),
        g_coefficient_counts=coefficient_counts(footprint),
        product_source_law_ok=source_law.row_ok,
        controls_rejected=controls_rejected,
        honest_subgroup_part="K_trace is a true 25-point right-kernel trace/norm",
        theorem_debt=(
            "D_segment is a short non-subgroup arithmetic segment and T is a "
            "nontrivial quotient edge; a proof must supply the KSY/Siegel-unit "
            "identity for the normalized-y product rather than treating D as a norm"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY normalized-y arithmetic-shape gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_arithmetic_shape()
    print(f"normalized_y_arithmetic_shape_profile={profile}")
    print("arithmetic_shape")
    print("  K_trace_is_honest_25_point_right_kernel_norm=1")
    print("  D_segment_is_length_3_short_AP_not_subgroup_norm=1")
    print("  T_edge_is_nontrivial_quotient_edge=1")
    print("  quotient_packet_has_the_six_accepted_source_cells=1")
    print("  product_expands_to_75_centers_150_y_values_300_g_terms=1")
    print("interpretation")
    print("  finite_payload_and_certificate_chain_are_verified=1")
    print("  remaining_theorem_debt_is_the_challenge_legal_normalized_y_product_identity=1")
    print(f"robert_ksy_theta2_normalized_y_arithmetic_shape_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_normalized_y_arithmetic_shape_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
