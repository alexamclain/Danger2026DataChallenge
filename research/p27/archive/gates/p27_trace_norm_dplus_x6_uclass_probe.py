#!/usr/bin/env python3
"""Post-Dplus x6/U-class geometry probe.

After Dplus, the A-coordinate is already a function of t=y-1.  This probe
looks one layer deeper at the second selected-halving sheet:

    x6 = second half after the root candidate xp
    U6 = x6 + 1/x6
    d3 = chi(x6^2 + A*x6 + 1)

The point is to see whether d3 lives on the full root sheet or on a smaller
reciprocal-reduced object, and whether any factor is already forced.
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


def sign_set_label(values: list[int]) -> str:
    seen = tuple(sorted({value for value in values if value in (-1, 1)}))
    if not seen:
        return "missing"
    return ",".join(sign_name(value) for value in seen)


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
                    candidates, _root_disc = candidate_roots(y)
                    if not candidates:
                        stats["Dplus_no_valid_candidate"] += 1
                        continue

                    y_d3: list[int] = []
                    y_chix6: list[int] = []
                    y_chi_uplus: list[int] = []
                    y_U_values: defaultdict[int, list[int]] = defaultdict(list)
                    y_x6_values: set[int] = set()
                    y_x5_values: set[int] = set()

                    for root_index, cand_A, xp in candidates:
                        stats["Dplus_candidates"] += 1
                        if cand_A % P != A:
                            stats["candidate_A_formula_mismatch"] += 1
                        d1, x5s = label2.halve_all(cand_A, xp)
                        stats[f"d1_{sign_name(d1)}"] += 1
                        if d1 != 1:
                            stats["d1_failure"] += 1
                            continue
                        for x5 in x5s:
                            y_x5_values.add(x5 % P)
                            d2, x6s = label2.halve_all(cand_A, x5)
                            stats[f"d2_{sign_name(d2)}"] += 1
                            if d2 != 1:
                                stats["d2_failure"] += 1
                                continue
                            for x6 in x6s:
                                x6 %= P
                                y_x6_values.add(x6)
                                U = (x6 + transfer.inv(x6)) % P
                                y_U_values[U].append(x6)
                                d3, _x7s = label2.halve_all(cand_A, x6)
                                chi_x6 = transfer.chi(x6)
                                chi_uplus = transfer.chi(U + cand_A)
                                chi_udisc = transfer.chi((U * U - 4) % P)
                                stats[f"d3_branch_{sign_name(d3)}"] += 1
                                stats[f"chi_x6_{sign_name(chi_x6)}"] += 1
                                stats[f"chi_UplusA_{sign_name(chi_uplus)}"] += 1
                                stats[f"chi_Udisc_{sign_name(chi_udisc)}"] += 1
                                if d3 != chi_x6 * chi_uplus:
                                    stats["d3_factor_mismatch"] += 1
                                y_d3.append(d3)
                                y_chix6.append(chi_x6)
                                y_chi_uplus.append(chi_uplus)

                    if not y_d3:
                        stats["Dplus_no_x6_branches"] += 1
                        continue

                    stats["analyzed_y"] += 1
                    stats[f"y_x5_count_{len(y_x5_values)}"] += 1
                    stats[f"y_x6_count_{len(y_x6_values)}"] += 1
                    stats[f"y_U_count_{len(y_U_values)}"] += 1
                    stats[f"y_d3_signs_{sign_set_label(y_d3)}"] += 1
                    stats[f"y_chix6_signs_{sign_set_label(y_chix6)}"] += 1
                    stats[f"y_chi_UplusA_signs_{sign_set_label(y_chi_uplus)}"] += 1
                    if len({value for value in y_d3 if value in (-1, 1)}) == 1:
                        stats["y_d3_constant"] += 1
                        stats[f"y_d3_constant_{sign_name(y_d3[0])}"] += 1
                    else:
                        stats["y_d3_mixed"] += 1
                    if len({value for value in y_chix6 if value in (-1, 1)}) == 1:
                        stats["y_chix6_constant"] += 1
                    else:
                        stats["y_chix6_mixed"] += 1
                    if set(y_chi_uplus) == {1}:
                        stats["y_UplusA_all_square"] += 1
                    else:
                        stats["y_UplusA_not_all_square"] += 1

                    for U, xs in y_U_values.items():
                        stats[f"U_fiber_size_{len(xs)}"] += 1
                        if len(xs) == 2 and xs[0] * xs[1] % P != 1:
                            stats["U_reciprocal_pair_mismatch"] += 1
                        u_d3: list[int] = []
                        u_chix6: list[int] = []
                        u_chi_uplus: list[int] = []
                        for x6 in xs:
                            d3, _x7s = label2.halve_all(A, x6)
                            u_d3.append(d3)
                            u_chix6.append(transfer.chi(x6))
                            u_chi_uplus.append(transfer.chi(U + A))
                        stats[f"U_d3_signs_{sign_set_label(u_d3)}"] += 1
                        stats[f"U_chix6_signs_{sign_set_label(u_chix6)}"] += 1
                        stats[f"U_chi_UplusA_signs_{sign_set_label(u_chi_uplus)}"] += 1

                    if max_y and stats["analyzed_y"] >= max_y:
                        return stats

    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    analyzed = stats["analyzed_y"]
    if analyzed:
        print(f"  y_d3_constant_rate = {stats['y_d3_constant'] / analyzed:.9f}")
        print(f"  y_UplusA_all_square_rate = {stats['y_UplusA_all_square'] / analyzed:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-y", type=int, default=0)
    args = parser.parse_args()

    print("p27 trace/norm Dplus x6/U-class probe")
    print("question = after Dplus, does d3 reduce on the x6 reciprocal sheet?")
    print(f"p = {P}")
    print("definitions:")
    print("  t = y - 1")
    print("  A = (t - 1/t)^4/4 - 2")
    print("  U = x6 + 1/x6")
    print("  d3 = chi(x6^2 + A*x6 + 1) = chi(x6)*chi(U + A)")
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
    print("  UplusA_forced_square iff y_UplusA_not_all_square and chi_UplusA_-1 are zero")
    print("  then d3 reduces to chi(x6) on the Dplus second-halving sheet")
    print("  this is a CAS class target, not yet a source-space shrink")
    print("p27_trace_norm_dplus_x6_uclass_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
