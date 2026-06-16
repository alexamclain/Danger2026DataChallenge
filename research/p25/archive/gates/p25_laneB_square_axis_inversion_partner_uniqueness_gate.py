#!/usr/bin/env python3
"""Uniqueness gate for the inversion-partner repair layer.

The inversion-partner repair gate found that the illegal anomaly

    - S * X^3 * Y

becomes value-side admissible if we add the partner layer

    + S * X * Y^-2.

This gate checks that this is not an arbitrary choice.  Among all equal-weight
three-point S-layers

    + (1 + D + D^2) * x^base

added to the negative anomaly, the selected-defect and raw-producer identities
pass only in two cases:

    base = X^3Y      : trivial cancellation,
    base = X Y^-2   : nontrivial inversion-partner completion.

So an equal-coefficient local producer has a unique nontrivial target layer.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_inversion_partner_repair_gate import inversion_coord
from p25_laneB_square_axis_local_graph_residue_gate import (
    BASE_C,
    QUOTIENT_ORDER,
    triangular_parameters,
)
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    coord_from_q,
    q_from_coord,
)
from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    raw_producer_conditions,
    split_prime_for,
    value_conditions_hold,
)


SQUARE_C = 169
RAW_KERNEL_SIZE = 25
ANOMALY_BASE = X_STEP * 3 + Y_STEP
PARTNER_BASE = (X_STEP - 2 * Y_STEP) % QUOTIENT_ORDER
PARTNER_TO_ANOMALY_SHIFT = (2 * X_STEP + 3 * Y_STEP) % QUOTIENT_ORDER


Coord = tuple[int, int]


@dataclass(frozen=True)
class LayerHit:
    base: int
    layer: tuple[int, int, int]
    coords: tuple[Coord, Coord, Coord]
    value_ok: bool
    raw_ok: bool
    is_trivial_cancellation: bool
    is_inversion_partner: bool


@dataclass(frozen=True)
class FieldProfile:
    modulus_name: str
    modulus: int
    passing_bases: tuple[int, ...]
    raw_passing_bases: tuple[int, ...]
    both_passing_bases: tuple[int, ...]
    nontrivial_bases: tuple[int, ...]
    hit_profiles: tuple[LayerHit, ...]


@dataclass(frozen=True)
class ShapePoint:
    q_value: int
    right: int
    c_coord: int
    residue: int
    fiber: int
    local_h: int
    trace_bit: int
    triangular_h: int
    triangular_s: int
    triangular_t: int
    base43_digit: int
    base43_remainder: int


def s_layer(base: int) -> tuple[int, int, int]:
    return tuple((base + multiplier * S_STEP) % QUOTIENT_ORDER for multiplier in range(3))


def packet_from_layers(
    positive_layer: tuple[int, int, int],
    negative_layer: tuple[int, int, int],
    modulus: int,
) -> list[int]:
    packet = [0] * QUOTIENT_ORDER
    for q_value in positive_layer:
        right, c_coord = coord_from_q(q_value)
        packet[right * SQUARE_C + c_coord] = (
            packet[right * SQUARE_C + c_coord] + 1
        ) % modulus
    for q_value in negative_layer:
        right, c_coord = coord_from_q(q_value)
        packet[right * SQUARE_C + c_coord] = (
            packet[right * SQUARE_C + c_coord] - 1
        ) % modulus
    return packet


def layer_coords(layer: tuple[int, int, int]) -> tuple[Coord, Coord, Coord]:
    return tuple(coord_from_q(q_value) for q_value in layer)  # type: ignore[return-value]


def layer_is_inversion_partner(layer: tuple[int, int, int]) -> bool:
    anomaly_coords = {coord_from_q(q_value) for q_value in anomaly_orbit()}
    partner_coords = {inversion_coord(coord) for coord in anomaly_coords}
    return {coord_from_q(q_value) for q_value in layer} == partner_coords


def field_profile(modulus_name: str, modulus: int) -> FieldProfile:
    anomaly = tuple(anomaly_orbit())
    passing: list[int] = []
    raw_passing: list[int] = []
    both_passing: list[int] = []
    hits: list[LayerHit] = []
    for base in range(QUOTIENT_ORDER):
        layer = s_layer(base)
        packet = packet_from_layers(layer, anomaly, modulus)
        value_ok = value_conditions_hold(packet, SQUARE_C, modulus)
        raw_ok = raw_producer_conditions(packet, SQUARE_C, modulus)
        if value_ok:
            passing.append(base)
        if raw_ok:
            raw_passing.append(base)
        if value_ok and raw_ok:
            both_passing.append(base)
            hits.append(
                LayerHit(
                    base=base,
                    layer=layer,
                    coords=layer_coords(layer),
                    value_ok=value_ok,
                    raw_ok=raw_ok,
                    is_trivial_cancellation=layer == anomaly,
                    is_inversion_partner=layer_is_inversion_partner(layer),
                )
            )
    nontrivial = tuple(base for base in both_passing if s_layer(base) != anomaly)
    return FieldProfile(
        modulus_name=modulus_name,
        modulus=modulus,
        passing_bases=tuple(passing),
        raw_passing_bases=tuple(raw_passing),
        both_passing_bases=tuple(both_passing),
        nontrivial_bases=nontrivial,
        hit_profiles=tuple(hits),
    )


def triangular_lookup() -> dict[int, tuple[int, int, int]]:
    return {
        q_value: (h_value, s_value, t_value)
        for h_value, s_value, t_value, _right, _c_coord, q_value in triangular_parameters()
    }


def shape_points(layer: tuple[int, int, int]) -> tuple[ShapePoint, ...]:
    lookup = triangular_lookup()
    rows: list[ShapePoint] = []
    for q_value in layer:
        right, c_coord = coord_from_q(q_value)
        residue = c_coord % BASE_C
        fiber = c_coord // BASE_C
        h_value, s_value, t_value = lookup.get(q_value, (-1, -1, -1))
        rows.append(
            ShapePoint(
                q_value=q_value,
                right=right,
                c_coord=c_coord,
                residue=residue,
                fiber=fiber,
                local_h=(right - residue) % RIGHT_DEGREE,
                trace_bit=template_bits(BASE_C, residue)[right],
                triangular_h=h_value,
                triangular_s=s_value,
                triangular_t=t_value,
                base43_digit=q_value // X_STEP,
                base43_remainder=q_value % X_STEP,
            )
        )
    return tuple(rows)


def integer_completion_coefficients() -> dict[int, int]:
    coefficients = {q_value: 1 for q_value in s_layer(PARTNER_BASE)}
    for q_value in anomaly_orbit():
        coefficients[q_value] = coefficients.get(q_value, 0) - 1
    return {q_value: value for q_value, value in coefficients.items() if value}


def first_boundary(coefficients: dict[int, int], direction: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for q_value, value in coefficients.items():
        out[q_value] = out.get(q_value, 0) + value
        shifted = (q_value + direction) % QUOTIENT_ORDER
        out[shifted] = out.get(shifted, 0) - value
    return {q_value: value for q_value, value in out.items() if value}


def first_boundary_distribution() -> tuple[Counter[int], tuple[int, ...]]:
    coefficients = integer_completion_coefficients()
    support_by_direction: dict[int, int] = {}
    for direction in range(1, QUOTIENT_ORDER):
        support_by_direction[direction] = len(first_boundary(coefficients, direction))
    minimum = min(support_by_direction.values())
    min_directions = tuple(
        sorted(direction for direction, support in support_by_direction.items() if support == minimum)
    )
    return Counter(support_by_direction.values()), min_directions


def main() -> int:
    print("p25 Lane B square-axis inversion-partner uniqueness gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} D={S_STEP} X={X_STEP} Y={Y_STEP} "
        f"anomaly_base={ANOMALY_BASE} partner_base={PARTNER_BASE}"
    )
    anomaly_layer = tuple(anomaly_orbit())
    partner_layer = s_layer(PARTNER_BASE)
    partner_qs_sorted = tuple(sorted(partner_layer))
    anomaly_qs_sorted = tuple(sorted(anomaly_layer))
    partner_is_negation = partner_qs_sorted == tuple(sorted((-q_value) % QUOTIENT_ORDER for q_value in anomaly_layer))
    partner_to_anomaly_deltas = tuple(
        (anomaly_q - partner_q) % QUOTIENT_ORDER
        for partner_q, anomaly_q in zip(partner_layer, anomaly_layer)
    )
    anomaly_shape = shape_points(anomaly_layer)
    partner_shape = shape_points(partner_layer)
    distribution, min_directions = first_boundary_distribution()
    expected_distribution = Counter({4: 2, 8: 2, 9: 2, 10: 4, 11: 4, 12: 492})

    field_rows = (
        field_profile("quotient", split_prime_for(QUOTIENT_ORDER)),
        field_profile("raw_split", split_prime_for(RAW_KERNEL_SIZE * QUOTIENT_ORDER)),
    )
    expected_bases = (PARTNER_BASE, ANOMALY_BASE)
    fields_ok = 0
    for row in field_rows:
        row_ok = (
            row.passing_bases == expected_bases
            and row.raw_passing_bases == expected_bases
            and row.both_passing_bases == expected_bases
            and row.nontrivial_bases == (PARTNER_BASE,)
            and len(row.hit_profiles) == 2
            and row.hit_profiles[0].base == PARTNER_BASE
            and row.hit_profiles[0].is_inversion_partner
            and not row.hit_profiles[0].is_trivial_cancellation
            and row.hit_profiles[1].base == ANOMALY_BASE
            and row.hit_profiles[1].is_trivial_cancellation
        )
        fields_ok += int(row_ok)
        print(
            f"profile {row.modulus_name}: "
            f"modulus={row.modulus} "
            f"value_passing_bases={list(row.passing_bases)} "
            f"raw_passing_bases={list(row.raw_passing_bases)} "
            f"both_passing_bases={list(row.both_passing_bases)} "
            f"nontrivial_bases={list(row.nontrivial_bases)} "
            f"ok={int(row_ok)}"
        )
        for hit in row.hit_profiles:
            print(
                f"  hit base={hit.base} layer={list(hit.layer)} "
                f"coords={list(hit.coords)} "
                f"trivial={int(hit.is_trivial_cancellation)} "
                f"inversion_partner={int(hit.is_inversion_partner)}"
            )

    shape_ok = (
        anomaly_layer == (138, 310, 482)
        and partner_layer == (25, 197, 369)
        and partner_is_negation
        and partner_to_anomaly_deltas == (PARTNER_TO_ANOMALY_SHIFT,) * 3
        and [point.residue for point in anomaly_shape] == [7, 8, 9]
        and [point.fiber for point in anomaly_shape] == [3, 3, 3]
        and [point.local_h for point in anomaly_shape] == [2, 2, 2]
        and [point.trace_bit for point in anomaly_shape] == [1, 1, 1]
        and [point.residue for point in partner_shape] == [4, 5, 6]
        and [point.fiber for point in partner_shape] == [9, 9, 9]
        and [point.local_h for point in partner_shape] == [0, 0, 0]
        and [point.trace_bit for point in partner_shape] == [0, 0, 0]
        and distribution == expected_distribution
        and min_directions == (S_STEP, (-S_STEP) % QUOTIENT_ORDER)
    )

    print(
        "layer_shapes: "
        f"anomaly_layer={list(anomaly_layer)} "
        f"partner_layer={list(partner_layer)} "
        f"partner_is_negation={int(partner_is_negation)} "
        f"partner_to_anomaly_shift={list(partner_to_anomaly_deltas)} "
        f"shape_ok={int(shape_ok)}"
    )
    print("anomaly_shape")
    for point in anomaly_shape:
        print(f"  {point}")
    print("partner_shape")
    for point in partner_shape:
        print(f"  {point}")
    print(
        "completion_boundary_profile: "
        f"support_distribution={dict(sorted(distribution.items()))} "
        f"minimal_directions={list(min_directions)}"
    )
    print("group_ring_law")
    print("  anomaly = S * X^3 * Y")
    print("  partner = S * X * Y^-2")
    print("  anomaly = partner * X^2 * Y^3")
    print("  completion = S * X * Y^-2 * (1 - X^2 * Y^3)")
    print("interpretation")
    print("  equal_weight_S_layer_completion_has_unique_nontrivial_solution=1")
    print("  unique_nontrivial_solution_is_the_inversion_partner_layer=1")
    print("  partner_layer_is_top_fiber_trace_zero_against_bottom_fiber_trace_one=1")
    print("  completed_six_point_row_still_has_only_signed_D_minimal_boundaries=1")
    print(f"square_axis_inversion_partner_uniqueness_rows={fields_ok}/{len(field_rows)} shape={int(shape_ok)}")
    print("conclusion=reported_p25_laneB_square_axis_inversion_partner_uniqueness_gate")
    return 0 if fields_ok == len(field_rows) and shape_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
