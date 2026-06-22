#!/usr/bin/env python3
"""Visible branch-atom screen for the descended Dplus U6 row bit.

The symbolic resultant for the reciprocal tower has special branch factors

    t, t-1, t+1, t^2+1, t^2+2t-1, t^2-2t-1.

This probe asks the narrow follow-up question: is the descended row bit
chi(U6+2)=chi(x6) just a product of these visible t-branch characters or the
nearest A/X branch atoms?
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import combinations

from p27_trace_norm_dplus_a_coordinate_bridge_probe import a_from_t
from p27_trace_norm_dplus_h90_x6_coboundary_probe import dplus_x6_target
from p27_trace_norm_dplus_reciprocal_tower_probe import P, parse_seed_groups, x_parent_from_t
from p27_trace_norm_post_dplus_probe import sign_name, trace_norm_d_class_parts, transfer


@dataclass(frozen=True)
class ComboScore:
    combo: tuple[str, ...]
    polarity: int
    train_matches: int
    train_total: int
    heldout_matches: int
    heldout_total: int
    combined_matches: int
    combined_total: int


def chi(value: int) -> int:
    return transfer.chi(value % P)


def branch_features(t: int) -> dict[str, int]:
    A = a_from_t(t)
    X = x_parent_from_t(t)
    t2 = t * t % P
    B = (t2 + 1) % P
    C = (t2 + 2 * t - 1) % P
    R = (t2 - 2 * t - 1) % P
    features = {
        "t": t,
        "t_minus_1": t - 1,
        "t_plus_1": t + 1,
        "y=t_plus_1": t + 1,
        "t2_minus_1": t2 - 1,
        "B=t2_plus_1": B,
        "C=t2_plus_2t_minus_1": C,
        "R=t2_minus_2t_minus_1": R,
        "B*C": B * C,
        "B*R": B * R,
        "C*R": C * R,
        "B*C*R": B * C % P * R,
        "A": A,
        "A_minus_2": A - 2,
        "A_plus_2": A + 2,
        "X": X,
        "X_minus_2": X - 2,
        "X_plus_2": X + 2,
    }
    return {name: chi(value) for name, value in features.items()}


def collect_group(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_y: int,
) -> tuple[list[dict[str, int]], Counter[str]]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    seen_y: set[int] = set()
    rows: list[dict[str, int]] = []
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
                    target = dplus_x6_target(y, stats)
                    if target not in (-1, 1):
                        continue
                    t = (y - 1) % P
                    row = {"target": target, "y": y}
                    row.update(branch_features(t))
                    rows.append(row)
                    stats["analyzed_y"] += 1
                    if max_y and stats["analyzed_y"] >= max_y:
                        return rows, stats

    return rows, stats


def feature_profile(rows: list[dict[str, int]]) -> tuple[list[str], Counter[str]]:
    stats: Counter[str] = Counter()
    names = sorted(key for key in rows[0] if key not in ("target", "y")) if rows else []
    active = []
    for name in names:
        counts = Counter(row[name] for row in rows)
        for value, count in counts.items():
            stats[f"{name}_{sign_name(value)}"] = count
        if counts.get(0, 0):
            stats["features_with_zero"] += 1
            continue
        if len(counts) <= 1:
            stats["constant_features"] += 1
            continue
        active.append(name)
    stats["active_features"] = len(active)
    return active, stats


def combo_value(row: dict[str, int], combo: tuple[str, ...], polarity: int) -> int:
    value = polarity
    for name in combo:
        value *= row[name]
    return value


def score_combo(train: list[dict[str, int]], heldout: list[dict[str, int]], combo: tuple[str, ...], polarity: int) -> ComboScore:
    train_matches = sum(1 for row in train if combo_value(row, combo, polarity) == row["target"])
    heldout_matches = sum(1 for row in heldout if combo_value(row, combo, polarity) == row["target"])
    return ComboScore(
        combo=combo,
        polarity=polarity,
        train_matches=train_matches,
        train_total=len(train),
        heldout_matches=heldout_matches,
        heldout_total=len(heldout),
        combined_matches=train_matches + heldout_matches,
        combined_total=len(train) + len(heldout),
    )


def combo_name(score: ComboScore) -> str:
    prefix = "" if score.polarity == 1 else "-"
    return prefix + "*".join(score.combo)


def iter_combos(features: list[str], max_weight: int):
    for weight in range(1, min(max_weight, len(features)) + 1):
        yield from combinations(features, weight)


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(label: str, scores: list[ComboScore], keep: int) -> None:
    print(f"{label}:")
    if not scores:
        print("  none")
        return
    for score in scores[:keep]:
        print(
            "  "
            f"combo={combo_name(score)} "
            f"train={score.train_matches}/{score.train_total} "
            f"heldout={score.heldout_matches}/{score.heldout_total} "
            f"combined={score.combined_matches}/{score.combined_total}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-y", type=int, default=0)
    parser.add_argument("--max-weight", type=int, default=5)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 trace/norm Dplus U6 row-bit branch-atom probe")
    print("question = is the descended U6 row bit a visible t-branch character product?")
    print(f"p = {P}")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"max_y = {args.max_y}")
    print(f"max_weight = {args.max_weight}")

    chunks = transfer.parse_range(args.chunks)
    tids = transfer.parse_range(args.tids)
    groups = parse_seed_groups(args.seed_groups)
    if len(groups) != 2:
        raise ValueError("expected exactly two seed groups for train/heldout")

    train, train_stats = collect_group(groups[0], chunks, tids, args.draws_per_thread, args.max_y)
    heldout, heldout_stats = collect_group(groups[1], chunks, tids, args.draws_per_thread, args.max_y)
    print_counter(f"train_seeds_{','.join(str(seed) for seed in groups[0])}", train_stats)
    print_counter(f"heldout_seeds_{','.join(str(seed) for seed in groups[1])}", heldout_stats)

    features, profile = feature_profile(train + heldout)
    print_counter("feature_profile", profile)
    print("active_features:")
    for feature in features:
        print(f"  {feature}")

    exact: list[ComboScore] = []
    scores: list[ComboScore] = []
    for combo in iter_combos(features, args.max_weight):
        for polarity in (1, -1):
            score = score_combo(train, heldout, combo, polarity)
            scores.append(score)
            if score.combined_matches == score.combined_total:
                exact.append(score)

    scores.sort(
        key=lambda score: (
            score.heldout_matches / score.heldout_total if score.heldout_total else 0,
            score.train_matches / score.train_total if score.train_total else 0,
            score.combined_matches,
        ),
        reverse=True,
    )
    print_scores("exact_branch_atom_combos", exact, args.top)
    print_scores("best_branch_atom_combos", scores, args.top)
    print("verdict:")
    print("  promote only an exact or strong heldout branch-atom product")
    print("  otherwise the descended row bit remains a CAS/Prym class")
    print("p27_trace_norm_dplus_u6_rowbit_branch_atom_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
