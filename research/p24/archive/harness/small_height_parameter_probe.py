#!/usr/bin/env python3
"""Small-height constant parameter probe for p = n^2 + 7.

The LFT-in-n probe rules out simple rational formulas in n with small
coefficients.  A separate possible shortcut is that one of the Montgomery
parameters themselves is a bounded-height rational number independent of n:

    A = r,  A^2 = r,  or  j = r.

Such a pattern would be a very cheap construction if it persisted through the
near-square family.  This script uses exact Montgomery trace convolution over
small p=n^2+7 primes and intersects the DANGER x-only bucket with bounded-height
rational constants.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from near_square_formula_probe import (
    all_montgomery_traces_fft,
    is_prime_trial,
    legendre_table,
    montgomery_j_from_A,
    sqrt_mod_p3,
    v2,
    verifier_k,
)


@dataclass(frozen=True)
class RationalConstant:
    num: int
    den: int

    def eval(self, p: int) -> int | None:
        if self.den % p == 0:
            return None
        return (self.num % p) * pow(self.den % p, p - 2, p) % p

    def label(self) -> str:
        if self.den == 1:
            return str(self.num)
        return f"{self.num}/{self.den}"


def rational_constants(bound: int, include_negative: bool) -> list[RationalConstant]:
    out: set[RationalConstant] = set()
    nums = range(-bound, bound + 1) if include_negative else range(0, bound + 1)
    for den in range(1, bound + 1):
        for num in nums:
            if math.gcd(abs(num), den) != 1:
                continue
            out.add(RationalConstant(num, den))
    return sorted(out, key=lambda r: (max(abs(r.num), r.den), r.den, r.num))


def prime_rows(min_p: int, max_p: int, max_rows: int) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    for n in range(2, math.isqrt(max_p - 7) + 1, 2):
        p = n * n + 7
        if p < min_p:
            continue
        if is_prime_trial(p):
            rows.append((n, p))
            if len(rows) >= max_rows:
                break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=1_000_000)
    ap.add_argument("--max-rows", type=int, default=35)
    ap.add_argument("--height", type=int, default=80)
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows)
    signed = rational_constants(args.height, include_negative=True)
    unsigned = rational_constants(args.height, include_negative=False)
    families = {
        "A": signed,
        "A2": unsigned,
        "j": signed,
    }
    hits = {name: {r: 0 for r in rs} for name, rs in families.items()}
    valid = {name: {r: 0 for r in rs} for name, rs in families.items()}
    survivors = {name: set(rs) for name, rs in families.items()}

    print("small-height constant Montgomery parameter probe")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"height={args.height}")
    for name, rs in families.items():
        print(f"{name}_candidate_count={len(rs)}")

    for index, (n, p) in enumerate(rows, start=1):
        k = verifier_k(p)
        chi = legendre_table(p)
        traces, fft_error = all_montgomery_traces_fft(p, chi)

        good_A = np.zeros(p, dtype=np.bool_)
        good_A2 = np.zeros(p, dtype=np.bool_)
        good_j = np.zeros(p, dtype=np.bool_)
        for A in range(p):
            if (A * A - 4) % p == 0:
                continue
            t = int(traces[A])
            if max(v2(p + 1 - t), v2(p + 1 + t)) >= k:
                good_A[A] = True
                good_A2[A * A % p] = True
                j = montgomery_j_from_A(A, p)
                if j is not None:
                    good_j[j] = True

        good_sets = {"A": good_A, "A2": good_A2, "j": good_j}
        next_survivors = {name: set() for name in families}
        for name, constants in families.items():
            good = good_sets[name]
            for r in constants:
                value = r.eval(p)
                if value is None:
                    continue
                if name == "A" and (value * value - 4) % p == 0:
                    continue
                if name == "A2":
                    root = sqrt_mod_p3(value, p)
                    if root is None or (root * root - 4) % p == 0:
                        continue
                valid[name][r] += 1
                if bool(good[value]):
                    hits[name][r] += 1
                    if r in survivors[name]:
                        next_survivors[name].add(r)
        survivors = next_survivors

        print(
            f"row={index:02d} n={n} p={p} k={k} "
            f"good_A={int(np.count_nonzero(good_A))} "
            f"good_A2={int(np.count_nonzero(good_A2))} "
            f"good_j={int(np.count_nonzero(good_j))} "
            f"survivors_A={len(survivors['A'])} "
            f"survivors_A2={len(survivors['A2'])} "
            f"survivors_j={len(survivors['j'])} "
            f"fft_error={fft_error:.2e}"
        )

    for name in ("A", "A2", "j"):
        ranked = sorted(
            families[name],
            key=lambda r: (hits[name][r], valid[name][r], -max(abs(r.num), r.den)),
            reverse=True,
        )
        print(f"top_{name}_constants_by_hit_count")
        for r in ranked[: args.top]:
            print(f"  hits={hits[name][r]:2d}/{valid[name][r]:2d} value={r.label()}")
        print(f"perfect_{name}_survivors={len(survivors[name])}")
        for r in sorted(survivors[name], key=lambda x: x.label())[: args.top]:
            print(f"  survivor={r.label()}")
    print("conclusion=no_bounded_height_constant_parameter" if all(not s for s in survivors.values()) else "conclusion=surviving_constant_parameter_lead")


if __name__ == "__main__":
    main()
