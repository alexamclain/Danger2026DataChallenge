#!/usr/bin/env python3
"""Audit the dual trace-gcd certificate on small actual-CM Lang rows.

The representative p24 theorem can be phrased as a linearized gcd:

    K = common kernel of four full right-trace blocks,
    first 16 tail coordinates have no nonzero common zero on K.

Equivalently the common-kernel subspace polynomial `P_K` has trivial gcd with
the tail trace maps.  This script computes that dual kernel statement for
small actual-CM Lang rows and compares it with the primal prefix+tail rank
augmentation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from hermitian_mixed_left_subfield_normality_audit import (
    subfield_power_basis,
)
from k_character_tensor_rank_scan import ExtensionField, FpE
from lang_arc_strength_audit import transformed_blocks_for_row
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class TraceGcdProfile:
    omitted: int
    kept_capacity: int
    prefix_block_count: int
    prefix_len: int
    tail_len: int
    prefix_rank: int
    leading_rank: int
    primal_tail_augmentation: int
    dual_kernel_dim: int
    tail_rank_on_kernel: int
    trace_gcd_degree: int
    tail_kernel_det: int | None
    primal_dual_match: bool


@dataclass(frozen=True)
class TraceGcdRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_lengths: tuple[int, ...]
    transformed_rank: int
    profiles: tuple[TraceGcdProfile, ...]


def prefix_split(lengths: list[int], target: int) -> tuple[int, int, int]:
    prefix_len = 0
    block_count = 0
    for length in lengths:
        if prefix_len + length > target:
            break
        prefix_len += length
        block_count += 1
    return block_count, prefix_len, target - prefix_len


def base_value(value: FpE, field: ExtensionField) -> int:
    if any(coord % field.q for coord in value[1:]):
        raise ValueError("trace did not land in base field")
    return value[0] % field.q


def relative_trace_to_base(value: FpE, degree: int, field: ExtensionField) -> int:
    total = field.zero
    for i in range(degree):
        total = field.add(total, field.pow(value, field.q**i))
    return base_value(total, field)


def trace_pair_row(
    value: FpE,
    basis: list[FpE],
    degree: int,
    field: ExtensionField,
) -> list[int]:
    return [
        relative_trace_to_base(field.mul(base, value), degree, field)
        for base in basis
    ]


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return mat[:rank], pivots


def nullspace_basis(matrix: list[list[int]], q: int, cols: int) -> list[list[int]]:
    reduced, pivots = rref(matrix, q)
    pivot_set = set(pivots)
    free_cols = [col for col in range(cols) if col not in pivot_set]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vec = [0] * cols
        vec[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-reduced[row][free_col]) % q
        basis.append(vec)
    return basis


def det_mod(matrix: list[list[int]], q: int) -> int | None:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return None
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = (det * pivot_value) % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det % q


def combine_basis(
    coeffs: list[int],
    basis: list[FpE],
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for coeff, base in zip(coeffs, basis):
        if coeff:
            total = field.add(total, field.scalar_mul(coeff, base))
    return total


def trace_gcd_profile(
    blocks: list[list[FpE]],
    omitted: int,
    left_len: int,
    q: int,
    field: ExtensionField,
    basis: list[FpE],
) -> TraceGcdProfile | None:
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    lengths = [len(block) for block in kept]
    if sum(lengths) < left_len:
        return None
    block_count, prefix_len, tail_len = prefix_split(lengths, left_len)
    values = [value for block in kept for value in block]
    prefix = values[:prefix_len]
    tail = values[prefix_len:left_len]
    leading = values[:left_len]
    prefix_rank = fq_rank(prefix, q)
    leading_rank = fq_rank(leading, q)
    primal_tail_aug = leading_rank - prefix_rank

    prefix_matrix = [
        trace_pair_row(value, basis, left_len, field)
        for value in prefix
    ]
    kernel_coeffs = nullspace_basis(prefix_matrix, q, left_len)
    kernel_values = [
        combine_basis(coeffs, basis, field)
        for coeffs in kernel_coeffs
    ]
    tail_on_kernel = [
        [
            relative_trace_to_base(field.mul(kernel_value, tail_value), left_len, field)
            for kernel_value in kernel_values
        ]
        for tail_value in tail
    ]
    tail_rank = rank_mod_q(tail_on_kernel, q)
    gcd_degree = len(kernel_values) - tail_rank
    tail_det = det_mod(tail_on_kernel, q)
    return TraceGcdProfile(
        omitted=omitted,
        kept_capacity=sum(lengths),
        prefix_block_count=block_count,
        prefix_len=prefix_len,
        tail_len=tail_len,
        prefix_rank=prefix_rank,
        leading_rank=leading_rank,
        primal_tail_augmentation=primal_tail_aug,
        dual_kernel_dim=len(kernel_values),
        tail_rank_on_kernel=tail_rank,
        trace_gcd_degree=gcd_degree,
        tail_kernel_det=tail_det,
        primal_dual_match=(primal_tail_aug == tail_rank),
    )


def audit_row(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    args: argparse.Namespace,
) -> TraceGcdRow | None:
    try:
        extension_degree, field, blocks = transformed_blocks_for_row(
            D, q, ell, cycle, m, factor, left, right, left_orbit, args.seed
        )
    except ValueError:
        return None
    left_len = len(left_orbit)
    if field.degree % left_len:
        return None
    basis = subfield_power_basis(q, left_len, field, args.seed)
    values = [value for block in blocks for value in block]
    profiles = tuple(
        profile
        for omitted in range(len(blocks))
        if (
            profile := trace_gcd_profile(
                blocks, omitted, left_len, q, field, basis
            )
        )
        is not None
    )
    if not profiles:
        return None
    return TraceGcdRow(
        D=D,
        q=q,
        ell=ell,
        h=len(cycle),
        m=m,
        n=len(cycle) // m,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=left_len,
        right_orbit_lengths=tuple(len(block) for block in blocks),
        transformed_rank=fq_rank(values, q),
        profiles=profiles,
    )


def scan(args: argparse.Namespace) -> list[TraceGcdRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[TraceGcdRow] = []
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
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
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
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_row(
                                    D,
                                    q,
                                    ell,
                                    shifted,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args,
                                )
                                if row and row.transformed_rank >= row.left_orbit_len:
                                    rows.append(row)
                                    if len(rows) >= args.max_rows:
                                        return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def profile_text(profile: TraceGcdProfile) -> str:
    return (
        f"omit{profile.omitted}:cap{profile.kept_capacity}:"
        f"blocks{profile.prefix_block_count}:tail{profile.tail_len}:"
        f"prank{profile.prefix_rank}/{profile.prefix_len}:"
        f"lead{profile.leading_rank}:"
        f"aug{profile.primal_tail_augmentation}:"
        f"K{profile.dual_kernel_dim}:"
        f"tailK{profile.tail_rank_on_kernel}:"
        f"gcddeg{profile.trace_gcd_degree}:"
        f"det{profile.tail_kernel_det}:"
        f"match{int(profile.primal_dual_match)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("Lang trace-gcd kernel audit")
    print(f"rows={len(rows)}")
    print("columns: D q ell h m n deg ext pair left right_lengths rank profiles")
    for row in rows:
        profiles = ";".join(profile_text(profile) for profile in row.profiles)
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"deg={row.factor_degree} ext={row.extension_degree} "
            f"pair=({row.left},{row.right}) left={row.left_orbit_rep}:L{row.left_orbit_len} "
            f"right_lengths={list(row.right_orbit_lengths)} "
            f"rank={row.transformed_rank}/{row.left_orbit_len} "
            f"profiles=[{profiles}]"
        )
    print()
    print("interpretation")
    print("  gcddeg_zero_is_the_dual_trace_gcd_certificate=1")
    print("  square_tail_kernel_det_is_a_linearized_resultant_witness=1")
    print("  primal_dual_match_checks_tail_augmentation_equals_tail_rank_on_K=1")
    print("  p24_target_values_are_K16_tailK16_gcddeg0_for_the_representative=1")
    print("conclusion=reported_lang_trace_gcd_kernel_audit")


if __name__ == "__main__":
    main()
