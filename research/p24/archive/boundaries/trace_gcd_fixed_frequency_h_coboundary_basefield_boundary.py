#!/usr/bin/env python3
"""Base-field form of the p24 H-coboundary target.

For the mixed centered marginal

    C(r,s),  1 <= r < 157, 1 <= s < 211,

the left-character profile is

    G_s = sum_r zeta_157^r C(r,s).

Since the nonzero powers of zeta_157 form an F_p-basis of F_p(mu_157), the
order-7 H-coboundary theorem is equivalent to the base-field row identities

    sum_{s in qH} C(r,s) = 0

for every left row r and every H-coset qH, where H=<2^7> has order 30 in
(Z/211Z)^*.  This script records that finite dictionary and checks that the
analogous identity is not a generic actual-CM packet symmetry.
"""

from __future__ import annotations

import random

from trace_gcd_fixed_frequency_unit_symmetry_boundary import (
    LEFT as PINNED_LEFT,
    RIGHT as PINNED_RIGHT,
    RIGHT_PRIMITIVE as PINNED_RIGHT_PRIMITIVE,
    load_pinned_packet,
)


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
Q = 1009
TOY_ROWS = 5


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not mat:
        return 0
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if mat[row][col] % q), None)
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [value * inv % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if scale:
                mat[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(mat[row], mat[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def log_table(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("generator is not primitive")
    return logs


def cosets_by_log_residue(modulus: int, generator: int, step: int) -> list[list[int]]:
    logs = log_table(modulus, generator)
    return [
        sorted(
            [value for value in range(1, modulus) if logs[value] % step == residue],
            key=logs.__getitem__,
        )
        for residue in range(step)
    ]


def h_coset_sums(row: list[int], cosets: list[list[int]], q: int) -> list[int]:
    return [sum(row[value] for value in coset) % q for coset in cosets]


def matrix_h_coset_sums(matrix: list[list[int]], cosets: list[list[int]], q: int) -> list[list[int]]:
    return [h_coset_sums(row, cosets, q) for row in matrix]


def random_globally_centered_matrix(rng: random.Random, rows: int, right: int, q: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for _ in range(rows):
        row = [0] + [rng.randrange(q) for _value in range(1, right)]
        row[1] = (row[1] - sum(row[1:])) % q
        matrix.append(row)
    return matrix


def force_h_trace_zero(matrix: list[list[int]], cosets: list[list[int]], q: int) -> list[list[int]]:
    adjusted = [row[:] for row in matrix]
    for row in adjusted:
        for coset in cosets:
            row[coset[0]] = (row[coset[0]] - sum(row[value] for value in coset)) % q
    return adjusted


def coboundary_potential(row: list[int], cosets: list[list[int]], gamma: int, right: int, q: int) -> list[int]:
    potential = [0] * right
    for coset in cosets:
        value = coset[0]
        running = 0
        for _index in range(len(coset) - 1):
            running = (running - row[value]) % q
            value = gamma * value % right
            potential[value] = running
        if gamma * value % right != coset[0]:
            raise RuntimeError("bad H-cycle")
    return potential


def coboundary_from_potential(potential: list[int], gamma: int, right: int, q: int) -> list[int]:
    row = [0] * right
    for value in range(1, right):
        row[value] = (potential[value] - potential[gamma * value % right]) % q
    return row


def same_nonzero_row(left: list[int], right: list[int], q: int) -> bool:
    return all((left[index] - right[index]) % q == 0 for index in range(1, len(left)))


def pinned_h_cosets() -> list[list[int]]:
    # For the pinned right=7 row, the Frobenius subgroup is the square subgroup
    # <2>={1,2,4}, so the quotient has two cosets.
    return cosets_by_log_residue(PINNED_RIGHT, PINNED_RIGHT_PRIMITIVE, 2)


def pinned_coset_sum_matrix() -> tuple[list[list[int]], int, int]:
    packet = load_pinned_packet()
    cosets = pinned_h_cosets()
    matrix = [[0] + row[:] for row in packet.centered]
    sums = matrix_h_coset_sums(matrix, cosets, packet.q)
    zero_entries = sum(int(value == 0) for row in sums for value in row)
    return sums, zero_entries, packet.q


def main() -> None:
    rng = random.Random(20260606)
    logs = log_table(RIGHT, GEN)
    p_log = logs[P24 % RIGHT]
    gamma = pow(GEN, H_STEP, RIGHT)
    cosets = cosets_by_log_residue(RIGHT, GEN, H_STEP)

    centered = random_globally_centered_matrix(rng, TOY_ROWS, RIGHT, Q)
    centered_sums = matrix_h_coset_sums(centered, cosets, Q)
    forced = force_h_trace_zero(centered, cosets, Q)
    forced_sums = matrix_h_coset_sums(forced, cosets, Q)
    reconstructed = [
        coboundary_from_potential(
            coboundary_potential(row, cosets, gamma, RIGHT, Q),
            gamma,
            RIGHT,
            Q,
        )
        for row in forced
    ]
    reconstruction_matches = all(
        same_nonzero_row(row, rebuilt, Q)
        for row, rebuilt in zip(forced, reconstructed)
    )
    pinned_sums, pinned_zero_entries, pinned_q = pinned_coset_sum_matrix()
    pinned_rank = rank_mod(pinned_sums, pinned_q)

    print("Trace-GCD fixed-frequency H-coboundary base-field boundary")
    print("p24_finite_dictionary")
    print(f"  p24_p_mod_211={P24 % RIGHT}")
    print(f"  p24_log_base_2_mod_211={p_log}")
    print(f"  h_generator=2^{H_STEP}_mod_211={gamma}")
    print(f"  h_coset_count={len(cosets)}")
    print(f"  h_coset_size={len(cosets[0])}")
    print(f"  toy_rows={TOY_ROWS}")
    print(f"  ordinary_centered_h_coset_sum_rank={rank_mod(centered_sums, Q)}")
    print(f"  ordinary_centering_has_h_coset_leak={int(any(any(value for value in row) for row in centered_sums))}")
    print(f"  forced_h_trace_zero_rank={rank_mod(forced_sums, Q)}")
    print(f"  forced_h_trace_zero_all_zero={int(all(all(value == 0 for value in row) for row in forced_sums))}")
    print(f"  h_trace_zero_reconstructs_rowwise_coboundary={int(reconstruction_matches)}")
    print("pinned_actual_cm_analogue")
    print(f"  D=-13319")
    print(f"  q={pinned_q}")
    print(f"  left_component={PINNED_LEFT}")
    print(f"  right_component={PINNED_RIGHT}")
    print(f"  h_coset_sums={pinned_sums}")
    print(f"  h_coset_sum_zero_entries={pinned_zero_entries}/6")
    print(f"  h_coset_sum_rank={pinned_rank}")
    print("interpretation")
    print("  p24_h_coboundary_is_basefield_h_coset_column_sum_vanishing=1")
    print("  ordinary_centering_does_not_force_basefield_h_coset_vanishing=1")
    print("  actual_cm_analogue_refutes_generic_h_coboundary=1")
    print("  next_theorem_must_prove_specific_p24_gaussian_period_marginal_identity=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_h_coboundary_basefield_boundary")

    if (p_log, gamma, len(cosets), len(cosets[0])) != (198, 128, 7, 30):
        raise SystemExit(1)
    if not any(any(value for value in row) for row in centered_sums):
        raise SystemExit(1)
    if any(any(value != 0 for value in row) for row in forced_sums):
        raise SystemExit(1)
    if not reconstruction_matches:
        raise SystemExit(1)
    if pinned_zero_entries == 6 or pinned_rank == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
