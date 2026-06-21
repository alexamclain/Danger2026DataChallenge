#!/usr/bin/env python3
"""Kummer-line Belyi structure probe for p27.

The signed-doubling reduction leaves d3/d4 on the Kummer line

    K = x([2]P),  E': V^2 = U^3 + 4U.

This probe records the exact ramification of the residual-X map to K and tests
the nearest cheap consequence: whether the d3/d4 labels are just branch-value
characters of the resulting Belyi coordinate.  They are not, but the Belyi
normalization is useful for the next Magma/Sage branch-class extraction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable

import sympy as sp

from p27_eprime_double_kummer_line_probe import KRow, to_krows
from p27_equotient_2isogeny_line_probe import quotient_rows
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates


@dataclass(frozen=True)
class BranchScore:
    name: str
    good: int
    total: int
    zeros: int
    polarity: int


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def symbolic_belyi_data() -> dict[str, sp.Expr]:
    x, k = sp.symbols("X K")
    k_num = (x**2 - 2 * x - 1) ** 2 * (x**2 + 2 * x - 1) ** 2
    k_den = 4 * x * (x - 1) * (x + 1) * (x**2 + 1) ** 2
    relation = sp.expand(k * k_den - k_num)
    derivative_num = sp.factor(sp.together(sp.diff(k_num / k_den, x)).as_numer_denom()[0])
    branch_resultant = sp.factor(sp.resultant(relation, sp.diff(relation, x), x))
    return {
        "K_num": sp.factor(k_num),
        "K_den": sp.factor(k_den),
        "relation": relation,
        "derivative_num": derivative_num,
        "branch_resultant": branch_resultant,
        "belyi_lambda": sp.factor(-k**2 / 4),
    }


def collect_krows(q: int) -> tuple[list[KRow], list[KRow], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    d3_rows, d4_rows, quotient_stats = quotient_bit_rows_from_candidates(candidates, q)
    qd3, d3_iso_stats = quotient_rows(d3_rows, q)
    qd4, d4_iso_stats = quotient_rows(d4_rows, q)
    kd3, d3_k_stats = to_krows(qd3, q)
    kd4, d4_k_stats = to_krows(qd4, q)
    stats: Counter = Counter()
    stats.update({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    stats.update({f"d3_eprime_{key}": value for key, value in d3_iso_stats.items()})
    stats.update({f"d4_eprime_{key}": value for key, value in d4_iso_stats.items()})
    stats.update({f"d3_k_{key}": value for key, value in d3_k_stats.items()})
    stats.update({f"d4_k_{key}": value for key, value in d4_k_stats.items()})
    return kd3, kd4, stats


def branch_atoms(q: int) -> list[tuple[str, Callable[[int], int]]]:
    return [
        ("K", lambda k: k % q),
        ("K2p4", lambda k: (k * k + 4) % q),
        ("K2", lambda k: (k * k) % q),
    ]


def score_branch_products(rows: list[KRow], q: int) -> list[BranchScore]:
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
                    value = value * fn(row.k) % q
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
    scores.sort(key=lambda s: (s.good / s.total if s.total else 0, s.good, -s.zeros), reverse=True)
    return scores


def atom_distribution(rows: list[KRow], q: int) -> Counter:
    stats: Counter = Counter()
    for name, fn in branch_atoms(q):
        plus = 0
        minus = 0
        zero = 0
        for row in rows:
            chi = legendre(fn(row.k), q)
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


def lambda_collision_stats(rows: list[KRow], q: int) -> Counter:
    stats: Counter = Counter()
    by_lambda: dict[int, set[int]] = defaultdict(set)
    counts: Counter = Counter()
    for row in rows:
        lam = (-row.k * row.k * inv(4, q)) % q
        by_lambda[lam].add(row.target)
        counts[lam] += 1
    stats["rows"] = len(rows)
    stats["lambda_classes"] = len(by_lambda)
    stats["collision_classes"] = sum(1 for count in counts.values() if count > 1)
    stats["mixed_collision_classes"] = sum(
        1 for lam, targets in by_lambda.items() if counts[lam] > 1 and len(targets) > 1
    )
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[BranchScore]) -> None:
    print(f"{prefix}:")
    for score in scores:
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

    data = symbolic_belyi_data()
    print("p27 Kummer-line Belyi structure probe")
    print(f"K_num = {data['K_num']}")
    print(f"K_den = {data['K_den']}")
    print(f"branch_resultant = {data['branch_resultant']}")
    print(f"derivative_num = {data['derivative_num']}")
    print("finite branch values = K=0 and K^2+4=0")
    print("pole branch value = K=infinity, with double poles above X^2+1=0")
    print("Belyi coordinate lambda = -K^2/4 has branch values 0, 1, infinity")
    print()

    for q in parse_ints(args.small_primes):
        kd3, kd4, setup_stats = collect_krows(q)
        print(f"q={q}:")
        print_counter("  setup_stats", setup_stats)
        for label, rows in [("d3", kd3), ("d4", kd4)]:
            print_counter(f"  {label}_lambda_descent_stats", lambda_collision_stats(rows, q))
            print_counter(f"  {label}_branch_atom_distribution", atom_distribution(rows, q))
            print_scores(f"  {label}_branch_atom_scores", score_branch_products(rows, q)[: args.top])
    print("p27_kummer_belyi_structure_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
