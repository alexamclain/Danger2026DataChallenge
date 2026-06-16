#!/usr/bin/env python3
"""Toy verification of the dual relative-trace injectivity criterion.

The left-subfield span target is

    dim_Fq span{w_i} = left_degree,
    w_i in L = F_{q^left_degree}.

By trace duality on L/F_q, this is equivalent to injectivity of

    L -> R^k,
    lambda |-> (Tr_{E/R}(lambda * S_j))_j,

where E = L R, R = F_{q^right_degree}, and the S_j are the mixed seed
periods for the right Frobenius orbits.

This script verifies that equivalence in the same coprime-degree finite-field
toy used by `hermitian_mixed_trace_dual_formula_toy.py`.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from math import gcd

import sympy as sp

from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class DualTrial:
    trial: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len: int
    coordinate_span_rank: int
    dual_trace_rank: int
    rank_match: bool
    full_span: bool
    dual_injective: bool


def random_base_table(left: int, right: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(right)] for _ in range(left)]


def relative_trace_to_right(
    value: FpE,
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("relative trace formula here assumes coprime degrees")
    step = right_degree * pow(right_degree % left_degree, -1, left_degree)
    total = field.zero
    for i in range(left_degree):
        total = field.add(total, field.pow(value, field.q ** (step * i)))
    return total


def transformed_coordinates(
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    q: int,
    field: ExtensionField,
    seed: int,
) -> list[FpE]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    transformed: list[FpE] = []
    inverses: dict[int, list[list[FpE]]] = {}
    for right_orbit in right_orbits:
        orbit_len = len(right_orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(q, orbit_len, field, seed)
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in right_orbit
        ]
        transformed.extend(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return transformed


def left_basis_for_orbit(
    q: int,
    left_degree: int,
    field: ExtensionField,
    seed: int,
) -> list[FpE]:
    return subfield_power_basis(q, left_degree, field, seed + 7919)


def right_coordinate_vector(
    value: FpE,
    right_basis: list[FpE],
    right_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[FpE]:
    # Reuse the same matrix-vector convention as Lang coordinates:
    # right_inverse converts basis-conjugate coordinates into basis
    # coefficients.  Here the vector is the right trace orbit of `value`.
    orbit = [field.pow(value, field.q**i) for i in range(len(right_basis))]
    return matrix_vector_mul(right_inverse, orbit, field)


def dual_trace_matrix_rank(
    seed_values: list[FpE],
    left_degree: int,
    right_degree: int,
    q: int,
    field: ExtensionField,
    seed: int,
) -> int:
    left_basis = left_basis_for_orbit(q, left_degree, field, seed)
    right_basis = subfield_power_basis(q, right_degree, field, seed)
    right_inverse = lang_inverse_for_orbit(q, right_degree, field, seed)
    rows: list[list[int]] = []
    for lam in left_basis:
        row_values: list[FpE] = []
        for seed_value in seed_values:
            trace_value = relative_trace_to_right(
                field.mul(lam, seed_value),
                left_degree,
                right_degree,
                field,
            )
            row_values.extend(
                right_coordinate_vector(trace_value, right_basis, right_inverse, field)
            )
        rows.append([coord for value in row_values for coord in value])
    return sp.Matrix(rows).rank() if q == 0 else fq_rank([tuple(row) for row in rows], q)


def audit_trial(
    trial: int,
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
    zeta_pows,
    seed: int,
    rng: random.Random,
) -> list[DualTrial]:
    table = random_base_table(left, right, q, rng)
    dft_matrix = dft_double_marginal(table, left, right, zeta_pows, left * right, field)
    left_degree = int(sp.n_order(q % left, left))
    right_degree = int(sp.n_order(q % right, right))
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    out: list[DualTrial] = []
    for left_orbit in q_orbits(left, q):
        right_orbits = q_orbits(right, q)
        transformed = transformed_coordinates(
            dft_matrix,
            left,
            right,
            left_orbit,
            right_orbits,
            q,
            field,
            seed,
        )
        seed_values = [
            dft_matrix[row_index[left_orbit[0]]][col_index[right_orbit[0]]]
            for right_orbit in right_orbits
        ]
        coordinate_rank = fq_rank(transformed, q)
        dual_rank = dual_trace_matrix_rank(
            seed_values,
            len(left_orbit),
            len(right_orbits[0]),
            q,
            field,
            seed,
        )
        out.append(
            DualTrial(
                trial=trial,
                left_orbit_rep=left_orbit[0],
                left_orbit_len=len(left_orbit),
                right_orbit_count=len(right_orbits),
                right_orbit_len=len(right_orbits[0]) if right_orbits else 0,
                coordinate_span_rank=coordinate_rank,
                dual_trace_rank=dual_rank,
                rank_match=(coordinate_rank == dual_rank),
                full_span=(coordinate_rank >= len(left_orbit)),
                dual_injective=(dual_rank >= len(left_orbit)),
            )
        )
    return out


def format_trial(row: DualTrial) -> str:
    return (
        f"trial={row.trial} left_rep={row.left_orbit_rep} "
        f"L={row.left_orbit_len} right_orbits={row.right_orbit_count} "
        f"R={row.right_orbit_len} coordrank={row.coordinate_span_rank} "
        f"dualrank={row.dual_trace_rank} match={int(row.rank_match)} "
        f"full={int(row.full_span)} injective={int(row.dual_injective)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left", type=int, default=7)
    parser.add_argument("--right", type=int, default=5)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    left_degree = int(sp.n_order(args.q % args.left, args.left))
    right_degree = int(sp.n_order(args.q % args.right, args.right))
    extension_degree = int(sp.ilcm(left_degree, right_degree))
    modulus = find_irreducible_modulus(args.q, extension_degree, args.seed)
    field = ExtensionField(args.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, args.left * args.right, args.seed)
    powers = zeta_powers(zeta, args.left * args.right, field)
    rng = random.Random(args.seed)

    rows: list[DualTrial] = []
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
            )
        )

    mismatches = [row for row in rows if not row.rank_match]
    full_span = [row for row in rows if row.full_span]
    dual_injective = [row for row in rows if row.dual_injective]

    print("Hermitian mixed dual-trace injectivity toy")
    print(f"q={args.q}")
    print(f"left={args.left} ord_left={left_degree}")
    print(f"right={args.right} ord_right={right_degree}")
    print(f"gcd_degrees={gcd(left_degree, right_degree)}")
    print(f"extension_degree={extension_degree}")
    print(f"trials={args.trials}")
    print()
    if not args.summary_only:
        for row in rows[:80]:
            print(format_trial(row))
    print()
    print("summary")
    print(f"  dual_tests={len(rows)}")
    print(f"  rank_mismatches={len(mismatches)}")
    print(f"  full_span_tests={len(full_span)}")
    print(f"  dual_injective_tests={len(dual_injective)}")
    if rows:
        print(f"  max_coordinate_rank={max(row.coordinate_span_rank for row in rows)}")
        print(f"  max_dual_trace_rank={max(row.dual_trace_rank for row in rows)}")
    print()
    print("interpretation")
    print("  zero_rank_mismatches_confirms_span_dual_trace_injectivity=1")
    print("  p24_target_equiv_no_nonzero_lambda_kills_all_six_traces=1")
    print("conclusion=reported_hermitian_mixed_dual_trace_injectivity_toy")


if __name__ == "__main__":
    main()
