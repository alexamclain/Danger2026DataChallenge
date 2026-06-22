#!/usr/bin/env python3
"""Fit-significance calibration for p27 K-line finite-field screens.

Several K-line probes ask whether a target bit is chi(f(K)) for a polynomial
or branch-divisor family.  Exact fits in small fields can be pure
interpolation when the candidate family is large compared with 2^rows.

This probe estimates the expected number of exact fits under a random-sign
model:

    expected_exact ~= 2 * family_size / 2^nrows

where the factor 2 allows a global polarity flip.  The estimate is only a
calibration, but it is enough to distinguish "q863 exact cubics are expected"
from "q1471 d3 exact cubics would be decisive".
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from dataclasses import dataclass

from p27_k_belyi_involution_probe import collect_rows


@dataclass(frozen=True)
class Family:
    name: str
    degree: int
    size_kind: str


FAMILIES = [
    Family("monic_cubic", 3, "monic"),
    Family("monic_quartic", 4, "monic"),
    Family("projective_cubic", 3, "projective"),
    Family("projective_quartic", 4, "projective"),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def family_size(q: int, family: Family) -> int:
    if family.size_kind == "monic":
        return q**family.degree
    if family.size_kind == "projective":
        return (q ** (family.degree + 1) - 1) // (q - 1)
    raise ValueError(family.size_kind)


def expected_exact(size: int, rows: int) -> float:
    return 2.0 * size / (2.0**rows)


def poisson_at_least_one(lam: float) -> float:
    if lam > 50:
        return 1.0
    return 1.0 - math.exp(-lam)


def verdict(lam: float) -> str:
    if lam >= 10:
        return "interpolation_likely"
    if lam >= 0.25:
        return "local_fit_not_decisive"
    if lam >= 0.01:
        return "exact_fit_interesting_needs_guard"
    return "exact_fit_decisive_if_stable"


def collect_counts(q: int) -> Counter:
    kd3, kd4, _sd3, _sd4, setup_stats = collect_rows(q)
    stats: Counter = Counter()
    stats["d3_rows"] = len(kd3)
    stats["d3_plus"] = sum(1 for row in kd3 if row.target == 1)
    stats["d3_minus"] = sum(1 for row in kd3 if row.target == -1)
    stats["d4_rows"] = len(kd4)
    stats["d4_plus"] = sum(1 for row in kd4 if row.target == 1)
    stats["d4_minus"] = sum(1 for row in kd4 if row.target == -1)
    for key, value in setup_stats.items():
        if key.endswith("_mixed_k_class"):
            stats[key] = value
    return stats


def print_field(q: int) -> None:
    counts = collect_counts(q)
    print(f"q={q}:")
    for key in sorted(counts):
        print(f"  {key} = {counts[key]}")
    for target in ("d3", "d4"):
        rows = counts[f"{target}_rows"]
        if rows <= 0:
            continue
        print(f"  {target}_fit_significance:")
        for family in FAMILIES:
            size = family_size(q, family)
            lam = expected_exact(size, rows)
            prob = poisson_at_least_one(lam)
            print(
                "    "
                f"{family.name}: family_size={size} "
                f"expected_exact={lam:.9g} "
                f"p_at_least_one={prob:.9g} "
                f"verdict={verdict(lam)}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,863,991,1471,1607,1847")
    args = parser.parse_args()

    print("p27 K-line fit-significance probe")
    print("model = random signs, exact up to global polarity")
    for q in parse_ints(args.small_primes):
        print_field(q)
    print("p27_kline_fit_significance_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
