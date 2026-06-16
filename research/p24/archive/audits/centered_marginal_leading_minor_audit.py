#!/usr/bin/env python3
"""Audit leading square minors of centered Hermitian CRT marginals.

The centered-profile theorem reduces the p24 mixed block to the base-field
rank condition for

    C(a,b) = M(a,b) - M(a,0) - M(0,b) + M(0,0),
    1 <= a < left, 1 <= b < right.

For p24, a sufficient certificate is that the leading `156 x 156` square
minor of the `left=157, right=211` matrix `C` is nonzero modulo p.  This
script tests the analogous leading-minor statement on small actual-CM rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
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
class PairMinor:
    left: int
    right: int
    rows: int
    cols: int
    rank: int
    leading_applicable: bool
    leading_rank: int
    leading_det: int | None
    consecutive_windows: int
    consecutive_full_windows: int
    first_full_window: int | None


@dataclass(frozen=True)
class MinorRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    components: tuple[int, ...]
    pairs: tuple[PairMinor, ...]


def det_mod(matrix: list[list[int]], q: int) -> int:
    """Determinant modulo q by Gaussian elimination."""

    if not matrix:
        return 1
    rows = len(matrix)
    cols = len(matrix[0])
    if rows != cols:
        raise ValueError("det_mod expects a square matrix")
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(cols):
        pivot = None
        for row in range(col, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = (det * pivot_value) % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, rows):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det % q


def column_window(matrix: list[list[int]], start: int, width: int) -> list[list[int]]:
    return [row[start : start + width] for row in matrix]


def audit_pair(centered: list[list[int]], left: int, right: int, q: int) -> PairMinor:
    rows = len(centered)
    cols = len(centered[0]) if rows else 0
    rank = rank_mod_q(centered, q)
    width = left - 1
    leading_applicable = cols >= width and rows == width
    leading_rank = -1
    leading_det: int | None = None
    consecutive_windows = 0
    consecutive_full_windows = 0
    first_full_window: int | None = None
    if leading_applicable:
        leading = column_window(centered, 0, width)
        leading_rank = rank_mod_q(leading, q)
        leading_det = det_mod(leading, q)
        consecutive_windows = cols - width + 1
        for start in range(consecutive_windows):
            det = det_mod(column_window(centered, start, width), q)
            if det:
                consecutive_full_windows += 1
                if first_full_window is None:
                    first_full_window = start
    return PairMinor(
        left=left,
        right=right,
        rows=rows,
        cols=cols,
        rank=rank,
        leading_applicable=leading_applicable,
        leading_rank=leading_rank,
        leading_det=leading_det,
        consecutive_windows=consecutive_windows,
        consecutive_full_windows=consecutive_full_windows,
        first_full_window=first_full_window,
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
) -> MinorRow | None:
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
    pairs: list[PairMinor] = []
    for left in components:
        if left <= 2:
            continue
        for right in components:
            if right <= 2:
                continue
            marginal = double_marginal(kernel, left, right, q)
            centered = centered_double_marginal(marginal, q)
            pairs.append(audit_pair(centered, left, right, q))
    if not pairs:
        return None
    return MinorRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        components=components,
        pairs=tuple(pairs),
    )


def scan(args: argparse.Namespace) -> list[MinorRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[MinorRow] = []
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
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and len([c for c in coprime_components(m) if c > 2]) >= 2
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
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
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


def format_pair(pair: PairMinor) -> str:
    leading = (
        f"lead_rank{pair.leading_rank}:lead_det{pair.leading_det}"
        if pair.leading_applicable
        else "lead_na"
    )
    windows = (
        f"windows{pair.consecutive_full_windows}/{pair.consecutive_windows}"
        f":first{pair.first_full_window}"
        if pair.leading_applicable
        else "windows_na"
    )
    return (
        f"({pair.left},{pair.right}):shape{pair.rows}x{pair.cols}"
        f":rank{pair.rank}:{leading}:{windows}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-cases", type=int, default=20)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=200000)
    parser.add_argument("--max-prime-quotients", type=int, default=24)
    parser.add_argument("--max-composite-quotients", type=int, default=80)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=1_000_000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=160)
    parser.add_argument("--max-m", type=int, default=420)
    parser.add_argument("--max-factor-degree", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    rows = scan(args)
    pairs = [pair for row in rows for pair in row.pairs]
    applicable = [pair for pair in pairs if pair.leading_applicable]
    full_rank = [pair for pair in applicable if pair.rank == pair.rows]
    leading_full = [
        pair for pair in applicable if pair.leading_rank == pair.rows
    ]
    print("Centered marginal leading-minor audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"origin_shift={args.origin_shift}")
    print(
        "basis=C(a,b), 1<=a<left, 1<=b<right; "
        "leading minor uses b=1..left-1"
    )
    print()
    for row in rows:
        print(
            f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} h={row.h:4d} "
            f"m={row.m:4d} n={row.n:4d} deg={row.factor_degree:4d} "
            f"comps={list(row.components)} pairs="
            + ",".join(format_pair(pair) for pair in row.pairs)
        )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  pairs={len(pairs)}")
    print(f"  leading_applicable_pairs={len(applicable)}")
    print(f"  full_rank_applicable_pairs={len(full_rank)}")
    print(f"  leading_full_pairs={len(leading_full)}")
    print(
        "  full_rank_but_leading_zero_pairs="
        f"{sum(1 for pair in full_rank if pair.leading_rank < pair.rows)}"
    )
    if applicable:
        print(
            "  max_consecutive_full_window_count="
            f"{max(pair.consecutive_full_windows for pair in applicable)}"
        )
    print("conclusion=reported_centered_marginal_leading_minor_audit")


if __name__ == "__main__":
    main()
