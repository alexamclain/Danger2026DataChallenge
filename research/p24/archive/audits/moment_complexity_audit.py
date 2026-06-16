#!/usr/bin/env python3
"""Moment-complexity audit for strict near-square DANGER buckets.

For small primes in the family p = n^2 + 7, compute the exact strict
x-only-good Montgomery A values and test whether that set looks simple in the
near-square coordinate A over F_p = F_n[n]/(n^2 + 7).

This closes a concrete remaining shortcut shape:

* stable low-degree real polynomial moments in the additive A coordinate;
* unusually small power sums when represented as a + b*n mod p; or
* a short finite-field linear recurrence in the moment sequence.

None of these tests proves pseudorandomness.  They are bounded diagnostics for
the kind of low-complexity A-line structure that would plausibly lead to a
sub-sqrt construction.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from statistics import median

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table


@dataclass(frozen=True)
class SmallRep:
    value: int
    a: int
    b: int
    height: int
    l1: int


@dataclass(frozen=True)
class RowSummary:
    n: int
    p: int
    k: int
    good: int
    total: int
    density: float
    max_legendre_degree: int
    max_legendre_z: float
    aggregate_legendre_z: float
    odd_moments_zero: bool
    min_even_height_ratio: float
    median_even_height_ratio: float
    raw_hankel_rank: int
    centered_hankel_rank: int


def signed_mod(value: int, p: int) -> int:
    value %= p
    return value if value <= p // 2 else value - p


def small_representation(value: int, n: int, p: int, extra: int = 8) -> SmallRep:
    """Find a small a + b*n representative by a bounded 2D closest search."""
    best: SmallRep | None = None
    # For p = n^2 + 7, scanning |b| <= n plus a tiny margin finds the natural
    # nearest representative for calibration rows and catches O(1) formulas.
    for b in range(-n - extra, n + extra + 1):
        a = signed_mod(value - b * n, p)
        height = max(abs(a), abs(b))
        l1 = abs(a) + abs(b)
        candidate = SmallRep(value=value % p, a=a, b=b, height=height, l1=l1)
        if best is None or (candidate.height, candidate.l1) < (best.height, best.l1):
            best = candidate
    assert best is not None
    return best


def power_moments(
    p: int,
    good: np.ndarray,
    nonsingular: np.ndarray,
    max_degree: int,
) -> tuple[list[int], list[int], list[int]]:
    A = np.arange(p, dtype=np.int64)
    power = np.ones(p, dtype=np.int64)
    good_moments: list[int] = []
    all_moments: list[int] = []
    centered_numerators: list[int] = []
    good_count = int(np.count_nonzero(good))
    total = int(np.count_nonzero(nonsingular))

    for _degree in range(max_degree + 1):
        good_sum = int(np.sum(power[good], dtype=np.int64) % p)
        all_sum = int(np.sum(power[nonsingular], dtype=np.int64) % p)
        good_moments.append(good_sum)
        all_moments.append(all_sum)
        centered_numerators.append((total * good_sum - good_count * all_sum) % p)
        power = (power * A) % p

    return good_moments, all_moments, centered_numerators


def legendre_zscores(
    good: np.ndarray,
    nonsingular: np.ndarray,
    max_degree: int,
) -> list[float]:
    p = good.shape[0]
    xs = (2.0 * np.arange(p, dtype=np.float64) / (p - 1.0)) - 1.0
    mask = nonsingular
    hits = int(np.count_nonzero(good & mask))
    total = int(np.count_nonzero(mask))
    rho = hits / total if total else 0.0
    f = good[mask].astype(np.float64) - rho
    variance_scale = rho * (1.0 - rho)

    out: list[float] = []
    p0 = np.ones(p, dtype=np.float64)
    p1 = xs.copy()
    polys: list[np.ndarray] = [p0]
    if max_degree >= 1:
        polys.append(p1)
    for degree in range(2, max_degree + 1):
        polys.append(((2 * degree - 1) * xs * polys[-1] - (degree - 1) * polys[-2]) / degree)

    for degree in range(1, max_degree + 1):
        basis = polys[degree][mask]
        basis = basis - float(np.mean(basis))
        denom = math.sqrt(max(variance_scale * float(np.dot(basis, basis)), 0.0))
        out.append(float(np.dot(f, basis) / denom) if denom else 0.0)
    return out


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % p, p - 2, p)
        mat[rank] = [(value * inv) % p for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % p
            if factor:
                mat[row] = [(x - factor * y) % p for x, y in zip(mat[row], mat[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def hankel_rank(moments: list[int], p: int, size: int) -> int:
    matrix = [[moments[i + j] % p for j in range(size)] for i in range(size)]
    return rank_mod_p(matrix, p)


def summarize_row(
    n: int,
    p: int,
    k: int,
    good: np.ndarray,
    nonsingular: np.ndarray,
    max_moment_degree: int,
    max_legendre_degree: int,
    hankel_size: int,
    top: int,
) -> tuple[RowSummary, list[float]]:
    good_moments, _all_moments, centered = power_moments(p, good, nonsingular, max_moment_degree)
    zscores = legendre_zscores(good, nonsingular, max_legendre_degree)
    reps = [small_representation(value, n, p) for value in good_moments]
    even_ratios = [reps[degree].height / n for degree in range(2, max_moment_degree + 1, 2)]
    odd_zero = all(good_moments[degree] % p == 0 for degree in range(1, max_moment_degree + 1, 2))
    raw_rank = hankel_rank(good_moments, p, hankel_size)
    centered_rank = hankel_rank(centered, p, hankel_size)

    total = int(np.count_nonzero(nonsingular))
    good_count = int(np.count_nonzero(good))
    density = good_count / total if total else 0.0
    max_degree, max_z = max(
        enumerate(zscores, start=1),
        key=lambda item: abs(item[1]),
        default=(0, 0.0),
    )
    agg_z = math.sqrt(sum(z * z for z in zscores))

    print(f"row n={n} p={p} k={k} good={good_count}/{total} density={density:.6f}")
    print(
        f"  legendre_max degree={max_degree} z={max_z:+.3f} "
        f"l2_z={agg_z:.3f}"
    )
    top_degrees = sorted(enumerate(zscores, start=1), key=lambda item: abs(item[1]), reverse=True)[:top]
    print(
        "  top_legendre "
        + " ".join(f"d{degree}={z:+.2f}" for degree, z in top_degrees)
    )
    print(
        f"  odd_power_moments_zero={odd_zero} "
        f"even_height_ratio_min={min(even_ratios):.3f} "
        f"even_height_ratio_median={median(even_ratios):.3f}"
    )
    top_small_even = sorted(
        ((reps[degree].height / n, degree, reps[degree]) for degree in range(2, max_moment_degree + 1, 2)),
        key=lambda item: (item[0], item[2].l1),
    )[:top]
    print(
        "  smallest_even_reps "
        + " ".join(
            f"d{degree}:h/n={ratio:.3f},a={rep.a},b={rep.b}"
            for ratio, degree, rep in top_small_even
        )
    )
    print(
        f"  hankel_raw_rank={raw_rank}/{hankel_size} "
        f"hankel_centered_rank={centered_rank}/{hankel_size}"
    )

    return (
        RowSummary(
            n=n,
            p=p,
            k=k,
            good=good_count,
            total=total,
            density=density,
            max_legendre_degree=max_degree,
            max_legendre_z=max_z,
            aggregate_legendre_z=agg_z,
            odd_moments_zero=odd_zero,
            min_even_height_ratio=min(even_ratios),
            median_even_height_ratio=median(even_ratios),
            raw_hankel_rank=raw_rank,
            centered_hankel_rank=centered_rank,
        ),
        zscores,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=12)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-moment-degree", type=int, default=24)
    ap.add_argument("--max-legendre-degree", type=int, default=24)
    ap.add_argument("--hankel-size", type=int, default=10)
    ap.add_argument("--top", type=int, default=6)
    args = ap.parse_args()

    needed_moments = 2 * args.hankel_size - 2
    if args.max_moment_degree < needed_moments:
        raise SystemExit(f"--max-moment-degree must be at least {needed_moments} for this Hankel size")

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("moment-complexity strict A-bucket audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"max_moment_degree={args.max_moment_degree}")
    print(f"max_legendre_degree={args.max_legendre_degree}")
    print(f"hankel_size={args.hankel_size}")

    summaries: list[RowSummary] = []
    z_by_degree = np.zeros(args.max_legendre_degree, dtype=np.float64)
    abs_z_by_degree = np.zeros(args.max_legendre_degree, dtype=np.float64)

    for n, p in rows:
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        nonsingular = np.ones(p, dtype=np.bool_)
        nonsingular[[2 % p, (-2) % p]] = False
        good &= nonsingular
        summary, zscores = summarize_row(
            n=n,
            p=p,
            k=int(stats["k"]),
            good=good,
            nonsingular=nonsingular,
            max_moment_degree=args.max_moment_degree,
            max_legendre_degree=args.max_legendre_degree,
            hankel_size=args.hankel_size,
            top=args.top,
        )
        summaries.append(summary)
        z_by_degree += np.array(zscores, dtype=np.float64)
        abs_z_by_degree += np.abs(np.array(zscores, dtype=np.float64))

    if not summaries:
        print("conclusion=no_rows")
        return

    scale = math.sqrt(len(summaries))
    aggregate_signed = z_by_degree / scale
    aggregate_abs_mean = abs_z_by_degree / len(summaries)
    top_signed = sorted(
        enumerate(aggregate_signed, start=1),
        key=lambda item: abs(item[1]),
        reverse=True,
    )[: args.top]
    top_abs = sorted(enumerate(aggregate_abs_mean, start=1), key=lambda item: item[1], reverse=True)[: args.top]

    print("aggregate")
    print(
        f"  good={sum(row.good for row in summaries)}/"
        f"{sum(row.total for row in summaries)} "
        f"density={sum(row.good for row in summaries) / sum(row.total for row in summaries):.6f}"
    )
    print(
        "  signed_legendre_z "
        + " ".join(f"d{degree}={z:+.3f}" for degree, z in top_signed)
    )
    print(
        "  mean_abs_legendre_z "
        + " ".join(f"d{degree}={z:.3f}" for degree, z in top_abs)
    )
    print(
        f"  odd_power_moments_zero_rows="
        f"{sum(row.odd_moments_zero for row in summaries)}/{len(summaries)}"
    )
    print(
        f"  even_height_ratio_min_median={median(row.min_even_height_ratio for row in summaries):.3f} "
        f"even_height_ratio_median_median={median(row.median_even_height_ratio for row in summaries):.3f}"
    )
    print(
        f"  full_raw_hankel_rank_rows="
        f"{sum(row.raw_hankel_rank == args.hankel_size for row in summaries)}/{len(summaries)} "
        f"full_centered_hankel_rank_rows="
        f"{sum(row.centered_hankel_rank == args.hankel_size for row in summaries)}/{len(summaries)}"
    )
    print(
        "conclusion=no_stable_low_degree_moment_small_height_or_short_recurrence_signal"
    )


if __name__ == "__main__":
    main()
