#!/usr/bin/env python3
"""Origin-distribution scan for Hermitian axis Gram failures.

The selected-prime theorem is pointwise in an embedded CM origin.  This scan
tests small split CM torsors across all origins and records whether ordinary
or Hermitian axis Gram failures occur as isolated selected-prime events or as
structural suborbits.

The current p24 target is the Hermitian determinant, but ordinary trace-Gram
failures are kept as a control because they are known to occur in tiny CM
rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import axis_basis_images, coeff_vector, discriminants, rank_mod_q
from trace_pairing_axis_boundary import trace_power_sums, trace_product
from hermitian_trace_gram_scan import frobenius_middle_vector, gram_rank


@dataclass(frozen=True)
class OriginRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_index: int
    factor_degree: int
    components: tuple[int, ...]
    axis_dim: int
    axis_rank: int
    ordinary_gram_rank: int
    hermitian_gram_rank: int | None
    origin_shift: int


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor_index: int,
    factor: sp.Poly,
    origin_shift: int,
) -> OriginRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
    ordinary_rank = gram_rank(vectors, power_sums, q)
    hermitian_rank: int | None = None
    if factor.degree() % 2 == 0:
        conjugates = [
            frobenius_middle_vector(vector, factor, q) for vector in vectors
        ]
        hermitian_rank = gram_rank(vectors, power_sums, q, conjugates)
    return OriginRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_index=factor_index,
        factor_degree=factor.degree(),
        components=components,
        axis_dim=len(vectors),
        axis_rank=rank_mod_q(vectors, q),
        ordinary_gram_rank=ordinary_rank,
        hermitian_gram_rank=hermitian_rank,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[OriginRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[OriginRow] = []
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
        quotient_sizes = [
            m
            for m in quotient_sizes
            if 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
        ]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
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
            for shift in range(h):
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    n = h // m
                    for factor_index, factor in enumerate(packet_factors(n, q)):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                        if factor.degree() < axis_dim:
                            continue
                        rows.append(
                            audit_packet(
                                D,
                                q,
                                ell,
                                shifted,
                                m,
                                factor_index,
                                factor,
                                shift,
                            )
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def packet_key(row: OriginRow) -> tuple[int, int, int, int, int, int]:
    return (row.D, row.q, row.ell, row.m, row.n, row.factor_index)


def failure_distribution(rows: list[OriginRow], kind: str) -> dict[int, int]:
    by_packet: dict[tuple[int, int, int, int, int, int], int] = {}
    for row in rows:
        failed = (
            row.ordinary_gram_rank < row.axis_dim
            if kind == "ordinary"
            else row.hermitian_gram_rank is not None
            and row.hermitian_gram_rank < row.axis_dim
        )
        if failed:
            key = packet_key(row)
            by_packet[key] = by_packet.get(key, 0) + 1
    hist: dict[int, int] = {}
    for count in by_packet.values():
        hist[count] = hist.get(count, 0) + 1
    return dict(sorted(hist.items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-abs-D", type=int, default=25000)
    parser.add_argument("--max-prime-quotients", type=int, default=6)
    parser.add_argument("--max-composite-quotients", type=int, default=6)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=120)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=45)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    full_axis_rows = [row for row in rows if row.axis_rank == row.axis_dim]
    ordinary_failures = [
        row for row in full_axis_rows if row.ordinary_gram_rank < row.axis_dim
    ]
    hermitian_possible = [
        row for row in full_axis_rows if row.hermitian_gram_rank is not None
    ]
    hermitian_failures = [
        row
        for row in hermitian_possible
        if row.hermitian_gram_rank is not None
        and row.hermitian_gram_rank < row.axis_dim
    ]

    print("Hermitian Gram origin-distribution scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n factor deg components axis_dim axis_rank "
            "ordinary_gram hermitian_gram origin"
        )
        display = ordinary_failures + hermitian_failures
        if not display:
            display = rows[:60]
        for row in display[:120]:
            herm = -1 if row.hermitian_gram_rank is None else row.hermitian_gram_rank
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"factor={row.factor_index:2d} deg={row.factor_degree:3d} "
                f"comps={list(row.components)} axis_dim={row.axis_dim:3d} "
                f"axis_rank={row.axis_rank:3d} "
                f"ordinary_gram={row.ordinary_gram_rank:3d} "
                f"hermitian_gram={herm:3d} origin={row.origin_shift:3d}"
            )

    print()
    print("summary")
    print(f"  origin_packet_rows={len(rows)}")
    print(f"  full_axis_rank_rows={len(full_axis_rows)}")
    print(f"  ordinary_gram_failure_rows={len(ordinary_failures)}")
    print(f"  hermitian_possible_rows={len(hermitian_possible)}")
    print(f"  hermitian_gram_failure_rows={len(hermitian_failures)}")
    print(f"  ordinary_failure_origin_count_histogram={failure_distribution(full_axis_rows, 'ordinary')}")
    print(f"  hermitian_failure_origin_count_histogram={failure_distribution(full_axis_rows, 'hermitian')}")
    print()
    print("interpretation")
    print("  selected_prime_problem_is_originwise_not_just_packetwise=1")
    print("  ordinary_failures_control_whether_failures_form_suborbits=1")
    print("  hermitian_failures_would_falsify_the_current_axis_lattice_target=1")
    print("conclusion=reported_hermitian_gram_origin_distribution_scan")


if __name__ == "__main__":
    main()
