#!/usr/bin/env python3
"""Sparse theta_{3,1} combination obstruction for the p25 bridge.

The single-edge scan rules out every individual finite-difference edge of the
canonical square-axis theta_{3,1} pullback.  This gate checks the next natural
escape: can the primitive bridge be repaired by a small translated combination
of the best theta edges?

Over the verifier field, no translated edge with support at most 12 works, no
pair of such edges works with arbitrary scalars, and no triple of the globally
minimal six-point +/-D edges works.  The translated D-edge family does contain
the bridge in its convolution span, but only through a dense coefficient vector:
after adding the full three-dimensional nullspace, at least 504 translated
edges remain nonzero.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import MODULUS
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_theta31_edge_direction_scan_gate import (
    edge_coefficients,
    quotient_theta_packet,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class SparseCombinationProfile:
    small_directions: tuple[int, ...]
    minimal_directions: tuple[int, ...]
    all_small_translated_edges: int
    minimal_translated_edges: int
    scalar_single_matches: int
    scalar_pair_support_candidates: int
    scalar_pair_matches: int
    minimal_triple_support_candidates: int
    minimal_triple_checked: int
    minimal_triple_matches: int
    minimal_triple_need_histogram: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class DenseSpanProfile:
    primitive_root: int
    omega: int
    edge_zero_frequencies: tuple[int, ...]
    bridge_zero_frequency_hits: tuple[int, ...]
    edge_nonzero_frequency_count: int
    canonical_solution_support: int
    canonical_solution_distinct_values: int
    row_class_distinct_values: tuple[int, int, int]
    row_class_max_multiplicities: tuple[int, int, int]
    min_support_after_nullspace: int


def translate(coefficients: dict[int, int], shift: int) -> dict[int, int]:
    return {
        (q_value + shift) % QUOTIENT_ORDER: value
        for q_value, value in coefficients.items()
    }


def solve_scalar_single(edge: dict[int, int], target: dict[int, int]) -> int | None:
    scalar: int | None = None
    for q_value in set(edge) | set(target):
        edge_value = edge.get(q_value, 0) % MODULUS
        target_value = target.get(q_value, 0) % MODULUS
        if edge_value == 0:
            if target_value:
                return None
            continue
        if target_value == 0:
            return None
        candidate = target_value * pow(edge_value, -1, MODULUS) % MODULUS
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def solve_scalar_pair(edge_a: dict[int, int], edge_b: dict[int, int], target: dict[int, int]) -> tuple[int, int] | None:
    q_values = sorted(set(edge_a) | set(edge_b) | set(target))
    for index, q1 in enumerate(q_values):
        a1 = edge_a.get(q1, 0) % MODULUS
        b1 = edge_b.get(q1, 0) % MODULUS
        t1 = target.get(q1, 0) % MODULUS
        for q2 in q_values[index + 1 :]:
            a2 = edge_a.get(q2, 0) % MODULUS
            b2 = edge_b.get(q2, 0) % MODULUS
            t2 = target.get(q2, 0) % MODULUS
            determinant = (a1 * b2 - a2 * b1) % MODULUS
            if not determinant:
                continue
            inverse = pow(determinant, -1, MODULUS)
            alpha = (t1 * b2 - t2 * b1) * inverse % MODULUS
            beta = (a1 * t2 - a2 * t1) * inverse % MODULUS
            if all(
                (alpha * edge_a.get(q_value, 0) + beta * edge_b.get(q_value, 0) - target.get(q_value, 0)) % MODULUS
                == 0
                for q_value in q_values
            ):
                return alpha, beta
            return None

    single_a = solve_scalar_single(edge_a, target)
    if single_a is not None:
        return single_a, 0
    single_b = solve_scalar_single(edge_b, target)
    if single_b is not None:
        return 0, single_b
    return None


def solve_scalar_triple(
    edge_a: dict[int, int],
    edge_b: dict[int, int],
    edge_c: dict[int, int],
    target: dict[int, int],
) -> tuple[int, int, int] | None:
    q_values = sorted(set(edge_a) | set(edge_b) | set(edge_c) | set(target))
    matrix = [
        [
            edge_a.get(q_value, 0) % MODULUS,
            edge_b.get(q_value, 0) % MODULUS,
            edge_c.get(q_value, 0) % MODULUS,
            target.get(q_value, 0) % MODULUS,
        ]
        for q_value in q_values
    ]
    row = 0
    pivots: list[int] = []
    for column in range(3):
        pivot = next((candidate for candidate in range(row, len(matrix)) if matrix[candidate][column] % MODULUS), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column] % MODULUS, -1, MODULUS)
        matrix[row] = [(value * inverse) % MODULUS for value in matrix[row]]
        for other_row in range(len(matrix)):
            if other_row == row or not matrix[other_row][column] % MODULUS:
                continue
            factor = matrix[other_row][column] % MODULUS
            matrix[other_row] = [
                (matrix[other_row][entry] - factor * matrix[row][entry]) % MODULUS
                for entry in range(4)
            ]
        pivots.append(column)
        row += 1

    if any(
        all(equation[column] % MODULUS == 0 for column in range(3)) and equation[3] % MODULUS
        for equation in matrix
    ):
        return None

    solution = [0, 0, 0]
    for row_index, column in enumerate(pivots):
        solution[column] = matrix[row_index][3] % MODULUS
    return tuple(solution)  # type: ignore[return-value]


def translated_edges(directions: tuple[int, ...], packet: list[int]) -> list[tuple[int, int, dict[int, int], set[int]]]:
    edges: list[tuple[int, int, dict[int, int], set[int]]] = []
    for direction in directions:
        base = edge_coefficients(packet, direction)
        for shift in range(QUOTIENT_ORDER):
            coefficients = translate(base, shift)
            edges.append((direction, shift, coefficients, set(coefficients)))
    return edges


def sparse_combination_profile() -> SparseCombinationProfile:
    packet = quotient_theta_packet()
    target = bridge_coefficients()
    target_support = set(target)
    small_directions = tuple(
        direction
        for direction in range(1, QUOTIENT_ORDER)
        if len(edge_coefficients(packet, direction)) <= 12
    )
    minimal_directions = tuple(
        direction
        for direction in small_directions
        if len(edge_coefficients(packet, direction)) == 6
    )

    small_edges = translated_edges(small_directions, packet)
    minimal_edges = [edge for edge in small_edges if edge[0] in minimal_directions]

    single_matches = sum(
        1
        for _, _, edge, _ in small_edges
        if solve_scalar_single(edge, target) is not None
    )

    pair_support_candidates = 0
    pair_matches = 0
    for index, (_, _, edge_a, support_a) in enumerate(small_edges):
        for _, _, edge_b, support_b in small_edges[index:]:
            if (support_a ^ support_b) - target_support:
                continue
            pair_support_candidates += 1
            solution = solve_scalar_pair(edge_a, edge_b, target)
            if solution is not None and all(value % MODULUS for value in solution):
                pair_matches += 1

    inverted_support: defaultdict[int, set[int]] = defaultdict(set)
    for index, (_, _, _, support) in enumerate(minimal_edges):
        for q_value in support:
            inverted_support[q_value].add(index)

    triple_need_histogram: Counter[int] = Counter()
    triple_support_candidates = 0
    triple_checked = 0
    triple_matches = 0
    for index_a, (_, _, edge_a, support_a) in enumerate(minimal_edges):
        for index_b in range(index_a, len(minimal_edges)):
            _, _, edge_b, support_b = minimal_edges[index_b]
            outside_counts: dict[int, int] = {}
            for q_value in support_a - target_support:
                outside_counts[q_value] = outside_counts.get(q_value, 0) + 1
            for q_value in support_b - target_support:
                outside_counts[q_value] = outside_counts.get(q_value, 0) + 1
            needed = [q_value for q_value, count in outside_counts.items() if count == 1]
            triple_need_histogram[len(needed)] += 1
            if len(needed) > 6:
                continue
            if needed:
                candidates = set(inverted_support[needed[0]])
                for q_value in needed[1:]:
                    candidates &= inverted_support[q_value]
                    if not candidates:
                        break
            else:
                candidates = set(range(len(minimal_edges)))
            for index_c in sorted(candidate for candidate in candidates if candidate >= index_b):
                _, _, edge_c, _ = minimal_edges[index_c]
                triple_support_candidates += 1
                solution = solve_scalar_triple(edge_a, edge_b, edge_c, target)
                triple_checked += 1
                if solution is not None and all(value % MODULUS for value in solution):
                    triple_matches += 1

    return SparseCombinationProfile(
        small_directions=small_directions,
        minimal_directions=minimal_directions,
        all_small_translated_edges=len(small_edges),
        minimal_translated_edges=len(minimal_edges),
        scalar_single_matches=single_matches,
        scalar_pair_support_candidates=pair_support_candidates,
        scalar_pair_matches=pair_matches,
        minimal_triple_support_candidates=triple_support_candidates,
        minimal_triple_checked=triple_checked,
        minimal_triple_matches=triple_matches,
        minimal_triple_need_histogram=tuple(sorted(triple_need_histogram.items())),
    )


def primitive_root() -> int:
    factors = (2, 3, 5, 13, 169)
    for candidate in range(2, MODULUS):
        if all(pow(candidate, (MODULUS - 1) // factor, MODULUS) != 1 for factor in factors):
            return candidate
    raise AssertionError("no primitive root found")


def dft(vector: list[int], omega: int) -> list[int]:
    output: list[int] = []
    for frequency in range(QUOTIENT_ORDER):
        omega_frequency = pow(omega, frequency, MODULUS)
        power = 1
        total = 0
        for value in vector:
            total = (total + value * power) % MODULUS
            power = power * omega_frequency % MODULUS
        output.append(total)
    return output


def idft(values: list[int], omega: int) -> list[int]:
    inverse_order = pow(QUOTIENT_ORDER, -1, MODULUS)
    omega_inverse = pow(omega, -1, MODULUS)
    output: list[int] = []
    for index in range(QUOTIENT_ORDER):
        omega_index = pow(omega_inverse, index, MODULUS)
        power = 1
        total = 0
        for value in values:
            total = (total + value * power) % MODULUS
            power = power * omega_index % MODULUS
        output.append(total * inverse_order % MODULUS)
    return output


def dense_span_profile() -> DenseSpanProfile:
    packet = quotient_theta_packet()
    edge = edge_coefficients(packet, S_STEP)
    target = bridge_coefficients()
    root = primitive_root()
    omega = pow(root, (MODULUS - 1) // QUOTIENT_ORDER, MODULUS)
    edge_vector = [edge.get(index, 0) % MODULUS for index in range(QUOTIENT_ORDER)]
    target_vector = [target.get(index, 0) % MODULUS for index in range(QUOTIENT_ORDER)]
    edge_hat = dft(edge_vector, omega)
    target_hat = dft(target_vector, omega)
    zero_frequencies = tuple(index for index, value in enumerate(edge_hat) if value == 0)
    bridge_zero_hits = tuple(index for index in zero_frequencies if target_hat[index] == 0)
    coefficient_hat = [
        target_hat[index] * pow(edge_hat[index], -1, MODULUS) % MODULUS
        if edge_hat[index]
        else 0
        for index in range(QUOTIENT_ORDER)
    ]
    coefficients = idft(coefficient_hat, omega)
    row_class_counters = [
        Counter(coefficients[index] for index in range(residue, QUOTIENT_ORDER, 3))
        for residue in range(3)
    ]
    return DenseSpanProfile(
        primitive_root=root,
        omega=omega,
        edge_zero_frequencies=zero_frequencies,
        bridge_zero_frequency_hits=bridge_zero_hits,
        edge_nonzero_frequency_count=QUOTIENT_ORDER - len(zero_frequencies),
        canonical_solution_support=sum(1 for value in coefficients if value % MODULUS),
        canonical_solution_distinct_values=len(set(coefficients)),
        row_class_distinct_values=tuple(len(counter) for counter in row_class_counters),  # type: ignore[arg-type]
        row_class_max_multiplicities=tuple(max(counter.values()) for counter in row_class_counters),  # type: ignore[arg-type]
        min_support_after_nullspace=sum(
            (QUOTIENT_ORDER // 3) - max(counter.values())
            for counter in row_class_counters
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge theta31 sparse-combination obstruction gate")
    print(f"quotient_order={QUOTIENT_ORDER} modulus={MODULUS} D={S_STEP}")
    sparse_profile = sparse_combination_profile()
    dense_profile = dense_span_profile()
    expected_sparse = SparseCombinationProfile(
        small_directions=(163, 172, 335, 344),
        minimal_directions=(172, 335),
        all_small_translated_edges=2028,
        minimal_translated_edges=1014,
        scalar_single_matches=0,
        scalar_pair_support_candidates=3042,
        scalar_pair_matches=0,
        minimal_triple_support_candidates=643383,
        minimal_triple_checked=643383,
        minimal_triple_matches=0,
        minimal_triple_need_histogram=(
            (0, 1521),
            (4, 16),
            (5, 256),
            (6, 3816),
            (7, 128),
            (8, 2012),
            (9, 1392),
            (10, 14628),
            (11, 66048),
            (12, 424788),
        ),
    )
    expected_dense = DenseSpanProfile(
        primitive_root=6,
        omega=103466,
        edge_zero_frequencies=(0, 169, 338),
        bridge_zero_frequency_hits=(0, 169, 338),
        edge_nonzero_frequency_count=504,
        canonical_solution_support=507,
        canonical_solution_distinct_values=507,
        row_class_distinct_values=(169, 169, 169),
        row_class_max_multiplicities=(1, 1, 1),
        min_support_after_nullspace=504,
    )
    row_ok = (
        sparse_profile == expected_sparse
        and dense_profile == expected_dense
        and sparse_profile.minimal_directions == (S_STEP, (-S_STEP) % QUOTIENT_ORDER)
    )

    print(f"bridge_coefficients={sorted(bridge_coefficients().items())}")
    print(f"sparse_combination_profile={sparse_profile}")
    print(f"dense_span_profile={dense_profile}")
    print("combination_laws")
    print("  no support <= 12 translated theta edge scales to the bridge")
    print("  no two support <= 12 translated theta edges span the bridge, even with arbitrary field scalars")
    print("  no three globally minimal translated +/-D theta edges span the bridge")
    print("  translated D edges span the bridge only through a coefficient vector with at least 504 nonzero translates")
    print("interpretation")
    print("  canonical_theta31_sparse_edge_corrections_do_not_produce_the_bridge=1")
    print("  theta31_D_edge_deconvolution_is_dense_after_all_nullspace_repairs=1")
    print("  producer_must_modify_the_theta_packet_or_add_new_arithmetic_structure=1")
    print("  small_translated_edge_sums_should_not_be_treated_as_a_remaining_escape=1")
    print(f"square_axis_bridge_theta31_sparse_combination_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_theta31_sparse_combination_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
