#!/usr/bin/env python3
"""Orientation phase table for the p27 trace/norm Dplus lane.

The post-Dplus product screen killed low-weight character products.  This
probe records the simpler transition table: after the production C-style
Dplus predicate, do the exact cover orientation signs

    eps_h = chi(t),          t = y - 1
    eps_v = chi((t + 1)C),   C = t^2 + 2t - 1

or the named half-norm phases H/VQ/T_line bias the next selected gates enough
to matter with a raw-y denominator?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from types import SimpleNamespace

from p27_trace_norm_dplus_cover_probe import dplus_core
from p27_trace_norm_post_dplus_probe import P, collect_rows, transfer


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def state_label(row: dict[str, int], keys: tuple[str, ...]) -> str:
    return ",".join(f"{key}={sign_name(row.get(key, 0))}" for key in keys)


def collect_orientation_rows(args: argparse.Namespace) -> tuple[list[dict[str, int]], Counter[str]]:
    rows, stats = collect_rows(args)
    out: list[dict[str, int]] = []
    cover_stats: Counter[str] = Counter()
    for row in rows:
        y = int(row["y"])
        k = transfer.k_value(y)
        w = transfer.sqrt_mod(k)
        if w is None:
            cover_stats["w_missing"] += 1
            continue
        core_pack = dplus_core(y, w)
        if core_pack is None:
            cover_stats["core_missing"] += 1
            continue
        core, parts = core_pack
        d_cover = -transfer.chi(core)
        if d_cover != 1:
            cover_stats[f"cover_D_{sign_name(d_cover)}"] += 1
        enriched = dict(row)
        enriched.update(
            {
                "eps_h": int(parts["eps_h"]),
                "eps_v": int(parts["eps_v"]),
                "hcore_chi": transfer.chi(parts["hcore"]),
                "vcore_chi": transfer.chi(parts["vcore"]),
                "core_chi": transfer.chi(core),
                "cover_D": d_cover,
            }
        )
        out.append(enriched)
    stats.update({f"cover_{key}": value for key, value in cover_stats.items()})
    return out, stats


def summarize_state(rows: list[dict[str, int]], keys: tuple[str, ...], target: str) -> Counter:
    stats: Counter = Counter()
    by_state: defaultdict[str, Counter] = defaultdict(Counter)
    for row in rows:
        target_value = int(row.get(target, 0))
        if target_value not in (-1, 1):
            continue
        label = state_label(row, keys)
        by_state[label]["total"] += 1
        by_state[label][f"target_{sign_name(target_value)}"] += 1

    total = sum(counter["total"] for counter in by_state.values())
    plus = sum(counter["target_+1"] for counter in by_state.values())
    stats["states"] = len(by_state)
    stats["rows"] = total
    stats["target_plus"] = plus
    stats["target_minus"] = total - plus
    stats["target_plus_rate_x1000000"] = plus * 1_000_000 // total if total else 0
    for label, counter in sorted(by_state.items()):
        state_total = counter["total"]
        state_plus = counter["target_+1"]
        state_minus = counter["target_-1"]
        stats[f"state_{label}_total"] = state_total
        stats[f"state_{label}_plus"] = state_plus
        stats[f"state_{label}_minus"] = state_minus
        stats[f"state_{label}_plus_rate_x1000000"] = (
            state_plus * 1_000_000 // state_total if state_total else 0
        )
        stats[f"state_{label}_source_share_x1000000"] = (
            state_total * 1_000_000 // total if total else 0
        )
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_table(label: str, rows: list[dict[str, int]], keys: tuple[str, ...], target: str) -> None:
    stats = summarize_state(rows, keys, target)
    print_counter(f"{label}_{target}_{'_'.join(keys)}", stats)
    print(f"{label}_{target}_{'_'.join(keys)}_table:")
    print("  state total plus minus plus_rate source_share")
    state_prefix = "state_"
    state_suffix = "_total"
    for key in sorted(k for k in stats if k.startswith(state_prefix) and k.endswith(state_suffix)):
        state = key[len(state_prefix) : -len(state_suffix)]
        total = stats[key]
        plus = stats[f"state_{state}_plus"]
        minus = stats[f"state_{state}_minus"]
        plus_rate = stats[f"state_{state}_plus_rate_x1000000"] / 1_000_000
        share = stats[f"state_{state}_source_share_x1000000"] / 1_000_000
        print(f"  {state} {total} {plus} {minus} {plus_rate:.9f} {share:.9f}")


def run_one(label: str, args: argparse.Namespace) -> None:
    rows, stats = collect_orientation_rows(args)
    print_counter(f"{label}_sample", stats)
    print(f"{label}_usable_rows = {len(rows)}")
    for target in ("d3", "d4"):
        for keys in (
            ("eps_h", "eps_v"),
            ("H", "VQ"),
            ("eps_h", "eps_v", "T_line"),
            ("hcore_chi", "vcore_chi"),
        ):
            print_table(label, rows, keys, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-rows", type=int, default=20000)
    args = parser.parse_args()

    print("p27 trace/norm orientation phase probe")
    print("question = do Dplus orientation signs bias post-Dplus selected gates?")
    print(f"p = {P}")
    print(f"seed_groups = {args.seed_groups}")
    for index, seeds in enumerate(args.seed_groups.split(";"), start=1):
        subargs = SimpleNamespace(
            seeds=seeds,
            chunks=args.chunks,
            tids=args.tids,
            draws_per_thread=args.draws_per_thread,
            max_rows=args.max_rows,
        )
        run_one(f"group{index}_seeds_{seeds.replace(',', '_')}", subargs)
    print("p27_trace_norm_orientation_phase_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
