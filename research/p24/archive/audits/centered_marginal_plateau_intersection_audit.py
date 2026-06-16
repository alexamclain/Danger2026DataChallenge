#!/usr/bin/env python3
"""Audit plateau-subspace intersections for centered marginal trace codes.

For point columns P_b, the dual trace code is the row span of the point
matrix P.  A right-window factor vanishes exactly when this row span meets the
subspace of words constant on a cyclic plateau.

This script also tests whether the row span is stable under the multiplicative
Frobenius permutation b -> q*b, a possible stronger symmetry than cyclic
shift-invariance.
"""

from __future__ import annotations

import argparse

from centered_marginal_cyclic_code_boundary import (
    point_matrix,
    scan as scan_cyclic_boundary,
    shift_row,
)
from l1_axis_injectivity_scan import rank_mod_q


def permute_row(row: list[int], multiplier: int) -> list[int]:
    n = len(row)
    out = [0 for _ in range(n)]
    for index, value in enumerate(row):
        out[(multiplier * index) % n] = value
    return out


def plateau_constraint_rows(length: int, start: int, plateau: int) -> list[list[int]]:
    """Rows cutting out words constant on start,...,start+plateau-1."""

    rows: list[list[int]] = []
    base = start % length
    for offset in range(1, plateau):
        row = [0 for _ in range(length)]
        row[base] = 1
        row[(start + offset) % length] = -1
        rows.append(row)
    return rows


def rank_with_constraints(
    generators: list[list[int]],
    constraints: list[list[int]],
    q: int,
) -> int:
    """Dimension of rowspace(generators) intersect kernel(constraints)."""

    if not generators:
        return 0
    code_rank = rank_mod_q(generators, q)
    products = [
        [
            sum(row[i] * constraint[i] for i in range(len(row))) % q
            for constraint in constraints
        ]
        for row in generators
    ]
    image_rank = rank_mod_q(products, q)
    return code_rank - image_rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    args = parser.parse_args()

    row = scan_cyclic_boundary(args)
    if row is None:
        raise SystemExit("no eligible case found")

    # Rebuild the point matrix via the row values in the boundary audit would
    # require changing its return type; instead reuse its private construction
    # by reconstructing from the determinant sequence is impossible.  Importing
    # the scan result is enough metadata, so call a tiny helper copied from the
    # boundary module through a second scan is avoided by storing only ranks.
    #
    # The boundary scan does not expose P.  For this audit, recompute by using
    # the same lower-level helper through a local import path.
    from centered_marginal_cyclic_code_boundary import audit_case
    from crt_partial_moment_projection_scan import coprime_components
    from cycle_period_complexity_scan import find_full_cycle_prime
    from cypari2 import Pari
    from hermitian_double_marginal_audit import double_marginal, kernel_matrix
    from l1_axis_injectivity_scan import discriminants
    from packetized_relative_content_scan import packet_factors
    from relative_moment_projection_scan import (
        find_splitting_primes,
        quotient_sizes_any,
        section_fiber_polynomials,
    )
    import sympy as sp
    from math import gcd

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    matrix: list[list[int]] | None = None
    for D in discriminants(args.max_abs_D, args.only_D):
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if h != row.h:
            continue
        for q, roots in find_splitting_primes(
            pari, hilbert, h, args.q_start, args.q_stop, args.max_splitting_primes
        ):
            if q != row.q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            _ell, cycle = full
            for m in quotient_sizes_any(
                h,
                max_prime=args.max_prime_quotients,
                max_composite=args.max_composite_quotients,
                min_n=args.min_n,
                max_n=args.max_n,
            ):
                if m != row.m or gcd(m, h // m) != 1:
                    continue
                for factor in packet_factors(h // m, q):
                    if factor.degree() != row.factor_degree:
                        continue
                    candidate = audit_case(D, q, row.ell, cycle, m, factor, row.left, row.right)
                    if candidate is None:
                        continue
                    residues = [
                        fiber.rem(factor)
                        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
                    ]
                    marginal = double_marginal(
                        kernel_matrix(residues, factor, q), row.left, row.right, q
                    )
                    matrix = point_matrix(marginal, row.left, row.right, q)
                    break
                if matrix is not None:
                    break
            if matrix is not None:
                break
        if matrix is not None:
            break
    if matrix is None:
        raise RuntimeError("failed to reconstruct point matrix")

    code_rank = rank_mod_q(matrix, row.q)
    shift_span = rank_mod_q(matrix + [shift_row(r, 1) for r in matrix], row.q)
    mult = row.q % row.right
    multiplier_span = rank_mod_q(matrix + [permute_row(r, mult) for r in matrix], row.q)
    plateau_dims = [
        rank_with_constraints(
            matrix,
            plateau_constraint_rows(row.right, start, row.left),
            row.q,
        )
        for start in range(row.right)
    ]

    print("Centered marginal plateau-intersection audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"code_rank={code_rank}")
    print(f"cyclic_shift_span_rank={shift_span}")
    print(f"frobenius_multiplier={mult}")
    print(f"frobenius_multiplier_span_rank={multiplier_span}")
    print(f"plateau_intersection_dims={plateau_dims}")
    print(f"max_plateau_intersection_dim={max(plateau_dims)}")
    print(f"zero_plateau_intersections={sum(1 for d in plateau_dims if d == 0)}/{len(plateau_dims)}")
    print()
    print("interpretation")
    print("  plateau_intersection_zero_equiv_all_window_factors_nonzero=1")
    print("  multiplier_stability_would_give_extra_frobenius_symmetry=1")
    print("conclusion=reported_centered_marginal_plateau_intersection_audit")


if __name__ == "__main__":
    main()
