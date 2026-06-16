#!/usr/bin/env python3
"""p24 trace-lattice model for high-v2 and odd trace conditioning.

This enumerates the Hasse trace lattice

    |t| <= floor(2*sqrt(p))
    p + 1 - t is divisible by 2^d

and measures how target trace residues modulo odd factors cut that lattice.
It is a probability-model helper, not a curve sampler or verifier.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import combinations

P24 = 10**24 + 7
P24_TRACES = (1020608380936, -78903246840, -1178414874616)
P24_XONLY_TRACES = tuple(sorted(set(P24_TRACES) | {-t for t in P24_TRACES}))


@dataclass
class Accum:
    count: int = 0
    mass: float = 0.0

    def add(self, weight: float) -> None:
        self.count += 1
        self.mass += weight


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def trace_weight(t: int, p: int) -> float:
    root_p = math.sqrt(p)
    u = t / (2.0 * root_p)
    if abs(u) > 1.0:
        return 0.0
    return math.sqrt(max(0.0, 1.0 - u * u)) / (math.pi * root_p)


def lattice_traces(p: int, d: int, bound: int):
    modulus = 1 << d
    residue = (p + 1) % modulus
    first = -bound + ((residue + bound) % modulus)
    t = first
    while t <= bound:
        yield t
        t += modulus


def lattice_traces_for_residues(d: int, bound: int, residues: list[int]):
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


def fmt(acc: Accum, total: Accum) -> str:
    count_rate = acc.count / total.count if total.count else 0.0
    mass_rate = acc.mass / total.mass if total.mass else 0.0
    return f"{acc.count}/{total.count}:{count_rate:.6f} mass={mass_rate:.6f}"


def target_rows(traces: tuple[int, ...], ells: list[int]) -> list[tuple[int, int, int, str]]:
    rows = []
    for t in traces:
        order = P24 + 1 - t
        twist_order = P24 + 1 + t
        rows.append(
            (
                t,
                v2(order),
                v2(twist_order),
                ",".join(str(t % ell) for ell in ells),
            )
        )
    return rows


def residue_sets(traces: tuple[int, ...], ells: list[int]) -> dict[int, set[int]]:
    return {ell: {t % ell for t in traces} for ell in ells}


def two_adic_residues(p: int, d: int, xonly: bool) -> list[int]:
    residue = (p + 1) % (1 << d)
    if not xonly:
        return [residue]
    return [residue, -residue]


def summarize_combinations(
    p: int,
    d: int,
    bound: int,
    traces: tuple[int, ...],
    ells: list[int],
    xonly: bool,
) -> None:
    residues = residue_sets(traces, ells)
    lattice = list(lattice_traces_for_residues(d, bound, two_adic_residues(p, d, xonly)))
    weights = {t: trace_weight(t, p) for t in lattice}
    total = Accum(len(lattice), sum(weights.values()))

    print()
    print(f"combination_summary d={d} total={total.count} mass={total.mass:.12e}")
    for r in range(1, min(5, len(ells)) + 1):
        best: list[tuple[float, tuple[int, ...], Accum, float]] = []
        for combo in combinations(ells, r):
            acc = Accum()
            for t in lattice:
                if all(t % ell in residues[ell] for ell in combo):
                    acc.add(weights[t])
            ideal = math.prod(len(residues[ell]) / ell for ell in combo)
            rate = acc.mass / total.mass if total.mass else 0.0
            best.append((rate, combo, acc, ideal))
        best.sort()
        print(f"  size={r}")
        for rate, combo, acc, ideal in best[:8]:
            product = math.prod(combo)
            print(
                f"    combo={combo} product={product} "
                f"{fmt(acc, total)} ideal={ideal:.6e}"
            )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19, 29, 31, 37, 41, 71])
    ap.add_argument("--d-min", type=int, default=16)
    ap.add_argument("--d-max", type=int, default=40)
    ap.add_argument("--combo-d", type=int, default=40)
    ap.add_argument("--xonly", action="store_true", help="use signed traces, allowing the quadratic twist")
    args = ap.parse_args()

    p = P24
    bound = math.isqrt(4 * p)
    traces = P24_XONLY_TRACES if args.xonly else P24_TRACES
    residues = residue_sets(traces, args.ells)

    print("p24 trace-lattice high-v2 / odd-residue model")
    print(f"p={p}")
    print(f"hasse_trace_bound=floor(2sqrt(p))={bound}")
    print(f"ells={args.ells}")
    print(f"xonly_twist_symmetric={args.xonly}")
    print("target_traces=" + ",".join(str(t) for t in traces))
    for t, curve_two, twist_two, mods in target_rows(traces, args.ells):
        print(
            f"target_trace_detail t={t} "
            f"v2_order={curve_two} v2_twist_order={twist_two} residues={mods}"
        )
    print("target_residues=" + ",".join(f"ell{ell}:{sorted(residues[ell])}" for ell in args.ells))
    print()

    print("d total_count total_mass prefix conditional_count_rate conditional_mass_rate ideal_independent")
    for d in range(args.d_min, args.d_max + 1):
        total = Accum()
        prefix_acc = [Accum() for _ in args.ells]
        residues_2adic = two_adic_residues(p, d, args.xonly)
        for t in lattice_traces_for_residues(d, bound, residues_2adic):
            w = trace_weight(t, p)
            total.add(w)
            ok = True
            for i, ell in enumerate(args.ells):
                ok = ok and (t % ell in residues[ell])
                if ok:
                    prefix_acc[i].add(w)

        ideal = 1.0
        for i, ell in enumerate(args.ells):
            ideal *= len(residues[ell]) / ell
            print(
                f"{d:2d} {total.count:7d} {total.mass:.12e} "
                f"through_ell={ell:2d} {fmt(prefix_acc[i], total)} ideal={ideal:.6e}"
            )
        print()

    summarize_combinations(p, args.combo_d, bound, traces, args.ells, args.xonly)


if __name__ == "__main__":
    main()
