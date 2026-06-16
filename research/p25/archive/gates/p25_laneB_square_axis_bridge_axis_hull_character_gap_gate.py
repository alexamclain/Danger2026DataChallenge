#!/usr/bin/env python3
"""Character gap between the p25 bridge graph and its axis-product hull.

The source-axis coupling gate shows that the positive bridge layer is a graph
over right mod 3, not the product of the right trace and three C-axis values.
This gate records the dual consequence: the tempting axis-product hull has the
same pure C-character support, but it loses all mixed right/C characters.

Thus a producer cannot be a separated "right trace times C selector" local
factor.  It must create the mixed character payload coming from the D=(22,3)
alignment.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    MODULUS,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]
Mask = dict[Coord, int]


@dataclass(frozen=True)
class CharacterSupportProfile:
    name: str
    support_size: int
    nonzero_count: int
    zero_count: int
    nonzero_by_right_character: tuple[int, int, int]
    zero_by_right_character: tuple[int, int, int]
    scalar_nonzero: int
    pure_right_nonzero: int
    pure_c_nonzero: int
    mixed_nonzero: int
    all_nontrivial_c_characters_present: int


def add_mask(left: Mask, right: Mask) -> Mask:
    out = dict(left)
    for coord, value in right.items():
        out[coord] = out.get(coord, 0) + value
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def translate(mask: Mask, shift: Coord, coefficient: int = 1) -> Mask:
    return {
        ((right + shift[0]) % RIGHT_DEGREE, (c_log + shift[1]) % C_ORDER): coefficient * value
        for (right, c_log), value in mask.items()
    }


def true_positive_mask() -> Mask:
    base = (BASE_POINT[0] % RIGHT_DEGREE, BASE_POINT[1] % C_ORDER)
    d_shift = (D_SHIFT[0] % RIGHT_DEGREE, D_SHIFT[1] % C_ORDER)
    return {
        ((base[0] + index * d_shift[0]) % RIGHT_DEGREE, (base[1] + index * d_shift[1]) % C_ORDER): 1
        for index in range(RIGHT_DEGREE)
    }


def axis_hull(mask: Mask) -> Mask:
    c_values = sorted({c_log for _right, c_log in mask})
    return {
        (right, c_log): 1
        for right in range(RIGHT_DEGREE)
        for c_log in c_values
    }


def signed_from_positive(positive: Mask) -> Mask:
    bridge_shift = (BRIDGE_SHIFT[0] % RIGHT_DEGREE, BRIDGE_SHIFT[1] % C_ORDER)
    return add_mask(positive, translate(positive, bridge_shift, coefficient=-1))


def character_value(zeta_right: int, zeta_c: int, a_char: int, b_char: int, coord: Coord) -> int:
    right, c_log = coord
    return (
        pow(zeta_right, a_char * right, MODULUS)
        * pow(zeta_c, b_char * c_log, MODULUS)
    ) % MODULUS


def character_sum(mask: Mask, zeta_right: int, zeta_c: int, a_char: int, b_char: int) -> int:
    return sum(
        coefficient * character_value(zeta_right, zeta_c, a_char, b_char, coord)
        for coord, coefficient in mask.items()
    ) % MODULUS


def support_profile(name: str, mask: Mask) -> CharacterSupportProfile:
    root = primitive_root(MODULUS)
    zeta_right = pow(root, (MODULUS - 1) // RIGHT_DEGREE, MODULUS)
    zeta_c = pow(root, (MODULUS - 1) // C_ORDER, MODULUS)

    nonzero_by_a = [0, 0, 0]
    zero_by_a = [0, 0, 0]
    scalar_nonzero = 0
    pure_right_nonzero = 0
    pure_c_nonzero = 0
    mixed_nonzero = 0
    for a_char in range(RIGHT_DEGREE):
        for b_char in range(C_ORDER):
            total = character_sum(mask, zeta_right, zeta_c, a_char, b_char)
            if total:
                nonzero_by_a[a_char] += 1
                if a_char == 0 and b_char == 0:
                    scalar_nonzero += 1
                elif b_char == 0:
                    pure_right_nonzero += 1
                elif a_char == 0:
                    pure_c_nonzero += 1
                else:
                    mixed_nonzero += 1
            else:
                zero_by_a[a_char] += 1

    nonzero_count = sum(nonzero_by_a)
    all_nontrivial_c = int(pure_c_nonzero == C_ORDER - 1)
    return CharacterSupportProfile(
        name=name,
        support_size=len(mask),
        nonzero_count=nonzero_count,
        zero_count=RIGHT_DEGREE * C_ORDER - nonzero_count,
        nonzero_by_right_character=tuple(nonzero_by_a),
        zero_by_right_character=tuple(zero_by_a),
        scalar_nonzero=scalar_nonzero,
        pure_right_nonzero=pure_right_nonzero,
        pure_c_nonzero=pure_c_nonzero,
        mixed_nonzero=mixed_nonzero,
        all_nontrivial_c_characters_present=all_nontrivial_c,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge axis-hull character-gap gate")
    print(
        f"quotient_source_group=C_{RIGHT_DEGREE}xC_{C_ORDER} "
        f"field={MODULUS} base=({BASE_POINT[0] % RIGHT_DEGREE},{BASE_POINT[1]}) "
        f"D=({D_SHIFT[0] % RIGHT_DEGREE},{D_SHIFT[1]}) "
        f"T=({BRIDGE_SHIFT[0] % RIGHT_DEGREE},{BRIDGE_SHIFT[1]})"
    )
    positive = true_positive_mask()
    positive_hull = axis_hull(positive)
    signed = signed_from_positive(positive)
    signed_hull = signed_from_positive(positive_hull)

    profiles = (
        support_profile("true_positive_graph", positive),
        support_profile("positive_axis_product_hull", positive_hull),
        support_profile("true_signed_bridge", signed),
        support_profile("signed_axis_product_hull", signed_hull),
    )
    expected = (
        CharacterSupportProfile("true_positive_graph", 3, 505, 2, (169, 168, 168), (0, 1, 1), 1, 0, 168, 336, 1),
        CharacterSupportProfile("positive_axis_product_hull", 9, 169, 338, (169, 0, 0), (0, 169, 169), 1, 0, 168, 0, 1),
        CharacterSupportProfile("true_signed_bridge", 6, 504, 3, (168, 168, 168), (1, 1, 1), 0, 0, 168, 336, 1),
        CharacterSupportProfile("signed_axis_product_hull", 18, 168, 339, (168, 0, 0), (1, 169, 169), 0, 0, 168, 0, 1),
    )
    true_positive, axis_positive, true_signed, axis_signed = profiles
    row_ok = (
        profiles == expected
        and true_positive.pure_c_nonzero == axis_positive.pure_c_nonzero == C_ORDER - 1
        and true_signed.pure_c_nonzero == axis_signed.pure_c_nonzero == C_ORDER - 1
        and true_positive.mixed_nonzero - axis_positive.mixed_nonzero == 2 * (C_ORDER - 1)
        and true_signed.mixed_nonzero - axis_signed.mixed_nonzero == 2 * (C_ORDER - 1)
        and set(positive_hull) > set(positive)
        and set(signed_hull) > set(signed)
    )

    print("character_support_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("axis_hull_gap")
    print("  true positive graph and positive axis hull both have all 168 pure C characters")
    print("  positive axis hull has 0 mixed right/C characters; true graph has 336")
    print("  signed axis hull has 0 mixed right/C characters; true signed bridge has 336")
    print("  the missing 336 mixed characters are exactly the two nontrivial right characters times all nontrivial C characters")
    print("interpretation")
    print("  separated_right_trace_times_C_selector_matches_only_the_pure_C_shadow=1")
    print("  bridge_graph_requires_full_mixed_right_C_character_payload=1")
    print("  source_axis_hull_overproduces_in_support_and_underproduces_in_mixed_characters=1")
    print("  producer_must_realize_the_D_aligned_graph_not_just_axis_projections=1")
    print(f"square_axis_bridge_axis_hull_character_gap_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_axis_hull_character_gap_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
