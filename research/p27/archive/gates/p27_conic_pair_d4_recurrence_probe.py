#!/usr/bin/env python3
"""D4 recurrence screen on the p27 legal conic-pair intersection.

The d3 conic-pair screen showed that the free pair surface covers every legal
d3-plus (A,x5) class in tested fields, but is too sparse as a raw sampler.
This probe asks the next recurrence question:

* after taking one legal all-plus step, does the next coordinate re-enter the
  same legal source?
* is d4 visible as a simple squareclass product in the current conic-pair lift
  variables, without paying the next conic Legendre test directly?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

from p27_conic_pair_sampler_legal_incidence_probe import (
    conic_pair_sampler_stats,
    legal_sets,
    raw_cr_image,
)
from p27_conic_chain_source_probe import sqrt_table
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows, sqrt_mod
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


FEATURES = [
    "-1",
    "c",
    "r",
    "R",
    "h",
    "g",
    "s",
    "d",
    "L",
    "a",
    "R+1",
    "R-1",
    "r+1",
    "r-1",
    "c+1",
    "c-1",
    "h+1",
    "g+1",
    "L+1",
    "L-1",
    "L+a",
    "L-a",
    "L+r",
    "L-r",
    "h*g",
    "h*r",
    "g*r",
    "c*r",
    "c*R",
]


@dataclass(frozen=True)
class Lift:
    c: int
    r: int
    h: int
    g: int
    R: int


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def next_square_branches(a: int, x: int, p: int) -> list[int]:
    d_chi, branches = halve_all(a, x, p)
    if d_chi != 1:
        return []
    return [branch for branch in branches if legendre(branch, p) == 1]


def d4_for_next_branch(a: int, x6: int, p: int) -> int | None:
    _, x7s = halve_all(a, x6, p)
    return normalize_pm1([legendre(x7, p) for x7 in x7s])


def conic_lifts(a: int, x: int, p: int, roots: list[list[int]]) -> list[Lift]:
    out: list[Lift] = []
    for c in roots[(2 - a) % p]:
        for r in roots[x % p]:
            qp = (r * r + c * r + 1) % p
            qm = (r * r - c * r + 1) % p
            for h in roots[qp]:
                for g in roots[qm]:
                    s = (h + g) % p
                    disc = (s * s - 4) % p
                    for delta in roots[disc]:
                        inv2 = inv(2, p)
                        candidates = [(s + delta) * inv2 % p]
                        if delta:
                            candidates.append((s - delta) * inv2 % p)
                        for R in candidates:
                            out.append(Lift(c=c, r=r, h=h, g=g, R=R))
    return out


def roots_mod(a: int, p: int) -> list[int]:
    root = sqrt_mod(a, p)
    if root is None:
        return []
    if root == 0:
        return [0]
    return [root, (-root) % p]


def conic_lifts_modsqrt(a: int, x: int, p: int) -> list[Lift]:
    out: list[Lift] = []
    for c in roots_mod((2 - a) % p, p):
        for r in roots_mod(x % p, p):
            qp = (r * r + c * r + 1) % p
            qm = (r * r - c * r + 1) % p
            for h in roots_mod(qp, p):
                for g in roots_mod(qm, p):
                    s = (h + g) % p
                    disc = (s * s - 4) % p
                    inv2 = inv(2, p)
                    for delta in roots_mod(disc, p):
                        candidates = [(s + delta) * inv2 % p]
                        if delta:
                            candidates.append((s - delta) * inv2 % p)
                        for R in candidates:
                            out.append(Lift(c=c, r=r, h=h, g=g, R=R))
    return out


def feature_values(lift: Lift, p: int) -> dict[str, int]:
    c, r, h, g, R = lift.c, lift.r, lift.h, lift.g, lift.R
    s = (h + g) % p
    d = (h - g) % p
    a = (R - inv(R, p)) % p if R else 0
    L = (d - 2 * r) % p
    return {
        "-1": -1,
        "c": c,
        "r": r,
        "R": R,
        "h": h,
        "g": g,
        "s": s,
        "d": d,
        "L": L,
        "a": a,
        "R+1": R + 1,
        "R-1": R - 1,
        "r+1": r + 1,
        "r-1": r - 1,
        "c+1": c + 1,
        "c-1": c - 1,
        "h+1": h + 1,
        "g+1": g + 1,
        "L+1": L + 1,
        "L-1": L - 1,
        "L+a": L + a,
        "L-a": L - a,
        "L+r": L + r,
        "L-r": L - r,
        "h*g": h * g,
        "h*r": h * r,
        "g*r": g * r,
        "c*r": c * r,
        "c*R": c * R,
    }


def feature_mask(lift: Lift, p: int) -> tuple[int | None, Counter]:
    values = feature_values(lift, p)
    stats: Counter = Counter()
    mask = 0
    for i, name in enumerate(FEATURES):
        chi = legendre(values[name], p)
        if chi == 0:
            stats[f"feature_zero_{name}"] += 1
            return None, stats
        if chi == -1:
            mask |= 1 << i
    return mask, stats


def target_bit(value: int) -> int:
    if value == 1:
        return 0
    if value == -1:
        return 1
    raise ValueError(value)


def parity(n: int) -> int:
    return bin(n).count("1") & 1


def solve_gf2(equations: list[tuple[int, int]], nvars: int) -> int | None:
    basis: dict[int, tuple[int, int]] = {}
    for mask, rhs in equations:
        row = mask
        val = rhs
        while row:
            lead = row.bit_length() - 1
            if lead not in basis:
                basis[lead] = (row, val)
                break
            brow, bval = basis[lead]
            row ^= brow
            val ^= bval
        else:
            if val:
                return None

    solution = 0
    for lead in sorted(basis):
        row, val = basis[lead]
        accum = parity(row & solution)
        if accum != val:
            solution |= 1 << lead
    # Verify because the compact back-substitution above depends on basis form.
    for mask, rhs in equations:
        if parity(mask & solution) != rhs:
            return None
    return solution


def combo_name(mask: int) -> str:
    names = [FEATURES[i] for i in range(len(FEATURES)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def best_single_features(equations: list[tuple[int, int]]) -> list[tuple[int, int, str, int]]:
    out: list[tuple[int, int, str, int]] = []
    total = len(equations)
    for i, name in enumerate(FEATURES):
        good = 0
        good_neg = 0
        bit = 1 << i
        for mask, rhs in equations:
            val = 1 if mask & bit else 0
            good += val == rhs
            good_neg += (val ^ 1) == rhs
        if good >= good_neg:
            out.append((good, total, name, 1))
        else:
            out.append((good_neg, total, name, -1))
    out.sort(reverse=True)
    return out[:8]


def screen_field(p: int, include_raw: bool) -> tuple[Counter, list[tuple[int, int]]]:
    roots = sqrt_table(p)
    _, sampler_image, _ = conic_pair_sampler_stats(p)
    legal_stats, legal, d3_plus, d3_minus = legal_sets(p)
    raw_image = raw_cr_image(p) if include_raw else set()

    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum2_{key}": value for key, value in enum_stats.items()})
    stats.update({f"legal_{key}": value for key, value in legal_stats.items()})

    by_ax: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for cand in candidates:
        by_ax[(int(cand["A"]), int(cand["x5"]))].append(cand)

    equations: list[tuple[int, int]] = []
    seen_ax: set[tuple[int, int]] = set()
    for ax, group in by_ax.items():
        if ax in seen_ax:
            continue
        seen_ax.add(ax)
        a, x5 = ax
        bit_values = [candidate_bits(cand, p) for cand in group]
        d3 = normalize_pm1([bits.d3 for bits in bit_values if bits.d3 is not None])
        if d3 != 1:
            continue
        d4 = normalize_pm1([bits.d4 for bits in bit_values if bits.d4 is not None])
        if d4 not in (-1, 1):
            stats["d4_not_normalized_on_ax"] += 1
            continue

        stats["d3_plus_unique_ax"] += 1
        stats[f"d4_{d4}_unique_ax"] += 1
        x6s = next_square_branches(a, x5, p)
        stats[f"x6_square_branch_count_{len(x6s)}"] += 1
        for x6 in x6s:
            next_ax = (a, x6)
            stats["x6_square_branches"] += 1
            stats[f"x6_d4_{d4_for_next_branch(a, x6, p)}"] += 1
            if next_ax in sampler_image:
                stats["x6_in_sampler_image"] += 1
            if next_ax in legal:
                stats["x6_in_legal"] += 1
            if next_ax in d3_plus:
                stats["x6_in_legal_d3_plus"] += 1
            if next_ax in d3_minus:
                stats["x6_in_legal_d3_minus"] += 1
            if include_raw and next_ax in raw_image:
                stats["x6_in_raw_cr"] += 1

        lifts = conic_lifts(a, x5, p, roots)
        stats["conic_lifts"] += len(lifts)
        if not lifts:
            stats["d3_plus_without_lift"] += 1
            continue
        for lift in lifts:
            formula_d4 = legendre((lift.R * lift.R + lift.c * lift.R + 1) % p, p)
            if formula_d4 != d4:
                stats["formula_d4_mismatch"] += 1
            mask, mask_stats = feature_mask(lift, p)
            stats.update(mask_stats)
            if mask is None:
                stats["feature_zero_rows"] += 1
                continue
            equations.append((mask, target_bit(d4)))
            stats["feature_rows"] += 1

    for key in [
        "x6_in_sampler_image",
        "x6_in_legal",
        "x6_in_legal_d3_plus",
        "x6_in_legal_d3_minus",
        "x6_in_raw_cr",
    ]:
        stats.setdefault(key, 0)
    return stats, equations


def screen_p27_sample(label: str, target: int, seed: int, max_draws: int) -> tuple[str, Counter, list[tuple[int, int]]]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))

    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    by_ax: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for cand in candidates:
        by_ax[(int(cand["A"]), int(cand["x5"]))].append(cand)
    stats["unique_ax"] = len(by_ax)

    equations: list[tuple[int, int]] = []
    for ax, group in by_ax.items():
        a, x5 = ax
        bit_values = [candidate_bits(cand, P) for cand in group]
        d3 = normalize_pm1([bits.d3 for bits in bit_values if bits.d3 is not None])
        if d3 != 1:
            continue
        d4 = normalize_pm1([bits.d4 for bits in bit_values if bits.d4 is not None])
        if d4 not in (-1, 1):
            stats["d4_not_normalized_on_ax"] += 1
            continue
        stats["d3_plus_unique_ax"] += 1
        stats[f"d4_{d4}_unique_ax"] += 1
        x6s = next_square_branches(a, x5, P)
        stats[f"x6_square_branch_count_{len(x6s)}"] += 1
        for x6 in x6s:
            stats["x6_square_branches"] += 1
            stats[f"x6_d4_{d4_for_next_branch(a, x6, P)}"] += 1

        lifts = conic_lifts_modsqrt(a, x5, P)
        stats["conic_lifts"] += len(lifts)
        if not lifts:
            stats["d3_plus_without_lift"] += 1
            continue
        for lift in lifts:
            formula_d4 = legendre((lift.R * lift.R + lift.c * lift.R + 1) % P, P)
            if formula_d4 != d4:
                stats["formula_d4_mismatch"] += 1
            mask, mask_stats = feature_mask(lift, P)
            stats.update(mask_stats)
            if mask is None:
                stats["feature_zero_rows"] += 1
                continue
            equations.append((mask, target_bit(d4)))
            stats["feature_rows"] += 1
    return label, stats, equations


def print_field(prefix: str, p: int, stats: Counter, equations: list[tuple[int, int]]) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    branches = stats["x6_square_branches"]
    if branches:
        if "x6_in_sampler_image" in stats:
            print(f"  x6_sampler_image_rate = {stats['x6_in_sampler_image'] / branches:.9f}")
        if "x6_in_legal" in stats:
            print(f"  x6_legal_reentry_rate = {stats['x6_in_legal'] / branches:.9f}")
        if stats["x6_in_raw_cr"]:
            print(f"  x6_raw_cr_rate = {stats['x6_in_raw_cr'] / branches:.9f}")
    if stats["conic_lifts"]:
        print(f"  feature_row_rate = {stats['feature_rows'] / stats['conic_lifts']:.9f}")
    solution = solve_gf2(equations, len(FEATURES)) if equations else None
    if solution is None:
        print("  exact_feature_combo = none")
    else:
        print(f"  exact_feature_combo = {combo_name(solution)}")
    print("  best_single_features:")
    for good, total, name, polarity in best_single_features(equations):
        rate = good / total if total else 0.0
        print(f"    {name} polarity={polarity} good={good}/{total} rate={rate:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--raw-cr-limit", type=int, default=700)
    parser.add_argument("--p27-target", type=int, default=1000)
    parser.add_argument("--p27-heldout-target", type=int, default=1000)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--p27-max-draws", type=int, default=1000000)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    print("p27 conic-pair d4 recurrence probe")
    print("target = d4 after legal d3-plus conic-pair lift")
    print("feature span excludes the tautological next conic R^2+c*R+1")

    combined: list[tuple[int, int]] = []
    for p in parse_ints(args.small_primes):
        stats, equations = screen_field(p, include_raw=p <= args.raw_cr_limit)
        combined.extend(equations)
        print_field(f"q{p}", p, stats, equations)

    if not args.skip_p27:
        for label, stats, equations in [
            screen_p27_sample("p27_train", args.p27_target, args.p27_seed, args.p27_max_draws),
            screen_p27_sample(
                "p27_heldout",
                args.p27_heldout_target,
                args.p27_heldout_seed,
                args.p27_max_draws,
            ),
        ]:
            combined.extend(equations)
            print_field(label, P, stats, equations)

    print("combined_feature_span:")
    solution = solve_gf2(combined, len(FEATURES)) if combined else None
    if solution is None:
        print("  exact_feature_combo = none")
    else:
        print(f"  exact_feature_combo = {combo_name(solution)}")
    for good, total, name, polarity in best_single_features(combined):
        rate = good / total if total else 0.0
        print(f"  best_single {name} polarity={polarity} good={good}/{total} rate={rate:.9f}")
    print("p27_conic_pair_d4_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
