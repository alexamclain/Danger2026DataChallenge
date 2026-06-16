#!/usr/bin/env python3
"""Origin distribution of Hermitian axis Gram determinant values.

Rank nonvanishing is the certificate condition, but a proof may get easier if
the determinant is invariant, or invariant up to a predictable square/norm,
when the embedded CM origin is rotated.  This script records determinant
values across all origins in small split CM rows.

The output is deliberately small: number of selected-origin tests, zero count,
distinct nonzero determinant values, and Legendre squareclass counts.
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
from hermitian_trace_gram_scan import frobenius_middle_vector


@dataclass(frozen=True)
class DetRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_index: int
    factor_degree: int
    axis_dim: int
    axis_rank: int
    determinant: int | None
    origin_shift: int


def det_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix]
    n = len(mat)
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
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
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            for k in range(col, n):
                mat[row][k] = (mat[row][k] - scale * mat[col][k]) % q
    return det % q


def hermitian_gram_matrix(
    vectors: list[list[int]],
    factor: sp.Poly,
    q: int,
    power_sums: list[int],
) -> list[list[int]]:
    conjugates = [frobenius_middle_vector(vector, factor, q) for vector in vectors]
    return [
        [trace_product(left, right, power_sums, q) for right in conjugates]
        for left in vectors
    ]


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor_index: int,
    factor: sp.Poly,
    origin_shift: int,
) -> DetRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    axis_rank = rank_mod_q(vectors, q)
    determinant: int | None = None
    if axis_rank == len(vectors) and len(vectors) <= 80:
        power_sums = trace_power_sums(factor, q, 2 * factor.degree() - 2)
        determinant = det_mod(hermitian_gram_matrix(vectors, factor, q, power_sums), q)
    return DetRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_index=factor_index,
        factor_degree=factor.degree(),
        axis_dim=len(vectors),
        axis_rank=axis_rank,
        determinant=determinant,
        origin_shift=origin_shift,
    )


def scan(args: argparse.Namespace) -> list[DetRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[DetRow] = []
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
                        row = audit_packet(
                            D, q, ell, shifted, m, factor_index, factor, shift
                        )
                        if row is not None:
                            rows.append(row)
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def packet_key(row: DetRow) -> tuple[int, int, int, int, int, int]:
    return (row.D, row.q, row.ell, row.m, row.n, row.factor_index)


def legendre_label(value: int, q: int) -> str:
    if value % q == 0:
        return "zero"
    return "square" if pow(value % q, (q - 1) // 2, q) == 1 else "nonsquare"


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

    rows = [row for row in scan(args) if row.determinant is not None]
    packets: dict[tuple[int, int, int, int, int, int], list[DetRow]] = {}
    for row in rows:
        packets.setdefault(packet_key(row), []).append(row)

    print("Hermitian Gram determinant distribution")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell m n factor deg axis_dim origins zeros "
            "distinct_values squareclasses"
        )
        for key, group in sorted(packets.items())[:80]:
            D, q, ell, m, n, factor_index = key
            values = [row.determinant % q for row in group if row.determinant is not None]
            squareclasses: dict[str, int] = {}
            for value in values:
                label = legendre_label(value, q)
                squareclasses[label] = squareclasses.get(label, 0) + 1
            sample = group[0]
            print(
                f"D={D:7d} q={q:7d} ell={ell:3d} m={m:3d} n={n:3d} "
                f"factor={factor_index:2d} deg={sample.factor_degree:3d} "
                f"axis_dim={sample.axis_dim:3d} origins={len(values):3d} "
                f"zeros={sum(1 for value in values if value == 0):3d} "
                f"distinct_values={len(set(values)):3d} "
                f"squareclasses={dict(sorted(squareclasses.items()))}"
            )

    zero_packets = 0
    invariant_packets = 0
    all_squareclass_invariant_packets = 0
    total_packets = len(packets)
    distinct_hist: dict[int, int] = {}
    for key, group in packets.items():
        q = key[1]
        values = [row.determinant % q for row in group if row.determinant is not None]
        if any(value == 0 for value in values):
            zero_packets += 1
        distinct = len(set(values))
        distinct_hist[distinct] = distinct_hist.get(distinct, 0) + 1
        if distinct == 1:
            invariant_packets += 1
        labels = {legendre_label(value, q) for value in values}
        if len(labels) == 1:
            all_squareclass_invariant_packets += 1

    print()
    print("summary")
    print(f"  determinant_origin_rows={len(rows)}")
    print(f"  determinant_packets={total_packets}")
    print(f"  packets_with_zero_determinant_origin={zero_packets}")
    print(f"  origin_invariant_packets={invariant_packets}")
    print(f"  squareclass_invariant_packets={all_squareclass_invariant_packets}")
    print(f"  distinct_value_count_histogram={dict(sorted(distinct_hist.items()))}")
    print()
    print("interpretation")
    print("  determinant_origin_invariance_would_weaken_selected_origin_problem=1")
    print("  moving_determinants_mean_selected_local_lattice_data_remains_real=1")
    print("conclusion=reported_hermitian_gram_determinant_distribution")


if __name__ == "__main__":
    main()
