#!/usr/bin/env python3
"""P27 S-map pair-resolvent screen.

The S-map quartic

    F(Y) = 0,  Y = S_next^2

has four roots after d3.  The previous probe showed that d4 is the common
squareclass of those roots, while the visible quartic factors are flat.

This probe tests a sharper resolvent.  Pair the quartic roots using the
available d3 square roots:

    S^2 = x + 1/x + 2
    E^2 = S^2 - 4
    M = 2*S*E

Then one quadratic factor is:

    Y^2 + a1*Y + B
    a1 = -2*S^2 + M

For a quadratic pair with square product B, the common root squareclass is:

    chi(-a1 + 2*sqrt(B)).

This is a real recurrence candidate only if it is sign-independent and agrees
with d4 over p27 and guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, inv, legendre, sample_rows, sqrt_mod
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def quartic_c2_c1(a: int, s2: int, p: int) -> tuple[int, int]:
    return (
        (-4 * a * s2 + 8 * a + 24 * s2 - 16) % p,
        (16 * a * s2 - 32 * s2) % p,
    )


def pair_resolvent_chars(a: int, s2: int, p: int) -> tuple[set[int], Counter]:
    """Return possible resolvent squareclasses over all sign choices."""

    stats: Counter = Counter()
    s_root = sqrt_mod(s2, p)
    e_root = sqrt_mod(s2 - 4, p)
    if s_root is None:
        stats["S2_nonsquare"] += 1
        return set(), stats
    if e_root is None:
        stats["S2_minus_4_nonsquare"] += 1
        return set(), stats

    c2, c1 = quartic_c2_c1(a, s2, p)
    chars: set[int] = set()
    roots_s = [s_root, (-s_root) % p] if s_root else [0]
    roots_e = [e_root, (-e_root) % p] if e_root else [0]
    for s in roots_s:
        for e in roots_e:
            m = 2 * s % p * e % p
            if m == 0:
                stats["zero_M"] += 1
                continue
            a1 = (-2 * s2 + m) % p
            a2 = (-2 * s2 - m) % p
            denom = (a2 - a1) % p
            if denom == 0:
                stats["zero_pair_denominator"] += 1
                continue
            sum_bc = (c2 - a1 * a2) % p
            # From B+C=sum_bc and a1*C+a2*B=c1.
            b = (c1 - a1 * sum_bc) % p * inv(denom, p) % p
            c = (sum_bc - b) % p
            if (b * c - 16 * (a - 2) * (a - 2)) % p:
                stats["pair_product_mismatch"] += 1
                continue
            beta = sqrt_mod(b, p)
            if beta is None:
                stats["B_nonsquare"] += 1
                continue
            stats["B_square"] += 1
            beta_roots = [beta, (-beta) % p] if beta else [0]
            local_chars = {legendre((-a1 + 2 * beta_i) % p, p) for beta_i in beta_roots}
            local_chars.discard(0)
            if len(local_chars) != 1:
                stats["beta_sign_changes_class"] += 1
            chars.update(local_chars)
    if not chars:
        stats["no_resolvent_chars"] += 1
    elif len(chars) == 1:
        stats["sign_independent_resolvent"] += 1
    else:
        stats["sign_dependent_resolvent"] += 1
    return chars, stats


def collect_p27(target: int, seed: int, max_draws: int) -> Counter:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    for row in rows:
        cand = row["root0"]
        assert isinstance(cand, dict)
        a = int(cand["A"])
        x5 = int(cand["x5"])
        _, x6s = halve_all(a, x5, P)
        d3 = normalize_pm1([legendre(x6, P) for x6 in x6s])
        if d3 != 1:
            stats["d3_not_plus"] += 1
            continue
        x6 = int(x6s[0])
        s2 = (x6 + inv(x6, P) + 2) % P
        _, x7s = halve_all(a, x6, P)
        d4 = normalize_pm1([legendre(x7, P) for x7 in x7s])
        if d4 not in (-1, 1):
            stats["d4_unusable"] += 1
            continue
        chars, row_stats = pair_resolvent_chars(a, s2, P)
        stats.update(row_stats)
        stats["rows"] += 1
        stats[f"d4_{d4}"] += 1
        if len(chars) == 1:
            value = next(iter(chars))
            stats[f"resolvent_{value}"] += 1
            if value == d4:
                stats["resolvent_matches_d4"] += 1
            else:
                stats["resolvent_mismatch_d4"] += 1
        elif d4 in chars:
            stats["resolvent_contains_d4"] += 1
        else:
            stats["resolvent_misses_d4"] += 1
    return stats


def collect_small_field(q: int) -> Counter:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in candidates:
        bits = candidate_bits(cand, q)
        if bits.d3 != 1 or bits.d4 not in (-1, 1):
            continue
        a = int(cand["A"])
        x5 = int(cand["x5"])
        _, x6s = halve_all(a, x5, q)
        if not x6s:
            stats["no_x6"] += 1
            continue
        x6 = int(x6s[0])
        s2 = (x6 + inv(x6, q) + 2) % q
        chars, row_stats = pair_resolvent_chars(a, s2, q)
        stats.update(row_stats)
        stats["rows"] += 1
        stats[f"d4_{bits.d4}"] += 1
        if len(chars) == 1:
            value = next(iter(chars))
            stats[f"resolvent_{value}"] += 1
            if value == bits.d4:
                stats["resolvent_matches_d4"] += 1
            else:
                stats["resolvent_mismatch_d4"] += 1
        elif bits.d4 in chars:
            stats["resolvent_contains_d4"] += 1
        else:
            stats["resolvent_misses_d4"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    rows = stats["rows"]
    if rows:
        print(f"  match_rate = {stats['resolvent_matches_d4'] / rows:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=2500000)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 S-map pair-resolvent probe")
    print("quadratic_pair = Y^2 + a1*Y + B")
    print("a1 = -2*S^2 + 2*S*E, E^2=S^2-4")
    print("root_squareclass = chi(-a1 + 2*sqrt(B))")

    print_counter("p27_train", collect_p27(args.target, args.seed, args.max_draws))
    print_counter("p27_heldout", collect_p27(args.target, args.heldout_seed, args.max_draws))
    print("small_field_pair_resolvent_screens:")
    for q in parse_ints(args.small_primes):
        print_counter(f"q{q}", collect_small_field(q))

    print("p27_smap_pair_resolvent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
