#!/usr/bin/env python3
"""P27 u+2 sequence recurrence screen.

Starting from the compactD=-1 / d2 stratum, walk the selected nonsplit
halving path using the u+2 x-square gate.  This asks whether the successive
characters chi(u_j+2) show a prefix-conditioned recurrence that could beat the
random 1/2 loss per gate.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_halving_usquare_gate_probe import halve_u_records
from p27_label2_alpha_branch_recurrence_probe import P, sample_rows


def selected_step(a: int, x: int) -> tuple[int, int | None, Counter]:
    stats: Counter = Counter()
    d_chi, records = halve_u_records(a, x)
    if d_chi != 1:
        stats["d_not_square"] += 1
        return d_chi, None, stats

    good = [rec for rec in records if int(rec["w_chi"]) == 1]
    if len(good) != 1:
        stats[f"good_w_records_{len(good)}"] += 1
    if not good:
        return 0, None, stats

    rec = good[0]
    xs = rec["xs"]
    assert isinstance(xs, list)
    if len(xs) != 2:
        stats[f"x_count_{len(xs)}"] += 1
    bit = int(rec["u_plus_2_chi"])
    if bit != int(rec["u_minus_2_chi"]):
        stats["uplus_uminus_mismatch"] += 1
    if bit == 1 and xs:
        return bit, int(xs[0]), stats
    return bit, None, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=6000000)
    parser.add_argument("--max-gates", type=int, default=12)
    args = parser.parse_args()

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    gate_counts: list[Counter] = [Counter() for _ in range(args.max_gates + 1)]
    prefix_hist: Counter = Counter()
    anomaly_stats: Counter = Counter()

    # Use one T-deck representative per pair.  The paired-root probe already
    # verifies that the obvious T/branch choices agree on d3/d4.
    for row in rows:
        cand = row["root0"]
        assert isinstance(cand, dict)
        a = int(cand["A"])
        x = int(cand["x5"])
        prefix_len = 0
        for gate in range(3, args.max_gates + 1):
            bit, nx, stats = selected_step(a, x)
            anomaly_stats.update(stats)
            gate_counts[gate]["samples"] += 1
            gate_counts[gate][f"bit_{bit}"] += 1
            if bit == 1 and nx is not None:
                prefix_len += 1
                gate_counts[gate]["continue"] += 1
                x = nx
                continue
            break
        prefix_hist[prefix_len] += 1

    print("p27 u+2 sequence recurrence probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"max_gates = {args.max_gates}")
    print(f"sampled_pairs = {len(rows)}")
    for key in sorted(sample_stats):
        print(f"sample_stat {key} = {sample_stats[key]}")
    print("gate_prefix_rates:")
    for gate in range(3, args.max_gates + 1):
        row = gate_counts[gate]
        samples = row["samples"]
        if not samples:
            continue
        plus = row["bit_1"]
        minus = row["bit_-1"]
        zero = row["bit_0"]
        cont = row["continue"]
        print(
            f"  gate={gate} samples={samples} plus={plus} minus={minus} "
            f"zero={zero} continue={cont} plus_rate={plus / samples:.9f}"
        )
    print("prefix_success_length_hist:")
    for length in sorted(prefix_hist):
        print(
            f"  plus_prefix_len={length} count={prefix_hist[length]} "
            f"rate={prefix_hist[length] / len(rows) if rows else 0.0:.9f}"
        )
    print("anomaly_stats:")
    if anomaly_stats:
        for key in sorted(anomaly_stats):
            print(f"  {key} = {anomaly_stats[key]}")
    else:
        print("  none")
    print("p27_usquare_sequence_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
