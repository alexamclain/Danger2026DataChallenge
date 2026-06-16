#!/usr/bin/env python3
"""Function-complexity gate for low-moment relative traces.

The low-moment route asks for a few power sums of each child fiber:

    P_d(u) = sum_v Y_{u+a v}^d.

This script records two facts on small embedded CM towers:

1. P_1(u) is tautologically the parent period Z_u.  It is not a new producer
   datum once the selected parent root is known.
2. The higher moments P_d, d >= 2, do not generally look like low-degree
   functions of Z_u or low-complexity sequences in u.  Thus the useful
   simplification is "two moments are free" in p24, not "higher moments have
   an obvious small parent-period formula."
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from cypari2 import Pari

from cycle_period_complexity_scan import (
    bm_linear_complexity,
    dft_support,
    find_full_cycle_prime,
    find_splitting_prime,
    period_sequence,
)


PINNED_D = -5000


@dataclass(frozen=True)
class MomentRow:
    D: int
    q: int
    ell: int
    h: int
    parent_count: int
    child_factor: int
    quotient_size: int
    moment_degree: int
    p1_parent_identity: bool
    parent_distinct: bool
    interp_degree: int | None
    full_interp_degree: int
    bm_complexity: int
    dft_support_size: int | None


def divisors(n: int) -> list[int]:
    out: list[int] = []
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def interpolate_degree(xs: list[int], ys: list[int], q: int) -> int:
    """Return degree of the unique polynomial through distinct xs."""
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


def moment_values(
    fine_periods: list[int],
    parent_count: int,
    child_factor: int,
    degree: int,
    q: int,
) -> list[int]:
    return [
        sum(
            pow(fine_periods[parent + parent_count * v], degree, q)
            for v in range(child_factor)
        )
        % q
        for parent in range(parent_count)
    ]


def candidate_refinements(
    h: int,
    min_parent: int,
    max_parent: int,
    min_child: int,
    max_child: int,
    max_quotient: int,
) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for quotient_size in divisors(h):
        if quotient_size >= h or quotient_size > max_quotient:
            continue
        for child_factor in divisors(quotient_size):
            if child_factor <= 1 or child_factor == quotient_size:
                continue
            parent_count = quotient_size // child_factor
            if not (min_parent <= parent_count <= max_parent):
                continue
            if not (min_child <= child_factor <= max_child):
                continue
            out.append((parent_count, child_factor))
    return sorted(set(out), key=lambda row: (row[0] * row[1], row[0], row[1]))


def discriminant_stream(max_abs_D: int) -> list[int]:
    return [PINNED_D] + [
        D
        for D in range(-200, -max_abs_D - 1, -1)
        if D != PINNED_D and D % 4 in (0, 1)
    ]


def audit_refinement(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    parent_count: int,
    child_factor: int,
    max_moment_degree: int,
) -> list[MomentRow]:
    h = len(cycle)
    quotient_size = parent_count * child_factor
    parents = period_sequence(cycle, parent_count, q)
    fine = period_sequence(cycle, quotient_size, q)
    p1_values = moment_values(fine, parent_count, child_factor, 1, q)
    p1_identity = p1_values == parents
    parent_distinct = len(set(parents)) == parent_count
    rows: list[MomentRow] = []
    for degree in range(1, max_moment_degree + 1):
        values = moment_values(fine, parent_count, child_factor, degree, q)
        interp = (
            interpolate_degree(parents, values, q)
            if parent_distinct
            else None
        )
        rows.append(
            MomentRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                parent_count=parent_count,
                child_factor=child_factor,
                quotient_size=quotient_size,
                moment_degree=degree,
                p1_parent_identity=p1_identity,
                parent_distinct=parent_distinct,
                interp_degree=interp,
                full_interp_degree=parent_count - 1,
                bm_complexity=bm_linear_complexity(values * 2, q),
                dft_support_size=dft_support(values, q),
            )
        )
    return rows


def scan(args: argparse.Namespace) -> list[MomentRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[MomentRow] = []
    cases = 0
    seen: set[int] = set()
    for D in discriminant_stream(args.max_abs_D):
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
        full = find_full_cycle_prime(roots, D, q, args.ell_bound)
        if full is None:
            continue
        ell, cycle = full
        refinements = candidate_refinements(
            h,
            args.min_parent,
            args.max_parent,
            args.min_child,
            args.max_child,
            args.max_quotient,
        )
        if not refinements:
            continue
        for parent_count, child_factor in refinements[: args.max_refinements_per_case]:
            rows.extend(
                audit_refinement(
                    D,
                    q,
                    ell,
                    cycle,
                    parent_count,
                    child_factor,
                    args.max_moment_degree,
                )
            )
        cases += 1
        if cases >= args.max_cases:
            break
    return rows


def fmt_optional(value: int | None) -> str:
    return "NA" if value is None else str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=10)
    parser.add_argument("--min-h", type=int, default=6)
    parser.add_argument("--max-h", type=int, default=90)
    parser.add_argument("--max-abs-D", type=int, default=15000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=6000)
    parser.add_argument("--ell-bound", type=int, default=43)
    parser.add_argument("--min-parent", type=int, default=2)
    parser.add_argument("--max-parent", type=int, default=30)
    parser.add_argument("--min-child", type=int, default=2)
    parser.add_argument("--max-child", type=int, default=12)
    parser.add_argument("--max-quotient", type=int, default=60)
    parser.add_argument("--max-refinements-per-case", type=int, default=6)
    parser.add_argument("--max-moment-degree", type=int, default=5)
    args = parser.parse_args()

    rows = scan(args)
    nontrivial = [row for row in rows if row.moment_degree >= 2]
    nontrivial_parent_ge3 = [
        row for row in nontrivial if row.parent_count >= 3
    ]
    p1_ok = [row for row in rows if row.moment_degree == 1 and row.p1_parent_identity]
    p1_total = [row for row in rows if row.moment_degree == 1]
    full_nontrivial = [
        row
        for row in nontrivial
        if row.interp_degree == row.full_interp_degree
    ]
    low_nontrivial = [
        row
        for row in nontrivial
        if row.interp_degree is not None
        and row.interp_degree <= max(1, row.full_interp_degree // 2)
    ]
    low_nontrivial_parent_ge3 = [
        row
        for row in nontrivial_parent_ge3
        if row.interp_degree is not None
        and row.interp_degree <= max(1, row.full_interp_degree // 2)
    ]
    high_bm_nontrivial = [
        row
        for row in nontrivial
        if row.bm_complexity >= max(1, row.parent_count - 1)
    ]

    print("trace-GCD low-moment function-complexity gate")
    print(f"rows={len(rows)}")
    print(f"p1_parent_identity_rows={len(p1_ok)}/{len(p1_total)}")
    print(f"nontrivial_moment_rows={len(nontrivial)}")
    print(f"nontrivial_parent_ge3_rows={len(nontrivial_parent_ge3)}")
    print(f"nontrivial_full_interp_rows={len(full_nontrivial)}")
    print(f"nontrivial_low_interp_rows={len(low_nontrivial)}")
    print(f"nontrivial_parent_ge3_low_interp_rows={len(low_nontrivial_parent_ge3)}")
    print(f"nontrivial_high_bm_rows={len(high_bm_nontrivial)}")
    print()
    print(
        "columns: D q ell h a b d P1=parent parent_distinct "
        "interp/full bm dft_support"
    )
    for row in rows:
        dft_text = fmt_optional(row.dft_support_size)
        interp_text = fmt_optional(row.interp_degree)
        print(
            f"D={row.D:6d} q={row.q:5d} ell={row.ell:2d} h={row.h:3d} "
            f"a={row.parent_count:2d} b={row.child_factor:2d} "
            f"d={row.moment_degree:2d} P1={int(row.p1_parent_identity)} "
            f"parent_distinct={int(row.parent_distinct)} "
            f"interp={interp_text:>2s}/{row.full_interp_degree:<2d} "
            f"bm={row.bm_complexity:2d} dft={dft_text}"
        )
    print()
    print("p24_consequence")
    print("  p24_first_layer_nominal_low_moments=4")
    print("  p24_first_layer_nontrivial_low_moments=3")
    print("  p24_second_layer_nominal_low_moments=26")
    print("  p24_second_layer_nontrivial_low_moments=25")
    print("  p24_selected_path_nominal_low_moments=30")
    print("  p24_selected_path_nontrivial_new_low_moments=28")
    print()
    print("interpretation")
    print("  first_relative_trace_power_sum_is_the_parent_period=1")
    print("  p24_low_moment_payload_has_two_automatic_P1_values=1")
    print("  higher_relative_trace_moments_do_not_show_a_generic_low_degree_parent_formula=1")
    print("  producer_must_construct_nontrivial_higher_moments_by_class_field_or_trace_formula=1")
    print("conclusion=reported_trace_gcd_low_moment_function_complexity_gate")

    if not rows:
        raise SystemExit(1)
    if len(p1_ok) != len(p1_total):
        raise SystemExit(1)
    if not nontrivial:
        raise SystemExit(1)
    if low_nontrivial_parent_ge3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
