#!/usr/bin/env python3
"""Toy gate for the nonzero-orbit crossed coinvariant norm.

The fixed p24 resultant can be targeted by one square coinvariant map

    Phi_full : R^4 + C_tail -> E/(tau_R - 1)E.

For a nonzero right Frobenius orbit the analogous object is not an ordinary
base polynomial.  It is the crossed/block-cycle norm of the transported
square maps Phi_t.  This toy builds tiny finite-extension coinvariant maps,
packages them into a block-cycle operator, and checks:

    det(block_cycle(Phi_t)) = signed product_t det(Phi_t),

with controls where one local coinvariant map is forced singular.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

from block_cycle_fitting_zero_detection_toy import block_cycle_matrix, det_mod
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from trace_gcd_full_coinvariant_tail_toy import (
    adjoint_rows,
    audit_tuple,
    find_good_row,
    tail_basis_slice,
)
from trace_gcd_prefix_adjoint_trace_toy import random_element
from trace_gcd_prefix_hilbert90_toy import (
    coboundary_rows,
    coboundary_trace_failures,
)


@dataclass(frozen=True)
class LocalMap:
    label: str
    determinant: int
    coinvariant_full: bool
    primal_full: bool
    matrix: list[list[int]]


@dataclass(frozen=True)
class CycleRow:
    label: str
    local_dets: tuple[int, ...]
    local_full_count: int
    block_det: int
    expected_det: int
    determinant_match: bool
    zero_detection: bool
    full_rank_detection: bool


def build_local_map(
    label: str,
    prefix_seeds: list[FpE],
    tail_seed: FpE,
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_basis: list[FpE],
    left_inverse: list[list[FpE]],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
    cob_rows: list[list[int]],
) -> LocalMap:
    row = audit_tuple(
        label,
        prefix_seeds,
        tail_seed,
        left_basis,
        right_basis,
        tail_basis,
        left_inverse,
        left_degree,
        right_degree,
        field,
        cob_rows,
    )
    matrix = adjoint_rows(
        prefix_seeds,
        tail_seed,
        right_basis,
        tail_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    determinant = det_mod(matrix, field.q)
    if row.coinvariant_full != (determinant != 0):
        raise AssertionError("coinvariant full-rank event does not match determinant")
    if row.primal_full != row.coinvariant_full:
        raise AssertionError("trace-GCD primal full event does not match coinvariant event")
    return LocalMap(
        label=label,
        determinant=determinant,
        coinvariant_full=row.coinvariant_full,
        primal_full=row.primal_full,
        matrix=matrix,
    )


def build_good_local_map(
    label: str,
    args: argparse.Namespace,
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_basis: list[FpE],
    left_inverse: list[list[FpE]],
    field: ExtensionField,
    cob_rows: list[list[int]],
    rng: random.Random,
) -> LocalMap:
    good = find_good_row(
        args.k,
        left_basis,
        right_basis,
        tail_basis,
        left_inverse,
        args.left_degree,
        args.right_degree,
        field,
        cob_rows,
        rng,
        attempts=args.good_attempts,
    )
    if good is None:
        raise RuntimeError("failed to find a full-rank local coinvariant map")
    return build_local_map(
        label,
        good[0],
        good[1],
        right_basis,
        tail_basis,
        left_basis,
        left_inverse,
        args.left_degree,
        args.right_degree,
        field,
        cob_rows,
    )


def build_forced_singular_local_map(
    label: str,
    args: argparse.Namespace,
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_basis: list[FpE],
    left_inverse: list[list[FpE]],
    field: ExtensionField,
    cob_rows: list[list[int]],
    rng: random.Random,
) -> LocalMap:
    repeated = random_element(field, rng)
    prefix = [repeated] + [random_element(field, rng) for _ in range(args.k - 1)]
    return build_local_map(
        label,
        prefix,
        repeated,
        right_basis,
        tail_basis,
        left_basis,
        left_inverse,
        args.left_degree,
        args.right_degree,
        field,
        cob_rows,
    )


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def audit_cycle(label: str, maps: list[LocalMap], q: int) -> CycleRow:
    matrices = [local.matrix for local in maps]
    block = block_cycle_matrix(matrices, q)
    block_det = det_mod(block, q)
    source_dim = len(matrices[0])
    orbit_len = len(matrices)
    sign = 1 if (source_dim * (orbit_len - 1)) % 2 == 0 else -1
    expected = product([local.determinant for local in maps], q)
    if sign < 0:
        expected = (-expected) % q
    all_local_full = all(local.coinvariant_full for local in maps)
    return CycleRow(
        label=label,
        local_dets=tuple(local.determinant for local in maps),
        local_full_count=sum(local.coinvariant_full for local in maps),
        block_det=block_det,
        expected_det=expected,
        determinant_match=block_det == expected,
        zero_detection=(any(det == 0 for det in (local.determinant for local in maps)) == (block_det == 0)),
        full_rank_detection=all_local_full == (block_det != 0),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--left-degree", type=int, default=5)
    parser.add_argument("--right-degree", type=int, default=2)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--orbit-len", type=int, default=3)
    parser.add_argument("--random-cycles", type=int, default=12)
    parser.add_argument("--good-attempts", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if gcd(args.left_degree, args.right_degree) != 1:
        raise ValueError("left and right degrees must be coprime")
    tail_dim = args.left_degree - args.k * args.right_degree
    if not (0 < tail_dim <= args.right_degree):
        raise ValueError("toy expects 0 < left_degree-k*right_degree <= right_degree")

    extension_degree = args.left_degree * args.right_degree
    field = ExtensionField(
        args.q,
        extension_degree,
        find_irreducible_modulus(args.q, extension_degree, args.seed),
    )
    rng = random.Random(args.seed)
    left_seed = args.seed + 17
    right_seed = args.seed + 29
    left_basis = subfield_power_basis(args.q, args.left_degree, field, left_seed)
    right_basis = subfield_power_basis(args.q, args.right_degree, field, right_seed)
    left_inverse = lang_inverse_for_orbit(args.q, args.left_degree, field, left_seed)
    tail_basis = tail_basis_slice(right_basis, tail_dim)
    cob_rows = coboundary_rows(args.left_degree, args.right_degree, field)
    cob_failures = coboundary_trace_failures(
        cob_rows,
        args.left_degree,
        args.right_degree,
        field,
    )

    rows: list[CycleRow] = []
    good_cycle = [
        build_good_local_map(
            f"good_{i}",
            args,
            right_basis,
            tail_basis,
            left_basis,
            left_inverse,
            field,
            cob_rows,
            rng,
        )
        for i in range(args.orbit_len)
    ]
    rows.append(audit_cycle("all_full_coinvariant_cycle", good_cycle, args.q))

    singular_cycle = list(good_cycle)
    singular_cycle[args.orbit_len // 2] = build_forced_singular_local_map(
        "forced_tail_inside_prefix_span",
        args,
        right_basis,
        tail_basis,
        left_basis,
        left_inverse,
        field,
        cob_rows,
        rng,
    )
    rows.append(audit_cycle("forced_singular_coinvariant_cycle", singular_cycle, args.q))

    for cycle_index in range(args.random_cycles):
        maps = []
        for local_index in range(args.orbit_len):
            if (cycle_index + local_index) % 5 == 0:
                maps.append(
                    build_forced_singular_local_map(
                        f"random_{cycle_index}_{local_index}_forced",
                        args,
                        right_basis,
                        tail_basis,
                        left_basis,
                        left_inverse,
                        field,
                        cob_rows,
                        rng,
                    )
                )
            else:
                maps.append(
                    build_good_local_map(
                        f"random_{cycle_index}_{local_index}_good",
                        args,
                        right_basis,
                        tail_basis,
                        left_basis,
                        left_inverse,
                        field,
                        cob_rows,
                        rng,
                    )
                )
        rows.append(audit_cycle(f"random_cycle_{cycle_index}", maps, args.q))

    print("Trace-GCD crossed coinvariant norm toy")
    print(f"q={args.q}")
    print(f"left_degree={args.left_degree}")
    print(f"right_degree={args.right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"tail_dim={tail_dim}")
    print(f"orbit_len={args.orbit_len}")
    print(f"source_dim={args.k * args.right_degree + tail_dim}")
    print(f"p24_sign_positive={int((156 * (35 - 1)) % 2 == 0)}")
    print("columns: label local_full block_det expected determinant_match zero_detection full_rank_detection local_dets")
    for row in rows:
        print(
            f"row label={row.label} local_full={row.local_full_count}/{args.orbit_len} "
            f"block_det={row.block_det} expected={row.expected_det} "
            f"determinant_match={int(row.determinant_match)} "
            f"zero_detection={int(row.zero_detection)} "
            f"full_rank_detection={int(row.full_rank_detection)} "
            f"local_dets={list(row.local_dets)}"
        )
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  coboundary_trace_failures={cob_failures}")
    print(f"  determinant_mismatches={sum(not row.determinant_match for row in rows)}")
    print(f"  zero_detection_failures={sum(not row.zero_detection for row in rows)}")
    print(f"  full_rank_detection_failures={sum(not row.full_rank_detection for row in rows)}")
    print(
        "  found_all_full_coinvariant_cycle="
        f"{int(any(row.label == 'all_full_coinvariant_cycle' and row.block_det != 0 for row in rows))}"
    )
    print(
        "  forced_singular_coinvariant_cycle_detected="
        f"{int(any(row.label == 'forced_singular_coinvariant_cycle' and row.block_det == 0 for row in rows))}"
    )
    print("interpretation")
    print("  crossed_norm_of_square_coinvariant_maps_detects_any_local_singularity=1")
    print("  p24_nonzero_resultant_can_be_targeted_as_crossed_coinvariant_norm=1")
    print("conclusion=reported_trace_gcd_crossed_coinvariant_norm_toy")
    if (
        cob_failures
        or any(not row.determinant_match for row in rows)
        or any(not row.zero_detection for row in rows)
        or any(not row.full_rank_detection for row in rows)
        or not any(row.label == "all_full_coinvariant_cycle" and row.block_det != 0 for row in rows)
        or not any(row.label == "forced_singular_coinvariant_cycle" and row.block_det == 0 for row in rows)
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
