#!/usr/bin/env python3
"""Linear-complexity probe for centered marginal alpha products.

After beta cancellation and left-sign normalization, the origin-translated
leading minor gives a sequence

    F(t), t mod right.

If `F(t)` had low linear complexity, the product over right translations might
admit a small recurrence/resultant certificate.  This script tests that on
small actual-CM rows.
"""

from __future__ import annotations

import argparse

from centered_marginal_origin_product_audit import (
    scan,
    translation_det_on_zero_sum,
)


def berlekamp_massey(sequence: list[int], q: int) -> int:
    c = [1]
    b = [1]
    length = 0
    m = 1
    last = 1
    for n, value in enumerate(sequence):
        discrepancy = value % q
        for i in range(1, length + 1):
            discrepancy = (discrepancy + c[i] * sequence[n - i]) % q
        if discrepancy == 0:
            m += 1
            continue
        old = c[:]
        scale = discrepancy * pow(last, -1, q) % q
        if len(c) < len(b) + m:
            c.extend([0] * (len(b) + m - len(c)))
        for j, coeff in enumerate(b):
            c[j + m] = (c[j + m] - scale * coeff) % q
        if 2 * length <= n:
            length = n + 1 - length
            b = old
            last = discrepancy
            m = 1
        else:
            m += 1
    return length


def normalized_right_sequence(row) -> list[int]:
    by_right: dict[int, int] = {}
    for alpha, value in enumerate(row.alpha_values):
        sign = translation_det_on_zero_sum(row.left, alpha)
        normalized = value if sign == 1 else (-value) % row.q
        key = alpha % row.right
        if key in by_right and by_right[key] != normalized:
            raise AssertionError("right-normalized alpha class mismatch")
        by_right[key] = normalized
    return [by_right[t] for t in range(row.right)]


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
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")
    seq = normalized_right_sequence(row)
    doubled = seq + seq
    complexity = berlekamp_massey(doubled, row.q)
    zero_count = sum(1 for value in seq if value == 0)

    print("Centered marginal alpha-sequence complexity")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"sequence_length={len(seq)}")
    print(f"zero_count={zero_count}")
    print(f"distinct_values={len(set(seq))}")
    print(f"linear_complexity_on_two_periods={complexity}")
    print(f"complexity_ratio={complexity}/{len(seq)}")
    print(f"values_prefix={seq[:40]}")
    print()
    print("interpretation")
    print("  low_complexity_would_support_recurrence_resultant_route=1")
    print("  full_or_near_full_complexity_demotes_simple_recurrence_route=1")
    print("conclusion=reported_centered_marginal_alpha_sequence_complexity")


if __name__ == "__main__":
    main()
