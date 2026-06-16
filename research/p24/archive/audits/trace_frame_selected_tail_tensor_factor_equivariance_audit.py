#!/usr/bin/env python3
"""Tensor-factor equivariance audit for the selected-tail determinant.

The corrected p24 trace-frame target is not just the fixed full leading
minor.  On the prefix chart it is the residual selected-tail determinant:

    K_2 -> selected coordinates in the next relative coefficient block.

The norm-compressed route would like Frobenius transport across the scalar
extension tensor factors to preserve this determinant line up to p-units.  In
small CM rows this script checks the finite shadow of that statement:

* full leading determinant zero/nonzero status across tensor factors;
* selected-tail determinant zero/nonzero status across tensor factors;
* equality of base norms in the deterministic trivialization.

The tail determinant value depends on the chosen prefix-kernel basis, so norm
equality is stronger than what the p-unit theorem requires.  Uniform
zero/nonzero status is the main falsifier.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
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
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
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
    frequencies_for_target,
    pivot_columns_over_extension,
)
from trace_frame_residual_tail_audit import linear_combo, prefix_relation_basis
from trace_frame_residual_tail_origin_action_audit import (
    determinant,
    norm_base,
    residue_vectors_for_origin,
)


@dataclass(frozen=True)
class SelectedTailFactorRow:
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
    prefix_blocks: int
    prefix_rank: int
    residual_dim: int
    full_pivots: tuple[int, ...]
    full_det_zero: bool
    full_det_norm_base: int | None
    tail_det_zero: bool | None
    tail_det_norm_base: int | None


def determinant_zero(value: FpE, field: ExtensionField) -> bool:
    return value == field.zero


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    targets: list[str],
    seed: int,
    max_top_count: int,
) -> list[SelectedTailFactorRow]:
    h = len(cycle)
    n = h // m
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    residue_vectors = residue_vectors_for_origin(cycle, q, m, factor, origin_shift)

    tensor_factor_count = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // tensor_factor_count
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )

    out: list[SelectedTailFactorRow] = []
    for factor_index, selected_factor in enumerate(factors):
        for subdegree in divisors(tensor_factor_degree):
            if subdegree in (1, tensor_factor_degree):
                continue
            relative_degree = tensor_factor_degree // subdegree
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
            for target in targets:
                rows = character_rows(
                    residue_vectors,
                    frequencies_for_target(m, target),
                    zeta,
                    field,
                )
                elements = [
                    poly_mod(row_to_poly(row, field), selected_factor, field)
                    for row in rows
                ]
                elements = [value for value in elements if not b_is_zero(value, field)]
                raw_rank = rank_in_factor(rows, selected_factor, field)
                if raw_rank == 0 or len(elements) != raw_rank:
                    continue
                top_count = (raw_rank + subdegree - 1) // subdegree
                if top_count > relative_degree or top_count > max_top_count:
                    continue
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
                full_pivots = tuple(pivot_columns_over_extension(leading_matrix, field))
                full_det = determinant(leading_matrix, field)

                prefix_blocks = max(0, top_count - 1)
                prefix_cols = prefix_blocks * subdegree
                prefix_matrix = [row[:prefix_cols] for row in top_matrix]
                prefix_rank = rank_over_extension(prefix_matrix, field)
                residual_dim = raw_rank - prefix_rank
                tail_det_zero: bool | None = None
                tail_det_norm: int | None = None
                if residual_dim > 0:
                    relations = prefix_relation_basis(prefix_matrix, raw_rank, field)
                    tail_start = prefix_cols
                    tail_end = tail_start + subdegree
                    tail_rows = [row[tail_start:tail_end] for row in top_matrix]
                    residual_rows = [
                        linear_combo(relation, tail_rows, field)
                        for relation in relations
                    ]
                    leading_tail = [row[:residual_dim] for row in residual_rows]
                    tail_det = determinant(leading_tail, field)
                    tail_det_zero = determinant_zero(tail_det, field)
                    tail_det_norm = norm_base(tail_det, field)

                out.append(
                    SelectedTailFactorRow(
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
                        prefix_blocks=prefix_blocks,
                        prefix_rank=prefix_rank,
                        residual_dim=residual_dim,
                        full_pivots=full_pivots,
                        full_det_zero=determinant_zero(full_det, field),
                        full_det_norm_base=norm_base(full_det, field),
                        tail_det_zero=tail_det_zero,
                        tail_det_norm_base=tail_det_norm,
                    )
                )
    return out


def scan(args: argparse.Namespace) -> list[SelectedTailFactorRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    targets = args.target or ["axis"]
    out: list[SelectedTailFactorRow] = []
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
                m for m in quotient_sizes if len(coprime_components(m)) >= 2
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
                        targets,
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


def bool_key(value: bool | None) -> str:
    if value is None:
        return "NA"
    return "1" if value else "0"


def pivot_blocks(pivots: tuple[int, ...], subdegree: int) -> tuple[int, ...]:
    return tuple(pivot // subdegree for pivot in pivots)


def print_group_summary(
    key: tuple[int, int, int, int, int, str, int],
    rows: list[SelectedTailFactorRow],
) -> None:
    D, q, h, m, n, target, subdegree = key
    factor_count = rows[0].tensor_factor_count
    tail_present = [row for row in rows if row.tail_det_zero is not None]
    full_zero_count = sum(1 for row in rows if row.full_det_zero)
    tail_zero_count = sum(1 for row in tail_present if row.tail_det_zero)
    full_norm_values = [norm_key(row.full_det_norm_base) for row in rows]
    tail_norm_values = [norm_key(row.tail_det_norm_base) for row in tail_present]
    full_shapes = Counter(pivot_blocks(row.full_pivots, row.subdegree) for row in rows)
    residual_dims = sorted({row.residual_dim for row in rows})

    full_zero_uniform = full_zero_count in (0, len(rows))
    tail_zero_uniform = bool(tail_present) and tail_zero_count in (0, len(tail_present))
    full_norm_equal = len(set(full_norm_values)) == 1
    tail_norm_equal = bool(tail_norm_values) and len(set(tail_norm_values)) == 1

    print(
        f"group D={D} q={q} h={h} m={m} n={n} "
        f"target={target} subdegree={subdegree}"
    )
    print(
        f"  factors_covered={len(rows)}/{factor_count} "
        f"tensor_factor_degree={rows[0].tensor_factor_degree} "
        f"raw_ranks={sorted({row.raw_rank for row in rows})} "
        f"top_counts={sorted({row.top_count for row in rows})} "
        f"residual_dims={residual_dims}"
    )
    print(
        f"  full_zero_count={full_zero_count} "
        f"full_norm_distinct={len(set(full_norm_values))} "
        f"full_norm_values={sorted(set(full_norm_values))[:12]}"
    )
    print(
        f"  tail_present={len(tail_present)} "
        f"tail_zero_count={tail_zero_count} "
        f"tail_norm_distinct={len(set(tail_norm_values)) if tail_norm_values else 0} "
        f"tail_norm_values={sorted(set(tail_norm_values))[:12]}"
    )
    print(
        f"  full_pivot_shape_distinct={len(full_shapes)} "
        f"full_pivot_shape_hist={dict(full_shapes)}"
    )
    print(
        "  interpretation "
        f"full_zero_status_uniform={int(full_zero_uniform)} "
        f"tail_zero_status_uniform={int(tail_zero_uniform)} "
        f"full_norm_equal={int(full_norm_equal)} "
        f"tail_norm_equal={int(tail_norm_equal)} "
        f"selected_tail_transport_survives={int(full_zero_uniform and tail_zero_uniform)}"
    )
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=50000)
    ap.add_argument("--only-D", type=int)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=260)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=260)
    ap.add_argument("--max-m", type=int, default=60)
    ap.add_argument("--only-m", type=int)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=500000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=12)
    ap.add_argument("--max-composite-quotients", type=int, default=24)
    ap.add_argument("--max-factor-degree", type=int, default=60)
    ap.add_argument("--max-extension-degree", type=int, default=12)
    ap.add_argument("--min-tensor-factor-count", type=int, default=2)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=24)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=8)
    ap.add_argument("--max-rows", type=int, default=200)
    ap.add_argument("--origin-shift", type=int, default=0)
    ap.add_argument("--target", action="append")
    ap.add_argument("--seed", type=int, default=20260606)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    args = ap.parse_args()

    rows = scan(args)
    print("trace-frame selected-tail tensor-factor equivariance audit")
    print(f"targets={args.target or ['axis']}")
    print(f"origin_shift={args.origin_shift}")
    print(f"rows={len(rows)}")
    print("tail_determinant_values_are_basis_dependent_but_zero_status_is_not=1")
    print()

    groups: dict[
        tuple[int, int, int, int, int, str, int],
        list[SelectedTailFactorRow],
    ] = defaultdict(list)
    for row in rows:
        groups[
            (row.D, row.q, row.h, row.m, row.n, row.target, row.subdegree)
        ].append(row)
    for key in sorted(groups):
        print_group_summary(key, groups[key])

    print("sample_rows")
    for row in rows[: min(80, len(rows))]:
        pivots = ",".join(str(col) for col in row.full_pivots[:24])
        if len(row.full_pivots) > 24:
            pivots += ",..."
        blocks = ",".join(str(block) for block in pivot_blocks(row.full_pivots, row.subdegree))
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"factor_index={row.tensor_factor_index}/{row.tensor_factor_count} "
            f"target={row.target} factor_deg={row.factor_degree} "
            f"ext_deg={row.extension_degree} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} rel={row.relative_degree} "
            f"raw_rank={row.raw_rank} top_count={row.top_count} "
            f"prefix_rank={row.prefix_rank} residual_dim={row.residual_dim} "
            f"full_det_zero={int(row.full_det_zero)} "
            f"full_norm={row.full_det_norm_base if row.full_det_norm_base is not None else 'NA'} "
            f"tail_det_zero={bool_key(row.tail_det_zero)} "
            f"tail_norm={row.tail_det_norm_base if row.tail_det_norm_base is not None else 'NA'} "
            f"pivot_blocks=[{blocks}] pivots=[{pivots}]"
        )
    print()
    print("interpretation")
    print("  tail_zero_status_uniform=0 would falsify selected-tail tensor transport.")
    print("  tail_norm_equal=1 is stronger than needed because kernel bases may rescale.")
    print("  selected_tail_transport_survives=1 keeps the one-norm compression theorem alive.")
    print("conclusion=reported_trace_frame_selected_tail_tensor_factor_equivariance_audit")


if __name__ == "__main__":
    main()
