#!/usr/bin/env python3
"""P27 u+2 norm/coboundary screen.

For one halving step, with d=x^2+A*x+1 and s^2=d:

    u_+ + 2 = 2(x+s+1)
    u_- + 2 = 2(x-s+1)

so the norm through s is governed by x*(2-A).  This probe checks the exact
norm identities on p27 compactD rows and asks whether the selected w-square
branch's u+2 bit is visible in the small norm/branch character span.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_halving_usquare_gate_probe import halve_u_records
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows


FEATURES = [
    "x",
    "x-1",
    "x+1",
    "A-2",
    "A+2",
    "2-A",
    "-A-2",
    "x*(2-A)",
    "-x*(A+2)",
    "A2-4",
]


def bit_pm1(v: int) -> int:
    if v == 1:
        return 0
    if v == -1:
        return 1
    raise ValueError(v)


def popcount(n: int) -> int:
    return bin(n).count("1")


def combo_name(mask: int) -> str:
    names = [FEATURES[i] for i in range(len(FEATURES)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def feature_values(a: int, x: int) -> dict[str, int]:
    return {
        "x": x,
        "x-1": x - 1,
        "x+1": x + 1,
        "A-2": a - 2,
        "A+2": a + 2,
        "2-A": 2 - a,
        "-A-2": -a - 2,
        "x*(2-A)": x * (2 - a),
        "-x*(A+2)": -x * (a + 2),
        "A2-4": a * a - 4,
    }


def find_exact_combo(rows: list[tuple[int, int]]) -> int | None:
    if not rows:
        return None
    for combo in range(1 << len(FEATURES)):
        if all((popcount(mask & combo) & 1) == target for mask, target in rows):
            return combo
    return None


def best_combos(rows: list[tuple[int, int]], limit: int = 8) -> list[tuple[int, int, int]]:
    scored = []
    for combo in range(1 << len(FEATURES)):
        good = 0
        for mask, target in rows:
            good += (popcount(mask & combo) & 1) == target
        scored.append((good, popcount(combo), combo))
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return scored[:limit]


def collect_step_row(a: int, x: int) -> tuple[tuple[int, int] | None, Counter]:
    stats: Counter = Counter()
    d_chi, records = halve_u_records(a, x)
    if d_chi != 1:
        stats["d_not_square"] += 1
        return None, stats

    if len(records) != 2:
        stats[f"record_count_{len(records)}"] += 1
        return None, stats

    up = [int(rec["u_plus_2_chi"]) for rec in records]
    um = [int(rec["u_minus_2_chi"]) for rec in records]
    wc = [int(rec["w_chi"]) for rec in records]
    if any(v == 0 for v in up + um + wc):
        stats["zero_class"] += 1
        return None, stats

    x_chi = legendre(x)
    expected_up_norm = x_chi * legendre(2 - a)
    expected_um_norm = x_chi * legendre(-a - 2)
    expected_w_norm = legendre(a * a - 4)

    if up[0] * up[1] != expected_up_norm:
        stats["up_norm_mismatch"] += 1
    if um[0] * um[1] != expected_um_norm:
        stats["um_norm_mismatch"] += 1
    if wc[0] * wc[1] != expected_w_norm:
        stats["w_norm_mismatch"] += 1

    good = [i for i, c in enumerate(wc) if c == 1]
    if len(good) != 1:
        stats[f"good_w_count_{len(good)}"] += 1
        return None, stats
    gi = good[0]
    if up[gi] != um[gi]:
        stats["selected_up_um_mismatch"] += 1

    vals = feature_values(a, x)
    mask = 0
    for i, name in enumerate(FEATURES):
        c = legendre(vals[name])
        if c == 0:
            stats["zero_feature"] += 1
            return None, stats
        mask |= bit_pm1(c) << i
    target = bit_pm1(up[gi])
    return (mask, target), stats


def summarize_rows(name: str, rows: list[tuple[int, int]]) -> None:
    exact = find_exact_combo(rows)
    print(f"{name}:")
    print(f"  rows = {len(rows)}")
    print(f"  exact_combo = {combo_name(exact) if exact is not None else 'none'}")
    print("  best_combos:")
    for good, weight, combo in best_combos(rows):
        rate = good / len(rows) if rows else 0.0
        print(f"    good={good}/{len(rows)} rate={rate:.9f} weight={weight} combo={combo_name(combo)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=6000000)
    args = parser.parse_args()

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    d3_rows: list[tuple[int, int]] = []
    d4_rows: list[tuple[int, int]] = []
    stats: Counter = Counter()

    for row in rows:
        cand = row["root0"]
        assert isinstance(cand, dict)
        a = int(cand["A"])
        x5 = int(cand["x5"])
        packed, step_stats = collect_step_row(a, x5)
        stats.update(f"d3_{key}" for key in step_stats.elements())
        if packed is not None:
            d3_rows.append(packed)

        _, x6s = halve_all(a, x5)
        if not x6s:
            continue
        # The branch-recurrence probe shows the two branches agree on d3, so
        # one representative is enough for the norm-span screen.
        x6 = int(x6s[0])
        if legendre(x6 * x6 + a * x6 + 1) != 1:
            continue
        packed, step_stats = collect_step_row(a, x6)
        stats.update(f"d4_{key}" for key in step_stats.elements())
        if packed is not None:
            d4_rows.append(packed)

    print("p27 u+2 norm/coboundary probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"sampled_pairs = {len(rows)}")
    print("features = " + ", ".join(FEATURES))
    for key in sorted(sample_stats):
        print(f"sample_stat {key} = {sample_stats[key]}")
    print("norm_identity_stats:")
    if stats:
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
    else:
        print("  none")
    summarize_rows("d2_to_d3_selected_uplus_span", d3_rows)
    summarize_rows("d3_to_d4_selected_uplus_span", d4_rows)
    print("p27_usquare_norm_coboundary_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
