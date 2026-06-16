#!/usr/bin/env python3
"""Unit-span scan for centered marginal right determinant sequences.

This is a bounded recognition test for the simplest possible phase-aware
product formula for

    Delta_C(t), t mod right.

It builds right-cyclotomic norm units

    Norm_{F_q(mu_right)/F_q}(1 - c*zeta_right^(k*t))

constant units, and optional Heegner-fiber units.  It converts them and the
centered determinant sequence to discrete-log vectors modulo the prime factors
of q-1, and asks whether the target lies in the span before the dictionary
becomes the whole ambient space.

This is a falsifier, not a proof.  A sparse non-full-rank containment would
suggest a candidate phase-aware `Psi`; full-rank containment is just
interpolation in multiplicative clothing.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import random

import sympy as sp

from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import scan
from trace_gcd_chow_phase_divisor_span_scan import (
    UnitVector,
    contains_mod_prime,
    rank_mod_prime,
    right_binomial_units,
)
from phase_divisor_heegner_support_scan import heegner_roots


@dataclass(frozen=True)
class SpanResult:
    prime: int
    dictionary_rank: int
    target_in_span: bool
    first_containment_index: int | None
    first_containment_rank: int
    first_containment_random_rate: float
    random_containment_rate: float


def discrete_log_table(q: int) -> tuple[int, dict[int, int]]:
    generator = int(sp.primitive_root(q))
    table: dict[int, int] = {}
    value = 1
    for exponent in range(q - 1):
        table[value] = exponent
        value = value * generator % q
    if len(table) != q - 1:
        raise RuntimeError("primitive root table did not cover F_q^*")
    return generator, table


def log_vector(values: list[int] | tuple[int, ...], table: dict[int, int], q: int) -> list[int]:
    out: list[int] = []
    for value in values:
        value %= q
        if value == 0:
            raise ValueError("cannot take log of zero")
        out.append(table[value])
    return out


def constant_units(q: int, right: int, max_constant: int) -> list[UnitVector]:
    return [
        UnitVector(f"constant:c={c}", tuple([c % q for _ in range(right)]))
        for c in range(2, min(q, max_constant + 1))
    ]


def heegner_fiber_units(row, max_abs_D: int, max_h: int) -> list[UnitVector]:
    heegner = heegner_roots(row.q, max_abs_D, max_h)
    roots = sorted({root for roots in heegner.values() for root in roots})
    shifts_by_right: dict[int, list[int]] = defaultdict(list)
    for alpha in range(row.m):
        for beta in range(row.n):
            shift = (row.n * alpha + row.m * beta) % row.h
            shifts_by_right[alpha % row.right].append(shift)

    units: list[UnitVector] = []
    for root in roots:
        values: list[int] = []
        ok = True
        for t in range(row.right):
            product = 1
            for shift in shifts_by_right[t]:
                factor = (row.cycle[shift] - root) % row.q
                if factor == 0:
                    ok = False
                    break
                product = product * factor % row.q
            if not ok:
                break
            values.append(product)
        if ok:
            units.append(UnitVector(f"heegner_fiber:root={root}", tuple(values)))
    return units


def dedupe_units(units: list[UnitVector]) -> list[UnitVector]:
    seen: set[tuple[int, ...]] = set()
    out: list[UnitVector] = []
    for unit in units:
        if unit.values in seen:
            continue
        seen.add(unit.values)
        out.append(unit)
    return out


def first_containment_index(
    rows: list[list[int]],
    target: list[int],
    prime: int,
) -> tuple[int | None, int]:
    current: list[list[int]] = []
    current_rank = 0
    for index, row in enumerate(rows, start=1):
        current.append(row)
        current_rank = rank_mod_prime(current, prime)
        if contains_mod_prime(current, target, prime):
            return index, current_rank
    return None, current_rank


def random_containment_rate(
    rows: list[list[int]],
    length: int,
    prime: int,
    trials: int,
    rng: random.Random,
) -> float:
    if trials <= 0:
        return float("nan")
    hits = 0
    for _ in range(trials):
        target = [rng.randrange(prime) for _ in range(length)]
        hits += int(contains_mod_prime(rows, target, prime))
    return hits / trials


def span_results(
    unit_logs: list[list[int]],
    target_log: list[int],
    factors: list[int],
    random_controls: int,
    seed: int,
) -> list[SpanResult]:
    rng = random.Random(seed)
    out: list[SpanResult] = []
    for prime in factors:
        rows_mod = [[value % prime for value in vector] for vector in unit_logs]
        target_mod = [value % prime for value in target_log]
        first_index, first_rank = first_containment_index(rows_mod, target_mod, prime)
        if first_index is None:
            first_random_rate = float("nan")
        else:
            first_random_rate = random_containment_rate(
                rows_mod[:first_index],
                len(target_log),
                prime,
                random_controls,
                rng,
            )
        out.append(
            SpanResult(
                prime=prime,
                dictionary_rank=rank_mod_prime(rows_mod, prime),
                target_in_span=contains_mod_prime(rows_mod, target_mod, prime),
                first_containment_index=first_index,
                first_containment_rank=first_rank,
                first_containment_random_rate=first_random_rate,
                random_containment_rate=random_containment_rate(
                    rows_mod,
                    len(target_log),
                    prime,
                    random_controls,
                    rng,
                ),
            )
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument(
        "--unit-family",
        nargs="+",
        choices=("right-binomial", "constant", "heegner-fiber"),
        default=["right-binomial", "constant", "heegner-fiber"],
    )
    parser.add_argument("--max-binomial-constant", type=int, default=12)
    parser.add_argument("--max-constant-units", type=int, default=12)
    parser.add_argument("--max-heegner-abs-D", type=int, default=1000)
    parser.add_argument("--max-heegner-h", type=int, default=20)
    parser.add_argument("--random-controls", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered marginal row found")
    sequence = normalized_right_sequence(row)
    if any(value == 0 for value in sequence):
        raise SystemExit("target has zero determinant value; logs unavailable")
    generator, logs = discrete_log_table(row.q)
    factors = sorted(int(prime) for prime in sp.factorint(row.q - 1))
    requested = set(args.unit_family)
    units: list[UnitVector] = []
    if "right-binomial" in requested:
        units.extend(
            right_binomial_units(
                row.q,
                row.right,
                args.max_binomial_constant,
                args.seed,
            )
        )
    if "constant" in requested:
        units.extend(
            constant_units(row.q, row.right, args.max_constant_units)
        )
    if "heegner-fiber" in requested:
        units.extend(
            heegner_fiber_units(
                row,
                args.max_heegner_abs_D,
                args.max_heegner_h,
            )
        )
    units = dedupe_units(units)
    unit_logs = [log_vector(unit.values, logs, row.q) for unit in units]
    target_log = log_vector(sequence, logs, row.q)
    results = span_results(
        unit_logs,
        target_log,
        factors,
        args.random_controls,
        args.seed + row.q + row.right,
    )

    print("Centered marginal phase-unit span scan")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"log_generator={generator}")
    print(f"q_minus_1_factorization={sp.factorint(row.q - 1)}")
    print(f"unit_families={args.unit_family}")
    print(f"target_values={sequence}")
    print(f"target_logs_mod_q_minus_1={target_log}")
    print(f"unit_dictionary_size={len(units)}")
    print(f"unit_dictionary_names_prefix={[unit.name for unit in units[:16]]}")
    for result in results:
        print(f"mod_prime={result.prime}")
        print(f"  dictionary_rank={result.dictionary_rank}/{row.right}")
        print(f"  target_in_span={int(result.target_in_span)}")
        print(f"  first_containment_index={result.first_containment_index}")
        print(f"  first_containment_rank={result.first_containment_rank}")
        print(
            "  first_containment_random_rate="
            f"{result.first_containment_random_rate:.6f}"
        )
        print(f"  random_containment_rate={result.random_containment_rate:.6f}")
    print()
    print("interpretation")
    print("  sparse_nonfull_rank_containment_with_low_random_rate_would_suggest_special_product=1")
    print("  full_rank_containment_is_only_interpolation=1")
    print("  target_missing_from_nonfull_rank_components_demotes_simple_unit_dictionary=1")
    print("conclusion=reported_centered_marginal_phase_unit_span_scan")


if __name__ == "__main__":
    main()
