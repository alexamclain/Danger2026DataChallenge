#!/usr/bin/env python3
"""Power relation between origin norms and reduced trace-GCD right products.

For h=m*n and a right component d | m, the origin-action audit writes

    shift = n*alpha + m*beta mod h.

The reduced trace-GCD theorem uses only the right coordinate t mod d:

    Pi_right = prod_{t mod d} Delta(t).

This script checks, on small actual-CM rows, whether products over larger
origin fibers are just powers of Pi_right.  That is the exact relation one
expects if the other CRT/recovery directions contribute p-unit phase factors.

The result is a producer-theorem bookkeeping check: a full-origin norm can
prove the right norm only if it is available by a formula that does not
enumerate the full class set.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

from lang_trace_gcd_origin_action_audit import OriginDet, first_row, product_mod
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence


def product(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * value) % modulus
    return out


def values_by_omitted(records: tuple[OriginDet, ...]) -> dict[int, list[OriginDet]]:
    out: dict[int, list[OriginDet]] = defaultdict(list)
    for record in records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


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
        raise SystemExit("no eligible origin-action row found")
    if row.m % row.right != 0:
        raise SystemExit("right component must divide m")

    left_other_multiplicity = row.m // row.right
    full_origin_multiplicity = row.n * left_other_multiplicity

    print("Lang trace-gcd origin norm power audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"left_other_multiplicity=m/right={left_other_multiplicity}")
    print(f"full_origin_multiplicity=n*m/right={full_origin_multiplicity}")

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        pi_right = product(seq, row.q)
        all_values = [record.determinant for record in records]
        all_product = product_mod(all_values, row.q)
        expected_all = pow(pi_right, full_origin_multiplicity, row.q)
        beta_products = []
        for beta in sorted({record.beta for record in records}):
            beta_values = [
                record.determinant
                for record in records
                if record.beta == beta
            ]
            beta_products.append((beta, product_mod(beta_values, row.q)))
        expected_beta = pow(pi_right, left_other_multiplicity, row.q)
        beta_distinct = len({value for _, value in beta_products})
        beta_ok = all(value == expected_beta for _, value in beta_products)
        all_ok = all_product == expected_all
        failures += int(mismatches != 0 or not beta_ok or not all_ok)

        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  pi_right={pi_right}")
        print(f"  expected_beta_product=pi_right^(m/right)={expected_beta}")
        print(f"  beta_product_distinct={beta_distinct}")
        print(f"  beta_products_sample={beta_products[:8]}")
        print(f"  beta_products_match_expected={int(beta_ok)}")
        print(f"  all_origin_product={all_product}")
        print(f"  expected_all_origin_product=pi_right^(n*m/right)={expected_all}")
        print(f"  all_origin_product_match_expected={int(all_ok)}")

    print("interpretation")
    print("  origin_norm_power_relation=1 means larger origin norms add no new phase")
    print("  full_origin_norm_can_help_only_if_available_without_class_enumeration=1")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_origin_norm_power_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
