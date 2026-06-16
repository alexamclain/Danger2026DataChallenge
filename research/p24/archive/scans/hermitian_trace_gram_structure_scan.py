#!/usr/bin/env python3
"""Structure scan for the Hermitian axis trace-Gram matrix.

This tests whether the Hermitian trace pairing

    <x,y> = Tr(x * y^(q^(d/2)))

has the representation-theoretic simplifications one would hope for:

1. complement-kernel invariance: <F_r,F_s> depends only on r-s;
2. CRT trace-zero block orthogonality:

       <U_c, U_c'> = 0 for c != c',
       <constant, U_c> = 0.

If both held, the 368-dimensional p24 Hermitian determinant would split into
one constant factor and the 2-, 157-, and 211-axis block determinants.  If not,
the determinant is still a plausible p-unit target, but not a free character
factorization.
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
from crt_partial_moment_projection_scan import (
    coprime_components,
    scale_poly,
    sum_polys,
    zero_poly_like,
)
from l1_axis_injectivity_scan import coeff_vector, discriminants, rank_mod_q
from trace_pairing_axis_boundary import trace_power_sums, trace_product
from hermitian_trace_gram_scan import frobenius_middle_vector


@dataclass(frozen=True)
class HermitianStructureRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    trace_zero_axis_rank: int
    hermitian_gram_rank: int
    kernel_diff_circulant: bool
    constant_orthogonal_components: int
    component_count: int
    zero_cross_block_pairs: int
    total_cross_block_pairs: int
    max_cross_block_rank: int
    origin_shift: int


def hermitian_pair_matrix(
    left_vectors: list[list[int]],
    right_vectors: list[list[int]],
    factor: sp.Poly,
    q: int,
    power_sums: list[int],
) -> list[list[int]]:
    right_conjugates = [
        frobenius_middle_vector(vector, factor, q) for vector in right_vectors
    ]
    return [
        [trace_product(left, right, power_sums, q) for right in right_conjugates]
        for left in left_vectors
    ]


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


def component_axis_sums(
    residues: list[sp.Poly],
    component: int,
    factor: sp.Poly,
) -> list[sp.Poly]:
    out: list[sp.Poly] = []
    for t in range(component):
        terms = [residues[r] for r in range(t, len(residues), component)]
        out.append(sum_polys(terms).rem(factor) if terms else zero_poly_like(residues[0]))
    return out


def trace_zero_axis_basis(
    residues: list[sp.Poly],
    components: tuple[int, ...],
    factor: sp.Poly,
) -> tuple[list[tuple[str, sp.Poly]], dict[str, list[int]]]:
    images: list[tuple[str, sp.Poly]] = [("constant", sum_polys(residues).rem(factor))]
    blocks: dict[str, list[int]] = {"constant": [0]}
    for component in components:
        axis = component_axis_sums(residues, component, factor)
        start = len(images)
        for t in range(1, component):
            diff = (axis[t] + scale_poly(axis[0], -1)).rem(factor)
            images.append((f"U{component}_{t}", diff))
        blocks[str(component)] = list(range(start, len(images)))
    return images, blocks


def matrix_subrank(
    matrix: list[list[int]],
    rows: list[int],
    cols: list[int],
    q: int,
) -> int:
    return rank_mod_q([[matrix[r][c] % q for c in cols] for r in rows], q)


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> HermitianStructureRow | None:
    if factor.degree() % 2:
        return None
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
    kernel = hermitian_pair_matrix(
        residue_vectors, residue_vectors, factor, q, power_sums
    )

    components = coprime_components(m)
    images, blocks = trace_zero_axis_basis(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    gram = hermitian_pair_matrix(vectors, vectors, factor, q, power_sums)

    constant_block = blocks["constant"]
    constant_orthogonal = 0
    for component in components:
        block = blocks[str(component)]
        if matrix_subrank(gram, constant_block, block, q) == 0:
            constant_orthogonal += 1

    zero_cross = 0
    total_cross = 0
    max_cross = 0
    names = [str(component) for component in components]
    for i, left_name in enumerate(names):
        for right_name in names[i + 1 :]:
            rank = matrix_subrank(gram, blocks[left_name], blocks[right_name], q)
            total_cross += 1
            if rank == 0:
                zero_cross += 1
            max_cross = max(max_cross, rank)

    return HermitianStructureRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(vectors),
        trace_zero_axis_rank=rank_mod_q(vectors, q),
        hermitian_gram_rank=rank_mod_q(gram, q),
        kernel_diff_circulant=is_diff_circulant(kernel, q),
        constant_orthogonal_components=constant_orthogonal,
        component_count=len(components),
        zero_cross_block_pairs=zero_cross,
        total_cross_block_pairs=total_cross,
        max_cross_block_rank=max_cross,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[HermitianStructureRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[HermitianStructureRow] = []
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
                        row = audit_packet(D, q, ell, shifted, m, factor, shift)
                        if row is not None:
                            rows.append(row)
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=75)
    parser.add_argument("--max-m", type=int, default=90)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_gram_rows = [row for row in rows if row.hermitian_gram_rank == row.axis_dim]
    diff_circulant_rows = [row for row in rows if row.kernel_diff_circulant]
    all_constant_orthogonal_rows = [
        row for row in rows
        if row.constant_orthogonal_components == row.component_count
    ]
    all_cross_orthogonal_rows = [
        row for row in rows
        if row.total_cross_block_pairs
        and row.zero_cross_block_pairs == row.total_cross_block_pairs
    ]

    print("Hermitian trace-Gram structure scan")
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
            "gram_rank diff_circ const_orth/comp zero_cross/total "
            "max_cross_rank origin"
        )
        display = (
            [row for row in rows if row.hermitian_gram_rank < row.axis_dim]
            + diff_circulant_rows
            + all_cross_orthogonal_rows
        )
        if not display:
            display = rows[:60]
        for row in display[:100]:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:3d} "
                f"axis_rank={row.trace_zero_axis_rank:3d} "
                f"gram_rank={row.hermitian_gram_rank:3d} "
                f"diff_circ={int(row.kernel_diff_circulant)} "
                f"const_orth={row.constant_orthogonal_components}/{row.component_count} "
                f"zero_cross={row.zero_cross_block_pairs}/{row.total_cross_block_pairs} "
                f"max_cross_rank={row.max_cross_block_rank:3d} "
                f"origin={row.origin_shift:3d}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  full_hermitian_gram_rows={len(full_gram_rows)}")
    print(f"  kernel_diff_circulant_rows={len(diff_circulant_rows)}")
    print(f"  constant_orthogonal_to_all_component_rows={len(all_constant_orthogonal_rows)}")
    print(f"  all_cross_component_blocks_zero_rows={len(all_cross_orthogonal_rows)}")
    if rows:
        print(
            "  max_cross_block_rank_seen="
            f"{max(row.max_cross_block_rank for row in rows)}"
        )
    print()
    print("interpretation")
    print("  diff_circulant_kernel_would_diagonalize_full_K_characters=1")
    print("  cross_block_zero_would_factor_the_axis_determinant_by_CRT_components=1")
    print("  failure_of_both_means_the_hermitian_punit_theorem_is_still_coupled=1")
    print("conclusion=reported_hermitian_trace_gram_structure_scan")


if __name__ == "__main__":
    main()
