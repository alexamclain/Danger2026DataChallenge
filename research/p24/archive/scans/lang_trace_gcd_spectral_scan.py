#!/usr/bin/env python3
"""Scan spectral complexity of reduced trace-gcd right sequences.

The p24 trace-gcd route reduces origin motion to a right-component determinant
sequence

    Delta_i(t),  t mod d.

The pinned `(4,7)` row has linear complexity equal to one right Frobenius
orbit.  This script checks whether that is a structural trace-gcd phenomenon
or a small exterior-power accident by scanning additional actual-CM rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from lang_trace_gcd_origin_action_audit import (
    OriginActionRow,
    OriginDet,
    audit_origin_row,
)
from lang_trace_gcd_sequence_complexity import (
    bm_connection,
    connection_polynomial_summary,
    nonnull_ints,
    reduced_right_sequence,
    verify_connection,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any


@dataclass(frozen=True)
class SpectralRow:
    D: int
    q: int
    h: int
    m: int
    n: int
    left: int
    right: int
    omitted: int
    tail_len: int
    kernel_dim: int
    zeros: int
    distinct: int
    complexity: int
    right_order: int
    single_orbit: bool
    full_or_near_full: bool
    connection_divides: bool
    connection_factorization: str
    right_mismatches: int
    product_mod_q: int | None


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * value) % modulus
    return out


def sequence_complexity(values: list[int], q: int) -> tuple[int, list[int], bool, str]:
    doubled = values + values
    connection = bm_connection(doubled, q)
    failures = verify_connection(doubled, connection, q)
    if failures:
        raise AssertionError("connection failed on doubled sequence")
    _, divides, factorization = connection_polynomial_summary(connection, len(values), q)
    return len(connection) - 1, connection, divides, factorization


def summarize_origin_row(row: OriginActionRow, min_tail_len: int) -> list[SpectralRow]:
    out: list[SpectralRow] = []
    records_by_omitted: dict[int, list[OriginDet]] = {}
    for record in row.records:
        records_by_omitted.setdefault(record.omitted, []).append(record)

    right_order = int(sp.n_order(row.q % row.right, row.right))
    for omitted, records in sorted(records_by_omitted.items()):
        if records[0].tail_len < min_tail_len:
            continue
        right_values, mismatches = reduced_right_sequence(records, row.right)
        if mismatches or any(value is None for value in right_values):
            out.append(
                SpectralRow(
                    D=row.D,
                    q=row.q,
                    h=row.h,
                    m=row.m,
                    n=row.n,
                    left=row.left,
                    right=row.right,
                    omitted=omitted,
                    tail_len=records[0].tail_len,
                    kernel_dim=records[0].kernel_dim,
                    zeros=-1,
                    distinct=-1,
                    complexity=-1,
                    right_order=right_order,
                    single_orbit=False,
                    full_or_near_full=False,
                    connection_divides=False,
                    connection_factorization="NA",
                    right_mismatches=mismatches,
                    product_mod_q=None,
                )
            )
            continue
        seq = nonnull_ints(right_values)
        complexity, _, divides, factorization = sequence_complexity(seq, row.q)
        out.append(
            SpectralRow(
                D=row.D,
                q=row.q,
                h=row.h,
                m=row.m,
                n=row.n,
                left=row.left,
                right=row.right,
                omitted=omitted,
                tail_len=records[0].tail_len,
                kernel_dim=records[0].kernel_dim,
                zeros=sum(1 for value in seq if value == 0),
                distinct=len(set(seq)),
                complexity=complexity,
                right_order=right_order,
                single_orbit=complexity == right_order,
                full_or_near_full=complexity >= row.right - right_order,
                connection_divides=divides,
                connection_factorization=factorization,
                right_mismatches=mismatches,
                product_mod_q=product_mod(seq, row.q),
            )
        )
    return out


def scan(args: argparse.Namespace) -> list[SpectralRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[SpectralRow] = []
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
        if not splits:
            continue
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
                            if args.require_prime_right and not sp.isprime(right):
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
                                    args,
                                )
                                if row is None:
                                    continue
                                out.extend(summarize_origin_row(row, args.min_tail_len))
                                if len(out) >= args.max_rows:
                                    return out[: args.max_rows]
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=24)
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
    parser.add_argument("--min-tail-len", type=int, default=0)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--require-prime-right", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("Lang trace-gcd right-sequence spectral scan")
    print(f"rows={len(rows)}")
    print(
        "columns: D q h m n pair omitted tail K zeros distinct product "
        "right_order complexity single_orbit full_or_near_full "
        "conn_divides mismatches factorization"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
            f"pair=({row.left},{row.right}) omitted={row.omitted} "
            f"tail={row.tail_len} K={row.kernel_dim} "
            f"zeros={row.zeros} distinct={row.distinct} "
            f"product={row.product_mod_q if row.product_mod_q is not None else 'NA'} "
            f"right_order={row.right_order} complexity={row.complexity} "
            f"single_orbit={int(row.single_orbit)} "
            f"full_or_near_full={int(row.full_or_near_full)} "
            f"conn_divides={int(row.connection_divides)} "
            f"mismatches={row.right_mismatches} "
            f"factorization={row.connection_factorization}"
        )
    print()
    print("interpretation")
    print("  single_orbit=1 supports a Gauss-period norm target.")
    print("  full_or_near_full=1 means the direct right-resultant is likely necessary.")
    print("conclusion=reported_lang_trace_gcd_spectral_scan")


if __name__ == "__main__":
    main()
