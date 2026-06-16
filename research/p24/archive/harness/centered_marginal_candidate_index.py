#!/usr/bin/env python3
"""Cheap indexer for centered-marginal stress-test candidates.

The full CM packet audits build Hilbert roots, cycles, packet factors, and
Hermitian kernels.  This script stops earlier: it looks for triples

    (D, q, m)

where the class number h admits h=m*n, the quotient components include a
left/right pair with useful Frobenius orbit lengths, and q is a splitting
prime for the Hilbert class polynomial.  It is meant to find targeted rows for
the heavier centered-marginal audits.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import discriminants
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any


@dataclass(frozen=True)
class Candidate:
    D: int
    h: int
    q: int
    m: int
    n: int
    components: tuple[int, ...]
    left: int
    right: int
    left_orbit_len: int
    right_orbit_len: int
    right_orbit_count: int
    axis_dim: int
    packet_degree: int


def orbit_len(q: int, modulus: int) -> int:
    return int(sp.n_order(q % modulus, modulus))


def candidate_pairs(q: int, components: tuple[int, ...], args: argparse.Namespace):
    for left in components:
        if left <= 2:
            continue
        left_len = orbit_len(q, left)
        if left_len < args.min_left_orbit_len:
            continue
        if args.max_left_orbit_len and left_len > args.max_left_orbit_len:
            continue
        for right in components:
            if right <= 2:
                continue
            right_len = orbit_len(q, right)
            if args.require_coprime_lens and gcd(left_len, right_len) != 1:
                continue
            if (right - 1) % right_len:
                continue
            right_count = (right - 1) // right_len
            if right_count < args.min_right_orbits:
                continue
            if args.max_right_orbits and right_count > args.max_right_orbits:
                continue
            yield left, right, left_len, right_len, right_count


def hermitian_packet_degree(q: int, n: int) -> int | None:
    if gcd(q, n) != 1:
        return None
    try:
        degree = int(sp.n_order(q % n, n))
    except Exception:
        return None
    if degree % 2:
        return None
    if pow(q, degree // 2, n) != n - 1:
        return None
    return degree


def scan(args: argparse.Namespace) -> list[Candidate]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[Candidate] = []
    seen: set[int] = set()
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            h = int(pari.qfbclassno(D))
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
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
            and len([c for c in coprime_components(m) if c > 2]) >= 2
        ]
        if not quotient_sizes:
            continue
        try:
            hilbert = pari.polclass(D)
            splits = find_splitting_primes(
                pari,
                hilbert,
                h,
                args.q_start,
                args.q_stop,
                args.max_splitting_primes,
            )
        except Exception:
            continue
        for q, _roots in splits:
            for m in quotient_sizes:
                components = coprime_components(m)
                axis_dim = 1 + sum(c - 1 for c in components)
                packet_degree = hermitian_packet_degree(q, h // m)
                if packet_degree is None:
                    continue
                for left, right, left_len, right_len, right_count in candidate_pairs(
                    q, components, args
                ):
                    if packet_degree < max(args.min_packet_degree, left_len):
                        continue
                    out.append(
                        Candidate(
                            D=D,
                            h=h,
                            q=q,
                            m=m,
                            n=h // m,
                            components=components,
                            left=left,
                            right=right,
                            left_orbit_len=left_len,
                            right_orbit_len=right_len,
                            right_orbit_count=right_count,
                            axis_dim=axis_dim,
                            packet_degree=packet_degree,
                        )
                    )
                    if len(out) >= args.max_rows:
                        return out
    return out


def format_candidate(row: Candidate) -> str:
    return (
        f"D={row.D} h={row.h} q={row.q} m={row.m} n={row.n} "
        f"components={list(row.components)} left={row.left}:L{row.left_orbit_len} "
        f"right={row.right}:R{row.right_orbit_len}x{row.right_orbit_count} "
        f"axis_dim={row.axis_dim} packet_degree={row.packet_degree}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=1000)
    parser.add_argument("--max-abs-D", type=int, default=300000)
    parser.add_argument("--max-prime-quotients", type=int, default=32)
    parser.add_argument("--max-composite-quotients", type=int, default=96)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=600)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=1_500_000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=600)
    parser.add_argument("--min-left-orbit-len", type=int, default=3)
    parser.add_argument("--max-left-orbit-len", type=int, default=12)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--max-right-orbits", type=int, default=12)
    parser.add_argument("--min-packet-degree", type=int, default=0)
    parser.add_argument("--require-coprime-lens", action="store_true")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    rows = scan(args)
    print("Centered marginal candidate index")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"min_left_orbit_len={args.min_left_orbit_len}")
    print(f"require_coprime_lens={int(args.require_coprime_lens)}")
    print()
    for row in rows:
        print(format_candidate(row))
    print()
    print("summary")
    print(f"  candidates={len(rows)}")
    if rows:
        print(f"  max_left_orbit_len={max(row.left_orbit_len for row in rows)}")
        print(f"  max_right_orbit_count={max(row.right_orbit_count for row in rows)}")
        print(f"  max_packet_degree={max(row.packet_degree for row in rows)}")
    print("conclusion=reported_centered_marginal_candidate_index")


if __name__ == "__main__":
    main()
