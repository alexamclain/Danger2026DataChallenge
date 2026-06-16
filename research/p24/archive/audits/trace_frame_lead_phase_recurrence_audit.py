#!/usr/bin/env python3
"""Linear-complexity audit for the leading trace-frame phase sequence.

The divisor and edge-shape scans show that the leading determinant norm is not
a low-degree plain-j or single-edge function.  This script tests a different
phase-aware possibility: maybe the origin-period sequence itself has unusually
small linear recurrence over the split prime field.

The comparison is against random controls with the same observed period.  A
real phase theorem should beat those controls, not merely exploit periodicity.
"""

from __future__ import annotations

import argparse
from collections import Counter
import random

from trace_frame_lead_divisor_support_scan import (
    fixed_cycle,
    lead_norm_pairs,
    minimal_period,
)


def inv(value: int, q: int) -> int:
    return pow(value % q, -1, q)


def bm_connection(sequence: list[int], q: int) -> list[int]:
    """Return delay-form connection c with c[0]=1 over F_q."""

    c = [1]
    b = [1]
    linear_complexity = 0
    shift = 1
    last_discrepancy = 1
    for n, value in enumerate(sequence):
        discrepancy = value % q
        for i in range(1, linear_complexity + 1):
            discrepancy = (discrepancy + c[i] * sequence[n - i]) % q
        if discrepancy == 0:
            shift += 1
            continue
        old_c = c[:]
        scale = discrepancy * inv(last_discrepancy, q) % q
        if len(c) < len(b) + shift:
            c.extend(0 for _ in range(len(b) + shift - len(c)))
        for j, coeff in enumerate(b):
            c[j + shift] = (c[j + shift] - scale * coeff) % q
        if 2 * linear_complexity <= n:
            linear_complexity = n + 1 - linear_complexity
            b = old_c
            last_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1
    return c[: linear_complexity + 1]


def verify_connection(sequence: list[int], connection: list[int], q: int) -> int:
    order = len(connection) - 1
    failures = 0
    for n in range(order, len(sequence)):
        total = sequence[n] % q
        for i in range(1, order + 1):
            total = (total + connection[i] * sequence[n - i]) % q
        failures += int(total % q != 0)
    return failures


def poly_trim(poly: list[int], q: int) -> list[int]:
    out = [value % q for value in poly]
    while out and out[-1] == 0:
        out.pop()
    return out or [0]


def poly_divmod(numerator: list[int], denominator: list[int], q: int) -> tuple[list[int], list[int]]:
    numerator = poly_trim(numerator, q)
    denominator = poly_trim(denominator, q)
    if denominator == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    if len(numerator) < len(denominator):
        return [0], numerator
    quotient = [0 for _ in range(len(numerator) - len(denominator) + 1)]
    remainder = numerator[:]
    den_inv = inv(denominator[-1], q)
    while len(remainder) >= len(denominator) and remainder != [0]:
        shift = len(remainder) - len(denominator)
        scale = remainder[-1] * den_inv % q
        quotient[shift] = scale
        for idx, coeff in enumerate(denominator):
            rem_idx = idx + shift
            remainder[rem_idx] = (remainder[rem_idx] - scale * coeff) % q
        remainder = poly_trim(remainder, q)
    return poly_trim(quotient, q), remainder


def characteristic_low_to_high(connection: list[int]) -> list[int]:
    return list(reversed(connection))


def period_polynomial(period: int, q: int) -> list[int]:
    poly = [0 for _ in range(period + 1)]
    poly[0] = q - 1
    poly[period] = 1
    return poly


def connection_summary(period_values: list[int], q: int) -> dict[str, object]:
    doubled = period_values * 2
    connection = bm_connection(doubled, q)
    order = len(connection) - 1
    failures = verify_connection(doubled, connection, q)
    period_poly = period_polynomial(len(period_values), q)
    quotient, remainder = poly_divmod(
        period_poly,
        characteristic_low_to_high(connection),
        q,
    )
    return {
        "order": order,
        "connection": connection,
        "failures": failures,
        "char_divides_period": int(remainder == [0]),
        "quotient_degree": len(quotient) - 1 if remainder == [0] else None,
    }


