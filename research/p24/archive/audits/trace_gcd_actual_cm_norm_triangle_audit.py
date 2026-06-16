#!/usr/bin/env python3
"""Actual-CM trace-GCD norm triangle audit.

This is the faithful small-row companion to ``trace_gcd_norm_triangle_toy.py``.
It reuses the actual trace-GCD tail-on-kernel matrices from the pinned
small-CM row and checks that the same norm object appears in three guises:

    orbit product of det(M_t)
    block-cycle/Fitting determinant built from the actual M_t
    split-interpolant/resultant norm of the right-phase determinant sequence

The default run is deliberately pinned and bounded; it is a theorem
microscope, not a class-set search.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_trace_gcd_block_cycle_norm_audit import (
    MatrixRecord,
    block_cycle_matrix,
    class_representatives,
    det_mod,
    first_matrix_row,
    frobenius_orbits,
    product_mod,
)
from lang_trace_gcd_factor_bezout_audit import dft_interpolate, eval_coeffs, is_base


def records_by_omitted(records: tuple[MatrixRecord, ...]) -> dict[int, list[MatrixRecord]]:
    out: dict[int, list[MatrixRecord]] = defaultdict(list)
    for record in records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


def field_product(values: list[FpE], field: ExtensionField) -> FpE:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def base_value(value: FpE) -> int | None:
    if not is_base(value):
        return None
    return int(value[0])


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
    parser.add_argument("--q-start", type=int, default=13463)
    parser.add_argument("--q-stop", type=int, default=13464)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=8)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int, default=140)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_matrix_row(args)
    if row is None:
        raise SystemExit("no eligible actual-CM matrix row found")

    right_order = int(sp.n_order(row.q % row.right, row.right))
    modulus = find_irreducible_modulus(row.q, right_order, args.seed)
    field = ExtensionField(row.q, right_order, modulus)
    root = primitive_root_of_order(field, row.right, args.seed)
    orbits = frobenius_orbits(row.right, row.q % row.right)

    print("trace-GCD actual-CM norm triangle audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"right_order={right_order}")
    print(f"extension_modulus_low_to_high={modulus}")
    print(f"root={root}")
    print(f"frobenius_orbits={orbits}")
    print("p24_analogue")
    print("  right=211")
    print("  block_size=16")
    print("  nonzero_orbit_len=35")
    print("  block_cycle_sign_positive=1")

    failures = 0
    for omitted, records in records_by_omitted(row.records).items():
        reps, det_mismatches = class_representatives(records, row.right)
        seq = [int(record.determinant) for record in reps]
        block_size = len(reps[0].matrix)
        coeffs = dft_interpolate(seq, root, field)
        evals = [
            eval_coeffs(coeffs, field.pow(root, t), field)
            for t in range(row.right)
        ]
        eval_mismatches = sum(
            1 for actual, expected in zip(evals, seq) if actual != field.embed(expected)
        )
        nonbase_positions = [index for index, coeff in enumerate(coeffs) if not is_base(coeff)]

        if det_mismatches or eval_mismatches:
            failures += 1

        print(f"omitted={omitted}")
        print(f"  right_class_det_mismatches={det_mismatches}")
        print(f"  block_size={block_size}")
        print(f"  determinant_values={seq}")
        print(f"  split_eval_mismatches={eval_mismatches}")
        print(f"  split_interpolant_base_coefficients={row.right - len(nonbase_positions)}/{row.right}")
        print(f"  split_interpolant_nonbase_positions={nonbase_positions}")
        print(f"  naive_base_polynomial_possible={int(not nonbase_positions)}")

        for orbit_index, orbit in enumerate(orbits):
            orbit_records = [reps[index] for index in orbit]
            matrices = [record.matrix for record in orbit_records]
            dets = [int(record.determinant) for record in orbit_records]
            scalar_product = product_mod(dets, row.q)
            block_det = det_mod(block_cycle_matrix(matrices, row.q), row.q)
            sign = 1 if (block_size * (len(orbit) - 1)) % 2 == 0 else -1
            signed_block_det = block_det if sign == 1 else (-block_det) % row.q
            split_norm = field_product([evals[index] for index in orbit], field)
            split_norm_base = base_value(split_norm)
            product_match = scalar_product == signed_block_det
            split_match = split_norm_base == scalar_product
            nonzero = scalar_product != 0
            failures += int(not product_match or not split_match)

            print(
                f"  orbit={orbit_index} rep={orbit[0]} len={len(orbit)} "
                f"sign={sign}"
            )
            print(f"    dets={dets}")
            print(f"    scalar_orbit_product={scalar_product}")
            print(f"    block_cycle_det={block_det}")
            print(f"    signed_block_cycle_det={signed_block_det}")
            print(f"    split_interpolant_norm_base={split_norm_base}")
            print(f"    product_equals_signed_block_cycle={int(product_match)}")
            print(f"    product_equals_split_norm={int(split_match)}")
            print(f"    orbit_norm_nonzero={int(nonzero)}")

    print("interpretation")
    print("  triangle_equalities=1 means scalar, Fitting, and split-norm views agree on the actual row")
    print("  naive_base_polynomial_possible=0 means the split/crossed-product distinction remains real")
    print("  p24 still needs a class-field theorem proving the analogous orbit norms are p-units")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_actual_cm_norm_triangle_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
