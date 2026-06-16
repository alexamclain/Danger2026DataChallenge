#!/usr/bin/env python3
"""p24 contract between the tower theorem and the 1092 scalar verifier.

The cheap verifier checks seven H-coset sums for each of 156 left coordinates.
This script records the exact finite Fourier contract that makes those checks
usable without materializing the full CM marginal:

* ordinary centering gives the trivial quotient character;
* the tower theorem must give the six nontrivial order-7 character sums;
* over F_p, these seven character equations are exactly the seven H-coset
  scalar equations.

The script deliberately does not compute any CM class-set data.  It only
checks the p24 quotient-character linear algebra and the failure modes that
would make a "1092 checks" claim too weak.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
H_STEP = 7
LEFT_ROWS = 156
NONZERO_RIGHT_COLUMNS = RIGHT - 1


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    rows = [
        [entry % modulus for entry in row]
        for row in matrix
        if any(entry % modulus for entry in row)
    ]
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
        inv = pow(rows[rank][col], -1, modulus)
        rows[rank] = [entry * inv % modulus for entry in rows[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    (entry - scale * pivot_entry) % modulus
                    for entry, pivot_entry in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def primitive_7th_root() -> int:
    if (P24 - 1) % H_STEP:
        raise RuntimeError("p24 does not contain seventh roots of unity")
    exponent = (P24 - 1) // H_STEP
    for candidate in range(2, 10_000):
        root = pow(candidate, exponent, P24)
        if root != 1 and pow(root, H_STEP, P24) == 1:
            return root
    raise RuntimeError("failed to find a nontrivial seventh root")


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


def character_matrix(zeta: int) -> list[list[int]]:
    return [
        [pow(zeta, (character * residue) % H_STEP, P24) for residue in range(H_STEP)]
        for character in range(H_STEP)
    ]


def projections(coset_sums: list[int], zeta: int) -> list[int]:
    return [
        sum(
            coset_sums[residue] * pow(zeta, (character * residue) % H_STEP, P24)
            for residue in range(H_STEP)
        )
        % P24
        for character in range(H_STEP)
    ]


def is_zero_vector(values: list[int]) -> bool:
    return all(value % P24 == 0 for value in values)


def random_coset_vector(rng: random.Random) -> list[int]:
    return [rng.randrange(P24) for _ in range(H_STEP)]


def random_centered_coset_vector(rng: random.Random) -> list[int]:
    values = [rng.randrange(P24) for _ in range(H_STEP - 1)]
    values.append((-sum(values)) % P24)
    return values


def inverse_character_basis(character: int, zeta: int) -> list[int]:
    return [
        pow(zeta, (-character * residue) % H_STEP, P24)
        for residue in range(H_STEP)
    ]


def main() -> None:
    logs = log_table()
    cosets = h_cosets(logs)
    zeta = primitive_7th_root()
    matrix = character_matrix(zeta)
    nontrivial_matrix = matrix[1:]
    nontrivial_plus_center = [matrix[0]] + matrix[1:]
    rng = random.Random(20260606)

    random_equivalence_trials = 64
    full_equivalence_failures = 0
    centered_equivalence_failures = 0
    for _trial in range(random_equivalence_trials):
        values = random_coset_vector(rng)
        if is_zero_vector(values) != is_zero_vector(projections(values, zeta)):
            full_equivalence_failures += 1
        centered = random_centered_coset_vector(rng)
        nontrivial_zero = is_zero_vector(projections(centered, zeta)[1:])
        if is_zero_vector(centered) != nontrivial_zero:
            centered_equivalence_failures += 1

    constant_leak = [1] * H_STEP
    constant_leak_projections = projections(constant_leak, zeta)

    missing_character = 3
    missing_character_control = inverse_character_basis(missing_character, zeta)
    missing_character_projections = projections(missing_character_control, zeta)
    missing_character_passes_other_nontrivial = all(
        value % P24 == 0
        for character, value in enumerate(missing_character_projections)
        if character not in (0, missing_character)
    )

    p_log = logs[P24 % RIGHT]
    p_h_shift = p_log % H_STEP
    full_marginal_entries = LEFT_ROWS * NONZERO_RIGHT_COLUMNS
    nontrivial_l_equation_scalars = LEFT_ROWS * (H_STEP - 1)
    centering_scalars = LEFT_ROWS
    verifier_scalars = LEFT_ROWS * H_STEP

    print("Trace-GCD fixed-frequency p24 character payload contract")
    print(f"p24={P24}")
    print(f"p24_mod_7={P24 % H_STEP}")
    print(f"right={RIGHT}")
    print(f"h_coset_count={len(cosets)}")
    print(f"h_coset_size={len(cosets[0])}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p24_h_quotient_frobenius_shift={p_h_shift}")
    print(f"zeta7={zeta}")
    print(f"zeta7_order_check={pow(zeta, H_STEP, P24)}")
    print(f"character_matrix_rank={rank_mod(matrix, P24)}")
    print(f"nontrivial_character_rank={rank_mod(nontrivial_matrix, P24)}")
    print(f"nontrivial_plus_center_rank={rank_mod(nontrivial_plus_center, P24)}")
    print(f"random_full_fourier_equivalence_failures={full_equivalence_failures}")
    print(f"random_centered_nontrivial_equivalence_failures={centered_equivalence_failures}")
    print(
        "constant_vector_passes_nontrivial_characters_without_centering="
        f"{int(is_zero_vector(constant_leak_projections[1:]))}"
    )
    print(
        "constant_vector_has_nonzero_trivial_character="
        f"{int(constant_leak_projections[0] % P24 != 0)}"
    )
    print(
        "missing_one_nontrivial_character_control_passes_the_other_five="
        f"{int(missing_character_passes_other_nontrivial)}"
    )
    print(
        "missing_one_nontrivial_character_control_is_nonzero="
        f"{int(not is_zero_vector(missing_character_control))}"
    )
    print(f"full_marginal_scalar_entries={full_marginal_entries}")
    print(f"six_nontrivial_L_equations_scalar_count={nontrivial_l_equation_scalars}")
    print(f"ordinary_centering_scalar_count={centering_scalars}")
    print(f"p24_scalar_equations={verifier_scalars}")
    print("interpretation")
    print("  ordinary_centering_plus_six_character_sums_equiv_h_coset_zero=1")
    print("  six_L_valued_character_identities_are_the_nontrivial_payload=1")
    print("  verifier_stage_checks_1092_scalars_after_payload_generation=1")
    print("  full_marginal_materialization_is_not_a_subsqrt_certificate=1")
    print("  omitting_centering_or_one_character_leaves_false_positives=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_character_payload_contract")

    if len(cosets) != H_STEP or len(cosets[0]) != 30:
        raise SystemExit(1)
    if (p_log, p_h_shift) != (198, 2):
        raise SystemExit(1)
    if pow(zeta, H_STEP, P24) != 1 or zeta == 1:
        raise SystemExit(1)
    if rank_mod(matrix, P24) != H_STEP:
        raise SystemExit(1)
    if rank_mod(nontrivial_matrix, P24) != H_STEP - 1:
        raise SystemExit(1)
    if rank_mod(nontrivial_plus_center, P24) != H_STEP:
        raise SystemExit(1)
    if full_equivalence_failures or centered_equivalence_failures:
        raise SystemExit(1)
    if not is_zero_vector(constant_leak_projections[1:]):
        raise SystemExit(1)
    if constant_leak_projections[0] % P24 == 0:
        raise SystemExit(1)
    if not missing_character_passes_other_nontrivial:
        raise SystemExit(1)
    if is_zero_vector(missing_character_control):
        raise SystemExit(1)
    if nontrivial_l_equation_scalars + centering_scalars != verifier_scalars:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
