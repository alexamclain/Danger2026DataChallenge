#!/usr/bin/env python3
"""Norm descent for beta_U_fixedB gamma on the p27 no-R cover.

For a quadratic extension GF(q^2)/GF(q), an element is a square in GF(q^2)
exactly when its norm is a square in GF(q).  This probe verifies that the
beta_U_fixedB selected class descends as

    chi_GF(q^2)(Unext + 2) = chi_GF(q)(Norm(Unext + 2))

and checks whether the resulting sign is uniform over each fixed base B.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


def norm_to_base(field: GF, value: int) -> int:
    return field.pow(value, field.p + 1)


def trace_to_base(field: GF, value: int) -> int:
    return field.add(value, field.pow(value, field.p))


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("beta_U norm descent expects q^2 fields")
    field = GF(p, n)
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    norm_values_by_b: defaultdict[int, set[int]] = defaultdict(set)
    trace_values_by_b: defaultdict[int, set[int]] = defaultdict(set)

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
        if cls != "beta_U_fixedB":
            continue

        norm_selector = norm_to_base(field, selector)
        trace_selector = trace_to_base(field, selector)
        norm_selector_base = base_value(field, norm_selector)
        trace_selector_base = base_value(field, trace_selector)
        if norm_selector_base is None or trace_selector_base is None:
            stats["nonbase_norm_or_trace"] += 1
            continue
        norm_chi = legendre_base(norm_selector_base, p)
        if norm_chi != gamma_chi:
            stats["gamma_norm_mismatch"] += 1

        stats["beta_U_points"] += 1
        stats[f"gamma_{gamma_chi}"] += 1
        stats[f"base_B_chi_{legendre_base(b, p)}"] += 1
        stats[f"norm_selector_chi_{norm_chi}"] += 1
        by_b[b]["points"] += 1
        by_b[b][f"gamma_{gamma_chi}"] += 1
        by_b[b][f"norm_chi_{norm_chi}"] += 1
        norm_values_by_b[b].add(norm_selector_base)
        trace_values_by_b[b].add(trace_selector_base)

    for b, row in by_b.items():
        signs = [key for key in row if key.startswith("gamma_")]
        if len(signs) > 1:
            stats["B_gamma_conflicts"] += 1
        norm_signs = [key for key in row if key.startswith("norm_chi_")]
        if len(norm_signs) > 1:
            stats["B_norm_chi_conflicts"] += 1
        stats[f"norm_values_per_B_{len(norm_values_by_b[b])}"] += 1
        stats[f"trace_values_per_B_{len(trace_values_by_b[b])}"] += 1

    print(f"GF({p}^{n}) q={field.q}")
    print(f"  active_beta_U_B = {len(by_b)}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  B_summary_top:")
    summary = Counter()
    for b, row in by_b.items():
        gamma = 1 if row["gamma_1"] else -1 if row["gamma_-1"] else 0
        summary[(legendre_base(b, p), row["points"], gamma, len(norm_values_by_b[b]), len(trace_values_by_b[b]))] += 1
    print("    columns = chiB points gamma norm_values trace_values")
    for vector, count in summary.most_common(16):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2")
    args = parser.parse_args()

    print("p27 B-line no-R beta_U norm-descent probe")
    print("question = does gamma descend as chi_base Norm(Unext+2), uniformly per B?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_betaU_norm_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
