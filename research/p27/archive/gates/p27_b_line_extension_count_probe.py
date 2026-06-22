#!/usr/bin/env python3
"""Extension-field counts for the descended p27 B-line cover.

The B-source descent probe shows that d3 descends to

    B = 8 X^2 / (X^2 - 1)^2

on legal d2 rows over p27 samples and prime guard fields.  This probe counts
that descended B-line object over small extension fields, as a lightweight
substitute for full function-field normalization.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable

from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)
from p27_kline_reverse_z_extension_count_probe import parse_ints


def source_b_plus(F: GF, X: int) -> int | None:
    X2 = F.sqr(X)
    den = F.sub(X2, F.one)
    if den == 0:
        return None
    return F.div(F.mul(F.c(8), X2), F.sqr(den))


def branch1_l(F: GF, B: int) -> int | None:
    if B in (0, F.two, F.neg(F.two)):
        return None
    num = F.pow(F.sub(B, F.two), 4)
    den = F.mul(F.mul(F.c(8), B), F.sqr(F.add(B, F.two)))
    if den == 0:
        return None
    return F.div(num, den)


def core_b_values(F: GF) -> set[int]:
    """B values satisfying the branch-1 core bucket condition."""

    out: set[int] = set()
    for B in range(F.size):
        L = branch1_l(F, B)
        if L is None:
            continue
        if F.squareclass(F.add(B, F.two)) != 1:
            continue
        if F.squareclass(F.sub(B, F.two)) != -1:
            continue
        if F.squareclass(L) != 1:
            continue
        if any(F.squareclass(K) == 1 for K in F.roots(L)):
            out.add(B)
    return out


def normalize(values: Iterable[int | None]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def candidate_bits(F: GF, A: int, x5: int) -> tuple[int | None, int | None]:
    d2, x6s = halve_all(F, A, x5)
    if d2 != 1 or not x6s:
        return None, None
    d3_values: list[int] = []
    d4_values: list[int] = []
    for x6 in x6s:
        d3 = F.squareclass(x6)
        d3_values.append(d3)
        if d3 != 1:
            continue
        d3_next, x7s = halve_all(F, A, x6)
        if d3_next != 1 or not x7s:
            d4_values.append(0)
            continue
        d4_values.extend(F.squareclass(x7) for x7 in x7s)
    d3 = normalize(d3_values)
    d4 = normalize(d4_values) if d3 == 1 else None
    return d3, d4


def count_field(q: int, n: int) -> Counter:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    stats: Counter = Counter()
    stats["field_size"] = F.size
    stats["modulus_degree"] = n
    core = core_b_values(F)
    stats["core_B"] = len(core)

    seen_candidates: set[tuple[int, int, int, int, int]] = set()
    by_b: defaultdict[int, list[tuple[int | None, int | None]]] = defaultdict(list)

    for X in range(F.size):
        if X in (0, F.one):
            stats["skip_X_degenerate"] += 1
            continue
        X2 = F.sqr(X)
        W2 = F.sub(F.mul(X2, X), X)
        T2 = F.mul(F.mul(X, F.add(X2, F.one)), F.add(F.add(X2, F.mul(F.two, X)), F.neg(F.one)))
        B = source_b_plus(F, X)
        if B is None:
            stats["B_degenerate"] += 1
            continue
        for W in F.roots(W2):
            for T in F.roots(T2):
                if compact_class(F, X, W, T) != -1:
                    stats["compact_not_target"] += 1
                    continue
                stats["source_rows"] += 1
                for root_index in (0, 1):
                    reason, cand = label2_candidate(F, X, W, T, root_index)
                    if cand is None:
                        stats[f"candidate_invalid_{reason}"] += 1
                        continue
                    A, x5 = cand
                    key = (X, W, T, A, x5)
                    if key in seen_candidates:
                        stats["duplicate_candidate"] += 1
                        continue
                    seen_candidates.add(key)
                    stats["candidates"] += 1
                    d2, _ = halve_all(F, A, x5)
                    if d2 != 1:
                        stats["d2_minus"] += 1
                        continue
                    stats["d2_plus_candidates"] += 1
                    if F.sqr(B) != F.add(A, F.two):
                        stats["A_plus_2_identity_mismatch"] += 1
                    by_b[B].append(candidate_bits(F, A, x5))

    stats["legal_B"] = len(by_b)
    stats["legal_B_in_core"] = len(set(by_b) & core)
    stats["legal_B_missing_core"] = len(set(by_b) - core)
    stats["core_B_without_legal"] = len(core - set(by_b))

    group_sizes: Counter = Counter()
    for values in by_b.values():
        group_sizes[len(values)] += 1
        d3 = normalize(d3 for d3, _d4 in values)
        if d3 == 1:
            stats["B_d3_plus"] += 1
            d4 = normalize(d4 for _d3, d4 in values)
            if d4 == 1:
                stats["B_d4_plus"] += 1
            elif d4 == -1:
                stats["B_d4_minus"] += 1
            elif d4 == 0:
                stats["B_d4_mixed"] += 1
            else:
                stats["B_d4_missing"] += 1
        elif d3 == -1:
            stats["B_d3_minus"] += 1
        elif d3 == 0:
            stats["B_d3_mixed"] += 1
        else:
            stats["B_d3_missing"] += 1
    for size, count in group_sizes.items():
        stats[f"B_group_size_{size}"] = count
    return stats


def print_stats(q: int, n: int, stats: Counter) -> None:
    N = stats["field_size"]
    print(f"GF({q}^{n}) N={N}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for key in [
        "core_B",
        "legal_B",
        "B_d3_plus",
        "B_d3_minus",
        "B_d4_plus",
        "B_d4_minus",
    ]:
        print(f"  {key}/N = {stats.get(key, 0) / N:.9f}")
    if stats["core_B"]:
        print(f"  legal_B/core_B = {stats.get('legal_B', 0) / stats['core_B']:.9f}")
    if stats["legal_B"]:
        print(f"  B_d3_plus/legal_B = {stats.get('B_d3_plus', 0) / stats['legal_B']:.9f}")
    d3_plus = stats.get("B_d3_plus", 0)
    if d3_plus:
        print(f"  B_d4_plus/B_d3_plus = {stats.get('B_d4_plus', 0) / d3_plus:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=7)
    parser.add_argument("--degrees", default="1,2,3,4")
    args = parser.parse_args()

    print("p27 B-line extension-count probe")
    print("B = 8 X^2/(X^2 - 1)^2, A+2=B^2")
    print("counts = core B, legal d2 B, descended d3/d4 groups")
    for n in parse_ints(args.degrees):
        print_stats(args.q, n, count_field(args.q, n))
    print("p27_b_line_extension_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
