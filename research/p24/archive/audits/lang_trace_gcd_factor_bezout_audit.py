#!/usr/bin/env python3
"""Factorwise cyclic-algebra audit for trace-GCD determinant sequences.

This script checks the finite distinction behind the factorwise Bezout gate:

* if the determinant values are Frobenius-compatible, they can come from a
  base polynomial in F_q[Y]/(Y^d - 1);
* if they are not, interpolation over F_q(mu_d) leaves the base field, so a
  naive F_q resultant is not an honest certificate;
* Frobenius orbit products/norms remain a safe compressed payload once an
  arithmetic producer proves they are the actual factor norms.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from math import gcd

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_trace_gcd_origin_action_audit import OriginDet, first_row
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % modulus)) % modulus
    return out


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


def is_base(value: FpE) -> bool:
    return all(coord == 0 for coord in value[1:])


def dft_interpolate(values: list[int], root: FpE, field: ExtensionField) -> list[FpE]:
    """Return coefficients c_k with f(root^t)=values[t]."""
    d = len(values)
    inv_d = pow(d, -1, field.q)
    coeffs: list[FpE] = []
    for k in range(d):
        total = field.zero
        for t, value in enumerate(values):
            root_power = field.pow(root, (-k * t) % d)
            term = field.mul(field.embed(value), root_power)
            total = field.add(total, term)
        coeffs.append(field.scalar_mul(inv_d, total))
    return coeffs


def eval_coeffs(coeffs: list[FpE], root_power: FpE, field: ExtensionField) -> FpE:
    total = field.zero
    power = field.one
    for coeff in coeffs:
        total = field.add(total, field.mul(coeff, power))
        power = field.mul(power, root_power)
    return total


def factor_degrees_via_sympy(right: int, q: int) -> list[int]:
    x = sp.symbols("x")
    factors = sp.factor_list(sp.Poly(x**right - 1, x, modulus=q))[1]
    return sorted(poly.degree() for poly, multiplicity in factors for _ in range(multiplicity))


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

    try:
        factor_degrees = factor_degrees_via_sympy(row.right, row.q)
    except Exception:
        factor_degrees = sorted(len(orbit) for orbit in orbits)

    print("Lang trace-gcd factorwise Bezout audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"right_order={right_order}")
    print(f"extension_modulus_low_to_high={modulus}")
    print(f"root={root}")
    print(f"frobenius_orbits={orbits}")
    print(f"factor_degrees={factor_degrees}")
    print(f"norm_scalar_payload_elements={2 * len(orbits)}")
    print(f"factor_residue_plus_inverse_coefficients={2 * sum(len(orbit) for orbit in orbits)}")

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        compat_mismatches = sum(
            1
            for t, value in enumerate(seq)
            if seq[(row.q * t) % row.right] != value
        )
        coeffs = dft_interpolate(seq, root, field)
        eval_mismatches = 0
        for t, value in enumerate(seq):
            actual = eval_coeffs(coeffs, field.pow(root, t), field)
            if actual != field.embed(value):
                eval_mismatches += 1
        nonbase_positions = [index for index, coeff in enumerate(coeffs) if not is_base(coeff)]
        orbit_products = [
            product_mod([seq[index] for index in orbit], row.q)
            for orbit in orbits
        ]
        orbit_base_residue_possible = [
            int(len({seq[index] for index in orbit}) == 1)
            for orbit in orbits
        ]
        product = product_mod(seq, row.q)
        orbit_product_product = product_mod(orbit_products, row.q)

        if mismatches or eval_mismatches or product != orbit_product_product:
            failures += 1

        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  frobenius_compatibility_mismatches={compat_mismatches}/{row.right}")
        print(f"  split_interpolation_eval_mismatches={eval_mismatches}")
        print(f"  split_interpolant_base_coefficients={row.right - len(nonbase_positions)}/{row.right}")
        print(f"  split_interpolant_nonbase_positions={nonbase_positions}")
        print(f"  base_polynomial_possible={int(compat_mismatches == 0 and not nonbase_positions)}")
        print(f"  orbit_products={orbit_products}")
        print(f"  orbit_products_nonzero={int(all(value != 0 for value in orbit_products))}")
        print(f"  base_factor_residue_possible_by_orbit={orbit_base_residue_possible}")
        print(
            "  ordinary_base_factor_residues_possible="
            f"{int(all(orbit_base_residue_possible))}"
        )
        print(f"  product={product}")
        print(f"  product_of_orbit_products={orbit_product_product}")
        print(f"  product_matches_orbit_products={int(product == orbit_product_product)}")

    print("interpretation")
    print("  base_polynomial_possible=0 rules out naive F_q[Y] interpolation")
    print("  ordinary_base_factor_residues_possible=0 rules out raw F_q[Y]/Phi_O residues")
    print("  orbit_products_nonzero=1 is the small norm payload once soundness is proved")
    print("  factor_Bezout_payload_needs_descended_or_twisted_actual_residue=1")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_factor_bezout_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
