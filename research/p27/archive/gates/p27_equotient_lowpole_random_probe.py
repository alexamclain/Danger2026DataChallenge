#!/usr/bin/env python3
"""Low-pole random E-function screen for p27 d3/d4.

The named Kummer basis did not explain the descended E-level bits.  This probe
tests a broader but still structured extraction proxy: small-integer sections
of L(nO) on E: W^2=X^3-X, and products of two such sections, which model
quadratic characters of low-pole rational functions.

It is not a proof of nonexistence.  It is a bounded falsifier for the next
most plausible "small explicit f3/f4" route before full Magma/Sage function
field elimination.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from dataclasses import dataclass

from p27_label2_alpha_branch_recurrence_probe import P, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    p27_rows,
    quotient_bit_rows_from_candidates,
)


@dataclass(frozen=True)
class Section:
    name: str
    x_power: int
    has_w: bool


@dataclass(frozen=True)
class Candidate:
    good: int
    zeros: int
    polarity: int
    coeffs_a: tuple[int, ...]
    coeffs_b: tuple[int, ...] | None
    pole_bound: int
    mode: str


def rr_basis(pole_bound: int) -> list[Section]:
    basis: list[Section] = []
    max_x = pole_bound // 2
    for i in range(max_x + 1):
        basis.append(Section("1" if i == 0 else f"X^{i}", i, False))
    max_xw = (pole_bound - 3) // 2
    for i in range(max_xw + 1):
        basis.append(Section("W" if i == 0 else f"X^{i}W", i, True))
    return basis


def section_values(rows: list[QuotientRow], p: int, basis: list[Section]) -> list[list[int]]:
    values: list[list[int]] = []
    for row in rows:
        x_pows = [1]
        for _ in range(1, max(section.x_power for section in basis) + 1):
            x_pows.append(x_pows[-1] * row.x % p)
        vals = []
        for section in basis:
            value = x_pows[section.x_power]
            if section.has_w:
                value = value * row.w % p
            vals.append(value)
        values.append(vals)
    return values


def random_coeffs(rng: random.Random, dim: int, coeff_bound: int) -> tuple[int, ...]:
    while True:
        coeffs = tuple(rng.randint(-coeff_bound, coeff_bound) for _ in range(dim))
        if any(coeffs):
            return coeffs


def eval_section(vals: list[int], coeffs: tuple[int, ...], p: int) -> int:
    acc = 0
    for coeff, value in zip(coeffs, vals):
        if coeff:
            acc = (acc + coeff * value) % p
    return acc


def target_bits(rows: list[QuotientRow]) -> list[int]:
    return [0 if row.target == 1 else 1 for row in rows]


def score_candidate(
    values: list[list[int]],
    targets: list[int],
    p: int,
    coeffs_a: tuple[int, ...],
    coeffs_b: tuple[int, ...] | None,
) -> tuple[int, int, int]:
    good_plus = 0
    good_minus = 0
    zeros = 0
    for vals, target in zip(values, targets):
        a = eval_section(vals, coeffs_a, p)
        chi_a = legendre(a, p)
        if chi_a == 0:
            zeros += 1
            continue
        chi = chi_a
        if coeffs_b is not None:
            b = eval_section(vals, coeffs_b, p)
            chi_b = legendre(b, p)
            if chi_b == 0:
                zeros += 1
                continue
            chi *= chi_b
        bit = 0 if chi == 1 else 1
        if bit == target:
            good_plus += 1
        else:
            good_minus += 1
    if good_plus >= good_minus:
        return good_plus, zeros, 1
    return good_minus, zeros, -1


def insert_best(best: list[Candidate], candidate: Candidate, limit: int) -> None:
    best.append(candidate)
    best.sort(key=lambda item: (item.good, -item.zeros, -sum(abs(c) for c in item.coeffs_a)), reverse=True)
    del best[limit:]


def coeffs_name(coeffs: tuple[int, ...], basis: list[Section]) -> str:
    terms = []
    for coeff, section in zip(coeffs, basis):
        if coeff == 0:
            continue
        terms.append(f"{coeff}*{section.name}")
    return " + ".join(terms) if terms else "0"


def candidate_name(candidate: Candidate, basis: list[Section]) -> str:
    left = coeffs_name(candidate.coeffs_a, basis)
    if candidate.coeffs_b is None:
        return left
    return f"({left}) * ({coeffs_name(candidate.coeffs_b, basis)})"


def random_screen(
    rows: list[QuotientRow],
    p: int,
    pole_bound: int,
    trials: int,
    coeff_bound: int,
    seed: int,
    include_products: bool,
    limit: int = 8,
) -> tuple[Counter, list[Candidate], list[Section]]:
    basis = rr_basis(pole_bound)
    values = section_values(rows, p, basis)
    targets = target_bits(rows)
    rng = random.Random(seed)
    best: list[Candidate] = []
    exact = 0
    for i in range(trials):
        coeffs_a = random_coeffs(rng, len(basis), coeff_bound)
        coeffs_b = None
        mode = "section"
        if include_products and i % 2 == 1:
            coeffs_b = random_coeffs(rng, len(basis), coeff_bound)
            mode = "product"
        good, zeros, polarity = score_candidate(values, targets, p, coeffs_a, coeffs_b)
        if good + zeros == len(rows) and zeros == 0:
            exact += 1
        insert_best(
            best,
            Candidate(good, zeros, polarity, coeffs_a, coeffs_b, pole_bound, mode),
            limit,
        )
    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["basis_dim"] = len(basis)
    stats["pole_bound"] = pole_bound
    stats["trials"] = trials
    stats["coeff_bound"] = coeff_bound
    stats["exact_candidates"] = exact
    stats["best_good"] = best[0].good if best else 0
    stats["best_zeros"] = best[0].zeros if best else 0
    stats["best_polarity"] = best[0].polarity if best else 0
    return stats, best, basis


def evaluate_candidates(
    rows: list[QuotientRow],
    p: int,
    basis: list[Section],
    candidates: list[Candidate],
) -> list[Candidate]:
    values = section_values(rows, p, basis)
    targets = target_bits(rows)
    out = []
    for candidate in candidates:
        good, zeros, polarity = score_candidate(
            values, targets, p, candidate.coeffs_a, candidate.coeffs_b
        )
        out.append(
            Candidate(
                good,
                zeros,
                polarity,
                candidate.coeffs_a,
                candidate.coeffs_b,
                candidate.pole_bound,
                candidate.mode,
            )
        )
    out.sort(key=lambda item: (item.good, -item.zeros), reverse=True)
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_candidates(prefix: str, candidates: list[Candidate], basis: list[Section], total: int) -> None:
    print(f"{prefix}:")
    for candidate in candidates:
        rate = candidate.good / total if total else 0.0
        print(
            f"  good={candidate.good}/{total} rate={rate:.9f} zeros={candidate.zeros} "
            f"polarity={candidate.polarity} mode={candidate.mode} "
            f"expr={candidate_name(candidate, basis)}"
        )


def run_family(
    label: str,
    rows: list[QuotientRow],
    heldout_rows: list[QuotientRow],
    p: int,
    pole_bounds: list[int],
    trials: int,
    coeff_bound: int,
    seed: int,
) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    print(f"  heldout_rows = {len(heldout_rows)}")
    for pole_bound in pole_bounds:
        stats, best, basis = random_screen(
            rows,
            p,
            pole_bound,
            trials,
            coeff_bound,
            seed + pole_bound,
            include_products=True,
        )
        print_counter(f"{label}_pole{pole_bound}_train", stats)
        print_candidates(f"{label}_pole{pole_bound}_train_best", best, basis, len(rows))
        heldout = evaluate_candidates(heldout_rows, p, basis, best)
        print_candidates(f"{label}_pole{pole_bound}_heldout_eval", heldout, basis, len(heldout_rows))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--heldout-target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--pole-bounds", default="5,7,9")
    parser.add_argument("--trials", type=int, default=2000)
    parser.add_argument("--coeff-bound", type=int, default=3)
    parser.add_argument("--small-primes", default="1087,1471")
    args = parser.parse_args()

    print("p27 E-quotient low-pole random function probe")
    print(f"trials_per_pole = {args.trials}")
    print(f"coeff_bound = {args.coeff_bound}")
    pole_bounds = [int(part) for part in args.pole_bounds.split(",") if part.strip()]

    d3_train, d4_train, train_stats = p27_rows(args.target, args.seed, args.max_draws)
    d3_hold, d4_hold, heldout_stats = p27_rows(args.heldout_target, args.heldout_seed, args.max_draws)
    print_counter("p27_train_quotient_stats", train_stats)
    print_counter("p27_heldout_quotient_stats", heldout_stats)
    run_family("p27_d3", d3_train, d3_hold, P, pole_bounds, args.trials, args.coeff_bound, args.seed)
    run_family("p27_d4", d4_train, d4_hold, P, pole_bounds, args.trials, args.coeff_bound, args.seed + 17)

    print("small_prime_lowpole_screens:")
    for prime in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_stats", qstats)
        run_family(f"q{prime}_d3", d3_rows, d3_rows, prime, pole_bounds, args.trials, args.coeff_bound, args.seed)
        run_family(f"q{prime}_d4", d4_rows, d4_rows, prime, pole_bounds, args.trials, args.coeff_bound, args.seed + 17)

    print("p27_equotient_lowpole_random_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
