#!/usr/bin/env python3
"""Beta-sequence complexity for marginal exterior determinants.

The origin-product package uses values

    a_beta = P(Omega_beta)

for beta-shifted multiplication by theta^(-beta).  This script checks whether
the beta sequence has a short recurrence or simple Frobenius compression on
small tensor-factor rows.
"""

from __future__ import annotations

import argparse

import sympy as sp

from tensor_factor_marginal_origin_action_audit import (
    determinant_rows_for_case,
    find_case,
    product,
)


def bm_linear_complexity_extension(sequence, field) -> int:
    if not sequence:
        return 0
    c = [field.one]
    b = [field.one]
    linear_complexity = 0
    m = 1
    last_discrepancy = field.one
    for n, value in enumerate(sequence):
        discrepancy = value
        for i in range(1, linear_complexity + 1):
            discrepancy = field.add(
                discrepancy,
                field.mul(c[i], sequence[n - i]),
            )
        if discrepancy == field.zero:
            m += 1
            continue
        old_c = c[:]
        scale = field.div(discrepancy, last_discrepancy)
        if len(c) < len(b) + m:
            c.extend(field.zero for _ in range(len(b) + m - len(c)))
        for j, coeff in enumerate(b):
            c[j + m] = field.sub(c[j + m], field.mul(scale, coeff))
        if 2 * linear_complexity <= n:
            linear_complexity = n + 1 - linear_complexity
            b = old_c
            last_discrepancy = discrepancy
            m = 1
        else:
            m += 1
    return linear_complexity


def additive_period(sequence) -> int:
    n = len(sequence)
    for period in range(1, n + 1):
        if n % period:
            continue
        if all(sequence[i] == sequence[(i + period) % n] for i in range(n)):
            return period
    return n


def frobenius_match_counts(sequence, q: int, extension_degree: int, field):
    n = len(sequence)
    q_mult = q % n
    Q_mult = pow(q, extension_degree, n)
    q_matches = 0
    Q_matches = 0
    for beta, value in enumerate(sequence):
        if sequence[(q_mult * beta) % n] == field.pow(value, q):
            q_matches += 1
        if sequence[(Q_mult * beta) % n] == value:
            Q_matches += 1
    return q_mult, Q_mult, q_matches, Q_matches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=3)
    parser.add_argument("--windows", type=int, default=2)
    parser.add_argument("--target", default="full")
    parser.add_argument("--without-constant", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    n = len(cycle) // m
    extension_degree, tensor_factor_degree, field_degree, field, dets = determinant_rows_for_case(
        q,
        cycle,
        m,
        factor,
        args.seed,
        args.subdegree,
        args.windows,
        args.target,
        not args.without_constant,
    )
    by_beta = {row.beta: row.det for row in dets if row.alpha == 0}
    if len(by_beta) != n:
        raise RuntimeError(f"expected {n} alpha=0 beta values, got {len(by_beta)}")
    sequence = [by_beta[beta] for beta in range(n)]
    bm = bm_linear_complexity_extension(sequence * 2, field)
    q_mult, Q_mult, q_matches, Q_matches = frobenius_match_counts(
        sequence,
        q,
        extension_degree,
        field,
    )

    print("tensor factor marginal beta-sequence complexity")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={len(cycle)}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"factor_degree={factor.degree()}")
    print(f"extension_degree={extension_degree}")
    print(f"tensor_factor_degree={tensor_factor_degree}")
    print(f"subdegree={args.subdegree}")
    print(f"windows={args.windows}")
    print(f"target={args.target}")
    print(f"include_constant={int(not args.without_constant)}")
    print(f"field_tuple_degree={field_degree}")
    print()
    print("beta_sequence")
    print(f"  distinct_values={len(set(sequence))}")
    print(f"  zero_count={sum(1 for value in sequence if value == field.zero)}")
    print(f"  additive_period={additive_period(sequence)}")
    print(f"  bm_complexity={bm}")
    print(f"  bm_over_n={bm / n:.6f}")
    print(f"  product={product(sequence, field)}")
    print()
    print("frobenius_tests")
    print(f"  q_mod_n={q_mult}")
    print(f"  Q_mod_n=q^extension_degree_mod_n={Q_mult}")
    print(f"  q_frobenius_matches={q_matches}/{n}")
    print(f"  Q_invariance_matches={Q_matches}/{n}")
    print()
    print("interpretation")
    print("  low_bm_or_short_period_would_support_beta_product_compression=1")
    print("  q_frobenius_matches_would_support_base_field_norm_packaging=1")
    print("  Q_invariance_matches_would_support_tensor_factor_orbit_compression=1")
    print("conclusion=reported_tensor_factor_marginal_beta_complexity")


if __name__ == "__main__":
    main()
