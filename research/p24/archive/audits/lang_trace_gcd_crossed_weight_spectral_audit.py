#!/usr/bin/env python3
"""Spectral audit for trace-GCD crossed-product orbit weights.

The crossed-product norm packages the raw orbit values correctly.  A stronger
producer theorem would exist if the whole right determinant sequence had
small Fourier support, e.g. one Frobenius orbit of coefficients.  The pinned
right-7 row has that property, but p24 exterior support shows it is not forced
by the determinant representation.

This script makes the small-row support explicit and reports the p24 exterior
support comparison in the same output.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_trace_gcd_exterior_support import (
    distinct_subset_sum_sizes,
    multiplicative_orbit,
    repeated_sum_sizes,
)
from lang_trace_gcd_factor_bezout_audit import dft_interpolate, frobenius_orbits
from lang_trace_gcd_origin_action_audit import OriginDet, first_row
from lang_trace_gcd_sequence_complexity import (
    bm_connection,
    connection_polynomial_summary,
    nonnull_ints,
    reduced_right_sequence,
    verify_connection,
)


P24 = 10**24 + 7
P24_RIGHT = 211
P24_TAIL = 16


def values_by_omitted(records: tuple[OriginDet, ...]) -> dict[int, list[OriginDet]]:
    out: dict[int, list[OriginDet]] = defaultdict(list)
    for record in records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


def coeff_support(coeffs: list[tuple[int, ...]], field: ExtensionField) -> list[int]:
    return [index for index, coeff in enumerate(coeffs) if coeff != field.zero]


def orbit_coverage(support: list[int], orbits: list[list[int]]) -> list[int]:
    support_set = set(support)
    return [
        index
        for index, orbit in enumerate(orbits)
        if any(value in support_set for value in orbit)
    ]


def full_orbit_support(support: list[int], orbits: list[list[int]]) -> list[int]:
    support_set = set(support)
    return [
        index
        for index, orbit in enumerate(orbits)
        if set(orbit).issubset(support_set)
    ]


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

    right_order = int(sp.n_order(row.q % row.right, row.right))
    modulus = find_irreducible_modulus(row.q, right_order, args.seed)
    field = ExtensionField(row.q, right_order, modulus)
    root = primitive_root_of_order(field, row.right, args.seed)
    orbits = frobenius_orbits(row.right, row.q % row.right)

    p24_orbit = multiplicative_orbit(P24 % P24_RIGHT, P24_RIGHT)
    p24_repeated = repeated_sum_sizes(p24_orbit, P24_RIGHT, P24_TAIL)
    p24_distinct = distinct_subset_sum_sizes(p24_orbit, P24_RIGHT, P24_TAIL)

    print("Lang trace-gcd crossed-weight spectral audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"right_order={right_order}")
    print(f"frobenius_orbits={orbits}")
    print(f"extension_modulus_low_to_high={modulus}")

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        coeffs = dft_interpolate(seq, root, field)
        support = coeff_support(coeffs, field)
        covered = orbit_coverage(support, orbits)
        full = full_orbit_support(support, orbits)
        connection = bm_connection(seq + seq, row.q)
        connection_failures = verify_connection(seq + seq, connection, row.q)
        _, divides, factorization = connection_polynomial_summary(
            connection, len(seq), row.q
        )
        failures += int(mismatches or connection_failures)

        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  dft_support={support}")
        print(f"  dft_support_size={len(support)}/{row.right}")
        print(f"  dft_support_orbits_touched={covered}")
        print(f"  dft_support_full_orbits={full}")
        print(f"  one_full_nonzero_orbit_support={int(len(full) == 1 and 0 not in full)}")
        print(f"  bm_order={len(connection) - 1}")
        print(f"  bm_connection={connection}")
        print(f"  bm_connection_failures={connection_failures}")
        print(f"  connection_divides_xn_minus_1={int(divides)}")
        print(f"  connection_factorization={factorization}")

    print("p24_exterior_support_comparison")
    print(f"  p24_right={P24_RIGHT}")
    print(f"  p24_p_mod_right={P24 % P24_RIGHT}")
    print(f"  p24_orbit_len={len(p24_orbit)}")
    print(f"  p24_tail={P24_TAIL}")
    print(f"  distinct_subset_sum_size_k1={p24_distinct[0]}")
    print(f"  distinct_subset_sum_size_k2={p24_distinct[1]}")
    print(f"  distinct_subset_sum_size_k3={p24_distinct[2]}")
    print(f"  distinct_subset_sum_size_k16={p24_distinct[P24_TAIL - 1]}")
    print(f"  repeated_sum_size_k2={p24_repeated[1]}")
    print(f"  full_support_by_k3={int(p24_distinct[2] == P24_RIGHT)}")
    print("interpretation")
    print("  small row has one-orbit DFT support, matching BM order right_order")
    print("  p24 exterior support is full by k=3, so one-orbit support needs CM cancellation")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_crossed_weight_spectral_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
