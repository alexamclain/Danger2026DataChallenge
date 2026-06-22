#!/usr/bin/env python3
"""Frobenius/subfield audit for p27 B-line all-plus plateaus.

The B-line extension ladder found field-local all-plus plateaus that die at
different gates.  This probe asks whether those plateau sets are explained by
proper subfields or short Frobenius orbits.  A subfield/source explanation
would be a concrete sampler lead; full-orbit field-local tails are evidence
against promoting the plateau counts as p27 structure.
"""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable

from p27_b_line_prefix_extension_count_probe import collect_field
from p27_extension_prefix_count_probe import GF, find_irreducible
from p27_kline_reverse_z_extension_count_probe import parse_ints


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def proper_divisors(n: int) -> list[int]:
    return [d for d in divisors(n) if d < n]


def min_subfield_degree(F: GF, value: int) -> int:
    for d in divisors(F.n):
        if F.pow(value, F.q**d) == value:
            return d
    return F.n


def frobenius_orbit_size(F: GF, value: int) -> int:
    seen: set[int] = set()
    current = value
    for step in range(1, F.n + 1):
        seen.add(current)
        current = F.pow(current, F.q)
        if current == value:
            return step
    return len(seen)


def normalized_pattern(values: Iterable[tuple[int | None, ...]], max_gate: int) -> tuple[int | None, ...]:
    pattern: list[int | None] = []
    for index in range(max_gate - 2):
        vals = {bits[index] for bits in values if bits[index] in (-1, 0, 1)}
        if not vals:
            pattern.append(None)
        elif len(vals) == 1:
            pattern.append(vals.pop())
        else:
            pattern.append(0)
    return tuple(pattern)


def prefix_survives(pattern: tuple[int | None, ...], gate: int) -> bool:
    return all(bit == 1 for bit in pattern[: gate - 2])


def first_stop_gate(pattern: tuple[int | None, ...]) -> str:
    for index, bit in enumerate(pattern):
        if bit != 1:
            label = "missing" if bit is None else ("mixed" if bit == 0 else "minus")
            return f"gate{index + 3}_{label}"
    return f"survives_gate{len(pattern) + 2}"


def summarize_set(F: GF, values: set[int]) -> Counter:
    stats: Counter = Counter()
    stats["count"] = len(values)
    if not values:
        return stats
    for value in values:
        stats[f"min_subfield_degree_{min_subfield_degree(F, value)}"] += 1
        stats[f"frobenius_orbit_{frobenius_orbit_size(F, value)}"] += 1
        for d in proper_divisors(F.n):
            if F.pow(value, F.q**d) == value:
                stats[f"in_GF_q^{d}"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, n: int, max_gate: int) -> None:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    groups, collect_stats = collect_field(F, max_gate)
    patterns = {B: normalized_pattern(values, max_gate) for B, values in groups.items()}
    print(f"GF({q}^{n}) N={F.size} max_gate={max_gate}:")
    print_counter("  collect_stats", collect_stats)
    print_counter("  all_legal_B", summarize_set(F, set(patterns)))

    legal_count = len(patterns)
    print("  prefix_survival_sets:")
    for gate in range(3, max_gate + 1):
        values = {B for B, pattern in patterns.items() if prefix_survives(pattern, gate)}
        stats = summarize_set(F, values)
        scaled = (len(values) * (2 ** (gate - 2)) / legal_count) if legal_count else 0.0
        print(
            f"    gate{gate}: count={len(values)} "
            f"rate={(len(values) / legal_count if legal_count else 0.0):.9f} "
            f"scaled={scaled:.9f}"
        )
        for key in sorted(stats):
            if key == "count":
                continue
            print(f"      {key} = {stats[key]}")

    stop_sets: dict[str, set[int]] = {}
    for B, pattern in patterns.items():
        stop_sets.setdefault(first_stop_gate(pattern), set()).add(B)
    print("  first_stop_sets:")
    for label in sorted(stop_sets):
        stats = summarize_set(F, stop_sets[label])
        print(f"    {label}: count={stats['count']}")
        for key in sorted(stats):
            if key == "count":
                continue
            print(f"      {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="7:5,7:6,23:3,103:2")
    parser.add_argument("--max-gate", type=int, default=10)
    args = parser.parse_args()

    print("p27 B-line Frobenius plateau probe")
    print("question = are all-plus plateau sets subfield/Frobenius-short sources?")
    print(f"max_gate = {args.max_gate}")
    for spec in args.fields.split(","):
        if not spec.strip():
            continue
        q_raw, n_raw = spec.split(":", 1)
        run_field(int(q_raw), int(n_raw), args.max_gate)
    print("p27_b_line_frobenius_plateau_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
