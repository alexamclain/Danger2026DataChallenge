#!/usr/bin/env python3
"""Quotient automorphism orbit audit for p27 line bits.

The trace/norm quotient is

    C: b^2 = 16 - a^4
    a = t - 1/t,  b = w(t^2 + 1)/t^2.

The EK automorphisms t -> -1/t, t -> 1/t, and t -> -t induce quotient
automorphisms.  The first preserves (a,b) and gave the Hilbert-90 boundary.
The latter two send a -> -a.  This gate asks whether domain_line or T_line has
an exact orbit law under a -> -a that could halve or structure the selected
stratum.
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from itertools import combinations
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


norm_gate = load_gate("p27_component_norm_gate.py")
transfer = norm_gate.transfer
P = transfer.P


COMPONENTS = (
    "domain_line",
    "pref",
    "h",
    "vq",
    "h_vq",
    "D",
    "T",
    "T_line",
    "line_norm",
)

BASE_SIGNS = (
    "a_chi",
    "b_chi",
    "chi_t",
    "chi_B",
    "chi_C",
    "chi_R",
    "chi_a_plus_2",
    "chi_a_minus_2",
    "chi_a2_minus_4",
    "chi_a2_plus_4",
    "chi_y_minus_2",
    "chi_one_minus_t2",
    "h_norm",
    "v_norm",
    "h_inner",
    "v_inner",
    "domain_line",
    "line_norm",
)


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def w_flip(y: int, w: int) -> tuple[int, int]:
    return y % P, (-w) % P


TRANSFORMS = (
    ("w_flip", w_flip),
    ("neg_inv_t", transfer.transform_neg_inv_t),
    ("inv_t", transfer.transform_inv_t),
    ("neg_t", transfer.transform_neg_t),
)


def candidate_signs(comps: dict[str, int], max_degree: int) -> dict[str, int]:
    atoms = {name: comps[name] for name in BASE_SIGNS if comps.get(name, 0)}
    out: dict[str, int] = {"1": 1, "-1": -1}
    for name, value in atoms.items():
        out[name] = value
        out[f"-{name}"] = -value
    names = sorted(atoms)
    for degree in range(2, max_degree + 1):
        for combo in combinations(names, degree):
            value = 1
            for name in combo:
                value *= atoms[name]
            label = "*".join(combo)
            out[label] = value
            out[f"-{label}"] = -value
    return out


def quotient_relation(source: dict[str, int], image: dict[str, int]) -> str:
    same_a = image["a"] == source["a"]
    neg_a = image["a"] == (-source["a"]) % P
    same_b = image["b"] == source["b"]
    neg_b = image["b"] == (-source["b"]) % P
    a_part = "a" if same_a else "-a" if neg_a else "other_a"
    b_part = "b" if same_b else "-b" if neg_b else "other_b"
    return f"{a_part},{b_part}"


def collect_rows(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_rows: int,
) -> tuple[list[tuple[int, int, dict[str, int]]], Counter[str]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)
    rows: list[tuple[int, int, dict[str, int]]] = []
    seen_ab: set[tuple[int, int]] = set()
    for y, w in points:
        comps = norm_gate.norm_component_values(y, w)
        if comps is None:
            stats["component_unusable"] += 1
            continue
        a = comps["a"]
        b = comps["b"]
        if (a, b) in seen_ab:
            stats["duplicate_ab"] += 1
            continue
        seen_ab.add((a, b))
        rows.append((y, w, comps))
        if max_rows and len(rows) >= max_rows:
            break
    stats["rows"] = len(rows)
    return rows, stats


def audit_transforms(
    rows: list[tuple[int, int, dict[str, int]]],
    max_match_degree: int,
) -> dict[str, dict[str, Counter[str]]]:
    out: dict[str, dict[str, Counter[str]]] = {}
    for name, transform in TRANSFORMS:
        comp_stats = {component: Counter() for component in COMPONENTS}
        relation_stats: Counter[str] = Counter()
        for y, w, source in rows:
            image_point = transform(y, w)
            if image_point is None:
                relation_stats["undefined"] += 1
                continue
            image = norm_gate.norm_component_values(*image_point)
            if image is None:
                relation_stats["image_unusable"] += 1
                continue
            relation = quotient_relation(source, image)
            relation_stats[relation] += 1
            candidates = candidate_signs(source, max_match_degree)
            for component in COMPONENTS:
                ratio = image[component] * source[component]
                stats = comp_stats[component]
                stats["rows"] += 1
                stats[f"ratio_{sign_name(ratio)}"] += 1
                for label, value in candidates.items():
                    if ratio == value:
                        stats[f"match::{label}"] += 1
        out[name] = {"relations": relation_stats, **comp_stats}
    return out


def line_pair_stats(rows: list[tuple[int, int, dict[str, int]]], key: str) -> Counter[str]:
    by_a: dict[int, int] = {}
    stats: Counter[str] = Counter()
    for _y, _w, comps in rows:
        a = comps["a"]
        value = comps[key]
        old = by_a.get(a)
        if old is None:
            by_a[a] = value
        elif old != value:
            stats["line_inconsistent"] += 1
    seen: set[int] = set()
    for a, value in by_a.items():
        if a in seen:
            continue
        b = (-a) % P
        seen.add(a)
        seen.add(b)
        other = by_a.get(b)
        if other is None:
            stats["missing_neg_a"] += 1
            continue
        stats["pairs"] += 1
        stats[f"pair_{sign_name(value)}{sign_name(other)}"] += 1
        ratio = value * other
        stats[f"ratio_{sign_name(ratio)}"] += 1
    stats["line_rows"] = len(by_a)
    return stats


def exact_labels(stats: Counter[str], rows: int, top: int) -> list[str]:
    labels = []
    for key, value in stats.items():
        if key.startswith("match::") and value == rows:
            labels.append(key.split("::", 1)[1])
    if labels:
        return sorted(labels)[:top]
    top_rows = [
        (value, key.split("::", 1)[1])
        for key, value in stats.items()
        if key.startswith("match::")
    ]
    top_rows.sort(reverse=True)
    return [f"{label}:{value}" for value, label in top_rows[:top]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-rows", type=int, default=0)
    parser.add_argument("--max-match-degree", type=int, default=2)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    rows, stats = collect_rows(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )
    audits = audit_transforms(rows, args.max_match_degree)

    print("p27_quotient_automorphism_orbit_gate")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "rows",
        "component_unusable",
        "duplicate_ab",
    ):
        print(f"  {key}={stats[key]}")

    print("line_neg_a_pairs:")
    for key in ("domain_line", "T_line"):
        pair_stats = line_pair_stats(rows, key)
        print(
            "  "
            f"key={key} line_rows={pair_stats['line_rows']} pairs={pair_stats['pairs']} "
            f"missing_neg_a={pair_stats['missing_neg_a']} "
            f"pair_+1+1={pair_stats['pair_+1+1']} pair_+1-1={pair_stats['pair_+1-1']} "
            f"pair_-1+1={pair_stats['pair_-1+1']} pair_-1-1={pair_stats['pair_-1-1']} "
            f"ratio_+1={pair_stats['ratio_+1']} ratio_-1={pair_stats['ratio_-1']}"
        )

    print("transform_ratios:")
    for name in (transform_name for transform_name, _transform in TRANSFORMS):
        relation_stats = audits[name]["relations"]
        print(
            "  "
            f"transform={name} relations="
            f"{','.join(f'{key}:{value}' for key, value in sorted(relation_stats.items()))}"
        )
        for component in COMPONENTS:
            component_stats = audits[name][component]
            rows_n = component_stats["rows"]
            labels = exact_labels(component_stats, rows_n, args.top)
            print(
                "  "
                f"transform={name} component={component} rows={rows_n} "
                f"ratio_+1={component_stats['ratio_+1']} "
                f"ratio_-1={component_stats['ratio_-1']} "
                f"exact_or_top={','.join(labels) or 'none'}"
            )

    print("p27_quotient_automorphism_orbit_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
