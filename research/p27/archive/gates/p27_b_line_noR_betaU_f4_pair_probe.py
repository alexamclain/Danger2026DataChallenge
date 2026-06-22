#!/usr/bin/env python3
"""Pair-level f4 structure above gamma-positive beta_U points.

The beta_U next-gate probe showed f4 is mixed on every active base B row.  This
probe zooms in one level deeper:

  beta_U gamma=+1 point -> two materialized x6 roots,
  each x6 root -> two x7 halves.

It checks whether the f4 signs are organized by x6-pair products, by the
reciprocal pair x6 <-> 1/x6, or whether f4 is already a fresh half-cover at
this finer level.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv
from p27_b_line_noR_betaU_next_gate_probe import curve_a, next_halves
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value
from p27_b_line_noR_quadratic_subcover_classifier import classify


def sign_label(signs: list[int]) -> str:
    plus = signs.count(1)
    minus = signs.count(-1)
    zero = signs.count(0)
    return f"p{plus}_m{minus}_z{zero}"


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("beta_U f4 pair probe expects q^2 fields")
    field = GF(p, n)
    stats: Counter = Counter()
    beta_point_summary: Counter = Counter()
    x6_pair_summary: Counter = Counter()
    reciprocal_summary: Counter = Counter()

    for x, w, t, beta, bline, x5, unext, selector in enumerate_points(field):
        if base_value(field, bline) is None:
            continue
        degrees = {
            "X": element_degree(field, x),
            "W": element_degree(field, w),
            "T": element_degree(field, t),
            "beta": element_degree(field, beta),
            "B": element_degree(field, bline),
            "x5": element_degree(field, x5),
            "U": element_degree(field, unext),
            "selector": element_degree(field, selector),
        }
        point_degree = lcm(list(degrees.values()))
        gamma_chi = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma_chi)
        if cls != "beta_U_fixedB" or gamma_chi != 1:
            continue

        a = curve_a(field, x)
        if a is None:
            stats["bad_curve_a"] += 1
            continue

        x6_roots = roots_x_plus_inv(field, unext)
        stats["gamma_plus_betaU_points"] += 1
        stats[f"x6_roots_{len(x6_roots)}"] += 1
        beta_f4_signs: list[int] = []
        x6_pair_products: list[int] = []

        for x6 in x6_roots:
            x7_roots = next_halves(field, a, x6)
            stats[f"x7_roots_{len(x7_roots)}"] += 1
            f4_signs = [field.legendre(x7) for x7 in x7_roots]
            beta_f4_signs.extend(f4_signs)
            label = sign_label(f4_signs)
            x6_pair_summary[label] += 1

            product_value = 1
            for x7 in x7_roots:
                product_value = field.mul(product_value, x7)
            product_chi = field.legendre(product_value)
            x6_pair_products.append(product_chi)
            x6_pair_summary[f"product_chi_{product_chi}"] += 1

            # For roots x7 = 2*x6 +/- 2*sqrt(d), product is -4*(A*x6+1).
            expected_product = field.neg(field.mul_int(field.add(field.mul(a, x6), field.elt(1)), 4))
            if product_value != expected_product:
                stats["x7_pair_product_formula_mismatch"] += 1
            expected_chi = field.legendre(expected_product)
            if expected_chi != product_chi:
                stats["x7_pair_product_chi_mismatch"] += 1

        beta_point_summary[sign_label(beta_f4_signs)] += 1
        beta_point_summary[f"x6_pair_product_pattern_{tuple(x6_pair_products)}"] += 1
        if len(x6_pair_products) == 2:
            reciprocal_summary[(x6_pair_products[0], x6_pair_products[1])] += 1
            reciprocal_summary[f"product_of_pair_products_{x6_pair_products[0] * x6_pair_products[1]}"] += 1

    for zero_key in (
        "bad_curve_a",
        "x7_pair_product_formula_mismatch",
        "x7_pair_product_chi_mismatch",
    ):
        stats[zero_key] += 0

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  beta_point_summary:")
    for key, count in beta_point_summary.most_common(16):
        print(f"    {key} = {count}")
    print("  x6_pair_summary:")
    for key, count in x6_pair_summary.most_common(16):
        print(f"    {key} = {count}")
    print("  reciprocal_pair_product_summary:")
    for key, count in reciprocal_summary.most_common(16):
        print(f"    {key} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71^2,167^2,199^2,263^2,311^2")
    args = parser.parse_args()

    print("p27 B-line no-R beta_U f4 pair probe")
    print("question = is mixed f4 organized at x6-pair level?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_betaU_f4_pair_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
