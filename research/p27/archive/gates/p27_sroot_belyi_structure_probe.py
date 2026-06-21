#!/usr/bin/env python3
"""Branch structure of the rational S-root map for p27.

The rational square-root coordinate

    S = (U^2 - 4)/(2V),  K = S^2

is a map from the residual elliptic quotient to P^1_S.  This probe records its
branch values and tests whether the visible branch atoms explain d3/d4.  The
answer is no: the quadratic branch atoms are already square on selected rows,
while chi(S) is anti-invariant on the S/-S pairs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

import sympy as sp

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_sroot_branch_divisor_probe import SRow, collect_rows


@dataclass(frozen=True)
class BranchScore:
    name: str
    good: int
    total: int
    zeros: int
    polarity: int


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def symbolic_s_branch_data() -> dict[str, sp.Expr]:
    x, s = sp.symbols("X S")
    k_num = (x**2 - 2 * x - 1) ** 2 * (x**2 + 2 * x - 1) ** 2
    k_den = 4 * x * (x - 1) * (x + 1) * (x**2 + 1) ** 2
    relation = sp.expand(s**2 * k_den - k_num)
    branch_resultant = sp.factor(sp.resultant(relation, sp.diff(relation, x), x))
    derivative_num = sp.factor(sp.together(sp.diff(k_num / k_den, x)).as_numer_denom()[0])
    return {
        "S_relation": relation,
        "branch_resultant": branch_resultant,
        "derivative_num_via_K": derivative_num,
    }


def branch_atoms(q: int) -> list[tuple[str, Callable[[int], int]]]:
    return [
        ("S", lambda s: s % q),
        ("S2m2Sp2", lambda s: (s * s - 2 * s + 2) % q),
        ("S2p2Sp2", lambda s: (s * s + 2 * s + 2) % q),
        ("S2", lambda s: (s * s) % q),
    ]


def atom_distribution(rows: list[SRow], q: int) -> Counter:
    stats: Counter = Counter()
    for name, fn in branch_atoms(q):
        plus = 0
        minus = 0
        zero = 0
        for row in rows:
            chi = legendre(fn(row.s), q)
            if chi == 1:
                plus += 1
            elif chi == -1:
                minus += 1
            else:
                zero += 1
        stats[f"{name}_plus"] = plus
        stats[f"{name}_minus"] = minus
        stats[f"{name}_zero"] = zero
    return stats


def score_branch_products(rows: list[SRow], q: int) -> list[BranchScore]:
    atoms = branch_atoms(q)
    scores: list[BranchScore] = []
    for mask in range(1 << len(atoms)):
        name_parts = [atoms[i][0] for i in range(len(atoms)) if (mask >> i) & 1]
        name = "*".join(name_parts) if name_parts else "1"
        good_plus = 0
        good_minus = 0
        total = 0
        zeros = 0
        for row in rows:
            value = 1
            for i, (_, fn) in enumerate(atoms):
                if (mask >> i) & 1:
                    value = value * fn(row.s) % q
            chi = legendre(value, q)
            if chi == 0:
                zeros += 1
                continue
            total += 1
            if chi == row.target:
                good_plus += 1
            if chi == -row.target:
                good_minus += 1
        if good_plus >= good_minus:
            scores.append(BranchScore(name, good_plus, total, zeros, 1))
        else:
            scores.append(BranchScore(name, good_minus, total, zeros, -1))
    scores.sort(key=lambda score: (score.good / score.total if score.total else 0.0, score.good), reverse=True)
    return scores


def pair_stats(rows: list[SRow], q: int) -> Counter:
    by_s = {row.s: row.target for row in rows}
    stats: Counter = Counter()
    seen: set[int] = set()
    for row in rows:
        if row.s in seen:
            continue
        partner = (-row.s) % q
        if partner not in by_s:
            stats["missing_partner"] += 1
            seen.add(row.s)
            continue
        seen.add(row.s)
        seen.add(partner)
        stats["pairs"] += 1
        if by_s[partner] == row.target:
            stats["same_target_pairs"] += 1
        else:
            stats["mixed_target_pairs"] += 1
        if legendre(row.s, q) == -legendre(partner, q):
            stats["opposite_chi_s_pairs"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[BranchScore], limit: int) -> None:
    print(f"{prefix}:")
    for score in scores[:limit]:
        rate = score.good / score.total if score.total else 0.0
        print(
            f"  {score.name}: good={score.good}/{score.total} "
            f"rate={rate:.9f} zeros={score.zeros} polarity={score.polarity}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    print("p27 S-root branch-structure probe")
    data = symbolic_s_branch_data()
    print(f"branch_resultant = {data['branch_resultant']}")
    print(f"derivative_num_via_K = {data['derivative_num_via_K']}")
    print("finite branch atoms = S, S^2-2S+2, S^2+2S+2")
    print()
    for q in parse_ints(args.small_primes):
        sd3, sd4, setup_stats = collect_rows(q)
        print(f"q={q}:")
        print_counter("  setup_stats", setup_stats)
        for label, rows in [("d3", sd3), ("d4", sd4)]:
            print_counter(f"  {label}_pair_stats", pair_stats(rows, q))
            print_counter(f"  {label}_branch_atom_distribution", atom_distribution(rows, q))
            print_scores(f"  {label}_branch_atom_scores", score_branch_products(rows, q), args.top)
    print("p27_sroot_belyi_structure_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
