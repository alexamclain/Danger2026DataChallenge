#!/usr/bin/env python3
"""Point-count the p27 B-line reduced d3 cover over prime fields.

The online Magma saturation for the reduced cover is too heavy, but the cover
is a nested sequence of quadratic equations.  This probe counts the affine
eta=+1 chart directly over small prime fields and separates:

  * legal first-half chart points,
  * reduced U_next roots satisfying
        (U_next - 2*x5)^2 = 4*(x5^2 + A*x5 + 1),
  * materializable x6 roots with x6 + 1/x6 = U_next,
  * selector roots gamma^2 = U_next + 2.

This is not a replacement for normalization.  It is a cheap falsifier/guard:
if the reduced U cover contains many nonmaterializable U branches, offline CAS
should normalize the materialized x6 or selector cover rather than only the
U-cover.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict


DEFAULT_PRIMES = "7,23,103,607,1607,1847,2087"


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def sqrt_mod(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
        return None
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return r if r * r % p == a else None

    # Tonelli-Shanks fallback for any odd prime used in ad hoc replay.
    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while legendre(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        t2i = t * t % p
        while t2i != 1:
            t2i = t2i * t2i % p
            i += 1
            if i == m:
                return None
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r if r * r % p == a else None


def roots_mod(a: int, p: int) -> list[int]:
    r = sqrt_mod(a, p)
    if r is None:
        return []
    if r == 0:
        return [0]
    return [r, (-r) % p]


def roots_x_plus_inv(unext: int, p: int) -> list[int]:
    """Return roots of x^2 - unext*x + 1 over F_p."""

    disc = (unext * unext - 4) % p
    sd = sqrt_mod(disc, p)
    if sd is None:
        return []
    inv2 = inv(2, p)
    roots = [((unext + sd) * inv2) % p]
    other = ((unext - sd) * inv2) % p
    if other != roots[0]:
        roots.append(other)
    return roots


def source_b_plus(x: int, p: int) -> int | None:
    den = (x * x - 1) % p
    if den == 0:
        return None
    return 8 * x * x % p * inv(den * den, p) % p


def field_rows(p: int) -> tuple[Counter, dict[int, Counter]]:
    stats: Counter = Counter()
    by_b: defaultdict[int, Counter] = defaultdict(Counter)
    eta = 1
    for x in range(p):
        x2 = x * x % p
        x3 = x2 * x % p
        x4 = x2 * x2 % p
        x5_pow = x4 * x % p
        x6_pow = x5_pow * x % p
        x8 = x4 * x4 % p

        if x == 0 or x in (1, p - 1) or (x2 + 1) % p == 0:
            stats["bad_X_denominator"] += 1
            continue

        bline = source_b_plus(x, p)
        if bline is None:
            stats["bad_Bline"] += 1
            continue

        a_den = pow(x - 1, 4, p) * pow(x + 1, 4, p) % p
        if a_den == 0:
            stats["bad_A_den"] += 1
            continue
        a_num = -2 * ((x8 - 4 * x6_pow - 26 * x4 - 4 * x2 + 1) % p) % p
        a = a_num * inv(a_den, p) % p

        t2 = x * ((x2 + 1) % p) % p
        t2 = t2 * ((x2 + 2 * x - 1) % p) % p
        for w in roots_mod((x3 - x) % p, p):
            for t in roots_mod(t2, p):
                u_den = (t - 2 * x2) % p
                u_den = u_den * (x - 1) % p * pow(x + 1, 2, p) % p
                if u_den == 0:
                    stats["bad_U_den"] += 1
                    continue

                mt = (2 * w * x2 + 2 * w * x + x4 + 2 * x3 - 2 * x - 1) % p
                m0 = (
                    w * x5_pow
                    + 3 * w * x4
                    + 2 * w * x3
                    + 2 * w * x2
                    + w * x
                    - w
                    + 2 * x6_pow
                    + 4 * x5_pow
                    + 4 * x3
                    - 2 * x2
                ) % p
                criterion_num = w * ((x2 + 1) % p) % p * ((m0 + mt * t) % p) % p
                r_roots = roots_mod(criterion_num * inv(x, p), p)
                if not r_roots:
                    stats["compactD_not_square"] += 1
                    continue

                u_core = (
                    eta * 4 * t * w * x
                    + t * x3
                    + t * x2
                    - t * x
                    - t
                    + 2 * x5_pow
                    + 2 * x4
                    - 2 * x3
                    - 2 * x2
                ) % p
                u_num = 2 * u_core % p
                beta_rhs = (u_num * u_num - 4 * u_den * u_den) % p
                beta_rhs = beta_rhs * inv(u_den * u_den, p) % p
                beta_roots = roots_mod(beta_rhs, p)
                if not beta_roots:
                    stats["first_half_beta_not_square"] += 1
                    continue

                for r in r_roots:
                    stats["legal_R_points"] += 1
                    by_b[bline]["legal_R_points"] += 1
                    # R is present only for point-count multiplicity.  It does
                    # not change beta, U_next, x6, or selector values.
                    _ = r
                    for beta in beta_roots:
                        stats["legal_chart_points"] += 1
                        by_b[bline]["legal_chart_points"] += 1
                        x5_num = (u_num + beta * u_den) % p
                        x5 = x5_num * inv(2 * u_den, p) % p
                        d_next = (x5 * x5 + a * x5 + 1) % p
                        sd_next = sqrt_mod(d_next, p)
                        if sd_next is None:
                            stats["reduced_U_no_root"] += 1
                            by_b[bline]["reduced_U_no_root"] += 1
                            continue
                        for sign, sd in [(1, sd_next), (-1, (-sd_next) % p)]:
                            if sd_next == 0 and sign == -1:
                                continue
                            unext = (2 * x5 + 2 * sd) % p
                            stats["reduced_U_points"] += 1
                            by_b[bline]["reduced_U_points"] += 1
                            x6_roots = roots_x_plus_inv(unext, p)
                            stats[f"U_materialization_roots_{len(x6_roots)}"] += 1
                            by_b[bline][f"U_materialization_roots_{len(x6_roots)}"] += 1
                            selector = (unext + 2) % p
                            selector_chi = legendre(selector, p)
                            stats[
                                f"U_materialization_roots_{len(x6_roots)}_selector_chi_{selector_chi}"
                            ] += 1
                            by_b[bline][
                                f"U_materialization_roots_{len(x6_roots)}_selector_chi_{selector_chi}"
                            ] += 1
                            stats[f"selector_chi_{selector_chi}"] += 1
                            by_b[bline][f"selector_chi_{selector_chi}"] += 1
                            gamma_roots = roots_mod(selector, p)
                            stats["selector_gamma_points"] += len(gamma_roots)
                            by_b[bline]["selector_gamma_points"] += len(gamma_roots)
                            if selector_chi == 1:
                                stats["materialized_x6_from_selector_plus_U"] += len(x6_roots)
                                by_b[bline]["materialized_x6_from_selector_plus_U"] += len(x6_roots)
                            elif selector_chi == -1:
                                stats["materialized_x6_from_selector_minus_U"] += len(x6_roots)
                                by_b[bline]["materialized_x6_from_selector_minus_U"] += len(x6_roots)
                            for x6 in x6_roots:
                                stats["materialized_x6_points"] += 1
                                by_b[bline]["materialized_x6_points"] += 1
                                x6_chi = legendre(x6, p)
                                stats[f"x6_chi_{x6_chi}"] += 1
                                if x6_chi != selector_chi:
                                    stats["selector_x6_mismatch"] += 1

    return stats, dict(by_b)


def print_ratio(stats: Counter, numerator: str, denominator: str) -> None:
    den = stats[denominator]
    value = stats[numerator] / den if den else 0.0
    print(f"  {numerator}_per_{denominator} = {value:.9f}")


def summarize_b_fibers(by_b: dict[int, Counter]) -> Counter:
    out: Counter = Counter()
    for row in by_b.values():
        for key in [
            "legal_chart_points",
            "reduced_U_points",
            "materialized_x6_points",
            "selector_gamma_points",
        ]:
            out[f"{key}_fiber_{row[key]}"] += 1
        pair = (row["reduced_U_points"], row["materialized_x6_points"])
        out[f"U_x6_fiber_pair_{pair}"] += 1
        sel_pair = (row["selector_chi_1"], row["selector_chi_-1"])
        out[f"selector_pm_fiber_pair_{sel_pair}"] += 1
    return out


def run_field(p: int) -> None:
    stats, by_b = field_rows(p)
    fiber_stats = summarize_b_fibers(by_b)
    stats["B_fibers"] = len(by_b)

    print(f"q={p}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for numerator, denominator in [
        ("reduced_U_points", "legal_chart_points"),
        ("materialized_x6_points", "legal_chart_points"),
        ("selector_gamma_points", "reduced_U_points"),
        ("materialized_x6_points", "reduced_U_points"),
    ]:
        print_ratio(stats, numerator, denominator)
    print("  fiber_summary:")
    for key in sorted(fiber_stats):
        print(f"    {key} = {fiber_stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default=DEFAULT_PRIMES)
    args = parser.parse_args()

    print("p27 B-line reduced-cover pointcount probe")
    print("chart = eta_plus")
    print(f"small_primes = {args.small_primes}")
    for p in parse_ints(args.small_primes):
        run_field(p)
    print("p27_b_line_reduced_cover_pointcount_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
