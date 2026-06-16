#!/usr/bin/env python3
"""Full-prefix gate audit for near-square rows in pp16A.

The one-witness pp24/pp28 files choose a single representative per prime.
For p = n^2 + 7 with n == 0 mod 8, that representative always lands in the
nonsplit character gate (chi(A+2), chi(A-2), chi(A^2-4)) = (1, -1, -1).

This script checks Sutherland's all-prefix pp16A file to separate a genuine
good-A-set property from a selection bias.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from upstream_dataset_feature_audit import legendre, quantiles, target_order_count


ROOT = Path(__file__).resolve().parent
PP16A = ROOT / "upstream_DANGER3" / "pp16A.txt.gz"


def rows(path: Path):
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            p_s, a_s = line.strip().split(",")
            yield int(p_s), int(a_s)


def is_near_square(p: int, c: int, n_mod: int, n_residue: int) -> bool:
    n = math.isqrt(p)
    return p - n * n == c and n % n_mod == n_residue


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, default=PP16A)
    ap.add_argument("--c", type=int, default=7)
    ap.add_argument("--n-mod", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--min-p", type=int, default=0)
    ap.add_argument("--max-p", type=int, default=1 << 16)
    args = ap.parse_args()

    total_by_p: Counter[int] = Counter()
    gate_by_p: dict[int, Counter[tuple[int, int, int]]] = defaultdict(Counter)
    target_by_p: dict[int, int] = {}
    gate_by_target: dict[int, Counter[tuple[int, int, int]]] = defaultdict(Counter)
    total_by_target: Counter[int] = Counter()
    split_total: Counter[int] = Counter()
    gate_total: Counter[tuple[int, int, int]] = Counter()

    for p, A in rows(args.path):
        if p < args.min_p or p > args.max_p:
            continue
        if not is_near_square(p, args.c, args.n_mod, args.n_residue):
            continue
        gate = (legendre(A + 2, p), legendre(A - 2, p), legendre(A * A - 4, p))
        total_by_p[p] += 1
        gate_by_p[p][gate] += 1
        gate_total[gate] += 1
        split_total[gate[2]] += 1
        target_count = target_by_p.setdefault(p, target_order_count(p))
        gate_by_target[target_count][gate] += 1
        total_by_target[target_count] += 1

    counts = list(total_by_p.values())
    normalized = [count / math.sqrt(p) for p, count in total_by_p.items()]
    target_hist = Counter(target_by_p.values())
    dominant_gate = gate_total.most_common(1)[0][0] if gate_total else None
    dominant_capture_by_p = []
    if dominant_gate is not None:
        for p, count in total_by_p.items():
            dominant_capture_by_p.append(gate_by_p[p][dominant_gate] / count)

    print("upstream pp16A near-square full-prefix gate audit")
    print(f"path={args.path}")
    print(f"c={args.c}")
    print(f"n_mod={args.n_mod}")
    print(f"n_residue={args.n_residue}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"prime_rows={len(total_by_p)}")
    print(f"good_A_rows={sum(total_by_p.values())}")
    print(f"target_order_count_hist={dict(sorted(target_hist.items()))}")
    print(f"split_total={dict(sorted(split_total.items()))}")
    print("gate_total=" + ",".join(f"{key}:{value}" for key, value in sorted(gate_total.items())))
    print("gate_by_target_order_count")
    for target_count in sorted(gate_by_target):
        counter = gate_by_target[target_count]
        dominant = counter.most_common(1)[0][0]
        capture = counter[dominant] / total_by_target[target_count]
        print(
            f"  target_orders={target_count} total={total_by_target[target_count]} "
            f"dominant_gate={dominant} capture={capture:.6f} "
            + ",".join(f"{key}:{value}" for key, value in sorted(counter.items()))
        )
    if counts:
        print(f"mean_good_A={mean(counts):.6f}")
        print(f"mean_good_A_over_sqrt={mean(normalized):.6f}")
        print(
            "good_A_over_sqrt_quantiles_10_25_50_75_90="
            + ",".join(f"{x:.6f}" for x in quantiles(normalized, (0.10, 0.25, 0.50, 0.75, 0.90)))
        )
    if dominant_gate is not None:
        capture = gate_total[dominant_gate] / sum(total_by_p.values())
        print(f"dominant_gate={dominant_gate}")
        print(f"dominant_gate_capture={capture:.6f}")
        print(
            "dominant_gate_capture_by_p_quantiles_10_25_50_75_90="
            + ",".join(f"{x:.6f}" for x in quantiles(dominant_capture_by_p, (0.10, 0.25, 0.50, 0.75, 0.90)))
        )
    for p in sorted(total_by_p)[-12:]:
        print(
            f"tail p={p} n={math.isqrt(p)} good_A={total_by_p[p]} "
            f"good_A_over_sqrt={total_by_p[p] / math.sqrt(p):.6f} "
            f"dominant_gate_count={gate_by_p[p][dominant_gate] if dominant_gate is not None else 0}"
        )
    print("conclusion=near_square_one_witness_gate_must_be_checked_against_full_prefix_density")


if __name__ == "__main__":
    main()
