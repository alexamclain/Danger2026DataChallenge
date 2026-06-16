#!/usr/bin/env python3
"""Small-prime X1(24) -> order-48 probe.

Research helper only.  It samples Sutherland's optimized X1(24) equation,
maps rational points to Tate normal form with marked point P=(0,0) of order 24,
tests whether P has a rational half Q, and when it does maps R=3Q to a
Montgomery x-coordinate of order 16.  The resulting Montgomery point can be fed
through the same first-branch halving diagnostic used for X1(16).
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


DEFAULT_URL = "https://math.mit.edu/~drew/X1/FFFc24.txt"

Point = Optional[tuple[int, int]]


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


def chi(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    v = pow(a, (p - 1) // 2, p)
    return -1 if v == p - 1 else int(v)


def sqrt_mod_roots(a: int, p: int) -> list[int]:
    return sorted(int(r) % p for r in sp.sqrt_mod(a % p, p, all_roots=True))


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
    b = r * s % p * rm1 % p
    if b == 0:
        return None
    c = s * rm1 % p
    return b, c


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


def short_add(p: int, A: int, B: int, P: Point, Q: Point) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if x1 == x2 and y1 == y2:
        den = (2 * y1) % p
        if den == 0:
            return None
        lam = (3 * x1 * x1 + A) % p * inv(den, p) % p
    else:
        den = (x2 - x1) % p
        if den == 0:
            return None
        lam = (y2 - y1) % p * inv(den, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return x3, y3


def short_double(p: int, A: int, B: int, P: Point) -> Point:
    return short_add(p, A, B, P, P)


def tate_to_short_params(p: int, b: int, c: int) -> tuple[int, int, int, int]:
    a = (c - 1) % p
    e = (a * a - 4 * b) % p
    A = 27 * (24 * a % p * b % p - e * e) % p
    B = 54 * (e * e % p * e % p - 36 * a % p * b % p * e % p + 216 * b * b) % p
    return a, e, A, B


def tate_to_short_point(p: int, b: int, c: int, P: tuple[int, int]) -> tuple[int, int]:
    a, e, _, _ = tate_to_short_params(p, b, c)
    u, v = P
    x = (36 * u + 3 * e) % p
    y = (216 * v - 108 * (a * u + b)) % p
    return x, y


def short_to_tate_point(p: int, b: int, c: int, P: tuple[int, int]) -> tuple[int, int]:
    a, e, _, _ = tate_to_short_params(p, b, c)
    x, y = P
    inv36 = inv(36, p)
    inv216 = inv(216, p)
    u = (x - 3 * e) % p * inv36 % p
    v = (y + 108 * (a * u + b)) % p * inv216 % p
    return u, v


def short_halves(p: int, A: int, B: int, P: tuple[int, int]) -> list[tuple[int, int]]:
    xp, _ = P
    sx = sp.symbols("sx")
    expr = (
        sx**4
        - 2 * A * sx**2
        - 8 * B * sx
        + A * A
        - 4 * xp * (sx**3 + A * sx + B)
    )
    poly = sp.Poly(expr, sx, modulus=p)
    out: list[tuple[int, int]] = []
    for root, multiplicity in poly.ground_roots().items():
        if multiplicity <= 0:
            continue
        xq = int(root) % p
        rhs = (xq * xq % p * xq + A * xq + B) % p
        for yq in sqrt_mod_roots(rhs, p):
            Q = (xq, yq)
            if short_double(p, A, B, Q) == P:
                out.append(Q)
    return sorted(set(out))


def roots_mod_prime(poly: sp.Poly, p: int) -> list[int]:
    roots: list[int] = []
    for root, multiplicity in poly.ground_roots().items():
        if multiplicity <= 0:
            continue
        roots.append(int(root) % p)
    return sorted(set(roots))


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


def current_k(p: int) -> int:
    q = int(sp.integer_nthroot(p, 2)[0])
    bound = q + 1 + 2 * int(sp.integer_nthroot(q, 2)[0])
    return bound.bit_length()


def order48_to_montgomery(p: int, b: int, c: int, Q_tate: tuple[int, int]) -> tuple[int, int] | None:
    P = (0, 0)
    T = tate_mul(p, b, c, 12, P)
    H = tate_mul(p, b, c, 6, P)
    R = tate_mul(p, b, c, 3, Q_tate)
    if T is None or H is None or R is None:
        return None
    alpha = T[0]
    h = H[0]
    d = (h - alpha) % p
    if d == 0:
        return None
    _, e, _, _ = tate_to_short_params(p, b, c)
    A = (12 * alpha + e) % p * inv(4 * d, p) % p
    xR = (R[0] - alpha) % p * inv(d, p) % p
    if A <= 2 or A >= p - 2 or xR == 0:
        return None
    return A, xR


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=1000003)
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260602)
    ap.add_argument("--cache", type=Path, default=Path("runs/x1_24_probe/FFFc24.txt"))
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--target-depth", type=int, default=0)
    ap.add_argument("--max-order48", type=int, default=0)
    args = ap.parse_args()

    text = load_polynomial_text(args.cache, args.url)
    sx, sy = sp.symbols("x y")
    expr = sp.sympify(text.replace("^", "**"))
    rng = random.Random(args.seed)

    k = current_k(args.p)
    start_depth = 4
    target_depth = args.target_depth if args.target_depth else min(k, 16)
    target_depth = max(start_depth, min(target_depth, k))

    fiber_roots = Counter()
    half_count_hist = Counter()
    split_hist = Counter()
    zero_steps = Counter()
    depth_hist = Counter()
    depth_survive = Counter()
    split_depth_survive: dict[int, Counter[int]] = {-1: Counter(), 1: Counter(), 0: Counter()}
    total_roots = 0
    mapped_tate = 0
    nonsingular_short = 0
    order24_checked = 0
    order24_ok = 0
    halfable = 0
    mapped_order48 = 0
    factor_seconds = 0.0
    half_seconds = 0.0
    examples: list[tuple[int, int, int, int, int, int]] = []
    t0 = time.perf_counter()

    for _ in range(args.samples):
        xv = rng.randrange(args.p)
        poly = sp.Poly(expr.subs(sx, xv), sy, modulus=args.p)
        ft0 = time.perf_counter()
        roots = roots_mod_prime(poly, args.p)
        factor_seconds += time.perf_counter() - ft0
        fiber_roots[len(roots)] += 1
        total_roots += len(roots)

        for yv in roots:
            if args.max_order48 and mapped_order48 >= args.max_order48:
                break
            tate = x1_optimized_to_tate(args.p, xv, yv)
            if tate is None:
                continue
            mapped_tate += 1
            b, c = tate
            a, e, As, Bs = tate_to_short_params(args.p, b, c)
            disc = (-4 * As * As % args.p * As - 27 * Bs * Bs) % args.p
            if disc == 0:
                continue
            nonsingular_short += 1

            P = (0, 0)
            order24_checked += 1
            if tate_mul(args.p, b, c, 24, P) is None and tate_mul(args.p, b, c, 12, P) is not None:
                order24_ok += 1
            Ps = tate_to_short_point(args.p, b, c, P)

            ht0 = time.perf_counter()
            halves = short_halves(args.p, As, Bs, Ps)
            half_seconds += time.perf_counter() - ht0
            half_count_hist[len(halves)] += 1
            if not halves:
                continue
            halfable += 1

            # Deterministic first half: enough for a production-style section.
            Qs = halves[0]
            Qt = short_to_tate_point(args.p, b, c, Qs)
            if tate_mul(args.p, b, c, 2, Qt) != P:
                continue
            if tate_mul(args.p, b, c, 48, Qt) is not None:
                continue
            if tate_mul(args.p, b, c, 24, Qt) is None:
                continue

            pair = order48_to_montgomery(args.p, b, c, Qt)
            if pair is None:
                continue
            A, xR = pair
            mapped_order48 += 1
            split = chi((A * A - 4) % args.p, args.p)
            split_hist[split] += 1
            step = xonly_zero_step(args.p, A, xR, max_steps=16)
            zero_steps[step if step is not None else -1] += 1
            depth = first_branch_depth(args.p, A, xR, start_depth, target_depth)
            depth_hist[depth] += 1
            for d in range(start_depth, depth + 1):
                depth_survive[d] += 1
                split_depth_survive[split][d] += 1
            if len(examples) < 5:
                examples.append((xv, yv, A, xR, split, depth))
        if args.max_order48 and mapped_order48 >= args.max_order48:
            break

    elapsed = time.perf_counter() - t0
    print("X1(24) -> order48 small-prime probe")
    print(f"source_url={args.url}")
    print(f"cache={args.cache}")
    print(f"p={args.p}")
    print(f"p_mod_24={args.p % 24}")
    print(f"p_mod_3={args.p % 3}")
    print(f"k={k}")
    print(f"samples={args.samples}")
    print(f"seed={args.seed}")
    print(f"target_depth={target_depth}")
    print(f"max_order48={args.max_order48}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"factor_seconds={factor_seconds:.6f}")
    print(f"half_seconds={half_seconds:.6f}")
    print(f"fibers_per_second={args.samples / elapsed if elapsed else 0.0:.3f}")
    print(f"roots_per_second={total_roots / elapsed if elapsed else 0.0:.3f}")
    print(f"order48_per_second={mapped_order48 / elapsed if elapsed else 0.0:.3f}")
    print(f"total_roots={total_roots}")
    print(f"mapped_tate={mapped_tate}")
    print(f"nonsingular_short={nonsingular_short}")
    print(f"order24_checked={order24_checked}")
    print(f"order24_ok={order24_ok}")
    print(f"halfable_order24_points={halfable}")
    print(f"mapped_order48_montgomery={mapped_order48}")
    print(f"avg_roots_per_fiber={total_roots / args.samples:.6f}")
    print("fiber_root_count_hist=" + ",".join(f"{k}:{fiber_roots[k]}" for k in sorted(fiber_roots)))
    print("half_count_hist=" + ",".join(f"{k}:{half_count_hist[k]}" for k in sorted(half_count_hist)))
    print("montgomery_split_hist=" + ",".join(f"{k}:{split_hist[k]}" for k in sorted(split_hist)))
    print("marked_point_zero_step_hist=" + ",".join(f"{k}:{zero_steps[k]}" for k in sorted(zero_steps)))
    print("first_branch_depth_hist=" + ",".join(f"{k}:{depth_hist[k]}" for k in sorted(depth_hist)))
    print("first_branch_survival depth count rate")
    for d in range(start_depth, target_depth + 1):
        rate = depth_survive[d] / mapped_order48 if mapped_order48 else 0.0
        print(f"{d} {depth_survive[d]} {rate:.9f}")
    print("first_branch_survival_by_split split depth count rate")
    for split in sorted(split_hist):
        denom = split_hist[split]
        for d in range(start_depth, target_depth + 1):
            count = split_depth_survive[split][d]
            rate = count / denom if denom else 0.0
            print(f"{split} {d} {count} {rate:.9f}")
    print("examples=x,y,A,xR,split,depth")
    for row in examples:
        print(" ".join(str(v) for v in row))


if __name__ == "__main__":
    main()
