#!/usr/bin/env python3
"""Geometry-only shortlist for nonvacuous lambda-plateau rowspace tests.

The actual rowspace audit is PARI-heavy because it builds CM roots and packet
rows.  This script does only the cheap front half: class number, quotient
shapes, Frobenius orbit lengths, and dimension checks.  Its job is to find
small rows where a later actual-CM rowspace audit could test

    ker(B_leading) subset ker(C_plateau)

nonvacuously, instead of rediscovering dimension-loss or noncoprime orbit
obstructions.
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
from l1_axis_injectivity_scan import discriminants
from relative_moment_projection_scan import quotient_sizes_any


@dataclass(frozen=True)
class GeometryHit:
    D: int
    h: int
    q: int
    m: int
    n: int
    left: int
    right: int
    left_len: int
    right_lens: tuple[int, ...]
    right_orbit_count: int
    min_after_delete: int
    max_after_delete: int
    prefix_lengths: tuple[int, ...]
    tail_lengths: tuple[int, ...]
    extension_degree: int


def orbit_prefix_tail_lengths(
    right_lens: list[int],
    left_len: int,
) -> tuple[int, ...]:
    out: list[int] = []
    for omitted in range(len(right_lens)):
        prefix = 0
        for index, orbit_len in enumerate(right_lens):
            if index == omitted:
                continue
            if prefix + orbit_len > left_len:
                break
            prefix += orbit_len
        out.append(prefix)
    return tuple(out)


def geometry_hits_for(
    D: int,
    h: int,
    q: int,
    m: int,
    max_extension_degree: int,
    min_left_len: int,
) -> list[GeometryHit]:
    n = h // m
    components = tuple(component for component in coprime_components(m) if component > 2)
    if len(components) < 2 or gcd(m, n) != 1:
        return []
    try:
        extension_degree = int(sp.n_order(q % m, m))
    except ValueError:
        return []
    if extension_degree > max_extension_degree:
        return []

    hits: list[GeometryHit] = []
    for left in components:
        for left_orbit in q_orbits(left, q):
            left_len = len(left_orbit)
            if left_len < min_left_len:
                continue
            for right in components:
                if right == left:
                    continue
                right_orbits = q_orbits(right, q)
                right_lens = [len(orbit) for orbit in right_orbits]
                if len(right_lens) < 2:
                    continue
                if any(gcd(left_len, right_len) != 1 for right_len in right_lens):
                    continue
                after_delete = [
                    sum(length for i, length in enumerate(right_lens) if i != omitted)
                    for omitted in range(len(right_lens))
                ]
                if min(after_delete) < left_len:
                    continue
                prefix_lengths = orbit_prefix_tail_lengths(right_lens, left_len)
                tail_lengths = tuple(left_len - prefix for prefix in prefix_lengths)
                if not any(prefix > 0 and tail > 0 for prefix, tail in zip(prefix_lengths, tail_lengths)):
                    continue
                hits.append(
                    GeometryHit(
                        D=D,
                        h=h,
                        q=q,
                        m=m,
                        n=n,
                        left=left,
                        right=right,
                        left_len=left_len,
                        right_lens=tuple(right_lens),
                        right_orbit_count=len(right_lens),
                        min_after_delete=min(after_delete),
                        max_after_delete=max(after_delete),
                        prefix_lengths=prefix_lengths,
                        tail_lengths=tail_lengths,
                        extension_degree=extension_degree,
                    )
                )
    return hits


def scan(args: argparse.Namespace) -> list[GeometryHit]:
    pari = Pari()
    pari.allocatemem(args.pari_stack_mb * 1024 * 1024)
    out: list[GeometryHit] = []
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
        hilbert = None
        if args.require_full_cycle:
            try:
                hilbert = pari.polclass(D)
            except Exception:
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
            if m <= args.max_m
            and gcd(m, h // m) == 1
            and len([component for component in coprime_components(m) if component > 2]) >= 2
        ]
        if not quotient_sizes:
            continue
        for q in sp.primerange(args.q_start, args.q_stop):
            if q <= h + 1:
                continue
            if args.require_full_cycle:
                assert hilbert is not None
                try:
                    roots = [int(root) for root in pari.polrootsmod(hilbert, int(q))]
                except Exception:
                    continue
                if len(roots) != h or find_full_cycle_prime(roots, D, int(q)) is None:
                    continue
            for m in quotient_sizes:
                out.extend(
                    geometry_hits_for(
                        D,
                        h,
                        int(q),
                        m,
                        args.max_extension_degree,
                        args.min_left_orbit_len,
                    )
                )
                if len(out) >= args.max_hits:
                    return out
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-h", type=int, default=300)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-abs-D", type=int, default=80_000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=30_000)
    parser.add_argument("--max-prime-quotients", type=int, default=16)
    parser.add_argument("--max-composite-quotients", type=int, default=48)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--max-m", type=int, default=420)
    parser.add_argument("--max-extension-degree", type=int, default=16)
    parser.add_argument("--min-left-orbit-len", type=int, default=3)
    parser.add_argument("--max-hits", type=int, default=20)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-full-cycle", action="store_true")
    parser.add_argument("--pari-stack-mb", type=int, default=256)
    args = parser.parse_args()

    hits = scan(args)
    print("Trace-GCD nonvacuous geometry filter")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_range=[{args.q_start},{args.q_stop})")
    print(f"max_extension_degree={args.max_extension_degree}")
    print(f"min_left_orbit_len={args.min_left_orbit_len}")
    print(f"require_full_cycle={int(args.require_full_cycle)}")
    print(f"hits={len(hits)}")
    print(
        "columns: D h q m n pair left_len right_lens right_orbits "
        "after_delete prefix_lengths tail_lengths ext_degree"
    )
    for hit in hits:
        print(
            f"row D={hit.D} h={hit.h} q={hit.q} m={hit.m} n={hit.n} "
            f"pair=({hit.left},{hit.right}) left_len={hit.left_len} "
            f"right_lens={list(hit.right_lens)} "
            f"right_orbits={hit.right_orbit_count} "
            f"after_delete=({hit.min_after_delete},{hit.max_after_delete}) "
            f"prefix_lengths={list(hit.prefix_lengths)} "
            f"tail_lengths={list(hit.tail_lengths)} "
            f"ext_degree={hit.extension_degree}"
        )
    print("interpretation")
    print("  geometry_hit_means_nonvacuous_rowspace_audit_is_dimension_possible=1")
    print("  hit_still_requires_split_prime_cycle_and_actual_cm_rowspace_check=1")
    print("conclusion=reported_trace_gcd_nonvacuous_geometry_filter")


if __name__ == "__main__":
    main()
