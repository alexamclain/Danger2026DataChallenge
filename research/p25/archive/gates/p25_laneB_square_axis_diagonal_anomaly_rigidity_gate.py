#!/usr/bin/env python3
"""Rigidity gate for the selected-defect-visible diagonal anomaly.

The scalar-balance selected-defect gate leaves exactly three visible points:

    (right, c) = (0,46), (1,47), (2,48).

This gate records what those points are in the square-axis geometry.  They are
not an arbitrary blemish: they are the single S-orbit term X^3 Y, equivalently
the fixed h=2, t=1 middle slice of the bottom boundary fiber.  The support is a
diagonal graph, not a row-only, C-only, row-plus-column, or proper congruence
pullback correction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    BASE_C,
    QUOTIENT_ORDER,
    SQUARE_C,
    triangular_parameters,
)
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class DiagonalPoint:
    q_value: int
    right: int
    c_coord: int
    residue: int
    fiber: int
    h_value: int
    s_value: int
    t_value: int
    base43_digit: int
    base43_remainder: int


@dataclass(frozen=True)
class PullbackProfile:
    divisor: int
    residue_count: int
    pullback_size: int
    exact_pullback: bool
    residues: tuple[int, ...]


def diagonal_points() -> list[DiagonalPoint]:
    triangular_by_q = {
        q_value: (h_value, s_value, t_value, right, c_coord)
        for h_value, s_value, t_value, right, c_coord, q_value in triangular_parameters()
    }
    rows: list[DiagonalPoint] = []
    for q_value in anomaly_orbit():
        h_value, s_value, t_value, right, c_coord = triangular_by_q[q_value]
        coord_right, coord_c = coord_from_q(q_value)
        if (right, c_coord) != (coord_right, coord_c):
            raise AssertionError("quotient-coordinate mismatch")
        rows.append(
            DiagonalPoint(
                q_value=q_value,
                right=right,
                c_coord=c_coord,
                residue=c_coord % BASE_C,
                fiber=c_coord // BASE_C,
                h_value=h_value,
                s_value=s_value,
                t_value=t_value,
                base43_digit=q_value // X_STEP,
                base43_remainder=q_value % X_STEP,
            )
        )
    return rows


def support() -> set[tuple[int, int]]:
    return {(point.right, point.c_coord) for point in diagonal_points()}


def selected_value(right: int, c_coord: int) -> int:
    return -1 if (right, c_coord) in support() else 0


def mixed_second_differences() -> tuple[int, ...]:
    cols = sorted({c_coord for _right, c_coord in support()})
    values: set[int] = set()
    for r0, r1 in combinations(range(RIGHT_DEGREE), 2):
        for c0, c1 in combinations(cols, 2):
            values.add(
                selected_value(r0, c0)
                + selected_value(r1, c1)
                - selected_value(r0, c1)
                - selected_value(r1, c0)
            )
    return tuple(sorted(values))


def divisor_pullback_profiles() -> list[PullbackProfile]:
    anomaly = set(anomaly_orbit())
    profiles: list[PullbackProfile] = []
    for divisor in (1, 3, 13, 39, 169):
        residues = tuple(sorted({q_value % divisor for q_value in anomaly}))
        pullback = {
            q_value for q_value in range(QUOTIENT_ORDER) if q_value % divisor in residues
        }
        profiles.append(
            PullbackProfile(
                divisor=divisor,
                residue_count=len(residues),
                pullback_size=len(pullback),
                exact_pullback=pullback == anomaly,
                residues=residues,
            )
        )
    return profiles


def residual_slice_counts() -> tuple[Counter[tuple[int, int]], Counter[int]]:
    ht_counts: Counter[tuple[int, int]] = Counter()
    h_counts: Counter[int] = Counter()
    for h_value, _s_value, t_value, _right, _c_coord, _q_value in triangular_parameters():
        ht_counts[(h_value, t_value)] += 1
        h_counts[h_value] += 1
    return ht_counts, h_counts


def main() -> int:
    print("p25 Lane B square-axis diagonal-anomaly rigidity gate")
    print(f"right_degree={RIGHT_DEGREE} square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    points = diagonal_points()
    anomaly = [point.q_value for point in points]
    coords = [(point.right, point.c_coord) for point in points]
    residues = [point.residue for point in points]
    fibers = [point.fiber for point in points]
    h_values = [point.h_value for point in points]
    s_values = [point.s_value for point in points]
    t_values = [point.t_value for point in points]
    base43_digits = [point.base43_digit for point in points]
    base43_remainders = [point.base43_remainder for point in points]
    ht_counts, h_counts = residual_slice_counts()
    pullback_profiles = divisor_pullback_profiles()
    diffs = mixed_second_differences()
    quotient_modulus = split_prime_for(QUOTIENT_ORDER)
    raw_split_modulus = split_prime_for(25 * QUOTIENT_ORDER)
    odd_field_diff_nonzero = all(
        any(diff % modulus for diff in diffs)
        for modulus in (quotient_modulus, raw_split_modulus)
    )
    row_counts = Counter(right for right, _c_coord in coords)
    col_counts = Counter(c_coord for _right, c_coord in coords)
    diagonal_constant = {(point.c_coord - point.right) % SQUARE_C for point in points}
    residue_diagonal_constant = {
        (point.residue - point.right) % BASE_C for point in points
    }
    q_step_deltas = [
        (anomaly[(index + 1) % len(anomaly)] - anomaly[index]) % QUOTIENT_ORDER
        for index in range(len(anomaly))
    ]
    q_offsets_from_seed = [
        (q_value - (X_STEP * 3 + Y_STEP)) % QUOTIENT_ORDER for q_value in anomaly
    ]

    expected_coords = [(0, 46), (1, 47), (2, 48)]
    expected_pullback_sizes = {1: 507, 3: 507, 13: 117, 39: 39, 169: 9}
    row_ok = (
        anomaly == [138, 310, 482]
        and coords == expected_coords
        and residues == [7, 8, 9]
        and fibers == [3, 3, 3]
        and h_values == [2, 2, 2]
        and s_values == [0, 1, 2]
        and t_values == [1, 1, 1]
        and base43_digits == [3, 7, 11]
        and base43_remainders == [Y_STEP, Y_STEP, Y_STEP]
        and all((digit - 1) % 4 == 2 for digit in base43_digits)
        and ht_counts[(2, 1)] == 3
        and h_counts[2] == 9
        and set(coords)
        == {
            (point.right, point.c_coord)
            for point in points
            if point.h_value == 2 and point.t_value == 1
        }
        and row_counts == Counter({0: 1, 1: 1, 2: 1})
        and col_counts == Counter({46: 1, 47: 1, 48: 1})
        and diagonal_constant == {46}
        and residue_diagonal_constant == {7}
        and q_step_deltas == [S_STEP, S_STEP, 163]
        and q_offsets_from_seed == [0, S_STEP, 2 * S_STEP]
        and diffs == (-2, -1, 1)
        and odd_field_diff_nonzero
        and all(not profile.exact_pullback for profile in pullback_profiles)
        and {
            profile.divisor: profile.pullback_size for profile in pullback_profiles
        }
        == expected_pullback_sizes
        and X_STEP * 3 + Y_STEP == 138
    )

    print(
        "diagonal_anomaly: "
        f"q_values={anomaly} "
        f"coords={coords} "
        f"residues={residues} "
        f"fibers={fibers} "
        f"h_values={h_values} "
        f"s_values={s_values} "
        f"t_values={t_values} "
        f"base43_digits={base43_digits} "
        f"base43_remainders={base43_remainders} "
        f"q_step_deltas={q_step_deltas} "
        f"q_offsets_from_seed={q_offsets_from_seed} "
        f"ok={int(row_ok)}"
    )
    print(
        "slice_profile: "
        f"h2_total={h_counts[2]} "
        f"h2_t0={ht_counts[(2, 0)]} "
        f"h2_t1={ht_counts[(2, 1)]} "
        f"h2_t2={ht_counts[(2, 2)]} "
        f"diagonal_c_minus_right={sorted(diagonal_constant)} "
        f"diagonal_residue_minus_right={sorted(residue_diagonal_constant)}"
    )
    print(
        "separation_tests: "
        f"row_counts={dict(sorted(row_counts.items()))} "
        f"column_counts={dict(sorted(col_counts.items()))} "
        f"mixed_second_differences={list(diffs)} "
        f"quotient_modulus={quotient_modulus} "
        f"raw_split_modulus={raw_split_modulus} "
        f"odd_field_diff_nonzero={int(odd_field_diff_nonzero)}"
    )
    print("proper_divisor_pullback_profiles")
    for profile in pullback_profiles:
        print(
            f"  divisor={profile.divisor} "
            f"residue_count={profile.residue_count} "
            f"pullback_size={profile.pullback_size} "
            f"exact_pullback={int(profile.exact_pullback)} "
            f"residues={list(profile.residues)}"
        )
    print("diagonal_anomaly_law")
    print("  anomaly = (1 + D + D^2) * X^3 * Y")
    print("  anomaly = fixed h=2, t=1 slice of the square-axis residual")
    print("  quotient coordinates satisfy c-right = 46 and residue-right = 7")
    print(f"square_axis_diagonal_anomaly_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  scalar_balance_leaves_a_specific_middle_slice_not_random_noise=1")
    print("  diagonal_defect_is_not_row_only_C_only_or_row_plus_column=1")
    print("  diagonal_defect_is_not_a_proper_modulus_pullback=1")
    print("  producer_must_cancel_the_fixed_h2_t1_coefficient_slice=1")
    print("conclusion=reported_p25_laneB_square_axis_diagonal_anomaly_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
