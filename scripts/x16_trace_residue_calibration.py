#!/usr/bin/env python3
"""Small-prime calibration for X1(16) trace residues.

This intentionally uses brute-force point counting over small fields.  It does
not touch the active p23 run and is meant to test whether the X1(16) family
looks roughly residue-uniform modulo tiny odd primes.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import Counter


P23 = 10**23 + 117
P23_TRACES = (321963163766, -227792650122)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = math.isqrt(n)
    d = 3
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def sqrt_mod(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    if p % 8 == 5:
        x = pow(a, (p + 3) // 8, p)
        if x * x % p == a:
            return x
        return x * pow(2, (p - 1) // 4, p) % p

    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        t2 = t * t % p
        while t2 != 1:
            i += 1
            t2 = t2 * t2 % p
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def x16_montgomery_A_values(p: int, rng: random.Random, want: int) -> list[int]:
    """Sample Montgomery A parameters from Sutherland's X1(16) model."""
    out: list[int] = []
    attempts = 0
    max_attempts = want * 1000 + 1000
    while len(out) < want and attempts < max_attempts:
        attempts += 1
        y = rng.randrange(1, p)
        y2 = y * y % p
        y3 = y2 * y % p
        qa = (y2 - 2 * y) % p
        if qa == 0:
            continue
        qb = (2 * y2 - y3) % p
        qc = (1 - y) % p
        disc = (qb * qb - 4 * qa * qc) % p
        sd = sqrt_mod(disc, p)
        if sd is None:
            continue

        inv_2qa = inv(2 * qa, p)
        for x in (((sd - qb) * inv_2qa) % p, ((-sd - qb) * inv_2qa) % p):
            xy = x * y % p
            x2 = x * x % p
            denr = (x2 * y - x) % p
            dens = xy
            if denr == 0 or dens == 0:
                continue
            rnum = (x2 * y - xy + y - 1) % p
            snum = (xy - y + 1) % p
            r = rnum * inv(denr, p) % p
            s = snum * inv(dens, p) % p
            if r in (0, 1) or s == 0:
                continue

            rm1 = (r - 1) % p
            bt = r * s % p * rm1 % p
            if bt == 0:
                continue
            c = s * rm1 % p
            a = (c - 1) % p
            e = (a * a - 4 * bt) % p

            rs = r * s % p
            den = (rs - 2 * r + 1) % p
            u4 = r * rm1 % p
            s2 = s * s % p
            term = (r - s2 + s - 1) % p
            denn = den * den % p
            numer8 = u4 * ((r - s) % p) % p * term % p

            x8_num = (36 * numer8 + 3 * e * denn) % p
            lam_num = 36 * ((u4 * denn - numer8) % p) % p
            if lam_num == 0:
                continue
            A = 3 * x8_num % p * inv(lam_num, p) % p
            if A <= 2 or A >= p - 2:
                continue
            out.append(A)
            if len(out) >= want:
                break
    return out


def trace_for_montgomery_A(p: int, A: int) -> int:
    legendre = 0
    for x in range(p):
        rhs = (x * x % p * x + A * x * x + x) % p
        if rhs == 0:
            continue
        legendre += 1 if pow(rhs, (p - 1) // 2, p) == 1 else -1
    # #E = p + 1 + legendre, so trace = -legendre.
    return -legendre


def find_calibration_prime(start: int, modulus: int, residue: int) -> int:
    n = start + ((residue - start) % modulus)
    while not is_prime(n):
        n += modulus
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=80)
    ap.add_argument("--start", type=int, default=20_000)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11])
    ap.add_argument("--seed", type=int, default=20260601)
    args = ap.parse_args()

    modulus = 8
    for ell in args.ells:
        modulus *= ell
    p = find_calibration_prime(args.start, modulus, P23 % modulus)
    rng = random.Random(args.seed)
    As = x16_montgomery_A_values(p, rng, args.samples)
    traces = [trace_for_montgomery_A(p, A) for A in As]

    print(f"calibration_prime={p}")
    print(f"p23_mod_modulus={P23 % modulus} modulus={modulus}")
    print(f"samples={len(traces)} seed={args.seed}")
    print()
    for ell in args.ells:
        residues = {t % ell for t in P23_TRACES}
        counts = Counter(t % ell for t in traces)
        accepted = sum(c for r, c in counts.items() if r in residues)
        rate = accepted / len(traces) if traces else 0.0
        ideal = len(residues) / ell
        print(
            f"ell={ell:2d} target_residues={sorted(residues)} "
            f"accepted={accepted:3d}/{len(traces):3d} rate={rate:.4f} ideal={ideal:.4f} "
            f"counts={dict(sorted(counts.items()))}"
        )

    print()
    active = [True] * len(traces)
    ideal_product = 1.0
    for ell in args.ells:
        residues = {t % ell for t in P23_TRACES}
        ideal_product *= len(residues) / ell
        for i, t in enumerate(traces):
            active[i] = active[i] and (t % ell in residues)
        survivors = sum(active)
        rate = survivors / len(traces) if traces else 0.0
        print(
            f"cumulative_through_ell={ell:2d} survivors={survivors:3d}/{len(traces):3d} "
            f"rate={rate:.4f} ideal_independent={ideal_product:.4f}"
        )


if __name__ == "__main__":
    main()
