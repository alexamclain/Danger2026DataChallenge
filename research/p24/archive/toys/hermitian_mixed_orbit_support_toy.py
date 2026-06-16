#!/usr/bin/env python3
"""Toy tests for right-orbit support and Frobenius-stability candidates.

This script uses the same random mixed-DFT toy as the trace-dual audits.  It
tests two stronger theorem candidates that are cheap to falsify at small
scale:

1. delete-one right-orbit rank:
   any all-but-one set of right orbit packets still spans the left field;

2. right-orbit trace support:
   every nonzero lambda in L has at least two nonzero right-orbit traces.

It also records whether the transformed coordinate span U is Frobenius-stable.
These are not p24 evidence; they are theorem-shape filters.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass
from math import gcd

import sympy as sp

from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_dual_trace_injectivity_toy import (
    left_basis_for_orbit,
    relative_trace_to_right,
    transformed_coordinates,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class SupportTrial:
    trial: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len: int
    full_rank: int
    min_delete_one_rank: int
    delete_one_full_count: int
    min_delete_one_leading_rank: int
    delete_one_leading_full_count: int
    min_lambda_support: int
    lambda_zero_support_count: int
    lambda_one_support_count: int
    stability_defect: int


def random_base_table(left: int, right: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(right)] for _ in range(left)]


def linear_combination(coeffs: tuple[int, ...], basis: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for coeff, value in zip(coeffs, basis):
        total = field.add(total, field.scalar_mul(coeff, value))
    return total


def support_counts_for_left_orbit(
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    q: int,
    field: ExtensionField,
    seed: int,
    rng: random.Random,
    lambda_samples: int,
) -> tuple[int, int, int]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    left_basis = left_basis_for_orbit(q, len(left_orbit), field, seed)
    seed_values = [
        dft_matrix[row_index[left_orbit[0]]][col_index[right_orbit[0]]]
        for right_orbit in right_orbits
    ]
    min_support = len(seed_values)
    zero_support = 0
    one_support = 0
    if lambda_samples:
        coeff_iter = (
            tuple(rng.randrange(q) for _ in left_basis)
            for _ in range(lambda_samples)
        )
    else:
        coeff_iter = itertools.product(range(q), repeat=len(left_basis))
    for coeffs in coeff_iter:
        if all(coeff == 0 for coeff in coeffs):
            continue
        lam = linear_combination(coeffs, left_basis, field)
        support = 0
        for seed_value in seed_values:
            trace_value = relative_trace_to_right(
                field.mul(lam, seed_value),
                len(left_orbit),
                len(right_orbits[0]),
                field,
            )
            if trace_value != field.zero:
                support += 1
        min_support = min(min_support, support)
        if support == 0:
            zero_support += 1
        if support == 1:
            one_support += 1
    return min_support, zero_support, one_support


def audit_trial(
    trial: int,
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
    powers,
    seed: int,
    rng: random.Random,
    lambda_samples: int,
) -> list[SupportTrial]:
    table = random_base_table(left, right, q, rng)
    dft_matrix = dft_double_marginal(table, left, right, powers, left * right, field)
    right_orbits = q_orbits(right, q)
    out: list[SupportTrial] = []
    for left_orbit in q_orbits(left, q):
        transformed = transformed_coordinates(
            dft_matrix, left, right, left_orbit, right_orbits, q, field, seed
        )
        full_rank = fq_rank(transformed, q)
        delete_ranks: list[int] = []
        delete_leading_ranks: list[int] = []
        for omitted in range(len(right_orbits)):
            kept = [
                right_orbit
                for index, right_orbit in enumerate(right_orbits)
                if index != omitted
            ]
            subset_transformed = transformed_coordinates(
                dft_matrix, left, right, left_orbit, kept, q, field, seed
            )
            delete_ranks.append(fq_rank(subset_transformed, q))
            delete_leading_ranks.append(
                fq_rank(subset_transformed[: len(left_orbit)], q)
            )
        frob_transformed = [field.pow(value, field.q) for value in transformed]
        stability_defect = fq_rank(transformed + frob_transformed, q) - full_rank
        min_support, zero_support, one_support = support_counts_for_left_orbit(
            dft_matrix,
            left,
            right,
            left_orbit,
            right_orbits,
            q,
            field,
            seed,
            rng,
            lambda_samples,
        )
        out.append(
            SupportTrial(
                trial=trial,
                left_orbit_rep=left_orbit[0],
                left_orbit_len=len(left_orbit),
                right_orbit_count=len(right_orbits),
                right_orbit_len=len(right_orbits[0]) if right_orbits else 0,
                full_rank=full_rank,
                min_delete_one_rank=min(delete_ranks) if delete_ranks else full_rank,
                delete_one_full_count=sum(
                    1 for rank in delete_ranks if rank >= len(left_orbit)
                ),
                min_delete_one_leading_rank=(
                    min(delete_leading_ranks) if delete_leading_ranks else full_rank
                ),
                delete_one_leading_full_count=sum(
                    1 for rank in delete_leading_ranks if rank >= len(left_orbit)
                ),
                min_lambda_support=min_support,
                lambda_zero_support_count=zero_support,
                lambda_one_support_count=one_support,
                stability_defect=stability_defect,
            )
        )
    return out


def format_trial(row: SupportTrial) -> str:
    return (
        f"trial={row.trial} left_rep={row.left_orbit_rep} "
        f"L={row.left_orbit_len} right_orbits={row.right_orbit_count} "
        f"R={row.right_orbit_len} full_rank={row.full_rank} "
        f"min_delete_one_rank={row.min_delete_one_rank} "
        f"delete_one_full={row.delete_one_full_count}/{row.right_orbit_count} "
        f"min_delete_one_leading_rank={row.min_delete_one_leading_rank} "
        f"delete_one_leading_full="
        f"{row.delete_one_leading_full_count}/{row.right_orbit_count} "
        f"min_support={row.min_lambda_support} "
        f"zero_support={row.lambda_zero_support_count} "
        f"one_support={row.lambda_one_support_count} "
        f"stability_defect={row.stability_defect}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left", type=int, default=7)
    parser.add_argument("--right", type=int, default=31)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument(
        "--lambda-samples",
        type=int,
        default=0,
        help="sample this many nonzero lambda candidates instead of exhaustive enumeration",
    )
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    left_degree = int(sp.n_order(args.q % args.left, args.left))
    right_degree = int(sp.n_order(args.q % args.right, args.right))
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("toy expects coprime left/right orbit degrees")
    extension_degree = int(sp.ilcm(left_degree, right_degree))
    modulus = find_irreducible_modulus(args.q, extension_degree, args.seed)
    field = ExtensionField(args.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, args.left * args.right, args.seed)
    powers = zeta_powers(zeta, args.left * args.right, field)
    rng = random.Random(args.seed)

    rows: list[SupportTrial] = []
    for trial in range(args.trials):
        rows.extend(
            audit_trial(
                trial,
                args.left,
                args.right,
                args.q,
                field,
                powers,
                args.seed,
                rng,
                args.lambda_samples,
            )
        )

    full_rows = [row for row in rows if row.full_rank >= row.left_orbit_len]
    delete_full_rows = [
        row for row in rows if row.min_delete_one_rank >= row.left_orbit_len
    ]
    delete_leading_full_rows = [
        row for row in rows
        if row.delete_one_leading_full_count == row.right_orbit_count
    ]
    support_zero = [row for row in rows if row.lambda_zero_support_count]
    support_one = [row for row in rows if row.lambda_one_support_count]
    stable = [row for row in rows if row.stability_defect == 0]

    print("Hermitian mixed orbit-support toy")
    print(f"q={args.q}")
    print(f"left={args.left} ord_left={left_degree}")
    print(f"right={args.right} ord_right={right_degree}")
    print(f"right_orbits={(args.right - 1) // right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"trials={args.trials}")
    print(f"lambda_samples={args.lambda_samples}")
    print()
    if not args.summary_only:
        for row in rows[:80]:
            print(format_trial(row))
    print()
    print("summary")
    print(f"  support_tests={len(rows)}")
    print(f"  full_rank_tests={len(full_rows)}")
    print(f"  delete_one_full_rank_tests={len(delete_full_rows)}")
    print(f"  delete_one_leading_full_rank_tests={len(delete_leading_full_rows)}")
    print(f"  zero_support_failures={len(support_zero)}")
    print(f"  one_support_strong_failures={len(support_one)}")
    print(f"  frobenius_stable_tests={len(stable)}")
    if rows:
        print(f"  min_lambda_support={min(row.min_lambda_support for row in rows)}")
        print(
            "  min_delete_one_leading_rank="
            f"{min(row.min_delete_one_leading_rank for row in rows)}"
        )
        print(f"  max_stability_defect={max(row.stability_defect for row in rows)}")
    print()
    print("interpretation")
    print("  original_dual_injectivity_holds_when_zero_support_failures_is_0=1")
    print("  delete_one_strong_theorem_survives_when_one_support_failures_is_0=1")
    print("  leading_delete_one_prefix_full_is_stronger_than_delete_one_rank=1")
    print("  frobenius_stability_is_extra_not_forced_by_random_model=1")
    print("conclusion=reported_hermitian_mixed_orbit_support_toy")


if __name__ == "__main__":
    main()
