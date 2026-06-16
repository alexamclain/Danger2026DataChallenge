#!/usr/bin/env python3
"""Packetized relative-content scan for small CM cycles.

This is the finite-field analogue of the p24 exact certificate target:

    gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1,

where `f_a` is a Frobenius packet factor of `Phi_n` over the base field and

    J_u(X) = sum_k j_{u+m*k} X^k.

Unlike `natural_relative_resolvent_scan.py`, this script does not require the
relative roots of unity to live in the base field.  It keeps the CM roots in a
split prime field `F_q`, factors `Phi_n` over `F_q`, and tests the content
ideal packet by packet.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

X = sp.symbols("X")


@dataclass(frozen=True)
class PacketRow:
    quotient_m: int
    subgroup_n: int
    factor_degree: int
    content_gcd_degree: int
    energy_remainder_zero: bool
    packet_norm_zero: bool
    hermitian_remainder_zero: bool
    hermitian_norm_zero: bool


@dataclass(frozen=True)
class ScanRow:
    D: int
    q: int
    ell: int
    h: int
    rows: tuple[PacketRow, ...]


def poly_from_coeffs(coeffs: list[int], q: int) -> sp.Poly:
    return sp.Poly(sum((c % q) * X**i for i, c in enumerate(coeffs)), X, modulus=q)


def packet_factors(n: int, q: int) -> list[sp.Poly]:
    pari = Pari()
    fac = pari(f"factor(Mod(1,{q})*polcyclo({n}))")
    out: list[sp.Poly] = []
    for i in range(len(fac[0])):
        factor = fac[0][i]
        exp = int(fac[1][i])
        if exp != 1:
            raise ValueError("cyclotomic factor was not squarefree")
        degree = int(pari.poldegree(factor))
        coeffs = [int(pari.polcoef(factor, j)) % q for j in range(degree + 1)]
        out.append(poly_from_coeffs(coeffs, q))
    return out


def quotient_sizes_with_prime_subgroup(h: int, max_quotients: int, min_n: int) -> list[int]:
    out: list[int] = []
    for n in sorted(sp.divisors(h)):
        n = int(n)
        if n <= 2 or n < min_n or not sp.isprime(n):
            continue
        m = h // n
        if 2 <= m < h:
            out.append(m)
    return sorted(out, key=lambda m: (h // m, m))[:max_quotients]


def fiber_polynomials(cycle: list[int], q: int, m: int) -> list[sp.Poly]:
    h = len(cycle)
    n = h // m
    return [
        poly_from_coeffs([cycle[u + m * k] for k in range(n)], q)
        for u in range(m)
    ]


def content_gcd_degree(factor: sp.Poly, fibers: list[sp.Poly]) -> int:
    gcd = factor
    for fiber in fibers:
        gcd = sp.gcd(gcd, fiber.rem(factor))
        if gcd.degree() == 0:
            return 0
    return gcd.degree()


def autocorrelation_energy_poly(cycle: list[int], q: int, m: int) -> sp.Poly:
    h = len(cycle)
    n = h // m
    coeffs: list[int] = []
    for d in range(n):
        offset = m * d
        total = 0
        for i, value in enumerate(cycle):
            total = (total + cycle[(i + offset) % h] * value) % q
        coeffs.append(total)
    return poly_from_coeffs(coeffs, q)


def gram_energy_poly(cycle: list[int], q: int, m: int) -> sp.Poly:
    h = len(cycle)
    n = h // m
    coeffs = [0] * n
    for u in range(m):
        fiber = [cycle[u + m * k] % q for k in range(n)]
        for k, left in enumerate(fiber):
            for ell, right in enumerate(fiber):
                coeffs[(k - ell) % n] = (coeffs[(k - ell) % n] + left * right) % q
    return poly_from_coeffs(coeffs, q)


def hermitian_energy_poly(cycle: list[int], q: int, m: int) -> sp.Poly:
    h = len(cycle)
    n = h // m
    fibers = [
        [cycle[u + m * k] % q for k in range(n)]
        for u in range(m)
    ]
    coeffs = [0] * n
    for u in range(m):
        inv_u = (-u) % m
        carry = (u + inv_u) // m
        left = fibers[u]
        right = fibers[inv_u]
        for k, left_value in enumerate(left):
            for ell, right_value in enumerate(right):
                coeffs[(carry + k + ell) % n] = (
                    coeffs[(carry + k + ell) % n] + left_value * right_value
                ) % q
    return poly_from_coeffs(coeffs, q)


def audit_quotient(cycle: list[int], q: int, m: int) -> list[PacketRow]:
    h = len(cycle)
    n = h // m
    factors = packet_factors(n, q)
    fibers = fiber_polynomials(cycle, q, m)
    energy_poly = autocorrelation_energy_poly(cycle, q, m)
    gram_poly = gram_energy_poly(cycle, q, m)
    if energy_poly != gram_poly:
        raise AssertionError("autocorrelation and Gram energy polynomials differ")
    hermitian_poly = hermitian_energy_poly(cycle, q, m)
    rows: list[PacketRow] = []
    for factor in factors:
        content_degree = content_gcd_degree(factor, fibers)
        energy_remainder = energy_poly.rem(factor)
        energy_zero = energy_remainder.is_zero
        resultant = int(sp.resultant(factor.as_expr(), energy_poly.as_expr(), X)) % q
        hermitian_remainder = hermitian_poly.rem(factor)
        hermitian_zero = hermitian_remainder.is_zero
        hermitian_resultant = int(sp.resultant(factor.as_expr(), hermitian_poly.as_expr(), X)) % q
        rows.append(
            PacketRow(
                quotient_m=m,
                subgroup_n=n,
                factor_degree=factor.degree(),
                content_gcd_degree=content_degree,
                energy_remainder_zero=energy_zero,
                packet_norm_zero=(resultant == 0),
                hermitian_remainder_zero=hermitian_zero,
                hermitian_norm_zero=(hermitian_resultant == 0),
            )
        )
    return rows


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_quotients: int,
    min_n: int,
    q_start: int,
    q_stop: int,
) -> list[ScanRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    out: list[ScanRow] = []
    seen: set[int] = set()
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
        quotient_sizes = quotient_sizes_with_prime_subgroup(h, max_quotients, min_n)
        if not quotient_sizes:
            continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        rows = tuple(
            row
            for m in quotient_sizes
            for row in audit_quotient(cycle, q, m)
        )
        if rows:
            out.append(ScanRow(D=D, q=q, ell=ell, h=h, rows=rows))
        if len(out) >= max_cases:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=12)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=90)
    ap.add_argument("--max-abs-D", type=int, default=15000)
    ap.add_argument("--max-quotients", type=int, default=3)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=120000)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_quotients=args.max_quotients,
        min_n=args.min_n,
        q_start=args.q_start,
        q_stop=args.q_stop,
    )

    print("packetized relative-content scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n factor_degree content_gcd_degree "
            "energy_zero packet_norm_zero hermitian_zero hermitian_norm_zero"
        )
        for row in rows:
            for prow in row.rows:
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={prow.quotient_m:3d} n={prow.subgroup_n:3d} "
                    f"factor_degree={prow.factor_degree:2d} "
                    f"content_gcd_degree={prow.content_gcd_degree:2d} "
                    f"energy_zero={int(prow.energy_remainder_zero)} "
                    f"packet_norm_zero={int(prow.packet_norm_zero)} "
                    f"hermitian_zero={int(prow.hermitian_remainder_zero)} "
                    f"hermitian_norm_zero={int(prow.hermitian_norm_zero)}"
                )

    packet_rows = [prow for row in rows for prow in row.rows]
    content_failures = sum(1 for prow in packet_rows if prow.content_gcd_degree > 0)
    energy_zeros = sum(1 for prow in packet_rows if prow.energy_remainder_zero)
    norm_zeros = sum(1 for prow in packet_rows if prow.packet_norm_zero)
    hermitian_zeros = sum(1 for prow in packet_rows if prow.hermitian_remainder_zero)
    hermitian_norm_zeros = sum(1 for prow in packet_rows if prow.hermitian_norm_zero)
    nonlinear_packets = sum(1 for prow in packet_rows if prow.factor_degree > 1)
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  packet_rows={len(packet_rows)}")
    print(f"  nonlinear_packets={nonlinear_packets}")
    print(f"  content_failures={content_failures}")
    print(f"  energy_zero_packets={energy_zeros}")
    print(f"  packet_norm_zero_packets={norm_zeros}")
    print(f"  hermitian_zero_packets={hermitian_zeros}")
    print(f"  hermitian_norm_zero_packets={hermitian_norm_zeros}")
    print()
    print("interpretation")
    print("  content_gcd_degree_zero_is_exact_packet_certificate=1")
    print("  energy_nonzero_is_scalar_sufficient_packet_certificate=1")
    print("  hermitian_energy_nonzero_is_positive_scalar_sufficient_certificate=1")
    print("  roots_of_unity_in_base_field_required=0")
    print("conclusion=reported_packetized_relative_content_scan")


if __name__ == "__main__":
    main()
