#!/usr/bin/env python3
"""Norm descent comparison for the surviving fixed-B no-R subcovers.

The beta_U_fixedB pass found that chi(Norm(Unext + 2)) is uniform over each
active base B row and explains the 16/32 point fiber split.  This probe asks
whether hidden_mixed_fixedB has a comparable signature or whether beta_U is
the only fixed-B subcover worth sending to divisor/Kummer extraction first.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


TARGET_CLASSES = ("beta_U_fixedB", "hidden_mixed_fixedB")


def norm_to_base(field: GF, value: int) -> int:
    return field.pow(value, field.p + 1)


def trace_to_base(field: GF, value: int) -> int:
    return field.add(value, field.pow(value, field.p))


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("fixed-B norm descent expects q^2 fields")

    field = GF(p, n)
    stats: dict[str, Counter] = {cls: Counter() for cls in TARGET_CLASSES}
    by_class_b: dict[str, defaultdict[int, Counter]] = {
        cls: defaultdict(Counter) for cls in TARGET_CLASSES
    }
    norm_values_by_class_b: dict[str, defaultdict[int, set[int]]] = {
        cls: defaultdict(set) for cls in TARGET_CLASSES
    }
    trace_values_by_class_b: dict[str, defaultdict[int, set[int]]] = {
        cls: defaultdict(set) for cls in TARGET_CLASSES
    }

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
        if cls not in TARGET_CLASSES:
            continue

        norm_selector = norm_to_base(field, selector)
        trace_selector = trace_to_base(field, selector)
        norm_selector_base = base_value(field, norm_selector)
        trace_selector_base = base_value(field, trace_selector)
        if norm_selector_base is None or trace_selector_base is None:
            stats[cls]["nonbase_norm_or_trace"] += 1
            continue

        norm_chi = legendre_base(norm_selector_base, p)
        if norm_chi != gamma_chi:
            stats[cls]["gamma_norm_mismatch"] += 1

        row = by_class_b[cls][b]
        row["points"] += 1
        row[f"gamma_{gamma_chi}"] += 1
        row[f"norm_chi_{norm_chi}"] += 1
        stats[cls]["points"] += 1
        stats[cls][f"gamma_{gamma_chi}"] += 1
        stats[cls][f"base_B_chi_{legendre_base(b, p)}"] += 1
        stats[cls][f"norm_selector_chi_{norm_chi}"] += 1
        norm_values_by_class_b[cls][b].add(norm_selector_base)
        trace_values_by_class_b[cls][b].add(trace_selector_base)

    print(f"GF({p}^{n}) q={field.q}")
    for cls in TARGET_CLASSES:
        by_b = by_class_b[cls]
        for b, row in by_b.items():
            signs = [key for key in row if key.startswith("gamma_")]
            if len(signs) > 1:
                stats[cls]["B_gamma_conflicts"] += 1
            norm_signs = [key for key in row if key.startswith("norm_chi_")]
            if len(norm_signs) > 1:
                stats[cls]["B_norm_chi_conflicts"] += 1
            stats[cls][f"norm_values_per_B_{len(norm_values_by_class_b[cls][b])}"] += 1
            stats[cls][f"trace_values_per_B_{len(trace_values_by_class_b[cls][b])}"] += 1

        for zero_key in ("gamma_norm_mismatch", "B_gamma_conflicts", "B_norm_chi_conflicts"):
            stats[cls][zero_key] += 0

        print(f"  class {cls}")
        print(f"    active_B = {len(by_b)}")
        for key in sorted(stats[cls]):
            print(f"    {key} = {stats[cls][key]}")
        print("    B_summary_top:")
        print("      columns = chiB points gamma norm_values trace_values")
        summary = Counter()
        for b, row in by_b.items():
            gamma = 1 if row["gamma_1"] else -1 if row["gamma_-1"] else 0
            summary[
                (
                    legendre_base(b, p),
                    row["points"],
                    gamma,
                    len(norm_values_by_class_b[cls][b]),
                    len(trace_values_by_class_b[cls][b]),
                )
            ] += 1
        for vector, count in summary.most_common(16):
            print(f"      {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2")
    args = parser.parse_args()

    print("p27 B-line no-R fixed-B norm-descent comparison")
    print("question = is beta_U special, or does hidden_mixed have the same norm/fiber signature?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_fixedB_norm_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
