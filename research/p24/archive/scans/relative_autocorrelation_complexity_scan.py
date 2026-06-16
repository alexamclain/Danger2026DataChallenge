#!/usr/bin/env python3
"""Complexity scan for the relative autocorrelation sequence C_d.

The energy certificate rewrites the harmful test as a nonzero Fourier
coefficient of

    C_d = sum_i j_{i+m*d} j_i.

If C_d had low recurrence complexity along the recovery subgroup, the scalar
energy route might be computable without enumerating all n terms.  This scan
checks that hope on small complete CM cycles with all roots of unity in the
base field.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import (
    bm_linear_complexity,
    dft_support,
    find_full_cycle_prime,
)
from natural_relative_resolvent_scan import (
    find_splitting_prime_with_mu_h,
    quotient_sizes,
)


@dataclass(frozen=True)
class AutocorrelationRow:
    D: int
    q: int
    ell: int
    h: int
    quotient_size: int
    subgroup_size: int
    distinct: int
    bm: int
    dft_support: int | None
    energy_zero_count: int | None


def autocorrelation_sequence(cycle: list[int], q: int, m: int) -> list[int]:
    h = len(cycle)
    n = h // m
    out: list[int] = []
    for d in range(n):
        offset = m * d
        total = 0
        for i, value in enumerate(cycle):
            total = (total + value * cycle[(i + offset) % h]) % q
        out.append(total)
    return out


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_quotients: int,
    q_start: int,
    q_stop: int,
) -> list[AutocorrelationRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[AutocorrelationRow] = []
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
        split = find_splitting_prime_with_mu_h(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        case_rows = 0
        for m in quotient_sizes(h, max_quotients):
            n = h // m
            if n < 3:
                continue
            seq = autocorrelation_sequence(cycle, q, m)
            bm = bm_linear_complexity(seq * 2, q)
            support = dft_support(seq, q)
            zero_count = None if support is None else n - support
            rows.append(
                AutocorrelationRow(
                    D=D,
                    q=q,
                    ell=ell,
                    h=h,
                    quotient_size=m,
                    subgroup_size=n,
                    distinct=len(set(seq)),
                    bm=bm,
                    dft_support=support,
                    energy_zero_count=zero_count,
                )
            )
            case_rows += 1
        if case_rows:
            cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=40)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=96)
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--max-quotients", type=int, default=6)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=250000)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_quotients=args.max_quotients,
        q_start=args.q_start,
        q_stop=args.q_stop,
    )

    print("relative autocorrelation complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print("columns: D q ell h m n distinct bm bm_over_n dft_support energy_zeros")
        for row in rows:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.quotient_size:3d} n={row.subgroup_size:3d} "
                f"distinct={row.distinct:3d} bm={row.bm:3d} "
                f"bm_over_n={row.bm / row.subgroup_size:5.2f} "
                f"dft_support={'NA' if row.dft_support is None else row.dft_support:>3} "
                f"energy_zeros={'NA' if row.energy_zero_count is None else row.energy_zero_count}"
            )

    full_bm = sum(1 for row in rows if row.bm >= row.subgroup_size - 1)
    low_bm = sum(1 for row in rows if row.bm <= max(2, row.subgroup_size // 2))
    dft_rows = [row for row in rows if row.dft_support is not None]
    full_support = sum(1 for row in dft_rows if row.dft_support == row.subgroup_size)
    total_energy_zeros = sum(row.energy_zero_count or 0 for row in dft_rows)

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  full_or_near_full_bm_rows={full_bm}")
    print(f"  low_bm_rows={low_bm}")
    print(f"  dft_rows={len(dft_rows)}")
    print(f"  full_dft_support_rows={full_support}")
    print(f"  total_energy_zeros={total_energy_zeros}")
    print()
    print("interpretation")
    print("  low_bm_C_d_would_support_recurrence_compression_of_energy=1")
    print("  full_bm_and_full_dft_support_support_high_order_autocorrelation_barrier=1")
    print("  scan_is_toy_scale_and_not_a_p24_proof=1")
    print("conclusion=reported_relative_autocorrelation_complexity_scan")


if __name__ == "__main__":
    main()

