#!/usr/bin/env python3
"""Square-axis local graph-residue gate for p25 Lane B.

The graph-lift Fourier gate describes the C_169 boundary residual on the
quotient C_3 x C_169.  This gate pushes that graph down to the actual local
source cycle.

For the square-axis case the raw order is

    12675 = 25 * 507,  with quotient order 507 = 3 * 169.

The 18 residual quotient points lift to 18 residue classes modulo 507, each
with exactly 25 raw exponents.  Equivalently, the residual is the triangular
comb

    q = 43*(h+1) + 172*s + 9*t  mod 507,
    h = 0,1,2,  s = 0,1,2,  t = 0..h.

Each class is a product rectangle in the actual local data: one singleton
mod677 C-source residue and one 25-element mod151 right-source coset.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    P25,
    precompute_source_logs,
    quotient_coordinates,
    quotient_exponent,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


BASE_C = 13
SQUARE_C = BASE_C * BASE_C
QUOTIENT_ORDER = RIGHT_DEGREE * SQUARE_C
RAW_ORDER = 25 * QUOTIENT_ORDER


@dataclass(frozen=True)
class LocalClassProfile:
    q_value: int
    right: int
    residue: int
    fiber: int
    h_value: int
    source_exponent_count: int
    right_residue_count: int
    c_residue_count: int
    right_log_mod3_values: tuple[int, ...]
    c_log_values: tuple[int, ...]


def case_by_name(name: str):
    for case in PULLBACK_CASES:
        if case.name == name:
            return case
    raise ValueError(f"unknown pullback case: {name}")


def residual_bit(right: int, c_coord: int) -> int:
    residue = c_coord % BASE_C
    fiber = c_coord // BASE_C
    h_value = (right - residue) % RIGHT_DEGREE
    boundary = 9 - 3 * h_value
    return int(template_bits(BASE_C, residue)[right] and fiber == boundary)


def triangular_parameters() -> list[tuple[int, int, int, int, int, int]]:
    rows: list[tuple[int, int, int, int, int, int]] = []
    for h_value in range(RIGHT_DEGREE):
        for s_value in range(RIGHT_DEGREE):
            for t_value in range(h_value + 1):
                right = (s_value + h_value + 1) % RIGHT_DEGREE
                residue = 10 - 3 * h_value + s_value + 3 * t_value
                fiber = 9 - 3 * h_value
                c_coord = residue + BASE_C * fiber
                q_value = (SQUARE_C * right + RIGHT_DEGREE * c_coord) % QUOTIENT_ORDER
                expected_q = (
                    43 * (h_value + 1) + 172 * s_value + 9 * t_value
                ) % QUOTIENT_ORDER
                if q_value != expected_q:
                    raise AssertionError("triangular q formula mismatch")
                rows.append((h_value, s_value, t_value, right, c_coord, q_value))
    return rows


def quotient_residual_points() -> dict[int, tuple[int, int, int, int]]:
    points: dict[int, tuple[int, int, int, int]] = {}
    for right in range(RIGHT_DEGREE):
        for c_coord in range(SQUARE_C):
            if not residual_bit(right, c_coord):
                continue
            residue = c_coord % BASE_C
            fiber = c_coord // BASE_C
            h_value = (right - residue) % RIGHT_DEGREE
            q_value = (SQUARE_C * right + RIGHT_DEGREE * c_coord) % QUOTIENT_ORDER
            points[q_value] = (right, residue, fiber, h_value)
    return points


def local_class_profile(case, q_value: int, right: int, c_coord: int) -> LocalClassProfile:
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator = pow(P25, case.rho_exp, right_source.modulus)
    c_generator = pow(P25, case.rho_exp, c_source.modulus)
    source_exponents = [q_value + QUOTIENT_ORDER * lift for lift in range(case.b_trace)]
    right_residues = {
        pow(right_generator, exponent, right_source.modulus)
        for exponent in source_exponents
    }
    c_residues = {
        pow(c_generator, exponent, c_source.modulus)
        for exponent in source_exponents
    }
    right_logs = tuple(sorted({exponent % right_source.expected_order % RIGHT_DEGREE for exponent in source_exponents}))
    c_logs = tuple(sorted({exponent % c_source.expected_order for exponent in source_exponents}))
    residue = c_coord % BASE_C
    fiber = c_coord // BASE_C
    h_value = (right - residue) % RIGHT_DEGREE
    return LocalClassProfile(
        q_value=q_value,
        right=right,
        residue=residue,
        fiber=fiber,
        h_value=h_value,
        source_exponent_count=len(source_exponents),
        right_residue_count=len(right_residues),
        c_residue_count=len(c_residues),
        right_log_mod3_values=right_logs,
        c_log_values=c_logs,
    )


def main() -> int:
    print("p25 Lane B square-axis local graph-residue gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    case = case_by_name("square_axis_C3xC169")
    source_logs = precompute_source_logs(case)
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]

    quotient_hits = 0
    residual_raw_hits = 0
    raw_by_q: dict[int, int] = {}
    for e_value, (right, c_coord) in enumerate(coordinates):
        q_value = quotient_exponent(case, right, c_coord)
        quotient_hits += int(q_value == e_value % QUOTIENT_ORDER)
        bit = residual_bit(right, c_coord)
        residual_raw_hits += bit
        if bit:
            raw_by_q[q_value] = raw_by_q.get(q_value, 0) + 1

    graph_points = quotient_residual_points()
    triangular_rows = triangular_parameters()
    triangular_qs = {q_value for _h, _s, _t, _right, _c_coord, q_value in triangular_rows}
    graph_qs = set(graph_points)
    raw_qs = set(raw_by_q)
    q_sets_match = graph_qs == triangular_qs == raw_qs

    class_profiles: list[LocalClassProfile] = []
    class_rows_ok = 0
    for h_value, s_value, t_value, right, c_coord, q_value in triangular_rows:
        residue = c_coord % BASE_C
        fiber = c_coord // BASE_C
        graph_point = graph_points.get(q_value)
        profile = local_class_profile(case, q_value, right, c_coord)
        class_profiles.append(profile)
        row_ok = (
            graph_point == (right, residue, fiber, h_value)
            and raw_by_q.get(q_value) == case.b_trace == 25
            and profile.source_exponent_count == 25
            and profile.right_residue_count == 25
            and profile.c_residue_count == 1
            and profile.right_log_mod3_values == (right,)
            and profile.c_log_values == ((RIGHT_DEGREE * c_coord) % SQUARE_C,)
            and residual_bit(right, c_coord) == 1
            and q_value == (43 * (h_value + 1) + 172 * s_value + 9 * t_value) % QUOTIENT_ORDER
        )
        class_rows_ok += int(row_ok)

    h_q_counts = [0, 0, 0]
    h_raw_counts = [0, 0, 0]
    h_boundary_fibers: list[set[int]] = [set(), set(), set()]
    for profile in class_profiles:
        h_q_counts[profile.h_value] += 1
        h_raw_counts[profile.h_value] += raw_by_q[profile.q_value]
        h_boundary_fibers[profile.h_value].add(profile.fiber)

    expected_h_q_counts = [3, 6, 9]
    expected_h_raw_counts = [75, 150, 225]
    expected_h_boundary_fibers = [{9}, {6}, {3}]
    row_ok = (
        case.raw_order == RAW_ORDER
        and quotient_hits == case.raw_order
        and residual_raw_hits == 18 * case.b_trace == 450
        and len(graph_points) == 18
        and len(triangular_rows) == 18
        and q_sets_match
        and all(count == case.b_trace for count in raw_by_q.values())
        and class_rows_ok == 18
        and h_q_counts == expected_h_q_counts
        and h_raw_counts == expected_h_raw_counts
        and h_boundary_fibers == expected_h_boundary_fibers
    )

    print(
        f"case {case.name}: "
        f"raw_order={case.raw_order} B={case.b_trace} "
        f"quotient_hits={quotient_hits}/{case.raw_order} "
        f"residual_raw_hits={residual_raw_hits}/450 "
        f"graph_q_count={len(graph_points)}/18 "
        f"triangular_q_count={len(triangular_rows)}/18 "
        f"raw_q_count={len(raw_by_q)}/18 "
        f"q_sets_match={int(q_sets_match)} "
        f"class_rows={class_rows_ok}/18 "
        f"h_q_counts={h_q_counts} "
        f"h_raw_counts={h_raw_counts} "
        f"h_boundary_fibers={[sorted(values) for values in h_boundary_fibers]} "
        f"ok={int(row_ok)}"
    )
    print("triangular_q_law")
    print("  q = 43*(h+1) + 172*s + 9*t mod 507")
    print("  h = 0,1,2; s = 0,1,2; t = 0..h")
    print("local_classes")
    for profile in sorted(class_profiles, key=lambda item: item.q_value):
        print(
            f"  q={profile.q_value}: "
            f"right={profile.right} a={profile.residue} b={profile.fiber} h={profile.h_value} "
            f"raw_lift={raw_by_q[profile.q_value]} "
            f"right_residue_count={profile.right_residue_count} "
            f"c_residue_count={profile.c_residue_count} "
            f"right_log_mod3={list(profile.right_log_mod3_values)} "
            f"c_log={list(profile.c_log_values)}"
        )
    print(f"square_axis_local_graph_residue_rows={int(row_ok)}/1")
    print("interpretation")
    print("  graph_lift_residual_is_an_explicit_18_class_comb_mod_507=1")
    print("  every_residual_class_lifts_to_25_raw_exponents=1")
    print("  each_class_is_one_mod677_singleton_times_one_25_element_mod151_coset=1")
    print("  local_square_axis_producer_must_realize_the_triangular_exponent_comb=1")
    print("conclusion=reported_p25_laneB_square_axis_local_graph_residue_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
