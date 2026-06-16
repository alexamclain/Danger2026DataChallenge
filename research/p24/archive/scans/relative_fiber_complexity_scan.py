#!/usr/bin/env python3
"""Linear-complexity diagnostics for relative fibers.

The augmentation determinant

    Res(Phi_n, J_u)

could be computable without enumerating an order-n fiber if the sequence

    j_u, j_{u+m}, ..., j_{u+m(n-1)}

had a short linear recurrence.  This scan measures Berlekamp-Massey complexity
of those fibers in small CM cycles and records primitive packet vanishings on
the same rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from cypari2 import Pari

from cycle_period_complexity_scan import (
    bm_linear_complexity,
    find_full_cycle_prime,
    find_splitting_prime,
)
from packetized_relative_content_scan import fiber_polynomials, packet_factors
from relative_normality_prime_composite_scan import quotient_sizes_any, rotate


@dataclass(frozen=True)
class FiberComplexityRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    shift: int
    u: int
    bm: int
    distinct: int
    primitive_zero_count: int


def primitive_zero_count(cycle: list[int], q: int, m: int, u: int) -> int:
    fibers = fiber_polynomials(cycle, q, m)
    return sum(
        fibers[u].rem(factor).is_zero
        for factor in packet_factors(len(cycle) // m, q)
        if factor.degree() > 0
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
) -> list[FiberComplexityRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[FiberComplexityRow] = []
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
            n = h // m
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for u in range(m):
                    values = [shifted[u + m * k] % q for k in range(n)]
                    rows.append(
                        FiberComplexityRow(
                            D=D,
                            q=q,
                            ell=ell,
                            h=h,
                            m=m,
                            n=n,
                            n_is_prime=all(n % d for d in range(2, int(n**0.5) + 1)),
                            shift=shift,
                            u=u,
                            bm=bm_linear_complexity(values * 2, q),
                            distinct=len(set(values)),
                            primitive_zero_count=primitive_zero_count(shifted, q, m, u),
                        )
                    )
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
    ap.add_argument("--max-shifts", type=int, default=4)
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

    print("relative fiber complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"max_n={args.max_n}")
    print(f"q_stop={args.q_stop}")
    print(f"max_shifts={args.max_shifts}")
    print()

    low_threshold = lambda n: n // 2
    interesting = [
        row for row in rows
        if row.bm <= low_threshold(row.n) or row.primitive_zero_count
    ]
    if not args.summary_only:
        print("columns: D q ell h m n n_prime shift u bm bm_over_n distinct primitive_zero_count")
        for row in interesting:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                f"shift={row.shift:3d} u={row.u:3d} bm={row.bm:3d} "
                f"bm_over_n={row.bm / row.n:5.2f} distinct={row.distinct:3d} "
                f"primitive_zero_count={row.primitive_zero_count:2d}"
            )

    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    print()
    print("summary")
    print(f"  fiber_rows={len(rows)}")
    print(f"  prime_fiber_rows={len(prime_rows)}")
    print(f"  composite_fiber_rows={len(composite_rows)}")
    print(f"  prime_full_or_near_full_bm={sum(row.bm >= row.n - 1 for row in prime_rows)}")
    print(f"  composite_full_or_near_full_bm={sum(row.bm >= row.n - 1 for row in composite_rows)}")
    print(f"  prime_low_bm={sum(row.bm <= low_threshold(row.n) for row in prime_rows)}")
    print(f"  composite_low_bm={sum(row.bm <= low_threshold(row.n) for row in composite_rows)}")
    print(f"  prime_primitive_zero_fibers={sum(row.primitive_zero_count > 0 for row in prime_rows)}")
    print(f"  composite_primitive_zero_fibers={sum(row.primitive_zero_count > 0 for row in composite_rows)}")
    print(f"  min_prime_bm_over_n={min((row.bm / row.n for row in prime_rows), default=0):.6f}")
    print(f"  min_composite_bm_over_n={min((row.bm / row.n for row in composite_rows), default=0):.6f}")
    print()
    print("interpretation")
    print("  low_bm_fiber_would_support_fast_resultant_compression=1")
    print("  full_bm_fibers_keep_augmentation_determinant_high_order=1")
    print("conclusion=reported_relative_fiber_complexity_scan")


if __name__ == "__main__":
    main()
