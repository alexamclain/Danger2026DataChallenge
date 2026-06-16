#!/usr/bin/env python3
"""Origin-action audit for the trace-frame residual-tail determinant.

The residual-tail frontier reduces the leading trace-frame coordinate to:

    prefix Top blocks + a small leading slice in the next Top block.

For p24 this is a 179 + 179 + 10 coordinate.  The alpha part of an origin
shift is understood up to a harmless sign, while the beta part is the real
class-field phase.  This script checks small tensor rows where the residual
tail is proper and records how the full leading determinant and the tail
determinant move across the full origin orbit.

The tail determinant is computed after a deterministic right-kernel basis for
the prefix block.  Its exact value depends on that basis; its zero/nonzero
status does not.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from axis_minor_origin_action_audit import crt_coordinates
from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    relative_norm_to_base,
)
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
from trace_frame_plucker_pivot_audit import frequencies_for_target
from trace_frame_residual_tail_audit import linear_combo, prefix_relation_basis


@dataclass(frozen=True)
class OriginTailRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    subdegree: int
    relative_degree: int
    target: str
    shift: int
    alpha: int
    beta: int
    raw_rank: int
    top_count: int
    prefix_blocks: int
    prefix_rank: int
    residual_dim: int
    full_det: FpE
    full_det_norm_base: int | None
    tail_det: FpE | None
    tail_det_norm_base: int | None


def determinant(matrix: list[list[FpE]], field: ExtensionField) -> FpE:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a square matrix")
    mat = [row[:] for row in matrix]
    det = field.one
    for col in range(size):
        pivot = None
        for row in range(col, size):
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
        for row in range(col + 1, size):
            scale = mat[row][col]
            if scale == field.zero:
                continue
            factor = field.mul(scale, inv)
            mat[row] = [
                field.sub(left, field.mul(factor, right))
                for left, right in zip(mat[row], mat[col])
            ]
    return det


def norm_base(value: FpE, field: ExtensionField) -> int | None:
    return base_value_or_none(relative_norm_to_base(value, field.degree, field), field)


def residue_vectors_for_origin(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    shift: int,
) -> list[list[int]]:
    shifted = rotate(cycle, shift)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(shifted, q, m, "complement")
    ]
    return [coeff_vector(residue, factor.degree(), q) for residue in residues]


def rows_for_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    targets: list[str],
    seed: int,
    max_top_count: int,
) -> list[OriginTailRow]:
    h = len(cycle)
    n = h // m
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]

    out: list[OriginTailRow] = []
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
        for shift in range(h):
            residue_vectors = residue_vectors_for_origin(cycle, q, m, factor, shift)
            alpha, beta = crt_coordinates(shift, m, n)
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
                full_det = determinant(leading_matrix, field)

                prefix_blocks = max(0, top_count - 1)
                prefix_cols = prefix_blocks * subdegree
                prefix_matrix = [row[:prefix_cols] for row in top_matrix]
                prefix_rank = rank_over_extension(prefix_matrix, field)
                residual_dim = raw_rank - prefix_rank
                tail_det: FpE | None = None
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
                    tail_det_norm = norm_base(tail_det, field)
                out.append(
                    OriginTailRow(
                        D=D,
                        q=q,
                        ell=ell,
                        h=h,
                        m=m,
                        n=n,
                        factor_degree=factor.degree(),
                        extension_degree=extension_degree,
                        tensor_factor_degree=tensor_factor_degree,
                        subdegree=subdegree,
                        relative_degree=relative_degree,
                        target=target,
                        shift=shift,
                        alpha=alpha,
                        beta=beta,
                        raw_rank=raw_rank,
                        top_count=top_count,
                        prefix_blocks=prefix_blocks,
                        prefix_rank=prefix_rank,
                        residual_dim=residual_dim,
                        full_det=full_det,
                        full_det_norm_base=norm_base(full_det, field),
                        tail_det=tail_det,
                        tail_det_norm_base=tail_det_norm,
                    )
                )
    return out


def find_rows(args: argparse.Namespace) -> list[OriginTailRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    targets = args.target or ["axis"]
    seen: set[int] = set()
    out: list[OriginTailRow] = []
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
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    rows = rows_for_case(
                        D,
                        q,
                        ell,
                        cycle,
                        m,
                        factor,
                        targets,
                        args.seed,
                        args.max_top_count,
                    )
                    if rows:
                        out.extend(rows)
                        cases += 1
                        if args.first_case_only or cases >= args.max_cases:
                            return out
        if cases >= args.max_cases:
            break
    return out


def value_summary(values: list[FpE | None], zero_value: FpE) -> str:
    present = [value for value in values if value is not None]
    return (
        f"count={len(present)} distinct={len(set(present))} "
        f"zeros={sum(1 for value in present if value == zero_value)}"
    )


def norm_summary(values: list[int | None]) -> str:
    present = [value for value in values if value is not None]
    return (
        f"count={len(present)} distinct={len(set(present))} "
        f"zeros={sum(1 for value in present if value == 0)}"
    )


def print_group_summary(
    key: tuple[int, int, int, int, str, int],
    rows: list[OriginTailRow],
) -> None:
    D, q, h, m, target, subdegree = key
    n = rows[0].n
    zero = tuple(0 for _ in rows[0].full_det)
    proper_rows = [row for row in rows if 0 < row.residual_dim < row.subdegree]
    by_alpha: dict[int, list[OriginTailRow]] = defaultdict(list)
    by_beta: dict[int, list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        by_alpha[row.alpha].append(row)
        by_beta[row.beta].append(row)

    full_beta_distincts = [
        len({row.full_det for row in alpha_rows})
        for alpha_rows in by_alpha.values()
    ]
    tail_beta_distincts = [
        len({row.tail_det for row in alpha_rows if row.tail_det is not None})
        for alpha_rows in by_alpha.values()
    ]
    tail_beta_zero_counts = [
        sum(1 for row in alpha_rows if row.tail_det == zero)
        for alpha_rows in by_alpha.values()
    ]
    beta0 = [row for row in rows if row.beta == 0]
    alpha0 = [row for row in rows if row.alpha == 0]

    def norm_products_by_alpha(kind: str) -> list[int | None]:
        products: list[int | None] = []
        for alpha_rows in by_alpha.values():
            total = 1
            for row in alpha_rows:
                value = row.full_det_norm_base if kind == "full" else row.tail_det_norm_base
                if value is None:
                    total = -1
                    break
                total = (total * value) % row.q
            products.append(None if total == -1 else total)
        return products

    full_norm_products = norm_products_by_alpha("full")
    tail_norm_products = norm_products_by_alpha("tail")

    print(
        f"group D={D} q={q} h={h} m={m} n={n} "
        f"target={target} subdegree={subdegree}"
    )
    print(
        f"  rows={len(rows)} proper_partial_rows={len(proper_rows)} "
        f"raw_ranks={sorted({row.raw_rank for row in rows})} "
        f"top_counts={sorted({row.top_count for row in rows})} "
        f"residual_dims={sorted({row.residual_dim for row in rows})}"
    )
    print(f"  full_det_all {value_summary([row.full_det for row in rows], zero)}")
    print(f"  full_norm_all {norm_summary([row.full_det_norm_base for row in rows])}")
    print(f"  tail_det_all {value_summary([row.tail_det for row in rows], zero)}")
    print(f"  tail_norm_all {norm_summary([row.tail_det_norm_base for row in rows])}")
    print(f"  pure_alpha_beta0_full_norm {norm_summary([row.full_det_norm_base for row in beta0])}")
    print(f"  pure_alpha_beta0_tail_norm {norm_summary([row.tail_det_norm_base for row in beta0])}")
    print(f"  pure_beta_alpha0_full_norm {norm_summary([row.full_det_norm_base for row in alpha0])}")
    print(f"  pure_beta_alpha0_tail_norm {norm_summary([row.tail_det_norm_base for row in alpha0])}")
    print(
        "  beta_orbit_full_det_distinct "
        f"min={min(full_beta_distincts)} max={max(full_beta_distincts)} "
        f"expected_beta_count={n}"
    )
    print(
        "  beta_orbit_tail_det_distinct "
        f"min={min(tail_beta_distincts)} max={max(tail_beta_distincts)} "
        f"tail_zero_count_min={min(tail_beta_zero_counts)} "
        f"tail_zero_count_max={max(tail_beta_zero_counts)} "
        f"expected_beta_count={n}"
    )
    # Avoid reconstructing the field just for products.  Tuple products are not
    # meaningful without the original modulus, so product diagnostics are
    # reported by zero status.
    beta_product_zero_by_alpha = [
        any(row.tail_det == zero for row in alpha_rows)
        for alpha_rows in by_alpha.values()
    ]
    print(
        "  tail_product_over_beta_zero_by_alpha "
        f"count={len(beta_product_zero_by_alpha)} "
        f"zero_products={sum(beta_product_zero_by_alpha)}"
    )
    print(
        "  full_norm_product_over_beta_by_alpha "
        f"{norm_summary(full_norm_products)}"
    )
    print(
        "  tail_norm_product_over_beta_by_alpha "
        f"{norm_summary(tail_norm_products)}"
    )
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--min-h", type=int, default=1)
    ap.add_argument("--max-h", type=int, default=240)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=240)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=20000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=48)
    ap.add_argument("--max-composite-quotients", type=int, default=48)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=1)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument("--first-case-only", action="store_true")
    ap.add_argument(
        "--target",
        action="append",
        help="Target such as axis, constant_plus_4, constant_plus_3.",
    )
    args = ap.parse_args()

    rows = find_rows(args)
    print("trace-frame residual tail origin-action audit")
    print(f"rows={len(rows)}")
    print("tail_determinant_values_are_basis_dependent_but_zero_status_is_not=1")
    print()
    groups: dict[tuple[int, int, int, int, str, int], list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        groups[(row.D, row.q, row.h, row.m, row.target, row.subdegree)].append(row)
    for key in sorted(groups):
        print_group_summary(key, groups[key])

    print("sample_rows")
    for row in rows[: min(80, len(rows))]:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} "
            f"shift={row.shift} alpha={row.alpha} beta={row.beta} "
            f"target={row.target} factor_deg={row.factor_degree} "
            f"ext_deg={row.extension_degree} tensor_deg={row.tensor_factor_degree} "
            f"subdeg={row.subdegree} reldeg={row.relative_degree} "
            f"raw_rank={row.raw_rank} top_count={row.top_count} "
            f"prefix_rank={row.prefix_rank} residual_dim={row.residual_dim} "
            f"full_det_zero={int(row.full_det == tuple(0 for _ in row.full_det))} "
            f"full_norm={row.full_det_norm_base if row.full_det_norm_base is not None else 'NA'} "
            f"tail_det_zero={int(row.tail_det == tuple(0 for _ in row.full_det)) if row.tail_det is not None else 'NA'} "
            f"tail_norm={row.tail_det_norm_base if row.tail_det_norm_base is not None else 'NA'}"
        )
    print("conclusion=reported_trace_frame_residual_tail_origin_action_audit")


if __name__ == "__main__":
    main()
