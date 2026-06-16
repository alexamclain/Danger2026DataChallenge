#!/usr/bin/env python3
"""Moore determinant audit for one tensor factor.

For a finite field factor `B/E`, elements `x_1,...,x_r` are E-linearly
independent iff the Moore matrix

    (x_i^(Q^j))_{0 <= i,j < r},      Q = |E|,

has nonzero determinant in `B`.

This script checks the Moore-rank formulation on small one-factor tensor rows.
It is the intrinsic version of the coordinate-minor certificate.
"""

from __future__ import annotations

import argparse

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import (
    PolyE,
    equal_degree_factors,
    poly_mod,
    poly_mul,
    poly_powmod,
    poly_sub,
    rank_in_factor,
    row_to_poly,
    sympy_factor_to_poly_e,
    trim,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    axis_frequency_set,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


def b_zero(field: ExtensionField) -> PolyE:
    return [field.zero]


def b_one(field: ExtensionField) -> PolyE:
    return [field.one]


def b_is_zero(value: PolyE, field: ExtensionField) -> bool:
    value = trim(value, field)
    return len(value) == 1 and value[0] == field.zero


def b_add(left: PolyE, right: PolyE, modulus: PolyE, field: ExtensionField) -> PolyE:
    n = max(len(left), len(right))
    out = [field.zero for _ in range(n)]
    for i in range(n):
        a = left[i] if i < len(left) else field.zero
        b = right[i] if i < len(right) else field.zero
        out[i] = field.add(a, b)
    return poly_mod(trim(out, field), modulus, field)


def b_sub(left: PolyE, right: PolyE, modulus: PolyE, field: ExtensionField) -> PolyE:
    return poly_mod(poly_sub(left, right, field), modulus, field)


def b_mul(left: PolyE, right: PolyE, modulus: PolyE, field: ExtensionField) -> PolyE:
    return poly_mod(poly_mul(left, right, field), modulus, field)


def b_pow(base: PolyE, exponent: int, modulus: PolyE, field: ExtensionField) -> PolyE:
    return poly_powmod(base, exponent, modulus, field)


def b_inv(value: PolyE, modulus: PolyE, field: ExtensionField) -> PolyE:
    if b_is_zero(value, field):
        raise ZeroDivisionError("inverse of zero in tensor factor")
    degree = len(modulus) - 1
    return b_pow(value, field.q ** (field.degree * degree) - 2, modulus, field)


def rank_over_factor(matrix: list[list[PolyE]], modulus: PolyE, field: ExtensionField) -> int:
    mat = [
        [poly_mod(entry, modulus, field) for entry in row]
        for row in matrix
        if any(not b_is_zero(entry, field) for entry in row)
    ]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if not b_is_zero(mat[row][col], field):
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = b_inv(mat[rank][col], modulus, field)
        mat[rank] = [b_mul(value, inv, modulus, field) for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
            if b_is_zero(scale, field):
                continue
            mat[row] = [
                b_sub(left, b_mul(scale, right, modulus, field), modulus, field)
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def moore_rank(elements: list[PolyE], modulus: PolyE, field: ExtensionField) -> int:
    q_power = field.q ** field.degree
    rows: list[list[PolyE]] = []
    for value in elements:
        row: list[PolyE] = []
        current = poly_mod(value, modulus, field)
        for _ in range(len(elements)):
            row.append(current)
            current = b_pow(current, q_power, modulus, field)
        rows.append(row)
    return rank_over_factor(rows, modulus, field)


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def audit(args: argparse.Namespace) -> list[dict[str, int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[dict[str, int]] = []
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
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue

                    residues = [
                        fiber.rem(factor)
                        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
                    ]
                    residue_vectors = [
                        coeff_vector(residue, factor.degree(), q)
                        for residue in residues
                    ]
                    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
                    field = ExtensionField(q, extension_degree, modulus)
                    zeta = primitive_root_of_order(field, m, args.seed)
                    frequencies = axis_frequency_set(m)
                    rows = character_rows(residue_vectors, frequencies, zeta, field)
                    factors = equal_degree_factors(
                        sympy_factor_to_poly_e(factor, field),
                        tensor_factor_degree,
                        field,
                        args.seed,
                    )
                    selected = factors[0]
                    elements = [
                        poly_mod(row_to_poly(row, field), selected, field)
                        for row in rows
                    ]
                    coord_rank = rank_in_factor(rows, selected, field)
                    m_rank = moore_rank(elements, selected, field)
                    out.append(
                        {
                            "D": D,
                            "q": q,
                            "ell": ell,
                            "h": h,
                            "m": m,
                            "n": n,
                            "factor_degree": factor.degree(),
                            "extension_degree": extension_degree,
                            "tensor_factor_degree": tensor_factor_degree,
                            "axis_dim": len(frequencies),
                            "coordinate_rank": coord_rank,
                            "moore_rank": m_rank,
                        }
                    )
                    case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=4)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=80)
    parser.add_argument("--max-m", type=int, default=20)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=20)
    parser.add_argument("--max-extension-degree", type=int, default=4)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = audit(args)
    mismatches = [row for row in rows if row["coordinate_rank"] != row["moore_rank"]]
    full_rows = [row for row in rows if row["moore_rank"] == row["axis_dim"]]
    possible = [
        row for row in rows
        if row["tensor_factor_degree"] >= row["axis_dim"]
    ]
    possible_failures = [
        row for row in possible
        if row["moore_rank"] < row["axis_dim"]
    ]

    print("tensor factor Moore audit")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print("columns: D q ell h m n deg ext factor_deg axis coord_rank moore_rank")
        for row in rows[:60]:
            print(
                f"D={row['D']:7d} q={row['q']:7d} ell={row['ell']:3d} "
                f"h={row['h']:3d} m={row['m']:3d} n={row['n']:3d} "
                f"deg={row['factor_degree']:3d} ext={row['extension_degree']:2d} "
                f"factor_deg={row['tensor_factor_degree']:3d} "
                f"axis={row['axis_dim']:3d} "
                f"coord_rank={row['coordinate_rank']:3d} "
                f"moore_rank={row['moore_rank']:3d}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  coordinate_moore_mismatch_rows={len(mismatches)}")
    print(f"  moore_full_rank_rows={len(full_rows)}")
    print(f"  one_factor_dimension_possible_rows={len(possible)}")
    print(f"  one_factor_dimension_possible_moore_failure_rows={len(possible_failures)}")
    print()
    print("interpretation")
    print("  Moore_rank_equals_coordinate_rank_confirms_intrinsic_rank_certificate=1")
    print("  Moore_full_rank_is_the_coordinate-free_one_factor_target=1")
    print("conclusion=reported_tensor_factor_moore_audit")


if __name__ == "__main__":
    main()
