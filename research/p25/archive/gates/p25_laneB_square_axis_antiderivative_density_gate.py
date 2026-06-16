#!/usr/bin/env python3
"""Density gate for the diagonal anomaly's D-antiderivative.

The boundary gate gives a promising local equation

    (1 - D) A = X^3 Y - X^3 Y^2,
    A = (1 + D + D^2) X^3 Y.

This gate records the catch.  On the quotient 507-cycle, D is a generator, so
solutions to this first-difference equation are unique up to constants.  The
local antiderivative A has support 3 but degree 3.  Forcing degree zero fixes
the constant term and makes the solution dense on all 507 quotient classes.

Thus the signed-D antiderivative clue is real, but a quotient-linear
degree-zero repair is exactly the scalar-balance escape: dense, and still
visible to selected-defect after the scalar cancels.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_selected_defect_value_gate import split_prime_for


RAW_KERNEL_SIZE = 25
RAW_ORDER = RAW_KERNEL_SIZE * QUOTIENT_ORDER


@dataclass(frozen=True)
class AntiderivativeProfile:
    modulus_name: str
    modulus: int
    sparse_support: int
    sparse_degree: int
    sparse_boundary_ok: bool
    degree_zero_constant: int
    degree_zero_support: int
    degree_zero_degree: int
    degree_zero_boundary_ok: bool
    correction_constant: int
    correction_support: int
    correction_degree: int
    correction_boundary_ok: bool
    minus_one_support: int
    minus_one_degree: int
    raw_sparse_block_support: int
    raw_degree_zero_block_support: int


def boundary(vector: list[int], direction: int, modulus: int) -> list[int]:
    out = [0] * len(vector)
    for index, value in enumerate(vector):
        if value % modulus == 0:
            continue
        out[index] = (out[index] + value) % modulus
        out[(index + direction) % len(vector)] = (
            out[(index + direction) % len(vector)] - value
        ) % modulus
    return out


def support_size(vector: list[int], modulus: int) -> int:
    return sum(1 for value in vector if value % modulus)


def degree(vector: list[int], modulus: int) -> int:
    return sum(vector) % modulus


def anomaly_vector(modulus: int, sign: int = 1) -> list[int]:
    vector = [0] * QUOTIENT_ORDER
    for q_value in anomaly_orbit():
        vector[q_value] = sign % modulus
    return vector


def add_constant(vector: list[int], constant: int, modulus: int) -> list[int]:
    return [(value + constant) % modulus for value in vector]


def scalar_constant_for_degree_zero(vector: list[int], modulus: int) -> int:
    return (-degree(vector, modulus) * pow(QUOTIENT_ORDER, -1, modulus)) % modulus


def edge_vector(modulus: int) -> list[int]:
    return boundary(anomaly_vector(modulus), S_STEP, modulus)


def d_cycle() -> list[int]:
    seen: list[int] = []
    current = 0
    for _ in range(QUOTIENT_ORDER):
        seen.append(current)
        current = (current + S_STEP) % QUOTIENT_ORDER
    return seen


def profile(modulus_name: str, modulus: int) -> AntiderivativeProfile:
    sparse = anomaly_vector(modulus)
    edge = edge_vector(modulus)
    sparse_boundary = boundary(sparse, S_STEP, modulus)
    dz_constant = scalar_constant_for_degree_zero(sparse, modulus)
    degree_zero = add_constant(sparse, dz_constant, modulus)

    correction = anomaly_vector(modulus, sign=-1)
    correction_edge = [(-value) % modulus for value in edge]
    correction_constant = scalar_constant_for_degree_zero(correction, modulus)
    degree_zero_correction = add_constant(correction, correction_constant, modulus)
    minus_one_solution = add_constant(sparse, modulus - 1, modulus)

    return AntiderivativeProfile(
        modulus_name=modulus_name,
        modulus=modulus,
        sparse_support=support_size(sparse, modulus),
        sparse_degree=degree(sparse, modulus),
        sparse_boundary_ok=sparse_boundary == edge,
        degree_zero_constant=dz_constant,
        degree_zero_support=support_size(degree_zero, modulus),
        degree_zero_degree=degree(degree_zero, modulus),
        degree_zero_boundary_ok=boundary(degree_zero, S_STEP, modulus) == edge,
        correction_constant=correction_constant,
        correction_support=support_size(degree_zero_correction, modulus),
        correction_degree=degree(degree_zero_correction, modulus),
        correction_boundary_ok=boundary(degree_zero_correction, S_STEP, modulus)
        == correction_edge,
        minus_one_support=support_size(minus_one_solution, modulus),
        minus_one_degree=degree(minus_one_solution, modulus),
        raw_sparse_block_support=RAW_KERNEL_SIZE * support_size(sparse, modulus),
        raw_degree_zero_block_support=RAW_KERNEL_SIZE
        * support_size(degree_zero_correction, modulus),
    )


def main() -> int:
    print("p25 Lane B square-axis antiderivative-density gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} raw_order={RAW_ORDER} "
        f"D={S_STEP} X={X_STEP} Y={Y_STEP}"
    )
    cycle = d_cycle()
    cycle_ok = (
        len(set(cycle)) == QUOTIENT_ORDER
        and cycle[0] == 0
        and cycle[1] == S_STEP
        and cycle[-1] == (-S_STEP) % QUOTIENT_ORDER
        and (cycle[-1] + S_STEP) % QUOTIENT_ORDER == 0
    )
    expected_edge = {
        X_STEP * 3 + Y_STEP: 1,
        X_STEP * 3 + 2 * Y_STEP: -1,
    }
    profiles = (
        profile("quotient", split_prime_for(QUOTIENT_ORDER)),
        profile("raw_split", split_prime_for(RAW_ORDER)),
    )
    edge = edge_vector(profiles[0].modulus)
    edge_support = {
        index: (value if value < profiles[0].modulus // 2 else value - profiles[0].modulus)
        for index, value in enumerate(edge)
        if value
    }

    ok_rows = 0
    for row in profiles:
        row_ok = (
            row.sparse_support == 3
            and row.sparse_degree == 3
            and row.sparse_boundary_ok
            and row.degree_zero_support == QUOTIENT_ORDER
            and row.degree_zero_degree == 0
            and row.degree_zero_boundary_ok
            and row.correction_support == QUOTIENT_ORDER
            and row.correction_degree == 0
            and row.correction_boundary_ok
            and row.minus_one_support == QUOTIENT_ORDER - 3
            and row.minus_one_degree == (3 - QUOTIENT_ORDER) % row.modulus
            and row.raw_sparse_block_support == 75
            and row.raw_degree_zero_block_support == RAW_ORDER
        )
        ok_rows += int(row_ok)
        print(
            f"profile {row.modulus_name}: "
            f"modulus={row.modulus} "
            f"sparse_support={row.sparse_support} "
            f"sparse_degree={row.sparse_degree} "
            f"sparse_boundary_ok={int(row.sparse_boundary_ok)} "
            f"degree_zero_constant={row.degree_zero_constant} "
            f"degree_zero_support={row.degree_zero_support} "
            f"degree_zero_degree={row.degree_zero_degree} "
            f"degree_zero_boundary_ok={int(row.degree_zero_boundary_ok)} "
            f"correction_constant={row.correction_constant} "
            f"correction_support={row.correction_support} "
            f"correction_degree={row.correction_degree} "
            f"correction_boundary_ok={int(row.correction_boundary_ok)} "
            f"minus_one_support={row.minus_one_support} "
            f"minus_one_degree={row.minus_one_degree} "
            f"raw_sparse_block_support={row.raw_sparse_block_support} "
            f"raw_degree_zero_block_support={row.raw_degree_zero_block_support} "
            f"ok={int(row_ok)}"
        )
    row_ok = (
        cycle_ok
        and edge_support == expected_edge
        and ok_rows == len(profiles)
    )
    print(
        "quotient_antiderivative_law: "
        f"D_cycle_generator={int(cycle_ok)} "
        f"edge_support={edge_support} "
        f"edge_degree={sum(edge_support.values())} "
        f"profiles_ok={ok_rows}/{len(profiles)} "
        f"ok={int(row_ok)}"
    )
    print("support_classification")
    print("  A + c has support 3 for c=0, support 504 for c=-1, and support 507 otherwise")
    print("  degree(A+c)=3+507*c, so degree zero forces a dense nonzero scalar")
    print("  -A+c has degree zero at c=3/507, again dense on all quotient classes")
    print(f"square_axis_antiderivative_density_rows={int(row_ok)}/1")
    print("interpretation")
    print("  sparse_D_antiderivative_is_the_visible_degree_three_anomaly=1")
    print("  degree_zero_D_antiderivative_is_forced_to_be_dense=1")
    print("  scalar_balance_is_the_unique_quotient_linear_degree_zero_antiderivative=1")
    print("  producer_must_find_a_non_quotient_linear_or_raw_source_mechanism=1")
    print("conclusion=reported_p25_laneB_square_axis_antiderivative_density_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
