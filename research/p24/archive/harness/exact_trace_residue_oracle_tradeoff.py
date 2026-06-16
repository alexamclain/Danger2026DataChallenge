#!/usr/bin/env python3
"""Optimistic tradeoff for exact trace-residue construction.

Potential loophole:

    Maybe we do not need to orient an X0(N) subgroup.  Perhaps it is enough to
    impose exact trace residues modulo some level N; once the trace is one of
    the strict Hasse representatives, x0 construction is cheap.

This script prices a deliberately generous oracle:

* The oracle may impose the exact union of target trace residues modulo N.
* The construction cost is only the Gamma0(N) index, even though exact trace
  residues are richer than a bare X0(N) point.
* The remaining work is proportional to the number of Hasse traces left by
  that residue oracle.

Even under this generous model the product is Theta(sqrt(p)); changing N only
trades modular level against residual trace lifts.  This is the trace-residue
version of the X0/X1 orientation barrier.
"""

from __future__ import annotations

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
class Row:
    label: str
    level: int
    factorization: dict[int, int]
    gamma0: int
    survivor_count: int
    target_residue_count: int
    proxy: float


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def hasse_traces() -> list[int]:
    bound = math.isqrt(4 * P24)
    return list(range(-bound, bound + 1))


def survivor_count_for_level(level: int) -> tuple[int, int]:
    residues = {trace % level for trace in TARGET_TRACES}
    bound = math.isqrt(4 * P24)
    count = 0
    for residue in residues:
        first = -bound + ((residue + bound) % level)
        if first <= bound:
            count += ((bound - first) // level) + 1
    return count, len(residues)


def row(label: str, level: int) -> Row:
    survivors, residue_count = survivor_count_for_level(level)
    gamma0 = gamma0_index(level)
    # Expected oracle tries per strict target trace class, normalized so
    # survivor_count == len(TARGET_TRACES) means no residual trace search.
    proxy = gamma0 * max(1.0, survivors / len(TARGET_TRACES))
    return Row(label, level, sp.factorint(level), gamma0, survivors, residue_count, proxy)


def candidate_levels() -> list[tuple[str, int]]:
    levels: list[tuple[str, int]] = []
    for d in (16, 20, 24, 28, 32, 36, 40, 41):
        levels.append((f"2^{d}", 1 << d))
    # Levels near the width/6 and width thresholds, where an exact-residue
    # oracle could first isolate a constant number of Hasse representatives.
    width = 2 * math.isqrt(4 * P24) + 1
    for denom in (24, 12, 6, 3, 2, 1):
        n = max(3, width // denom)
        levels.append((f"width/{denom}", n))
    # Concrete mixed levels that looked best in earlier target-divisor audits.
    levels.extend(
        [
            ("mixed_best_gamma0", 1003580360576),
            ("hasse_width_best_gamma0", 2007160721152),
            ("odd_prime_cofactor", 454747350887),
            ("middle_large_odd", 43309271513),
            ("small_odd_21", 21),
        ]
    )
    # Deduplicate while preserving labels for first occurrence.
    seen: set[int] = set()
    out: list[tuple[str, int]] = []
    for label, level in levels:
        if level not in seen:
            seen.add(level)
            out.append((label, level))
    return out


def main() -> None:
    sqrt_p = math.isqrt(P24)
    width = 2 * math.isqrt(4 * P24) + 1
    print("p24 exact trace-residue oracle tradeoff")
    print(f"p={P24}")
    print(f"sqrt_floor_p={sqrt_p}")
    print(f"hasse_trace_interval_width={width}")
    print(f"target_trace_count={len(TARGET_TRACES)}")
    print()
    print(
        "label level factors gamma0/sqrt target_residues survivors "
        "oracle_proxy/sqrt"
    )

    rows = [row(label, level) for label, level in candidate_levels()]
    for item in sorted(rows, key=lambda r: r.proxy):
        print(
            f"{item.label:24s} {item.level:15d} {item.factorization!s:32s} "
            f"{item.gamma0 / sqrt_p:12.6f} {item.target_residue_count:15d} "
            f"{item.survivor_count:9d} {item.proxy / sqrt_p:17.6f}"
        )

    best = min(rows, key=lambda r: r.proxy)
    print()
    print("best_sampled_level")
    print(f"  label={best.label}")
    print(f"  level={best.level}")
    print(f"  survivors={best.survivor_count}")
    print(f"  gamma0_over_sqrt={best.gamma0 / sqrt_p:.6f}")
    print(f"  oracle_proxy_over_sqrt={best.proxy / sqrt_p:.6f}")
    print()
    print("interpretation")
    print("  exact_trace_residue_oracle_is_stronger_than_X0=1")
    print("  increasing_level_reduces_hasse_lifts_but_raises_gamma0=1")
    print("  sampled_best_proxy_constant_times_sqrt=1")
    print(
        "conclusion=unoriented_exact_trace_residue_construction_trades_constants_"
        "but_not_the_sqrt_exponent"
    )


if __name__ == "__main__":
    main()
