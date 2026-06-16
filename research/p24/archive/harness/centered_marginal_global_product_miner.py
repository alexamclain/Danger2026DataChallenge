#!/usr/bin/env python3
"""Global-product miner for centered marginal determinant sequences.

The centered cyclic-resultant route can use one scalar

    Pi_C,right = product_t Delta_C(t)

instead of the full right-phase vector.  This script tests whether that scalar
has a tiny product formula in the elementary right-binomial unit dictionary.

Constants are intentionally excluded by default: since gcd(right,q-1)=1 in
the pinned rows, constant units can make scalar logs artificially trivial.
Low-weight scalar matches without vector matches are weak evidence; they can
suggest a possible global `Psi_all`, but not an orbit-wise divisor identity.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, product

import sympy as sp

from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import scan
from centered_marginal_phase_unit_span_scan import (
    discrete_log_table,
    log_vector,
)
from trace_gcd_chow_phase_coordinate_scan import product_mod
from trace_gcd_chow_phase_divisor_span_scan import (
    UnitVector,
    right_binomial_units,
)


@dataclass(frozen=True)
class Feature:
    name: str
    values: tuple[int, ...]
    vector_log: tuple[int, ...]
    scalar_log: int
    scalar_value: int


@dataclass(frozen=True)
class Match:
    terms: tuple[tuple[str, int], ...]


def dedupe_units(units: list[UnitVector]) -> list[UnitVector]:
    seen: set[tuple[int, ...]] = set()
    out: list[UnitVector] = []
    for unit in units:
        if unit.values in seen:
            continue
        seen.add(unit.values)
        out.append(unit)
    return out


def build_features(units: list[UnitVector], logs: dict[int, int], q: int) -> list[Feature]:
    features: list[Feature] = []
    for unit in units:
        vector = tuple(log_vector(unit.values, logs, q))
        features.append(
            Feature(
                name=unit.name,
                values=unit.values,
                vector_log=vector,
                scalar_log=sum(vector) % (q - 1),
                scalar_value=product_mod(list(unit.values), q),
            )
        )
    return features


def low_weight_scalar_matches(
    features: list[Feature],
    target_log: int,
    modulus: int,
    max_features: int,
    max_terms: int,
    exponent_bound: int,
    limit: int,
) -> list[Match]:
    selected = features[:max_features]
    exponents = [e for e in range(-exponent_bound, exponent_bound + 1) if e != 0]
    matches: list[Match] = []
    for term_count in range(1, max_terms + 1):
        for indices in combinations(range(len(selected)), term_count):
            for powers in product(exponents, repeat=term_count):
                total = sum(
                    powers[i] * selected[index].scalar_log
                    for i, index in enumerate(indices)
                )
                if total % modulus == target_log % modulus:
                    matches.append(
                        Match(
                            tuple(
                                (selected[index].name, powers[i])
                                for i, index in enumerate(indices)
                            )
                        )
                    )
                    if len(matches) >= limit:
                        return matches
    return matches


def low_weight_vector_matches(
    features: list[Feature],
    target_vector: tuple[int, ...],
    modulus: int,
    max_features: int,
    max_terms: int,
    exponent_bound: int,
    limit: int,
) -> list[Match]:
    selected = features[:max_features]
    exponents = [e for e in range(-exponent_bound, exponent_bound + 1) if e != 0]
    width = len(target_vector)
    matches: list[Match] = []
    for term_count in range(1, max_terms + 1):
        for indices in combinations(range(len(selected)), term_count):
            for powers in product(exponents, repeat=term_count):
                total = [0 for _ in range(width)]
                for i, index in enumerate(indices):
                    power = powers[i]
                    for col, value in enumerate(selected[index].vector_log):
                        total[col] = (total[col] + power * value) % modulus
                if tuple(total) == tuple(value % modulus for value in target_vector):
                    matches.append(
                        Match(
                            tuple(
                                (selected[index].name, powers[i])
                                for i, index in enumerate(indices)
                            )
                        )
                    )
                    if len(matches) >= limit:
                        return matches
    return matches


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
    parser.add_argument("--max-binomial-constant", type=int, default=20)
    parser.add_argument("--max-formula-features", type=int, default=32)
    parser.add_argument("--max-combo-terms", type=int, default=2)
    parser.add_argument("--exponent-bound", type=int, default=4)
    parser.add_argument("--match-limit", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered marginal row found")
    sequence = normalized_right_sequence(row)
    if any(value == 0 for value in sequence):
        raise SystemExit("target has zero determinant value; logs unavailable")
    generator, logs = discrete_log_table(row.q)
    units = dedupe_units(
        right_binomial_units(
            row.q,
            row.right,
            args.max_binomial_constant,
            args.seed,
        )
    )
    features = build_features(units, logs, row.q)
    target_vector_log = tuple(log_vector(sequence, logs, row.q))
    target_scalar_value = product_mod(sequence, row.q)
    target_scalar_log = logs[target_scalar_value]
    modulus = row.q - 1
    scalar_matches = low_weight_scalar_matches(
        features,
        target_scalar_log,
        modulus,
        args.max_formula_features,
        args.max_combo_terms,
        args.exponent_bound,
        args.match_limit,
    )
    vector_matches = low_weight_vector_matches(
        features,
        target_vector_log,
        modulus,
        args.max_formula_features,
        args.max_combo_terms,
        args.exponent_bound,
        args.match_limit,
    )

    print("Centered marginal global-product miner")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"gcd_right_q_minus_1={sp.gcd(row.right, row.q - 1)}")
    print(f"q_minus_1_factorization={sp.factorint(row.q - 1)}")
    print(f"log_generator={generator}")
    print(f"target_values={sequence}")
    print(f"target_scalar_value={target_scalar_value}")
    print(f"target_scalar_log={target_scalar_log}")
    print(f"unit_dictionary_size={len(units)}")
    print(f"feature_prefix={[feature.name for feature in features[:12]]}")
    print(f"max_formula_features={args.max_formula_features}")
    print(f"max_combo_terms={args.max_combo_terms}")
    print(f"exponent_bound={args.exponent_bound}")
    print(f"scalar_match_count={len(scalar_matches)}")
    for match in scalar_matches:
        print(f"  scalar_match={match.terms}")
    print(f"vector_match_count={len(vector_matches)}")
    for match in vector_matches:
        print(f"  vector_match={match.terms}")
    print()
    print("interpretation")
    print("  scalar_only_match_is_weak_without_vector_or_divisor_identity=1")
    print("  no_low_weight_scalar_match_demotes_simple_global_product_formula=1")
    print("  vector_match_would_suggest_orbitwise_phase_formula=1")
    print("conclusion=reported_centered_marginal_global_product_miner")


if __name__ == "__main__":
    main()
