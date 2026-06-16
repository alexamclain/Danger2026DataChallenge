#!/usr/bin/env python3
"""Boundary gate for the selected-defect diagonal anomaly.

The diagonal-anomaly rigidity gate identifies the leftover selected-defect
obstruction as the fixed h=2, t=1 slice

    A = (1 + D + D^2) * X^3 * Y.

This gate records its strongest local relation: because D^3 = Y on the
quotient,

    (1 - D) A = X^3 Y - X^3 Y^2.

So the anomaly is a length-3 D-segment whose D-boundary telescopes to a
two-point Y-edge inside the same h=2 bottom boundary fiber.  That does not
solve the producer problem, but it makes the next target sharper: an allowed
producer would need a genuinely mixed D-antiderivative of this local edge.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import (
    BASE_C,
    QUOTIENT_ORDER,
    triangular_parameters,
)
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q


@dataclass(frozen=True)
class Endpoint:
    q_value: int
    coefficient: int
    right: int
    c_coord: int
    residue: int
    fiber: int
    h_value: int
    s_value: int
    t_value: int


@dataclass(frozen=True)
class BoundaryProfile:
    direction: int
    label: str
    support_count: int
    coefficient_counts: tuple[tuple[int, int], ...]
    endpoints: tuple[Endpoint, ...]


def direction_label(direction: int) -> str:
    labels = {
        S_STEP % QUOTIENT_ORDER: "+D",
        (-S_STEP) % QUOTIENT_ORDER: "-D",
        (2 * S_STEP) % QUOTIENT_ORDER: "+2D",
        (-2 * S_STEP) % QUOTIENT_ORDER: "-2D",
        Y_STEP % QUOTIENT_ORDER: "+Y",
        (-Y_STEP) % QUOTIENT_ORDER: "-Y",
    }
    return labels.get(direction, "other")


def triangular_lookup() -> dict[int, tuple[int, int, int]]:
    return {
        q_value: (h_value, s_value, t_value)
        for h_value, s_value, t_value, _right, _c_coord, q_value in triangular_parameters()
    }


def first_boundary_coefficients(direction: int) -> dict[int, int]:
    coefficients: dict[int, int] = {}
    for point in anomaly_orbit():
        coefficients[point] = coefficients.get(point, 0) + 1
        shifted = (point + direction) % QUOTIENT_ORDER
        coefficients[shifted] = coefficients.get(shifted, 0) - 1
    return {
        point: coefficient
        for point, coefficient in sorted(coefficients.items())
        if coefficient
    }


def boundary_profile(direction: int) -> BoundaryProfile:
    lookup = triangular_lookup()
    coefficients = first_boundary_coefficients(direction)
    endpoints: list[Endpoint] = []
    for q_value, coefficient in coefficients.items():
        right, c_coord = coord_from_q(q_value)
        h_value, s_value, t_value = lookup.get(q_value, (-1, -1, -1))
        endpoints.append(
            Endpoint(
                q_value=q_value,
                coefficient=coefficient,
                right=right,
                c_coord=c_coord,
                residue=c_coord % BASE_C,
                fiber=c_coord // BASE_C,
                h_value=h_value,
                s_value=s_value,
                t_value=t_value,
            )
        )
    return BoundaryProfile(
        direction=direction,
        label=direction_label(direction),
        support_count=len(coefficients),
        coefficient_counts=tuple(sorted(Counter(coefficients.values()).items())),
        endpoints=tuple(endpoints),
    )


def all_boundary_profiles() -> list[BoundaryProfile]:
    return [
        boundary_profile(direction)
        for direction in range(1, QUOTIENT_ORDER)
    ]


def endpoint_summary(profile: BoundaryProfile) -> list[tuple[int, int, int, int, int, int, int, int]]:
    return [
        (
            endpoint.q_value,
            endpoint.coefficient,
            endpoint.right,
            endpoint.c_coord,
            endpoint.h_value,
            endpoint.s_value,
            endpoint.t_value,
            endpoint.fiber,
        )
        for endpoint in profile.endpoints
    ]


def main() -> int:
    print("p25 Lane B square-axis diagonal-anomaly boundary gate")
    print(f"quotient_order={QUOTIENT_ORDER} D={S_STEP} X={X_STEP} Y={Y_STEP}")
    profiles = all_boundary_profiles()
    support_distribution = Counter(profile.support_count for profile in profiles)
    support2 = [profile for profile in profiles if profile.support_count == 2]
    support4 = [profile for profile in profiles if profile.support_count == 4]
    plus_d = boundary_profile(S_STEP)
    minus_d = boundary_profile((-S_STEP) % QUOTIENT_ORDER)
    plus_2d = boundary_profile((2 * S_STEP) % QUOTIENT_ORDER)
    minus_2d = boundary_profile((-2 * S_STEP) % QUOTIENT_ORDER)
    plus_d_summary = endpoint_summary(plus_d)
    minus_d_summary = endpoint_summary(minus_d)
    plus_2d_summary = endpoint_summary(plus_2d)
    minus_2d_summary = endpoint_summary(minus_2d)

    row_ok = (
        support_distribution == Counter({2: 2, 4: 2, 6: 502})
        and {profile.direction for profile in support2}
        == {S_STEP, (-S_STEP) % QUOTIENT_ORDER}
        and {profile.direction for profile in support4}
        == {(2 * S_STEP) % QUOTIENT_ORDER, (-2 * S_STEP) % QUOTIENT_ORDER}
        and plus_d_summary
        == [
            (138, 1, 0, 46, 2, 0, 1, 3),
            (147, -1, 0, 49, 2, 0, 2, 3),
        ]
        and minus_d_summary
        == [
            (473, -1, 2, 45, 2, 2, 0, 3),
            (482, 1, 2, 48, 2, 2, 1, 3),
        ]
        and plus_2d_summary
        == [
            (138, 1, 0, 46, 2, 0, 1, 3),
            (147, -1, 0, 49, 2, 0, 2, 3),
            (310, 1, 1, 47, 2, 1, 1, 3),
            (319, -1, 1, 50, 2, 1, 2, 3),
        ]
        and minus_2d_summary
        == [
            (301, -1, 1, 44, 2, 1, 0, 3),
            (310, 1, 1, 47, 2, 1, 1, 3),
            (473, -1, 2, 45, 2, 2, 0, 3),
            (482, 1, 2, 48, 2, 2, 1, 3),
        ]
    )

    print(
        "diagonal_anomaly_boundary: "
        f"anomaly={anomaly_orbit()} "
        f"support_distribution={dict(sorted(support_distribution.items()))} "
        f"support2_directions={[profile.direction for profile in support2]} "
        f"support4_directions={[profile.direction for profile in support4]} "
        f"ok={int(row_ok)}"
    )
    print("minimal_boundary_profiles")
    for profile in support2 + support4:
        print(
            f"  direction={profile.direction} label={profile.label} "
            f"support={profile.support_count} "
            f"coefficient_counts={dict(profile.coefficient_counts)} "
            f"endpoints={endpoint_summary(profile)}"
        )
    print("telescoping_law")
    print("  A = (1 + D + D^2) * X^3 * Y")
    print("  (1 - D)A = X^3*Y - X^3*Y^2")
    print("  (1 - D^-1)A = D^2*X^3*Y - D^2*X^3")
    print(f"square_axis_diagonal_anomaly_boundary_rows={int(row_ok)}/1")
    print("interpretation")
    print("  diagonal_anomaly_is_a_length_three_D_segment=1")
    print("  only_signed_D_directions_give_a_two_point_boundary=1")
    print("  anomaly_boundary_is_a_local_Y_edge_inside_the_h2_bottom_fiber=1")
    print("  producer_candidate_should_be_tested_for_a_mixed_D_antiderivative=1")
    print("conclusion=reported_p25_laneB_square_axis_diagonal_anomaly_boundary_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
