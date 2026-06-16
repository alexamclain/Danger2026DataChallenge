#!/usr/bin/env python3
"""Mine small CM Plucker products for norm-identity candidates.

For a rectangular marginal matrix, each maximal minor is a Plucker coordinate
of the relevant exterior vector.  The p24 proof route asks for a selected
Plucker p-unit, or better an origin-stable product over beta shifts that can
be recognized as a class-field norm/resultant.

This script is deliberately small-scale.  It enumerates or samples maximal
minors on one toy tensor-factor row, computes their beta products, pushes those
products down to the base field, and compares "simple" norm behavior with
random tensor-factor controls of the same shape.
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections import Counter
from dataclasses import dataclass
from math import comb

import sympy as sp

from k_character_tensor_rank_scan import ExtensionField
from tensor_factor_dual_basis_window_audit import top_window_coords
from tensor_factor_marginal_origin_action_audit import determinant, product
from tensor_factor_marginal_random_support_audit import (
    PreparedCase,
    combined_rows,
    prepare_case,
    random_b_element,
)
from tensor_factor_moore_audit import b_mul
from tensor_factor_subfield_trace_audit import divisors


Matrix = list[list[tuple[int, ...]]]


@dataclass(frozen=True)
class MinorSpec:
    mode: str
    indices: tuple[int, ...]

    @property
    def label(self) -> str:
        return f"{self.mode}:{','.join(str(i) for i in self.indices)}"


@dataclass(frozen=True)
class MinorSummary:
    spec: MinorSpec
    zero_count: int
    distinct_count: int
    beta_product: tuple[int, ...]
    product_subfield_degree: int
    norm_to_base: tuple[int, ...]
    norm_int: int | None
    norm_height: int | None
    norm_factor_count: int | None
    alpha_product_distinct: int | None
    alpha_product_zero_count: int | None


def matrix_for_shift(
    values,
    prepared: PreparedCase,
    alpha: int,
    beta: int,
) -> Matrix:
    multiplier = prepared.theta_inv_powers[beta]
    sequence = []
    for r in range(prepared.m):
        shifted_value = b_mul(
            multiplier,
            values[(r + alpha) % prepared.m],
            prepared.selected_factor,
            prepared.field,
        )
        sequence.append(
            top_window_coords(
                shifted_value,
                prepared.windows,
                prepared.subdegree,
                prepared.relative_degree,
                prepared.gprime_theta,
                prepared.basis_columns,
                prepared.selected_factor,
                prepared.field,
            )
        )
    return combined_rows(
        sequence,
        prepared.components,
        prepared.include_constant,
        prepared.field,
    )


def minor_value(matrix: Matrix, spec: MinorSpec, field: ExtensionField):
    if spec.mode == "cols":
        square = [[row[col] for col in spec.indices] for row in matrix]
    elif spec.mode == "rows":
        square = [matrix[row][:] for row in spec.indices]
    else:
        raise ValueError(f"unknown minor mode {spec.mode}")
    return determinant(square, field)


def sampled_combinations(
    n: int,
    k: int,
    max_count: int,
    rng: random.Random,
) -> list[tuple[int, ...]]:
    total = comb(n, k)
    if total <= max_count:
        return list(itertools.combinations(range(n), k))
    out: set[tuple[int, ...]] = set()
    while len(out) < max_count:
        out.add(tuple(sorted(rng.sample(range(n), k))))
    return sorted(out)


def minor_specs(rows: int, cols: int, max_minors: int, seed: int) -> list[MinorSpec]:
    rng = random.Random(seed + 500_123 + 13 * rows + 17 * cols)
    if rows <= cols:
        return [
            MinorSpec("cols", combo)
            for combo in sampled_combinations(cols, rows, max_minors, rng)
        ]
    return [
        MinorSpec("rows", combo)
        for combo in sampled_combinations(rows, cols, max_minors, rng)
    ]


def subfield_degree(value: tuple[int, ...], field: ExtensionField) -> int:
    if value == field.zero:
        return 0
    for degree in divisors(field.degree):
        if field.pow(value, field.q**degree) == value:
            return degree
    return field.degree


def norm_to_base(value: tuple[int, ...], field: ExtensionField) -> tuple[int, ...]:
    if value == field.zero:
        return field.zero
    exponent = (field.q**field.degree - 1) // (field.q - 1)
    return field.pow(value, exponent)


def base_int(value: tuple[int, ...], field: ExtensionField) -> int | None:
    if all(coord == 0 for coord in value[1:]):
        return value[0] % field.q
    return None


def norm_height(value: int | None, q: int) -> int | None:
    if value is None:
        return None
    return min(value, (-value) % q)


def factor_count(value: int | None) -> int | None:
    if value is None or value == 0:
        return None
    return sum(sp.factorint(value).values())


def summarize_minor(
    prepared: PreparedCase,
    spec: MinorSpec,
    shifted_matrices: dict[int, list[Matrix]],
    include_alpha_products: bool,
) -> MinorSummary:
    field = prepared.field
    beta_values = [
        minor_value(matrix, spec, field)
        for matrix in shifted_matrices[0]
    ]
    beta_product = product(beta_values, field)
    norm = norm_to_base(beta_product, field)
    norm_int = base_int(norm, field)

    alpha_product_distinct: int | None = None
    alpha_product_zero_count: int | None = None
    if include_alpha_products:
        alpha_products = []
        for alpha in range(prepared.m):
            sequence = [
                minor_value(matrix, spec, field)
                for matrix in shifted_matrices[alpha]
            ]
            alpha_products.append(product(sequence, field))
        alpha_product_distinct = len(set(alpha_products))
        alpha_product_zero_count = sum(1 for value in alpha_products if value == field.zero)

    return MinorSummary(
        spec=spec,
        zero_count=sum(1 for value in beta_values if value == field.zero),
        distinct_count=len(set(beta_values)),
        beta_product=beta_product,
        product_subfield_degree=subfield_degree(beta_product, field),
        norm_to_base=norm,
        norm_int=norm_int,
        norm_height=norm_height(norm_int, field.q),
        norm_factor_count=factor_count(norm_height(norm_int, field.q)),
        alpha_product_distinct=alpha_product_distinct,
        alpha_product_zero_count=alpha_product_zero_count,
    )


def precompute_shifted_matrices(
    values,
    prepared: PreparedCase,
    include_alpha_products: bool,
) -> dict[int, list[Matrix]]:
    alphas = range(prepared.m) if include_alpha_products else (0,)
    return {
        alpha: [
            matrix_for_shift(values, prepared, alpha, beta)
            for beta in range(prepared.n)
        ]
        for alpha in alphas
    }


def summarize_all(
    values,
    prepared: PreparedCase,
    specs: list[MinorSpec],
    include_alpha_products: bool,
) -> list[MinorSummary]:
    shifted_matrices = precompute_shifted_matrices(
        values,
        prepared,
        include_alpha_products,
    )
    return [
        summarize_minor(prepared, spec, shifted_matrices, include_alpha_products)
        for spec in specs
    ]


def sort_key(summary: MinorSummary):
    zero = summary.zero_count
    degree = summary.product_subfield_degree if summary.product_subfield_degree else 99
    height = summary.norm_height if summary.norm_height is not None else 10**18
    factors = summary.norm_factor_count if summary.norm_factor_count is not None else 10**9
    return (zero, degree, height, factors, summary.distinct_count, summary.spec.label)


def random_control_summaries(
    args: argparse.Namespace,
    prepared: PreparedCase,
    specs: list[MinorSpec],
) -> list[dict[str, object]]:
    rng = random.Random(args.seed + 880_301)
    out: list[dict[str, object]] = []
    for _ in range(args.random_trials):
        values = [random_b_element(rng, prepared) for _ in range(prepared.m)]
        summaries = summarize_all(values, prepared, specs, include_alpha_products=False)
        nonzero = [summary for summary in summaries if summary.zero_count == 0]
        best = min(nonzero, key=sort_key) if nonzero else None
        out.append(
            {
                "nonzero_minors": len(nonzero),
                "zero_free_best_height": best.norm_height if best else None,
                "zero_free_best_subfield_degree": best.product_subfield_degree if best else None,
                "zero_free_best_factor_count": best.norm_factor_count if best else None,
                "zero_free_best_distinct": best.distinct_count if best else None,
            }
        )
    return out


def hist(values) -> dict[object, int]:
    return dict(sorted(Counter(values).items(), key=lambda item: (str(item[0]), item[1])))


def print_minor(summary: MinorSummary) -> None:
    print(
        f"  {summary.spec.label:24s} "
        f"zeros={summary.zero_count:2d} distinct={summary.distinct_count:3d} "
        f"prod_deg={summary.product_subfield_degree:2d} "
        f"norm={summary.norm_int} height={summary.norm_height} "
        f"height_factor_count={summary.norm_factor_count} "
        f"alpha_products_distinct={summary.alpha_product_distinct} "
        f"alpha_product_zeros={summary.alpha_product_zero_count} "
        f"product={summary.beta_product}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--max-minors", type=int, default=200)
    parser.add_argument("--random-trials", type=int, default=40)
    parser.add_argument("--include-alpha-products", action="store_true")
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=3)
    parser.add_argument("--windows", type=int, default=2)
    parser.add_argument("--target", default="full")
    parser.add_argument("--without-constant", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    prepared = prepare_case(args)
    base_matrix = matrix_for_shift(prepared.cm_values, prepared, 0, 0)
    rows = len(base_matrix)
    cols = len(base_matrix[0]) if rows else 0
    specs = minor_specs(rows, cols, args.max_minors, args.seed)
    cm_summaries = summarize_all(
        prepared.cm_values,
        prepared,
        specs,
        include_alpha_products=args.include_alpha_products,
    )
    cm_ranked = sorted(cm_summaries, key=sort_key)
    controls = random_control_summaries(args, prepared, specs)

    best_heights = [
        row["zero_free_best_height"]
        for row in controls
        if row["zero_free_best_height"] is not None
    ]
    best_degrees = [
        row["zero_free_best_subfield_degree"]
        for row in controls
        if row["zero_free_best_subfield_degree"] is not None
    ]
    best_factors = [
        row["zero_free_best_factor_count"]
        for row in controls
        if row["zero_free_best_factor_count"] is not None
    ]
    nonzero_counts = [row["nonzero_minors"] for row in controls]

    print("tensor factor Plucker norm miner")
    print(f"D={prepared.D}")
    print(f"q={prepared.q}")
    print(f"ell={prepared.ell}")
    print(f"h={prepared.h}")
    print(f"m={prepared.m}")
    print(f"n={prepared.n}")
    print(f"factor_degree={prepared.factor_degree}")
    print(f"extension_degree={prepared.extension_degree}")
    print(f"tensor_factor_degree={prepared.tensor_factor_degree}")
    print(f"subdegree={prepared.subdegree}")
    print(f"windows={prepared.windows}")
    print(f"components={prepared.components}")
    print(f"include_constant={int(prepared.include_constant)}")
    print(f"matrix_shape={rows}x{cols}")
    print(f"minor_mode={specs[0].mode if specs else 'none'}")
    print(f"minors_tested={len(specs)}")
    print(f"random_trials={args.random_trials}")
    print()

    print("cm_best_minors")
    for summary in cm_ranked[: args.top]:
        print_minor(summary)
    print()

    print("cm_aggregate")
    print(f"  zero_free_minors={sum(1 for s in cm_summaries if s.zero_count == 0)}")
    print(f"  product_subfield_degree_hist={hist(s.product_subfield_degree for s in cm_summaries)}")
    print(f"  beta_zero_count_hist={hist(s.zero_count for s in cm_summaries)}")
    print()

    print("random_controls")
    print(f"  nonzero_minor_count_min={min(nonzero_counts) if nonzero_counts else 'NA'}")
    print(f"  nonzero_minor_count_max={max(nonzero_counts) if nonzero_counts else 'NA'}")
    print(f"  best_height_min={min(best_heights) if best_heights else 'NA'}")
    print(f"  best_height_max={max(best_heights) if best_heights else 'NA'}")
    print(f"  best_height_hist={hist(best_heights)}")
    print(f"  best_subfield_degree_hist={hist(best_degrees)}")
    print(f"  best_factor_count_hist={hist(best_factors)}")
    print()

    cm_best = cm_ranked[0] if cm_ranked else None
    print("interpretation")
    if cm_best is not None:
        print(f"  cm_best_zero_count={cm_best.zero_count}")
        print(f"  cm_best_norm_height={cm_best.norm_height}")
        print(f"  cm_best_product_subfield_degree={cm_best.product_subfield_degree}")
    print("  unusually_small_or_low_degree_cm_products_are_norm_identity_candidates=1")
    print("  matching_random_controls_means_no_visible_cm_specific_norm_structure=1")
    print("conclusion=reported_tensor_factor_plucker_norm_miner")


if __name__ == "__main__":
    main()
