#!/usr/bin/env python3
"""Post-CM-root x-only projection toy.

This isolates the easy tail of the p24 plan.  Once a Montgomery parameter `A`
with a strict target trace is known, an accepted DANGER3 `x0` can be found by
projecting arbitrary x-coordinates by the odd part of the relevant curve or
twist order, then trimming to exact verifier depth.

The script uses small fields by default.  It is not a p24 root selector; it
checks that the remaining `x0` construction is a short x-only group operation
after the hard target-trace `A` has been supplied.
"""

from __future__ import annotations

import argparse
from math import gcd, isqrt

from fixed_trace_montgomery_verifier_toy import (
    legendre,
    montgomery_trace,
    pp_verify,
)


def compute_k(p: int) -> int:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    k = 0
    value = 1
    while value <= bound:
        k += 1
        value <<= 1
    return k


def v2(n: int) -> int:
    out = 0
    n = abs(n)
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def xDBL(p: int, a24: int, X: int, Z: int) -> tuple[int, int]:
    u = (X + Z) % p
    v = (X - Z) % p
    uu = u * u % p
    vv = v * v % p
    w = (uu - vv) % p
    return uu * vv % p, w * ((vv + a24 * w) % p) % p


def xADD(p: int, xP: int, X0: int, Z0: int, X1: int, Z1: int) -> tuple[int, int]:
    u = (X0 - Z0) * (X1 + Z1) % p
    v = (X0 + Z0) * (X1 - Z1) % p
    s = (u + v) % p
    d = (u - v) % p
    return s * s % p, xP * d * d % p


def xMUL(p: int, A: int, xP: int, n: int) -> tuple[int, int]:
    if n == 0:
        return 0, 0
    a24 = (A + 2) * pow(4, -1, p) % p
    X0, Z0 = xP % p, 1
    if n == 1:
        return X0, Z0
    X1, Z1 = xDBL(p, a24, X0, Z0)
    for bit in bin(n)[3:]:
        if bit == "1":
            X0, Z0 = xADD(p, xP, X0, Z0, X1, Z1)
            X1, Z1 = xDBL(p, a24, X1, Z1)
        else:
            X1, Z1 = xADD(p, xP, X0, Z0, X1, Z1)
            X0, Z0 = xDBL(p, a24, X0, Z0)
    return X0, Z0


def affine_x(p: int, X: int, Z: int) -> int | None:
    if Z % p == 0:
        return None
    return X * pow(Z, -1, p) % p


def exact_depth_projection(
    p: int,
    A: int,
    X: int,
    Z: int,
    k: int,
    max_depth: int,
) -> int | None:
    a24 = (A + 2) * pow(4, -1, p) % p
    CX, CZ = X, Z
    zero_depth = None
    for depth in range(1, max_depth + 1):
        CX, CZ = xDBL(p, a24, CX, CZ)
        if CZ % p == 0:
            zero_depth = depth
            break
    if zero_depth is None or zero_depth < k:
        return None
    target_doubles = zero_depth - k
    CX, CZ = X, Z
    for _ in range(target_doubles):
        CX, CZ = xDBL(p, a24, CX, CZ)
    return affine_x(p, CX, CZ)


def side_data(p: int, trace: int, twist: bool) -> tuple[int, int, int]:
    order = p + 1 + trace if twist else p + 1 - trace
    depth = v2(order)
    odd = order >> depth
    return order, depth, odd


def find_projected_x(
    p: int,
    A: int,
    trace: int,
    trials: int,
) -> tuple[str, int, int, int] | None:
    k = compute_k(p)
    sides = [
        ("curve",) + side_data(p, trace, False),
        ("twist",) + side_data(p, trace, True),
    ]
    for side_name, _order, depth, odd in sides:
        if depth < k:
            continue
        for x in range(trials):
            QX, QZ = xMUL(p, A, x, odd)
            candidate = exact_depth_projection(p, A, QX, QZ, k, depth)
            if candidate is not None and pp_verify(p, A, candidate):
                return side_name, x, odd, candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=103)
    parser.add_argument("--A", type=int)
    parser.add_argument("--trace", type=int, default=8)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--scan-target-trace", action="store_true")
    args = parser.parse_args()

    print("post-CM-root x-only projection toy")
    print(f"p={args.p}")
    print(f"k={compute_k(args.p)}")
    print(f"target_abs_trace={abs(args.trace)}")

    candidates: list[tuple[int, int]] = []
    if args.A is not None:
        trace = montgomery_trace(args.A, args.p)
        if trace is None:
            raise SystemExit("singular A")
        candidates.append((args.A, trace))
    else:
        for A in range(args.p):
            if gcd(A * A - 4, args.p) != 1:
                continue
            trace = montgomery_trace(A, args.p)
            if trace is not None and abs(trace) == abs(args.trace):
                candidates.append((A, trace))
                if not args.scan_target_trace:
                    break

    found = 0
    for A, trace in candidates:
        result = find_projected_x(args.p, A, trace, args.trials)
        split = legendre(A * A - 4, args.p)
        if result is None:
            print(f"A={A} trace={trace} split={split} found=0")
            continue
        side, seed_x, odd, x0 = result
        found += 1
        print(
            f"A={A} trace={trace} split={split} found=1 "
            f"side={side} seed_x={seed_x} odd={odd} x0={x0} "
            f"verify={int(pp_verify(args.p, A, x0))}"
        )

    print()
    print(f"candidates={len(candidates)}")
    print(f"found={found}")
    print("conclusion=post_cm_root_projection_constructs_x0_for_strict_target_trace_A")


if __name__ == "__main__":
    main()
