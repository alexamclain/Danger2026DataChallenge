#!/usr/bin/env python3
"""Oriented-edge boundary for the centered full-origin product.

If the centered full-origin p-unit came from a bounded local modular
correspondence, a natural first model would be a low-bidegree function of an
oriented edge in the split-prime class cycle:

    Delta_origin(i) = R(j_i, j_{i+1}).

This boundary tests that model on the pinned actual-CM row used by the
centered full-origin gates.  The determinant is repeated along the beta
direction but the oriented edge varies through the full class cycle; no
polynomial or rational expression of bidegree <= 4 is found.
"""

from __future__ import annotations

import argparse
import random

from packet_scalar_edge_shape_scan import (
    first_polynomial_bidegree,
    first_rational_bidegree,
)
from centered_marginal_full_origin_phase_sensitivity_gate import pinned_args
from centered_marginal_origin_product_audit import scan


MAX_BIDEGREE = 4
RANDOM_CONTROLS = 8
RANDOM_COMBOS = 8
SEED = 20260606


def edge_samples(row, edge_step: int) -> tuple[list[int], list[int], list[int]]:
    xs: list[int] = []
    zs: list[int] = []
    ys: list[int] = []
    cycle = list(row.cycle)
    for alpha, value in enumerate(row.alpha_values):
        for beta in range(row.n):
            shift = (row.n * alpha + row.m * beta) % row.h
            xs.append(cycle[shift] % row.q)
            zs.append(cycle[(shift + edge_step) % row.h] % row.q)
            ys.append(value % row.q)
    return xs, zs, ys


def random_repeated_alpha_values(row, rng: random.Random) -> list[int]:
    ys: list[int] = []
    for _alpha in range(row.m):
        value = rng.randrange(row.q)
        ys.extend([value] * row.n)
    return ys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-step", type=int, default=1)
    parser.add_argument("--max-bidegree", type=int, default=MAX_BIDEGREE)
    parser.add_argument("--random-controls", type=int, default=RANDOM_CONTROLS)
    parser.add_argument("--random-combos", type=int, default=RANDOM_COMBOS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    row = scan(pinned_args())
    if row is None:
        raise SystemExit("pinned row not found")

    xs, zs, ys = edge_samples(row, args.edge_step)
    rng = random.Random(args.seed)
    poly = first_polynomial_bidegree(xs, zs, ys, row.q, args.max_bidegree)
    rat = first_rational_bidegree(
        xs,
        zs,
        ys,
        row.q,
        args.max_bidegree,
        rng,
        args.random_combos,
    )

    random_poly_hits = 0
    random_rat_hits = 0
    for _trial in range(args.random_controls):
        random_ys = random_repeated_alpha_values(row, rng)
        random_poly_hits += int(
            first_polynomial_bidegree(
                xs,
                zs,
                random_ys,
                row.q,
                args.max_bidegree,
            )
            is not None
        )
        random_rat_hits += int(
            first_rational_bidegree(
                xs,
                zs,
                random_ys,
                row.q,
                args.max_bidegree,
                rng,
                args.random_combos,
            )
            is not None
        )

    print("Centered marginal full-origin oriented-edge shape boundary")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"edge_step={args.edge_step}")
    print(f"sample_count={len(xs)}")
    print(f"distinct_edge_x={len(set(xs))}")
    print(f"distinct_edge_pairs={len(set(zip(xs, zs)))}")
    print(f"determinant_distinct_values={len(set(ys))}")
    print(f"max_bidegree={args.max_bidegree}")
    print(f"first_polynomial_bidegree_leq_{args.max_bidegree}={poly}")
    print(f"first_rational_bidegree_leq_{args.max_bidegree}={rat}")
    print(f"random_repeated_alpha_polynomial_hits={random_poly_hits}/{args.random_controls}")
    print(f"random_repeated_alpha_rational_hits={random_rat_hits}/{args.random_controls}")
    print("interpretation")
    print("  centered_full_origin_product_is_not_bounded_oriented_edge_function=1")
    print("  bounded_local_correspondence_norm_needs_more_than_one_edge=1")
    print("  phase_aware_fitting_divisor_still_required=1")
    print("conclusion=reported_centered_marginal_full_origin_edge_shape_boundary")

    if (row.D, row.q, row.m, row.n, row.left, row.right) != (-13319, 13463, 28, 5, 4, 7):
        raise SystemExit(1)
    if poly is not None or rat is not None:
        raise SystemExit(1)
    if random_poly_hits or random_rat_hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
