#!/usr/bin/env python3
"""Does f4 descend to the beta_U norm-map quotient?

The beta_U_fixedB class controls the f3/materialization layer through

    gamma = chi_base(Norm(Unext + 2)).

The norm-fiber profile then showed a stable low-support split.  This probe
asks the next sqrt-beating question: after beta_U gamma=+1, does the next
selected sign f4 become constant on the finer quotient coordinate

    (B, N),  N = Norm(Unext + 2)?

If yes, the norm map carries a plausible f4 quotient.  If no, beta_U is a
one-gate class and f4 remains a fresh half-cover over the norm quotient.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv
from p27_b_line_noR_betaU_next_gate_probe import curve_a, next_halves
from p27_b_line_noR_betaU_norm_descent_probe import norm_to_base
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


def sign_label(value: int | None) -> str:
    if value == 1:
        return "plus"
    if value == -1:
        return "minus"
    if value == 0:
        return "mixed"
    return "missing"


def normalize_signs(values: Counter[int]) -> int | None:
    signs = {key for key, count in values.items() if count and key in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def summarize_groups(label: str, groups: dict[object, Counter[int]]) -> Counter[str]:
    stats: Counter[str] = Counter()
    size_hist: Counter[int] = Counter()
    for values in groups.values():
        total = sum(values.values())
        size_hist[total] += 1
        sign = normalize_signs(values)
        stats[f"{label}_{sign_label(sign)}_groups"] += 1
        if sign == 0:
            stats[f"{label}_mixed_rows"] += total
    stats[f"{label}_groups"] = len(groups)
    for size, count in size_hist.items():
        stats[f"{label}_size_{size}"] = count
    return stats


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("beta_U norm/f4 descent expects q^2 fields")
    field = GF(p, n)
    stats: Counter[str] = Counter()
    f4_by_b: defaultdict[int, Counter[int]] = defaultdict(Counter)
    f4_by_bn: defaultdict[tuple[int, int], Counter[int]] = defaultdict(Counter)
    f4_by_n: defaultdict[int, Counter[int]] = defaultdict(Counter)
    beta_point_patterns: Counter[tuple[int, int, int, str]] = Counter()

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

        norm_base = base_value(field, norm_to_base(field, selector))
        if norm_base is None:
            stats["nonbase_norm"] += 1
            continue
        norm_chi = legendre_base(norm_base, p)
        if norm_chi != gamma_chi:
            stats["gamma_norm_mismatch"] += 1
        stats["betaU_points"] += 1
        stats[f"betaU_gamma_{gamma_chi}"] += 1

        if gamma_chi != 1:
            continue

        a = curve_a(field, x)
        if a is None:
            stats["bad_curve_a"] += 1
            continue

        beta_f4: Counter[int] = Counter()
        x6_roots = roots_x_plus_inv(field, unext)
        stats[f"x6_roots_{len(x6_roots)}"] += 1
        for x6 in x6_roots:
            x7_roots = next_halves(field, a, x6)
            stats[f"x7_roots_{len(x7_roots)}"] += 1
            for x7 in x7_roots:
                f4 = field.legendre(x7)
                beta_f4[f4] += 1
                f4_by_b[b][f4] += 1
                f4_by_bn[(b, norm_base)][f4] += 1
                f4_by_n[norm_base][f4] += 1

        beta_sign = normalize_signs(beta_f4)
        beta_point_patterns[
            (
                legendre_base(b, p),
                norm_chi,
                len(x6_roots),
                sign_label(beta_sign),
            )
        ] += 1
        if beta_sign == 0:
            stats["beta_point_f4_mixed"] += 1
        elif beta_sign == 1:
            stats["beta_point_f4_plus"] += 1
        elif beta_sign == -1:
            stats["beta_point_f4_minus"] += 1
        else:
            stats["beta_point_f4_missing"] += 1

    stats.update(summarize_groups("B_f4", f4_by_b))
    stats.update(summarize_groups("BN_f4", f4_by_bn))
    stats.update(summarize_groups("N_f4", f4_by_n))
    for zero_key in (
        "bad_curve_a",
        "gamma_norm_mismatch",
        "nonbase_norm",
        "B_f4_mixed_groups",
        "BN_f4_mixed_groups",
        "N_f4_mixed_groups",
    ):
        stats[zero_key] += 0

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  beta_point_patterns:")
    print("    columns = chiB norm_chi x6_roots f4_pattern")
    for vector, count in beta_point_patterns.most_common(16):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71^2,167^2,199^2,263^2,311^2")
    args = parser.parse_args()

    print("p27 B-line no-R beta_U norm/f4 descent probe")
    print("question = after beta_U gamma=+1, is f4 constant on (B, Norm(Unext+2))?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_betaU_norm_f4_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
