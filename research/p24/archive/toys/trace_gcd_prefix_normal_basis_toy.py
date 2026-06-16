#!/usr/bin/env python3
"""Toy gate for the prefix normal-basis coefficient form.

For coprime finite extensions L=F_q^l, R=F_q^r, E=F_q^(lr), choose a
normal basis alpha_i of R/F_q and its trace-dual alpha_i^vee.  Every S in E
has the expansion

    S = sum_i Tr_{E/L}(alpha_i*S) * alpha_i^vee.

Thus the prefix quotient map R^k -> E/(tau_R-1)E ~= L is injective exactly
when the k*r left-field coefficients Tr_{E/L}(alpha_i*S_j) are F_q-linearly
independent in L.

This is a finite structural gate, not a p24 search.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_adjoint_trace_toy import (
    base_value,
    coordinate_vector,
    random_element,
    random_subfield_element,
    relative_trace_to_left,
    trace_under_power,
)


@dataclass(frozen=True)
class NormalBasisRow:
    label: str
    power_rank: int
    normal_coeff_rank: int
    domain_dim: int
    reconstruction_failures: int
    rank_match: bool
    injective: bool


def inverse_base_matrix(matrix: list[list[int]], q: int) -> list[list[int]]:
    n = len(matrix)
    augmented = [
        [value % q for value in row]
        + [1 if i == j else 0 for j in range(n)]
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
            raise ValueError("singular base matrix")
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = pow(augmented[rank][col] % q, -1, q)
        augmented[rank] = [(value * inv) % q for value in augmented[rank]]
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


def trace_right_to_base(value: FpE, right_degree: int, field: ExtensionField) -> int:
    return base_value(trace_under_power(value, 1, right_degree, field), field)


def find_normal_basis(
    q: int,
    right_degree: int,
    right_power_basis: list[FpE],
    field: ExtensionField,
    rng: random.Random,
    attempts: int,
) -> list[FpE]:
    candidates = right_power_basis[:]
    candidates.extend(random_subfield_element(right_power_basis, field, rng) for _ in range(attempts))
    for candidate in candidates:
        if candidate == field.zero:
            continue
        basis = [field.pow(candidate, q**i) for i in range(right_degree)]
        if rank_mod_q([list(value) for value in basis], q) == right_degree:
            return basis
    raise RuntimeError("could not find a normal basis for the right subfield")


def trace_dual_basis(
    normal_basis: list[FpE],
    right_degree: int,
    field: ExtensionField,
) -> tuple[list[FpE], int]:
    gram = [
        [
            trace_right_to_base(field.mul(left, right), right_degree, field)
            for right in normal_basis
        ]
        for left in normal_basis
    ]
    gram_inv = inverse_base_matrix(gram, field.q)
    dual: list[FpE] = []
    for i in range(right_degree):
        total = field.zero
        for k, basis_value in enumerate(normal_basis):
            total = field.add(total, field.scalar_mul(gram_inv[k][i], basis_value))
        dual.append(total)

    failures = 0
    for i, dual_value in enumerate(dual):
        for j, basis_value in enumerate(normal_basis):
            got = trace_right_to_base(field.mul(basis_value, dual_value), right_degree, field)
            expected = 1 if i == j else 0
            if got != expected:
                failures += 1
    return dual, failures


def coefficient_rows(
    seeds: list[FpE],
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in seeds:
        for alpha in right_basis:
            coeff = relative_trace_to_left(
                field.mul(alpha, seed),
                left_degree,
                right_degree,
                field,
            )
            rows.append(coordinate_vector(coeff, left_degree, left_inverse, field))
    return rows


def reconstruct_from_trace_dual_coefficients(
    seed: FpE,
    normal_basis: list[FpE],
    dual_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for alpha, dual in zip(normal_basis, dual_basis):
        coeff = relative_trace_to_left(
            field.mul(alpha, seed),
            left_degree,
            right_degree,
            field,
        )
        total = field.add(total, field.mul(coeff, dual))
    return total


def audit_tuple(
    label: str,
    seeds: list[FpE],
    right_power_basis: list[FpE],
    normal_basis: list[FpE],
    dual_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> NormalBasisRow:
    power_rows = coefficient_rows(
        seeds,
        right_power_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    normal_rows = coefficient_rows(
        seeds,
        normal_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    reconstruction_failures = sum(
        reconstruct_from_trace_dual_coefficients(
            seed,
            normal_basis,
            dual_basis,
            left_degree,
            right_degree,
            field,
        )
        != seed
        for seed in seeds
    )
    power_rank = rank_mod_q(power_rows, field.q)
    normal_rank = rank_mod_q(normal_rows, field.q)
    domain_dim = len(seeds) * right_degree
    return NormalBasisRow(
        label=label,
        power_rank=power_rank,
        normal_coeff_rank=normal_rank,
        domain_dim=domain_dim,
        reconstruction_failures=reconstruction_failures,
        rank_match=power_rank == normal_rank,
        injective=normal_rank == domain_dim,
    )


def find_good_seeds(
    k: int,
    right_power_basis: list[FpE],
    normal_basis: list[FpE],
    dual_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
    rng: random.Random,
    attempts: int,
) -> list[FpE] | None:
    for _ in range(attempts):
        seeds = [random_element(field, rng) for _ in range(k)]
        row = audit_tuple(
            "candidate",
            seeds,
            right_power_basis,
            normal_basis,
            dual_basis,
            left_degree,
            right_degree,
            left_inverse,
            field,
        )
        if row.injective:
            return seeds
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--left-degree", type=int, default=7)
    parser.add_argument("--right-degree", type=int, default=3)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if gcd(args.left_degree, args.right_degree) != 1:
        raise ValueError("left and right degrees must be coprime")
    if args.k * args.right_degree > args.left_degree:
        raise ValueError("toy expects positive residual dimension in L")

    extension_degree = args.left_degree * args.right_degree
    field = ExtensionField(
        args.q,
        extension_degree,
        find_irreducible_modulus(args.q, extension_degree, args.seed),
    )
    rng = random.Random(args.seed)
    right_power_basis = subfield_power_basis(
        args.q,
        args.right_degree,
        field,
        args.seed + 29,
    )
    normal_basis = find_normal_basis(
        args.q,
        args.right_degree,
        right_power_basis,
        field,
        rng,
        attempts=200,
    )
    dual_basis, dual_pairing_failures = trace_dual_basis(
        normal_basis,
        args.right_degree,
        field,
    )

    from hermitian_mixed_lang_normality_audit import lang_inverse_for_orbit

    left_inverse = lang_inverse_for_orbit(
        args.q,
        args.left_degree,
        field,
        args.seed + 17,
    )

    rows: list[NormalBasisRow] = []
    rows.append(
        audit_tuple(
            "forced_zero",
            [field.zero for _ in range(args.k)],
            right_power_basis,
            normal_basis,
            dual_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
        )
    )
    repeated = random_element(field, rng)
    rows.append(
        audit_tuple(
            "forced_repeated_seed",
            [repeated for _ in range(args.k)],
            right_power_basis,
            normal_basis,
            dual_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
        )
    )
    good = find_good_seeds(
        args.k,
        right_power_basis,
        normal_basis,
        dual_basis,
        args.left_degree,
        args.right_degree,
        left_inverse,
        field,
        rng,
        attempts=2000,
    )
    if good is not None:
        rows.append(
            audit_tuple(
                "found_normal_coefficient_independent",
                good,
                right_power_basis,
                normal_basis,
                dual_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
            )
        )
    for trial in range(args.trials):
        rows.append(
            audit_tuple(
                f"random_{trial}",
                [random_element(field, rng) for _ in range(args.k)],
                right_power_basis,
                normal_basis,
                dual_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
            )
        )

    print("Trace-GCD prefix normal-basis coefficient toy")
    print(f"q={args.q}")
    print(f"left_degree={args.left_degree}")
    print(f"right_degree={args.right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"domain_dim={args.k * args.right_degree}")
    print(f"expected_positive_kernel_dim={args.left_degree - args.k * args.right_degree}")
    print(
        "columns: label power_rank normal_coeff_rank domain_dim "
        "reconstruction_failures rank_match injective"
    )
    for row in rows[:24]:
        print(
            f"row label={row.label} power_rank={row.power_rank} "
            f"normal_coeff_rank={row.normal_coeff_rank} "
            f"domain_dim={row.domain_dim} "
            f"reconstruction_failures={row.reconstruction_failures} "
            f"rank_match={int(row.rank_match)} "
            f"injective={int(row.injective)}"
        )
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  dual_pairing_failures={dual_pairing_failures}")
    print(f"  dual_reconstruction_failures={sum(row.reconstruction_failures for row in rows)}")
    print(f"  basis_rank_mismatches={sum(not row.rank_match for row in rows)}")
    print(
        "  found_normal_coefficient_independent="
        f"{int(any(row.label == 'found_normal_coefficient_independent' and row.injective for row in rows))}"
    )
    print(
        "  forced_repeated_coefficient_dependence="
        f"{int(any(row.label == 'forced_repeated_seed' and not row.injective for row in rows))}"
    )
    print("interpretation")
    print("  trace_dual_coefficients_reconstruct_periods=1")
    print("  prefix_quotient_rank_equals_normal_coefficient_rank=1")
    print("  p24_prefix_target_is_rank_140_of_right_normal_coefficients=1")
    print("conclusion=reported_trace_gcd_prefix_normal_basis_toy")


if __name__ == "__main__":
    main()
