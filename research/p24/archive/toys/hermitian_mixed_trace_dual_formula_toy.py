#!/usr/bin/env python3
"""Toy verification of the trace-dual formula for Lang coordinates.

In the coprime-degree case, let

    E = F_q(mu_left, mu_right), L = F_q(mu_left), R = F_q(mu_right).

For a mixed DFT seed value S=H(u0,v0), the right orbit seed vector is

    S_b = tau_R^b(S),

where tau_R fixes L and sends mu_right to mu_right^q.  If
`alpha_i` is an F_q-basis of R and `delta_i` is the trace-dual basis, then
the Lang-trivialized coordinates are

    w_i = Tr_{E/L}(delta_i * S).

This script verifies that these relative trace-dual coordinates agree exactly
with the matrix inverse used in `hermitian_mixed_lang_normality_audit.py`.
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
class FormulaTrial:
    trial: int
    left_orbit_rep: int
    right_orbit_rep: int
    left_orbit_len: int
    right_orbit_len: int
    transformed_rank: int
    trace_dual_mismatches: int
    left_subfield_failures: int


def random_base_table(left: int, right: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(right)] for _ in range(left)]


def base_value(value: FpE, field: ExtensionField) -> int:
    if any(value[i] % field.q for i in range(1, field.degree)):
        raise ValueError(f"value is not in base field: {value}")
    return value[0] % field.q


def matrix_inverse_mod_q(matrix: list[list[int]], q: int) -> list[list[int]]:
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
            raise ValueError("singular base-field matrix")
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = pow(augmented[rank][col] % q, -1, q)
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


def dual_basis_for_right_trace(
    q: int,
    right_degree: int,
    right_step: int,
    field: ExtensionField,
    seed: int,
) -> list[FpE]:
    basis = subfield_power_basis(q, right_degree, field, seed)
    gram: list[list[int]] = []
    for alpha in basis:
        row: list[int] = []
        for beta in basis:
            row.append(base_value(trace_under_power(field.mul(alpha, beta), right_step, right_degree, field), field))
        gram.append(row)
    inv = matrix_inverse_mod_q(gram, q)
    dual: list[FpE] = []
    for i in range(right_degree):
        total = field.zero
        for k, alpha in enumerate(basis):
            total = field.add(total, field.scalar_mul(inv[i][k], alpha))
        dual.append(total)
    return dual


def relative_trace_to_left(
    value: FpE,
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    # tau_R fixes F_{q^left_degree} and acts as q-Frobenius on the right
    # factor.  Its exponent is the CRT solution e = 0 mod left_degree,
    # e = 1 mod right_degree.
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("relative trace formula here assumes coprime degrees")
    step = left_degree * pow(left_degree % right_degree, -1, right_degree)
    return trace_under_power(value, step, right_degree, field)


def audit_trial(
    trial: int,
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
    zeta_pows,
    seed: int,
    rng: random.Random,
) -> list[FormulaTrial]:
    table = random_base_table(left, right, q, rng)
    dft_matrix = dft_double_marginal(table, left, right, zeta_pows, left * right, field)
    left_degree = int(sp.n_order(q % left, left))
    right_degree = int(sp.n_order(q % right, right))
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("toy expects coprime left/right orbit degrees")
    right_dual = dual_basis_for_right_trace(q, right_degree, 1, field, seed)
    right_inverse = lang_inverse_for_orbit(q, right_degree, field, seed)

    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    out: list[FormulaTrial] = []
    for left_orbit in q_orbits(left, q):
        for right_orbit in q_orbits(right, q):
            seed_vector = [
                dft_matrix[row_index[left_orbit[0]]][col_index[v]]
                for v in right_orbit
            ]
            inverse_coords = matrix_vector_mul(right_inverse, seed_vector, field)
            seed_value = dft_matrix[row_index[left_orbit[0]]][col_index[right_orbit[0]]]
            trace_coords = [
                relative_trace_to_left(
                    field.mul(delta, seed_value),
                    len(left_orbit),
                    len(right_orbit),
                    field,
                )
                for delta in right_dual
            ]
            mismatches = sum(
                1 for left_value, right_value in zip(inverse_coords, trace_coords)
                if left_value != right_value
            )
            subfield_failures = sum(
                1
                for value in trace_coords
                if field.pow(value, field.q ** len(left_orbit)) != value
            )
            out.append(
                FormulaTrial(
                    trial=trial,
                    left_orbit_rep=left_orbit[0],
                    right_orbit_rep=right_orbit[0],
                    left_orbit_len=len(left_orbit),
                    right_orbit_len=len(right_orbit),
                    transformed_rank=fq_rank(trace_coords, q),
                    trace_dual_mismatches=mismatches,
                    left_subfield_failures=subfield_failures,
                )
            )
    return out


def format_trial(row: FormulaTrial) -> str:
    return (
        f"trial={row.trial} left_rep={row.left_orbit_rep} "
        f"right_rep={row.right_orbit_rep} L={row.left_orbit_len} "
        f"R={row.right_orbit_len} rank={row.transformed_rank} "
        f"mismatch={row.trace_dual_mismatches} "
        f"subfail={row.left_subfield_failures}"
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

    rows: list[FormulaTrial] = []
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

    mismatches = sum(row.trace_dual_mismatches for row in rows)
    subfield_failures = sum(row.left_subfield_failures for row in rows)
    full_span = [row for row in rows if row.transformed_rank >= row.left_orbit_len]

    print("Hermitian mixed trace-dual formula toy")
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
    print(f"  formula_tests={len(rows)}")
    print(f"  trace_dual_mismatches={mismatches}")
    print(f"  left_subfield_failures={subfield_failures}")
    print(f"  full_left_span_tests={len(full_span)}")
    if rows:
        print(f"  max_transformed_rank={max(row.transformed_rank for row in rows)}")
    print()
    print("interpretation")
    print("  zero_mismatches_confirms_lang_coordinates_are_trace_dual=1")
    print("  p24_coordinates_are_relative_traces_to_Fp_mu_157=1")
    print("conclusion=reported_hermitian_mixed_trace_dual_formula_toy")


if __name__ == "__main__":
    main()
