#!/usr/bin/env python3
"""Cramer/Bezout certificate for the fixed-frequency R7 relation.

The cyclic-syzygy formulation says that the seven fixed-frequency relations
are one module membership statement over

    R7 = F_q[y] / (y^7 - 1).

For a certificate/proof surface we do not want to divide pointwise after seeing
the seven roots.  A better finite identity is Cramer's rule in R7:

    D(y) T(y) = N_2(y) P_2(y) + N_3(y) P_3(y)
              + N_5(y) P_5(y) + N_6(y) P_6(y),

where D is a selected 4x4 prefix minor and D is a unit in R7.  Unitness is a
Bezout condition for D against y^7 - 1, equivalently invertibility of cyclic
multiplication by D.

This toy checks the finite implication and controls:
* a valid Cramer/Bezout package gives the full vector relation;
* corrupting a non-pivot coordinate of the tail is caught by the full identity;
* if the selected denominator is a zero divisor, Cramer division is rejected
  even when some pointwise relations may still exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
import random

from l1_axis_injectivity_scan import rank_mod_q


Q = 29
N = 7
PREFIX_COUNT = 4
AMBIENT_DIM = 5
PIVOT_ROWS = tuple(range(PREFIX_COUNT))


Poly = list[int]
VectorSection = list[Poly]


@dataclass(frozen=True)
class CramerCase:
    label: str
    denominator_unit: bool
    denominator_inverse_exists: bool
    pivot_identity_holds: bool
    full_identity_holds: bool
    recovered_relation_holds: bool
    prefix_full_frequencies: int
    tail_inside_frequencies: int
    relation_certificate_valid: bool


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
    raise RuntimeError("no primitive root")


def roots_of_order_7() -> list[int]:
    root = primitive_root(Q)
    omega = pow(root, (Q - 1) // N, Q)
    return [pow(omega, index, Q) for index in range(N)]


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix if any(value % q for value in row)]
    width = len(rows[0]) if rows else 0
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


def invert_matrix(matrix: list[list[int]]) -> list[list[int]]:
    width = len(matrix)
    augmented = [
        [value % Q for value in row] + [1 if i == j else 0 for j in range(width)]
        for i, row in enumerate(matrix)
    ]
    reduced, pivots = rref(augmented, Q)
    if pivots[:width] != list(range(width)):
        raise ValueError("matrix is singular")
    return [row[width:] for row in reduced]


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(matrix[row][col] * vector[col] for col in range(len(vector))) % Q
        for row in range(len(matrix))
    ]


def interpolate(values: list[int], roots: list[int]) -> Poly:
    vandermonde = [[pow(root, power, Q) for power in range(N)] for root in roots]
    return mat_vec(invert_matrix(vandermonde), values)


def evaluate(poly: Poly, value: int) -> int:
    return sum(coeff * pow(value, power, Q) for power, coeff in enumerate(poly)) % Q


def cyclic_add(left: Poly, right: Poly) -> Poly:
    return [(a + b) % Q for a, b in zip(left, right)]


def cyclic_sub(left: Poly, right: Poly) -> Poly:
    return [(a - b) % Q for a, b in zip(left, right)]


def cyclic_mul(left: Poly, right: Poly) -> Poly:
    out = [0] * N
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[(i + j) % N] = (out[(i + j) % N] + a * b) % Q
    return out


def scalar_poly(value: int) -> Poly:
    return [value % Q] + [0] * (N - 1)


def sign_of_permutation(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inversions += int(perm[i] > perm[j])
    return -1 if inversions % 2 else 1


def det_poly(matrix: list[list[Poly]]) -> Poly:
    size = len(matrix)
    total = [0] * N
    for perm in permutations(range(size)):
        term = scalar_poly(sign_of_permutation(perm))
        for row, col in enumerate(perm):
            term = cyclic_mul(term, matrix[row][col])
        total = cyclic_add(total, term)
    return total


def invert_cyclic_unit(poly: Poly) -> Poly | None:
    columns = []
    for col in range(N):
        basis = [0] * N
        basis[col] = 1
        columns.append(cyclic_mul(poly, basis))
    matrix = [[columns[col][row] for col in range(N)] for row in range(N)]
    target = [1] + [0] * (N - 1)
    augmented = [row + [target[index]] for index, row in enumerate(matrix)]
    reduced, pivots = rref(augmented, Q)
    if pivots[:N] != list(range(N)):
        return None
    return [reduced[row][-1] % Q for row in range(N)]


def vector_section_from_values(values: list[list[int]], roots: list[int]) -> VectorSection:
    return [
        interpolate([values[root_index][coord] for root_index in range(N)], roots)
        for coord in range(AMBIENT_DIM)
    ]


def local_values(section: VectorSection, root: int) -> list[int]:
    return [evaluate(poly, root) for poly in section]


def vector_scale(poly: Poly, section: VectorSection) -> VectorSection:
    return [cyclic_mul(poly, coord_poly) for coord_poly in section]


def vector_add(left: VectorSection, right: VectorSection) -> VectorSection:
    return [cyclic_add(a, b) for a, b in zip(left, right)]


def vector_sub(left: VectorSection, right: VectorSection) -> VectorSection:
    return [cyclic_sub(a, b) for a, b in zip(left, right)]


def zero_section(section: VectorSection) -> bool:
    return all(all(value % Q == 0 for value in coord) for coord in section)


def prefix_matrix(prefix_sections: list[VectorSection]) -> list[list[Poly]]:
    return [
        [prefix_sections[col][row] for col in range(PREFIX_COUNT)]
        for row in PIVOT_ROWS
    ]


def cramer_numerators(
    prefix_sections: list[VectorSection],
    tail_section: VectorSection,
) -> tuple[Poly, list[Poly]]:
    matrix = prefix_matrix(prefix_sections)
    denominator = det_poly(matrix)
    numerators: list[Poly] = []
    for col in range(PREFIX_COUNT):
        replaced = [[entry[:] for entry in row] for row in matrix]
        for row_index, pivot_row in enumerate(PIVOT_ROWS):
            replaced[row_index][col] = tail_section[pivot_row]
        numerators.append(det_poly(replaced))
    return denominator, numerators


def cramer_identity_section(
    denominator: Poly,
    numerators: list[Poly],
    prefix_sections: list[VectorSection],
    tail_section: VectorSection,
) -> VectorSection:
    left = vector_scale(denominator, tail_section)
    right: VectorSection = [[0] * N for _ in range(AMBIENT_DIM)]
    for numerator, section in zip(numerators, prefix_sections):
        right = vector_add(right, vector_scale(numerator, section))
    return vector_sub(left, right)


def projected_identity_section(
    identity: VectorSection,
) -> VectorSection:
    return [identity[row] for row in PIVOT_ROWS]


def random_full_prefix_values(rng: random.Random) -> list[list[list[int]]]:
    out: list[list[list[int]]] = []
    for _root_index in range(N):
        while True:
            prefix = [
                [rng.randrange(Q) for _coord in range(AMBIENT_DIM)]
                for _col in range(PREFIX_COUNT)
            ]
            pivot_matrix = [
                [prefix[col][row] for col in range(PREFIX_COUNT)]
                for row in PIVOT_ROWS
            ]
            if rank_mod_q(pivot_matrix, Q) == PREFIX_COUNT:
                out.append(prefix)
                break
    return out


def combine_local(coeffs: list[int], prefix: list[list[int]]) -> list[int]:
    return [
        sum(coeffs[col] * prefix[col][coord] for col in range(PREFIX_COUNT)) % Q
        for coord in range(AMBIENT_DIM)
    ]


def solve_local(columns: list[list[int]], target: list[int]) -> bool:
    matrix = [
        [columns[col][row] for col in range(PREFIX_COUNT)] + [target[row]]
        for row in range(AMBIENT_DIM)
    ]
    reduced, _pivots = rref(matrix, Q)
    return not any(
        all(row[col] % Q == 0 for col in range(PREFIX_COUNT)) and row[-1] % Q
        for row in reduced
    )


def analyze_case(
    label: str,
    prefix_sections: list[VectorSection],
    tail_section: VectorSection,
    roots: list[int],
) -> CramerCase:
    denominator, numerators = cramer_numerators(prefix_sections, tail_section)
    denominator_inverse = invert_cyclic_unit(denominator)
    identity = cramer_identity_section(
        denominator,
        numerators,
        prefix_sections,
        tail_section,
    )
    full_identity = zero_section(identity)
    pivot_identity = zero_section(projected_identity_section(identity))
    recovered = False
    if denominator_inverse is not None and full_identity:
        recovered_section: VectorSection = [[0] * N for _ in range(AMBIENT_DIM)]
        for numerator, section in zip(numerators, prefix_sections):
            coeff = cyclic_mul(denominator_inverse, numerator)
            recovered_section = vector_add(recovered_section, vector_scale(coeff, section))
        recovered = zero_section(vector_sub(tail_section, recovered_section))

    prefix_full = 0
    tail_inside = 0
    for root in roots:
        prefix_values = [local_values(section, root) for section in prefix_sections]
        tail_value = local_values(tail_section, root)
        prefix_full += int(rank_mod_q(prefix_values, Q) == PREFIX_COUNT)
        tail_inside += int(solve_local(prefix_values, tail_value))

    denominator_unit = denominator_inverse is not None
    return CramerCase(
        label=label,
        denominator_unit=denominator_unit,
        denominator_inverse_exists=denominator_inverse is not None,
        pivot_identity_holds=pivot_identity,
        full_identity_holds=full_identity,
        recovered_relation_holds=recovered,
        prefix_full_frequencies=prefix_full,
        tail_inside_frequencies=tail_inside,
        relation_certificate_valid=denominator_unit and full_identity and recovered,
    )


def print_case(case: CramerCase) -> None:
    print(
        f"case={case.label} "
        f"denominator_unit={int(case.denominator_unit)} "
        f"denominator_inverse_exists={int(case.denominator_inverse_exists)} "
        f"pivot_identity_holds={int(case.pivot_identity_holds)} "
        f"full_identity_holds={int(case.full_identity_holds)} "
        f"recovered_relation_holds={int(case.recovered_relation_holds)} "
        f"prefix_full_frequencies={case.prefix_full_frequencies}/{N} "
        f"tail_inside_frequencies={case.tail_inside_frequencies}/{N} "
        f"relation_certificate_valid={int(case.relation_certificate_valid)}"
    )


def main() -> None:
    rng = random.Random(20260606)
    roots = roots_of_order_7()
    prefix_local = random_full_prefix_values(rng)
    coeff_local = [
        [rng.randrange(Q) for _col in range(PREFIX_COUNT)]
        for _root_index in range(N)
    ]
    tail_local = [
        combine_local(coeffs, prefix)
        for coeffs, prefix in zip(coeff_local, prefix_local)
    ]

    prefix_sections = [
        vector_section_from_values(
            [prefix_local[root_index][col] for root_index in range(N)],
            roots,
        )
        for col in range(PREFIX_COUNT)
    ]
    tail_section = vector_section_from_values(tail_local, roots)

    corrupted_tail = [coord[:] for coord in tail_section]
    corrupt_values = [local_values(corrupted_tail, root) for root in roots]
    corrupt_values[2][AMBIENT_DIM - 1] = (corrupt_values[2][AMBIENT_DIM - 1] + 1) % Q
    corrupted_tail = vector_section_from_values(corrupt_values, roots)

    zero_divisor_prefix_local = [
        [[value for value in column] for column in prefix]
        for prefix in prefix_local
    ]
    zero_divisor_prefix_local[3][1][0] = zero_divisor_prefix_local[3][0][0]
    zero_divisor_prefix_local[3][1][1] = zero_divisor_prefix_local[3][0][1]
    zero_divisor_prefix_local[3][1][2] = zero_divisor_prefix_local[3][0][2]
    zero_divisor_prefix_local[3][1][3] = zero_divisor_prefix_local[3][0][3]
    zero_divisor_sections = [
        vector_section_from_values(
            [zero_divisor_prefix_local[root_index][col] for root_index in range(N)],
            roots,
        )
        for col in range(PREFIX_COUNT)
    ]
    zero_divisor_tail = vector_section_from_values(
        [
            combine_local(coeffs, prefix)
            for coeffs, prefix in zip(coeff_local, zero_divisor_prefix_local)
        ],
        roots,
    )

    cases = [
        analyze_case("valid_cramer_bezout_certificate", prefix_sections, tail_section, roots),
        analyze_case("corrupted_nonpivot_tail_control", prefix_sections, corrupted_tail, roots),
        analyze_case(
            "zero_divisor_denominator_control",
            zero_divisor_sections,
            zero_divisor_tail,
            roots,
        ),
    ]

    print("Trace-GCD fixed-frequency Cramer/Bezout toy")
    print(f"q={Q}")
    print(f"ring=F_q[y]/(y^{N}-1)")
    print(f"prefix_count={PREFIX_COUNT}")
    print(f"ambient_dim={AMBIENT_DIM}")
    for case in cases:
        print_case(case)
    print("interpretation")
    print("  cramer_bezout_certificate_implies_relation_section=1")
    print("  denominator_unit_is_selected_prefix_plucker_gate=1")
    print("  full_vector_identity_detects_post_projection_corruption=1")
    print("  zero_divisor_denominator_rejected_before_division=1")
    print("  p24_fixed_frequency_certificate_surface=one_R7_unit_denominator_plus_four_numerators")
    print("conclusion=reported_trace_gcd_fixed_frequency_cramer_bezout_toy")

    valid, corrupted, zero_divisor = cases
    if not valid.relation_certificate_valid:
        raise SystemExit(1)
    if corrupted.full_identity_holds or corrupted.relation_certificate_valid:
        raise SystemExit(1)
    if zero_divisor.denominator_unit or zero_divisor.relation_certificate_valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
