#!/usr/bin/env python3
"""Tensor-factor equivariance audit for the fixed leading Plucker minor.

The norm-compressed p24 route would like one degree-8 determinant-line norm
to cover the 70 scalar-extension tensor factors.  This is stronger than
packetwise nonvanishing: the fixed leading minor must be transported across
tensor factors by p-unit changes of trivialization, or else one needs 70
separate degree-8 p-unit targets.

This audit checks compact CM rows where a packet factor splits over
E=F_q(mu_m).  For each scalar-extension factor it computes the same fixed
leading trace-frame determinant and compares rank, pivot shape, zero status,
and base norm.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
from trace_frame_plucker_pivot_audit import (
    pivot_blocks,
    pivot_columns_over_extension,
)
from trace_frame_residual_tail_origin_action_audit import determinant, norm_base


@dataclass(frozen=True)
class FactorEquivarianceRow:
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
    tensor_factor_count: int
    tensor_factor_index: int
    subdegree: int
    relative_degree: int
    raw_rank: int
    top_count: int
    target_dim: int
    top_rank: int
    pivot_columns: tuple[int, ...]
    det_zero: bool
    det_norm_base: int | None


def frequencies_for_target(m: int, target: str) -> list[int]:
    if target == "axis":
        return axis_frequency_set(m)
    for name, frequencies in frequency_blocks(m):
        if target == name:
            return frequencies
        if target == f"constant_plus_{name}":
            return sorted(set([0] + frequencies))
    raise ValueError(f"unknown target {target!r} for m={m}")


def residue_vectors_for_origin(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    origin_shift: int,
) -> list[list[int]]:
    shifted = rotate(cycle, origin_shift)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(shifted, q, m, "complement")
    ]
    return [coeff_vector(residue, factor.degree(), q) for residue in residues]


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    target: str,
    seed: int,
    max_top_count: int,
) -> list[FactorEquivarianceRow]:
    h = len(cycle)
    n = h // m
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    residue_vectors = residue_vectors_for_origin(cycle, q, m, factor, origin_shift)
    rows = character_rows(
        residue_vectors,
        frequencies_for_target(m, target),
        zeta,
        field,
    )

    tensor_factor_count = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // tensor_factor_count
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )

    out: list[FactorEquivarianceRow] = []
    for factor_index, selected_factor in enumerate(factors):
        elements = [
            poly_mod(row_to_poly(row, field), selected_factor, field)
            for row in rows
        ]
        elements = [value for value in elements if not b_is_zero(value, field)]
        raw_rank = rank_in_factor(rows, selected_factor, field)
        if raw_rank == 0 or len(elements) != raw_rank:
            continue
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
            top_matrix = [
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
            leading_matrix = [row[:raw_rank] for row in top_matrix]
            pivots = tuple(pivot_columns_over_extension(leading_matrix, field))
            det = determinant(leading_matrix, field)
            out.append(
                FactorEquivarianceRow(
                    D=D,
                    q=q,
                    ell=ell,
                    h=h,
                    m=m,
                    n=n,
                    origin_shift=origin_shift,
                    target=target,
                    factor_degree=factor.degree(),
                    extension_degree=extension_degree,
                    tensor_factor_degree=tensor_factor_degree,
                    tensor_factor_count=len(factors),
                    tensor_factor_index=factor_index,
                    subdegree=subdegree,
                    relative_degree=relative_degree,
                    raw_rank=raw_rank,
                    top_count=top_count,
                    target_dim=top_count * subdegree,
                    top_rank=len(pivots),
                    pivot_columns=pivots,
                    det_zero=(det == field.zero),
                    det_norm_base=norm_base(det, field),
                )
            )
    return out


def scan(args: argparse.Namespace) -> list[FactorEquivarianceRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[FactorEquivarianceRow] = []
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
                    tensor_factor_count = int(sp.igcd(factor.degree(), extension_degree))
                    if tensor_factor_count < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // tensor_factor_count
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    rows = audit_case(
                        D,
                        q,
                        ell,
                        cycle,
                        m,
                        factor,
                        args.origin_shift,
                        args.target,
                        args.seed,
                        args.max_top_count,
                    )
                    if rows:
                        out.extend(rows)
                        cases += 1
                        if cases >= args.max_cases or len(out) >= args.max_rows:
                            return out[: args.max_rows]
        if cases >= args.max_cases or len(out) >= args.max_rows:
            break
    return out[: args.max_rows]


def norm_key(value: int | None) -> str:
    return "NA" if value is None else str(value)


def print_group_summary(
    key: tuple[int, int, int, int, int, str, int],
    rows: list[FactorEquivarianceRow],
) -> None:
    D, q, h, m, n, target, subdegree = key
    factor_count = rows[0].tensor_factor_count
    raw_ranks = sorted({row.raw_rank for row in rows})
    top_ranks = sorted({row.top_rank for row in rows})
    zero_count = sum(1 for row in rows if row.det_zero)
    norm_values = [norm_key(row.det_norm_base) for row in rows]
    pivot_shapes = Counter(
        pivot_blocks(row.pivot_columns, row.subdegree)
        for row in rows
    )
    print(
        f"group D={D} q={q} h={h} m={m} n={n} "
        f"target={target} subdegree={subdegree}"
    )
    print(
        f"  factors_covered={len(rows)}/{factor_count} "
        f"tensor_factor_degree={rows[0].tensor_factor_degree} "
        f"raw_ranks={raw_ranks} top_ranks={top_ranks} "
        f"zero_count={zero_count}"
    )
    print(
        f"  det_norm_distinct={len(set(norm_values))} "
        f"det_norm_values={sorted(set(norm_values))[:12]}"
    )
    print(
        f"  pivot_shape_distinct={len(pivot_shapes)} "
        f"pivot_shape_hist={dict(pivot_shapes)}"
    )
    print(
        "  interpretation "
        f"zero_status_uniform={int(zero_count in (0, len(rows)))} "
        f"norm_equal={int(len(set(norm_values)) == 1)} "
        f"pivot_shape_equal={int(len(pivot_shapes) == 1)}"
    )
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=50000)
    ap.add_argument("--only-D", type=int)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=220)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=220)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=500000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=8)
    ap.add_argument("--max-composite-quotients", type=int, default=12)
    ap.add_argument("--max-factor-degree", type=int, default=60)
    ap.add_argument("--max-extension-degree", type=int, default=12)
    ap.add_argument("--min-tensor-factor-count", type=int, default=2)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=24)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=8)
    ap.add_argument("--max-rows", type=int, default=160)
    ap.add_argument("--origin-shift", type=int, default=0)
    ap.add_argument("--target", default="axis")
    ap.add_argument("--seed", type=int, default=20260605)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    args = ap.parse_args()

    rows = scan(args)
    print("trace-frame tensor-factor equivariance audit")
    print(f"target={args.target}")
    print(f"origin_shift={args.origin_shift}")
    print(f"rows={len(rows)}")
    print()

    groups: dict[
        tuple[int, int, int, int, int, str, int],
        list[FactorEquivarianceRow],
    ] = defaultdict(list)
    for row in rows:
        groups[
            (row.D, row.q, row.h, row.m, row.n, row.target, row.subdegree)
        ].append(row)
    for key in sorted(groups):
        print_group_summary(key, groups[key])

    print("sample_rows")
    for row in rows[: min(80, len(rows))]:
        pivots = ",".join(str(col) for col in row.pivot_columns[:24])
        if len(row.pivot_columns) > 24:
            pivots += ",..."
        blocks = ",".join(
            str(block) for block in pivot_blocks(row.pivot_columns, row.subdegree)
        )
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"factor_index={row.tensor_factor_index}/{row.tensor_factor_count} "
            f"target={row.target} factor_deg={row.factor_degree} "
            f"ext_deg={row.extension_degree} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} rel={row.relative_degree} "
            f"raw_rank={row.raw_rank} top_count={row.top_count} "
            f"target_dim={row.target_dim} top_rank={row.top_rank} "
            f"det_zero={int(row.det_zero)} "
            f"det_norm={row.det_norm_base if row.det_norm_base is not None else 'NA'} "
            f"pivot_blocks=[{blocks}] pivots=[{pivots}]"
        )
    print()
    print("interpretation")
    print("  zero_status_uniform=1 supports tensor-factor rank/vanishing symmetry.")
    print("  norm_equal=1 supports a single fixed determinant-line norm in this row.")
    print("  norm_equal=0 means equality is not automatic in the chosen trivialization.")
    print("  pivot_shape_equal=0 warns against packetwise or factorwise pivot descent.")
    print("conclusion=reported_trace_frame_tensor_factor_equivariance_audit")


if __name__ == "__main__":
    main()
