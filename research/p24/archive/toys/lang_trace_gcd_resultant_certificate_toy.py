#!/usr/bin/env python3
"""Toy verifier for the trace-gcd cyclic-resultant certificate.

The p24 trace-gcd origin product reduces to a right-cycle determinant sequence

    Delta(t) = f(omega^t),        t mod 211.

For a split toy field this script checks three equivalent finite certificates:

* every value `Delta(t)` is nonzero;
* the product/resultant `prod_t Delta(t)` is nonzero;
* a Bezout identity `A(Y) f(Y) + B(Y) (Y^d-1) = 1` exists.

The real p24 arithmetic problem is to produce the actual Pluecker-Fourier
polynomial `f` for the embedded CM trace-gcd data.  Once `f` is supplied, this
is the finite verifier shape.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp

from lang_trace_gcd_plucker_spectral_toy import primitive_root_of_order


def poly_from_coeffs(coeffs: list[int], q: int, x) -> sp.Poly:
    return sp.Poly(
        sum((coeff % q) * x**idx for idx, coeff in enumerate(coeffs)),
        x,
        modulus=q,
    )


def poly_eval(poly: sp.Poly, value: int, q: int) -> int:
    total = 0
    power = 1
    coeffs = [int(poly.nth(idx)) % q for idx in range(poly.degree() + 1)]
    for coeff in coeffs:
        total = (total + coeff * power) % q
        power = power * value % q
    return total


def normalize_constant(poly: sp.Poly, q: int, x) -> sp.Poly:
    if poly.is_zero:
        return poly
    if poly.degree() != 0:
        return poly
    value = int(poly.nth(0)) % q
    return sp.Poly(value, x, modulus=q)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=337)
    parser.add_argument("--right", type=int, default=7)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--force-zero", action="store_true")
    args = parser.parse_args()

    x = sp.symbols("x")
    root = primitive_root_of_order(args.q, args.right)
    rng = random.Random(args.seed)

    while True:
        coeffs = [rng.randrange(args.q) for _ in range(args.right)]
        if args.force_zero:
            # Make f(root^0)=0 while keeping degree < right.
            coeffs[0] = (-sum(coeffs[1:])) % args.q
        f = poly_from_coeffs(coeffs, args.q, x)
        modulus = sp.Poly(x**args.right - 1, x, modulus=args.q)
        values = [poly_eval(f, pow(root, t, args.q), args.q) for t in range(args.right)]
        product = 1
        for value in values:
            product = product * value % args.q
        gcd = sp.gcd(f, modulus)
        if args.force_zero or product:
            break

    s, t, g = sp.gcdex(f, modulus, x, modulus=args.q)
    s = sp.Poly(s, x, modulus=args.q)
    t = sp.Poly(t, x, modulus=args.q)
    g = normalize_constant(sp.Poly(g, x, modulus=args.q), args.q, x)
    bezout_lhs = (s * f + t * modulus).rem(modulus)
    bezout_constant = int(bezout_lhs.nth(0)) % args.q if bezout_lhs.degree() <= 0 else None
    resultant = int(sp.resultant(f.as_expr(), modulus.as_expr(), x)) % args.q

    print("Lang trace-gcd resultant certificate toy")
    print(f"q={args.q}")
    print(f"right={args.right}")
    print(f"root={root}")
    print(f"force_zero={int(args.force_zero)}")
    print(f"f_coeffs_low_to_high={[int(f.nth(i)) % args.q for i in range(args.right)]}")
    print(f"value_zero_count={sum(1 for value in values if value == 0)}")
    print(f"values={values}")
    print(f"product_mod_q={product}")
    print(f"resultant_mod_q={resultant}")
    print(f"product_resultant_match={int(product == resultant)}")
    print(f"gcd_degree={gcd.degree()}")
    print(f"gcd_coeffs={gcd.all_coeffs()}")
    print(f"bezout_g={g.as_expr()}")
    print(f"bezout_lhs_mod_xn_minus_1={bezout_lhs.as_expr()}")
    print(f"bezout_unit_certificate={int(bezout_constant == 1)}")
    print("interpretation")
    print("  gcd_degree_zero_or_bezout_unit_implies_all_right_values_nonzero=1")
    print("  p24_missing_input_is_actual_CM_pluecker_polynomial_f=1")
    print("conclusion=reported_lang_trace_gcd_resultant_certificate_toy")


if __name__ == "__main__":
    main()
