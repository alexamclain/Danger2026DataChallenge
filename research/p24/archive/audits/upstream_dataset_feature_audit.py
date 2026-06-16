#!/usr/bin/env python3
"""Data audit for Sutherland's upstream DANGER3 Pomerance datasets.

The upstream repository contains three useful kinds of small-prime data:

* pp12: all triples through 2^12,
* pp16A: all distinct valid (p,A) prefixes through 2^16,
* pp24: one valid triple for each prime through 2^24.

This script deliberately avoids point counting.  It measures the features that
are visible directly from the certificate and from the Montgomery x-only
verifier: split/nonsplit class, terminal 2-torsion branch, simple size
statistics, and the observed scaling of the valid A-set in the all-prefix
file.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_DANGER3"

LARGE_TRIPLES = [
    (10**12 + 39, 249665736657, 326654630116, "readme_1e12"),
    (10**13 + 37, 3975240388830, 3363870254431, "readme_1e13"),
    (10**14 + 31, 29435557274911, 60189380554757, "readme_1e14"),
    (10**15 + 37, 501253912199979, 227109452032906, "readme_1e15"),
    (10**16 + 61, 7091819576975137, 7486903304256253, "readme_1e16"),
    (10**17 + 3, 38900982538808192, 78529976024049678, "readme_1e17"),
    (10**18 + 3, 650095865875375253, 446015633473605308, "readme_1e18"),
    # The upstream README update says 10^19+61, but the verifier challenge
    # triple and local README use 10^19+51 with these A,x values.
    (10**19 + 51, 238792350205097889, 9647351248508855176, "update_1e19"),
    (10**20 + 39, 80635707401894747894, 31614069099331127513, "update_1e20"),
    (10**21 + 117, 51546435219887079991, 144666470127730980460, "update_1e21"),
    (10**22 + 9, 9992566338662824267458, 3694769590833803032125, "update_1e22"),
    (10**23 + 117, 24163028207499560363686, 64911014007772963770218, "update_1e23"),
]


@dataclass(frozen=True)
class TripleFeatures:
    p: int
    A: int
    x: int
    k: int
    split: int
    terminal: str
    fx_char: int
    min_A_ratio: float
    min_x_ratio: float


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii")
    return path.open("rt", encoding="ascii")


def rows(path: Path, limit: int | None = None):
    with open_text(path) as handle:
        for index, line in enumerate(handle):
            if limit is not None and index >= limit:
                break
            line = line.strip()
            if not line:
                continue
            yield tuple(int(part) for part in line.split(","))


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def double_xz(p: int, C: int, X: int, Z: int) -> tuple[int, int]:
    U = (X + Z) * (X + Z) % p
    V = (X - Z) * (X - Z) % p
    W = (U - V) % p
    return U * V % p, W * ((V + C * W) % p) % p


def terminal_branch(p: int, A: int, x: int, k: int) -> str:
    inv4 = pow(4, -1, p)
    C = (A + 2) * inv4 % p
    X, Z = x % p, 1
    prev = (X, Z)
    for _ in range(k):
        prev = (X, Z)
        X, Z = double_xz(p, C, X, Z)
    if Z % p != 0 or math.gcd(prev[1], p) != 1:
        return "not_verified"
    xp = prev[0] * pow(prev[1], -1, p) % p
    if xp == 0:
        return "zero_root"
    if (xp * xp + A * xp + 1) % p == 0:
        return "quadratic_root"
    return "other_root"


def target_order_count(p: int) -> int:
    k = verifier_k(p)
    step = 1 << k
    q = math.isqrt(p)
    lo = p + 1 - 2 * q
    hi = p + 1 + 2 * q
    first = lo + ((step - lo) % step)
    if first > hi:
        return 0
    return 1 + (hi - first) // step


def features_for_triple(p: int, A: int, x: int) -> TripleFeatures:
    k = verifier_k(p)
    split = legendre(A * A - 4, p)
    fx = x * (x * x + A * x + 1) % p
    return TripleFeatures(
        p=p,
        A=A,
        x=x,
        k=k,
        split=split,
        terminal=terminal_branch(p, A, x, k),
        fx_char=legendre(fx, p),
        min_A_ratio=min(A, p - A) / p,
        min_x_ratio=min(x, p - x) / p,
    )


def linreg_loglog(points: list[tuple[int, int]]) -> tuple[float, float]:
    xs = [math.log(p) for p, count in points if count > 0]
    ys = [math.log(count) for _p, count in points if count > 0]
    mx = mean(xs)
    my = mean(ys)
    var = sum((x - mx) ** 2 for x in xs)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    alpha = cov / var
    beta = my - alpha * mx
    return alpha, beta


def quantiles(values: list[float], qs: tuple[float, ...]) -> list[float]:
    if not values:
        return [0.0 for _ in qs]
    ordered = sorted(values)
    out = []
    for q in qs:
        index = min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))
        out.append(ordered[index])
    return out


def audit_one_per_prime(path: Path, limit: int | None) -> None:
    split_counts: Counter[int] = Counter()
    terminal_counts: Counter[str] = Counter()
    fx_counts: Counter[int] = Counter()
    mod8_split: Counter[tuple[int, int]] = Counter()
    target_counts: Counter[int] = Counter()
    min_A_ratios: list[float] = []
    min_x_ratios: list[float] = []
    rows_seen = 0

    for p, A, x in rows(path, limit):
        feat = features_for_triple(p, A, x)
        rows_seen += 1
        split_counts[feat.split] += 1
        terminal_counts[feat.terminal] += 1
        fx_counts[feat.fx_char] += 1
        mod8_split[(p % 8, feat.split)] += 1
        target_counts[target_order_count(p)] += 1
        min_A_ratios.append(feat.min_A_ratio)
        min_x_ratios.append(feat.min_x_ratio)

    print(f"one_per_prime_file={path}")
    print(f"rows={rows_seen}")
    print(f"split_counts={dict(sorted(split_counts.items()))}")
    print(f"terminal_counts={dict(sorted(terminal_counts.items()))}")
    print(f"fx_char_counts={dict(sorted(fx_counts.items()))}")
    print(f"target_order_count_hist={dict(sorted(target_counts.items()))}")
    print("mod8_split_counts=" + ",".join(f"{key}:{value}" for key, value in sorted(mod8_split.items())))
    qa = quantiles(min_A_ratios, (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
    qx = quantiles(min_x_ratios, (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
    print("min_A_over_p_quantiles_1_10_25_50_75_90_99=" + ",".join(f"{x:.6f}" for x in qa))
    print("min_x_over_p_quantiles_1_10_25_50_75_90_99=" + ",".join(f"{x:.6f}" for x in qx))


def audit_prefix_scaling(path: Path, limit: int | None) -> None:
    counts: Counter[int] = Counter()
    split_counts: Counter[tuple[int, int]] = Counter()
    residue_counts: Counter[tuple[int, int]] = Counter()
    for p, A in rows(path, limit):
        counts[p] += 1
        split_counts[(p, legendre(A * A - 4, p))] += 1
        residue_counts[(p % 8, legendre(A * A - 4, p))] += 1

    points = sorted(counts.items())
    alpha_all, beta_all = linreg_loglog(points)
    late = points[len(points) // 2 :]
    alpha_late, beta_late = linreg_loglog(late)
    normalized = [count / math.sqrt(p) for p, count in late]
    qn = quantiles(normalized, (0.10, 0.25, 0.50, 0.75, 0.90))

    split_total = Counter()
    for (_p, split), count in split_counts.items():
        split_total[split] += count

    print(f"prefix_file={path}")
    print(f"prime_rows={len(points)}")
    print(f"prefix_rows={sum(counts.values())}")
    print(f"loglog_good_A_exponent_all={alpha_all:.6f}")
    print(f"loglog_good_A_exponent_upper_half={alpha_late:.6f}")
    print(f"good_A_over_sqrt_p_upper_half_quantiles_10_25_50_75_90={','.join(f'{x:.6f}' for x in qn)}")
    print(f"prefix_split_counts={dict(sorted(split_total.items()))}")
    print("prefix_mod8_split_counts=" + ",".join(f"{key}:{value}" for key, value in sorted(residue_counts.items())))

    by_k: dict[int, list[tuple[int, int]]] = defaultdict(list)
    by_target_count: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for p, count in points:
        by_k[verifier_k(p)].append((p, count))
        by_target_count[target_order_count(p)].append((p, count))

    print("prefix_by_verifier_k")
    for k, k_points in sorted(by_k.items()):
        normalized_k = [count / math.sqrt(p) for p, count in k_points]
        qk = quantiles(normalized_k, (0.10, 0.25, 0.50, 0.75, 0.90))
        print(
            f"  k={k} primes={len(k_points)} mean_good_A_over_sqrt={mean(normalized_k):.6f} "
            f"quantiles_10_25_50_75_90={','.join(f'{x:.6f}' for x in qk)}"
        )

    print("prefix_by_target_order_count")
    for target_count, target_points in sorted(by_target_count.items()):
        normalized_target = [count / math.sqrt(p) for p, count in target_points]
        qt = quantiles(normalized_target, (0.10, 0.25, 0.50, 0.75, 0.90))
        print(
            f"  target_orders={target_count} primes={len(target_points)} "
            f"mean_good_A_over_sqrt={mean(normalized_target):.6f} "
            f"quantiles_10_25_50_75_90={','.join(f'{x:.6f}' for x in qt)}"
        )

    for p, count in points[-8:]:
        print(
            f"tail_prefix p={p} bitlen={p.bit_length()} good_A={count} "
            f"good_A_over_sqrt={count / math.sqrt(p):.6f} "
            f"split={split_counts[(p, 1)]} nonsplit={split_counts[(p, -1)]}"
        )


def audit_all_triple_scaling(path: Path, limit: int | None) -> None:
    triple_counts: Counter[int] = Counter()
    prefix_seen: set[tuple[int, int]] = set()
    prefix_counts: Counter[int] = Counter()
    for p, A, _x in rows(path, limit):
        triple_counts[p] += 1
        key = (p, A)
        if key not in prefix_seen:
            prefix_seen.add(key)
            prefix_counts[p] += 1

    points = sorted(triple_counts.items())
    prefix_points = sorted(prefix_counts.items())
    alpha_triples, _ = linreg_loglog(points)
    alpha_prefix, _ = linreg_loglog(prefix_points)
    ratios = [triple_counts[p] / prefix_counts[p] for p in triple_counts if prefix_counts[p]]
    qr = quantiles(ratios, (0.10, 0.25, 0.50, 0.75, 0.90))

    print(f"all_triples_file={path}")
    print(f"prime_rows={len(points)}")
    print(f"triple_rows={sum(triple_counts.values())}")
    print(f"distinct_prefix_rows={len(prefix_seen)}")
    print(f"loglog_all_triples_exponent={alpha_triples:.6f}")
    print(f"loglog_distinct_A_exponent_in_all_triples={alpha_prefix:.6f}")
    print(f"x_per_good_A_quantiles_10_25_50_75_90={','.join(f'{x:.6f}' for x in qr)}")
    for p, count in points[-8:]:
        print(
            f"tail_triples p={p} bitlen={p.bit_length()} triples={count} "
            f"distinct_A={prefix_counts[p]} x_per_A={count / prefix_counts[p]:.6f}"
        )


def audit_large_readme_triples() -> None:
    print("large_readme_triples")
    print("label p k p_mod8 split terminal fx_char min_A/p min_x/p target_orders")
    for p, A, x, label in LARGE_TRIPLES:
        feat = features_for_triple(p, A, x)
        print(
            f"{label} {p} {feat.k} {p % 8} {feat.split} {feat.terminal} "
            f"{feat.fx_char} {feat.min_A_ratio:.6f} {feat.min_x_ratio:.6f} "
            f"{target_order_count(p)}"
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--one-file", type=Path, default=UPSTREAM / "pp24.txt.gz")
    ap.add_argument("--prefix-file", type=Path, default=UPSTREAM / "pp16A.txt.gz")
    ap.add_argument("--all-triples-file", type=Path, default=UPSTREAM / "pp12.txt.gz")
    ap.add_argument("--one-limit", type=int, default=None)
    ap.add_argument("--prefix-limit", type=int, default=None)
    ap.add_argument("--all-limit", type=int, default=None)
    args = ap.parse_args()

    print("upstream DANGER3 dataset feature audit")
    audit_one_per_prime(args.one_file, args.one_limit)
    print()
    audit_prefix_scaling(args.prefix_file, args.prefix_limit)
    print()
    audit_all_triple_scaling(args.all_triples_file, args.all_limit)
    print()
    audit_large_readme_triples()


if __name__ == "__main__":
    main()
