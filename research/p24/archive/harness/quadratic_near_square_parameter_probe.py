#!/usr/bin/env python3
"""Probe degree-2 rational formulas in the family p = n^2 + 7.

The LFT probes test (a*n+b)/(c*n+d).  Since the family itself is quadratic in
n, a hidden near-square section could reasonably have the form

    (a*n^2 + b*n + c) / (d*n^2 + e*n + f).

This script reuses the exact small-field marker sets from the X1(16) and
Legendre probes, then intersects them with all primitive degree-2 rational
functions of bounded coefficient height.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from functools import reduce
from itertools import product

from legendre_near_square_parameter_probe import (
    prime_rows,
    split_strict_good_parameters,
)
from x16_near_square_section_probe import good_parameter_sets as x16_good_parameter_sets


@dataclass(frozen=True)
class QuadraticFormula:
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int

    def eval(self, n: int, p: int) -> int | None:
        num = (self.a * n * n + self.b * n + self.c) % p
        den = (self.d * n * n + self.e * n + self.f) % p
        if den == 0:
            return None
        return num * pow(den, p - 2, p) % p

    def label(self) -> str:
        return (
            f"({self.a}*n^2+{self.b}*n+{self.c})/"
            f"({self.d}*n^2+{self.e}*n+{self.f})"
        )


def proportional(left: tuple[int, int, int], right: tuple[int, int, int]) -> bool:
    return all(left[i] * right[j] == left[j] * right[i] for i in range(3) for j in range(i + 1, 3))


def normalize(coeffs: tuple[int, int, int, int, int, int]) -> QuadraticFormula | None:
    a, b, c, d, e, f = coeffs
    if (a, b, c) == (0, 0, 0) or (d, e, f) == (0, 0, 0):
        return None
    if proportional((a, b, c), (d, e, f)):
        return None
    g = reduce(math.gcd, (abs(x) for x in coeffs))
    if g:
        a, b, c, d, e, f = (x // g for x in coeffs)
    first = next(x for x in (a, b, c, d, e, f) if x != 0)
    if first < 0:
        a, b, c, d, e, f = (-a, -b, -c, -d, -e, -f)
    return QuadraticFormula(a, b, c, d, e, f)


def quadratic_formulas(bound: int) -> list[QuadraticFormula]:
    seen: set[QuadraticFormula] = set()
    vals = range(-bound, bound + 1)
    for coeffs in product(vals, repeat=6):
        q = normalize(coeffs)
        if q is not None:
            seen.add(q)
    return sorted(
        seen,
        key=lambda row: (
            sum(abs(x) for x in (row.a, row.b, row.c, row.d, row.e, row.f)),
            row.a,
            row.b,
            row.c,
            row.d,
            row.e,
            row.f,
        ),
    )


def marker_set(p: int, mode: str):
    if mode.startswith("legendre-"):
        return split_strict_good_parameters(p, mode.removeprefix("legendre-"))
    if mode.startswith("x16-"):
        return x16_good_parameter_sets(p, mode.removeprefix("x16-"))
    raise ValueError(mode)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        choices=["legendre-root", "legendre-lambda", "legendre-landen", "x16-y", "x16-y2", "x16-u"],
        default="legendre-lambda",
    )
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--coeff-bound", type=int, default=3)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = quadratic_formulas(args.coeff_bound)
    hits = {f: 0 for f in fs}
    valid = {f: 0 for f in fs}
    survivors = set(fs)

    print("quadratic near-square parameter formula probe")
    print("family=p=n^2+7")
    print(f"mode={args.mode}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"formula_count={len(fs)}")

    for index, (n, p) in enumerate(rows, start=1):
        marked, stats = marker_set(p, args.mode)
        next_survivors: set[QuadraticFormula] = set()
        for f in fs:
            value = f.eval(n, p)
            if value is None or value == 0:
                continue
            valid[f] += 1
            if bool(marked[value]):
                hits[f] += 1
                if f in survivors:
                    next_survivors.add(f)
        survivors = next_survivors
        detail = " ".join(f"{key}={value}" for key, value in stats.items() if key != "fft_error_scaled")
        print(
            f"row={index:02d} n={n} p={p} {detail} "
            f"survivors_all_rows_so_far={len(survivors)}"
        )

    ranked = sorted(
        fs,
        key=lambda f: (
            hits[f],
            valid[f],
            -sum(abs(x) for x in (f.a, f.b, f.c, f.d, f.e, f.f)),
        ),
        reverse=True,
    )
    print("top_formulas_by_hit_count")
    for f in ranked[: args.top]:
        print(f"  hits={hits[f]:2d}/{valid[f]:2d} formula={f.label()}")
    print(f"perfect_survivors={len(survivors)}")
    for f in sorted(survivors, key=lambda row: row.label())[: args.top]:
        print(f"  survivor={f.label()}")
    print(
        "conclusion=no_low_height_quadratic_formula"
        if not survivors
        else "conclusion=surviving_quadratic_formula_lead"
    )


if __name__ == "__main__":
    main()
