#!/usr/bin/env python3
"""Audit rank of the off-diagonal Hermitian Schur coupling.

After splitting the Hermitian axis Gram matrix into diagonal CRT component
blocks, write

    G = D + E

where D is block diagonal and E contains only cross-block pairings.  If E has
small rank, then the Schur correction is a low-rank determinant.  If E has
large rank even in small rows, the correction is genuinely coupled.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_component_schur_audit import block_dets, max_cross_rank
from hermitian_gram_determinant_distribution import det_mod
from hermitian_trace_gram_structure_scan import hermitian_pair_matrix, trace_zero_axis_basis
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
class CouplingRankRow:
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
    diagonal_blocks_nonsingular: bool
    correction_ratio: int | None
    offdiag_rank: int
    offdiag_rank_ratio_num: int
    offdiag_rank_ratio_den: int
    max_cross_rank: int


def offdiag_matrix(
    gram: list[list[int]],
    blocks: dict[str, list[int]],
    q: int,
) -> list[list[int]]:
    out = [[value % q for value in row] for row in gram]
    for indices in blocks.values():
        for r in indices:
            for c in indices:
                out[r][c] = 0
    return out


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
) -> CouplingRankRow | None:
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
    offdiag = offdiag_matrix(gram, blocks, q)
    offdiag_rank = rank_mod_q(offdiag, q)
    axis_dim = len(vectors)
    return CouplingRankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=axis_dim,
        full_rank=full_rank,
        full_det=full_det,
        diagonal_blocks_nonsingular=(diagonal_product is not None),
        correction_ratio=correction_ratio,
        offdiag_rank=offdiag_rank,
        offdiag_rank_ratio_num=offdiag_rank,
        offdiag_rank_ratio_den=axis_dim,
        max_cross_rank=max_cross_rank(gram, blocks, q),
    )


def scan(args: argparse.Namespace) -> list[CouplingRankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[CouplingRankRow] = []
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
                    if factor.degree() > args.max_factor_degree:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=30)
    parser.add_argument("--max-cases", type=int, default=30)
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
    parser.add_argument("--max-factor-degree", type=int, default=120)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_rows = [row for row in rows if row.full_rank == row.axis_dim and row.full_det]
    high_offdiag_rows = [
        row for row in rows
        if 2 * row.offdiag_rank >= row.axis_dim
    ]
    print("Hermitian Schur off-diagonal coupling-rank audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg comps axis_dim full_rank full_det "
            "diag_nonsing correction offdiag_rank max_cross"
        )
        display = high_offdiag_rows or rows[:80]
        for row in display[:120]:
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:4d} full_rank={row.full_rank:4d} "
                f"full_det={row.full_det:8d} "
                f"diag_nonsing={int(row.diagonal_blocks_nonsingular)} "
                f"correction={row.correction_ratio} "
                f"offdiag_rank={row.offdiag_rank:4d}/{row.axis_dim:<4d} "
                f"max_cross={row.max_cross_rank:3d}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  full_nonzero_rows={len(full_rows)}")
    print(f"  high_offdiag_rank_rows={len(high_offdiag_rows)}")
    if rows:
        print(f"  max_offdiag_rank={max(row.offdiag_rank for row in rows)}")
        print(
            "  max_offdiag_rank_ratio="
            f"{max(row.offdiag_rank / row.axis_dim for row in rows):.6f}"
        )
        print(f"  max_cross_rank_seen={max(row.max_cross_rank for row in rows)}")
    print()
    print("interpretation")
    print("  high_offdiag_rank_rules_out_tiny_low_rank_schur_correction=1")
    print("  mixed_character_pairing_remains_the_coupled_punit_target=1")
    print("conclusion=reported_hermitian_schur_coupling_rank_audit")


if __name__ == "__main__":
    main()
