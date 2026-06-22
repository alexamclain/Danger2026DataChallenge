#!/usr/bin/env python3
"""Reciprocal quotient screen for the p27 E-prime d3 z-source.

The staged E-prime z-source has a reciprocal equation in s=z^2.  Setting

    r = s + 1/s

gives a quadratic quotient over the saturated first-half layer.  This probe
checks what that quotient remembers on actual p27 and guard-field rows.

Expected structural alternatives:

* If the r-quotient discriminant is the d3 bit, the quotient names a useful
  branch class directly.
* If the quotient is always solvable after d2 and d3 is only chi(r+2), then
  r has quotiented away exactly the squareclass we need.  The route is still
  useful as a normalization target, but not as a source shortcut by itself.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, inv, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates


def roots_mod(a: int, p: int) -> list[int]:
    a %= p
    if a == 0:
        return [0]
    if legendre(a, p) != 1:
        return []
    r = pow(a, (p + 1) // 4, p) if p % 4 == 3 else None
    if r is None or r * r % p != a:
        # Small guard fields in this lane are 7 mod 8, hence 3 mod 4.
        raise ValueError(f"sqrt path unavailable for p={p}")
    return [r, (-r) % p] if r else [0]


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def eprime_terms(cand: dict[str, int], p: int) -> dict[str, int] | None:
    x = int(cand["X"]) % p
    w = int(cand["W"]) % p
    t = int(cand["T"]) % p
    x5 = int(cand["x5"]) % p
    if x in (0, 1, p - 1):
        return None

    x2 = x * x % p
    x3 = x2 * x % p
    x4 = x2 * x2 % p
    x5p = x4 * x % p
    x6 = x5p * x % p
    x8 = x4 * x4 % p
    d = (x2 + 1) % p
    if d == 0:
        return None

    # In the E' quotient Wnum = V*X^2 equals W*(X^2+1).
    wnum = w * d % p
    u_core = (
        4 * t * wnum * x
        + d
        * (
            t * x3
            + t * x2
            - t * x
            - t
            + 2 * x5p
            + 2 * x4
            - 2 * x3
            - 2 * x2
        )
    ) % p
    u_num_scaled = 2 * u_core % p
    u_den = (t - 2 * x2) % p
    u_den = u_den * (x - 1) % p * pow((x + 1) % p, 2, p) % p
    lterm = u_den * d % p
    a_den = pow((x - 1) % p, 4, p) * pow((x + 1) % p, 4, p) % p
    a_num = -2 * (x8 - 4 * x6 - 26 * x4 - 4 * x2 + 1) % p
    if lterm == 0 or a_den == 0:
        return None

    # The first-half branch convention has
    #   C = U_num_scaled + B*U_den*D = 2*U_den*D*x5.
    cterm = 2 * lterm * x5 % p

    # Discriminant of
    #   2*C*(A_den*r + A_num) - U_den*D*A_den*(r^2 - 4)
    ar = -lterm * a_den % p
    br = 2 * cterm * a_den % p
    cr = (2 * cterm * a_num + 4 * lterm * a_den) % p
    disc = (br * br - 4 * ar * cr) % p

    # Simplified branch core after using the first-half equation.  It should
    # have the same squareclass as disc up to a global square factor.
    disc_core = lterm * x5 % p
    disc_core = disc_core * (a_den * u_num_scaled + lterm * a_num) % p

    return {
        "x5": x5,
        "disc": disc,
        "disc_core": disc_core,
    }


def candidate_d3_and_r(cand: dict[str, int], p: int) -> tuple[int | None, list[int], Counter]:
    stats: Counter = Counter()
    terms = eprime_terms(cand, p)
    if terms is None:
        stats["term_degenerate"] += 1
        return None, [], stats

    a = int(cand["A"])
    x5 = int(cand["x5"])
    d2_chi, x6s = halve_all(a, x5, p)
    if d2_chi != 1 or not x6s:
        stats["d2_not_square"] += 1
        return None, [], stats

    d3_values = [legendre(x6, p) for x6 in x6s]
    d3 = normalize_pm1(d3_values)
    if d3 not in (-1, 1):
        stats["d3_not_normalized"] += 1
        return None, [], stats

    r_values = sorted({(x6 + inv(x6, p)) % p for x6 in x6s if x6 % p})
    if not r_values:
        stats["no_r_values"] += 1
    elif len(r_values) != 1:
        stats["multiple_r_values"] += 1

    r = r_values[0] if len(r_values) == 1 else None
    if r is not None:
        if legendre(r + 2, p) == d3:
            stats["r_plus_2_matches_d3"] += 1
        else:
            stats["r_plus_2_mismatch_d3"] += 1
        if legendre(r - 2, p) == d3:
            stats["r_minus_2_matches_d3"] += 1
        else:
            stats["r_minus_2_mismatch_d3"] += 1

    disc_chi = legendre(terms["disc"], p)
    core_chi = legendre(terms["disc_core"], p)
    if disc_chi == 1:
        stats["r_discriminant_square"] += 1
    elif disc_chi == -1:
        stats["r_discriminant_nonsquare"] += 1
    else:
        stats["r_discriminant_zero"] += 1
    if disc_chi == core_chi:
        stats["disc_core_same_squareclass"] += 1
    else:
        stats["disc_core_diff_squareclass"] += 1
    if disc_chi == d3:
        stats["r_discriminant_matches_d3"] += 1
    else:
        stats["r_discriminant_mismatch_d3"] += 1

    return d3, r_values, stats


def dedupe_candidates(candidates: list[dict[str, int]]) -> list[dict[str, int]]:
    seen: set[tuple[int, int, int, int, int]] = set()
    out: list[dict[str, int]] = []
    for cand in candidates:
        key = (
            int(cand["X"]),
            int(cand["W"]),
            int(cand["T"]),
            int(cand["A"]),
            int(cand["x5"]),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(cand)
    return out


def analyze(label: str, candidates: list[dict[str, int]], p: int) -> Counter:
    stats: Counter = Counter()
    for cand in dedupe_candidates(candidates):
        stats["candidates"] += 1
        d3, r_values, cstats = candidate_d3_and_r(cand, p)
        stats.update(cstats)
        if d3 == 1:
            stats["d3_plus"] += 1
        elif d3 == -1:
            stats["d3_minus"] += 1
        if len(r_values) == 1:
            stats["single_r_value"] += 1
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    usable = stats["d3_plus"] + stats["d3_minus"]
    if usable:
        print(f"  d3_plus_rate = {stats['d3_plus'] / usable:.9f}")
        print(f"  r_discriminant_square_rate = {stats['r_discriminant_square'] / usable:.9f}")
        print(f"  r_plus_2_match_rate = {stats['r_plus_2_matches_d3'] / usable:.9f}")
    return stats


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 E-prime reciprocal r-quotient branch probe")
    print("r = z^2 + z^-2")
    print(f"p = {P}")

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    train_candidates: list[dict[str, int]] = []
    for row in rows:
        train_candidates.extend(all_oriented_candidates_from_row(row, P))
    print("p27_train_sample_stats:")
    for key in sorted(sample_stats):
        print(f"  {key} = {sample_stats[key]}")
    analyze("p27_train", train_candidates, P)

    rows_h, sample_stats_h = sample_rows(args.target, args.heldout_seed, args.max_draws)
    held_candidates: list[dict[str, int]] = []
    for row in rows_h:
        held_candidates.extend(all_oriented_candidates_from_row(row, P))
    print("p27_heldout_sample_stats:")
    for key in sorted(sample_stats_h):
        print(f"  {key} = {sample_stats_h[key]}")
    analyze("p27_heldout", held_candidates, P)

    print("small_prime_rquotient_branch_screens:")
    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print(f"q={q}:")
        for key in sorted(enum_stats):
            print(f"  enum_{key} = {enum_stats[key]}")
        analyze(f"q{q}", candidates, q)

    print("p27_eprime_rquotient_branch_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
