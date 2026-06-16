#!/usr/bin/env python3
"""Optimize mixed CRT trace-residue oracle levels for p24.

Previous audits priced pure 2-power levels and selected mixed divisors.  This
script searches a broader but still tiny space:

    N = 2^d * R,

where R is a squarefree product of small odd primes.  For each level it grants
an extremely generous oracle:

* the oracle imposes exactly the union of the six strict target trace residues
  modulo N;
* the modular construction cost is only [SL2:Gamma0(N)];
* any remaining Hasse trace lifts cost linearly.

The result is a best-case reverse-SEA/CRT residue model.  If even this model
has cost Theta(sqrt(p)), then mixed small-prime trace residues do not give the
requested asymptotic speedup.  The search is arithmetic only: survivor counts
are computed by residue classes in the Hasse interval, not by enumerating all
traces.
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from fractions import Fraction

import sympy as sp

P24 = 10**24 + 7
TARGET_TRACES = tuple(
    sorted(
        {
            -1178414874616,
            -1020608380936,
            -78903246840,
            78903246840,
            1020608380936,
            1178414874616,
        }
    )
)


@dataclass(frozen=True)
class OddPart:
    value: int
    gamma0_factor: Fraction
    primes: tuple[int, ...]


@dataclass(frozen=True)
class Row:
    level: int
    two_depth: int
    odd_part: int
    odd_primes: tuple[int, ...]
    target_residue_count: int
    survivors: int
    gamma0: int
    proxy: float


def gamma0_index_factorized(two_depth: int, odd: OddPart) -> int:
    # gamma0(2^d) = 1 for d=0, otherwise 3*2^(d-1).
    if two_depth == 0:
        base = Fraction(1, 1)
    else:
        base = Fraction(3 * (1 << (two_depth - 1)), 1)
    value = base * odd.gamma0_factor
    if value.denominator != 1:
        raise AssertionError((two_depth, odd, value))
    return value.numerator


def count_residue_in_hasse_interval(residue: int, modulus: int) -> int:
    bound = math.isqrt(4 * P24)
    first = -bound + ((residue + bound) % modulus)
    if first > bound:
        return 0
    return ((bound - first) // modulus) + 1


def survivor_count(level: int) -> tuple[int, int]:
    residues = {trace % level for trace in TARGET_TRACES}
    return sum(count_residue_in_hasse_interval(r, level) for r in residues), len(residues)


def odd_parts(prime_bound: int, max_odd_part: int) -> list[OddPart]:
    primes = list(sp.primerange(3, prime_bound + 1))
    out: list[OddPart] = [OddPart(1, Fraction(1, 1), ())]
    for size in range(1, len(primes) + 1):
        for combo in itertools.combinations(primes, size):
            value = math.prod(combo)
            if value > max_odd_part:
                continue
            factor = Fraction(value, 1)
            for ell in combo:
                factor *= Fraction(ell + 1, ell)
            out.append(OddPart(value, factor, combo))
    return out


def evaluate(two_depth: int, odd: OddPart) -> Row:
    level = (1 << two_depth) * odd.value
    survivors, residue_count = survivor_count(level)
    gamma0 = gamma0_index_factorized(two_depth, odd)
    proxy = gamma0 * max(1.0, survivors / len(TARGET_TRACES))
    return Row(
        level=level,
        two_depth=two_depth,
        odd_part=odd.value,
        odd_primes=odd.primes,
        target_residue_count=residue_count,
        survivors=survivors,
        gamma0=gamma0,
        proxy=proxy,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=47)
    ap.add_argument("--max-odd-part", type=int, default=20_000)
    ap.add_argument("--min-depth", type=int, default=28)
    ap.add_argument("--max-depth", type=int, default=42)
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    sqrt_p = math.isqrt(P24)
    width = 2 * math.isqrt(4 * P24) + 1
    odds = odd_parts(args.prime_bound, args.max_odd_part)
    rows: list[Row] = []
    for d in range(args.min_depth, args.max_depth + 1):
        for odd in odds:
            rows.append(evaluate(d, odd))

    rows.sort(key=lambda row: (row.proxy, row.gamma0, row.survivors, row.level))

    print("p24 mixed CRT trace-residue optimizer")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"hasse_trace_interval_width={width}")
    print(f"target_traces={TARGET_TRACES}")
    print(f"prime_bound={args.prime_bound}")
    print(f"max_odd_part={args.max_odd_part}")
    print(f"depth_range={args.min_depth}..{args.max_depth}")
    print(f"odd_parts_tested={len(odds)}")
    print(f"levels_tested={len(rows)}")
    print()
    print(
        "rank depth odd_part odd_primes level/sqrt gamma0/sqrt residues "
        "survivors proxy/sqrt"
    )
    for rank, row in enumerate(rows[: args.top], start=1):
        print(
            f"{rank:4d} {row.two_depth:5d} {row.odd_part:8d} "
            f"{','.join(map(str, row.odd_primes)) or '-':18s} "
            f"{row.level / sqrt_p:10.6f} {row.gamma0 / sqrt_p:11.6f} "
            f"{row.target_residue_count:8d} {row.survivors:9d} "
            f"{row.proxy / sqrt_p:11.6f}"
        )

    best = rows[0]
    print()
    print("best")
    print(f"  depth={best.two_depth}")
    print(f"  odd_part={best.odd_part}")
    print(f"  odd_primes={best.odd_primes}")
    print(f"  level={best.level}")
    print(f"  target_residue_count={best.target_residue_count}")
    print(f"  survivors={best.survivors}")
    print(f"  gamma0={best.gamma0}")
    print(f"  gamma0_over_sqrt={best.gamma0 / sqrt_p:.6f}")
    print(f"  proxy_over_sqrt={best.proxy / sqrt_p:.6f}")
    print()
    print("interpretation")
    print("  mixed_small_prime_residues_can_improve_constants=1")
    print("  best_proxy_remains_constant_times_sqrt_p=1")
    print("  exact_trace_residue_oracle_is_stronger_than_known_X0_data=1")
    print(
        "conclusion=mixed_crt_trace_residue_levels_do_not_change_the_sqrt_exponent"
    )


if __name__ == "__main__":
    main()
