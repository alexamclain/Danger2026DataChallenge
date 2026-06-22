#!/usr/bin/env python3
"""Visible selector screen for beta_U same-sign f4 x6 pairs.

The beta_U f4 pair probe found the exact norm

    x7_plus*x7_minus = -4*(A*x6 + 1).

When this product has nonsquare character, the two x7 roots are automatically
mixed and give no f4 gain.  When it has square character, the pair is either
same-plus or same-minus.  This probe screens natural x6-level squareclasses
for that remaining same-sign choice.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv
from p27_b_line_noR_betaU_next_gate_probe import curve_a, next_halves
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value
from p27_b_line_noR_quadratic_subcover_classifier import classify


def inv_or_none(field: GF, value: int) -> int | None:
    if value == 0:
        return None
    return field.inv(value)


def atom_values(field: GF, a: int, x6: int, unext: int, bline: int) -> dict[str, int | None]:
    inv_x6 = inv_or_none(field, x6)
    atoms: dict[str, int | None] = {
        "x6": x6,
        "x6+1": field.add_int(x6, 1),
        "x6-1": field.sub_int(x6, 1),
        "x6+2": field.add_int(x6, 2),
        "x6-2": field.sub_int(x6, 2),
        "A*x6+1": field.add(field.mul(a, x6), field.elt(1)),
        "A*x6-1": field.sub(field.mul(a, x6), field.elt(1)),
        "x6+A": field.add(x6, a),
        "x6-A": field.sub(x6, a),
        "u": unext,
        "u+2": field.add_int(unext, 2),
        "u-2": field.sub_int(unext, 2),
        "B": bline,
        "A": a,
    }
    if inv_x6 is not None:
        atoms["x6+1/x6"] = field.add(x6, inv_x6)
        atoms["x6-1/x6"] = field.sub(x6, inv_x6)
    d_next = field.add(field.add(field.sq(x6), field.mul(a, x6)), field.elt(1))
    atoms["d_next"] = d_next
    atoms["x6*(A*x6+1)"] = field.mul(x6, atoms["A*x6+1"] or 0)
    atoms["(x6+1)*(A*x6+1)"] = field.mul(atoms["x6+1"] or 0, atoms["A*x6+1"] or 0)
    atoms["(x6-1)*(A*x6+1)"] = field.mul(atoms["x6-1"] or 0, atoms["A*x6+1"] or 0)
    return atoms


def product_chi(atom_chis: dict[str, int], labels: tuple[str, ...]) -> int:
    out = 1
    for label in labels:
        out *= atom_chis[label]
    return out


def collect_rows(field: GF) -> tuple[list[dict[str, object]], Counter]:
    stats: Counter = Counter()
    rows: list[dict[str, object]] = []

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

        for x6 in roots_x_plus_inv(field, unext):
            x7_roots = next_halves(field, a, x6)
            if len(x7_roots) != 2:
                stats[f"x7_roots_{len(x7_roots)}"] += 1
                continue
            f4_signs = [field.legendre(root) for root in x7_roots]
            if f4_signs[0] != f4_signs[1]:
                stats["mixed_pairs"] += 1
                continue
            target = f4_signs[0]
            stats["same_sign_pairs"] += 1
            stats[f"same_target_{target}"] += 1

            raw_atoms = atom_values(field, a, x6, unext, bline)
            atom_chis: dict[str, int] = {}
            for label, value in raw_atoms.items():
                if value is None:
                    stats[f"atom_{label}_missing"] += 1
                    continue
                chi = field.legendre(value)
                if chi == 0:
                    stats[f"atom_{label}_zero"] += 1
                    continue
                atom_chis[label] = chi
            rows.append({"target": target, "atom_chis": atom_chis})

    stats["screen_rows"] = len(rows)
    return rows, stats


def screen(rows: list[dict[str, object]], max_weight: int) -> tuple[Counter, list[tuple[int, str, int, int, int]]]:
    stats: Counter = Counter()
    if not rows:
        return stats, []
    labels = sorted(set.intersection(*(set(row["atom_chis"].keys()) for row in rows)))
    stats["common_atoms"] = len(labels)
    results: list[tuple[int, str, int, int, int]] = []

    for weight in range(1, max_weight + 1):
        best: tuple[int, str, int, int, int] | None = None
        tested = 0
        for combo in combinations(labels, weight):
            tested += 1
            match = 0
            opposite = 0
            for row in rows:
                pred = product_chi(row["atom_chis"], combo)
                if pred == row["target"]:
                    match += 1
                else:
                    opposite += 1
            best_match = max(match, opposite)
            polarity = "" if match >= opposite else "-"
            label = polarity + "*".join(combo)
            candidate = (weight, label, best_match, len(rows), len(rows) - best_match)
            if best is None or candidate[2] > best[2]:
                best = candidate
        if best is not None:
            results.append(best)
            stats[f"weight_{weight}_tested"] += tested
    return stats, results


def run_field(p: int, n: int, max_weight: int) -> None:
    if n != 2:
        raise ValueError("same-sign selector probe expects q^2 fields")
    field = GF(p, n)
    rows, stats = collect_rows(field)
    screen_stats, best = screen(rows, max_weight)
    stats.update(screen_stats)

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  best_products:")
    print("    columns = weight label matches total misses")
    for row in best:
        print(f"    {row}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71^2,167^2,199^2,263^2,311^2")
    parser.add_argument("--max-weight", type=int, default=3)
    args = parser.parse_args()

    print("p27 B-line no-R beta_U same-sign f4 selector probe")
    print("question = can natural x6-level characters choose same-plus vs same-minus?")
    print(f"fields = {args.fields}")
    print(f"max_weight = {args.max_weight}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n, args.max_weight)
    print("p27_b_line_noR_betaU_same_sign_selector_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
