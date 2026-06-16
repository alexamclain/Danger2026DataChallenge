#!/usr/bin/env python3
"""Cyclic 7-section package for the fixed-frequency no-defect relations.

For p24 the fixed frequencies are the multiples of 5 in Z/35Z, i.e. a
7-cycle.  Since

    10^24 + 7 = 1 mod 7,

the seven fixed frequencies are base-rational on the 7-part.  Thus seven
relations

    V_{a,1} in span(V_{a,2}, V_{a,3}, V_{a,5}, V_{a,6})

are equivalent, as finite algebra, to one vector-valued syzygy over

    R = F_p[y] / (y^7 - 1).

This toy records that equivalence and its limits: a cyclic syzygy packages the
seven relations, but interpolation alone is still post-fit unless the syzygy
is constructed intrinsically from the CM/Lang object.
"""

from __future__ import annotations

from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q


Q = 29
N = 7
AMBIENT_DIM = 5
PREFIX_COUNT = 4


@dataclass(frozen=True)
class CyclicSyzygyCase:
    label: str
    prefix_full_count: int
    tail_inside_count: int
    pointwise_relations: bool
    cyclic_syzygy_exists: bool
    fixed_ordinary_count: int
    fixed_ordinary_all: bool
    postfit_coefficients_interpolate: bool
    failed_relation_count: int


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root found")


def roots_of_order_7() -> list[int]:
    root = primitive_root(Q)
    omega = pow(root, (Q - 1) // N, Q)
    if pow(omega, N, Q) != 1 or any(pow(omega, k, Q) == 1 for k in range(1, N)):
        raise AssertionError("omega does not have order 7")
    return [pow(omega, i, Q) for i in range(N)]


def e(index: int) -> list[int]:
    row = [0] * AMBIENT_DIM
    row[index] = 1
    return row


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix if any(value % q for value in row)]
    if not rows:
        return [], []
    width = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(width):
        pivot = None
        for row in range(pivot_row, len(rows)):
            if rows[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % q, -1, q)
        rows[pivot_row] = [(value * inv) % q for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            scale = rows[row][col] % q
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[pivot_row])
                ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def solve_columns(columns: list[list[int]], target: list[int]) -> list[int] | None:
    """Solve sum_j coeff_j columns[j] = target with free variables set to zero."""

    rows = [
        [columns[col][coord] % Q for col in range(len(columns))] + [target[coord] % Q]
        for coord in range(AMBIENT_DIM)
    ]
    reduced, pivots = rref(rows, Q)
    coeff_count = len(columns)
    for row in reduced:
        if all(row[col] % Q == 0 for col in range(coeff_count)) and row[-1] % Q:
            return None
    solution = [0] * coeff_count
    for row_index, pivot_col in enumerate(pivots):
        if pivot_col < coeff_count:
            solution[pivot_col] = reduced[row_index][-1] % Q
    return solution


def invert_matrix(matrix: list[list[int]]) -> list[list[int]]:
    width = len(matrix)
    augmented = [
        [value % Q for value in row] + [1 if i == j else 0 for j in range(width)]
        for i, row in enumerate(matrix)
    ]
    reduced, pivots = rref(augmented, Q)
    if pivots[:width] != list(range(width)):
        raise AssertionError("matrix not invertible")
    return [row[width:] for row in reduced]


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(matrix[row][col] * vector[col] for col in range(len(vector))) % Q
        for row in range(len(matrix))
    ]


def interpolate(values: list[int], roots: list[int]) -> list[int]:
    vandermonde = [[pow(root, power, Q) for power in range(N)] for root in roots]
    return mat_vec(invert_matrix(vandermonde), values)


def evaluate(poly: list[int], value: int) -> int:
    return sum(coeff * pow(value, power, Q) for power, coeff in enumerate(poly)) % Q


def vector_section_from_values(values: list[list[int]], roots: list[int]) -> list[list[int]]:
    return [
        interpolate([values[root_index][coord] for root_index in range(N)], roots)
        for coord in range(AMBIENT_DIM)
    ]


def cyclic_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * N
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[(i + j) % N] = (out[(i + j) % N] + a * b) % Q
    return out


def cyclic_vector_combination(
    coeff_sections: list[list[int]],
    prefix_sections: list[list[list[int]]],
) -> list[list[int]]:
    out = [[0] * N for _coord in range(AMBIENT_DIM)]
    for coeffs, section in zip(coeff_sections, prefix_sections):
        for coord in range(AMBIENT_DIM):
            product = cyclic_mul(coeffs, section[coord])
            out[coord] = [
                (out[coord][power] + product[power]) % Q
                for power in range(N)
            ]
    return out


def section_equal(left: list[list[int]], right: list[list[int]]) -> bool:
    return all(
        (left[coord][power] - right[coord][power]) % Q == 0
        for coord in range(AMBIENT_DIM)
        for power in range(N)
    )


def add_scaled(terms: list[tuple[int, list[int]]]) -> list[int]:
    return [
        sum(scale * row[coord] for scale, row in terms) % Q
        for coord in range(AMBIENT_DIM)
    ]


