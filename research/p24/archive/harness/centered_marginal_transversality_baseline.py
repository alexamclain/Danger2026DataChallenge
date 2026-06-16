#!/usr/bin/env python3
"""Random-Grassmannian baseline for the centered marginal plateau theorem.

The p24 centered-profile route asks a 156-dimensional row space in the
centered hyperplane `w_0=0` of dimension 210 to avoid 211 centered plateau
subspaces.  For a fixed plateau, the centered plateau subspace has dimension
54, so the dimensions are complementary:

    156 + 54 = 210.

This script computes the exact random-subspace probability that a uniformly
random 156-plane in the centered hyperplane intersects one fixed centered
plateau subspace nontrivially.  It is not a certificate.  It is a calibration
for theorem search: any probabilistic or equidistribution import must lift
this Schubert-divisor avoidance to the actual CM trace-form subspace.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext


def fixed_failure_probability(q: int, k: int, u: int, precision: int) -> Decimal:
    """Probability a random k-plane in F_q^(k+u) meets a fixed u-plane."""

    getcontext().prec = precision
    qq = Decimal(q)
    disjoint = Decimal(1)
    for i in range(1, k + 1):
        disjoint *= (Decimal(1) - qq ** Decimal(-i))
        disjoint /= (Decimal(1) - qq ** Decimal(-(u + i)))
    return Decimal(1) - disjoint


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=10**24 + 7)
    parser.add_argument("--ambient", type=int, default=210)
    parser.add_argument("--row-dim", type=int, default=156)
    parser.add_argument("--plateau-length", type=int, default=157)
    parser.add_argument("--right", type=int, default=211)
    parser.add_argument("--window-count", type=int, default=211)
    parser.add_argument("--precision", type=int, default=80)
    args = parser.parse_args()

    plateau_constraints = args.plateau_length - 1
    plateau_dim = args.right - args.plateau_length
    if args.row_dim + plateau_dim != args.ambient:
        raise SystemExit("this calibration expects complementary dimensions")

    fixed = fixed_failure_probability(
        args.q,
        args.row_dim,
        plateau_dim,
        args.precision,
    )
    union = min(Decimal(args.window_count) * fixed, Decimal(1))

    print("Centered marginal transversality baseline")
    print(f"q={args.q}")
    print(f"centered_ambient_dim={args.ambient}")
    print(f"right={args.right}")
    print(f"row_dim={args.row_dim}")
    print(f"plateau_length={args.plateau_length}")
    print(f"plateau_constraints={plateau_constraints}")
    print(f"centered_plateau_subspace_dim={plateau_dim}")
    print(f"dimension_sum={args.row_dim + plateau_dim}")
    print(f"window_count={args.window_count}")
    print(f"fixed_plateau_failure_probability={fixed:.12E}")
    print(f"union_bound_any_plateau_failure={union:.12E}")
    print()
    print("interpretation")
    print("  random_transversality_predicts_success=1")
    print("  event_is_a_schubert_divisor_not_a_sparse_fourier_event=1")
    print("  probability_is_not_a_certificate_without_arithmetic_lift=1")
    print("conclusion=reported_centered_marginal_transversality_baseline")


if __name__ == "__main__":
    main()
