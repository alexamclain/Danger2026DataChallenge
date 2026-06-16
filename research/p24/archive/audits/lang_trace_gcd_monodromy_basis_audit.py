#!/usr/bin/env python3
"""Monodromy-product audit for trace-GCD block-cycle norms.

For square blocks, a block-cycle determinant can be collapsed numerically to
the determinant of a product of the small blocks:

    det(block_cycle(M_i)) = sign * det(M_{r-1} ... M_0).

This looks like a smaller producer object.  But in the trace-GCD construction
the columns of `M_t` are expressed in a nullspace basis chosen separately for
each translated prefix kernel.  Unless those bases are coherently identified,
the raw product is a basis artifact rather than a natural monodromy map.

This audit checks both facts on a small actual-CM row:

* determinant product identity holds;
* the kernel nullspace pivot/free-column data varies, so the raw monodromy
  should not be treated as an intrinsic p24 producer object without an
  additional basis-descent theorem.
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
    rref,
    trace_pair_row,
)
from lang_trace_gcd_origin_action_audit import crt_alpha_beta
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class MatrixRecord:
    alpha: int
    beta: int
    omitted: int
    prefix_len: int
    tail_len: int
    determinant: int
    matrix: tuple[tuple[int, ...], ...]
    prefix_pivots: tuple[int, ...]
    kernel_free_cols: tuple[int, ...]


@dataclass(frozen=True)
class MatrixRow:
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_len: int
    records: tuple[MatrixRecord, ...]


def tail_matrix_with_basis_data(blocks, omitted: int, left_len: int, q: int, field, basis):
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
    _reduced, pivots = rref(prefix_matrix, q)
    pivot_set = set(pivots)
    free_cols = tuple(col for col in range(left_len) if col not in pivot_set)
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
    determinant = det_mod(matrix, q)
    if determinant is None:
        return None
    return matrix, determinant, tuple(pivots), free_cols, prefix_len, tail_len


def matrix_mul(left, right, q: int):
    rows = len(left)
    mid = len(right)
    cols = len(right[0])
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(mid):
            if not left[i][k]:
                continue
            for j in range(cols):
                out[i][j] = (out[i][j] + left[i][k] * right[k][j]) % q
    return out


def product_matrix(matrices, q: int):
    size = len(matrices[0])
    out = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    for matrix in matrices:
        out = matrix_mul(matrix, out, q)
    return out


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * value % q
    return out


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


def audit_row(D, q, ell, cycle, m, factor, left, right, left_orbit, args):
    h = len(cycle)
    n = h // m
    records: list[MatrixRecord] = []
    extension_degree = None
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
        basis = subfield_power_basis(q, len(left_orbit), field, args.seed)
        for omitted in range(len(blocks)):
            if args.only_omitted is not None and omitted != args.only_omitted:
                continue
            data = tail_matrix_with_basis_data(
                blocks, omitted, len(left_orbit), q, field, basis
            )
            if data is None:
                continue
            matrix, determinant, pivots, free_cols, prefix_len, tail_len = data
            alpha, beta = crt_alpha_beta(shift, m, n)
            records.append(
                MatrixRecord(
                    alpha=alpha,
                    beta=beta,
                    omitted=omitted,
                    prefix_len=prefix_len,
                    tail_len=tail_len,
                    determinant=determinant,
                    matrix=tuple(tuple(value % q for value in row) for row in matrix),
                    prefix_pivots=pivots,
                    kernel_free_cols=free_cols,
                )
            )
    if not records or extension_degree is None:
        return None
    return MatrixRow(
        D=D,
        q=q,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_len=len(left_orbit),
        records=tuple(records),
    )


def first_row(args):
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
                            if len(q_orbits(right, q)) < args.min_right_orbits:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_row(
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


def by_omitted(records):
    out: dict[int, list[MatrixRecord]] = {}
    for record in records:
        out.setdefault(record.omitted, []).append(record)
    return dict(sorted(out.items()))


def right_reps(records: list[MatrixRecord], right: int):
    by_right: dict[int, MatrixRecord] = {}
    mismatches = 0
    for record in records:
        key = record.alpha % right
        if key in by_right and by_right[key].determinant != record.determinant:
            mismatches += 1
        by_right.setdefault(key, record)
    return [by_right[t] for t in range(right)], mismatches


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
    parser.add_argument("--only_omitted", "--only-omitted", dest="only_omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_row(args)
    if row is None:
        raise SystemExit("no eligible monodromy row found")

    orbits = frobenius_orbits(row.right, row.q % row.right)

    print("Lang trace-gcd monodromy basis audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit_len={row.left_orbit_len}")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"frobenius_orbits={orbits}")

    failures = 0
    for omitted, records in by_omitted(row.records).items():
        reps, mismatches = right_reps(records, row.right)
        if mismatches:
            failures += 1
        print(f"omitted={omitted}")
        print(f"  right_class_det_mismatches={mismatches}")
        print(f"  prefix_lengths_by_t={[record.prefix_len for record in reps]}")
        print(f"  tail_lengths_by_t={[record.tail_len for record in reps]}")
        print(f"  prefix_pivots_by_t={[record.prefix_pivots for record in reps]}")
        print(f"  kernel_free_cols_by_t={[record.kernel_free_cols for record in reps]}")
        print(
            "  kernel_basis_pattern_distinct="
            f"{len({(record.prefix_pivots, record.kernel_free_cols) for record in reps})}"
        )
        for orbit_index, orbit in enumerate(orbits):
            orbit_records = [reps[index] for index in orbit]
            matrices = [record.matrix for record in orbit_records]
            determinants = [record.determinant for record in orbit_records]
            monodromy = product_matrix(matrices, row.q)
            monodromy_det = det_mod(monodromy, row.q)
            product = product_mod(determinants, row.q)
            basis_patterns = {
                (record.prefix_pivots, record.kernel_free_cols)
                for record in orbit_records
            }
            match = monodromy_det == product
            failures += int(not match)
            print(f"  orbit={orbit_index} rep={orbit[0]} len={len(orbit)}")
            print(f"    determinants={determinants}")
            print(f"    product={product}")
            print(f"    monodromy_det={monodromy_det}")
            print(f"    monodromy_det_match={int(match)}")
            print(f"    orbit_basis_pattern_distinct={len(basis_patterns)}")
            print(
                "    monodromy_intrinsic_without_basis_descent="
                f"{int(len(basis_patterns) == 1)}"
            )

    print("interpretation")
    print("  monodromy_det_match=1 is determinant algebra.")
    print("  prefix_len=0 means the pinned row has no nontrivial prefix-kernel descent.")
    print("  varying nonzero-prefix basis patterns would make raw products non-intrinsic.")
    print("  p24 monodromy compression needs an additional coherent-kernel-basis theorem.")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_monodromy_basis_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
