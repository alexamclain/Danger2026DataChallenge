#!/usr/bin/env python3
"""Small-field descent audit for the Dplus reciprocal tower.

The p27 same-stream probes show that after Dplus the next class can be written
as chi(x6), with

    A = (t - 1/t)^4/4 - 2
    X = t^3 + 2*t^2 - 1/t
    F_A(X,U5) = 0
    F_A(U5,U6) = 0
    x6^2 - U6*x6 + 1 = 0.

This probe enumerates that reciprocal-coordinate tower over small prime fields
and checks where the x6 class descends.  It deliberately separates the bare
tower from the selected legal/core source cut: if the bare tower has mixed
A/B fibers, then CAS/GPU work must keep the selected-source equations rather
than treating the reciprocal tower alone as a source sampler.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict


def parse_fields(raw: str) -> list[int]:
    return [int(part) for part in raw.replace(",", " ").split() if part.strip()]


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def chi(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    v = pow(a, (q - 1) // 2, q)
    return 1 if v == 1 else -1


def sign_name(v: int) -> str:
    return {1: "plus", -1: "minus", 0: "zero"}.get(v, f"other_{v}")


def a_from_t(t: int, q: int) -> int:
    a = (t - inv(t, q)) % q
    return (pow(a, 4, q) * inv(4, q) - 2) % q


def b_from_t(t: int, q: int) -> int:
    t2 = t * t % q
    return (t2 - 1) % q * (t2 - 1) % q * inv(2 * t2, q) % q


def x_from_t(t: int, q: int) -> int:
    return (pow(t, 3, q) + 2 * t % q * t - inv(t, q)) % q


def f_a(A: int, U: int, V: int, q: int) -> int:
    v2m4 = (V * V - 4) % q
    return (
        v2m4 * v2m4
        - 4 * U % q * v2m4 % q * ((V + A) % q)
        + 16 * ((V + A) % q) * ((V + A) % q)
    ) % q


def transition_roots(A: int, U: int, q: int, cache: dict[tuple[int, int], list[int]]) -> list[int]:
    """Return [V : F_A(U,V)=0], caching only reached (A,U) pairs."""
    key = (A % q, U % q)
    if key not in cache:
        cache[key] = [V for V in range(q) if f_a(A, U, V, q) == 0]
    return cache[key]


def normalize_signs(values: list[int]) -> int | None:
    signs = {value for value in values if value in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def summarize_groups(label: str, groups: dict[int, list[int]]) -> Counter[str]:
    stats: Counter[str] = Counter()
    for values in groups.values():
        stats[f"{label}_size_{len(values)}"] += 1
        sign = normalize_signs(values)
        if sign is None:
            stats[f"{label}_missing"] += 1
        elif sign == 0:
            stats[f"{label}_mixed"] += 1
            stats[f"{label}_mixed_rows"] += len(values)
        else:
            stats[f"{label}_{sign_name(sign)}"] += 1
    stats[f"{label}_groups"] = len(groups)
    return stats


def collect_field(q: int, with_materialization_filters: bool) -> Counter[str]:
    stats: Counter[str] = Counter()
    root_cache: dict[tuple[int, int], list[int]] = {}
    d3_by_t: defaultdict[int, list[int]] = defaultdict(list)
    d3_by_a: defaultdict[int, list[int]] = defaultdict(list)
    d3_by_b: defaultdict[int, list[int]] = defaultdict(list)
    d3_by_a_b: defaultdict[int, list[int]] = defaultdict(list)

    for t in range(1, q):
        stats["t_nonzero"] += 1
        A = a_from_t(t, q)
        B = b_from_t(t, q)
        X = x_from_t(t, q)
        u5_roots = transition_roots(A, X, q, root_cache)
        stats[f"u5_root_count_{len(u5_roots)}"] += 1
        for U5 in u5_roots:
            if with_materialization_filters:
                c1 = chi(U5 * U5 - 4, q)
                c2 = chi(U5 + A, q)
                if c1 != 1 or c2 != 1:
                    stats[f"u5_filter_disc_{sign_name(c1)}_plusA_{sign_name(c2)}"] += 1
                    continue
            u6_roots = transition_roots(A, U5, q, root_cache)
            stats[f"u6_root_count_{len(u6_roots)}"] += 1
            for U6 in u6_roots:
                if with_materialization_filters:
                    c1 = chi(U6 * U6 - 4, q)
                    c2 = chi(U6 + A, q)
                    if c1 != 1 or c2 != 1:
                        stats[f"u6_filter_disc_{sign_name(c1)}_plusA_{sign_name(c2)}"] += 1
                        continue
                d3 = chi(U6 + 2, q)
                stats[f"d3_{sign_name(d3)}"] += 1
                if d3 == 0:
                    continue
                d3_by_t[t].append(d3)
                d3_by_a[A].append(d3)
                d3_by_b[B].append(d3)
                # B determines A by A=B^2-2, but keeping a joint key catches
                # accidental collisions if a future variant changes B.
                d3_by_a_b[(A * q + B) % (q * q)].append(d3)

    stats.update(summarize_groups("t", d3_by_t))
    stats.update(summarize_groups("A", d3_by_a))
    stats.update(summarize_groups("B", d3_by_b))
    stats.update(summarize_groups("AB", d3_by_a_b))
    stats["active_t"] = len(d3_by_t)
    stats["active_A"] = len(d3_by_a)
    stats["active_B"] = len(d3_by_b)
    stats["transition_root_cache_entries"] = len(root_cache)
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for group in ("t", "A", "B", "AB"):
        groups = stats[f"{group}_groups"]
        mixed = stats[f"{group}_mixed"]
        print(f"  {group}_mixed_rate = {(mixed / groups) if groups else 0.0:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="607,1607,1847")
    parser.add_argument(
        "--no-materialization-filters",
        action="store_true",
        help="Enumerate the bare F_A tower without U^2-4 and U+A square filters.",
    )
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    with_filters = not args.no_materialization_filters
    print("p27 trace/norm Dplus reciprocal tower small-field probe")
    print("question = where does chi(x6)=chi(U6+2) descend on the tower?")
    print(f"fields = {','.join(str(q) for q in fields)}")
    print(f"materialization_filters = {int(with_filters)}")
    for q in fields:
        stats = collect_field(q, with_filters)
        print_counter(f"q{q}", stats)
    print("verdict:")
    print("  zero A/B mixed groups would support a tower-level base class")
    print("  mixed A/B groups mean the selected legal/core source cut is essential")
    print("p27_trace_norm_dplus_reciprocal_tower_smallfield_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
