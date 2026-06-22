#!/usr/bin/env python3
"""Exact extension-field prefix profile for the p27 B-line gate sequence.

The B-line deep-descent probe showed, on p27 samples, that the original
Bplus value determines selected gate bits through d12.  This probe asks the
next source-size question over exact small extension fields:

    how quickly do all-plus B values thin as d3,d4,d5,... are imposed?

If the B-line is going to beat sqrt by itself, the prefix counts should show a
non-random recurrence, dependency, or saturation.  Random independent Kummer
classes should keep the scaled count

    prefix_B(d3..dj) * 2^(j-2) / legal_B

near 1 until finite-field tails dominate.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Optional

from p27_b_line_extension_count_probe import source_b_plus
from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)
from p27_kline_reverse_z_extension_count_probe import parse_ints


Bit = Optional[int]


def strict_normalize(values: Iterable[Bit]) -> Bit:
    vals = {value for value in values if value is not None}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def selected_gate_bits(F: GF, A: int, x5: int, max_gate: int) -> tuple[Bit, ...]:
    """Return descended selected gate bits d3..d_max_gate for one legal row."""

    bits: list[Bit] = []
    active = {x5}
    for _gate in range(3, max_gate + 1):
        values: list[int] = []
        next_active: set[int] = set()
        for x in sorted(active):
            d, branches = halve_all(F, A, x)
            if d != 1 or not branches:
                values.append(0)
                continue
            for branch in branches:
                chi = F.squareclass(branch)
                values.append(chi)
                if chi == 1:
                    next_active.add(branch)
        bit = strict_normalize(values)
        bits.append(bit)
        if bit != 1:
            break
        active = next_active
        if not active:
            break
    while len(bits) < max_gate - 2:
        bits.append(None)
    return tuple(bits)


def collect_b_groups(F: GF, max_gate: int) -> tuple[defaultdict[int, list[tuple[Bit, ...]]], Counter]:
    groups: defaultdict[int, list[tuple[Bit, ...]]] = defaultdict(list)
    stats: Counter = Counter()
    seen_candidates: set[tuple[int, int, int, int, int]] = set()
    bit_cache: dict[tuple[int, int], tuple[Bit, ...]] = {}

    for X in range(F.size):
        X2 = F.sqr(X)
        B = source_b_plus(F, X)
        if B is None:
            stats["skip_B_degenerate"] += 1
            continue
        W2 = F.sub(F.mul(X2, X), X)
        T2 = F.mul(F.mul(X, F.add(X2, F.one)), F.add(F.add(X2, F.mul(F.two, X)), F.neg(F.one)))
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
                    d2, _branches = halve_all(F, A, x5)
                    if d2 != 1:
                        stats["d2_minus"] += 1
                        continue
                    if F.sqr(B) != F.add(A, F.two):
                        stats["A_plus_2_identity_mismatch"] += 1
                    ax_key = (A, x5)
                    if ax_key not in bit_cache:
                        bit_cache[ax_key] = selected_gate_bits(F, A, x5, max_gate)
                    groups[B].append(bit_cache[ax_key])
                    stats["d2_plus_candidates"] += 1

    stats["legal_B"] = len(groups)
    stats["unique_A_x5"] = len(bit_cache)
    for values in groups.values():
        stats[f"B_group_size_{len(values)}"] += 1
    return groups, stats


def bit_label(bit: Bit) -> str:
    if bit == 1:
        return "plus"
    if bit == -1:
        return "minus"
    if bit == 0:
        return "mixed_or_zero"
    return "missing"


def summarize_prefix(groups: defaultdict[int, list[tuple[Bit, ...]]], max_gate: int) -> Counter:
    stats: Counter = Counter()
    active = set(groups)
    legal_B = len(active)
    stats["initial_legal_B"] = legal_B
    for index, gate in enumerate(range(3, max_gate + 1)):
        next_active: set[int] = set()
        for B in active:
            bit = strict_normalize(bits[index] for bits in groups[B])
            stats[f"gate{gate}_{bit_label(bit)}_B"] += 1
            if bit == 1:
                next_active.add(B)
        stats[f"gate{gate}_active_B"] = len(active)
        stats[f"gate{gate}_prefix_plus_B"] = len(next_active)
        if legal_B:
            stats[f"gate{gate}_scaled_x1000000"] = (len(next_active) * (2 ** (gate - 2)) * 1_000_000) // legal_B
        active = next_active
    return stats


def summarize_patterns(groups: defaultdict[int, list[tuple[Bit, ...]]], max_gate: int) -> Counter:
    stats: Counter = Counter()
    for values in groups.values():
        pattern = tuple(strict_normalize(bits[index] for bits in values) for index in range(max_gate - 2))
        stats["pattern_" + ",".join(bit_label(bit) for bit in pattern)] += 1
        for index, bit in enumerate(pattern):
            if bit != 1:
                stats[f"first_stop_gate_{index + 3}_{bit_label(bit)}"] += 1
                break
        else:
            stats[f"survives_through_gate_{max_gate}"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, n: int, max_gate: int) -> None:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    groups, collect_stats = collect_b_groups(F, max_gate)
    prefix_stats = summarize_prefix(groups, max_gate)
    pattern_stats = summarize_patterns(groups, max_gate)
    print(f"GF({q}^{n}) N={F.size} max_gate={max_gate}:")
    print_counter("  collect_stats", collect_stats)
    print_counter("  prefix_stats", prefix_stats)
    print_counter("  pattern_stats", pattern_stats)

    legal_B = prefix_stats["initial_legal_B"]
    if legal_B:
        print("  scaled_prefix:")
        for gate in range(3, max_gate + 1):
            plus = prefix_stats[f"gate{gate}_prefix_plus_B"]
            scaled = plus * (2 ** (gate - 2)) / legal_B
            rate = plus / legal_B
            print(f"    gate{gate}: plus={plus} rate={rate:.9f} scaled={scaled:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=7)
    parser.add_argument("--degrees", default="1,2,3,4,5")
    parser.add_argument("--max-gate", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line extension prefix-profile probe")
    print("question = do B-line all-plus prefixes thin randomly or show coupling?")
    for n in parse_ints(args.degrees):
        run_field(args.q, n, args.max_gate)
    print("p27_b_line_prefix_profile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
