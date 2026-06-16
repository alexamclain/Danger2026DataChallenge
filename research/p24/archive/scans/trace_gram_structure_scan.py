#!/usr/bin/env python3
"""Structure scan for the axis trace-Gram matrix.

The trace-Gram certificate is useful only if its determinant has exploitable
structure.  This script tests the first two possible simplifications on small
CM packets:

1. Is the kernel K_{r,s}=Tr(F_r F_s) circulant in r-s or r+s?
2. Is the axis Gram matrix block-diagonal, or nearly so, across the CRT
   components of m?

The expected useful outcome would be a sum/difference-circulant kernel or
zero cross-blocks.  A negative result means the trace-Gram determinant is a
real phase-aware autocorrelation object, not a free character product.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import (
    axis_basis_images,
    coeff_vector,
    discriminants,
    rank_mod_q,
)
from trace_pairing_axis_boundary import trace_power_sums, trace_product


@dataclass(frozen=True)
class StructureRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    axis_rank: int
    gram_rank: int
    kernel_sum_circulant: bool
    kernel_diff_circulant: bool
    zero_cross_block_pairs: int
    total_cross_block_pairs: int
    max_cross_block_rank: int
    origin_shift: int


def matrix_rank(matrix: list[list[int]], q: int) -> int:
    return rank_mod_q(matrix, q)


def kernel_matrix(
    residue_vectors: list[list[int]],
    power_sums: list[int],
    q: int,
) -> list[list[int]]:
    return [
        [trace_product(left, right, power_sums, q) for right in residue_vectors]
        for left in residue_vectors
    ]


def is_sum_circulant(matrix: list[list[int]], q: int) -> bool:
    m = len(matrix)
    values: dict[int, int] = {}
    for r in range(m):
        for s in range(m):
            key = (r + s) % m
            value = matrix[r][s] % q
            if key in values and values[key] != value:
                return False
            values[key] = value
    return True


def is_diff_circulant(matrix: list[list[int]], q: int) -> bool:
    m = len(matrix)
    values: dict[int, int] = {}
    for r in range(m):
        for s in range(m):
            key = (r - s) % m
            value = matrix[r][s] % q
            if key in values and values[key] != value:
                return False
            values[key] = value
    return True


def block_names(components: tuple[int, ...]) -> dict[str, list[int]]:
    """Return axis-basis indices for constant and component blocks."""
    out: dict[str, list[int]] = {"constant": [0]}
    index = 1
    for component in components:
        size = component - 1
        out[str(component)] = list(range(index, index + size))
        index += size
    return out


def cross_block_stats(
    gram: list[list[int]],
    components: tuple[int, ...],
    q: int,
) -> tuple[int, int, int]:
    blocks = block_names(components)
    names = [name for name in blocks if name != "constant"]
    zero_pairs = 0
    total_pairs = 0
    max_rank = 0
    for i, left_name in enumerate(names):
        for right_name in names[i + 1 :]:
            left = blocks[left_name]
            right = blocks[right_name]
            sub = [[gram[r][s] % q for s in right] for r in left]
            rank = matrix_rank(sub, q)
            total_pairs += 1
            if rank == 0:
                zero_pairs += 1
            max_rank = max(max_rank, rank)
    return zero_pairs, total_pairs, max_rank


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> StructureRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [
        coeff_vector(residue, factor.degree(), q) for residue in residues
    ]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    kernel = kernel_matrix(residue_vectors, power_sums, q)

    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    axis_vectors = [
        coeff_vector(poly, factor.degree(), q) for _, poly in images
    ]
    gram = [
        [trace_product(left, right, power_sums, q) for right in axis_vectors]
        for left in axis_vectors
    ]
    zero_pairs, total_pairs, max_cross_rank = cross_block_stats(
        gram, components, q
    )
    return StructureRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(axis_vectors),
        axis_rank=matrix_rank(axis_vectors, q),
        gram_rank=matrix_rank(gram, q),
        kernel_sum_circulant=is_sum_circulant(kernel, q),
        kernel_diff_circulant=is_diff_circulant(kernel, q),
        zero_cross_block_pairs=zero_pairs,
        total_cross_block_pairs=total_pairs,
        max_cross_block_rank=max_cross_rank,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[StructureRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[StructureRow] = []
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
        quotient_sizes = [
            m
            for m in quotient_sizes
            if m <= args.max_m
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
        ]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
            ]
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
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    n = h // m
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                        if factor.degree() < axis_dim:
                            continue
                        rows.append(
                            audit_packet(D, q, ell, shifted, m, factor, shift)
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=20)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=70)
    parser.add_argument("--max-m", type=int, default=90)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_axis_rows = [row for row in rows if row.axis_rank == row.axis_dim]
    full_gram_rows = [row for row in rows if row.gram_rank == row.axis_dim]
    sum_circ_rows = [row for row in rows if row.kernel_sum_circulant]
    diff_circ_rows = [row for row in rows if row.kernel_diff_circulant]
    all_cross_zero_rows = [
        row
        for row in rows
        if row.total_cross_block_pairs
        and row.zero_cross_block_pairs == row.total_cross_block_pairs
    ]

    print("trace-Gram structure scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"max_m={args.max_m}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg components axis_dim axis_rank "
            "gram_rank sum_circ diff_circ zero_cross/total max_cross_rank origin"
        )
        display = (
            [row for row in rows if row.gram_rank < row.axis_dim]
            +
            [row for row in rows if row.axis_rank < row.axis_dim]
            +
            [row for row in rows if row.kernel_sum_circulant or row.kernel_diff_circulant]
            + all_cross_zero_rows
        )
        if not display:
            display = rows[:40]
        for row in display[:80]:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:3d} axis_rank={row.axis_rank:3d} "
                f"gram_rank={row.gram_rank:3d} "
                f"sum_circ={int(row.kernel_sum_circulant)} "
                f"diff_circ={int(row.kernel_diff_circulant)} "
                f"zero_cross={row.zero_cross_block_pairs}/{row.total_cross_block_pairs} "
                f"max_cross_rank={row.max_cross_block_rank:3d} "
                f"origin={row.origin_shift:3d}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  full_axis_rank_rows={len(full_axis_rows)}")
    print(f"  full_trace_gram_rank_rows={len(full_gram_rows)}")
    print(f"  kernel_sum_circulant_rows={len(sum_circ_rows)}")
    print(f"  kernel_diff_circulant_rows={len(diff_circ_rows)}")
    print(f"  all_cross_blocks_zero_rows={len(all_cross_zero_rows)}")
    if rows:
        max_cross = max(row.max_cross_block_rank for row in rows)
        print(f"  max_cross_block_rank_seen={max_cross}")
    print()
    print("interpretation")
    print("  circulant_kernel_would_give_free_character_factorization=1")
    print("  zero_cross_blocks_would_give_free_crt_block_factorization=1")
    print("  absence_of_both_means_trace_gram_is_phase_aware_not_formal=1")
    print("conclusion=reported_trace_gram_structure_scan")


if __name__ == "__main__":
    main()
