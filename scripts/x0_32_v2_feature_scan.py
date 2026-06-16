#!/usr/bin/env python3
"""Scan cheap X0(32) parameter features against curve-level v2(#E).

This is a small-prime research helper.  After the relevant-v2 probe, the
nonsplit X0(32) question is no longer a state-orientation question: in the
nonsplit/cyclic case, order-32 state depth is controlled by curve-level
v2(p + 1 - t).  This script asks whether cheap features of the X0(32)
parameterization predict higher curve-level v2 before doing exact trace work.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter
from dataclasses import dataclass

import sympy as sp

import x0_32_small_prime_probe as x0
import x16_trace_residue_calibration as trace_cal


@dataclass(frozen=True)
class Row:
    v: int
    u: int
    A: int
    curve_v2: int
    split_class: str


def inv_or_none(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def feature_values(p: int, v: int, u: int, A: int) -> dict[str, int]:
    v %= p
    u %= p
    A %= p
    u2 = u * u % p
    v2 = v * v % p
    A2 = A * A % p
    vals: dict[str, int] = {
        "u": u,
        "u-1": u - 1,
        "u+1": u + 1,
        "u^2+1": u2 + 1,
        "u^2+u+1": u2 + u + 1,
        "u^2-u+1": u2 - u + 1,
        "v": v,
        "v-1": v - 1,
        "v+1": v + 1,
        "v^2-1": v2 - 1,
        "v^2+1": v2 + 1,
        "u+v": u + v,
        "u-v": u - v,
        "u*v": u * v,
        "u^2-v^2": u2 - v2,
        "u^2+v^2": u2 + v2,
        "A": A,
        "A-2": A - 2,
        "A+2": A + 2,
        "A^2-4": A2 - 4,
        "A^2+4": A2 + 4,
        "A*u+1": A * u + 1,
        "A*v+1": A * v + 1,
    }
    inv_u = inv_or_none(u, p)
    inv_v = inv_or_none(v, p)
    if inv_u is not None:
        vu = v * inv_u % p
        vals["v/u"] = vu
        vals["v/u-1"] = vu - 1
        vals["v/u+1"] = vu + 1
    if inv_v is not None:
        uv = u * inv_v % p
        vals["u/v"] = uv
        vals["u/v-1"] = uv - 1
        vals["u/v+1"] = uv + 1
    return vals


def feature_labels(p: int, v: int, u: int, A: int, quartic_root: int | None) -> list[str]:
    labels: list[str] = []
    for name, value in feature_values(p, v, u, A).items():
        chi = x0.legendre(value, p)
        labels.append(f"{name}:leg={chi:+d}")
        if quartic_root is not None and chi != 0:
            q = pow(value % p, (p - 1) // 4, p)
            if q == 1:
                cls = "+1"
            elif q == p - 1:
                cls = "-1"
            elif q == quartic_root:
                cls = "+i"
            elif q == (-quartic_root) % p:
                cls = "-i"
            else:
                cls = "?"
            labels.append(f"{name}:quartic={cls}")
    return labels


def collect_rows(p: int, samples: int, seed: int, root_method: str) -> list[Row]:
    rng = random.Random(seed)
    trace_cache: dict[int, int] = {}
    rows: list[Row] = []
    for _ in range(samples):
        v = rng.randrange(0, p)
        rhs = (1 - pow(v, 4, p)) % p
        for u in x0.sqrt_mod_roots(rhs, p):
            if u in (0, 1, p - 1):
                continue
            j = x0.j_x0_32(u, p)
            if j is None:
                continue
            for A in x0.montgomery_As_from_j(j, p, root_method):
                if A not in trace_cache:
                    trace = trace_cal.trace_for_montgomery_A(p, A)
                    trace_cache[A] = x0.v2(p + 1 - trace)
                split_class = "split" if x0.legendre(A * A - 4, p) == 1 else "nonsplit"
                rows.append(Row(v=v, u=u, A=A, curve_v2=trace_cache[A], split_class=split_class))
    return rows


def print_top(rows: list[Row], p: int, thresholds: list[int], top: int, quartic: bool) -> None:
    quartic_root = pow(2, (p - 1) // 4, p) if quartic and p % 4 == 1 else None
    label_totals: Counter[str] = Counter()
    label_hits: dict[int, Counter[str]] = {thr: Counter() for thr in thresholds}
    for row in rows:
        labels = feature_labels(p, row.v, row.u, row.A, quartic_root)
        for label in labels:
            label_totals[label] += 1
            for thr in thresholds:
                if row.curve_v2 >= thr:
                    label_hits[thr][label] += 1

    total = len(rows)
    for thr in thresholds:
        base_hits = sum(1 for row in rows if row.curve_v2 >= thr)
        base_rate = base_hits / total if total else 0.0
        print(f"threshold_v2>={thr} base_hits={base_hits}/{total} base_rate={base_rate:.6f}")
        ranked: list[tuple[float, str]] = []
        for label, selected in label_totals.items():
            if selected == 0:
                continue
            hits = label_hits[thr][label]
            if hits == 0:
                continue
            precision = hits / selected
            coverage = selected / total
            capture = hits / base_hits if base_hits else 0.0
            lift = precision / base_rate if base_rate else 0.0
            score = lift * capture
            ranked.append(
                (
                    score,
                    (
                        f"feature={label} selected={selected} hits={hits} "
                        f"coverage={coverage:.4f} capture={capture:.4f} "
                        f"precision={precision:.4f} lift={lift:.3f}"
                    ),
                )
            )
        for _score, line in sorted(ranked, reverse=True)[:top]:
            print(line)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--samples", type=int, default=80)
    ap.add_argument("--seed", type=int, default=563)
    ap.add_argument("--root-method", choices=("auto", "brute", "sympy"), default="auto")
    ap.add_argument("--class-filter", choices=("all", "split", "nonsplit"), default="nonsplit")
    ap.add_argument("--thresholds", default="6,7,8")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--quartic", action="store_true")
    args = ap.parse_args()

    if args.p <= 3 or not sp.isprime(args.p):
        raise SystemExit("--p must be an odd prime")
    root_method = args.root_method
    if root_method == "auto":
        root_method = "brute" if args.p <= 200_000 else "sympy"
    thresholds = [int(x) for x in args.thresholds.split(",") if x]

    start = time.perf_counter()
    all_rows = collect_rows(args.p, args.samples, args.seed, root_method)
    rows = [row for row in all_rows if args.class_filter == "all" or row.split_class == args.class_filter]
    elapsed = time.perf_counter() - start

    print("X0(32) curve-v2 cheap feature scan")
    print(f"p={args.p}")
    print(f"samples={args.samples}")
    print(f"seed={args.seed}")
    print(f"root_method={root_method}")
    print(f"class_filter={args.class_filter}")
    print(f"quartic_features={1 if args.quartic else 0}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"all_rows={len(all_rows)}")
    print(f"rows={len(rows)}")
    print("split_class_counts=" + ",".join(f"{k}:{Counter(row.split_class for row in all_rows)[k]}" for k in sorted(Counter(row.split_class for row in all_rows))))
    print("curve_v2_hist=" + ",".join(f"{k}:{Counter(row.curve_v2 for row in rows)[k]}" for k in sorted(Counter(row.curve_v2 for row in rows))))
    print()
    print_top(rows, args.p, thresholds, args.top, args.quartic)


if __name__ == "__main__":
    main()
