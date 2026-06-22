#!/usr/bin/env python3
"""Alpha-cover branch-class probe for p27 d3/d4.

The projective Magma smoke verifies that the order-4 alpha cover maps with
degree 4 to the residual elliptic curve E.  This probe records the next
structural consequence: for the eliminated quartic

    R^4 - 2*a*R^2 + b = 0,
    a = pref*m0,
    b = 4*pref^2*T2*S^2,

the R-discriminant has squareclass T2 on E.  Thus the visible quadratic
subcover of the cyclic-quartic alpha cover is only T^2=T2.  The script then
checks that T2 is already square on the active p27 and guard-field d3/d4 rows,
so the alpha branch discriminant is not the missing later-gate selector.
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


BRANCH_ATOMS = [
    "T2",
    "S",
    "S_conj",
    "mt_linear",
    "mt_coeff",
    "m0",
    "prefactor",
    "L",
    "X",
    "W",
    "X-1",
    "X+1",
    "X2+1",
    "X2+2X-1",
    "X2-2X-1",
]


@dataclass(frozen=True)
class MaskRow:
    mask: int
    target_bit: int


def t2_value(x: int, p: int) -> int:
    x2 = x * x % p
    return x * (x2 + 1) * (x2 + 2 * x - 1) % p


def branch_values(row: QuotientRow, p: int) -> dict[str, int]:
    vals = feature_values(row.x, row.w, p)
    vals["T2"] = t2_value(row.x, p)
    return vals


def popcount(n: int) -> int:
    return bin(n).count("1")


def combo_name(mask: int) -> str:
    names = [BRANCH_ATOMS[i] for i in range(len(BRANCH_ATOMS)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def rows_to_masks(rows: list[QuotientRow], p: int) -> tuple[list[MaskRow], Counter]:
    out: list[MaskRow] = []
    stats: Counter = Counter()
    for row in rows:
        vals = branch_values(row, p)
        mask = 0
        skip = False
        for i, name in enumerate(BRANCH_ATOMS):
            chi = legendre(vals[name], p)
            stats[f"{name}_chi_{chi}"] += 1
            if chi == 0:
                skip = True
                break
            if chi == -1:
                mask |= 1 << i
        if skip:
            stats["zero_atom_skips"] += 1
            continue
        out.append(MaskRow(mask=mask, target_bit=0 if row.target == 1 else 1))
    stats["input_rows"] = len(rows)
    stats["usable_rows"] = len(out)
    return out, stats


def score_combo(rows: list[MaskRow], combo: int, polarity: int) -> int:
    flip = 0 if polarity == 1 else 1
    return sum(((popcount(row.mask & combo) & 1) ^ flip) == row.target_bit for row in rows)


def screen(rows: list[MaskRow], top: int) -> tuple[Counter, list[tuple[int, int, int, int]]]:
    stats: Counter = Counter()
    best: list[tuple[int, int, int, int]] = []
    total = len(rows)
    exact = 0
    for combo in range(1 << len(BRANCH_ATOMS)):
        plus = score_combo(rows, combo, 1)
        minus = score_combo(rows, combo, -1)
        if plus >= minus:
            good, polarity = plus, 1
        else:
            good, polarity = minus, -1
        if good == total:
            exact += 1
        best.append((good, -popcount(combo), polarity, combo))
    best.sort(reverse=True)
    stats["rows"] = total
    stats["branch_atoms"] = len(BRANCH_ATOMS)
    stats["combos_tested"] = 1 << len(BRANCH_ATOMS)
    stats["exact_combos"] = exact
    stats["best_good"] = best[0][0] if best else 0
    stats["best_weight"] = -best[0][1] if best else 0
    stats["best_polarity"] = best[0][2] if best else 0
    return stats, best[:top]


def evaluate(rows: list[MaskRow], combos: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    for _, neg_weight, polarity, combo in combos:
        out.append((score_combo(rows, combo, polarity), neg_weight, polarity, combo))
    out.sort(reverse=True)
    return out


def print_counter(label: str, stats: Counter) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_best(label: str, rows: list[tuple[int, int, int, int]], total: int) -> None:
    print(f"{label}:")
    for good, neg_weight, polarity, combo in rows:
        rate = good / total if total else 0.0
        print(
            f"  good={good}/{total} rate={rate:.9f} "
            f"weight={-neg_weight} polarity={polarity} combo={combo_name(combo)}"
        )


def run_dataset(label: str, d3_rows: list[QuotientRow], d4_rows: list[QuotientRow], p: int, top: int) -> dict[str, object]:
    print(f"{label}:")
    print(f"  p = {p}")
    print(f"  d3_rows = {len(d3_rows)}")
    print(f"  d4_rows_after_d3 = {len(d4_rows)}")
    d3_masks, d3_mask_stats = rows_to_masks(d3_rows, p)
    d4_masks, d4_mask_stats = rows_to_masks(d4_rows, p)
    print_counter(f"{label}_d3_branch_atom_stats", d3_mask_stats)
    print_counter(f"{label}_d4_branch_atom_stats", d4_mask_stats)
    d3_stats, d3_best = screen(d3_masks, top)
    d4_stats, d4_best = screen(d4_masks, top)
    print_counter(f"{label}_d3_branch_screen", d3_stats)
    print_best(f"{label}_d3_branch_best", d3_best, d3_stats["rows"])
    print_counter(f"{label}_d4_branch_screen", d4_stats)
    print_best(f"{label}_d4_branch_best", d4_best, d4_stats["rows"])
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
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    print("p27 alpha branch-class probe")
    print("quartic = R^4 - 2*a*R^2 + b")
    print("a = prefactor*m0")
    print("b = 4*prefactor^2*T2*S^2")
    print("disc_R squareclass = T2")
    print("unique_quadratic_subcover = T^2=T2")
    print("branch_atoms = " + ", ".join(BRANCH_ATOMS))

    d3_train, d4_train, train_stats = p27_rows(args.target, args.seed, args.max_draws)
    print_counter("p27_train_quotient_stats", train_stats)
    train = run_dataset("p27_train", d3_train, d4_train, P, args.top)

    d3_hold, d4_hold, hold_stats = p27_rows(args.heldout_target, args.heldout_seed, args.max_draws)
    print_counter("p27_heldout_quotient_stats", hold_stats)
    heldout = run_dataset("p27_heldout", d3_hold, d4_hold, P, args.top)

    print("p27_train_best_on_heldout:")
    print_best(
        "  d3_branch_train_best_eval",
        evaluate(heldout["d3_masks"], train["d3_best"]),
        len(heldout["d3_masks"]),
    )
    print_best(
        "  d4_branch_train_best_eval",
        evaluate(heldout["d4_masks"], train["d4_best"]),
        len(heldout["d4_masks"]),
    )

    print("small_prime_branch_screens:")
    for prime in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_stats", qstats)
        run_dataset(f"q{prime}", d3_rows, d4_rows, prime, args.top)

    print("p27_alpha_branch_class_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
