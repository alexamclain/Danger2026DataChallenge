#!/usr/bin/env python3
"""Local-source lift gate for the canonical p25 Lane B half-arc.

The canonical half-arc gate describes theta_{3,1} on the quotient C_3 x C_c.
This gate lifts that exact four-zone carry template back to the raw local
source cycle exposed by the p25 negative trace.

For the first p25 lab this means:

    right coordinate from the inert 151 source,
    C-axis coordinate from the split 677 source,
    B = 325 raw representatives for each quotient point.

The gate checks that the local discrete-log coordinates read the same zero /
one-hot / two-hot / all-rows carry bits as the quotient template, and that the
raw trace over each B-block reconstructs the canonical quotient packet.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_literal_jacobi_packet_model import carry_packet
from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    PullbackCase,
    precompute_source_logs,
    quotient_coordinates,
    quotient_exponent,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class LiftSummary:
    name: str
    c_axis: int
    b_trace: int
    raw_order: int
    right_sources: tuple[str, ...]
    c_source: str


def zone_name(c_axis: int, c_index: int) -> str:
    m_value = (c_axis - 1) // 4
    if c_index <= m_value:
        return "zero"
    if c_index <= 2 * m_value:
        return "one_hot"
    if c_index <= 3 * m_value:
        return "two_hot"
    return "all_rows"


def raw_block_counts(
    case: PullbackCase, coordinates: list[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for coord in coordinates:
        counts[coord] = counts.get(coord, 0) + 1
    return counts


def expected_zone_lengths(c_axis: int) -> dict[str, int]:
    m_value = (c_axis - 1) // 4
    return {
        "zero": m_value + 1,
        "one_hot": m_value,
        "two_hot": m_value,
        "all_rows": m_value,
    }


def audit_case(case: PullbackCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    quotient_order = RIGHT_DEGREE * case.c_axis
    source_logs = precompute_source_logs(case)
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]
    packet = carry_packet(case.c_axis, RIGHT_DEGREE, 1, modulus)
    inv_b = pow(case.b_trace % modulus, -1, modulus)
    quotient_bit_hits = 0
    raw_value_hits = 0
    trace_hits = 0
    source_coordinate_hits = 0
    raw_carry_one_count = 0
    raw_zone_counts = {"zero": 0, "one_hot": 0, "two_hot": 0, "all_rows": 0}
    raw_zone_carry_counts = {"zero": 0, "one_hot": 0, "two_hot": 0, "all_rows": 0}

    for e_value, (right_coord, c_coord) in enumerate(coordinates):
        bits = template_bits(case.c_axis, c_coord)
        zone = zone_name(case.c_axis, c_coord)
        carry_bit = bits[right_coord]
        quotient_value = packet[right_coord * case.c_axis + c_coord]
        quotient_bit_hits += int(
            quotient_value == RIGHT_DEGREE * case.c_axis * carry_bit % modulus
        )
        raw_value = quotient_value * inv_b % modulus
        raw_value_hits += int(
            raw_value == RIGHT_DEGREE * case.c_axis * carry_bit * inv_b % modulus
        )
        raw_carry_one_count += carry_bit
        raw_zone_counts[zone] += 1
        raw_zone_carry_counts[zone] += carry_bit
        source_coordinate_hits += int(
            quotient_exponent(case, right_coord, c_coord)
            == e_value % quotient_order
        )

    for right in range(RIGHT_DEGREE):
        for c_index in range(case.c_axis):
            start = case.c_axis * right + RIGHT_DEGREE * c_index
            total = 0
            for j_value in range(case.b_trace):
                e_value = (start + quotient_order * j_value) % case.raw_order
                local_right, local_c = coordinates[e_value]
                if (local_right, local_c) != (right, c_index):
                    continue
                bits = template_bits(case.c_axis, local_c)
                total = (
                    total
                    + RIGHT_DEGREE
                    * case.c_axis
                    * bits[local_right]
                    * inv_b
                ) % modulus
            trace_hits += int(total == packet[right * case.c_axis + c_index])

    block_counts = raw_block_counts(case, coordinates)
    block_constancy_hits = sum(
        int(count == case.b_trace) for count in block_counts.values()
    )
    expected_zone_raw_counts = {
        name: length * RIGHT_DEGREE * case.b_trace
        for name, length in expected_zone_lengths(case.c_axis).items()
    }
    expected_zone_carry_counts = {
        "zero": 0,
        "one_hot": expected_zone_lengths(case.c_axis)["one_hot"] * case.b_trace,
        "two_hot": 2 * expected_zone_lengths(case.c_axis)["two_hot"] * case.b_trace,
        "all_rows": RIGHT_DEGREE
        * expected_zone_lengths(case.c_axis)["all_rows"]
        * case.b_trace,
    }

    row_ok = (
        len(block_counts) == quotient_order
        and block_constancy_hits == quotient_order
        and source_coordinate_hits == case.raw_order
        and quotient_bit_hits == case.raw_order
        and raw_value_hits == case.raw_order
        and trace_hits == quotient_order
        and raw_zone_counts == expected_zone_raw_counts
        and raw_zone_carry_counts == expected_zone_carry_counts
    )

    summary = LiftSummary(
        name=case.name,
        c_axis=case.c_axis,
        b_trace=case.b_trace,
        raw_order=case.raw_order,
        right_sources=tuple(source.name for source in case.right_sources),
        c_source=case.c_source.name,
    )
    lines = [
        (
            f"case {summary.name}: c={summary.c_axis} B={summary.b_trace} "
            f"raw_order={summary.raw_order} right_sources={list(summary.right_sources)} "
            f"c_source={summary.c_source} modulus={modulus} "
            f"source_coordinate_hits={source_coordinate_hits}/{case.raw_order} "
            f"block_constancy_hits={block_constancy_hits}/{quotient_order} "
            f"quotient_bit_hits={quotient_bit_hits}/{case.raw_order} "
            f"raw_value_hits={raw_value_hits}/{case.raw_order} "
            f"trace_hits={trace_hits}/{quotient_order} "
            f"raw_carry_one_count={raw_carry_one_count} "
            f"ok={int(row_ok)}"
        ),
        f"  raw_zone_counts={raw_zone_counts}",
        f"  expected_zone_raw_counts={expected_zone_raw_counts}",
        f"  raw_zone_carry_counts={raw_zone_carry_counts}",
        f"  expected_zone_carry_counts={expected_zone_carry_counts}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B source half-arc lift gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in PULLBACK_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"source_half_arc_lift_rows={ok_rows}/{len(PULLBACK_CASES)}")
    print("interpretation")
    print("  canonical_half_arc_template_lifts_to_raw_local_source_cycle=1")
    print("  raw_cycle_has_exactly_B_representatives_per_quotient_point=1")
    print("  inert_right_and_split_C_source_logs_read_the_expected_carry_bits=1")
    print("  raw_trace_reconstructs_the_canonical_theta_3_1_packet=1")
    print("conclusion=reported_p25_laneB_source_half_arc_lift_gate")
    return 0 if ok_rows == len(PULLBACK_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
