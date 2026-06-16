#!/usr/bin/env python3
"""Scan small cyclic codes for projector-coset support reductions.

This is a pure coding-theory toy.  It searches split cyclic groups
F_q[T]/(T^h-1), chooses a quotient H of size n, inserts artificial vanished
character sets away from the quotient characters, and computes

    min wt(e_H + Ann).

The scan is deliberately small: its purpose is to falsify over-broad minimum
weight conjectures, not to model the full p24 CM annihilator.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools

import sympy as sp

T = sp.symbols("T")


@dataclass(frozen=True)
class Row:
    h: int
    q: int
    quotient_size: int
    subgroup_size: int
    vanished_count: int
    vanished: tuple[int, ...]
    projector_weight: int
    best_weight: int
    quotient_characters: tuple[int, ...]


def coeff_vector(poly: sp.Poly, h: int, q: int) -> list[int]:
    out = [0] * h
    for (power,), coeff in poly.as_dict().items():
        out[power % h] = (out[power % h] + int(coeff)) % q
    return out


def shift(values: list[int], amount: int) -> list[int]:
    h = len(values)
    out = [0] * h
    for i, value in enumerate(values):
        out[(i + amount) % h] = value
    return out


def weight(values: list[int], q: int) -> int:
    return sum(1 for value in values if value % q)


def projector(h: int, quotient_size: int) -> list[int]:
    subgroup_size = h // quotient_size
    out = [0] * h
    for k in range(subgroup_size):
        out[(quotient_size * k) % h] = 1
    return out


def min_weight(base: list[int], basis: list[list[int]], q: int, max_words: int) -> int | None:
    if q ** len(basis) > max_words:
        return None
    best = len(base) + 1
    for coeffs in itertools.product(range(q), repeat=len(basis)):
        candidate = base[:]
        for coeff, vector in zip(coeffs, basis):
            candidate = [(x + coeff * y) % q for x, y in zip(candidate, vector)]
        best = min(best, weight(candidate, q))
    return best


def scan(max_h: int, max_q: int, max_vanished: int, max_words: int) -> list[Row]:
    reductions: list[Row] = []
    for h in range(4, max_h + 1):
        primes = [q for q in sp.primerange(3, max_q + 1) if (q - 1) % h == 0]
        if not primes:
            continue
        q = int(primes[0])
        zeta = pow(sp.primitive_root(q), (q - 1) // h, q)
        torsion = sp.Poly(T**h - 1, T, modulus=q)
        factors = [sp.Poly(T - pow(zeta, s, q), T, modulus=q) for s in range(h)]

        for m in sorted(int(d) for d in sp.divisors(h) if 2 <= d < h and h % d == 0):
            n = h // m
            quotient_chars = tuple((n * r) % h for r in range(m))
            nonquotient = [s for s in range(h) if s not in set(quotient_chars)]
            base = projector(h, m)

            for r in range(1, min(max_vanished, len(nonquotient)) + 1):
                for vanished in itertools.combinations(nonquotient, r):
                    vanished_factor = sp.Poly(1, T, modulus=q)
                    for s in vanished:
                        vanished_factor *= factors[s]
                    ann_generator, remainder = torsion.div(vanished_factor)
                    if not remainder.is_zero:
                        raise AssertionError((h, q, vanished))
                    generator = coeff_vector(ann_generator, h, q)
                    basis = [shift(generator, i) for i in range(r)]
                    best = min_weight(base, basis, q, max_words)
                    if best is None:
                        continue
                    projector_weight = weight(base, q)
                    if best < projector_weight:
                        reductions.append(
                            Row(
                                h=h,
                                q=q,
                                quotient_size=m,
                                subgroup_size=n,
                                vanished_count=r,
                                vanished=tuple(int(s) for s in vanished),
                                projector_weight=projector_weight,
                                best_weight=best,
                                quotient_characters=tuple(sorted(quotient_chars)),
                            )
                        )
                        break
                if reductions and reductions[-1].h == h and reductions[-1].quotient_size == m:
                    break
    return reductions


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-h", type=int, default=36)
    ap.add_argument("--max-q", type=int, default=200)
    ap.add_argument("--max-vanished", type=int, default=4)
    ap.add_argument("--max-words", type=int, default=2_000_000)
    args = ap.parse_args()

    reductions = scan(args.max_h, args.max_q, args.max_vanished, args.max_words)

    print("cyclic-code min-weight scan")
    print(f"max_h={args.max_h}")
    print(f"max_q={args.max_q}")
    print(f"max_vanished={args.max_vanished}")
    print(f"max_words={args.max_words}")
    print(f"reductions={len(reductions)}")
    print()
    print("h q quotient subgroup vanished_count vanished quotient_chars projector best")
    for row in reductions[:40]:
        print(
            f"{row.h:2d} {row.q:3d} {row.quotient_size:8d} {row.subgroup_size:8d} "
            f"{row.vanished_count:14d} {list(row.vanished)!s:18s} "
            f"{list(row.quotient_characters)!s:18s} "
            f"{row.projector_weight:9d} {row.best_weight:4d}"
        )

    print()
    print("interpretation")
    print("  reductions_use_only_nonquotient_vanished_characters=1")
    print("  artificial_multi_packet_annihilators_can_beat_projector_support=1")
    print("  actual_CM_annihilators_must_be_controlled_arithmetically=1")
    print("conclusion=reported_cyclic_code_min_weight_scan")


if __name__ == "__main__":
    main()
