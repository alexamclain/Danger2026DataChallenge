#!/usr/bin/env python3
"""Probe finite-field invariants of the p27 B-line d3 fiber.

The A/B/K/Sroot fixture bridges reduce the front-door class-extraction task to
one descended Kummer class.  This probe asks whether that class can be seen
without full normalization by looking at symmetric invariants of the next-root
fiber over each legal B value.

For each p27-signature guard field, it records:
  * legal B fiber sizes,
  * the distinct next x-values and their x -> 1/x quotient u=x+1/x,
  * simple norm/trace/power-sum selector attempts,
  * interpolation degrees of the fiber polynomial coefficients on legal B.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Iterable

from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def poly_roots_coeffs(roots: Iterable[int], p: int) -> list[int]:
    coeff = [1]
    for root in roots:
        new = [0] * (len(coeff) + 1)
        for i, value in enumerate(coeff):
            new[i] = (new[i] - value * root) % p
            new[i + 1] = (new[i + 1] + value) % p
        coeff = new
    return coeff


def interpolation_degree(points: list[tuple[int, int]], p: int) -> int:
    """Return the degree of the polynomial interpolating points over F_p."""

    xs = [x for x, _y in points]
    dd = [y % p for _x, y in points]
    n = len(points)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            dd[i] = (dd[i] - dd[i - 1]) * inv(xs[i] - xs[i - j], p) % p

    poly = [0]
    basis = [1]
    for j, coefficient in enumerate(dd):
        if coefficient:
            if len(poly) < len(basis):
                poly.extend([0] * (len(basis) - len(poly)))
            for i, value in enumerate(basis):
                poly[i] = (poly[i] + coefficient * value) % p
        if j == n - 1:
            continue
        next_basis = [0] * (len(basis) + 1)
        xj = xs[j]
        for i, value in enumerate(basis):
            next_basis[i] = (next_basis[i] - value * xj) % p
            next_basis[i + 1] = (next_basis[i + 1] + value) % p
        basis = next_basis

    degree = -1
    for i, value in enumerate(poly):
        if value % p:
            degree = i
    return degree


def collect_b_fibers(q: int) -> tuple[dict[int, list[int]], dict[int, int], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    groups: defaultdict[int, list[int]] = defaultdict(list)
    signs: dict[int, int] = {}
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in dedupe_candidates(candidates):
        stats["deduped_candidates"] += 1
        A = int(cand["A"]) % q
        x5 = int(cand["x5"]) % q
        X = int(cand["X"]) % q
        d2, branches = halve_all(A, x5, q)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        B = source_b_plus(X, q)
        if B is None:
            stats["b_degenerate"] += 1
            continue
        for x6 in branches:
            groups[B].append(x6 % q)

    for B, roots in groups.items():
        root_signs = {legendre(root, q) for root in roots}
        signs[B] = next(iter(root_signs)) if len(root_signs) == 1 else 0
        if signs[B] == 0:
            stats["mixed_f3_sign_B"] += 1

    stats["B_groups"] = len(groups)
    return dict(groups), signs, stats


def exact_power_sum_hits(
    rows: list[tuple[int, int, list[int]]],
    q: int,
    max_power: int,
    reciprocal: bool,
) -> tuple[list[tuple[int, str, int]], list[tuple[int, int, int, int]]]:
    exact: list[tuple[int, str, int]] = []
    near: list[tuple[int, int, int, int]] = []
    for exponent in range(1, max_power + 1):
        match = 0
        opposite = 0
        zero = 0
        for _B, sign, roots in rows:
            if reciprocal:
                value = sum(
                    (pow(root, exponent, q) + pow(inv(root, q), exponent, q)) % q
                    for root in roots
                    if root
                ) % q
            else:
                value = sum(pow(root, exponent, q) for root in roots) % q
            chi = legendre(value, q) if value else 0
            if chi == 0:
                zero += 1
            elif chi == sign:
                match += 1
            elif chi == -sign:
                opposite += 1
        total = len(rows) - zero
        best = max(match, opposite)
        if total and best == total:
            exact.append((exponent, "match" if match >= opposite else "opposite", zero))
        elif total and best * 4 >= 3 * total:
            near.append((exponent, best, total, zero))
    return exact, near


def coefficient_degrees(
    rows: list[tuple[int, int, list[int]]],
    q: int,
    use_u: bool,
) -> tuple[int, list[int]]:
    if use_u:
        root_sets = [
            (B, sorted({(root + inv(root, q)) % q for root in roots if root}))
            for B, _sign, roots in rows
        ]
    else:
        root_sets = [(B, roots) for B, _sign, roots in rows]
    degrees = {len(roots) for _B, roots in root_sets}
    if len(degrees) != 1:
        raise ValueError(f"varying root-set degrees: {sorted(degrees)}")
    root_degree = next(iter(degrees))
    coeff_points: list[list[tuple[int, int]]] = [[] for _ in range(root_degree)]
    for B, roots in root_sets:
        coeffs = poly_roots_coeffs(roots, q)
        for i in range(root_degree):
            coeff_points[i].append((B, coeffs[i]))
    return root_degree, [interpolation_degree(points, q) for points in coeff_points]


def run_field(q: int, max_power: int, low_degree: int) -> None:
    groups, signs, setup_stats = collect_b_fibers(q)
    rows = [(B, signs[B], sorted(set(roots))) for B, roots in sorted(groups.items())]
    stats = Counter(setup_stats)

    for B, roots in groups.items():
        unique_roots = sorted(set(roots))
        unique_u = sorted({(root + inv(root, q)) % q for root in unique_roots if root})
        stats[f"occurrence_roots_{len(roots)}"] += 1
        stats[f"unique_x_roots_{len(unique_roots)}"] += 1
        stats[f"unique_u_roots_{len(unique_u)}"] += 1
        stats[f"f3_sign_{signs[B]}"] += 1
        stats[f"reciprocal_closed_{all(inv(root, q) in unique_roots for root in unique_roots if root)}"] += 1
        stats[f"negation_closed_{all((-root) % q in unique_roots for root in unique_roots)}"] += 1

        occurrence_product = 1
        for root in roots:
            occurrence_product = occurrence_product * root % q
        stats[f"occurrence_product_chi_{legendre(occurrence_product, q)}"] += 1

        unique_product = 1
        for root in unique_roots:
            unique_product = unique_product * root % q
        stats[f"unique_product_chi_{legendre(unique_product, q)}"] += 1

        u_plus_signs = {legendre((u + 2) % q, q) for u in unique_u}
        stats[f"u_plus_2_sign_classes_{len(u_plus_signs)}"] += 1
        if len(u_plus_signs) == 1 and next(iter(u_plus_signs)) == signs[B]:
            stats["u_plus_2_matches_f3"] += 1

    x_exact, x_near = exact_power_sum_hits(rows, q, max_power=max_power, reciprocal=False)
    r_exact, r_near = exact_power_sum_hits(rows, q, max_power=max_power, reciprocal=True)
    x_degree, x_coeff_degrees = coefficient_degrees(rows, q, use_u=False)
    u_degree, u_coeff_degrees = coefficient_degrees(rows, q, use_u=True)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print(f"  x_unique_polynomial_degree = {x_degree}")
    print(f"  x_coeff_interpolation_degrees = {x_coeff_degrees}")
    print(f"  x_low_coeff_indices_le_{low_degree} = {[i for i, degree in enumerate(x_coeff_degrees) if 0 <= degree <= low_degree]}")
    print(f"  u_polynomial_degree = {u_degree}")
    print(f"  u_coeff_interpolation_degrees = {u_coeff_degrees}")
    print(f"  u_low_coeff_indices_le_{low_degree} = {[i for i, degree in enumerate(u_coeff_degrees) if 0 <= degree <= low_degree]}")
    print(f"  x_power_sum_exact_hits = {x_exact if x_exact else 'none'}")
    print(f"  reciprocal_power_sum_exact_hits = {r_exact if r_exact else 'none'}")
    print(f"  x_power_sum_near_75pct = {x_near if x_near else 'none'}")
    print(f"  reciprocal_power_sum_near_75pct = {r_near if r_near else 'none'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--max-power", type=int, default=64)
    parser.add_argument("--low-degree", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line fiber invariant probe")
    print("question = do simple symmetric invariants of the d3 root fiber expose f3(B)?")
    print(f"small_primes = {args.small_primes}")
    print(f"max_power = {args.max_power}")
    print(f"low_degree_threshold = {args.low_degree}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.max_power, args.low_degree)
    print("p27_b_line_fiber_invariant_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
