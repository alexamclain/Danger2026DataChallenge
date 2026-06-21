#!/usr/bin/env python3
"""Joint p27 line-bit screen for visible divisor characters.

Previous gates tested domain_line and T_line separately.  The practical target
is their simultaneous +1 stratum, so this gate joins the two line bits by `a`
and tests:

  * product_bit = domain_line * T_line;
  * enrichment of the joint (++ ) stratum by visible branch / 2-isogeny
    character products.

The basis is the same named 16-character visible span used by
p27_line_character_span_gate.py.
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


span = load_gate("p27_line_character_span_gate.py")
evaluator = span.evaluator
transfer = span.transfer
P = span.P
BASIS = span.BASIS


def mask_label(mask: int) -> str:
    return span.mask_label(mask)


def popcount(value: int) -> int:
    return span.popcount(value)


def collect_joint_records(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_records: int,
) -> tuple[list[tuple[int, int, int]], Counter[str]]:
    domain_records, target_records, stats = evaluator.collect_line_records(
        seeds=seeds,
        chunks=chunks,
        tids=tids,
        draws_per_thread=draws_per_thread,
        max_records=0,
    )
    domain = dict(domain_records)
    target = dict(target_records)
    rows: list[tuple[int, int, int]] = []
    for a in sorted(set(domain) & set(target)):
        rows.append((a, domain[a], target[a]))
        if max_records and len(rows) >= max_records:
            break
    stats["joint_records"] = len(rows)
    stats["joint_++"] = sum(1 for _a, d, t in rows if d == 1 and t == 1)
    stats["joint_+-"] = sum(1 for _a, d, t in rows if d == 1 and t == -1)
    stats["joint_-+"] = sum(1 for _a, d, t in rows if d == -1 and t == 1)
    stats["joint_--"] = sum(1 for _a, d, t in rows if d == -1 and t == -1)
    return rows, stats


def signed_masks(rows: list[tuple[int, int, int]]) -> tuple[list[int], dict[str, int], int, Counter[str]]:
    exprs = [(name, evaluator.ModularExpression(expr)) for name, expr in BASIS]
    basis_neg_masks = [0 for _name, _expr in BASIS]
    masks = {
        "domain_plus": 0,
        "domain_minus": 0,
        "target_plus": 0,
        "target_minus": 0,
        "product_plus": 0,
        "product_minus": 0,
        "joint_pp": 0,
    }
    stats: Counter[str] = Counter()
    row_index = 0
    for a, domain_bit, target_bit in rows:
        env = evaluator.env_for_a(a)
        if env is None:
            stats["env_none"] += 1
            continue
        signs: list[int] = []
        usable = True
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
        if domain_bit == 1:
            masks["domain_plus"] |= bit
        else:
            masks["domain_minus"] |= bit
        if target_bit == 1:
            masks["target_plus"] |= bit
        else:
            masks["target_minus"] |= bit
        if domain_bit * target_bit == 1:
            masks["product_plus"] |= bit
        else:
            masks["product_minus"] |= bit
        if domain_bit == 1 and target_bit == 1:
            masks["joint_pp"] |= bit
        row_index += 1
    stats["rows"] = row_index
    return basis_neg_masks, masks, row_index, stats


def exact_metrics(
    negbits: int,
    plus_mask: int,
    minus_mask: int,
    rowmask: int,
    rows: int,
) -> tuple[int, int, int, int, float]:
    plus_count = popcount(plus_mask)
    baseline = plus_count / rows if rows else 0.0
    exact_plus = int(rows > 0 and negbits == minus_mask)
    exact_minus = int(rows > 0 and negbits == plus_mask)
    selected_plus = rowmask ^ negbits
    selected_minus = negbits
    good_plus = popcount(selected_plus & plus_mask)
    total_plus = popcount(selected_plus)
    good_minus = popcount(selected_minus & plus_mask)
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


def selector_lift(negbits: int, select_negative: bool, good_mask: int, rowmask: int, rows: int) -> tuple[int, int, float]:
    selected = negbits if select_negative else (rowmask ^ negbits)
    total = popcount(selected)
    good = popcount(selected & good_mask)
    baseline = popcount(good_mask) / rows if rows else 0.0
    lift = (good / total) / baseline if total and baseline else 0.0
    return good, total, lift


def scan_exact_product(label: str, basis_neg_masks: list[int], masks: dict[str, int], rows: int, prefix_size: int, top: int) -> None:
    rowmask = (1 << rows) - 1 if rows else 0
    prefix_n = min(prefix_size, rows)
    prefix_mask = (1 << prefix_n) - 1 if prefix_n else 0
    prefix_plus = masks["product_plus"] & prefix_mask
    prefix_minus = masks["product_minus"] & prefix_mask
    full_plus = masks["product_plus"]
    full_minus = masks["product_minus"]
    survivors: list[int] = []
    best_rows: list[tuple[float, int, int, int]] = []
    current_negbits = 0
    previous_gray = 0
    for ordinal in range(1 << len(BASIS)):
        mask = ordinal ^ (ordinal >> 1)
        changed = mask ^ previous_gray
        if changed:
            changed_index = (changed & -changed).bit_length() - 1
            current_negbits ^= basis_neg_masks[changed_index]
        previous_gray = mask
        prefix_negbits = current_negbits & prefix_mask
        exact_plus, exact_minus, _good, _total, _lift = exact_metrics(
            prefix_negbits, prefix_plus, prefix_minus, prefix_mask, prefix_n
        )
        if exact_plus or exact_minus:
            survivors.append(mask)
        full_exact_plus, full_exact_minus, good, total, lift = exact_metrics(
            current_negbits, full_plus, full_minus, rowmask, rows
        )
        exact = int(full_exact_plus or full_exact_minus)
        best_rows.append((lift, good, total, mask if not exact else -mask - 1))
    full_exact = 0
    for mask in survivors:
        negbits = 0
        for i, basis_mask in enumerate(basis_neg_masks):
            if mask & (1 << i):
                negbits ^= basis_mask
        exact_plus, exact_minus, _good, _total, _lift = exact_metrics(
            negbits, full_plus, full_minus, rowmask, rows
        )
        full_exact += int(exact_plus or exact_minus)
    best_rows.sort(reverse=True, key=lambda row: (row[0], row[1], -row[2]))
    print(f"{label}_product_span:")
    print(f"  rows={rows}")
    print(f"  product_+1={popcount(full_plus)}")
    print(f"  product_-1={popcount(full_minus)}")
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


def scan_joint_selector(label: str, basis_neg_masks: list[int], masks: dict[str, int], rows: int, prefix_size: int, top: int) -> None:
    rowmask = (1 << rows) - 1 if rows else 0
    prefix_n = min(prefix_size, rows)
    prefix_mask = (1 << prefix_n) - 1 if prefix_n else 0
    prefix_good = masks["joint_pp"] & prefix_mask
    full_good = masks["joint_pp"]
    prefix_best: list[tuple[float, int, int, int, int]] = []
    current_negbits = 0
    previous_gray = 0
    for ordinal in range(1 << len(BASIS)):
        mask = ordinal ^ (ordinal >> 1)
        changed = mask ^ previous_gray
        if changed:
            changed_index = (changed & -changed).bit_length() - 1
            current_negbits ^= basis_neg_masks[changed_index]
        previous_gray = mask
        prefix_negbits = current_negbits & prefix_mask
        for select_negative in (0, 1):
            good, total, lift = selector_lift(
                prefix_negbits,
                bool(select_negative),
                prefix_good,
                prefix_mask,
                prefix_n,
            )
            prefix_best.append((lift, good, total, mask, select_negative))
    prefix_best.sort(reverse=True, key=lambda row: (row[0], row[1], -row[2]))

    print(f"{label}_joint_pp_selector:")
    print(f"  rows={rows}")
    print(f"  joint_pp={popcount(full_good)}")
    print(f"  baseline={popcount(full_good) / rows if rows else 0.0:.9f}")
    print(f"  prefix_rows={prefix_n}")
    print(f"  prefix_baseline={popcount(prefix_good) / prefix_n if prefix_n else 0.0:.9f}")
    for rank, (prefix_lift, prefix_good_count, prefix_total, mask, select_negative) in enumerate(prefix_best[:top], 1):
        negbits = 0
        for i, basis_mask in enumerate(basis_neg_masks):
            if mask & (1 << i):
                negbits ^= basis_mask
        full_good_count, full_total, full_lift = selector_lift(
            negbits,
            bool(select_negative),
            full_good,
            rowmask,
            rows,
        )
        orientation = "negative" if select_negative else "positive"
        print(
            "  top "
            f"rank={rank} prefix_lift={prefix_lift:.9f} prefix_good={prefix_good_count} "
            f"prefix_total={prefix_total} full_lift={full_lift:.9f} "
            f"full_good={full_good_count} full_total={full_total} "
            f"orientation={orientation} label={mask_label(mask)}"
        )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-records", type=int, default=8192)
    parser.add_argument("--prefix-size", type=int, default=2048)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args(argv[1:])

    records, collect_stats = collect_joint_records(
        seeds=transfer.parse_range(args.seeds),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_records=args.max_records,
    )
    basis_neg_masks, masks, rows, stats = signed_masks(records)
    print("p27_line_joint_character_span_gate")
    print(f"p={P}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "domain_records",
        "target_records",
        "joint_records",
        "joint_++",
        "joint_+-",
        "joint_-+",
        "joint_--",
        "domain_inconsistent",
        "target_line_inconsistent",
    ):
        print(f"  {key}={collect_stats[key]}")
    print("usable:")
    for key in ("rows", "unusable_rows"):
        print(f"  {key}={stats[key]}")
    scan_exact_product("joint", basis_neg_masks, masks, rows, args.prefix_size, args.top)
    scan_joint_selector("joint", basis_neg_masks, masks, rows, args.prefix_size, args.top)
    print("p27_line_joint_character_span_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

