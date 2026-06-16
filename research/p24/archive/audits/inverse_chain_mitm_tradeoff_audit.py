#!/usr/bin/env python3
"""Exact small-field tradeoff audit for inverse-chain MITM splits.

The tempting inverse-chain strategy is:

    1. construct a curve with an x-only point of order 2^h;
    2. lift the remaining k-h levels by a baby-step/giant-step or inverse tree.

This beats sqrt scaling only if the first stage and residual stage do not
multiply back to the full 2^k trace entropy.  This audit computes exact
Montgomery traces over small primes p = n^2 + 7 and measures, for every split
depth h, the conditional probability that a partial-depth curve is also a
full-depth curve.

It also prints the weaker X0/cyclic-subgroup conditioning.  X0 depth can be
large at almost no cost in this congruence class, precisely because it omits
the orientation needed by the verifier.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows
from near_square_formula_probe import all_montgomery_traces_fft, legendre_table, v2, verifier_k
from partial_oriented_sampler_exponent_audit import x0_residues


@dataclass(frozen=True)
class SplitRow:
    depth: int
    total: int
    full: int
    x1_partial: int
    x0_partial: int

    @property
    def full_density(self) -> float:
        return self.full / self.total if self.total else 0.0

    @property
    def x1_density(self) -> float:
        return self.x1_partial / self.total if self.total else 0.0

    @property
    def x0_density(self) -> float:
        return self.x0_partial / self.total if self.total else 0.0

    @property
    def x1_residual(self) -> float:
        return self.full / self.x1_partial if self.x1_partial else 0.0

    @property
    def x0_residual(self) -> float:
        return self.full / self.x0_partial if self.x0_partial else 0.0

    @property
    def x1_stage_cost(self) -> float:
        return self.total / self.x1_partial if self.x1_partial else float("inf")

    @property
    def x0_stage_cost(self) -> float:
        return self.total / self.x0_partial if self.x0_partial else float("inf")

    @property
    def x1_residual_cost(self) -> float:
        return self.x1_partial / self.full if self.full else float("inf")

    @property
    def x0_residual_cost(self) -> float:
        return self.x0_partial / self.full if self.full else float("inf")


def exact_exponents(p: int, max_depth: int) -> tuple[np.ndarray, np.ndarray, int, float]:
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    x1_exp = np.zeros(p, dtype=np.int16)
    nonsingular = np.ones(p, dtype=np.bool_)
    nonsingular[[2 % p, (-2) % p]] = False

    for A in range(p):
        if not bool(nonsingular[A]):
            continue
        split = int(chi[(A * A - 4) % p]) == 1
        t = int(traces[A])
        curve_v = v2(p + 1 - t)
        twist_v = v2(p + 1 + t)
        if split:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        x1_exp[A] = min(max(curve_exp, twist_exp), max_depth)

    return traces, x1_exp, int(np.count_nonzero(nonsingular)), float(fft_error)


def x0_mask_for_depth(p: int, traces: np.ndarray, depth: int) -> np.ndarray:
    modulus = 1 << depth
    trace_mod = traces % modulus
    neg_trace_mod = (-traces) % modulus
    mask = np.zeros(p, dtype=np.bool_)
    for residue in x0_residues(p, depth):
        mask |= trace_mod == residue
        mask |= neg_trace_mod == residue
    mask[[2 % p, (-2) % p]] = False
    return mask


def audit_one(n: int, p: int, depths: list[int]) -> list[SplitRow]:
    k = verifier_k(p)
    traces, x1_exp, total, fft_error = exact_exponents(p, k)
    full_mask = x1_exp >= k
    full = int(np.count_nonzero(full_mask))
    rows: list[SplitRow] = []
    print(f"row n={n} p={p} k={k} total_A={total} full={full} full_density={full/total:.8f} fft_error={fft_error:.2e}")
    print("  h x1_partial x1_density x1_residual x1_stage*x1_residual x0_partial x0_density x0_residual x0_stage*x0_residual")
    for h in depths:
        if h > k:
            continue
        x1_partial = int(np.count_nonzero(x1_exp >= h))
        x0_partial = int(np.count_nonzero(x0_mask_for_depth(p, traces, h)))
        row = SplitRow(h, total, full, x1_partial, x0_partial)
        rows.append(row)
        x1_product = row.x1_stage_cost * row.x1_residual_cost
        x0_product = row.x0_stage_cost * row.x0_residual_cost
        print(
            f"  {h:2d} {x1_partial:10d} {row.x1_density:.8f} {row.x1_residual:.8f} "
            f"{x1_product:20.6f} {x0_partial:10d} {row.x0_density:.8f} "
            f"{row.x0_residual:.8f} {x0_product:20.6f}"
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=220_000)
    ap.add_argument("--max-rows", type=int, default=8)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--depths", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7, 8, 10, 12])
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("inverse-chain MITM split tradeoff audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"depths={args.depths}")

    aggregate: dict[int, list[int]] = {}
    for n, p in rows:
        for row in audit_one(n, p, args.depths):
            acc = aggregate.setdefault(row.depth, [0, 0, 0, 0])
            acc[0] += row.total
            acc[1] += row.full
            acc[2] += row.x1_partial
            acc[3] += row.x0_partial

    print("aggregate")
    print("  h total full x1_partial x1_residual x1_product x0_partial x0_residual x0_product")
    for h in sorted(aggregate):
        total, full, x1_partial, x0_partial = aggregate[h]
        row = SplitRow(h, total, full, x1_partial, x0_partial)
        print(
            f"  {h:2d} {total:8d} {full:6d} {x1_partial:10d} "
            f"{row.x1_residual:.8f} {row.x1_stage_cost * row.x1_residual_cost:12.6f} "
            f"{x0_partial:10d} {row.x0_residual:.8f} "
            f"{row.x0_stage_cost * row.x0_residual_cost:12.6f}"
        )

    print("conclusion=partial_depth_or_X0_conditioning_moves_entropy_between_stages_but_the_product_remains_the_full_depth_cost")


if __name__ == "__main__":
    main()
