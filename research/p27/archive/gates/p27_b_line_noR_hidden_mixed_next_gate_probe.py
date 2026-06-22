#!/usr/bin/env python3
"""Next-gate test for the hidden_mixed_fixedB no-R class.

The fixed-B norm comparison showed hidden_mixed_fixedB has norm descent and
per-B gamma uniformity, but its visible fiber-size split is chi(B), not gamma.
This probe asks whether the gamma-positive hidden_mixed rows nevertheless
couple to the next selected gate f4 after materializing x6.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv
from p27_b_line_noR_betaU_next_gate_probe import curve_a, next_halves
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


TARGET_CLASS = "hidden_mixed_fixedB"


def sign_label(signs: list[int]) -> str:
    return f"p{signs.count(1)}_m{signs.count(-1)}_z{signs.count(0)}"


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("hidden_mixed next-gate probe expects q^2 fields")

    field = GF(p, n)
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    f4_by_b: defaultdict[int, Counter] = defaultdict(Counter)
    point_f4_summary: Counter = Counter()
    pair_summary: Counter = Counter()

    for x, w, t, beta, bline, x5, unext, selector in enumerate_points(field):
        b = base_value(field, bline)
        if b is None:
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
        if cls != TARGET_CLASS:
            continue

        a = curve_a(field, x)
        if a is None:
            stats["bad_curve_a"] += 1
            continue

        chi_b = legendre_base(b, p)
        stats["hidden_points"] += 1
        stats[f"hidden_gamma_{gamma_chi}"] += 1
        stats[f"hidden_chiB_{chi_b}"] += 1
        by_b[b]["hidden_points"] += 1
        by_b[b][f"gamma_{gamma_chi}"] += 1
        by_b[b][f"chiB_{chi_b}"] += 1

        if gamma_chi != 1:
            continue

        x6_roots = roots_x_plus_inv(field, unext)
        stats[f"x6_roots_{len(x6_roots)}"] += 1
        by_b[b][f"x6_roots_{len(x6_roots)}"] += 1
        point_f4_signs: list[int] = []

        for x6 in x6_roots:
            stats["x6_materialized_roots"] += 1
            by_b[b]["x6_materialized_roots"] += 1
            x7_roots = next_halves(field, a, x6)
            stats[f"x7_roots_{len(x7_roots)}"] += 1
            by_b[b][f"x7_roots_{len(x7_roots)}"] += 1
            f4_pair = [field.legendre(x7) for x7 in x7_roots]
            pair_summary[sign_label(f4_pair)] += 1
            product_value = 1
            for x7 in x7_roots:
                stats["x7_roots"] += 1
                by_b[b]["x7_roots"] += 1
                f4 = field.legendre(x7)
                stats[f"f4_{f4}"] += 1
                by_b[b][f"f4_{f4}"] += 1
                f4_by_b[b][f"f4_{f4}"] += 1
                point_f4_signs.append(f4)
                product_value = field.mul(product_value, x7)
                if x7:
                    v = field.add(x7, field.inv(x7))
                    if field.legendre(field.add_int(v, 2)) != f4:
                        stats["vplus2_x7_chi_mismatch"] += 1
            expected_product = field.neg(field.mul_int(field.add(field.mul(a, x6), field.elt(1)), 4))
            if product_value != expected_product:
                stats["x7_pair_product_formula_mismatch"] += 1
            pair_summary[f"product_chi_{field.legendre(product_value)}"] += 1
        point_f4_summary[sign_label(point_f4_signs)] += 1

    for b, row in by_b.items():
        gamma_keys = [key for key in row if key.startswith("gamma_")]
        f4_keys = [key for key in f4_by_b[b] if key.startswith("f4_")]
        if len(gamma_keys) > 1:
            stats["B_gamma_conflicts"] += 1
        if len(f4_keys) > 1:
            stats["B_f4_conflicts"] += 1
        if row["gamma_1"]:
            stats[f"gamma_plus_B_chiB_{1 if row['chiB_1'] else -1}"] += 1
            stats[f"gamma_plus_B_f4_keycount_{len(f4_keys)}"] += 1
            stats[f"gamma_plus_B_x7_roots_{row['x7_roots']}"] += 1

    for zero_key in (
        "bad_curve_a",
        "B_gamma_conflicts",
        "B_f4_conflicts",
        "vplus2_x7_chi_mismatch",
        "x7_pair_product_formula_mismatch",
    ):
        stats[zero_key] += 0

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  point_f4_summary:")
    for key, count in point_f4_summary.most_common(16):
        print(f"    {key} = {count}")
    print("  x6_pair_summary:")
    for key, count in pair_summary.most_common(16):
        print(f"    {key} = {count}")
    print("  B_summary_top:")
    print("    columns = chiB hidden gamma x6 x7 f4+ f4-")
    summary = Counter()
    for b, row in by_b.items():
        gamma = 1 if row["gamma_1"] else -1 if row["gamma_-1"] else 0
        chi_b = 1 if row["chiB_1"] else -1
        summary[
            (
                chi_b,
                row["hidden_points"],
                gamma,
                row["x6_materialized_roots"],
                row["x7_roots"],
                row["f4_1"],
                row["f4_-1"],
            )
        ] += 1
    for vector, count in summary.most_common(16):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2,199^2,263^2,311^2")
    args = parser.parse_args()

    print("p27 B-line no-R hidden_mixed next-gate probe")
    print("question = after hidden_mixed gamma=+1, is f4 coupled or fresh?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_hidden_mixed_next_gate_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
