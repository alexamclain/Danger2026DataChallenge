#!/usr/bin/env python3
"""Small-prime p24-congruence X1(16) calibration.

The p23 production C path specialized square roots for p == 5 mod 8.  The p24
target is p == 7 mod 8, where square roots are actually simpler
(`a^((p+1)/4)`).  This script checks the same X1(16) -> Montgomery ->
successive-halving path over small p24-congruence primes.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import Counter


P24 = 10**24 + 7


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


def find_calibration_prime(start: int, modulus: int, residue: int) -> int:
    n = start + ((residue - start) % modulus)
    while not is_prime(n):
        n += modulus
    return n


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    v = pow(a, (p - 1) // 2, p)
    return -1 if v == p - 1 else v


def sqrt_mod(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
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
    while legendre(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        probe = t * t % p
        while probe != 1:
            i += 1
            probe = probe * probe % p
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def x16_roots_for_y(y: int, p: int) -> list[tuple[int, int]]:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return []
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    sd = sqrt_mod(disc, p)
    if sd is None:
        return []
    inv_2qa = inv(2 * qa, p)
    out: list[tuple[int, int]] = []
    for x_model in ((sd - qb) * inv_2qa % p, (-sd - qb) * inv_2qa % p):
        ym1 = (y - 1) % p
        den_a = 4 * pow(ym1, 4, p) % p
        den_x = (x_model - y) % p
        if den_a == 0 or den_x == 0:
            continue
        num = (
            y**8
            - 8 * y**7
            + 24 * y**6
            - 32 * y**5
            + 8 * y**4
            + 32 * y**3
            - 48 * y**2
            + 32 * y
            - 8
        ) % p
        A = num * inv(den_a, p) % p
        xP = x_model * inv(den_x, p) % p
        if A not in (2, p - 2) and xP != 0:
            out.append((A, xP))
    return out


def y_predicts_nonsplit(y: int, p: int) -> bool:
    y2 = y * y % p
    f = (y2 - 2) * (y2 - 4 * y + 2) % p
    return f != 0 and legendre(f, p) != 1


def halve_once_first(p: int, A: int, x: int) -> int | None:
    d = (x * x + A * x + 1) % p
    sd = sqrt_mod(d, p)
    if sd is None:
        return None
    inv2 = (p + 1) // 2
    for rd in (sd, (-sd) % p):
        u = (2 * x + 2 * rd) % p
        sw = sqrt_mod((u * u - 4) % p, p)
        if sw is None:
            continue
        for nx in ((u + sw) * inv2 % p, (u - sw) * inv2 % p):
            if nx:
                return nx
    return None


def first_branch_depth(p: int, A: int, x: int, target: int) -> int:
    depth = 4
    while depth < target:
        nx = halve_once_first(p, A, x)
        if nx is None:
            break
        x = nx
        depth += 1
    return depth


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=50_000)
    ap.add_argument("--samples", type=int, default=20_000)
    ap.add_argument("--target-depth", type=int, default=18)
    ap.add_argument("--seed", type=int, default=20260603)
    ap.add_argument("--extra-mod", type=int, default=3 * 5 * 7 * 11)
    args = ap.parse_args()

    modulus = 8 * args.extra_mod
    p = find_calibration_prime(args.start, modulus, P24 % modulus)
    rng = random.Random(args.seed)
    attempts = 0
    accepted = 0
    nonsplit = 0
    depths: Counter[int] = Counter()
    nonsplit_depths: Counter[int] = Counter()

    while accepted < args.samples:
        attempts += 1
        y = rng.randrange(1, p)
        roots = x16_roots_for_y(y, p)
        if not roots:
            continue
        yns = y_predicts_nonsplit(y, p)
        for A, xP in roots:
            if accepted >= args.samples:
                break
            depth = first_branch_depth(p, A, xP, args.target_depth)
            depths[depth] += 1
            accepted += 1
            if yns:
                nonsplit += 1
                nonsplit_depths[depth] += 1

    print(f"calibration_prime = {p}")
    print(f"p_mod_8 = {p % 8}")
    print(f"p24_mod_modulus = {P24 % modulus} modulus = {modulus}")
    print(f"attempted_y = {attempts}")
    print(f"accepted_x16 = {accepted}")
    print(f"nonsplit = {nonsplit}")
    print(f"target_depth = {args.target_depth}")
    for label, total, table in (
        ("all_x16", accepted, depths),
        ("nonsplit", nonsplit, nonsplit_depths),
    ):
        print(f"group = {label} total = {total}")
        for d in range(4, args.target_depth + 1):
            surv = sum(c for depth, c in table.items() if depth >= d)
            rate = surv / total if total else 0.0
            print(f"  survive_depth_{d} = {surv}/{total} rate = {rate:.6f}")


if __name__ == "__main__":
    main()
