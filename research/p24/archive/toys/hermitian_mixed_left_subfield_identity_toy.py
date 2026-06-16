#!/usr/bin/env python3
"""Finite-field toy for the mixed left-subfield identity.

This is not a CM computation.  It isolates the algebra behind the p24
Lang-normality target in a tiny coprime-degree case, for example

    q=2, left=7, right=5,
    ord_7(2)=3, ord_5(2)=4, gcd(3,4)=1.

For any base-field table M(a,b), form the mixed DFT block and then
Lang-trivialize the right Frobenius orbit.  The transformed coordinates should
land in the left character subfield F_{q^ord_left(q)}.  This is the formal
reason the p24 mixed block reduces to normality inside F_{p^156}.

The script also reports individual-coordinate normal ranks as a diagnostic.
Those do not by themselves imply full mixed-block rank; the actual condition
is the F_q-rank of the transformed coordinate tuple.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from math import gcd

import sympy as sp

from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    matrix_vector_mul,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)


@dataclass(frozen=True)
class ToyTrial:
    trial: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len: int
    transformed_count: int
    transformed_fq_rank: int
    row_orbit_rank: int
    left_subfield_failures: int
    max_single_normal_rank: int
    normal_coordinate_count: int


def frobenius(value: FpE, power: int, field: ExtensionField) -> FpE:
    return field.pow(value, field.q**power)


def random_base_table(left: int, right: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(right)] for _ in range(left)]


def submatrix(matrix, rows: list[int], cols: list[int]):
    return [[matrix[row][col] for col in cols] for row in rows]


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


def individual_normal_rank(value: FpE, degree: int, q: int, field: ExtensionField) -> int:
    return fq_rank([frobenius(value, i, field) for i in range(degree)], q)


def audit_trial(
    trial: int,
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
    zeta_pows,
    seed: int,
    rng: random.Random,
) -> list[ToyTrial]:
    table = random_base_table(left, right, q, rng)
    dft_matrix = dft_double_marginal(table, left, right, zeta_pows, left * right, field)
    right_orbits = q_orbits(right, q)
    out: list[ToyTrial] = []
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    for left_orbit in q_orbits(left, q):
        row_indices = [row_index[u] for u in left_orbit]
        col_indices = [col_index[v] for orbit in right_orbits for v in orbit]
        row_orbit_rank = rank_over_extension(
            submatrix(dft_matrix, row_indices, col_indices),
            field,
        )
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
        left_len = len(left_orbit)
        subfield_failures = sum(
            1 for value in transformed if frobenius(value, left_len, field) != value
        )
        normal_ranks = [
            individual_normal_rank(value, left_len, q, field)
            for value in transformed
            if value != field.zero
        ]
        out.append(
            ToyTrial(
                trial=trial,
                left_orbit_rep=left_orbit[0],
                left_orbit_len=left_len,
                right_orbit_count=len(right_orbits),
                right_orbit_len=len(right_orbits[0]) if right_orbits else 0,
                transformed_count=len(transformed),
                transformed_fq_rank=fq_rank(transformed, q),
                row_orbit_rank=row_orbit_rank,
                left_subfield_failures=subfield_failures,
                max_single_normal_rank=max(normal_ranks) if normal_ranks else 0,
                normal_coordinate_count=sum(
                    1 for rank in normal_ranks if rank == left_len
                ),
            )
        )
    return out


def format_trial(row: ToyTrial) -> str:
    return (
        f"trial={row.trial} left_rep={row.left_orbit_rep} "
        f"L={row.left_orbit_len} right_orbits={row.right_orbit_count} "
        f"R={row.right_orbit_len} count={row.transformed_count} "
        f"rank={row.transformed_fq_rank} rowrank={row.row_orbit_rank} "
        f"subfail={row.left_subfield_failures} "
        f"maxsingle={row.max_single_normal_rank} "
        f"normalcount={row.normal_coordinate_count}"
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

    m = args.left * args.right
    left_degree = int(sp.n_order(args.q % args.left, args.left))
    right_degree = int(sp.n_order(args.q % args.right, args.right))
    extension_degree = int(sp.ilcm(left_degree, right_degree))
    modulus = find_irreducible_modulus(args.q, extension_degree, args.seed)
    field = ExtensionField(args.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, args.seed)
    powers = zeta_powers(zeta, m, field)
    rng = random.Random(args.seed)

    rows: list[ToyTrial] = []
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

    subfield_failures = sum(row.left_subfield_failures for row in rows)
    full_span = [row for row in rows if row.transformed_fq_rank >= row.left_orbit_len]
    single_normal = [row for row in rows if row.normal_coordinate_count > 0]

    print("Hermitian mixed left-subfield identity toy")
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
    print(f"  left_orbit_tests={len(rows)}")
    print(f"  left_subfield_failures={subfield_failures}")
    print(f"  full_left_span_tests={len(full_span)}")
    print(f"  individual_normal_coordinate_tests_diagnostic={len(single_normal)}")
    if rows:
        print(f"  max_transformed_fq_rank={max(row.transformed_fq_rank for row in rows)}")
        print(
            "  max_individual_normal_rank_diagnostic="
            f"{max(row.max_single_normal_rank for row in rows)}"
        )
    print()
    print("interpretation")
    print("  zero_subfield_failures_is_formal_coprime_left_right_landing=1")
    print("  individual_normality_is_diagnostic_not_sufficient=1")
    print("  full_left_span_requires_independent_transformed_coordinates=1")
    print("conclusion=reported_hermitian_mixed_left_subfield_identity_toy")


if __name__ == "__main__":
    main()
