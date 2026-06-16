#!/usr/bin/env python3
"""Cheap shape index for p24-style Lang leading-tail analogues.

The heavy Lang pivot miner needs Hilbert roots, a full CM cycle, packet
factors, DFTs, and Lang coordinates.  This index stops before all of that.  It
uses only:

* class numbers via qfbclassno;
* quotient shapes h = m*n;
* candidate rational primes q with (D/q)=1;
* Frobenius orbit lengths modulo CRT components;
* Hermitian packet degree ord_n(q).

Rows reported here are not proofs and not actual-CM audits.  They are cheap
shortlist entries for the heavier scripts.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from l1_axis_injectivity_scan import discriminants
from relative_moment_projection_scan import quotient_sizes_any


@dataclass(frozen=True)
class TailShapeCandidate:
    D: int
    h: int
    q: int
    m: int
    n: int
    components: tuple[int, ...]
    left: int
    left_orbit_rep: int
    right: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_lengths: tuple[int, ...]
    packet_degree: int
    axis_dim: int
    deletion_count: int
    tail_deletion_count: int
    min_full_blocks: int
    max_full_blocks: int
    min_tail_len: int
    max_tail_len: int
    min_kept_capacity: int


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


def prefix_tail_for_lengths(lengths: list[int], left_len: int) -> tuple[int, int, int]:
    prefix_len = 0
    full_blocks = 0
    for length in lengths:
        if prefix_len + length > left_len:
            break
        prefix_len += length
        full_blocks += 1
    return full_blocks, prefix_len, left_len - prefix_len


def deletion_tail_metrics(
    right_orbit_lengths: tuple[int, ...],
    left_len: int,
) -> tuple[int, int, int, int, int, int]:
    tail_lengths: list[int] = []
    full_blocks: list[int] = []
    kept_capacities: list[int] = []
    tail_deletions = 0
    for omitted in range(len(right_orbit_lengths)):
        kept = [
            length for index, length in enumerate(right_orbit_lengths)
            if index != omitted
        ]
        capacity = sum(kept)
        kept_capacities.append(capacity)
        blocks, _prefix_len, tail_len = prefix_tail_for_lengths(kept, left_len)
        full_blocks.append(blocks)
        tail_lengths.append(tail_len)
        if capacity >= left_len and tail_len > 0:
            tail_deletions += 1
    return (
        tail_deletions,
        min(full_blocks) if full_blocks else 0,
        max(full_blocks) if full_blocks else 0,
        min(tail_lengths) if tail_lengths else 0,
        max(tail_lengths) if tail_lengths else 0,
        min(kept_capacities) if kept_capacities else 0,
    )


def shape_candidates_for_q(
    D: int,
    h: int,
    q: int,
    quotient_sizes: list[int],
    args: argparse.Namespace,
) -> list[TailShapeCandidate]:
    out: list[TailShapeCandidate] = []
    for m in quotient_sizes:
        components = coprime_components(m)
        axis_dim = 1 + sum(component - 1 for component in components)
        n = h // m
        packet_degree = hermitian_packet_degree(q, n)
        if packet_degree is None or packet_degree < args.min_packet_degree:
            continue
        for left in components:
            if left <= 2:
                continue
            left_orbits = q_orbits(left, q)
            for left_orbit in left_orbits:
                left_len = len(left_orbit)
                if left_len < args.min_left_orbit_len:
                    continue
                if args.max_left_orbit_len and left_len > args.max_left_orbit_len:
                    continue
                if packet_degree < left_len:
                    continue
                for right in components:
                    if right <= 2:
                        continue
                    right_orbits = q_orbits(right, q)
                    right_lengths = tuple(len(orbit) for orbit in right_orbits)
                    if len(right_lengths) < args.min_right_orbits:
                        continue
                    if args.max_right_orbits and len(right_lengths) > args.max_right_orbits:
                        continue
                    if min(right_lengths) < args.min_right_orbit_len:
                        continue
                    if args.require_coprime_lens and any(
                        gcd(left_len, length) != 1 for length in right_lengths
                    ):
                        continue
                    (
                        tail_deletions,
                        min_full_blocks,
                        max_full_blocks,
                        min_tail_len,
                        max_tail_len,
                        min_kept_capacity,
                    ) = deletion_tail_metrics(right_lengths, left_len)
                    if min_kept_capacity < left_len:
                        continue
                    if args.require_tail and tail_deletions == 0:
                        continue
                    if args.require_tail_all_deletions and tail_deletions != len(right_lengths):
                        continue
                    if (args.require_tail or args.require_tail_all_deletions) and max_tail_len < args.min_tail_len:
                        continue
                    if min_full_blocks < args.min_full_blocks:
                        continue
                    out.append(
                        TailShapeCandidate(
                            D=D,
                            h=h,
                            q=q,
                            m=m,
                            n=n,
                            components=components,
                            left=left,
                            left_orbit_rep=left_orbit[0],
                            right=right,
                            left_orbit_len=left_len,
                            right_orbit_count=len(right_lengths),
                            right_orbit_lengths=right_lengths,
                            packet_degree=packet_degree,
                            axis_dim=axis_dim,
                            deletion_count=len(right_lengths),
                            tail_deletion_count=tail_deletions,
                            min_full_blocks=min_full_blocks,
                            max_full_blocks=max_full_blocks,
                            min_tail_len=min_tail_len,
                            max_tail_len=max_tail_len,
                            min_kept_capacity=min_kept_capacity,
                        )
                    )
                    if len(out) >= args.max_rows:
                        return out
    return out


def scan(args: argparse.Namespace) -> list[TailShapeCandidate]:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    primes = list(sp.primerange(args.q_start, args.q_stop))
    out: list[TailShapeCandidate] = []
    seen: set[int] = set()
    discriminant_count = 0
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
            and 1 + sum(component - 1 for component in coprime_components(m))
            <= args.max_axis_dim
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
        ]
        if not quotient_sizes:
            continue
        q_tests = 0
        q_min = max(args.q_start, h + 2) if args.require_q_gt_h else args.q_start
        for q in primes:
            if q < q_min:
                continue
            if args.max_q_tests_per_D and q_tests >= args.max_q_tests_per_D:
                break
            q_tests += 1
            if gcd(q, D) != 1:
                continue
            if int(pari.kronecker(D, q)) != 1:
                continue
            out.extend(shape_candidates_for_q(D, h, q, quotient_sizes, args))
            if len(out) >= args.max_rows:
                return out[: args.max_rows]
        discriminant_count += 1
        if args.max_discriminants and discriminant_count >= args.max_discriminants:
            break
    return out[: args.max_rows]


def format_candidate(row: TailShapeCandidate) -> str:
    return (
        f"D={row.D} h={row.h} q={row.q} m={row.m} n={row.n} "
        f"components={list(row.components)} "
        f"left={row.left}[{row.left_orbit_rep}]:L{row.left_orbit_len} "
        f"right={row.right}:orbits{list(row.right_orbit_lengths)} "
        f"tails={row.tail_deletion_count}/{row.deletion_count} "
        f"tail_range={row.min_tail_len}..{row.max_tail_len} "
        f"full_blocks={row.min_full_blocks}..{row.max_full_blocks} "
        f"kept_min={row.min_kept_capacity} axis_dim={row.axis_dim} "
        f"packet_degree={row.packet_degree}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-discriminants", type=int, default=0)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=1000)
    parser.add_argument("--max-abs-D", type=int, default=300000)
    parser.add_argument("--max-prime-quotients", type=int, default=32)
    parser.add_argument("--max-composite-quotients", type=int, default=96)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=600)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=1_000_000)
    parser.add_argument("--max-q-tests-per-D", type=int, default=200)
    parser.add_argument("--max-axis-dim", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=600)
    parser.add_argument("--min-left-orbit-len", type=int, default=3)
    parser.add_argument("--max-left-orbit-len", type=int, default=12)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--max-right-orbits", type=int, default=12)
    parser.add_argument("--min-right-orbit-len", type=int, default=1)
    parser.add_argument("--min-packet-degree", type=int, default=0)
    parser.add_argument("--min-full-blocks", type=int, default=1)
    parser.add_argument("--min-tail-len", type=int, default=1)
    parser.add_argument("--require-tail", action="store_true")
    parser.add_argument("--require-tail-all-deletions", action="store_true")
    parser.add_argument("--require-coprime-lens", action="store_true")
    parser.add_argument("--require-q-gt-h", action="store_true", default=True)
    parser.add_argument("--allow-q-le-h", dest="require_q_gt_h", action="store_false")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    rows = scan(args)
    print("Lang tail shape index")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_q_tests_per_D={args.max_q_tests_per_D}")
    print(f"min_left_orbit_len={args.min_left_orbit_len}")
    print(f"min_right_orbits={args.min_right_orbits}")
    print(f"min_right_orbit_len={args.min_right_orbit_len}")
    print(f"require_tail={int(args.require_tail)}")
    print(f"require_tail_all_deletions={int(args.require_tail_all_deletions)}")
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
        print(f"  max_right_orbit_len={max(max(row.right_orbit_lengths) for row in rows)}")
        print(f"  max_tail_len={max(row.max_tail_len for row in rows)}")
        print(f"  max_packet_degree={max(row.packet_degree for row in rows)}")
    print("conclusion=reported_lang_tail_shape_index")


if __name__ == "__main__":
    main()
