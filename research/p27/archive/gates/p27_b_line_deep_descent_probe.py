#!/usr/bin/env python3
"""Deep selected-gate descent test on the p27 B-line.

The B-source descent probe showed that d3 and d4 descend to the original
Bplus coordinate.  This probe asks the compounding question: do later selected
gate bits d5, d6, ... also descend to the same B value?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


def selected_gate_bits(A: int, x5: int, p: int, max_gate: int) -> tuple[int | None, ...]:
    """Return bits for gates d3..d_max_gate along the all-plus selected tower."""

    bits: list[int | None] = []
    active = [x5 % p]
    for _gate in range(3, max_gate + 1):
        values: list[int] = []
        next_active: set[int] = set()
        for x in active:
            d, branches = halve_all(A, x, p)
            if d != 1 or not branches:
                values.append(0)
                continue
            for branch in branches:
                chi = legendre(branch, p)
                values.append(chi)
                if chi == 1:
                    next_active.add(branch)
        bit = normalize(values)
        bits.append(bit)
        if bit != 1:
            break
        active = sorted(next_active)
        if not active:
            break
    while len(bits) < max_gate - 2:
        bits.append(None)
    return tuple(bits)


def collect_b_groups(candidates: list[dict[str, int]], p: int, max_gate: int) -> tuple[defaultdict[int, list[tuple[int | None, ...]]], Counter]:
    groups: defaultdict[int, list[tuple[int | None, ...]]] = defaultdict(list)
    stats: Counter = Counter()
    cache: dict[tuple[int, int], tuple[int | None, ...]] = {}
    for cand in dedupe_candidates(candidates):
        stats["deduped_candidates"] += 1
        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        d2, _branches = halve_all(A, x5, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        B = source_b_plus(int(cand["X"]) % p, p)
        if B is None:
            stats["b_degenerate"] += 1
            continue
        key = (A, x5)
        if key not in cache:
            cache[key] = selected_gate_bits(A, x5, p, max_gate)
        groups[B].append(cache[key])
        stats["d2_plus_candidates"] += 1
    stats["B_groups"] = len(groups)
    for values in groups.values():
        stats[f"B_group_size_{len(values)}"] += 1
    return groups, stats


def summarize_deep_descent(groups: defaultdict[int, list[tuple[int | None, ...]]], max_gate: int) -> Counter:
    stats: Counter = Counter()
    active_groups = set(groups)
    for index, gate in enumerate(range(3, max_gate + 1)):
        next_active: set[int] = set()
        for B in active_groups:
            values = [bits[index] for bits in groups[B] if bits[index] in (-1, 0, 1)]
            bit = normalize(values)
            label = "missing"
            if bit == 1:
                label = "plus"
                next_active.add(B)
            elif bit == -1:
                label = "minus"
            elif bit == 0:
                label = "mixed"
            stats[f"gate{gate}_{label}_B"] += 1
        stats[f"gate{gate}_active_B"] = len(active_groups)
        active_groups = next_active
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_prefix_table(
    label: str,
    group_stats: Counter,
    descent_stats: Counter,
    max_gate: int,
    source_draws: int | None,
) -> None:
    groups = group_stats["B_groups"]
    print(f"{label}_prefix_table:")
    print("  gate active plus minus mixed missing transition_rate prefix_rate scaled_half_loss source_draws_per_plus")
    for gate in range(3, max_gate + 1):
        active = descent_stats[f"gate{gate}_active_B"]
        plus = descent_stats[f"gate{gate}_plus_B"]
        minus = descent_stats[f"gate{gate}_minus_B"]
        mixed = descent_stats[f"gate{gate}_mixed_B"]
        missing = descent_stats[f"gate{gate}_missing_B"]
        transition = plus / active if active else 0.0
        prefix_rate = plus / groups if groups else 0.0
        depth = gate - 2
        scaled = plus * (2**depth) / groups if groups else 0.0
        if source_draws and plus:
            source_per_plus = source_draws / plus
            source_label = f"{source_per_plus:.6f}"
        else:
            source_label = "inf"
        print(
            f"  {gate} {active} {plus} {minus} {mixed} {missing} "
            f"{transition:.9f} {prefix_rate:.9f} {scaled:.9f} {source_label}"
        )


def run_candidates(
    label: str,
    candidates: list[dict[str, int]],
    p: int,
    max_gate: int,
    source_draws: int | None = None,
) -> None:
    groups, group_stats = collect_b_groups(candidates, p, max_gate)
    print_counter(f"{label}_b_group_stats", group_stats)
    descent_stats = summarize_deep_descent(groups, max_gate)
    print_counter(f"{label}_deep_descent_stats", descent_stats)
    print_prefix_table(label, group_stats, descent_stats, max_gate, source_draws)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=3000)
    parser.add_argument("--p27-heldout-target", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--max-gate", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line deep selected-gate descent probe")
    print("question = do d3,d4,d5,... descend to original Bplus?")
    print(f"max_gate = {args.max_gate}")

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats)
        run_candidates("p27_train", candidates, P, args.max_gate, sample_stats["sample_x_draws"])

    if args.p27_heldout_target:
        candidates, sample_stats = p27_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats)
        run_candidates("p27_heldout", candidates, P, args.max_gate, sample_stats["sample_x_draws"])

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print_counter(f"q{q}_enum_stats", enum_stats)
        run_candidates(f"q{q}", candidates, q, args.max_gate)

    print("p27_b_line_deep_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
