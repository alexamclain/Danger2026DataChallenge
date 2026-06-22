#!/usr/bin/env python3
"""K/Sroot selected-prefix profile for the p27 Kummer tower.

The reverse-z profile showed that, after imposing d3=+1, every Sroot fiber is
flat of degree 32 in the promotion fields.  This probe asks the source-size
question one step earlier: do the selected bits d3,d4,... descend to K or
Sroot, and do all-plus prefixes thin like fresh half-covers?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Optional

from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)
from p27_kline_reverse_z_extension_count_probe import ks_coordinates, parse_ints


Bit = Optional[int]


def strict_normalize(values: Iterable[Bit]) -> Bit:
    vals = {value for value in values if value is not None}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def bit_label(bit: Bit) -> str:
    if bit == 1:
        return "plus"
    if bit == -1:
        return "minus"
    if bit == 0:
        return "mixed_or_zero"
    return "missing"


def selected_gate_bits(F: GF, A: int, x5: int, max_gate: int) -> tuple[Bit, ...]:
    """Return selected gate bits d3..d_max_gate for one legal d2 row."""

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


def collect_groups(
    F: GF,
    max_gate: int,
) -> tuple[dict[str, defaultdict[int, list[tuple[Bit, ...]]]], Counter]:
    groups: dict[str, defaultdict[int, list[tuple[Bit, ...]]]] = {
        "K": defaultdict(list),
        "Sroot": defaultdict(list),
    }
    stats: Counter = Counter()
    seen_candidates: set[tuple[int, int, int, int, int]] = set()
    bit_cache: dict[tuple[int, int], tuple[Bit, ...]] = {}
    k_to_s: defaultdict[int, set[int]] = defaultdict(set)
    s_to_k: dict[int, int] = {}

    for X in range(F.size):
        if X in (0, F.one):
            stats["skip_X_degenerate"] += 1
            continue
        X2 = F.sqr(X)
        W2 = F.sub(F.mul(X2, X), X)
        T2 = F.mul(F.mul(X, F.add(X2, F.one)), F.add(F.add(X2, F.mul(F.two, X)), F.neg(F.one)))
        for W in F.roots(W2):
            ks = ks_coordinates(F, X, W)
            if ks is None:
                stats["ks_degenerate"] += 1
                continue
            K, Sroot = ks
            k_to_s[K].add(Sroot)
            prior_k = s_to_k.get(Sroot)
            if prior_k is not None and prior_k != K:
                stats["Sroot_to_mixed_K"] += 1
            s_to_k[Sroot] = K
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
                    stats["d2_plus_candidates"] += 1
                    ax_key = (A, x5)
                    if ax_key not in bit_cache:
                        bit_cache[ax_key] = selected_gate_bits(F, A, x5, max_gate)
                    bits = bit_cache[ax_key]
                    groups["K"][K].append(bits)
                    groups["Sroot"][Sroot].append(bits)

    stats["unique_A_x5"] = len(bit_cache)
    stats["unique_K_seen"] = len(k_to_s)
    stats["unique_Sroot_seen"] = len(s_to_k)
    stats["K_to_Sroot_size_hist_keys"] = len(Counter(len(v) for v in k_to_s.values()))
    for coord, coord_groups in groups.items():
        stats[f"legal_{coord}"] = len(coord_groups)
        for values in coord_groups.values():
            stats[f"{coord}_group_size_{len(values)}"] += 1
    return groups, stats


def summarize_prefix(groups: defaultdict[int, list[tuple[Bit, ...]]], max_gate: int) -> Counter:
    stats: Counter = Counter()
    active = set(groups)
    initial = len(active)
    stats["initial_groups"] = initial
    for index, gate in enumerate(range(3, max_gate + 1)):
        next_active: set[int] = set()
        for key in active:
            bit = strict_normalize(bits[index] for bits in groups[key])
            stats[f"gate{gate}_{bit_label(bit)}_groups"] += 1
            if bit == 1:
                next_active.add(key)
        stats[f"gate{gate}_active_groups"] = len(active)
        stats[f"gate{gate}_prefix_plus_groups"] = len(next_active)
        if initial:
            stats[f"gate{gate}_scaled_x1000000"] = (
                len(next_active) * (2 ** (gate - 2)) * 1_000_000
            ) // initial
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


def print_coord_summary(coord: str, groups: defaultdict[int, list[tuple[Bit, ...]]], max_gate: int) -> None:
    prefix_stats = summarize_prefix(groups, max_gate)
    pattern_stats = summarize_patterns(groups, max_gate)
    print_counter(f"  {coord}_prefix_stats", prefix_stats)
    print_counter(f"  {coord}_pattern_stats", pattern_stats)

    initial = prefix_stats["initial_groups"]
    if initial:
        print(f"  {coord}_scaled_prefix:")
        previous = initial
        for gate in range(3, max_gate + 1):
            plus = prefix_stats[f"gate{gate}_prefix_plus_groups"]
            rate = plus / initial
            step_rate = plus / previous if previous else 0.0
            scaled = plus * (2 ** (gate - 2)) / initial
            print(
                f"    gate{gate}: plus={plus} rate={rate:.9f} "
                f"step_rate={step_rate:.9f} scaled={scaled:.9f}"
            )
            previous = plus


def run_field(q: int, n: int, max_gate: int) -> None:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    groups, collect_stats = collect_groups(F, max_gate)
    print(f"GF({q}^{n}) N={F.size} max_gate={max_gate}:")
    print_counter("  collect_stats", collect_stats)
    for coord in ("K", "Sroot"):
        print_coord_summary(coord, groups[coord], max_gate)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=1607)
    parser.add_argument("--degrees", default="1")
    parser.add_argument("--max-gate", type=int, default=8)
    args = parser.parse_args()

    print("p27 K/Sroot prefix-profile probe")
    print("question = do K or Sroot selected prefixes thin randomly or show coupling?")
    print("source = residual E/T + compactD=-1 + label-2 candidate map")
    print("coordinates = K=x([2]P), Sroot^2=K")
    for n in parse_ints(args.degrees):
        run_field(args.q, n, args.max_gate)
    print("p27_sroot_prefix_profile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
