#!/usr/bin/env python3
"""Dplus reciprocal-coordinate tower verifier.

This probe verifies the symbolic tower that sits behind the post-Dplus x6
class:

    t = y - 1
    A = (t - 1/t)^4/4 - 2
    X = xp + 1/xp = t^3 + 2*t^2 - 1/t

and the reciprocal halving correspondence

    F_A(U,V) = (V^2-4)^2
               - 4*U*(V^2-4)*(V+A)
               + 16*(V+A)^2.

For Dplus rows, the observed reciprocal coordinates satisfy:

    F_A(X,U5) = 0
    F_A(U5,U6) = 0

with U5 = x5 + 1/x5 and U6 = x6 + 1/x6.  The remaining next-gate class is
chi(x6), because chi(U6 + A)=+1.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_trace_norm_post_dplus_probe import (
    P,
    candidate_roots,
    sign_name,
    trace_norm_d_class_parts,
    transfer,
    label2,
)
from p27_trace_norm_dplus_a_coordinate_bridge_probe import a_from_t


def parse_seed_groups(raw: str) -> list[list[int]]:
    groups: list[list[int]] = []
    for part in raw.split(";"):
        part = part.strip()
        if part:
            groups.append(transfer.parse_range(part))
    return groups


def x_parent_from_t(t: int) -> int:
    return (pow(t, 3, P) + 2 * t % P * t - transfer.inv(t)) % P


def f_a(A: int, U: int, V: int) -> int:
    v2m4 = (V * V - 4) % P
    return (
        v2m4 * v2m4
        - 4 * U % P * v2m4 % P * ((V + A) % P)
        + 16 * ((V + A) % P) ** 2
    ) % P


def collect_group(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_y: int,
) -> Counter[str]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    stats: Counter[str] = Counter()
    seen_y: set[int] = set()

    for seed in seeds:
        for chunk in chunks:
            for tid in tids:
                rng = transfer.cuda_rng(seed, chunk, tid)
                for _draw in range(draws_per_thread):
                    y = transfer.rand_below96(rng, P, mask)
                    stats["raw_y_draws"] += 1
                    if y == 0:
                        stats["zero_y"] += 1
                        continue
                    if y in seen_y:
                        stats["duplicate_y"] += 1
                        continue
                    seen_y.add(y)
                    if not transfer.x16_y_predicts_nonsplit(y):
                        continue
                    stats["nonsplit_y"] += 1
                    d_class, _parts = trace_norm_d_class_parts(y)
                    stats[f"D_{sign_name(d_class)}"] += 1
                    if d_class != 1:
                        continue
                    stats["Dplus_y"] += 1

                    t = (y - 1) % P
                    if t == 0:
                        stats["zero_t"] += 1
                        continue
                    A = a_from_t(t)
                    X = x_parent_from_t(t)
                    candidates, _root_disc = candidate_roots(y)
                    if not candidates:
                        stats["Dplus_no_valid_candidate"] += 1
                        continue
                    xp_values: list[int] = []
                    U5_values: defaultdict[int, list[int]] = defaultdict(list)
                    U6_values: defaultdict[int, list[int]] = defaultdict(list)

                    for _root_index, cand_A, xp in candidates:
                        stats["Dplus_candidates"] += 1
                        xp %= P
                        xp_values.append(xp)
                        if cand_A % P != A:
                            stats["candidate_A_formula_mismatch"] += 1
                        if (xp + transfer.inv(xp)) % P != X:
                            stats["X_formula_mismatch"] += 1
                        d1, x5s = label2.halve_all(cand_A, xp)
                        stats[f"d1_{sign_name(d1)}"] += 1
                        if d1 != 1:
                            stats["d1_failure"] += 1
                            continue
                        for x5 in x5s:
                            x5 %= P
                            U5 = (x5 + transfer.inv(x5)) % P
                            U5_values[U5].append(x5)
                            if f_a(A, X, U5) != 0:
                                stats["F_X_U5_mismatch"] += 1
                            stats[f"U5_disc_{sign_name(transfer.chi(U5 * U5 - 4))}"] += 1
                            stats[f"U5_plusA_{sign_name(transfer.chi(U5 + A))}"] += 1
                            d2, x6s = label2.halve_all(cand_A, x5)
                            stats[f"d2_{sign_name(d2)}"] += 1
                            if d2 != 1:
                                stats["d2_failure"] += 1
                                continue
                            for x6 in x6s:
                                x6 %= P
                                U6 = (x6 + transfer.inv(x6)) % P
                                U6_values[U6].append(x6)
                                if f_a(A, U5, U6) != 0:
                                    stats["F_U5_U6_mismatch"] += 1
                                stats[f"U6_disc_{sign_name(transfer.chi(U6 * U6 - 4))}"] += 1
                                stats[f"U6_plusA_{sign_name(transfer.chi(U6 + A))}"] += 1
                                d3, _x7s = label2.halve_all(cand_A, x6)
                                if d3 != transfer.chi(x6):
                                    stats["d3_chix6_mismatch"] += 1

                    if len(xp_values) == 2 and xp_values[0] * xp_values[1] % P == 1:
                        stats["xp_reciprocal_pair"] += 1
                    else:
                        stats["xp_reciprocal_pair_failure"] += 1
                    stats[f"U5_count_{len(U5_values)}"] += 1
                    stats[f"U6_count_{len(U6_values)}"] += 1
                    for U5, xs in U5_values.items():
                        stats[f"U5_fiber_size_{len(xs)}"] += 1
                        if len(xs) == 2 and xs[0] * xs[1] % P != 1:
                            stats["U5_reciprocal_pair_mismatch"] += 1
                    for U6, xs in U6_values.items():
                        stats[f"U6_fiber_size_{len(xs)}"] += 1
                        if len(xs) == 2 and xs[0] * xs[1] % P != 1:
                            stats["U6_reciprocal_pair_mismatch"] += 1
                    stats["analyzed_y"] += 1
                    if max_y and stats["analyzed_y"] >= max_y:
                        return stats

    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-y", type=int, default=0)
    args = parser.parse_args()

    print("p27 trace/norm Dplus reciprocal tower probe")
    print("question = verify X -> U5 -> U6 reciprocal-coordinate tower")
    print(f"p = {P}")
    print("definitions:")
    print("  t = y - 1")
    print("  A = (t - 1/t)^4/4 - 2")
    print("  X = xp + 1/xp = t^3 + 2*t^2 - 1/t")
    print("  F_A(U,V) = (V^2-4)^2 - 4*U*(V^2-4)*(V+A) + 16*(V+A)^2")
    print("  U5 = x5 + 1/x5")
    print("  U6 = x6 + 1/x6")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"max_y = {args.max_y}")

    chunks = transfer.parse_range(args.chunks)
    tids = transfer.parse_range(args.tids)
    for index, seeds in enumerate(parse_seed_groups(args.seed_groups), start=1):
        stats = collect_group(
            seeds=seeds,
            chunks=chunks,
            tids=tids,
            draws_per_thread=args.draws_per_thread,
            max_y=args.max_y,
        )
        print_counter(f"group{index}_seeds_{','.join(str(seed) for seed in seeds)}", stats)

    print("verdict:")
    print("  reciprocal_tower_exact iff all mismatch/failure counters are zero")
    print("  CAS target = normalize F_A(X,U5)=0 and F_A(U5,U6)=0 with square side conditions")
    print("p27_trace_norm_dplus_reciprocal_tower_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
