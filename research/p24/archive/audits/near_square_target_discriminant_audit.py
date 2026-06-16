#!/usr/bin/env python3
"""CM-shape audit for strict DANGER traces in the family p = n^2 + 7.

A common way finite-field trace identities become constructive is via small-CM
or Jacobi-sum evaluations: the target trace t satisfies

    t^2 - 4p = D f^2

with a fixed small fundamental discriminant D, or at least with a large square
conductor f.  This script checks that possible selector against the strict
DANGER trace residue for small calibration primes n^2 + 7 and for p24.

It is deliberately not a search for Montgomery parameters.  It only tests the
theorem-level escape hatch "the trace class is secretly a cheap CM class".
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import product

from sympy import factorint


P24 = 10**24 + 7
N24 = 10**12
K24 = 40


@dataclass(frozen=True)
class TraceCMShape:
    t: int
    fundamental_D: int
    conductor: int
    abs_D_over_p: float
    conductor_over_sqrt_p: float


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    r = math.isqrt(n)
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def danger_trace_representatives(p: int, k: int) -> list[int]:
    """Hasse representatives of t == p + 1 mod 2^k."""
    modulus = 1 << k
    bound = math.isqrt(4 * p)
    residue = (p + 1) % modulus
    first = -bound + ((residue + bound) % modulus)
    out: list[int] = []
    t = first
    while t <= bound:
        out.append(t)
        t += modulus
    return out


def is_squarefree_from_factorization(factors: dict[int, int]) -> bool:
    return all(exp == 1 for exp in factors.values())


def is_fundamental_discriminant(D: int) -> bool:
    if D >= 0:
        return False
    if D % 4 == 1:
        return is_squarefree_from_factorization(factorint(abs(D)))
    if D % 4 == 0:
        d = D // 4
        if d % 4 not in (2, 3):
            return False
        return is_squarefree_from_factorization(factorint(abs(d)))
    return False


def square_divisors_from_factorization(factors: dict[int, int]) -> list[int]:
    choices = [[prime**e for e in range(exp // 2 + 1)] for prime, exp in factors.items()]
    return sorted((math.prod(combo) for combo in product(*choices)), reverse=True)


def cm_shape_for_trace(p: int, t: int) -> TraceCMShape:
    delta = t * t - 4 * p
    if delta >= 0:
        raise ValueError("ordinary Hasse trace should have negative discriminant")
    factors = factorint(abs(delta))
    for conductor in square_divisors_from_factorization(factors):
        D = delta // (conductor * conductor)
        if is_fundamental_discriminant(D):
            return TraceCMShape(
                t=t,
                fundamental_D=D,
                conductor=conductor,
                abs_D_over_p=abs(D) / p,
                conductor_over_sqrt_p=conductor / math.sqrt(p),
            )
    raise RuntimeError(f"no fundamental discriminant found for delta={delta}")


def prime_rows(min_p: int, max_p: int, max_rows: int) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    start = max(2, math.isqrt(max(0, min_p - 7)))
    if start * start + 7 < min_p:
        start += 1
    if start % 2:
        start += 1
    for n in range(start, math.isqrt(max_p - 7) + 1, 2):
        p = n * n + 7
        if p < min_p:
            continue
        if is_prime_trial(p):
            rows.append((n, p))
            if len(rows) >= max_rows:
                break
    return rows


def summarize_one(n: int, p: int, k: int) -> tuple[list[TraceCMShape], str]:
    traces = danger_trace_representatives(p, k)
    shapes = [cm_shape_for_trace(p, t) for t in traces]
    best_small_D = min(shapes, key=lambda row: row.abs_D_over_p)
    largest_conductor = max(shapes, key=lambda row: row.conductor)
    line = (
        f"n={n} p={p} k={k} target_traces={len(traces)} "
        f"min_abs_D_over_p={best_small_D.abs_D_over_p:.6f} "
        f"max_conductor={largest_conductor.conductor} "
        f"max_conductor_over_sqrt_p={largest_conductor.conductor_over_sqrt_p:.6e}"
    )
    return shapes, line


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=500_000)
    ap.add_argument("--max-rows", type=int, default=20)
    ap.add_argument("--include-p24", action="store_true")
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()

    print("near-square strict-target CM-shape audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"max_rows={args.max_rows}")

    rows = prime_rows(args.min_p, args.max_p, args.max_rows)
    min_ratios: list[float] = []
    max_conductor_ratios: list[float] = []
    for n, p in rows:
        shapes, line = summarize_one(n, p, verifier_k(p))
        print(line)
        min_ratios.append(min(row.abs_D_over_p for row in shapes))
        max_conductor_ratios.append(max(row.conductor_over_sqrt_p for row in shapes))
        if args.detail:
            for row in shapes:
                print(
                    f"  t={row.t} fundamental_D={row.fundamental_D} "
                    f"conductor={row.conductor} abs_D_over_p={row.abs_D_over_p:.6f}"
                )

    if rows:
        print("small_scale_summary")
        print(f"  rows={len(rows)}")
        print(f"  median_min_abs_D_over_p={sorted(min_ratios)[len(min_ratios)//2]:.6f}")
        print(f"  min_min_abs_D_over_p={min(min_ratios):.6f}")
        print(f"  max_conductor_over_sqrt_p={max(max_conductor_ratios):.6e}")

    if args.include_p24:
        print("p24_detail")
        shapes, line = summarize_one(N24, P24, K24)
        print(line)
        for row in shapes:
            print(
                f"  t={row.t} fundamental_D={row.fundamental_D} "
                f"conductor={row.conductor} abs_D_over_p={row.abs_D_over_p:.6f}"
            )

    if args.include_p24:
        print("conclusion=p24_strict_target_traces_are_large_discriminant_CM_classes_not_a_small_CM_identity")
    else:
        print("conclusion=reported_near_square_strict_target_discriminant_shapes")


if __name__ == "__main__":
    main()
