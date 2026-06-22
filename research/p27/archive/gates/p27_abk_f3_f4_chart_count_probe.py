#!/usr/bin/env python3
"""Point-count the staged p27 A/B/K f3 -> f4 chart over prime fields.

The symbolic CAS brief asks offline Magma/Sage to normalize the staged tower

    reduced U cover,
    H^2 = U + 2,
    F_A(U,V) = 0,
    gamma^2 = V + 2.

This probe is a cheap finite-field guard for that request.  It does not
normalize the curve.  It counts the nested equations directly over prime
fields and asks whether the f4/f3 gamma layer looks sourceable or like a fresh
half-cover after the f3-plus cut.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache

from p27_b_line_reduced_cover_pointcount_probe import inv, legendre, roots_mod, source_b_plus


DEFAULT_PRIMES = "7,23,103,607,1607,1847,2087"


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def fnext_value(a: int, u: int, v: int, p: int) -> int:
    v2m4 = (v * v - 4) % p
    return (
        v2m4 * v2m4
        - 4 * u * v2m4 * ((v + a) % p)
        + 16 * ((v + a) % p) * ((v + a) % p)
    ) % p


@lru_cache(maxsize=None)
def fnext_roots(p: int, a: int, u: int) -> tuple[int, ...]:
    return tuple(v for v in range(p) if fnext_value(a, u, v, p) == 0)


def row_counts(p: int, compactd: bool) -> tuple[Counter, dict[int, Counter]]:
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
        if (a + 2 - bline * bline) % p:
            stats["A_B_identity_mismatch"] += 1

        t2 = x * ((x2 + 1) % p) % p
        t2 = t2 * ((x2 + 2 * x - 1) % p) % p
        for w in roots_mod((x3 - x) % p, p):
            for t in roots_mod(t2, p):
                u_den = (t - 2 * x2) % p
                u_den = u_den * (x - 1) % p * pow(x + 1, 2, p) % p
                if u_den == 0:
                    stats["bad_U_den"] += 1
                    continue

                if compactd:
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
                    compact_multiplicity = len(r_roots)
                else:
                    compact_multiplicity = 1

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

                for beta in beta_roots:
                    stats["legal_chart_points"] += compact_multiplicity
                    by_b[bline]["legal_chart_points"] += compact_multiplicity
                    x5_num = (u_num + beta * u_den) % p
                    x5 = x5_num * inv(2 * u_den, p) % p
                    d_next = (x5 * x5 + a * x5 + 1) % p
                    sd_roots = roots_mod(d_next, p)
                    if not sd_roots:
                        stats["reduced_U_no_root"] += compact_multiplicity
                        by_b[bline]["reduced_U_no_root"] += compact_multiplicity
                        continue

                    for sd in sd_roots:
                        unext = (2 * x5 + 2 * sd) % p
                        h_roots = roots_mod((unext + 2) % p, p)
                        stats["reduced_U_points"] += compact_multiplicity
                        by_b[bline]["reduced_U_points"] += compact_multiplicity
                        stats[f"H_roots_{len(h_roots)}"] += compact_multiplicity
                        by_b[bline][f"H_roots_{len(h_roots)}"] += compact_multiplicity
                        if not h_roots:
                            stats["f3_minus_U"] += compact_multiplicity
                            by_b[bline]["f3_minus_U"] += compact_multiplicity
                            continue

                        stats["f3_plus_U"] += compact_multiplicity
                        by_b[bline]["f3_plus_U"] += compact_multiplicity
                        v_roots = fnext_roots(p, a, unext)
                        stats[f"V_roots_{len(v_roots)}"] += compact_multiplicity
                        by_b[bline][f"V_roots_{len(v_roots)}"] += compact_multiplicity
                        stats["H_points"] += compact_multiplicity * len(h_roots)
                        by_b[bline]["H_points"] += compact_multiplicity * len(h_roots)
                        stats["HV_points"] += compact_multiplicity * len(h_roots) * len(v_roots)
                        by_b[bline]["HV_points"] += compact_multiplicity * len(h_roots) * len(v_roots)

                        gamma_signs: set[int] = set()
                        for v in v_roots:
                            gamma_chi = legendre(v + 2, p)
                            gamma_signs.add(gamma_chi)
                            stats[f"gamma_chi_{gamma_chi}"] += compact_multiplicity * len(h_roots)
                            by_b[bline][f"gamma_chi_{gamma_chi}"] += compact_multiplicity * len(h_roots)
                            gamma_roots = roots_mod((v + 2) % p, p)
                            stats["gamma_points"] += compact_multiplicity * len(h_roots) * len(gamma_roots)
                            by_b[bline]["gamma_points"] += compact_multiplicity * len(h_roots) * len(gamma_roots)
                        sign_key = tuple(sorted(gamma_signs))
                        stats[f"V_gamma_sign_set_{sign_key}"] += compact_multiplicity
                        by_b[bline][f"V_gamma_sign_set_{sign_key}"] += compact_multiplicity

    for key in [
        "A_B_identity_mismatch",
        "bad_A_den",
        "bad_Bline",
        "bad_U_den",
        "compactD_not_square",
        "first_half_beta_not_square",
        "reduced_U_no_root",
    ]:
        stats.setdefault(key, 0)
    return stats, dict(by_b)


def ratio(stats: Counter, num: str, den: str) -> float:
    return stats[num] / stats[den] if stats[den] else 0.0


def summarize_by_b(by_b: dict[int, Counter]) -> Counter:
    out: Counter = Counter()
    for row in by_b.values():
        out[f"f3_pm_pair_{(row['f3_plus_U'], row['f3_minus_U'])}"] += 1
        out[f"HV_gamma_pair_{(row['HV_points'], row['gamma_points'])}"] += 1
        out[f"gamma_pm_pair_{(row['gamma_chi_1'], row['gamma_chi_-1'])}"] += 1
        for key, value in row.items():
            if key.startswith("V_roots_") or key.startswith("V_gamma_sign_set_"):
                out[f"{key}_Bcount_nonzero"] += int(value > 0)
    return out


def add_b_class_stats(stats: Counter, by_b: dict[int, Counter]) -> None:
    for row in by_b.values():
        plus = row["f3_plus_U"]
        minus = row["f3_minus_U"]
        if plus and not minus:
            prefix = "B_f3_plus_only"
        elif minus and not plus:
            prefix = "B_f3_minus_only"
        elif plus and minus:
            prefix = "B_f3_mixed"
        else:
            prefix = "B_f3_empty"
        stats[prefix] += 1
        for key in [
            "f3_plus_U",
            "f3_minus_U",
            "HV_points",
            "gamma_points",
            "gamma_chi_1",
            "gamma_chi_-1",
            "gamma_chi_0",
        ]:
            stats[f"{prefix}_{key}"] += row[key]


def print_counter(prefix: str, stats: Counter, limit: int | None = None) -> None:
    print(f"{prefix}:")
    items = stats.most_common(limit) if limit else sorted(stats.items())
    if limit:
        for key, value in items:
            print(f"  {key} = {value}")
        omitted = len(stats) - min(len(stats), limit)
        if omitted:
            print(f"  omitted_distinct_keys = {omitted}")
    else:
        for key, value in items:
            print(f"  {key} = {value}")


def run_field(p: int, compactd: bool, fiber_limit: int) -> None:
    label = "compactD" if compactd else "noR"
    stats, by_b = row_counts(p, compactd)
    stats["B_fibers"] = len(by_b)
    add_b_class_stats(stats, by_b)

    print(f"q={p} mode={label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for num, den in [
        ("reduced_U_points", "legal_chart_points"),
        ("f3_plus_U", "reduced_U_points"),
        ("HV_points", "f3_plus_U"),
        ("gamma_points", "HV_points"),
        ("gamma_chi_1", "HV_points"),
        ("gamma_chi_-1", "HV_points"),
        ("B_f3_plus_only_gamma_chi_1", "B_f3_plus_only_HV_points"),
        ("B_f3_plus_only_gamma_chi_-1", "B_f3_plus_only_HV_points"),
        ("B_f3_plus_only_gamma_points", "B_f3_plus_only_HV_points"),
    ]:
        print(f"  {num}_per_{den} = {ratio(stats, num, den):.9f}")
    print_counter(f"q={p} mode={label} fiber_summary_top", summarize_by_b(by_b), fiber_limit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default=DEFAULT_PRIMES)
    parser.add_argument("--modes", default="noR,compactD")
    parser.add_argument("--fiber-limit", type=int, default=20)
    args = parser.parse_args()

    modes = {part.strip() for part in args.modes.split(",") if part.strip()}
    print("p27 ABK f3/f4 chart count probe")
    print("chart = reduced_U, H^2=U+2, F_A(U,V)=0, gamma^2=V+2")
    print(f"fields = {args.small_primes}")
    print(f"modes = {','.join(sorted(modes))}")
    print("question = is f4/f3 gamma sourceable or another fresh half-cover?")
    for p in parse_ints(args.small_primes):
        if "noR" in modes:
            run_field(p, compactd=False, fiber_limit=args.fiber_limit)
        if "compactD" in modes:
            run_field(p, compactd=True, fiber_limit=args.fiber_limit)
    print("p27_abk_f3_f4_chart_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
