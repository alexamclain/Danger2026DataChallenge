#!/usr/bin/env python3
"""Audit dyadic residues of A and j as strict trace-v2 labels.

The remaining live constructive shape is a cheap curve-level label that
predicts the high 2-adic Frobenius condition.  Since the verifier target is
itself a 2-power condition, this script focuses on integer representatives
modulo 2^b:

    A mod 2^b,      j(A) mod 2^b.

For exact small p=n^2+7 rows it computes the strict x-only good set, then
aggregates bucket lift/capture over dyadic moduli.  A real construction-level
label should show a stable growing lift with non-negligible capture; random
small buckets only move constants around.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table, montgomery_j_from_A


@dataclass(frozen=True)
class Bucket:
    kind: str
    bits: int
    residue: int
    hits: int
    total: int
    lift: float
    capture: float
    coverage: float
    score: float


def row_values(p: int, kind: str, nonsingular: np.ndarray) -> np.ndarray:
    values = np.zeros(p, dtype=np.int64)
    if kind == "A":
        values[:] = np.arange(p, dtype=np.int64)
        return values
    if kind == "j":
        for A in np.nonzero(nonsingular)[0]:
            values[A] = montgomery_j_from_A(int(A), p)
        return values
    raise ValueError(kind)


def aggregate(rows: list[tuple[int, int]], max_bits: int, kinds: list[str]) -> tuple[list[Bucket], int, int]:
    hit_totals: dict[tuple[str, int, int], int] = {}
    total_totals: dict[tuple[str, int, int], int] = {}
    all_hits = 0
    all_total = 0

    for _n, p in rows:
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        nonsingular = np.ones(p, dtype=np.bool_)
        nonsingular[[2 % p, (-2) % p]] = False
        good &= nonsingular
        all_hits += int(stats["good"])
        all_total += int(stats["nonsingular"])

        for kind in kinds:
            values = row_values(p, kind, nonsingular)
            selected_values = values[nonsingular]
            selected_good = good[nonsingular]
            for bits in range(1, max_bits + 1):
                modulus = 1 << bits
                residues = selected_values & (modulus - 1)
                totals = np.bincount(residues, minlength=modulus)
                hits = np.bincount(residues, weights=selected_good.astype(np.int64), minlength=modulus)
                for residue in range(modulus):
                    key = (kind, bits, residue)
                    total_totals[key] = total_totals.get(key, 0) + int(totals[residue])
                    hit_totals[key] = hit_totals.get(key, 0) + int(hits[residue])

    base = all_hits / all_total if all_total else 0.0
    buckets: list[Bucket] = []
    for key, total in total_totals.items():
        hits = hit_totals.get(key, 0)
        if not total or not all_hits or not all_total:
            continue
        kind, bits, residue = key
        precision = hits / total
        lift = precision / base if base else 0.0
        capture = hits / all_hits
        coverage = total / all_total
        score = lift * math.sqrt(capture)
        buckets.append(
            Bucket(
                kind=kind,
                bits=bits,
                residue=residue,
                hits=hits,
                total=total,
                lift=lift,
                capture=capture,
                coverage=coverage,
                score=score,
            )
        )
    return buckets, all_hits, all_total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=250_000)
    ap.add_argument("--max-rows", type=int, default=12)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-bits", type=int, default=12)
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    buckets, all_hits, all_total = aggregate(rows, args.max_bits, ["A", "j"])
    base = all_hits / all_total if all_total else 0.0

    print("dyadic A/j residue strict trace-v2 audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"max_bits={args.max_bits}")
    print(f"good={all_hits}/{all_total}")
    print(f"base_rate={base:.8f}")
    print()

    for kind in ("A", "j"):
        print(f"{kind}_best_by_bits")
        for bits in range(1, args.max_bits + 1):
            candidates = [b for b in buckets if b.kind == kind and b.bits == bits]
            best_lift = max(candidates, key=lambda b: (b.lift, b.capture))
            best_score = max(candidates, key=lambda b: (b.score, b.lift))
            print(
                f"  bits={bits:2d} "
                f"best_lift r={best_lift.residue:5d} lift={best_lift.lift:.3f} "
                f"capture={best_lift.capture:.4f} hits={best_lift.hits}/{best_lift.total} "
                f"best_score r={best_score.residue:5d} score={best_score.score:.3f} "
                f"lift={best_score.lift:.3f} capture={best_score.capture:.4f}"
            )
        print()

    ranked = sorted(buckets, key=lambda b: (b.score, b.lift), reverse=True)
    print("top_buckets_by_score")
    for b in ranked[: args.top]:
        print(
            f"  {b.kind} bits={b.bits:2d} r={b.residue:5d} "
            f"lift={b.lift:.3f} capture={b.capture:.4f} coverage={b.coverage:.4f} "
            f"hits={b.hits}/{b.total} score={b.score:.3f}"
        )
    print(
        "conclusion=dyadic_A_or_j_residues_show_only_constant_bucket_lifts_not_a_"
        "growing_trace_v2_selector"
    )


if __name__ == "__main__":
    main()
