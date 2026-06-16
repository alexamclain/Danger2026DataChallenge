#!/usr/bin/env python3
"""Linear-recurrence audit for marginal beta Plucker sequences.

If the beta values

    a_beta = P(Omega_beta)

satisfy a short recurrence, then the origin-stable product

    prod_beta a_beta

can be packaged as a recurrence/norm certificate instead of as a raw list of
all beta shifts.  This script extracts the Berlekamp-Massey connection
polynomial over the K-character coefficient field and verifies that it
regenerates the beta sequence on small tensor-factor rows.
"""

from __future__ import annotations

import argparse

from tensor_factor_marginal_origin_action_audit import (
    determinant_rows_for_case,
    find_case,
    product,
)


def bm_connection(sequence, field):
    """Return delay-form connection c with c[0]=1.

    The recurrence is:

        a_n + c[1] a_{n-1} + ... + c[L] a_{n-L} = 0.
    """
    c = [field.one]
    b = [field.one]
    linear_complexity = 0
    shift = 1
    last_discrepancy = field.one
    for n, value in enumerate(sequence):
        discrepancy = value
        for i in range(1, linear_complexity + 1):
            discrepancy = field.add(
                discrepancy,
                field.mul(c[i], sequence[n - i]),
            )
        if discrepancy == field.zero:
            shift += 1
            continue
        old_c = c[:]
        scale = field.div(discrepancy, last_discrepancy)
        if len(c) < len(b) + shift:
            c.extend(field.zero for _ in range(len(b) + shift - len(c)))
        for j, coeff in enumerate(b):
            c[j + shift] = field.sub(c[j + shift], field.mul(scale, coeff))
        if 2 * linear_complexity <= n:
            linear_complexity = n + 1 - linear_complexity
            b = old_c
            last_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1
    return c[: linear_complexity + 1]


def verify_connection(sequence, connection, field) -> int:
    failures = 0
    order = len(connection) - 1
    for n in range(order, len(sequence)):
        total = sequence[n]
        for i in range(1, order + 1):
            total = field.add(total, field.mul(connection[i], sequence[n - i]))
        if total != field.zero:
            failures += 1
    return failures


def generate_from_connection(initial, connection, count: int, field):
    order = len(connection) - 1
    if order == 0:
        return []
    out = list(initial[:order])
    while len(out) < count:
        value = field.zero
        for i in range(1, order + 1):
            value = field.sub(value, field.mul(connection[i], out[-i]))
        out.append(value)
    return out[:count]


def characteristic_coefficients(connection):
    """Return coefficients of lambda^L + c1 lambda^(L-1)+...+cL."""
    return list(connection)


def trim_poly(poly, field):
    out = poly[:]
    while out and out[-1] == field.zero:
        out.pop()
    return out or [field.zero]


def poly_divmod(numerator, denominator, field):
    numerator = trim_poly(numerator, field)
    denominator = trim_poly(denominator, field)
    if denominator == [field.zero]:
        raise ZeroDivisionError("polynomial division by zero")
    if len(numerator) < len(denominator):
        return [field.zero], numerator
    quotient = [field.zero for _ in range(len(numerator) - len(denominator) + 1)]
    remainder = numerator[:]
    den_lead_inv = field.inv(denominator[-1])
    while len(remainder) >= len(denominator) and remainder != [field.zero]:
        shift = len(remainder) - len(denominator)
        scale = field.mul(remainder[-1], den_lead_inv)
        quotient[shift] = scale
        for idx, coeff in enumerate(denominator):
            rem_idx = idx + shift
            remainder[rem_idx] = field.sub(remainder[rem_idx], field.mul(scale, coeff))
        remainder = trim_poly(remainder, field)
    return trim_poly(quotient, field), remainder


def period_polynomial(n: int, field):
    poly = [field.zero for _ in range(n + 1)]
    poly[0] = field.neg(field.one)
    poly[n] = field.one
    return poly


def characteristic_polynomial_low_to_high(connection):
    # connection [1,c1,...,cL] represents x^L+c1*x^(L-1)+...+cL.
    return list(reversed(connection))


def nonzero_connection_terms(connection, field):
    return [
        (idx, value)
        for idx, value in enumerate(connection)
        if value != field.zero
    ]


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
    doubled = sequence * 2
    connection = bm_connection(doubled, field)
    order = len(connection) - 1
    recurrence_failures = verify_connection(doubled, connection, field)
    generated = generate_from_connection(sequence, connection, len(doubled), field)
    generation_mismatches = sum(
        1 for left, right in zip(generated, doubled) if left != right
    )
    periodic_closure_failures = verify_connection(sequence + sequence[:order], connection, field)
    char_poly = characteristic_polynomial_low_to_high(connection)
    period_poly = period_polynomial(n, field)
    quotient, remainder = poly_divmod(period_poly, char_poly, field)
    char_divides_period = int(remainder == [field.zero])
    sequence_product = product(sequence, field)

    print("tensor factor beta recurrence audit")
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
    print("sequence")
    print(f"  distinct_values={len(set(sequence))}")
    print(f"  zero_count={sum(1 for value in sequence if value == field.zero)}")
    print(f"  product={sequence_product}")
    print()
    print("recurrence")
    print(f"  order={order}")
    print(f"  order_over_n={order / n:.6f}")
    print(f"  nonzero_connection_terms={nonzero_connection_terms(connection, field)}")
    print(f"  characteristic_coefficients={characteristic_coefficients(connection)}")
    print(f"  characteristic_divides_T^n_minus_1={char_divides_period}")
    print(f"  quotient_degree_if_divides={len(quotient)-1 if char_divides_period else 'NA'}")
    print(f"  recurrence_failures_on_doubled_sequence={recurrence_failures}")
    print(f"  generation_mismatches_on_doubled_sequence={generation_mismatches}")
    print(f"  periodic_closure_failures={periodic_closure_failures}")
    print()
    print("interpretation")
    print("  recurrence_order_L_gives_L_dimensional_norm_surface_for_beta_product=1")
    print("  useful_compression_requires_L_much_smaller_than_n_asymptotically=1")
    print("conclusion=reported_tensor_factor_beta_recurrence_audit")


if __name__ == "__main__":
    main()
