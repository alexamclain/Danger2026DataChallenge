#!/usr/bin/env python3
"""Post-Dplus U6 Kummer parity probe.

The reciprocal tower shows that Dplus rows have four U6 values after

    F_A(X(t), U5) = 0
    F_A(U5, U6) = 0.

The next selected class is chi(x6)=chi(U6+2).  This probe checks whether that
class is a branch-choice bit across the four U6 values or a single bit attached
to the Dplus source row.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_trace_norm_dplus_a_coordinate_bridge_probe import a_from_t
from p27_trace_norm_dplus_reciprocal_tower_probe import P, f_a, parse_seed_groups, x_parent_from_t
from p27_trace_norm_post_dplus_probe import (
    candidate_roots,
    label2,
    sign_name,
    trace_norm_d_class_parts,
    transfer,
)


def sign_pattern(signs: list[int]) -> str:
    return "".join("+" if sign == 1 else "-" if sign == -1 else "0" for sign in sorted(signs))


def collect_group(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_y: int,
) -> Counter[str]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    seen_y: set[int] = set()
    stats: Counter[str] = Counter()

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

                    U6_signs: dict[int, int] = {}
                    x6_signs: dict[int, int] = {}
                    for _root_index, cand_A, xp in candidates:
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
                            if f_a(A, X, U5) != 0:
                                stats["F_X_U5_mismatch"] += 1
                            d2, x6s = label2.halve_all(cand_A, x5)
                            stats[f"d2_{sign_name(d2)}"] += 1
                            if d2 != 1:
                                stats["d2_failure"] += 1
                                continue
                            for x6 in x6s:
                                x6 %= P
                                U6 = (x6 + transfer.inv(x6)) % P
                                if f_a(A, U5, U6) != 0:
                                    stats["F_U5_U6_mismatch"] += 1
                                u6_sign = transfer.chi(U6 + 2)
                                x6_sign = transfer.chi(x6)
                                if u6_sign != x6_sign:
                                    stats["x6_u6plus2_mismatch"] += 1
                                previous = U6_signs.get(U6)
                                if previous is not None and previous != u6_sign:
                                    stats["U6_duplicate_sign_mismatch"] += 1
                                U6_signs[U6] = u6_sign
                                x6_signs[x6] = x6_sign

                    stats[f"U6_count_{len(U6_signs)}"] += 1
                    if len(U6_signs) != 4:
                        stats["unexpected_U6_count"] += 1
                        continue

                    signs = list(U6_signs.values())
                    stats[f"U6_pattern_{sign_pattern(signs)}"] += 1
                    plus_count = sum(1 for sign in signs if sign == 1)
                    minus_count = sum(1 for sign in signs if sign == -1)
                    stats[f"U6_plus_count_{plus_count}"] += 1
                    stats[f"U6_minus_count_{minus_count}"] += 1
                    product = 1
                    for sign in signs:
                        product *= sign
                    stats[f"U6_sign_product_{sign_name(product)}"] += 1
                    if len(set(signs)) == 1:
                        stats["U6_uniform_sign"] += 1
                    else:
                        stats["U6_mixed_sign"] += 1

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

    print("p27 trace/norm Dplus U6 parity probe")
    print("question = is chi(U6+2)=chi(x6) a branch-choice bit or a Dplus-row bit?")
    print(f"p = {P}")
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
    print("  U6 branch class descends to Dplus row iff U6_mixed_sign=0")
    print("  sourceable only if the descended row bit is named by CAS/H90/theta data")
    print("p27_trace_norm_dplus_u6_parity_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