def random_period_values(period: int, q: int, rng: random.Random, nonzero: bool) -> list[int]:
    values: list[int] = []
    while len(values) < period:
        value = rng.randrange(1 if nonzero else 0, q)
        values.append(value)
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--D", type=int, default=-10919)
    parser.add_argument("--q", type=int, default=11243)
    parser.add_argument("--ell", type=int, default=2)
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--factor-index", type=int, default=0)
    parser.add_argument("--subdegree", type=int, default=2)
    parser.add_argument("--target", default="axis")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-top-count", type=int, default=4)
    parser.add_argument("--random-trials", type=int, default=80)
    args = parser.parse_args()

    rng = random.Random(args.seed + 9181)
    cycle = fixed_cycle(args.D, args.q, args.ell)
    pairs, metadata = lead_norm_pairs(
        cycle,
        args.q,
        args.m,
        args.factor_index,
        args.subdegree,
        args.target,
        args.seed,
        args.max_top_count,
    )
    values = [value % args.q for _, value in pairs]
    period = minimal_period(values)
    period_values = values[:period]
    actual = connection_summary(period_values, args.q)
    random_orders: list[int] = []
    random_divides = 0
    nonzero = all(value != 0 for value in period_values)
    for _ in range(args.random_trials):
        control = random_period_values(period, args.q, rng, nonzero)
        summary = connection_summary(control, args.q)
        random_orders.append(int(summary["order"]))
        random_divides += int(summary["char_divides_period"])

    print("trace-frame leading phase recurrence audit")
    print(f"D={args.D}")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"h={len(cycle)}")
    print(f"m={args.m}")
    print(f"n={metadata['n']}")
    print(f"factor_index={args.factor_index}")
    print(f"factor_degree={metadata['factor_degree']}")
    print(f"tensor_factor_degree={metadata['tensor_factor_degree']}")
    print(f"subdegree={args.subdegree}")
    print(f"raw_rank={metadata['raw_rank']}")
    print(f"top_count={metadata['top_count']}")
    print(f"value_count={len(values)}")
    print(f"period={period}")
    print(f"orbit_size={len(values) // period if period else 0}")
    print(f"distinct_period_values={len(set(period_values))}")
    print(f"zero_period_values={sum(1 for value in period_values if value == 0)}")
    print("actual_recurrence")
    print(f"  order={actual['order']}")
    print(f"  order_over_period={int(actual['order']) / period:.6f}")
    print(f"  connection={actual['connection']}")
    print(f"  recurrence_failures={actual['failures']}")
    print(f"  characteristic_divides_T^period_minus_1={actual['char_divides_period']}")
    print(f"  quotient_degree_if_divides={actual['quotient_degree'] if actual['quotient_degree'] is not None else 'NA'}")
    print("random_controls")
    print(f"  trials={args.random_trials}")
    print(f"  order_min={min(random_orders) if random_orders else 'NA'}")
    print(f"  order_max={max(random_orders) if random_orders else 'NA'}")
    print(f"  order_hist={dict(sorted(Counter(random_orders).items()))}")
    print(f"  characteristic_divides_count={random_divides}")
    print("interpretation")
    print("  random_controls_preserve_period_and_nonzero_status=1")
    print("  actual_order_below_random_min=" + str(int(bool(random_orders) and int(actual["order"]) < min(random_orders))))
    print("  low_recurrence_phase_shortcut_visible=" + str(int(bool(random_orders) and int(actual["order"]) < min(random_orders))))
    print("  matching_random_complexity_closes_simple_phase_recurrence_shortcut=" + str(int(bool(random_orders) and int(actual["order"]) >= min(random_orders))))
    print("conclusion=reported_trace_frame_lead_phase_recurrence_audit")


if __name__ == "__main__":
    main()
