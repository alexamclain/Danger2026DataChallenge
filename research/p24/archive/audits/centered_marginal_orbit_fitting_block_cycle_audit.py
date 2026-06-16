#!/usr/bin/env python3
"""Actual-CM block-cycle audit for centered orbit Fitting determinants.

The centered crossed-product target packages a right Frobenius orbit product

    prod_{t in O} Delta_C(t)

as one phase-aware Fitting determinant.  This audit checks the finite
determinant-line plumbing on the pinned actual-CM row by building the actual
centered Schubert window matrices and placing the matrices in a block-cycle
operator.

It does not prove the p-unit theorem.  It verifies the sign and
zero-detection conventions that a future class-field/Borcherds producer must
hit without expanding the p24 5460-by-5460 orbit matrices.
"""

from __future__ import annotations

from centered_marginal_cyclic_code_boundary import affine_window_det, point_matrix
from centered_marginal_full_origin_phase_sensitivity_gate import (
    matching_factor,
    pinned_args,
)
from centered_marginal_origin_product_audit import product_mod, scan
from block_cycle_fitting_zero_detection_toy import block_cycle_matrix, det_mod, rank_mod
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from relative_moment_projection_scan import section_fiber_polynomials


def window_matrix(points: list[list[int]], start: int, width: int, q: int) -> list[list[int]]:
    out: list[list[int]] = []
    right = len(points[0])
    for row in points:
        base = row[start % right]
        out.append([(row[(start + offset) % right] - base) % q for offset in range(1, width + 1)])
    return out


def block_diagonal(matrices: list[list[list[int]]], q: int) -> list[list[int]]:
    block_size = len(matrices[0])
    total = block_size * len(matrices)
    out = [[0 for _ in range(total)] for _ in range(total)]
    for block, matrix in enumerate(matrices):
        offset = block * block_size
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                out[offset + i][offset + j] = value % q
    return out


def make_singular(matrix: list[list[int]]) -> list[list[int]]:
    out = [row[:] for row in matrix]
    if len(out) > 1:
        out[-1] = out[0][:]
    else:
        out[0] = [0]
    return out


def main() -> None:
    row = scan(pinned_args())
    if row is None:
        raise SystemExit("pinned row not found")
    factor = matching_factor(row)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(list(row.cycle), row.q, row.m, "complement")
    ]
    marginal = double_marginal(kernel_matrix(residues, factor, row.q), row.left, row.right, row.q)
    points = point_matrix(marginal, row.left, row.right, row.q)
    width = row.left - 1
    windows = [window_matrix(points, start, width, row.q) for start in range(row.right)]
    window_dets = [det_mod(matrix, row.q) for matrix in windows]
    affine_dets = [affine_window_det(points, start, width, row.q) for start in range(row.right)]

    orbits = [[0]] + q_orbits(row.right, row.q)
    determinant_mismatches = 0
    direct_sum_mismatches = 0
    zero_detection_failures = 0
    singular_control_failures = 0
    full_rank_iff_failures = 0

    print("Centered marginal orbit-Fitting block-cycle audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"window_width={width}")
    print(f"window_det_values={window_dets}")
    print(f"affine_window_det_mismatches={sum(1 for a, b in zip(window_dets, affine_dets) if a != b)}")

    for orbit in orbits:
        matrices = [windows[index] for index in orbit]
        dets = [window_dets[index] for index in orbit]
        product = product_mod(dets, row.q)
        direct = det_mod(block_diagonal(matrices, row.q), row.q)
        cycle = block_cycle_matrix(matrices, row.q)
        cycle_det = det_mod(cycle, row.q)
        cycle_rank = rank_mod(cycle, row.q)
        sign = 1 if (width * (len(orbit) - 1)) % 2 == 0 else -1
        expected_cycle = product if sign == 1 else (-product) % row.q
        determinant_mismatches += int(cycle_det != expected_cycle)
        direct_sum_mismatches += int(direct != product)
        zero_detection_failures += int((cycle_det == 0) != any(det == 0 for det in dets))
        full_rank_iff_failures += int((cycle_rank == len(cycle)) != all(det != 0 for det in dets))

        singular_matrices = matrices[:]
        singular_matrices[0] = make_singular(singular_matrices[0])
        singular_cycle_det = det_mod(block_cycle_matrix(singular_matrices, row.q), row.q)
        singular_control_failures += int(singular_cycle_det != 0)

        print(f"orbit={orbit}")
        print(f"  orbit_len={len(orbit)}")
        print(f"  local_dets={dets}")
        print(f"  orbit_product={product}")
        print(f"  direct_sum_det={direct}")
        print(f"  block_cycle_sign={sign}")
        print(f"  block_cycle_det={cycle_det}")
        print(f"  expected_block_cycle_det={expected_cycle}")
        print(f"  block_cycle_full_rank={int(cycle_rank == len(cycle))}")
        print(f"  singular_control_block_cycle_det={singular_cycle_det}")

    print("totals")
    print(f"orbit_count={len(orbits)}")
    print(f"determinant_mismatches={determinant_mismatches}")
    print(f"direct_sum_mismatches={direct_sum_mismatches}")
    print(f"zero_detection_failures={zero_detection_failures}")
    print(f"full_rank_iff_failures={full_rank_iff_failures}")
    print(f"singular_control_failures={singular_control_failures}")
    print("interpretation")
    print("  actual_centered_orbit_product_equals_direct_sum_fitting_det=1")
    print("  actual_centered_orbit_product_equals_signed_block_cycle_fitting_det=1")
    print("  block_cycle_zero_detects_orbit_schubert_zero=1")
    print("  crossed_product_fitting_plumbing_is_not_the_missing_arithmetic=1")
    print("conclusion=reported_centered_marginal_orbit_fitting_block_cycle_audit")

    if (row.D, row.q, row.m, row.n, row.left, row.right) != (-13319, 13463, 28, 5, 4, 7):
        raise SystemExit(1)
    if window_dets != affine_dets:
        raise SystemExit(1)
    if determinant_mismatches or direct_sum_mismatches:
        raise SystemExit(1)
    if zero_detection_failures or full_rank_iff_failures or singular_control_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
