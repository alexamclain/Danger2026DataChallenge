#!/usr/bin/env python3
"""Inspect the cyclic-code shape of packet-factor vanishings.

For a quotient h=m*n and a relative fiber

    J_u(X) = sum_k j_{u+m*k} X^k,

the strong relative-resultant theorem fails at packet factor f | Phi_n when

    J_u mod f = 0.

This is not the same as the whole primitive part vanishing.  It says that the
length-n coefficient vector lies in the cyclic code of polynomials divisible
by one irreducible factor f.  This diagnostic records actual small-CM hits and
compares them to random nonzero codewords in the same code.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
import random

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import bm_linear_complexity, find_full_cycle_prime
from packetized_relative_content_scan import fiber_polynomials, packet_factors, poly_from_coeffs
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any, rotate


@dataclass(frozen=True)
class ShapeRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    orbit_degree: int
    shift: int
    u: int
    bm: int
    distinct: int
    zero_coeffs: int
    trivial_zero: bool
    proper_periods: tuple[int, ...]
    random_min_bm: int
    random_max_bm: int
    random_periodic: int
    sample_coeffs: tuple[int, ...]


def proper_periods(values: list[int]) -> tuple[int, ...]:
    n = len(values)
    out: list[int] = []
    for d in sorted(int(x) for x in sp.divisors(n)):
        if d == n:
            continue
        if all(values[k] == values[k % d] for k in range(n)):
            out.append(d)
    return tuple(out)


def poly_coefficients(poly: sp.Poly, n: int, q: int) -> list[int]:
    out = [0] * n
    for (power,), coeff in poly.as_dict().items():
        if power < n:
            out[power] = int(coeff) % q
    return out


def random_codeword_stats(
    factor: sp.Poly,
    n: int,
    q: int,
    trials: int,
    rng: random.Random,
) -> tuple[int, int, int]:
    """Sample nonzero length-n vectors divisible by factor."""
    degree = factor.degree()
    if trials <= 0 or degree >= n:
        return 0, 0, 0
    bms: list[int] = []
    periodic = 0
    var = factor.gens[0]
    for _ in range(trials):
        coeffs = [rng.randrange(q) for _ in range(n - degree)]
        if all(c == 0 for c in coeffs):
            coeffs[0] = 1
        multiplier = poly_from_coeffs(coeffs, q)
        values = poly_coefficients((factor * multiplier).rem(sp.Poly(var**n - 1, var, modulus=q)), n, q)
        bms.append(bm_linear_complexity(values * 2, q))
        if proper_periods(values):
            periodic += 1
    return min(bms), max(bms), periodic


def factor_orbit_degree(n: int, q: int) -> int:
    if math.gcd(n, q) != 1:
        return 0
    try:
        return int(sp.n_order(q % n, n))
    except ValueError:
        return 0


def audit_hit(
    D: int,
    q: int,
    ell: int,
    shifted: list[int],
    m: int,
    factor: sp.Poly,
    shift: int,
    u: int,
    random_trials: int,
    rng: random.Random,
) -> ShapeRow:
    h = len(shifted)
    n = h // m
    values = [shifted[u + m * k] % q for k in range(n)]
    random_min_bm, random_max_bm, random_periodic = random_codeword_stats(
        factor,
        n,
        q,
        random_trials,
        rng,
    )
    return ShapeRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        orbit_degree=factor_orbit_degree(n, q),
        shift=shift,
        u=u,
        bm=bm_linear_complexity(values * 2, q),
        distinct=len(set(values)),
        zero_coeffs=sum(value == 0 for value in values),
        trivial_zero=(sum(values) % q) == 0,
        proper_periods=proper_periods(values),
        random_min_bm=random_min_bm,
        random_max_bm=random_max_bm,
        random_periodic=random_periodic,
        sample_coeffs=tuple(values[: min(n, 12)]),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[ShapeRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rng = random.Random(args.seed)
    rows: list[ShapeRow] = []
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

        case_had_full_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_full_cycle = True
            ell, cycle = full
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    n = h // m
                    fibers = fiber_polynomials(shifted, q, m)
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        for u, fiber in enumerate(fibers):
                            if fiber.rem(factor).is_zero:
                                rows.append(
                                    audit_hit(
                                        D,
                                        q,
                                        ell,
                                        shifted,
                                        m,
                                        factor,
                                        shift,
                                        u,
                                        args.random_trials,
                                        rng,
                                    )
                                )
                                if len(rows) >= args.max_hits:
                                    return rows
        if case_had_full_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--max-hits", type=int, default=20)
    parser.add_argument("--random-trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    rows = scan(args)
    prime_rows = [row for row in rows if row.n_is_prime]
    composite_rows = [row for row in rows if not row.n_is_prime]

    print("relative packet-factor vanishing shape scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"scan_origins={args.scan_origins}")
    print(f"include_linear={args.include_linear}")
    print(f"random_trials={args.random_trials}")
    print()
    print(
        "columns: D q ell h m n n_prime deg orbit_deg shift u "
        "bm bm_over_n distinct zero_coeffs trivial_zero proper_periods "
        "random_bm_range random_periodic sample_coeffs"
    )
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
            f"m={row.m:3d} n={row.n:3d} n_prime={int(row.n_is_prime)} "
            f"deg={row.factor_degree:3d} orbit_deg={row.orbit_degree:3d} "
            f"shift={row.shift:3d} u={row.u:3d} bm={row.bm:3d} "
            f"bm_over_n={row.bm / row.n:5.2f} distinct={row.distinct:3d} "
            f"zero_coeffs={row.zero_coeffs:3d} trivial_zero={int(row.trivial_zero)} "
            f"proper_periods={list(row.proper_periods)} "
            f"random_bm_range=[{row.random_min_bm},{row.random_max_bm}] "
            f"random_periodic={row.random_periodic}/{args.random_trials} "
            f"sample_coeffs={list(row.sample_coeffs)}"
        )

    print()
    print("summary")
    print(f"  zero_hits={len(rows)}")
    print(f"  prime_zero_hits={len(prime_rows)}")
    print(f"  composite_zero_hits={len(composite_rows)}")
    print(f"  hits_with_proper_period={sum(bool(row.proper_periods) for row in rows)}")
    print(f"  hits_with_low_bm_le_half_n={sum(row.bm <= row.n // 2 for row in rows)}")
    print(f"  hits_with_trivial_zero={sum(row.trivial_zero for row in rows)}")
    print()
    print("interpretation")
    print("  J_u_mod_f_zero_is_one_Frobenius_packet_factor_vanishing=1")
    print("  prime_zero_hits_would_directly_challenge_the_p24_resultant_target=1")
    print("  no_period_or_low_bm_signal_means_no_simple_recurrence_or_imprimitive_escape=1")
    print("conclusion=reported_relative_packet_factor_vanishing_shape")


if __name__ == "__main__":
    main()
