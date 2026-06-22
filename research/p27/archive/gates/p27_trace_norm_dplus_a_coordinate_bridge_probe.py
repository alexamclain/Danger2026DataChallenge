#!/usr/bin/env python3
"""Dplus H90/quotient coordinate bridge to the A-line.

The current queue asks whether Dplus H90 coordinates map cheaply to the A-line
surface carrying post-Dplus d3/d4.  This probe checks the explicit bridge on
actual p27 Dplus rows:

    t = y - 1
    a = t - 1/t
    A = (t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1)/(4*t^4)
      = a^4/4 - 2

It also verifies the useful squareclass identities:

    A + 2 = ((t^2 - 1)^2/(2*t^2))^2
    A - 2 = -(((t^2 + 1)*w)/(2*t^2))^2,  w^2=-(t^2+2t-1)(t^2-2t-1).

This is a bridge test, not a production search.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_trace_norm_post_dplus_probe import (
    P,
    candidate_roots,
    selected_halving_profile,
    sign_name,
    trace_norm_d_class_parts,
    transfer,
)


def parse_seed_groups(raw: str) -> list[list[int]]:
    groups: list[list[int]] = []
    for part in raw.split(";"):
        part = part.strip()
        if part:
            groups.append(transfer.parse_range(part))
    return groups


def normalize_signs(values: list[int]) -> int | None:
    seen = {value for value in values if value in (-1, 1)}
    if not seen:
        return None
    if len(seen) == 1:
        return seen.pop()
    return 0


def summarize_groups(label: str, groups: dict[int, list[int]]) -> Counter[str]:
    stats: Counter[str] = Counter()
    for values in groups.values():
        stats[f"{label}_size_{len(values)}"] += 1
        sign = normalize_signs(values)
        if sign == 1:
            stats[f"{label}_plus"] += 1
        elif sign == -1:
            stats[f"{label}_minus"] += 1
        elif sign == 0:
            stats[f"{label}_mixed"] += 1
            stats[f"{label}_mixed_rows"] += len(values)
        else:
            stats[f"{label}_missing"] += 1
    stats[f"{label}_groups"] = len(groups)
    return stats


def a_from_t(t: int) -> int:
    t %= P
    t2 = t * t % P
    t4 = t2 * t2 % P
    t6 = t4 * t2 % P
    t8 = t4 * t4 % P
    num = (t8 - 4 * t6 - 2 * t4 - 4 * t2 + 1) % P
    den = 4 * t4 % P
    return num * transfer.inv(den) % P


def a_from_conic_a(conic_a: int) -> int:
    return (pow(conic_a % P, 4, P) * transfer.inv(4) - 2) % P


def bline_from_t(t: int) -> int:
    t %= P
    t2 = t * t % P
    return (t2 - 1) % P * (t2 - 1) % P * transfer.inv(2 * t2) % P


def aminus2_from_h90(t: int, w: int) -> int:
    t %= P
    w %= P
    t2 = t * t % P
    num = (t2 + 1) % P * w % P
    den = 2 * t2 % P
    square = num * transfer.inv(den) % P
    return (-square * square) % P


def collect_group(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_rows: int,
) -> Counter[str]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    stats: Counter[str] = Counter()
    seen_y: set[int] = set()
    d3_by_A: defaultdict[int, list[int]] = defaultdict(list)
    d4_by_A_after_d3: defaultdict[int, list[int]] = defaultdict(list)

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
                    k = transfer.k_value(y)
                    w = transfer.sqrt_mod(k)
                    if w is None:
                        stats["missing_w"] += 1
                        continue
                    z = transfer.sqrt_mod(transfer.f_value(y))
                    if z is None:
                        stats["missing_z"] += 1
                        continue

                    conic_a = (t - transfer.inv(t)) % P
                    conic_g = w * transfer.inv(t) % P
                    if (conic_a * conic_a + conic_g * conic_g - 4) % P != 0:
                        stats["conic_relation_mismatch"] += 1

                    A_t = a_from_t(t)
                    if a_from_conic_a(conic_a) != A_t:
                        stats["A_from_conic_a_mismatch"] += 1
                    Bline = bline_from_t(t)
                    if (Bline * Bline - 2 - A_t) % P != 0:
                        stats["A_Bline_mismatch"] += 1
                    if (Bline * Bline - (A_t + 2)) % P != 0:
                        stats["Aplus2_Bline_square_mismatch"] += 1
                    if aminus2_from_h90(t, w) != (A_t - 2) % P:
                        stats["Aminus2_h90_square_mismatch"] += 1

                    candidates, _root_disc = candidate_roots(y)
                    if not candidates:
                        stats["Dplus_no_valid_candidate"] += 1
                        continue
                    y_A_values: set[int] = set()
                    for _root_index, A, xp in candidates:
                        stats["Dplus_candidates"] += 1
                        y_A_values.add(A % P)
                        if A % P != A_t:
                            stats["candidate_A_formula_mismatch"] += 1
                        profile = selected_halving_profile(A, xp)
                        d1 = int(profile["d1"])
                        d2 = int(profile["d2"])
                        d3 = int(profile["d3"])
                        d4 = int(profile["d4"])
                        stats[f"d1_{sign_name(d1)}"] += 1
                        stats[f"d2_{sign_name(d2)}"] += 1
                        stats[f"d3_{sign_name(d3)}"] += 1
                        if d3 == 1:
                            stats[f"d4_after_d3_{sign_name(d4)}"] += 1
                        if d1 != 1 or d2 != 1:
                            stats["Dplus_prefix_failure"] += 1
                            continue
                        d3_by_A[A % P].append(d3)
                        if d3 == 1:
                            d4_by_A_after_d3[A % P].append(d4)
                        stats["usable_Dplus_candidates"] += 1
                    if len(y_A_values) > 1:
                        stats["same_y_multiple_A"] += 1
                    else:
                        stats["same_y_single_A"] += 1
                    if max_rows and stats["usable_Dplus_candidates"] >= max_rows:
                        stats.update(summarize_groups("d3_A", d3_by_A))
                        stats.update(summarize_groups("d4_A_after_d3", d4_by_A_after_d3))
                        return stats

    stats.update(summarize_groups("d3_A", d3_by_A))
    stats.update(summarize_groups("d4_A_after_d3", d4_by_A_after_d3))
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    d3_groups = stats["d3_A_groups"]
    d4_groups = stats["d4_A_after_d3_groups"]
    print(
        "  d3_A_mixed_rate = "
        f"{(stats['d3_A_mixed'] / d3_groups) if d3_groups else 0.0:.9f}"
    )
    print(
        "  d4_A_after_d3_mixed_rate = "
        f"{(stats['d4_A_after_d3_mixed'] / d4_groups) if d4_groups else 0.0:.9f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-rows", type=int, default=20000)
    args = parser.parse_args()

    print("p27 trace/norm Dplus A-coordinate bridge probe")
    print("question = is A a cheap H90/quotient coordinate before root materialization?")
    print(f"p = {P}")
    print("formulas:")
    print("  t = y - 1")
    print("  a = t - 1/t")
    print("  g = w/t")
    print("  a^2 + g^2 = 4")
    print("  A = (t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1)/(4*t^4)")
    print("  A = a^4/4 - 2")
    print("  A + 2 = ((t^2 - 1)^2/(2*t^2))^2")
    print("  A - 2 = -(((t^2 + 1)*w)/(2*t^2))^2")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"max_rows = {args.max_rows}")

    chunks = transfer.parse_range(args.chunks)
    tids = transfer.parse_range(args.tids)
    for index, seeds in enumerate(parse_seed_groups(args.seed_groups), start=1):
        stats = collect_group(
            seeds=seeds,
            chunks=chunks,
            tids=tids,
            draws_per_thread=args.draws_per_thread,
            max_rows=args.max_rows,
        )
        print_counter(f"group{index}_seeds_{','.join(str(seed) for seed in seeds)}", stats)

    print("verdict:")
    print("  coordinate_bridge = exact in tested rows iff all mismatch counters are zero")
    print("  bridge_meaning = A is a rational function of t, equivalently of conic a")
    print("  remaining_math = compare A-level d3/d4 Kummer classes with Dplus H90 payload classes")
    print("p27_trace_norm_dplus_a_coordinate_bridge_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
