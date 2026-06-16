#!/usr/bin/env python3
"""Value audit for the leading trace-frame Plucker determinant.

The pivot audit records *which* Plucker coordinate works in small rows.  This
script records the value shape of that coordinate: the determinant of the
leading square coordinate matrix, together with the Gaussian pivot residual
products grouped by top-coefficient block.

For p24 the analogous determinant is the named coordinate

    I_lead = 179 + 179 + 10.

The small-row purpose is not to certify p24, but to decide whether the next
theorem should be phrased as one black-box determinant or as a product of
block/tail p-units.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    relative_norm_to_base,
)
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
    top_window_coords,
)
from tensor_factor_moore_audit import b_is_zero
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_plucker_pivot_audit import frequencies_for_target


Matrix = list[list[FpE]]


@dataclass(frozen=True)
class DeterminantProfile:
    determinant: FpE
    det_base: int | None
    det_norm_base: int | None
    swap_parity: int
    block_products: tuple[FpE, ...]
    block_norms_base: tuple[int | None, ...]
    zero_block_products: tuple[int, ...]


@dataclass(frozen=True)
class ValueRow:
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
    leading_columns: int
    determinant_zero: bool
    det_base: int | None
    det_norm_base: int | None
    block_norms_base: tuple[int | None, ...]
    zero_block_products: tuple[int, ...]


def determinant_profile(
    matrix: Matrix,
    subdegree: int,
    block_count: int,
    field: ExtensionField,
) -> DeterminantProfile:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("expected square matrix")
    mat = [row[:] for row in matrix]
    det = field.one
    swap_parity = 0
    block_products = [field.one for _ in range(block_count)]
    zero_block_products = [0 for _ in range(block_count)]

    for col in range(size):
        pivot = None
        for row in range(col, size):
            if mat[row][col] != field.zero:
                pivot = row
                break
        block = min(block_count - 1, col // subdegree)
        if pivot is None:
            det = field.zero
            zero_block_products[block] += 1
            continue
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            swap_parity ^= 1
        pivot_value = mat[col][col]
        det = field.mul(det, pivot_value)
        block_products[block] = field.mul(block_products[block], pivot_value)
        inv = field.inv(pivot_value)
        for row in range(col + 1, size):
            scale = mat[row][col]
            if scale == field.zero:
                continue
            factor = field.mul(scale, inv)
            mat[row] = [
                field.sub(left, field.mul(factor, right))
                for left, right in zip(mat[row], mat[col])
            ]

    if swap_parity:
        det = field.neg(det)
    det_norm = relative_norm_to_base(det, field.degree, field)
    block_norms = tuple(
        base_value_or_none(relative_norm_to_base(value, field.degree, field), field)
        for value in block_products
    )
    return DeterminantProfile(
        determinant=det,
        det_base=base_value_or_none(det, field),
        det_norm_base=base_value_or_none(det_norm, field),
        swap_parity=swap_parity,
        block_products=tuple(block_products),
        block_norms_base=block_norms,
        zero_block_products=tuple(zero_block_products),
    )


def target_value_rows(
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
) -> list[ValueRow]:
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

    out: list[ValueRow] = []
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
        leading = [row[:raw_rank] for row in top_matrix]
        profile = determinant_profile(leading, subdegree, top_count, field)
        out.append(
            ValueRow(
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
                leading_columns=raw_rank,
                determinant_zero=(profile.determinant == field.zero),
                det_base=profile.det_base,
                det_norm_base=profile.det_norm_base,
                block_norms_base=profile.block_norms_base,
                zero_block_products=profile.zero_block_products,
            )
        )
    return out


def scan(args: argparse.Namespace) -> list[ValueRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[ValueRow] = []
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
                        out.extend(
                            target_value_rows(
                                D,
                                q,
                                ell,
                                h,
                                m,
                                factor,
                                shift,
                                residue_vectors,
                                args.target,
                                args.seed,
                                args.max_top_count,
                            )
                        )
                        case_had_row = True
                        if len(out) >= args.max_rows:
                            return out
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return out


def fmt_tuple(values: tuple[int | None, ...]) -> str:
    return "[" + ",".join("NA" if value is None else str(value) for value in values) + "]"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=24)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=48)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--target", default="axis")
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--max-top-count", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    nonzero = [row for row in rows if not row.determinant_zero]
    base_values = [row.det_base for row in rows if row.det_base is not None]
    norm_values = [row.det_norm_base for row in rows if row.det_norm_base is not None]
    block_norm_shapes = Counter(row.block_norms_base for row in rows)

    print("trace-frame leading residual value audit")
    print(f"target={args.target}")
    print(f"rows={len(rows)}")
    print(f"nonzero_determinant_rows={len(nonzero)}")
    print(f"zero_determinant_rows={len(rows) - len(nonzero)}")
    print(f"determinants_in_base_field={len(base_values)}")
    print(f"distinct_det_base_values={len(set(base_values))}")
    print(f"determinant_norms_available={len(norm_values)}")
    print(f"distinct_det_norms={len(set(norm_values))}")
    print(f"zero_det_norms={sum(1 for value in norm_values if value == 0)}")
    print(f"scan_origins={args.scan_origins}")
    print()
    print(
        "columns: D q ell h m n origin target deg ext factor_deg sub rel raw "
        "top_count det_zero det_base det_norm block_norms zero_block_products"
    )
    for row in rows[: min(80, len(rows))]:
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"origin={row.origin_shift:3d} target={row.target:>16s} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"sub={row.subdegree:3d} rel={row.relative_degree:3d} "
            f"raw={row.raw_rank:3d} top_count={row.top_count:2d} "
            f"det_zero={int(row.determinant_zero)} "
            f"det_base={row.det_base if row.det_base is not None else 'NA'} "
            f"det_norm={row.det_norm_base if row.det_norm_base is not None else 'NA'} "
            f"block_norms={fmt_tuple(row.block_norms_base)} "
            f"zero_blocks={list(row.zero_block_products)}"
        )
    print()
    print("block_norm_shape_hist")
    for shape, count in sorted(block_norm_shapes.items(), key=lambda item: (str(item[0]), item[1])):
        print(f"  block_norms={fmt_tuple(shape)} count={count}")
    print()
    print("interpretation")
    print("  determinant_nonzero_is_the_named_leading_Plucker_coordinate=1")
    print("  block_norms_are_candidate_residual_punit_factors=1")
    print("conclusion=reported_trace_frame_leading_residual_value_audit")


if __name__ == "__main__":
    main()
