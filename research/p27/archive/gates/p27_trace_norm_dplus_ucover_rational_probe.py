#!/usr/bin/env python3
"""Rational reconstruction screen for the post-Dplus four-U cover.

The x6/U-class probe showed that after Dplus, each y has four values

    U = x6 + 1/x6

and the d3 class is chi(x6).  This probe asks whether the quartic

    prod(Z - U_i) = Z^4 - e1 Z^3 + e2 Z^2 - e3 Z + e4

has low-degree rational coefficients in an obvious base coordinate:

    t = y - 1
    a = t - 1/t
    A = a^4/4 - 2

It is a falsifier for a cheap visible four-U source law, not a proof that no
higher-degree or quotient/Prym description exists.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_trace_norm_post_dplus_probe import (
    P,
    candidate_roots,
    sign_name,
    trace_norm_d_class_parts,
    transfer,
    label2,
)
from p27_trace_norm_dplus_a_coordinate_bridge_probe import a_from_t


@dataclass(frozen=True)
class Row:
    t: int
    a: int
    A: int
    coeffs: tuple[int, int, int, int]


def parse_seed_groups(raw: str) -> list[list[int]]:
    groups: list[list[int]] = []
    for part in raw.split(";"):
        part = part.strip()
        if part:
            groups.append(transfer.parse_range(part))
    return groups


def inv(value: int) -> int:
    return transfer.inv(value)


def elementary_symmetric_4(values: list[int]) -> tuple[int, int, int, int]:
    coeffs = [1, 0, 0, 0, 0]
    for value in values:
        for index in range(4, 0, -1):
            coeffs[index] = (coeffs[index] + coeffs[index - 1] * value) % P
    return coeffs[1], coeffs[2], coeffs[3], coeffs[4]


def collect_rows(
    seed_groups: list[list[int]],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    limit: int,
) -> tuple[list[Row], Counter[str]]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    stats: Counter[str] = Counter()
    seen_y: set[int] = set()
    rows: list[Row] = []

    for seeds in seed_groups:
        for seed in seeds:
            for chunk in chunks:
                for tid in tids:
                    rng = transfer.cuda_rng(seed, chunk, tid)
                    for _draw in range(draws_per_thread):
                        y = transfer.rand_below96(rng, P, mask)
                        stats["raw_y_draws"] += 1
                        if y == 0:
                            stats["zero_y"] += 1
                            continue
                        if y in seen_y:
                            stats["duplicate_y"] += 1
                            continue
                        seen_y.add(y)
                        if not transfer.x16_y_predicts_nonsplit(y):
                            continue
                        stats["nonsplit_y"] += 1
                        d_class, _parts = trace_norm_d_class_parts(y)
                        stats[f"D_{sign_name(d_class)}"] += 1
                        if d_class != 1:
                            continue
                        stats["Dplus_y"] += 1

                        t = (y - 1) % P
                        if t == 0:
                            stats["zero_t"] += 1
                            continue
                        A = a_from_t(t)
                        conic_a = (t - inv(t)) % P
                        candidates, _root_disc = candidate_roots(y)
                        if not candidates:
                            stats["Dplus_no_valid_candidate"] += 1
                            continue
                        U_values: set[int] = set()
                        for _root_index, cand_A, xp in candidates:
                            if cand_A % P != A:
                                stats["candidate_A_formula_mismatch"] += 1
                            d1, x5s = label2.halve_all(cand_A, xp)
                            if d1 != 1:
                                stats["d1_failure"] += 1
                                continue
                            for x5 in x5s:
                                d2, x6s = label2.halve_all(cand_A, x5)
                                if d2 != 1:
                                    stats["d2_failure"] += 1
                                    continue
                                for x6 in x6s:
                                    x6 %= P
                                    U_values.add((x6 + inv(x6)) % P)
                        stats[f"U_count_{len(U_values)}"] += 1
                        if len(U_values) != 4:
                            stats["bad_U_count"] += 1
                            continue
                        coeffs = elementary_symmetric_4(sorted(U_values))
                        rows.append(Row(t=t, a=conic_a, A=A, coeffs=coeffs))
                        stats["accepted_rows"] += 1
                        if len(rows) >= limit:
                            return rows, stats
    return rows, stats


def solve_linear(matrix: list[list[int]], vector: list[int]) -> list[int] | None:
    if not matrix:
        return None
    mat = [row[:] + [value % P] for row, value in zip(matrix, vector)]
    nrows = len(mat)
    ncols = len(matrix[0])
    pivot_rows: list[tuple[int, int]] = []
    row_index = 0
    for col in range(ncols):
        pivot = None
        for candidate in range(row_index, nrows):
            if mat[candidate][col] % P:
                pivot = candidate
                break
        if pivot is None:
            continue
        mat[row_index], mat[pivot] = mat[pivot], mat[row_index]
        scale = inv(mat[row_index][col])
        mat[row_index] = [(value * scale) % P for value in mat[row_index]]
        for other in range(nrows):
            if other == row_index or mat[other][col] % P == 0:
                continue
            factor = mat[other][col]
            mat[other] = [
                (mat[other][index] - factor * mat[row_index][index]) % P
                for index in range(ncols + 1)
            ]
        pivot_rows.append((row_index, col))
        row_index += 1
        if row_index == nrows:
            break

    for row in mat:
        if all(row[col] % P == 0 for col in range(ncols)) and row[ncols] % P:
            return None

    solution = [0] * ncols
    for prow, col in pivot_rows:
        solution[col] = mat[prow][ncols]
    return solution


def eval_rational(solution: list[int], degree: int, x: int) -> int | None:
    numerator = 0
    power = 1
    for index in range(degree + 1):
        numerator = (numerator + solution[index] * power) % P
        power = power * x % P

    denominator = 1
    power = x % P
    offset = degree + 1
    for index in range(1, degree + 1):
        denominator = (denominator + solution[offset + index - 1] * power) % P
        power = power * x % P
    if denominator == 0:
        return None
    return numerator * inv(denominator) % P


def fit_rational(samples: list[int], values: list[int], degree: int) -> list[int] | None:
    matrix: list[list[int]] = []
    vector: list[int] = []
    for x, value in zip(samples, values):
        row: list[int] = []
        power = 1
        for _index in range(degree + 1):
            row.append(power)
            power = power * x % P
        power = x % P
        for _index in range(1, degree + 1):
            row.append((-value * power) % P)
            power = power * x % P
        matrix.append(row)
        vector.append(value)

    solution = solve_linear(matrix, vector)
    if solution is None:
        return None
    for x, value in zip(samples, values):
        if eval_rational(solution, degree, x) != value:
            return None
    return solution


def screen(rows: list[Row], train_size: int, max_degree: int) -> list[tuple[str, int, str]]:
    train = rows[:train_size]
    heldout = rows[train_size:]
    variables = [
        ("t", lambda row: row.t),
        ("a", lambda row: row.a),
        ("A", lambda row: row.A),
    ]
    results: list[tuple[str, int, str]] = []
    for name, getter in variables:
        train_x = [getter(row) for row in train]
        heldout_x = [getter(row) for row in heldout]
        for coeff_index in range(4):
            train_y = [row.coeffs[coeff_index] for row in train]
            heldout_y = [row.coeffs[coeff_index] for row in heldout]
            verdict = f"none_deg_le_{max_degree}"
            for degree in range(1, max_degree + 1):
                solution = fit_rational(train_x, train_y, degree)
                if solution is None:
                    continue
                if all(
                    eval_rational(solution, degree, x) == value
                    for x, value in zip(heldout_x, heldout_y)
                ):
                    verdict = f"degree_{degree}"
                    break
            results.append((name, coeff_index + 1, verdict))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-groups", default="121,122;123,124")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=512)
    parser.add_argument("--rows", type=int, default=150)
    parser.add_argument("--train", type=int, default=100)
    parser.add_argument("--max-degree", type=int, default=20)
    args = parser.parse_args()

    rows, stats = collect_rows(
        seed_groups=parse_seed_groups(args.seed_groups),
        chunks=transfer.parse_range(args.chunks),
        tids=transfer.parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        limit=args.rows,
    )
    if len(rows) <= args.train:
        raise SystemExit("not enough rows for heldout screen")

    print("p27 trace/norm Dplus U-cover rational reconstruction probe")
    print("question = do four-U cover coefficients have low-degree rational formulas?")
    print(f"p = {P}")
    print("quartic = prod(Z-U_i) = Z^4 - e1 Z^3 + e2 Z^2 - e3 Z + e4")
    print(f"seed_groups = {args.seed_groups}")
    print(f"chunks = {args.chunks}")
    print(f"tids = {args.tids}")
    print(f"draws_per_thread = {args.draws_per_thread}")
    print(f"rows = {args.rows}")
    print(f"train = {args.train}")
    print(f"heldout = {len(rows) - args.train}")
    print(f"max_degree = {args.max_degree}")
    print("sample_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("screen:")
    for variable, coeff_index, verdict in screen(rows, args.train, args.max_degree):
        print(f"  variable={variable} coeff=e{coeff_index} verdict={verdict}")
    print("verdict:")
    print("  promote_visible_four_U_cover = 0 unless a screen verdict is degree_*")
    print("  continue = CAS/quotient extraction for the four-U cover and x6 class")
    print("p27_trace_norm_dplus_ucover_rational_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
