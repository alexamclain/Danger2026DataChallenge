#!/usr/bin/env python3
"""Short oriented-path boundary for the centered full-origin product.

The one-edge gate rules out

    Delta_origin(i) = R(j_i, j_{i+1})

for bounded low-bidegree `R` on the pinned actual-CM row.  The next local
correspondence shape is a short oriented path.  This probe asks whether the
same determinant is a low total-degree polynomial/rational function of

    (j_i, j_{i+1}, ..., j_{i+path_vertices-1}).

The degree caps are kept below the generic interpolation threshold for the
140 samples, and random controls preserve the observed repeated-alpha output
shape.
"""

from __future__ import annotations

import argparse
from itertools import product
import random

from abstract_embedded_pairing_non_genus_toy import null_vector_mod_q
from embedded_selector_identity_toy import nullspace_mod
from packet_scalar_edge_shape_scan import rank_mod

from centered_marginal_full_origin_phase_sensitivity_gate import pinned_args
from centered_marginal_origin_product_audit import scan


SEED = 20260606
RANDOM_CONTROLS = 8
RANDOM_COMBOS = 12


def total_degree_exponents(variables: int, degree: int) -> list[tuple[int, ...]]:
    return [
        exponents
        for exponents in product(range(degree + 1), repeat=variables)
        if sum(exponents) <= degree
    ]


def monomial_row(coords: tuple[int, ...], exponents: list[tuple[int, ...]], q: int) -> list[int]:
    powers: list[list[int]] = []
    for coord in coords:
        values = [1]
        for _ in range(max(sum(exp) for exp in exponents) if exponents else 0):
            values.append(values[-1] * coord % q)
        powers.append(values)
    row: list[int] = []
    for exp in exponents:
        value = 1
        for index, power in enumerate(exp):
            value = value * powers[index][power] % q
        row.append(value)
    return row


def has_polynomial_total_degree(
    coords: list[tuple[int, ...]],
    ys: list[int],
    q: int,
    degree: int,
) -> bool:
    exponents = total_degree_exponents(len(coords[0]), degree)
    matrix = [monomial_row(point, exponents, q) for point in coords]
    augmented = [row + [y % q] for row, y in zip(matrix, ys)]
    return rank_mod(matrix, q) == rank_mod(augmented, q)


def first_polynomial_total_degree(
    coords: list[tuple[int, ...]],
    ys: list[int],
    q: int,
    max_degree: int,
) -> int | None:
    for degree in range(max_degree + 1):
        if has_polynomial_total_degree(coords, ys, q, degree):
            return degree
    return None


def eval_poly(coeffs: list[int], point: tuple[int, ...], exponents: list[tuple[int, ...]], q: int) -> int:
    row = monomial_row(point, exponents, q)
    return sum(coeff * value for coeff, value in zip(coeffs, row)) % q


def rational_candidate_valid(
    candidate: list[int],
    coords: list[tuple[int, ...]],
    ys: list[int],
    q: int,
    degree: int,
) -> bool:
    exponents = total_degree_exponents(len(coords[0]), degree)
    variables = len(exponents)
    numerator = [value % q for value in candidate[:variables]]
    denominator = [value % q for value in candidate[variables:]]
    if all(value == 0 for value in denominator):
        return False
    for point, y in zip(coords, ys):
        den_value = eval_poly(denominator, point, exponents, q)
        if den_value == 0:
            return False
        if eval_poly(numerator, point, exponents, q) != y * den_value % q:
            return False
    return True


def has_rational_total_degree(
    coords: list[tuple[int, ...]],
    ys: list[int],
    q: int,
    degree: int,
    rng: random.Random,
    random_combos: int,
) -> bool:
    exponents = total_degree_exponents(len(coords[0]), degree)
    rows: list[list[int]] = []
    for point, y in zip(coords, ys):
        row = monomial_row(point, exponents, q)
        rows.append(row + [(-y * value) % q for value in row])

    vector = null_vector_mod_q(rows, q)
    if vector is not None and rational_candidate_valid(vector, coords, ys, q, degree):
        return True

    basis, _ = nullspace_mod(rows, q)
    if not basis:
        return False
    candidates = basis[:]
    for _ in range(random_combos):
        coeffs = [rng.randrange(q) for _ in basis]
        if not any(coeffs):
            coeffs[0] = 1
        candidate = [0] * len(basis[0])
        for coeff, base in zip(coeffs, basis):
            if coeff:
                candidate = [(value + coeff * b) % q for value, b in zip(candidate, base)]
        candidates.append(candidate)
    return any(
        rational_candidate_valid(candidate, coords, ys, q, degree)
        for candidate in candidates
    )


def first_rational_total_degree(
    coords: list[tuple[int, ...]],
    ys: list[int],
    q: int,
    max_degree: int,
    rng: random.Random,
    random_combos: int,
) -> int | None:
    for degree in range(max_degree + 1):
        if has_rational_total_degree(coords, ys, q, degree, rng, random_combos):
            return degree
    return None


