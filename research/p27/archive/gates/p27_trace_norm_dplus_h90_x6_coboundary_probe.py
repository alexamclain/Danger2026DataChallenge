#!/usr/bin/env python3
"""Compare the post-Dplus x6 class with simple H90 coboundary atoms.

The H90 payload screen already killed low-weight products of the named
payload signs.  This sharper probe targets the remaining plausible bridge:

    after Dplus, d3 = chi(x6);
    the H90 second layer has rho^2 = A_eta = U_eta + z*W_eta.

If chi(x6) differs from an H90 branch class by a simple coboundary, it should
show up as a stable product of signs built from H90 atoms or first-order
rho +/- atom divisors.  This is a bounded finite-field falsifier, not a broad
coefficient search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from types import SimpleNamespace

from p27_trace_norm_post_dplus_probe import (
    P,
    bit_pm1,
    candidate_roots,
    combo_name,
    iter_weighted_combos,
    label2,
    popcount,
    sign_name,
    trace_norm_d_class_parts,
    transfer,
)
from p27_trace_norm_dplus_a_coordinate_bridge_probe import a_from_t


BASE_LINEAR_ATOMS = ("one", "t", "B", "C", "w", "z")
RHO_NAMES = (
    "rho_actual_plus",
    "rho_actual_minus",
    "rho_other_plus",
    "rho_other_minus",
)


def parse_seed_groups(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(";") if part.strip()]


def chi(value: int) -> int:
    return transfer.chi(value % P)


def h90_elements(y: int) -> dict[str, int] | None:
    y %= P
    t = (y - 1) % P
    if t == 0:
        return None
    z = transfer.sqrt_mod(transfer.f_value(y))
    if z is None:
        return None
    w = transfer.sqrt_mod(transfer.k_value(y))
    if w is None:
        return None

    B = (t * t + 1) % P
    C = (t * t + 2 * t - 1) % P
    R = (t * t - 2 * t - 1) % P
    F = t * C % P * B % P
    eps_h = chi(t)
    eps_v = chi(y * C)
    if eps_h == 0 or eps_v == 0:
        return None
    eta = eps_h * eps_v

    def values(for_eta: int) -> dict[str, int | None]:
        Ueta = 2 * t % P * t % P
        Ueta = Ueta * (t - 1) % P
        Ueta = Ueta * B % P * B % P
        Ueta = Ueta * ((for_eta * w + C) % P) % P
        Weta = (t - 1) * B % P
        Weta = Weta * ((4 * t % P * t % P * t + for_eta * B % P * w) % P) % P
        Aplus = (Ueta + z * Weta) % P
        Aminus = (Ueta - z * Weta) % P
        return {
            "Ueta": Ueta,
            "Weta": Weta,
            "Aplus": Aplus,
            "Aminus": Aminus,
            "rho_plus": transfer.sqrt_mod(Aplus),
            "rho_minus": transfer.sqrt_mod(Aminus),
        }

    actual = values(eta)
    other = values(-eta)
    if (
        actual["rho_plus"] is None
        or actual["rho_minus"] is None
        or other["rho_plus"] is None
        or other["rho_minus"] is None
    ):
        return None

    return {
        "y": y,
        "t": t,
        "B": B,
        "C": C,
        "R": R,
        "F": F,
        "z": z,
        "w": w,
        "zw": z * w % P,
        "eta": eta,
        "eps_h": eps_h,
        "eps_v": eps_v,
        "U_actual": int(actual["Ueta"]),
        "W_actual": int(actual["Weta"]),
        "A_actual_plus": int(actual["Aplus"]),
        "A_actual_minus": int(actual["Aminus"]),
        "rho_actual_plus": int(actual["rho_plus"]),
        "rho_actual_minus": int(actual["rho_minus"]),
        "U_other": int(other["Ueta"]),
        "W_other": int(other["Weta"]),
        "A_other_plus": int(other["Aplus"]),
        "A_other_minus": int(other["Aminus"]),
        "rho_other_plus": int(other["rho_plus"]),
        "rho_other_minus": int(other["rho_minus"]),
        "one": 1,
    }


def h90_feature_signs(elements: dict[str, int]) -> dict[str, int]:
    signs = {
        "eta": int(elements["eta"]),
        "eps_h": int(elements["eps_h"]),
        "eps_v": int(elements["eps_v"]),
    }

    for name in (
        "y",
        "t",
        "B",
        "C",
        "R",
        "F",
        "z",
        "w",
        "zw",
        "U_actual",
        "W_actual",
        "A_actual_plus",
        "A_actual_minus",
        "U_other",
        "W_other",
        "A_other_plus",
        "A_other_minus",
    ):
        signs[name] = chi(elements[name])

    for rho_name in RHO_NAMES:
        rho = elements[rho_name]
        signs[rho_name] = chi(rho)
        for atom_name in BASE_LINEAR_ATOMS:
            atom = elements[atom_name]
            signs[f"{rho_name}_plus_{atom_name}"] = chi(rho + atom)
            signs[f"{rho_name}_minus_{atom_name}"] = chi(rho - atom)

    return signs


def dplus_x6_target(y: int, stats: Counter[str]) -> int:
    t = (y - 1) % P
    A = a_from_t(t)
    candidates, _root_disc = candidate_roots(y)
    if not candidates:
        stats["Dplus_no_valid_candidate"] += 1
        return 0

    signs: list[int] = []
    for _root_index, cand_A, xp in candidates:
        stats["Dplus_candidates"] += 1
        if cand_A % P != A:
            stats["candidate_A_formula_mismatch"] += 1
        d1, x5s = label2.halve_all(cand_A, xp)
        stats[f"d1_{sign_name(d1)}"] += 1
        if d1 != 1:
            stats["d1_failure"] += 1
            continue
        for x5 in x5s:
            d2, x6s = label2.halve_all(cand_A, x5)
            stats[f"d2_{sign_name(d2)}"] += 1
            if d2 != 1:
                stats["d2_failure"] += 1
                continue
            for x6 in x6s:
                x6 %= P
                U = (x6 + transfer.inv(x6)) % P
                d3, _x7s = label2.halve_all(cand_A, x6)
                chi_x6 = chi(x6)
                chi_uplus = chi(U + cand_A)
                stats[f"chi_UplusA_{sign_name(chi_uplus)}"] += 1
                stats[f"chi_x6_{sign_name(chi_x6)}"] += 1
                if d3 != chi_x6 * chi_uplus:
                    stats["d3_factor_mismatch"] += 1
                if chi_uplus != 1:
                    stats["UplusA_not_square"] += 1
                signs.append(chi_x6)

    good = {value for value in signs if value in (-1, 1)}
    if not good:
        stats["no_x6_sign"] += 1
        return 0
    if len(good) != 1:
        stats["mixed_x6_sign"] += 1
        return 0
    target = next(iter(good))
    stats[f"target_{sign_name(target)}"] += 1
    return target


def collect_group(seeds: str, args: argparse.Namespace) -> tuple[list[dict[str, int]], Counter[str]]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    stats: Counter[str] = Counter()
    rows: list[dict[str, int]] = []
    seen_y: set[int] = set()
    max_y = args.max_y

    for seed in transfer.parse_range(seeds):
        for chunk in transfer.parse_range(args.chunks):
            for tid in transfer.parse_range(args.tids):
                rng = transfer.cuda_rng(seed, chunk, tid)
                for _draw in range(args.draws_per_thread):
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

                    elements = h90_elements(y)
                    if elements is None:
                        stats["missing_h90_elements"] += 1
                        continue
                    target = dplus_x6_target(y, stats)
                    if target not in (-1, 1):
                        continue

                    row = {"target": target, "y": y}
                    row.update(h90_feature_signs(elements))
                    rows.append(row)
                    stats["analyzed_y"] += 1
                    if max_y and stats["analyzed_y"] >= max_y:
                        return rows, stats
    return rows, stats


def feature_profile(rows: list[dict[str, int]]) -> tuple[list[str], Counter[str]]:
    counters: dict[str, Counter[int]] = {}
    for row in rows:
        for key, value in row.items():
            if key in ("target", "y"):
                continue
            counters.setdefault(key, Counter())[int(value)] += 1

    stats: Counter[str] = Counter()
    active: list[str] = []
    for key in sorted(counters):
        counter = counters[key]
        if counter[0]:
            stats["features_with_zero"] += 1
            continue
        signs = {sign for sign, count in counter.items() if count and sign in (-1, 1)}
        if len(signs) < 2:
            stats["constant_features"] += 1
            continue
        active.append(key)
    stats["active_features"] = len(active)
    return active, stats


def encoded_rows(rows: list[dict[str, int]], features: tuple[str, ...]) -> list[tuple[int, int]]:
    encoded: list[tuple[int, int]] = []
    for row in rows:
        target = int(row["target"])
        if target not in (-1, 1):
            continue
        mask = 0
        ok = True
        for idx, feature in enumerate(features):
            value = int(row.get(feature, 0))
            if value not in (-1, 1):
                ok = False
                break
            mask |= bit_pm1(value) << idx
        if ok:
            encoded.append((mask, bit_pm1(target)))
    return encoded


def bitset_rows(rows: list[dict[str, int]], features: tuple[str, ...]) -> tuple[int, int, list[int]]:
    target_bits = 0
    feature_bits = [0 for _ in features]
    row_index = 0
    for row in rows:
        target = int(row["target"])
        if target not in (-1, 1):
            continue
        values: list[int] = []
        ok = True
        for feature in features:
            value = int(row.get(feature, 0))
            if value not in (-1, 1):
                ok = False
                break
            values.append(value)
        if not ok:
            continue
        if bit_pm1(target):
            target_bits |= 1 << row_index
        for idx, value in enumerate(values):
            if bit_pm1(value):
                feature_bits[idx] |= 1 << row_index
        row_index += 1
    return row_index, target_bits, feature_bits


def combo_bits(feature_bits: list[int], combo: int) -> int:
    out = 0
    active = combo
    while active:
        lsb = active & -active
        out ^= feature_bits[lsb.bit_length() - 1]
        active ^= lsb
    return out


def score_bitset(nrows: int, target_bits: int, feature_bits: list[int], combo: int, orient: int) -> int:
    predicted = combo_bits(feature_bits, combo)
    diff_count = popcount(predicted ^ target_bits)
    if orient == 1:
        return nrows - diff_count
    return diff_count


def exact_combo_bitset(
    nrows: int,
    target_bits: int,
    feature_bits: list[int],
    max_weight: int,
) -> tuple[int, int] | None:
    for combo in iter_weighted_combos(len(feature_bits), max_weight):
        good_plus = score_bitset(nrows, target_bits, feature_bits, combo, 1)
        if nrows and good_plus == nrows:
            return combo, 1
        good_minus = score_bitset(nrows, target_bits, feature_bits, combo, -1)
        if nrows and good_minus == nrows:
            return combo, -1
    return None


def scan_train_heldout(
    train_rows: list[dict[str, int]],
    heldout_rows: list[dict[str, int]],
    features: tuple[str, ...],
    max_weight: int,
    top: int,
) -> None:
    train_n, train_target, train_feature_bits = bitset_rows(train_rows, features)
    held_n, held_target, held_feature_bits = bitset_rows(heldout_rows, features)
    all_n, all_target, all_feature_bits = bitset_rows(train_rows + heldout_rows, features)
    exact = exact_combo_bitset(all_n, all_target, all_feature_bits, max_weight) if all_n else None
    print("h90_x6_coboundary_span:")
    print("  features = " + ", ".join(features))
    print(f"  train_rows = {train_n}")
    print(f"  heldout_rows = {held_n}")
    if exact is None:
        print(f"  exact_combo_weight_le_{max_weight} = none")
    else:
        combo, orient = exact
        print(
            f"  exact_combo_weight_le_{max_weight} = "
            f"{'' if orient == 1 else '-'}{combo_name(features, combo)}"
        )
    scored = []
    for combo in iter_weighted_combos(len(features), max_weight):
        train_plus = score_bitset(train_n, train_target, train_feature_bits, combo, 1)
        train_minus = score_bitset(train_n, train_target, train_feature_bits, combo, -1)
        if train_plus >= train_minus:
            orient = 1
            train_good = train_plus
        else:
            orient = -1
            train_good = train_minus
        held_good = score_bitset(held_n, held_target, held_feature_bits, combo, orient)
        train_rate = train_good / train_n if train_n else 0.0
        held_rate = held_good / held_n if held_n else 0.0
        scored.append((train_rate, held_rate, train_good, train_n, held_good, held_n, orient, combo))
    scored.sort(key=lambda item: (-item[0], -item[1], popcount(item[7]), item[7]))
    print(f"  best_low_weight_train_heldout max_weight={max_weight}:")
    for train_rate, held_rate, train_good, train_total, held_good, held_total, orient, combo in scored[:top]:
        print(
            "    "
            f"train={train_good}/{train_total} {train_rate:.9f} "
            f"heldout={held_good}/{held_total} {held_rate:.9f} "
            f"weight={popcount(combo)} combo={'' if orient == 1 else '-'}{combo_name(features, combo)}"
        )


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    total = stats["target_+1"] + stats["target_-1"]
    if total:
        print(f"  target_plus_rate = {stats['target_+1'] / total:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--max-y", type=int, default=0)
    parser.add_argument("--max-weight", type=int, default=3)
    parser.add_argument("--top", type=int, default=16)
    args = parser.parse_args()

    print("p27 trace/norm Dplus H90-x6 coboundary probe")
    print("question = does chi(x6) equal a simple H90/rho coboundary after Dplus?")
    print(f"p = {P}")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"max_y = {args.max_y}")
    print(f"max_weight = {args.max_weight}")

    groups: list[tuple[str, list[dict[str, int]], Counter[str]]] = []
    all_rows: list[dict[str, int]] = []
    for index, seeds in enumerate(parse_seed_groups(args.seed_groups), start=1):
        rows, stats = collect_group(seeds, args)
        label = f"group{index}_seeds_{seeds.replace(',', '_')}"
        groups.append((label, rows, stats))
        all_rows.extend(rows)
        print_counter(label, stats)

    features, profile_stats = feature_profile(all_rows)
    print_counter("feature_profile", profile_stats)
    if len(groups) >= 2:
        scan_train_heldout(
            train_rows=groups[0][1],
            heldout_rows=groups[1][1],
            features=tuple(features),
            max_weight=args.max_weight,
            top=args.top,
        )

    print("verdict:")
    print("  promote only if an exact or strong heldout H90/rho coboundary appears")
    print("  otherwise keep Dplus/H90 as CAS class comparison, not GPU bucket work")
    print("p27_trace_norm_dplus_h90_x6_coboundary_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
