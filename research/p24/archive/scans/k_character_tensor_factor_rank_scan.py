#!/usr/bin/env python3
"""Per-factor tensor K-character rank scan.

`k_character_tensor_rank_scan.py` computes rank in the full tensor algebra

    A tensor F_q(mu_m) ~= E[X]/(f).

This script goes one step further for small rows: it factors `f` over
`E=F_q(mu_m)` and measures the axis-character rank in each irreducible tensor
factor.  For p24 the corresponding question is whether one of the 70 factors
of degree 5549 already carries full 368-dimensional axis rank.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    axis_frequency_set,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)


PolyE = list[FpE]


def trim(poly: PolyE, field: ExtensionField) -> PolyE:
    out = poly[:]
    while len(out) > 1 and out[-1] == field.zero:
        out.pop()
    if not out:
        return [field.zero]
    return out


def poly_degree(poly: PolyE, field: ExtensionField) -> int:
    poly = trim(poly, field)
    if len(poly) == 1 and poly[0] == field.zero:
        return -1
    return len(poly) - 1


def poly_add(left: PolyE, right: PolyE, field: ExtensionField) -> PolyE:
    n = max(len(left), len(right))
    out = [field.zero for _ in range(n)]
    for i in range(n):
        a = left[i] if i < len(left) else field.zero
        b = right[i] if i < len(right) else field.zero
        out[i] = field.add(a, b)
    return trim(out, field)


def poly_sub(left: PolyE, right: PolyE, field: ExtensionField) -> PolyE:
    n = max(len(left), len(right))
    out = [field.zero for _ in range(n)]
    for i in range(n):
        a = left[i] if i < len(left) else field.zero
        b = right[i] if i < len(right) else field.zero
        out[i] = field.sub(a, b)
    return trim(out, field)


def poly_mul(left: PolyE, right: PolyE, field: ExtensionField) -> PolyE:
    if poly_degree(left, field) < 0 or poly_degree(right, field) < 0:
        return [field.zero]
    out = [field.zero for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        if a == field.zero:
            continue
        for j, b in enumerate(right):
            if b != field.zero:
                out[i + j] = field.add(out[i + j], field.mul(a, b))
    return trim(out, field)


def poly_divmod(left: PolyE, right: PolyE, field: ExtensionField) -> tuple[PolyE, PolyE]:
    right = trim(right, field)
    if poly_degree(right, field) < 0:
        raise ZeroDivisionError("polynomial division by zero")
    rem = trim(left, field)
    quotient = [field.zero for _ in range(max(0, len(rem) - len(right) + 1))]
    right_degree = poly_degree(right, field)
    right_lc_inv = field.inv(right[-1])
    while poly_degree(rem, field) >= right_degree:
        shift = poly_degree(rem, field) - right_degree
        coeff = field.mul(rem[-1], right_lc_inv)
        quotient[shift] = coeff
        for i in range(right_degree + 1):
            rem[shift + i] = field.sub(rem[shift + i], field.mul(coeff, right[i]))
        rem = trim(rem, field)
    return trim(quotient, field), rem


def poly_mod(left: PolyE, modulus: PolyE, field: ExtensionField) -> PolyE:
    return poly_divmod(left, modulus, field)[1]


def poly_monic(poly: PolyE, field: ExtensionField) -> PolyE:
    poly = trim(poly, field)
    if poly_degree(poly, field) < 0:
        return poly
    inv_lc = field.inv(poly[-1])
    return [field.mul(coeff, inv_lc) for coeff in poly]


def poly_gcd(left: PolyE, right: PolyE, field: ExtensionField) -> PolyE:
    a = trim(left, field)
    b = trim(right, field)
    while poly_degree(b, field) >= 0:
        a, b = b, poly_mod(a, b, field)
    return poly_monic(a, field)


def poly_powmod(base: PolyE, exponent: int, modulus: PolyE, field: ExtensionField) -> PolyE:
    result = [field.one]
    current = poly_mod(base, modulus, field)
    e = exponent
    while e:
        if e & 1:
            result = poly_mod(poly_mul(result, current, field), modulus, field)
        current = poly_mod(poly_mul(current, current, field), modulus, field)
        e >>= 1
    return result


def sympy_factor_to_poly_e(factor: sp.Poly, field: ExtensionField) -> PolyE:
    x = factor.gens[0]
    return [
        field.embed(int(factor.coeff_monomial(x**i)))
        for i in range(factor.degree() + 1)
    ]


def row_to_poly(row: list[FpE], field: ExtensionField) -> PolyE:
    return trim(row[:], field)


def random_poly(max_degree: int, field: ExtensionField, rng: random.Random) -> PolyE:
    return trim(
        [
            tuple(rng.randrange(field.q) for _ in range(field.degree))
            for _ in range(max_degree)
        ],
        field,
    )


def equal_degree_factors(
    poly: PolyE,
    factor_degree: int,
    field: ExtensionField,
    seed: int,
) -> list[PolyE]:
    poly = poly_monic(poly, field)
    total_degree = poly_degree(poly, field)
    if total_degree == factor_degree:
        return [poly]
    if total_degree % factor_degree:
        raise ValueError("factor_degree does not divide polynomial degree")
    rng = random.Random(seed + 1000003 * total_degree + 9176 * factor_degree)
    factors = [poly]
    target_count = total_degree // factor_degree
    exponent = (field.q ** (field.degree * factor_degree) - 1) // 2
    x_poly = [field.zero, field.one]
    attempts = 0
    while len(factors) < target_count:
        attempts += 1
        if attempts > 2000:
            raise RuntimeError("equal-degree factorization did not split")
        candidate = random_poly(total_degree, field, rng)
        if poly_degree(candidate, field) <= 0:
            candidate = x_poly
        new_factors: list[PolyE] = []
        changed = False
        for f in factors:
            if poly_degree(f, field) == factor_degree:
                new_factors.append(f)
                continue
            h = poly_sub(poly_powmod(candidate, exponent, f, field), [field.one], field)
            g = poly_gcd(f, h, field)
            g_degree = poly_degree(g, field)
            f_degree = poly_degree(f, field)
            if 0 < g_degree < f_degree:
                quotient, remainder = poly_divmod(f, g, field)
                if poly_degree(remainder, field) >= 0:
                    raise AssertionError("nonzero remainder in factor split")
                new_factors.append(poly_monic(g, field))
                new_factors.append(poly_monic(quotient, field))
                changed = True
            else:
                new_factors.append(f)
        if changed:
            factors = new_factors
    return sorted((poly_monic(f, field) for f in factors), key=lambda f: repr(f))


def rank_in_factor(rows: list[list[FpE]], factor: PolyE, field: ExtensionField) -> int:
    degree = poly_degree(factor, field)
    matrix: list[list[FpE]] = []
    for row in rows:
        reduced = poly_mod(row_to_poly(row, field), factor, field)
        reduced = reduced + [field.zero] * (degree - len(reduced))
        matrix.append(reduced[:degree])
    return rank_over_extension(matrix, field)


@dataclass(frozen=True)
class FactorRankRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_count: int
    tensor_factor_degree: int
    axis_dim: int
    full_tensor_axis_rank: int
    factor_ranks: tuple[int, ...]
    factor_full_rank_count: int


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> FactorRankRow:
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
    zeta = primitive_root_of_order(field, m, seed)
    axis_frequencies = axis_frequency_set(m)
    axis_rows = character_rows(residue_vectors, axis_frequencies, zeta, field)
    full_tensor_axis_rank = rank_over_extension(axis_rows, field)

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    factor_ranks = tuple(rank_in_factor(axis_rows, f, field) for f in factors)
    return FactorRankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        tensor_factor_count=len(factors),
        tensor_factor_degree=tensor_factor_degree,
        axis_dim=len(axis_frequencies),
        full_tensor_axis_rank=full_tensor_axis_rank,
        factor_ranks=factor_ranks,
        factor_full_rank_count=sum(rank == len(axis_frequencies) for rank in factor_ranks),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[FactorRankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[FactorRankRow] = []
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
        if args.max_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m <= args.max_m]
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
        if not splits:
            continue
        case_had_row = False
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
                    if factor.degree() // gcd_degree > args.max_tensor_factor_degree:
                        continue
                    rows.append(audit_packet(D, q, ell, cycle, m, factor, args.seed))
                    case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=10)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--max-m", type=int, default=40)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=40)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    one_factor_full = [row for row in rows if row.factor_full_rank_count]
    equal_factor_rank_rows = [
        row for row in rows if len(set(row.factor_ranks)) <= 1
    ]
    unequal_factor_rank_rows = [
        row for row in rows if len(set(row.factor_ranks)) > 1
    ]
    dimension_possible_one_factor = [
        row for row in rows if row.tensor_factor_degree >= row.axis_dim
    ]
    dimension_possible_no_full_factor = [
        row for row in dimension_possible_one_factor
        if row.factor_full_rank_count == 0
    ]
    full_tensor_possible = [
        row for row in rows if row.factor_degree >= row.axis_dim
    ]
    full_tensor_failures = [
        row for row in full_tensor_possible
        if row.full_tensor_axis_rank < row.axis_dim
    ]
    factor_count_hist: dict[int, int] = {}
    for row in rows:
        factor_count_hist[row.tensor_factor_count] = (
            factor_count_hist.get(row.tensor_factor_count, 0) + 1
        )

    print("K-character tensor factor-rank scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_m={args.max_m}")
    print(f"max_factor_degree={args.max_factor_degree}")
    print(f"max_extension_degree={args.max_extension_degree}")
    print(f"min_tensor_factor_count={args.min_tensor_factor_count}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext factors factor_deg axis "
            "tensor_rank factor_ranks full_factor_count"
        )
        display = dimension_possible_no_full_factor + rows[:60]
        seen_keys: set[tuple[int, int, int, int, int]] = set()
        for row in display[:80]:
            key = (row.D, row.q, row.m, row.n, row.factor_degree)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"factors={row.tensor_factor_count:2d} "
                f"factor_deg={row.tensor_factor_degree:3d} "
                f"axis={row.axis_dim:3d} "
                f"tensor_rank={row.full_tensor_axis_rank:3d} "
                f"factor_ranks={list(row.factor_ranks)} "
                f"full_factor_count={row.factor_full_rank_count}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  tensor_factor_count_histogram={dict(sorted(factor_count_hist.items()))}")
    print(f"  full_tensor_axis_possible_rows={len(full_tensor_possible)}")
    print(f"  full_tensor_axis_failure_rows={len(full_tensor_failures)}")
    print(f"  one_factor_full_axis_rows={len(one_factor_full)}")
    print(f"  equal_factor_rank_rows={len(equal_factor_rank_rows)}")
    print(f"  unequal_factor_rank_rows={len(unequal_factor_rank_rows)}")
    print(f"  one_factor_dimension_possible_rows={len(dimension_possible_one_factor)}")
    print(f"  one_factor_dimension_possible_no_full_factor_rows={len(dimension_possible_no_full_factor)}")
    print()
    print("interpretation")
    print("  one_factor_full_axis_row_means_a_single_tensor_factor_certifies_axis_rank=1")
    print("  equal_factor_rank_rows_are_predicted_by_semilinear_frobenius_symmetry=1")
    print("  dimension_possible_no_full_factor_is_counterevidence_for_one_factor_theorem=1")
    print("conclusion=reported_k_character_tensor_factor_rank_scan")


if __name__ == "__main__":
    main()
