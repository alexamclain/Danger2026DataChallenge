#!/usr/bin/env python3
"""Global-product miner for the trace-GCD Chow determinant.

The global Chow/Borcherds route asks for one scalar

    Pi_all = product_t Delta(t)

instead of separate right-orbit products.  This script tests a danger in that
route on small actual-CM data: a one-scalar match in F_q^* is much easier than
an honest divisor identity.

For the pinned D=-13319 row, it builds the same bounded phase-unit dictionary
used by `trace_gcd_chow_phase_divisor_span_scan.py`, computes both

    phase vector logs:  (log Delta(t))_t
    global scalar log:  sum_t log Delta(t),

and asks whether low-weight products of candidate units match either object.
Scalar-only matches are reported as weak evidence unless they also match the
full phase vector.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, product

import sympy as sp

from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence
from trace_gcd_chow_phase_coordinate_scan import product_mod, values_by_omitted
from trace_gcd_chow_phase_divisor_span_scan import (
    UnitVector,
    contains_mod_prime,
    discrete_log_table,
    log_vector,
    ordered_dictionary,
    rank_mod_prime,
    right_binomial_units,
)
from trace_gcd_chow_plain_divisor_scan import first_row_with_cycle


@dataclass(frozen=True)
class LogFeature:
    name: str
    vector_logs: tuple[int, ...]
    scalar_log: int
    scalar_value: int


@dataclass(frozen=True)
class ComboMatch:
    terms: tuple[tuple[str, int], ...]


def scalar_log(value: int, logs: dict[int, int], q: int) -> int:
    value %= q
    if value == 0:
        raise ValueError("cannot take log of zero")
    return logs[value]


def constant_units(q: int, right: int, max_constant: int) -> list[UnitVector]:
    return [
        UnitVector(f"constant:c={c}", tuple([c % q for _ in range(right)]))
        for c in range(2, min(q, max_constant + 1))
    ]


def dedupe_units(units: list[UnitVector]) -> list[UnitVector]:
    seen: set[tuple[int, ...]] = set()
    out: list[UnitVector] = []
    for unit in units:
        if unit.values in seen:
            continue
        seen.add(unit.values)
        out.append(unit)
    return out


def build_features(
    units: list[UnitVector],
    logs: dict[int, int],
    q: int,
) -> list[LogFeature]:
    features: list[LogFeature] = []
    for unit in units:
        vector_logs = tuple(log_vector(unit.values, logs, q - 1))
        scalar_value = product_mod(list(unit.values), q)
        features.append(
            LogFeature(
                name=unit.name,
                vector_logs=vector_logs,
                scalar_log=sum(vector_logs) % (q - 1),
                scalar_value=scalar_value,
            )
        )
    return features


def first_containment_index_1d(
    feature_logs: list[int],
    target: int,
    prime: int,
) -> tuple[int | None, int, bool]:
    if target % prime == 0:
        return 0, 0, True
    for index, value in enumerate(feature_logs, start=1):
        if value % prime:
            return index, 1, True
    return None, 0, False


def low_weight_matches(
    features: list[LogFeature],
    target: tuple[int, ...] | int,
    modulus: int,
    max_features: int,
    max_terms: int,
    exponent_bound: int,
    limit: int,
    *,
    scalar: bool,
) -> list[ComboMatch]:
    """Search tiny signed products matching either scalar or vector logs."""
    selected = features[:max_features]
    exponents = [e for e in range(-exponent_bound, exponent_bound + 1) if e != 0]
    matches: list[ComboMatch] = []
    if scalar:
        target_scalar = int(target) % modulus
        for term_count in range(1, max_terms + 1):
            for indices in combinations(range(len(selected)), term_count):
                for powers in product(exponents, repeat=term_count):
                    total = sum(
                        powers[i] * selected[index].scalar_log
                        for i, index in enumerate(indices)
                    )
                    if total % modulus == target_scalar:
                        matches.append(
                            ComboMatch(
                                tuple(
                                    (selected[index].name, powers[i])
                                    for i, index in enumerate(indices)
                                )
                            )
                        )
                        if len(matches) >= limit:
                            return matches
    else:
        target_vector = tuple(int(value) % modulus for value in target)  # type: ignore[arg-type]
        width = len(target_vector)
        for term_count in range(1, max_terms + 1):
            for indices in combinations(range(len(selected)), term_count):
                for powers in product(exponents, repeat=term_count):
                    total = [0 for _ in range(width)]
                    for i, index in enumerate(indices):
                        logs = selected[index].vector_logs
                        power = powers[i]
                        for col, value in enumerate(logs):
                            total[col] = (total[col] + power * value) % modulus
                    if tuple(total) == target_vector:
                        matches.append(
                            ComboMatch(
                                tuple(
                                    (selected[index].name, powers[i])
                                    for i, index in enumerate(indices)
                                )
                            )
                        )
                        if len(matches) >= limit:
                            return matches
    return matches


def right_binomial_formula_mismatches(
    q: int,
    right: int,
    max_constant: int,
    seed: int,
) -> int:
    """Check product_t Norm(1-c*zeta^(k*t)) = (1-c^right)^ord_q(right)."""
    order = int(sp.n_order(q % right, right))
    units = right_binomial_units(q, right, max_constant, seed)
    mismatches = 0
    for unit in units:
        parts = dict(part.split("=", 1) for part in unit.name.split(":")[1:])
        c = int(parts["c"])
        expected = pow((1 - pow(c, right, q)) % q, order, q)
        actual = product_mod(list(unit.values), q)
        mismatches += int(actual != expected)
    return mismatches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--all-omitted", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument(
        "--unit-family",
        nargs="+",
        choices=("right-binomial", "heegner-fiber"),
        default=["right-binomial", "heegner-fiber"],
    )
    parser.add_argument("--max-binomial-constant", type=int, default=8)
    parser.add_argument("--max-heegner-abs-D", type=int, default=1000)
    parser.add_argument("--max-heegner-h", type=int, default=20)
    parser.add_argument("--max-constant-units", type=int, default=12)
    parser.add_argument("--max-formula-features", type=int, default=28)
    parser.add_argument("--max-combo-terms", type=int, default=2)
    parser.add_argument("--exponent-bound", type=int, default=3)
    parser.add_argument("--match-limit", type=int, default=5)
    args = parser.parse_args()

    bundle = first_row_with_cycle(args)
    if bundle is None:
        raise SystemExit("no eligible global-product row found")
    row = bundle.row
    generator, logs = discrete_log_table(row.q)
    factors = sorted(int(prime) for prime in sp.factorint(row.q - 1))

    units = dedupe_units(
        ordered_dictionary(args, bundle)
        + constant_units(row.q, row.right, args.max_constant_units)
    )
    features = build_features(units, logs, row.q)
    feature_scalar_values = {feature.scalar_value for feature in features}
    feature_scalar_logs = {feature.scalar_log for feature in features}

    print("trace-GCD global Chow-product miner")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"q_minus_1_factorization={sp.factorint(row.q - 1)}")
    print(f"log_generator={generator}")
    print(f"unit_families={args.unit_family}")
    print(f"unit_dictionary_size={len(units)}")
    print(f"distinct_global_products={len(feature_scalar_values)}")
    print(f"distinct_global_logs={len(feature_scalar_logs)}")
    print(f"feature_prefix={[feature.name for feature in features[:12]]}")
    print(
        "right_binomial_global_formula_mismatches="
        f"{right_binomial_formula_mismatches(row.q, row.right, args.max_binomial_constant, args.seed)}"
    )

    failures = 0
    for omitted, records in values_by_omitted(bundle).items():
        if args.only_omitted is not None and omitted != args.only_omitted:
            continue
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        if any(value == 0 for value in seq):
            failures += 1
            print(f"omitted={omitted} skipped_zero_target=1")
            continue
        target_logs = tuple(log_vector(seq, logs, row.q - 1))
        pi_all = product_mod(seq, row.q)
        pi_log = scalar_log(pi_all, logs, row.q)
        low_scalar = low_weight_matches(
            features,
            pi_log,
            row.q - 1,
            args.max_formula_features,
            args.max_combo_terms,
            args.exponent_bound,
            args.match_limit,
            scalar=True,
        )
        low_vector = low_weight_matches(
            features,
            target_logs,
            row.q - 1,
            args.max_formula_features,
            args.max_combo_terms,
            args.exponent_bound,
            args.match_limit,
            scalar=False,
        )
        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  pi_all={pi_all}")
        print(f"  pi_all_log={pi_log}")
        print(f"  target_vector_logs={list(target_logs)}")
        print(f"  low_weight_scalar_matches={low_scalar}")
        print(f"  low_weight_vector_matches={low_vector}")
        print(f"  scalar_match_without_vector_match={int(bool(low_scalar) and not low_vector)}")
        for prime in factors:
            vector_rows = [
                [value % prime for value in feature.vector_logs]
                for feature in features
            ]
            target_vector_mod = [value % prime for value in target_logs]
            vector_rank = rank_mod_prime(vector_rows, prime)
            vector_contains = contains_mod_prime(vector_rows, target_vector_mod, prime)
            scalar_rows = [[feature.scalar_log % prime] for feature in features]
            scalar_rank = rank_mod_prime(scalar_rows, prime)
            scalar_contains = contains_mod_prime(scalar_rows, [pi_log % prime], prime)
            first_index, first_rank, first_contains = first_containment_index_1d(
                [feature.scalar_log for feature in features],
                pi_log,
                prime,
            )
            print(f"  mod_prime={prime}")
            print(f"    scalar_dictionary_rank={scalar_rank}/1")
            print(f"    scalar_target_in_span={int(scalar_contains)}")
            print(f"    scalar_first_containment_index={first_index}")
            print(f"    scalar_first_containment_rank={first_rank}")
            print(f"    scalar_first_containment_success={int(first_contains)}")
            print(f"    vector_dictionary_rank={vector_rank}/{row.right}")
            print(f"    vector_target_in_span={int(vector_contains)}")

    print("interpretation")
    print("  scalar containment in one dimension is expected once any nonzero unit log appears.")
    print("  low scalar matches without vector matches are numerology, not divisor identities.")
    print("  a useful global Borcherds producer must compare divisors/local intersections,")
    print("  not merely reproduce Pi_all as an isolated element of F_q^*.")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_global_product_miner")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
