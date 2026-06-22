#!/usr/bin/env python3
"""Layer counts for the p27 B-line localized reduced cover.

The charted Magma staging isolates two natural offline CAS objects:

  * noR:  X,W,T,beta,Bline,Unext with denominator charting
  * full: noR plus compactD_R

This probe counts both layers over small extension fields in one pass.  The
goal is not to replace normalization; it is to give the offline CAS task a
denominator-aware diagnostic for whether compactD_R behaves like an independent
fresh half-cover and whether the reduced cover has obvious component-period
signals over extension fields.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, roots_x_plus_inv, source_b_plus


def ratio(num: int, den: int) -> float:
    return num / den if den else 0.0


def count_field(field: GF) -> tuple[Counter, dict[int, Counter]]:
    F = field
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    eta = F.elt(1)

    for x in range(F.q):
        x2 = F.sq(x)
        x3 = F.mul(x2, x)
        x4 = F.sq(x2)
        x5_pow = F.mul(x4, x)
        x6_pow = F.mul(x5_pow, x)
        x8 = F.sq(x4)

        if x == 0 or x == F.elt(1) or x == F.neg(F.elt(1)) or F.add_int(x2, 1) == 0:
            stats["bad_X_denominator"] += 1
            continue

        bline = source_b_plus(F, x)
        if bline is None:
            stats["bad_Bline"] += 1
            continue
        stats["valid_X"] += 1
        by_b[bline]["valid_X"] += 1

        a_den = F.mul(F.pow(F.sub_int(x, 1), 4), F.pow(F.add_int(x, 1), 4))
        if a_den == 0:
            stats["bad_A_den"] += 1
            continue
        poly = F.add(
            F.add(F.sub(x8, F.mul_int(x6_pow, 4)), F.sub(F.neg(F.mul_int(x4, 26)), F.mul_int(x2, 4))),
            F.elt(1),
        )
        a_num = F.neg(F.mul_int(poly, 2))
        a = F.div(a_num, a_den)

        t2 = F.mul(F.mul(x, F.add_int(x2, 1)), F.sub(F.add(x2, F.mul_int(x, 2)), F.elt(1)))
        for w in F.roots_square(F.sub(x3, x)):
            stats["W_points"] += 1
            by_b[bline]["W_points"] += 1
            for t in F.roots_square(t2):
                stats["T_points"] += 1
                by_b[bline]["T_points"] += 1
                u_den = F.mul(
                    F.mul(F.sub(t, F.mul_int(x2, 2)), F.sub_int(x, 1)),
                    F.pow(F.add_int(x, 1), 2),
                )
                if u_den == 0:
                    stats["bad_U_den"] += 1
                    by_b[bline]["bad_U_den"] += 1
                    continue

                mt = F.sub_int(
                    F.add(
                        F.add(F.mul_int(F.mul(w, x2), 2), F.mul_int(F.mul(w, x), 2)),
                        F.add(F.add(x4, F.mul_int(x3, 2)), F.neg(F.mul_int(x, 2))),
                    ),
                    1,
                )
                m0 = F.add(
                    F.add(
                        F.add(
                            F.add(F.mul(w, x5_pow), F.mul_int(F.mul(w, x4), 3)),
                            F.add(F.mul_int(F.mul(w, x3), 2), F.mul_int(F.mul(w, x2), 2)),
                        ),
                        F.add(F.sub(F.mul(w, x), w), F.mul_int(x6_pow, 2)),
                    ),
                    F.add(F.add(F.mul_int(x5_pow, 4), F.mul_int(x3, 4)), F.neg(F.mul_int(x2, 2))),
                )
                criterion_num = F.mul(F.mul(w, F.add_int(x2, 1)), F.add(m0, F.mul(mt, t)))
                r_rhs = F.div(criterion_num, x)
                r_roots = F.roots_square(r_rhs)
                stats[f"compactD_R_roots_{len(r_roots)}"] += 1
                by_b[bline][f"compactD_R_roots_{len(r_roots)}"] += 1

                u_core = F.add(
                    F.add(
                        F.add(F.mul_int(F.mul(F.mul(F.mul(eta, t), w), x), 4), F.mul(t, x3)),
                        F.add(F.mul(t, x2), F.neg(F.mul(t, x))),
                    ),
                    F.add(
                        F.add(F.neg(t), F.mul_int(x5_pow, 2)),
                        F.add(F.add(F.mul_int(x4, 2), F.neg(F.mul_int(x3, 2))), F.neg(F.mul_int(x2, 2))),
                    ),
                )
                u_num = F.mul_int(u_core, 2)
                beta_rhs = F.div(F.sub(F.sq(u_num), F.mul_int(F.sq(u_den), 4)), F.sq(u_den))
                beta_roots = F.roots_square(beta_rhs)
                stats[f"beta_roots_{len(beta_roots)}"] += 1
                by_b[bline][f"beta_roots_{len(beta_roots)}"] += 1
                r_chi = F.legendre(r_rhs)
                beta_chi = F.legendre(beta_rhs)
                if r_chi != beta_chi:
                    stats["compact_beta_squareclass_mismatch"] += 1
                    by_b[bline]["compact_beta_squareclass_mismatch"] += 1
                if r_rhs != 0 and beta_rhs != 0:
                    ratio_chi = F.legendre(F.div(r_rhs, beta_rhs))
                    stats[f"compact_beta_ratio_chi_{ratio_chi}"] += 1
                    by_b[bline][f"compact_beta_ratio_chi_{ratio_chi}"] += 1
                if not beta_roots:
                    continue

                for beta in beta_roots:
                    stats["noR_chart_points"] += 1
                    by_b[bline]["noR_chart_points"] += 1
                    x5_num = F.add(u_num, F.mul(beta, u_den))
                    x5 = F.div(x5_num, F.mul_int(u_den, 2))
                    d_next = F.add(F.add(F.sq(x5), F.mul(a, x5)), F.elt(1))
                    if r_rhs != 0 and beta_rhs != 0:
                        ratio_chi = F.legendre(F.div(r_rhs, beta_rhs))
                        dnext_chi = F.legendre(d_next)
                        if ratio_chi != dnext_chi:
                            stats["compact_beta_ratio_dnext_mismatch"] += 1
                            by_b[bline]["compact_beta_ratio_dnext_mismatch"] += 1
                    sd_roots = F.roots_square(d_next)
                    stats[f"reduced_U_roots_{len(sd_roots)}"] += 1
                    by_b[bline][f"reduced_U_roots_{len(sd_roots)}"] += 1
                    for sd in sd_roots:
                        unext = F.add(F.mul_int(x5, 2), F.mul_int(sd, 2))
                        stats["noR_reduced_U_points"] += 1
                        by_b[bline]["noR_reduced_U_points"] += 1
                        stats["full_reduced_U_points"] += len(r_roots)
                        by_b[bline]["full_reduced_U_points"] += len(r_roots)

                        x6_roots = roots_x_plus_inv(F, unext)
                        selector = F.add_int(unext, 2)
                        gamma_roots = F.roots_square(selector)
                        stats["noR_x6_points"] += len(x6_roots)
                        stats["noR_gamma_points"] += len(gamma_roots)
                        stats["full_x6_points"] += len(x6_roots) * len(r_roots)
                        stats["full_gamma_points"] += len(gamma_roots) * len(r_roots)
                        by_b[bline]["noR_x6_points"] += len(x6_roots)
                        by_b[bline]["noR_gamma_points"] += len(gamma_roots)
                        by_b[bline]["full_x6_points"] += len(x6_roots) * len(r_roots)
                        by_b[bline]["full_gamma_points"] += len(gamma_roots) * len(r_roots)

    for key in (
        "bad_A_den",
        "bad_Bline",
        "bad_U_den",
        "valid_X",
        "W_points",
        "T_points",
        "noR_chart_points",
        "noR_reduced_U_points",
        "full_reduced_U_points",
        "noR_x6_points",
        "noR_gamma_points",
        "full_x6_points",
        "full_gamma_points",
        "compact_beta_squareclass_mismatch",
        "compact_beta_ratio_chi_-1",
        "compact_beta_ratio_chi_1",
        "compact_beta_ratio_dnext_mismatch",
    ):
        stats.setdefault(key, 0)
    return stats, dict(by_b)


def summarize_b_fibers(by_b: dict[int, Counter]) -> Counter:
    out: Counter = Counter()
    for row in by_b.values():
        for key in (
            "valid_X",
            "noR_reduced_U_points",
            "full_reduced_U_points",
            "noR_gamma_points",
            "full_gamma_points",
        ):
            out[f"{key}_fiber_{row[key]}"] += 1
        pair = (row["noR_reduced_U_points"], row["full_reduced_U_points"])
        out[f"noR_full_pair_{pair}"] += 1
    return out


def print_top(counter: Counter, prefix: str, limit: int) -> None:
    print(f"  {prefix}:")
    for key, value in counter.most_common(limit):
        print(f"    {key} = {value}")
    omitted = len(counter) - min(len(counter), limit)
    if omitted:
        print(f"    omitted_distinct_keys = {omitted}")


def run_field(p: int, n: int, fiber_limit: int) -> None:
    F = GF(p, n)
    stats, by_b = count_field(F)
    stats["B_fibers"] = len(by_b)
    fiber_stats = summarize_b_fibers(by_b)

    print(f"GF({p}^{n}) q={F.q}:")
    terms = " + ".join(f"{c}*x^{i}" for i, c in enumerate(F.modulus) if c)
    print(f"  modulus = x^{n}" + (f" + {terms}" if terms else ""))
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for num, den in (
        ("noR_chart_points", "T_points"),
        ("noR_reduced_U_points", "noR_chart_points"),
        ("full_reduced_U_points", "noR_reduced_U_points"),
        ("noR_reduced_U_points", "q"),
        ("full_reduced_U_points", "q"),
        ("noR_gamma_points", "noR_reduced_U_points"),
        ("full_gamma_points", "full_reduced_U_points"),
    ):
        den_value = F.q if den == "q" else stats[den]
        print(f"  {num}_per_{den} = {ratio(stats[num], den_value):.9f}")
    print_top(fiber_stats, "fiber_summary_top", fiber_limit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="607,7^3,7^4,7^5,23^2,23^3")
    parser.add_argument("--fiber-limit", type=int, default=16)
    args = parser.parse_args()

    print("p27 B-line localized cover layer-count probe")
    print("chart = eta_plus, denominator-localized")
    print("layers = noR reduced cover vs compactD_R full cover")
    print(f"fields = {args.fields}")
    for p, n in parse_field_specs(args.fields):
        run_field(p, n, args.fiber_limit)
    print("p27_b_line_localized_cover_layer_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
