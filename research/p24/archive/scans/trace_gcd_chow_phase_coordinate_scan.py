#!/usr/bin/env python3
"""Phase-coordinate diagnostic for the trace-GCD Chow determinant.

The plain-j scan shows that the selected trace-GCD Chow determinant is not a
low-degree function of the visible CM root.  This script asks the next,
phase-aware question on small actual-CM rows:

* does the determinant factor through the right phase coordinate
  `alpha mod right`;
* what Frobenius/DFT support does the resulting right-phase sequence have;
* how much smaller is that phase description than plain-j interpolation?

This is still a diagnostic, not a p24 producer.  A positive right-phase
descent identifies the finite object `f_trace(Y)` whose orbit norms are the
certificate payload; p-unitness still needs the class-field/Fitting theorem.
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
from lang_trace_gcd_crossed_weight_spectral_audit import (
    coeff_support,
    full_orbit_support,
    orbit_coverage,
)
from lang_trace_gcd_exterior_support import (
    distinct_subset_sum_sizes,
    multiplicative_orbit,
)
from lang_trace_gcd_factor_bezout_audit import dft_interpolate, frobenius_orbits
from lang_trace_gcd_sequence_complexity import (
    bm_connection,
    connection_polynomial_summary,
    nonnull_ints,
    reduced_right_sequence,
    verify_connection,
)
from packet_scalar_divisor_shape_toy import polynomial_degree, rational_degree
from trace_gcd_chow_plain_divisor_scan import (
    RowWithCycle,
    determinant_pairs,
    first_row_with_cycle,
)


P24 = 10**24 + 7
P24_RIGHT = 211
P24_TAIL = 16


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % modulus)) % modulus
    return out


def values_by_omitted(bundle: RowWithCycle) -> dict[int, list]:
    out = defaultdict(list)
    for record in bundle.row.records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


def phase_orbit_products(seq: list[int], orbits: list[list[int]], q: int) -> list[tuple[int, int, int]]:
    return [
        (index, len(orbit), product_mod([seq[t] for t in orbit], q))
        for index, orbit in enumerate(orbits)
    ]


def print_p24_exterior_comparison() -> None:
    p24_orbit = multiplicative_orbit(P24 % P24_RIGHT, P24_RIGHT)
    p24_distinct = distinct_subset_sum_sizes(p24_orbit, P24_RIGHT, P24_TAIL)
    print("p24_exterior_support_comparison")
    print(f"  p24_right={P24_RIGHT}")
    print(f"  p24_p_mod_right={P24 % P24_RIGHT}")
    print(f"  p24_orbit_len={len(p24_orbit)}")
    print(f"  p24_tail={P24_TAIL}")
    print(f"  distinct_subset_sum_size_k1={p24_distinct[0]}")
    print(f"  distinct_subset_sum_size_k2={p24_distinct[1]}")
    print(f"  distinct_subset_sum_size_k3={p24_distinct[2]}")
    print(f"  distinct_subset_sum_size_k16={p24_distinct[P24_TAIL - 1]}")
    print(f"  full_support_by_k3={int(p24_distinct[2] == P24_RIGHT)}")


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
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--all-omitted", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--skip-plain-degree", action="store_true")
    parser.add_argument("--max-dft-extension-degree", type=int, default=16)
    args = parser.parse_args()

    bundle = first_row_with_cycle(args)
    if bundle is None:
        raise SystemExit("no eligible trace-gcd phase-coordinate row found")

    row = bundle.row
    right_order = int(sp.n_order(row.q % row.right, row.right))
    orbits = frobenius_orbits(row.right, row.q % row.right)
    can_dft = right_order <= args.max_dft_extension_degree
    field: ExtensionField | None = None
    root = None
    if can_dft:
        modulus = find_irreducible_modulus(row.q, right_order, args.seed)
        field = ExtensionField(row.q, right_order, modulus)
        root = primitive_root_of_order(field, row.right, args.seed)
    else:
        modulus = []

    print("trace-GCD Chow phase-coordinate scan")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"right_order={right_order}")
    print(f"frobenius_orbits={orbits}")
    print(f"dft_extension_enabled={int(can_dft)}")
    if can_dft:
        print(f"extension_modulus_low_to_high={modulus}")

    failures = 0
    for omitted, records in values_by_omitted(bundle).items():
        if args.only_omitted is not None and omitted != args.only_omitted:
            continue
        pairs = determinant_pairs(bundle, omitted)
        plain_poly = plain_rat = None
        if not args.skip_plain_degree:
            plain_poly = polynomial_degree(pairs, row.q)
            plain_rat = rational_degree(pairs, row.q)
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        connection = bm_connection(seq + seq, row.q)
        connection_failures = verify_connection(seq + seq, connection, row.q)
        _, divides, factorization = connection_polynomial_summary(
            connection, len(seq), row.q
        )
        orbit_products = phase_orbit_products(seq, orbits, row.q)
        phase_compression = len(records) / len(seq)
        failures += int(mismatches or connection_failures)

        print(f"omitted={omitted}")
        print(f"  origin_records={len(records)}")
        print(f"  phase_compression_factor={phase_compression:.6g}")
        if plain_poly is not None and plain_rat is not None:
            print(f"  plain_j_polynomial_degree={plain_poly}")
            print(f"  plain_j_rational_degree={plain_rat}")
        print(f"  right_class_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  right_zero_count={sum(value == 0 for value in seq)}")
        print(f"  right_distinct_count={len(set(seq))}")
        print(f"  right_total_product={product_mod(seq, row.q)}")
        print(f"  right_orbit_products={orbit_products}")
        print(f"  bm_order={len(connection) - 1}")
        print(f"  bm_connection={connection}")
        print(f"  bm_connection_failures={connection_failures}")
        print(f"  connection_divides_xn_minus_1={int(divides)}")
        print(f"  connection_factorization={factorization}")
        if can_dft and field is not None and root is not None:
            coeffs = dft_interpolate(seq, root, field)
            support = coeff_support(coeffs, field)
            covered = orbit_coverage(support, orbits)
            full = full_orbit_support(support, orbits)
            print(f"  dft_support={support}")
            print(f"  dft_support_size={len(support)}/{row.right}")
            print(f"  dft_support_orbits_touched={covered}")
            print(f"  dft_support_full_orbits={full}")
            print(f"  one_full_nonzero_orbit_support={int(len(full) == 1 and 0 not in full)}")

    print_p24_exterior_comparison()
    print("interpretation")
    print("  right_class_mismatches=0 means the determinant descends to the right phase algebra.")
    print("  small DFT support is a helpful phase-aware simplification in the toy row.")
    print("  p24 full exterior support means such simplification would need arithmetic cancellation.")
    print("  orbit products are the safe certificate payload even when DFT support is full.")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_chow_phase_coordinate_scan")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
