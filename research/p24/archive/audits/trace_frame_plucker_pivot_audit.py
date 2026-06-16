#!/usr/bin/env python3
"""Mine deterministic Plucker coordinates for trace-frame toy rows.

The p24 trace-frame certificate needs a named Plucker coordinate of

    Top_3(W_axis) <= C^3

to be nonzero.  Earlier audits checked only the rank profile.  This script
records the actual pivot coordinate chosen by deterministic row reduction in
small tensor-factor rows, using the minimal top window

    top_count = ceil(raw_rank / subdegree).

The output is meant to test whether the "named coordinate" might be governed
by a stable rule rather than by a random-looking existential minor.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    rank_in_factor,
    row_to_poly,
    sympy_factor_to_poly_e,
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
    rotate,
    section_fiber_polynomials,
)
from tensor_factor_dual_basis_window_audit import (
    discriminants,
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    top_window_coords,
)
from tensor_factor_moore_audit import b_is_zero
from tensor_factor_subfield_trace_audit import divisors


@dataclass(frozen=True)
class PivotRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    origin_shift: int
    target: str
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    subdegree: int
    relative_degree: int
    raw_rank: int
    top_count: int
    target_dim: int
    top_rank: int
    pivot_columns: tuple[int, ...]


def pivot_columns_over_extension(
    matrix: list[list[FpE]],
    field: ExtensionField,
) -> list[int]:
    mat = [row[:] for row in matrix if any(value != field.zero for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = field.inv(mat[rank][col])
        mat[rank] = [field.mul(value, inv) for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return pivots


def frequencies_for_target(m: int, target: str) -> list[int]:
    if target == "axis":
        return axis_frequency_set(m)
    for name, frequencies in frequency_blocks(m):
        if target == name:
            return frequencies
        if target == f"constant_plus_{name}":
            return sorted(set([0] + frequencies))
    raise ValueError(f"unknown target {target!r} for m={m}")


def pivot_blocks(pivots: tuple[int, ...], subdegree: int) -> tuple[int, ...]:
    return tuple(sorted({col // subdegree for col in pivots}))


def audit_target(
    D: int,
    q: int,
    ell: int,
    h: int,
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    residue_vectors: list[list[int]],
    target: str,
    seed: int,
    max_top_count: int,
) -> list[PivotRow]:
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    rows = character_rows(
        residue_vectors,
        frequencies_for_target(m, target),
        zeta,
        field,
    )

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    raw_rank = rank_in_factor(rows, selected_factor, field)
    if raw_rank == 0:
        return []

    out: list[PivotRow] = []
    for subdegree in divisors(tensor_factor_degree):
        if subdegree in (1, tensor_factor_degree):
            continue
        relative_degree = tensor_factor_degree // subdegree
        top_count = (raw_rank + subdegree - 1) // subdegree
        if top_count > relative_degree or top_count > max_top_count:
            continue
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
        matrix = [
            top_window_coords(
                value,
                top_count,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                selected_factor,
                field,
            )
            for value in elements
        ]
        pivots = tuple(pivot_columns_over_extension(matrix, field))
        out.append(
            PivotRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                m=m,
                n=h // m,
                origin_shift=origin_shift,
                target=target,
                factor_degree=factor.degree(),
                extension_degree=extension_degree,
                tensor_factor_degree=tensor_factor_degree,
                subdegree=subdegree,
                relative_degree=relative_degree,
                raw_rank=raw_rank,
                top_count=top_count,
                target_dim=top_count * subdegree,
                top_rank=len(pivots),
                pivot_columns=pivots,
            )
        )
    return out


def scan(args: argparse.Namespace) -> list[PivotRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[PivotRow] = []
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
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
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
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
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
                        if len(divisors(tensor_factor_degree)) <= 2:
                            continue
                        residues = [
                            fiber.rem(factor)
                            for fiber in section_fiber_polynomials(
                                shifted,
                                q,
                                m,
                                "complement",
                            )
                        ]
                        residue_vectors = [
                            coeff_vector(residue, factor.degree(), q)
                            for residue in residues
                        ]
                        rows.extend(
                            audit_target(
                                D,
                                q,
                                ell,
                                h,
                                m,
                                factor,
                                shift,
                                residue_vectors,
                                args.target,
                                args.seed,
                                args.max_top_count,
                            )
                        )
                        case_had_row = True
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=12)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=48)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--target", default="axis")
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--max-top-count", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    full = [row for row in rows if row.top_rank == row.raw_rank]
    failures = [row for row in rows if row.top_rank < row.raw_rank]
    pivot_shapes = Counter(
        (row.subdegree, row.top_count, pivot_blocks(row.pivot_columns, row.subdegree))
        for row in full
    )

    print("trace-frame Plucker pivot audit")
    print(f"target={args.target}")
    print(f"rows={len(rows)}")
    print(f"full_top_rank_rows={len(full)}")
    print(f"top_rank_failure_rows={len(failures)}")
    print(f"scan_origins={args.scan_origins}")
    print()
    print(
        "columns: D q ell h m n origin target deg ext factor_deg "
        "sub rel raw top_count target_dim top_rank pivot_blocks pivots"
    )
    display = failures[:24] or rows[: min(len(rows), 80)]
    for row in display:
        pivots = ",".join(str(col) for col in row.pivot_columns[:40])
        if len(row.pivot_columns) > 40:
            pivots += ",..."
        blocks = ",".join(
            str(block) for block in pivot_blocks(row.pivot_columns, row.subdegree)
        )
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"origin={row.origin_shift:3d} target={row.target:>16s} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"sub={row.subdegree:3d} rel={row.relative_degree:3d} "
            f"raw={row.raw_rank:3d} top_count={row.top_count:2d} "
            f"target_dim={row.target_dim:3d} top_rank={row.top_rank:3d} "
            f"pivot_blocks=[{blocks}] pivots=[{pivots}]"
        )

    print()
    print("pivot_shape_hist")
    for shape, count in sorted(pivot_shapes.items()):
        subdegree, top_count, blocks = shape
        print(
            f"  subdegree={subdegree} top_count={top_count} "
            f"blocks={list(blocks)} count={count}"
        )
    print()
    print("interpretation")
    print("  full_top_rank_rows_are_named_Plucker_coordinates=1")
    print("  repeated_pivot_shapes_are_candidate_certificate_rules=1")
    print("conclusion=reported_trace_frame_plucker_pivot_audit")


if __name__ == "__main__":
    main()