def analyze_case(
    label: str,
    prefix_values: list[list[list[int]]],
    tail_values: list[list[int]],
) -> CyclicSyzygyCase:
    roots = roots_of_order_7()
    local_solutions: list[list[int] | None] = []
    prefix_full_count = 0
    tail_inside_count = 0
    fixed_ordinary_count = 0
    for root_index in range(N):
        columns = [prefix_values[j][root_index] for j in range(PREFIX_COUNT)]
        target = tail_values[root_index]
        prefix_full = rank_mod_q(columns, Q) == PREFIX_COUNT
        solution = solve_columns(columns, target)
        tail_inside = solution is not None
        if prefix_full:
            prefix_full_count += 1
        if tail_inside:
            tail_inside_count += 1
        if prefix_full and tail_inside:
            fixed_ordinary_count += 1
        local_solutions.append(solution)

    prefix_sections = [
        vector_section_from_values(prefix_values[j], roots)
        for j in range(PREFIX_COUNT)
    ]
    tail_section = vector_section_from_values(tail_values, roots)
    cyclic_syzygy_exists = False
    postfit_coefficients_interpolate = False
    if all(solution is not None for solution in local_solutions):
        coefficient_values = [
            [local_solutions[root_index][j] for root_index in range(N)]  # type: ignore[index]
            for j in range(PREFIX_COUNT)
        ]
        coeff_sections = [interpolate(values, roots) for values in coefficient_values]
        reconstructed = cyclic_vector_combination(coeff_sections, prefix_sections)
        cyclic_syzygy_exists = section_equal(reconstructed, tail_section)
        postfit_coefficients_interpolate = cyclic_syzygy_exists and all(
            evaluate(coeff_sections[j], roots[root_index])
            == coefficient_values[j][root_index]
            for j in range(PREFIX_COUNT)
            for root_index in range(N)
        )

    return CyclicSyzygyCase(
        label=label,
        prefix_full_count=prefix_full_count,
        tail_inside_count=tail_inside_count,
        pointwise_relations=tail_inside_count == N,
        cyclic_syzygy_exists=cyclic_syzygy_exists,
        fixed_ordinary_count=fixed_ordinary_count,
        fixed_ordinary_all=fixed_ordinary_count == N,
        postfit_coefficients_interpolate=postfit_coefficients_interpolate,
        failed_relation_count=N - tail_inside_count,
    )


def print_case(case: CyclicSyzygyCase) -> None:
    print(
        f"case={case.label} prefix_full_count={case.prefix_full_count}/7 "
        f"tail_inside_count={case.tail_inside_count}/7 "
        f"pointwise_relations={int(case.pointwise_relations)} "
        f"cyclic_syzygy_exists={int(case.cyclic_syzygy_exists)} "
        f"fixed_ordinary_count={case.fixed_ordinary_count}/7 "
        f"fixed_ordinary_all={int(case.fixed_ordinary_all)} "
        f"postfit_coefficients_interpolate={int(case.postfit_coefficients_interpolate)} "
        f"failed_relation_count={case.failed_relation_count}"
    )


def main() -> None:
    basis = [e(i) for i in range(AMBIENT_DIM)]
    constant_prefix = [[basis[j][:] for _root in range(N)] for j in range(PREFIX_COUNT)]
    good_tail = [
        add_scaled(
            [
                (1 + root_index, basis[0]),
                (2 + 3 * root_index, basis[1]),
                (4 + root_index * root_index, basis[2]),
                (7 + 2 * root_index, basis[3]),
            ]
        )
        for root_index in range(N)
    ]

    outside_tail = [row[:] for row in good_tail]
    outside_tail[3] = basis[4][:]

    prefix_defect = [[value[:] for value in section] for section in constant_prefix]
    prefix_defect[3][2] = prefix_defect[2][2][:]
    prefix_defect_tail = [row[:] for row in good_tail]
    prefix_defect_tail[2] = add_scaled(
        [(3, basis[0]), (5, basis[1]), (7, basis[2])]
    )

    rows = [
        analyze_case("cyclic_syzygy_good", constant_prefix, good_tail),
        analyze_case("one_fixed_tail_outside_control", constant_prefix, outside_tail),
        analyze_case("prefix_defect_tail_inside_control", prefix_defect, prefix_defect_tail),
    ]

    print("Trace-GCD fixed-frequency cyclic 7-section syzygy toy")
    print(f"q={Q}")
    print(f"n={N}")
    print(f"p24_p_mod_7={(10**24 + 7) % 7}")
    print(f"p24_p_equals_1_mod_7={int((10**24 + 7) % 7 == 1)}")
    print(f"ambient_dim={AMBIENT_DIM}")
    print(f"prefix_count={PREFIX_COUNT}")
    for row in rows:
        print_case(row)
    print("interpretation")
    print("  cyclic_7_syzygy_packages_seven_fixed_relations=1")
    print("  pointwise_relations_interpolate_because_p24_p_is_1_mod_7=1")
    print("  single_failed_fixed_relation_blocks_cyclic_syzygy=1")
    print("  prefix_plucker_full_rank_remains_separate_from_cyclic_syzygy=1")
    print("  p24_needs_intrinsic_cyclic_syzygy_not_postfit_coefficients=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_cyclic_syzygy_toy")

    good, outside, prefix_bad = rows
    if not good.cyclic_syzygy_exists or not good.fixed_ordinary_all:
        raise SystemExit(1)
    if outside.cyclic_syzygy_exists or outside.failed_relation_count != 1:
        raise SystemExit(1)
    if not prefix_bad.cyclic_syzygy_exists or prefix_bad.fixed_ordinary_all:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
