#!/usr/bin/env python3
"""Probe fixed-degree algebraic Montgomery sections for p = n^2 + 7.

Earlier near-square probes tested rational formulas for A(n), A(n)^2, j(n),
and several X1/Legendre coordinates.  A slightly broader shortcut would be a
constant-degree algebraic section: for example, a root A of

    q2(n) A^2 + q1(n) A + q0(n) = 0,

where each qi(n) is a small element of Z[n].  In the family p = n^2 + 7, every
integer polynomial in n reduces modulo p to a + b n, so affine coefficients in
n already cover bounded-height polynomial coefficients after reduction.

Such a section would be a real asymptotic win if it forced depth k as p grows:
for p24 we would solve one fixed quadratic, not sample about sqrt(p) curves.
This script tests that possibility exactly on small near-square primes.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import product

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table


@dataclass(frozen=True)
class Affine:
    a: int
    b: int

    def eval(self, n: int, p: int) -> int:
        return (self.a * n + self.b) % p

    def label(self) -> str:
        if self.a == 0:
            return str(self.b)
        if self.b == 0:
            return f"{self.a}*n"
        sign = "+" if self.b > 0 else ""
        return f"{self.a}*n{sign}{self.b}"


@dataclass(frozen=True)
class QuadraticSection:
    q2: Affine
    q1: Affine
    q0: Affine

    def normalized(self) -> "QuadraticSection":
        vals = (self.q2.a, self.q2.b, self.q1.a, self.q1.b, self.q0.a, self.q0.b)
        g = 0
        for value in vals:
            g = math.gcd(g, abs(value))
        if g > 1:
            vals = tuple(value // g for value in vals)
        first = next((value for value in vals if value), 0)
        if first < 0:
            vals = tuple(-value for value in vals)
        return QuadraticSection(
            Affine(vals[0], vals[1]),
            Affine(vals[2], vals[3]),
            Affine(vals[4], vals[5]),
        )

    def label(self) -> str:
        return f"({self.q2.label()})*A^2 + ({self.q1.label()})*A + ({self.q0.label()})"


def sections(bound: int, require_quadratic: bool) -> list[QuadraticSection]:
    vals = range(-bound, bound + 1)
    out: set[QuadraticSection] = set()
    for c2a, c2b, c1a, c1b, c0a, c0b in product(vals, repeat=6):
        if c2a == c2b == c1a == c1b == c0a == c0b == 0:
            continue
        if require_quadratic and c2a == c2b == 0:
            continue
        row = QuadraticSection(
            Affine(c2a, c2b),
            Affine(c1a, c1b),
            Affine(c0a, c0b),
        ).normalized()
        if require_quadratic and row.q2.a == row.q2.b == 0:
            continue
        out.add(row)
    return sorted(
        out,
        key=lambda row: (
            sum(abs(v) for v in (row.q2.a, row.q2.b, row.q1.a, row.q1.b, row.q0.a, row.q0.b)),
            row.q2.a,
            row.q2.b,
            row.q1.a,
            row.q1.b,
            row.q0.a,
            row.q0.b,
        ),
    )


def sqrt_mod_p3(a: int, p: int, chi: np.ndarray) -> int | None:
    a %= p
    if a == 0:
        return 0
    if int(chi[a]) != 1:
        return None
    return pow(a, (p + 1) // 4, p)


def roots(section: QuadraticSection, n: int, p: int, chi: np.ndarray) -> tuple[int, ...]:
    c2 = section.q2.eval(n, p)
    c1 = section.q1.eval(n, p)
    c0 = section.q0.eval(n, p)

    if c2 == 0:
        if c1 == 0:
            return ()
        return ((-c0 * pow(c1, p - 2, p)) % p,)

    inv_2c2 = pow((2 * c2) % p, p - 2, p)
    disc = (c1 * c1 - 4 * c2 * c0) % p
    root_disc = sqrt_mod_p3(disc, p, chi)
    if root_disc is None:
        return ()
    root1 = ((-c1 + root_disc) * inv_2c2) % p
    root2 = ((-c1 - root_disc) * inv_2c2) % p
    if root1 == root2:
        return (root1,)
    return (root1, root2)


def hits_good_root(section: QuadraticSection, n: int, p: int, chi: np.ndarray, good: np.ndarray) -> bool:
    for root in roots(section, n, p, chi):
        if (root * root - 4) % p != 0 and bool(good[root]):
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=220_000)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--coeff-bound", type=int, default=3)
    ap.add_argument("--allow-linear", action="store_true")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    candidates = sections(args.coeff_bound, require_quadratic=not args.allow_linear)
    survivors = set(range(len(candidates)))
    hit_counts = [0] * len(candidates)
    valid_counts = [0] * len(candidates)

    print("implicit quadratic near-square section probe")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"allow_linear={args.allow_linear}")
    print(f"section_count={len(candidates)}")

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        next_survivors: set[int] = set()
        row_hits = 0
        row_valid = 0
        for idx in survivors:
            section = candidates[idx]
            rs = roots(section, n, p, chi)
            if not rs:
                continue
            valid_counts[idx] += 1
            row_valid += 1
            hit = any((root * root - 4) % p != 0 and bool(good[root]) for root in rs)
            if hit:
                hit_counts[idx] += 1
                row_hits += 1
                next_survivors.add(idx)
        survivors = next_survivors

        print(
            f"row={row_index:02d} n={n} p={p} k={stats['k']} "
            f"good={stats['good']}/{stats['nonsingular']} "
            f"valid_survivor_sections={row_valid} "
            f"hit_survivor_sections={row_hits} "
            f"perfect_survivors={len(survivors)}"
        )
        if not survivors:
            break

    ranked = sorted(
        range(len(candidates)),
        key=lambda idx: (hit_counts[idx], valid_counts[idx], -sum(abs(v) for v in (
            candidates[idx].q2.a,
            candidates[idx].q2.b,
            candidates[idx].q1.a,
            candidates[idx].q1.b,
            candidates[idx].q0.a,
            candidates[idx].q0.b,
        ))),
        reverse=True,
    )
    print("top_sections_by_hit_count")
    for idx in ranked[: args.top]:
        print(f"  hits={hit_counts[idx]:2d}/{valid_counts[idx]:2d} section={candidates[idx].label()}")

    print(f"perfect_survivor_count={len(survivors)}")
    for idx in sorted(survivors, key=lambda i: candidates[i].label())[: args.top]:
        print(f"  survivor={candidates[idx].label()}")
    print(
        "conclusion=no_low_height_implicit_quadratic_section"
        if not survivors
        else "conclusion=surviving_implicit_quadratic_section_lead"
    )


if __name__ == "__main__":
    main()
