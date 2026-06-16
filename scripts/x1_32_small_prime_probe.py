#!/usr/bin/env python3
"""Small-prime X1(32) sampler probe.

This is a calibration/research helper, not a p23 production sampler. It parses
Sutherland's optimized X1(32) equation, samples random x-fibers over small prime
fields, factors the resulting degree-10 polynomial in y, maps rational points
through the optimized-model -> Tate normal form formulas, and tests marked
point conversion to Montgomery x-only coordinates.

Early runs showed that the X1(16)-specialized marked x-coordinate formula does
not transfer to FFFc32. This probe now keeps that old formula as a comparison
and also tests a general Tate-normal-form-to-Montgomery map that tracks the
marked point through the rational 2-torsion point.
"""

from __future__ import annotations

import argparse
import random
import time
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Optional

import sympy as sp


DEFAULT_URL = "https://math.mit.edu/~drew/X1/FFFc32.txt"


def load_polynomial_text(cache_path: Path | None, url: str) -> str:
    if cache_path and cache_path.exists():
        return cache_path.read_text().strip()
    text = urllib.request.urlopen(url, timeout=20).read().decode().strip()
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(text + "\n")
    return text


def inv(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError
    return pow(a, p - 2, p)


Point = Optional[tuple[int, int]]


def x1_optimized_to_tate(p: int, x: int, y: int) -> tuple[int, int] | None:
    x %= p
    y %= p
    xy = x * y % p
    x2 = x * x % p
    denr = (x2 * y - x) % p
    dens = xy
    if denr == 0 or dens == 0:
        return None
    rnum = (x2 * y - xy + y - 1) % p
    snum = (xy - y + 1) % p
    r = rnum * inv(denr, p) % p
    s = snum * inv(dens, p) % p
    if r in (0, 1) or s == 0:
        return None

    rm1 = (r - 1) % p
    bt = r * s % p * rm1 % p
    if bt == 0:
        return None
    c = s * rm1 % p
    return bt, c


def map_to_montgomery_x16_formula(p: int, x: int, y: int) -> tuple[int, int] | None:
    """Old comparison path: mirror x16_root_to_montgomery_A128."""
    tate = x1_optimized_to_tate(p, x, y)
    if tate is None:
        return None
    bt, c = tate
    # Recover r,s only for the X1(16)-specialized marked-point expression.
    x %= p
    y %= p
    xy = x * y % p
    x2 = x * x % p
    denr = (x2 * y - x) % p
    dens = xy
    rnum = (x2 * y - xy + y - 1) % p
    snum = (xy - y + 1) % p
    r = rnum * inv(denr, p) % p
    s = snum * inv(dens, p) % p
    rm1 = (r - 1) % p
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
        return None
    inv_lam = inv(lam_num, p)
    A = (3 * x8_num) % p * inv_lam % p
    xP = (-36 * numer8) % p * inv_lam % p
    if A <= 2 or A >= p - 2:
        return None
    return A, xP


def tate_add(p: int, b: int, c: int, P: Point, Q: Point) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    a1 = (1 - c) % p
    a2 = (-b) % p
    a3 = (-b) % p

    if x1 == x2 and (y1 + y2 + a1 * x1 + a3) % p == 0:
        return None

    if x1 == x2 and y1 == y2:
        den = (2 * y1 + a1 * x1 + a3) % p
        if den == 0:
            return None
        lam = (3 * x1 * x1 + 2 * a2 * x1 - a1 * y1) % p
        lam = lam * inv(den, p) % p
    else:
        den = (x2 - x1) % p
        if den == 0:
            return None
        lam = (y2 - y1) % p * inv(den, p) % p

    nu = (y1 - lam * x1) % p
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % p
    y3 = (-(lam + a1) * x3 - nu - a3) % p
    return x3, y3


def tate_mul(p: int, b: int, c: int, n: int, P: Point) -> Point:
    out: Point = None
    addend = P
    while n:
        if n & 1:
            out = tate_add(p, b, c, out, addend)
        addend = tate_add(p, b, c, addend, addend)
        n >>= 1
    return out


def map_to_montgomery_tate(p: int, x: int, y: int) -> tuple[int, int] | None:
    """Generic Tate-normal-form marked-point map for an order-32 point."""
    tate = x1_optimized_to_tate(p, x, y)
    if tate is None:
        return None
    b, c = tate
    P = (0, 0)
    H = tate_mul(p, b, c, 8, P)
    T = tate_mul(p, b, c, 16, P)
    if H is None or T is None:
        return None

    h = H[0]
    alpha = T[0]
    d = (h - alpha) % p
    if d == 0:
        return None
    b2 = ((1 - c) * (1 - c) - 4 * b) % p
    A = (12 * alpha + b2) % p * inv(4 * d, p) % p
    xP = (-alpha) % p * inv(d, p) % p
    if A <= 2 or A >= p - 2:
        return None
    return A, xP


def mong_dbl(p: int, A: int, X: int, Z: int) -> tuple[int, int]:
    X2 = X * X % p
    Z2 = Z * Z % p
    XZ = X * Z % p
    Xn = (X2 - Z2) ** 2 % p
    Zn = 4 * XZ * (X2 + A * XZ + Z2) % p
    return Xn, Zn


def xonly_zero_step(p: int, A: int, x0: int, max_steps: int = 16) -> int | None:
    X, Z = x0 % p, 1
    for step in range(1, max_steps + 1):
        X, Z = mong_dbl(p, A, X, Z)
        if Z == 0:
            return step
    return None


def current_k(p: int) -> int:
    q = int(sp.integer_nthroot(p, 2)[0])
    bound = q + 1 + 2 * int(sp.integer_nthroot(q, 2)[0])
    return bound.bit_length()


def sqrt_mod_roots(a: int, p: int) -> list[int]:
    return sorted(int(r) % p for r in sp.sqrt_mod(a % p, p, all_roots=True))


def halve_once_first(p: int, A: int, x: int) -> int | None:
    inv2 = (p + 1) // 2
    roots_d = sqrt_mod_roots((x * x + A * x + 1) % p, p)
    if not roots_d:
        return None
    for sd in roots_d:
        u = (2 * x + 2 * sd) % p
        roots_w = sqrt_mod_roots((u * u - 4) % p, p)
        for sw in roots_w:
            for cand in (((u + sw) * inv2) % p, ((u - sw) * inv2) % p):
                if cand:
                    return cand
    return None


def first_branch_depth(p: int, A: int, x: int, start_depth: int, target_depth: int) -> int:
    depth = start_depth
    while depth < target_depth:
        nx = halve_once_first(p, A, x)
        if nx is None:
            break
        x = nx
        depth += 1
    return depth


def roots_mod_prime(poly: sp.Poly, p: int) -> list[int]:
    roots: list[int] = []
    for root, multiplicity in poly.ground_roots().items():
        if multiplicity <= 0:
            continue
        roots.append(int(root) % p)
    return sorted(set(roots))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=1009)
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--cache", type=Path, default=Path("runs/x1_32_probe/FFFc32.txt"))
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--map", choices=("tate", "x16", "both"), default="tate")
    ap.add_argument("--target-depth", type=int, default=0)
    ap.add_argument("--max-mapped", type=int, default=0)
    args = ap.parse_args()

    text = load_polynomial_text(args.cache, args.url)
    sx, sy = sp.symbols("x y")
    expr = sp.sympify(text.replace("^", "**"))
    rng = random.Random(args.seed)

    fiber_roots = Counter()
    zero_steps = Counter()
    zero_steps_x16 = Counter()
    mapped = 0
    mapped_x16 = 0
    nonsingular = 0
    total_roots = 0
    k = current_k(args.p)
    start_depth = 5
    target_depth = args.target_depth if args.target_depth else min(k, 16)
    target_depth = max(start_depth, min(target_depth, k))
    depth_survive = Counter()
    depth_hist = Counter()
    t0 = time.perf_counter()
    factor_seconds = 0.0
    examples: list[tuple[int, int, int, int, int]] = []

    for _ in range(args.samples):
        xv = rng.randrange(args.p)
        poly = sp.Poly(expr.subs(sx, xv), sy, modulus=args.p)
        ft0 = time.perf_counter()
        roots = roots_mod_prime(poly, args.p)
        factor_seconds += time.perf_counter() - ft0
        fiber_roots[len(roots)] += 1
        total_roots += len(roots)
        for yv in roots:
            if args.max_mapped and mapped >= args.max_mapped:
                break
            if args.map in ("x16", "both"):
                old_pair = map_to_montgomery_x16_formula(args.p, xv, yv)
                if old_pair is not None:
                    mapped_x16 += 1
                    old_A, old_xP = old_pair
                    old_step = xonly_zero_step(args.p, old_A, old_xP, max_steps=16)
                    zero_steps_x16[old_step if old_step is not None else -1] += 1

            mapped_pair = map_to_montgomery_tate(args.p, xv, yv)
            if mapped_pair is None:
                continue
            mapped += 1
            A, xP = mapped_pair
            if (A * A - 4) % args.p != 0:
                nonsingular += 1
            step = xonly_zero_step(args.p, A, xP, max_steps=16)
            zero_steps[step if step is not None else -1] += 1
            depth = first_branch_depth(args.p, A, xP, start_depth, target_depth)
            depth_hist[depth] += 1
            for d in range(start_depth, depth + 1):
                depth_survive[d] += 1
            if len(examples) < 5:
                examples.append((xv, yv, A, xP, step if step is not None else -1))
        if args.max_mapped and mapped >= args.max_mapped:
            break

    elapsed = time.perf_counter() - t0
    print("X1(32) small-prime fiber probe")
    print(f"source_url={args.url}")
    print(f"cache={args.cache}")
    print(f"p={args.p}")
    print(f"k={k}")
    print(f"samples={args.samples}")
    print(f"seed={args.seed}")
    print(f"map={args.map}")
    print(f"target_depth={target_depth}")
    print(f"max_mapped={args.max_mapped}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"factor_seconds={factor_seconds:.6f}")
    print(f"fibers_per_second={args.samples / elapsed:.3f}")
    print(f"roots_per_second={total_roots / elapsed if elapsed else 0.0:.3f}")
    print(f"total_roots={total_roots}")
    print(f"mapped_montgomery_tate={mapped}")
    print(f"nonsingular_montgomery={nonsingular}")
    if args.map in ("x16", "both"):
        print(f"mapped_montgomery_x16_formula={mapped_x16}")
    print(f"avg_roots_per_fiber={total_roots / args.samples:.6f}")
    print("fiber_root_count_hist=" + ",".join(f"{k}:{fiber_roots[k]}" for k in sorted(fiber_roots)))
    print("marked_point_zero_step_hist_tate=" + ",".join(f"{k}:{zero_steps[k]}" for k in sorted(zero_steps)))
    if args.map in ("x16", "both"):
        print("marked_point_zero_step_hist_x16_formula=" + ",".join(f"{k}:{zero_steps_x16[k]}" for k in sorted(zero_steps_x16)))
    print("first_branch_depth_hist_tate=" + ",".join(f"{k}:{depth_hist[k]}" for k in sorted(depth_hist)))
    print("first_branch_survival_tate depth count rate")
    for d in range(start_depth, target_depth + 1):
        rate = depth_survive[d] / mapped if mapped else 0.0
        print(f"{d} {depth_survive[d]} {rate:.9f}")
    print("examples=x,y,A,xP,zero_step")
    for row in examples:
        print(" ".join(str(v) for v in row))


if __name__ == "__main__":
    main()
