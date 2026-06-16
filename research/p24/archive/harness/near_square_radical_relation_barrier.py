#!/usr/bin/env python3
"""Barrier for lifting the p=n^2+7 CM identity to strict target traces.

The identity p = n^2 + 7 gives an explicit square root of -7 in F_p and a
cheap CM curve with j=-3375.  A tempting stricter route is that this radical
data might also select one of the large-discriminant target CM classes.

For ordinary elliptic curves this can only happen through genus data unless
the CM fields are actually the same.  An ordinary curve has commutative
endomorphism algebra: if it were isogenous to, or carried endomorphisms from,
both Q(sqrt(-7)) and Q(sqrt(D_K)), then these quadratic fields would have to
coincide.  For p24 the strict target fields are all different from Q(sqrt(-7)).
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24 = 10**24 + 7
N24 = 10**12
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(abs(n)).items():
        if exp & 1:
            out *= int(prime)
    return out


def fundamental_discriminant_from_trace(p: int, trace: int) -> int:
    delta = trace * trace - 4 * p
    if delta >= 0:
        raise ValueError("trace outside ordinary Hasse interval")
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def same_quadratic_field(D1: int, D2: int) -> bool:
    return squarefree_part(D1) == squarefree_part(D2)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def prime_rows(
    min_p: int,
    max_p: int,
    max_rows: int,
    n_modulus: int = 8,
    n_residue: int = 0,
) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    n = max(1, math.isqrt(min_p - 7))
    while len(rows) < max_rows:
        p = n * n + 7
        if p > max_p:
            break
        if p >= min_p and n % n_modulus == n_residue and sp.isprime(p):
            rows.append((n, p))
        n += 1
    return rows


def danger_trace_representatives(p: int, k: int) -> list[int]:
    modulus = 1 << k
    q = math.isqrt(p)
    lo = p + 1 - 2 * q
    hi = p + 1 + 2 * q
    first = lo + ((modulus - lo) % modulus)
    return [p + 1 - order for order in range(first, hi + 1, modulus)]


def p24_report() -> None:
    print("p24 near-square radical relation barrier")
    print(f"p={P24}")
    print(f"n={N24}")
    print(f"n^2 mod p={(N24 * N24) % P24}")
    print(f"sqrt_minus_7_in_Fp={N24}")
    print("cheap_CM_field_D=-7")
    print("target trace field relation")
    for trace in TARGET_TRACES:
        D = fundamental_discriminant_from_trace(P24, trace)
        quotient = abs(D) // 7 if abs(D) % 7 == 0 else None
        print(f"  trace={trace}")
        print(f"    fundamental_D={D}")
        print(f"    same_field_as_D_minus_7={same_quadratic_field(D, -7)}")
        print(f"    contains_minus_7_as_prime_discriminant={abs(D) % 7 == 0}")
        if quotient is not None:
            sqrt_quot = (trace * pow(2 * N24, -1, P24)) % P24
            print(f"    quotient_abs_D_over_7={quotient}")
            print(f"    explicit_sqrt_of_quotient_mod_p={sqrt_quot}")
            print(f"    sqrt_check={(sqrt_quot * sqrt_quot - quotient) % P24}")
        print(f"    v2_curve_order={v2(P24 + 1 - trace)}")
        print(f"    ordinary_trace_not_zero_mod_p={trace % P24 != 0}")
    print()
    print(
        "p24_conclusion=the_D_minus_7_radical_supplies_only_genus_splitting; "
        "strict_target_CM_fields_are_distinct_ordinary_fields"
    )


def calibration_report(min_p: int, max_p: int, max_rows: int) -> None:
    rows = prime_rows(min_p, max_p, max_rows, n_modulus=8, n_residue=0)
    print()
    print("small near-square calibration")
    print(f"min_p={min_p}")
    print(f"max_p={max_p}")
    print(f"rows={len(rows)}")
    print("row n p k target_traces same_D_minus_7_fields minus7_prime_discriminant_hits")
    for index, (n, p) in enumerate(rows, start=1):
        q = math.isqrt(p)
        k = (q + 1 + math.isqrt(4 * q)).bit_length()
        traces = danger_trace_representatives(p, k)
        same = 0
        minus7_factor = 0
        for trace in traces:
            D = fundamental_discriminant_from_trace(p, trace)
            same += int(same_quadratic_field(D, -7))
            minus7_factor += int(abs(D) % 7 == 0)
        print(f"{index:02d} {n} {p} {k} {len(traces)} {same} {minus7_factor}")
    print(
        "calibration_conclusion=near_square_D_minus_7_field_coincidence_is_not_the_"
        "generic_strict_trace_mechanism"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=500)
    ap.add_argument("--max-p", type=int, default=50_000)
    ap.add_argument("--max-rows", type=int, default=8)
    args = ap.parse_args()
    p24_report()
    calibration_report(args.min_p, args.max_p, args.max_rows)


if __name__ == "__main__":
    main()
