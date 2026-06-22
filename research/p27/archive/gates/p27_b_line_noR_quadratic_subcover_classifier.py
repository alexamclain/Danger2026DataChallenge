#!/usr/bin/env python3
"""Classify q^2 no-R coordinate-degree mechanisms.

This refines the coordinate-degree probe into named quadratic subcovers:

  * B_orbit: the B coordinate itself has degree 2,
  * base_point: the whole no-R point is already over the base field,
  * WT_only_zero: only W or T leaves the base field, and the selector is zero,
  * beta_U_fixedB: B is base-field but beta/x5/U/selector leave the base field,
  * hidden_mixed_fixedB: B is base-field and both hidden X/W/T plus beta/U
    coordinates leave the base field.

The goal is to decide which q^2 mechanisms deserve CAS attention.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm


def classify(degrees: dict[str, int], point_degree: int, gamma_chi: int) -> str:
    if point_degree == 1:
        return "base_point"
    if degrees["B"] == point_degree:
        return "B_orbit"
    hidden_extension = any(degrees[name] > 1 for name in ("X", "W", "T"))
    beta_u_extension = any(degrees[name] > 1 for name in ("beta", "x5", "U", "selector"))
    if hidden_extension and not beta_u_extension and gamma_chi == 0:
        return "WT_only_zero"
    if beta_u_extension and not hidden_extension:
        return "beta_U_fixedB"
    if beta_u_extension and hidden_extension:
        return "hidden_mixed_fixedB"
    return "other_fixedB"


def run_field(p: int, n: int) -> None:
    field = GF(p, n)
    if n != 2:
        raise ValueError("quadratic subcover classifier expects degree-2 fields")
    rows = enumerate_points(field)
    stats: Counter = Counter()
    class_gamma: Counter = Counter()
    class_vectors: Counter = Counter()

    for x, w, t, beta, bline, x5, unext, selector in rows:
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
        stats["points"] += 1
        stats[f"class_{cls}"] += 1
        stats[f"class_{cls}_gamma_{gamma_chi}"] += 1
        class_gamma[(cls, gamma_chi)] += 1
        vector = (
            cls,
            degrees["B"],
            degrees["X"],
            degrees["W"],
            degrees["T"],
            degrees["beta"],
            degrees["x5"],
            degrees["U"],
            degrees["selector"],
            gamma_chi,
        )
        class_vectors[vector] += 1

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  class_gamma:")
    for (cls, gamma_chi), count in sorted(class_gamma.items()):
        print(f"    {cls} gamma {gamma_chi} = {count}")
    print("  class_vectors_top:")
    print("    columns = class B X W T beta x5 U selector gamma_chi")
    for vector, count in class_vectors.most_common(20):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="7^2,23^2,71^2,103^2,167^2")
    args = parser.parse_args()

    print("p27 B-line no-R quadratic subcover classifier")
    print("interpretation = classify q^2 mechanisms for CAS routing")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_quadratic_subcover_classifier_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
