#!/usr/bin/env python3
"""Audit diagonal-block and Schur-product structure of Hermitian axis Gram.

The Hermitian axis determinant is the best intrinsic p-unit target currently
on the table.  A tempting reduction is:

    full determinant = product(component determinants) * small correction.

This script checks whether the diagonal block determinants are themselves
nonzero, and records the correction ratio

    det(full Gram) / product det(diagonal blocks)

on small composite CRT rows.  If any diagonal block is singular while the full
Gram is nonsingular, the naive component-punit route is dead in that row.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_gram_determinant_distribution import det_mod
from hermitian_trace_gram_structure_scan import (
    hermitian_pair_matrix,
    matrix_subrank,
    trace_zero_axis_basis,
)
from l1_axis_injectivity_scan import coeff_vector, discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from trace_pairing_axis_boundary import trace_power_sums


@dataclass(frozen=True)
class BlockDet:
    name: str
    size: int
    rank: int
    det: int | None


@dataclass(frozen=True)
class SchurRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    full_rank: int
    full_det: int
    blocks: tuple[BlockDet, ...]
    diagonal_product: int | None
    correction_ratio: int | None
    max_cross_rank: int


def submatrix(matrix: list[list[int]], rows: list[int], cols: list[int]) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def block_dets(
    gram: list[list[int]],
    blocks: dict[str, list[int]],
    q: int,
) -> tuple[BlockDet, ...]:
    out: list[BlockDet] = []
    for name, indices in blocks.items():
        square = submatrix(gram, indices, indices)
        rank = rank_mod_q(square, q)
        det = det_mod(square, q) if len(square) and len(square) == len(square[0]) else None
        out.append(BlockDet(name=name, size=len(indices), rank=rank, det=det))
    return tuple(out)


def max_cross_rank(gram: list[list[int]], blocks: dict[str, list[int]], q: int) -> int:
    names = list(blocks)
    out = 0
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            out = max(out, matrix_subrank(gram, blocks[left], blocks[right], q))
    return out


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
) -> SchurRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images, blocks = trace_zero_axis_basis(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    gram = hermitian_pair_matrix(vectors, vectors, factor, q, power_sums)

    full_rank = rank_mod_q(gram, q)
    full_det = det_mod(gram, q)
    bdets = block_dets(gram, blocks, q)
    diagonal_product: int | None = 1
    for block in bdets:
        if block.det is None or block.det % q == 0:
            diagonal_product = None
            break
        diagonal_product = (diagonal_product * block.det) % q
    correction_ratio = None
    if diagonal_product is not None:
        correction_ratio = full_det * pow(diagonal_product, -1, q) % q

    return SchurRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(vectors),
        full_rank=full_rank,
        full_det=full_det,
        blocks=bdets,
        diagonal_product=diagonal_product,
        correction_ratio=correction_ratio,
        max_cross_rank=max_cross_rank(gram, blocks, q),
    )


def scan(args: argparse.Namespace) -> list[SchurRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[SchurRow] = []
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
        quotient_sizes = [
            m
            for m in quotient_sizes
            if sp.gcd(m, h // m) == 1
            and m <= args.max_m
            and len(coprime_components(m)) >= 2
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
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
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim:
                        continue
                    row = audit_packet(D, q, ell, shifted, m, factor)
                    if row is not None:
                        rows.append(row)
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def format_blocks(blocks: tuple[BlockDet, ...]) -> str:
    return ",".join(
        f"{block.name}:size{block.size}:rank{block.rank}:det{block.det}"
        for block in blocks
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=40)
    parser.add_argument("--max-cases", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=260)
    parser.add_argument("--max-abs-D", type=int, default=120000)
    parser.add_argument("--max-prime-quotients", type=int, default=16)
    parser.add_argument("--max-composite-quotients", type=int, default=40)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=260)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=1_000_000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=100)
    parser.add_argument("--max-m", type=int, default=180)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_rows = [row for row in rows if row.full_rank == row.axis_dim and row.full_det]
    singular_diag_rows = [
        row for row in full_rows
        if any(block.det == 0 for block in row.blocks)
    ]
    correction_rows = [
        row for row in full_rows
        if row.correction_ratio is not None
    ]
    correction_values = [row.correction_ratio for row in correction_rows]

    print("Hermitian component Schur audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg comps axis_dim full_rank full_det "
            "diag_product correction max_cross blocks"
        )
        display = singular_diag_rows or rows[:80]
        for row in display[:120]:
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:4d} full_rank={row.full_rank:4d} "
                f"full_det={row.full_det:8d} diag_product={row.diagonal_product} "
                f"correction={row.correction_ratio} max_cross={row.max_cross_rank:3d} "
                f"blocks={format_blocks(row.blocks)}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  full_nonzero_rows={len(full_rows)}")
    print(f"  full_nonzero_but_singular_diagonal_block_rows={len(singular_diag_rows)}")
    print(f"  correction_ratio_rows={len(correction_rows)}")
    print(f"  distinct_correction_ratios={len(set(correction_values))}")
    print(f"  correction_ratio_one_rows={sum(1 for value in correction_values if value == 1)}")
    if rows:
        print(f"  max_cross_rank_seen={max(row.max_cross_rank for row in rows)}")
    print()
    print("interpretation")
    print("  singular_diagonal_blocks_kill_naive_component_punit_factorization=1")
    print("  correction_ratio_not_one_means_cross_coupling_changes_the_unit=1")
    print("conclusion=reported_hermitian_component_schur_audit")


if __name__ == "__main__":
    main()
