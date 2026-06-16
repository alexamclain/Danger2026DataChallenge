#!/usr/bin/env python3
"""Toy gate for the full prefix-plus-tail coinvariant target.

The prefix Hilbert-90 target uses the injective coinvariant map

    R^k -> E/(tau_R - 1)E.

For the fixed p24 trace-GCD resultant, the tail can be folded into the same
class-field object.  If C is the selected tail-coordinate subspace of R, the
square target is

    R^k + C -> E/(tau_R - 1)E,
    (y_j, z) -> [sum_j y_j*S_j + z*S_tail].

In p24, k=4, dim R=35, dim C=16, and dim L=156, so this is square.  This toy
checks the finite duality:

    full trace-GCD map on L is injective
      iff the trace-adjoint R^k + C -> L is surjective
      iff the coinvariant map R^k + C -> E/(tau_R-1)E has full rank.

The arithmetic p24 work is proving this for the actual CM periods, not
finding it by random search.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_adjoint_trace_toy import (
    coordinate_vector,
    random_element,
    relative_trace_to_left,
    relative_trace_to_right,
    trace_to_base,
)
from trace_gcd_prefix_hilbert90_toy import (
    coboundary_rows,
    coboundary_trace_failures,
    row_span_intersection_dim,
    standard_basis,
)


@dataclass(frozen=True)
class FullCoinvariantRow:
    label: str
    source_dim: int
    primal_rank: int
    adjoint_rank: int
    phi_rank: int
    coinvariant_rank: int
    coboundary_intersection_dim: int
    primal_full: bool
    adjoint_full: bool
    coinvariant_full: bool
    duality_match: bool
    coinvariant_match: bool


def tail_basis_slice(right_basis: list[FpE], tail_dim: int) -> list[FpE]:
    return right_basis[:tail_dim]


def phi_rows(
    prefix_seeds: list[FpE],
    tail_seed: FpE,
    right_basis: list[FpE],
    tail_basis: list[FpE],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in prefix_seeds:
        for y in right_basis:
            rows.append(list(field.mul(y, seed)))
    for y in tail_basis:
        rows.append(list(field.mul(y, tail_seed)))
    return rows


def adjoint_rows(
    prefix_seeds: list[FpE],
    tail_seed: FpE,
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in prefix_seeds:
        for y in right_basis:
            trace_value = relative_trace_to_left(
                field.mul(y, seed),
                left_degree,
                right_degree,
                field,
            )
            rows.append(coordinate_vector(trace_value, left_degree, left_inverse, field))
    for y in tail_basis:
        trace_value = relative_trace_to_left(
            field.mul(y, tail_seed),
            left_degree,
            right_degree,
            field,
        )
        rows.append(coordinate_vector(trace_value, left_degree, left_inverse, field))
    return rows


def primal_rows(
    prefix_seeds: list[FpE],
    tail_seed: FpE,
    left_basis: list[FpE],
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for lam in left_basis:
        row: list[int] = []
        for seed in prefix_seeds:
            trace_value = relative_trace_to_right(
                field.mul(lam, seed),
                left_degree,
                right_degree,
                field,
            )
            for y in right_basis:
                row.append(trace_to_base(field.mul(y, trace_value), right_degree, field))
        tail_trace = relative_trace_to_right(
            field.mul(lam, tail_seed),
            left_degree,
            right_degree,
            field,
        )
        for y in tail_basis:
            row.append(trace_to_base(field.mul(y, tail_trace), right_degree, field))
        rows.append(row)
    return rows


def audit_tuple(
    label: str,
    prefix_seeds: list[FpE],
    tail_seed: FpE,
    left_basis: list[FpE],
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_inverse: list[list[FpE]],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
    cob_rows: list[list[int]],
) -> FullCoinvariantRow:
    source_dim = len(prefix_seeds) * right_degree + len(tail_basis)
    prows = primal_rows(
        prefix_seeds,
        tail_seed,
        left_basis,
        right_basis,
        tail_basis,
        left_degree,
        right_degree,
        field,
    )
    arows = adjoint_rows(
        prefix_seeds,
        tail_seed,
        right_basis,
        tail_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    phrows = phi_rows(prefix_seeds, tail_seed, right_basis, tail_basis, field)
    primal_rank = rank_mod_q(prows, field.q)
    adjoint_rank = rank_mod_q(arows, field.q)
    phi_rank = rank_mod_q(phrows, field.q)
    intersection = row_span_intersection_dim(phrows, cob_rows, field.q)
    coinvariant_rank = phi_rank - intersection
    primal_full = primal_rank == left_degree
    adjoint_full = adjoint_rank == left_degree
    coinvariant_full = coinvariant_rank == left_degree
    return FullCoinvariantRow(
        label=label,
        source_dim=source_dim,
        primal_rank=primal_rank,
        adjoint_rank=adjoint_rank,
        phi_rank=phi_rank,
        coinvariant_rank=coinvariant_rank,
        coboundary_intersection_dim=intersection,
        primal_full=primal_full,
        adjoint_full=adjoint_full,
        coinvariant_full=coinvariant_full,
        duality_match=primal_full == adjoint_full,
        coinvariant_match=adjoint_full == coinvariant_full,
    )


def find_good_row(
    k: int,
    left_basis: list[FpE],
    right_basis: list[FpE],
    tail_basis: list[FpE],
    left_inverse: list[list[FpE]],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
    cob_rows: list[list[int]],
    rng: random.Random,
    attempts: int,
) -> tuple[list[FpE], FpE] | None:
    for _ in range(attempts):
        prefix = [random_element(field, rng) for _ in range(k)]
        tail = random_element(field, rng)
        row = audit_tuple(
            "candidate",
            prefix,
            tail,
            left_basis,
            right_basis,
            tail_basis,
            left_inverse,
            left_degree,
            right_degree,
            field,
            cob_rows,
        )
        if row.primal_full and row.coinvariant_full:
            return prefix, tail
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left-degree", type=int, default=5)
    parser.add_argument("--right-degree", type=int, default=2)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--trials", type=int, default=100)
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
    rng = random.Random(args.seed)

    rows: list[FullCoinvariantRow] = []
    zero_prefix = [field.zero for _ in range(args.k)]
    rows.append(
        audit_tuple(
            "forced_zero",
            zero_prefix,
            field.zero,
            left_basis,
            right_basis,
            tail_basis,
            left_inverse,
            args.left_degree,
            args.right_degree,
            field,
            cob_rows,
        )
    )

    repeated = random_element(field, rng)
    rows.append(
        audit_tuple(
            "forced_tail_inside_prefix_span",
            [repeated] + [random_element(field, rng) for _ in range(args.k - 1)],
            repeated,
            left_basis,
            right_basis,
            tail_basis,
            left_inverse,
            args.left_degree,
            args.right_degree,
            field,
            cob_rows,
        )
    )

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
        attempts=4000,
    )
    if good is not None:
        rows.append(
            audit_tuple(
                "found_full_coinvariant_unit",
                good[0],
                good[1],
                left_basis,
                right_basis,
                tail_basis,
                left_inverse,
                args.left_degree,
                args.right_degree,
                field,
                cob_rows,
            )
        )

    for trial in range(args.trials):
        rows.append(
            audit_tuple(
                f"random_{trial}",
                [random_element(field, rng) for _ in range(args.k)],
                random_element(field, rng),
                left_basis,
                right_basis,
                tail_basis,
                left_inverse,
                args.left_degree,
                args.right_degree,
                field,
                cob_rows,
            )
        )

    print("Trace-GCD full coinvariant tail toy")
    print(f"q={args.q}")
    print(f"left_degree={args.left_degree}")
    print(f"right_degree={args.right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"tail_dim={tail_dim}")
    print(f"source_dim={args.k * args.right_degree + tail_dim}")
    print("columns: label primal_rank adjoint_rank phi_rank coinv_rank intersection primal_full adjoint_full coinv_full duality_match coinv_match")
    for row in rows[:24]:
        print(
            f"row label={row.label} primal_rank={row.primal_rank} "
            f"adjoint_rank={row.adjoint_rank} phi_rank={row.phi_rank} "
            f"coinv_rank={row.coinvariant_rank} "
            f"intersection={row.coboundary_intersection_dim} "
            f"primal_full={int(row.primal_full)} "
            f"adjoint_full={int(row.adjoint_full)} "
            f"coinv_full={int(row.coinvariant_full)} "
            f"duality_match={int(row.duality_match)} "
            f"coinv_match={int(row.coinvariant_match)}"
        )
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  coboundary_rank={rank_mod_q(cob_rows, args.q)}")
    print(f"  coboundary_trace_failures={cob_failures}")
    print(f"  duality_mismatches={sum(not row.duality_match for row in rows)}")
    print(f"  coinvariant_mismatches={sum(not row.coinvariant_match for row in rows)}")
    print(
        "  found_full_coinvariant_unit="
        f"{int(any(row.label == 'found_full_coinvariant_unit' and row.coinvariant_full for row in rows))}"
    )
    print(
        "  forced_tail_inside_prefix_span_detected="
        f"{int(any(row.label == 'forced_tail_inside_prefix_span' and not row.coinvariant_full for row in rows))}"
    )
    print("interpretation")
    print("  full_prefix_tail_trace_gcd_injective_iff_square_coinvariant_unit=1")
    print("  p24_fixed_resultant_can_be_targeted_as_R4_plus_C_to_coinvariants=1")
    print("conclusion=reported_trace_gcd_full_coinvariant_tail_toy")
    if (
        cob_failures
        or any(not row.duality_match for row in rows)
        or any(not row.coinvariant_match for row in rows)
        or not any(row.label == "found_full_coinvariant_unit" and row.coinvariant_full for row in rows)
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
