#!/usr/bin/env python3
"""Toy check for the Lang trace-coordinate origin covariance.

This is a finite-linear-algebra check, not a CM computation.  For a random
left x right marginal table M(a,b), translate both indices by alpha and verify
the predicted action on the DFT + Lang-trivialized right-orbit coordinates:

    H'_{u,v} = zeta^(-alpha*(u*m/left + v*m/right)) H_{u,v}.

After Lang trivialization on a right Frobenius orbit, the right phase becomes
the F_q-linear multiplication matrix by gamma=zeta^(-alpha*v0*m/right) on the
right cyclotomic subfield.  The left phase is a common nonzero scalar.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from hermitian_mixed_left_subfield_normality_audit import (
    transformed_coordinates_for_left_orbit,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class CovarianceCase:
    q: int
    left: int
    right: int
    alpha: int
    left_orbit_rep: int
    right_orbit_count: int
    mismatch_count: int


def shifted_marginal(
    marginal: list[list[int]], alpha: int, q: int
) -> list[list[int]]:
    left = len(marginal)
    right = len(marginal[0])
    return [
        [
            marginal[(a + alpha) % left][(b + alpha) % right] % q
            for b in range(right)
        ]
        for a in range(left)
    ]


def multiplication_matrix_on_subfield(
    q: int,
    orbit_len: int,
    gamma: FpE,
    field: ExtensionField,
    seed: int,
) -> list[list[FpE]]:
    basis = subfield_power_basis(q, orbit_len, field, seed)
    inverse = lang_inverse_for_orbit(q, orbit_len, field, seed)
    columns: list[list[FpE]] = []
    for basis_value in basis:
        conjugates = [
            field.pow(field.mul(gamma, basis_value), field.q**row)
            for row in range(orbit_len)
        ]
        columns.append(matrix_vector_mul(inverse, conjugates, field))
    return [
        [columns[col][row] for col in range(orbit_len)]
        for row in range(orbit_len)
    ]


def block_ranges(lengths: list[int]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    offset = 0
    for length in lengths:
        ranges.append((offset, offset + length))
        offset += length
    return ranges


def run_case(
    q: int,
    left: int,
    right: int,
    alpha: int,
    seed: int,
) -> CovarianceCase:
    m = left * right
    degree = 1
    while pow(q, degree, m) != 1:
        degree += 1
    modulus = find_irreducible_modulus(q, degree, seed)
    field = ExtensionField(q, degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    powers = zeta_powers(zeta, m, field)

    rng = random.Random(seed + 1009 * q + 37 * left + 41 * right)
    marginal = [[rng.randrange(q) for _ in range(right)] for _ in range(left)]
    shifted = shifted_marginal(marginal, alpha, q)
    dft = dft_double_marginal(marginal, left, right, powers, m, field)
    shifted_dft = dft_double_marginal(shifted, left, right, powers, m, field)

    left_orbits = q_orbits(left, q)
    right_orbits = q_orbits(right, q)
    left_orbit = max(left_orbits, key=len)
    transformed = transformed_coordinates_for_left_orbit(
        dft, left, right, left_orbit, right_orbits, q, field, seed
    )
    shifted_transformed = transformed_coordinates_for_left_orbit(
        shifted_dft, left, right, left_orbit, right_orbits, q, field, seed
    )

    step_left = m // left
    step_right = m // right
    u0 = left_orbit[0]
    left_phase = powers[(-alpha * u0 * step_left) % m]
    ranges = block_ranges([len(orbit) for orbit in right_orbits])
    mismatches = 0
    for orbit, (start, stop) in zip(right_orbits, ranges):
        gamma = powers[(-alpha * orbit[0] * step_right) % m]
        action = multiplication_matrix_on_subfield(
            q, len(orbit), gamma, field, seed
        )
        predicted = matrix_vector_mul(action, transformed[start:stop], field)
        predicted = [field.mul(left_phase, value) for value in predicted]
        actual = shifted_transformed[start:stop]
        mismatches += sum(1 for left_value, right_value in zip(predicted, actual) if left_value != right_value)

    return CovarianceCase(
        q=q,
        left=left,
        right=right,
        alpha=alpha,
        left_orbit_rep=u0,
        right_orbit_count=len(right_orbits),
        mismatch_count=mismatches,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--left", type=int, default=3)
    parser.add_argument("--right", type=int, default=7)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    print("Lang origin covariance toy")
    for alpha in range(args.left * args.right):
        case = run_case(args.q, args.left, args.right, alpha, args.seed)
        print(
            f"alpha={case.alpha} left_orbit={case.left_orbit_rep} "
            f"right_orbits={case.right_orbit_count} "
            f"mismatches={case.mismatch_count}"
        )
        if case.mismatch_count:
            raise SystemExit("covariance mismatch")
    print("conclusion=origin_covariance_formula_verified")


if __name__ == "__main__":
    main()
