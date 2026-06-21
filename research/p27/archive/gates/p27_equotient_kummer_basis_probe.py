#!/usr/bin/env python3
"""Named E-quotient Kummer/theta basis screen for p27 d3/d4.

Earlier probes showed that d3 and d4 descend to the residual elliptic quotient
E: W^2 = X^3-X, but are not degree-1 line characters.  This probe tests the
next principled possibility: are those bits products of the named torsion,
2-descent, and order-4/Hilbert-90 functions already present on E?

This is intentionally a small structural basis, not an arbitrary rational
function search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_label2_alpha_branch_recurrence_probe import P, feature_values, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    p27_rows,
    quotient_bit_rows_from_candidates,
)


BASIS = [
    "X",
    "W",
    "X-1",
    "X+1",
    "X2+1",
    "X2+2X-1",
    "X2-2X-1",
    "S",
    "S_conj",
    "mt_linear",
    "m0",
    "mt_coeff",
    "prefactor",
    "L",
]


@dataclass(frozen=True)
class MaskRow:
    mask: int
    target_bit: int


def popcount(n: int) -> int:
    return bin(n).count("1")


def combo_name(mask: int) -> str:
    names = [BASIS[i] for i in range(len(BASIS)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def rows_to_masks(rows: list[QuotientRow], p: int) -> tuple[list[MaskRow], Counter]:
    out: list[MaskRow] = []
    stats: Counter = Counter()
    for row in rows:
        vals = feature_values(row.x, row.w, p)
        mask = 0
        skip = False
        for i, name in enumerate(BASIS):
            chi = legendre(vals[name], p)
            if chi == 0:
                stats[f"zero_{name}"] += 1
                skip = True
                break
            if chi == -1:
                mask |= 1 << i
        if skip:
            stats["zero_feature_skips"] += 1
            continue
        target_bit = 0 if row.target == 1 else 1
        out.append(MaskRow(mask=mask, target_bit=target_bit))
    stats["usable_rows"] = len(out)
    stats["input_rows"] = len(rows)
    return out, stats


def score_combo(rows: list[MaskRow], combo: int, polarity: int) -> int:
    # polarity = +1 tests product == target; -1 tests product == -target.
    flip = 0 if polarity == 1 else 1
    return sum(((popcount(row.mask & combo) & 1) ^ flip) == row.target_bit for row in rows)


def screen_basis(rows: list[MaskRow], limit: int = 12) -> tuple[Counter, list[tuple[int, int, int, int]]]:
    stats: Counter = Counter()
    total = len(rows)
    best: list[tuple[int, int, int, int]] = []
    exact = 0
    for combo in range(1 << len(BASIS)):
        good_plus = score_combo(rows, combo, 1)
        good_minus = score_combo(rows, combo, -1)
        if good_plus >= good_minus:
            good, polarity = good_plus, 1
        else:
            good, polarity = good_minus, -1
        if good == total:
            exact += 1
        best.append((good, -popcount(combo), polarity, combo))
    best.sort(reverse=True)
    stats["rows"] = total
    stats["basis_size"] = len(BASIS)
    stats["combos_tested"] = 1 << len(BASIS)
    stats["exact_combos"] = exact
    stats["best_good"] = best[0][0] if best else 0
    stats["best_weight"] = -best[0][1] if best else 0
    stats["best_polarity"] = best[0][2] if best else 0
    return stats, best[:limit]


def evaluate_combos(rows: list[MaskRow], combos: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    for _, neg_weight, polarity, combo in combos:
        out.append((score_combo(rows, combo, polarity), neg_weight, polarity, combo))
    out.sort(reverse=True)
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_combos(prefix: str, rows: list[tuple[int, int, int, int]], total: int) -> None:
    print(f"{prefix}:")
    for good, neg_weight, polarity, combo in rows:
        rate = good / total if total else 0.0
        print(
            f"  good={good}/{total} rate={rate:.9f} "
            f"weight={-neg_weight} polarity={polarity} combo={combo_name(combo)}"
        )


def run_dataset(label: str, d3_rows: list[QuotientRow], d4_rows: list[QuotientRow], p: int) -> dict[str, object]:
    print(f"{label}:")
    print(f"  p = {p}")
    print(f"  d3_rows = {len(d3_rows)}")
    print(f"  d4_rows_after_d3 = {len(d4_rows)}")
    d3_masks, d3_mask_stats = rows_to_masks(d3_rows, p)
    d4_masks, d4_mask_stats = rows_to_masks(d4_rows, p)
    print_counter(f"{label}_d3_mask_stats", d3_mask_stats)
    print_counter(f"{label}_d4_mask_stats", d4_mask_stats)
    d3_stats, d3_best = screen_basis(d3_masks)
    d4_stats, d4_best = screen_basis(d4_masks)
    print_counter(f"{label}_d3_basis_screen", d3_stats)
    print_combos(f"{label}_d3_best_combos", d3_best, d3_stats["rows"])
    print_counter(f"{label}_d4_basis_screen", d4_stats)
    print_combos(f"{label}_d4_best_combos", d4_best, d4_stats["rows"])
    return {
        "d3_masks": d3_masks,
        "d4_masks": d4_masks,
        "d3_best": d3_best,
        "d4_best": d4_best,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--heldout-target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--small-primes", default="1087,1471,1607")
    args = parser.parse_args()

    print("p27 E-quotient Kummer/theta basis probe")
    print("basis = " + ", ".join(BASIS))

    d3_train, d4_train, train_stats = p27_rows(args.target, args.seed, args.max_draws)
    print_counter("p27_train_quotient_stats", train_stats)
    train = run_dataset("p27_train", d3_train, d4_train, P)

    d3_hold, d4_hold, hold_stats = p27_rows(args.heldout_target, args.heldout_seed, args.max_draws)
    print_counter("p27_heldout_quotient_stats", hold_stats)
    heldout = run_dataset("p27_heldout", d3_hold, d4_hold, P)

    print("p27_train_best_on_heldout:")
    print_combos(
        "  d3_train_best_eval",
        evaluate_combos(heldout["d3_masks"], train["d3_best"]),
        len(heldout["d3_masks"]),
    )
    print_combos(
        "  d4_train_best_eval",
        evaluate_combos(heldout["d4_masks"], train["d4_best"]),
        len(heldout["d4_masks"]),
    )

    print("small_prime_basis_screens:")
    for prime in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_stats", qstats)
        run_dataset(f"q{prime}", d3_rows, d4_rows, prime)

    print("p27_equotient_kummer_basis_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
