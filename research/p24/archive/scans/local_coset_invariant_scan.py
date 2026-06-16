#!/usr/bin/env python3
"""Search toy CM cycles for bounded-degree local coset invariants.

The support/projector barrier leaves a loophole: a p-specific finite-field
identity might not look like a sparse group-algebra operator.  At toy scale we
can search for the easiest version of such an identity.

For the D=-5000, h=30 generator cycle, fix a quotient size m.  A local formula
F(j_i, j_{i+1}, ..., j_{i+w-1}) would be useful if it is constant on cosets
i mod m, without aggregating the whole subgroup <g^m>.  We search for
nonconstant polynomials of bounded total degree satisfying

    F(window_i) = F(window_{i+m})

over the splitting field F_q.
"""

from __future__ import annotations

import argparse
import itertools

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import D, ELL, H, Q, isogeny_neighbors, pari_linear_roots, walk_cycle


def monomial_exponents(width: int, degree: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for exps in itertools.product(range(degree + 1), repeat=width):
        if sum(exps) <= degree:
            out.append(exps)
    return out


def eval_monomial(window: list[int], exps: tuple[int, ...], q: int) -> int:
    value = 1
    for x, e in zip(window, exps):
        value = value * pow(x, e, q) % q
    return value


def rank_mod_q(rows: list[list[int]], q: int) -> int:
    if not rows:
        return 0
    matrix = sp.Matrix([[x % q for x in row] for row in rows])
    return int(sp.polys.matrices.DomainMatrix.from_Matrix(matrix, sp.GF(q)).rank())


def nullity_for_constraints(cycle: list[int], quotient: int, width: int, degree: int, q: int) -> tuple[int, int, int, int]:
    exps = monomial_exponents(width, degree)
    windows = [
        [cycle[(i + j) % len(cycle)] for j in range(width)]
        for i in range(len(cycle))
    ]
    rows: list[list[int]] = []
    for i in range(len(cycle)):
        j = (i + quotient) % len(cycle)
        if i < j or j < quotient:
            rows.append(
                [
                    (eval_monomial(windows[i], exp, q) - eval_monomial(windows[j], exp, q)) % q
                    for exp in exps
                ]
            )
    rank_constraints = rank_mod_q(rows, q)
    invariant_dim = len(exps) - rank_constraints

    # Evaluate candidate monomial span on quotient representatives.  If the
    # invariant space dimension is only 1, it is just constants.  This rank is
    # an upper bound on how many quotient labels local polynomials could carry.
    quotient_rows: list[list[int]] = []
    for i in range(quotient):
        quotient_rows.append([eval_monomial(windows[i], exp, q) for exp in exps])
    quotient_eval_rank = rank_mod_q(quotient_rows, q)
    return len(exps), rank_constraints, invariant_dim, quotient_eval_rank


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-width", type=int, default=4)
    ap.add_argument("--max-degree", type=int, default=4)
    args = ap.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    print("local coset invariant scan")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"max_width={args.max_width}")
    print(f"max_degree={args.max_degree}")
    print("columns: quotient width degree monomials constraint_rank invariant_dim quotient_eval_rank nonconstant_exists")
    for quotient in (2, 3, 5, 6, 10, 15):
        for width in range(1, args.max_width + 1):
            for degree in range(1, args.max_degree + 1):
                monomials, rank_constraints, invariant_dim, quotient_eval_rank = nullity_for_constraints(
                    cycle, quotient, width, degree, Q
                )
                print(
                    f"m={quotient:2d} w={width} d={degree} "
                    f"mon={monomials:3d} rank={rank_constraints:3d} "
                    f"inv_dim={invariant_dim:3d} qrank={quotient_eval_rank:3d} "
                    f"nonconstant={int(invariant_dim > 1)}"
                )
        print()
    print("interpretation")
    print("  nonconstant_local_coset_invariant_would_be_a_seedless_formula_lead=1")
    print("  absence_at_small_width_degree_supports_projector_barrier=1")
    print("  large_monomial_spaces_eventually_interpolate_and_are_not_meaningful=1")
    print("conclusion=reported_local_coset_invariant_scan")


if __name__ == "__main__":
    main()
