#!/usr/bin/env python3
"""Selected-defect test for the p25 square-axis scalar-balance escape.

The scalar-balance escape gate shows that the q-binomial anomaly can be made
degree zero by adding a dense scalar background.  This gate checks whether
that scalar background hides the anomaly from the actual Lane B value-side
contract.

It does not.  The scalar component cancels under

    selected_defect(r,c) = g(r,c) - g(r,0),

leaving exactly the three anomaly points in quotient coordinates:

    (right,c) = (0,46), (1,47), (2,48).

That three-point diagonal defect fails the selected-defect value identities
and the raw producer identities.  Thus scalar balancing fixes degree but does
not place the q-binomial anomaly in a harmless homogeneous kernel.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    coord_from_q,
    q_from_coord,
)
from p25_laneB_square_axis_scalar_balance_escape_gate import scalar_balanced_vector
from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    raw_producer_conditions,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


SQUARE_C = 169
QUOTIENT_ORDER = RIGHT_DEGREE * SQUARE_C


@dataclass(frozen=True)
class DefectProfile:
    modulus_name: str
    modulus: int
    scalar_component: int
    scalar_cancels: bool
    packet_degree: int
    packet_raw_producer_ok: bool
    defect_support: tuple[tuple[int, int], ...]
    defect_values: tuple[int, ...]
    defect_row_sums: tuple[int, int, int]
    defect_c_zero_values: tuple[int, int, int]
    inversion_sum_values: tuple[int, ...]
    value_conditions_ok: bool


def q_vector_to_packet(q_values: list[int]) -> list[int]:
    return [
        q_values[q_from_coord(right, c_coord)]
        for right in range(RIGHT_DEGREE)
        for c_coord in range(SQUARE_C)
    ]


def negative_anomaly_packet(modulus: int) -> list[int]:
    q_values = [0] * QUOTIENT_ORDER
    for q_value in anomaly_orbit():
        q_values[q_value] = modulus - 1
    return q_vector_to_packet(q_values)


def scalar_packet(modulus: int) -> list[int]:
    scalar = 3 * pow(QUOTIENT_ORDER, -1, modulus) % modulus
    return [scalar] * QUOTIENT_ORDER


def support_coords(row: list[int], modulus: int) -> tuple[tuple[int, int], ...]:
    coords: list[tuple[int, int]] = []
    for right in range(RIGHT_DEGREE):
        for c_coord in range(SQUARE_C):
            if row[right * SQUARE_C + c_coord] % modulus:
                coords.append((right, c_coord))
    return tuple(coords)


def inversion_sum_values(row: list[int], modulus: int) -> tuple[int, ...]:
    values: set[int] = set()
    for right in range(RIGHT_DEGREE):
        for c_coord in range(1, SQUARE_C):
            values.add(
                (
                    row[right * SQUARE_C + c_coord]
                    + row[
                        ((-right) % RIGHT_DEGREE) * SQUARE_C
                        + ((-c_coord) % SQUARE_C)
                    ]
                )
                % modulus
            )
    return tuple(sorted(values))


def profile(modulus_name: str, modulus: int) -> DefectProfile:
    q_values = scalar_balanced_vector(modulus)
    packet = q_vector_to_packet(q_values)
    scalar = scalar_packet(modulus)
    neg_anomaly = negative_anomaly_packet(modulus)
    defect = selected_defect(packet, SQUARE_C, modulus)
    scalar_defect = selected_defect(scalar, SQUARE_C, modulus)
    neg_anomaly_defect = selected_defect(neg_anomaly, SQUARE_C, modulus)
    coords = support_coords(defect, modulus)
    values = tuple(defect[right * SQUARE_C + c_coord] for right, c_coord in coords)
    row_sums = tuple(
        sum(defect[right * SQUARE_C : (right + 1) * SQUARE_C]) % modulus
        for right in range(RIGHT_DEGREE)
    )
    c_zero_values = tuple(defect[right * SQUARE_C] for right in range(RIGHT_DEGREE))
    return DefectProfile(
        modulus_name=modulus_name,
        modulus=modulus,
        scalar_component=scalar[0],
        scalar_cancels=(
            all(value == 0 for value in scalar_defect)
            and defect == neg_anomaly_defect
        ),
        packet_degree=sum(packet) % modulus,
        packet_raw_producer_ok=raw_producer_conditions(packet, SQUARE_C, modulus),
        defect_support=coords,
        defect_values=values,
        defect_row_sums=row_sums,  # type: ignore[arg-type]
        defect_c_zero_values=c_zero_values,  # type: ignore[arg-type]
        inversion_sum_values=inversion_sum_values(defect, modulus),
        value_conditions_ok=value_conditions_hold(defect, SQUARE_C, modulus),
    )


def main() -> int:
    quotient_modulus = split_prime_for(QUOTIENT_ORDER)
    raw_split_modulus = split_prime_for(25 * QUOTIENT_ORDER)
    profiles = (
        profile("quotient", quotient_modulus),
        profile("raw_split", raw_split_modulus),
    )
    expected_support = tuple(coord_from_q(q_value) for q_value in anomaly_orbit())
    print("p25 Lane B square-axis scalar-balance selected-defect gate")
    print(f"square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    ok_rows = 0
    for row in profiles:
        row_ok = (
            row.scalar_cancels
            and row.packet_degree == 0
            and not row.packet_raw_producer_ok
            and row.defect_support == expected_support
            and row.defect_values == (row.modulus - 1,) * 3
            and row.defect_row_sums == (row.modulus - 1,) * 3
            and row.defect_c_zero_values == (0, 0, 0)
            and row.inversion_sum_values == (0, row.modulus - 1)
            and not row.value_conditions_ok
        )
        ok_rows += int(row_ok)
        print(
            f"profile {row.modulus_name}: "
            f"modulus={row.modulus} "
            f"scalar_component={row.scalar_component} "
            f"scalar_cancels={int(row.scalar_cancels)} "
            f"packet_degree={row.packet_degree} "
            f"packet_raw_producer_ok={int(row.packet_raw_producer_ok)} "
            f"defect_support={list(row.defect_support)} "
            f"defect_values={list(row.defect_values)} "
            f"defect_row_sums={list(row.defect_row_sums)} "
            f"defect_c_zero_values={list(row.defect_c_zero_values)} "
            f"inversion_sum_values={list(row.inversion_sum_values)} "
            f"value_conditions_ok={int(row.value_conditions_ok)} "
            f"ok={int(row_ok)}"
        )
    print("interpretation")
    print("  scalar_background_cancels_under_selected_defect=1")
    print("  scalar_balance_leaves_the_three_point_anomaly_defect_visible=1")
    print("  anomaly_defect_fails_value_side_and_raw_producer_identities=1")
    print("  q_binomial_escape_is_not_in_the_homogeneous_selected_defect_kernel=1")
    print(f"square_axis_scalar_balance_defect_rows={ok_rows}/{len(profiles)}")
    print("conclusion=reported_p25_laneB_square_axis_scalar_balance_defect_gate")
    return 0 if ok_rows == len(profiles) else 1


if __name__ == "__main__":
    raise SystemExit(main())
