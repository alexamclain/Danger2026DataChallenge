#!/usr/bin/env python3
"""Orbitwise Schur-bridge falsifier for trace-GCD determinants.

The trace-GCD certificate uses a square tail-on-kernel determinant

    Pi_t = det(B_t | ker A_t).

For ordinary finite matrices there is a stronger Gram/Schur identity

    det([A;B][A;B]^T) det(N^T N)
      = det(A A^T) det(BN)^2,

where columns of N are a kernel basis for A.  This script tests the identity
and its orbit products on actual small-CM trace-GCD rows.  Passing this audit
does not prove p24: the Gram factors are stronger p-unit targets than rank.
Failing it, or seeing zero Gram factors where the trace-GCD determinant is
nonzero, would demote the Hermitian-Schur proof route quickly.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
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
    det_mod,
    nullspace_basis,
    prefix_split,
    relative_trace_to_base,
    trace_pair_row,
)
from lang_trace_gcd_origin_action_audit import crt_alpha_beta
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class SchurRecord:
    shift: int
    alpha: int
    beta: int
    omitted: int
    prefix_len: int
    tail_len: int
    prefix_rank: int
    kernel_dim: int
    tail_rank: int
    tail_det: int | None
    prefix_gram_det: int | None
    full_gram_det: int | None
    kernel_gram_det: int | None
    schur_left: int | None
    schur_right: int | None
    schur_ok: bool


@dataclass(frozen=True)
class SchurRow:
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
    records: tuple[SchurRecord, ...]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(col) for col in zip(*matrix)]


def matmul_mod(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    if not left:
        return []
    cols = len(right[0]) if right else 0
    mid = len(right)
    return [
        [
            sum(row[k] * right[k][col] for k in range(mid)) % q
            for col in range(cols)
        ]
        for row in left
    ]


def gram_det(matrix: list[list[int]], q: int) -> int | None:
    return det_mod(matmul_mod(matrix, transpose(matrix), q), q)


def inverse_matrix(matrix: list[list[int]], q: int) -> list[list[int]] | None:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return None
    augmented = [
        [value % q for value in row] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if augmented[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return None
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = pow(augmented[rank][col], -1, q)
        augmented[rank] = [(inv * value) % q for value in augmented[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = augmented[row][col] % q
            if not scale:
                continue
            augmented[row] = [
                (left - scale * right) % q
                for left, right in zip(augmented[row], augmented[rank])
            ]
        rank += 1
    return [row[n:] for row in augmented]


def trace_metric_matrix(basis, degree: int, field) -> list[list[int]]:
    return [
        [
            relative_trace_to_base(field.mul(left, right), degree, field)
            for right in basis
        ]
        for left in basis
    ]


def metric_gram_det_rows(
    matrix: list[list[int]],
    metric_inverse: list[list[int]],
    q: int,
) -> int | None:
    return det_mod(
        matmul_mod(matmul_mod(matrix, metric_inverse, q), transpose(matrix), q),
        q,
    )


def metric_gram_det_kernel(
    kernel_vectors: list[list[int]],
    metric: list[list[int]],
    q: int,
) -> int | None:
    return det_mod(
        matmul_mod(
            matmul_mod(kernel_vectors, metric, q),
            transpose(kernel_vectors),
            q,
        ),
        q,
    )


def product_mod(values: list[int | None], q: int) -> int | None:
    out = 1
    for value in values:
        if value is None:
            return None
        out = (out * value) % q
    return out


def safe_mul(values: list[int | None], q: int) -> int | None:
    out = 1
    for value in values:
        if value is None:
            return None
        out = out * value % q
    return out


def rank_matrix(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 0
    return rank_mod_q(matrix, q)


def trace_matrices_for_blocks(
    blocks,
    omitted: int,
    left_len: int,
    q: int,
    field,
    basis,
) -> tuple[list[list[int]], list[list[int]], list[list[int]]] | None:
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    lengths = [len(block) for block in kept]
    if sum(lengths) < left_len:
        return None
    _block_count, prefix_len, tail_len = prefix_split(lengths, left_len)
    values = [value for block in kept for value in block]
    prefix_values = values[:prefix_len]
    tail_values = values[prefix_len:left_len]
    prefix_matrix = [
        trace_pair_row(value, basis, left_len, field)
        for value in prefix_values
    ]
    tail_matrix = [
        trace_pair_row(value, basis, left_len, field)
        for value in tail_values
    ]
    kernel_vectors = nullspace_basis(prefix_matrix, q, left_len)
    return prefix_matrix, tail_matrix, kernel_vectors


def schur_record_for_omission(
    shift: int,
    alpha: int,
    beta: int,
    omitted: int,
    blocks,
    left_len: int,
    q: int,
    field,
    basis,
    require_square_tail: bool,
    min_prefix_len: int,
    metric: list[list[int]] | None,
    metric_inverse: list[list[int]] | None,
) -> SchurRecord | None:
    matrices = trace_matrices_for_blocks(
        blocks, omitted, left_len, q, field, basis
    )
    if matrices is None:
        return None
    prefix_matrix, tail_matrix, kernel_vectors = matrices
    prefix_rank = rank_matrix(prefix_matrix, q)
    kernel_dim = len(kernel_vectors)
    tail_len = len(tail_matrix)
    if len(prefix_matrix) < min_prefix_len:
        return None
    if require_square_tail and tail_len != kernel_dim:
        return None

    kernel_columns = transpose(kernel_vectors)
    tail_on_kernel = matmul_mod(tail_matrix, kernel_columns, q)
    tail_rank = rank_matrix(tail_on_kernel, q)
    tail_det = det_mod(tail_on_kernel, q)

    full_matrix = prefix_matrix + tail_matrix
    if metric is None or metric_inverse is None:
        prefix_gram = gram_det(prefix_matrix, q)
        full_gram = gram_det(full_matrix, q)
        kernel_gram = gram_det(kernel_vectors, q)
    else:
        prefix_gram = metric_gram_det_rows(prefix_matrix, metric_inverse, q)
        full_gram = metric_gram_det_rows(full_matrix, metric_inverse, q)
        kernel_gram = metric_gram_det_kernel(kernel_vectors, metric, q)
    if (
        prefix_gram is None
        or full_gram is None
        or kernel_gram is None
        or tail_det is None
    ):
        schur_left = None
        schur_right = None
        schur_ok = False
    else:
        schur_left = full_gram * kernel_gram % q
        schur_right = prefix_gram * tail_det * tail_det % q
        schur_ok = schur_left == schur_right

    return SchurRecord(
        shift=shift,
        alpha=alpha,
        beta=beta,
        omitted=omitted,
        prefix_len=len(prefix_matrix),
        tail_len=tail_len,
        prefix_rank=prefix_rank,
        kernel_dim=kernel_dim,
        tail_rank=tail_rank,
        tail_det=tail_det,
        prefix_gram_det=prefix_gram,
        full_gram_det=full_gram,
        kernel_gram_det=kernel_gram,
        schur_left=schur_left,
        schur_right=schur_right,
        schur_ok=schur_ok,
    )


def audit_schur_row(
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
) -> SchurRow | None:
    h = len(cycle)
    n = h // m
    max_shift = h if args.max_origin_shifts is None else min(h, args.max_origin_shifts)
    records: list[SchurRecord] = []
    extension_degree = None
    right_lengths = None
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
        metric = None
        metric_inverse = None
        if args.metric_aware:
            metric = trace_metric_matrix(basis, len(left_orbit), field)
            metric_inverse = inverse_matrix(metric, q)
            if metric_inverse is None:
                continue
        alpha, beta = crt_alpha_beta(shift, m, n)
        for omitted in range(len(blocks)):
            if args.only_omitted is not None and omitted != args.only_omitted:
                continue
            record = schur_record_for_omission(
                shift,
                alpha,
                beta,
                omitted,
                blocks,
                len(left_orbit),
                q,
                field,
                basis,
                args.require_square_tail,
                args.min_prefix_len,
                metric,
                metric_inverse,
            )
            if record is not None:
                records.append(record)
    if not records or extension_degree is None or right_lengths is None:
        return None
    return SchurRow(
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


def scan(args: argparse.Namespace) -> list[SchurRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[SchurRow] = []
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
                                row = audit_schur_row(
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
                                    rows.append(row)
                                    if len(rows) >= args.max_rows:
                                        return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def frobenius_orbits(q: int, modulus: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        x = start
        while x not in seen:
            seen.add(x)
            orbit.append(x)
            x = x * q % modulus
        out.append(orbit)
    return out


def right_class_mismatch_count(records: list[SchurRecord], attr: str, right: int) -> int:
    values: dict[int, int | None] = {}
    mismatches = 0
    for record in records:
        key = record.alpha % right
        value = getattr(record, attr)
        if key in values and values[key] != value:
            mismatches += 1
        values.setdefault(key, value)
    return mismatches


def beta0_by_right(records: list[SchurRecord], right: int, attr: str) -> list[int | None]:
    values: dict[int, int | None] = {}
    for record in records:
        if record.beta == 0:
            values[record.alpha % right] = getattr(record, attr)
    return [values.get(t) for t in range(right)]


def summarize_row(row: SchurRow) -> None:
    print(
        f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
        f"deg={row.factor_degree} ext={row.extension_degree} "
        f"pair=({row.left},{row.right}) left={row.left_orbit_rep}:L{row.left_orbit_len} "
        f"right_lengths={list(row.right_orbit_lengths)} records={len(row.records)}"
    )
    by_omitted: dict[int, list[SchurRecord]] = defaultdict(list)
    for record in row.records:
        by_omitted[record.omitted].append(record)
    orbits = frobenius_orbits(row.q % row.right, row.right)
    for omitted, records in sorted(by_omitted.items()):
        schur_fail = sum(1 for record in records if not record.schur_ok)
        tail_zero = sum(1 for record in records if record.tail_det == 0)
        prefix_gram_zero = sum(1 for record in records if record.prefix_gram_det == 0)
        full_gram_zero = sum(1 for record in records if record.full_gram_det == 0)
        kernel_gram_zero = sum(1 for record in records if record.kernel_gram_det == 0)
        tail_nonzero_gram_zero = sum(
            1
            for record in records
            if record.tail_det not in (None, 0)
            and (
                record.prefix_gram_det == 0
                or record.full_gram_det == 0
                or record.kernel_gram_det == 0
            )
        )
        print(
            f"  omitted={omitted} count={len(records)} "
            f"tail_zero={tail_zero} schur_fail={schur_fail} "
            f"prefixGram0={prefix_gram_zero} fullGram0={full_gram_zero} "
            f"kernelGram0={kernel_gram_zero} "
            f"tailNonzeroButSomeGram0={tail_nonzero_gram_zero}"
        )
        for attr in [
            "tail_det",
            "prefix_gram_det",
            "full_gram_det",
            "kernel_gram_det",
        ]:
            print(
                f"    {attr}_right_class_mismatches="
                f"{right_class_mismatch_count(records, attr, row.right)}"
            )
        for orbit_id, orbit in enumerate(orbits):
            tail_values = beta0_by_right(records, row.right, "tail_det")
            prefix_values = beta0_by_right(records, row.right, "prefix_gram_det")
            full_values = beta0_by_right(records, row.right, "full_gram_det")
            kernel_values = beta0_by_right(records, row.right, "kernel_gram_det")
            tail_product = product_mod([tail_values[t] for t in orbit], row.q)
            prefix_product = product_mod([prefix_values[t] for t in orbit], row.q)
            full_product = product_mod([full_values[t] for t in orbit], row.q)
            kernel_product = product_mod([kernel_values[t] for t in orbit], row.q)
            left = safe_mul([full_product, kernel_product], row.q)
            right = None
            if prefix_product is not None and tail_product is not None:
                right = prefix_product * tail_product * tail_product % row.q
            orbit_ok = left is not None and right is not None and left == right
            print(
                f"    orbit={orbit_id} members={orbit} "
                f"tailProd={tail_product} prefixGramProd={prefix_product} "
                f"fullGramProd={full_product} kernelGramProd={kernel_product} "
                f"orbitSchur={int(orbit_ok)}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=1)
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
    parser.add_argument("--min-prefix-len", type=int, default=0)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--metric-aware", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("Orbitwise Schur bridge falsifier")
    print(f"metric_aware={int(args.metric_aware)}")
    print(f"rows={len(rows)}")
    for row in rows:
        summarize_row(row)
    print("interpretation")
    print("  schur_fail=0 checks the finite Schur identity in actual-CM coordinates.")
    print("  tailNonzeroButSomeGram0>0 means the Gram route is strictly stronger here.")
    print("  right_class_mismatches=0 supports descent to the reduced right sequence.")
    print("conclusion=reported_orbitwise_schur_bridge_falsifier")


if __name__ == "__main__":
    main()
