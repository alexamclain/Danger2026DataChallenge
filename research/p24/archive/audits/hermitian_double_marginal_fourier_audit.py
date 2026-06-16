#!/usr/bin/env python3
"""Fourier audit for centered Hermitian CRT double marginals.

The centered double marginal for components c,d is a trace-zero matrix on
residue classes.  After adjoining the c- and d-th roots of unity, its rank is
equivalent to the rank of the nonzero-frequency double DFT:

    H(u,v) = sum_{a mod c, b mod d} zeta_c^(u a) zeta_d^(v b) M(a,b),
    1 <= u < c, 1 <= v < d.

This is the character-pairing form of the Hermitian Schur correction.  It
does not prove p-unitness, but it turns the centered CRT marginal theorem into
a mixed K-character pairing theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class FourierPairRank:
    left: int
    right: int
    centered_rank_base: int
    centered_rank_extension: int
    nonzero_dft_rank: int
    rank_match: bool


@dataclass(frozen=True)
class FourierRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    components: tuple[int, ...]
    pair_ranks: tuple[FourierPairRank, ...]


def embed_matrix(matrix: list[list[int]], field: ExtensionField):
    return [[field.embed(value) for value in row] for row in matrix]


def dft_double_marginal(
    marginal: list[list[int]],
    left: int,
    right: int,
    zeta_powers,
    m: int,
    field: ExtensionField,
):
    step_left = m // left
    step_right = m // right
    rows = []
    for u in range(1, left):
        row = []
        for v in range(1, right):
            total = field.zero
            for a in range(left):
                left_weight = zeta_powers[(u * step_left * a) % m]
                for b in range(right):
                    coeff = field.mul(
                        left_weight,
                        zeta_powers[(v * step_right * b) % m],
                    )
                    total = field.add(
                        total,
                        field.mul(coeff, field.embed(marginal[a][b])),
                    )
            row.append(total)
        rows.append(row)
    return rows


def zeta_powers(zeta, m: int, field: ExtensionField):
    powers = [field.one]
    for _ in range(1, m):
        powers.append(field.mul(powers[-1], zeta))
    return powers


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> FourierRow | None:
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
    kernel = kernel_matrix(residues, factor, q)
    components = coprime_components(m)
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    powers = zeta_powers(zeta, m, field)

    pair_ranks: list[FourierPairRank] = []
    for left in components:
        for right in components:
            marginal = double_marginal(kernel, left, right, q)
            centered = centered_double_marginal(marginal, q)
            centered_rank_base = rank_mod_q(centered, q)
            centered_rank_extension = rank_over_extension(embed_matrix(centered, field), field)
            dft_matrix = dft_double_marginal(
                marginal,
                left,
                right,
                powers,
                m,
                field,
            )
            nonzero_dft_rank = rank_over_extension(dft_matrix, field)
            pair_ranks.append(
                FourierPairRank(
                    left=left,
                    right=right,
                    centered_rank_base=centered_rank_base,
                    centered_rank_extension=centered_rank_extension,
                    nonzero_dft_rank=nonzero_dft_rank,
                    rank_match=(
                        centered_rank_base
                        == centered_rank_extension
                        == nonzero_dft_rank
                    ),
                )
            )

    return FourierRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        components=components,
        pair_ranks=tuple(pair_ranks),
    )


def scan(args: argparse.Namespace) -> list[FourierRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[FourierRow] = []
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
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    row = audit_packet(D, q, ell, shifted, m, factor, args.seed)
                    if row is not None:
                        rows.append(row)
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def pair_summary(row: FourierRow) -> str:
    return ",".join(
        f"({pair.left},{pair.right}):base{pair.centered_rank_base}"
        f"/ext{pair.centered_rank_extension}/dft{pair.nonzero_dft_rank}"
        f":match{int(pair.rank_match)}"
        for pair in row.pair_ranks
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-cases", type=int, default=20)
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
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    mismatches = [
        pair for row in rows for pair in row.pair_ranks if not pair.rank_match
    ]
    print("Hermitian double-marginal Fourier audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext comps "
            "pair_ranks=(c,d):base/ext/dft:match"
        )
        for row in rows[:80]:
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} ext={row.extension_degree:2d} "
                f"comps={list(row.components)} pair_ranks={pair_summary(row)}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  pair_blocks={sum(len(row.pair_ranks) for row in rows)}")
    print(f"  rank_mismatches={len(mismatches)}")
    if rows:
        print(f"  max_extension_degree={max(row.extension_degree for row in rows)}")
        print(
            "  max_nonzero_dft_rank="
            f"{max(pair.nonzero_dft_rank for row in rows for pair in row.pair_ranks)}"
        )
    print()
    print("interpretation")
    print("  zero_mismatches_confirms_centered_marginal_rank_equals_nonzero_DFT_rank=1")
    print("  nonzero_DFT_entries_are_mixed_K_character_pairings=1")
    print("  p24_schur_correction_can_be_stated_as_character_pairing_punit=1")
    print("conclusion=reported_hermitian_double_marginal_fourier_audit")


if __name__ == "__main__":
    main()
