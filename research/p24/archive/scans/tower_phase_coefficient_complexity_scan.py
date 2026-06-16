#!/usr/bin/env python3
"""Coefficient-complexity scan for embedded tower phase refinements.

For a complete small CM cycle of length

    h = a * b * r,

form fine H-periods of quotient size ``a*b`` and recovery size ``r``.  Group
these fine periods into ``a`` parent periods, each with ``b`` children.  Above
each parent period ``Z_u`` there is a degree-``b`` child polynomial

    C_u(Y) = prod_v (Y - y_{u+a*v}).

The p24 tower dream needs these relative child polynomials for

    a = 2, then a = 314, b = 211.

This scan asks whether, in small CM data, the coefficients of ``C_u`` are
low-complexity functions of the parent period ``Z_u``.  Full interpolation
degree ``a-1`` means the relative phase relation is just a dense embedded
table at this scale; unexpectedly low degree would be a theorem candidate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import (
    bm_linear_complexity,
    find_full_cycle_prime,
    find_splitting_prime,
)
from embedded_decomposition_calibration import monic_poly_from_roots


@dataclass(frozen=True)
class ChainRow:
    D: int
    q: int
    ell: int
    h: int
    parent_count: int
    child_factor: int
    recovery_size: int
    parent_distinct: bool
    fine_distinct: bool
    max_interp_degree: int
    avg_interp_degree: float
    full_degree_coeffs: int
    coeff_slots: int
    informative_full_degree_coeffs: int
    informative_slots: int
    informative_low_degree_coeffs: int
    max_bm: int
    avg_bm: float
    low_degree_coeffs: int
    low_bm_coeffs: int


def divisors_between(n: int, lo: int, hi: int) -> list[int]:
    return [int(d) for d in sp.divisors(n) if lo <= d <= hi]


def interpolate_degree(xs: list[int], ys: list[int], q: int) -> int:
    """Return the degree of the unique polynomial through distinct xs."""
    n = len(xs)
    coeffs = [0] * n
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        numerator = [1]
        denominator = 1
        for j, xj in enumerate(xs):
            if i == j:
                continue
            new = [0] * (len(numerator) + 1)
            for k, coeff in enumerate(numerator):
                new[k] = (new[k] - coeff * xj) % q
                new[k + 1] = (new[k + 1] + coeff) % q
            numerator = new
            denominator = denominator * ((xi - xj) % q) % q
        scale = yi * pow(denominator, -1, q) % q
        for k, coeff in enumerate(numerator):
            coeffs[k] = (coeffs[k] + scale * coeff) % q
    for degree in range(n - 1, -1, -1):
        if coeffs[degree] % q:
            return degree
    return -1


def period(values: list[int], q: int) -> int:
    return sum(values) % q


def parent_periods(cycle: list[int], q: int, parent_count: int) -> list[int]:
    h = len(cycle)
    return [
        period([cycle[(u + parent_count * k) % h] for k in range(h // parent_count)], q)
        for u in range(parent_count)
    ]


def fine_periods(
    cycle: list[int],
    q: int,
    quotient_size: int,
    recovery_size: int,
) -> list[int]:
    h = len(cycle)
    return [
        period(
            [cycle[(w + quotient_size * k) % h] for k in range(recovery_size)],
            q,
        )
        for w in range(quotient_size)
    ]


def audit_chain(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    parent_count: int,
    child_factor: int,
) -> ChainRow:
    h = len(cycle)
    quotient_size = parent_count * child_factor
    recovery_size = h // quotient_size
    parents = parent_periods(cycle, q, parent_count)
    fine = fine_periods(cycle, q, quotient_size, recovery_size)

    child_polys: list[list[int]] = []
    for u in range(parent_count):
        children = [fine[u + parent_count * v] for v in range(child_factor)]
        child_polys.append(monic_poly_from_roots(children, q))

    degrees: list[int] = []
    bms: list[int] = []
    if len(set(parents)) == parent_count:
        for coeff_index in range(child_factor):
            coeff_values = [poly[coeff_index] for poly in child_polys]
            degrees.append(interpolate_degree(parents, coeff_values, q))
            bms.append(bm_linear_complexity(coeff_values * 2, q))

    full_degree = parent_count - 1
    low_degree_limit = max(0, parent_count // 2)
    low_bm_limit = max(1, parent_count // 2)
    informative = degrees[:-1] if degrees else []
    return ChainRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        parent_count=parent_count,
        child_factor=child_factor,
        recovery_size=recovery_size,
        parent_distinct=len(set(parents)) == parent_count,
        fine_distinct=len(set(fine)) == quotient_size,
        max_interp_degree=max(degrees, default=-1),
        avg_interp_degree=sum(degrees) / len(degrees) if degrees else -1,
        full_degree_coeffs=sum(degree == full_degree for degree in degrees),
        coeff_slots=len(degrees),
        informative_full_degree_coeffs=sum(
            degree == full_degree for degree in informative
        ),
        informative_slots=len(informative),
        informative_low_degree_coeffs=sum(
            degree <= low_degree_limit for degree in informative
        ),
        max_bm=max(bms, default=-1),
        avg_bm=sum(bms) / len(bms) if bms else -1,
        low_degree_coeffs=sum(degree <= low_degree_limit for degree in degrees),
        low_bm_coeffs=sum(bm <= low_bm_limit for bm in bms),
    )


def scan(args: argparse.Namespace) -> list[ChainRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -args.max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[ChainRow] = []
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
        if not (args.min_h <= h <= args.max_h):
            continue
        split = find_splitting_prime(pari, hilbert, h, args.q_start, args.q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        case_rows = 0
        for quotient_size in divisors_between(h, args.min_quotient, args.max_quotient):
            if quotient_size == h:
                continue
            recovery_size = h // quotient_size
            if recovery_size < args.min_recovery:
                continue
            for child_factor in divisors_between(quotient_size, args.min_child, args.max_child):
                if child_factor == quotient_size:
                    continue
                parent_count = quotient_size // child_factor
                if not (args.min_parent <= parent_count <= args.max_parent):
                    continue
                rows.append(
                    audit_chain(D, q, ell, cycle, parent_count, child_factor)
                )
                case_rows += 1
                if case_rows >= args.max_rows_per_case:
                    break
            if case_rows >= args.max_rows_per_case:
                break
        if case_rows:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def print_row(row: ChainRow) -> None:
    print(
        f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
        f"a={row.parent_count:3d} b={row.child_factor:3d} r={row.recovery_size:3d} "
        f"parent_distinct={int(row.parent_distinct)} fine_distinct={int(row.fine_distinct)} "
        f"max_deg={row.max_interp_degree:3d} avg_deg={row.avg_interp_degree:6.2f} "
        f"full_deg_coeffs={row.full_degree_coeffs:3d}/{row.coeff_slots:3d} "
        f"informative_full={row.informative_full_degree_coeffs:3d}/{row.informative_slots:3d} "
        f"max_bm={row.max_bm:3d} avg_bm={row.avg_bm:6.2f} "
        f"low_deg_coeffs={row.low_degree_coeffs:3d} low_bm_coeffs={row.low_bm_coeffs:3d}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=10)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--min-quotient", type=int, default=6)
    parser.add_argument("--max-quotient", type=int, default=80)
    parser.add_argument("--min-parent", type=int, default=3)
    parser.add_argument("--max-parent", type=int, default=40)
    parser.add_argument("--min-child", type=int, default=2)
    parser.add_argument("--max-child", type=int, default=13)
    parser.add_argument("--min-recovery", type=int, default=2)
    parser.add_argument("--max-rows-per-case", type=int, default=10)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    print("tower phase coefficient complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print()

    if not args.summary_only:
        print("columns: D q ell h a(parent) b(child) r(recovery) distinct flags coefficient degrees/BM")
        for row in rows:
            print_row(row)
        print()

    good = [row for row in rows if row.parent_distinct and row.fine_distinct]
    coeff_slots = sum(row.coeff_slots for row in good)
    full_coeffs = sum(row.full_degree_coeffs for row in good)
    informative_slots = sum(row.informative_slots for row in good)
    informative_full = sum(row.informative_full_degree_coeffs for row in good)
    informative_low = sum(row.informative_low_degree_coeffs for row in good)
    low_deg = sum(row.low_degree_coeffs for row in good)
    low_bm = sum(row.low_bm_coeffs for row in good)
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  good_distinct_rows={len(good)}")
    print(f"  coeff_slots={coeff_slots}")
    print(f"  full_degree_coeffs={full_coeffs}")
    print(f"  informative_coeff_slots={informative_slots}")
    print(f"  informative_full_degree_coeffs={informative_full}")
    print(f"  informative_low_degree_coeffs={informative_low}")
    print(f"  low_degree_coeffs={low_deg}")
    print(f"  low_bm_coeffs={low_bm}")
    print(
        "  max_interp_degree_seen="
        f"{max((row.max_interp_degree for row in good), default=-1)}"
    )
    print(
        "  avg_interp_degree_over_rows="
        f"{sum(row.avg_interp_degree for row in good) / len(good) if good else -1:.6f}"
    )
    print()
    print("interpretation")
    print("  coefficient_of_Y_to_child_minus_1_is_forced_to_be_minus_parent_period=1")
    print("  low_degree_coefficients_would_support_formulaic_relative_phase=1")
    print("  full_degree_coefficients_mean_dense_parent_phase_table_at_toy_scale=1")
    print(
        "conclusion=reported_tower_phase_coefficient_complexity_scan"
    )


if __name__ == "__main__":
    main()
