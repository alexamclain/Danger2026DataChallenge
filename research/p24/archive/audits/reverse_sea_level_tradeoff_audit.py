#!/usr/bin/env python3
"""Reverse-SEA trace-residue level tradeoff audit for p24.

Exact trace residues modulo odd primes can isolate the six strict x-only
target traces after a partial 2-adic prefix.  This is powerful as an oracle,
but a constructive reverse-SEA method would have to impose that modular
information by some growing-level modular condition.

This script quantifies the optimistic tradeoff.  For selected depths d, it:

1. enumerates the Hasse trace lattice with
   t == +/- (p+1) mod 2^d;
2. greedily adds exact odd trace-residue conditions until only the six target
   traces remain;
3. prices the combined information by the optimistic cyclic-level proxy
   N = 2^d * product(ell), reporting [SL2:Gamma0(N)] and [SL2:Gamma1(N)].

The proxy is deliberately generous: exact trace residues are richer than X0
cyclic-subgroup data, and marked/eigenvalue data is closer to Gamma1 or worse.
If even this optimistic Gamma0 proxy is not sub-sqrt, the reverse-SEA route is
not an asymptotic improvement.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from fractions import Fraction

import sympy as sp

P24 = 10**24 + 7
TARGET_TRACES = tuple(
    sorted({1020608380936, -78903246840, -1178414874616, -1020608380936, 78903246840, 1178414874616})
)


@dataclass(frozen=True)
class Tradeoff:
    depth: int
    initial_count: int
    repeat_lower_bound: int
    gamma0_lower_bound: int
    selected_ells: tuple[int, ...]
    selected_product: int
    final_count: int
    isolated: bool
    gamma0_index: int
    gamma1_index: int


def lattice_traces(depth: int) -> list[int]:
    bound = math.isqrt(4 * P24)
    modulus = 1 << depth
    residues = {(P24 + 1) % modulus, (-(P24 + 1)) % modulus}
    out: set[int] = set()
    for residue in residues:
        first = -bound + ((residue + bound) % modulus)
        t = first
        while t <= bound:
            out.add(t)
            t += modulus
    return sorted(out)


def target_residues(ell: int) -> set[int]:
    return {trace % ell for trace in TARGET_TRACES}


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def gamma1_index(n: int) -> int:
    value = Fraction(n * n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell * ell - 1, ell * ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def branch_repeat_lower_bound(depth: int) -> int:
    """Lower bound on odd modulus R needed by any exact-residue isolator.

    On each fixed 2-adic branch, traces form t_j = first + j*2^d.  For odd R,
    the same residue modulo R repeats every R positions in j.  If a target at
    index j has another branch point j +/- R inside the Hasse interval, then
    exact residues modulo R cannot isolate the target.  Thus R must exceed the
    target's distance to at least one branch boundary, for every target.
    """
    target_set = set(TARGET_TRACES)
    traces = lattice_traces(depth)
    if set(traces) == target_set:
        return 1

    bound = math.isqrt(4 * P24)
    modulus = 1 << depth
    residues = {(P24 + 1) % modulus, (-(P24 + 1)) % modulus}
    lower = 1
    for residue in residues:
        first = -bound + ((residue + bound) % modulus)
        branch: list[int] = []
        t = first
        while t <= bound:
            branch.append(t)
            t += modulus
        length = len(branch)
        for index, trace in enumerate(branch):
            if trace in target_set:
                lower = max(lower, max(index, length - 1 - index) + 1)
    return lower


def greedy_for_depth(depth: int, primes: list[int], max_steps: int) -> Tradeoff:
    survivors = lattice_traces(depth)
    initial_count = len(survivors)
    lower_bound = branch_repeat_lower_bound(depth)
    target_set = set(TARGET_TRACES)
    selected: list[int] = []
    product = 1

    step = 0
    while set(survivors) != target_set and step < max_steps:
        best: tuple[int, int, list[int]] | None = None
        for ell in primes:
            if ell in selected:
                continue
            residues = target_residues(ell)
            kept = [trace for trace in survivors if trace % ell in residues]
            row = (len(kept), ell, kept)
            if best is None or row[0] < best[0]:
                best = row
        if best is None or best[0] == len(survivors):
            break
        kept_count, ell, kept = best
        selected.append(ell)
        product *= ell
        survivors = kept
        step += 1

    level_proxy = (1 << depth) * product
    return Tradeoff(
        depth=depth,
        initial_count=initial_count,
        repeat_lower_bound=lower_bound,
        gamma0_lower_bound=gamma0_index(1 << depth) * lower_bound,
        selected_ells=tuple(selected),
        selected_product=product,
        final_count=len(survivors),
        isolated=set(survivors) == target_set,
        gamma0_index=gamma0_index(level_proxy),
        gamma1_index=gamma1_index(level_proxy),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--depths", type=int, nargs="+", default=[24, 26, 28, 30, 32, 34, 36, 38, 40])
    ap.add_argument("--max-ell", type=int, default=500)
    ap.add_argument("--max-steps", type=int, default=12)
    ap.add_argument("--max-initial-count", type=int, default=1_000_000)
    args = ap.parse_args()

    primes = [ell for ell in sp.primerange(3, args.max_ell + 1)]
    sqrt_p = math.isqrt(P24)
    print("p24 reverse-SEA exact-residue level tradeoff audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"depths={args.depths}")
    print(f"max_ell={args.max_ell}")
    print(f"max_steps={args.max_steps}")
    print(f"max_initial_count={args.max_initial_count}")
    print(
        "depth initial_count R_lower gamma0_lower/sqrt selected_ells product "
        "final isolated gamma0/sqrt gamma1/sqrt"
    )

    results: list[Tradeoff] = []
    for depth in args.depths:
        initial_count = len(lattice_traces(depth))
        if initial_count > args.max_initial_count:
            print(f"{depth:2d} {initial_count:13d} skip_initial_count_too_large")
            continue
        row = greedy_for_depth(depth, primes, args.max_steps)
        results.append(row)
        print(
            f"{row.depth:2d} {row.initial_count:13d} "
            f"{row.repeat_lower_bound:7d} {row.gamma0_lower_bound / sqrt_p:17.6f} "
            f"{','.join(str(ell) for ell in row.selected_ells) or '-':>24s} "
            f"{row.selected_product:12d} {row.final_count:5d} {int(row.isolated):8d} "
            f"{row.gamma0_index / sqrt_p:12.6f} {row.gamma1_index / sqrt_p:12.6e}"
        )

    isolated = [row for row in results if row.isolated]
    if isolated:
        best = min(isolated, key=lambda row: row.gamma0_index)
        print("best_isolating_gamma0")
        print(
            f"  depth={best.depth} selected_ells={best.selected_ells} "
            f"product={best.selected_product} gamma0={best.gamma0_index} "
            f"gamma0_over_sqrt={best.gamma0_index / sqrt_p:.6f}"
        )
    else:
        print("best_isolating_gamma0=none")

    print("conclusion=reverse_sea_exact_residue_construction_is_not_subsqrt_under_optimistic_level_proxy")


if __name__ == "__main__":
    main()
