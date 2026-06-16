#!/usr/bin/env python3
"""Coefficient-rigidity screen for p25 Hilbert-90 source chains.

The lift-selection gate identifies the active support-three source graphs.
This gate checks the next possible escape: keep the correct support and the
rigid 197/310 first-boundary direction, but allow nonuniform coefficients on
the three source points.

The double boundary map to the signed bridge has rank three on each active
support, so the coefficient vector is unique.  It is exactly the recorded
all-equal vector, and among the eight sign patterns in {+/-1}^3 only that one
works.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    BoundaryWitness,
    PotentialBoundaryRow,
    boundary,
    inversion_boundary,
    source_boundary_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_lift_selection_gate import (
    one_point_per_row,
)
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import MODULUS


PolyItems = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class CoefficientRigidityRow:
    orientation_mask: int
    boundary_direction_q: int
    q_values: tuple[int, ...]
    recorded_coefficients: tuple[int, ...]
    basis_images: tuple[PolyItems, ...]
    matrix_rank_mod2029: int
    kernel_dimension_mod2029: int
    unique_solution_mod2029: tuple[int, ...]
    unique_solution_signed: tuple[int, ...]
    sign_pattern_hits: tuple[tuple[int, ...], ...]
    coefficient_solution_matches_recorded: bool


@dataclass(frozen=True)
class CoefficientRigidityProfile:
    row_count: int
    all_rows_rank_three: bool
    all_kernels_trivial: bool
    all_solutions_match_recorded: bool
    all_sign_pattern_hits_unique: bool
    rows: tuple[CoefficientRigidityRow, ...]


def normalize(poly: dict[int, int]) -> dict[int, int]:
    return {q_value: value for q_value, value in poly.items() if value}


def add_scaled(target: dict[int, int], source: dict[int, int], scalar: int) -> None:
    for q_value, value in source.items():
        target[q_value] = target.get(q_value, 0) + scalar * value
        if target[q_value] == 0:
            del target[q_value]


def basis_image(q_value: int, direction: int) -> dict[int, int]:
    return inversion_boundary(boundary({q_value: 1}, direction))


def signed_mod(value: int) -> int:
    value %= MODULUS
    return value if value <= MODULUS // 2 else value - MODULUS


def rank_mod(matrix: list[list[int]]) -> int:
    rows = [row[:] for row in matrix]
    rank = 0
    col_count = len(rows[0]) if rows else 0
    for col in range(col_count):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col] % MODULUS), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % MODULUS, -1, MODULUS)
        rows[rank] = [(value * inv) % MODULUS for value in rows[rank]]
        for r, row in enumerate(rows):
            if r == rank or row[col] % MODULUS == 0:
                continue
            factor = row[col] % MODULUS
            rows[r] = [(value - factor * rows[rank][c]) % MODULUS for c, value in enumerate(row)]
        rank += 1
    return rank


def solve_unique_mod(matrix: list[list[int]], rhs: list[int]) -> tuple[int, ...]:
    augmented = [row[:] + [value % MODULUS] for row, value in zip(matrix, rhs)]
    rank = 0
    col_count = len(matrix[0]) if matrix else 0
    pivots: list[int] = []
    for col in range(col_count):
        pivot = next((r for r in range(rank, len(augmented)) if augmented[r][col] % MODULUS), None)
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = pow(augmented[rank][col] % MODULUS, -1, MODULUS)
        augmented[rank] = [(value * inv) % MODULUS for value in augmented[rank]]
        for r, row in enumerate(augmented):
            if r == rank or row[col] % MODULUS == 0:
                continue
            factor = row[col] % MODULUS
            augmented[r] = [
                (value - factor * augmented[rank][c]) % MODULUS
                for c, value in enumerate(row)
            ]
        pivots.append(col)
        rank += 1

    if rank != col_count:
        raise AssertionError(f"solution is not unique: rank={rank}, cols={col_count}")
    for row in augmented[rank:]:
        if all(value % MODULUS == 0 for value in row[:col_count]) and row[-1] % MODULUS:
            raise AssertionError("inconsistent system")

    solution = [0] * col_count
    for row_index, col in enumerate(pivots):
        solution[col] = augmented[row_index][-1] % MODULUS
    return tuple(solution)


def row_system(q_values: tuple[int, ...], direction: int) -> tuple[list[list[int]], list[int], tuple[PolyItems, ...]]:
    columns = tuple(basis_image(q_value, direction) for q_value in q_values)
    support = sorted(set(bridge_coefficients()) | {q_value for column in columns for q_value in column})
    matrix = [[column.get(q_value, 0) % MODULUS for column in columns] for q_value in support]
    rhs = [bridge_coefficients().get(q_value, 0) % MODULUS for q_value in support]
    return matrix, rhs, tuple(tuple(sorted(column.items())) for column in columns)


def sign_pattern_hits(q_values: tuple[int, ...], direction: int) -> tuple[tuple[int, ...], ...]:
    bridge = bridge_coefficients()
    hits: list[tuple[int, ...]] = []
    basis = tuple(basis_image(q_value, direction) for q_value in q_values)
    for coefficients in product((-1, 1), repeat=len(q_values)):
        image: dict[int, int] = {}
        for coefficient, column in zip(coefficients, basis):
            add_scaled(image, column, coefficient)
        if normalize(image) == bridge:
            hits.append(tuple(coefficients))
    return tuple(hits)


def coefficient_row(row: PotentialBoundaryRow, witness: BoundaryWitness) -> CoefficientRigidityRow:
    q_values = tuple(q_value for q_value, _coefficient in witness.antiderivative)
    recorded_coefficients = tuple(coefficient for _q_value, coefficient in witness.antiderivative)
    matrix, rhs, basis_images = row_system(q_values, witness.direction_q)
    rank = rank_mod(matrix)
    solution_mod = solve_unique_mod(matrix, rhs)
    solution_signed = tuple(signed_mod(value) for value in solution_mod)
    hits = sign_pattern_hits(q_values, witness.direction_q)
    return CoefficientRigidityRow(
        orientation_mask=row.orientation_mask,
        boundary_direction_q=witness.direction_q,
        q_values=q_values,
        recorded_coefficients=recorded_coefficients,
        basis_images=basis_images,
        matrix_rank_mod2029=rank,
        kernel_dimension_mod2029=len(q_values) - rank,
        unique_solution_mod2029=solution_mod,
        unique_solution_signed=solution_signed,
        sign_pattern_hits=hits,
        coefficient_solution_matches_recorded=solution_signed == recorded_coefficients,
    )


def coefficient_rigidity_profile() -> CoefficientRigidityProfile:
    boundary_profile = source_boundary_profile()
    rows = tuple(
        coefficient_row(row, witness)
        for row in boundary_profile.rows
        if row.bridge_zero_compatible
        for witness in row.best_witnesses
        if one_point_per_row(tuple(q_value for q_value, _coefficient in witness.antiderivative))
    )
    return CoefficientRigidityProfile(
        row_count=len(rows),
        all_rows_rank_three=all(row.matrix_rank_mod2029 == 3 for row in rows),
        all_kernels_trivial=all(row.kernel_dimension_mod2029 == 0 for row in rows),
        all_solutions_match_recorded=all(row.coefficient_solution_matches_recorded for row in rows),
        all_sign_pattern_hits_unique=all(row.sign_pattern_hits == (row.recorded_coefficients,) for row in rows),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain coefficient-rigidity gate")
    profile = coefficient_rigidity_profile()
    expected_rows = (
        CoefficientRigidityRow(1, 197, (0, 172, 482), (-1, -1, -1), (((197, -1), (310, 1)), ((138, 1), (172, 1), (335, -1), (369, -1)), ((25, -1), (172, -1), (335, 1), (482, 1))), 3, 0, (2028, 2028, 2028), (-1, -1, -1), ((-1, -1, -1),), True),
        CoefficientRigidityRow(1, 310, (172, 197, 369), (1, 1, 1), (((25, 1), (172, 1), (335, -1), (482, -1)), ((197, 1), (310, -1)), ((138, -1), (172, -1), (335, 1), (369, 1))), 3, 0, (1, 1, 1), (1, 1, 1), ((1, 1, 1),), True),
        CoefficientRigidityRow(6, 197, (138, 310, 335), (-1, -1, -1), (((138, 1), (172, 1), (335, -1), (369, -1)), ((197, -1), (310, 1)), ((25, -1), (172, -1), (335, 1), (482, 1))), 3, 0, (2028, 2028, 2028), (-1, -1, -1), ((-1, -1, -1),), True),
        CoefficientRigidityRow(6, 310, (0, 25, 335), (1, 1, 1), (((197, 1), (310, -1)), ((25, 1), (172, 1), (335, -1), (482, -1)), ((138, -1), (172, -1), (335, 1), (369, 1))), 3, 0, (1, 1, 1), (1, 1, 1), ((1, 1, 1),), True),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_rank_three
        and profile.all_kernels_trivial
        and profile.all_solutions_match_recorded
        and profile.all_sign_pattern_hits_unique
        and profile.rows == expected_rows
    )

    print(
        "source_chain_coefficient_rigidity_summary: "
        f"row_count={profile.row_count} "
        f"all_rows_rank_three={int(profile.all_rows_rank_three)} "
        f"all_kernels_trivial={int(profile.all_kernels_trivial)} "
        f"all_solutions_match_recorded={int(profile.all_solutions_match_recorded)} "
        f"all_sign_pattern_hits_unique={int(profile.all_sign_pattern_hits_unique)}"
    )
    print("coefficient_rigidity_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("interpretation")
    print("  active_source_chain_support_and_boundary_direction_force_equal_coefficients=1")
    print("  double_boundary_matrix_has_rank_three_and_trivial_kernel_on_each_active_chain=1")
    print("  no_nonuniform_plusminus_sign_pattern_recovers_the_signed_bridge=1")
    print("  producer_must_realize_the_active_lift_with_the_recorded_all_equal_weight_vector=1")
    print(f"square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
