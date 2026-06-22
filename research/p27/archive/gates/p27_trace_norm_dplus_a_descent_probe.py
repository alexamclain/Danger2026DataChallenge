#!/usr/bin/env python3
"""A-descent bridge test for trace/norm Dplus rows.

The trace/norm Dplus lane and the conic/A-line lane have been developed as
separate frontiers.  Dplus is an exact first-two-selected-gate prefix in the
C-style raw-y stream; the A-line lane shows that later selected bits descend to
whole A fibers on the legal label-2 source.

This probe asks whether post-Dplus d3/d4 in the trace/norm stream also descend
to A.  If yes, Dplus post-gate work should be routed through A-level Kummer
class extraction.  If no, trace/norm keeps an independent orientation payload.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_trace_norm_post_dplus_probe import (
    P,
    candidate_roots,
    selected_halving_profile,
    trace_norm_d_class_parts,
    transfer,
)


def sign_label(value: int) -> str:
    if value == 1:
        return "plus"
    if value == -1:
        return "minus"
    if value == 0:
        return "zero"
    return f"other_{value}"


def parse_seed_groups(raw: str) -> list[list[int]]:
    groups: list[list[int]] = []
    for group in raw.split(";"):
        group = group.strip()
        if not group:
            continue
        groups.append(transfer.parse_range(group))
    return groups


def normalize_signs(values: list[int]) -> int | None:
    seen = {value for value in values if value in (-1, 1)}
    if not seen:
        return None
    if len(seen) == 1:
        return seen.pop()
    return 0


def summarize_groups(label: str, groups: dict[object, list[int]]) -> Counter:
    stats: Counter = Counter()
    size_hist: Counter = Counter()
    for values in groups.values():
        size_hist[len(values)] += 1
        sign = normalize_signs(values)
        if sign == 1:
            stats[f"{label}_plus_groups"] += 1
        elif sign == -1:
            stats[f"{label}_minus_groups"] += 1
        elif sign == 0:
            stats[f"{label}_mixed_groups"] += 1
            stats[f"{label}_mixed_rows"] += len(values)
        else:
            stats[f"{label}_missing_groups"] += 1
    stats[f"{label}_groups"] = len(groups)
    for size, count in size_hist.items():
        stats[f"{label}_size_{size}"] = count
    return stats


def collect_group_stats(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_rows: int,
) -> Counter:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    stats: Counter = Counter()
    seen_y: set[int] = set()

    d3_by_A: defaultdict[int, list[int]] = defaultdict(list)
    d4_by_A_after_d3: defaultdict[int, list[int]] = defaultdict(list)
    d3_by_A_xp: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    d4_by_A_xp_after_d3: defaultdict[tuple[int, int], list[int]] = defaultdict(list)

    for seed in seeds:
        for chunk in chunks:
            for tid in tids:
                rng = transfer.cuda_rng(seed, chunk, tid)
                for _ in range(draws_per_thread):
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
                    stats[f"D_{sign_label(d_class)}"] += 1
                    if d_class != 1:
                        continue
                    stats["Dplus_y"] += 1

                    candidates, _root_disc = candidate_roots(y)
                    if not candidates:
                        stats["Dplus_no_valid_candidate"] += 1
                        continue
                    for _root_index, A, xp in candidates:
                        stats["Dplus_candidates"] += 1
                        profile = selected_halving_profile(A, xp)
                        d1 = int(profile["d1"])
                        d2 = int(profile["d2"])
                        d3 = int(profile["d3"])
                        d4 = int(profile["d4"])
                        stats[f"d1_{sign_label(d1)}"] += 1
                        stats[f"d2_{sign_label(d2)}"] += 1
                        stats[f"d3_{sign_label(d3)}"] += 1
                        if d3 == 1:
                            stats[f"d4_after_d3_{sign_label(d4)}"] += 1
                        if d1 != 1 or d2 != 1:
                            stats["Dplus_prefix_failure"] += 1
                            continue
                        key_axp = (A % P, xp % P)
                        d3_by_A[A % P].append(d3)
                        d3_by_A_xp[key_axp].append(d3)
                        if d3 == 1:
                            d4_by_A_after_d3[A % P].append(d4)
                            d4_by_A_xp_after_d3[key_axp].append(d4)
                        stats["usable_Dplus_candidates"] += 1
                        if max_rows and stats["usable_Dplus_candidates"] >= max_rows:
                            stats.update(summarize_groups("d3_A", d3_by_A))
                            stats.update(summarize_groups("d4_A_after_d3", d4_by_A_after_d3))
                            stats.update(summarize_groups("d3_A_xp", d3_by_A_xp))
                            stats.update(summarize_groups("d4_A_xp_after_d3", d4_by_A_xp_after_d3))
                            return stats

    stats.update(summarize_groups("d3_A", d3_by_A))
    stats.update(summarize_groups("d4_A_after_d3", d4_by_A_after_d3))
    stats.update(summarize_groups("d3_A_xp", d3_by_A_xp))
    stats.update(summarize_groups("d4_A_xp_after_d3", d4_by_A_xp_after_d3))
    return stats


def print_counter(label: str, stats: Counter) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    d3_groups = stats["d3_A_groups"]
    d3_mixed = stats["d3_A_mixed_groups"]
    d4_groups = stats["d4_A_after_d3_groups"]
    d4_mixed = stats["d4_A_after_d3_mixed_groups"]
    print(
        "  d3_A_mixed_rate = "
        f"{(d3_mixed / d3_groups) if d3_groups else 0.0:.9f}"
    )
    print(
        "  d4_A_after_d3_mixed_rate = "
        f"{(d4_mixed / d4_groups) if d4_groups else 0.0:.9f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-rows", type=int, default=20000)
    args = parser.parse_args()

    print("p27 trace/norm Dplus A-descent bridge probe")
    print("question = do post-Dplus d3/d4 descend to whole A fibers?")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"max_rows = {args.max_rows}")

    chunks = transfer.parse_range(args.chunks)
    tids = transfer.parse_range(args.tids)
    for idx, seeds in enumerate(parse_seed_groups(args.seed_groups), start=1):
        stats = collect_group_stats(
            seeds=seeds,
            chunks=chunks,
            tids=tids,
            draws_per_thread=args.draws_per_thread,
            max_rows=args.max_rows,
        )
        print_counter(f"group{idx}_seeds_{','.join(str(seed) for seed in seeds)}", stats)

    print("p27_trace_norm_dplus_a_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
