#!/usr/bin/env python3
"""Prefix-intersection audit for the factorized Schubert theorem.

For p24 the prefix part of the trace-frame theorem is

    rank Top_2(W_axis) = 358.

Writing

    W_axis = A + B,
    A = constant + 2-axis + 157-axis,     dim A = 158,
    B = 211-axis,                         dim B = 210,

the target `C^2` has dimension 358.  If the component images have full rank,
then maximal prefix rank is equivalent to

    dim Top_2(A) cap Top_2(B) = 158 + 210 - 358 = 10.

This script checks the analogous intersection statement in compact CM tensor
rows.  It keeps the same component ordering convention used by the local
`coprime_components` helper: A is constant plus all but the last component,
and B is the final component.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import ceil

import sympy as sp

from beta_orbit_tensor_factor_bridge_audit import eligible_cases
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
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
    top_window_coords,
)
from tensor_factor_moore_audit import b_is_zero
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_annihilator_kernel_audit import block_indices


@dataclass(frozen=True)
class PrefixIntersectionRow:
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
    leading_top_count: int
    prefix_blocks: int
    prefix_target_dim: int
    a_name: str
    b_name: str
    a_dim: int
    b_dim: int
    axis_dim: int
    rank_a: int
    rank_b: int
    rank_axis_prefix: int
    intersection_dim: int
    expected_min_intersection: int
    component_full: bool
    intersection_minimal: bool
    prefix_max_rank: bool


def row_rank(rows, field: ExtensionField) -> int:
    return rank_over_extension(rows, field)


def top_rows_for_positions(top_matrix, positions: list[int]):
    return [top_matrix[index] for index in positions]


def summarize_case(case, args: argparse.Namespace) -> list[PrefixIntersectionRow]:
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
    blocks = block_indices(m)
    if len(blocks) < 2:
        return []
    a_blocks = blocks[:-1]
    b_block = blocks[-1]
    a_positions = [pos for _, _, positions in a_blocks for pos in positions]
    b_positions = b_block[2]
    a_name = "+".join(name for name, _, _ in a_blocks)
    b_name = b_block[0]
    frequencies = [freq for _, freqs, _ in blocks for freq in freqs]

    rows = character_rows(residue_vectors, frequencies, zeta, field)
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    if len(elements) != len(frequencies):
        return []

    out: list[PrefixIntersectionRow] = []
    for subdegree in divisors(tensor_factor_degree):
        if subdegree in (1, tensor_factor_degree):
            continue
        relative_degree = tensor_factor_degree // subdegree
        leading_top_count = ceil(len(frequencies) / subdegree)
        prefix_blocks = leading_top_count - 1
        if prefix_blocks <= 0 or leading_top_count > relative_degree:
            continue
        if leading_top_count > args.max_top_count:
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
                prefix_blocks,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                selected_factor,
                field,
            )
            for value in elements
        ]
        rank_a = row_rank(top_rows_for_positions(top_matrix, a_positions), field)
        rank_b = row_rank(top_rows_for_positions(top_matrix, b_positions), field)
        rank_axis = row_rank(top_matrix, field)
        intersection = rank_a + rank_b - rank_axis
        target_dim = prefix_blocks * subdegree
        expected_min_intersection = max(0, len(frequencies) - target_dim)
        out.append(
            PrefixIntersectionRow(
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
                leading_top_count=leading_top_count,
                prefix_blocks=prefix_blocks,
                prefix_target_dim=target_dim,
                a_name=a_name,
                b_name=b_name,
                a_dim=len(a_positions),
                b_dim=len(b_positions),
                axis_dim=len(frequencies),
                rank_a=rank_a,
                rank_b=rank_b,
                rank_axis_prefix=rank_axis,
                intersection_dim=intersection,
                expected_min_intersection=expected_min_intersection,
                component_full=(rank_a == len(a_positions) and rank_b == len(b_positions)),
                intersection_minimal=(intersection == expected_min_intersection),
                prefix_max_rank=(rank_axis == min(len(frequencies), target_dim)),
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
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-prime-n", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--require-composite-m", action="store_true")
    args = ap.parse_args()

    rows: list[PrefixIntersectionRow] = []
    for case in eligible_cases(args):
        rows.extend(summarize_case(case, args))

    print("trace-frame prefix-intersection audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n factor_deg E_deg tensor_count tensor_deg "
        "subdeg rel leading_top prefix_blocks prefix_target "
        "A B dims rankA rankB rankPrefix intersection expected_intersection "
        "component_full intersection_minimal prefix_max_rank"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"factor_deg={row.factor_degree} E_deg={row.extension_degree} "
            f"tensor_count={row.tensor_factor_count} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} rel={row.relative_degree} "
            f"leading_top={row.leading_top_count} prefix_blocks={row.prefix_blocks} "
            f"prefix_target={row.prefix_target_dim} "
            f"A={row.a_name} B={row.b_name} "
            f"dims={row.a_dim}+{row.b_dim}->{row.axis_dim} "
            f"rankA={row.rank_a} rankB={row.rank_b} "
            f"rankPrefix={row.rank_axis_prefix} "
            f"intersection={row.intersection_dim} "
            f"expected_intersection={row.expected_min_intersection} "
            f"component_full={int(row.component_full)} "
            f"intersection_minimal={int(row.intersection_minimal)} "
            f"prefix_max_rank={int(row.prefix_max_rank)}"
        )
    print()
    print("interpretation")
    print("  component_full=1 means both sides have full prefix image rank.")
    print("  expected_intersection is the dimension forced by target capacity.")
    print("  intersection_minimal=1 is the prefix direct-position theorem.")
    print("  prefix_max_rank=1 is the factorized prefix p-unit condition.")
    print("conclusion=reported_trace_frame_prefix_intersection_audit")


if __name__ == "__main__":
    main()
