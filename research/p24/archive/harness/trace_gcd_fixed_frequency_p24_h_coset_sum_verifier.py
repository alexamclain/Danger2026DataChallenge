#!/usr/bin/env python3
"""Explicit p24 verifier interface for the 1092 H-coset equations.

The proposed fixed-frequency theorem reduces to the base-field identities

    sum_{s in qH} C(r,s) = 0

for 156 left rows and 7 cosets of H=<2^7> in `(Z/211Z)^*`.  This script does
not compute the p24 CM marginal `C(r,s)`; doing that by class-set enumeration
would defeat the point.  It records the exact deterministic verifier surface
that any tower-native construction must hit:

    full input:       156 x 210 centered marginal columns;
    compressed input: 156 x 7 H-coset sums;
    accept iff all 1092 scalar equations vanish in F_p.
"""

from __future__ import annotations

from math import isqrt
import random


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
LEFT_ROWS = 156
NONZERO_RIGHT_COLUMNS = RIGHT - 1
EQUATION_COUNT = LEFT_ROWS * H_STEP


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("GEN is not primitive modulo 211")
    return logs


def h_cosets(logs: dict[int, int]) -> list[list[int]]:
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % H_STEP == residue],
            key=logs.__getitem__,
        )
        for residue in range(H_STEP)
    ]


def h_coset_sums(row: list[int], cosets: list[list[int]], modulus: int = P24) -> list[int]:
    return [sum(row[value] for value in coset) % modulus for coset in cosets]


def compressed_sums(matrix: list[list[int]], cosets: list[list[int]], modulus: int = P24) -> list[list[int]]:
    if len(matrix) != LEFT_ROWS:
        raise ValueError("expected 156 left rows")
    if any(len(row) != RIGHT for row in matrix):
        raise ValueError("expected rows indexed by residues 0..210")
    return [h_coset_sums(row, cosets, modulus) for row in matrix]


def verify_direct_sums(sums: list[list[int]], modulus: int = P24) -> bool:
    if len(sums) != LEFT_ROWS:
        return False
    if any(len(row) != H_STEP for row in sums):
        return False
    return all(value % modulus == 0 for row in sums for value in row)


def verify_centered_marginal(matrix: list[list[int]], cosets: list[list[int]], modulus: int = P24) -> bool:
    return verify_direct_sums(compressed_sums(matrix, cosets, modulus), modulus)


def first_nonzero_equation(sums: list[list[int]], modulus: int = P24) -> tuple[int, int, int] | None:
    for row_index, row in enumerate(sums):
        for coset_index, value in enumerate(row):
            residue = value % modulus
            if residue:
                return row_index, coset_index, residue
    return None


def random_centered_matrix(rng: random.Random) -> list[list[int]]:
    matrix: list[list[int]] = []
    for _row in range(LEFT_ROWS):
        row = [0] + [rng.randrange(P24) for _value in range(1, RIGHT)]
        row[1] = (row[1] - sum(row[1:])) % P24
        matrix.append(row)
    return matrix


def force_h_coset_sums_zero(matrix: list[list[int]], cosets: list[list[int]]) -> list[list[int]]:
    adjusted = [row[:] for row in matrix]
    for row in adjusted:
        for coset in cosets:
            row[coset[0]] = (row[coset[0]] - sum(row[value] for value in coset)) % P24
    return adjusted


def corrupt_one_entry(matrix: list[list[int]]) -> list[list[int]]:
    corrupted = [row[:] for row in matrix]
    corrupted[0][1] = (corrupted[0][1] + 1) % P24
    return corrupted


def main() -> None:
    logs = log_table()
    cosets = h_cosets(logs)
    rng = random.Random(20260606)
    p_log = logs[P24 % RIGHT]
    sqrt_floor = isqrt(P24)

    centered = random_centered_matrix(rng)
    forced = force_h_coset_sums_zero(centered, cosets)
    corrupted = corrupt_one_entry(forced)

    forced_sums = compressed_sums(forced, cosets)
    corrupted_sums = compressed_sums(corrupted, cosets)
    zero_direct = [[0] * H_STEP for _row in range(LEFT_ROWS)]
    corrupt_direct = [row[:] for row in zero_direct]
    corrupt_direct[17][3] = 1

    random_centered_accepts = verify_centered_marginal(centered, cosets)
    forced_accepts = verify_centered_marginal(forced, cosets)
    corrupted_accepts = verify_centered_marginal(corrupted, cosets)
    zero_direct_accepts = verify_direct_sums(zero_direct)
    corrupt_direct_accepts = verify_direct_sums(corrupt_direct)

    first_failure = first_nonzero_equation(corrupted_sums)

    print("Trace-GCD fixed-frequency p24 H-coset sum verifier")
    print(f"p24={P24}")
    print(f"sqrt_floor={sqrt_floor}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={GEN}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"h_generator=2^{H_STEP}_mod_211={pow(GEN, H_STEP, RIGHT)}")
    print(f"left_rows={LEFT_ROWS}")
    print(f"nonzero_right_columns={NONZERO_RIGHT_COLUMNS}")
    print(f"h_coset_count={len(cosets)}")
    print(f"h_coset_size={len(cosets[0])}")
    print(f"full_marginal_scalar_entries={LEFT_ROWS * NONZERO_RIGHT_COLUMNS}")
    print(f"compressed_h_coset_sum_entries={EQUATION_COUNT}")
    print(f"p24_scalar_equations={EQUATION_COUNT}")
    print(f"sqrt_floor_div_scalar_equations={sqrt_floor // EQUATION_COUNT}")
    print(f"random_centered_rejected={int(not random_centered_accepts)}")
    print(f"forced_h_coset_zero_accepted={int(forced_accepts)}")
    print(f"corrupted_marginal_rejected={int(not corrupted_accepts)}")
    print(f"zero_direct_sums_accepted={int(zero_direct_accepts)}")
    print(f"corrupt_direct_sums_rejected={int(not corrupt_direct_accepts)}")
    print(f"first_corrupted_failure={first_failure}")
    print("interpretation")
    print("  p24_h_coset_verifier_checks_1092_scalar_equations=1")
    print("  compressed_input_is_156_by_7_coset_sum_matrix=1")
    print("  full_marginal_input_is_156_by_210_centered_matrix=1")
    print("  verifier_does_not_compute_cm_class_set=1")
    print("  tower_proof_must_supply_zero_h_coset_sums=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_h_coset_sum_verifier")

    if (p_log, len(cosets), len(cosets[0])) != (198, H_STEP, 30):
        raise SystemExit(1)
    if EQUATION_COUNT != 1092 or LEFT_ROWS * NONZERO_RIGHT_COLUMNS != 32760:
        raise SystemExit(1)
    if random_centered_accepts:
        raise SystemExit(1)
    if not forced_accepts or corrupted_accepts:
        raise SystemExit(1)
    if not zero_direct_accepts or corrupt_direct_accepts:
        raise SystemExit(1)
    if first_failure is None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
