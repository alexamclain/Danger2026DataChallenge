#!/usr/bin/env python3
"""Next-gate test on the beta_U_fixedB no-R norm class.

The beta_U norm descent gives a real one-gate structure:

    gamma = chi(Norm(Unext + 2))
    gamma=+1 rows have 16 beta_U points over B
    gamma=-1 rows have 32 beta_U points over B

This probe asks the sqrt-beating question: after restricting to the
gamma=+1 beta_U rows and materializing x6 from Unext = x6 + 1/x6, does the
next selected gate f4 show a coupled/sign-uniform pattern, or does it behave
like another fresh half-cover?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


def curve_a(field: GF, x: int) -> int | None:
    x2 = field.sq(x)
    x3 = field.mul(x2, x)
    x4 = field.sq(x2)
    x5 = field.mul(x4, x)
    x6 = field.mul(x5, x)
    x8 = field.sq(x4)
    a_den = field.mul(field.pow(field.sub_int(x, 1), 4), field.pow(field.add_int(x, 1), 4))
    if a_den == 0:
        return None
    poly = field.add(
        field.add(field.sub(x8, field.mul_int(x6, 4)), field.sub(field.neg(field.mul_int(x4, 26)), field.mul_int(x2, 4))),
        field.elt(1),
    )
    a_num = field.neg(field.mul_int(poly, 2))
    return field.div(a_num, a_den)


def next_halves(field: GF, a: int, x_value: int) -> list[int]:
    d_next = field.add(field.add(field.sq(x_value), field.mul(a, x_value)), field.elt(1))
    roots = field.roots_square(d_next)
    out: set[int] = set()
    for root in roots:
        out.add(field.add(field.mul_int(x_value, 2), field.mul_int(root, 2)))
    return sorted(out)


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("beta_U next-gate probe expects q^2 fields")
    field = GF(p, n)
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    f4_signs_by_b: defaultdict[int, Counter] = defaultdict(Counter)

    for x, _w, _t, _beta, bline, _x5, unext, selector in enumerate_points(field):
        b = base_value(field, bline)
        if b is None:
            continue
        degrees = {
            "X": element_degree(field, x),
            "W": element_degree(field, _w),
            "T": element_degree(field, _t),
            "beta": element_degree(field, _beta),
            "B": element_degree(field, bline),
            "x5": element_degree(field, _x5),
            "U": element_degree(field, unext),
            "selector": element_degree(field, selector),
        }
        point_degree = lcm(list(degrees.values()))
        gamma_chi = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma_chi)
        if cls != "beta_U_fixedB":
            continue

        a = curve_a(field, x)
        if a is None:
            stats["bad_curve_a"] += 1
            continue

        stats["betaU_points"] += 1
        stats[f"betaU_gamma_{gamma_chi}"] += 1
        by_b[b]["betaU_points"] += 1
        by_b[b][f"gamma_{gamma_chi}"] += 1
        by_b[b][f"chiB_{legendre_base(b, p)}"] += 1

        if gamma_chi != 1:
            continue

        x6_roots = roots_x_plus_inv(field, unext)
        stats[f"x6_roots_{len(x6_roots)}"] += 1
        by_b[b][f"x6_roots_{len(x6_roots)}"] += 1
        for x6 in x6_roots:
            stats["x6_materialized_roots"] += 1
            by_b[b]["x6_materialized_roots"] += 1
            x7_roots = next_halves(field, a, x6)
            stats[f"x7_roots_{len(x7_roots)}"] += 1
            by_b[b][f"x7_roots_{len(x7_roots)}"] += 1
            if not x7_roots:
                continue
            for x7 in x7_roots:
                stats["x7_roots"] += 1
                by_b[b]["x7_roots"] += 1
                f4 = field.legendre(x7)
                stats[f"f4_{f4}"] += 1
                by_b[b][f"f4_{f4}"] += 1
                f4_signs_by_b[b][f"f4_{f4}"] += 1
                if x7:
                    v = field.add(x7, field.inv(x7))
                    vplus2 = field.add_int(v, 2)
                    if field.legendre(vplus2) != f4:
                        stats["vplus2_x7_chi_mismatch"] += 1

    for b, row in by_b.items():
        gamma_keys = [key for key in row if key.startswith("gamma_")]
        f4_keys = [key for key in f4_signs_by_b[b] if key.startswith("f4_")]
        if len(gamma_keys) > 1:
            stats["B_gamma_conflicts"] += 1
        if len(f4_keys) > 1:
            stats["B_f4_conflicts"] += 1
        if row["gamma_1"]:
            stats[f"gamma_plus_B_f4_keycount_{len(f4_keys)}"] += 1
            stats[f"gamma_plus_B_x7_roots_{row['x7_roots']}"] += 1

    for zero_key in ("bad_curve_a", "B_gamma_conflicts", "B_f4_conflicts", "vplus2_x7_chi_mismatch"):
        stats[zero_key] += 0

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  B_summary_top:")
    print("    columns = chiB betaU gamma x6 x7 f4+ f4-")
    summary = Counter()
    for b, row in by_b.items():
        gamma = 1 if row["gamma_1"] else -1 if row["gamma_-1"] else 0
        summary[
            (
                legendre_base(b, p),
                row["betaU_points"],
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
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2")
    args = parser.parse_args()

    print("p27 B-line no-R beta_U next-gate probe")
    print("question = after beta_U gamma=+1, is f4 coupled or fresh?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_betaU_next_gate_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
