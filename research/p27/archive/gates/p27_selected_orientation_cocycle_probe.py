#!/usr/bin/env python3
"""P27 selected-branch orientation/cocycle span screen.

The local U+2 norm screen killed visible A,x norm factors.  This probe asks
the next sharper question: after the w-square branch is selected, can the next
U+2 bit be expressed as a GF(2) product of natural selected-branch orientation
characters from the successful prefix?

This is still a finite-field falsifier, not a theorem.  A positive exact span
would name a concrete H90/cocycle relation to derive.  A negative result kills
the simplest selected-s orientation products.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

from p27_halving_usquare_gate_probe import halve_u_records
from p27_label2_alpha_branch_recurrence_probe import P, legendre, sample_rows, sqrt_mod


LOCAL_FEATURES = [
    ("x", lambda a, x, s, u, uo: x),
    ("x-1", lambda a, x, s, u, uo: x - 1),
    ("x+1", lambda a, x, s, u, uo: x + 1),
    ("A-2", lambda a, x, s, u, uo: a - 2),
    ("A+2", lambda a, x, s, u, uo: a + 2),
    ("2-A", lambda a, x, s, u, uo: 2 - a),
    ("-A-2", lambda a, x, s, u, uo: -a - 2),
    ("x*(2-A)", lambda a, x, s, u, uo: x * (2 - a)),
    ("-x*(A+2)", lambda a, x, s, u, uo: -x * (a + 2)),
    ("A2-4", lambda a, x, s, u, uo: a * a - 4),
]

ORIENTATION_FEATURES = [
    ("s_sel", lambda a, x, s, u, uo: s),
    ("s_other", lambda a, x, s, u, uo: -s),
    ("u_sel", lambda a, x, s, u, uo: u),
    ("u_other", lambda a, x, s, u, uo: uo),
    ("x+s_sel", lambda a, x, s, u, uo: x + s),
    ("x-s_sel", lambda a, x, s, u, uo: x - s),
    ("A+s_sel", lambda a, x, s, u, uo: a + s),
    ("A-s_sel", lambda a, x, s, u, uo: a - s),
    ("s_sel+1", lambda a, x, s, u, uo: s + 1),
    ("s_sel-1", lambda a, x, s, u, uo: s - 1),
    ("u_sel+A", lambda a, x, s, u, uo: u + a),
    ("u_sel-A", lambda a, x, s, u, uo: u - a),
    ("u_other+A", lambda a, x, s, u, uo: uo + a),
    ("u_other-A", lambda a, x, s, u, uo: uo - a),
]


def bit_pm1(v: int) -> int:
    if v == 1:
        return 0
    if v == -1:
        return 1
    raise ValueError(v)


def popcount(n: int) -> int:
    return bin(n).count("1")


def combo_name(combo: int, names: list[str]) -> str:
    if combo == 0:
        return "1"
    out = [names[i] for i in range(len(names)) if (combo >> i) & 1]
    return " * ".join(out) if out else "1"


def selected_transition(a: int, x: int) -> tuple[dict[str, object] | None, Counter]:
    stats: Counter = Counter()
    d = (x * x + a * x + 1) % P
    sd = sqrt_mod(d)
    if sd is None:
        stats["d_not_square"] += 1
        return None, stats

    d_chi, records = halve_u_records(a, x)
    if d_chi != 1:
        stats["d_chi_mismatch"] += 1
        return None, stats
    good = [rec for rec in records if int(rec["w_chi"]) == 1]
    if len(good) != 1:
        stats[f"good_w_records_{len(good)}"] += 1
        return None, stats

    rec = good[0]
    sign = int(rec["sign"])
    s_sel = sd if sign == 1 else (-sd) % P
    u_sel = int(rec["u"])
    u_other = (2 * x - 2 * s_sel) % P
    up = int(rec["u_plus_2_chi"])
    um = int(rec["u_minus_2_chi"])
    if up != um:
        stats["uplus_uminus_mismatch"] += 1
    xs = rec["xs"]
    assert isinstance(xs, list)
    if len(xs) != 2:
        stats[f"x_count_{len(xs)}"] += 1
    return {
        "target": bit_pm1(up),
        "target_pm1": up,
        "next_x": int(xs[0]) if xs else None,
        "s_sel": s_sel,
        "u_sel": u_sel,
        "u_other": u_other,
    }, stats


def transition_feature_bits(a: int, x: int, trans: dict[str, object]) -> tuple[list[int], list[str]] | None:
    s = int(trans["s_sel"])
    u = int(trans["u_sel"])
    uo = int(trans["u_other"])
    bits: list[int] = []
    names: list[str] = []
    for family, funcs in [("local", LOCAL_FEATURES), ("orient", ORIENTATION_FEATURES)]:
        for name, fn in funcs:
            c = legendre(fn(a, x, s, u, uo))
            if c == 0:
                return None
            bits.append(bit_pm1(c))
            names.append(f"{family}:{name}")
    return bits, names


def columns_from_rows(rows: list[tuple[int, int]], nfeatures: int) -> tuple[list[int], int]:
    cols = [0] * nfeatures
    target = 0
    for r, (mask, t) in enumerate(rows):
        if t:
            target |= 1 << r
        for i in range(nfeatures):
            if (mask >> i) & 1:
                cols[i] |= 1 << r
    return cols, target


def solve_exact(rows: list[tuple[int, int]], names: list[str]) -> int | None:
    if not rows:
        return None
    cols, target = columns_from_rows(rows, len(names))
    all_ones = (1 << len(rows)) - 1
    # Include const_-1 so complements are represented as genuine character
    # products; bit 1 means "nonsquare", so XOR with all ones flips target.
    cols = [all_ones] + cols
    aug_names = ["const_-1"] + names
    basis: dict[int, int] = {}
    basis_combo: dict[int, int] = {}
    for i, col in enumerate(cols):
        vec = col
        combo = 1 << i
        while vec:
            pivot = vec.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vec
                basis_combo[pivot] = combo
                break
            vec ^= basis[pivot]
            combo ^= basis_combo[pivot]

    vec = target
    combo = 0
    while vec:
        pivot = vec.bit_length() - 1
        if pivot not in basis:
            return None
        vec ^= basis[pivot]
        combo ^= basis_combo[pivot]

    # Convert from augmented combo bit positions back to caller convention by
    # returning an encoded combo over augmented names.  The caller prints with
    # augmented names separately.
    names[:] = aug_names
    return combo


def best_low_weight(rows: list[tuple[int, int]], names: list[str], max_weight: int, limit: int) -> list[tuple[int, int, int]]:
    if not rows:
        return []
    cols, target = columns_from_rows(rows, len(names))
    all_ones = (1 << len(rows)) - 1
    cols = [all_ones] + cols
    aug_names = ["const_-1"] + names
    scored: list[tuple[int, int, int]] = []
    for weight in range(0, max_weight + 1):
        if weight == 0:
            combos = [()]
        else:
            combos = combinations(range(len(cols)), weight)
        for idxs in combos:
            pred = 0
            combo = 0
            for idx in idxs:
                pred ^= cols[idx]
                combo |= 1 << idx
            good = len(rows) - popcount(pred ^ target)
            scored.append((good, weight, combo))
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    # Mutate names in the same way as solve_exact for easy printing.
    names[:] = aug_names
    return scored[:limit]


def summarize_gate(name: str, rows: list[tuple[int, int]], feature_names: list[str]) -> None:
    print(f"{name}:")
    print(f"  rows = {len(rows)}")
    target_ones = sum(t for _, t in rows)
    print(f"  target_minus_bits = {target_ones}")
    print(f"  target_plus_rate = {(1 - target_ones / len(rows)) if rows else 0.0:.9f}")

    exact_names = feature_names[:]
    exact = solve_exact(rows, exact_names)
    print(f"  exact_combo = {combo_name(exact, exact_names) if exact is not None else 'none'}")

    best_names = feature_names[:]
    print("  best_weight_le_3:")
    for good, weight, combo in best_low_weight(rows, best_names, 3, 8):
        rate = good / len(rows) if rows else 0.0
        print(
            f"    good={good}/{len(rows)} rate={rate:.9f} "
            f"weight={weight} combo={combo_name(combo, best_names)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=6000000)
    parser.add_argument("--max-target-gate", type=int, default=6)
    args = parser.parse_args()

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    gate_rows: dict[int, list[tuple[int, int]]] = {g: [] for g in range(3, args.max_target_gate + 1)}
    gate_feature_names: dict[int, list[str]] = {}
    stats: Counter = Counter()

    for row in rows:
        cand = row["root0"]
        assert isinstance(cand, dict)
        a = int(cand["A"])
        x = int(cand["x5"])
        prefix_bits: list[int] = []
        prefix_names: list[str] = []
        for gate in range(3, args.max_target_gate + 1):
            trans, step_stats = selected_transition(a, x)
            stats.update(f"gate{gate}_{key}" for key in step_stats.elements())
            if trans is None:
                break
            packed = transition_feature_bits(a, x, trans)
            if packed is None:
                stats[f"gate{gate}_zero_feature"] += 1
                break
            bits, names = packed
            offset = len(prefix_bits)
            prefix_bits.extend(bits)
            prefix_names.extend(f"g{gate}:{name}" for name in names)
            if gate not in gate_feature_names:
                gate_feature_names[gate] = prefix_names[:]
            elif gate_feature_names[gate] != prefix_names:
                raise RuntimeError("feature name drift")
            mask = 0
            for i, bit in enumerate(prefix_bits):
                mask |= bit << i
            gate_rows[gate].append((mask, int(trans["target"])))

            # Continue only on plus targets; otherwise the next selected
            # halving gate is not defined over F_p on this path.
            if int(trans["target_pm1"]) != 1 or trans["next_x"] is None:
                break
            x = int(trans["next_x"])
            if len(prefix_bits) == offset:
                raise RuntimeError("empty feature block")

    print("p27 selected orientation/cocycle span probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"max_target_gate = {args.max_target_gate}")
    print(f"sampled_pairs = {len(rows)}")
    for key in sorted(sample_stats):
        print(f"sample_stat {key} = {sample_stats[key]}")
    print("anomaly_stats:")
    if stats:
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
    else:
        print("  none")
    for gate in range(3, args.max_target_gate + 1):
        summarize_gate(
            f"gate_{gate}_selected_uplus_from_prefix_orientation_span",
            gate_rows[gate],
            gate_feature_names.get(gate, []),
        )
    print("feature_block:")
    for i, name in enumerate([name for name, _ in LOCAL_FEATURES] + [name for name, _ in ORIENTATION_FEATURES]):
        print(f"  {i:02d} {name}")
    print("p27_selected_orientation_cocycle_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
