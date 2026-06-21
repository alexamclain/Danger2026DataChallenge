#!/usr/bin/env python3
"""Component descent audit for the p27 T_line bit.

The transfer gate treats T_line as a black-box normalization of

    D = -x_pref * vq * h
    T = D * chi(y)
    T_line = T                  if chi(a)=+1
             T * chi(b)         if chi(a)=-1.

This gate splits those factors and asks which pieces descend to the a-line,
which pieces carry the b-flip cocycle, and whether any normalized component is
already the remaining T_line selector.
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


transfer = load_gate("p27_trace_norm_transfer_gate.py")
P = transfer.P

Row = tuple[int, int, dict[str, int]]


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def component_values(y: int, w: int) -> dict[str, int] | None:
    y %= P
    w %= P
    f = transfer.f_value(y)
    if transfer.chi(f) != 1:
        return None
    z = transfer.sqrt_mod(f)
    if z is None:
        return None

    y2 = y * y % P
    ym1 = (y - 1) % P
    ym2 = (y - 2) % P
    b_quad = (y2 - 2 * y + 2) % P
    c_quad = (y2 - 2) % P
    ch = 4 * c_quad % P * b_quad % P
    av = 8 * y % P * pow(ym1, 2, P) % P

    nh_scale = 8 * ym1 % P
    nh_scale_chi = transfer.chi(nh_scale)
    nv_scale_chi = transfer.chi(y * c_quad)
    chi_c = transfer.chi(c_quad)
    chi_2b = transfer.chi(2 * b_quad)
    x_pref = transfer.chi((-y * ym2) % P)
    y_chi = transfer.chi(y)
    if 0 in (nh_scale_chi, nv_scale_chi, chi_c, chi_2b, x_pref, y_chi):
        return None

    sqrt_nh = nh_scale * z % P
    if nh_scale_chi < 0:
        sqrt_nh = (-sqrt_nh) % P
    h = transfer.chi(2 * (ch + sqrt_nh))

    sqrt_nv_num = 4 * y % P * z % P * w % P
    if nv_scale_chi < 0:
        sqrt_nv_num = (-sqrt_nv_num) % P
    v_arg_num = (c_quad * av + sqrt_nv_num) % P
    vq = chi_2b * transfer.chi(2 * v_arg_num) * chi_c
    if h == 0 or vq == 0:
        return None

    coords = transfer.quotient_coordinates(y, w)
    if coords is None:
        return None
    a, b = coords
    a_chi = transfer.chi(a)
    b_chi = transfer.chi(b)
    if a_chi == 0 or b_chi == 0:
        return None

    d = -x_pref * vq * h
    t = d * y_chi
    line_norm = 1 if a_chi == 1 else b_chi
    t_line = t * line_norm
    pref = -x_pref * y_chi

    return {
        "a": a,
        "b": b,
        "a_chi": a_chi,
        "b_chi": b_chi,
        "x_pref": x_pref,
        "y": y_chi,
        "pref": pref,
        "h": h,
        "vq": vq,
        "h_vq": h * vq,
        "pref_h": pref * h,
        "pref_vq": pref * vq,
        "D": d,
        "T": t,
        "line_norm": line_norm,
        "T_line": t_line,
    }


def collect_rows(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_rows: int,
) -> tuple[list[Row], Counter[str]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)
    rows: list[Row] = []
    for y, w in points:
        comps = component_values(y, w)
        if comps is None:
            stats["component_unusable"] += 1
            continue
        a = comps["a"]
        b = comps["b"]
        if (b * b - (16 - pow(a, 4, P))) % P != 0:
            stats["quotient_relation_fail"] += 1
            continue
        rows.append((a, b, comps))
        if max_rows and len(rows) >= max_rows:
            break
    stats["component_rows"] = len(rows)
    return rows, stats


COMPONENTS = (
    "x_pref",
    "y",
    "pref",
    "h",
    "vq",
    "h_vq",
    "pref_h",
    "pref_vq",
    "D",
    "T",
    "line_norm",
    "T_line",
)

MODES = ("raw", "b", "a", "ab", "p26line")


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


def line_map(rows: list[Row], component: str, mode: str) -> tuple[dict[int, int], Counter[str]]:
    by_a: dict[int, int] = {}
    stats: Counter[str] = Counter()
    for a, _b, comps in rows:
        value = normalize(comps[component], comps, mode)
        stats[f"value_{sign_name(value)}"] += 1
        old = by_a.get(a)
        if old is None:
            by_a[a] = value
        elif old != value:
            stats["inconsistent"] += 1
    stats["line_rows"] = len(by_a)
    stats["rows"] = len(rows)
    stats["line_+1"] = sum(1 for value in by_a.values() if value == 1)
    stats["line_-1"] = sum(1 for value in by_a.values() if value == -1)
    return by_a, stats


def score_against_target(candidate: dict[int, int], target: dict[int, int]) -> tuple[int, int, int, int, float]:
    common = sorted(set(candidate) & set(target))
    rows = len(common)
    if rows == 0:
        return 0, 0, 0, 0, 0.0
    signs = [candidate[a] for a in common]
    targets = [target[a] for a in common]
    exact_plus = int(all(sign == tgt for sign, tgt in zip(signs, targets)))
    exact_minus = int(all(-sign == tgt for sign, tgt in zip(signs, targets)))
    target_plus = sum(1 for tgt in targets if tgt == 1)
    baseline = target_plus / rows if rows else 0.0
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


def audit_b_flip(rows: list[Row]) -> dict[str, Counter[str]]:
    by_a: dict[int, list[tuple[int, dict[str, int]]]] = defaultdict(list)
    for a, b, comps in rows:
        by_a[a].append((b, comps))
    out = {component: Counter() for component in COMPONENTS}
    for a, pairs in by_a.items():
        by_b = {b: comps for b, comps in pairs}
        for b, comps in list(by_b.items()):
            b2 = (-b) % P
            if b2 not in by_b or b > b2:
                continue
            comps2 = by_b[b2]
            for component in COMPONENTS:
                ratio = comps2[component] * comps[component]
                stats = out[component]
                stats["pairs"] += 1
                stats[f"ratio_{sign_name(ratio)}"] += 1
                if ratio == 1:
                    stats["invariant"] += 1
                if ratio == -1:
                    stats["anti_invariant"] += 1
                if ratio == comps["a_chi"]:
                    stats["matches_chi_a"] += 1
                if ratio == -comps["a_chi"]:
                    stats["anti_chi_a"] += 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-rows", type=int, default=0)
    parser.add_argument("--top", type=int, default=16)
    args = parser.parse_args()

    rows, stats = collect_rows(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )
    target_line, target_stats = line_map(rows, "T_line", "raw")
    bflip = audit_b_flip(rows)

    print("p27_tline_component_descent_gate")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "component_rows",
        "component_unusable",
        "quotient_relation_fail",
    ):
        print(f"  {key}={stats[key]}")

    print("b_flip_ratios:")
    for component in COMPONENTS:
        s = bflip[component]
        print(
            "  "
            f"component={component} pairs={s['pairs']} invariant={s['invariant']} "
            f"anti_invariant={s['anti_invariant']} matches_chi_a={s['matches_chi_a']} "
            f"anti_chi_a={s['anti_chi_a']} ratio_+1={s['ratio_+1']} ratio_-1={s['ratio_-1']}"
        )

    print("line_descent:")
    scored: list[tuple[float, int, int, int, int, str, str, int, int]] = []
    for component in COMPONENTS:
        for mode in MODES:
            candidate, s = line_map(rows, component, mode)
            exact_plus, exact_minus, good, total, lift = score_against_target(candidate, target_line)
            scored.append(
                (
                    lift,
                    good,
                    total,
                    exact_plus,
                    exact_minus,
                    component,
                    mode,
                    s["inconsistent"],
                    s["line_rows"],
                )
            )
            if s["inconsistent"] == 0:
                print(
                    "  "
                    f"component={component} mode={mode} line_rows={s['line_rows']} "
                    f"line_+1={s['line_+1']} line_-1={s['line_-1']} "
                    f"exact_plus={exact_plus} exact_minus={exact_minus} "
                    f"best_lift={lift:.9f} good={good} total={total}"
                )

    scored.sort(reverse=True, key=lambda row: (row[3] or row[4], row[0], row[1], -row[2]))
    print("top_against_T_line:")
    for rank, (lift, good, total, exact_plus, exact_minus, component, mode, inconsistent, line_rows) in enumerate(scored[: args.top], 1):
        print(
            "  "
            f"rank={rank} component={component} mode={mode} inconsistent={inconsistent} "
            f"line_rows={line_rows} exact_plus={exact_plus} exact_minus={exact_minus} "
            f"best_lift={lift:.9f} good={good} total={total}"
        )
    print(f"target_line_rows={target_stats['line_rows']}")
    print("p27_tline_component_descent_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

