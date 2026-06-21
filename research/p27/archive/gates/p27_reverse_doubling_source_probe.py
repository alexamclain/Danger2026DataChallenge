#!/usr/bin/env python3
"""P27 reverse-doubling all-plus source screen.

The U+2 gate gives a real continuation-scope shrink, but the independent
Legendre precheck had a bad exchange rate.  This probe tests the next source
idea: reverse the next x-square condition through Montgomery doubling.

For q = x_next, Montgomery xDBL gives

    x_prev = (q^2 - 1)^2 / (4*q*(q^2 + A*q + 1)).

To source the all-plus gate, set q = z^2.  A legal rational half also needs
q^2 + A*q + 1 square, so the true source has z and a y-root for that factor.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_label2_alpha_branch_recurrence_probe import (
    P,
    compact_class,
    halve_all,
    inv,
    label2_candidate,
    legendre,
    sample_rows,
    sqrt_mod,
)


SMALL_PRIMES_Q7MOD8 = [23, 31, 47, 71, 79, 103, 127, 151, 167, 191, 199, 223, 239, 263, 271]


def roots_mod(a: int, p: int) -> list[int]:
    r = sqrt_mod(a, p)
    if r is None:
        return []
    if r == 0:
        return [0]
    return [r, (-r) % p]


def xdouble(a: int, q: int, p: int) -> int | None:
    den = 4 * q % p
    den = den * ((q * q + a * q + 1) % p) % p
    if den == 0:
        return None
    num = (q * q - 1) % p
    num = num * num % p
    return num * inv(den, p) % p


def label2_oriented_candidates_from_xwt(x: int, w: int, t: int, p: int) -> list[dict[str, int]]:
    out: list[dict[str, int]] = []
    for ri in [0, 1]:
        reason, cand = label2_candidate(x, w, t, ri, p)
        if cand is None:
            continue
        out.append(
            {
                "A": int(cand["A"]),
                "x5": int(cand["x5"]),
                "root_index": ri,
            }
        )
    return out


def all_oriented_candidates_from_row(row: dict[str, object], p: int = P) -> list[dict[str, int]]:
    x = int(row["X"])
    w = int(row["W"])
    t2 = x * (x * x + 1) % p
    t2 = t2 * ((x * x + 2 * x - 1) % p) % p
    out: list[dict[str, int]] = []
    for t in roots_mod(t2, p):
        for cand in label2_oriented_candidates_from_xwt(x, w, t, p):
            cand = dict(cand)
            cand["X"] = x
            cand["W"] = w
            cand["T"] = t
            out.append(cand)
    return out


def enumerate_small_prime_candidates(p: int) -> tuple[list[dict[str, int]], Counter]:
    out: list[dict[str, int]] = []
    stats: Counter = Counter()
    for x in range(p):
        for w in roots_mod((x * x * x - x) % p, p):
            t2 = x * (x * x + 1) % p
            t2 = t2 * ((x * x + 2 * x - 1) % p) % p
            for t in roots_mod(t2, p):
                comp = compact_class(x, w, t, p)
                if comp != -1:
                    stats["compact_not_target"] += 1
                    continue
                cands = label2_oriented_candidates_from_xwt(x, w, t, p)
                if not cands:
                    stats["no_label2_candidate"] += 1
                    continue
                for cand in cands:
                    cand = dict(cand)
                    cand["X"] = x
                    cand["W"] = w
                    cand["T"] = t
                    out.append(cand)
    return out, stats


def analyze_candidates(candidates: list[dict[str, int]], p: int) -> Counter:
    stats: Counter = Counter()
    unique_ax5: set[tuple[int, int]] = set()
    unique_ax5_plus: set[tuple[int, int]] = set()
    fiber_hist: Counter = Counter()
    by_ax5: defaultdict[tuple[int, int], int] = defaultdict(int)

    for cand in candidates:
        a = int(cand["A"])
        x5 = int(cand["x5"])
        ax5 = (a, x5)
        unique_ax5.add(ax5)
        by_ax5[ax5] += 1
        stats["oriented_candidates"] += 1
        d2_chi, x6s = halve_all(a, x5, p)
        if d2_chi != 1:
            stats["d2_not_square"] += 1
            continue
        if len(x6s) != 2:
            stats[f"x6_count_{len(x6s)}"] += 1
        branch_squareclasses = []
        source_z_points = 0
        source_zy_points = 0
        reverse_mismatch = 0
        point_mismatch = 0
        for x6 in x6s:
            stats["x6_branches"] += 1
            xd = xdouble(a, x6, p)
            if xd != x5 % p:
                reverse_mismatch += 1
            d3 = (x6 * x6 + a * x6 + 1) % p
            x6_chi = legendre(x6, p)
            d3_chi = legendre(d3, p)
            # Legal rational selected halves should satisfy chi(x6)=chi(d3).
            if x6_chi != d3_chi:
                point_mismatch += 1
            branch_squareclasses.append(x6_chi)
            if x6_chi == 1:
                stats["x6_square_branches"] += 1
                z_roots = len(roots_mod(x6, p))
                y_roots = len(roots_mod(d3, p))
                source_z_points += z_roots
                source_zy_points += z_roots * y_roots
        if reverse_mismatch:
            stats["reverse_mismatch"] += reverse_mismatch
        if point_mismatch:
            stats["point_mismatch"] += point_mismatch
        if branch_squareclasses:
            fiber_hist[tuple(sorted(branch_squareclasses))] += 1
            if all(c == 1 for c in branch_squareclasses):
                stats["d3_plus_candidates"] += 1
                unique_ax5_plus.add(ax5)
            elif all(c == -1 for c in branch_squareclasses):
                stats["d3_minus_candidates"] += 1
            else:
                stats["mixed_x6_squareclass_candidates"] += 1
        stats["reverse_z_points"] += source_z_points
        stats["reverse_zy_points"] += source_zy_points

    stats["unique_A_x5"] = len(unique_ax5)
    stats["unique_A_x5_d3_plus"] = len(unique_ax5_plus)
    for key, count in fiber_hist.items():
        stats[f"fiber_hist_{key}"] = count
    for _, count in by_ax5.items():
        stats[f"ax5_multiplicity_{count}"] += 1
    return stats


def print_stats(prefix: str, stats: Counter) -> None:
    oriented = stats["oriented_candidates"]
    d3_plus = stats["d3_plus_candidates"]
    x6_branches = stats["x6_branches"]
    x6_square = stats["x6_square_branches"]
    unique_ax5 = stats["unique_A_x5"]
    unique_plus = stats["unique_A_x5_d3_plus"]
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print(
        "  oriented_d3_plus_rate = "
        f"{(d3_plus / oriented) if oriented else 0.0:.9f}"
    )
    print(
        "  branch_square_rate = "
        f"{(x6_square / x6_branches) if x6_branches else 0.0:.9f}"
    )
    print(
        "  unique_A_x5_d3_plus_rate = "
        f"{(unique_plus / unique_ax5) if unique_ax5 else 0.0:.9f}"
    )
    print(
        "  reverse_z_points_per_oriented = "
        f"{(stats['reverse_z_points'] / oriented) if oriented else 0.0:.9f}"
    )
    print(
        "  reverse_zy_points_per_oriented = "
        f"{(stats['reverse_zy_points'] / oriented) if oriented else 0.0:.9f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--small-primes", default=",".join(str(p) for p in SMALL_PRIMES_Q7MOD8))
    args = parser.parse_args()

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    p27_candidates: list[dict[str, int]] = []
    for row in rows:
        p27_candidates.extend(all_oriented_candidates_from_row(row, P))
    # Deduplicate exact T/root duplicates while preserving genuinely different x5.
    seen: set[tuple[int, int, int, int, int]] = set()
    deduped = []
    for cand in p27_candidates:
        key = (cand["X"], cand["W"], cand["T"], cand["A"], cand["x5"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(cand)

    print("p27 reverse-doubling all-plus source probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"sampled_pairs = {len(rows)}")
    for key in sorted(sample_stats):
        print(f"sample_stat {key} = {sample_stats[key]}")
    print_stats("p27_sample_oriented_candidates", analyze_candidates(deduped, P))

    print("small_prime_enumeration:")
    primes = [int(part) for part in args.small_primes.split(",") if part.strip()]
    for prime in primes:
        if prime % 8 != 7:
            print(f"  q={prime} skipped_not_7_mod_8")
            continue
        cands, enum_stats = enumerate_small_prime_candidates(prime)
        stats = analyze_candidates(cands, prime)
        print(f"  q={prime}:")
        for key in sorted(enum_stats):
            print(f"    enum_{key} = {enum_stats[key]}")
        oriented = stats["oriented_candidates"]
        d3_plus = stats["d3_plus_candidates"]
        excess = d3_plus - oriented / 2
        print(f"    oriented_candidates = {oriented}")
        print(f"    unique_A_x5 = {stats['unique_A_x5']}")
        print(f"    d3_plus_candidates = {d3_plus}")
        print(f"    d3_plus_rate = {(d3_plus / oriented) if oriented else 0.0:.9f}")
        print(f"    d3_excess_over_half = {excess:.3f}")
        print(f"    x6_branches = {stats['x6_branches']}")
        print(f"    x6_square_branches = {stats['x6_square_branches']}")
        print(f"    branch_square_rate = {(stats['x6_square_branches'] / stats['x6_branches']) if stats['x6_branches'] else 0.0:.9f}")
        print(f"    reverse_mismatch = {stats['reverse_mismatch']}")
        print(f"    point_mismatch = {stats['point_mismatch']}")
        print(f"    reverse_z_points_per_oriented = {(stats['reverse_z_points'] / oriented) if oriented else 0.0:.9f}")
        print(f"    reverse_zy_points_per_oriented = {(stats['reverse_zy_points'] / oriented) if oriented else 0.0:.9f}")
        for key in sorted(k for k in stats if k.startswith("fiber_hist_")):
            print(f"    {key} = {stats[key]}")
    print("p27_reverse_doubling_source_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
