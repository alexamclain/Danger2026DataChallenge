#!/usr/bin/env python3
"""GF(2) span screen for visible p27 line divisor characters.

This tests whether domain_line or T_line is a product of the visible branch and
2-isogeny branch characters on the elliptic line model.  It is deliberately
narrow: the basis is made of named low-complexity divisor characters, not
arbitrary polynomial interpolation.
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


evaluator = load_gate("p27_line_rational_evaluator.py")
transfer = evaluator.transfer
P = evaluator.P

BASIS = (
    ("a", "a"),
    ("a_minus_2", "a-2"),
    ("a_plus_2", "a+2"),
    ("a2_minus_4", "a2-4"),
    ("a2_plus_4", "a2+4"),
    ("u", "u"),
    ("u_minus_1", "u-1"),
    ("u_plus_1", "u+1"),
    ("u2_minus_1", "u2-1"),
    ("u2_plus_1", "u2+1"),
    ("phi0", "phi0"),
    ("phi0_branch", "phi0_2+4"),
    ("phi1", "phi1"),
    ("phi1_branch", "phi1_2-6*phi1+1"),
    ("phim1", "phim1"),
    ("phim1_branch", "phim1_2+6*phim1+1"),
)


def popcount(value: int) -> int:
    if hasattr(value, "bit_count"):
        return value.bit_count()
    return bin(value).count("1")


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def mask_label(mask: int) -> str:
    names = [name for i, (name, _expr) in enumerate(BASIS) if mask & (1 << i)]
    return "*".join(names) if names else "1"


def signed_masks(records: list[tuple[int, int]]) -> tuple[list[int], int, int, int, Counter[str]]:
    exprs = [(name, evaluator.ModularExpression(expr)) for name, expr in BASIS]
    basis_neg_masks = [0 for _name, _expr in BASIS]
    target_plus_mask = 0
    target_minus_mask = 0
    stats: Counter[str] = Counter()
    row_index = 0
    for a, target in records:
        env = evaluator.env_for_a(a)
        if env is None:
            stats["env_none"] += 1
            continue
        usable = True
        signs: list[int] = []
        for name, expr in exprs:
            try:
                sign = transfer.chi(expr.eval(env))
            except ZeroDivisionError:
                sign = 0
            if sign == 0:
                stats[f"zero_{name}"] += 1
                usable = False
            signs.append(sign)
        if not usable:
            stats["unusable_rows"] += 1
            continue
        bit = 1 << row_index
        for i, sign in enumerate(signs):
            if sign == -1:
                basis_neg_masks[i] |= bit
        if target == 1:
            target_plus_mask |= bit
            stats["target_+1"] += 1
        else:
            target_minus_mask |= bit
            stats["target_-1"] += 1
        row_index += 1
    stats["rows"] = row_index
    return basis_neg_masks, target_plus_mask, target_minus_mask, row_index, stats


def mask_metrics(
    negbits: int,
    target_plus_mask: int,
    target_minus_mask: int,
    rowmask: int,
    rows: int,
) -> tuple[int, int, int, int, float]:
    target_plus = popcount(target_plus_mask)
    baseline = target_plus / rows if rows else 0.0
    exact_plus = int(rows > 0 and negbits == target_minus_mask)
    exact_minus = int(rows > 0 and negbits == target_plus_mask)

    selected_plus = rowmask ^ negbits
    selected_minus = negbits
    good_plus = popcount(selected_plus & target_plus_mask)
    total_plus = popcount(selected_plus)
    good_minus = popcount(selected_minus & target_plus_mask)
    total_minus = popcount(selected_minus)

    best_good = best_total = 0
    best_lift = 0.0
    for good, total in ((good_plus, total_plus), (good_minus, total_minus)):
        if total and baseline:
            lift = (good / total) / baseline
            if lift > best_lift:
                best_lift = lift
                best_good = good
                best_total = total
    return exact_plus, exact_minus, best_good, best_total, best_lift


def scan_scope(label: str, records: list[tuple[int, int]], prefix_size: int, top: int) -> None:
    basis_neg_masks, target_plus_mask, target_minus_mask, rows, stats = signed_masks(records)
    prefix_n = min(prefix_size, rows)
    rowmask = (1 << rows) - 1 if rows else 0
    prefix_mask = (1 << prefix_n) - 1 if prefix_n else 0
    prefix_target_plus = target_plus_mask & prefix_mask
    prefix_target_minus = target_minus_mask & prefix_mask
    survivors: list[int] = []
    best_rows: list[tuple[float, int, int, int]] = []
    previous_gray = 0
    current_negbits = 0
    for ordinal in range(1 << len(BASIS)):
        mask = ordinal ^ (ordinal >> 1)
        changed = mask ^ previous_gray
        if changed:
            changed_index = (changed & -changed).bit_length() - 1
            current_negbits ^= basis_neg_masks[changed_index]
        previous_gray = mask
        prefix_negbits = current_negbits & prefix_mask
        exact_plus, exact_minus, _good, _total, _lift = mask_metrics(
            prefix_negbits,
            prefix_target_plus,
            prefix_target_minus,
            prefix_mask,
            prefix_n,
        )
        if exact_plus or exact_minus:
            survivors.append(mask)
        full_exact_plus, full_exact_minus, good, total, lift = mask_metrics(
            current_negbits,
            target_plus_mask,
            target_minus_mask,
            rowmask,
            rows,
        )
        exact = int(full_exact_plus or full_exact_minus)
        best_rows.append((lift, good, total, mask if not exact else -mask - 1))

    full_exact = 0
    exact_masks: list[int] = []
    for mask in survivors:
        negbits = 0
        for i, basis_mask in enumerate(basis_neg_masks):
            if mask & (1 << i):
                negbits ^= basis_mask
        exact_plus, exact_minus, _good, _total, _lift = mask_metrics(
            negbits,
            target_plus_mask,
            target_minus_mask,
            rowmask,
            rows,
        )
        if exact_plus or exact_minus:
            full_exact += 1
            exact_masks.append(mask)
    best_rows.sort(reverse=True, key=lambda row: (row[0], row[1], -row[2]))

    print(f"{label}_span:")
    for key in ("rows", "target_+1", "target_-1", "unusable_rows"):
        print(f"  {key}={stats[key]}")
    print(f"  basis_count={len(BASIS)}")
    print(f"  candidate_count={1 << len(BASIS)}")
    print(f"  prefix_rows={prefix_n}")
    print(f"  prefix_exact_survivors={len(survivors)}")
    print(f"  full_exact_count={full_exact}")
    for rank, (lift, good, total, raw_mask) in enumerate(best_rows[:top], 1):
        exact = raw_mask < 0
        mask = -raw_mask - 1 if exact else raw_mask
        print(
            "  top "
            f"rank={rank} lift={lift:.9f} good={good} total={total} "
            f"exact={int(exact)} label={mask_label(mask)}"
        )
    for mask in exact_masks[:top]:
        print(f"  exact label={mask_label(mask)}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-records", type=int, default=8192)
    parser.add_argument("--prefix-size", type=int, default=2048)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args(argv[1:])

    domain_records, target_records, stats = evaluator.collect_line_records(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_records=args.max_records,
    )
    print("p27_line_character_span_gate")
    print(f"p={P}")
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
    print("basis:")
    for i, (name, expr) in enumerate(BASIS):
        print(f"  {i}: {name} = {expr}")
    scan_scope("domain_line", domain_records, args.prefix_size, args.top)
    scan_scope("target_line", target_records, args.prefix_size, args.top)
    print("p27_line_character_span_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
