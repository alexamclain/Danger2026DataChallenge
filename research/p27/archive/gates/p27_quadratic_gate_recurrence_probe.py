#!/usr/bin/env python3
"""P27 quadratic gate recurrence probe.

The S-map pair resolvent simplifies in the natural square-root coordinate.
If

    A = 2 - c^2
    x = r^2

then the next selected x-square gate is:

    next_gate = chi(r^2 + c*r + 1).

The sign of c and r should not matter on the selected nonsplit tower.  This is
a source-shaped statement: each next gate is a conic condition

    h^2 = r^2 + c*r + 1

instead of an opaque quartic root-squareclass.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows, sqrt_mod
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def quadratic_gate_chars(a: int, x: int, p: int) -> tuple[set[int], Counter]:
    stats: Counter = Counter()
    r0 = sqrt_mod(x, p)
    c0 = sqrt_mod(2 - a, p)
    if r0 is None:
        stats["x_not_square"] += 1
        return set(), stats
    if c0 is None:
        stats["two_minus_A_not_square"] += 1
        return set(), stats
    chars: set[int] = set()
    r_roots = [r0, (-r0) % p] if r0 else [0]
    c_roots = [c0, (-c0) % p] if c0 else [0]
    for r in r_roots:
        for c in c_roots:
            chi = legendre((r * r + c * r + 1) % p, p)
            if chi:
                chars.add(chi)
    if len(chars) == 1:
        stats["sign_independent"] += 1
    elif len(chars) > 1:
        stats["sign_dependent"] += 1
    else:
        stats["no_nonzero_chars"] += 1
    return chars, stats


def selected_next_x(a: int, x: int, p: int) -> tuple[int | None, int | None, Counter]:
    stats: Counter = Counter()
    d_chi, xs = halve_all(a, x, p)
    if d_chi != 1 or not xs:
        stats["d_not_square"] += 1
        return d_chi, None, stats
    target = normalize_pm1([legendre(xx, p) for xx in xs])
    if target not in (-1, 1):
        stats["target_not_normalized"] += 1
        return target, None, stats
    next_square = next((xx for xx in xs if legendre(xx, p) == 1), None)
    return target, next_square, stats


def collect_p27(target: int, seed: int, max_draws: int, max_gates: int) -> Counter:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    for row in rows:
        cand = row["root0"]
        assert isinstance(cand, dict)
        a = int(cand["A"])
        x = int(cand["x5"])
        for gate in range(3, max_gates + 1):
            expected, next_x, step_stats = selected_next_x(a, x, P)
            stats.update({f"gate{gate}_{key}": value for key, value in step_stats.items()})
            if expected not in (-1, 1):
                break
            chars, formula_stats = quadratic_gate_chars(a, x, P)
            stats.update({f"gate{gate}_{key}": value for key, value in formula_stats.items()})
            stats[f"gate{gate}_rows"] += 1
            stats[f"gate{gate}_target_{expected}"] += 1
            if len(chars) == 1:
                value = next(iter(chars))
                stats[f"gate{gate}_formula_{value}"] += 1
                if value == expected:
                    stats[f"gate{gate}_matches"] += 1
                else:
                    stats[f"gate{gate}_mismatches"] += 1
            elif expected in chars:
                stats[f"gate{gate}_contains_expected"] += 1
            else:
                stats[f"gate{gate}_misses_expected"] += 1
            if expected != 1 or next_x is None:
                break
            x = int(next_x)
    stats["sampled_rows"] = len(rows)
    return stats


def collect_small_field(q: int) -> Counter:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in candidates:
        bits = candidate_bits(cand, q)
        a = int(cand["A"])
        x5 = int(cand["x5"])
        for gate, expected, x in [(3, bits.d3, x5)]:
            if expected not in (-1, 1):
                continue
            chars, formula_stats = quadratic_gate_chars(a, x, q)
            stats.update({f"gate{gate}_{key}": value for key, value in formula_stats.items()})
            stats[f"gate{gate}_rows"] += 1
            stats[f"gate{gate}_target_{expected}"] += 1
            if len(chars) == 1 and next(iter(chars)) == expected:
                stats[f"gate{gate}_matches"] += 1
            elif expected in chars:
                stats[f"gate{gate}_contains_expected"] += 1
            else:
                stats[f"gate{gate}_misses_expected"] += 1
        if bits.d3 != 1 or bits.d4 not in (-1, 1):
            continue
        _, x6s = halve_all(a, x5, q)
        if not x6s:
            continue
        x6 = int(x6s[0])
        chars, formula_stats = quadratic_gate_chars(a, x6, q)
        stats.update({f"gate4_{key}": value for key, value in formula_stats.items()})
        stats["gate4_rows"] += 1
        stats[f"gate4_target_{bits.d4}"] += 1
        if len(chars) == 1 and next(iter(chars)) == bits.d4:
            stats["gate4_matches"] += 1
        elif bits.d4 in chars:
            stats["gate4_contains_expected"] += 1
        else:
            stats["gate4_misses_expected"] += 1
    return stats


def print_counter(prefix: str, stats: Counter, max_gates: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for gate in range(3, max_gates + 1):
        rows = stats[f"gate{gate}_rows"]
        if rows:
            print(f"  gate{gate}_match_rate = {stats[f'gate{gate}_matches'] / rows:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=2500000)
    parser.add_argument("--max-gates", type=int, default=8)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 quadratic gate recurrence probe")
    print("A = 2 - c^2, x = r^2")
    print("next_gate = chi(r^2 + c*r + 1)")
    print("source_conic = h^2 = r^2 + c*r + 1")

    print_counter("p27_train", collect_p27(args.target, args.seed, args.max_draws, args.max_gates), args.max_gates)
    print_counter(
        "p27_heldout",
        collect_p27(args.target, args.heldout_seed, args.max_draws, args.max_gates),
        args.max_gates,
    )
    print("small_field_quadratic_gate_screens:")
    for q in parse_ints(args.small_primes):
        print_counter(f"q{q}", collect_small_field(q), 4)

    print("p27_quadratic_gate_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
