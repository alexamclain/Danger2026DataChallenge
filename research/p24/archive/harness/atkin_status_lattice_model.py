#!/usr/bin/env python3
"""Model odd-prime Atkin/Elkies status filters for p24 target traces.

Exact trace residues modulo ell are powerful but expensive to compute.  A
cheaper classical predicate is the Atkin/Elkies status:

    delta = t^2 - 4p mod ell

with delta square, nonsquare, or zero.  For a given ell, if all target traces
share only one status, an X0(ell)-style root/no-root predicate might give a
cheap half-bit filter.  If the signed x-only target traces already include both
square and nonsquare statuses, the predicate is useless.

This script enumerates the Hasse trace lattice and measures ideal status
filters, both target-only and in combination with a 2-adic prefix.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import combinations

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)
SIGNED_TARGET_TRACES = tuple(sorted(set(TARGET_TRACES) | {-t for t in TARGET_TRACES}))


@dataclass
class Accum:
    count: int = 0
    mass: float = 0.0

    def add(self, weight: float) -> None:
        self.count += 1
        self.mass += weight


def legendre(a: int, ell: int) -> int:
    a %= ell
    if a == 0:
        return 0
    v = pow(a, (ell - 1) // 2, ell)
    return -1 if v == ell - 1 else 1


def status(t: int, ell: int) -> int:
    return legendre(t * t - 4 * P24, ell)


def target_status_sets(traces: tuple[int, ...], ells: list[int]) -> dict[int, set[int]]:
    return {ell: {status(t, ell) for t in traces} for ell in ells}


def trace_weight(t: int) -> float:
    root_p = math.sqrt(P24)
    u = t / (2.0 * root_p)
    if abs(u) > 1:
        return 0.0
    return math.sqrt(max(0.0, 1.0 - u * u)) / (math.pi * root_p)


def lattice_traces(d: int):
    bound = math.isqrt(4 * P24)
    modulus = 1 << d
    residue = (P24 + 1) % modulus
    first = -bound + ((residue + bound) % modulus)
    t = first
    while t <= bound:
        yield t
        t += modulus


def lattice_traces_for_residues(d: int, residues: list[int]):
    bound = math.isqrt(4 * P24)
    modulus = 1 << d
    seen: set[int] = set()
    for residue in sorted({r % modulus for r in residues}):
        first = -bound + ((residue + bound) % modulus)
        t = first
        while t <= bound:
            if t not in seen:
                seen.add(t)
                yield t
            t += modulus


def two_adic_residues(d: int, xonly: bool) -> list[int]:
    residue = (P24 + 1) % (1 << d)
    if not xonly:
        return [residue]
    return [residue, -residue]


def fmt(acc: Accum, total: Accum) -> str:
    return (
        f"{acc.count}/{total.count}:{acc.count / total.count if total.count else 0:.6f} "
        f"mass={acc.mass / total.mass if total.mass else 0:.6f}"
    )


def summarize_prefix(d: int, traces: tuple[int, ...], ells: list[int], xonly: bool) -> None:
    target_sets = target_status_sets(traces, ells)
    all_traces = list(lattice_traces_for_residues(d, two_adic_residues(d, xonly)))
    status_cache = {(t, ell): status(t, ell) for t in all_traces for ell in ells}
    total = Accum()
    prefix = [Accum() for _ in ells]
    for t in all_traces:
        w = trace_weight(t)
        total.add(w)
        ok = True
        for i, ell in enumerate(ells):
            ok = ok and status_cache[(t, ell)] in target_sets[ell]
            if ok:
                prefix[i].add(w)

    print()
    print(f"prefix_summary d={d} total={total.count}")
    ideal = 1.0
    for i, ell in enumerate(ells):
        # Status distribution is approximately half square/half nonsquare with
        # a tiny zero class; use empirical prefix rates as the real model.
        ideal *= len(target_sets[ell]) / 3.0
        print(
            f"  through_ell={ell:3d} target_status={sorted(target_sets[ell])} "
            f"{fmt(prefix[i], total)} naive_status_ideal={ideal:.6e}"
        )


def summarize_combos(d: int, traces: tuple[int, ...], ells: list[int], max_size: int, xonly: bool) -> None:
    target_sets = target_status_sets(traces, ells)
    all_traces = list(lattice_traces_for_residues(d, two_adic_residues(d, xonly)))
    weights = {t: trace_weight(t) for t in all_traces}
    status_cache = {(t, ell): status(t, ell) for t in all_traces for ell in ells}
    total = Accum(len(all_traces), sum(weights.values()))

    print()
    print(f"combo_summary d={d} total={total.count}")
    for r in range(1, min(max_size, len(ells)) + 1):
        rows = []
        for combo in combinations(ells, r):
            acc = Accum()
            for t in all_traces:
                if all(status_cache[(t, ell)] in target_sets[ell] for ell in combo):
                    acc.add(weights[t])
            rows.append((acc.mass / total.mass if total.mass else 0.0, combo, acc))
        rows.sort()
        print(f"  size={r}")
        for _rate, combo, acc in rows[:10]:
            informative = sum(1 for ell in combo if len(target_sets[ell]) < 3)
            print(f"    combo={combo} informative={informative} {fmt(acc, total)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71])
    ap.add_argument("--d", type=int, default=28)
    ap.add_argument("--combo-size", type=int, default=5)
    ap.add_argument("--curve-only", action="store_true")
    args = ap.parse_args()

    traces = TARGET_TRACES if args.curve_only else SIGNED_TARGET_TRACES
    target_sets = target_status_sets(traces, args.ells)

    print("p24 Atkin/Elkies status lattice model")
    print(f"p={P24}")
    print(f"d={args.d}")
    print(f"curve_only={args.curve_only}")
    print(f"target_traces={traces}")
    for ell in args.ells:
        print(f"ell={ell:3d} target_status={sorted(target_sets[ell])}")

    summarize_prefix(args.d, traces, args.ells, not args.curve_only)
    summarize_combos(args.d, traces, args.ells, args.combo_size, not args.curve_only)


if __name__ == "__main__":
    main()
