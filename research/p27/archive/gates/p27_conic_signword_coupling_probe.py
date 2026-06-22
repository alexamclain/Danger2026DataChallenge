#!/usr/bin/env python3
"""Conic-chain sign-word / prefix-coupling telemetry for p27.

The quadratic recurrence gives selected gate signs

    s_j = chi(r_j^2 + c*r_j + 1)

when A=2-c^2 and x_j=r_j^2.  A single positive sign is only a half-gate; a
sqrt-beating mechanism needs coupling across many signs or a source that
samples the all-plus tower cheaply.

This probe records the all-plus prefix profile on legal label-2 starts.  It is
the CPU-side bounded version of the GPU recurrence-coupling telemetry ask.
"""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Optional

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


Bit = Optional[int]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def selected_gate_bits(a: int, x0: int, p: int, max_depth: int) -> tuple[Bit, ...]:
    """Return selected conic signs through max_depth, stopping after failure.

    Depth 1 corresponds to d3 / s_3, depth 2 to d4 / s_4, etc.  Later signs
    are not F_p-observable after the first negative sign, because the next
    recurrence coordinate would live off the current square-root stratum.
    """

    bits: list[Bit] = []
    active = [x0 % p]
    for _depth in range(1, max_depth + 1):
        values: list[int] = []
        next_active: set[int] = set()
        for x in active:
            d_chi, branches = halve_all(a, x, p)
            if d_chi != 1 or not branches:
                values.append(-1)
                continue
            for branch in branches:
                chi = legendre(branch, p)
                values.append(chi)
                if chi == 1:
                    next_active.add(branch)
        bit = normalize(values)
        bits.append(bit)
        if bit != 1 or not next_active:
            break
        active = sorted(next_active)

    while len(bits) < max_depth:
        bits.append(None)
    return tuple(bits)


def candidates_to_unique_ax(candidates: list[dict[str, int]], p: int) -> dict[tuple[int, int], dict[str, int]]:
    by_ax: dict[tuple[int, int], dict[str, int]] = {}
    for cand in candidates:
        key = (int(cand["A"]) % p, int(cand["x5"]) % p)
        by_ax.setdefault(key, cand)
    return by_ax


def p27_candidates(target: int, seed: int, max_draws: int) -> tuple[dict[tuple[int, int], dict[str, int]], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sample_rows"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    by_ax = candidates_to_unique_ax(candidates, P)
    stats["unique_ax"] = len(by_ax)
    return by_ax, stats


def small_field_candidates(q: int) -> tuple[dict[tuple[int, int], dict[str, int]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    by_ax = candidates_to_unique_ax(candidates, q)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats["legal_candidates"] = len(candidates)
    stats["unique_ax"] = len(by_ax)
    return by_ax, stats


def summarize_bitwords(by_ax: dict[tuple[int, int], dict[str, int]], p: int, max_depth: int) -> Counter:
    stats: Counter = Counter()
    stats["rows"] = len(by_ax)
    pattern_counter: Counter = Counter()
    prefix_alive = [0] * (max_depth + 1)
    prefix_alive[0] = len(by_ax)

    for (a, x0) in by_ax:
        bits = selected_gate_bits(a, x0, p, max_depth)
        pattern = []
        first_stop = None
        alive = True
        for depth, bit in enumerate(bits, start=1):
            if bit == 1 and alive:
                prefix_alive[depth] += 1
                pattern.append("+")
                continue
            alive = False
            if bit == -1:
                pattern.append("-")
                if first_stop is None:
                    first_stop = depth
            elif bit == 0:
                pattern.append("0")
                if first_stop is None:
                    first_stop = depth
            else:
                pattern.append(".")
        if first_stop is None:
            stats[f"survives_depth{max_depth}"] += 1
        else:
            stats[f"first_stop_depth{first_stop}"] += 1
        pattern_counter["".join(pattern)] += 1

    for depth in range(1, max_depth + 1):
        previous = prefix_alive[depth - 1]
        current = prefix_alive[depth]
        stats[f"depth{depth}_prefix_plus"] = current
        stats[f"depth{depth}_previous_prefix"] = previous
        if stats["rows"]:
            stats[f"depth{depth}_prefix_rate_x1000000"] = current * 1_000_000 // stats["rows"]
            stats[f"depth{depth}_scaled_x1000000"] = current * (2 ** depth) * 1_000_000 // stats["rows"]
        if previous:
            stats[f"depth{depth}_transition_rate_x1000000"] = current * 1_000_000 // previous

    for pattern, count in pattern_counter.most_common(16):
        stats[f"pattern_{pattern}"] = count
    return stats


def print_counter(prefix: str, stats: Counter, max_depth: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    rows = stats["rows"]
    if rows:
        print(f"{prefix}_prefix_table:")
        print("  depth previous plus transition_rate prefix_rate scaled_half_loss")
        for depth in range(1, max_depth + 1):
            previous = stats[f"depth{depth}_previous_prefix"]
            plus = stats[f"depth{depth}_prefix_plus"]
            transition = plus / previous if previous else 0.0
            prefix_rate = plus / rows
            scaled = plus * (2 ** depth) / rows
            print(
                f"  {depth} {previous} {plus} "
                f"{transition:.9f} {prefix_rate:.9f} {scaled:.9f}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=4000)
    parser.add_argument("--p27-heldout-target", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=3000000)
    parser.add_argument("--max-depth", type=int, default=14)
    args = parser.parse_args()

    print("p27 conic sign-word coupling probe")
    print("depth d corresponds to selected gate d_{d+2}")
    print("test = all-plus prefix scaling for s_j=chi(r_j^2+c*r_j+1)")
    print(f"max_depth = {args.max_depth}")

    if args.p27_target:
        by_ax, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats, 0)
        print_counter("p27_train", summarize_bitwords(by_ax, P, args.max_depth), args.max_depth)

    if args.p27_heldout_target:
        by_ax, sample_stats = p27_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats, 0)
        print_counter("p27_heldout", summarize_bitwords(by_ax, P, args.max_depth), args.max_depth)

    for q in parse_ints(args.small_primes):
        by_ax, enum_stats = small_field_candidates(q)
        print_counter(f"q{q}_enum_stats", enum_stats, 0)
        print_counter(f"q{q}", summarize_bitwords(by_ax, q, args.max_depth), args.max_depth)

    print("p27_conic_signword_coupling_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
