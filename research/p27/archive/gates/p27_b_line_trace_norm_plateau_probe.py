#!/usr/bin/env python3
"""Trace/norm bucket audit for p27 B-line plateau sets.

After the Frobenius audit killed proper-subfield and short-orbit explanations,
the next named Frobenius-invariant source candidates are trace and norm maps to
proper subfields.  This probe asks whether all-plus prefix survival is exactly
determined by trace, norm, or trace+norm buckets among legal B values.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from typing import Union

from p27_b_line_frobenius_plateau_probe import divisors, normalized_pattern, prefix_survives
from p27_b_line_prefix_extension_count_probe import collect_field
from p27_extension_prefix_count_probe import GF, find_irreducible


BucketKey = Union[int, tuple[int, int]]


def relative_trace(F: GF, value: int, degree: int) -> int:
    """Trace from GF(q^n) to the fixed GF(q^degree) subfield."""

    total = F.zero
    current = value
    steps = F.n // degree
    for _ in range(steps):
        total = F.add(total, current)
        current = F.pow(current, F.q**degree)
    return total


def relative_norm(F: GF, value: int, degree: int) -> int:
    """Norm from GF(q^n) to the fixed GF(q^degree) subfield."""

    if value == F.zero:
        return F.zero
    exponent = (F.q**F.n - 1) // (F.q**degree - 1)
    return F.pow(value, exponent)


def candidate_invariants(F: GF) -> list[tuple[str, Callable[[int], BucketKey]]]:
    invariants: list[tuple[str, Callable[[int], BucketKey]]] = []
    for degree in divisors(F.n):
        if degree == F.n:
            continue
        invariants.append((f"trace_to_{degree}", lambda value, d=degree: relative_trace(F, value, d)))
        invariants.append((f"norm_to_{degree}", lambda value, d=degree: relative_norm(F, value, d)))
        invariants.append(
            (
                f"trace_norm_to_{degree}",
                lambda value, d=degree: (
                    relative_trace(F, value, d),
                    relative_norm(F, value, d),
                ),
            )
        )
    return invariants


def classify_by_bucket(
    values: Iterable[int],
    selected: set[int],
    key_fn: Callable[[int], BucketKey],
) -> Counter:
    buckets: defaultdict[BucketKey, Counter] = defaultdict(Counter)
    for value in values:
        buckets[key_fn(value)]["selected" if value in selected else "rejected"] += 1

    stats: Counter = Counter()
    stats["buckets"] = len(buckets)
    stats["selected"] = len(selected)
    stats["total"] = sum(sum(counter.values()) for counter in buckets.values())
    for counter in buckets.values():
        size = sum(counter.values())
        stats[f"bucket_size_{size}"] += 1
        if counter["selected"] and counter["rejected"]:
            stats["mixed_buckets"] += 1
            stats["mixed_rows"] += size
            stats["mixed_selected_rows"] += counter["selected"]
            stats["mixed_rejected_rows"] += counter["rejected"]
        elif counter["selected"]:
            stats["pure_selected_buckets"] += 1
            stats["pure_selected_rows"] += counter["selected"]
        else:
            stats["pure_rejected_buckets"] += 1
            stats["pure_rejected_rows"] += counter["rejected"]
        stats["majority_correct_rows"] += max(counter["selected"], counter["rejected"])

    stats["exact_union_of_buckets"] = int(stats["mixed_buckets"] == 0)
    if stats["total"]:
        stats["majority_accuracy_x1000000"] = stats["majority_correct_rows"] * 1_000_000 // stats["total"]
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, n: int, max_gate: int) -> None:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    groups, collect_stats = collect_field(F, max_gate)
    patterns = {B: normalized_pattern(values, max_gate) for B, values in groups.items()}
    legal = set(patterns)
    invariants = candidate_invariants(F)

    print(f"GF({q}^{n}) N={F.size} max_gate={max_gate}:")
    print_counter("  collect_stats", collect_stats)
    print(f"  invariant_count = {len(invariants)}")

    for gate in range(3, max_gate + 1):
        selected = {B for B, pattern in patterns.items() if prefix_survives(pattern, gate)}
        if not legal:
            continue
        print(
            f"  gate{gate}_target: selected={len(selected)} "
            f"legal={len(legal)} rate={len(selected) / len(legal):.9f}"
        )
        if not selected:
            continue
        best_name = ""
        best_stats: Counter | None = None
        for name, key_fn in invariants:
            stats = classify_by_bucket(legal, selected, key_fn)
            print_counter(f"  gate{gate}_{name}", stats)
            if best_stats is None or stats["majority_accuracy_x1000000"] > best_stats["majority_accuracy_x1000000"]:
                best_name = name
                best_stats = stats
        if best_stats is not None:
            print(
                f"  gate{gate}_best_invariant = {best_name} "
                f"accuracy_x1000000={best_stats['majority_accuracy_x1000000']} "
                f"mixed_buckets={best_stats['mixed_buckets']} "
                f"exact={best_stats['exact_union_of_buckets']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23:3,103:2")
    parser.add_argument("--max-gate", type=int, default=10)
    args = parser.parse_args()

    print("p27 B-line trace/norm plateau probe")
    print("question = are prefix plateaus exact trace/norm bucket unions?")
    print(f"max_gate = {args.max_gate}")
    for spec in args.fields.split(","):
        if not spec.strip():
            continue
        q_raw, n_raw = spec.split(":", 1)
        run_field(int(q_raw), int(n_raw), args.max_gate)
    print("p27_b_line_trace_norm_plateau_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
