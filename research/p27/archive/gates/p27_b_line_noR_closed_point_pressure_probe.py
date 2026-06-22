#!/usr/bin/env python3
"""Closed-point pressure for the p27 no-R reduced B-line cover.

This parses localized-cover layer-count logs and applies the standard Mobius
transform

    closed_n = (1/n) * sum_{d|n} mu(d) * #X(F_{q^(n/d)})

to the affine no-R counts.  It is a diagnostic, not a normalization result.
The aim is to identify which extension degrees must be respected by the
component/quotient/Prym CAS pass.
"""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_INPUTS = [
    Path("research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_7_7n2_20260622.txt"),
    Path("research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_23_20260622.txt"),
    Path("research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_20260622.txt"),
]


def mobius(n: int) -> int:
    m = n
    primes = 0
    d = 2
    while d * d <= m:
        if m % d == 0:
            m //= d
            primes += 1
            if m % d == 0:
                return 0
            while m % d == 0:
                m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        primes += 1
    return -1 if primes % 2 else 1


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def parse_counts(paths: list[Path]) -> dict[int, dict[int, dict[str, int]]]:
    counts: dict[int, dict[int, dict[str, int]]] = defaultdict(dict)
    header_re = re.compile(r"^GF\((\d+)\^(\d+)\) q=(\d+):$")
    value_re = re.compile(r"^  ([A-Za-z0-9_]+) = (\d+)$")

    for path in paths:
        base: int | None = None
        degree: int | None = None
        values: dict[str, int] = {}
        for raw_line in path.read_text().splitlines():
            line = raw_line.rstrip()
            header = header_re.match(line)
            if header:
                if base is not None and degree is not None:
                    counts[base][degree] = values
                base = int(header.group(1))
                degree = int(header.group(2))
                values = {"q": int(header.group(3))}
                continue
            match = value_re.match(line)
            if match and base is not None:
                values[match.group(1)] = int(match.group(2))
        if base is not None and degree is not None:
            counts[base][degree] = values
    return counts


def closed_points(series: dict[int, int], n: int) -> int | None:
    total = 0
    for d in divisors(n):
        degree = n // d
        if degree not in series:
            return None
        total += mobius(d) * series[degree]
    if total % n != 0:
        raise ValueError(f"nonintegral closed-point transform at n={n}: {total}/{n}")
    return total // n


def print_base(base: int, rows: dict[int, dict[str, int]]) -> None:
    max_n = max(rows)
    noR = {n: rows[n].get("noR_reduced_U_points", 0) for n in rows}
    gamma = {n: rows[n].get("noR_gamma_points", 0) for n in rows}

    print(f"base GF({base})")
    print("degree q noR_points noR_per_q gamma_points gamma_per_noR closed_noR closed_gamma")
    for n in range(1, max_n + 1):
        if n not in rows:
            print(f"{n} missing")
            continue
        qn = rows[n]["q"]
        c_noR = closed_points(noR, n)
        c_gamma = closed_points(gamma, n)
        gamma_per = gamma[n] / noR[n] if noR[n] else 0.0
        print(
            f"{n} {qn} {noR[n]} {noR[n] / qn:.9f} "
            f"{gamma[n]} {gamma_per:.9f} {c_noR} {c_gamma}"
        )

    low_nonzero = [n for n in range(1, max_n + 1) if n in rows and (closed_points(noR, n) or 0) > 0]
    coprime_low = []
    for i, a in enumerate(low_nonzero):
        for b in low_nonzero[i + 1 :]:
            if math.gcd(a, b) == 1:
                coprime_low.append((a, b))
    print(f"low_nonzero_closed_degrees = {low_nonzero}")
    print(f"coprime_nonzero_degree_pairs = {coprime_low[:8]}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", type=Path, default=DEFAULT_INPUTS)
    args = parser.parse_args()

    print("p27 B-line no-R closed-point/component pressure")
    print("interpretation = affine Mobius transform; use as CAS component/quotient routing")
    print()
    counts = parse_counts(args.inputs)
    for base in sorted(counts):
        print_base(base, counts[base])
    print("p27_b_line_noR_closed_point_pressure_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
