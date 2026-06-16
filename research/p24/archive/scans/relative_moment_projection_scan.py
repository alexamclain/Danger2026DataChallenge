#!/usr/bin/env python3
"""Low-degree quotient-moment projections for relative-content packets.

For a quotient h=m*n and a Frobenius packet factor f | Phi_n, the exact
relative-content certificate is that the vector

    (J_0 mod f, ..., J_{m-1} mod f)

is nonzero in the packet field.  This scan tests whether simple quotient
moments

    M_e = sum_u u^e J_u mod f

certify the same nonzero vector in small CM cycles with a small bounded e.
The case e=0 is the quotient trace of the relative packet; larger e are
finite-difference probes on the quotient coordinate.  If a bounded e worked
robustly, it would be a scalar theorem target strictly weaker than coordinate
product nonvanishing.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from embedded_decomposition_calibration import pari_linear_roots
from packetized_relative_content_scan import fiber_polynomials, packet_factors

X = sp.symbols("X")


@dataclass(frozen=True)
class ProjectionRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    content_zero: bool
    first_nonzero_moment: int | None
    zero_moments_prefix: int
    coord_zero_count: int
    origin_shift: int
    section: str


def rotate(cycle: list[int], shift: int) -> list[int]:
    if shift == 0:
        return cycle
    return cycle[shift:] + cycle[:shift]


def quotient_sizes_any(
    h: int,
    max_prime: int,
    max_composite: int,
    min_n: int,
    max_n: int,
) -> list[int]:
    prime_ms: list[int] = []
    composite_ms: list[int] = []
    for n in sorted(int(d) for d in sp.divisors(h)):
        if n < min_n or n > max_n or n >= h:
            continue
        m = h // n
        if m < 2:
            continue
        if sp.isprime(n):
            prime_ms.append(m)
        elif n > 2:
            composite_ms.append(m)
    prime_ms = sorted(prime_ms, key=lambda m: (h // m, m))[:max_prime]
    composite_ms = sorted(composite_ms, key=lambda m: (h // m, m))[:max_composite]
    return sorted(set(prime_ms + composite_ms), key=lambda m: (h // m, m))


def find_splitting_primes(
    pari: Pari,
    hilbert,
    h: int,
    start: int,
    stop: int,
    max_count: int,
) -> list[tuple[int, list[int]]]:
    if max_count <= 1:
        split = find_splitting_prime(pari, hilbert, h, start, stop)
        return [] if split is None else [split]
    out: list[tuple[int, list[int]]] = []
    for q in sp.primerange(max(start, h + 2), stop):
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            out.append((int(q), roots))
            if len(out) >= max_count:
                break
    return out


def section_fiber_polynomials(
    cycle: list[int],
    q: int,
    m: int,
    section: str,
) -> list[sp.Poly]:
    h = len(cycle)
    n = h // m
    if section == "contiguous":
        return fiber_polynomials(cycle, q, m)
    if section == "complement":
        if sp.gcd(m, n) != 1:
            raise ValueError("complement section requires gcd(m,n)=1")
        return [
            sp.Poly(
                sum((cycle[(n * r + m * k) % h] % q) * X**k for k in range(n)),
                X,
                modulus=q,
            )
            for r in range(m)
        ]
    raise ValueError(f"unknown section: {section}")


def first_nonzero_moment(
    residues: list[sp.Poly],
    factor: sp.Poly,
    q: int,
    max_degree: int,
) -> tuple[int | None, int]:
    """Return first e with sum_u u^e residues[u] nonzero, and zero prefix."""
    zero_prefix = 0
    for degree in range(max_degree + 1):
        total = sp.Poly(0, factor.gens[0], modulus=q)
        for u, residue in enumerate(residues):
            coeff = pow(u % q, degree, q)
            if coeff:
                total = (total + coeff * residue).rem(factor)
        if not total.is_zero:
            return degree, zero_prefix
        zero_prefix += 1
    return None, zero_prefix


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    max_degree: int,
    origin_shift: int,
    section: str,
) -> ProjectionRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, section)
    ]
    coord_zero_count = sum(residue.is_zero for residue in residues)
    content_zero = coord_zero_count == m
    first, prefix = first_nonzero_moment(residues, factor, q, max_degree)
    return ProjectionRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        content_zero=content_zero,
        first_nonzero_moment=first,
        zero_moments_prefix=prefix,
        coord_zero_count=coord_zero_count,
        origin_shift=origin_shift,
        section=section,
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
    include_linear: bool,
    max_moment_degree: int,
    scan_origins: bool,
    only_D: int | None,
    section: str,
    max_splitting_primes: int,
) -> list[ProjectionRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    if only_D is None:
        discriminants = [-5000] + [
            D for D in range(-200, -max_abs_D - 1, -1)
            if D % 4 in (0, 1)
        ]
    else:
        discriminants = [only_D]

    rows: list[ProjectionRow] = []
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
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            q_start,
            q_stop,
            max_splitting_primes,
        )
        if not splits:
            continue
        case_had_full_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_full_cycle = True
            ell, cycle = full
            shifts = range(h) if scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    n = h // m
                    if section == "complement" and sp.gcd(m, n) != 1:
                        continue
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not include_linear:
                            continue
                        rows.append(
                            audit_packet(
                                D,
                                q,
                                ell,
                                shifted,
                                m,
                                factor,
                                max_moment_degree,
                                shift,
                                section,
                            )
                        )
        if not case_had_full_cycle:
            continue
        cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=40)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=120)
    ap.add_argument("--max-abs-D", type=int, default=30000)
    ap.add_argument("--max-prime-quotients", type=int, default=4)
    ap.add_argument("--max-composite-quotients", type=int, default=4)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=200)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=300000)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--max-moment-degree", type=int, default=4)
    ap.add_argument("--scan-origins", action="store_true")
    ap.add_argument("--only-D", type=int)
    ap.add_argument("--section", choices=("contiguous", "complement"), default="contiguous")
    ap.add_argument("--max-splitting-primes", type=int, default=1)
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
        include_linear=args.include_linear,
        max_moment_degree=args.max_moment_degree,
        scan_origins=args.scan_origins,
        only_D=args.only_D,
        section=args.section,
        max_splitting_primes=args.max_splitting_primes,
    )

    print("relative quotient-moment projection scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"max_n={args.max_n}")
    print(f"q_stop={args.q_stop}")
    print(f"include_linear={args.include_linear}")
    print(f"max_moment_degree={args.max_moment_degree}")
    print(f"scan_origins={args.scan_origins}")
    print(f"only_D={args.only_D}")
    print(f"section={args.section}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg origin coord_zero content_zero "
            "first_nonzero_moment zero_prefix section"
        )
        for row in rows:
            interesting = (
                row.content_zero
                or row.coord_zero_count
                or row.first_nonzero_moment is None
                or (row.first_nonzero_moment is not None and row.first_nonzero_moment > 0)
            )
            if interesting:
                first = "NA" if row.first_nonzero_moment is None else str(row.first_nonzero_moment)
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
                    f"deg={row.factor_degree:3d} origin={row.origin_shift:3d} "
                    f"coord_zero={row.coord_zero_count:3d} "
                    f"content_zero={int(row.content_zero)} "
                    f"first_nonzero_moment={first:>2s} "
                    f"zero_prefix={row.zero_moments_prefix:2d} "
                    f"section={row.section}"
                )

    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]
    missed = [row for row in rows if row.first_nonzero_moment is None and not row.content_zero]
    content_failures = [row for row in rows if row.content_zero]
    moment_hist: dict[str, int] = {}
    for row in rows:
        key = "content_zero" if row.content_zero else (
            ">{}".format(args.max_moment_degree)
            if row.first_nonzero_moment is None
            else str(row.first_nonzero_moment)
        )
        moment_hist[key] = moment_hist.get(key, 0) + 1
    prime_missed = [row for row in prime_rows if row.first_nonzero_moment is None and not row.content_zero]
    composite_missed = [
        row for row in composite_rows
        if row.first_nonzero_moment is None and not row.content_zero
    ]
    nonzero_content_rows = [row for row in rows if not row.content_zero]
    moment0_failures = [
        row for row in nonzero_content_rows
        if row.first_nonzero_moment is None or row.first_nonzero_moment > 0
    ]
    moment01_failures = [
        row for row in nonzero_content_rows
        if row.first_nonzero_moment is None or row.first_nonzero_moment > 1
    ]
    expected_moment0_failures_random = sum(
        row.q ** (-row.factor_degree) for row in nonzero_content_rows
    )
    expected_moment01_failures_random = sum(
        row.q ** (-2 * row.factor_degree) for row in nonzero_content_rows
    )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  prime_packet_rows={len(prime_rows)}")
    print(f"  composite_packet_rows={len(composite_rows)}")
    print(f"  content_failures={len(content_failures)}")
    print(f"  nonzero_content_missed_by_moments={len(missed)}")
    print(f"  prime_missed_by_moments={len(prime_missed)}")
    print(f"  composite_missed_by_moments={len(composite_missed)}")
    print(f"  moment_histogram={dict(sorted(moment_hist.items()))}")
    print(f"  moment0_failures={len(moment0_failures)}")
    print(f"  moment01_failures={len(moment01_failures)}")
    print(f"  expected_moment0_failures_random={expected_moment0_failures_random:.6f}")
    print(f"  expected_moment01_failures_random={expected_moment01_failures_random:.6f}")
    if missed:
        sample = missed[:8]
        print("  missed_samples:")
        for row in sample:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
                f"deg={row.factor_degree} origin={row.origin_shift}"
            )
    print()
    print("interpretation")
    print("  first_nonzero_moment_exists_implies_exact_content_certificate=1")
    print("  bounded_moment_success_would_be_weaker_than_coordinate_product=1")
    print("  no_moment_within_bound_means_this_projection_family_is_too_weak=1")
    print("conclusion=reported_relative_moment_projection_scan")


if __name__ == "__main__":
    main()
