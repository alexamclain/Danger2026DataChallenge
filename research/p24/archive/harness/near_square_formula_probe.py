#!/usr/bin/env python3
"""Search for low-height Montgomery formulas in the family p = n^2 + 7.

The p24 prime is special because p = (10^12)^2 + 7.  A natural possible
shortcut would be a low-height rational expression in n that always gives a
Montgomery parameter A whose curve or twist has the required DANGER 2-power.

This script tests that idea at small scale without brute-forcing p^2 work.  It
uses the Montgomery trace convolution

    t(A) = - sum_c chi(c^2 - 4) chi(A + c)

to compute every trace for small p = n^2 + 7, then checks all LFTs

    A(n) = (a*n + b)/(c*n + d)

with small integer coefficients.  With ``--square-parameter`` it instead
interprets the LFT as B(n) = A(n)^2 and tests both square roots.  With
``--j-parameter`` it interprets the LFT as a Montgomery j-invariant and tests
whether any compatible Montgomery parameter is in the DANGER bucket.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from functools import reduce
from itertools import product

import numpy as np


@dataclass(frozen=True)
class Formula:
    a: int
    b: int
    c: int
    d: int

    def eval(self, n: int, p: int) -> int | None:
        den = (self.c * n + self.d) % p
        if den == 0:
            return None
        return ((self.a * n + self.b) % p) * pow(den, p - 2, p) % p

    def label(self) -> str:
        return f"({self.a}*n+{self.b})/({self.c}*n+{self.d})"


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


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def next_pow2(n: int) -> int:
    return 1 << (n - 1).bit_length()


def legendre_table(p: int) -> np.ndarray:
    chi = np.zeros(p, dtype=np.int16)
    exp = (p - 1) // 2
    for a in range(1, p):
        r = pow(a, exp, p)
        chi[a] = 1 if r == 1 else -1
    return chi


def all_montgomery_traces_fft(p: int, chi: np.ndarray) -> tuple[np.ndarray, float]:
    c = np.arange(p, dtype=np.int64)
    f = chi[(c * c - 4) % p].astype(np.float64)
    g = chi.astype(np.float64)

    # r[d] = f[-d], so cyclic convolution gives sum_c f[c] g[A+c].
    r = np.empty(p, dtype=np.float64)
    r[0] = f[0]
    r[1:] = f[:0:-1]

    nfft = next_pow2(2 * p - 1)
    conv = np.fft.irfft(np.fft.rfft(r, nfft) * np.fft.rfft(g, nfft), nfft)[: 2 * p - 1]
    folded = conv[:p].copy()
    folded[: p - 1] += conv[p:]
    rounded = np.rint(folded)
    max_error = float(np.max(np.abs(folded - rounded)))
    return (-rounded).astype(np.int64), max_error


def sqrt_mod_p3(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    return pow(a, (p + 1) // 4, p)


def montgomery_j_from_A(A: int, p: int) -> int | None:
    B = A * A % p
    den = (B - 4) % p
    if den == 0:
        return None
    return 256 * pow((B - 3) % p, 3, p) * pow(den, p - 2, p) % p


def normalize_lft(a: int, b: int, c: int, d: int) -> Formula | None:
    if a == b == c == d == 0:
        return None
    if a * d - b * c == 0:
        return None
    g = reduce(math.gcd, (abs(a), abs(b), abs(c), abs(d)))
    if g:
        a, b, c, d = a // g, b // g, c // g, d // g
    first = next(x for x in (a, b, c, d) if x != 0)
    if first < 0:
        a, b, c, d = -a, -b, -c, -d
    return Formula(a, b, c, d)


def formulas(bound: int) -> list[Formula]:
    seen: set[Formula] = set()
    vals = range(-bound, bound + 1)
    for a, b, c, d in product(vals, repeat=4):
        f = normalize_lft(a, b, c, d)
        if f is not None:
            seen.add(f)
    return sorted(
        seen,
        key=lambda row: (
            abs(row.a) + abs(row.b) + abs(row.c) + abs(row.d),
            row.a,
            row.b,
            row.c,
            row.d,
        ),
    )


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
    ap.add_argument("--min-p", type=int, default=1_000)
    ap.add_argument("--max-p", type=int, default=250_000)
    ap.add_argument("--max-rows", type=int, default=40)
    ap.add_argument("--coeff-bound", type=int, default=5)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument(
        "--square-parameter",
        action="store_true",
        help="interpret the LFT as B=A^2 and test both square roots",
    )
    ap.add_argument(
        "--j-parameter",
        action="store_true",
        help="interpret the LFT as the Montgomery j-invariant",
    )
    args = ap.parse_args()
    if args.square_parameter and args.j_parameter:
        raise SystemExit("--square-parameter and --j-parameter are mutually exclusive")

    rows = prime_rows(args.min_p, args.max_p, args.max_rows)
    fs = formulas(args.coeff_bound)
    hits = {f: 0 for f in fs}
    valid = {f: 0 for f in fs}
    survivors = set(fs)

    print("near-square low-height Montgomery A(n) formula probe")
    print(f"family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"square_parameter={args.square_parameter}")
    print(f"j_parameter={args.j_parameter}")
    print(f"formula_count={len(fs)}")

    for index, (n, p) in enumerate(rows, start=1):
        k = verifier_k(p)
        chi = legendre_table(p)
        traces, fft_error = all_montgomery_traces_fft(p, chi)
        good = np.zeros(p, dtype=np.bool_)
        good_j = np.zeros(p, dtype=np.bool_) if args.j_parameter else None
        for A in range(p):
            if (A * A - 4) % p == 0:
                continue
            t = int(traces[A])
            if max(v2(p + 1 - t), v2(p + 1 + t)) >= k:
                good[A] = True
                if good_j is not None:
                    j = montgomery_j_from_A(A, p)
                    if j is not None:
                        good_j[j] = True
        good_count = int(np.count_nonzero(good))
        good_j_count = int(np.count_nonzero(good_j)) if good_j is not None else 0

        next_survivors: set[Formula] = set()
        for f in fs:
            value = f.eval(n, p)
            if value is None:
                continue

            if args.j_parameter:
                assert good_j is not None
                valid[f] += 1
                if bool(good_j[value]):
                    hits[f] += 1
                    if f in survivors:
                        next_survivors.add(f)
                continue

            if args.square_parameter:
                root = sqrt_mod_p3(value, p)
                if root is None:
                    continue
                candidates = {root, (-root) % p}
            else:
                candidates = {value}

            usable = [A for A in candidates if (A * A - 4) % p != 0]
            if not usable:
                continue
            valid[f] += 1
            if any(bool(good[A]) for A in usable):
                hits[f] += 1
                if f in survivors:
                    next_survivors.add(f)
        survivors = next_survivors
        print(
            f"row={index:02d} n={n} p={p} k={k} good_A={good_count} "
            f"good_j={good_j_count} "
            f"good_rate={good_count / (p - 2):.6f} fft_error={fft_error:.2e} "
            f"survivors_all_rows_so_far={len(survivors)}"
        )

    ranked = sorted(fs, key=lambda f: (hits[f], valid[f], -sum(map(abs, (f.a, f.b, f.c, f.d)))), reverse=True)
    print("top_formulas_by_hit_count")
    for f in ranked[: args.top]:
        print(f"  hits={hits[f]:2d}/{valid[f]:2d} formula={f.label()}")
    print(f"perfect_survivors={len(survivors)}")
    for f in sorted(survivors, key=lambda row: row.label())[: args.top]:
        print(f"  survivor={f.label()}")
    print("conclusion=no_low_height_LFT_formula" if not survivors else "conclusion=surviving_low_height_formula_lead")


if __name__ == "__main__":
    main()
