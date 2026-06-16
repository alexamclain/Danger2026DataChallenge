#!/usr/bin/env python3
"""Robert bridge-edge quotient contract for the p25 source matrix.

The oriented-phase gate says the bridge signs are a C-side odd phase on the
active support, while the character obstruction says that phase is not a plain
C_169 character.  This gate records the sharper quotient/divisor shape that a
Robert/Siegel producer has to realize.

After the 25-point kernel trace and the 3-point D-segment are in place, the
negative bridge layer is the positive layer translated by a single edge class:

    U = (2, 113) in C_3 x C_169.

On the raw source C_75 x C_169 this has 25 representatives, because adding the
kernel trace shift K=(57,0) does not change the product.  The recorded formal
representative T=(38,113) is one of them.  Pure C-side or pure right-side
edges fail: the orientation is a divisor/unit quotient edge coupled to the
D/K support, not a same-row C character or row-only tag.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_source_matrix_harness_gate import source_matrix_from_raw
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    edge_factor,
    geometric_factor,
    monomial,
    multiply_factors,
    source_mask_to_raw,
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


@dataclass(frozen=True)
class BridgeEdgeQuotientProfile:
    positive_support: int
    negative_support: int
    raw_positive_to_negative_translates: tuple[Coord, ...]
    raw_translates_equal_bridge_shift_mod_kernel: bool
    recorded_bridge_shift_is_representative: bool
    quotient_edge_class: Coord
    quotient_edge_order: int
    raw_recorded_edge_order: int
    visible_positive_segment: tuple[Coord, ...]
    visible_negative_segment: tuple[Coord, ...]
    visible_negative_is_positive_plus_edge: bool
    same_row_c_differences: tuple[tuple[int, int], ...]
    pure_c_edge_is_rejected_structurally: bool
    pure_right_edge_is_rejected_structurally: bool
    representative_profiles: tuple[CandidateProfile, ...]


def source_index(right_log: int, c_log: int) -> int:
    return right_log * C_ORDER + c_log


def add_coord(left: Coord, right: Coord, moduli: Coord = (RIGHT_ORDER, C_ORDER)) -> Coord:
    return (
        (left[0] + right[0]) % moduli[0],
        (left[1] + right[1]) % moduli[1],
    )


def scale_coord(step: Coord, scale: int, moduli: Coord = (RIGHT_ORDER, C_ORDER)) -> Coord:
    return ((step[0] * scale) % moduli[0], (step[1] * scale) % moduli[1])


def additive_order(step: Coord, moduli: Coord) -> int:
    current = (0, 0)
    for order in range(1, moduli[0] * moduli[1] + 1):
        current = add_coord(current, step, moduli)
        if current == (0, 0):
            return order
    raise AssertionError(f"failed to find additive order for {step} modulo {moduli}")


def signed_cells(sign: int) -> set[Coord]:
    matrix = source_matrix_from_raw(target_raw_bridge())
    out = set()
    for right_log in range(RIGHT_ORDER):
        for c_log in range(C_ORDER):
            value = matrix[source_index(right_log, c_log)]
            if sign * value > 0:
                out.add((right_log, c_log))
    return out


def translate_cells(cells: set[Coord], step: Coord) -> set[Coord]:
    return {add_coord(cell, step) for cell in cells}


def positive_to_negative_translates(positive: set[Coord], negative: set[Coord]) -> tuple[Coord, ...]:
    out = []
    for right_step in range(RIGHT_ORDER):
        for c_step in range(C_ORDER):
            step = (right_step, c_step)
            if step != (0, 0) and translate_cells(positive, step) == negative:
                out.append(step)
    return tuple(out)


def kernel_translate_class(step: Coord) -> tuple[Coord, ...]:
    return tuple(sorted(add_coord(step, scale_coord(KERNEL_SHIFT, index)) for index in range(25)))


def visible_cells(cells: set[Coord]) -> tuple[Coord, ...]:
    return tuple(sorted({(right_log % 3, c_log) for right_log, c_log in cells}))


def same_row_c_differences(positive: set[Coord], negative: set[Coord]) -> tuple[tuple[int, int], ...]:
    counts: Counter[int] = Counter()
    for right_log in range(RIGHT_ORDER):
        positives = [c_log for row, c_log in positive if row == right_log]
        negatives = [c_log for row, c_log in negative if row == right_log]
        for positive_c in positives:
            for negative_c in negatives:
                counts[(negative_c - positive_c) % C_ORDER] += 1
    return tuple(sorted(counts.items()))


def formal_edge_profile(name: str, edge_step: Coord) -> CandidateProfile:
    factors = (
        ("base", monomial(BASE_POINT)),
        ("kernel_trace", geometric_factor(KERNEL_SHIFT, 25)),
        ("D_segment", geometric_factor(D_SHIFT, 3)),
        ("edge", edge_factor(edge_step)),
    )
    raw = source_mask_to_raw(multiply_factors(factors))
    target = target_raw_bridge()
    return profile_candidate(name, raw, target)


def bridge_edge_quotient_profile() -> BridgeEdgeQuotientProfile:
    positive = signed_cells(1)
    negative = signed_cells(-1)
    translates = positive_to_negative_translates(positive, negative)
    quotient_edge = (BRIDGE_SHIFT[0] % 3, BRIDGE_SHIFT[1])
    visible_positive = visible_cells(positive)
    visible_negative = visible_cells(negative)
    visible_positive_plus_edge = tuple(
        sorted(add_coord(cell, quotient_edge, (3, C_ORDER)) for cell in visible_positive)
    )
    representative_profiles = (
        formal_edge_profile("quotient_edge_representative_(2,113)", quotient_edge),
        formal_edge_profile("recorded_raw_bridge_edge_(38,113)", BRIDGE_SHIFT),
        formal_edge_profile("pure_C_edge_(0,113)", (0, BRIDGE_SHIFT[1])),
        formal_edge_profile("pure_right_edge_(38,0)", (BRIDGE_SHIFT[0], 0)),
    )
    return BridgeEdgeQuotientProfile(
        positive_support=len(positive),
        negative_support=len(negative),
        raw_positive_to_negative_translates=translates,
        raw_translates_equal_bridge_shift_mod_kernel=translates == kernel_translate_class(BRIDGE_SHIFT),
        recorded_bridge_shift_is_representative=BRIDGE_SHIFT in translates,
        quotient_edge_class=quotient_edge,
        quotient_edge_order=additive_order(quotient_edge, (3, C_ORDER)),
        raw_recorded_edge_order=additive_order(BRIDGE_SHIFT, (RIGHT_ORDER, C_ORDER)),
        visible_positive_segment=visible_positive,
        visible_negative_segment=visible_negative,
        visible_negative_is_positive_plus_edge=visible_negative == visible_positive_plus_edge,
        same_row_c_differences=same_row_c_differences(positive, negative),
        pure_c_edge_is_rejected_structurally=(0, BRIDGE_SHIFT[1]) not in translates,
        pure_right_edge_is_rejected_structurally=(BRIDGE_SHIFT[0], 0) not in translates,
        representative_profiles=representative_profiles,
    )


def main() -> int:
    print("p25 Lane B Robert bridge-edge quotient contract gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile = bridge_edge_quotient_profile()
    by_name = {candidate.name: candidate for candidate in profile.representative_profiles}
    expected_translates = tuple((right_log, 113) for right_log in range(2, RIGHT_ORDER, 3))
    row_ok = (
        profile.positive_support == 75
        and profile.negative_support == 75
        and profile.raw_positive_to_negative_translates == expected_translates
        and profile.raw_translates_equal_bridge_shift_mod_kernel
        and profile.recorded_bridge_shift_is_representative
        and profile.quotient_edge_class == (2, 113)
        and profile.quotient_edge_order == 507
        and profile.raw_recorded_edge_order == 12675
        and profile.visible_positive_segment == ((0, 31), (1, 25), (2, 28))
        and profile.visible_negative_segment == ((0, 138), (1, 141), (2, 144))
        and profile.visible_negative_is_positive_plus_edge
        and profile.same_row_c_differences == ((107, 25), (116, 50))
        and profile.pure_c_edge_is_rejected_structurally
        and profile.pure_right_edge_is_rejected_structurally
        and by_name["quotient_edge_representative_(2,113)"].ok
        and by_name["recorded_raw_bridge_edge_(38,113)"].ok
        and not by_name["pure_C_edge_(0,113)"].ok
        and not by_name["pure_right_edge_(38,0)"].ok
    )

    print(f"bridge_edge_quotient_profile={profile}")
    print("representative_profiles")
    for candidate in profile.representative_profiles:
        print(f"  {candidate}")
    print("quotient_edge_contract")
    print("  positive_layer + (2,113) in C3xC169 equals the negative layer")
    print("  raw representatives are exactly T plus the 25-point kernel trace class")
    print("  the edge has primitive quotient order 507 and primitive raw order 12675")
    print("  pure C-side and pure right-side edges fail the source-matrix harness")
    print("interpretation")
    print("  robert_divisor_or_unit_quotient_must_supply_the_coupled_bridge_edge_class=1")
    print("  orientation_is_a_non_character_edge_quotient_not_a_same_row_C_phase=1")
    print(f"robert_bridge_edge_quotient_contract_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_bridge_edge_quotient_contract_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
