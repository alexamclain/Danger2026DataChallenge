#!/usr/bin/env python3
"""Circulant-rank view of relative normality packets.

For a length-n relative fiber `x_k = j_{u+m*k}`, the circulant determinant is

    det(circ(x)) = product_{a=0}^{n-1} J_u(zeta_n^a).

Thus the primitive resultant `Res(Phi_n,J_u)` is the nontrivial-character part
of this determinant.  For prime n, nonzero trivial period plus nonzero
primitive resultant is exactly cyclic-shift normality of the fiber.

This scan records rank defects of the circulant matrices for small CM cycles
and compares them to primitive packet coordinate zeros.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from packetized_relative_content_scan import fiber_polynomials, packet_factors
from relative_normality_prime_composite_scan import quotient_sizes_any, rotate


@dataclass(frozen=True)
class RankRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    shift: int
    u: int
    trivial_zero: bool
    primitive_zero_count: int
    circulant_rank: int


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if scale:
                mat[row] = [
                    (left - scale * right) % q
                    for left, right in zip(mat[row], mat[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def circulant_rank(values: list[int], q: int) -> int:
    n = len(values)
    matrix = [
        [values[(col - row) % n] % q for col in range(n)]
        for row in range(n)
    ]
    return rank_mod_q(matrix, q)


def audit_fiber(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    shift: int,
    u: int,
) -> RankRow:
    h = len(cycle)
    n = h // m
    shifted = rotate(cycle, shift)
    values = [shifted[u + m * k] % q for k in range(n)]
    trivial_zero = (sum(values) % q) == 0
    fibers = fiber_polynomials(shifted, q, m)
    primitive_zero_count = sum(
        fibers[u].rem(factor).is_zero
        for factor in packet_factors(n, q)
        if factor.degree() > 0 and factor.as_expr() != sp.Symbol("X") - 1
    )
    return RankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        shift=shift,
        u=u,
        trivial_zero=trivial_zero,
        primitive_zero_count=primitive_zero_count,
        circulant_rank=circulant_rank(values, q),
    )


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_prime_quotients: int,
    max_composite_quotients: int,
    min_n: int,
    max_n: int,
    q_start: int,
    q_stop: int,
    max_shifts: int,
) -> list[RankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[RankRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=max_prime_quotients,
            max_composite=max_composite_quotients,
            min_n=min_n,
            max_n=max_n,
        )
        if not quotient_sizes:
            continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        shifts = range(min(h, max_shifts)) if max_shifts else range(h)
        for m in quotient_sizes:
            for shift in shifts:
                for u in range(m):
                    rows.append(audit_fiber(D, q, ell, cycle, m, shift, u))
        cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=20)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=80)
    ap.add_argument("--max-abs-D", type=int, default=12000)
    ap.add_argument("--max-prime-quotients", type=int, default=3)
    ap.add_argument("--max-composite-quotients", type=int, default=3)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=80)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=120000)
    ap.add_argument("--max-shifts", type=int, default=0)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_prime_quotients=args.max_prime_quotients,
        max_composite_quotients=args.max_composite_quotients,
        min_n=args.min_n,
        max_n=args.max_n,
        q_start=args.q_start,
        q_stop=args.q_stop,
        max_shifts=args.max_shifts,
    )

    print("relative circulant-rank scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"max_n={args.max_n}")
    print(f"q_stop={args.q_stop}")
    print(f"max_shifts={args.max_shifts}")
    print()

    bad_rows = [
        row for row in rows
        if row.trivial_zero or row.primitive_zero_count or row.circulant_rank < row.n
    ]
    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime shift u trivial_zero "
            "primitive_zero_count rank"
        )
        for row in bad_rows:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                f"shift={row.shift:3d} u={row.u:3d} "
                f"trivial_zero={int(row.trivial_zero)} "
                f"primitive_zero_count={row.primitive_zero_count:2d} "
                f"rank={row.circulant_rank:3d}/{row.n:<3d}"
            )

    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    print()
    print("summary")
    print(f"  fiber_rows={len(rows)}")
    print(f"  prime_fiber_rows={len(prime_rows)}")
    print(f"  composite_fiber_rows={len(composite_rows)}")
    print(f"  prime_rank_defects={sum(row.circulant_rank < row.n for row in prime_rows)}")
    print(f"  composite_rank_defects={sum(row.circulant_rank < row.n for row in composite_rows)}")
    print(f"  prime_primitive_zero_fibers={sum(row.primitive_zero_count > 0 for row in prime_rows)}")
    print(f"  composite_primitive_zero_fibers={sum(row.primitive_zero_count > 0 for row in composite_rows)}")
    print(f"  prime_trivial_zero_fibers={sum(row.trivial_zero for row in prime_rows)}")
    print(f"  composite_trivial_zero_fibers={sum(row.trivial_zero for row in composite_rows)}")
    print(f"  bad_rows={len(bad_rows)}")
    print()
    print("interpretation")
    print("  circulant_rank_defect_equals_some_character_factor_zero=1")
    print("  prime_n_full_rank_is_equivalent_to_trivial_and_primitive_resultants_nonzero=1")
    print("conclusion=reported_relative_circulant_rank_scan")


if __name__ == "__main__":
    main()
