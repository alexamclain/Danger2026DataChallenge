#!/usr/bin/env python3
"""Multiplication-table diagnostic for CM quotient periods.

Gaussian periods in cyclotomic fields have multiplication constants
(`cyclotomic numbers') with strong combinatorial structure.  A tempting p24
hope is that CM quotient periods might similarly have a small/sparse
multiplication table, letting us compute the unordered child polynomial
without high-order class-character traces.

This toy computes the split finite-field analogue.  For a quotient period
vector y=(y_0,...,y_{m-1}), use its cyclic shifts as a normal-basis candidate
in the split quotient algebra F_q^m.  For each pair of shifts, solve

    shift_i(y) * shift_j(y) = sum_k c_{i,j,k} shift_k(y)

coordinatewise in F_q^m.  Sparse or low-rank coefficient patterns would be a
positive Gaussian-period signal.  Dense random-looking tables are evidence
that multiplication-table access is as data-heavy as the periods themselves.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from cypari2 import Pari

from abstract_embedded_pairing_non_genus_toy import components
from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle


@dataclass(frozen=True)
class TableStats:
    label: str
    q: int
    m: int
    normal_rank: int
    products: int
    zero_products: int
    min_support: int
    max_support: int
    avg_support: float
    distinct_rows: int
    random_avg_support: float
    random_min_support: int
    random_max_support: int


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    r = 0
    for c in range(len(rows[0])):
        pivot = None
        for i in range(r, len(rows)):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(len(rows)):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(x - factor * y) % q for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def solve_square(matrix_cols: list[list[int]], rhs: list[int], q: int) -> list[int] | None:
    """Solve M*c=rhs, where matrix_cols are columns of M."""
    m = len(rhs)
    rows = [[matrix_cols[c][r] % q for c in range(m)] + [rhs[r] % q] for r in range(m)]
    pivot_cols: list[int] = []
    r = 0
    for c in range(m):
        pivot = None
        for i in range(r, m):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(m):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(x - factor * y) % q for x, y in zip(rows[i], rows[r])]
        pivot_cols.append(c)
        r += 1
    for i in range(r, m):
        if rows[i][-1] % q:
            return None
    if len(pivot_cols) < m:
        return None
    out = [0] * m
    for row, col in enumerate(pivot_cols):
        out[col] = rows[row][-1] % q
    return out


def shift(values: list[int], amount: int) -> list[int]:
    amount %= len(values)
    return values[amount:] + values[:amount]


def table_stats(label: str, periods: list[int], q: int, random_controls: int, rng: random.Random) -> TableStats:
    m = len(periods)
    basis = [shift(periods, i) for i in range(m)]
    normal_rank = rank_mod([[basis[c][r] for c in range(m)] for r in range(m)], q)
    supports: list[int] = []
    rows_seen: set[tuple[int, ...]] = set()
    zero_products = 0
    for i in range(m):
        for j in range(m):
            product = [basis[i][r] * basis[j][r] % q for r in range(m)]
            coeffs = solve_square(basis, product, q)
            if coeffs is None:
                raise RuntimeError(f"period shifts are not a basis for {label}")
            support = sum(c != 0 for c in coeffs)
            supports.append(support)
            zero_products += int(support == 0)
            rows_seen.add(tuple(coeffs))

    random_supports: list[int] = []
    for _ in range(random_controls):
        while True:
            random_periods = [rng.randrange(q) for _ in range(m)]
            random_basis = [shift(random_periods, i) for i in range(m)]
            random_rank = rank_mod(
                [[random_basis[c][r] for c in range(m)] for r in range(m)],
                q,
            )
            if random_rank == m:
                break
        for i in range(m):
            for j in range(m):
                product = [random_basis[i][r] * random_basis[j][r] % q for r in range(m)]
                coeffs = solve_square(random_basis, product, q)
                if coeffs is None:
                    raise RuntimeError("random basis unexpectedly singular")
                random_supports.append(sum(c != 0 for c in coeffs))

    return TableStats(
        label=label,
        q=q,
        m=m,
        normal_rank=normal_rank,
        products=m * m,
        zero_products=zero_products,
        min_support=min(supports),
        max_support=max(supports),
        avg_support=sum(supports) / len(supports),
        distinct_rows=len(rows_seen),
        random_avg_support=sum(random_supports) / len(random_supports),
        random_min_support=min(random_supports),
        random_max_support=max(random_supports),
    )


def periods_from_cycle(cycle: list[int], q: int, quotient_size: int) -> list[int]:
    h = len(cycle)
    subgroup_size = h // quotient_size
    return [
        sum(cycle[(r + quotient_size * k) % h] for k in range(subgroup_size)) % q
        for r in range(quotient_size)
    ]


def d5000_periods() -> list[tuple[str, int, list[int]]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    D = -5000
    q = 1259
    ell = 3
    roots = pari_linear_roots(pari.polclass(D), q)
    graph = isogeny_neighbors(roots, ell, q)
    cycle = walk_cycle(graph)
    return [
        ("D=-5000 quotient=6", q, periods_from_cycle(cycle, q, 6)),
        ("D=-5000 quotient=10", q, periods_from_cycle(cycle, q, 10)),
    ]


def d2239_periods() -> list[tuple[str, int, list[int]]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    D = -2239
    q = 2243
    roots = pari_linear_roots(pari.polclass(D), q)
    # Full class generator for the cyclic ordering.
    graph = isogeny_neighbors(roots, 2, q)
    cycle = walk_cycle(graph)

    # Also include the embedded 5-cycle quotient from the ell=5 components,
    # sorted only as an unordered period vector.  Its shifts are an arbitrary
    # ordering, which is exactly the pairing problem this diagnostic probes.
    quotient_graph = isogeny_neighbors(roots, 5, q)
    comps = components(quotient_graph)
    component_periods = [sum(comp) % q for comp in comps]
    return [
        ("D=-2239 quotient=5 full-cycle", q, periods_from_cycle(cycle, q, 5)),
        ("D=-2239 quotient=7 full-cycle", q, periods_from_cycle(cycle, q, 7)),
        ("D=-2239 quotient=5 components", q, component_periods),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-controls", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    cases = d5000_periods() + d2239_periods()

    print("period multiplication-table scan")
    print(f"random_controls={args.random_controls}")
    print()
    print(
        "columns: label q m rank products zero_products min_support max_support "
        "avg_support distinct_rows random_avg random_min random_max"
    )
    for label, q, periods in cases:
        stats = table_stats(label, periods, q, args.random_controls, rng)
        print(
            f"label='{stats.label}' q={stats.q} m={stats.m} "
            f"rank={stats.normal_rank} products={stats.products} "
            f"zero_products={stats.zero_products} "
            f"min_support={stats.min_support} max_support={stats.max_support} "
            f"avg_support={stats.avg_support:.3f} "
            f"distinct_rows={stats.distinct_rows} "
            f"random_avg={stats.random_avg_support:.3f} "
            f"random_min={stats.random_min_support} "
            f"random_max={stats.random_max_support}"
        )
    print()
    print("interpretation")
    print("  dense_support_near_random_means_no_sparse_gaussian_period_table_visible=1")
    print("  full_distinct_rows_means_product_constants_do_not_collapse_obviously=1")
    print("  multiplication_table_access_is_equivalent_to_knowing_the_embedded_period_algebra=1")
    print("conclusion=reported_period_multiplication_table_scan")


if __name__ == "__main__":
    main()
