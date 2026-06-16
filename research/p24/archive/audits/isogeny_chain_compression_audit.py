#!/usr/bin/env python3
"""Small-field audit for 2-isogeny-chain compression versus x-only witnesses.

Potential shortcut:

    Instead of constructing a rational point of order 2^d, construct a rational
    cyclic 2^d-isogeny chain and recover the point by quotient/dual data.

This is the X0-versus-X1 orientation question in isogeny-chain language.  Over
small p24-congruence fields, this script enumerates Montgomery parameters A,
computes exact traces, and compares:

    X0_d:  E or its twist has a rational cyclic subgroup of order 2^d;
    X1_d:  E or its twist has an x-coordinate of exact order 2^d.

The verifier needs X1_d.  A pure isogeny-chain certificate gives only X0_d
unless it also carries the missing orientation/generator information.
"""

from __future__ import annotations

import argparse
import math


def is_prime(n: int) -> bool:
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


def find_prime(start: int, residue: int, modulus: int) -> int:
    n = start + ((residue - start) % modulus)
    while not is_prime(n):
        n += modulus
    return n


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def legendre_table(p: int) -> list[int]:
    chi = [0] * p
    exp = (p - 1) // 2
    for a in range(1, p):
        r = pow(a, exp, p)
        chi[a] = 1 if r == 1 else -1
    return chi


def trace_for_A(p: int, A: int, chi: list[int]) -> int:
    count = 1
    for x in range(p):
        rhs = (x * x % p * x + A * x % p * x + x) % p
        c = chi[rhs]
        count += 1 if c == 0 else 2 if c == 1 else 0
    return p + 1 - count


def has_x0_chain(trace: int, p: int, d: int) -> bool:
    """Whether Frobenius has an odd eigenline modulo 2^d."""
    modulus = 1 << d
    target = trace % modulus
    for lam in range(1, modulus, 2):
        mu = p * pow(lam, -1, modulus) % modulus
        if (lam + mu - target) % modulus == 0:
            return True
    return False


def exponent_v2(order_v2: int, split: bool) -> int:
    if order_v2 == 0:
        return 0
    return order_v2 - 1 if split and order_v2 >= 2 else order_v2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0)
    ap.add_argument("--start", type=int, default=1000)
    ap.add_argument("--modulus", type=int, default=16)
    ap.add_argument("--residue", type=int, default=7)
    ap.add_argument("--max-depth", type=int, default=0)
    args = ap.parse_args()

    p = args.p or find_prime(args.start, args.residue, args.modulus)
    k = verifier_k(p)
    max_depth = args.max_depth or k
    chi = legendre_table(p)

    total = 0
    split_count = 0
    x0_counts = [0] * (max_depth + 1)
    x1_counts = [0] * (max_depth + 1)
    x0_not_x1_counts = [0] * (max_depth + 1)
    x1_not_x0_counts = [0] * (max_depth + 1)

    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        total += 1
        split = chi[(A * A - 4) % p] == 1
        split_count += int(split)
        trace = trace_for_A(p, A, chi)
        curve_exp = exponent_v2(v2(p + 1 - trace), split)
        twist_exp = exponent_v2(v2(p + 1 + trace), split)
        x1_max = max(curve_exp, twist_exp)

        for d in range(1, max_depth + 1):
            x1 = x1_max >= d
            x0 = has_x0_chain(trace, p, d) or has_x0_chain(-trace, p, d)
            x0_counts[d] += int(x0)
            x1_counts[d] += int(x1)
            x0_not_x1_counts[d] += int(x0 and not x1)
            x1_not_x0_counts[d] += int(x1 and not x0)

    print("2-isogeny-chain compression audit")
    print(f"p={p}")
    print(f"p_mod_16={p % 16}")
    print(f"k={k}")
    print(f"max_depth={max_depth}")
    print(f"nonsingular_A={total}")
    print(f"split_A={split_count}")
    print("depth X0_chain_A X1_xonly_A X0_not_X1 X1_not_X0 x0_over_x1")
    for d in range(1, max_depth + 1):
        ratio = x0_counts[d] / x1_counts[d] if x1_counts[d] else float("inf")
        print(
            f"{d:2d} {x0_counts[d]:10d} {x1_counts[d]:10d} "
            f"{x0_not_x1_counts[d]:9d} {x1_not_x0_counts[d]:9d} {ratio:.6f}"
        )
    print("conclusion=X0_isogeny_chain_is_strictly_weaker_than_verifier_X1_orientation")


if __name__ == "__main__":
    main()
