#!/usr/bin/env python3
"""Trace/anti-trace audit for the p27 H/V half-norm coupling.

The involution audit found that pref=chi(y-2) and h*vq have the same boundary
under sigma(t)=-1/t.  This gate tests the next most structured possibility:
whether the descended T_line bit is the squareclass of a trace, anti-trace, or
norm of one of the named H/V sections under that involution.

No coefficients are fitted here.  Every tested section is named by the prior
component decomposition.
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


norm_gate = load_gate("p27_component_norm_gate.py")
transfer = norm_gate.transfer
P = transfer.P


def chi(value: int | None) -> int:
    return transfer.chi(value)


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def normalize(value: int, comps: dict[str, int], mode: str) -> int:
    if mode == "raw":
        return value
    if mode == "b":
        return value * comps["b_chi"]
    if mode == "a":
        return value * comps["a_chi"]
    if mode == "ab":
        return value * comps["a_chi"] * comps["b_chi"]
    if mode == "p26line":
        return value if comps["a_chi"] == 1 else value * comps["b_chi"]
    raise ValueError(mode)


def section_values(comps: dict[str, int]) -> dict[str, int]:
    t = comps["t"]
    b_factor = comps["B"] * comps["C"] % P
    pref_arg = (t - 1) % P
    h = comps["h_arg"]
    v = comps["v_arg"]
    hv = h * v % P
    return {
        "H": h,
        "V": v,
        "HV": hv,
        "pref_HV": pref_arg * hv % P,
        "BC_HV": b_factor * hv % P,
        "T_arg": pref_arg * b_factor % P * hv % P,
    }


def candidate_values(source: dict[str, int], image: dict[str, int]) -> dict[str, int]:
    source_sections = section_values(source)
    image_sections = section_values(image)
    out: dict[str, int] = {}
    for name, value in source_sections.items():
        sigma_value = image_sections[name]
        out[f"{name}:raw"] = chi(value)
        out[f"{name}:sigma"] = chi(sigma_value)
        out[f"{name}:trace"] = chi(value + sigma_value)
        out[f"{name}:anti_trace"] = chi(value - sigma_value)
        out[f"{name}:norm"] = chi(value * sigma_value)
    return out


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
        source = norm_gate.norm_component_values(y, w)
        image_point = transfer.transform_neg_inv_t(y, w)
        if source is None or image_point is None:
            stats["source_unusable"] += 1
            continue
        image = norm_gate.norm_component_values(*image_point)
        if image is None:
            stats["image_unusable"] += 1
            continue
        a = source["a"]
        b = source["b"]
        if image["a"] != a or image["b"] != b:
            stats["sigma_not_same_quotient"] += 1
            continue
        if (a, b) in seen_ab:
            stats["duplicate_ab"] += 1
            continue
        seen_ab.add((a, b))
        comps = {**source}
        comps.update(candidate_values(source, image))
        rows.append((a, b, comps))
        if max_rows and len(rows) >= max_rows:
            break
    stats["rows"] = len(rows)
    return rows, stats


def line_map(
    rows: list[tuple[int, int, dict[str, int]]],
    key: str,
    mode: str,
) -> tuple[dict[int, int], Counter[str]]:
    out: dict[int, int] = {}
    stats: Counter[str] = Counter()
    for a, _b, comps in rows:
        value = comps.get(key, 0)
        if value == 0:
            stats["zero"] += 1
            continue
        value = normalize(value, comps, mode)
        old = out.get(a)
        if old is None:
            out[a] = value
        elif old != value:
            stats["inconsistent"] += 1
        stats[f"value_{sign_name(value)}"] += 1
    stats["line_rows"] = len(out)
    stats["line_+1"] = sum(1 for value in out.values() if value == 1)
    stats["line_-1"] = sum(1 for value in out.values() if value == -1)
    return out, stats


def score(candidate: dict[int, int], target: dict[int, int]) -> tuple[int, int, int, int, float]:
    common = sorted(set(candidate) & set(target))
    if not common:
        return 0, 0, 0, 0, 0.0
    signs = [candidate[a] for a in common]
    targets = [target[a] for a in common]
    exact_plus = int(all(sign == tgt for sign, tgt in zip(signs, targets)))
    exact_minus = int(all(-sign == tgt for sign, tgt in zip(signs, targets)))
    target_plus = sum(1 for tgt in targets if tgt == 1)
    baseline = target_plus / len(targets) if targets else 0.0
    best_good = best_total = 0
    best_lift = 0.0
    for orient in (1, -1):
        selected = [tgt for sign, tgt in zip(signs, targets) if orient * sign == 1]
        if not selected or baseline == 0.0:
            continue
        good = sum(1 for tgt in selected if tgt == 1)
        lift = (good / len(selected)) / baseline
        if lift > best_lift:
            best_lift = lift
            best_good = good
            best_total = len(selected)
    return exact_plus, exact_minus, best_good, best_total, best_lift


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-rows", type=int, default=0)
    parser.add_argument("--top", type=int, default=24)
    args = parser.parse_args()

    rows, stats = collect_rows(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )
    target, target_stats = line_map(rows, "T_line", "raw")

    print("p27_hv_trace_coupling_gate")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "rows",
        "source_unusable",
        "image_unusable",
        "sigma_not_same_quotient",
        "duplicate_ab",
    ):
        print(f"  {key}={stats[key]}")

    section_names = ("H", "V", "HV", "pref_HV", "BC_HV", "T_arg")
    operations = ("raw", "sigma", "trace", "anti_trace", "norm")
    modes = ("raw", "b", "a", "ab", "p26line")
    scored: list[tuple[float, int, int, int, int, str, str, int, int, int]] = []
    for section in section_names:
        for operation in operations:
            key = f"{section}:{operation}"
            for mode in modes:
                candidate, s = line_map(rows, key, mode)
                exact_plus, exact_minus, good, total, lift = score(candidate, target)
                scored.append(
                    (
                        lift,
                        good,
                        total,
                        exact_plus,
                        exact_minus,
                        key,
                        mode,
                        s["inconsistent"],
                        s["zero"],
                        s["line_rows"],
                    )
                )
    scored.sort(reverse=True, key=lambda row: (row[3] or row[4], row[0], row[1], -row[2]))

    print("scores_against_T_line:")
    for rank, (lift, good, total, exact_plus, exact_minus, key, mode, inconsistent, zero, line_rows) in enumerate(scored[: args.top], 1):
        print(
            "  "
            f"rank={rank} candidate={key} mode={mode} line_rows={line_rows} "
            f"inconsistent={inconsistent} zero={zero} "
            f"exact_plus={exact_plus} exact_minus={exact_minus} "
            f"best_lift={lift:.9f} good={good} total={total}"
        )

    print(f"target_line_rows={target_stats['line_rows']}")
    print("p27_hv_trace_coupling_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