def path_samples(row, path_vertices: int) -> tuple[list[tuple[int, ...]], list[int]]:
    coords: list[tuple[int, ...]] = []
    ys: list[int] = []
    cycle = list(row.cycle)
    for alpha, value in enumerate(row.alpha_values):
        for beta in range(row.n):
            shift = (row.n * alpha + row.m * beta) % row.h
            coords.append(
                tuple(cycle[(shift + offset) % row.h] % row.q for offset in range(path_vertices))
            )
            ys.append(value % row.q)
    return coords, ys


def random_repeated_alpha_values(row, rng: random.Random) -> list[int]:
    ys: list[int] = []
    for _alpha in range(row.m):
        value = rng.randrange(row.q)
        ys.extend([value] * row.n)
    return ys


def run_case(
    row,
    path_vertices: int,
    max_poly_degree: int,
    max_rat_degree: int,
    rng: random.Random,
    random_controls: int,
    random_combos: int,
) -> dict[str, object]:
    coords, ys = path_samples(row, path_vertices)
    poly = first_polynomial_total_degree(coords, ys, row.q, max_poly_degree)
    rat = first_rational_total_degree(
        coords,
        ys,
        row.q,
        max_rat_degree,
        rng,
        random_combos,
    )
    random_poly_hits = 0
    random_rat_hits = 0
    for _trial in range(random_controls):
        random_ys = random_repeated_alpha_values(row, rng)
        random_poly_hits += int(
            first_polynomial_total_degree(coords, random_ys, row.q, max_poly_degree)
            is not None
        )
        random_rat_hits += int(
            first_rational_total_degree(
                coords,
                random_ys,
                row.q,
                max_rat_degree,
                rng,
                random_combos,
            )
            is not None
        )
    return {
        "path_vertices": path_vertices,
        "sample_count": len(coords),
        "distinct_path_points": len(set(coords)),
        "determinant_distinct_values": len(set(ys)),
        "poly_monomials_at_cap": len(total_degree_exponents(path_vertices, max_poly_degree)),
        "rat_monomials_at_cap": len(total_degree_exponents(path_vertices, max_rat_degree)),
        "max_poly_total_degree": max_poly_degree,
        "max_rat_total_degree": max_rat_degree,
        "first_polynomial_total_degree": poly,
        "first_rational_total_degree": rat,
        "random_repeated_alpha_polynomial_hits": random_poly_hits,
        "random_repeated_alpha_rational_hits": random_rat_hits,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-controls", type=int, default=RANDOM_CONTROLS)
    parser.add_argument("--random-combos", type=int, default=RANDOM_COMBOS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    row = scan(pinned_args())
    if row is None:
        raise SystemExit("pinned row not found")
    rng = random.Random(args.seed)
    cases = [
        # These caps stay below generic interpolation for 140 samples:
        # C(3+7, 7)=120 and 2*C(3+5, 5)=112.
        run_case(row, 3, 7, 5, rng, args.random_controls, args.random_combos),
        # C(4+5, 5)=126 and 2*C(4+3, 3)=70.
        run_case(row, 4, 5, 3, rng, args.random_controls, args.random_combos),
    ]

    print("Centered marginal full-origin short-path shape boundary")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    for case in cases:
        print(f"path_vertices={case['path_vertices']}")
        print(f"  sample_count={case['sample_count']}")
        print(f"  distinct_path_points={case['distinct_path_points']}")
        print(f"  determinant_distinct_values={case['determinant_distinct_values']}")
        print(f"  max_poly_total_degree={case['max_poly_total_degree']}")
        print(f"  poly_monomials_at_cap={case['poly_monomials_at_cap']}")
        print(f"  first_polynomial_total_degree={case['first_polynomial_total_degree']}")
        print(f"  max_rat_total_degree={case['max_rat_total_degree']}")
        print(f"  rat_monomials_at_cap={case['rat_monomials_at_cap']}")
        print(f"  first_rational_total_degree={case['first_rational_total_degree']}")
        print(
            "  random_repeated_alpha_polynomial_hits="
            f"{case['random_repeated_alpha_polynomial_hits']}/{args.random_controls}"
        )
        print(
            "  random_repeated_alpha_rational_hits="
            f"{case['random_repeated_alpha_rational_hits']}/{args.random_controls}"
        )
    print("interpretation")
    print("  short_oriented_paths_have_no_subgeneric_low_degree_formula=1")
    print("  local_correspondence_norm_must_use_richer_phase_or_direct_fitting_divisor=1")
    print("conclusion=reported_centered_marginal_full_origin_path_shape_boundary")

    if (row.D, row.q, row.m, row.n, row.left, row.right) != (-13319, 13463, 28, 5, 4, 7):
        raise SystemExit(1)
    for case in cases:
        if case["first_polynomial_total_degree"] is not None:
            raise SystemExit(1)
        if case["first_rational_total_degree"] is not None:
            raise SystemExit(1)
        if case["random_repeated_alpha_polynomial_hits"] != 0:
            raise SystemExit(1)
        if case["random_repeated_alpha_rational_hits"] != 0:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
