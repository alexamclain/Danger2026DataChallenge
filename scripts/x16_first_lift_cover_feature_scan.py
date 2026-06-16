#!/usr/bin/env python3
"""Scan cheap features on the first X1(16)->X1(32) lift cover.

This is a research helper, not a production kernel.  It samples the p23
X1(16) nonsplit stream conditioned on the exact first-lift squareclass

    z^2 = H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2),

then asks whether simple sign-invariant characters on this cover predict
deeper first-branch halving survival.  The scanned features are norms

    Norm(q(y) + z) = q(y)^2 - H(y),

for small linear and quadratic q.  A stable, high-lift feature here would be
evidence for a cheap tower-section label beyond the already-demoted d-gate.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import defaultdict
from dataclasses import dataclass


P23 = 100000000000000000000117


def inv(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError
    return pow(a, p - 2, p)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def sqrt_p5(a: int, p: int, sqrtm1: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    x = pow(a, (p + 3) // 8, p)
    x2 = x * x % p
    if x2 == a:
        return x
    if x2 == (-a) % p:
        x = x * sqrtm1 % p
        if x * x % p == a:
            return x
    return None


def x16_A_num(y: int, p: int) -> int:
    y2 = y * y % p
    y3 = y2 * y % p
    y4 = y2 * y2 % p
    y5 = y4 * y % p
    y6 = y3 * y3 % p
    y7 = y6 * y % p
    y8 = y4 * y4 % p
    return (
        y8
        - 8 * y7
        + 24 * y6
        - 32 * y5
        + 8 * y4
        + 32 * y3
        - 48 * y2
        + 32 * y
        - 8
    ) % p


def x16_y_nonsplit_value(y: int, p: int) -> int:
    y2 = y * y % p
    return ((y2 - 2) * (y2 - 4 * y + 2)) % p


def x16_y_first_d_value(y: int, p: int) -> int:
    y2 = y * y % p
    return ((y - 1) * (y2 - 2) * (y2 - 2 * y + 2)) % p


def x16_roots_for_y(y: int, p: int, sqrtm1: int) -> list[int]:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return []
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    D = (qb * qb - 4 * qa * qc) % p
    sd = sqrt_p5(D, p, sqrtm1)
    if sd is None:
        return []
    inv_2qa = inv(2 * qa, p)
    return [((sd - qb) * inv_2qa) % p, ((-sd - qb) * inv_2qa) % p]


def x16_root_to_montgomery(y: int, x: int, p: int) -> tuple[int, int] | None:
    ym1 = (y - 1) % p
    denA = 4 * pow(ym1, 4, p) % p
    denx = (x - y) % p
    if denA == 0 or denx == 0:
        return None
    A = x16_A_num(y, p) * inv(denA, p) % p
    xP = x * inv(denx, p) % p
    if A <= 2 or A >= p - 2:
        return None
    return A, xP


def halve_once_first(p: int, A: int, x: int, sqrtm1: int) -> int | None:
    inv2 = (p + 1) // 2
    d = (x * x + A * x + 1) % p
    sd = sqrt_p5(d, p, sqrtm1)
    if sd is None:
        return None
    for rd in (sd, (-sd) % p):
        u = (2 * x + 2 * rd) % p
        sw = sqrt_p5((u * u - 4) % p, p, sqrtm1)
        if sw is None:
            continue
        for cand in (((u + sw) * inv2) % p, ((u - sw) * inv2) % p):
            if cand:
                return cand
    return None


def first_branch_depth(p: int, A: int, x: int, sqrtm1: int, target_depth: int) -> int:
    depth = 4
    while depth < target_depth:
        nx = halve_once_first(p, A, x, sqrtm1)
        if nx is None:
            break
        x = nx
        depth += 1
    return depth


@dataclass(frozen=True)
class Feature:
    name: str
    coeffs: tuple[int, ...]

    def q(self, y: int, p: int) -> int:
        total = 0
        yp = 1
        for c in self.coeffs:
            total = (total + c * yp) % p
            yp = yp * y % p
        return total

    def value(self, y: int, H: int, p: int) -> int:
        q = self.q(y, p)
        return (q * q - H) % p


def canonical_coeffs(coeffs: tuple[int, ...]) -> tuple[int, ...]:
    coeffs = tuple(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs = coeffs[:-1]
    if not coeffs:
        return ()
    for c in reversed(coeffs):
        if c != 0:
            if c < 0:
                coeffs = tuple(-x for x in coeffs)
            return coeffs
    return ()


def build_features(max_coeff: int) -> list[Feature]:
    seen: set[tuple[int, ...]] = set()
    out: list[Feature] = []
    for degree in (0, 1, 2):
        ranges = [range(-max_coeff, max_coeff + 1) for _ in range(degree + 1)]
        stack: list[tuple[int, ...]] = [()]
        for r in ranges:
            stack = [prefix + (v,) for prefix in stack for v in r]
        for coeffs in stack:
            key = canonical_coeffs(coeffs)
            if not key or key in seen:
                continue
            seen.add(key)
            terms = []
            for i, c in enumerate(key):
                if c == 0:
                    continue
                if i == 0:
                    terms.append(str(c))
                elif i == 1:
                    terms.append(f"{c}*y")
                else:
                    terms.append(f"{c}*y^{i}")
            qname = "+".join(terms).replace("+-", "-")
            out.append(Feature(name=f"Norm({qname}+z)", coeffs=key))
    return out


def update_stats(stats: dict, feature: Feature, sign: int, depth: int, depths: list[int]) -> None:
    if sign == 0:
        return
    row = stats[(feature.name, sign)]
    row["total"] += 1
    for d in depths:
        if depth >= d:
            row[f"hit{d}"] += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=P23)
    ap.add_argument("--accepted", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20260626)
    ap.add_argument("--target-depth", type=int, default=12)
    ap.add_argument("--depths", type=int, nargs="+", default=[6, 8, 10, 12])
    ap.add_argument("--max-coeff", type=int, default=2)
    ap.add_argument("--report-top", type=int, default=30)
    args = ap.parse_args()

    p = args.p
    if p % 8 != 5:
        raise SystemExit("This helper currently expects p == 5 mod 8.")
    sqrtm1 = pow(2, (p - 1) // 4, p)
    features = build_features(args.max_coeff)
    rng = random.Random(args.seed)
    pbits = p.bit_length()

    stats: dict = defaultdict(lambda: defaultdict(int))
    base = defaultdict(int)
    attempts = 0
    accepted = 0
    y_accept = 0
    root_rows = 0
    t0 = time.time()

    while accepted < args.accepted:
        attempts += 1
        y = rng.getrandbits(pbits)
        if y >= p or y == 0:
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

        for x in roots:
            mapped = x16_root_to_montgomery(y, x, p)
            if mapped is None:
                continue
            A, xP = mapped
            depth = first_branch_depth(p, A, xP, sqrtm1, args.target_depth)
            root_rows += 1
            accepted += 1
            base["total"] += 1
            for d in args.depths:
                if depth >= d:
                    base[f"hit{d}"] += 1

            for feature in features:
                sign = legendre(feature.value(y, H, p), p)
                update_stats(stats, feature, sign, depth, args.depths)
            if accepted >= args.accepted:
                break

    elapsed = time.time() - t0
    print("X1(16) first-lift cover feature scan")
    print(f"p = {p}")
    print(f"seed = {args.seed}")
    print(f"target_depth = {args.target_depth}")
    print(f"depths = {' '.join(str(d) for d in args.depths)}")
    print(f"features = {len(features)}")
    print(f"accepted_curve_rows = {accepted}")
    print(f"accepted_y_values = {y_accept}")
    print(f"root_rows_seen = {root_rows}")
    print(f"attempts = {attempts}")
    print(f"elapsed_seconds = {elapsed:.6f}")
    print(f"accepted_curve_rate = {accepted / elapsed:.3f}/s")
    print()
    print("base total " + " ".join(f"hit{d} rate{d}" for d in args.depths))
    vals = [f"{base['total']}"]
    for d in args.depths:
        hit = base[f"hit{d}"]
        vals.extend([str(hit), f"{hit / base['total']:.9f}"])
    print(" ".join(vals))
    print()

    target = max(args.depths)
    base_rate = base[f"hit{target}"] / base["total"] if base["total"] else 0.0
    rows = []
    by_name: dict[str, dict[int, dict]] = defaultdict(dict)
    for (name, sign), row in stats.items():
        by_name[name][sign] = row
        total = row["total"]
        hit = row[f"hit{target}"]
        rate = hit / total if total else 0.0
        lift = rate / base_rate if base_rate else 0.0
        capture = hit / base[f"hit{target}"] if base[f"hit{target}"] else 0.0
        rows.append((lift, hit, total, rate, capture, name, sign))
    rows.sort(reverse=True)

    print(f"top_features_by_lift_at_depth_{target}")
    print("lift hit total rate capture sign feature")
    for lift, hit, total, rate, capture, name, sign in rows[: args.report_top]:
        print(f"{lift:.6f} {hit} {total} {rate:.9f} {capture:.6f} {sign:+d} {name}")

    print()
    print(f"best_balanced_features_depth_{target}")
    print("score lift_plus lift_minus hit_plus hit_minus total_plus total_minus feature")
    balanced = []
    for name, signs in by_name.items():
        if 1 not in signs or -1 not in signs:
            continue
        rp = signs[1]
        rm = signs[-1]
        hp = rp[f"hit{target}"]
        hm = rm[f"hit{target}"]
        tp = rp["total"]
        tm = rm["total"]
        lp = (hp / tp / base_rate) if tp and base_rate else 0.0
        lm = (hm / tm / base_rate) if tm and base_rate else 0.0
        score = max(lp, lm) * min(tp, tm) / base["total"]
        balanced.append((score, lp, lm, hp, hm, tp, tm, name))
    balanced.sort(reverse=True)
    for score, lp, lm, hp, hm, tp, tm, name in balanced[: args.report_top]:
        print(f"{score:.6f} {lp:.6f} {lm:.6f} {hp} {hm} {tp} {tm} {name}")


if __name__ == "__main__":
    main()
