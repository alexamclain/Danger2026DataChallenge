#!/usr/bin/env python3
"""Antiderivative rigidity for the p25 square-axis bridge.

The bridge factorization gate showed that the legal six-point correction is

    S * X * Y^-2 * (1 - X^2Y^3).

This gate asks a slightly broader question.  For every nonzero direction d in
C_507, solve

    F(q) - F(q + d) = bridge(q)

and minimize the support of F by adding constants on each d-cycle.  If a
producer tries to explain the bridge merely as a sparse first difference, this
enumeration identifies all possible directions.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import (
    BRIDGE_STEP,
    bridge_coefficients,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import MODULUS
from p25_laneB_square_axis_inversion_partner_uniqueness_gate import (
    ANOMALY_BASE,
    PARTNER_BASE,
    s_layer,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class DirectionProfile:
    direction: int
    cycle_count: int
    minimal_support: int
    support: tuple[int, ...]
    support_coefficients: tuple[tuple[int, int], ...]
    degree: int
    cycle_supports: tuple[int, ...]
    primitive_direction: bool
    degree_zero_support_mod: int | None


def cycles_for_direction(direction: int) -> tuple[tuple[int, ...], ...]:
    seen = [False] * QUOTIENT_ORDER
    cycles: list[tuple[int, ...]] = []
    for start in range(QUOTIENT_ORDER):
        if seen[start]:
            continue
        cycle: list[int] = []
        q_value = start
        while not seen[q_value]:
            seen[q_value] = True
            cycle.append(q_value)
            q_value = (q_value + direction) % QUOTIENT_ORDER
        cycles.append(tuple(cycle))
    return tuple(cycles)


def minimize_cycle_values(
    cycle: tuple[int, ...],
    coefficients: dict[int, int],
    direction: int,
) -> tuple[dict[int, int], int] | None:
    values = {cycle[0]: 0}
    current = 0
    for q_value in cycle[:-1]:
        current -= coefficients.get(q_value, 0)
        values[(q_value + direction) % QUOTIENT_ORDER] = current

    if values[cycle[-1]] - values[cycle[0]] != coefficients.get(cycle[-1], 0):
        return None

    counts = Counter(values[q_value] for q_value in cycle)
    best_frequency = max(counts.values())
    zero_value = min(value for value, frequency in counts.items() if frequency == best_frequency)
    minimized = {q_value: values[q_value] - zero_value for q_value in cycle}
    support = sum(1 for value in minimized.values() if value)
    return minimized, support


def degree_zero_support_mod(values: dict[int, int], degree: int) -> int:
    scalar = (-degree * pow(QUOTIENT_ORDER, -1, MODULUS)) % MODULUS
    return sum(1 for q_value in range(QUOTIENT_ORDER) if (values[q_value] + scalar) % MODULUS)


def direction_profile(direction: int) -> DirectionProfile | None:
    coefficients = bridge_coefficients()
    values: dict[int, int] = {}
    cycle_supports: list[int] = []
    cycles = cycles_for_direction(direction)
    for cycle in cycles:
        minimized = minimize_cycle_values(cycle, coefficients, direction)
        if minimized is None:
            return None
        cycle_values, cycle_support = minimized
        values.update(cycle_values)
        cycle_supports.append(cycle_support)

    support = tuple(sorted(q_value for q_value, value in values.items() if value))
    support_coefficients = tuple((q_value, values[q_value]) for q_value in support)
    degree = sum(values.values())
    primitive = gcd(direction, QUOTIENT_ORDER) == 1
    return DirectionProfile(
        direction=direction,
        cycle_count=len(cycles),
        minimal_support=len(support),
        support=support,
        support_coefficients=support_coefficients,
        degree=degree,
        cycle_supports=tuple(sorted(cycle_supports)),
        primitive_direction=primitive,
        degree_zero_support_mod=degree_zero_support_mod(values, degree) if primitive else None,
    )


def all_profiles() -> tuple[DirectionProfile, ...]:
    profiles: list[DirectionProfile] = []
    for direction in range(1, QUOTIENT_ORDER):
        profile = direction_profile(direction)
        if profile is not None:
            profiles.append(profile)
    return tuple(profiles)


def main() -> int:
    print("p25 Lane B square-axis bridge-antiderivative rigidity gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} modulus={MODULUS} "
        f"bridge_step={BRIDGE_STEP} reverse_step={(-BRIDGE_STEP) % QUOTIENT_ORDER}"
    )
    profiles = all_profiles()
    impossible_count = (QUOTIENT_ORDER - 1) - len(profiles)
    support_distribution = Counter(profile.minimal_support for profile in profiles)
    minimum_support = min(support_distribution)
    second_support = min(value for value in support_distribution if value > minimum_support)
    minimum_profiles = tuple(
        profile for profile in profiles if profile.minimal_support == minimum_support
    )
    second_profiles = tuple(
        profile for profile in profiles if profile.minimal_support == second_support
    )

    expected_minimum = (
        DirectionProfile(
            direction=BRIDGE_STEP,
            cycle_count=1,
            minimal_support=3,
            support=tuple(sorted(s_layer(ANOMALY_BASE))),
            support_coefficients=tuple((q_value, -1) for q_value in sorted(s_layer(ANOMALY_BASE))),
            degree=-3,
            cycle_supports=(3,),
            primitive_direction=True,
            degree_zero_support_mod=QUOTIENT_ORDER,
        ),
        DirectionProfile(
            direction=(-BRIDGE_STEP) % QUOTIENT_ORDER,
            cycle_count=1,
            minimal_support=3,
            support=tuple(sorted(s_layer(PARTNER_BASE))),
            support_coefficients=tuple((q_value, 1) for q_value in sorted(s_layer(PARTNER_BASE))),
            degree=3,
            cycle_supports=(3,),
            primitive_direction=True,
            degree_zero_support_mod=QUOTIENT_ORDER,
        ),
    )

    row_ok = (
        len(profiles) == 468
        and impossible_count == 38
        and minimum_support == 3
        and second_support == 6
        and tuple(sorted(minimum_profiles, key=lambda row: row.direction)) == expected_minimum
        and tuple(profile.direction for profile in second_profiles) == (197, 310)
        and all(profile.degree_zero_support_mod == QUOTIENT_ORDER for profile in minimum_profiles)
    )

    print(
        "antiderivative_scan: "
        f"possible_directions={len(profiles)} "
        f"impossible_directions={impossible_count} "
        f"minimum_support={minimum_support} "
        f"second_support={second_support} "
        f"ok={int(row_ok)}"
    )
    print(f"support_distribution={dict(sorted(support_distribution.items()))}")
    print("minimum_profiles")
    for profile in minimum_profiles:
        print(f"  {profile}")
    print("second_profiles")
    for profile in second_profiles:
        print(f"  {profile}")
    print("degree_zero_repair")
    print("  the two support-3 antiderivatives are primitive one-cycle directions")
    print("  forcing degree zero over F_2029 adds a nonzero scalar on every q in C_507")
    print(f"  degree_zero_support_mod_2029={QUOTIENT_ORDER}/{QUOTIENT_ORDER}")
    print("interpretation")
    print("  only_the_bridge_step_and_reverse_have_three_point_antiderivatives=1")
    print("  every_other_first_difference_direction_needs_support_at_least_six=1")
    print("  sparse_bridge_antiderivatives_have_degree_plus_or_minus_three=1")
    print("  degree_zero_first_difference_repair_is_dense_on_C507=1")
    print("  producer_must_explain_the_specific_top_to_bottom_bridge_not_an_alternate_sparse_boundary=1")
    print(f"square_axis_bridge_antiderivative_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_antiderivative_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
