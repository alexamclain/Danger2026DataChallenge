#!/usr/bin/env python3
"""Square-axis fiber-alphabet gate for p25 Lane B.

The imprimitive-lift obstruction says the C_169 target is not merely pulled
back from C_13.  This gate records the positive structure left behind.

Write the C-axis coordinate as

    j = a + 13*b, with a,b in C_13.

For each fixed right row and residue a, the b-fiber is not constant, but it is
one of only six binary words of length 13.  The six words have rank 6 over both
F_2 and an odd field.  Their weights are exactly 6 plus the C_13 trace-shadow
bit, so the alphabet refines the C_13 half-arc without being a C_13 lift.

This gives a compact target for a square-axis producer: it must place the six
fiber words in the right 39 residue slots while still carrying all primitive
C_169 character support.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import rank_mod
from p25_selected_defect_value_gate import RIGHT_DEGREE


BASE_C = 13
SQUARE_C = BASE_C * BASE_C
ODD_RANK_FIELD = 1_000_003


@dataclass(frozen=True)
class FiberAlphabetProfile:
    unique_patterns: int
    pattern_weights: tuple[int, ...]
    pattern_counts: tuple[int, ...]
    rank_f2: int
    rank_odd: int
    trace_weight_hits: int
    trace_weight_total: int
    zero_trace_pattern_count: int
    one_trace_pattern_count: int


def fiber_word(right: int, residue: int) -> tuple[int, ...]:
    return tuple(
        template_bits(SQUARE_C, residue + BASE_C * fiber)[right]
        for fiber in range(BASE_C)
    )


def pattern_data() -> list[tuple[tuple[int, ...], list[tuple[int, int, int]]]]:
    by_pattern: dict[tuple[int, ...], list[tuple[int, int, int]]] = {}
    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            word = fiber_word(right, residue)
            trace_bit = template_bits(BASE_C, residue)[right]
            by_pattern.setdefault(word, []).append((right, residue, trace_bit))
    return sorted(by_pattern.items(), key=lambda item: (sum(item[0]), item[0]))


def profile() -> FiberAlphabetProfile:
    data = pattern_data()
    patterns = [list(pattern) for pattern, _cells in data]
    trace_weight_hits = 0
    trace_weight_total = 0
    zero_trace_pattern_count = 0
    one_trace_pattern_count = 0
    for pattern, cells in data:
        trace_bits = {trace_bit for _right, _residue, trace_bit in cells}
        if len(trace_bits) != 1:
            continue
        trace_bit = next(iter(trace_bits))
        zero_trace_pattern_count += int(trace_bit == 0)
        one_trace_pattern_count += int(trace_bit == 1)
        for _right, _residue, cell_trace_bit in cells:
            trace_weight_total += 1
            trace_weight_hits += int(sum(pattern) == 6 + cell_trace_bit)
    return FiberAlphabetProfile(
        unique_patterns=len(data),
        pattern_weights=tuple(sum(pattern) for pattern, _cells in data),
        pattern_counts=tuple(len(cells) for _pattern, cells in data),
        rank_f2=rank_mod(patterns, 2),
        rank_odd=rank_mod(patterns, ODD_RANK_FIELD),
        trace_weight_hits=trace_weight_hits,
        trace_weight_total=trace_weight_total,
        zero_trace_pattern_count=zero_trace_pattern_count,
        one_trace_pattern_count=one_trace_pattern_count,
    )


def main() -> int:
    print("p25 Lane B square-axis fiber-alphabet gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C}")
    current = profile()
    row_ok = (
        current.unique_patterns == 6
        and current.pattern_weights == (6, 6, 6, 7, 7, 7)
        and current.pattern_counts == (4, 7, 10, 6, 3, 9)
        and current.rank_f2 == 6
        and current.rank_odd == 6
        and current.trace_weight_hits == current.trace_weight_total == RIGHT_DEGREE * BASE_C
        and current.zero_trace_pattern_count == 3
        and current.one_trace_pattern_count == 3
    )
    print(
        f"case square_axis_C3xC169: "
        f"unique_fiber_patterns={current.unique_patterns}/6 "
        f"pattern_weights={list(current.pattern_weights)} "
        f"pattern_counts={list(current.pattern_counts)} "
        f"rank_f2={current.rank_f2} "
        f"rank_odd={current.rank_odd} "
        f"trace_weight_hits={current.trace_weight_hits}/{current.trace_weight_total} "
        f"zero_trace_pattern_count={current.zero_trace_pattern_count}/3 "
        f"one_trace_pattern_count={current.one_trace_pattern_count}/3 "
        f"ok={int(row_ok)}"
    )
    print("fiber_patterns")
    for index, (pattern, cells) in enumerate(pattern_data(), start=1):
        trace_bits = sorted({trace_bit for _right, _residue, trace_bit in cells})
        print(
            f"  P{index}: weight={sum(pattern)} count={len(cells)} "
            f"trace_bits={trace_bits} word={list(pattern)}"
        )
    print(f"square_axis_fiber_alphabet_rows={int(row_ok)}/1")
    print("interpretation")
    print("  C169_refinement_uses_six_binary_fiber_words=1")
    print("  fiber_word_weight_is_six_plus_the_C13_trace_shadow_bit=1")
    print("  six_fiber_words_have_rank_six_over_F2_and_odd_fields=1")
    print("  square_axis_producer_can_target_a_compact_fiber_alphabet=1")
    print("conclusion=reported_p25_laneB_square_axis_fiber_alphabet_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
