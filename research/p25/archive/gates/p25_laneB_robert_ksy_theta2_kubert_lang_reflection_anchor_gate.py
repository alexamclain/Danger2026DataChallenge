#!/usr/bin/env python3
"""Reflection-anchor gate for the p25 Kubert-Lang row-pair packet.

The row-pair permutation gate showed that fixed T leaves three cyclic row
translates.  This gate records the sharper anti-invariant anchor:

    T = -2C

where C is the center of the positive D-segment.  All three fixed-T translates
have C-axis midpoint c=28, but only the recorded packet has the correct row
coordinate C=(2,28), equivalently T/2=-C.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate import (
    d_segment_t_edge_shape,
    fixed_t_edge_shape,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    add_quotient,
    scale_quotient,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_gate import (
    NEGATIVE_C_AXIS,
    POSITIVE_C_AXIS,
    pair_permutation_packet,
    profile_row_pair_permutation_rigidity,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    packet_entries,
    profile_source_quotient_packet,
)


Coord = tuple[int, int]
D_STEP = (1, 3)
T_STEP = (2, 113)


@dataclass(frozen=True)
class FixedTReflectionAnchorLaw:
    positive_by_row: tuple[int, int, int]
    negative_by_row: tuple[int, int, int]
    base: Coord
    center: Coord
    center_c_axis_midpoint: int
    negative_double_center: Coord
    half_t: Coord
    negative_center: Coord
    t_is_negative_double_center: bool
    half_t_is_negative_center: bool
    source_contract_ok: bool
    trace_correct: bool


@dataclass(frozen=True)
class ReflectionAnchorProfile:
    permutations_scanned: int
    d_segment_t_edge_hits: int
    fixed_t_edge_hits: int
    fixed_t_anchor_laws: tuple[FixedTReflectionAnchorLaw, ...]
    reflection_anchor_hits: int
    source_contract_hits: int
    trace_correct_hits: int
    target_anchor_law: FixedTReflectionAnchorLaw
    all_fixed_t_laws_share_c_axis_midpoint: bool
    c_axis_midpoint_alone_is_insufficient: bool
    reflection_anchor_selects_unique_target: bool
    recommendation: str
    row_ok: bool


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % QUOTIENT_RIGHT_ORDER, (-coord[1]) % C_ORDER)


def half_coord(coord: Coord) -> Coord:
    return (
        (coord[0] * pow(2, -1, QUOTIENT_RIGHT_ORDER)) % QUOTIENT_RIGHT_ORDER,
        (coord[1] * pow(2, -1, C_ORDER)) % C_ORDER,
    )


def positive_coords(packet: Ring) -> set[Coord]:
    return {coord for coord, coefficient in packet.items() if coefficient > 0}


def negative_coords(packet: Ring) -> set[Coord]:
    return {coord for coord, coefficient in packet.items() if coefficient < 0}


def find_positive_segment_base(packet: Ring) -> Coord:
    positives = positive_coords(packet)
    negatives = negative_coords(packet)
    for base in sorted(positives):
        segment = {add_quotient(base, scale_quotient(D_STEP, index)) for index in range(3)}
        if segment != positives:
            continue
        t_segment = {add_quotient(point, T_STEP) for point in segment}
        if t_segment == negatives:
            return base
    raise AssertionError("packet is not a fixed-T D segment")


def profile_anchor_law(
    positive_by_row: tuple[int, int, int],
    negative_by_row: tuple[int, int, int],
) -> FixedTReflectionAnchorLaw:
    packet = pair_permutation_packet(positive_by_row, negative_by_row)
    base = find_positive_segment_base(packet)
    center = add_quotient(base, D_STEP)
    negative_double_center = inverse_coord(scale_quotient(center, 2))
    half_t = half_coord(T_STEP)
    negative_center = inverse_coord(center)
    source_profile = profile_source_quotient_packet(
        f"reflection_anchor_pos_{positive_by_row}_neg_{negative_by_row}",
        packet_entries(packet),
        1,
    )
    return FixedTReflectionAnchorLaw(
        positive_by_row=positive_by_row,
        negative_by_row=negative_by_row,
        base=base,
        center=center,
        center_c_axis_midpoint=center[1],
        negative_double_center=negative_double_center,
        half_t=half_t,
        negative_center=negative_center,
        t_is_negative_double_center=negative_double_center == T_STEP,
        half_t_is_negative_center=half_t == negative_center,
        source_contract_ok=source_profile.ok,
        trace_correct=source_profile.bridge_profile.trace_correct,
    )


def profile_reflection_anchor() -> ReflectionAnchorProfile:
    packets = tuple(
        (positive_by_row, negative_by_row, pair_permutation_packet(positive_by_row, negative_by_row))
        for positive_by_row in permutations(POSITIVE_C_AXIS)
        for negative_by_row in permutations(NEGATIVE_C_AXIS)
    )
    fixed_t_laws = tuple(
        profile_anchor_law(positive_by_row, negative_by_row)
        for positive_by_row, negative_by_row, packet in packets
        if fixed_t_edge_shape(packet)
    )
    anchor_laws = tuple(
        law
        for law in fixed_t_laws
        if law.t_is_negative_double_center and law.half_t_is_negative_center
    )
    source_laws = tuple(law for law in fixed_t_laws if law.source_contract_ok)
    rigidity = profile_row_pair_permutation_rigidity()
    target_law = anchor_laws[0]
    all_share_midpoint = {law.center_c_axis_midpoint for law in fixed_t_laws} == {28}
    c_axis_insufficient = all_share_midpoint and len(fixed_t_laws) == 3
    anchor_selects_target = (
        len(anchor_laws) == 1
        and len(source_laws) == 1
        and target_law == source_laws[0]
        and target_law.center == (2, 28)
        and target_law.base == (1, 25)
        and target_law.negative_double_center == T_STEP
        and target_law.half_t == (1, 141)
        and target_law.negative_center == (1, 141)
        and target_law.source_contract_ok
        and target_law.trace_correct
    )
    row_ok = (
        C_ORDER == 169
        and QUOTIENT_RIGHT_ORDER == 3
        and rigidity.row_ok
        and len(packets) == 36
        and sum(int(d_segment_t_edge_shape(packet)) for _pos, _neg, packet in packets) == 9
        and sum(int(fixed_t_edge_shape(packet)) for _pos, _neg, packet in packets) == 3
        and tuple(
            (
                law.center,
                law.negative_double_center,
                law.t_is_negative_double_center,
                law.source_contract_ok,
            )
            for law in fixed_t_laws
        )
        == (
            ((1, 28), (1, 113), False, False),
            ((0, 28), (0, 113), False, False),
            ((2, 28), (2, 113), True, True),
        )
        and all_share_midpoint
        and c_axis_insufficient
        and anchor_selects_target
    )
    return ReflectionAnchorProfile(
        permutations_scanned=len(packets),
        d_segment_t_edge_hits=sum(int(d_segment_t_edge_shape(packet)) for _pos, _neg, packet in packets),
        fixed_t_edge_hits=len(fixed_t_laws),
        fixed_t_anchor_laws=fixed_t_laws,
        reflection_anchor_hits=len(anchor_laws),
        source_contract_hits=len(source_laws),
        trace_correct_hits=sum(int(law.trace_correct) for law in fixed_t_laws),
        target_anchor_law=target_law,
        all_fixed_t_laws_share_c_axis_midpoint=all_share_midpoint,
        c_axis_midpoint_alone_is_insufficient=c_axis_insufficient,
        reflection_anchor_selects_unique_target=anchor_selects_target,
        recommendation=(
            "a theorem source must recover the row of the anti-invariant "
            "center C=-T/2, not only the C-axis midpoint c=28 or fixed T"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang reflection-anchor gate")
    profile = profile_reflection_anchor()
    print(f"reflection_anchor_profile={profile}")
    print("anchor_scan")
    print(f"  permutations_scanned={profile.permutations_scanned}")
    print(f"  d_segment_t_edge_hits={profile.d_segment_t_edge_hits}")
    print(f"  fixed_t_edge_hits={profile.fixed_t_edge_hits}")
    print(f"  reflection_anchor_hits={profile.reflection_anchor_hits}")
    print(f"  source_contract_hits={profile.source_contract_hits}")
    print(f"  trace_correct_hits={profile.trace_correct_hits}")
    print("fixed_T_centers")
    for law in profile.fixed_t_anchor_laws:
        print(
            "  "
            f"positive_by_row={law.positive_by_row} "
            f"negative_by_row={law.negative_by_row} "
            f"center={law.center} -2C={law.negative_double_center} "
            f"T=-2C={int(law.t_is_negative_double_center)} "
            f"source_ok={int(law.source_contract_ok)}"
        )
    print("target_anchor")
    print(f"  base={profile.target_anchor_law.base}")
    print(f"  center={profile.target_anchor_law.center}")
    print(f"  half_T={profile.target_anchor_law.half_t}")
    print(f"  negative_center={profile.target_anchor_law.negative_center}")
    print("interpretation")
    print("  all_fixed_T_translates_share_C_axis_midpoint_c28=1")
    print("  C_axis_midpoint_alone_is_insufficient=1")
    print("  reflection_anchor_T_equals_negative_2C_selects_unique_target=1")
    print(
        "robert_ksy_theta2_kubert_lang_reflection_anchor_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_reflection_anchor_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
