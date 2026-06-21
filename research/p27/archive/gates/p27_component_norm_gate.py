#!/usr/bin/env python3
"""Named norm/half-norm audit for the p27 T_line components.

This gate follows the p27 component descent pass one layer further.  It does
not fit high-degree functions.  It only tests squareclasses that come from the
visible branch divisors, the domain half-norm, and the two norm expressions
inside the h and vq components.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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


transfer = load_gate("p27_trace_norm_transfer_gate.py")
tline_gate = load_gate("p27_tline_component_descent_gate.py")
P = transfer.P


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def inv(value: int) -> int:
    return pow(value % P, P - 2, P)


def chi(value: int | None) -> int:
    return transfer.chi(value)


def norm_component_values(y: int, w: int) -> dict[str, int] | None:
    comps = tline_gate.component_values(y, w)
    if comps is None:
        return None

    y %= P
    w %= P
    t = (y - 1) % P
    if t == 0:
        return None
    z = transfer.sqrt_mod(transfer.f_value(y))
    if z is None:
        return None

    y2 = y * y % P
    b_quad = (y2 - 2 * y + 2) % P       # B = t^2 + 1
    c_quad = (y2 - 2) % P               # C = t^2 + 2t - 1
    r_quad = (y2 - 4 * y + 2) % P       # R = t^2 - 2t - 1

    a = comps["a"]
    b = comps["b"]
    a_chi = comps["a_chi"]
    b_chi = comps["b_chi"]

    # h = chi(2 * (4CB +/- 8tz)), with sign chosen as in the component gate.
    h_A = 4 * c_quad % P * b_quad % P
    h_U = 8 * t % P * z % P
    if chi(8 * t) < 0:
        h_U = (-h_U) % P
    h_arg = (h_A + h_U) % P
    h_recomputed = chi(2 * h_arg)

    h_norm_value = (h_A * h_A - pow(8 * t % P, 2, P) * transfer.f_value(y)) % P
    h_inner_value = (c_quad * b_quad - 4 * pow(t, 3, P)) % P

    # vq = chi(2B) * chi(2 * (C*8yt^2 +/- 4yzw)) * chi(C).
    # The same sign rule makes the square-root term carry the observed
    # b-flip cocycle.
    v_A = c_quad * (8 * y % P) % P * pow(t, 2, P) % P
    q = z * w % P
    v_U = 4 * y % P * q % P
    if chi(y * c_quad) < 0:
        v_U = (-v_U) % P
    v_arg = (v_A + v_U) % P
    vq_recomputed = chi(2 * b_quad) * chi(2 * v_arg) * chi(c_quad)

    v_norm_value = (v_A * v_A - pow(4 * y % P, 2, P) * transfer.f_value(y) % P * transfer.k_value(y)) % P
    # Remove the obvious square y^2 and C^2 where possible; this is the
    # branch-divisor part of the same norm expression.
    v_inner_value = (4 * pow(t, 3, P) + b_quad * r_quad) % P

    domain_line = chi(transfer.f_value(y))
    t_chi = chi(t)
    out = {
        **comps,
        "t": t,
        "z": z,
        "q": q,
        "B": b_quad,
        "C": c_quad,
        "R": r_quad,
        "domain_line": domain_line,
        "chi_t": t_chi,
        "chi_B": chi(b_quad),
        "chi_C": chi(c_quad),
        "chi_R": chi(r_quad),
        "chi_a_plus_2": chi(a + 2),
        "chi_a_minus_2": chi(a - 2),
        "chi_a2_minus_4": chi(a * a - 4),
        "chi_a2_plus_4": chi(a * a + 4),
        "chi_y_minus_2": chi(y - 2),
        "chi_one_minus_t2": chi(1 - t * t),
        "chi_q": chi(q),
        "h_A": h_A,
        "h_U": h_U,
        "h_arg": h_arg,
        "h_norm": chi(h_norm_value),
        "h_inner": chi(h_inner_value),
        "v_A": v_A,
        "v_U": v_U,
        "v_arg": v_arg,
        "v_norm": chi(v_norm_value),
        "v_inner": chi(v_inner_value),
        "line_norm": 1 if a_chi == 1 else b_chi,
    }

    out["h_arg_sign"] = h_recomputed
    out["vq_arg_sign"] = vq_recomputed
    out["h_norm_factor"] = out["chi_C"] * out["chi_B"] * out["h_inner"]
    out["v_norm_factor"] = out["chi_t"] * out["v_inner"]
    out["q2_expected_sign"] = chi(transfer.f_value(y) * transfer.k_value(y))
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
        comps = norm_component_values(y, w)
        if comps is None:
            stats["component_unusable"] += 1
            continue
        a = comps["a"]
        b = comps["b"]
        if (a, b) in seen_ab:
            stats["duplicate_ab"] += 1
            continue
        seen_ab.add((a, b))
        rows.append((a, b, comps))
        if max_rows and len(rows) >= max_rows:
            break
    stats["component_rows"] = len(rows)
    return rows, stats


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


def line_map(
    rows: list[tuple[int, int, dict[str, int]]],
    key: str,
    mode: str = "raw",
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
    stats["rows"] = len(rows)
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


NAMED_ATOMS: tuple[tuple[str, str], ...] = (
    ("domain_line", "raw"),
    ("chi_B", "raw"),
    ("chi_C", "raw"),
    ("chi_R", "raw"),
    ("chi_a_plus_2", "raw"),
    ("chi_a_minus_2", "raw"),
    ("chi_a2_minus_4", "raw"),
    ("chi_a2_plus_4", "raw"),
    ("chi_y_minus_2", "raw"),
    ("chi_one_minus_t2", "raw"),
    ("h_norm", "raw"),
    ("h_inner", "raw"),
    ("v_norm", "p26line"),
    ("v_inner", "raw"),
    ("chi_q", "p26line"),
)


def product_map(maps: list[dict[int, int]], keys: tuple[int, ...]) -> dict[int, int]:
    common = set(maps[keys[0]])
    for idx in keys[1:]:
        common &= set(maps[idx])
    out: dict[int, int] = {}
    for a in common:
        value = 1
        for idx in keys:
            value *= maps[idx][a]
        out[a] = value
    return out


def product_span(
    line_maps: list[tuple[str, dict[int, int]]],
    target: dict[int, int],
    top: int,
    max_degree: int,
) -> tuple[list[tuple[float, int, int, int, int, str]], Counter[str]]:
    stats: Counter[str] = Counter()
    maps = [m for _name, m in line_maps]
    scored: list[tuple[float, int, int, int, int, str]] = []
    for degree in range(1, max_degree + 1):
        for keys in combinations(range(len(maps)), degree):
            stats["product_count"] += 1
            candidate = product_map(maps, keys)
            exact_plus, exact_minus, good, total, lift = score(candidate, target)
            if exact_plus or exact_minus:
                stats["exact_products"] += 1
            label = "*".join(line_maps[idx][0] for idx in keys)
            scored.append((lift, good, total, exact_plus, exact_minus, label))
    scored.sort(reverse=True, key=lambda row: (row[3] or row[4], row[0], row[1], -row[2]))
    return scored[:top], stats


def formula_checks(rows: list[tuple[int, int, dict[str, int]]]) -> Counter[str]:
    stats: Counter[str] = Counter()
    for _a, _b, comps in rows:
        stats["rows"] += 1
        if comps["h_arg_sign"] != comps["h"]:
            stats["h_recompute_mismatch"] += 1
        if comps["vq_arg_sign"] != comps["vq"]:
            stats["vq_recompute_mismatch"] += 1
        if comps["h_norm_factor"] != comps["h_norm"]:
            stats["h_norm_factor_mismatch"] += 1
        if comps["v_norm_factor"] == comps["v_norm"]:
            stats["v_norm_factor_agree"] += 1
        if comps["h_inner"] == -comps["chi_one_minus_t2"]:
            stats["h_inner_anti_xpref"] += 1
        if comps["v_inner"] == -comps["chi_one_minus_t2"]:
            stats["v_inner_anti_xpref"] += 1
        if comps["chi_B"] == comps["chi_a_plus_2"]:
            stats["B_equals_a_plus_2"] += 1
        if comps["chi_B"] == -comps["chi_a_minus_2"]:
            stats["B_anti_a_minus_2"] += 1
        if comps["chi_C"] == -comps["chi_R"]:
            stats["C_anti_R"] += 1
        if comps["chi_y_minus_2"] != comps["pref"]:
            stats["pref_formula_mismatch"] += 1
        if comps["q2_expected_sign"] != 1:
            stats["q2_non_square"] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-rows", type=int, default=0)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--max-product-degree", type=int, default=4)
    args = parser.parse_args()

    rows, stats = collect_rows(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )
    target, target_stats = line_map(rows, "T_line", "raw")
    checks = formula_checks(rows)

    print("p27_component_norm_gate")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "component_rows",
        "component_unusable",
        "duplicate_ab",
    ):
        print(f"  {key}={stats[key]}")
    print("formula_checks:")
    for key in (
        "rows",
        "h_recompute_mismatch",
        "vq_recompute_mismatch",
        "h_norm_factor_mismatch",
        "v_norm_factor_agree",
        "h_inner_anti_xpref",
        "v_inner_anti_xpref",
        "B_equals_a_plus_2",
        "B_anti_a_minus_2",
        "C_anti_R",
        "pref_formula_mismatch",
        "q2_non_square",
    ):
        print(f"  {key}={checks[key]}")

    print("named_atom_scores_against_T_line:")
    atom_maps: list[tuple[str, dict[int, int]]] = []
    scored: list[tuple[float, int, int, int, int, str, int, int]] = []
    for key, mode in NAMED_ATOMS:
        candidate, s = line_map(rows, key, mode)
        label = f"{key}:{mode}"
        if s["inconsistent"] == 0 and s["zero"] == 0:
            atom_maps.append((label, candidate))
        exact_plus, exact_minus, good, total, lift = score(candidate, target)
        scored.append((lift, good, total, exact_plus, exact_minus, label, s["inconsistent"], s["zero"]))
    scored.sort(reverse=True, key=lambda row: (row[3] or row[4], row[0], row[1], -row[2]))
    for rank, (lift, good, total, exact_plus, exact_minus, label, inconsistent, zero) in enumerate(scored[: args.top], 1):
        print(
            "  "
            f"rank={rank} atom={label} inconsistent={inconsistent} zero={zero} "
            f"exact_plus={exact_plus} exact_minus={exact_minus} "
            f"best_lift={lift:.9f} good={good} total={total}"
        )

    top_products, product_stats = product_span(
        atom_maps,
        target,
        top=args.top,
        max_degree=args.max_product_degree,
    )
    print("named_product_span:")
    print(f"  usable_atoms={len(atom_maps)}")
    print(f"  product_count={product_stats['product_count']}")
    print(f"  exact_products={product_stats['exact_products']}")
    for rank, (lift, good, total, exact_plus, exact_minus, label) in enumerate(top_products, 1):
        print(
            "  "
            f"rank={rank} product={label} exact_plus={exact_plus} exact_minus={exact_minus} "
            f"best_lift={lift:.9f} good={good} total={total}"
        )

    print(f"target_line_rows={target_stats['line_rows']}")
    print("p27_component_norm_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
