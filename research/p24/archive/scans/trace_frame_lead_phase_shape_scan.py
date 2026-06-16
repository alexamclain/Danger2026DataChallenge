#!/usr/bin/env python3
"""Phase-coordinate shape diagnostic for the leading trace-frame determinant.

The plain-j scan showed that the leading determinant norm has Frobenius-packet
periodicity but does not look like a low-degree divisor in the selected
j-coordinate.  This script tests the next simplest phase-aware coordinate:

    (j_i, j_{i+step}).

It asks whether the determinant norm is a low-bidegree polynomial or rational
function of this oriented edge, and compares with random controls that preserve
the observed origin period.
"""

from __future__ import annotations

import argparse
import random

from packet_scalar_edge_shape_scan import (
    first_polynomial_bidegree,
    first_rational_bidegree,
)
from trace_frame_lead_divisor_support_scan import fixed_cycle, lead_norm_pairs, minimal_period


def periodic_random_values(length: int, period: int, q: int, rng: random.Random) -> list[int]:
    if period <= 0 or length % period != 0:
        return [rng.randrange(q) for _ in range(length)]
    base = [rng.randrange(q) for _ in range(period)]
    return [base[i % period] for i in range(length)]


def variables(pair: tuple[int, int] | None) -> int | None:
    if pair is None:
        return None
    return (pair[0] + 1) * (pair[1] + 1)


def fmt_pair(pair: tuple[int, int] | None) -> str:
    return "none" if pair is None else f"{pair[0]},{pair[1]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--D", type=int, default=-10919)
    parser.add_argument("--q", type=int, default=11243)
    parser.add_argument("--ell", type=int, default=2)
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--factor-index", type=int, default=0)
    parser.add_argument("--subdegree", type=int, default=2)
    parser.add_argument("--target", default="axis")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--max-bidegree", type=int, default=5)
    parser.add_argument("--random-trials", type=int, default=12)
    parser.add_argument("--random-combos", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-top-count", type=int, default=4)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    cycle = fixed_cycle(args.D, args.q, args.ell)
    pairs, metadata = lead_norm_pairs(
        cycle,
        args.q,
        args.m,
        args.factor_index,
        args.subdegree,
        args.target,
        args.seed,
        args.max_top_count,
    )
    h = len(cycle)
    if len(pairs) != h:
        raise RuntimeError("phase scan expects one value at every origin")
    ys = [value for _, value in pairs]
    xs = [cycle[i] % args.q for i in range(h)]
    zs = [cycle[(i + args.step) % h] % args.q for i in range(h)]
    period = minimal_period(ys)

    poly = first_polynomial_bidegree(xs, zs, ys, args.q, args.max_bidegree)
    rat = first_rational_bidegree(
        xs,
        zs,
        ys,
        args.q,
        args.max_bidegree,
        rng,
        args.random_combos,
    )
    poly_hits = 0
    rat_hits = 0
    for _ in range(args.random_trials):
        random_ys = periodic_random_values(h, period, args.q, rng)
        if first_polynomial_bidegree(xs, zs, random_ys, args.q, args.max_bidegree) is not None:
            poly_hits += 1
        if first_rational_bidegree(
            xs,
            zs,
            random_ys,
            args.q,
            args.max_bidegree,
            rng,
            args.random_combos,
        ) is not None:
            rat_hits += 1

    print("trace-frame leading phase-shape scan")
    print(f"D={args.D}")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"h={h}")
    print(f"m={args.m}")
    print(f"n={metadata['n']}")
    print(f"factor_index={args.factor_index}")
    print(f"factor_degree={metadata['factor_degree']}")
    print(f"tensor_factor_degree={metadata['tensor_factor_degree']}")
    print(f"subdegree={args.subdegree}")
    print(f"raw_rank={metadata['raw_rank']}")
    print(f"top_count={metadata['top_count']}")
    print(f"step={args.step % h}")
    print(f"origin_value_period={period}")
    print(f"origin_value_orbit_size={h // period if period else 0}")
    print(f"distinct_norm_values={len(set(ys))}")
    print(f"max_bidegree={args.max_bidegree}")
    print(f"poly_bidegree={fmt_pair(poly)}")
    print(f"poly_variables={variables(poly)}")
    print(f"poly_random_hits={poly_hits}/{args.random_trials}")
    print(f"rat_bidegree={fmt_pair(rat)}")
    print(f"rat_variables={variables(rat)}")
    print(f"rat_random_hits={rat_hits}/{args.random_trials}")
    print()
    print("interpretation")
    print("  random_controls_preserve_origin_period=1")
    print("  low_phase_fit_without_random_hits_supports_phase_identity=" + str(int((poly is not None and poly_hits == 0) or (rat is not None and rat_hits == 0))))
    print("  no_phase_fit_or_random_explained_fit_closes_simple_edge_route=" + str(int((poly is None or poly_hits > 0) and (rat is None or rat_hits > 0))))
    print("conclusion=reported_trace_frame_lead_phase_shape_scan")


if __name__ == "__main__":
    main()
