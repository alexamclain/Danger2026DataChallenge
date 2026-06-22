#!/usr/bin/env python3
"""Norm-fiber profile for the beta_U_fixedB no-R class.

The beta_U norm descent shows that gamma is uniform per active base B and
matches chi_base(Norm(Unext+2)).  This probe looks one layer deeper: for each
active B, collect the base-field norm values N=Norm(Unext+2) and record the
fiber profile of the map beta_U -> N.

If gamma-positive rows are exactly the low-support/ramified fibers of this
norm map, that is not a sampler by itself, but it gives CAS a sharper target:
explain the branch/ramification profile of the norm map on the chi(B)=+1
beta_U support.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_betaU_norm_descent_probe import norm_to_base
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


def profile_label(values: Counter[int]) -> str:
    mults = Counter(values.values())
    return ",".join(f"{mult}x{count}" for mult, count in sorted(mults.items()))


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("beta_U norm-fiber profile expects q^2 fields")
    field = GF(p, n)
    by_b: defaultdict[int, list[int]] = defaultdict(list)
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
        gamma_chi = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma_chi)
        if cls != "beta_U_fixedB":
            continue
        norm_base = base_value(field, norm_to_base(field, selector))
        if norm_base is None:
            stats["nonbase_norm"] += 1
            continue
        by_b[b].append(norm_base)

    profile_rows: Counter[tuple[int, int, int, str]] = Counter()
    bad_uniform = 0
    cutoff_mismatch = 0
    for b, norms in by_b.items():
        norm_counts: Counter[int] = Counter(norms)
        norm_signs = {legendre_base(norm, p) for norm in norm_counts}
        if len(norm_signs) != 1:
            bad_uniform += 1
            gamma = 0
        else:
            gamma = norm_signs.pop()
        nvalues = len(norm_counts)
        points = len(norms)
        label = profile_label(norm_counts)
        profile_rows[(gamma, points, nvalues, label)] += 1
        stats[f"gamma_{gamma}_B"] += 1
        stats[f"gamma_{gamma}_points"] += points
        stats[f"gamma_{gamma}_norm_values_{nvalues}"] += 1
        stats[f"profile_gamma_{gamma}_{points}_{nvalues}_{label}"] += 1
        # Empirical profile from previous runs: gamma+ has <=8 norm values,
        # gamma- has >8.  Track this exact cutoff as a falsifier, not a rule.
        if (gamma == 1 and nvalues > 8) or (gamma == -1 and nvalues <= 8):
            cutoff_mismatch += 1

    stats["active_B"] = len(by_b)
    stats["B_norm_sign_conflicts"] = bad_uniform
    stats["norm_value_cutoff_8_mismatch"] = cutoff_mismatch

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  profile_summary:")
    print("    columns = gamma points distinct_norm_values multiplicity_profile count")
    for (gamma, points, nvalues, label), count in sorted(profile_rows.items()):
        print(f"    {gamma} {points} {nvalues} {label} {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2,199^2,263^2,311^2")
    args = parser.parse_args()

    print("p27 B-line no-R beta_U norm-fiber profile probe")
    print("question = is gamma the low-support/ramified profile of Norm(Unext+2)?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_betaU_norm_fiber_profile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
