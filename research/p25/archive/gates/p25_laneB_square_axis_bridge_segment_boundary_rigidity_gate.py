#!/usr/bin/env python3
"""Boundary rigidity for the p25 square-axis bridge D segment.

The character-coset obstruction says the bridge graph is not a simple
character selector.  This gate records the complementary divisor-style
obstruction: if a producer obtains the positive bridge layer as a sparse
first-difference boundary, the boundary direction is forced to be the D
direction, up to the trace kernel in the raw lift.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_trace_rectangle_gate import (
    D_RAW_STEP,
    KERNEL_RAW_STEP,
    POSITIVE_BASE,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER


@dataclass(frozen=True)
class BoundaryProfile:
    name: str
    group_order: int
    support_size: int
    direction_count: int
    support_distribution: tuple[tuple[int, int], ...]
    zero_boundary_directions: tuple[int, ...]
    minimal_nonzero_support: int
    minimal_nonzero_directions: tuple[int, ...]
    second_support: int
    second_support_directions: tuple[int, ...]
    off_minimum_support: int


def translate(values: set[int], shift: int, order: int) -> set[int]:
    return {(value + shift) % order for value in values}


def boundary_support(values: set[int], shift: int, order: int) -> int:
    return len(values ^ translate(values, shift, order))


def positive_quotient_segment() -> set[int]:
    return {
        (POSITIVE_BASE + index * D_RAW_STEP) % QUOTIENT_ORDER
        for index in range(3)
    }


def positive_raw_trace_rectangle() -> set[int]:
    return {
        (POSITIVE_BASE + d_index * D_RAW_STEP + kernel_index * KERNEL_RAW_STEP) % RAW_ORDER
        for d_index in range(3)
        for kernel_index in range(25)
    }


def profile_for(name: str, values: set[int], order: int) -> BoundaryProfile:
    support_by_direction = {
        direction: boundary_support(values, direction, order)
        for direction in range(1, order)
    }
    distribution = tuple(sorted(Counter(support_by_direction.values()).items()))
    zero_directions = tuple(
        direction for direction, support in support_by_direction.items() if support == 0
    )
    nonzero_supports = sorted({support for support in support_by_direction.values() if support})
    minimal = nonzero_supports[0]
    second = nonzero_supports[1]
    minimal_directions = tuple(
        direction for direction, support in support_by_direction.items() if support == minimal
    )
    second_directions = tuple(
        direction for direction, support in support_by_direction.items() if support == second
    )
    off_minimum = min(
        support
        for direction, support in support_by_direction.items()
        if support and direction not in set(minimal_directions)
    )
    return BoundaryProfile(
        name=name,
        group_order=order,
        support_size=len(values),
        direction_count=order - 1,
        support_distribution=distribution,
        zero_boundary_directions=zero_directions,
        minimal_nonzero_support=minimal,
        minimal_nonzero_directions=minimal_directions,
        second_support=second,
        second_support_directions=second_directions,
        off_minimum_support=off_minimum,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge segment-boundary rigidity gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} raw_order={RAW_ORDER} "
        f"D={D_RAW_STEP} kernel={KERNEL_RAW_STEP} base={POSITIVE_BASE}"
    )
    quotient = positive_quotient_segment()
    raw = positive_raw_trace_rectangle()
    profiles = (
        profile_for("visible_C507_D_segment", quotient, QUOTIENT_ORDER),
        profile_for("raw_C12675_trace_rectangle", raw, RAW_ORDER),
    )
    expected = (
        BoundaryProfile(
            "visible_C507_D_segment",
            507,
            3,
            506,
            ((2, 2), (4, 2), (6, 502)),
            (),
            2,
            (172, 335),
            4,
            (163, 344),
            4,
        ),
        BoundaryProfile(
            "raw_C12675_trace_rectangle",
            12675,
            75,
            12674,
            ((0, 24), (50, 50), (100, 50), (150, 12550)),
            tuple(kernel_index * KERNEL_RAW_STEP for kernel_index in range(1, 25)),
            50,
            tuple(
                sorted(
                    {
                        (sign * D_RAW_STEP + kernel_index * KERNEL_RAW_STEP) % RAW_ORDER
                        for sign in (1, -1)
                        for kernel_index in range(25)
                    }
                )
            ),
            100,
            tuple(
                sorted(
                    {
                        (sign * 2 * D_RAW_STEP + kernel_index * KERNEL_RAW_STEP) % RAW_ORDER
                        for sign in (1, -1)
                        for kernel_index in range(25)
                    }
                )
            ),
            100,
        ),
    )
    row_ok = profiles == expected

    print("boundary_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("boundary_laws")
    print("  visible quotient: only +/-D gives a two-point endpoint boundary")
    print("  raw lift: pure kernel shifts give zero boundary because of trace invariance")
    print("  raw lift: only +/-D plus a kernel shift gives the minimal nonzero 50-point boundary")
    print("  every off-D raw direction has boundary support at least 100")
    print("interpretation")
    print("  bridge_D_segment_boundary_direction_is_forced_in_the_visible_quotient=1")
    print("  raw_trace_rectangle_boundary_direction_is_forced_modulo_kernel=1")
    print("  sparse_divisor_or_modular_unit_boundary_candidates_must_use_D_not_an_unrelated_direction=1")
    print("  kernel_trace_invariance_is_the_only_zero_boundary_escape=1")
    print(f"square_axis_bridge_segment_boundary_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_segment_boundary_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
