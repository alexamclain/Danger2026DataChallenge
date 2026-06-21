#!/usr/bin/env python3
"""Post-Dplus trace/norm screen for p27.

The GPU A/B made Dplus look like a 4x stratum; the C depth histogram then
identified it as the first two selected halving gates.  This probe treats that
as prior art and asks the next question: after conditioning on the production
C-style Dplus predicate, do any named trace/norm signs predict the next
selected gate?
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
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
label2 = load_gate("p27_label2_alpha_branch_recurrence_probe.py")
tline = load_gate("p27_tline_component_descent_gate.py")
P = transfer.P

PRE_FEATURES = (
    "H",
    "VQ",
    "X_pref",
    "chi_y",
    "chi_t",
    "chi_y_minus_2",
    "chi_B",
    "chi_C",
    "chi_R",
    "chi_F",
    "chi_root_disc",
)

ROOT_FEATURES = PRE_FEATURES + (
    "root_index",
    "chi_root",
    "chi_root_minus_y",
    "chi_A",
    "chi_A_minus_2",
    "chi_A_plus_2",
    "chi_xP",
    "chi_xP_minus_1",
    "chi_xP_plus_1",
    "chi_a",
    "chi_b",
    "T_line",
)


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def bit_pm1(sign: int) -> int:
    if sign == 1:
        return 0
    if sign == -1:
        return 1
    raise ValueError(sign)


def popcount(value: int) -> int:
    return bin(value).count("1")


def combo_name(features: tuple[str, ...], mask: int) -> str:
    names = [features[i] for i in range(len(features)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def trace_norm_d_class_parts(y: int) -> tuple[int, dict[str, int]]:
    """Mirror x16_y_trace_norm_d_class128 from src/pomerance.c."""
    y %= P
    y2 = y * y % P
    two_y = 2 * y % P
    four_y = 4 * y % P
    b_quad = (y2 - two_y + 2) % P
    c_quad = (y2 - 2) % P
    r_quad = (y2 - four_y + 2) % P
    ym1 = (y - 1) % P
    ym2 = (y - 2) % P

    parts = {
        "B": b_quad,
        "C": c_quad,
        "R": r_quad,
        "F": ym1 * c_quad % P * b_quad % P,
        "root_disc": 0,
    }

    ch = 4 * c_quad % P * b_quad % P
    nh = 64 * pow(ym1, 3, P) % P * c_quad % P * b_quad % P
    sqrt_nh = transfer.sqrt_mod(nh)
    if sqrt_nh is None:
        return 0, parts
    h_arg = 2 * ((ch + sqrt_nh) % P) % P
    h = transfer.chi(h_arg)
    if h == 0:
        return 0, parts

    av = 8 * y % P * pow(ym1, 2, P) % P
    nv = -16 * y2 % P * ym1 % P * r_quad % P * b_quad % P
    sqrt_nv = transfer.sqrt_mod(nv)
    if sqrt_nv is None:
        return 0, parts
    chi_2b = transfer.chi(2 * b_quad)
    chi_v = transfer.chi(2 * ((av + sqrt_nv) % P))
    if chi_2b == 0 or chi_v == 0:
        return 0, parts
    vq = chi_2b * chi_v

    x_pref = transfer.chi(-y * ym2)
    if x_pref == 0:
        return 0, parts

    parts.update(
        {
            "H": h,
            "VQ": vq,
            "X_pref": x_pref,
            "chi_y": transfer.chi(y),
            "chi_t": transfer.chi(ym1),
            "chi_y_minus_2": transfer.chi(ym2),
            "chi_B": transfer.chi(b_quad),
            "chi_C": transfer.chi(c_quad),
            "chi_R": transfer.chi(r_quad),
            "chi_F": transfer.chi(parts["F"]),
        }
    )
    return -x_pref * vq * h, parts


def candidate_roots(y: int) -> tuple[list[tuple[int, int, int]], int]:
    """Return C-ordered (root_index_sign, A, xP) candidates for one y."""
    y %= P
    y2 = y * y % P
    y3 = y2 * y % P
    qa = (y2 - 2 * y) % P
    if qa == 0:
        return [], 0
    qb = (2 * y2 - y3) % P
    qc = (1 - y) % P
    disc = (qb * qb - 4 * qa % P * qc) % P
    sd = transfer.sqrt_mod(disc)
    if sd is None:
        return [], disc
    inv_2qa = transfer.inv(2 * qa)
    roots = [((sd - qb) * inv_2qa) % P, (((-sd) % P - qb) * inv_2qa) % P]
    out: list[tuple[int, int, int]] = []
    for ri, root in enumerate(roots):
        ax = label2.root_to_a_xp(root, y)
        if ax is None:
            continue
        a, xp = ax
        out.append((1 if ri == 0 else -1, a, xp))
    return out, disc


def selected_halving_profile(a: int, xp: int) -> dict[str, object]:
    d1, x5s = label2.halve_all(a, xp)
    out: dict[str, object] = {
        "d1": d1,
        "d2": 0,
        "d3": 0,
        "d4": 0,
        "x5_count": len(x5s),
        "x6_count": 0,
        "x7_count": 0,
    }
    if d1 != 1 or not x5s:
        return out
    x5 = x5s[0]
    d2, x6s = label2.halve_all(a, x5)
    out["d2"] = d2
    out["x6_count"] = len(x6s)
    if d2 != 1 or not x6s:
        return out
    x6 = x6s[0]
    d3, x7s = label2.halve_all(a, x6)
    out["d3"] = d3
    out["x7_count"] = len(x7s)
    if d3 != 1 or not x7s:
        return out
    x7 = x7s[0]
    d4, _x8s = label2.halve_all(a, x7)
    out["d4"] = d4
    return out


def feature_mask(row: dict[str, int], names: tuple[str, ...]) -> int | None:
    mask = 0
    for i, name in enumerate(names):
        value = row.get(name, 0)
        if value == 0:
            return None
        mask |= bit_pm1(value) << i
    return mask


CompressedRows = list[tuple[int, int, int]]


def compress_rows(rows: list[tuple[int, int]]) -> CompressedRows:
    counts: Counter[tuple[int, int]] = Counter(rows)
    return [(mask, target_bit, count) for (mask, target_bit), count in counts.items()]


def score_combo(rows: CompressedRows, combo: int, orient: int) -> tuple[int, int]:
    good = 0
    total = 0
    for mask, target_bit, count in rows:
        parity = popcount(mask & combo) & 1
        if orient == 1:
            good += count if parity == target_bit else 0
        else:
            good += count if parity != target_bit else 0
        total += count
    return good, total


def iter_weighted_combos(nfeatures: int, max_weight: int):
    yield 0
    for weight in range(1, max_weight + 1):
        for idxs in combinations(range(nfeatures), weight):
            combo = 0
            for idx in idxs:
                combo |= 1 << idx
            yield combo


def exact_combo(rows: CompressedRows, nfeatures: int, max_weight: int) -> tuple[int, int] | None:
    for combo in iter_weighted_combos(nfeatures, max_weight):
        good_plus, total = score_combo(rows, combo, 1)
        if total and good_plus == total:
            return combo, 1
        good_minus, total = score_combo(rows, combo, -1)
        if total and good_minus == total:
            return combo, -1
    return None


def best_low_weight(
    train: CompressedRows,
    heldout: CompressedRows,
    features: tuple[str, ...],
    max_weight: int,
    limit: int,
) -> list[tuple[float, float, int, int, int, int, int]]:
    scored: list[tuple[float, float, int, int, int, int, int]] = []
    nfeatures = len(features)
    for combo in iter_weighted_combos(nfeatures, max_weight):
        weight = popcount(combo)
        train_plus, train_total = score_combo(train, combo, 1)
        train_minus, _ = score_combo(train, combo, -1)
        if train_plus >= train_minus:
            orient = 1
            train_good = train_plus
        else:
            orient = -1
            train_good = train_minus
        held_good, held_total = score_combo(heldout, combo, orient)
        train_rate = train_good / train_total if train_total else 0.0
        held_rate = held_good / held_total if held_total else 0.0
        scored.append((train_rate, held_rate, train_good, train_total, held_good, held_total, combo * orient))
    scored.sort(key=lambda item: (-item[0], -item[1], popcount(abs(item[6])), abs(item[6])))
    return scored[:limit]


def collect_rows(args: argparse.Namespace) -> tuple[list[dict[str, int]], Counter[str]]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    rows: list[dict[str, int]] = []
    seen_y: set[int] = set()
    stats: Counter[str] = Counter()
    for seed in transfer.parse_range(args.seeds):
        for chunk in transfer.parse_range(args.chunks):
            for tid in transfer.parse_range(args.tids):
                rng = transfer.cuda_rng(seed, chunk, tid)
                for _ in range(args.draws_per_thread):
                    y = transfer.rand_below96(rng, P, mask)
                    stats["raw_y_draws"] += 1
                    if y == 0:
                        stats["zero_y"] += 1
                        continue
                    if y in seen_y:
                        stats["duplicate_y"] += 1
                        continue
                    seen_y.add(y)
                    y2 = y * y % P
                    if not transfer.x16_y_predicts_nonsplit(y):
                        continue
                    stats["nonsplit_y"] += 1

                    d_class, parts = trace_norm_d_class_parts(y)
                    if d_class == 0:
                        stats["D_zero"] += 1
                        continue
                    stats[f"D_{sign_name(d_class)}"] += 1
                    if d_class != 1:
                        continue
                    stats["Dplus_y"] += 1

                    candidates, root_disc = candidate_roots(y)
                    parts["root_disc"] = root_disc
                    parts["chi_root_disc"] = transfer.chi(root_disc)
                    if not candidates:
                        stats["Dplus_no_valid_candidate"] += 1
                        continue
                    k = transfer.k_value(y)
                    w = transfer.sqrt_mod(k)
                    comps = tline.component_values(y, w) if w is not None else None
                    for root_index, a, xp in candidates:
                        stats["Dplus_candidates"] += 1
                        prof = selected_halving_profile(a, xp)
                        for key in ("d1", "d2", "d3", "d4"):
                            stats[f"{key}_{sign_name(int(prof[key]))}"] += 1
                        if prof["d1"] != 1 or prof["d2"] != 1:
                            stats["Dplus_prefix_failure"] += 1
                            continue
                        row = {name: int(parts.get(name, 0)) for name in PRE_FEATURES}
                        root = 0
                        # Reconstruct the same root just for named root features.
                        for ri, aa, xxp in candidates:
                            if ri == root_index and aa == a and xxp == xp:
                                # root = xP * (root-y) is not invertible to recover here;
                                # recompute below from the quadratic roots if needed.
                                break
                        y3 = y2 * y % P
                        qa = (y2 - 2 * y) % P
                        qb = (2 * y2 - y3) % P
                        sd = transfer.sqrt_mod(root_disc)
                        if sd is not None and qa:
                            inv_2qa = transfer.inv(2 * qa)
                            root = (((sd if root_index == 1 else (-sd) % P) - qb) * inv_2qa) % P
                        row.update(
                            {
                                "root_index": root_index,
                                "chi_root": transfer.chi(root),
                                "chi_root_minus_y": transfer.chi(root - y),
                                "chi_A": transfer.chi(a),
                                "chi_A_minus_2": transfer.chi(a - 2),
                                "chi_A_plus_2": transfer.chi(a + 2),
                                "chi_xP": transfer.chi(xp),
                                "chi_xP_minus_1": transfer.chi(xp - 1),
                                "chi_xP_plus_1": transfer.chi(xp + 1),
                                "d3": int(prof["d3"]),
                                "d4": int(prof["d4"]),
                            }
                        )
                        if comps is not None:
                            row.update(
                                {
                                    "chi_a": comps["a_chi"],
                                    "chi_b": comps["b_chi"],
                                    "T_line": comps["T_line"],
                                }
                            )
                        else:
                            row.update({"chi_a": 0, "chi_b": 0, "T_line": 0})
                        rows.append(row)
                        if args.max_rows and len(rows) >= args.max_rows:
                            return rows, stats
    return rows, stats


def print_span(name: str, rows: list[dict[str, int]], features: tuple[str, ...], target: str, args: argparse.Namespace) -> None:
    encoded: list[tuple[int, int]] = []
    skipped = 0
    for row in rows:
        target_value = int(row[target])
        if target_value not in (-1, 1):
            continue
        mask = feature_mask(row, features)
        if mask is None:
            skipped += 1
            continue
        encoded.append((mask, bit_pm1(target_value)))
    split = len(encoded) // 2
    train = compress_rows(encoded[:split])
    heldout = compress_rows(encoded[split:])
    compressed = compress_rows(encoded)
    exact = exact_combo(compressed, len(features), args.max_weight) if encoded else None
    print(f"{name}:")
    print("  features = " + ", ".join(features))
    print(f"  target = {target}")
    print(f"  rows = {len(encoded)}")
    print(f"  skipped = {skipped}")
    print(
        "  target_plus_rate = "
        f"{(sum(1 for _m, t in encoded if t == 0) / len(encoded)) if encoded else 0.0:.9f}"
    )
    if exact is None:
        print(f"  exact_combo_weight_le_{args.max_weight} = none")
    else:
        combo, orient = exact
        prefix = "" if orient == 1 else "-"
        print(f"  exact_combo_weight_le_{args.max_weight} = {prefix}{combo_name(features, combo)}")
    print(f"  best_low_weight_train_heldout max_weight={args.max_weight}:")
    for train_rate, held_rate, train_good, train_total, held_good, held_total, signed_combo in best_low_weight(
        train, heldout, features, args.max_weight, args.top
    ):
        orient = 1 if signed_combo >= 0 else -1
        combo = abs(signed_combo)
        prefix = "" if orient == 1 else "-"
        print(
            "    "
            f"train={train_good}/{train_total} {train_rate:.9f} "
            f"heldout={held_good}/{held_total} {held_rate:.9f} "
            f"weight={popcount(combo)} combo={prefix}{combo_name(features, combo)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121,122")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-rows", type=int, default=20000)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    rows, stats = collect_rows(args)
    print("p27_trace_norm_post_dplus_probe")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_y_draws",
        "duplicate_y",
        "zero_y",
        "nonsplit_y",
        "D_zero",
        "D_+1",
        "D_-1",
        "Dplus_y",
        "Dplus_no_valid_candidate",
        "Dplus_candidates",
        "Dplus_prefix_failure",
        "d1_+1",
        "d1_-1",
        "d2_+1",
        "d2_-1",
        "d3_+1",
        "d3_-1",
        "d4_+1",
        "d4_-1",
    ):
        print(f"  {key}={stats[key]}")
    print(f"usable_prefix_rows = {len(rows)}")
    d3_plus = sum(1 for row in rows if row["d3"] == 1)
    d3_total = sum(1 for row in rows if row["d3"] in (-1, 1))
    d4_plus = sum(1 for row in rows if row["d4"] == 1)
    d4_total = sum(1 for row in rows if row["d4"] in (-1, 1))
    print("post_dplus_rates:")
    print(f"  d3_plus = {d3_plus}/{d3_total} {(d3_plus / d3_total) if d3_total else 0.0:.9f}")
    print(f"  d4_plus_after_d3 = {d4_plus}/{d4_total} {(d4_plus / d4_total) if d4_total else 0.0:.9f}")
    print_span("pre_root_trace_norm_span_d3", rows, PRE_FEATURES, "d3", args)
    print_span("root_trace_norm_span_d3", rows, ROOT_FEATURES, "d3", args)
    print_span("pre_root_trace_norm_span_d4", rows, PRE_FEATURES, "d4", args)
    print_span("root_trace_norm_span_d4", rows, ROOT_FEATURES, "d4", args)
    print("verdict:")
    print(
        "  Dplus_prefix_exact = "
        f"{int(stats['Dplus_prefix_failure'] == 0 and len(rows) > 0)}"
    )
    print("  promote_named_post_dplus_character = 0 unless a listed low-weight exact combo is non-none")
    print("p27_trace_norm_post_dplus_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
