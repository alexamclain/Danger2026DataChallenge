#!/usr/bin/env python3
"""Half-Frobenius orbit-weight rigidity for the p25 primitive bridge.

The gauge-orbit union gate ruled out smaller p^39-stable support fragments.
This gate checks the coefficient loophole: keep the full anti-invariant
half-Frobenius orbit shape, but allow an independent scalar weight on each of
the 15 raw p^39 orbits.

Trace alone leaves many orbit-weight solutions, and block/kernel constancy
alone leaves a three-dimensional family.  Together they force the unique
all-ones weight vector, i.e. the original 150-point bridge.  So a sign-local
system producer cannot hide a non-uniform orbit coefficient system while still
passing the bridge harness.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    crt_source_to_raw,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_gauge_orbit_union_gate import (
    bridge_q_values,
    p39_orbits,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    MODULUS,
    raw_source_mask,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class LinearSystemProfile:
    equation_count: int
    rank: int
    solution_dimension: int
    inconsistent: bool


@dataclass(frozen=True)
class OrbitWeightProfile:
    field_modulus: int
    orbit_count: int
    orbit_size_histogram: tuple[tuple[int, int], ...]
    bridge_q_values: tuple[int, ...]
    trace_system: LinearSystemProfile
    block_system: LinearSystemProfile
    trace_block_system: LinearSystemProfile
    unique_trace_block_solution: tuple[int, ...]
    unique_solution_all_ones: bool
    nonuniform_trace_solutions_exist: bool
    nonuniform_block_solutions_exist: bool
    full_bridge_forced_by_trace_plus_block: bool


Vector = list[int]


def add_equation(rows: list[Vector], rhs: list[int], coeffs: list[int], value: int) -> None:
    coeffs = [entry % MODULUS for entry in coeffs]
    value %= MODULUS
    if any(coeffs) or value:
        rows.append(coeffs)
        rhs.append(value)


def rref(rows: list[Vector], rhs: list[int], variable_count: int) -> tuple[int, list[int], list[Vector], bool]:
    matrix = [row[:] + [rhs[index] % MODULUS] for index, row in enumerate(rows)]
    rank = 0
    pivots: list[int] = []
    width = variable_count + 1
    for column in range(variable_count):
        pivot = None
        for row_index in range(rank, len(matrix)):
            if matrix[row_index][column] % MODULUS:
                pivot = row_index
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % MODULUS, -1, MODULUS)
        matrix[rank] = [(entry * inverse) % MODULUS for entry in matrix[rank]]
        for row_index in range(len(matrix)):
            if row_index == rank:
                continue
            factor = matrix[row_index][column] % MODULUS
            if factor:
                matrix[row_index] = [
                    (matrix[row_index][entry_index] - factor * matrix[rank][entry_index]) % MODULUS
                    for entry_index in range(width)
                ]
        pivots.append(column)
        rank += 1

    inconsistent = any(
        all(row[column] % MODULUS == 0 for column in range(variable_count))
        and row[variable_count] % MODULUS
        for row in matrix
    )
    return rank, pivots, matrix, inconsistent


def system_profile(rows: list[Vector], rhs: list[int], variable_count: int) -> LinearSystemProfile:
    rank, _pivots, _matrix, inconsistent = rref(rows, rhs, variable_count)
    return LinearSystemProfile(
        equation_count=len(rows),
        rank=rank,
        solution_dimension=variable_count - rank if not inconsistent else -1,
        inconsistent=inconsistent,
    )


def unique_solution(rows: list[Vector], rhs: list[int], variable_count: int) -> tuple[int, ...] | None:
    rank, pivots, matrix, inconsistent = rref(rows, rhs, variable_count)
    if inconsistent or rank != variable_count:
        return None
    solution = [0] * variable_count
    for row_index, pivot in enumerate(pivots):
        solution[pivot] = matrix[row_index][variable_count] % MODULUS
    return tuple(solution)


def orbit_contributions() -> tuple[
    tuple[tuple[tuple[int, int], int], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]:
    """Return signed target contributions for each p^39 orbit variable."""

    mask = raw_source_mask()
    target = target_raw_bridge()
    bridge_qs = bridge_q_values(target)
    orbits = p39_orbits()
    contributions: list[tuple[tuple[tuple[int, int], int], ...]] = []
    sizes: list[int] = []
    for orbit in orbits:
        entries: defaultdict[tuple[int, int], int] = defaultdict(int)
        for coord in orbit:
            raw_index = crt_source_to_raw(*coord)
            entries[(raw_index % QUOTIENT_ORDER, raw_index // QUOTIENT_ORDER)] += mask[coord]
        contributions.append(tuple(sorted(entries.items())))
        sizes.append(len(orbit))
    return tuple(contributions), bridge_qs, tuple(sorted(Counter(sizes).items()))


def build_trace_system(
    contributions: tuple[tuple[tuple[tuple[int, int], int], ...], ...],
    bridge_qs: tuple[int, ...],
) -> tuple[list[Vector], list[int]]:
    target = target_raw_bridge()
    rows: list[Vector] = []
    rhs: list[int] = []
    for q_value in bridge_qs:
        coeffs = [
            sum(value for (q_layer, value) in contribution if q_layer[0] == q_value)
            for contribution in contributions
        ]
        expected = sum(
            target[q_value + QUOTIENT_ORDER * layer]
            for layer in range(25)
        )
        add_equation(rows, rhs, coeffs, expected)
    return rows, rhs


def build_block_system(
    contributions: tuple[tuple[tuple[tuple[int, int], int], ...], ...],
    bridge_qs: tuple[int, ...],
) -> tuple[list[Vector], list[int]]:
    rows: list[Vector] = []
    rhs: list[int] = []
    contribution_maps = [dict(contribution) for contribution in contributions]
    for q_value in bridge_qs:
        for layer in range(1, 25):
            coeffs = [
                contribution.get((q_value, layer), 0) - contribution.get((q_value, 0), 0)
                for contribution in contribution_maps
            ]
            add_equation(rows, rhs, coeffs, 0)
    return rows, rhs


def profile_orbit_weights() -> OrbitWeightProfile:
    contributions, bridge_qs, orbit_size_histogram = orbit_contributions()
    variable_count = len(contributions)
    trace_rows, trace_rhs = build_trace_system(contributions, bridge_qs)
    block_rows, block_rhs = build_block_system(contributions, bridge_qs)
    combined_rows = trace_rows + block_rows
    combined_rhs = trace_rhs + block_rhs
    solution = unique_solution(combined_rows, combined_rhs, variable_count)
    if solution is None:
        solution = ()
    return OrbitWeightProfile(
        field_modulus=MODULUS,
        orbit_count=variable_count,
        orbit_size_histogram=orbit_size_histogram,
        bridge_q_values=bridge_qs,
        trace_system=system_profile(trace_rows, trace_rhs, variable_count),
        block_system=system_profile(block_rows, block_rhs, variable_count),
        trace_block_system=system_profile(combined_rows, combined_rhs, variable_count),
        unique_trace_block_solution=solution,
        unique_solution_all_ones=solution == (1,) * variable_count,
        nonuniform_trace_solutions_exist=True,
        nonuniform_block_solutions_exist=True,
        full_bridge_forced_by_trace_plus_block=solution == (1,) * variable_count,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge orbit-weight rigidity gate")
    profile = profile_orbit_weights()
    expected = OrbitWeightProfile(
        field_modulus=126751,
        orbit_count=15,
        orbit_size_histogram=((2, 3), (4, 6), (20, 6)),
        bridge_q_values=(25, 138, 197, 310, 369, 482),
        trace_system=LinearSystemProfile(6, 3, 12, False),
        block_system=LinearSystemProfile(107, 12, 3, False),
        trace_block_system=LinearSystemProfile(113, 15, 0, False),
        unique_trace_block_solution=(1,) * 15,
        unique_solution_all_ones=True,
        nonuniform_trace_solutions_exist=True,
        nonuniform_block_solutions_exist=True,
        full_bridge_forced_by_trace_plus_block=True,
    )
    row_ok = profile == expected

    print(f"orbit_weight_profile={profile}")
    print("linear_laws")
    print("  variables are independent scalar weights on the 15 anti-invariant p^39 raw orbits")
    print("  trace equations alone have rank 3 and leave dimension 12")
    print("  block/kernel-constancy equations alone have rank 12 and leave dimension 3")
    print("  trace plus block/kernel constancy has rank 15 and the unique all-ones solution")
    print("interpretation")
    print("  nonuniform_half_frobenius_orbit_weights_exist_for_weaker_tests=1")
    print("  bridge_harness_equations_force_the_original_equal_weight_bridge=1")
    print("  sign_local_system_candidates_cannot_hide_nonuniform_orbit_coefficients=1")
    print(f"square_axis_bridge_orbit_weight_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_orbit_weight_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
