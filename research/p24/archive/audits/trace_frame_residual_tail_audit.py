#!/usr/bin/env python3
"""Audit the residual tail Schubert coordinate in trace-frame toy rows.

The p24 leading trace-frame determinant factors conceptually as:

    first full top block(s)  +  residual tail in the next block.

For p24, after the first two C-blocks the expected kernel has dimension

    368 - 2*179 = 10,

and the leading Plucker coordinate asks the first 10 normal-basis coordinates
of the third block to separate that residual kernel.  This script computes the
same residual object in small CM tensor rows.  It is deliberately local: the
goal is to identify the right proof surface, not to scan for large data.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    rank_in_factor,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from tensor_factor_dual_basis_window_audit import (
    discriminants,
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    solve_square,
    top_window_coords,
)
from tensor_factor_moore_audit import b_add, b_is_zero, b_mul, b_pow, b_sub
from tensor_factor_subfield_trace_audit import divisors, element_rank
from trace_frame_plucker_pivot_audit import frequencies_for_target, pivot_columns_over_extension


Matrix = list[list[FpE]]


@dataclass(frozen=True)
class ResidualTailRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    origin_shift: int
    target: str
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    subdegree: int
    relative_degree: int
    raw_rank: int
    top_count: int
    prefix_blocks: int
    prefix_rank: int
    residual_dim: int
    tail_rank: int
    leading_tail_rank: int
    tail_annihilator_q_degree: int
    tail_annihilator_q_support: int
    tail_annihilator_image_rank: int
    head_projection_q_support: int
    tail_pivots: tuple[int, ...]
    trace_dual_mismatches: int
    shift_intersection_min: int | None
    shift_intersection_max: int | None
    frobenius_invariant_shifts: tuple[int, ...]


def transpose(matrix: Matrix) -> Matrix:
    if not matrix:
        return []
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]


def right_nullspace(matrix: Matrix, field: ExtensionField) -> Matrix:
    """Return a basis of right-kernel vectors for matrix * x = 0."""

    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    mat = [row[:] for row in matrix]
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = field.inv(mat[rank][col])
        mat[rank] = [field.mul(value, inv) for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break

    pivot_set = set(pivots)
    free_cols = [col for col in range(cols) if col not in pivot_set]
    basis: Matrix = []
    for free_col in free_cols:
        vec = [field.zero for _ in range(cols)]
        vec[free_col] = field.one
        for row, pivot_col in enumerate(pivots):
            vec[pivot_col] = field.neg(mat[row][free_col])
        basis.append(vec)
    return basis


def linear_combo(coeffs: list[FpE], rows: Matrix, field: ExtensionField) -> list[FpE]:
    if not rows:
        return []
    out = [field.zero for _ in range(len(rows[0]))]
    for coeff, row in zip(coeffs, rows):
        if coeff == field.zero:
            continue
        out = [
            field.add(current, field.mul(coeff, value))
            for current, value in zip(out, row)
        ]
    return out


def poly_scalar_mul(
    scalar: FpE,
    value,
    factor,
    field: ExtensionField,
):
    if scalar == field.zero:
        return [field.zero]
    return [field.mul(scalar, coeff) for coeff in value]


def c_from_coords(
    coords: list[FpE],
    subfield_basis,
    factor,
    field: ExtensionField,
):
    out = [field.zero]
    for coeff, basis_value in zip(coords, subfield_basis):
        if coeff == field.zero:
            continue
        out = b_add(
            out,
            poly_scalar_mul(coeff, basis_value, factor, field),
            factor,
            field,
        )
    return out


def c_trace_to_E(
    value,
    subdegree: int,
    factor,
    field: ExtensionField,
) -> FpE:
    q_power = field.q ** field.degree
    total = [field.zero]
    current = value
    for _ in range(subdegree):
        total = b_add(total, current, factor, field)
        current = b_pow(current, q_power, factor, field)
    reduced = total + [field.zero]
    if any(coeff != field.zero for coeff in reduced[1:]):
        raise RuntimeError("subfield trace did not land in E")
    return reduced[0]


def trace_dual_basis_coords(
    subfield_basis,
    subdegree: int,
    factor,
    field: ExtensionField,
) -> list[list[FpE]]:
    gram_columns: Matrix = []
    for right in subfield_basis:
        column: list[FpE] = []
        for left in subfield_basis:
            column.append(
                c_trace_to_E(
                    b_mul(left, right, factor, field),
                    subdegree,
                    factor,
                    field,
                )
            )
        gram_columns.append(column)
    out: list[list[FpE]] = []
    for index in range(subdegree):
        rhs = [
            field.one if row == index else field.zero
            for row in range(subdegree)
        ]
        out.append(solve_square(gram_columns, rhs, field))
    return out


def trace_dual_coordinate_mismatches(
    rows: Matrix,
    subfield_basis,
    subdegree: int,
    factor,
    field: ExtensionField,
) -> int:
    if not rows:
        return 0
    dual_coords = trace_dual_basis_coords(subfield_basis, subdegree, factor, field)
    dual_elements = [
        c_from_coords(coords, subfield_basis, factor, field)
        for coords in dual_coords
    ]
    mismatches = 0
    for row in rows:
        value = c_from_coords(row, subfield_basis, factor, field)
        recovered = [
            c_trace_to_E(
                b_mul(value, dual, factor, field),
                subdegree,
                factor,
                field,
            )
            for dual in dual_elements
        ]
        if recovered != row:
            mismatches += 1
    return mismatches


def qpoly_support_count_c(coeffs, field: ExtensionField) -> int:
    return sum(1 for coeff in coeffs if not b_is_zero(coeff, field))


def projection_q_support(
    head_dim: int,
    subfield_basis,
    subdegree: int,
    factor,
    field: ExtensionField,
) -> int:
    if head_dim <= 0:
        return 0
    q_power = field.q ** field.degree
    dual_coords = trace_dual_basis_coords(subfield_basis, subdegree, factor, field)
    dual_elements = [
        c_from_coords(coords, subfield_basis, factor, field)
        for coords in dual_coords
    ]
    coeffs = []
    for frob_index in range(subdegree):
        coeff = [field.zero]
        exponent = q_power**frob_index
        for basis_value, dual_value in zip(
            subfield_basis[:head_dim],
            dual_elements[:head_dim],
        ):
            coeff = b_add(
                coeff,
                b_mul(
                    basis_value,
                    b_pow(dual_value, exponent, factor, field),
                    factor,
                    field,
                ),
                factor,
                field,
            )
        coeffs.append(coeff)
    return qpoly_support_count_c(coeffs, field)


def qpoly_eval_c(
    coeffs,
    x,
    factor,
    field: ExtensionField,
):
    q_power = field.q ** field.degree
    total = [field.zero]
    current_power = 1
    for coeff in coeffs:
        term = b_mul(coeff, b_pow(x, current_power, factor, field), factor, field)
        total = b_add(total, term, factor, field)
        current_power *= q_power
    return total


def qpoly_annihilator_c(
    elements,
    factor,
    field: ExtensionField,
):
    q_power = field.q ** field.degree
    coeffs = [[field.one]]
    for value in elements:
        y = qpoly_eval_c(coeffs, value, factor, field)
        if b_is_zero(y, field):
            continue
        scale = b_pow(y, q_power - 1, factor, field)
        new_coeffs = [[field.zero] for _ in range(len(coeffs) + 1)]
        for i, coeff in enumerate(coeffs):
            new_coeffs[i] = b_sub(
                new_coeffs[i],
                b_mul(scale, coeff, factor, field),
                factor,
                field,
            )
            new_coeffs[i + 1] = b_add(
                new_coeffs[i + 1],
                b_pow(coeff, q_power, factor, field),
                factor,
                field,
            )
        coeffs = new_coeffs
    return coeffs


def qpoly_degree_c(coeffs, field: ExtensionField) -> int:
    for index in range(len(coeffs) - 1, -1, -1):
        if not b_is_zero(coeffs[index], field):
            return index
    return -1


def tail_annihilator_image_profile(
    residual_rows: Matrix,
    residual_dim: int,
    subfield_basis,
    factor,
    field: ExtensionField,
) -> tuple[int, int, int, int]:
    tail_basis = subfield_basis[residual_dim:]
    ann_tail = qpoly_annihilator_c(tail_basis, factor, field)
    residual_elements = [
        c_from_coords(row, subfield_basis, factor, field)
        for row in residual_rows
    ]
    images = [
        qpoly_eval_c(ann_tail, value, factor, field)
        for value in residual_elements
    ]
    return (
        qpoly_degree_c(ann_tail, field),
        qpoly_support_count_c(ann_tail, field),
        element_rank(images, factor, field),
        projection_q_support(
            residual_dim,
            subfield_basis,
            len(subfield_basis),
            factor,
            field,
        ),
    )


def prefix_relation_basis(
    prefix_matrix: Matrix,
    raw_rank: int,
    field: ExtensionField,
) -> Matrix:
    if not prefix_matrix or not prefix_matrix[0]:
        return [
            [
                field.one if i == j else field.zero
                for i in range(raw_rank)
            ]
            for j in range(raw_rank)
        ]
    return right_nullspace(transpose(prefix_matrix), field)


def cyclic_shift(row: list[FpE], amount: int) -> list[FpE]:
    if not row:
        return []
    shift = amount % len(row)
    return row[shift:] + row[:shift]


def shift_intersection_profile(
    rows: Matrix,
    subdegree: int,
    field: ExtensionField,
) -> tuple[int | None, int | None, tuple[int, ...]]:
    rank = rank_over_extension(rows, field)
    if rank == 0 or subdegree <= 1:
        return None, None, ()
    intersections: list[int] = []
    invariant_shifts: list[int] = []
    for shift in range(1, subdegree):
        shifted = [cyclic_shift(row, shift) for row in rows]
        combined_rank = rank_over_extension(rows + shifted, field)
        intersection = 2 * rank - combined_rank
        intersections.append(intersection)
        if combined_rank == rank:
            invariant_shifts.append(shift)
    return min(intersections), max(intersections), tuple(invariant_shifts)


def residual_tail_profile(
    top_matrix: Matrix,
    subdegree: int,
    top_count: int,
    subfield_basis,
    factor,
    field: ExtensionField,
) -> tuple[
    int,
    int,
    int,
    int,
    int,
    int,
    int,
    int,
    int,
    tuple[int, ...],
    int,
    int | None,
    int | None,
    tuple[int, ...],
]:
    raw_rank = len(top_matrix)
    prefix_blocks = max(0, top_count - 1)
    prefix_cols = prefix_blocks * subdegree
    prefix_matrix = [row[:prefix_cols] for row in top_matrix]
    prefix_rank = rank_over_extension(prefix_matrix, field)
    residual_dim = raw_rank - prefix_rank
    if residual_dim <= 0:
        return prefix_blocks, prefix_rank, residual_dim, 0, 0, 0, 0, 0, 0, (), 0, None, None, ()

    relations = prefix_relation_basis(prefix_matrix, raw_rank, field)
    tail_start = prefix_cols
    tail_end = tail_start + subdegree
    tail_rows = [row[tail_start:tail_end] for row in top_matrix]
    residual_rows = [
        linear_combo(relation, tail_rows, field)
        for relation in relations
    ]
    residual_rows = [row for row in residual_rows if any(value != field.zero for value in row)]
    tail_rank = rank_over_extension(residual_rows, field)
    leading_tail = [row[:residual_dim] for row in residual_rows]
    leading_tail_rank = rank_over_extension(leading_tail, field)
    (
        tail_annihilator_q_degree,
        tail_annihilator_q_support,
        tail_annihilator_image_rank,
        head_projection_q_support,
    ) = (
        tail_annihilator_image_profile(
            residual_rows,
            residual_dim,
            subfield_basis,
            factor,
            field,
        )
    )
    tail_pivots = tuple(pivot_columns_over_extension(residual_rows, field))
    trace_dual_mismatches = trace_dual_coordinate_mismatches(
        residual_rows,
        subfield_basis,
        subdegree,
        factor,
        field,
    )
    shift_min, shift_max, invariant_shifts = shift_intersection_profile(
        residual_rows,
        subdegree,
        field,
    )
    return (
        prefix_blocks,
        prefix_rank,
        residual_dim,
        tail_rank,
        leading_tail_rank,
        tail_annihilator_q_degree,
        tail_annihilator_q_support,
        tail_annihilator_image_rank,
        head_projection_q_support,
        tail_pivots,
        trace_dual_mismatches,
        shift_min,
        shift_max,
        invariant_shifts,
    )


def audit_target(
    D: int,
    q: int,
    ell: int,
    h: int,
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    residue_vectors: list[list[int]],
    target: str,
    seed: int,
    max_top_count: int,
) -> list[ResidualTailRow]:
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    rows = character_rows(
        residue_vectors,
        frequencies_for_target(m, target),
        zeta,
        field,
    )

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    raw_rank = rank_in_factor(rows, selected_factor, field)
    if raw_rank == 0 or len(elements) != raw_rank:
        return []

    out: list[ResidualTailRow] = []
    for subdegree in divisors(tensor_factor_degree):
        if subdegree in (1, tensor_factor_degree):
            continue
        relative_degree = tensor_factor_degree // subdegree
        top_count = (raw_rank + subdegree - 1) // subdegree
        if top_count > relative_degree or top_count > max_top_count:
            continue
        subfield_basis = normal_subfield_basis(
            subdegree,
            tensor_factor_degree,
            selected_factor,
            field,
        )
        basis_columns = relative_basis_columns(
            subfield_basis,
            relative_degree,
            selected_factor,
            field,
        )
        gprime_theta = relative_gprime_theta(
            subdegree,
            tensor_factor_degree,
            selected_factor,
            field,
        )
        top_matrix = [
            top_window_coords(
                value,
                top_count,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                selected_factor,
                field,
            )
            for value in elements
        ]
        (
            prefix_blocks,
            prefix_rank,
            residual_dim,
            tail_rank,
            leading_tail_rank,
            tail_annihilator_q_degree,
            tail_annihilator_q_support,
            tail_annihilator_image_rank,
            head_projection_q_support,
            tail_pivots,
            trace_dual_mismatches,
            shift_min,
            shift_max,
            invariant_shifts,
        ) = residual_tail_profile(
            top_matrix,
            subdegree,
            top_count,
            subfield_basis,
            selected_factor,
            field,
        )
        out.append(
            ResidualTailRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                m=m,
                n=h // m,
                origin_shift=origin_shift,
                target=target,
                factor_degree=factor.degree(),
                extension_degree=extension_degree,
                tensor_factor_degree=tensor_factor_degree,
                subdegree=subdegree,
                relative_degree=relative_degree,
                raw_rank=raw_rank,
                top_count=top_count,
                prefix_blocks=prefix_blocks,
                prefix_rank=prefix_rank,
                residual_dim=residual_dim,
                tail_rank=tail_rank,
                leading_tail_rank=leading_tail_rank,
                tail_annihilator_q_degree=tail_annihilator_q_degree,
                tail_annihilator_q_support=tail_annihilator_q_support,
                tail_annihilator_image_rank=tail_annihilator_image_rank,
                head_projection_q_support=head_projection_q_support,
                tail_pivots=tail_pivots,
                trace_dual_mismatches=trace_dual_mismatches,
                shift_intersection_min=shift_min,
                shift_intersection_max=shift_max,
                frobenius_invariant_shifts=invariant_shifts,
            )
        )
    return out


def scan(args: argparse.Namespace) -> list[ResidualTailRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[ResidualTailRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
        if args.max_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m <= args.max_m]
        if not quotient_sizes:
            continue

        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        if not splits:
            continue
        case_had_row = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    extension_degree = int(sp.n_order(q % m, m))
                    if extension_degree > args.max_extension_degree:
                        continue
                    n = h // m
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        if factor.degree() > args.max_factor_degree:
                            continue
                        gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                        if gcd_degree < args.min_tensor_factor_count:
                            continue
                        tensor_factor_degree = factor.degree() // gcd_degree
                        if tensor_factor_degree > args.max_tensor_factor_degree:
                            continue
                        if len(divisors(tensor_factor_degree)) <= 2:
                            continue
                        residues = [
                            fiber.rem(factor)
                            for fiber in section_fiber_polynomials(
                                shifted,
                                q,
                                m,
                                "complement",
                            )
                        ]
                        residue_vectors = [
                            coeff_vector(residue, factor.degree(), q)
                            for residue in residues
                        ]
                        targets = args.target or ["axis"]
                        for target in targets:
                            rows = audit_target(
                                D,
                                q,
                                ell,
                                h,
                                m,
                                factor,
                                shift,
                                residue_vectors,
                                target,
                                args.seed,
                                args.max_top_count,
                            )
                            out.extend(rows)
                            if rows:
                                case_had_row = True
                                cases += 1
                            if args.max_rows is not None and len(out) >= args.max_rows:
                                return out[: args.max_rows]
            if case_had_row and args.one_prime_per_D:
                break
        if cases >= args.max_cases:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--min-h", type=int, default=1)
    ap.add_argument("--max-h", type=int, default=240)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=240)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=20000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=48)
    ap.add_argument("--max-composite-quotients", type=int, default=48)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=1)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=10)
    ap.add_argument("--max-rows", type=int, default=80)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument("--scan-origins", action="store_true")
    ap.add_argument("--one-prime-per-D", action="store_true")
    ap.add_argument(
        "--target",
        action="append",
        help="Target such as axis, constant_plus_4, constant_plus_3.",
    )
    args = ap.parse_args()

    rows = scan(args)
    failures = [
        row for row in rows
        if row.residual_dim > 0 and row.leading_tail_rank < row.residual_dim
    ]
    full_tail = [
        row for row in rows
        if row.residual_dim > 0 and row.tail_rank == row.residual_dim
    ]
    invariant = [
        row for row in rows
        if row.frobenius_invariant_shifts
    ]
    trace_dual_bad = [
        row for row in rows
        if row.trace_dual_mismatches
    ]
    annihilator_degree_bad = [
        row for row in rows
        if row.residual_dim > 0
        and row.tail_annihilator_q_degree != row.subdegree - row.residual_dim
    ]
    annihilator_rank_bad = [
        row for row in rows
        if row.tail_annihilator_image_rank != row.leading_tail_rank
    ]
    proper_residual = [
        row for row in rows
        if 0 < row.residual_dim < row.subdegree
    ]
    proper_invariant = [
        row for row in proper_residual
        if row.frobenius_invariant_shifts
    ]
    proper_full_support = [
        row for row in proper_residual
        if row.tail_annihilator_q_support == row.tail_annihilator_q_degree + 1
        and row.head_projection_q_support == row.subdegree
    ]
    print("trace-frame residual tail audit")
    print(f"rows={len(rows)}")
    print(f"residual_rows={sum(1 for row in rows if row.residual_dim > 0)}")
    print(f"proper_partial_tail_rows={len(proper_residual)}")
    print(f"full_tail_rank_rows={len(full_tail)}")
    print(f"leading_tail_failures={len(failures)}")
    print(f"trace_dual_mismatch_rows={len(trace_dual_bad)}")
    print(f"tail_annihilator_degree_mismatch_rows={len(annihilator_degree_bad)}")
    print(f"tail_annihilator_image_rank_mismatch_rows={len(annihilator_rank_bad)}")
    print(f"frobenius_invariant_residual_rows={len(invariant)}")
    print(f"proper_frobenius_invariant_residual_rows={len(proper_invariant)}")
    print(f"proper_full_qsupport_rows={len(proper_full_support)}")
    for row in rows[: min(len(rows), 80)]:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} "
            f"shift={row.origin_shift} target={row.target} "
            f"factor_deg={row.factor_degree} ext_deg={row.extension_degree} "
            f"tensor_deg={row.tensor_factor_degree} subdeg={row.subdegree} "
            f"reldeg={row.relative_degree} raw_rank={row.raw_rank} "
            f"top_count={row.top_count} prefix_blocks={row.prefix_blocks} "
            f"prefix_rank={row.prefix_rank} residual_dim={row.residual_dim} "
            f"tail_rank={row.tail_rank} leading_tail_rank={row.leading_tail_rank} "
            f"tail_ann_qdeg={row.tail_annihilator_q_degree} "
            f"tail_ann_qsupport={row.tail_annihilator_q_support} "
            f"tail_ann_image_rank={row.tail_annihilator_image_rank} "
            f"head_proj_qsupport={row.head_projection_q_support} "
            f"tail_pivots={list(row.tail_pivots)} "
            f"trace_dual_mismatches={row.trace_dual_mismatches} "
            f"shift_intersection_min={row.shift_intersection_min} "
            f"shift_intersection_max={row.shift_intersection_max} "
            f"invariant_shifts={list(row.frobenius_invariant_shifts)}"
        )
    print("conclusion=reported_trace_frame_residual_tail_audit")


if __name__ == "__main__":
    main()
