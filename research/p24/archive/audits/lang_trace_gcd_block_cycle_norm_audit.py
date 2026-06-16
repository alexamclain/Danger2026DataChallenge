#!/usr/bin/env python3
"""Block-cyclic crossed-product norm audit for trace-GCD tail maps.

The scalar crossed-product audit packages the determinant values

    Delta(t) = det(M_t)

as a weighted cycle.  This audit lifts one level lower: it uses the actual
tail-on-kernel matrices `M_t` and forms a block cyclic operator with `M_t` as
the blocks.  Its determinant is the orbit product up to the block-permutation
sign:

    det(block_cycle(M_0,...,M_{r-1}))
      = (-1)^(k*(r-1)) * prod_i det(M_i).

For p24, `k=16` and nonzero orbit length `r=35`, so the sign is positive.
This is the finite matrix/Fitting object a producer theorem should try to
construct p-integrally.
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
from hermitian_mixed_left_subfield_normality_audit import subfield_power_basis
from lang_arc_strength_audit import transformed_blocks_for_row
from lang_trace_gcd_kernel_audit import (
    combine_basis,
    det_mod,
    nullspace_basis,
    prefix_split,
    relative_trace_to_base,
    trace_pair_row,
)
from lang_trace_gcd_origin_action_audit import OriginDet, crt_alpha_beta
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class MatrixRecord:
    shift: int
    alpha: int
    beta: int
    omitted: int
    determinant: int | None
    matrix: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class MatrixRow:
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
    records: tuple[MatrixRecord, ...]


def tail_on_kernel_matrix(blocks, omitted: int, left_len: int, q: int, field, basis):
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    lengths = [len(block) for block in kept]
    if sum(lengths) < left_len:
        return None
    _block_count, prefix_len, tail_len = prefix_split(lengths, left_len)
    values = [value for block in kept for value in block]
    prefix = values[:prefix_len]
    tail = values[prefix_len:left_len]
    prefix_matrix = [
        trace_pair_row(value, basis, left_len, field)
        for value in prefix
    ]
    kernel_coeffs = nullspace_basis(prefix_matrix, q, left_len)
    kernel_values = [
        combine_basis(coeffs, basis, field)
        for coeffs in kernel_coeffs
    ]
    if tail_len != len(kernel_values):
        return None
    matrix = [
        [
            relative_trace_to_base(field.mul(kernel_value, tail_value), left_len, field)
            for kernel_value in kernel_values
        ]
        for tail_value in tail
    ]
    return matrix


def audit_matrix_row(
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
) -> MatrixRow | None:
    h = len(cycle)
    n = h // m
    records: list[MatrixRecord] = []
    right_lengths: tuple[int, ...] | None = None
    extension_degree: int | None = None
    max_shift = h if args.max_origin_shifts is None else min(h, args.max_origin_shifts)
    for shift in range(max_shift):
        shifted = rotate(cycle, shift)
        try:
            ext_degree, field, blocks = transformed_blocks_for_row(
                D, q, ell, shifted, m, factor, left, right, left_orbit, args.seed
            )
        except ValueError:
            continue
        extension_degree = ext_degree
        right_lengths = tuple(len(block) for block in blocks)
        basis = subfield_power_basis(q, len(left_orbit), field, args.seed)
        for omitted in range(len(blocks)):
            if args.only_omitted is not None and omitted != args.only_omitted:
                continue
            matrix = tail_on_kernel_matrix(
                blocks, omitted, len(left_orbit), q, field, basis
            )
            if matrix is None:
                continue
            determinant = det_mod(matrix, q)
            alpha, beta = crt_alpha_beta(shift, m, n)
            records.append(
                MatrixRecord(
                    shift=shift,
                    alpha=alpha,
                    beta=beta,
                    omitted=omitted,
                    determinant=determinant,
                    matrix=tuple(tuple(value % q for value in row) for row in matrix),
                )
            )
    if not records or right_lengths is None or extension_degree is None:
        return None
    return MatrixRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=len(left_orbit),
        right_orbit_lengths=right_lengths,
        records=tuple(records),
    )


def first_matrix_row(args: argparse.Namespace) -> MatrixRow | None:
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
                                row = audit_matrix_row(
                                    D,
                                    q,
                                    ell,
                                    cycle,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args,
                                )
                                if row is not None:
                                    return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def block_cycle_matrix(matrices: list[tuple[tuple[int, ...], ...]], q: int) -> list[list[int]]:
    orbit_len = len(matrices)
    block_size = len(matrices[0])
    total = orbit_len * block_size
    out = [[0 for _ in range(total)] for _ in range(total)]
    for block_col, matrix in enumerate(matrices):
        block_row = (block_col + 1) % orbit_len
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                out[block_row * block_size + i][block_col * block_size + j] = value % q
    return out


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def frobenius_orbits(modulus: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = value * multiplier % modulus
        out.append(orbit)
    return out


def records_by_omitted(records: tuple[MatrixRecord, ...]) -> dict[int, list[MatrixRecord]]:
    out: dict[int, list[MatrixRecord]] = {}
    for record in records:
        out.setdefault(record.omitted, []).append(record)
    return dict(sorted(out.items()))


def class_representatives(records: list[MatrixRecord], right: int):
    by_right: dict[int, MatrixRecord] = {}
    det_mismatches = 0
    for record in records:
        key = record.alpha % right
        if key in by_right and by_right[key].determinant != record.determinant:
            det_mismatches += 1
        by_right.setdefault(key, record)
    return [by_right[t] for t in range(right)], det_mismatches


def main() -> None:
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_matrix_row(args)
    if row is None:
        raise SystemExit("no eligible matrix row found")

    orbits = frobenius_orbits(row.right, row.q % row.right)
    p24_block_size = 16
    p24_orbit_len = 35

    print("Lang trace-gcd block-cycle norm audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"frobenius_orbits={orbits}")
    print(f"p24_block_size={p24_block_size}")
    print(f"p24_nonzero_orbit_len={p24_orbit_len}")
    print(f"p24_nonzero_block_cycle_dimension={p24_block_size * p24_orbit_len}")
    print(f"p24_block_cycle_sign_positive={int((p24_block_size * (p24_orbit_len - 1)) % 2 == 0)}")

    failures = 0
    for omitted, records in records_by_omitted(row.records).items():
        reps, det_mismatches = class_representatives(records, row.right)
        if det_mismatches:
            failures += 1
        block_size = len(reps[0].matrix)
        print(f"omitted={omitted}")
        print(f"  right_class_det_mismatches={det_mismatches}")
        print(f"  block_size={block_size}")
        print(f"  determinants={[record.determinant for record in reps]}")
        for orbit_index, orbit in enumerate(orbits):
            orbit_records = [reps[index] for index in orbit]
            matrices = [record.matrix for record in orbit_records]
            dets = [int(record.determinant) for record in orbit_records if record.determinant is not None]
            product = product_mod(dets, row.q)
            block_matrix = block_cycle_matrix(matrices, row.q)
            block_det = det_mod(block_matrix, row.q)
            block_rank = rank_mod(block_matrix, row.q)
            block_dim = len(block_matrix)
            local_singular_count = sum(1 for det in dets if det == 0)
            sign = 1 if (block_size * (len(orbit) - 1)) % 2 == 0 else -1
            signed_product = product if sign == 1 else (-product) % row.q
            match = block_det == signed_product
            failures += int(not match)
            print(
                f"  orbit={orbit_index} rep={orbit[0]} len={len(orbit)} "
                f"block_cycle_dim={block_dim}"
            )
            print(f"    dets={dets}")
            print(f"    local_singular_count={local_singular_count}")
            print(f"    product={product}")
            print(f"    sign={sign}")
            print(f"    signed_product={signed_product}")
            print(f"    block_cycle_det={block_det}")
            print(f"    block_cycle_rank={block_rank}/{block_dim}")
            print(f"    block_cycle_full_rank={int(block_rank == block_dim)}")
            print(
                "    block_cycle_full_rank_iff_no_local_singular="
                f"{int((block_rank == block_dim) == (local_singular_count == 0))}"
            )
            print(f"    block_cycle_match={int(match)}")
            print(f"    block_cycle_nonzero={int(block_det != 0)}")

    print("interpretation")
    print("  block_cycle_match=1 lifts the scalar crossed norm to tail-on-kernel matrices")
    print("  full-rank block cycle is equivalent here to no local singular tail map")
    print("  p24 producer can target seven block-cycle/Fitting determinants")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_block_cycle_norm_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
