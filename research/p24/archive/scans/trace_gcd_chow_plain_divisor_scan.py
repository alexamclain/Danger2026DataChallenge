#!/usr/bin/env python3
"""Plain-j divisor diagnostic for the trace-GCD Chow determinant.

The trace-GCD p-unit target is the orbit Chow norm

    prod_t det(P V_t A).

This script tests the easiest divisor explanation on small actual-CM rows:
as the CM origin moves, is a selected tail-on-kernel determinant a low
complexity rational function of the plain CM root j_i?  A positive result
would be a useful Borcherds/modular-unit lead.  Generic interpolants do not
disprove a phase-aware divisor, but they do rule out the naive "it is already
a simple function of j" shortcut.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from l1_axis_injectivity_scan import discriminants
from lang_trace_gcd_origin_action_audit import OriginActionRow, audit_origin_row
from packet_scalar_divisor_shape_toy import (
    polynomial_degree,
    random_values_like,
    rational_degree,
)
from packet_scalar_edge_shape_scan import (
    first_polynomial_bidegree,
    first_rational_bidegree,
)
from packetized_relative_content_scan import packet_factors
from phase_divisor_heegner_support_scan import (
    heegner_roots,
    interpolant_roots,
    root_hits,
)
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any


@dataclass(frozen=True)
class RowWithCycle:
    row: OriginActionRow
    cycle: tuple[int, ...]


def first_row_with_cycle(args: argparse.Namespace) -> RowWithCycle | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    audit_args = argparse.Namespace(**vars(args))
    if args.all_omitted:
        audit_args.only_omitted = None
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
            and (args.only_m is None or m == args.only_m)
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
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
        case_had_cycle = False
        for q, roots in splits:
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_origin_row(
                                    D,
                                    q,
                                    ell,
                                    cycle,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    audit_args,
                                )
                                if row is not None:
                                    return RowWithCycle(row=row, cycle=tuple(cycle))
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def minimal_period(values: list[int]) -> int:
    if not values:
        return 0
    n = len(values)
    for period in range(1, n + 1):
        if n % period == 0 and all(values[i] == values[i % period] for i in range(n)):
            return period
    return n


def determinant_pairs(bundle: RowWithCycle, omitted: int) -> list[tuple[int, int]]:
    cycle = bundle.cycle
    records = [
        record
        for record in bundle.row.records
        if record.omitted == omitted and record.determinant is not None
    ]
    return [
        (cycle[record.shift] % bundle.row.q, int(record.determinant) % bundle.row.q)
        for record in sorted(records, key=lambda record: record.shift)
    ]


def determinant_edge_values(
    bundle: RowWithCycle,
    omitted: int,
    step: int,
) -> tuple[list[int], list[int], list[int]]:
    cycle = bundle.cycle
    records = [
        record
        for record in bundle.row.records
        if record.omitted == omitted and record.determinant is not None
    ]
    ordered = sorted(records, key=lambda record: record.shift)
    xs = [cycle[record.shift] % bundle.row.q for record in ordered]
    zs = [cycle[(record.shift + step) % len(cycle)] % bundle.row.q for record in ordered]
    ys = [int(record.determinant) % bundle.row.q for record in ordered]
    return xs, zs, ys


def degree_control_summary(
    pairs: list[tuple[int, int]],
    q: int,
    controls: int,
    seed: int,
) -> tuple[int, int, float, float, int, int]:
    poly = polynomial_degree(pairs, q)
    rat = rational_degree(pairs, q)
    if controls <= 0:
        return poly, rat, float("nan"), float("nan"), -1, -1
    rng = random.Random(seed)
    xs = [x for x, _ in pairs]
    zero_count = sum(1 for _, y in pairs if y == 0)
    random_polys: list[int] = []
    random_rats: list[int] = []
    for _ in range(controls):
        random_pairs = random_values_like(xs, q, zero_count, rng)
        random_polys.append(polynomial_degree(random_pairs, q))
        random_rats.append(rational_degree(random_pairs, q))
    return (
        poly,
        rat,
        sum(random_polys) / controls,
        sum(random_rats) / controls,
        min(random_polys),
        min(random_rats),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int, default=0)
    parser.add_argument("--all-omitted", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--random-controls", type=int, default=3)
    parser.add_argument("--edge-step", type=int, default=1)
    parser.add_argument("--max-edge-bidegree", type=int, default=4)
    parser.add_argument("--edge-random-combos", type=int, default=8)
    parser.add_argument("--max-heegner-abs-D", type=int, default=3000)
    parser.add_argument("--max-heegner-h", type=int, default=30)
    args = parser.parse_args()

    bundle = first_row_with_cycle(args)
    if bundle is None:
        raise SystemExit("no eligible trace-gcd origin row found")

    row = bundle.row
    omitted_values = sorted({record.omitted for record in row.records})
    print("trace-GCD Chow plain-j divisor scan")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit={row.left_orbit_rep}:L{row.left_orbit_len}")
    print(f"right_lengths={list(row.right_orbit_lengths)}")
    print(f"omitted_values={omitted_values}")

    heegner = heegner_roots(row.q, args.max_heegner_abs_D, args.max_heegner_h)
    selected_omitted = omitted_values if args.all_omitted else [args.only_omitted]
    failures = 0
    for omitted in selected_omitted:
        pairs = determinant_pairs(bundle, omitted)
        if len(pairs) < 2:
            failures += 1
            print(f"omitted={omitted} skipped_pairs={len(pairs)}")
            continue
        ys = [y for _, y in pairs]
        degree, num_roots, den_roots = interpolant_roots(pairs, row.q)
        poly, rat, rand_poly, rand_rat, rand_poly_min, rand_rat_min = (
            degree_control_summary(pairs, row.q, args.random_controls, args.seed + omitted)
        )
        cm_roots = {x for x, _ in pairs}
        hits = root_hits(num_roots, heegner)
        period = minimal_period(ys)
        print(f"omitted={omitted}")
        print(f"  value_rows={len(pairs)}")
        print(f"  zero_values={sum(1 for y in ys if y == 0)}")
        print(f"  distinct_values={len(set(ys))}")
        print(f"  origin_value_period={period}")
        print(f"  origin_value_orbit_size={len(pairs) // period if period else 0}")
        print(f"  polynomial_degree={poly}")
        print(f"  rational_degree={rat}")
        print(f"  rational_degree_from_roots={degree}")
        print(f"  random_polynomial_degree_mean={rand_poly:.3f}")
        print(f"  random_rational_degree_mean={rand_rat:.3f}")
        print(f"  random_polynomial_degree_min={rand_poly_min}")
        print(f"  random_rational_degree_min={rand_rat_min}")
        print(f"  numerator_roots={num_roots}")
        print(f"  denominator_roots={den_roots}")
        print(f"  numerator_roots_in_target_cm={sorted(set(num_roots) & cm_roots)}")
        print(f"  numerator_roots_outside_target_cm={int(not set(num_roots) <= cm_roots)}")
        print(f"  numerator_root_heegner_hits={[(hit.root, hit.discriminants) for hit in hits]}")
        print(
            "  numerator_roots_with_small_heegner_support="
            f"{sum(bool(hit.discriminants) for hit in hits)}"
        )
        if args.max_edge_bidegree >= 0:
            xs, zs, edge_ys = determinant_edge_values(bundle, omitted, args.edge_step)
            edge_rng = random.Random(args.seed + 1000 + omitted)
            edge_poly = first_polynomial_bidegree(
                xs, zs, edge_ys, row.q, args.max_edge_bidegree
            )
            edge_rat = first_rational_bidegree(
                xs,
                zs,
                edge_ys,
                row.q,
                args.max_edge_bidegree,
                edge_rng,
                args.edge_random_combos,
            )
            print(f"  edge_step={args.edge_step}")
            print(f"  first_edge_polynomial_bidegree_leq_{args.max_edge_bidegree}={edge_poly}")
            print(f"  first_edge_rational_bidegree_leq_{args.max_edge_bidegree}={edge_rat}")

    print("interpretation")
    print("  tested_plain_j_divisor_for_trace_gcd_chow=1")
    print("  low_degree_like_random_means_no_plain_j_shortcut=1")
    print("  generic_heegner_support_means_phase_aware_divisor_still_needed=1")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_chow_plain_divisor_scan")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
