#!/usr/bin/env python3
"""Extension-field B-line all-plus prefix counts for p27.

The deep p27 samples show that selected bits d3..d12 descend to the original
Bplus value.  This probe counts the descended B-line prefixes over small
extension fields as a lightweight falsifier for density anomalies before doing
heavier normalization.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable

from p27_b_line_extension_count_probe import core_b_values, source_b_plus
from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)
from p27_kline_reverse_z_extension_count_probe import parse_ints


def normalize(values: Iterable[int | None]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def selected_gate_bits(F: GF, A: int, x5: int, max_gate: int) -> tuple[int | None, ...]:
    """Return descended selected bits for gates d3..d_max_gate."""

    bits: list[int | None] = []
    active = [x5]
    for _gate in range(3, max_gate + 1):
        values: list[int] = []
        next_active: set[int] = set()
        for x in active:
            d, branches = halve_all(F, A, x)
            if d != 1 or not branches:
                values.append(0)
                continue
            for branch in branches:
                chi = F.squareclass(branch)
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


def collect_field(F: GF, max_gate: int) -> tuple[defaultdict[int, list[tuple[int | None, ...]]], Counter]:
    stats: Counter = Counter()
    groups: defaultdict[int, list[tuple[int | None, ...]]] = defaultdict(list)
    seen: set[tuple[int, int, int, int, int]] = set()
    bit_cache: dict[tuple[int, int], tuple[int | None, ...]] = {}

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
                    if key in seen:
                        stats["duplicate_candidate"] += 1
                        continue
                    seen.add(key)
                    stats["candidates"] += 1
                    d2, _branches = halve_all(F, A, x5)
                    if d2 != 1:
                        stats["d2_minus"] += 1
                        continue
                    stats["d2_plus_candidates"] += 1
                    ax_key = (A, x5)
                    if ax_key not in bit_cache:
                        bit_cache[ax_key] = selected_gate_bits(F, A, x5, max_gate)
                    groups[B].append(bit_cache[ax_key])

    stats["deduped_ax"] = len(bit_cache)
    stats["legal_B"] = len(groups)
    for values in groups.values():
        stats[f"B_group_size_{len(values)}"] += 1
    return groups, stats


def summarize_groups(groups: defaultdict[int, list[tuple[int | None, ...]]], max_gate: int) -> Counter:
    stats: Counter = Counter()
    active_groups = set(groups)
    stats["prefix_d2_legal_B"] = len(active_groups)
    for index, gate in enumerate(range(3, max_gate + 1)):
        next_active: set[int] = set()
        for B in active_groups:
            bit = normalize(bits[index] for bits in groups[B])
            if bit == 1:
                stats[f"gate{gate}_plus_B"] += 1
                next_active.add(B)
            elif bit == -1:
                stats[f"gate{gate}_minus_B"] += 1
            elif bit == 0:
                stats[f"gate{gate}_mixed_B"] += 1
            else:
                stats[f"gate{gate}_missing_B"] += 1
        stats[f"gate{gate}_active_B"] = len(active_groups)
        stats[f"prefix_gate{gate}_all_plus_B"] = len(next_active)
        active_groups = next_active
    return stats


def count_field(q: int, n: int, max_gate: int) -> Counter:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    stats: Counter = Counter()
    stats["field_size"] = F.size
    stats["modulus_degree"] = n

    core = core_b_values(F)
    stats["core_B"] = len(core)

    groups, group_stats = collect_field(F, max_gate)
    stats.update(group_stats)
    stats["legal_B_in_core"] = len(set(groups) & core)
    stats["legal_B_missing_core"] = len(set(groups) - core)
    stats["core_B_without_legal"] = len(core - set(groups))
    stats.update(summarize_groups(groups, max_gate))
    return stats


def print_stats(q: int, n: int, stats: Counter, max_gate: int) -> None:
    N = stats["field_size"]
    print(f"GF({q}^{n}) N={N}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print(f"  core_B/N = {stats.get('core_B', 0) / N:.9f}")
    print(f"  legal_B/N = {stats.get('legal_B', 0) / N:.9f}")
    if stats.get("core_B", 0):
        print(f"  legal_B/core_B = {stats.get('legal_B', 0) / stats['core_B']:.9f}")
    legal = stats.get("legal_B", 0)
    previous = legal
    for gate in range(3, max_gate + 1):
        plus = stats.get(f"prefix_gate{gate}_all_plus_B", 0)
        expected_scaled = (plus / legal * (2 ** (gate - 2))) if legal else 0.0
        step_rate = (plus / previous) if previous else 0.0
        print(
            f"  prefix_gate{gate}/legal_B = {(plus / legal if legal else 0.0):.9f} "
            f"step_rate={step_rate:.9f} scaled_by_half={expected_scaled:.6f}"
        )
        previous = plus


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=7)
    parser.add_argument("--degrees", default="1,2,3,4")
    parser.add_argument("--max-gate", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line prefix extension-count probe")
    print("B = 8 X^2/(X^2 - 1)^2, A+2=B^2")
    print("counts = legal B and all-plus prefixes for d3..dN")
    print(f"max_gate = {args.max_gate}")
    for n in parse_ints(args.degrees):
        print_stats(args.q, n, count_field(args.q, n, args.max_gate), args.max_gate)
    print("p27_b_line_prefix_extension_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
