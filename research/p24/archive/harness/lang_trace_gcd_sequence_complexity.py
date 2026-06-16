#!/usr/bin/env python3
"""Linear-complexity probe for the trace-gcd origin determinant sequence.

After origin covariance, the p24 proof target is a right-component sequence

    Delta_i(t),  t mod 211.

If this sequence has low linear complexity in small actual-CM rows, then the
211-factor product might admit a shorter recurrence/resultant certificate.
If it has full complexity, the product should be treated as a genuine
right-cycle norm unless a new CM identity is found.
"""

from __future__ import annotations

import argparse

import sympy as sp

from centered_marginal_alpha_sequence_complexity import berlekamp_massey
from lang_trace_gcd_origin_action_audit import (
    OriginDet,
    cyclic_period,
    first_row,
    product_mod,
)


def values_for_fixed_beta(records: list[OriginDet], beta: int) -> list[int | None]:
    by_alpha = {record.alpha: record.determinant for record in records if record.beta == beta}
    return [by_alpha[alpha] for alpha in range(len(by_alpha))]


def reduced_right_sequence(
    records: list[OriginDet], right: int
) -> tuple[list[int | None], int]:
    by_right: dict[int, int | None] = {}
    mismatches = 0
    for record in records:
        key = record.alpha % right
        if key in by_right and by_right[key] != record.determinant:
            mismatches += 1
        by_right.setdefault(key, record.determinant)
    return [by_right[t] for t in range(right)], mismatches


def nonnull_ints(values: list[int | None]) -> list[int]:
    if any(value is None for value in values):
        raise ValueError("sequence has missing determinant values")
    return [int(value) for value in values]


def bm_connection(sequence: list[int], q: int) -> list[int]:
    """Return delay-form connection [1,c1,...,cL]."""
    c = [1]
    b = [1]
    length = 0
    shift = 1
    last_discrepancy = 1
    for n, value in enumerate(sequence):
        discrepancy = value % q
        for i in range(1, length + 1):
            discrepancy = (discrepancy + c[i] * sequence[n - i]) % q
        if discrepancy == 0:
            shift += 1
            continue
        old = c[:]
        scale = discrepancy * pow(last_discrepancy, -1, q) % q
        if len(c) < len(b) + shift:
            c.extend([0] * (len(b) + shift - len(c)))
        for j, coeff in enumerate(b):
            c[j + shift] = (c[j + shift] - scale * coeff) % q
        if 2 * length <= n:
            length = n + 1 - length
            b = old
            last_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1
    return [coeff % q for coeff in c[: length + 1]]


def verify_connection(sequence: list[int], connection: list[int], q: int) -> int:
    failures = 0
    order = len(connection) - 1
    for n in range(order, len(sequence)):
        total = sequence[n] % q
        for i in range(1, order + 1):
            total = (total + connection[i] * sequence[n - i]) % q
        if total:
            failures += 1
    return failures


def connection_polynomial_summary(connection: list[int], period: int, q: int) -> tuple[list[int], bool, str]:
    x = sp.symbols("x")
    degree = len(connection) - 1
    poly = sp.Poly(
        sum(connection[i] * x ** (degree - i) for i in range(degree + 1)),
        x,
        modulus=q,
    )
    period_poly = sp.Poly(x**period - 1, x, modulus=q)
    divides_period = period_poly.rem(poly).is_zero
    factorization = str(sp.factor_list(poly, modulus=q))
    return [int(coeff) % q for coeff in poly.all_coeffs()], divides_period, factorization


def print_sequence_summary(label: str, values: list[int | None], q: int) -> None:
    seq = nonnull_ints(values)
    doubled = seq + seq
    complexity = berlekamp_massey(doubled, q)
    connection = bm_connection(doubled, q)
    failures = verify_connection(doubled, connection, q)
    poly_coeffs, divides_period, factorization = connection_polynomial_summary(
        connection, len(seq), q
    )
    print(f"{label}_length={len(seq)}")
    print(f"{label}_zero_count={sum(1 for value in seq if value == 0)}")
    print(f"{label}_distinct_count={len(set(seq))}")
    print(f"{label}_product_mod_q={product_mod(seq, q)}")
    print(f"{label}_linear_complexity_two_periods={complexity}")
    print(f"{label}_complexity_ratio={complexity}/{len(seq)}")
    print(f"{label}_connection={connection}")
    print(f"{label}_connection_failures={failures}")
    print(f"{label}_connection_poly_coeffs={poly_coeffs}")
    print(f"{label}_connection_divides_xn_minus_1={int(divides_period)}")
    print(f"{label}_connection_factorization={factorization}")
    print(f"{label}_values_prefix={seq[:40]}")


def frobenius_compatibility_mismatches(
    values: list[int | None], q_mod_right: int, right: int
) -> int:
    seq = nonnull_ints(values)
    return sum(
        1
        for t, value in enumerate(seq)
        if seq[(q_mod_right * t) % right] != value
    )


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
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_row(args)
    if row is None:
        raise SystemExit("no eligible trace-gcd sequence row found")

    print("Lang trace-gcd determinant sequence complexity")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit={row.left_orbit_rep}:L{row.left_orbit_len}")
    print(f"right_lengths={list(row.right_orbit_lengths)}")

    by_omitted: dict[int, list[OriginDet]] = {}
    for record in row.records:
        by_omitted.setdefault(record.omitted, []).append(record)

    for omitted, records in sorted(by_omitted.items()):
        print()
        print(f"omitted={omitted}")
        beta0_values = values_for_fixed_beta(records, beta=0)
        alpha_period = cyclic_period(beta0_values)
        print(f"alpha_period_on_beta0={alpha_period}")
        if alpha_period is not None:
            print_sequence_summary(
                "period_sequence", beta0_values[:alpha_period], row.q
            )
        right_values, right_mismatches = reduced_right_sequence(records, row.right)
        print(f"right_class_mismatches={right_mismatches}")
        if right_mismatches == 0:
            print_sequence_summary("right_sequence", right_values, row.q)
            print(
                "right_sequence_frobenius_compatibility_mismatches="
                f"{frobenius_compatibility_mismatches(right_values, row.q % row.right, row.right)}"
            )

    print()
    print("interpretation")
    print("  low_complexity_would_support_short_recurrence_resultant=1")
    print("  full_complexity_points_to_genuine_right_cycle_norm=1")
    print("conclusion=reported_lang_trace_gcd_sequence_complexity")


if __name__ == "__main__":
    main()
