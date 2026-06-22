#!/usr/bin/env python3
"""Exact cubic branch-support screen on the p27 B-line.

The B-line screens killed rational-linear support, irreducible quadratic plus
linears, and two-irreducible-quadratic support.  The remaining low-genus
branch family worth a direct finite-field check is a cubic on P1_B:

    f(B) = B^3 + a B^2 + b B + c.

If chi(f(B)) equals d3(B), up to global polarity, then z^2=f(B) is a genus-1
source candidate.  This probe tests that family exactly on finite fields by
treating the constant coefficient c as a shifted square/nonsquare bitset
intersection.  It is not a random coefficient fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps, mask_for_rows
from p27_kline_reverse_z_relation_probe import parse_ints


@dataclass(frozen=True)
class CubicHit:
    polarity: int
    coeffs: tuple[int, int, int]


def popcount(mask: int) -> int:
    return bin(mask).count("1")


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for a in range(1, p):
        r = pow(a, (p - 1) // 2, p)
        table[a] = 1 if r == 1 else -1
    return table


def first_bit(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def build_masks(p: int) -> dict[int, list[int]]:
    table = legendre_table(p)
    masks = {1: [], -1: []}
    for desired in (1, -1):
        for offset in range(p):
            mask = 0
            for c in range(p):
                if table[(c + offset) % p] == desired:
                    mask |= 1 << c
            masks[desired].append(mask)
    return masks


def bit_rows(label: str, q: int) -> tuple[list[tuple[int, int]], Counter]:
    d3, d4, stats = legal_b_maps(q)
    core = core_b_values(q)
    stats["core_B"] = len(core)
    stats["legal_B_in_core"] = len(set(d3) & core)
    stats["legal_B_missing_core"] = len(set(d3) - core)

    if label == "legal":
        rows = [(B, 0 if B in d3 else 1) for B in sorted(core)]
    elif label == "d3":
        rows = [(B, 0 if value == 1 else 1) for B, value in sorted(d3.items())]
    elif label == "d4":
        rows = [(B, 0 if value == 1 else 1) for B, value in sorted(d4.items())]
    else:
        raise ValueError(f"unknown family {label!r}")
    return rows, stats


def exact_monic_cubic_search(
    q: int,
    rows: list[tuple[int, int]],
    sample_limit: int,
) -> tuple[Counter, list[CubicHit]]:
    """Search B^3+aB^2+bB+c, allowing global squareclass polarity."""

    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["plus_rows"] = sum(1 for _B, bit in rows if bit == 0)
    stats["minus_rows"] = sum(1 for _B, bit in rows if bit == 1)
    stats["target_weight"] = popcount(mask_for_rows(rows))
    if not rows:
        stats["skipped_empty"] = 1
        return stats, []
    if stats["plus_rows"] == 0 or stats["minus_rows"] == 0:
        stats["skipped_one_sided"] = 1
        return stats, []

    masks = build_masks(q)
    all_c = (1 << q) - 1
    b_values = [B % q for B, _bit in rows]
    b2_values = [B * B % q for B in b_values]
    b3_values = [B * B % q * B % q for B in b_values]
    targets = [1 if bit == 0 else -1 for _B, bit in rows]
    hits: list[CubicHit] = []

    for a in range(q):
        for b in range(q):
            stats["ab_pairs"] += 1
            for polarity in (1, -1):
                intersection = all_c
                for i, target in enumerate(targets):
                    desired = polarity * target
                    offset = (b3_values[i] + a * b2_values[i] + b * b_values[i]) % q
                    intersection &= masks[desired][offset]
                    if not intersection:
                        break
                if intersection:
                    count = popcount(intersection)
                    stats[f"exact_polarity_{polarity}"] += count
                    if len(hits) < sample_limit:
                        hits.append(CubicHit(polarity=polarity, coeffs=(a, b, first_bit(intersection))))

    stats["exact_cubics"] = stats["exact_polarity_1"] + stats["exact_polarity_-1"]
    return stats, hits


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, families: list[str], sample_limit: int) -> None:
    print(f"q={q}:")
    for family in families:
        rows, source_stats = bit_rows(family, q)
        print_counter(f"q{q}_{family}_b_line_source_stats", source_stats)
        search_stats, hits = exact_monic_cubic_search(q, rows, sample_limit)
        print_counter(f"q{q}_{family}_monic_cubic_support_stats", search_stats)
        print(f"q{q}_{family}_monic_cubic_support_samples:")
        for hit in hits[:sample_limit]:
            a, b, c = hit.coeffs
            print(f"  polarity={hit.polarity} cubic=B^3+{a}*B^2+{b}*B+{c}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--families", default="d3")
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    families = [part.strip() for part in args.families.split(",") if part.strip()]
    print("p27 B-line exact monic cubic support probe")
    print("family = chi(B^3+aB^2+bB+c), global polarity allowed")
    print(f"small_primes = {args.small_primes}")
    print(f"families = {','.join(families)}")
    for q in parse_ints(args.small_primes):
        run_field(q, families, args.sample_limit)
    print("p27_b_line_cubic_support_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
