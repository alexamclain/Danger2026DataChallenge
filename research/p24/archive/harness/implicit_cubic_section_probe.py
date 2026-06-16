#!/usr/bin/env python3
"""Probe low-height implicit cubic sections for p = n^2 + 7.

This extends ``implicit_quadratic_section_probe.py`` by testing equations

    sum_i (a_i*n + b_i) A^i = 0,  i=0..3,

with small integer coefficients and nonzero cubic coefficient.  A persistent
survivor would be a fixed three-valued algebraic construction for the p24
Montgomery parameter.  To keep the test light, the script evaluates each
candidate only on the exact good-A set for each calibration field; a candidate
survives a row iff at least one of those good A values is a root.
"""

from __future__ import annotations

import argparse
import math
from itertools import product

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table


def normalize(values: tuple[int, ...]) -> tuple[int, ...]:
    g = 0
    for value in values:
        g = math.gcd(g, abs(value))
    if g > 1:
        values = tuple(value // g for value in values)
    first = next((value for value in values if value), 0)
    if first < 0:
        values = tuple(-value for value in values)
    return values


def cubic_sections(bound: int) -> list[tuple[int, ...]]:
    vals = range(-bound, bound + 1)
    out: set[tuple[int, ...]] = set()
    for raw in product(vals, repeat=8):
        # Stored high-to-low for stable normalization/labels:
        # c3=(raw0,raw1), c2=(raw2,raw3), c1=(raw4,raw5), c0=(raw6,raw7).
        if raw[0] == raw[1] == 0:
            continue
        out.add(normalize(tuple(raw)))
    return sorted(out, key=lambda row: (sum(abs(v) for v in row), row))


def coeff_values(candidates: np.ndarray, n: int, p: int) -> list[np.ndarray]:
    # Return c0,c1,c2,c3 arrays modulo p.
    c3 = (candidates[:, 0] * n + candidates[:, 1]) % p
    c2 = (candidates[:, 2] * n + candidates[:, 3]) % p
    c1 = (candidates[:, 4] * n + candidates[:, 5]) % p
    c0 = (candidates[:, 6] * n + candidates[:, 7]) % p
    return [c0, c1, c2, c3]


def label(row: tuple[int, ...]) -> str:
    pieces: list[str] = []
    for power, offset in ((3, 0), (2, 2), (1, 4), (0, 6)):
        a, b = row[offset], row[offset + 1]
        if a == 0 and b == 0:
            continue
        if a == 0:
            coeff = str(b)
        elif b == 0:
            coeff = f"{a}*n"
        else:
            sign = "+" if b > 0 else ""
            coeff = f"{a}*n{sign}{b}"
        if power == 0:
            pieces.append(f"({coeff})")
        elif power == 1:
            pieces.append(f"({coeff})*A")
        else:
            pieces.append(f"({coeff})*A^{power}")
    return " + ".join(pieces).replace("+ (-", "- (")


def survivor_mask_for_row(
    candidate_array: np.ndarray,
    survivor_indices: np.ndarray,
    n: int,
    p: int,
    good_roots: np.ndarray,
    chunk_size: int,
) -> np.ndarray:
    if good_roots.size == 0 or survivor_indices.size == 0:
        return np.zeros(survivor_indices.size, dtype=np.bool_)
    powers = [
        np.ones(good_roots.size, dtype=np.int64),
        good_roots.astype(np.int64) % p,
    ]
    powers.append((powers[1] * powers[1]) % p)
    powers.append((powers[2] * powers[1]) % p)

    hit = np.zeros(survivor_indices.size, dtype=np.bool_)
    for start in range(0, survivor_indices.size, chunk_size):
        stop = min(start + chunk_size, survivor_indices.size)
        idxs = survivor_indices[start:stop]
        chunk = candidate_array[idxs]
        coeffs = coeff_values(chunk, n, p)
        values = np.zeros((idxs.size, good_roots.size), dtype=np.int64)
        for coeff, Apow in zip(coeffs, powers):
            values += coeff[:, None] * Apow[None, :]
            values %= p
        hit[start:stop] = np.any(values == 0, axis=1)
    return hit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=220_000)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--coeff-bound", type=int, default=2)
    ap.add_argument("--chunk-size", type=int, default=4096)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    candidates = cubic_sections(args.coeff_bound)
    candidate_array = np.array(candidates, dtype=np.int64)
    survivors = np.arange(len(candidates), dtype=np.int64)
    hit_counts = np.zeros(len(candidates), dtype=np.int16)

    print("implicit cubic near-square section probe")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"section_count={len(candidates)}")

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        good_roots = np.flatnonzero(good).astype(np.int64)
        mask = survivor_mask_for_row(candidate_array, survivors, n, p, good_roots, args.chunk_size)
        hit_indices = survivors[mask]
        hit_counts[hit_indices] += 1
        print(
            f"row={row_index:02d} n={n} p={p} k={stats['k']} "
            f"good={stats['good']}/{stats['nonsingular']} "
            f"tested_survivors={survivors.size} "
            f"hit_survivors={hit_indices.size}"
        )
        survivors = hit_indices
        if survivors.size == 0:
            break

    ranked = sorted(
        range(len(candidates)),
        key=lambda idx: (int(hit_counts[idx]), -sum(abs(v) for v in candidates[idx])),
        reverse=True,
    )
    print("top_sections_by_hit_count")
    for idx in ranked[: args.top]:
        print(f"  hits={int(hit_counts[idx]):2d} section={label(candidates[idx])}")

    print(f"perfect_survivor_count={survivors.size}")
    for idx in survivors[: args.top]:
        print(f"  survivor={label(candidates[int(idx)])}")
    print(
        "conclusion=no_low_height_implicit_cubic_section"
        if survivors.size == 0
        else "conclusion=surviving_implicit_cubic_section_lead"
    )


if __name__ == "__main__":
    main()
