#!/usr/bin/env python3
"""Incidence test for the p27 conic-pair sampler against legal rows.

The direct conic-pair sampler is two-dimensional.  This probe checks whether
sampling it naively lands on legal label-2/compactD rows at a useful rate, or
whether it only helps after a separate legal pullback/quotient is found.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


def inv_table(p: int) -> list[int]:
    invs = [0] * p
    for a in range(1, p):
        invs[a] = pow(a, p - 2, p)
    return invs


def sqrt_table(p: int) -> list[list[int]]:
    roots: list[list[int]] = [[] for _ in range(p)]
    for x in range(p):
        roots[x * x % p].append(x)
    return roots


def conic_pair_sampler_stats(p: int) -> tuple[Counter, set[tuple[int, int]], Counter]:
    invs = inv_table(p)
    inv2 = invs[2]
    inv4 = invs[4]
    stats: Counter = Counter()
    image_ax: set[tuple[int, int]] = set()
    image_mult: Counter = Counter()

    for r_next in range(1, p):
        inv_r_next = invs[r_next]
        a_line = (r_next - inv_r_next) % p
        s = (r_next + inv_r_next) % p
        a2 = a_line * a_line % p
        for lam in range(1, p):
            stats["draws"] += 1
            a2_over_lam = a2 * invs[lam] % p
            d = (lam - a2_over_lam) * inv2 % p
            r = -(lam + a2_over_lam) * inv4 % p
            if r == 0:
                stats["degenerate_r"] += 1
                continue
            c = s * d % p * invs[(2 * r) % p] % p
            A = (2 - c * c) % p
            x = r * r % p
            key = (A, x)
            image_ax.add(key)
            image_mult[key] += 1
            stats["nondegenerate_outputs"] += 1

    stats["unique_A_x"] = len(image_ax)
    return stats, image_ax, image_mult


def raw_cr_image(p: int) -> set[tuple[int, int]]:
    return {
        ((2 - c * c) % p, r * r % p)
        for c in range(p)
        for r in range(p)
    }


def legal_sets(p: int) -> tuple[Counter, set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    legal: set[tuple[int, int]] = set()
    d3_plus: set[tuple[int, int]] = set()
    d3_minus: set[tuple[int, int]] = set()
    by_ax: defaultdict[tuple[int, int], Counter] = defaultdict(Counter)

    for cand in candidates:
        key = (int(cand["A"]), int(cand["x5"]))
        bits = candidate_bits(cand, p)
        legal.add(key)
        by_ax[key][bits.d3] += 1
        stats["oriented_legal_candidates"] += 1

    for key, hist in by_ax.items():
        stats["unique_legal_A_x"] += 1
        if hist[1] and not hist[-1]:
            d3_plus.add(key)
            stats["unique_d3_plus_A_x"] += 1
        elif hist[-1] and not hist[1]:
            d3_minus.add(key)
            stats["unique_d3_minus_A_x"] += 1
        elif hist[1] and hist[-1]:
            stats["unique_mixed_d3_A_x"] += 1
        else:
            stats["unique_d3_missing_A_x"] += 1

    return stats, legal, d3_plus, d3_minus


def screen_field(p: int, include_raw_cr: bool) -> Counter:
    stats, sampler_image, sampler_mult = conic_pair_sampler_stats(p)
    legal_stats, legal, d3_plus, d3_minus = legal_sets(p)
    stats.update(legal_stats)

    sampler_legal = sampler_image & legal
    sampler_plus = sampler_image & d3_plus
    sampler_minus = sampler_image & d3_minus
    stats["sampler_unique_legal_A_x"] = len(sampler_legal)
    stats["sampler_unique_d3_plus_A_x"] = len(sampler_plus)
    stats["sampler_unique_d3_minus_A_x"] = len(sampler_minus)
    stats["sampler_legal_draw_multiplicity"] = sum(sampler_mult[key] for key in sampler_legal)
    stats["sampler_d3_plus_draw_multiplicity"] = sum(sampler_mult[key] for key in sampler_plus)
    stats["sampler_d3_minus_draw_multiplicity"] = sum(sampler_mult[key] for key in sampler_minus)

    if include_raw_cr:
        raw_image = raw_cr_image(p)
        stats["raw_cr_unique_A_x"] = len(raw_image)
        stats["raw_cr_unique_legal_A_x"] = len(raw_image & legal)
        stats["raw_cr_unique_d3_plus_A_x"] = len(raw_image & d3_plus)
        stats["raw_cr_unique_d3_minus_A_x"] = len(raw_image & d3_minus)

    return stats


def print_counter(prefix: str, p: int, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    draws = stats["draws"]
    unique_image = stats["unique_A_x"]
    legal = stats["unique_legal_A_x"]
    plus = stats["unique_d3_plus_A_x"]
    if draws:
        print(
            "  sampler_legal_draw_rate = "
            f"{stats['sampler_legal_draw_multiplicity'] / draws:.9f}"
        )
        print(
            "  sampler_d3_plus_draw_rate = "
            f"{stats['sampler_d3_plus_draw_multiplicity'] / draws:.9f}"
        )
    if unique_image:
        print(
            "  sampler_legal_unique_rate = "
            f"{stats['sampler_unique_legal_A_x'] / unique_image:.9f}"
        )
        print(
            "  sampler_d3_plus_unique_rate = "
            f"{stats['sampler_unique_d3_plus_A_x'] / unique_image:.9f}"
        )
    if legal:
        print(
            "  legal_covered_by_sampler_rate = "
            f"{stats['sampler_unique_legal_A_x'] / legal:.9f}"
        )
    if plus:
        print(
            "  d3_plus_covered_by_sampler_rate = "
            f"{stats['sampler_unique_d3_plus_A_x'] / plus:.9f}"
        )
    print(f"  sampler_d3_plus_draw_rate_times_q = {stats['sampler_d3_plus_draw_multiplicity'] * p / draws if draws else 0.0:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="103,263,607,1607")
    parser.add_argument("--raw-cr-limit", type=int, default=700)
    args = parser.parse_args()

    print("p27 conic-pair sampler legal incidence probe")
    print("sampler parameters = nonzero R,L")
    print("image coordinate = (A=2-c^2, x=r^2)")
    for p in parse_ints(args.small_primes):
        include_raw_cr = p <= args.raw_cr_limit
        print_counter(f"q{p}", p, screen_field(p, include_raw_cr))
    print("p27_conic_pair_sampler_legal_incidence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
