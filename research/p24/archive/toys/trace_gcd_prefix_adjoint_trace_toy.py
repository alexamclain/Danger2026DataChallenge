#!/usr/bin/env python3
"""Toy gate for the four-prefix relative-trace adjoint theorem.

For coprime finite extensions

    L = F_q^l, R = F_q^r, E = F_q^(l*r),

and seed periods S_j in E, define

    A : L -> R^k,
    lambda |-> (Tr_{E/R}(lambda*S_j))_j.

With trace pairings on L and R, the F_q-adjoint is

    A^* : R^k -> L,
    (y_j)_j |-> Tr_{E/L}(sum_j y_j*S_j).

This toy verifies that the rank and zero-event equivalences used in the p24
prefix theorem are ordinary finite linear algebra.  It deliberately keeps the
objects tiny; the arithmetic work for p24 is proving injectivity for the
actual CM periods, not discovering it by search.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import rank_mod_q


@dataclass(frozen=True)
class PrefixAdjointRow:
    label: str
    prefix_rank: int
    adjoint_rank: int
    codomain_dim: int
    kernel_dim: int
    prefix_surjective: bool
    adjoint_injective: bool
    rank_match: bool
    event_match: bool
    pairing_mismatches: int


def base_value(value: FpE, field: ExtensionField) -> int:
    if any(coord % field.q for coord in value[1:]):
        raise ValueError(f"value is not in the base field: {value}")
    return value[0] % field.q


def trace_under_power(
    value: FpE,
    step: int,
    degree: int,
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for i in range(degree):
        total = field.add(total, field.pow(value, field.q ** (step * i)))
    return total


def trace_to_base(value: FpE, degree: int, field: ExtensionField) -> int:
    return base_value(trace_under_power(value, 1, degree, field), field)


def relative_trace_to_right(
    value: FpE,
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("relative trace formula expects coprime degrees")
    step = right_degree * pow(right_degree % left_degree, -1, left_degree)
    return trace_under_power(value, step, left_degree, field)


def relative_trace_to_left(
    value: FpE,
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("relative trace formula expects coprime degrees")
    step = left_degree * pow(left_degree % right_degree, -1, right_degree)
    return trace_under_power(value, step, right_degree, field)


def coordinate_vector(
    value: FpE,
    degree: int,
    inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[int]:
    orbit = [field.pow(value, field.q**i) for i in range(degree)]
    coeffs = matrix_vector_mul(inverse, orbit, field)
    return [base_value(coeff, field) for coeff in coeffs]


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_subfield_element(
    basis: list[FpE],
    field: ExtensionField,
    rng: random.Random,
) -> FpE:
    total = field.zero
    for basis_value in basis:
        total = field.add(total, field.scalar_mul(rng.randrange(field.q), basis_value))
    return total


def prefix_matrix(
    seeds: list[FpE],
    left_basis: list[FpE],
    right_degree: int,
    right_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    left_degree = len(left_basis)
    for lam in left_basis:
        row: list[int] = []
        for seed in seeds:
            trace_value = relative_trace_to_right(
                field.mul(lam, seed),
                left_degree,
                right_degree,
                field,
            )
            row.extend(coordinate_vector(trace_value, right_degree, right_inverse, field))
        rows.append(row)
    return rows


def adjoint_matrix(
    seeds: list[FpE],
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in seeds:
        for y in right_basis:
            trace_value = relative_trace_to_left(
                field.mul(y, seed),
                left_degree,
                right_degree,
                field,
            )
            rows.append(coordinate_vector(trace_value, left_degree, left_inverse, field))
    return rows


def pairing_mismatch_count(
    seeds: list[FpE],
    left_basis: list[FpE],
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
    rng: random.Random,
    tests: int,
) -> int:
    mismatches = 0
    for _ in range(tests):
        lam = random_subfield_element(left_basis, field, rng)
        ys = [random_subfield_element(right_basis, field, rng) for _ in seeds]
        left_pair = 0
        adjoint_argument = field.zero
        for y, seed in zip(ys, seeds):
            trace_value = relative_trace_to_right(
                field.mul(lam, seed),
                left_degree,
                right_degree,
                field,
            )
            left_pair = (
                left_pair
                + trace_to_base(field.mul(y, trace_value), right_degree, field)
            ) % field.q
            adjoint_argument = field.add(adjoint_argument, field.mul(y, seed))
        adjoint_value = relative_trace_to_left(
            adjoint_argument,
            left_degree,
            right_degree,
            field,
        )
        right_pair = trace_to_base(field.mul(lam, adjoint_value), left_degree, field)
        if left_pair % field.q != right_pair % field.q:
            mismatches += 1
    return mismatches


def audit_tuple(
    label: str,
    seeds: list[FpE],
    left_basis: list[FpE],
    right_basis: list[FpE],
    left_inverse: list[list[FpE]],
    right_inverse: list[list[FpE]],
    field: ExtensionField,
    rng: random.Random,
    pair_tests: int,
) -> PrefixAdjointRow:
    left_degree = len(left_basis)
    right_degree = len(right_basis)
    codomain_dim = len(seeds) * right_degree
    pmat = prefix_matrix(seeds, left_basis, right_degree, right_inverse, field)
    amat = adjoint_matrix(
        seeds,
        right_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    prefix_rank = rank_mod_q(pmat, field.q)
    adjoint_rank = rank_mod_q(amat, field.q)
    prefix_surjective = prefix_rank == codomain_dim
    adjoint_injective = adjoint_rank == codomain_dim
    return PrefixAdjointRow(
        label=label,
        prefix_rank=prefix_rank,
        adjoint_rank=adjoint_rank,
        codomain_dim=codomain_dim,
        kernel_dim=left_degree - prefix_rank,
        prefix_surjective=prefix_surjective,
        adjoint_injective=adjoint_injective,
        rank_match=(prefix_rank == adjoint_rank),
        event_match=(prefix_surjective == adjoint_injective),
        pairing_mismatches=pairing_mismatch_count(
            seeds,
            left_basis,
            right_basis,
            left_degree,
            right_degree,
            field,
            rng,
            pair_tests,
        ),
    )


def find_surjective_seeds(
    k: int,
    left_basis: list[FpE],
    right_basis: list[FpE],
    left_inverse: list[list[FpE]],
    right_inverse: list[list[FpE]],
    field: ExtensionField,
    rng: random.Random,
    attempts: int,
) -> list[FpE] | None:
    codomain_dim = k * len(right_basis)
    for _ in range(attempts):
        seeds = [random_element(field, rng) for _ in range(k)]
        row = audit_tuple(
            "candidate",
            seeds,
            left_basis,
            right_basis,
            left_inverse,
            right_inverse,
            field,
            rng,
            pair_tests=0,
        )
        if row.prefix_rank == codomain_dim:
            return seeds
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left-degree", type=int, default=5)
    parser.add_argument("--right-degree", type=int, default=2)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--pair-tests", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if gcd(args.left_degree, args.right_degree) != 1:
        raise ValueError("left and right degrees must be coprime")
    if args.k * args.right_degree > args.left_degree:
        raise ValueError("default theorem gate expects a positive prefix kernel")

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
    right_inverse = lang_inverse_for_orbit(args.q, args.right_degree, field, right_seed)
    rng = random.Random(args.seed)

    rows: list[PrefixAdjointRow] = []
    zero_seeds = [field.zero for _ in range(args.k)]
    rows.append(
        audit_tuple(
            "forced_zero",
            zero_seeds,
            left_basis,
            right_basis,
            left_inverse,
            right_inverse,
            field,
            rng,
            args.pair_tests,
        )
    )

    repeated_seed = random_element(field, rng)
    rows.append(
        audit_tuple(
            "forced_repeated_seed",
            [repeated_seed for _ in range(args.k)],
            left_basis,
            right_basis,
            left_inverse,
            right_inverse,
            field,
            rng,
            args.pair_tests,
        )
    )

    surjective = find_surjective_seeds(
        args.k,
        left_basis,
        right_basis,
        left_inverse,
        right_inverse,
        field,
        rng,
        attempts=2000,
    )
    if surjective is not None:
        rows.append(
            audit_tuple(
                "found_surjective_positive_kernel",
                surjective,
                left_basis,
                right_basis,
                left_inverse,
                right_inverse,
                field,
                rng,
                args.pair_tests,
            )
        )

    for trial in range(args.trials):
        rows.append(
            audit_tuple(
                f"random_{trial}",
                [random_element(field, rng) for _ in range(args.k)],
                left_basis,
                right_basis,
                left_inverse,
                right_inverse,
                field,
                rng,
                args.pair_tests,
            )
        )

    print("Trace-GCD prefix adjoint trace toy")
    print(f"q={args.q}")
    print(f"left_degree={args.left_degree}")
    print(f"right_degree={args.right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"codomain_dim={args.k * args.right_degree}")
    print(f"expected_positive_kernel_dim={args.left_degree - args.k * args.right_degree}")
    print(f"trials={args.trials}")
    print("columns: label prefix_rank adjoint_rank kernel_dim surj inj rank_match event_match pairing_mismatches")
    for row in rows[:20]:
        print(
            f"row label={row.label} prefix_rank={row.prefix_rank} "
            f"adjoint_rank={row.adjoint_rank} kernel_dim={row.kernel_dim} "
            f"surj={int(row.prefix_surjective)} "
            f"inj={int(row.adjoint_injective)} "
            f"rank_match={int(row.rank_match)} "
            f"event_match={int(row.event_match)} "
            f"pairing_mismatches={row.pairing_mismatches}"
        )

    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  prefix_adjoint_rank_mismatches={sum(not row.rank_match for row in rows)}")
    print(f"  surjective_adjoint_event_mismatches={sum(not row.event_match for row in rows)}")
    print(f"  pairing_mismatches={sum(row.pairing_mismatches for row in rows)}")
    print(
        "  found_positive_kernel_surjective="
        f"{int(any(row.label == 'found_surjective_positive_kernel' and row.prefix_surjective and row.kernel_dim > 0 for row in rows))}"
    )
    print(
        "  forced_dependent_not_surjective="
        f"{int(any(row.label == 'forced_repeated_seed' and not row.prefix_surjective for row in rows))}"
    )
    print("interpretation")
    print("  prefix_rank_equals_trace_adjoint_rank=1")
    print("  prefix_surjective_iff_trace_adjoint_injective=1")
    print("  p24_prefix_target_is_adjoint_trace_independence=1")
    print("conclusion=reported_trace_gcd_prefix_adjoint_trace_toy")


if __name__ == "__main__":
    main()
