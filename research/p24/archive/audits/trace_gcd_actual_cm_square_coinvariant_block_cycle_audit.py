#!/usr/bin/env python3
"""Actual-CM block-cycle audit for square coinvariant maps.

The nonzero p24 target is the skew/crossed norm of transported square
coinvariant maps

    Phi_t : R^4 + C_t -> E/(tau_R - 1)E.

The tail-on-kernel block-cycle audits already check this norm after choosing
prefix kernels.  This audit performs the parallel check one level higher: for
each right-origin class on bounded small actual-CM rows, it builds the full
square coordinate matrix representing `Phi_t`, groups the determinants by
right Frobenius orbit, and verifies

    det(block_cycle(Phi_t : t in O))
      = (-1)^(d*(|O|-1)) * product_{t in O} det(Phi_t).

For p24, `d=156` and `|O|=35`, so the sign is positive.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from types import SimpleNamespace

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import lang_inverse_for_orbit
from lang_arc_strength_audit import transformed_blocks_for_row
from lang_trace_gcd_block_cycle_norm_audit import (
    block_cycle_matrix,
    class_representatives,
    det_mod,
    frobenius_orbits,
    product_mod,
    rank_mod,
)
from lang_trace_gcd_origin_action_audit import crt_alpha_beta
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import rotate
from trace_gcd_prefix_adjoint_trace_toy import coordinate_vector
from trace_gcd_two_resultant_holdout_audit import CASES, Case, case_args


@dataclass(frozen=True)
class SquareCoinvariantRecord:
    shift: int
    alpha: int
    beta: int
    omitted: int
    determinant: int | None
    matrix: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class SquareCoinvariantRow:
    label: str
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
    records: tuple[SquareCoinvariantRecord, ...]


def transpose(columns: list[list[int]]) -> list[list[int]]:
    if not columns:
        return []
    return [
        [columns[col][row] for col in range(len(columns))]
        for row in range(len(columns[0]))
    ]


def square_coinvariant_matrix(
    blocks,
    omitted: int,
    left_len: int,
    field,
    basis_inverse,
) -> list[list[int]] | None:
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    values = [value for block in kept for value in block]
    if len(values) < left_len:
        return None
    coords = values[:left_len]
    columns = [
        coordinate_vector(coord, left_len, basis_inverse, field)
        for coord in coords
    ]
    return transpose(columns)


def records_by_omitted(
    records: tuple[SquareCoinvariantRecord, ...],
) -> dict[int, list[SquareCoinvariantRecord]]:
    out: dict[int, list[SquareCoinvariantRecord]] = {}
    for record in records:
        out.setdefault(record.omitted, []).append(record)
    return dict(sorted(out.items()))


def audit_square_row(
    label: str,
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    args: SimpleNamespace,
) -> SquareCoinvariantRow | None:
    h = len(cycle)
    n = h // m
    records: list[SquareCoinvariantRecord] = []
    right_lengths: tuple[int, ...] | None = None
    extension_degree: int | None = None
    max_shift = h if args.max_origin_shifts is None else min(h, args.max_origin_shifts)
    basis_inverses = {}
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
        left_len = len(left_orbit)
        if left_len not in basis_inverses:
            basis_inverses[left_len] = lang_inverse_for_orbit(
                q,
                left_len,
                field,
                args.seed + 157,
            )
        for omitted in range(len(blocks)):
            if args.only_omitted is not None and omitted != args.only_omitted:
                continue
            matrix = square_coinvariant_matrix(
                blocks,
                omitted,
                left_len,
                field,
                basis_inverses[left_len],
            )
            if matrix is None:
                continue
            determinant = det_mod(matrix, q)
            alpha, beta = crt_alpha_beta(shift, m, n)
            records.append(
                SquareCoinvariantRecord(
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
    return SquareCoinvariantRow(
        label=label,
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


def first_square_row(case: Case) -> SquareCoinvariantRow | None:
    args = case_args(case)
    pari = Pari()
    pari.allocatemem(args.pari_stack_mb * 1024 * 1024)
    hilbert = pari.polclass(case.D)
    h = int(pari.poldegree(hilbert))
    roots = [int(root) for root in pari.polrootsmod(hilbert, case.q)]
    full = find_full_cycle_prime(roots, case.D, case.q)
    if full is None:
        return None
    ell, cycle = full
    n = h // case.m
    for factor in packet_factors(n, case.q):
        if factor.degree() == 1 and not args.include_linear:
            continue
        if factor.degree() < args.min_factor_degree:
            continue
        if factor.degree() > args.max_factor_degree:
            continue
        if gcd(case.m, n) != 1:
            continue
        extension_degree = int(sp.n_order(case.q % case.m, case.m))
        if extension_degree > args.max_extension_degree:
            continue
        for left_orbit in q_orbits(case.left, case.q):
            if len(left_orbit) < args.min_left_orbit_len:
                continue
            row = audit_square_row(
                case.label,
                case.D,
                case.q,
                ell,
                cycle,
                case.m,
                factor,
                case.left,
                case.right,
                left_orbit,
                args,
            )
            if row is not None:
                return row
    return None


def main() -> None:
    rows = [row for case in CASES if (row := first_square_row(case)) is not None]
    print("Trace-GCD actual-CM square coinvariant block-cycle audit")
    print("p24_target=skew_reduced_norm_of_transported_square_coinvariant_maps")
    print("p24_square_dim=156")
    print("p24_nonzero_orbit_len=35")
    print("p24_block_cycle_sign_positive=1")
    failures = 0
    orbit_tests = 0
    nonzero_orbit_tests = 0
    block_cycle_matches = 0
    full_rank_detection_matches = 0
    full_rank_orbits = 0
    singular_orbits = 0

    for row in rows:
        orbits = frobenius_orbits(row.right, row.q % row.right)
        print(f"case={row.label}")
        print(f"  D={row.D}")
        print(f"  q={row.q}")
        print(f"  h={row.h}")
        print(f"  m={row.m}")
        print(f"  n={row.n}")
        print(f"  factor_degree={row.factor_degree}")
        print(f"  extension_degree={row.extension_degree}")
        print(f"  pair=({row.left},{row.right})")
        print(f"  left_orbit_rep={row.left_orbit_rep}")
        print(f"  left_orbit_len={row.left_orbit_len}")
        print(f"  right_orbit_lengths={list(row.right_orbit_lengths)}")
        print(f"  frobenius_orbits={orbits}")
        for omitted, records in records_by_omitted(row.records).items():
            reps, det_mismatches = class_representatives(records, row.right)
            if det_mismatches:
                failures += 1
            block_size = len(reps[0].matrix)
            print(f"  omitted={omitted}")
            print(f"    right_class_det_mismatches={det_mismatches}")
            print(f"    block_size={block_size}")
            print(f"    determinants={[record.determinant for record in reps]}")
            for orbit_index, orbit in enumerate(orbits):
                orbit_records = [reps[index] for index in orbit]
                matrices = [record.matrix for record in orbit_records]
                dets = [int(record.determinant) for record in orbit_records]
                local_singular_count = sum(det == 0 for det in dets)
                product = product_mod(dets, row.q)
                block_matrix = block_cycle_matrix(matrices, row.q)
                block_det = det_mod(block_matrix, row.q)
                block_rank = rank_mod(block_matrix, row.q)
                block_dim = len(block_matrix)
                sign = 1 if (block_size * (len(orbit) - 1)) % 2 == 0 else -1
                signed_product = product if sign == 1 else (-product) % row.q
                match = block_det == signed_product
                full_rank_match = (block_rank == block_dim) == (local_singular_count == 0)
                orbit_tests += 1
                nonzero_orbit_tests += int(orbit[0] != 0)
                block_cycle_matches += int(match)
                full_rank_detection_matches += int(full_rank_match)
                full_rank_orbits += int(block_rank == block_dim)
                singular_orbits += int(block_rank != block_dim)
                failures += int(not match or not full_rank_match)
                print(
                    f"    orbit={orbit_index} rep={orbit[0]} len={len(orbit)} "
                    f"block_cycle_dim={block_dim}"
                )
                print(f"      dets={dets}")
                print(f"      local_singular_count={local_singular_count}")
                print(f"      product={product}")
                print(f"      sign={sign}")
                print(f"      signed_product={signed_product}")
                print(f"      block_cycle_det={block_det}")
                print(f"      block_cycle_rank={block_rank}/{block_dim}")
                print(f"      block_cycle_match={int(match)}")
                print(
                    "      block_cycle_full_rank_iff_no_local_singular="
                    f"{int(full_rank_match)}"
                )
                print(f"      orbit_norm_nonzero={int(product != 0)}")

    print("totals")
    print(f"  cases={len(rows)}")
    print(f"  orbit_tests={orbit_tests}")
    print(f"  nonzero_orbit_tests={nonzero_orbit_tests}")
    print(f"  block_cycle_matches={block_cycle_matches}/{orbit_tests}")
    print(
        "  block_cycle_full_rank_detection_matches="
        f"{full_rank_detection_matches}/{orbit_tests}"
    )
    print(f"  full_rank_orbits={full_rank_orbits}/{orbit_tests}")
    print(f"  singular_control_orbits={singular_orbits}/{orbit_tests}")
    print("interpretation")
    print("  square_coinvariant_block_cycle_is_skew_reduced_norm=1")
    print("  nonzero_side_can_target_transported_square_coinvariant_maps=1")
    print("  p24_still_needs_punit_theorem_for_the_actual_skew_norm=1")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_actual_cm_square_coinvariant_block_cycle_audit")
    if failures or not rows or not full_rank_orbits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
