#!/usr/bin/env python3
"""K-character rank scan when the K roots of unity live in the base field.

For complement-section packet elements

    F_r mod f,      0 <= r < m,

full relative K-normality is F_q-linear independence of the rows `F_r` in the
packet field.  If `m | q-1`, the K-character DFT is available over F_q:

    G_s = sum_r zeta_m^(s*r) F_r.

The DFT is invertible, so the row rank of the `G_s` equals the row rank of the
`F_r`.  This scan separates two notions:

* character support: every `G_s` is nonzero;
* character rank: the `G_s` are linearly independent.

The point is to check whether nonzero character resolvents are enough in small
CM packets, or whether the Moore/full-rank theorem is genuinely stronger.
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
from l1_axis_injectivity_scan import coeff_vector, rank_mod_q


@dataclass(frozen=True)
class KCharacterRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    origin_shift: int
    full_k_rank: int
    dimension_possible: bool
    character_rank: int
    zero_character_count: int
    all_characters_nonzero: bool
    rank_defect_with_full_character_support: bool


def primitive_root_of_order(q: int, order: int) -> int | None:
    if (q - 1) % order:
        return None
    root = pow(sp.primitive_root(q), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        return None
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            return None
    return int(root)


def dft_rows(residues: list[sp.Poly], zeta: int, q: int, factor: sp.Poly) -> list[sp.Poly]:
    rows: list[sp.Poly] = []
    x = factor.gens[0]
    for s in range(len(residues)):
        total = sp.Poly(0, x, modulus=q)
        for r, residue in enumerate(residues):
            coeff = pow(zeta, s * r, q)
            if coeff:
                total += coeff * residue
        rows.append(total.rem(factor))
    return rows


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> KCharacterRow:
    h = len(cycle)
    n = h // m
    zeta = primitive_root_of_order(q, m)
    if zeta is None:
        raise ValueError("K roots of unity are not in the base field")
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    full_rank = rank_mod_q(residue_vectors, q)
    transformed = dft_rows(residues, zeta, q, factor)
    transformed_vectors = [
        coeff_vector(row, factor.degree(), q)
        for row in transformed
    ]
    character_rank = rank_mod_q(transformed_vectors, q)
    if character_rank != full_rank:
        raise AssertionError("DFT rank should match full K rank")
    zero_count = sum(row.is_zero for row in transformed)
    all_nonzero = zero_count == 0
    return KCharacterRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        origin_shift=origin_shift,
        full_k_rank=full_rank,
        dimension_possible=factor.degree() >= m,
        character_rank=character_rank,
        zero_character_count=zero_count,
        all_characters_nonzero=all_nonzero,
        rank_defect_with_full_character_support=all_nonzero and full_rank < m,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[KCharacterRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[KCharacterRow] = []
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
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    if (q - 1) % m:
                        continue
                    n = h // m
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        rows.append(audit_packet(D, q, ell, shifted, m, factor, shift))
                        case_had_cycle = True
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--max-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=8)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    rank_defects = [row for row in rows if row.full_k_rank < row.m]
    dimension_possible_rows = [row for row in rows if row.dimension_possible]
    dimension_bound_rows = [row for row in rows if not row.dimension_possible]
    possible_rank_defects = [
        row for row in rank_defects if row.dimension_possible
    ]
    zero_character_rows = [row for row in rows if row.zero_character_count]
    support_not_rank = [
        row for row in rows if row.rank_defect_with_full_character_support
    ]
    possible_support_not_rank = [
        row for row in support_not_rank if row.dimension_possible
    ]
    full_rank_rows = [row for row in rows if row.full_k_rank == row.m]
    support_hist: dict[int, int] = {}
    for row in rows:
        support = row.m - row.zero_character_count
        support_hist[support] = support_hist.get(support, 0) + 1

    print("K-character rank split scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"max_m={args.max_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg origin dim_possible rank zero_chars "
            "all_nonzero support_not_rank"
        )
        display = support_not_rank + zero_character_rows + rank_defects
        if not display:
            display = rows[:40]
        for row in display[:80]:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} origin={row.origin_shift:3d} "
                f"dim_possible={int(row.dimension_possible)} "
                f"rank={row.full_k_rank:3d}/{row.m:3d} "
                f"zero_chars={row.zero_character_count:3d} "
                f"all_nonzero={int(row.all_characters_nonzero)} "
                f"support_not_rank={int(row.rank_defect_with_full_character_support)}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  dimension_possible_rows={len(dimension_possible_rows)}")
    print(f"  dimension_bound_rows={len(dimension_bound_rows)}")
    print(f"  full_rank_rows={len(full_rank_rows)}")
    print(f"  rank_defect_rows={len(rank_defects)}")
    print(f"  dimension_possible_rank_defect_rows={len(possible_rank_defects)}")
    print(f"  zero_character_rows={len(zero_character_rows)}")
    print(f"  rank_defect_with_full_character_support_rows={len(support_not_rank)}")
    print(
        "  dimension_possible_rank_defect_with_full_character_support_rows="
        f"{len(possible_support_not_rank)}"
    )
    print(f"  character_support_histogram={dict(sorted(support_hist.items()))}")
    print()
    print("interpretation")
    print("  k_roots_in_base_field_required=1")
    print("  dft_preserves_full_k_rank=1")
    print("  full_character_support_does_not_necessarily_imply_full_rank_if_support_not_rank_rows_nonzero=1")
    print("conclusion=reported_k_character_rank_split_scan")


if __name__ == "__main__":
    main()
