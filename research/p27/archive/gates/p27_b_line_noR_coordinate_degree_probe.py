#!/usr/bin/env python3
"""Coordinate-degree profile for p27 no-R reduced B-line points.

This is a microscope for the degree-2/degree-3 closed-point pressure.  It
enumerates no-R reduced U points and records which coordinates force the
extension degree: the B-line coordinate, hidden X/W/T/beta coordinates, or
Unext/gamma itself.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs, source_b_plus


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def element_degree(field: GF, value: int) -> int:
    for d in divisors(field.n):
        if field.pow(value, field.p**d) == value:
            return d
    return field.n


def lcm(values: list[int]) -> int:
    out = 1
    for value in values:
        out = out * value // math.gcd(out, value)
    return out


def extension_source(b_degree: int, point_degree: int) -> str:
    if point_degree == 1:
        return "base_point"
    if b_degree == point_degree:
        return "B_orbit"
    if b_degree == 1:
        return "fiber_over_base_B"
    return "fiber_over_extension_B"


def enumerate_points(field: GF) -> list[tuple[int, ...]]:
    F = field
    eta = F.elt(1)
    rows: list[tuple[int, ...]] = []

    for x in range(F.q):
        x2 = F.sq(x)
        x3 = F.mul(x2, x)
        x4 = F.sq(x2)
        x5_pow = F.mul(x4, x)
        x6_pow = F.mul(x5_pow, x)
        x8 = F.sq(x4)

        if x == 0 or x == F.elt(1) or x == F.neg(F.elt(1)) or F.add_int(x2, 1) == 0:
            continue

        bline = source_b_plus(F, x)
        if bline is None:
            continue

        a_den = F.mul(F.pow(F.sub_int(x, 1), 4), F.pow(F.add_int(x, 1), 4))
        if a_den == 0:
            continue
        poly = F.add(
            F.add(F.sub(x8, F.mul_int(x6_pow, 4)), F.sub(F.neg(F.mul_int(x4, 26)), F.mul_int(x2, 4))),
            F.elt(1),
        )
        a_num = F.neg(F.mul_int(poly, 2))
        a = F.div(a_num, a_den)

        t2 = F.mul(F.mul(x, F.add_int(x2, 1)), F.sub(F.add(x2, F.mul_int(x, 2)), F.elt(1)))
        for w in F.roots_square(F.sub(x3, x)):
            for t in F.roots_square(t2):
                u_den = F.mul(
                    F.mul(F.sub(t, F.mul_int(x2, 2)), F.sub_int(x, 1)),
                    F.pow(F.add_int(x, 1), 2),
                )
                if u_den == 0:
                    continue

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
                if not beta_roots:
                    continue

                for beta in beta_roots:
                    x5_num = F.add(u_num, F.mul(beta, u_den))
                    x5 = F.div(x5_num, F.mul_int(u_den, 2))
                    d_next = F.add(F.add(F.sq(x5), F.mul(a, x5)), F.elt(1))
                    for sd in F.roots_square(d_next):
                        unext = F.add(F.mul_int(x5, 2), F.mul_int(sd, 2))
                        selector = F.add_int(unext, 2)
                        rows.append((x, w, t, beta, bline, x5, unext, selector))
    return rows


def run_field(p: int, n: int) -> None:
    F = GF(p, n)
    rows = enumerate_points(F)
    stats: Counter = Counter()
    vector_stats: Counter = Counter()
    selector_stats: Counter = Counter()

    for x, w, t, beta, bline, x5, unext, selector in rows:
        degrees = {
            "X": element_degree(F, x),
            "W": element_degree(F, w),
            "T": element_degree(F, t),
            "beta": element_degree(F, beta),
            "B": element_degree(F, bline),
            "x5": element_degree(F, x5),
            "U": element_degree(F, unext),
            "selector": element_degree(F, selector),
        }
        point_degree = lcm(list(degrees.values()))
        source = extension_source(degrees["B"], point_degree)
        gamma_chi = F.legendre(selector)

        stats["points"] += 1
        stats[f"point_degree_{point_degree}"] += 1
        stats[f"B_degree_{degrees['B']}"] += 1
        stats[f"source_{source}"] += 1
        stats[f"gamma_chi_{gamma_chi}"] += 1
        stats[f"source_{source}_gamma_{gamma_chi}"] += 1
        vector = (
            degrees["B"],
            degrees["X"],
            degrees["W"],
            degrees["T"],
            degrees["beta"],
            degrees["x5"],
            degrees["U"],
            degrees["selector"],
            point_degree,
            gamma_chi,
        )
        vector_stats[vector] += 1
        selector_stats[(degrees["B"], point_degree, gamma_chi)] += 1

    print(f"GF({p}^{n}) q={F.q}")
    print(f"  noR_U_points = {len(rows)}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  degree_vector_top:")
    print("    columns = B X W T beta x5 U selector point gamma_chi")
    for vector, count in vector_stats.most_common(20):
        print(f"    {vector} = {count}")
    print("  B_point_gamma_top:")
    for vector, count in selector_stats.most_common(20):
        print(f"    {vector} = {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="7^2,7^3,23^2,23^3")
    args = parser.parse_args()

    print("p27 B-line no-R coordinate-degree probe")
    print("columns = B, X, W, T, beta, x5, U, selector, full point degree")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_coordinate_degree_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
