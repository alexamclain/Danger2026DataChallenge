#!/usr/bin/env python3
"""Identify the BSM surface with the ordinary halving cover.

The staged BSM surface is

    m^2*(B^2+s^2-4) = 4*s^2*(s^2-4).

Set

    A = B^2 - 2,
    x = m^2/16,
    z = s^2.

Then the BSM equation becomes

    z^2 - 4*(x+1)*z - 4*x*(B^2-4) = 0,

whose discriminant in z is

    16*(x^2 + A*x + 1).

So a nondegenerate BSM point is exactly an x-square plus halving-discriminant
square point for E_A, with extra sign choices.  This probe validates the
identity and fiber counts on the p27 guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_bsm_surface_incidence_probe import legal_b_data, parse_ints
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, sqrt_table
from p27_label2_alpha_branch_recurrence_probe import legendre


def bsm_identity_stats(p: int) -> Counter:
    roots = sqrt_table(p)
    invs = inv_table(p)
    data, data_stats = legal_b_data(p)
    legal_bax = data["legal_bax"]
    d3plus_bax = data["d3plus_bax"]
    d3minus_bax = data["d3minus_bax"]
    inv16 = invs[16 % p]
    stats: Counter = Counter({f"data_{key}": value for key, value in data_stats.items()})
    by_bax: Counter = Counter()
    legal_by_bax: Counter = Counter()
    d3plus_by_bax: Counter = Counter()
    d3minus_hits: Counter = Counter()

    for B in range(p):
        B2 = B * B % p
        A = (B2 - 2) % p
        for s in range(p):
            z = s * s % p
            den = (B2 + z - 4) % p
            rhs = 4 * z % p * ((z - 4) % p) % p
            if den == 0:
                if rhs == 0:
                    stats["degenerate_den0_rhs0"] += 1
                else:
                    stats["degenerate_den0_rhs_nonzero"] += 1
                continue
            m2 = rhs * invs[den] % p
            for m in roots[m2]:
                if m == 0:
                    stats["skip_m0"] += 1
                    continue
                x = m * m % p * inv16 % p
                d = (x * x + A * x + 1) % p
                quad = (z * z - 4 * (x + 1) * z - 4 * x * (B2 - 4)) % p
                discr = 16 * d % p
                discr_from_z = (z - 2 * (x + 1)) ** 2 % p
                if quad:
                    stats["quadratic_identity_fail"] += 1
                if discr_from_z != 4 * d % p:
                    stats["z_discriminant_identity_fail"] += 1
                if legendre(x, p) != 1:
                    stats["x_not_square"] += 1
                if legendre(d, p) != 1:
                    stats["d_not_square"] += 1
                if legendre(discr, p) != 1:
                    stats["discriminant_not_square"] += 1

                bax = (B, A, x)
                by_bax[bax] += 1
                stats["bsm_points"] += 1
                if bax in legal_bax:
                    legal_by_bax[bax] += 1
                    stats["legal_bax_points"] += 1
                if bax in d3plus_bax:
                    d3plus_by_bax[bax] += 1
                    stats["d3plus_bax_points"] += 1
                if bax in d3minus_bax:
                    d3minus_hits[bax] += 1
                    stats["d3minus_bax_points"] += 1

    stats["unique_bax"] = len(by_bax)
    stats["unique_legal_bax_hit"] = len(legal_by_bax)
    stats["unique_d3plus_bax_hit"] = len(d3plus_by_bax)
    stats["unique_d3minus_bax_hit"] = len(d3minus_hits)
    for count, rows in Counter(by_bax.values()).items():
        stats[f"all_bax_fiber_{count}"] = rows
    for count, rows in Counter(legal_by_bax.values()).items():
        stats[f"legal_bax_fiber_{count}"] = rows
    for count, rows in Counter(d3plus_by_bax.values()).items():
        stats[f"d3plus_bax_fiber_{count}"] = rows
    for count, rows in Counter(d3minus_hits.values()).items():
        stats[f"d3minus_bax_fiber_{count}"] = rows
    for key in (
        "quadratic_identity_fail",
        "z_discriminant_identity_fail",
        "x_not_square",
        "d_not_square",
        "discriminant_not_square",
        "d3minus_bax_points",
    ):
        stats.setdefault(key, 0)
    return stats


def print_counter(prefix: str, p: int, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    if stats["bsm_points"]:
        print(f"  bsm_points_per_q2 = {stats['bsm_points'] / (p * p):.9f}")
    if stats["data_d3plus_ax"]:
        print(f"  d3plus_bsm_points_per_d3plus_ax = {stats['d3plus_bax_points'] / stats['data_d3plus_ax']:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 BSM halving-cover identity probe")
    print("surface = m^2*(B^2+s^2-4)=4*s^2*(s^2-4)")
    print("substitution = A=B^2-2, x=m^2/16, z=s^2")
    print("identity = z^2 - 4*(x+1)*z - 4*x*(B^2-4)=0")
    print("discriminant = 16*(x^2+A*x+1)")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", p, bsm_identity_stats(p))
    print("p27_bsm_halving_cover_identity_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
