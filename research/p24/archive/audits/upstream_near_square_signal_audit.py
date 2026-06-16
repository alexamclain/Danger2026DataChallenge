#!/usr/bin/env python3
"""Focused signal audit for Sutherland one-witness data.

The broad streaming audit prints a large near-square table.  This helper keeps
only the features relevant to the p24 analogy: primes p = n^2 + c, especially
c = 7 and n == 0 mod 8, and cheap Montgomery/x-only Legendre labels.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter
from pathlib import Path
from statistics import mean

from upstream_dataset_feature_audit import (
    legendre,
    quantiles,
    target_order_count,
    terminal_branch,
    verifier_k,
)

ROOT = Path(__file__).resolve().parent


def rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="ascii") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield tuple(int(part) for part in line.split(","))


def near_square_class(p: int, max_c: int) -> tuple[int, int] | None:
    n = math.isqrt(p)
    c = p - n * n
    if 0 < c <= max_c:
        return n, c
    return None


def safe_inv(value: int, p: int) -> int | None:
    value %= p
    if value == 0:
        return None
    return pow(value, -1, p)


def feature_values(p: int, A: int, x: int) -> dict[str, int]:
    inv_x = safe_inv(x, p)
    s = None if inv_x is None else (x + inv_x) % p
    rhs = x * (x * x + A * x + 1) % p
    values = {
        "A2-4": A * A - 4,
        "A+2": A + 2,
        "A-2": A - 2,
        "x": x,
        "x+1": x + 1,
        "x-1": x - 1,
        "x2-1": x * x - 1,
        "curve_rhs": rhs,
    }
    if s is not None:
        values["s=x+1/x"] = s
        values["s+A"] = s + A
        values["s+2"] = s + 2
        values["s-2"] = s - 2
    return values


def summarize(label: str, triples: list[tuple[int, int, int]], max_terminal: int) -> None:
    print(f"{label}_rows={len(triples)}")
    if not triples:
        return

    feature_counts: dict[str, Counter[int]] = {}
    terminal_counts: Counter[str] = Counter()
    target_counts: Counter[int] = Counter()
    min_a: list[float] = []
    min_x: list[float] = []

    for index, (p, A, x) in enumerate(triples):
        for name, value in feature_values(p, A, x).items():
            feature_counts.setdefault(name, Counter())[legendre(value, p)] += 1
        target_counts[target_order_count(p)] += 1
        min_a.append(min(A, p - A) / p)
        min_x.append(min(x, p - x) / p)
        if index < max_terminal:
            terminal_counts[terminal_branch(p, A, x, verifier_k(p))] += 1

    print(f"{label}_terminal_counts={dict(sorted(terminal_counts.items()))}")
    print(f"{label}_target_order_count_hist={dict(sorted(target_counts.items()))}")
    qs = (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99)
    print(f"{label}_min_A_mean={mean(min_a):.6f}")
    print(f"{label}_min_x_mean={mean(min_x):.6f}")
    print(f"{label}_min_A_quantiles=" + ",".join(f"{v:.6f}" for v in quantiles(min_a, qs)))
    print(f"{label}_min_x_quantiles=" + ",".join(f"{v:.6f}" for v in quantiles(min_x, qs)))
    print(f"{label}_feature_counts")
    for name in sorted(feature_counts):
        print(f"  {name}: {dict(sorted(feature_counts[name].items()))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "upstream_DANGER3" / "pp24.txt.gz",
    )
    parser.add_argument("--near-c", type=int, default=255)
    parser.add_argument("--max-terminal", type=int, default=50_000)
    args = parser.parse_args()

    all_sample: list[tuple[int, int, int]] = []
    near_rows: list[tuple[int, int, int]] = []
    p24_analog: list[tuple[int, int, int]] = []
    c_counts: Counter[int] = Counter()

    for row_index, (p, A, x) in enumerate(rows(args.source)):
        if len(all_sample) < 50_000:
            all_sample.append((p, A, x))
        near = near_square_class(p, args.near_c)
        if near is None:
            continue
        n, c = near
        c_counts[c] += 1
        if len(near_rows) < 50_000:
            near_rows.append((p, A, x))
        if c == 7 and n % 8 == 0:
            p24_analog.append((p, A, x))

    print("upstream near-square signal audit")
    print(f"source={args.source}")
    print(f"near_c_le_{args.near_c}_distinct_c={len(c_counts)}")
    print(f"near_c7_count={c_counts[7]}")
    summarize("initial_all_sample", all_sample, args.max_terminal)
    summarize("near_square_sample", near_rows, args.max_terminal)
    summarize("p24_analog_c7_n0mod8", p24_analog, args.max_terminal)


if __name__ == "__main__":
    main()
