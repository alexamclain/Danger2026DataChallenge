#!/usr/bin/env python3
"""Residue-coset mask gate for the p25 Lane B source half-arc.

The source half-arc lift gate verifies the canonical theta_{3,1} template on
the raw exponent cycle.  This gate rewrites the same target as actual residue
cosets at the local source primes.

For the first p25 lab:

    mod 151 right source: 3 quotient cosets, each of size 25;
    mod 677 C source:     13 quotient cosets, each of size 13;
    one C_3 x C_13 point: 25 * 13 = 325 residue pairs.

Thus the canonical half-arc is a union of product rectangles in the real local
residue data, not only a log-coordinate artifact.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    LocalSource,
    PullbackCase,
    P25,
    precompute_source_logs,
    quotient_coordinates,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class SourceClassSummary:
    source_name: str
    class_count: int
    class_sizes: tuple[int, ...]
    expected_class_count: int
    expected_class_size: int
    ok: bool


def source_residue_classes(
    case: PullbackCase,
    source: LocalSource,
    coordinates: list[tuple[int, int]],
) -> dict[int, set[int]]:
    generator = pow(P25, case.rho_exp, source.modulus)
    classes: dict[int, set[int]] = {}
    residue = 1
    for right_coord, c_coord in coordinates:
        key = right_coord if source in case.right_sources else c_coord
        classes.setdefault(key, set()).add(residue)
        residue = residue * generator % source.modulus
    return classes


def summarize_source(
    case: PullbackCase,
    source: LocalSource,
    coordinates: list[tuple[int, int]],
) -> SourceClassSummary:
    classes = source_residue_classes(case, source, coordinates)
    expected_class_count = RIGHT_DEGREE if source in case.right_sources else case.c_axis
    if source.expected_order % expected_class_count:
        raise AssertionError("unexpected source order")
    expected_class_size = source.expected_order // expected_class_count
    class_sizes = tuple(sorted(len(values) for values in classes.values()))
    ok = (
        len(classes) == expected_class_count
        and set(class_sizes) == {expected_class_size}
        and sum(class_sizes) == source.expected_order
    )
    return SourceClassSummary(
        source_name=source.name,
        class_count=len(classes),
        class_sizes=class_sizes,
        expected_class_count=expected_class_count,
        expected_class_size=expected_class_size,
        ok=ok,
    )


def quotient_block_counts(
    coordinates: list[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for coordinate in coordinates:
        counts[coordinate] = counts.get(coordinate, 0) + 1
    return counts


def zone_name(c_axis: int, c_index: int) -> str:
    m_value = (c_axis - 1) // 4
    if c_index <= m_value:
        return "zero"
    if c_index <= 2 * m_value:
        return "one_hot"
    if c_index <= 3 * m_value:
        return "two_hot"
    return "all_rows"


def expected_zone_lengths(c_axis: int) -> dict[str, int]:
    m_value = (c_axis - 1) // 4
    return {
        "zero": m_value + 1,
        "one_hot": m_value,
        "two_hot": m_value,
        "all_rows": m_value,
    }


def expected_carry_rectangles(c_axis: int) -> dict[str, int]:
    lengths = expected_zone_lengths(c_axis)
    return {
        "zero": 0,
        "one_hot": lengths["one_hot"],
        "two_hot": 2 * lengths["two_hot"],
        "all_rows": RIGHT_DEGREE * lengths["all_rows"],
    }


def audit_case(case: PullbackCase) -> tuple[list[str], bool]:
    source_logs = precompute_source_logs(case)
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]
    block_counts = quotient_block_counts(coordinates)
    source_summaries = [
        summarize_source(case, source, coordinates)
        for source in (*case.right_sources, case.c_source)
    ]
    residue_rectangle_size = 1
    for summary in source_summaries:
        residue_rectangle_size *= summary.expected_class_size

    carry_by_coord: dict[tuple[int, int], set[int]] = {}
    zone_rectangle_counts = {"zero": 0, "one_hot": 0, "two_hot": 0, "all_rows": 0}
    zone_carry_rectangle_counts = {
        "zero": 0,
        "one_hot": 0,
        "two_hot": 0,
        "all_rows": 0,
    }
    raw_carry_count = 0
    for right_coord, c_coord in coordinates:
        zone = zone_name(case.c_axis, c_coord)
        carry_bit = template_bits(case.c_axis, c_coord)[right_coord]
        carry_by_coord.setdefault((right_coord, c_coord), set()).add(carry_bit)
        raw_carry_count += carry_bit

    for (right_coord, c_coord), carries in carry_by_coord.items():
        if len(carries) != 1:
            continue
        carry_bit = next(iter(carries))
        zone = zone_name(case.c_axis, c_coord)
        zone_rectangle_counts[zone] += 1
        zone_carry_rectangle_counts[zone] += carry_bit

    block_constancy_hits = sum(
        int(count == case.b_trace) for count in block_counts.values()
    )
    carry_constancy_hits = sum(int(len(values) == 1) for values in carry_by_coord.values())
    expected_rectangle_count = RIGHT_DEGREE * case.c_axis
    expected_zone_rectangles = {
        name: RIGHT_DEGREE * length
        for name, length in expected_zone_lengths(case.c_axis).items()
    }
    expected_zone_carry_rectangles = expected_carry_rectangles(case.c_axis)

    row_ok = (
        len(block_counts) == expected_rectangle_count
        and block_constancy_hits == expected_rectangle_count
        and carry_constancy_hits == expected_rectangle_count
        and residue_rectangle_size == case.b_trace
        and all(summary.ok for summary in source_summaries)
        and zone_rectangle_counts == expected_zone_rectangles
        and zone_carry_rectangle_counts == expected_zone_carry_rectangles
        and raw_carry_count
        == case.b_trace * sum(expected_zone_carry_rectangles.values())
    )

    lines = [
        (
            f"case {case.name}: c={case.c_axis} B={case.b_trace} "
            f"raw_order={case.raw_order} quotient_rectangles={len(block_counts)} "
            f"expected_quotient_rectangles={expected_rectangle_count} "
            f"block_constancy_hits={block_constancy_hits}/{expected_rectangle_count} "
            f"carry_constancy_hits={carry_constancy_hits}/{expected_rectangle_count} "
            f"residue_rectangle_size={residue_rectangle_size} "
            f"raw_carry_count={raw_carry_count} "
            f"ok={int(row_ok)}"
        ),
        *[
            (
                f"  source {summary.source_name}: class_count={summary.class_count} "
                f"expected_class_count={summary.expected_class_count} "
                f"class_size_set={sorted(set(summary.class_sizes))} "
                f"expected_class_size={summary.expected_class_size} "
                f"ok={int(summary.ok)}"
            )
            for summary in source_summaries
        ],
        f"  zone_rectangle_counts={zone_rectangle_counts}",
        f"  expected_zone_rectangle_counts={expected_zone_rectangles}",
        f"  zone_carry_rectangle_counts={zone_carry_rectangle_counts}",
        f"  expected_zone_carry_rectangle_counts={expected_zone_carry_rectangles}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B residue-coset mask gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in PULLBACK_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"residue_coset_mask_rows={ok_rows}/{len(PULLBACK_CASES)}")
    print("interpretation")
    print("  canonical_half_arc_is_union_of_actual_local_residue_rectangles=1")
    print("  first_lab_151_by_677_rectangles_have_size_25_times_13_equals_325=1")
    print("  carry_mask_is_constant_on_each_residue_rectangle=1")
    print("  residue_rectangle_counts_match_the_zero_one_hot_two_hot_all_rows_template=1")
    print("conclusion=reported_p25_laneB_residue_coset_mask_gate")
    return 0 if ok_rows == len(PULLBACK_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
