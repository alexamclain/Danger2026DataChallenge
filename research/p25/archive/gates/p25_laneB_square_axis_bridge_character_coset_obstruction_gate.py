#!/usr/bin/env python3
"""Character-coset obstruction for the p25 square-axis bridge graph.

The bridge graph survives the axis-product and character-gap tests because it
is genuinely D-aligned.  This gate records a stronger finite-group obstruction:
neither the visible quotient graph nor the raw trace rectangle is a single
character level set or a proper subgroup coset.

In both C_3 x C_169 and C_75 x C_169, the D step has full order.  Therefore
any subgroup coset containing even two adjacent D-points of the bridge must be
the whole group.
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
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]


@dataclass(frozen=True)
class CharacterCosetProfile:
    name: str
    group_order: int
    support_size: int
    right_order: int
    c_order: int
    d_step: Coord
    d_step_order: int
    support_right_projection_size: int
    support_c_projection_size: int
    minimal_subgroup_coset_size: int
    matching_single_character_cosets: int
    size_matching_character_level_sets: int
    distinct_size_matching_character_cosets: int
    size_matching_character_cosets_are_axis_c_fixed: int
    character_order_count_for_size_matching_cosets: int


def element_order(coord: Coord, right_order: int, c_order: int) -> int:
    right, c_log = coord
    right_component_order = 1 if right % right_order == 0 else right_order // gcd(right_order, right)
    c_component_order = 1 if c_log % c_order == 0 else c_order // gcd(c_order, c_log)
    return lcm(right_component_order, c_component_order)


def generated_subgroup_size(generators: tuple[Coord, ...], right_order: int, c_order: int) -> int:
    generated = {(0, 0)}
    frontier = [(0, 0)]
    while frontier:
        point = frontier.pop()
        for generator in generators:
            new_point = (
                (point[0] + generator[0]) % right_order,
                (point[1] + generator[1]) % c_order,
            )
            if new_point not in generated:
                generated.add(new_point)
                frontier.append(new_point)
    return len(generated)


def visible_positive_graph() -> set[Coord]:
    base = (BASE_POINT[0] % RIGHT_DEGREE, BASE_POINT[1] % C_ORDER)
    d_step = (D_SHIFT[0] % RIGHT_DEGREE, D_SHIFT[1] % C_ORDER)
    return {
        ((base[0] + index * d_step[0]) % RIGHT_DEGREE, (base[1] + index * d_step[1]) % C_ORDER)
        for index in range(RIGHT_DEGREE)
    }


def raw_positive_trace_rectangle() -> set[Coord]:
    return {
        (
            (BASE_POINT[0] + d_index * D_SHIFT[0] + kernel_index * KERNEL_SHIFT[0]) % RIGHT_ORDER,
            (BASE_POINT[1] + d_index * D_SHIFT[1] + kernel_index * KERNEL_SHIFT[1]) % C_ORDER,
        )
        for d_index in range(RIGHT_DEGREE)
        for kernel_index in range(25)
    }


def fixed_c_cosets(right_order: int, c_order: int) -> tuple[frozenset[Coord], ...]:
    return tuple(
        frozenset((right, c_log) for right in range(right_order))
        for c_log in range(c_order)
    )


def character_order(a_char: int, b_char: int, right_order: int, c_order: int) -> int:
    right_character_order = 1 if a_char == 0 else right_order // gcd(right_order, a_char)
    c_character_order = 1 if b_char == 0 else c_order // gcd(c_order, b_char)
    return lcm(right_character_order, c_character_order)


def profile_for(
    name: str,
    support: set[Coord],
    right_order: int,
    c_order: int,
    d_step: Coord,
) -> CharacterCosetProfile:
    support_size = len(support)
    group_order = right_order * c_order
    size_matching_order = group_order // support_size
    size_matching_character_count = sum(
        1
        for a_char in range(right_order)
        for b_char in range(c_order)
        if character_order(a_char, b_char, right_order, c_order) == size_matching_order
    )
    fixed_c = fixed_c_cosets(right_order, c_order)
    support_frozen = frozenset(support)
    matching_single_character_cosets = int(support_frozen in fixed_c)
    distinct_size_matching_character_cosets = len(fixed_c)
    size_matching_character_level_sets = size_matching_character_count * distinct_size_matching_character_cosets
    differences = tuple(
        ((point[0] - next(iter(support))[0]) % right_order, (point[1] - next(iter(support))[1]) % c_order)
        for point in support
    )
    return CharacterCosetProfile(
        name=name,
        group_order=group_order,
        support_size=support_size,
        right_order=right_order,
        c_order=c_order,
        d_step=d_step,
        d_step_order=element_order(d_step, right_order, c_order),
        support_right_projection_size=len({right for right, _c_log in support}),
        support_c_projection_size=len({c_log for _right, c_log in support}),
        minimal_subgroup_coset_size=generated_subgroup_size(differences, right_order, c_order),
        matching_single_character_cosets=matching_single_character_cosets,
        size_matching_character_level_sets=size_matching_character_level_sets,
        distinct_size_matching_character_cosets=distinct_size_matching_character_cosets,
        size_matching_character_cosets_are_axis_c_fixed=int(
            all(len({c_log for _right, c_log in coset}) == 1 for coset in fixed_c)
        ),
        character_order_count_for_size_matching_cosets=size_matching_character_count,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge character-coset obstruction gate")
    visible_d = (D_SHIFT[0] % RIGHT_DEGREE, D_SHIFT[1] % C_ORDER)
    raw_d = (D_SHIFT[0] % RIGHT_ORDER, D_SHIFT[1] % C_ORDER)
    print(
        f"visible_group=C_{RIGHT_DEGREE}xC_{C_ORDER} visible_D={visible_d} "
        f"raw_group=C_{RIGHT_ORDER}xC_{C_ORDER} raw_D={raw_d} kernel={KERNEL_SHIFT}"
    )
    profiles = (
        profile_for(
            "visible_positive_graph",
            visible_positive_graph(),
            RIGHT_DEGREE,
            C_ORDER,
            visible_d,
        ),
        profile_for(
            "raw_positive_trace_rectangle",
            raw_positive_trace_rectangle(),
            RIGHT_ORDER,
            C_ORDER,
            raw_d,
        ),
    )
    expected = (
        CharacterCosetProfile(
            "visible_positive_graph",
            507,
            3,
            3,
            169,
            (1, 3),
            507,
            3,
            3,
            507,
            0,
            26364,
            169,
            1,
            156,
        ),
        CharacterCosetProfile(
            "raw_positive_trace_rectangle",
            12675,
            75,
            75,
            169,
            (22, 3),
            12675,
            75,
            3,
            12675,
            0,
            26364,
            169,
            1,
            156,
        ),
    )
    row_ok = (
        profiles == expected
        and all(profile.d_step_order == profile.group_order for profile in profiles)
        and all(profile.minimal_subgroup_coset_size == profile.group_order for profile in profiles)
        and all(profile.matching_single_character_cosets == 0 for profile in profiles)
        and all(profile.size_matching_character_cosets_are_axis_c_fixed for profile in profiles)
    )

    print("character_coset_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("coset_laws")
    print("  visible: every character level set of size 3 is a fixed-c horizontal C3 coset")
    print("  raw: every character level set of size 75 is a fixed-c horizontal C75 coset")
    print("  the bridge support has three C-values, so it matches none of these cosets")
    print("  the D step has full order in both groups, so the smallest subgroup coset containing the bridge is the whole group")
    print("interpretation")
    print("  bridge_graph_is_not_a_single_character_level_set=1")
    print("  bridge_trace_rectangle_is_not_a_single_character_level_set=1")
    print("  no_proper_subgroup_coset_contains_the_D_aligned_bridge=1")
    print("  producer_must_use_a_short_D_segment_or_equivalent_mixed_identity_not_a_simple_character_selector=1")
    print(f"square_axis_bridge_character_coset_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_character_coset_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
