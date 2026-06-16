#!/usr/bin/env python3
"""Scan quotient-derived features on the first X1(16)->X1(32) lift cover.

The first-lift cover

    z^2 = H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2)

has the Mobius symmetry y -> (y - 2)/(y - 1).  Over p23, with i^2=-1, a
quotient invariant is

    u = (y^2 - 2)/(y - 1),

and the elimination relation involves the special factors u - 2 +/- 2i.
This helper tests whether Legendre/quartic classes of these quotient features
predict deeper p23 first-branch halving survival.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter, defaultdict

from x16_first_lift_cover_feature_scan import (
    P23,
    first_branch_depth,
    inv,
    legendre,
    sqrt_p5,
    x16_root_to_montgomery,
    x16_roots_for_y,
    x16_y_first_d_value,
    x16_y_nonsplit_value,
)


def quartic_class(a: int, p: int, sqrtm1: int) -> str:
    a %= p
    if a == 0:
        return "0"
    q = pow(a, (p - 1) // 4, p)
    if q == 1:
        return "+1"
    if q == p - 1:
        return "-1"
    if q == sqrtm1:
        return "+i"
    if q == (-sqrtm1) % p:
        return "-i"
    return "?"


def feature_values(y: int, p: int, sqrtm1: int) -> dict[str, int]:
    y2 = y * y % p
    u = (y2 - 2) * inv(y - 1, p) % p
    two_i = (2 * sqrtm1) % p
    a = (u - 2 - two_i) % p
    b = (u - 2 + two_i) % p
    return {
        "u": u,
        "u-2": u - 2,
        "u-2-2i": a,
        "u-2+2i": b,
        "(u-2)^2+4": a * b % p,
        "quotient_Q": (u * u % p) * a % p * pow(b, 3, p) % p,
    }


def add_bucket(stats: dict, feature: str, kind: str, bucket: str, depth: int, depths: list[int]) -> None:
    row = stats[(feature, kind, bucket)]
    row["total"] += 1
    for d in depths:
        if depth >= d:
            row[f"hit{d}"] += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=P23)
    ap.add_argument("--accepted", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20260629)
    ap.add_argument("--target-depth", type=int, default=12)
    ap.add_argument("--depths", type=int, nargs="+", default=[6, 8, 10, 12])
    ap.add_argument("--report-top", type=int, default=30)
    args = ap.parse_args()

    p = args.p
    if p % 8 != 5:
        raise SystemExit("This helper currently expects p == 5 mod 8.")
    sqrtm1 = pow(2, (p - 1) // 4, p)
    rng = random.Random(args.seed)
    pbits = p.bit_length()

    base = defaultdict(int)
    stats: dict = defaultdict(lambda: defaultdict(int))
    attempts = 0
    accepted = 0
    y_accept = 0
    t0 = time.time()

    while accepted < args.accepted:
        attempts += 1
        y = rng.getrandbits(pbits)
        if y >= p or y in (0, 1):
            continue

        nonsplit_val = x16_y_nonsplit_value(y, p)
        if nonsplit_val == 0 or legendre(nonsplit_val, p) != -1:
            continue

        H = x16_y_first_d_value(y, p)
        if H == 0 or sqrt_p5(H, p, sqrtm1) is None:
            continue

        roots = x16_roots_for_y(y, p, sqrtm1)
        if not roots:
            continue
        y_accept += 1

        vals = feature_values(y, p, sqrtm1)
        labels: list[tuple[str, str, str]] = []
        for name, val in vals.items():
            labels.append((name, "legendre", f"{legendre(val, p):+d}"))
            labels.append((name, "quartic", quartic_class(val, p, sqrtm1)))

        for x in roots:
            mapped = x16_root_to_montgomery(y, x, p)
            if mapped is None:
                continue
            A, xP = mapped
            depth = first_branch_depth(p, A, xP, sqrtm1, args.target_depth)
            accepted += 1
            base["total"] += 1
            for d in args.depths:
                if depth >= d:
                    base[f"hit{d}"] += 1
            for feature, kind, bucket in labels:
                add_bucket(stats, feature, kind, bucket, depth, args.depths)
            if accepted >= args.accepted:
                break

    elapsed = time.time() - t0
    target = max(args.depths)
    base_rate = base[f"hit{target}"] / base["total"] if base["total"] else 0.0

    print("X1(16) first-lift quotient feature scan")
    print(f"p = {p}")
    print(f"seed = {args.seed}")
    print(f"target_depth = {args.target_depth}")
    print(f"depths = {' '.join(str(d) for d in args.depths)}")
    print(f"accepted_curve_rows = {accepted}")
    print(f"accepted_y_values = {y_accept}")
    print(f"attempts = {attempts}")
    print(f"elapsed_seconds = {elapsed:.6f}")
    print(f"accepted_curve_rate = {accepted / elapsed:.3f}/s")
    print(f"sqrtm1 = {sqrtm1}")
    print()

    vals = [f"{base['total']}"]
    print("base total " + " ".join(f"hit{d} rate{d}" for d in args.depths))
    for d in args.depths:
        hit = base[f"hit{d}"]
        vals.extend([str(hit), f"{hit / base['total']:.9f}"])
    print(" ".join(vals))
    print()

    rows = []
    for (feature, kind, bucket), row in stats.items():
        total = row["total"]
        hit = row[f"hit{target}"]
        rate = hit / total if total else 0.0
        lift = rate / base_rate if base_rate else 0.0
        capture = hit / base[f"hit{target}"] if base[f"hit{target}"] else 0.0
        rows.append((lift, hit, total, rate, capture, feature, kind, bucket))
    rows.sort(reverse=True)

    print(f"top_buckets_by_lift_at_depth_{target}")
    print("lift hit total rate capture kind bucket feature")
    for lift, hit, total, rate, capture, feature, kind, bucket in rows[: args.report_top]:
        print(f"{lift:.6f} {hit} {total} {rate:.9f} {capture:.6f} {kind} {bucket} {feature}")

    print()
    print(f"all_feature_buckets_depth_{target}")
    print("feature kind bucket hit total rate lift capture")
    for lift, hit, total, rate, capture, feature, kind, bucket in sorted(rows, key=lambda r: (r[5], r[6], r[7])):
        print(f"{feature} {kind} {bucket} {hit} {total} {rate:.9f} {lift:.6f} {capture:.6f}")


if __name__ == "__main__":
    main()

