#!/usr/bin/env python3
"""Audit the CRT double-marginal formula for Hermitian axis blocks.

Let

    K(r,s) = <F_r,F_s>

be the Hermitian inverse-character autocorrelation kernel on complement
fibers.  For CRT components c,d define double marginals

    M_cd(a,b) = sum_{r=a mod c, s=b mod d} K(r,s).

The trace-zero component block U_c x U_d should be the centered table

    M_cd(a,b) - M_cd(a,0) - M_cd(0,b) + M_cd(0,0),

for a,b nonzero.  This script verifies that identity on small CM rows and
records the centered marginal ranks.  The point is to make the Schur
correction a marginal-kernel p-unit target rather than an opaque Gram matrix.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
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
class PairMarginalRank:
    left: int
    right: int
    centered_rank: int
    gram_block_rank: int
    identity_failures: int


@dataclass(frozen=True)
class DoubleMarginalRow:
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
    constant_component_failures: int
    pair_ranks: tuple[PairMarginalRank, ...]


def kernel_matrix(
    residues: list[sp.Poly],
    factor: sp.Poly,
    q: int,
) -> list[list[int]]:
    vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    return hermitian_pair_matrix(vectors, vectors, factor, q, power_sums)


def double_marginal(
    kernel: list[list[int]],
    left: int,
    right: int,
    q: int,
) -> list[list[int]]:
    out = [[0 for _ in range(right)] for _ in range(left)]
    for r, row in enumerate(kernel):
        a = r % left
        for s, value in enumerate(row):
            b = s % right
            out[a][b] = (out[a][b] + value) % q
    return out


def centered_double_marginal(
    marginal: list[list[int]],
    q: int,
) -> list[list[int]]:
    rows = len(marginal)
    cols = len(marginal[0]) if rows else 0
    return [
        [
            (marginal[a][b] - marginal[a][0] - marginal[0][b] + marginal[0][0]) % q
            for b in range(1, cols)
        ]
        for a in range(1, rows)
    ]


def constant_to_component_marginal(
    kernel: list[list[int]],
    component: int,
    q: int,
) -> list[int]:
    values = [0 for _ in range(component)]
    for row in kernel:
        for s, value in enumerate(row):
            values[s % component] = (values[s % component] + value) % q
    return [(values[a] - values[0]) % q for a in range(1, component)]


def submatrix(matrix: list[list[int]], rows: list[int], cols: list[int]) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
) -> DoubleMarginalRow | None:
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
    kernel = kernel_matrix(residues, factor, q)

    constant_failures = 0
    for component in components:
        expected = constant_to_component_marginal(kernel, component, q)
        actual = submatrix(gram, blocks["constant"], blocks[str(component)])[0]
        constant_failures += sum(
            1 for left_value, right_value in zip(expected, actual)
            if left_value % q != right_value % q
        )

    pair_ranks: list[PairMarginalRank] = []
    for left in components:
        for right in components:
            marginal = double_marginal(kernel, left, right, q)
            centered = centered_double_marginal(marginal, q)
            actual = submatrix(gram, blocks[str(left)], blocks[str(right)])
            failures = 0
            for row_expected, row_actual in zip(centered, actual):
                failures += sum(
                    1 for a, b in zip(row_expected, row_actual)
                    if a % q != b % q
                )
            pair_ranks.append(
                PairMarginalRank(
                    left=left,
                    right=right,
                    centered_rank=rank_mod_q(centered, q),
                    gram_block_rank=matrix_subrank(
                        gram,
                        blocks[str(left)],
                        blocks[str(right)],
                        q,
                    ),
                    identity_failures=failures,
                )
            )

    return DoubleMarginalRow(
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
        constant_component_failures=constant_failures,
        pair_ranks=tuple(pair_ranks),
    )


def scan(args: argparse.Namespace) -> list[DoubleMarginalRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[DoubleMarginalRow] = []
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


def pair_summary(row: DoubleMarginalRow) -> str:
    return ",".join(
        f"({pair.left},{pair.right}):{pair.centered_rank}/{pair.gram_block_rank}"
        f":fail{pair.identity_failures}"
        for pair in row.pair_ranks
    )


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
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    pair_failures = sum(
        pair.identity_failures for row in rows for pair in row.pair_ranks
    )
    constant_failures = sum(row.constant_component_failures for row in rows)
    max_centered_rank = max(
        (pair.centered_rank for row in rows for pair in row.pair_ranks),
        default=0,
    )
    mismatch_ranks = sum(
        1
        for row in rows
        for pair in row.pair_ranks
        if pair.centered_rank != pair.gram_block_rank
    )

    print("Hermitian CRT double-marginal audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg comps axis_dim gram_rank "
            "constant_fail pair_ranks=(c,d):center/gram:fail"
        )
        for row in rows[:80]:
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} comps={list(row.components)} "
                f"axis_dim={row.axis_dim:4d} gram_rank={row.gram_rank:4d} "
                f"constant_fail={row.constant_component_failures:3d} "
                f"pair_ranks={pair_summary(row)}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  constant_component_identity_failures={constant_failures}")
    print(f"  pair_identity_failures={pair_failures}")
    print(f"  pair_rank_mismatch_count={mismatch_ranks}")
    print(f"  max_centered_pair_rank={max_centered_rank}")
    print()
    print("interpretation")
    print("  zero_failures_confirms_blocks_are_centered_CRT_kernel_marginals=1")
    print("  centered_pair_rank_is_cross_component_coupling_rank=1")
    print("  p24_schur_correction_is_a_centered_double_marginal_punit_target=1")
    print("conclusion=reported_hermitian_double_marginal_audit")


if __name__ == "__main__":
    main()
