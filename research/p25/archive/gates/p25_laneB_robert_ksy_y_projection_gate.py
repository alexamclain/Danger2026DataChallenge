#!/usr/bin/env python3
"""Projection/cancellation gate for the normalized KSY-y footprint.

The half-edge gate shows that the normalized Koo-Shin-Yoon coordinate

    y(Q) = -g(2Q) / g(Q)^4

does not directly emit the 150-cell bridge: the exponent footprint of
`y(P+h)/y(P-h)` has 300 cells.  This gate records the useful structure of that
failure:

    footprint = double_pushforward(bridge) - 4 * bridge.

Thus the coefficient-4 layer is exactly the desired bridge after scaling by
`-1/4`, while the coefficient-1 layer is a doubled bridge that must be
cancelled, separated theorem-side, or absorbed by a real `dlog` identity.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    scale_coord,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BRIDGE_SHIFT,
    C_ORDER,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class KsyYProjectionProfile:
    normalized_y_support: int
    bridge_support: int
    double_pushforward_support: int
    normalized_y_equals_double_minus_four_bridge: bool
    high_weight_layer_profile: CandidateProfile
    low_weight_layer_profile: CandidateProfile
    doubled_bridge_profile: CandidateProfile
    coefficient_blind_profile: CandidateProfile
    high_weight_layer_is_bridge: bool
    low_weight_layer_is_doubled_bridge: bool
    coefficient_blind_killed: bool
    row_ok: bool


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def add_rings(*rings: Ring) -> Ring:
    out: Ring = {}
    for ring in rings:
        for coord, coefficient in ring.items():
            add_ring_entry(out, coord, coefficient)
    return dict(sorted(out.items()))


def scale_ring(ring: Ring, scalar: int) -> Ring:
    return {coord: scalar * coefficient for coord, coefficient in sorted(ring.items())}


def double_pushforward(ring: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in ring.items():
        add_ring_entry(out, scale_coord(coord, 2), coefficient)
    return dict(sorted(out.items()))


def high_weight_bridge_layer(footprint: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in footprint.items():
        if abs(coefficient) == 4:
            if coefficient % -4 != 0:
                raise AssertionError("unexpected coefficient in high-weight layer")
            out[coord] = coefficient // -4
    return dict(sorted(out.items()))


def low_weight_doubled_layer(footprint: Ring) -> Ring:
    return {
        coord: coefficient
        for coord, coefficient in sorted(footprint.items())
        if abs(coefficient) == 1
    }


def coefficient_blind_layer(footprint: Ring) -> Ring:
    return {coord: 1 if coefficient > 0 else -1 for coord, coefficient in sorted(footprint.items())}


def translate_ring_for_edge(ring: Ring, step: Coord) -> Ring:
    return {
        add_coord(coord, step): coefficient
        for coord, coefficient in sorted(ring.items())
    }


def profile_projection() -> KsyYProjectionProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    footprint = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    doubled = double_pushforward(bridge)
    expected_footprint = add_rings(doubled, scale_ring(bridge, -4))

    high_layer = high_weight_bridge_layer(footprint)
    low_layer = low_weight_doubled_layer(footprint)
    blind_layer = coefficient_blind_layer(footprint)

    high_profile = bridge_profile("ksy_y_high_weight_layer_scaled_bridge", high_layer)
    low_profile = bridge_profile("ksy_y_low_weight_doubled_layer", low_layer)
    doubled_profile = bridge_profile("ksy_y_doubled_bridge_control", doubled)
    blind_profile = bridge_profile("ksy_y_coefficient_blind_footprint_control", blind_layer)

    row_ok = (
        BRIDGE_SHIFT == (38, 113)
        and footprint == expected_footprint
        and len(footprint) == 300
        and len(bridge) == 150
        and len(doubled) == 150
        and high_layer == bridge
        and low_layer == doubled
        and high_profile.ok
        and high_profile.raw_support == 150
        and not low_profile.ok
        and low_profile.raw_support == 150
        and low_profile.quotient_support == 6
        and not low_profile.trace_correct
        and blind_profile.raw_support == 300
        and blind_profile.quotient_support == 12
        and not blind_profile.ok
    )
    return KsyYProjectionProfile(
        normalized_y_support=len(footprint),
        bridge_support=len(bridge),
        double_pushforward_support=len(doubled),
        normalized_y_equals_double_minus_four_bridge=footprint == expected_footprint,
        high_weight_layer_profile=high_profile,
        low_weight_layer_profile=low_profile,
        doubled_bridge_profile=doubled_profile,
        coefficient_blind_profile=blind_profile,
        high_weight_layer_is_bridge=high_layer == bridge,
        low_weight_layer_is_doubled_bridge=low_layer == doubled,
        coefficient_blind_killed=not blind_profile.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY-y projection gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} bridge_edge={BRIDGE_SHIFT}")
    profile = profile_projection()
    print(f"ksy_y_projection_profile={profile}")
    print("projection_laws")
    print("  normalized_y_footprint = double_pushforward(bridge) - 4*bridge")
    print("  coefficient_abs_4_layer_scaled_by_-1/4_is_exact_bridge=1")
    print("  coefficient_abs_1_layer_is_doubled_bridge_not_target_bridge=1")
    print("  coefficient_blind_300_cell_footprint_fails_bridge_contract=1")
    print("interpretation")
    print("  KSY_y_route_needs_theorem_side_separation_or_cancellation_of_doubled_layer=1")
    print("  dlog_route_should_explain_why_the_g2Q_layer_does_not_survive_as_payload=1")
    print(f"robert_ksy_y_projection_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_y_projection_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
