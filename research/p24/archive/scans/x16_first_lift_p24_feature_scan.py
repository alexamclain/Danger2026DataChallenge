#!/usr/bin/env python3
"""p24-congruence scan for first X1(16)->X1(32) lift-cover features.

The first lift from Sutherland's X1(16) parameter y has cover

    z^2 = H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2).

For p23, p == 1 mod 4 and the quotient factors u - 2 +/- 2i live in Fp.
For p24-style primes, p == 3 mod 4, so i lives in Fp2.  This helper tests
whether the visible quotient/norm characters over Fp and Fp2 predict deeper
first-branch halving once we condition on:

    * nonsplit X1(16), and
    * H(y) square, i.e. the first lift to X1(32) exists.

It is a calibration probe only, not a production search.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import defaultdict
from dataclasses import dataclass

from x16_p24_calibration import (
    P24,
    find_calibration_prime,
    first_branch_depth,
    inv,
    legendre,
    sqrt_mod,
    x16_roots_for_y,
    y_predicts_nonsplit,
)


Fp2 = tuple[int, int]


def fp2_mul(x: Fp2, y: Fp2, p: int) -> Fp2:
    a, b = x
    c, d = y
    return ((a * c - b * d) % p, (a * d + b * c) % p)


def fp2_pow(x: Fp2, n: int, p: int) -> Fp2:
    out: Fp2 = (1, 0)
    base = x
    while n:
        if n & 1:
            out = fp2_mul(out, base, p)
        base = fp2_mul(base, base, p)
        n >>= 1
    return out


def fp2_square_class(x: Fp2, p: int) -> str:
    if x == (0, 0):
        return "0"
    q = fp2_pow(x, (p * p - 1) // 2, p)
    if q == (1, 0):
        return "+1"
    if q == (p - 1, 0):
        return "-1"
    return "?"


def fp2_quartic_class(x: Fp2, p: int) -> str:
    if x == (0, 0):
        return "0"
    q = fp2_pow(x, (p * p - 1) // 4, p)
    labels = {
        (1, 0): "+1",
        (p - 1, 0): "-1",
        (0, 1): "+i",
        (0, p - 1): "-i",
    }
    return labels.get(q, "?")


def first_lift_H(y: int, p: int) -> int:
    y2 = y * y % p
    return (y - 1) * (y2 - 2) % p * (y2 - 2 * y + 2) % p


def quotient_u(y: int, p: int) -> int | None:
    den = (y - 1) % p
    if den == 0:
        return None
    return (y * y - 2) * inv(den, p) % p


@dataclass(frozen=True)
class NormFeature:
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


def norm_features(max_coeff: int) -> list[NormFeature]:
    out: list[NormFeature] = []
    seen: set[tuple[int, ...]] = set()
    for degree in (0, 1, 2):
        stack = [()]
        for _ in range(degree + 1):
            stack = [prefix + (v,) for prefix in stack for v in range(-max_coeff, max_coeff + 1)]
        for coeffs in stack:
            coeffs = tuple(coeffs)
            while coeffs and coeffs[-1] == 0:
                coeffs = coeffs[:-1]
            if not coeffs:
                continue
            lead = next(c for c in reversed(coeffs) if c)
            if lead < 0:
                coeffs = tuple(-c for c in coeffs)
            if coeffs in seen:
                continue
            seen.add(coeffs)
            terms = []
            for i, c in enumerate(coeffs):
                if c == 0:
                    continue
                if i == 0:
                    terms.append(str(c))
                elif i == 1:
                    terms.append(f"{c}*y")
                else:
                    terms.append(f"{c}*y^{i}")
            name = "Norm(" + "+".join(terms).replace("+-", "-") + "+z)"
            out.append(NormFeature(name, coeffs))
    return out


def add_bucket(stats: dict, feature: str, kind: str, bucket: str, depth: int, depths: list[int]) -> None:
    row = stats[(feature, kind, bucket)]
    row["total"] += 1
    for d in depths:
        if depth >= d:
            row[f"hit{d}"] += 1


def feature_labels(y: int, H: int, p: int, norms: list[NormFeature]) -> list[tuple[str, str, str]]:
    u = quotient_u(y, p)
    if u is None:
        return []
    out: list[tuple[str, str, str]] = []

    fp_values = {
        "u": u,
        "u-2": (u - 2) % p,
        "(u-2)^2+4": ((u - 2) * (u - 2) + 4) % p,
    }
    for name, val in fp_values.items():
        out.append((name, "legendre", f"{legendre(val, p):+d}"))

    alpha_plus: Fp2 = ((u - 2) % p, 2 % p)
    alpha_minus: Fp2 = ((u - 2) % p, (-2) % p)
    for name, val in (("u-2+2i", alpha_plus), ("u-2-2i", alpha_minus)):
        out.append((name, "fp2_square", fp2_square_class(val, p)))
        out.append((name, "fp2_quartic", fp2_quartic_class(val, p)))

    for nf in norms:
        out.append((nf.name, "legendre", f"{legendre(nf.value(y, H, p), p):+d}"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0)
    ap.add_argument("--start", type=int, default=50_000)
    ap.add_argument("--extra-mod", type=int, default=3 * 5 * 7 * 11)
    ap.add_argument("--accepted", type=int, default=20_000)
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--target-depth", type=int, default=12)
    ap.add_argument("--depths", type=int, nargs="+", default=[6, 8, 10, 12])
    ap.add_argument("--norm-coeff", type=int, default=2)
    ap.add_argument("--report-top", type=int, default=30)
    args = ap.parse_args()

    modulus = 8 * args.extra_mod
    p = args.p or find_calibration_prime(args.start, modulus, P24 % modulus)
    if p % 4 != 3:
        raise SystemExit("This p24 Fp2 quotient probe expects p == 3 mod 4.")

    rng = random.Random(args.seed)
    pbits = p.bit_length()
    norms = norm_features(args.norm_coeff)
    stats: dict = defaultdict(lambda: defaultdict(int))
    base = defaultdict(int)
    attempts = 0
    accepted = 0
    accepted_y = 0
    t0 = time.time()

    while accepted < args.accepted:
        attempts += 1
        y = rng.getrandbits(pbits)
        if y >= p or y in (0, 1):
            continue
        if not y_predicts_nonsplit(y, p):
            continue

        H = first_lift_H(y, p)
        if H == 0 or sqrt_mod(H, p) is None:
            continue

        roots = x16_roots_for_y(y, p)
        if not roots:
            continue
        labels = feature_labels(y, H, p, norms)
        accepted_y += 1

        for A, xP in roots:
            depth = first_branch_depth(p, A, xP, args.target_depth)
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
    base_hit = base[f"hit{target}"]
    base_rate = base_hit / base["total"] if base["total"] else 0.0

    print("p24 X1(16) first-lift quotient/norm feature scan")
    print(f"p={p}")
    print(f"p_mod_8={p % 8}")
    print(f"p24_mod_modulus={P24 % modulus} modulus={modulus}")
    print(f"seed={args.seed}")
    print(f"target_depth={args.target_depth}")
    print(f"depths={' '.join(str(d) for d in args.depths)}")
    print(f"accepted_curve_rows={accepted}")
    print(f"accepted_y_values={accepted_y}")
    print(f"attempts={attempts}")
    print(f"norm_feature_count={len(norms)}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"accepted_curve_rate={accepted / elapsed:.3f}/s")
    print("base total " + " ".join(f"hit{d} rate{d}" for d in args.depths))
    vals = [str(base["total"])]
    for d in args.depths:
        hit = base[f"hit{d}"]
        vals.extend([str(hit), f"{hit / base['total']:.9f}"])
    print(" ".join(vals))

    rows = []
    for (feature, kind, bucket), row in stats.items():
        total = row["total"]
        hit = row[f"hit{target}"]
        rate = hit / total if total else 0.0
        lift = rate / base_rate if base_rate else 0.0
        capture = hit / base_hit if base_hit else 0.0
        rows.append((lift, hit, total, rate, capture, feature, kind, bucket))
    rows.sort(reverse=True)

    print(f"top_buckets_by_lift_at_depth_{target}")
    print("lift hit total rate capture kind bucket feature")
    for lift, hit, total, rate, capture, feature, kind, bucket in rows[: args.report_top]:
        print(f"{lift:.6f} {hit} {total} {rate:.9f} {capture:.6f} {kind} {bucket} {feature}")
    print("conclusion=features_are_constant_factor_only_unless_stable_high_lift_bucket_reappears_on_holdout")


if __name__ == "__main__":
    main()
