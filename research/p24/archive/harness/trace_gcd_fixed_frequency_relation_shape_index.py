#!/usr/bin/env python3
"""Geometry shortlist for fixed-frequency relation-section calibration rows.

The p24 no-fixed-defect theorem lives at right frequency length 35 with
Frobenius multiplier

    a |-> 22 a mod 35.

Actual-CM tests are only useful for the cyclic relation-section theorem when
the source dimension is large enough to contain at least one full right block
and a nonempty tail.  Rows with source dimension < 35 are tail-only and cannot
test `tau_a in image(P_a)` at the seven fixed frequencies.

This index deliberately stops before Hilbert polynomial construction.  It uses
only class numbers, quotient component shapes, splitting-by-Kronecker, and
Frobenius orbit arithmetic to find small candidates worth a later fixed-only
actual-CM audit.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd, lcm

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from l1_axis_injectivity_scan import discriminants


RIGHT_LEN = 35
P24_MULTIPLIER = 22
FIXED_FREQUENCY_COUNT = 7


@dataclass(frozen=True)
class RelationShapeHit:
    D: int
    h: int
    q: int
    m_min: int
    n_max: int
    components: tuple[int, ...]
    left: int
    left_orbit_rep: int
    left_len: int
    right: int
    right_orbit_count: int
    prefix_blocks: int
    tail_dim: int
    kept_blocks_after_delete: int
    fixed_frequency_count: int
    full_extension_degree: int
    fixed_only_extension_degree: int


@dataclass
class ScanStats:
    discriminants_seen: int = 0
    class_numbers_in_window: int = 0
    component_shapes: int = 0
    q_tests: int = 0
    kronecker_splits: int = 0
    right_component_cases: int = 0
    left_source_orbits: int = 0
    prefix_tail_shapes: int = 0
    quotient_subsets: int = 0


def component_subsets_containing(
    components: tuple[int, ...],
    required: tuple[int, ...],
    max_m: int,
) -> list[tuple[int, ...]]:
    required_set = set(required)
    rest = [component for component in components if component not in required_set]
    out: list[tuple[int, ...]] = []

    def rec(index: int, chosen: list[int], product: int) -> None:
        if product > max_m:
            return
        if index == len(rest):
            out.append(tuple(sorted(chosen)))
            return
        rec(index + 1, chosen, product)
        chosen.append(rest[index])
        rec(index + 1, chosen, product * rest[index])
        chosen.pop()

    start = list(required)
    start_product = 1
    for component in start:
        start_product *= component
    rec(0, start, start_product)
    return sorted(set(out), key=lambda row: (sp.prod(row), row))


def all_right_orbits_have_length(right: int, q: int, length: int) -> bool:
    orbits = q_orbits(right, q)
    return bool(orbits) and all(len(orbit) == length for orbit in orbits)


def fixed_frequency_count(multiplier: int, modulus: int) -> int:
    return sum(1 for a in range(modulus) if (multiplier * a - a) % modulus == 0)


def candidate_hits_for(
    D: int,
    h: int,
    q: int,
    args: argparse.Namespace,
    stats: ScanStats,
) -> list[RelationShapeHit]:
    if q % RIGHT_LEN != P24_MULTIPLIER:
        return []
    if gcd(q, h) != 1:
        return []
    components = tuple(component for component in coprime_components(h) if component > 2)
    if len(components) < 2:
        return []

    right_components = [
        component
        for component in components
        if component <= args.max_component
        and all_right_orbits_have_length(component, q, RIGHT_LEN)
    ]
    if not right_components:
        return []
    stats.right_component_cases += len(right_components)

    hits: list[RelationShapeHit] = []
    for right in right_components:
        right_orbit_count = len(q_orbits(right, q))
        for left in components:
            if left == right or left > args.max_component:
                continue
            for left_orbit in q_orbits(left, q):
                left_len = len(left_orbit)
                if left_len <= RIGHT_LEN:
                    continue
                if args.max_left_len and left_len > args.max_left_len:
                    continue
                if args.require_coprime_lens and gcd(left_len, RIGHT_LEN) != 1:
                    continue
                stats.left_source_orbits += 1
                prefix_blocks = left_len // RIGHT_LEN
                tail_dim = left_len - prefix_blocks * RIGHT_LEN
                if prefix_blocks < args.min_prefix_blocks or tail_dim <= 0:
                    continue
                kept_blocks = right_orbit_count - 1
                if kept_blocks <= prefix_blocks:
                    continue
                stats.prefix_tail_shapes += 1
                for subset in component_subsets_containing(
                    components,
                    (left, right),
                    args.max_m,
                ):
                    m_min = int(sp.prod(subset))
                    if h % m_min:
                        continue
                    n_max = h // m_min
                    if n_max < args.min_n or n_max > args.max_n:
                        continue
                    stats.quotient_subsets += 1
                    full_degree = 1
                    for component in subset:
                        full_degree = lcm(full_degree, int(sp.n_order(q % component, component)))
                    fixed_only_degree = int(sp.n_order(q % left, left))
                    hits.append(
                        RelationShapeHit(
                            D=D,
                            h=h,
                            q=q,
                            m_min=m_min,
                            n_max=n_max,
                            components=subset,
                            left=left,
                            left_orbit_rep=left_orbit[0],
                            left_len=left_len,
                            right=right,
                            right_orbit_count=right_orbit_count,
                            prefix_blocks=prefix_blocks,
                            tail_dim=tail_dim,
                            kept_blocks_after_delete=kept_blocks,
                            fixed_frequency_count=fixed_frequency_count(q % RIGHT_LEN, RIGHT_LEN),
                            full_extension_degree=full_degree,
                            fixed_only_extension_degree=fixed_only_degree,
                        )
                    )
                    if len(hits) >= args.max_hits_per_case:
                        return hits
    return hits


def scan(args: argparse.Namespace) -> tuple[list[RelationShapeHit], ScanStats]:
    pari = Pari()
    pari.allocatemem(args.pari_stack_mb * 1024 * 1024)
    stats = ScanStats()
    primes = [
        int(q)
        for q in sp.primerange(args.q_start, args.q_stop)
        if q % RIGHT_LEN == P24_MULTIPLIER
    ]
    out: list[RelationShapeHit] = []
    seen: set[int] = set()
    discriminant_count = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        stats.discriminants_seen += 1
        if D in seen:
            continue
        seen.add(D)
        try:
            h = int(pari.qfbclassno(D))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        stats.class_numbers_in_window += 1
        components = tuple(component for component in coprime_components(h) if component > 2)
        if len(components) < 2 or min(components) > args.max_component:
            continue
        stats.component_shapes += 1
        q_tests = 0
        for q in primes:
            if args.require_q_gt_h and q <= h + 1:
                continue
            if args.max_q_tests_per_D and q_tests >= args.max_q_tests_per_D:
                break
            q_tests += 1
            stats.q_tests += 1
            if gcd(q, D) != 1:
                continue
            if int(pari.kronecker(D, q)) != 1:
                continue
            stats.kronecker_splits += 1
            out.extend(candidate_hits_for(D, h, q, args, stats))
            if len(out) >= args.max_rows:
                return out[: args.max_rows], stats
        discriminant_count += 1
        if args.max_discriminants and discriminant_count >= args.max_discriminants:
            break
    return out[: args.max_rows], stats


def format_hit(hit: RelationShapeHit) -> str:
    return (
        f"D={hit.D} h={hit.h} q={hit.q} "
        f"m_min={hit.m_min} n_max={hit.n_max} "
        f"components={list(hit.components)} "
        f"left={hit.left}[{hit.left_orbit_rep}]:L{hit.left_len} "
        f"right={hit.right}:R35x{hit.right_orbit_count} "
        f"prefix_blocks={hit.prefix_blocks} tail_dim={hit.tail_dim} "
        f"kept_after_delete={hit.kept_blocks_after_delete} "
        f"fixed_freqs={hit.fixed_frequency_count} "
        f"full_ext={hit.full_extension_degree} "
        f"fixed_only_ext={hit.fixed_only_extension_degree}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-hits-per-case", type=int, default=4)
    parser.add_argument("--min-h", type=int, default=1000)
    parser.add_argument("--max-h", type=int, default=250_000)
    parser.add_argument("--max-abs-D", type=int, default=1_500_000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=300_000)
    parser.add_argument("--max-q-tests-per-D", type=int, default=60)
    parser.add_argument("--max-discriminants", type=int, default=0)
    parser.add_argument("--max-component", type=int, default=500)
    parser.add_argument("--max-left-len", type=int, default=120)
    parser.add_argument("--max-m", type=int, default=50_000)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=5_000)
    parser.add_argument("--min-prefix-blocks", type=int, default=1)
    parser.add_argument("--require-coprime-lens", action="store_true")
    parser.add_argument("--require-q-gt-h", action="store_true", default=True)
    parser.add_argument("--allow-q-le-h", dest="require_q_gt_h", action="store_false")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--pari-stack-mb", type=int, default=256)
    args = parser.parse_args()

    rows, stats = scan(args)
    print("Trace-GCD fixed-frequency relation-section shape index")
    print(f"right_len={RIGHT_LEN}")
    print(f"frobenius_mod_35={P24_MULTIPLIER}")
    print(f"target_fixed_frequency_count={FIXED_FREQUENCY_COUNT}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"max_h={args.max_h}")
    print(f"q_range=[{args.q_start},{args.q_stop})")
    print(f"max_q_tests_per_D={args.max_q_tests_per_D}")
    print(f"max_component={args.max_component}")
    print(f"max_left_len={args.max_left_len}")
    print(f"require_coprime_lens={int(args.require_coprime_lens)}")
    print(f"require_q_gt_h={int(args.require_q_gt_h)}")
    print()
    for row in rows:
        print(format_hit(row))
    print()
    print("summary")
    print(f"  hits={len(rows)}")
    print(f"  discriminants_seen={stats.discriminants_seen}")
    print(f"  class_numbers_in_window={stats.class_numbers_in_window}")
    print(f"  component_shapes={stats.component_shapes}")
    print(f"  q_tests={stats.q_tests}")
    print(f"  kronecker_splits={stats.kronecker_splits}")
    print(f"  right_component_cases={stats.right_component_cases}")
    print(f"  left_source_orbits={stats.left_source_orbits}")
    print(f"  prefix_tail_shapes={stats.prefix_tail_shapes}")
    print(f"  quotient_subsets={stats.quotient_subsets}")
    if rows:
        print(f"  min_full_extension_degree={min(row.full_extension_degree for row in rows)}")
        print(f"  min_fixed_only_extension_degree={min(row.fixed_only_extension_degree for row in rows)}")
        print(f"  max_prefix_blocks={max(row.prefix_blocks for row in rows)}")
        print(f"  tail_dims={sorted(set(row.tail_dim for row in rows))}")
    print("interpretation")
    print("  hit_has_p24_fixed_frequency_action=1")
    print("  hit_has_non_tail_only_prefix_tail_shape=1" if rows else "  hit_has_non_tail_only_prefix_tail_shape=0")
    print("  fixed_only_audit_can_avoid_full_35th_root_extension=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_relation_shape_index")


if __name__ == "__main__":
    main()
