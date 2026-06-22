#!/usr/bin/env python3
"""P27 S-map quartic recurrence probe.

After the reciprocal r-quotient screen, the actual d3/d4 gate is

    chi(r + 2), where r = x_next + 1/x_next.

Set r = S^2 - 2.  The Montgomery doubling quotient gives

    x_prev = S^2*(S^2 - 4) / (4*(S^2 + A - 2)).

Composing one more all-plus step gives a quartic in Y = S_next^2.  This probe
checks whether that quartic exposes a cheap recurrence/source for d4.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, inv, legendre, sample_rows
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


FEATURES = [
    "S2",
    "S2-4",
    "S2+4",
    "A-2",
    "A+2",
    "A+S2-2",
    "A+S2-6",
    "A*S2-2A-2S2",
    "quartic_c2",
    "quartic_c1",
]


@dataclass(frozen=True)
class SpanResult:
    good: int
    total: int
    combo: int


def popcount(value: int) -> int:
    return bin(value).count("1")


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def quartic_coeffs(a: int, s2: int, p: int) -> tuple[int, int, int, int, int]:
    """Return coefficients of F(Y) from highest to lowest degree."""

    return (
        1 % p,
        (-4 * s2) % p,
        (-4 * a * s2 + 8 * a + 24 * s2 - 16) % p,
        (16 * a * s2 - 32 * s2) % p,
        (16 * (a - 2) * (a - 2)) % p,
    )


def quartic_eval(coeffs: tuple[int, int, int, int, int], y: int, p: int) -> int:
    acc = 0
    for coeff in coeffs:
        acc = (acc * y + coeff) % p
    return acc


def quartic_roots_y(a: int, s2: int, p: int) -> list[int]:
    coeffs = quartic_coeffs(a, s2, p)
    return [y for y in range(p) if quartic_eval(coeffs, y, p) == 0]


def feature_values(a: int, s2: int, p: int) -> dict[str, int]:
    _, _, c2, c1, _ = quartic_coeffs(a, s2, p)
    return {
        "S2": s2,
        "S2-4": s2 - 4,
        "S2+4": s2 + 4,
        "A-2": a - 2,
        "A+2": a + 2,
        "A+S2-2": a + s2 - 2,
        "A+S2-6": a + s2 - 6,
        "A*S2-2A-2S2": a * s2 - 2 * a - 2 * s2,
        "quartic_c2": c2,
        "quartic_c1": c1,
    }


def combo_name(combo: int) -> str:
    names = [name for i, name in enumerate(FEATURES) if (combo >> i) & 1]
    return " * ".join(names) if names else "1"


def mask_for_features(a: int, s2: int, p: int) -> tuple[int | None, Counter]:
    stats: Counter = Counter()
    mask = 0
    values = feature_values(a, s2, p)
    for i, name in enumerate(FEATURES):
        chi = legendre(values[name], p)
        if chi == 0:
            stats[f"zero_feature_{name}"] += 1
            return None, stats
        if chi == -1:
            mask |= 1 << i
    return mask, stats


def best_span(rows: list[tuple[int, int]], limit: int) -> tuple[list[SpanResult], list[int]]:
    scored: list[SpanResult] = []
    exact: list[int] = []
    for combo in range(1 << len(FEATURES)):
        good = sum((popcount(mask & combo) & 1) == target for mask, target in rows)
        scored.append(SpanResult(good=good, total=len(rows), combo=combo))
        if good == len(rows):
            exact.append(combo)
    scored.sort(key=lambda item: (item.good, -popcount(item.combo), -item.combo), reverse=True)
    return scored[:limit], exact


def score_combo(rows: list[tuple[int, int]], combo: int) -> int:
    return sum((popcount(mask & combo) & 1) == target for mask, target in rows)


def collect_p27_rows(target: int, seed: int, max_draws: int) -> tuple[list[tuple[int, int]], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    out: list[tuple[int, int]] = []
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
        split_chi = legendre(s2 + a - 6, P)
        if split_chi == d4:
            stats["split_matches_d4"] += 1
        elif -split_chi == d4:
            stats["split_neg_matches_d4"] += 1
        stats[f"split_{split_chi}"] += 1
        stats[f"d4_{d4}"] += 1
        mask, mask_stats = mask_for_features(a, s2, P)
        stats.update(mask_stats)
        if mask is None:
            continue
        out.append((mask, 0 if d4 == 1 else 1))
    stats["rows"] = len(out)
    return out, stats


def small_field_screen(q: int) -> Counter:
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
        roots = quartic_roots_y(a, s2, q)
        square_roots = [y for y in roots if legendre(y, q) == 1]
        stats["rows"] += 1
        stats[f"d4_{bits.d4}"] += 1
        stats[f"roots_{len(roots)}"] += 1
        stats[f"square_y_roots_{len(square_roots)}"] += 1
        predicted = 1 if square_roots else -1
        if predicted == bits.d4:
            stats["root_squareclass_matches_d4"] += 1
        else:
            stats["root_squareclass_mismatch_d4"] += 1
        split_chi = legendre(s2 + a - 6, q)
        if split_chi == bits.d4:
            stats["split_matches_d4"] += 1
        elif -split_chi == bits.d4:
            stats["split_neg_matches_d4"] += 1
        stats[f"split_{split_chi}"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_span(prefix: str, train: list[tuple[int, int]], heldout: list[tuple[int, int]], limit: int) -> None:
    best, exact = best_span(train, limit)
    print(f"{prefix}:")
    print(f"  features = {', '.join(FEATURES)}")
    print(f"  train_rows = {len(train)}")
    print(f"  heldout_rows = {len(heldout)}")
    print(f"  exact_train_combos = {len(exact)}")
    print(f"  best_combos:")
    for result in best:
        heldout_good = score_combo(heldout, result.combo)
        train_rate = result.good / result.total if result.total else 0.0
        heldout_rate = heldout_good / len(heldout) if heldout else 0.0
        print(
            f"    train={result.good}/{result.total} rate={train_rate:.9f} "
            f"heldout={heldout_good}/{len(heldout)} rate={heldout_rate:.9f} "
            f"weight={popcount(result.combo)} combo={combo_name(result.combo)}"
        )


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=2500000)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    print("p27 S-map quartic recurrence probe")
    print("x_prev = S^2*(S^2-4)/(4*(S^2+A-2))")
    print(
        "F(Y)=Y^4-4*S2*Y^3+(-4*A*S2+8*A+24*S2-16)*Y^2"
        "+(16*A*S2-32*S2)*Y+16*(A-2)^2"
    )
    print(
        "disc_Y(F)=65536*S^4*(A-2)^2*(A+2)^2*(S-2)^2*(S+2)^2*(A+S^2-2)^2"
    )
    print("quadratic_split_discriminant = 16*S^2*(S^2+A-6)")

    train, train_stats = collect_p27_rows(args.target, args.seed, args.max_draws)
    print_counter("p27_train", train_stats)
    heldout, heldout_stats = collect_p27_rows(args.target, args.heldout_seed, args.max_draws)
    print_counter("p27_heldout", heldout_stats)
    print_span("p27_named_quartic_factor_span", train, heldout, args.limit)

    print("small_field_smap_quartic_screens:")
    for q in parse_ints(args.small_primes):
        stats = small_field_screen(q)
        print_counter(f"q{q}", stats)

    print("p27_smap_quartic_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
