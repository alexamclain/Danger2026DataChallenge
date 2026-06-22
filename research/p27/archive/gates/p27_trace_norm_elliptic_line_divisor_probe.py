#!/usr/bin/env python3
"""Small elliptic line-divisor screen for p27 trace/norm line bits.

The trace/norm quotient lands on the supersingular j=1728 curve

    E: v^2 = u^3 - u.

The existing evaluator tests rational functions in the quotient-line
coordinate a/u and the coset gate tests small torsion projections.  This
bounded probe tests the first visible elliptic divisor family itself:

    vertical lines u-c
    affine lines v + m*u + c

with small integer m,c.  These are L(3O)-type line divisors on the Weierstrass
model.  The goal is to find a named exact squareclass, or kill the first
visible elliptic-line explanation before asking for non-visible theta/H90
machinery.
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from pathlib import Path
import sys


def load_gate(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


transfer = load_gate("p27_trace_norm_transfer_gate.py")
P = transfer.P

Record = tuple[int, int, int]


def inv(value: int) -> int:
    return pow(value % P, P - 2, P)


def small_range(bound: int) -> list[int]:
    return list(range(-bound, bound + 1))


def elliptic_uv(a: int, b: int) -> tuple[int, int] | None:
    a %= P
    b %= P
    if a == 0:
        return None
    a2 = a * a % P
    u = 4 * inv(a2) % P
    v = 2 * b % P * inv(a2 * a % P) % P
    if (v * v - (u * u % P * u - u)) % P:
        raise RuntimeError("bad C -> E map")
    return u, v


def collect_records(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
) -> tuple[list[Record], list[Record], Counter[str]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)

    domain_records: list[Record] = []
    domain_seen: set[Record] = set()
    for y, w in points:
        coords = transfer.quotient_coordinates(y, w)
        if coords is None:
            stats["domain_quotient_undefined"] += 1
            continue
        a, b = coords
        if (b * b - (16 - pow(a, 4, P))) % P:
            stats["domain_quotient_relation_fail"] += 1
            continue
        uv = elliptic_uv(a, b)
        if uv is None:
            stats["domain_a_zero_skipped"] += 1
            continue
        target = transfer.chi(transfer.f_value(y))
        if target == 0:
            stats["domain_target_zero"] += 1
            continue
        row = (*uv, target)
        if row not in domain_seen:
            domain_seen.add(row)
            domain_records.append(row)

    quotient_rows, quotient_stats = transfer.collect_quotient_rows(points)
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    target_records: list[Record] = []
    target_seen: set[Record] = set()
    for a, b, target in quotient_rows:
        uv = elliptic_uv(a, b)
        if uv is None:
            stats["target_a_zero_skipped"] += 1
            continue
        line_target = transfer.normalized_line_target(a, b, target, "p26_Tline")
        if line_target is None or line_target == 0:
            stats["target_line_unusable"] += 1
            continue
        row = (*uv, line_target)
        if row not in target_seen:
            target_seen.add(row)
            target_records.append(row)

    stats["domain_records"] = len(domain_records)
    stats["target_records"] = len(target_records)
    return domain_records, target_records, stats


def vertical_value(c: int, u: int, _v: int) -> int:
    return (u - c) % P


def line_value(m: int, c: int, u: int, v: int) -> int:
    return (v + m * u + c) % P


def score_values(rows: list[Record], values: list[int], raw_draws: int) -> Counter[str]:
    stats: Counter[str] = Counter()
    signs: list[int] = []
    targets: list[int] = []
    for value, (_u, _v, target) in zip(values, rows):
        sign = transfer.chi(value)
        if sign == 0:
            stats["zero_eval"] += 1
        signs.append(sign)
        targets.append(target)

    rows_n = len(rows)
    stats["rows"] = rows_n
    stats["target_plus"] = sum(1 for target in targets if target == 1)
    stats["target_minus"] = sum(1 for target in targets if target == -1)
    if rows_n:
        stats["baseline_plus_rate_x1000000"] = stats["target_plus"] * 1_000_000 // rows_n
    stats["exact_plus"] = int(rows_n > 0 and stats["zero_eval"] == 0 and all(s == t for s, t in zip(signs, targets)))
    stats["exact_minus"] = int(rows_n > 0 and stats["zero_eval"] == 0 and all(-s == t for s, t in zip(signs, targets)))

    best_lift_num = -1
    for orientation in (1, -1):
        selected = [target for sign, target in zip(signs, targets) if sign and orientation * sign == 1]
        if not selected:
            continue
        selected_plus = sum(1 for target in selected if target == 1)
        selected_rate = selected_plus / len(selected)
        baseline = stats["target_plus"] / rows_n if rows_n else 0.0
        lift = selected_rate / baseline if baseline else 0.0
        lift_num = int(lift * 1_000_000_000)
        if lift_num > best_lift_num:
            best_lift_num = lift_num
            stats["best_orientation"] = orientation
            stats["best_selected"] = len(selected)
            stats["best_selected_plus"] = selected_plus
            stats["best_lift_x1000"] = int(lift * 1000)
            if raw_draws:
                stats["best_selected_per_source_x1000000000"] = len(selected) * 1_000_000_000 // raw_draws
                stats["best_target_per_source_x1000000000"] = selected_plus * 1_000_000_000 // raw_draws
    return stats


def score_candidate(rows: list[Record], kind: str, m: int, c: int, raw_draws: int) -> Counter[str]:
    if kind == "vertical":
        values = [vertical_value(c, u, v) for u, v, _target in rows]
    elif kind == "line":
        values = [line_value(m, c, u, v) for u, v, _target in rows]
    else:
        raise ValueError(kind)
    return score_values(rows, values, raw_draws)


def screen_scope(label: str, rows: list[Record], raw_draws: int, bound: int, top: int) -> None:
    scored: list[tuple[int, int, str, Counter[str]]] = []
    for c in small_range(bound):
        name = f"vertical_u_{c:+d}"
        stats = score_candidate(rows, "vertical", 0, c, raw_draws)
        scored.append((stats["best_lift_x1000"], stats["best_selected_plus"], name, stats))
    for m in small_range(bound):
        for c in small_range(bound):
            name = f"line_v_{m:+d}u_{c:+d}"
            stats = score_candidate(rows, "line", m, c, raw_draws)
            scored.append((stats["best_lift_x1000"], stats["best_selected_plus"], name, stats))

    exact = [(name, stats) for _lift, _good, name, stats in scored if stats["exact_plus"] or stats["exact_minus"]]
    print(f"{label}_elliptic_line_screen:")
    print(f"  rows = {len(rows)}")
    print(f"  raw_draws = {raw_draws}")
    print(f"  candidate_count = {len(scored)}")
    print(f"  exact_count = {len(exact)}")
    for name, stats in exact[:top]:
        print(
            "  exact "
            f"name={name} exact_plus={stats['exact_plus']} exact_minus={stats['exact_minus']} "
            f"zero={stats['zero_eval']}"
        )
    print("  top_by_lift:")
    for lift, _good, name, stats in sorted(scored, reverse=True)[:top]:
        print(
            "    "
            f"name={name} lift={lift / 1000:.3f} orientation={stats['best_orientation']} "
            f"selected={stats['best_selected']} selected_plus={stats['best_selected_plus']} "
            f"zero={stats['zero_eval']} "
            f"selected_per_source={stats['best_selected_per_source_x1000000000'] / 1_000_000_000:.9f} "
            f"target_per_source={stats['best_target_per_source_x1000000000'] / 1_000_000_000:.9f}"
        )


def print_counter(prefix: str, stats: Counter[str]) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def parse_groups(raw: str) -> list[tuple[str, list[int]]]:
    groups: list[tuple[str, list[int]]] = []
    for part in raw.split(";"):
        if not part.strip():
            continue
        label, seeds = part.split(":", 1)
        groups.append((label.strip(), transfer.parse_range(seeds.strip())))
    return groups


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="train:121,122;heldout:123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--bound", type=int, default=4)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 trace/norm elliptic line-divisor probe")
    print("curve = E: v^2 = u^3 - u")
    print("candidates = vertical u-c and affine lines v + m*u + c")
    print(f"coefficient_bound = {args.bound}")
    for label, seeds in parse_groups(args.seed_groups):
        domain_records, target_records, stats = collect_records(
            seeds=seeds,
            chunks=transfer.parse_range(args.chunks),
            tids=transfer.parse_range(args.tids),
            draws_per_thread=args.draws_per_thread,
        )
        print_counter(f"{label}_sample_stats", stats)
        raw_draws = stats["raw_draws"]
        screen_scope(f"{label}_domain", domain_records, raw_draws, args.bound, args.top)
        screen_scope(f"{label}_target", target_records, raw_draws, args.bound, args.top)
    print("p27_trace_norm_elliptic_line_divisor_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
