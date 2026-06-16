#!/usr/bin/env python3
"""Audit nontrivial CRT cross-block ranks in the Hermitian axis Gram matrix.

The broader structure scan records that CRT component blocks are not
orthogonal and that the largest cross-block rank seen is one.  Many tiny
examples have a component `2`, so rank one is then automatic on one side.

This focused scan filters for component pairs `c,d > 2`, where a rank-one
cross block would be a genuine structural signal.  A rank greater than one
falsifies the hoped-for low-rank CRT coupling reduction.
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
from l1_axis_injectivity_scan import coeff_vector, discriminants, rank_mod_q
from trace_pairing_axis_boundary import trace_power_sums
from hermitian_trace_gram_structure_scan import (
    hermitian_pair_matrix,
    matrix_subrank,
    trace_zero_axis_basis,
)


@dataclass(frozen=True)
class CrossRankRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    gram_rank: int
    pair_ranks: tuple[tuple[int, int, int], ...]


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
) -> CrossRankRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None

    components = coprime_components(m)
    interesting_pairs = [
        (left, right)
        for i, left in enumerate(components)
        for right in components[i + 1 :]
        if left > 2 and right > 2
    ]
    if not interesting_pairs:
        return None

    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    images, blocks = trace_zero_axis_basis(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    gram = hermitian_pair_matrix(vectors, vectors, factor, q, power_sums)

    pair_ranks = tuple(
        (
            left,
            right,
            matrix_subrank(gram, blocks[str(left)], blocks[str(right)], q),
        )
        for left, right in interesting_pairs
    )
    return CrossRankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(vectors),
        gram_rank=rank_mod_q(gram, q),
        pair_ranks=pair_ranks,
    )


def scan(args: argparse.Namespace) -> list[CrossRankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[CrossRankRow] = []
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
            and len([c for c in coprime_components(m) if c > 2]) >= 2
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
        ]
        if not quotient_sizes:
            continue

        splits = find_splitting_primes(
            pari, hilbert, h, args.q_start, args.q_stop, args.max_splitting_primes
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=500000)
    parser.add_argument("--max-prime-quotients", type=int, default=24)
    parser.add_argument("--max-composite-quotients", type=int, default=80)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=2_000_000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=160)
    parser.add_argument("--max-m", type=int, default=420)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    rows = scan(args)
    print("Hermitian nontrivial CRT cross-block rank audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    print(
        "columns: D q ell h m n deg components axis_dim gram_rank "
        "pair_ranks=(c,d,rank)"
    )
    for row in rows:
        pairs = ",".join(f"({c},{d},{rank})" for c, d, rank in row.pair_ranks)
        print(
            f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
            f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
            f"deg={row.factor_degree:4d} comps={list(row.components)} "
            f"axis_dim={row.axis_dim:4d} gram_rank={row.gram_rank:4d} "
            f"pair_ranks={pairs}"
        )

    ranks = [rank for row in rows for _, _, rank in row.pair_ranks]
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  pair_blocks={len(ranks)}")
    print(f"  max_nontrivial_pair_rank={max(ranks) if ranks else 'NA'}")
    print(f"  rank_gt_one_pair_blocks={sum(1 for rank in ranks if rank > 1)}")
    print()
    print("interpretation")
    print("  rank_gt_one_falsifies_pairwise_rank_one_CRT_coupling=1")
    print("  no_rows_means_small_data_did_not_reach_two_odd_CRT_components=1")
    print("conclusion=reported_hermitian_cross_block_rank_audit")


if __name__ == "__main__":
    main()
