#!/usr/bin/env python3
"""Factorization gate for the unique inversion-partner bridge.

The inversion-partner uniqueness gate narrows the anomaly repair to the signed
six-point row

    + S * X * Y^-2  -  S * X^3 * Y.

This gate records the exact group-ring edge it represents:

    S * X * Y^-2 * (1 - X^2 * Y^3).

The factorization is unique among oriented products S*x^z*(1 - x^t).  Its
Fourier profile has only the forced degree-zero and S-factor zeros, so this is
not a hidden low-frequency or quotient-compressed correction.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    MODULUS,
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_inversion_partner_uniqueness_gate import (
    ANOMALY_BASE,
    PARTNER_BASE,
    s_layer,
)
from p25_laneB_square_axis_local_graph_residue_gate import BASE_C, QUOTIENT_ORDER
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
from p25_selected_defect_value_gate import RIGHT_DEGREE


SQUARE_C = 169
BRIDGE_STEP = (ANOMALY_BASE - PARTNER_BASE) % QUOTIENT_ORDER


@dataclass(frozen=True)
class BridgePoint:
    q_value: int
    coefficient: int
    right: int
    c_coord: int
    residue: int
    fiber: int
    local_h: int
    trace_bit: int


@dataclass(frozen=True)
class BridgePair:
    partner_q: int
    anomaly_q: int
    partner_coord: tuple[int, int]
    anomaly_coord: tuple[int, int]
    residue_delta: int
    fiber_delta: int
    local_h_delta: int
    trace_bit_delta: int


def bridge_coefficients() -> dict[int, int]:
    coefficients = {q_value: 1 for q_value in s_layer(PARTNER_BASE)}
    for q_value in s_layer(ANOMALY_BASE):
        coefficients[q_value] = coefficients.get(q_value, 0) - 1
    return {q_value: value for q_value, value in sorted(coefficients.items()) if value}


def bridge_points() -> tuple[BridgePoint, ...]:
    rows: list[BridgePoint] = []
    for q_value, coefficient in bridge_coefficients().items():
        right, c_coord = coord_from_q(q_value)
        residue = c_coord % BASE_C
        fiber = c_coord // BASE_C
        rows.append(
            BridgePoint(
                q_value=q_value,
                coefficient=coefficient,
                right=right,
                c_coord=c_coord,
                residue=residue,
                fiber=fiber,
                local_h=(right - residue) % RIGHT_DEGREE,
                trace_bit=template_bits(BASE_C, residue)[right],
            )
        )
    return tuple(rows)


def partner_anomaly_pairs() -> tuple[BridgePair, ...]:
    rows: list[BridgePair] = []
    for partner_q in s_layer(PARTNER_BASE):
        anomaly_q = (partner_q + BRIDGE_STEP) % QUOTIENT_ORDER
        partner_right, partner_c = coord_from_q(partner_q)
        anomaly_right, anomaly_c = coord_from_q(anomaly_q)
        partner_residue = partner_c % BASE_C
        anomaly_residue = anomaly_c % BASE_C
        partner_fiber = partner_c // BASE_C
        anomaly_fiber = anomaly_c // BASE_C
        partner_h = (partner_right - partner_residue) % RIGHT_DEGREE
        anomaly_h = (anomaly_right - anomaly_residue) % RIGHT_DEGREE
        partner_bit = template_bits(BASE_C, partner_residue)[partner_right]
        anomaly_bit = template_bits(BASE_C, anomaly_residue)[anomaly_right]
        rows.append(
            BridgePair(
                partner_q=partner_q,
                anomaly_q=anomaly_q,
                partner_coord=(partner_right, partner_c),
                anomaly_coord=(anomaly_right, anomaly_c),
                residue_delta=(anomaly_residue - partner_residue) % BASE_C,
                fiber_delta=anomaly_fiber - partner_fiber,
                local_h_delta=(anomaly_h - partner_h) % RIGHT_DEGREE,
                trace_bit_delta=anomaly_bit - partner_bit,
            )
        )
    return tuple(rows)


def weighted_fourier_zeros() -> tuple[int, ...]:
    root = primitive_root(MODULUS)
    zeta = pow(root, (MODULUS - 1) // QUOTIENT_ORDER, MODULUS)
    coefficients = bridge_coefficients()
    zeros: list[int] = []
    for frequency in range(QUOTIENT_ORDER):
        total = sum(
            value * pow(zeta, frequency * q_value, MODULUS)
            for q_value, value in coefficients.items()
        ) % MODULUS
        if total == 0:
            zeros.append(frequency)
    return tuple(zeros)


def trace_to_c13() -> tuple[tuple[tuple[int, int], int], ...]:
    trace: dict[tuple[int, int], int] = defaultdict(int)
    for q_value, coefficient in bridge_coefficients().items():
        right, c_coord = coord_from_q(q_value)
        trace[(right, c_coord % BASE_C)] += coefficient
    return tuple(sorted((coord, value) for coord, value in trace.items() if value))


def oriented_s_edge_factorizations() -> tuple[tuple[int, int], ...]:
    target = bridge_coefficients()
    matches: list[tuple[int, int]] = []
    for base in range(QUOTIENT_ORDER):
        for step in range(1, QUOTIENT_ORDER):
            candidate: dict[int, int] = {}
            for s_shift in (0, S_STEP, 2 * S_STEP):
                plus = (base + s_shift) % QUOTIENT_ORDER
                minus = (base + step + s_shift) % QUOTIENT_ORDER
                candidate[plus] = candidate.get(plus, 0) + 1
                candidate[minus] = candidate.get(minus, 0) - 1
            candidate = {
                q_value: value for q_value, value in candidate.items() if value
            }
            if candidate == target:
                matches.append((base, step))
    return tuple(matches)


def first_boundary(coefficients: dict[int, int], direction: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for q_value, value in coefficients.items():
        out[q_value] = out.get(q_value, 0) + value
        shifted = (q_value + direction) % QUOTIENT_ORDER
        out[shifted] = out.get(shifted, 0) - value
    return {q_value: value for q_value, value in out.items() if value}


def first_boundary_distribution() -> tuple[Counter[int], tuple[int, ...]]:
    coefficients = bridge_coefficients()
    support_by_direction = {
        direction: len(first_boundary(coefficients, direction))
        for direction in range(1, QUOTIENT_ORDER)
    }
    minimum = min(support_by_direction.values())
    min_directions = tuple(
        sorted(
            direction
            for direction, support in support_by_direction.items()
            if support == minimum
        )
    )
    return Counter(support_by_direction.values()), min_directions


def main() -> int:
    print("p25 Lane B square-axis bridge-factorization gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} D={S_STEP} X={X_STEP} Y={Y_STEP} "
        f"partner_base={PARTNER_BASE} anomaly_base={ANOMALY_BASE} bridge_step={BRIDGE_STEP}"
    )
    coefficients = bridge_coefficients()
    points = bridge_points()
    pairs = partner_anomaly_pairs()
    zeros = weighted_fourier_zeros()
    trace = trace_to_c13()
    factorizations = oriented_s_edge_factorizations()
    distribution, min_directions = first_boundary_distribution()
    bridge_step_coord = coord_from_q(BRIDGE_STEP)
    expected_coefficients = {
        25: 1,
        138: -1,
        197: 1,
        310: -1,
        369: 1,
        482: -1,
    }
    expected_trace = (
        ((0, 6), 1),
        ((0, 7), -1),
        ((1, 4), 1),
        ((1, 8), -1),
        ((2, 5), 1),
        ((2, 9), -1),
    )
    expected_distribution = Counter({4: 2, 8: 2, 9: 2, 10: 4, 11: 4, 12: 492})

    row_ok = (
        coefficients == expected_coefficients
        and BRIDGE_STEP == 2 * X_STEP + 3 * Y_STEP
        and bridge_step_coord == (2, 94)
        and zeros == (0, 169, 338)
        and trace == expected_trace
        and factorizations == ((PARTNER_BASE, BRIDGE_STEP),)
        and all(pair.residue_delta == 3 for pair in pairs)
        and all(pair.fiber_delta == -6 for pair in pairs)
        and all(pair.local_h_delta == 2 for pair in pairs)
        and all(pair.trace_bit_delta == 1 for pair in pairs)
        and distribution == expected_distribution
        and min_directions == (S_STEP, (-S_STEP) % QUOTIENT_ORDER)
    )
    print(
        "bridge_coefficients: "
        f"coefficients={sorted(coefficients.items())} "
        f"support={len(coefficients)} "
        f"degree={sum(coefficients.values())} "
        f"ok={int(coefficients == expected_coefficients)}"
    )
    print("bridge_points")
    for point in points:
        print(f"  {point}")
    print(
        "bridge_factorization: "
        f"factorizations={list(factorizations)} "
        f"bridge_step_coord={bridge_step_coord} "
        f"bridge_step_expression=2X+3Y "
        f"unique={int(factorizations == ((PARTNER_BASE, BRIDGE_STEP),))}"
    )
    print("bridge_pairs")
    for pair in pairs:
        print(f"  {pair}")
    print(
        "bridge_fourier_and_trace: "
        f"weighted_zeros={list(zeros)} "
        f"nonzero_frequencies={QUOTIENT_ORDER - len(zeros)} "
        f"trace_C3x13={list(trace)}"
    )
    print(
        "bridge_boundary_profile: "
        f"support_distribution={dict(sorted(distribution.items()))} "
        f"minimal_directions={list(min_directions)}"
    )
    print("group_ring_law")
    print("  bridge = S * X * Y^-2 * (1 - X^2 * Y^3)")
    print("  bridge_step = X^2 * Y^3 = 113 = quotient_coord(2,94)")
    print("  bridge maps top fiber b=9 trace-zero points to bottom fiber b=3 trace-one points")
    print("interpretation")
    print("  bridge_has_unique_oriented_S_edge_factorization=1")
    print("  bridge_has_only_degree_and_S_factor_fourier_zeros=1")
    print("  bridge_trace_to_C3x13_is_a_six_point_residue_edge=1")
    print("  producer_must_realize_the_X2Y3_top_to_bottom_edge=1")
    print(f"square_axis_bridge_factorization_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_factorization_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
