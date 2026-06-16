#!/usr/bin/env python3
"""Low-degree local-feature audit for quotient CM periods.

The first p24 strict trace has an attractive order-19 quotient:

    index(<ell>) = ell = 19.

`norm_equals_index_local_phi_toy.py` already shows that a linear formula in a
few local Phi_ell features does not recover the quotient period on small
analogues.  This script pushes the same falsification test to bounded
polynomial degree.  It searches small CM discriminants with

    index(<ell>) = ell

and asks whether the horizontal cycle period attached to a root j can be
expressed as a low-degree polynomial in local features of the ell-isogeny
surface.

This is not a proof of nonexistence.  It is a cheap theorem laboratory:
bounded local formulas should fail quickly before we invest proof effort in
them.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from norm_equals_index_local_phi_toy import (
    Candidate,
    components,
    find_splitting_prime,
    form_order,
    isogeny_neighbors,
    phi_y_coeffs_at_x,
)


@dataclass(frozen=True)
class LocalRow:
    root: int
    period: int
    features: tuple[int, ...]


def find_candidates_with_min_h(
    max_abs_d: int,
    min_h: int,
    max_h: int,
    min_ell: int,
    max_ell: int,
    max_cases: int,
) -> list[Candidate]:
    pari = Pari()
    out: list[Candidate] = []
    for D in range(-3, -max_abs_d - 1, -1):
        if D % 4 not in (0, 1):
            continue
        try:
            h = int(pari.poldegree(pari.polclass(D)))
        except Exception:
            continue
        if h < min_h or h > max_h:
            continue
        for ell in sp.primerange(max(2, min_ell), max_ell + 1):
            if abs(D) % ell == 0 or sp.kronecker_symbol(D, int(ell)) != 1:
                continue
            order = form_order(pari, D, h, int(ell))
            index = h // order
            if index == ell:
                out.append(Candidate(D, h, int(ell), order, index))
                if len(out) >= max_cases:
                    return out
    return out


def local_rows(candidate: Candidate) -> tuple[int, list[LocalRow]] | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    split = find_splitting_prime(pari, candidate.D, candidate.h)
    if split is None:
        return None
    q, roots = split
    graph = isogeny_neighbors(roots, candidate.ell, q)
    comps = components(graph)
    if sorted({len(c) for c in comps}) != [candidate.order] or len(comps) != candidate.index:
        return None

    root_to_period: dict[int, int] = {}
    for comp in comps:
        period = sum(comp) % q
        for root in comp:
            root_to_period[root] = period

    rows: list[LocalRow] = []
    for root in roots:
        coeffs = phi_y_coeffs_at_x(pari, candidate.ell, q, root)
        total_neighbor_sum = (-coeffs[-2]) % q
        horizontal = graph[root]
        horizontal_sum = sum(horizontal) % q
        descending_sum = (total_neighbor_sum - horizontal_sum) % q
        horizontal_product = 1
        for value in horizontal:
            horizontal_product = horizontal_product * value % q

        # Fixed-width local summary.  It deliberately includes the root j and
        # the horizontal pair, so failure is stronger than failure from raw
        # Phi_ell coefficients alone.
        features = (
            1,
            root % q,
            total_neighbor_sum,
            horizontal_sum,
            descending_sum,
            horizontal_product,
        )
        rows.append(LocalRow(root=root, period=root_to_period[root], features=features))
    return q, rows


def exponent_vectors(feature_count: int, degree: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for exps in itertools.product(range(degree + 1), repeat=feature_count):
        if sum(exps) <= degree:
            out.append(exps)
    return out


def monomial_values(row: LocalRow, exps: tuple[int, ...], q: int) -> int:
    value = 1
    for feature, exp in zip(row.features, exps):
        if exp:
            value = value * pow(feature, exp, q) % q
    return value


def span_contains_period(rows: list[LocalRow], q: int, degree: int) -> dict[str, int]:
    exps = exponent_vectors(len(rows[0].features), degree)
    feature_matrix = [
        [monomial_values(row, exp, q) for exp in exps]
        for row in rows
    ]
    augmented = [row_values + [row.period % q] for row_values, row in zip(feature_matrix, rows)]
    feature_rank = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(feature_matrix), sp.GF(q)).rank()
    augmented_rank = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(augmented), sp.GF(q)).rank()
    return {
        "degree": degree,
        "monomials": len(exps),
        "feature_rank": int(feature_rank),
        "augmented_rank": int(augmented_rank),
        "full_row_rank": int(feature_rank == len(rows)),
        "formula_exists": int(feature_rank == augmented_rank),
        "non_interpolating_formula_exists": int(feature_rank == augmented_rank and feature_rank < len(rows)),
    }


def audit_candidate(candidate: Candidate, max_degree: int) -> dict[str, object] | None:
    found = local_rows(candidate)
    if found is None:
        return None
    q, rows = found
    results = [span_contains_period(rows, q, degree) for degree in range(1, max_degree + 1)]
    return {
        "D": candidate.D,
        "h": candidate.h,
        "ell": candidate.ell,
        "order": candidate.order,
        "index": candidate.index,
        "q": q,
        "rows": len(rows),
        "distinct_periods": len({row.period for row in rows}),
        "degree_results": results,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-d", type=int, default=80000)
    ap.add_argument("--min-h", type=int, default=60)
    ap.add_argument("--max-h", type=int, default=180)
    ap.add_argument("--min-ell", type=int, default=3)
    ap.add_argument("--max-ell", type=int, default=31)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--max-degree", type=int, default=3)
    args = ap.parse_args()

    candidates = find_candidates_with_min_h(
        args.max_abs_d,
        args.min_h,
        args.max_h,
        args.min_ell,
        args.max_ell,
        args.max_cases,
    )

    print("quotient period low-degree local-feature audit")
    print(f"max_abs_d={args.max_abs_d}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"min_ell={args.min_ell}")
    print(f"max_ell={args.max_ell}")
    print(f"max_cases={args.max_cases}")
    print(f"max_degree={args.max_degree}")
    print(f"candidate_count={len(candidates)}")
    for candidate in candidates:
        print(
            f"candidate D={candidate.D} h={candidate.h} ell={candidate.ell} "
            f"order={candidate.order} index={candidate.index}"
        )
    print()

    audited = 0
    any_formula = False
    any_non_interpolating_formula = False
    for candidate in candidates:
        result = audit_candidate(candidate, args.max_degree)
        if result is None:
            continue
        audited += 1
        print("audit")
        for key, value in result.items():
            if key != "degree_results":
                print(f"  {key}={value}")
        for degree_result in result["degree_results"]:
            any_formula = any_formula or bool(degree_result["formula_exists"])
            any_non_interpolating_formula = (
                any_non_interpolating_formula
                or bool(degree_result["non_interpolating_formula_exists"])
            )
            print(
                "  degree={degree} monomials={monomials} "
                "feature_rank={feature_rank} augmented_rank={augmented_rank} "
                "full_row_rank={full_row_rank} formula_exists={formula_exists} "
                "non_interpolating_formula_exists={non_interpolating_formula_exists}".format(**degree_result)
            )
        print()

    print("interpretation")
    print(f"  audited_cases={audited}")
    print(f"  any_low_degree_formula_found={int(any_formula)}")
    print(f"  any_non_interpolating_formula_found={int(any_non_interpolating_formula)}")
    print("  features_include_j_and_horizontal_pair=1")
    print("  full_row_rank_formula_should_be_read_as_interpolation=1")
    print("  negative_result_is_only_for_bounded_local_feature_span=1")
    print("conclusion=bounded_local_phi_feature_formula_not_supported")


if __name__ == "__main__":
    main()
