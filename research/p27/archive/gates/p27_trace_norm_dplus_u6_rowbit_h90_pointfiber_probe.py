#!/usr/bin/env python3
"""Small-field point-fiber descent for the Dplus U6 row bit.

The function-field factor test shows that the row-bit lift R(t,S^2-2) remains
irreducible over E_h90.  This weaker, finite-field probe asks a different
question:

    on rational small-field points, are row-bit fibers mixed over t, E_h90,
    the domain-spin cover, or the A_eta cover?

It is not a substitute for factorization.  It is a cheap compatibility screen:
mixed fibers over a base kill descent to that base; uniform fibers keep a
pointwise H90 compatibility signal alive.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Iterable


def parse_fields(raw: str) -> list[int]:
    return [int(part) for part in raw.replace(",", " ").split() if part.strip()]


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def chi(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1


def roots_square(a: int, q: int) -> list[int]:
    a %= q
    return [x for x in range(q) if x * x % q == a]


def sign_name(v: int) -> str:
    return {1: "plus", -1: "minus", 0: "zero"}.get(v, f"other_{v}")


def a_from_t(t: int, q: int) -> int:
    a = (t - inv(t, q)) % q
    return (pow(a, 4, q) * inv(4, q) - 2) % q


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
    key = (A % q, U % q)
    if key not in cache:
        cache[key] = [V for V in range(q) if f_a(A, U, V, q) == 0]
    return cache[key]


def row_signs_for_t(t: int, q: int, materialization_filters: bool) -> list[int]:
    A = a_from_t(t, q)
    X = x_from_t(t, q)
    cache: dict[tuple[int, int], list[int]] = {}
    signs: list[int] = []
    for U5 in transition_roots(A, X, q, cache):
        if materialization_filters and (chi(U5 * U5 - 4, q) != 1 or chi(U5 + A, q) != 1):
            continue
        for U6 in transition_roots(A, U5, q, cache):
            if materialization_filters and (chi(U6 * U6 - 4, q) != 1 or chi(U6 + A, q) != 1):
                continue
            sign = chi(U6 + 2, q)
            if sign in (-1, 1):
                signs.append(sign)
    return signs


def h90_values(t: int, q: int) -> tuple[int, int, int, int]:
    B = (t * t + 1) % q
    C = (t * t + 2 * t - 1) % q
    R = (t * t - 2 * t - 1) % q
    Fspin = t * C % q * B % q
    Ktrace = (-C * R) % q
    return B, C, Fspin, Ktrace


def extend_groups_for_t(
    q: int,
    t: int,
    signs: list[int],
    groups: dict[str, defaultdict[tuple[int, ...], list[int]]],
) -> Counter[str]:
    stats: Counter[str] = Counter()
    B, C, Fspin, Ktrace = h90_values(t, q)
    groups["t"][(t,)].extend(signs)
    stats["active_t"] += 1

    w_roots = roots_square(Ktrace, q)
    if not w_roots:
        stats["active_t_without_E_point"] += 1
    for w in w_roots:
        groups["E"][(t, w)].extend(signs)
        z_roots = roots_square(Fspin, q)
        if not z_roots:
            stats["E_points_without_Z_point"] += 1
        for z in z_roots:
            groups["Z"][(t, w, z)].extend(signs)
            for eta in (1, -1):
                Ueta = 2 * t % q * t % q * (t - 1) % q * B % q * B % q * ((eta * w + C) % q) % q
                Weta = (t - 1) % q * B % q * ((4 * t % q * t % q * t + eta * B % q * w) % q) % q
                Aeta = (Ueta + z * Weta) % q
                rho_roots = roots_square(Aeta, q)
                if not rho_roots:
                    stats[f"Z_points_without_Aeta_{sign_name(eta)}"] += 1
                label = "Aeta_plus" if eta == 1 else "Aeta_minus"
                for rho in rho_roots:
                    groups[label][(t, w, z, rho)].extend(signs)
    return stats


def summarize_groups(label: str, groups: dict[tuple[int, ...], list[int]]) -> Counter[str]:
    stats: Counter[str] = Counter()
    for values in groups.values():
        signs = set(values)
        stats[f"{label}_groups"] += 1
        stats[f"{label}_rows"] += len(values)
        stats[f"{label}_size_{len(values)}"] += 1
        if len(signs) == 1:
            stats[f"{label}_uniform_{sign_name(next(iter(signs)))}"] += 1
        else:
            stats[f"{label}_mixed"] += 1
            stats[f"{label}_mixed_rows"] += len(values)
    groups_count = stats[f"{label}_groups"]
    mixed = stats[f"{label}_mixed"]
    stats[f"{label}_mixed_x1000000"] = mixed * 1_000_000 // groups_count if groups_count else 0
    return stats


def collect_field(q: int, materialization_filters: bool) -> Counter[str]:
    groups: dict[str, defaultdict[tuple[int, ...], list[int]]] = {
        "t": defaultdict(list),
        "E": defaultdict(list),
        "Z": defaultdict(list),
        "Aeta_plus": defaultdict(list),
        "Aeta_minus": defaultdict(list),
    }
    stats: Counter[str] = Counter()
    t_mixed_without_E = 0
    t_mixed_with_E = 0

    signs_by_t: dict[int, list[int]] = {}
    for t in range(1, q):
        signs = row_signs_for_t(t, q, materialization_filters)
        if not signs:
            continue
        signs_by_t[t] = signs
        stats.update(extend_groups_for_t(q, t, signs, groups))

    for t, signs in signs_by_t.items():
        if len(set(signs)) <= 1:
            continue
        _B, _C, _Fspin, Ktrace = h90_values(t, q)
        if roots_square(Ktrace, q):
            t_mixed_with_E += 1
        else:
            t_mixed_without_E += 1
    stats["t_mixed_with_E_point"] = t_mixed_with_E
    stats["t_mixed_without_E_point"] = t_mixed_without_E

    for label, group in groups.items():
        stats.update(summarize_groups(label, group))
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run(fields: Iterable[int], materialization_filters: bool) -> None:
    print(f"materialization_filters = {int(materialization_filters)}")
    for q in fields:
        stats = collect_field(q, materialization_filters)
        print_counter(f"q{q}", stats)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71,167,199,263,607")
    parser.add_argument("--include-bare", action="store_true")
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    print("p27 trace/norm Dplus U6 row-bit H90 point-fiber probe")
    print("question = do small-field row-bit fibers descend over H90/domain-spin/Aeta rational points?")
    print(f"fields = {','.join(str(q) for q in fields)}")
    run(fields, materialization_filters=True)
    if args.include_bare:
        run(fields, materialization_filters=False)
    print("verdict:")
    print("  mixed fibers over a base kill pointwise descent to that base")
    print("  uniform fibers over E/Z/Aeta are compatibility evidence, not factorization proof")
    print("p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
