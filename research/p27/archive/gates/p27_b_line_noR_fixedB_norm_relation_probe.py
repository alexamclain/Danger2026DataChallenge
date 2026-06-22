#!/usr/bin/env python3
"""Compare beta_U and hidden_mixed fixed-B norm classes.

The beta_U norm class is the first fixed-B extraction target; hidden_mixed is
secondary.  This probe asks whether the two classes show an obvious shared
Prym/coboundary signature on the same square-B support:

  * are their gamma signs equal/opposite/constant-product per B?
  * do their norm-value support sizes line up?
  * do their base norm-value sets have large overlap?

This is intentionally a finite-field routing test, not a source sampler.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_fixedB_norm_descent_probe import norm_to_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


TARGET_CLASSES = ("beta_U_fixedB", "hidden_mixed_fixedB")


def normalize_sign(counter: Counter[int]) -> int | None:
    signs = {key for key, count in counter.items() if count and key in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def sign_label(sign: int | None) -> str:
    return {1: "plus", -1: "minus", 0: "mixed", None: "missing"}[sign]


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("fixed-B norm relation expects q^2 fields")
    field = GF(p, n)
    by_class_b: dict[str, defaultdict[int, Counter[int]]] = {
        cls: defaultdict(Counter) for cls in TARGET_CLASSES
    }
    norm_values: dict[str, defaultdict[int, set[int]]] = {
        cls: defaultdict(set) for cls in TARGET_CLASSES
    }
    points_by_class_b: dict[str, defaultdict[int, int]] = {
        cls: defaultdict(int) for cls in TARGET_CLASSES
    }
    stats: Counter[str] = Counter()

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
        gamma = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma)
        if cls not in TARGET_CLASSES:
            continue
        norm_base = base_value(field, norm_to_base(field, selector))
        if norm_base is None:
            stats["nonbase_norm"] += 1
            continue
        norm_chi = legendre_base(norm_base, p)
        if norm_chi != gamma:
            stats[f"{cls}_gamma_norm_mismatch"] += 1
        by_class_b[cls][b][gamma] += 1
        norm_values[cls][b].add(norm_base)
        points_by_class_b[cls][b] += 1

    common_b = sorted(set(by_class_b["beta_U_fixedB"]) & set(by_class_b["hidden_mixed_fixedB"]))
    relation_rows: Counter[tuple[int, int, int, int, int, int, int]] = Counter()
    for b in common_b:
        beta_sign = normalize_sign(by_class_b["beta_U_fixedB"][b])
        hidden_sign = normalize_sign(by_class_b["hidden_mixed_fixedB"][b])
        if beta_sign == 0:
            stats["beta_mixed_B"] += 1
            continue
        if hidden_sign == 0:
            stats["hidden_mixed_B"] += 1
            continue
        if beta_sign is None or hidden_sign is None:
            stats["missing_sign_B"] += 1
            continue
        beta_norms = norm_values["beta_U_fixedB"][b]
        hidden_norms = norm_values["hidden_mixed_fixedB"][b]
        overlap = len(beta_norms & hidden_norms)
        stats["common_B"] += 1
        stats[f"beta_sign_{sign_label(beta_sign)}"] += 1
        stats[f"hidden_sign_{sign_label(hidden_sign)}"] += 1
        stats[f"product_sign_{sign_label(beta_sign * hidden_sign)}"] += 1
        stats[f"beta_norm_values_{len(beta_norms)}"] += 1
        stats[f"hidden_norm_values_{len(hidden_norms)}"] += 1
        stats[f"norm_overlap_{overlap}"] += 1
        stats[f"chiB_{legendre_base(b, p)}"] += 1
        relation_rows[
            (
                legendre_base(b, p),
                beta_sign,
                hidden_sign,
                beta_sign * hidden_sign,
                len(beta_norms),
                len(hidden_norms),
                overlap,
            )
        ] += 1

    for zero_key in (
        "nonbase_norm",
        "beta_U_fixedB_gamma_norm_mismatch",
        "hidden_mixed_fixedB_gamma_norm_mismatch",
        "beta_mixed_B",
        "hidden_mixed_B",
    ):
        stats[zero_key] += 0

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  relation_summary:")
    print("    columns = chiB beta_sign hidden_sign product beta_norms hidden_norms overlap")
    for vector, count in relation_rows.most_common(20):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2,199^2,263^2,311^2")
    args = parser.parse_args()

    print("p27 B-line no-R fixed-B norm relation probe")
    print("question = do beta_U and hidden_mixed norm classes share an obvious relation?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_fixedB_norm_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
