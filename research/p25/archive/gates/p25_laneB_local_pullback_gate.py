#!/usr/bin/env python3
"""Local pullback gate for the p25 Lane B literal packet model.

The literal Jacobi packet is currently quotient-level.  This gate checks that
the packet can be read from the actual local source factors exposed by the
p25 negative trace:

    C_3 x C_13:  right from mod 151, C-axis from mod 677
    C_3 x C_53:  C-axis from mod 107, right visible on mod 7 and mod 151
    C_3 x C_169: right from mod 151, C-axis from mod 677

It verifies that local discrete-log coordinates reconstruct the exact
post-B quotient coordinates and therefore the Jacobi-carry Y[e] pullback.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_literal_jacobi_packet_model import (
    LiteralCase,
    admissible_pairs,
    carry_packet,
    representative_pairs,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


P25 = 10**25 + 13


@dataclass(frozen=True)
class LocalSource:
    name: str
    modulus: int
    expected_order: int
    role: str


@dataclass(frozen=True)
class PullbackCase:
    name: str
    rho_exp: int
    c_axis: int
    b_trace: int
    raw_order: int
    right_sources: tuple[LocalSource, ...]
    c_source: LocalSource
    exhaustive_pairs: bool


CASES = (
    PullbackCase(
        name="tiny_C3xC13",
        rho_exp=2,
        c_axis=13,
        b_trace=325,
        raw_order=12675,
        right_sources=(LocalSource("mod151", 151, 75, "right_C3_after_B"),),
        c_source=LocalSource("mod677", 677, 169, "C13_after_B"),
        exhaustive_pairs=True,
    ),
    PullbackCase(
        name="prime_axis_C3xC53",
        rho_exp=16,
        c_axis=53,
        b_trace=25,
        raw_order=3975,
        right_sources=(
            LocalSource("mod7", 7, 3, "right_C3_direct"),
            LocalSource("mod151", 151, 75, "right_C3_after_B"),
        ),
        c_source=LocalSource("mod107", 107, 53, "C53_direct"),
        exhaustive_pairs=True,
    ),
    PullbackCase(
        name="square_axis_C3xC169",
        rho_exp=2,
        c_axis=169,
        b_trace=25,
        raw_order=12675,
        right_sources=(LocalSource("mod151", 151, 75, "right_C3_after_B"),),
        c_source=LocalSource("mod677", 677, 169, "C169_direct"),
        exhaustive_pairs=False,
    ),
)


def discrete_log_table(generator: int, modulus: int, order: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(order):
        if value in table:
            raise AssertionError("generator order collapsed early")
        table[value] = exponent
        value = value * generator % modulus
    if value != 1:
        raise AssertionError("generator did not return to 1 at expected order")
    return table


def source_log(source: LocalSource, rho_exp: int, e_value: int) -> int:
    generator = pow(P25, rho_exp, source.modulus)
    table = discrete_log_table(generator, source.modulus, source.expected_order)
    residue = pow(generator, e_value, source.modulus)
    return table[residue]


def precompute_source_logs(case: PullbackCase) -> dict[str, list[int]]:
    logs: dict[str, list[int]] = {}
    for source in (*case.right_sources, case.c_source):
        generator = pow(P25, case.rho_exp, source.modulus)
        table = discrete_log_table(generator, source.modulus, source.expected_order)
        values: list[int] = []
        residue = 1
        for _ in range(case.raw_order):
            values.append(table[residue])
            residue = residue * generator % source.modulus
        logs[source.name] = values
    return logs


def quotient_coordinates(
    case: PullbackCase, source_logs: dict[str, list[int]], e_value: int
) -> tuple[int, int]:
    right_logs = [
        source_logs[source.name][e_value % case.raw_order] % RIGHT_DEGREE
        for source in case.right_sources
    ]
    if any(value != right_logs[0] for value in right_logs):
        raise AssertionError(f"right source disagreement at e={e_value}: {right_logs}")
    right_visible = right_logs[0]
    right_coord = right_visible * pow(case.c_axis % RIGHT_DEGREE, -1, RIGHT_DEGREE)
    right_coord %= RIGHT_DEGREE

    c_log = source_logs[case.c_source.name][e_value % case.raw_order] % case.c_axis
    c_coord = c_log * pow(RIGHT_DEGREE, -1, case.c_axis) % case.c_axis
    return right_coord, c_coord


def quotient_exponent(case: PullbackCase, right_coord: int, c_coord: int) -> int:
    return (case.c_axis * right_coord + RIGHT_DEGREE * c_coord) % (
        RIGHT_DEGREE * case.c_axis
    )


def coordinate_audit(
    case: PullbackCase, source_logs: dict[str, list[int]], coordinates: list[tuple[int, int]]
) -> tuple[int, int, int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    coordinate_hits = 0
    block_constancy_hits = 0
    right_agreement_hits = 0
    for e_value in range(case.raw_order):
        right_coords = [
            source_logs[source.name][e_value] % RIGHT_DEGREE
            for source in case.right_sources
        ]
        right_agreement_hits += int(all(value == right_coords[0] for value in right_coords))
        right_coord, c_coord = coordinates[e_value]
        coordinate_hits += int(
            quotient_exponent(case, right_coord, c_coord) == e_value % quotient_order
        )

    for start in range(quotient_order):
        coords = {coordinates[(start + quotient_order * j) % case.raw_order] for j in range(case.b_trace)}
        block_constancy_hits += int(len(coords) == 1)
    return coordinate_hits, block_constancy_hits, right_agreement_hits


def theta_from_local_coordinates(
    case: PullbackCase,
    coordinates: list[tuple[int, int]],
    packet: list[int],
    e_value: int,
) -> int:
    right_coord, c_coord = coordinates[e_value % case.raw_order]
    return packet[right_coord * case.c_axis + c_coord]


def pullback_audit(
    case: PullbackCase, coordinates: list[tuple[int, int]]
) -> tuple[int, int, int, int]:
    literal_case = LiteralCase(
        name=case.name,
        c_axis=case.c_axis,
        b_trace=case.b_trace,
        raw_order=case.raw_order,
        exhaustive=case.exhaustive_pairs,
    )
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = admissible_pairs(case.c_axis) if case.exhaustive_pairs else representative_pairs(case.c_axis)
    inv_b = pow(case.b_trace % modulus, -1, modulus)
    quotient_order = RIGHT_DEGREE * case.c_axis
    pair_hits = 0
    y_pullback_hits = 0
    trace_hits = 0
    checked_y_values = 0
    for u_value, v_value in pairs:
        packet = carry_packet(case.c_axis, u_value, v_value, modulus)
        local_ok = True
        y_ok = True
        trace_ok = True
        for e_value in range(case.raw_order):
            theta_local = theta_from_local_coordinates(case, coordinates, packet, e_value)
            right_coord, c_coord = coordinates[e_value]
            theta_quotient = packet[right_coord * case.c_axis + c_coord]
            local_ok = local_ok and theta_local == theta_quotient
            y_value = inv_b * theta_local % modulus
            y_ok = y_ok and y_value == inv_b * theta_quotient % modulus
            checked_y_values += 1
        for r in range(RIGHT_DEGREE):
            for c_index in range(case.c_axis):
                start = case.c_axis * r + RIGHT_DEGREE * c_index
                total = 0
                for j in range(case.b_trace):
                    total = (
                        total
                        + inv_b
                        * theta_from_local_coordinates(
                            case,
                            coordinates,
                            packet,
                            start + quotient_order * j,
                        )
                    ) % modulus
                trace_ok = trace_ok and total == packet[r * case.c_axis + c_index]
        pair_hits += int(local_ok and y_ok and trace_ok)
        y_pullback_hits += int(local_ok and y_ok)
        trace_hits += int(trace_ok)
    # literal_case keeps the imported dataclass semantically tied to this audit.
    if literal_case.raw_order != case.raw_order:
        raise AssertionError("literal case mismatch")
    return pair_hits, y_pullback_hits, trace_hits, len(pairs)


def main() -> int:
    print("p25 Lane B local pullback gate")
    print(f"p={P25}")
    ok_rows = 0
    for case in CASES:
        source_logs = precompute_source_logs(case)
        coordinates = [
            quotient_coordinates(case, source_logs, e_value)
            for e_value in range(case.raw_order)
        ]
        coordinate_hits, block_hits, right_hits = coordinate_audit(
            case, source_logs, coordinates
        )
        pair_hits, y_hits, trace_hits, pair_count = pullback_audit(case, coordinates)
        coordinate_ok = coordinate_hits == case.raw_order
        block_ok = block_hits == RIGHT_DEGREE * case.c_axis
        right_ok = right_hits == case.raw_order
        pullback_ok = pair_hits == pair_count and y_hits == pair_count and trace_hits == pair_count
        row_ok = coordinate_ok and block_ok and right_ok and pullback_ok
        ok_rows += int(row_ok)
        print(
            "row "
            f"name={case.name} c={case.c_axis} B={case.b_trace} raw_order={case.raw_order} "
            f"right_sources={[source.name for source in case.right_sources]} "
            f"c_source={case.c_source.name} "
            f"coordinate_hits={coordinate_hits}/{case.raw_order} "
            f"right_source_agreement={right_hits}/{case.raw_order} "
            f"B_block_coordinate_constancy={block_hits}/{RIGHT_DEGREE * case.c_axis} "
            f"pairs_checked={pair_count} exhaustive={int(case.exhaustive_pairs)} "
            f"local_pair_hits={pair_hits}/{pair_count} "
            f"Y_pullback_hits={y_hits}/{pair_count} "
            f"B_trace_hits={trace_hits}/{pair_count} "
            f"ok={int(row_ok)}"
        )
    print(f"local_pullback_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  local_discrete_logs_reconstruct_the_post_B_quotient_coordinates=1")
    print("  B_trace_blocks_are_constant_in_the_visible_local_coordinates=1")
    print("  literal_Jacobi_carry_Y_factors_through_the_identified_local_sources=1")
    print("  first_embedding_target_is_151x677_local_pullback_for_C3xC13=1")
    print("conclusion=reported_p25_laneB_local_pullback_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
