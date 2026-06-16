#!/usr/bin/env python3
"""Validate an ell=3 trace filter for Montgomery curves.

For p == 1 mod 3 and E_A: y^2 = x^3 + A*x^2 + x, the p23 target accepts
trace residues {0, 2} mod 3 and rejects residue 1 mod 3.

This script computes trace mod 3 from the 3-division polynomial using
polynomial Frobenius over Fp, then compares against brute-force point counts on
small fields.  It is a validation artifact, not a production benchmark.
"""

from __future__ import annotations

import argparse
import random
import time

import x16_trace_residue_calibration as cal


def trim(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def deg(a: list[int]) -> int:
    a = trim(a[:])
    return -1 if len(a) == 1 and a[0] == 0 else len(a) - 1


def add(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def sub(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def mod_poly(a: list[int], m: list[int], p: int) -> list[int]:
    a = trim(a[:])
    m = trim(m[:])
    md = deg(m)
    if md < 0:
        raise ZeroDivisionError
    inv_lc = pow(m[-1], p - 2, p)
    while deg(a) >= md:
        shift = deg(a) - md
        coeff = a[-1] * inv_lc % p
        for i in range(md + 1):
            a[i + shift] = (a[i + shift] - coeff * m[i]) % p
        trim(a)
    return a


def monic(a: list[int], p: int) -> list[int]:
    a = trim(a[:])
    if deg(a) < 0:
        return [0]
    inv_lc = pow(a[-1], p - 2, p)
    return [(x * inv_lc) % p for x in a]


def gcd_poly(a: list[int], b: list[int], p: int) -> list[int]:
    a = trim(a[:])
    b = trim(b[:])
    while deg(b) >= 0:
        a, b = b, mod_poly(a, b, p)
    return monic(a, p)


def powmod_poly(base: list[int], exp: int, modulus: list[int], p: int) -> list[int]:
    result = [1]
    b = mod_poly(base, modulus, p)
    while exp:
        if exp & 1:
            result = mod_poly(mul(result, b, p), modulus, p)
        b = mod_poly(mul(b, b, p), modulus, p)
        exp >>= 1
    return result


def trace_mod3_filter(A: int, p: int) -> int:
    """Return t(E_A) mod 3 for p == 1 mod 3."""
    if p % 3 != 1:
        raise ValueError("this validator currently assumes p == 1 mod 3")

    # psi_3 = 3*x^4 + 4*A*x^3 + 6*x^2 - 1
    psi = [p - 1, 0, 6 % p, (4 * A) % p, 3]
    xpoly = [0, 1]
    x_p_minus_x = sub(powmod_poly(xpoly, p, psi, p), xpoly, p)
    root_factor = gcd_poly(psi, x_p_minus_x, p)

    if deg(root_factor) <= 0:
        return 0

    # Classify rational x-coordinates by whether y^2=f(x) is square.
    f = [0, 1, A % p, 1]
    legendre_on_roots = powmod_poly(f, (p - 1) // 2, root_factor, p)
    nonsquare_factor = gcd_poly(root_factor, add(legendre_on_roots, [1], p), p)
    if deg(nonsquare_factor) > 0:
        return 1
    return 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=120)
    ap.add_argument("--start", type=int, default=20_000)
    ap.add_argument("--seed", type=int, default=20260601)
    args = ap.parse_args()

    p = cal.find_calibration_prime(args.start, 8 * 3 * 5 * 7 * 11, cal.P23 % (8 * 3 * 5 * 7 * 11))
    rng = random.Random(args.seed)
    As = cal.x16_montgomery_A_values(p, rng, args.samples)

    t0 = time.perf_counter()
    mismatches = []
    counts = {0: 0, 1: 0, 2: 0}
    for A in As:
        brute = cal.trace_for_montgomery_A(p, A) % 3
        filt = trace_mod3_filter(A, p)
        counts[filt] += 1
        if brute != filt:
            mismatches.append((A, brute, filt))
    elapsed = time.perf_counter() - t0

    print(f"calibration_prime={p}")
    print(f"samples={len(As)} seed={args.seed}")
    print(f"ell3_counts={counts}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"seconds_per_curve={elapsed / len(As):.6e}")


if __name__ == "__main__":
    main()
