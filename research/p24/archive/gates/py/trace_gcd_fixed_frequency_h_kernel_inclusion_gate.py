#!/usr/bin/env python3
"""Kernel-inclusion form of the p24 H-coset theorem.

The current fixed-frequency theorem asks for the 156 x 210 centered mixed
marginal C to have zero sums on the seven cosets of

    H = <2^7> <= (Z/211Z)^*.

Equivalently, the 7-dimensional Gaussian-period indicator subspace is
contained in the right kernel of C.  This script records that exact finite
linear algebra, and separates it from two tempting non-proofs:

* full row rank / left normality does not imply the H-kernel inclusion;
* invariance under right multiplication by p^156 would imply it, but that is a
  stronger symmetry not supplied by the CM packet.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
H_STEP = 7
LEFT_ROWS = 156
FIELD_Q = 1_000_003


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    rows = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if rows[row][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, q)
        rows[rank] = [value * inv % q for value in rows[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("2 is not primitive modulo 211")
    return logs


def h_cosets(logs: dict[int, int]) -> list[list[int]]:
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % H_STEP == residue],
            key=logs.__getitem__,
        )
        for residue in range(H_STEP)
    ]


def h_indicator_columns(cosets: list[list[int]]) -> list[list[int]]:
    columns: list[list[int]] = []
    for coset in cosets:
        indicator = [0] * (RIGHT - 1)
        for value in coset:
            indicator[value - 1] = 1
        columns.append(indicator)
    return columns


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]


def h_coset_sums(row: list[int], cosets: list[list[int]], q: int = FIELD_Q) -> list[int]:
    return [sum(row[value - 1] for value in coset) % q for coset in cosets]


def matrix_times_h_indicators(
    matrix: list[list[int]],
    cosets: list[list[int]],
    q: int = FIELD_Q,
) -> list[list[int]]:
    return [h_coset_sums(row, cosets, q) for row in matrix]


def random_centered_row(rng: random.Random, q: int = FIELD_Q) -> list[int]:
    row = [rng.randrange(q) for _ in range(RIGHT - 1)]
    row[0] = (row[0] - sum(row)) % q
    return row


def random_h_orthogonal_row(
    rng: random.Random,
    cosets: list[list[int]],
    q: int = FIELD_Q,
) -> list[int]:
    row = [0] * (RIGHT - 1)
    for coset in cosets:
        total = 0
        for value in coset[:-1]:
            entry = rng.randrange(q)
            row[value - 1] = entry
            total = (total + entry) % q
        row[coset[-1] - 1] = (-total) % q
    return row


def random_eta_invariant_centered_row(
    rng: random.Random,
    eta: int,
    q: int = FIELD_Q,
) -> list[int]:
    row = [None] * (RIGHT - 1)
    for start in range(1, RIGHT):
        if row[start - 1] is not None:
            continue
        orbit = []
        value = start
        while row[value - 1] is None:
            orbit.append(value)
            row[value - 1] = 0
            value = value * eta % RIGHT
        entry = rng.randrange(q)
        for value in orbit:
            row[value - 1] = entry
    out = [int(value) for value in row]
    # The eta-orbits all have equal size for eta=p^156.  Adjusting one orbit
    # preserves eta-invariance and enforces ordinary centering.
    orbit = []
    value = 1
    while value not in orbit:
        orbit.append(value)
        value = value * eta % RIGHT
    orbit_size = len(orbit)
    correction = sum(out) * pow(orbit_size, -1, q) % q
    for value in orbit:
        out[value - 1] = (out[value - 1] - correction) % q
    return out


def all_zero(matrix: list[list[int]], q: int = FIELD_Q) -> bool:
    return all(value % q == 0 for row in matrix for value in row)


def main() -> None:
    logs = log_table()
    cosets = h_cosets(logs)
    indicators = h_indicator_columns(cosets)
    indicator_rank = rank_mod_q(transpose(indicators), FIELD_Q)
    all_ones_in_indicator_span = rank_mod_q(
        transpose(indicators),
        FIELD_Q,
    ) == rank_mod_q(transpose(indicators) + [[1] * (RIGHT - 1)], FIELD_Q)

    rng = random.Random(20260606)
    h_orthogonal = [
        random_h_orthogonal_row(rng, cosets)
        for _row in range(LEFT_ROWS)
    ]
    centered_control = [
        random_centered_row(rng)
        for _row in range(LEFT_ROWS)
    ]
    eta = pow(P24, 156, RIGHT)
    eta_invariant = [
        random_eta_invariant_centered_row(rng, eta)
        for _row in range(LEFT_ROWS)
    ]

    h_orthogonal_sums = matrix_times_h_indicators(h_orthogonal, cosets)
    centered_control_sums = matrix_times_h_indicators(centered_control, cosets)
    eta_invariant_sums = matrix_times_h_indicators(eta_invariant, cosets)

    h_orthogonal_rank = rank_mod_q(h_orthogonal, FIELD_Q)
    centered_control_rank = rank_mod_q(centered_control, FIELD_Q)
    centered_h_leak_rank = rank_mod_q(centered_control_sums, FIELD_Q)

    eta_log_shift = logs[eta] % H_STEP
    eta_shift_generates_quotient = len({(i * eta_log_shift) % H_STEP for i in range(H_STEP)})

    print("Trace-GCD fixed-frequency H-kernel inclusion gate")
    print(f"field_q={FIELD_Q}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"p24_p156_mod_211={eta}")
    print(f"p24_p156_h_quotient_shift={eta_log_shift}")
    print(f"p156_shift_orbit_size_on_h_quotient={eta_shift_generates_quotient}")
    print(f"h_coset_count={len(cosets)}")
    print(f"h_coset_size={len(cosets[0])}")
    print(f"h_indicator_rank={indicator_rank}")
    print(f"all_ones_vector_in_h_indicator_span={int(all_ones_in_indicator_span)}")
    print(f"h_orthogonal_dimension={RIGHT - 1 - indicator_rank}")
    print(f"h_orthogonal_random_matrix_rank={h_orthogonal_rank}")
    print(f"centered_control_matrix_rank={centered_control_rank}")
    print(f"centered_control_h_leak_rank={centered_h_leak_rank}")
    print(f"h_orthogonal_has_zero_h_sums={int(all_zero(h_orthogonal_sums))}")
    print(f"centered_control_has_nonzero_h_sums={int(not all_zero(centered_control_sums))}")
    print(f"eta_invariant_centered_has_zero_h_sums={int(all_zero(eta_invariant_sums))}")
    print("interpretation")
    print("  h_coset_equations_are_right_kernel_inclusion=1")
    print("  p24_scalar_equations=1092")
    print("  h_period_indicator_subspace_dimension=7")
    print("  rowspace_h_orthogonal_dimension=203")
    print("  h_kernel_inclusion_is_compatible_with_full_156_rank=1")
    print("  full_rank_centering_does_not_imply_h_kernel_inclusion=1")
    print("  p156_multiplier_invariance_would_imply_h_kernel_inclusion=1")
    print("  p156_multiplier_invariance_is_sufficient_but_not_the_cm_theorem=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_h_kernel_inclusion_gate")

    if indicator_rank != H_STEP:
        raise SystemExit(1)
    if not all_ones_in_indicator_span:
        raise SystemExit(1)
    if h_orthogonal_rank != LEFT_ROWS:
        raise SystemExit(1)
    if centered_control_rank != LEFT_ROWS or centered_h_leak_rank != H_STEP - 1:
        raise SystemExit(1)
    if not all_zero(h_orthogonal_sums) or all_zero(centered_control_sums):
        raise SystemExit(1)
    if eta_shift_generates_quotient != H_STEP or not all_zero(eta_invariant_sums):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
