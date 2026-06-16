#!/usr/bin/env python3
"""Audit low-relative-degree congruences in trace-frame toy rows.

The p24 local-unit theorem fails in one tensor factor iff a nonzero
axis-supported vector satisfies

    g'(theta) * x_w has relative degree <= 27 over C.

Small rows can force the same kind of kernel by taking too few top relative
coefficient blocks.  This script inspects those forced kernels: are the
relations sparse in the axis components or in the remaining low coefficient
blocks, or do they already require cross-axis/full-tail support?
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp

from beta_orbit_tensor_factor_bridge_audit import eligible_cases
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    PolyE,
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
from relative_moment_projection_scan import section_fiber_polynomials
from tensor_factor_dual_basis_window_audit import (
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    solve_square,
    top_window_coords,
)
from tensor_factor_moore_audit import b_add, b_is_zero, b_mul
from tensor_factor_subfield_trace_audit import divisors, element_row
from trace_frame_residual_tail_audit import right_nullspace, transpose


@dataclass(frozen=True)
class CongruenceRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_count: int
    tensor_factor_degree: int
    subdegree: int
    relative_degree: int
    top_count: int
    axis_dim: int
    target_dim: int
    rank: int
    kernel_dim: int
    basis_index: int
    axis_support: int
    axis_block_touches: int
    low_nonzero_blocks: int
    low_scalar_support: int
    low_max_block: int
    high_zero: bool


def block_positions(m: int) -> list[tuple[str, list[int]]]:
    out: list[tuple[str, list[int]]] = []
    offset = 0
    for name, freqs in frequency_blocks(m):
        positions = list(range(offset, offset + len(freqs)))
        out.append((name, positions))
        offset += len(freqs)
    return out


def combine_elements(
    coeffs: list[FpE],
    elements: list[PolyE],
    factor: PolyE,
    field: ExtensionField,
) -> PolyE:
    total = [field.zero]
    for coeff, element in zip(coeffs, elements):
        if coeff == field.zero:
            continue
        total = b_add(total, b_mul([coeff], element, factor, field), factor, field)
    return total


def relative_coords(
    value: PolyE,
    gprime_theta: PolyE,
    basis_columns: list[list[FpE]],
    factor: PolyE,
    field: ExtensionField,
) -> list[FpE]:
    adjusted = b_mul(value, gprime_theta, factor, field)
    return solve_square(basis_columns, element_row(adjusted, factor, field), field)


def summarize_case(case, args: argparse.Namespace) -> list[CongruenceRow]:
    D, q, ell, cycle, m, factor = (
        case.D,
        case.q,
        case.ell,
        case.cycle,
        case.m,
        case.factor,
    )
    h = len(cycle)
    n = h // m
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, args.seed)
    tensor_factor_count = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // tensor_factor_count
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        args.seed,
    )[0]

    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    blocks = block_positions(m)
    frequencies = [freq for _, freqs in frequency_blocks(m) for freq in freqs]
    rows = character_rows(residue_vectors, frequencies, zeta, field)
    raw_rank = rank_in_factor(rows, selected_factor, field)
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]

    out: list[CongruenceRow] = []
    for subdegree in divisors(tensor_factor_degree):
        if subdegree in (1, tensor_factor_degree):
            continue
        relative_degree = tensor_factor_degree // subdegree
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
        max_top_count = min(args.max_top_count, relative_degree)
        for top_count in range(1, max_top_count + 1):
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
            rank = rank_over_extension(top_matrix, field)
            kernel_dim = raw_rank - rank
            if kernel_dim <= 0:
                continue
            kernel_basis = right_nullspace(transpose(top_matrix), field)
            for basis_index, coeffs in enumerate(kernel_basis[: args.max_kernel_basis]):
                combo = combine_elements(coeffs, elements, selected_factor, field)
                if b_is_zero(combo, field):
                    continue
                coords = relative_coords(
                    combo,
                    gprime_theta,
                    basis_columns,
                    selected_factor,
                    field,
                )
                low_block_limit = relative_degree - top_count
                low_blocks = [
                    coords[j * subdegree : (j + 1) * subdegree]
                    for j in range(low_block_limit)
                ]
                high_blocks = [
                    coords[j * subdegree : (j + 1) * subdegree]
                    for j in range(low_block_limit, relative_degree)
                ]
                nonzero_low_indices = [
                    j for j, block in enumerate(low_blocks)
                    if any(value != field.zero for value in block)
                ]
                axis_support = sum(1 for value in coeffs if value != field.zero)
                axis_block_touches = sum(
                    1 for _, positions in blocks
                    if any(coeffs[pos] != field.zero for pos in positions)
                )
                out.append(
                    CongruenceRow(
                        D=D,
                        q=q,
                        ell=ell,
                        h=h,
                        m=m,
                        n=n,
                        factor_degree=factor.degree(),
                        extension_degree=extension_degree,
                        tensor_factor_count=tensor_factor_count,
                        tensor_factor_degree=tensor_factor_degree,
                        subdegree=subdegree,
                        relative_degree=relative_degree,
                        top_count=top_count,
                        axis_dim=len(frequencies),
                        target_dim=top_count * subdegree,
                        rank=rank,
                        kernel_dim=kernel_dim,
                        basis_index=basis_index,
                        axis_support=axis_support,
                        axis_block_touches=axis_block_touches,
                        low_nonzero_blocks=len(nonzero_low_indices),
                        low_scalar_support=sum(
                            1 for block in low_blocks for value in block
                            if value != field.zero
                        ),
                        low_max_block=max(nonzero_low_indices) if nonzero_low_indices else -1,
                        high_zero=all(
                            value == field.zero
                            for block in high_blocks
                            for value in block
                        ),
                    )
                )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=40000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--max-discriminants", type=int, default=5000)
    ap.add_argument("--min-h", type=int, default=24)
    ap.add_argument("--max-h", type=int, default=220)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--max-n", type=int, default=200)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=30000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=32)
    ap.add_argument("--max-composite-quotients", type=int, default=16)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=2)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=2)
    ap.add_argument("--max-kernel-basis", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-prime-n", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--require-composite-m", action="store_true")
    args = ap.parse_args()

    rows: list[CongruenceRow] = []
    for case in eligible_cases(args):
        rows.extend(summarize_case(case, args))

    print("trace-frame low-relative-degree congruence audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n factor_deg E_deg tensor_count tensor_deg "
        "subdeg rel top axis_dim target_dim rank kernel_dim basis "
        "axis_support axis_block_touches low_nonzero_blocks low_scalar_support "
        "low_max_block high_zero"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"factor_deg={row.factor_degree} E_deg={row.extension_degree} "
            f"tensor_count={row.tensor_factor_count} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} rel={row.relative_degree} top={row.top_count} "
            f"axis_dim={row.axis_dim} target_dim={row.target_dim} "
            f"rank={row.rank} kernel_dim={row.kernel_dim} basis={row.basis_index} "
            f"axis_support={row.axis_support} "
            f"axis_block_touches={row.axis_block_touches} "
            f"low_nonzero_blocks={row.low_nonzero_blocks} "
            f"low_scalar_support={row.low_scalar_support} "
            f"low_max_block={row.low_max_block} "
            f"high_zero={int(row.high_zero)}"
        )
    print()
    print("interpretation")
    print("  high_zero=1 verifies the low-relative-degree congruence.")
    print("  axis_block_touches>1 means the relation is genuinely cross-axis.")
    print("  low_nonzero_blocks near rel-top means the low tail is not sparse.")
    print("conclusion=reported_trace_frame_low_degree_congruence_audit")


if __name__ == "__main__":
    main()

