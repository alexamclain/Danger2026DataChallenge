#!/usr/bin/env python3
"""H90 norm-one recurrence screen for the p27 label-2 cover.

The order-4 lift gives a natural norm-one element

    u = (m0 + mt*T) / (2*T*Salpha),

with u(T) * u(-T) = 1.  This is a better target than another broad visible
character scan: if the cyclic-quartic structure is useful for later gates,
simple squareclasses built from u or its H90 companions might correlate with
d3/d4 on heldout data.

The probe screens compact H90-derived features on train/heldout p27 samples.
It reports both canonical-T features and the subset whose squareclass is
invariant under T -> -T on the sampled rows.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_label2_alpha_branch_recurrence_probe import (
    P,
    bit_pm1,
    inv,
    legendre,
    sample_rows,
    sqrt_mod,
)


FEATURES = [
    "u",
    "u+1",
    "u-1",
    "u2+1",
    "u2-1",
    "u+uinv",
    "u-uinv",
    "mplus",
    "denom",
    "mtT",
    "m0",
    "Salpha",
    "prefactor",
    "L",
]


@dataclass(frozen=True)
class Dataset:
    name: str
    masks: list[int]
    d3_targets: list[int]
    d4_targets: list[int | None]
    invariant_mask: int
    stats: Counter


def popcount(n: int) -> int:
    return bin(n).count("1")


def normalize(values: list[int]) -> int | None:
    vals = {v for v in values if v in (-1, 1)}
    if len(vals) != 1:
        return None
    return vals.pop()


def h90_feature_values(x: int, w: int, t: int, p: int = P) -> dict[str, int]:
    x2 = x * x % p
    x3 = x2 * x % p
    mtlin = (2 * w * x + x3 + x2 - x - 1) % p
    mt = (x + 1) * mtlin % p
    m0 = (x2 + 1) * (x2 + 2 * x - 1) % p
    m0 = m0 * ((w * x + w + 2 * x2) % p) % p
    salpha = (w * (x + 1) + 2 * x2) % p
    denom = 2 * t % p * salpha % p
    mplus = (m0 + mt * t) % p
    mt_t = mt * t % p
    if denom == 0 or mplus == 0:
        return {}
    u = mplus * inv(denom, p) % p
    uinv = inv(u, p)
    pref = w * (x2 + 1) % p * inv(x, p) % p
    linear_l = (4 * w * x2 + 4 * w * x + x2 * x2 + 6 * x3 - 2 * x - 1) % p
    return {
        "u": u,
        "u+1": (u + 1) % p,
        "u-1": (u - 1) % p,
        "u2+1": (u * u + 1) % p,
        "u2-1": (u * u - 1) % p,
        "u+uinv": (u + uinv) % p,
        "u-uinv": (u - uinv) % p,
        "mplus": mplus,
        "denom": denom,
        "mtT": mt_t,
        "m0": m0,
        "Salpha": salpha,
        "prefactor": pref,
        "L": linear_l,
    }


def target_bits_from_candidate(cand: dict[str, object]) -> tuple[int | None, int | None]:
    d3_classes = [int(v) for v in cand["d3_classes"]]  # type: ignore[index]
    d3 = normalize(d3_classes)
    d4: int | None = None
    if d3 == 1:
        flat: list[int] = []
        for group in cand["d4_groups"]:  # type: ignore[index]
            flat.extend(int(v) for v in group)
        d4 = normalize(flat)
    return d3, d4


def collect_dataset(name: str, target: int, seed: int, max_draws: int) -> Dataset:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    masks: list[int] = []
    d3_targets: list[int] = []
    d4_targets: list[int | None] = []
    sign_mismatch = Counter()
    feature_seen = Counter()

    for row in rows:
        x = int(row["X"])
        w = int(row["W"])
        t2 = x * (x * x + 1) % P * ((x * x + 2 * x - 1) % P) % P
        t = sqrt_mod(t2)
        if t is None:
            stats["missing_t_reconstruct"] += 1
            continue

        root0 = row["root0"]
        assert isinstance(root0, dict)
        d3, d4 = target_bits_from_candidate(root0)
        if d3 is None:
            stats["d3_mixed_or_missing"] += 1
            continue

        vals = h90_feature_values(x, w, t)
        vals_neg = h90_feature_values(x, w, (-t) % P)
        if not vals or not vals_neg:
            stats["h90_degenerate"] += 1
            continue

        mask = 0
        skip = False
        for i, feature in enumerate(FEATURES):
            chi = legendre(vals[feature])
            chi_neg = legendre(vals_neg[feature])
            if chi == 0:
                stats[f"zero_{feature}"] += 1
                skip = True
                break
            if chi_neg == 0:
                stats[f"zero_neg_{feature}"] += 1
            else:
                feature_seen[feature] += 1
                if chi != chi_neg:
                    sign_mismatch[feature] += 1
            mask |= bit_pm1(chi) << i
        if skip:
            continue

        masks.append(mask)
        d3_targets.append(bit_pm1(d3))
        d4_targets.append(bit_pm1(d4) if d4 in (-1, 1) else None)

    invariant_mask = 0
    for i, feature in enumerate(FEATURES):
        if feature_seen[feature] and sign_mismatch[feature] == 0:
            invariant_mask |= 1 << i
        stats[f"sign_mismatch_{feature}"] = sign_mismatch[feature]
        stats[f"sign_seen_{feature}"] = feature_seen[feature]

    stats["sampled_pairs"] = len(rows)
    stats["usable_rows"] = len(masks)
    stats["d3_plus_rows"] = sum(1 for bit in d3_targets if bit == 0)
    stats["d3_minus_rows"] = sum(1 for bit in d3_targets if bit == 1)
    stats["d4_rows"] = sum(1 for bit in d4_targets if bit is not None)
    stats["d4_plus_rows"] = sum(1 for bit in d4_targets if bit == 0)
    stats["d4_minus_rows"] = sum(1 for bit in d4_targets if bit == 1)
    stats["invariant_feature_count"] = popcount(invariant_mask)
    return Dataset(name, masks, d3_targets, d4_targets, invariant_mask, stats)


def combo_name(combo: int) -> str:
    names = [FEATURES[i] for i in range(len(FEATURES)) if (combo >> i) & 1]
    return " * ".join(names) if names else "1"


def score_combo(combo: int, masks: list[int], targets: list[int | None]) -> tuple[int, int]:
    good = 0
    total = 0
    for mask, target in zip(masks, targets):
        if target is None:
            continue
        total += 1
        good += (popcount(mask & combo) & 1) == target
    return good, total


def best_combos(
    dataset: Dataset,
    target_name: str,
    allowed_mask: int,
    limit: int,
) -> list[tuple[int, int, int, int]]:
    targets: list[int | None]
    if target_name == "d3":
        targets = list(dataset.d3_targets)
    elif target_name == "d4":
        targets = dataset.d4_targets
    else:
        raise ValueError(target_name)

    allowed_bits = [i for i in range(len(FEATURES)) if (allowed_mask >> i) & 1]
    out: list[tuple[int, int, int, int]] = []
    for sub in range(1 << len(allowed_bits)):
        combo = 0
        for j, bit in enumerate(allowed_bits):
            if (sub >> j) & 1:
                combo |= 1 << bit
        good, total = score_combo(combo, dataset.masks, targets)
        if total:
            out.append((good, total, popcount(combo), combo))
    out.sort(key=lambda item: (item[0] / item[1], -item[2], item[0]), reverse=True)
    return out[:limit]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_combo_table(
    label: str,
    train: Dataset,
    heldout: Dataset,
    target_name: str,
    allowed_mask: int,
    limit: int,
) -> None:
    combos = best_combos(train, target_name, allowed_mask, limit)
    print(f"{label}:")
    print(f"  features = {combo_name(allowed_mask)}")
    if not combos:
        print("  none")
        return
    held_targets = list(heldout.d3_targets) if target_name == "d3" else heldout.d4_targets
    for good, total, weight, combo in combos:
        hgood, htotal = score_combo(combo, heldout.masks, held_targets)
        train_rate = good / total if total else 0.0
        held_rate = hgood / htotal if htotal else 0.0
        print(
            f"  train={good}/{total} rate={train_rate:.9f} "
            f"heldout={hgood}/{htotal} rate={held_rate:.9f} "
            f"weight={weight} combo={combo_name(combo)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=8000)
    parser.add_argument("--heldout-target", type=int, default=8000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    train = collect_dataset("train", args.target, args.seed, args.max_draws)
    heldout = collect_dataset("heldout", args.heldout_target, args.heldout_seed, args.max_draws)
    all_mask = (1 << len(FEATURES)) - 1
    shared_invariant = train.invariant_mask & heldout.invariant_mask

    print("p27 label2 H90 norm-one recurrence probe")
    print(f"p = {P}")
    print(f"features = {', '.join(FEATURES)}")
    print_counter("train_stats", train.stats)
    print_counter("heldout_stats", heldout.stats)
    print(f"train_invariant_features = {combo_name(train.invariant_mask)}")
    print(f"heldout_invariant_features = {combo_name(heldout.invariant_mask)}")
    print(f"shared_invariant_features = {combo_name(shared_invariant)}")
    print_combo_table("d3_all_h90_features", train, heldout, "d3", all_mask, args.top)
    print_combo_table("d3_Tsign_invariant_h90_features", train, heldout, "d3", shared_invariant, args.top)
    print_combo_table("d4_all_h90_features", train, heldout, "d4", all_mask, args.top)
    print_combo_table("d4_Tsign_invariant_h90_features", train, heldout, "d4", shared_invariant, args.top)
    print("p27_label2_h90_normone_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
