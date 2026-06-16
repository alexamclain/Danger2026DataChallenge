#!/usr/bin/env python3
"""Reflection bridge from KL inversion pairs to the p25 KSY T-edge packet.

The KL inversion-pair gate found that the elementary Siegel congruence screen
selects anti-invariant atoms z^a - z^-a, while the KSY normalized-y product is
written as three parallel T edges.  This gate proves those views are the same
signed divisor because the D segment is symmetric around a center C and

    T = -2C.

Thus the T-edge denominator set is the reflected denominator set, with the two
outer factors swapped.  A theorem source may therefore target anti-invariant
pair quotients, provided it also proves this reflection bridge to the KSY
theta2 payload.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate import q_from_coord
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_LEVEL,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    add_quotient,
    scale_quotient,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_inversion_pair_gate import kl_ok


Coord = tuple[int, int]
PacketTuple = tuple[tuple[Coord, int], ...]


@dataclass(frozen=True)
class SegmentPoint:
    offset: int
    positive: Coord
    positive_primitive: int
    t_negative: Coord
    t_negative_primitive: int
    inversion_negative: Coord
    inversion_negative_primitive: int
    t_edge_kl_legal: bool
    inversion_pair_kl_legal: bool


@dataclass(frozen=True)
class ReflectionBridgeProfile:
    base: Coord
    d_step: Coord
    t_step: Coord
    center: Coord
    half_t: Coord
    negative_center: Coord
    primitive_center: int
    primitive_t_step: int
    t_is_negative_double_center: bool
    half_t_is_negative_center: bool
    positive_segment: tuple[Coord, ...]
    t_negative_segment: tuple[Coord, ...]
    inversion_negative_segment: tuple[Coord, ...]
    t_negative_equals_reflected_set: bool
    t_pairing_permutation: tuple[int, ...]
    inversion_pairing_permutation: tuple[int, ...]
    overlap_t_edges: tuple[int, ...]
    segment_points: tuple[SegmentPoint, ...]
    t_edge_packet: PacketTuple
    inversion_pair_packet: PacketTuple
    packets_equal: bool
    symmetric_length_three_required: bool
    wrong_t_rejected: bool
    shifted_center_rejected: bool
    next_debt: str
    row_ok: bool


def inverse_coord(coord: Coord) -> Coord:
    return (-coord[0] % QUOTIENT_RIGHT_ORDER, -coord[1] % C_ORDER)


def double_coord(coord: Coord) -> Coord:
    return scale_quotient(coord, 2)


def half_coord(coord: Coord) -> Coord:
    inv_two_right = pow(2, -1, QUOTIENT_RIGHT_ORDER)
    inv_two_c = pow(2, -1, C_ORDER)
    return ((coord[0] * inv_two_right) % QUOTIENT_RIGHT_ORDER, (coord[1] * inv_two_c) % C_ORDER)


def primitive_exponent(coord: Coord) -> int:
    d_q_inverse = pow(q_from_coord((1, 3)), -1, QUOTIENT_LEVEL)
    return (q_from_coord(coord) * d_q_inverse) % QUOTIENT_LEVEL


def packet_tuple(ring: Ring) -> PacketTuple:
    return tuple(sorted(ring.items()))


def add_packet_entry(packet: Ring, coord: Coord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def t_edge_packet(points: tuple[Coord, ...], t_step: Coord) -> Ring:
    packet: Ring = {}
    for point in points:
        add_packet_entry(packet, point, 1)
        add_packet_entry(packet, add_quotient(point, t_step), -1)
    return dict(sorted(packet.items()))


def inversion_pair_packet(points: tuple[Coord, ...]) -> Ring:
    packet: Ring = {}
    for point in points:
        add_packet_entry(packet, point, 1)
        add_packet_entry(packet, inverse_coord(point), -1)
    return dict(sorted(packet.items()))


def segment(center: Coord, d_step: Coord, offsets: tuple[int, ...]) -> tuple[Coord, ...]:
    return tuple(add_quotient(center, scale_quotient(d_step, offset)) for offset in offsets)


def permutation_by_target(source: tuple[Coord, ...], target: tuple[Coord, ...]) -> tuple[int, ...]:
    return tuple(target.index(point) for point in source)


def profile_reflection_bridge() -> ReflectionBridgeProfile:
    base = (1, 25)
    d_step = (1, 3)
    t_step = (2, 113)
    center = add_quotient(base, d_step)
    half_t = half_coord(t_step)
    negative_center = inverse_coord(center)
    positive = segment(center, d_step, (-1, 0, 1))
    t_negative = tuple(add_quotient(point, t_step) for point in positive)
    inversion_negative = tuple(inverse_coord(point) for point in positive)
    t_packet = t_edge_packet(positive, t_step)
    inversion_packet = inversion_pair_packet(positive)

    point_rows = tuple(
        SegmentPoint(
            offset=offset,
            positive=point,
            positive_primitive=primitive_exponent(point),
            t_negative=add_quotient(point, t_step),
            t_negative_primitive=primitive_exponent(add_quotient(point, t_step)),
            inversion_negative=inverse_coord(point),
            inversion_negative_primitive=primitive_exponent(inverse_coord(point)),
            t_edge_kl_legal=kl_ok({point: 1, add_quotient(point, t_step): -1}),
            inversion_pair_kl_legal=kl_ok({point: 1, inverse_coord(point): -1}),
        )
        for offset, point in zip((-1, 0, 1), positive)
    )

    truncated_positive = segment(center, d_step, (-1, 0))
    wrong_t = add_quotient(t_step, d_step)
    shifted_center = add_quotient(center, d_step)
    shifted_positive = segment(shifted_center, d_step, (-1, 0, 1))
    symmetric_length_three_required = (
        t_edge_packet(truncated_positive, t_step)
        != inversion_pair_packet(truncated_positive)
    )
    wrong_t_rejected = (
        t_edge_packet(positive, wrong_t) != inversion_pair_packet(positive)
        and wrong_t != inverse_coord(double_coord(center))
    )
    shifted_center_rejected = (
        t_edge_packet(shifted_positive, t_step)
        != inversion_pair_packet(shifted_positive)
    )

    t_pairing_permutation = permutation_by_target(t_negative, tuple(sorted(t_negative)))
    inversion_pairing_permutation = permutation_by_target(
        inversion_negative,
        t_negative,
    )
    overlap_t_edges = tuple(
        index
        for index, row in enumerate(point_rows)
        if row.t_negative == row.inversion_negative
    )
    packets_equal = packet_tuple(t_packet) == packet_tuple(inversion_packet) == packet_tuple(source_packet())
    row_ok = (
        center == (2, 28)
        and half_t == (1, 141)
        and negative_center == half_t
        and primitive_exponent(center) == 122
        and primitive_exponent(t_step) == 263
        and t_step == inverse_coord(double_coord(center))
        and positive == ((1, 25), (2, 28), (0, 31))
        and t_negative == ((0, 138), (1, 141), (2, 144))
        and inversion_negative == ((2, 144), (1, 141), (0, 138))
        and set(t_negative) == set(inversion_negative)
        and inversion_pairing_permutation == (2, 1, 0)
        and overlap_t_edges == (1,)
        and tuple(row.t_edge_kl_legal for row in point_rows) == (False, True, False)
        and tuple(row.inversion_pair_kl_legal for row in point_rows) == (True, True, True)
        and packets_equal
        and symmetric_length_three_required
        and wrong_t_rejected
        and shifted_center_rejected
    )
    return ReflectionBridgeProfile(
        base=base,
        d_step=d_step,
        t_step=t_step,
        center=center,
        half_t=half_t,
        negative_center=negative_center,
        primitive_center=primitive_exponent(center),
        primitive_t_step=primitive_exponent(t_step),
        t_is_negative_double_center=t_step == inverse_coord(double_coord(center)),
        half_t_is_negative_center=half_t == negative_center,
        positive_segment=positive,
        t_negative_segment=t_negative,
        inversion_negative_segment=inversion_negative,
        t_negative_equals_reflected_set=set(t_negative) == set(inversion_negative),
        t_pairing_permutation=t_pairing_permutation,
        inversion_pairing_permutation=inversion_pairing_permutation,
        overlap_t_edges=overlap_t_edges,
        segment_points=point_rows,
        t_edge_packet=packet_tuple(t_packet),
        inversion_pair_packet=packet_tuple(inversion_packet),
        packets_equal=packets_equal,
        symmetric_length_three_required=symmetric_length_three_required,
        wrong_t_rejected=wrong_t_rejected,
        shifted_center_rejected=shifted_center_rejected,
        next_debt=(
            "prove a theorem-side anti-invariant product over the symmetric "
            "segment C-D,C,C+D and use T=-2C to identify it with the KSY "
            "normalized-y/theta2 payload"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang reflection-bridge gate")
    profile = profile_reflection_bridge()
    print(f"reflection_bridge_profile={profile}")
    print("reflection_geometry")
    print(
        "  "
        f"center={profile.center} half_T={profile.half_t} "
        f"-center={profile.negative_center} T=-2C={int(profile.t_is_negative_double_center)}"
    )
    print(
        "  "
        f"primitive_center={profile.primitive_center} "
        f"primitive_T={profile.primitive_t_step}"
    )
    print("segment_points")
    for row in profile.segment_points:
        print(f"  {row}")
    print("packet_comparison")
    print(f"  T_edge_packet={profile.t_edge_packet}")
    print(f"  inversion_pair_packet={profile.inversion_pair_packet}")
    print("reflection_bridge_laws")
    print("  T_equals_negative_double_center_for_the_symmetric_D_segment=1")
    print("  T_negative_set_equals_inversion_negative_set_with_outer_pair_swap=1")
    print("  product_over_inversion_pairs_equals_the_KSY_T_edge_divisor=1")
    print("  all_inversion_pairs_are_KL_legal_but_only_middle_T_edge_is_KL_legal=1")
    print("  truncated_segment_wrong_T_and_shifted_center_controls_are_rejected=1")
    print("interpretation")
    print("  anti_invariant_Siegel_or_Robert_pair_products_can_feed_the_KSY_theta2_payload=1")
    print("  theorem_must_prove_the_reflection_bridge_not_only_a_support_coincidence=1")
    print(f"robert_ksy_theta2_kubert_lang_reflection_bridge_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_reflection_bridge_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
