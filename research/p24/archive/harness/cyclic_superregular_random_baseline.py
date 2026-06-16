#!/usr/bin/env python3
"""Random baseline for cyclic consecutive-minor superregularity.

The coefficient-minor route asks whether the axis subspace `V` in
`F_q[X]/(f)` has nonzero leading minor after multiplication by `X^-beta` for
all relevant beta.  This is a cyclic consecutive-Pluecker condition.

For a random `r`-dimensional subspace of a `d`-dimensional packet over `F_q`,
each fixed projected `r x r` minor vanishes with probability about `1/q`.
The union over `n` beta shifts is therefore expected to have failure
probability about `n/q` when `n << q`.

This script compares the actual CM axis subspace with random full-rank
subspaces in the same packet field.  If random subspaces almost always pass,
then small-data success of the leading-minor route is generic evidence, not a
CM-specific theorem.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import coprime_components
from l1_axis_injectivity_scan import (
    axis_basis_images,
    coeff_vector,
    discriminants,
    rank_mod_q,
)
from hermitian_trace_gram_scan import poly_pow_mod, vector_to_poly

X = sp.symbols("X")


@dataclass(frozen=True)
class Case:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor: sp.Poly
    vectors: list[list[int]]


def det_mod(matrix: list[list[int]], q: int) -> int:
    return int(sp.Matrix(matrix).det()) % q


def multiply_vector_by_monomial(
    vector: list[int],
    exponent: int,
    factor: sp.Poly,
    q: int,
) -> list[int]:
    poly = vector_to_poly(vector, q)
    monomial = poly_pow_mod(sp.Poly(X, X, modulus=q), exponent, factor)
    shifted = (poly * monomial).rem(factor)
    return coeff_vector(shifted, factor.degree(), q)


def monomial_transforms(
    factor: sp.Poly,
    n: int,
    q: int,
) -> list[list[list[int]]]:
    d = factor.degree()
    transforms: list[list[list[int]]] = []
    for beta in range(n):
        exponent = (-beta) % n
        monomial = poly_pow_mod(sp.Poly(X, X, modulus=q), exponent, factor)
        images: list[list[int]] = []
        for j in range(d):
            basis_poly = sp.Poly(X**j, X, modulus=q)
            image = (basis_poly * monomial).rem(factor)
            images.append(coeff_vector(image, d, q))
        transforms.append(images)
    return transforms


def apply_transform(vector: list[int], transform: list[list[int]], q: int) -> list[int]:
    d = len(vector)
    out = [0] * d
    for coeff, image in zip(vector, transform):
        c = coeff % q
        if not c:
            continue
        out = [(left + c * right) % q for left, right in zip(out, image)]
    return out


def beta_leading_dets(
    vectors: list[list[int]],
    factor: sp.Poly,
    n: int,
    q: int,
    transforms: list[list[list[int]]] | None = None,
) -> list[int]:
    r = len(vectors)
    maps = transforms if transforms is not None else monomial_transforms(factor, n, q)
    out: list[int] = []
    for transform in maps:
        shifted = [
            apply_transform(vector, transform, q)
            for vector in vectors
        ]
        leading = [[row[col] % q for col in range(r)] for row in shifted]
        out.append(det_mod(leading, q))
    return out


def random_full_rank_vectors(
    rng: random.Random,
    r: int,
    d: int,
    q: int,
) -> list[list[int]]:
    while True:
        vectors = [[rng.randrange(q) for _ in range(d)] for _ in range(r)]
        if rank_mod_q(vectors, q) == r:
            return vectors


def first_case(args: argparse.Namespace) -> Case | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if sp.gcd(m, h // m) == 1
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
        ]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
            ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari, hilbert, h, args.q_start, args.q_stop, args.max_splitting_primes
        )
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    residues = [
                        fiber.rem(factor)
                        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
                    ]
                    images = axis_basis_images(residues, coprime_components(m), factor)
                    vectors = [
                        coeff_vector(poly, factor.degree(), q) for _, poly in images
                    ]
                    return Case(D, q, ell, h, m, n, factor, vectors)
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=12)
    parser.add_argument("--max-factor-degree", type=int, default=20)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    case = first_case(args)
    if case is None:
        raise SystemExit("no eligible case found")

    q = case.q
    d = case.factor.degree()
    r = len(case.vectors)
    transforms = monomial_transforms(case.factor, case.n, q)
    cm_dets = beta_leading_dets(case.vectors, case.factor, case.n, q, transforms)
    rng = random.Random(args.seed)

    random_failures = 0
    random_zero_total = 0
    random_distinct_values: list[int] = []
    for _ in range(args.random_trials):
        vectors = random_full_rank_vectors(rng, r, d, q)
        dets = beta_leading_dets(vectors, case.factor, case.n, q, transforms)
        zeros = sum(1 for value in dets if value == 0)
        random_zero_total += zeros
        if zeros:
            random_failures += 1
        random_distinct_values.append(len(set(dets)))

    print("cyclic consecutive-minor random baseline")
    print(f"D={case.D}")
    print(f"q={case.q}")
    print(f"ell={case.ell}")
    print(f"h={case.h}")
    print(f"m={case.m}")
    print(f"n={case.n}")
    print(f"factor_degree={d}")
    print(f"axis_dim={r}")
    print(f"random_trials={args.random_trials}")
    print(f"seed={args.seed}")
    print()
    print("cm_axis")
    print(f"  beta_tests={len(cm_dets)}")
    print(f"  beta_zero_count={sum(1 for value in cm_dets if value == 0)}")
    print(f"  beta_distinct_values={len(set(cm_dets))}")
    print()
    print("random_baseline")
    print(f"  subspaces_with_any_beta_zero={random_failures}")
    print(f"  beta_zero_total={random_zero_total}")
    print(f"  empirical_failure_rate={random_failures / args.random_trials:.6f}")
    print(f"  empirical_zero_rate_per_beta={random_zero_total / (args.random_trials * case.n):.6f}")
    print(f"  heuristic_any_failure_n_over_q={case.n / q:.6f}")
    if random_distinct_values:
        print(f"  random_distinct_values_min={min(random_distinct_values)}")
        print(f"  random_distinct_values_max={max(random_distinct_values)}")
    print()
    print("interpretation")
    print("  low_random_failure_rate_means_small_clean_CM_data_is_not_proof_like=1")
    print("  cyclic_superregularity_still_needs_selected_CM_arithmetic_input=1")
    print("conclusion=reported_cyclic_superregular_random_baseline")


if __name__ == "__main__":
    main()
