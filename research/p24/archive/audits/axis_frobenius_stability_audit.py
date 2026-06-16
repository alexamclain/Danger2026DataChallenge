#!/usr/bin/env python3
"""Audit whether packet axis component images are Frobenius submodules.

The module-directness proof would become much easier if the images of the
constant, 2-, 157-, and 211-axis pieces were Frobenius-stable submodules in
the H-packet field.  Then nonisomorphic Frobenius constituents could force
directness after proving component kernels.

This script tests that premise in small CM packet rows.  It computes the
component axis image span

    span{Y_t = sum_{r == t mod c} F_r}

and the trace-zero span

    span{Y_t - Y_0 : 1 <= t < c}

then checks whether applying packet-field Frobenius x -> x^q keeps those
spans stable.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from component_character_module_scan import (
    axis_sums,
    character_values,
    primitive_root_in_packet,
    poly_pow,
)
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from l1_axis_injectivity_scan import coeff_vector, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class StabilityRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    component: int
    full_rank: int
    full_plus_frob_rank: int
    trace_zero_rank: int
    trace_zero_plus_frob_rank: int
    character_mismatch_count: int | None
    character_count: int | None


def subtract_poly(left: sp.Poly, right: sp.Poly, factor: sp.Poly) -> sp.Poly:
    return (left - right).rem(factor)


def rank_polys(values: list[sp.Poly], degree: int, q: int) -> int:
    return rank_mod_q([coeff_vector(value, degree, q) for value in values], q)


def frobenius(value: sp.Poly, q: int, factor: sp.Poly) -> sp.Poly:
    return poly_pow(value, q, factor)


def audit_component(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    component: int,
) -> StabilityRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    axis = axis_sums(residues, component, factor)
    axis_frob = [frobenius(value, q, factor) for value in axis]
    trace_zero = [
        subtract_poly(axis[t], axis[0], factor)
        for t in range(1, component)
    ]
    trace_zero_frob = [frobenius(value, q, factor) for value in trace_zero]

    char_mismatches: int | None = None
    char_count: int | None = None
    zeta = None
    if component <= 80 and factor.degree() <= 160:
        zeta = primitive_root_in_packet(q, component, factor)
    if zeta is not None:
        chars = character_values(axis, zeta, factor)
        mismatches = 0
        total = 0
        for s in range(1, component):
            target = chars[(q * s) % component]
            if not subtract_poly(frobenius(chars[s], q, factor), target, factor).is_zero:
                mismatches += 1
            total += 1
        char_mismatches = mismatches
        char_count = total

    return StabilityRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        component=component,
        full_rank=rank_polys(axis, factor.degree(), q),
        full_plus_frob_rank=rank_polys(axis + axis_frob, factor.degree(), q),
        trace_zero_rank=rank_polys(trace_zero, factor.degree(), q),
        trace_zero_plus_frob_rank=rank_polys(
            trace_zero + trace_zero_frob,
            factor.degree(),
            q,
        ),
        character_mismatch_count=char_mismatches,
        character_count=char_count,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[StabilityRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[StabilityRow] = []
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
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
        case_had_row = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for component in coprime_components(m):
                        if component < args.min_component:
                            continue
                        if component > args.max_component:
                            continue
                        rows.append(
                            audit_component(
                                D,
                                q,
                                ell,
                                cycle,
                                m,
                                factor,
                                component,
                            )
                        )
                        case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=12)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=800000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--min-component", type=int, default=2)
    parser.add_argument("--max-component", type=int, default=40)
    parser.add_argument("--max-factor-degree", type=int, default=40)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_unstable = [
        row for row in rows if row.full_plus_frob_rank > row.full_rank
    ]
    trace_unstable = [
        row for row in rows
        if row.trace_zero_plus_frob_rank > row.trace_zero_rank
    ]
    char_rows = [row for row in rows if row.character_count is not None]
    char_mismatch_rows = [
        row for row in char_rows
        if row.character_mismatch_count not in (None, 0)
    ]

    print("axis Frobenius stability audit")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"component_window=[{args.min_component},{args.max_component}]")
    print(f"max_factor_degree={args.max_factor_degree}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg c full_rank full+F "
            "tz_rank tz+F char_mismatch"
        )
        display = trace_unstable[:80] if trace_unstable else rows[:80]
        for row in display:
            char_text = "NA"
            if row.character_count is not None:
                char_text = (
                    f"{row.character_mismatch_count}/{row.character_count}"
                )
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} c={row.component:3d} "
                f"full_rank={row.full_rank:3d} "
                f"full_plus_frob={row.full_plus_frob_rank:3d} "
                f"trace_zero_rank={row.trace_zero_rank:3d} "
                f"trace_zero_plus_frob={row.trace_zero_plus_frob_rank:3d} "
                f"char_mismatch={char_text}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  full_span_unstable_rows={len(full_unstable)}")
    print(f"  trace_zero_unstable_rows={len(trace_unstable)}")
    print(f"  character_equivariance_rows={len(char_rows)}")
    print(f"  character_mismatch_rows={len(char_mismatch_rows)}")
    print()
    print("interpretation")
    print("  full_span_unstable_means_packet_Frobenius_leaves_component_axis_span=0")
    print("  trace_zero_unstable_means_directness_is_not_forced_by_Frobenius_modules=1")
    print("  character_mismatch_means_sigma(G_s)_not_equal_G_{q*s}_at_fixed_H_root=1")
    print("conclusion=reported_axis_frobenius_stability_audit")


if __name__ == "__main__":
    main()
