#!/usr/bin/env python3
"""Exact small-prime check: nonsplit X1(16) marked depth equals v2(#E).

For nonsplit Montgomery curves the rational 2-Sylow subgroup is cyclic.  This
helper enumerates the X1(16) sampler stream over a small prime and verifies
that the marked point's first-branch halving depth is exactly the curve-level
2-adic valuation v2(#E(Fp)).
"""

from __future__ import annotations

import argparse
import time
from collections import Counter

from x16_exact_trace_enumeration import legendre, x16_A_from_y
from x16_trace_residue_calibration import inv, sqrt_mod, trace_for_montgomery_A


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def sqrt_mod_roots(a: int, p: int) -> list[int]:
    root = sqrt_mod(a, p)
    if root is None:
        return []
    root %= p
    if root == 0:
        return [0]
    return sorted({root, (-root) % p})


def x16_roots_for_y(y: int, p: int) -> list[int]:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return []
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    roots = sqrt_mod_roots(disc, p)
    if not roots:
        return []
    inv_2qa = inv(2 * qa, p)
    return sorted({((sd - qb) * inv_2qa) % p for sd in roots})


def halve_once_first(p: int, A: int, x: int) -> int | None:
    inv2 = (p + 1) // 2
    for sd in sqrt_mod_roots((x * x + A * x + 1) % p, p):
        u = (2 * x + 2 * sd) % p
        for sw in sqrt_mod_roots((u * u - 4) % p, p):
            for cand in (((u + sw) * inv2) % p, ((u - sw) * inv2) % p):
                if cand:
                    return cand
    return None


def first_branch_depth(p: int, A: int, x: int, target_depth: int) -> int:
    depth = 4
    while depth < target_depth:
        nx = halve_once_first(p, A, x)
        if nx is None:
            break
        x = nx
        depth += 1
    return depth


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--target-depth", type=int, default=16)
    ap.add_argument("--examples", type=int, default=8)
    args = ap.parse_args()

    p = args.p
    trace_cache: dict[int, int] = {}
    rows = 0
    class_counts: Counter[str] = Counter()
    class_mismatch: Counter[str] = Counter()
    class_depth_v2: Counter[str] = Counter()
    class_slack: Counter[str] = Counter()
    examples: list[tuple[str, int, int, int, int, int, int]] = []

    t0 = time.perf_counter()
    for y in range(1, p):
        A = x16_A_from_y(y, p)
        if A is None:
            continue
        roots = x16_roots_for_y(y, p)
        if not roots:
            continue
        if A not in trace_cache:
            trace_cache[A] = trace_for_montgomery_A(p, A)
        trace = trace_cache[A]
        e2 = v2(p + 1 - trace)
        cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
        for x in roots:
            den = (x - y) % p
            if den == 0:
                continue
            xP = x * inv(den, p) % p
            if xP == 0:
                continue
            depth = first_branch_depth(p, A, xP, args.target_depth)
            rows += 1
            class_counts[cls] += 1
            class_depth_v2[f"{cls}:depth={depth}:v2={e2}"] += 1
            class_slack[f"{cls}:slack={e2 - depth}"] += 1
            if e2 <= args.target_depth and depth != e2:
                class_mismatch[cls] += 1
                if len(examples) < args.examples:
                    examples.append((cls, y, x, A, xP, depth, e2))

    elapsed = time.perf_counter() - t0
    print("X1(16) marked depth vs v2(#E) exact check")
    print(f"p={p}")
    print(f"mod120={p % 120}")
    print(f"target_depth={args.target_depth}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"rows={rows}")
    print(f"trace_cache_size={len(trace_cache)}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print("mismatches_depth_ne_v2=" + ",".join(f"{k}:{class_mismatch[k]}" for k in sorted(class_counts)))
    print("slack_hist=" + ",".join(f"{k}:{class_slack[k]}" for k in sorted(class_slack)))
    print("class_depth_v2_hist=")
    for key in sorted(class_depth_v2):
        print(f"  {key}:{class_depth_v2[key]}")
    if examples:
        print("examples cls,y,x,A,xP,depth,v2")
        for row in examples:
            print(" ".join(str(v) for v in row))


if __name__ == "__main__":
    main()

