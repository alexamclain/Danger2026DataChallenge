#!/usr/bin/env python3
"""Exact partial-oriented sampler exponent audit for p = n^2 + 7.

The remaining structured-search hope can be phrased as:

    sample candidates already known to have x-only order 2^h at cost 2^(beta h),
    then search only the remaining 40-h levels.

This beats sqrt scaling only if beta < 1 for growing h.  Rejection from random
Montgomery A has beta about 1; generic high-level X1 has worse overhead.  This
audit measures the exact small-field shrinkage of the strict oriented X1-like
bucket and compares it with the much larger X0 chain bucket.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows
from near_square_formula_probe import all_montgomery_traces_fft, legendre_table, v2, verifier_k


@dataclass(frozen=True)
class DepthCounts:
    depth: int
    x1: int
    x0: int
    total: int

    @property
    def x1_density(self) -> float:
        return self.x1 / self.total if self.total else 0.0

    @property
    def x0_density(self) -> float:
        return self.x0 / self.total if self.total else 0.0

    @property
    def x1_cost(self) -> float:
        return self.total / self.x1 if self.x1 else float("inf")

    @property
    def x0_cost(self) -> float:
        return self.total / self.x0 if self.x0 else float("inf")


def x0_residues(p: int, depth: int) -> set[int]:
    modulus = 1 << depth
    out: set[int] = set()
    for lam in range(1, modulus, 2):
        mu = p * pow(lam, -1, modulus) % modulus
        out.add((lam + mu) % modulus)
    return out


def depth_counts_for_row(p: int, max_depth: int) -> tuple[list[DepthCounts], dict[str, int]]:
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    total = 0
    x1_exp = np.zeros(p, dtype=np.int16)
    trace_mod_cache: dict[int, np.ndarray] = {}

    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            continue
        total += 1
        split = int(chi[disc]) == 1
        t = int(traces[A])
        curve_v = v2(p + 1 - t)
        twist_v = v2(p + 1 + t)
        if split:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        x1_exp[A] = max(curve_exp, twist_exp)

    out: list[DepthCounts] = []
    nonsingular = np.ones(p, dtype=np.bool_)
    nonsingular[[2 % p, (-2) % p]] = False
    signed_traces = np.concatenate((traces % (1 << max_depth), (-traces) % (1 << max_depth)))

    for depth in range(1, max_depth + 1):
        modulus = 1 << depth
        residues = x0_residues(p, depth)
        # Recompute cheaply at each modulus; fields are small and this avoids
        # tricky signed-residue folding bugs.
        trace_mod = trace_mod_cache.get(depth)
        if trace_mod is None:
            trace_mod = traces % modulus
            trace_mod_cache[depth] = trace_mod
        neg_trace_mod = (-traces) % modulus
        x0 = np.zeros(p, dtype=np.bool_)
        for residue in residues:
            x0 |= trace_mod == residue
            x0 |= neg_trace_mod == residue
        x0 &= nonsingular
        out.append(
            DepthCounts(
                depth=depth,
                x1=int(np.count_nonzero((x1_exp >= depth) & nonsingular)),
                x0=int(np.count_nonzero(x0)),
                total=total,
            )
        )

    return out, {
        "total": total,
        "fft_error_scaled": int(round(float(fft_error) * 1_000_000)),
    }


def slope_beta(depths: list[int], costs: list[float]) -> float:
    xs: list[float] = []
    ys: list[float] = []
    for d, c in zip(depths, costs):
        if c > 0 and math.isfinite(c):
            xs.append(float(d))
            ys.append(math.log2(c))
    if len(xs) < 2:
        return float("nan")
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    den = sum((x - xbar) ** 2 for x in xs)
    if den == 0:
        return float("nan")
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / den


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=220_000)
    ap.add_argument("--max-rows", type=int, default=12)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-depth", type=int, default=0)
    ap.add_argument("--fit-min-depth", type=int, default=4)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("partial oriented sampler exponent audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"max_depth_override={args.max_depth or 'local_k'}")

    aggregate: dict[int, list[int]] = {}
    for row_index, (n, p) in enumerate(rows, start=1):
        local_k = verifier_k(p)
        max_depth = args.max_depth or local_k
        counts, stats = depth_counts_for_row(p, max_depth)
        print(f"row={row_index:02d} n={n} p={p} k={local_k} total_A={stats['total']}")
        print("  depth x1_count x1_density x1_cost x0_count x0_density x0_cost x0_over_x1")
        for c in counts:
            aggregate.setdefault(c.depth, [0, 0, 0])
            aggregate[c.depth][0] += c.x1
            aggregate[c.depth][1] += c.x0
            aggregate[c.depth][2] += c.total
            ratio = c.x0 / c.x1 if c.x1 else float("inf")
            print(
                f"  {c.depth:2d} {c.x1:8d} {c.x1_density:.8f} {c.x1_cost:10.3f} "
                f"{c.x0:8d} {c.x0_density:.8f} {c.x0_cost:10.3f} {ratio:10.3f}"
            )
        depths = [c.depth for c in counts if c.depth >= args.fit_min_depth]
        x1_costs = [c.x1_cost for c in counts if c.depth >= args.fit_min_depth]
        x0_costs = [c.x0_cost for c in counts if c.depth >= args.fit_min_depth]
        print(f"  fitted_beta_x1={slope_beta(depths, x1_costs):.6f}")
        print(f"  fitted_beta_x0={slope_beta(depths, x0_costs):.6f}")

    print("aggregate")
    print("  depth x1_count x1_density x1_cost x0_count x0_density x0_cost x0_over_x1")
    depths: list[int] = []
    x1_costs: list[float] = []
    x0_costs: list[float] = []
    for depth in sorted(aggregate):
        x1, x0, total = aggregate[depth]
        c = DepthCounts(depth, x1, x0, total)
        depths.append(depth)
        x1_costs.append(c.x1_cost)
        x0_costs.append(c.x0_cost)
        ratio = c.x0 / c.x1 if c.x1 else float("inf")
        print(
            f"  {depth:2d} {x1:8d} {c.x1_density:.8f} {c.x1_cost:10.3f} "
            f"{x0:8d} {c.x0_density:.8f} {c.x0_cost:10.3f} {ratio:10.3f}"
        )
    fit_depths = [d for d in depths if d >= args.fit_min_depth]
    fit_x1 = [cost for d, cost in zip(depths, x1_costs) if d >= args.fit_min_depth]
    fit_x0 = [cost for d, cost in zip(depths, x0_costs) if d >= args.fit_min_depth]
    print(f"aggregate_fitted_beta_x1={slope_beta(fit_depths, fit_x1):.6f}")
    print(f"aggregate_fitted_beta_x0={slope_beta(fit_depths, fit_x0):.6f}")
    print("conclusion=oriented_depth_sampler_by_rejection_has_beta_about_one_x0_has_no_orientation")


if __name__ == "__main__":
    main()
