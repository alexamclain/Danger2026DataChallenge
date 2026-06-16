#!/usr/bin/env python3
"""Raw source-axis coupling for the p25 square-axis bridge.

The trace-rectangle gate records the positive raw bridge layer as

    base + <507>_25 + {0,D,2D}

inside the raw cyclic source C_12675.  This gate rewrites that layer in the
actual split source axes C_75 x C_169.  The important point is that the support
is not an axis product.  It is a graph over the full right source axis, where
the C_169 singleton is determined by the right coordinate modulo 3.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]


@dataclass(frozen=True)
class AxisCouplingProfile:
    positive_size: int
    negative_size: int
    signed_size: int
    positive_right_projection_size: int
    positive_c_projection: tuple[int, ...]
    positive_axis_hull_size: int
    positive_axis_hull_false_positives: int
    positive_right_fiber_sizes: tuple[int, ...]
    positive_c_fiber_sizes: tuple[int, ...]
    positive_mod3_to_c: tuple[tuple[int, int], ...]
    negative_mod3_to_c: tuple[tuple[int, int], ...]
    positive_rectangles: tuple[tuple[int, int, int], ...]
    negative_rectangles: tuple[tuple[int, int, int], ...]
    signed_axis_hull_size: int
    signed_axis_hull_false_positives: int
    positive_rank_f2: int
    positive_rank_f2029: int
    signed_rank_f2: int
    signed_rank_f2029: int


def translate(points: set[Coord], shift: Coord) -> set[Coord]:
    return {
        ((right + shift[0]) % RIGHT_ORDER, (c_log + shift[1]) % C_ORDER)
        for right, c_log in points
    }


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    rows = [[value % modulus for value in row] for row in matrix]
    rank = 0
    if not rows:
        return 0
    col_count = len(rows[0])
    for col in range(col_count):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, modulus)
        rows[rank] = [(value * inv) % modulus for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank:
                continue
            factor = rows[row][col] % modulus
            if factor:
                rows[row] = [
                    (rows[row][idx] - factor * rows[rank][idx]) % modulus
                    for idx in range(col_count)
                ]
        rank += 1
    return rank


def matrix_for(mask: dict[Coord, int], modulus: int) -> list[list[int]]:
    return [
        [mask.get((right, c_log), 0) % modulus for c_log in range(C_ORDER)]
        for right in range(RIGHT_ORDER)
    ]


def positive_trace_rectangles(base: Coord) -> tuple[tuple[int, int, int], ...]:
    """Return (right_mod_3, c_log, size) for the three axis rectangles."""

    rectangles: list[tuple[int, int, int]] = []
    for d_index in range(RIGHT_DEGREE):
        right_mod = (base[0] + d_index * D_SHIFT[0]) % RIGHT_DEGREE
        c_log = (base[1] + d_index * D_SHIFT[1]) % C_ORDER
        rectangles.append((right_mod, c_log, RIGHT_ORDER // RIGHT_DEGREE))
    return tuple(sorted(rectangles))


def graph_law(points: set[Coord]) -> tuple[tuple[int, int], ...]:
    by_mod: dict[int, set[int]] = {right_mod: set() for right_mod in range(RIGHT_DEGREE)}
    for right, c_log in points:
        by_mod[right % RIGHT_DEGREE].add(c_log)
    return tuple(
        sorted(
            (right_mod, next(iter(c_values)))
            for right_mod, c_values in by_mod.items()
            if len(c_values) == 1
        )
    )


def axis_coupling_profile() -> AxisCouplingProfile:
    signed = raw_source_mask()
    positive = {coord for coord, value in signed.items() if value == 1}
    negative = {coord for coord, value in signed.items() if value == -1}
    positive_right_projection = {right for right, _c_log in positive}
    positive_c_projection = {c_log for _right, c_log in positive}
    signed_right_projection = {right for right, _c_log in signed}
    signed_c_projection = {c_log for _right, c_log in signed}

    positive_axis_hull_size = len(positive_right_projection) * len(positive_c_projection)
    signed_axis_hull_size = len(signed_right_projection) * len(signed_c_projection)

    positive_right_fiber_sizes = tuple(
        sorted(
            len({c_log for r_value, c_log in positive if r_value == right})
            for right in positive_right_projection
        )
    )
    positive_c_fiber_sizes = tuple(
        sorted(
            len({right for right, c_value in positive if c_value == c_log})
            for c_log in positive_c_projection
        )
    )

    positive_mask = {coord: 1 for coord in positive}
    return AxisCouplingProfile(
        positive_size=len(positive),
        negative_size=len(negative),
        signed_size=len(signed),
        positive_right_projection_size=len(positive_right_projection),
        positive_c_projection=tuple(sorted(positive_c_projection)),
        positive_axis_hull_size=positive_axis_hull_size,
        positive_axis_hull_false_positives=positive_axis_hull_size - len(positive),
        positive_right_fiber_sizes=positive_right_fiber_sizes,
        positive_c_fiber_sizes=positive_c_fiber_sizes,
        positive_mod3_to_c=graph_law(positive),
        negative_mod3_to_c=graph_law(negative),
        positive_rectangles=positive_trace_rectangles(BASE_POINT),
        negative_rectangles=positive_trace_rectangles(
            (
                (BASE_POINT[0] + BRIDGE_SHIFT[0]) % RIGHT_ORDER,
                (BASE_POINT[1] + BRIDGE_SHIFT[1]) % C_ORDER,
            )
        ),
        signed_axis_hull_size=signed_axis_hull_size,
        signed_axis_hull_false_positives=signed_axis_hull_size - len(signed),
        positive_rank_f2=rank_mod(matrix_for(positive_mask, 2), 2),
        positive_rank_f2029=rank_mod(matrix_for(positive_mask, 2029), 2029),
        signed_rank_f2=rank_mod(matrix_for(signed, 2), 2),
        signed_rank_f2029=rank_mod(matrix_for(signed, 2029), 2029),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge source-axis coupling gate")
    print(
        f"raw_source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} kernel={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    signed = raw_source_mask()
    positive = {coord for coord, value in signed.items() if value == 1}
    expected_positive = {
        (
            (BASE_POINT[0] + d_index * D_SHIFT[0] + kernel_index * KERNEL_SHIFT[0]) % RIGHT_ORDER,
            (BASE_POINT[1] + d_index * D_SHIFT[1] + kernel_index * KERNEL_SHIFT[1]) % C_ORDER,
        )
        for d_index in range(RIGHT_DEGREE)
        for kernel_index in range(25)
    }
    expected_negative = translate(expected_positive, BRIDGE_SHIFT)
    profile = axis_coupling_profile()
    expected = AxisCouplingProfile(
        positive_size=75,
        negative_size=75,
        signed_size=150,
        positive_right_projection_size=75,
        positive_c_projection=(25, 28, 31),
        positive_axis_hull_size=225,
        positive_axis_hull_false_positives=150,
        positive_right_fiber_sizes=(1,) * 75,
        positive_c_fiber_sizes=(25, 25, 25),
        positive_mod3_to_c=((0, 31), (1, 25), (2, 28)),
        negative_mod3_to_c=((0, 138), (1, 141), (2, 144)),
        positive_rectangles=((0, 31, 25), (1, 25, 25), (2, 28, 25)),
        negative_rectangles=((0, 138, 25), (1, 141, 25), (2, 144, 25)),
        signed_axis_hull_size=450,
        signed_axis_hull_false_positives=300,
        positive_rank_f2=3,
        positive_rank_f2029=3,
        signed_rank_f2=3,
        signed_rank_f2029=3,
    )
    row_ok = (
        positive == expected_positive
        and {coord for coord, value in signed.items() if value == -1} == expected_negative
        and KERNEL_SHIFT == (57, 0)
        and D_SHIFT == (22, 3)
        and D_SHIFT[0] % RIGHT_DEGREE == 1
        and D_SHIFT[1] == 3
        and profile == expected
    )

    print(f"axis_coupling_profile={profile}")
    print("source_axis_normal_form")
    print("  positive layer = union over i=0,1,2 of {right == 25 + 22*i mod 3} x {c = 25 + 3*i}")
    print("  equivalently, positive c is a graph of right mod 3")
    print("  negative layer is the bridge translate with the same coupled graph shape")
    print("separation_falsifier")
    print("  positive right projection has all 75 right-source values")
    print("  positive C projection has only 3 C-source values")
    print("  the axis product hull has 225 cells, with 150 false positives")
    print("  the signed axis product hull has 450 cells, with 300 false positives")
    print("interpretation")
    print("  raw_bridge_trace_rectangle_is_axis_coupled_not_axis_product=1")
    print("  producer_must_tie_the_three_C_values_to_right_mod_3=1")
    print("  kernel_trace_without_D_segment_alignment_overproduces_by_factor_3=1")
    print("  bridge_candidate_must_recover_three_right_kernel_cosets_with_their_C_singletons=1")
    print(f"square_axis_bridge_axis_coupling_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_axis_coupling_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
