#!/usr/bin/env python3
"""Large-factor elliptic quotient collision audit for p27.

The small torsion audit killed m=2,3,4,6,12.  This gate tests larger divisors
of the observed exponent on E: v^2=x^3-x, especially the p27 factor 345451.

The important statistic is collision purity.  A majority score over projection
classes is misleading when most classes are singletons; if a bit is determined
by an m-quotient class, then every repeated class must have a single target
sign.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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


ec = load_gate("p27_trace_norm_elliptic_coset_gate.py")
transfer = ec.transfer
P = ec.P
EXPONENT = ec.GROUP_EXPONENT_CANDIDATE


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def chi(value: int | None) -> int:
    return transfer.chi(value)


def signed_point_key(point: ec.Affine) -> tuple[str, int, int]:
    if point is None:
        return ("O", 0, 0)
    x, y = point
    return ("P", x, y)


def class_collision_stats(records: list[ec.Record], modulus: int, key_mode: str) -> Counter[str]:
    cofactor = EXPONENT // modulus
    by_class: dict[tuple[str, int, int], Counter[int]] = defaultdict(Counter)
    stats: Counter[str] = Counter()
    for point, target in records:
        projected = ec.affine_from_jac(ec.jac_mul(point, cofactor))
        key = ec.canonical_point_key(projected) if key_mode == "unsigned" else signed_point_key(projected)
        by_class[key][target] += 1
        stats["rows"] += 1
        stats[f"target_{sign_name(target)}"] += 1

    for counts in by_class.values():
        plus = counts[1]
        minus = counts[-1]
        total = plus + minus
        stats["classes"] += 1
        if total == 1:
            stats["singleton_classes"] += 1
            continue
        stats["non_singleton_classes"] += 1
        stats["non_singleton_rows"] += total
        pair_count = total * (total - 1) // 2
        disagree_pairs = plus * minus
        stats["collision_pairs"] += pair_count
        stats["disagree_pairs"] += disagree_pairs
        if plus and minus:
            stats["mixed_classes"] += 1
            stats["mixed_rows"] += total
        else:
            stats["pure_collision_classes"] += 1
    return stats


def score_signs(signs: list[int], targets: list[int]) -> Counter[str]:
    stats: Counter[str] = Counter()
    usable = [(sign, target) for sign, target in zip(signs, targets) if sign]
    stats["rows"] = len(targets)
    stats["usable"] = len(usable)
    stats["zero"] = len(targets) - len(usable)
    if not usable:
        return stats
    stats["target_+1"] = sum(1 for _sign, target in usable if target == 1)
    stats["target_-1"] = sum(1 for _sign, target in usable if target == -1)
    stats["exact_plus"] = int(all(sign == target for sign, target in usable))
    stats["exact_minus"] = int(all(-sign == target for sign, target in usable))
    baseline = stats["target_+1"] / stats["usable"] if stats["usable"] else 0.0
    for orient, label in ((1, "plus"), (-1, "minus")):
        selected = [target for sign, target in usable if orient * sign == 1]
        if not selected or baseline == 0.0:
            continue
        good = sum(1 for target in selected if target == 1)
        lift = (good / len(selected)) / baseline
        if lift > stats["best_lift_num"] / max(stats["best_lift_den"], 1):
            stats["best_good"] = good
            stats["best_total"] = len(selected)
            # Store as scaled integer for Counter; format with helper.
            stats["best_lift_scaled"] = round(lift * 1_000_000_000)
            stats["best_lift_num"] = round(lift * 1_000_000_000)
            stats["best_lift_den"] = 1_000_000_000
            stats["best_orient_" + label] = 1
    return stats


def projected_character_scores(records: list[ec.Record], modulus: int) -> list[tuple[float, str, Counter[str]]]:
    cofactor = EXPONENT // modulus
    names = (
        "x",
        "y",
        "x_minus_1",
        "x_plus_1",
        "x2_minus_1",
        "x2_plus_1",
        "x2",
        "x3_minus_x",
    )
    signs: dict[str, list[int]] = {name: [] for name in names}
    targets: list[int] = []
    for point, target in records:
        projected = ec.affine_from_jac(ec.jac_mul(point, cofactor))
        targets.append(target)
        if projected is None:
            for name in names:
                signs[name].append(0)
            continue
        x, y = projected
        x2 = x * x % P
        values = {
            "x": x,
            "y": y,
            "x_minus_1": x - 1,
            "x_plus_1": x + 1,
            "x2_minus_1": x2 - 1,
            "x2_plus_1": x2 + 1,
            "x2": x2,
            "x3_minus_x": x2 * x - x,
        }
        for name in names:
            signs[name].append(chi(values[name]))

    scored: list[tuple[float, str, Counter[str]]] = []
    for name in names:
        stats = score_signs(signs[name], targets)
        lift = stats["best_lift_scaled"] / 1_000_000_000 if stats["best_lift_scaled"] else 0.0
        scored.append((lift, name, stats))
    scored.sort(reverse=True, key=lambda row: (row[2]["exact_plus"] or row[2]["exact_minus"], row[0], row[2]["best_good"]))
    return scored


def print_collision(label: str, records: list[ec.Record], moduli: list[int], key_modes: list[str]) -> None:
    print(f"{label}_large_factor_collisions:")
    for modulus in moduli:
        if EXPONENT % modulus != 0:
            print(f"  m={modulus} skipped=not_divisor")
            continue
        for key_mode in key_modes:
            stats = class_collision_stats(records, modulus, key_mode)
            collision_pairs = stats["collision_pairs"]
            disagree_rate = stats["disagree_pairs"] / collision_pairs if collision_pairs else 0.0
            mixed_rate = stats["mixed_classes"] / stats["non_singleton_classes"] if stats["non_singleton_classes"] else 0.0
            print(
                "  "
                f"m={modulus} key={key_mode} rows={stats['rows']} classes={stats['classes']} "
                f"singleton_classes={stats['singleton_classes']} "
                f"non_singleton_classes={stats['non_singleton_classes']} "
                f"mixed_classes={stats['mixed_classes']} mixed_rate={mixed_rate:.9f} "
                f"collision_pairs={collision_pairs} disagree_pairs={stats['disagree_pairs']} "
                f"disagree_rate={disagree_rate:.9f}"
            )


def print_projected_chars(label: str, records: list[ec.Record], moduli: list[int], top: int) -> None:
    print(f"{label}_projected_character_scores:")
    for modulus in moduli:
        if EXPONENT % modulus != 0:
            continue
        for lift, name, stats in projected_character_scores(records, modulus)[:top]:
            print(
                "  "
                f"m={modulus} char={name} usable={stats['usable']} zero={stats['zero']} "
                f"exact_plus={stats['exact_plus']} exact_minus={stats['exact_minus']} "
                f"best_lift={lift:.9f} good={stats['best_good']} total={stats['best_total']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-records", type=int, default=0)
    parser.add_argument("--moduli", default="345451,690902,1036353,1381804,4145412")
    parser.add_argument("--key-modes", default="unsigned,signed")
    parser.add_argument("--top", type=int, default=4)
    args = parser.parse_args()

    moduli = [int(x) for x in args.moduli.split(",") if x]
    key_modes = [x for x in args.key_modes.split(",") if x]
    domain_records, target_records, stats = ec.collect_records(
        seeds=ec.parse_range(args.seeds),
        chunks=ec.parse_range(args.chunks),
        tids=ec.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_records=args.max_records,
    )

    print("p27_elliptic_large_factor_collision_gate")
    print(f"p={P}")
    print(f"exponent=(p+1)/2={EXPONENT}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "domain_records",
        "target_records",
        "domain_inconsistent",
        "target_line_inconsistent",
    ):
        print(f"  {key}={stats[key]}")
    print_collision("domain", domain_records, moduli, key_modes)
    print_collision("target_line", target_records, moduli, key_modes)
    print_projected_chars("domain", domain_records, moduli, args.top)
    print_projected_chars("target_line", target_records, moduli, args.top)
    print("p27_elliptic_large_factor_collision_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
