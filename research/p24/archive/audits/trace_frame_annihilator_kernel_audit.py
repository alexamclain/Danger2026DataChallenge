#!/usr/bin/env python3
"""Kernel-shape audit for the trace-frame annihilator obstruction.

The p24 trace-frame theorem is:

    W_axis(B) cap Ann_3 = {0}.

If it fails, a nonzero axis-supported K-character combination maps into the
canonical trace annihilator.  In small rows we can intentionally use too few
top trace-frame blocks so that a kernel is forced by dimension, then ask:

* is the kernel explained by one smooth-axis component block?
* or does it already require cross-block cancellation?

This does not prove p24.  It tells us whether a proposed theorem can plausibly
be componentwise, or whether it must control the full axis directness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp

from beta_orbit_tensor_factor_bridge_audit import eligible_cases
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    rank_in_factor,
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
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_residual_tail_audit import right_nullspace, transpose


@dataclass(frozen=True)
class KernelRow:
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
    single_block_kernel_dims: tuple[tuple[str, int], ...]
    pair_kernel_dims: tuple[tuple[str, str, int], ...]
    basis_support_min: int
    basis_support_max: int
    basis_block_touch_hist: tuple[tuple[int, int], ...]


def histogram(values: list[int]) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return tuple(sorted(out.items()))


def block_indices(m: int) -> list[tuple[str, list[int], list[int]]]:
    """Return `(name, frequencies, positions)` for the flattened axis order."""

    out: list[tuple[str, list[int], list[int]]] = []
    offset = 0
    for name, freqs in frequency_blocks(m):
        positions = list(range(offset, offset + len(freqs)))
        out.append((name, freqs, positions))
        offset += len(freqs)
    return out


def matrix_rank(rows, field: ExtensionField) -> int:
    return rank_over_extension(rows, field)


def restriction_rank(top_matrix, positions: list[int], field: ExtensionField) -> int:
    return matrix_rank([top_matrix[pos] for pos in positions], field)


def support_shape(kernel_basis, blocks, field: ExtensionField) -> tuple[int, int, tuple[tuple[int, int], ...]]:
    if not kernel_basis:
        return 0, 0, ()
    supports: list[int] = []
    block_touches: list[int] = []
    for vec in kernel_basis:
        supports.append(sum(1 for value in vec if value != field.zero))
        touched = 0
        for _, _, positions in blocks:
            if any(vec[pos] != field.zero for pos in positions):
                touched += 1
        block_touches.append(touched)
    return min(supports), max(supports), histogram(block_touches)


def summarize_case(case, args: argparse.Namespace) -> list[KernelRow]:
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
    frequencies = [freq for _, freqs, _ in blocks for freq in freqs]
    rows = character_rows(residue_vectors, frequencies, zeta, field)
    raw_rank = rank_in_factor(rows, selected_factor, field)
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]

    out: list[KernelRow] = []
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
            rank = matrix_rank(top_matrix, field)
            kernel_dim = raw_rank - rank
            if args.only_kernel_rows and kernel_dim == 0:
                continue
            kernel_basis = right_nullspace(transpose(top_matrix), field)
            support_min, support_max, touch_hist = support_shape(
                kernel_basis,
                blocks,
                field,
            )
            single_dims = tuple(
                (
                    name,
                    len(positions) - restriction_rank(top_matrix, positions, field),
                )
                for name, _, positions in blocks
            )
            pair_dims: list[tuple[str, str, int]] = []
            for i, (left_name, _, left_pos) in enumerate(blocks):
                for right_name, _, right_pos in blocks[i + 1:]:
                    positions = left_pos + right_pos
                    dim = len(positions) - restriction_rank(top_matrix, positions, field)
                    if dim:
                        pair_dims.append((left_name, right_name, dim))
            out.append(
                KernelRow(
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
                    single_block_kernel_dims=single_dims,
                    pair_kernel_dims=tuple(pair_dims),
                    basis_support_min=support_min,
                    basis_support_max=support_max,
                    basis_block_touch_hist=touch_hist,
                )
            )
    return out


def fmt_single(items: tuple[tuple[str, int], ...]) -> str:
    return "[" + ",".join(f"{name}:{dim}" for name, dim in items) + "]"


def fmt_pairs(items: tuple[tuple[str, str, int], ...]) -> str:
    if not items:
        return "[]"
    return "[" + ",".join(f"{left}+{right}:{dim}" for left, right, dim in items) + "]"


def fmt_hist(items: tuple[tuple[int, int], ...]) -> str:
    if not items:
        return "[]"
    return "[" + ",".join(f"{key}:{value}" for key, value in items) + "]"


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
    ap.add_argument("--only-kernel-rows", action=argparse.BooleanOptionalAction, default=True)
    args = ap.parse_args()

    rows: list[KernelRow] = []
    for case in eligible_cases(args):
        rows.extend(summarize_case(case, args))

    print("trace-frame annihilator kernel-shape audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n factor_deg E_deg tensor_count tensor_deg "
        "subdeg rel top axis_dim target_dim rank kernel_dim "
        "single_block_kernel_dims pair_kernel_dims "
        "basis_support_min basis_support_max basis_block_touch_hist"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"factor_deg={row.factor_degree} E_deg={row.extension_degree} "
            f"tensor_count={row.tensor_factor_count} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} rel={row.relative_degree} top={row.top_count} "
            f"axis_dim={row.axis_dim} target_dim={row.target_dim} "
            f"rank={row.rank} kernel_dim={row.kernel_dim} "
            f"single_block_kernel_dims={fmt_single(row.single_block_kernel_dims)} "
            f"pair_kernel_dims={fmt_pairs(row.pair_kernel_dims)} "
            f"basis_support_min={row.basis_support_min} "
            f"basis_support_max={row.basis_support_max} "
            f"basis_block_touch_hist={fmt_hist(row.basis_block_touch_hist)}"
        )
    print()
    print("interpretation")
    print("  single_block_kernel_dims=0 for all blocks rules out one-block explanation.")
    print("  pair_kernel_dims=[] rules out two-block explanation in the displayed kernel.")
    print("  high block-touch counts mean forced kernels require cross-axis cancellation.")
    print("  p24 theorem must rule out the zero kernel at top=3, not just component zeros.")
    print("conclusion=reported_trace_frame_annihilator_kernel_shape_audit")


if __name__ == "__main__":
    main()
