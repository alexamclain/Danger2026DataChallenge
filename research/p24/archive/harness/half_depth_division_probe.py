#!/usr/bin/env python3
"""Probe fixed-x half-depth division polynomials in the Montgomery A-line.

For fixed affine x and variable A, compute the projective Z-coordinate after
m Montgomery doublings.  Roots in A are curves for which this fixed x reaches
infinity after m doublings.

The tempting baby-step idea would be useful only if one fixed x produced about
2^m usable F_p roots.  In fact the modular-curve point count predicts O(1)
F_p roots per fixed x; this script checks that at small/medium m using FLINT.
"""

from __future__ import annotations

import argparse
import time

from flint import fmpz_mod_poly_ctx

P24 = 10**24 + 7


def montgomery_z_poly(p: int, x0: int, depth: int):
    ctx = fmpz_mod_poly_ctx(p)
    A = ctx([0, 1])
    X = ctx([x0 % p])
    Z = ctx([1])
    zprev = Z
    for _ in range(depth):
        X2 = X.square()
        Z2 = Z.square()
        XZ = X * Z
        zprev = Z
        X, Z = (X2 - Z2).square(), 4 * XZ * (X2 + A * XZ + Z2)
    return X, Z, zprev


def nonsingular_roots(p: int, zpoly, zprev, limit: int | None) -> list[int]:
    roots: list[int] = []
    for factor, mult in zpoly.factor()[1]:
        if factor.degree() != 1:
            continue
        # factor is x + c, root = -c.
        coeffs = factor.coeffs()
        root = (-int(coeffs[0])) % p
        if (root * root - 4) % p == 0:
            continue
        if int(zprev(root)) % p == 0:
            continue
        roots.append(root)
        if limit is not None and len(roots) >= limit:
            break
    return roots


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=P24)
    ap.add_argument("--x", type=int, default=3)
    ap.add_argument("--max-depth", type=int, default=16)
    ap.add_argument("--root-limit", type=int, default=20)
    args = ap.parse_args()

    print("fixed-x Montgomery A-line division probe", flush=True)
    print(f"p={args.p}", flush=True)
    print(f"x={args.x}", flush=True)
    print("depth degree build_seconds factor_seconds usable_roots first_roots", flush=True)
    for depth in range(1, args.max_depth + 1):
        t0 = time.perf_counter()
        _X, Z, Zprev = montgomery_z_poly(args.p, args.x, depth)
        t1 = time.perf_counter()
        roots = nonsingular_roots(args.p, Z, Zprev, args.root_limit)
        t2 = time.perf_counter()
        print(
            f"{depth:2d} {Z.degree():7d} {t1 - t0:12.6f} {t2 - t1:12.6f} "
            f"{len(roots):4d} {roots[:5]}",
            flush=True,
        )


if __name__ == "__main__":
    main()
