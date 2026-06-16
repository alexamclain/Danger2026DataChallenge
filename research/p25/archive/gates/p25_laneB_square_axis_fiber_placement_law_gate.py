#!/usr/bin/env python3
"""Square-axis fiber-placement law for p25 Lane B.

The square-axis fiber-alphabet gate compresses the C_169 target to six length-13
fiber words.  This gate records the exact placement law for those words.

Write the C_169 coordinate as j = a + 13*b.  For each right row r and C_13
residue a, set

    h = r - a mod 3.

The b-fiber is the C_13 half-arc row h.  If the C_13 trace-shadow bit at
(r,a) is 1, the fiber gets one additional boundary bit at position

    9 - 3*h.

So the square-axis target is a C_13 trace-shadow decorated by a deterministic
13-adic boundary injection.  A producer can be tested against this compact law
instead of an opaque 507-point mask.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_selected_defect_value_gate import RIGHT_DEGREE


BASE_C = 13
SQUARE_C = BASE_C * BASE_C


@dataclass(frozen=True)
class PlacementProfile:
    placement_hits: int
    placement_total: int
    h_counts: tuple[int, int, int]
    zero_trace_unmodified_hits: int
    zero_trace_total: int
    one_trace_boundary_hits: int
    one_trace_total: int
    boundary_positions: tuple[int, int, int]


def base_row(h_value: int) -> tuple[int, ...]:
    return tuple(template_bits(BASE_C, fiber)[h_value] for fiber in range(BASE_C))


def square_fiber(right: int, residue: int) -> tuple[int, ...]:
    return tuple(
        template_bits(SQUARE_C, residue + BASE_C * fiber)[right]
        for fiber in range(BASE_C)
    )


def predicted_fiber(right: int, residue: int) -> tuple[int, ...]:
    h_value = (right - residue) % RIGHT_DEGREE
    trace_bit = template_bits(BASE_C, residue)[right]
    out = list(base_row(h_value))
    if trace_bit:
        out[9 - 3 * h_value] = 1
    return tuple(out)


def profile() -> PlacementProfile:
    placement_hits = 0
    h_counts = [0, 0, 0]
    zero_trace_unmodified_hits = 0
    zero_trace_total = 0
    one_trace_boundary_hits = 0
    one_trace_total = 0
    boundary_positions = (9, 6, 3)
    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            h_value = (right - residue) % RIGHT_DEGREE
            trace_bit = template_bits(BASE_C, residue)[right]
            observed = square_fiber(right, residue)
            predicted = predicted_fiber(right, residue)
            h_counts[h_value] += 1
            placement_hits += int(observed == predicted)
            if trace_bit:
                one_trace_total += 1
                boundary = boundary_positions[h_value]
                without_boundary = list(observed)
                without_boundary[boundary] = 0
                one_trace_boundary_hits += int(
                    observed[boundary] == 1
                    and tuple(without_boundary) == base_row(h_value)
                )
            else:
                zero_trace_total += 1
                zero_trace_unmodified_hits += int(observed == base_row(h_value))
    return PlacementProfile(
        placement_hits=placement_hits,
        placement_total=RIGHT_DEGREE * BASE_C,
        h_counts=tuple(h_counts),
        zero_trace_unmodified_hits=zero_trace_unmodified_hits,
        zero_trace_total=zero_trace_total,
        one_trace_boundary_hits=one_trace_boundary_hits,
        one_trace_total=one_trace_total,
        boundary_positions=boundary_positions,
    )


def main() -> int:
    print("p25 Lane B square-axis fiber-placement law gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C}")
    current = profile()
    row_ok = (
        current.placement_hits == current.placement_total
        and current.h_counts == (13, 13, 13)
        and current.zero_trace_unmodified_hits == current.zero_trace_total == 21
        and current.one_trace_boundary_hits == current.one_trace_total == 18
        and current.boundary_positions == (9, 6, 3)
    )
    print(
        f"case square_axis_C3xC169: "
        f"placement_hits={current.placement_hits}/{current.placement_total} "
        f"h_counts={list(current.h_counts)} "
        f"zero_trace_unmodified_hits={current.zero_trace_unmodified_hits}/{current.zero_trace_total} "
        f"one_trace_boundary_hits={current.one_trace_boundary_hits}/{current.one_trace_total} "
        f"boundary_positions_by_h={list(current.boundary_positions)} "
        f"ok={int(row_ok)}"
    )
    print("law")
    print("  h = right - residue mod 3")
    print("  fiber = C13_half_arc_row[h]")
    print("  if C13_trace_bit(right,residue)=1: set fiber[9 - 3*h] = 1")
    print(f"square_axis_fiber_placement_law_rows={int(row_ok)}/1")
    print("interpretation")
    print("  C169_six_word_alphabet_has_exact_trace_shadow_placement_law=1")
    print("  zero_trace_slots_are_unmodified_C13_half_arc_rows=1")
    print("  one_trace_slots_are_single_boundary_bit_injections=1")
    print("  square_axis_producer_target_is_a_deterministic_13_adic_boundary_refinement=1")
    print("conclusion=reported_p25_laneB_square_axis_fiber_placement_law_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
