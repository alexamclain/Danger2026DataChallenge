#!/usr/bin/env python3
"""Gaussian-period selector boundary for the H-coboundary target.

The base-field H-coboundary theorem says that each row of the centered
`157 x 211` mixed marginal is orthogonal to the seven H-coset indicators in
the right additive coordinate, where

    H = <2^7> <= (Z/211Z)^*,     |H| = 30.

This script records the additive Fourier shape of those selectors.  The
nontrivial quotient-character selectors have full additive support: their
Fourier coefficients are ordinary Gauss sums, nonzero at every nonzero
additive frequency.  So the theorem is not a sparse right-frequency shortcut;
it is a full-support Gaussian-period cancellation identity.
"""

from __future__ import annotations


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
FIELD_Q = 8863  # 8863 - 1 = 42 * 211, contains mu_211 and mu_7.


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


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


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("GEN is not primitive")
    return logs


def h_cosets(logs: dict[int, int]) -> list[list[int]]:
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % H_STEP == residue],
            key=logs.__getitem__,
        )
        for residue in range(H_STEP)
    ]


def indicator_rows(cosets: list[list[int]]) -> list[list[int]]:
    rows: list[list[int]] = []
    for coset in cosets:
        row = [0] * RIGHT
        for value in coset:
            row[value] = 1
        rows.append(row)
    return rows


def additive_dft(row: list[int], zeta211: int) -> list[int]:
    return [
        sum(row[s] * pow(zeta211, (v * s) % RIGHT, FIELD_Q) for s in range(RIGHT)) % FIELD_Q
        for v in range(RIGHT)
    ]


def quotient_character_rows(cosets: list[list[int]], zeta7: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for k in range(1, H_STEP):
        row = [0] * RIGHT
        for residue, coset in enumerate(cosets):
            weight = pow(zeta7, k * residue % H_STEP, FIELD_Q)
            for value in coset:
                row[value] = weight
        rows.append(row)
    return rows


def support_size(values: list[int]) -> int:
    return sum(1 for value in values if value % FIELD_Q != 0)


def orbit_length_additive_shift(shift: int, modulus: int) -> int:
    value = 0
    for length in range(1, modulus + 1):
        value = (value + shift) % modulus
        if value == 0:
            return length
    raise RuntimeError("bad additive shift")


def main() -> None:
    logs = log_table()
    cosets = h_cosets(logs)
    root = primitive_root(FIELD_Q)
    zeta211 = pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // H_STEP, FIELD_Q)
    p_log = logs[P24 % RIGHT]
    p_shift = p_log % H_STEP

    indicators = indicator_rows(cosets)
    center = [[1 if value else 0 for value in range(RIGHT)]]
    indicator_rank = rank_mod([row[1:] for row in indicators], FIELD_Q)
    center_rank = rank_mod([row[1:] for row in center], FIELD_Q)
    combined_rank = rank_mod([row[1:] for row in indicators + center], FIELD_Q)

    indicator_supports = [support_size(additive_dft(row, zeta211)) for row in indicators]
    character_rows = quotient_character_rows(cosets, zeta7)
    character_dfts = [additive_dft(row, zeta211) for row in character_rows]
    character_zero_frequency_values = [values[0] for values in character_dfts]
    character_nonzero_supports = [support_size(values[1:]) for values in character_dfts]
    character_total_supports = [support_size(values) for values in character_dfts]

    print("Trace-GCD fixed-frequency H-coset selector boundary")
    print(f"field_q={FIELD_Q}")
    print(f"field_primitive_root={root}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={GEN}")
    print(f"h_step={H_STEP}")
    print(f"h_coset_count={len(cosets)}")
    print(f"h_coset_size={len(cosets[0])}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p24_h_quotient_frobenius_shift={p_shift}")
    print(f"p24_h_quotient_frobenius_orbit_length={orbit_length_additive_shift(p_shift, H_STEP)}")
    print(f"h_indicator_rank={indicator_rank}")
    print(f"ordinary_centering_rank={center_rank}")
    print(f"h_constraints_extra_rank_over_centering={combined_rank - center_rank}")
    print(f"h_indicator_additive_fourier_supports={indicator_supports}")
    print(f"quotient_character_zero_frequency_values={character_zero_frequency_values}")
    print(f"quotient_character_nonzero_additive_supports={character_nonzero_supports}")
    print(f"quotient_character_total_additive_supports={character_total_supports}")
    print("interpretation")
    print("  h_coset_constraints_are_six_new_centered_equations=1")
    print("  nontrivial_quotient_characters_have_full_nonzero_additive_support=1")
    print("  h_coboundary_is_not_a_sparse_right_frequency_shortcut=1")
    print("  p24_target_is_full_support_gaussian_period_cancellation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_h_coset_selector_boundary")

    if (p_log, p_shift, orbit_length_additive_shift(p_shift, H_STEP)) != (198, 2, 7):
        raise SystemExit(1)
    if (indicator_rank, center_rank, combined_rank - center_rank) != (7, 1, 6):
        raise SystemExit(1)
    if any(value != 0 for value in character_zero_frequency_values):
        raise SystemExit(1)
    if any(support != RIGHT - 1 for support in character_nonzero_supports):
        raise SystemExit(1)
    if any(support != RIGHT - 1 for support in character_total_supports):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
