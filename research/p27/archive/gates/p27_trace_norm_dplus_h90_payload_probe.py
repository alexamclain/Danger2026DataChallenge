#!/usr/bin/env python3
"""Post-Dplus telemetry for the named H90 second-layer class.

The branch extraction identifies the hard Dplus payload as

    A_eta = U_eta + z*W_eta

on the cover z^2 = F over E_h90.  This probe asks whether the finite-field
signs and selected square-root orientations attached to A_eta predict the next
selected gates d3/d4 on the same C-style Dplus rows used by the earlier
post-Dplus screens.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from types import SimpleNamespace

from p27_trace_norm_post_dplus_probe import (
    P,
    bit_pm1,
    combo_name,
    compress_rows,
    collect_rows,
    exact_combo,
    feature_mask,
    iter_weighted_combos,
    popcount,
    score_combo,
    sign_name,
    transfer,
)


H90_FEATURES = (
    "eta",
    "root_eta",
    "A_actual",
    "A_other_plus",
    "A_other_minus",
    "U_actual",
    "W_actual",
    "U_other",
    "W_other",
    "rho_actual",
    "rho_other_plus",
    "rho_other_minus",
    "root_rho_actual",
    "root_A_other_plus",
)


def h90_pack(y: int) -> dict[str, int] | None:
    y %= P
    t = (y - 1) % P
    if t == 0:
        return None
    z = transfer.sqrt_mod(transfer.f_value(y))
    if z is None:
        return None
    k = transfer.k_value(y)
    w = transfer.sqrt_mod(k)
    if w is None:
        return None
    b = (t * t + 1) % P
    c = (t * t + 2 * t - 1) % P
    eps_h = transfer.chi(t)
    eps_v = transfer.chi(y * c)
    if eps_h == 0 or eps_v == 0:
        return None
    eta = eps_h * eps_v

    def values(for_eta: int) -> tuple[int, int, int, int, int]:
        u_eta = 2 * t % P * t % P
        u_eta = u_eta * (t - 1) % P
        u_eta = u_eta * b % P * b % P
        u_eta = u_eta * ((for_eta * w + c) % P) % P
        w_eta = (t - 1) * b % P
        w_eta = w_eta * ((4 * t % P * t % P * t + for_eta * b % P * w) % P) % P
        a_plus = (u_eta + z * w_eta) % P
        a_minus = (u_eta - z * w_eta) % P
        return u_eta, w_eta, a_plus, a_minus, transfer.chi(a_plus)

    u_actual, w_actual, a_actual, a_actual_conj, chi_a_actual = values(eta)
    u_other, w_other, a_other_plus, a_other_minus, _chi_a_other = values(-eta)
    rho_actual = transfer.sqrt_mod(a_actual)
    rho_other_plus = transfer.sqrt_mod(a_other_plus)
    rho_other_minus = transfer.sqrt_mod(a_other_minus)
    return {
        "eta": eta,
        "eps_h": eps_h,
        "eps_v": eps_v,
        "A_actual": chi_a_actual,
        "A_actual_conj": transfer.chi(a_actual_conj),
        "A_other_plus": transfer.chi(a_other_plus),
        "A_other_minus": transfer.chi(a_other_minus),
        "U_actual": transfer.chi(u_actual),
        "W_actual": transfer.chi(w_actual),
        "U_other": transfer.chi(u_other),
        "W_other": transfer.chi(w_other),
        "rho_actual": transfer.chi(rho_actual) if rho_actual is not None else 0,
        "rho_other_plus": transfer.chi(rho_other_plus) if rho_other_plus is not None else 0,
        "rho_other_minus": transfer.chi(rho_other_minus) if rho_other_minus is not None else 0,
    }


def enrich_rows(rows: list[dict[str, int]]) -> tuple[list[dict[str, int]], Counter[str]]:
    stats: Counter[str] = Counter()
    out: list[dict[str, int]] = []
    for row in rows:
        pack = h90_pack(int(row["y"]))
        if pack is None:
            stats["missing_h90_pack"] += 1
            continue
        enriched = dict(row)
        enriched.update(pack)
        root_index = int(row.get("root_index", 0))
        if root_index in (-1, 1):
            enriched["root_eta"] = root_index * pack["eta"]
            enriched["root_rho_actual"] = root_index * pack["rho_actual"]
            enriched["root_A_other_plus"] = root_index * pack["A_other_plus"]
        else:
            enriched["root_eta"] = 0
            enriched["root_rho_actual"] = 0
            enriched["root_A_other_plus"] = 0
        stats[f"A_actual_{sign_name(pack['A_actual'])}"] += 1
        stats[f"A_actual_conj_{sign_name(pack['A_actual_conj'])}"] += 1
        stats[f"A_other_plus_{sign_name(pack['A_other_plus'])}"] += 1
        stats[f"A_other_minus_{sign_name(pack['A_other_minus'])}"] += 1
        out.append(enriched)
    stats["enriched_rows"] = len(out)
    return out, stats


def summarize_state(rows: list[dict[str, int]], feature: str, target: str) -> Counter[str]:
    stats: Counter[str] = Counter()
    buckets: defaultdict[int, Counter[str]] = defaultdict(Counter)
    for row in rows:
        f = int(row.get(feature, 0))
        t = int(row.get(target, 0))
        if f not in (-1, 1) or t not in (-1, 1):
            continue
        buckets[f]["total"] += 1
        buckets[f][f"target_{sign_name(t)}"] += 1
    for f, counter in buckets.items():
        total = counter["total"]
        plus = counter["target_+1"]
        stats[f"{feature}_{sign_name(f)}_total"] = total
        stats[f"{feature}_{sign_name(f)}_plus"] = plus
        stats[f"{feature}_{sign_name(f)}_minus"] = total - plus
        stats[f"{feature}_{sign_name(f)}_plus_rate_x1000000"] = plus * 1_000_000 // total if total else 0
    stats["rows"] = sum(counter["total"] for counter in buckets.values())
    stats["target_plus"] = sum(counter["target_+1"] for counter in buckets.values())
    stats["target_minus"] = stats["rows"] - stats["target_plus"]
    stats["target_plus_rate_x1000000"] = (
        stats["target_plus"] * 1_000_000 // stats["rows"] if stats["rows"] else 0
    )
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def encoded_rows(rows: list[dict[str, int]], features: tuple[str, ...], target: str) -> list[tuple[int, int]]:
    encoded: list[tuple[int, int]] = []
    for row in rows:
        target_value = int(row.get(target, 0))
        if target_value not in (-1, 1):
            continue
        mask = feature_mask(row, features)
        if mask is None:
            continue
        encoded.append((mask, bit_pm1(target_value)))
    return encoded


def scan_train_heldout(
    train_rows: list[dict[str, int]],
    heldout_rows: list[dict[str, int]],
    target: str,
    max_weight: int,
    top: int,
) -> None:
    train_encoded = encoded_rows(train_rows, H90_FEATURES, target)
    heldout_encoded = encoded_rows(heldout_rows, H90_FEATURES, target)
    train = compress_rows(train_encoded)
    heldout = compress_rows(heldout_encoded)
    all_rows = compress_rows(train_encoded + heldout_encoded)
    exact = exact_combo(all_rows, len(H90_FEATURES), max_weight) if train_encoded or heldout_encoded else None
    print(f"h90_payload_span_{target}:")
    print("  features = " + ", ".join(H90_FEATURES))
    print(f"  train_rows = {len(train_encoded)}")
    print(f"  heldout_rows = {len(heldout_encoded)}")
    if exact is None:
        print(f"  exact_combo_weight_le_{max_weight} = none")
    else:
        combo, orient = exact
        print(f"  exact_combo_weight_le_{max_weight} = {'' if orient == 1 else '-'}{combo_name(H90_FEATURES, combo)}")
    scored = []
    for combo in iter_weighted_combos(len(H90_FEATURES), max_weight):
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
        scored.append((train_rate, held_rate, train_good, train_total, held_good, held_total, orient, combo))
    scored.sort(key=lambda item: (-item[0], -item[1], popcount(item[7]), item[7]))
    print(f"  best_low_weight_train_heldout max_weight={max_weight}:")
    for train_rate, held_rate, train_good, train_total, held_good, held_total, orient, combo in scored[:top]:
        print(
            "    "
            f"train={train_good}/{train_total} {train_rate:.9f} "
            f"heldout={held_good}/{held_total} {held_rate:.9f} "
            f"weight={popcount(combo)} combo={'' if orient == 1 else '-'}{combo_name(H90_FEATURES, combo)}"
        )


def collect_group(seeds: str, args: argparse.Namespace) -> tuple[list[dict[str, int]], Counter[str]]:
    subargs = SimpleNamespace(
        seeds=seeds,
        chunks=args.chunks,
        tids=args.tids,
        draws_per_thread=args.draws_per_thread,
        max_rows=args.max_rows,
    )
    rows, stats = collect_rows(subargs)
    enriched, h90_stats = enrich_rows(rows)
    stats.update({f"h90_{key}": value for key, value in h90_stats.items()})
    return enriched, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-rows", type=int, default=20000)
    parser.add_argument("--max-weight", type=int, default=3)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 trace/norm Dplus H90 payload probe")
    print("question = does A_eta or its H90 telemetry predict post-Dplus d3/d4?")
    print(f"p = {P}")
    print(f"seed_groups = {args.seed_groups}")
    groups: list[tuple[str, list[dict[str, int]], Counter[str]]] = []
    for index, seeds in enumerate(args.seed_groups.split(";"), start=1):
        rows, stats = collect_group(seeds, args)
        label = f"group{index}_seeds_{seeds.replace(',', '_')}"
        groups.append((label, rows, stats))
        print_counter(f"{label}_sample", stats)
        for target in ("d3", "d4"):
            for feature in H90_FEATURES:
                print_counter(f"{label}_{target}_{feature}", summarize_state(rows, feature, target))
    if len(groups) >= 2:
        train_label, train_rows, _ = groups[0]
        held_label, held_rows, _ = groups[1]
        print(f"train_group = {train_label}")
        print(f"heldout_group = {held_label}")
        scan_train_heldout(train_rows, held_rows, "d3", args.max_weight, args.top)
        scan_train_heldout(train_rows, held_rows, "d4", args.max_weight, args.top)
    print("p27_trace_norm_dplus_h90_payload_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
