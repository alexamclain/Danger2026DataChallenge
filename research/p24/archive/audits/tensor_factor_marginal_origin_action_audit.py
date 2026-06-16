#!/usr/bin/env python3
"""Origin-action audit for marginal exterior determinants.

For an origin shift

    s == n*alpha + m*beta mod h,

the quotient fibers transform as

    J'_r(theta) = theta^(-beta) J_{r+alpha}(theta).

The alpha part is a CRT residue translation and should change the marginal
difference basis by a unimodular matrix.  The beta part multiplies inside the
packet factor before applying `Top_k`; it can change a chosen exterior
coordinate.  This script tests the resulting determinant values on small
tensor-factor rows where the combined marginal target is square.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from axis_minor_origin_action_audit import crt_coordinates
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import coeff_vector, discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from tensor_factor_dual_basis_window_audit import (
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    theta_element,
    top_window_coords,
)
from tensor_factor_top_coefficient_fourier_audit import embedded_residue_vector
from tensor_factor_moore_audit import b_mul, b_one, b_pow
from tensor_factor_subfield_trace_audit import divisors
from tensor_factor_crt_marginal_rank_audit import (
    component_marginals,
    vector_sub,
    vector_sum,
)


@dataclass(frozen=True)
class OriginDet:
    shift: int
    alpha: int
    beta: int
    det: tuple[int, ...]


def determinant(matrix: list[list[tuple[int, ...]]], field: ExtensionField) -> tuple[int, ...]:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("determinant requires a square matrix")
    mat = [row[:] for row in matrix]
    det = field.one
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            return field.zero
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = field.neg(det)
        pivot_value = mat[col][col]
        det = field.mul(det, pivot_value)
        inv = field.inv(pivot_value)
        mat[col] = [field.mul(value, inv) for value in mat[col]]
        for row in range(col + 1, n):
            scale = mat[row][col]
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[col])
            ]
    return det


def product(values: list[tuple[int, ...]], field: ExtensionField) -> tuple[int, ...]:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def combined_rows(sequence, components: tuple[int, ...], include_constant: bool, field: ExtensionField):
    rows = []
    if include_constant:
        rows.append(vector_sum(sequence, field))
    for component in components:
        marginals = component_marginals(sequence, component, field)
        rows.extend(vector_sub(value, marginals[0], field) for value in marginals[1:])
    return rows


def target_components(m: int, target: str) -> tuple[int, ...]:
    components = tuple(coprime_components(m))
    if target == "full":
        return components
    requested = int(target)
    if requested not in components:
        raise ValueError(f"component {requested} not among {components}")
    return (requested,)


def determinant_rows_for_case(
    q: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    subdegree: int,
    windows: int,
    target: str,
    include_constant: bool,
) -> tuple[int, int, int, ExtensionField, list[OriginDet]]:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]
    if subdegree not in divisors(tensor_factor_degree):
        raise ValueError("requested subdegree does not divide tensor factor degree")
    relative_degree = tensor_factor_degree // subdegree
    if windows > relative_degree:
        raise ValueError("requested windows exceed relative degree")

    subfield_basis = normal_subfield_basis(
        subdegree,
        tensor_factor_degree,
        selected_factor,
        field,
    )
    basis_columns = relative_basis_columns(
        subfield_basis,
        relative_degree,
        selected_factor,
        field,
    )
    gprime_theta = relative_gprime_theta(
        subdegree,
        tensor_factor_degree,
        selected_factor,
        field,
    )

    values = [
        poly_mod(row_to_poly(embedded_residue_vector(vector, field), field), selected_factor, field)
        for vector in residue_vectors
    ]
    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    theta_inv_powers = [b_one(field)]
    for _ in range(1, n):
        theta_inv_powers.append(b_mul(theta_inv_powers[-1], theta_inv, selected_factor, field))

    components = target_components(m, target)
    dets: list[OriginDet] = []
    for shift in range(h):
        alpha, beta = crt_coordinates(shift, m, n)
        multiplier = theta_inv_powers[beta]
        sequence = []
        for r in range(m):
            shifted_value = b_mul(multiplier, values[(r + alpha) % m], selected_factor, field)
            sequence.append(
                top_window_coords(
                    shifted_value,
                    windows,
                    subdegree,
                    relative_degree,
                    gprime_theta,
                    basis_columns,
                    selected_factor,
                    field,
                )
            )
        rows = combined_rows(sequence, components, include_constant, field)
        if not rows or len(rows) != len(rows[0]):
            raise ValueError(
                f"target is not square: rows={len(rows)} coords={len(rows[0]) if rows else 0}"
            )
        dets.append(
            OriginDet(
                shift=shift,
                alpha=alpha,
                beta=beta,
                det=determinant(rows, field),
            )
        )
    return extension_degree, tensor_factor_degree, len(dets[0].det), field, dets


def find_case(args: argparse.Namespace):
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
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if args.subdegree not in divisors(tensor_factor_degree):
                        continue
                    return D, q, ell, cycle, m, factor
        cases += 1
        if cases >= args.max_cases:
            break
    return None


def value_summary(values: list[tuple[int, ...]], field: ExtensionField) -> str:
    return (
        f"count={len(values)} distinct={len(set(values))} "
        f"zeros={sum(1 for value in values if value == field.zero)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
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

    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    n = len(cycle) // m
    extension_degree, tensor_factor_degree, field_degree, field, dets = determinant_rows_for_case(
        q,
        cycle,
        m,
        factor,
        args.seed,
        args.subdegree,
        args.windows,
        args.target,
        not args.without_constant,
    )
    all_values = [row.det for row in dets]
    beta0 = [row.det for row in dets if row.beta == 0]
    alpha0 = [row.det for row in dets if row.alpha == 0]
    by_alpha = {
        alpha: [row.det for row in dets if row.alpha == alpha]
        for alpha in sorted({row.alpha for row in dets})
    }
    alpha_products = {
        alpha: product(values, field)
        for alpha, values in by_alpha.items()
    }

    print("tensor factor marginal origin-action audit")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={len(cycle)}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"factor_degree={factor.degree()}")
    print(f"extension_degree={extension_degree}")
    print(f"tensor_factor_degree={tensor_factor_degree}")
    print(f"subdegree={args.subdegree}")
    print(f"windows={args.windows}")
    print(f"target={args.target}")
    print(f"include_constant={int(not args.without_constant)}")
    print(f"field_tuple_degree={field_degree}")
    print()
    print(f"all_shifts {value_summary(all_values, field)}")
    print(f"pure_alpha_beta0 {value_summary(beta0, field)}")
    print(f"pure_beta_alpha0 {value_summary(alpha0, field)}")
    print(
        "alpha_beta_products "
        f"count={len(alpha_products)} distinct={len(set(alpha_products.values()))} "
        f"zeros={sum(1 for value in alpha_products.values() if value == field.zero)}"
    )
    print()
    print("sample_alpha_products")
    for alpha, value in list(alpha_products.items())[:12]:
        print(f"  alpha={alpha:3d} product={value}")
    print()
    print("interpretation")
    print("  alpha_translation_should_change_marginal_basis_by_a_unit=1")
    print("  beta_shift_can_change_chosen_top_coefficient_exterior_coordinate=1")
    print("  product_over_beta_tests_origin_stable_p_unit_packaging=1")
    print("conclusion=reported_tensor_factor_marginal_origin_action_audit")


if __name__ == "__main__":
    main()
