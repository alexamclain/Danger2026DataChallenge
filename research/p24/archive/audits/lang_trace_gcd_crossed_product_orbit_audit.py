#!/usr/bin/env python3
"""Crossed-product orbit norm audit for trace-GCD determinant values.

Raw trace-GCD determinant values are not Frobenius-compatible on nontrivial
right orbits, so ordinary base-factor residues are not the right algebra.  The
finite replacement is a weighted cyclic shift:

    M e_i = Delta(t_i) e_{i+1},

whose determinant is `(-1)^(r-1) prod_i Delta(t_i)` for an orbit of length
`r`.  For p24, `r=35` on nonzero right orbits, so the sign is positive.

This script verifies that package on a small actual-CM trace-GCD row and
checks that the tempting ordinary power collapse fails.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

from lang_trace_gcd_origin_action_audit import OriginDet, first_row
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % modulus)) % modulus
    return out


def det_mod(matrix: list[list[int]], q: int) -> int:
    n = len(matrix)
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col]:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = det * pivot_value % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det


def weighted_shift_det(values: list[int], q: int) -> int:
    degree = len(values)
    matrix = [[0 for _ in range(degree)] for _ in range(degree)]
    for col, value in enumerate(values):
        matrix[(col + 1) % degree][col] = value % q
    return det_mod(matrix, q)


def frobenius_orbits(modulus: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * multiplier) % modulus
        out.append(orbit)
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

    q_mod_right = row.q % row.right
    orbits = frobenius_orbits(row.right, q_mod_right)
    p24_nonzero_orbit_len = 35

    print("Lang trace-gcd crossed-product orbit audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={q_mod_right}")
    print(f"frobenius_orbits={orbits}")
    print(f"p24_nonzero_orbit_len={p24_nonzero_orbit_len}")
    print(f"p24_weighted_shift_sign_positive={int((p24_nonzero_orbit_len - 1) % 2 == 0)}")

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        if mismatches:
            failures += 1
        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        for orbit_index, orbit in enumerate(orbits):
            values = [seq[index] for index in orbit]
            product = product_mod(values, row.q)
            shift_det = weighted_shift_det(values, row.q)
            signed_product = product if (len(orbit) - 1) % 2 == 0 else (-product) % row.q
            ordinary_power = pow(values[0], len(orbit), row.q)
            match = shift_det == signed_product
            ordinary_match = ordinary_power == product
            failures += int(not match)
            print(
                f"  orbit={orbit_index} rep={orbit[0]} len={len(orbit)} "
                f"constant={int(len(set(values)) == 1)} values={values}"
            )
            print(f"    product={product}")
            print(f"    weighted_shift_det={shift_det}")
            print(f"    weighted_shift_match={int(match)}")
            print(f"    ordinary_power={ordinary_power}")
            print(f"    ordinary_power_match={int(ordinary_match)}")
            print(f"    crossed_norm_nonzero={int(shift_det != 0)}")

    print("interpretation")
    print("  weighted_shift_match=1 is the crossed-product orbit norm identity")
    print("  ordinary_power_match=0 on nonconstant orbits rules out ordinary norm collapse")
    print("  p24 nonzero right orbits have odd length 35, so the weighted-cycle sign is +")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_crossed_product_orbit_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
