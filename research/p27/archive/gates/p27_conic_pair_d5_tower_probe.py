#!/usr/bin/env python3
"""D5 tower screen after the p27 conic-pair d4 selector.

The d4 recurrence says that once a legal d3-plus conic-pair lift exists, the
next selector is

    chi(-(L+a)(L-a)cR).

This probe asks whether the same transition identity repeats one level later
on rows where d4 is plus, and whether the two-step coordinate re-enters the
original legal label-2/compactD source.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

from p27_conic_chain_source_probe import sqrt_table
from p27_conic_pair_d4_recurrence_probe import (
    Lift,
    conic_lifts,
    conic_lifts_modsqrt,
    inv,
    normalize_pm1,
    roots_mod,
)
from p27_conic_pair_sampler_legal_incidence_probe import legal_sets
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


@dataclass(frozen=True)
class DeepBits:
    d3: int | None
    d4: int | None
    d5: int | None


def branch_squareclass_after(a: int, x: int, p: int) -> int | None:
    _, branches = halve_all(a, x, p)
    return normalize_pm1([legendre(branch, p) for branch in branches])


def next_square_branches(a: int, x: int, p: int) -> list[int]:
    _, branches = halve_all(a, x, p)
    return [branch for branch in branches if legendre(branch, p) == 1]


def deep_bits_for_ax(a: int, x5: int, p: int) -> DeepBits:
    d3 = branch_squareclass_after(a, x5, p)
    if d3 != 1:
        return DeepBits(d3=d3, d4=None, d5=None)

    x6s = next_square_branches(a, x5, p)
    d4_values = [branch_squareclass_after(a, x6, p) for x6 in x6s]
    d4 = normalize_pm1([value for value in d4_values if value is not None])
    if d4 != 1:
        return DeepBits(d3=d3, d4=d4, d5=None)

    x7s: list[int] = []
    for x6 in x6s:
        x7s.extend(next_square_branches(a, x6, p))
    d5_values = [branch_squareclass_after(a, x7, p) for x7 in x7s]
    d5 = normalize_pm1([value for value in d5_values if value is not None])
    return DeepBits(d3=d3, d4=d4, d5=d5)


def transition_lifts_table(c: int, r: int, p: int, roots: list[list[int]]) -> list[Lift]:
    out: list[Lift] = []
    qp = (r * r + c * r + 1) % p
    qm = (r * r - c * r + 1) % p
    for h in roots[qp]:
        for g in roots[qm]:
            s = (h + g) % p
            disc = (s * s - 4) % p
            inv2 = inv(2, p)
            for delta in roots[disc]:
                candidates = [(s + delta) * inv2 % p]
                if delta:
                    candidates.append((s - delta) * inv2 % p)
                for nxt in candidates:
                    out.append(Lift(c=c, r=r, h=h, g=g, R=nxt))
    return out


def transition_lifts_modsqrt(c: int, r: int, p: int) -> list[Lift]:
    out: list[Lift] = []
    qp = (r * r + c * r + 1) % p
    qm = (r * r - c * r + 1) % p
    for h in roots_mod(qp, p):
        for g in roots_mod(qm, p):
            s = (h + g) % p
            disc = (s * s - 4) % p
            inv2 = inv(2, p)
            for delta in roots_mod(disc, p):
                candidates = [(s + delta) * inv2 % p]
                if delta:
                    candidates.append((s - delta) * inv2 % p)
                for nxt in candidates:
                    out.append(Lift(c=c, r=r, h=h, g=g, R=nxt))
    return out


def selector_product(lift: Lift, p: int) -> int:
    a = (lift.R - inv(lift.R, p)) % p
    L = (lift.h - lift.g - 2 * lift.r) % p
    value = (-(L + a) * (L - a) * lift.c * lift.R) % p
    return legendre(value, p)


def direct_selector(lift: Lift, p: int) -> int:
    return legendre((lift.R * lift.R + lift.c * lift.R + 1) % p, p)


def screen_ax(
    a: int,
    x5: int,
    p: int,
    first_lifts: list[Lift],
    second_lift_fn,
    legal: set[tuple[int, int]] | None,
    d3_plus: set[tuple[int, int]] | None,
    d3_minus: set[tuple[int, int]] | None,
) -> tuple[Counter, bool]:
    stats: Counter = Counter()
    bits = deep_bits_for_ax(a, x5, p)
    if bits.d3 != 1:
        return stats, False
    stats["d3_plus_unique_ax"] += 1
    if bits.d4 not in (-1, 1):
        stats["d4_not_normalized"] += 1
        return stats, False
    stats[f"d4_{bits.d4}_unique_ax"] += 1
    if bits.d4 != 1:
        return stats, False
    if bits.d5 not in (-1, 1):
        stats["d5_not_normalized"] += 1
        return stats, False
    stats["d4_plus_unique_ax"] += 1
    stats[f"d5_{bits.d5}_unique_ax"] += 1

    for first in first_lifts:
        if selector_product(first, p) != 1:
            continue
        stats["first_lifts_d4_plus"] += 1
        second_lifts = second_lift_fn(first.c, first.R)
        stats["second_lifts"] += len(second_lifts)
        if not second_lifts:
            stats["d4_plus_first_lift_without_second_lift"] += 1
            continue
        for second in second_lifts:
            product = selector_product(second, p)
            direct = direct_selector(second, p)
            if product != direct:
                stats["universal_product_mismatch"] += 1
            if direct != bits.d5:
                stats["d5_direct_mismatch"] += 1
            if product != bits.d5:
                stats["d5_product_mismatch"] += 1
            next_ax = (a, second.R * second.R % p)
            stats["x7_square_branches"] += 1
            if legal is not None:
                if next_ax in legal:
                    stats["x7_in_legal"] += 1
                if d3_plus is not None and next_ax in d3_plus:
                    stats["x7_in_legal_d3_plus"] += 1
                if d3_minus is not None and next_ax in d3_minus:
                    stats["x7_in_legal_d3_minus"] += 1

    return stats, True


def merge_counter(dst: Counter, src: Counter) -> None:
    for key, value in src.items():
        dst[key] += value


def screen_field(p: int) -> Counter:
    roots = sqrt_table(p)
    legal_stats, legal, d3_plus, d3_minus = legal_sets(p)
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"legal_{key}": value for key, value in legal_stats.items()})

    by_ax: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for cand in candidates:
        by_ax[(int(cand["A"]), int(cand["x5"]))].append(cand)

    for (a, x5) in by_ax:
        first_lifts = conic_lifts(a, x5, p, roots)
        ax_stats, used = screen_ax(
            a,
            x5,
            p,
            first_lifts,
            lambda c, r: transition_lifts_table(c, r, p, roots),
            legal,
            d3_plus,
            d3_minus,
        )
        merge_counter(stats, ax_stats)
        if used:
            stats["screened_d4_plus_ax"] += 1

    for key in ["x7_in_legal", "x7_in_legal_d3_plus", "x7_in_legal_d3_minus"]:
        stats.setdefault(key, 0)
    return stats


def screen_p27_sample(label: str, target: int, seed: int, max_draws: int) -> tuple[str, Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    stats["oriented_candidates"] = len(candidates)

    by_ax: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for cand in candidates:
        by_ax[(int(cand["A"]), int(cand["x5"]))].append(cand)
    stats["unique_ax"] = len(by_ax)

    for (a, x5) in by_ax:
        first_lifts = conic_lifts_modsqrt(a, x5, P)
        ax_stats, used = screen_ax(
            a,
            x5,
            P,
            first_lifts,
            lambda c, r: transition_lifts_modsqrt(c, r, P),
            None,
            None,
            None,
        )
        merge_counter(stats, ax_stats)
        if used:
            stats["screened_d4_plus_ax"] += 1

    return label, stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    second = stats["second_lifts"]
    if second:
        print(f"  d5_product_mismatch_rate = {stats['d5_product_mismatch'] / second:.9f}")
        print(f"  universal_product_mismatch_rate = {stats['universal_product_mismatch'] / second:.9f}")
        if "x7_in_legal" in stats:
            print(f"  x7_legal_reentry_rate = {stats['x7_in_legal'] / second:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=500)
    parser.add_argument("--p27-heldout-target", type=int, default=500)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--p27-max-draws", type=int, default=1000000)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    print("p27 conic-pair d5 tower probe")
    print("selector_product = chi(-(L+a)(L-a)cR) on each transition")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", screen_field(p))

    if not args.skip_p27:
        for label, stats in [
            screen_p27_sample("p27_train", args.p27_target, args.p27_seed, args.p27_max_draws),
            screen_p27_sample(
                "p27_heldout",
                args.p27_heldout_target,
                args.p27_heldout_seed,
                args.p27_max_draws,
            ),
        ]:
            print_counter(label, stats)

    print("p27_conic_pair_d5_tower_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
