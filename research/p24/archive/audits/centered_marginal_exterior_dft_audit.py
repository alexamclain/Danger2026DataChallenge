#!/usr/bin/env python3
"""Exterior-DFT audit for centered marginal translation determinants.

For centered points P_b in F_q^d indexed by b mod r, the consecutive affine
minor

    F(t) = det(P_{t+1}-P_t, ..., P_{t+d}-P_t)

has an exact Fourier/Cauchy-Binet expansion after adjoining mu_r:

    F(t) = sum_k A_k zeta_r^(k*t),

where each A_k is a sum over d-subsets of nonzero right characters.  This
script checks that identity on small actual-CM rows and measures whether the
character expansion is sparse enough to suggest a component-module shortcut.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd

import sympy as sp
from cypari2 import Pari

from centered_marginal_cyclic_code_boundary import affine_window_det, point_matrix
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class ExteriorDftRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    extension_degree: int
    subset_count: int
    nonzero_term_count: int
    zero_det_q_count: int
    zero_det_v_count: int
    coefficient_support_size: int
    coefficient_frobenius_failures: int
    reconstruction_failures: int
    window_zero_count: int
    window_distinct_count: int
    frequency_term_histogram: tuple[tuple[int, int], ...]
    nonzero_frequency_orbits: tuple[tuple[int, ...], ...]
    orbit_products: tuple[tuple[tuple[int, ...], int], ...]


def det_extension(matrix: list[list[FpE]], field: ExtensionField) -> FpE:
    mat = [row[:] for row in matrix]
    n = len(mat)
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
        for row in range(col + 1, n):
            scale = field.mul(mat[row][col], inv)
            if scale == field.zero:
                continue
            for j in range(col, n):
                mat[row][j] = field.sub(
                    mat[row][j],
                    field.mul(scale, mat[col][j]),
                )
    return det


def histogram(values: list[int]) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return tuple(sorted(out.items()))


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def right_dft_points(
    points: list[list[int]],
    right: int,
    zeta: FpE,
    field: ExtensionField,
) -> dict[int, list[FpE]]:
    inv_right = field.embed(pow(right, -1, field.q))
    zeta_powers = [field.one]
    for _ in range(1, right):
        zeta_powers.append(field.mul(zeta_powers[-1], zeta))

    out: dict[int, list[FpE]] = {}
    for s in range(1, right):
        coords: list[FpE] = []
        for row in points:
            total = field.zero
            for b, value in enumerate(row):
                weight = zeta_powers[(-s * b) % right]
                total = field.add(total, field.mul(field.embed(value), weight))
            coords.append(field.mul(total, inv_right))
        out[s] = coords
    return out


def exterior_coefficients(
    point_dft: dict[int, list[FpE]],
    right: int,
    zeta: FpE,
    field: ExtensionField,
) -> tuple[list[FpE], int, int, int, list[int]]:
    d = len(next(iter(point_dft.values())))
    zeta_powers = [field.one]
    for _ in range(1, right):
        zeta_powers.append(field.mul(zeta_powers[-1], zeta))

    coeffs = [field.zero for _ in range(right)]
    nonzero_terms = 0
    zero_det_q = 0
    zero_det_v = 0
    terms_by_frequency = [0 for _ in range(right)]
    for subset in combinations(range(1, right), d):
        q_matrix = [[point_dft[s][row] for s in subset] for row in range(d)]
        det_q = det_extension(q_matrix, field)
        if det_q == field.zero:
            zero_det_q += 1
            continue
        v_matrix = [
            [field.sub(zeta_powers[(s * offset) % right], field.one) for offset in range(1, d + 1)]
            for s in subset
        ]
        det_v = det_extension(v_matrix, field)
        if det_v == field.zero:
            zero_det_v += 1
            continue
        frequency = sum(subset) % right
        term = field.mul(det_q, det_v)
        coeffs[frequency] = field.add(coeffs[frequency], term)
        terms_by_frequency[frequency] += 1
        nonzero_terms += 1
    return coeffs, nonzero_terms, zero_det_q, zero_det_v, terms_by_frequency


def evaluate_coefficients(
    coeffs: list[FpE],
    right: int,
    t: int,
    zeta: FpE,
    field: ExtensionField,
) -> FpE:
    powers = [field.one]
    for _ in range(1, right):
        powers.append(field.mul(powers[-1], zeta))
    total = field.zero
    for frequency, coeff in enumerate(coeffs):
        if coeff != field.zero:
            total = field.add(
                total,
                field.mul(coeff, powers[(frequency * t) % right]),
            )
    return total


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def coefficient_frobenius_failures(coeffs: list[FpE], q: int, right: int, field: ExtensionField) -> int:
    failures = 0
    for frequency, coeff in enumerate(coeffs):
        target = (q * frequency) % right
        if coeffs[target] != frobenius(coeff, field):
            failures += 1
    return failures


def nonzero_frequency_orbits(coeffs: list[FpE], q: int, right: int) -> tuple[tuple[int, ...], ...]:
    out: list[tuple[int, ...]] = []
    for orbit in q_orbits(right, q):
        if any(coeffs[frequency] != tuple(0 for _ in coeffs[0]) for frequency in orbit):
            out.append(tuple(orbit))
    return tuple(out)


def orbit_products(values: list[int], q: int, right: int) -> tuple[tuple[tuple[int, ...], int], ...]:
    out = [((0,), values[0] % q)]
    for orbit in q_orbits(right, q):
        out.append((tuple(orbit), product_mod([values[index] for index in orbit], q)))
    return tuple(out)


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    seed: int,
    max_subsets: int,
) -> ExteriorDftRow | None:
    h = len(cycle)
    n = h // m
    if factor.degree() % 2:
        return None
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    d = left - 1
    if d <= 0 or right < left:
        return None
    subset_count = comb(right - 1, d)
    if subset_count > max_subsets:
        return None

    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    marginal = double_marginal(kernel_matrix(residues, factor, q), left, right, q)
    points = point_matrix(marginal, left, right, q)
    values = [affine_window_det(points, start, d, q) for start in range(right)]

    extension_degree = int(sp.n_order(q % right, right))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, right, seed)
    point_dft = right_dft_points(points, right, zeta, field)
    coeffs, nonzero_terms, zero_det_q, zero_det_v, terms_by_frequency = (
        exterior_coefficients(point_dft, right, zeta, field)
    )
    reconstruction_failures = 0
    for t, value in enumerate(values):
        if evaluate_coefficients(coeffs, right, t, zeta, field) != field.embed(value):
            reconstruction_failures += 1

    return ExteriorDftRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        extension_degree=extension_degree,
        subset_count=subset_count,
        nonzero_term_count=nonzero_terms,
        zero_det_q_count=zero_det_q,
        zero_det_v_count=zero_det_v,
        coefficient_support_size=sum(1 for coeff in coeffs if coeff != field.zero),
        coefficient_frobenius_failures=coefficient_frobenius_failures(coeffs, q, right, field),
        reconstruction_failures=reconstruction_failures,
        window_zero_count=sum(1 for value in values if value == 0),
        window_distinct_count=len(set(values)),
        frequency_term_histogram=histogram(terms_by_frequency),
        nonzero_frequency_orbits=nonzero_frequency_orbits(coeffs, q, right),
        orbit_products=orbit_products(values, q, right),
    )


def scan(args: argparse.Namespace) -> ExteriorDftRow | None:
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
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([c for c in coprime_components(m) if c > 2]) >= 2
        ]
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
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                components = tuple(c for c in coprime_components(m) if c > 2)
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in components:
                        if args.only_left and left != args.only_left:
                            continue
                        for right in components:
                            if args.only_right and right != args.only_right:
                                continue
                            row = audit_case(
                                D,
                                q,
                                ell,
                                cycle,
                                m,
                                factor,
                                left,
                                right,
                                args.seed,
                                args.max_subsets,
                            )
                            if row is not None:
                                return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


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
    parser.add_argument("--max-subsets", type=int, default=20000)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")

    print("Centered marginal exterior-DFT audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"extension_degree={row.extension_degree}")
    print()
    print(f"subset_count={row.subset_count}")
    print(f"nonzero_term_count={row.nonzero_term_count}")
    print(f"zero_det_q_count={row.zero_det_q_count}")
    print(f"zero_det_v_count={row.zero_det_v_count}")
    print(f"coefficient_support_size={row.coefficient_support_size}/{row.right}")
    print(f"coefficient_frobenius_failures={row.coefficient_frobenius_failures}")
    print(f"reconstruction_failures={row.reconstruction_failures}")
    print(f"window_zero_count={row.window_zero_count}")
    print(f"window_distinct_count={row.window_distinct_count}")
    print(f"frequency_term_histogram={dict(row.frequency_term_histogram)}")
    print(f"nonzero_frequency_orbits={row.nonzero_frequency_orbits}")
    print("orbit_products")
    for orbit, value in row.orbit_products:
        print(f"  orbit={list(orbit)} product={value}")
    print()
    print("interpretation")
    print("  exterior_dft_formula_verified_if_reconstruction_failures_is_0=1")
    print("  full_support_demotes_sparse_character_module_shortcut=1")
    print("  zero_frobenius_failures_confirms_expected_base_valued_covariance=1")
    print("conclusion=reported_centered_marginal_exterior_dft_audit")


if __name__ == "__main__":
    main()
