#!/usr/bin/env python3
"""Plucker-Kummer payload toy.

Coordinate Kummer powers do not prevent determinant cancellation.  If the
Kummer payload is attached to the determinant/Plucker coordinate itself,
however, zero-detection is exact: det(M)^r is nonzero iff det(M) is nonzero.

This toy reuses the D=-5000 degree-3 Kummer calibration rows and contrasts:

1. coordinate Kummers of a rank-one matrix: all nonzero, determinant zero;
2. Plucker Kummer of the same determinant: zero, detecting failure;
3. Plucker Kummer of the actual two-parent matrix: nonzero.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from relative_kummer_nonvanishing_bridge_toy import relative_traces
from relative_tower_character_toy import (
    FINE_QUOTIENT,
    RECOVERY_SIZE,
    RELATIVE_DEGREE,
    TOP_QUOTIENT,
    f2_mul,
    f2_pow,
)
from kummer_coordinate_nonzero_det_boundary_toy import det2


Fq2 = tuple[int, int]


def all_nonzero(matrix: list[list[Fq2]]) -> bool:
    return all(value != (0, 0) for row in matrix for value in row)


def entry_kummers(matrix: list[list[Fq2]], exponent: int) -> list[list[Fq2]]:
    return [[f2_pow(value, exponent, Q) for value in row] for row in matrix]


def main() -> None:
    if RELATIVE_DEGREE != 3:
        raise AssertionError("toy specialized to the degree-3 layer")

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    fine_periods = [
        sum(cycle[(r + FINE_QUOTIENT * k) % H] for k in range(RECOVERY_SIZE)) % Q
        for r in range(FINE_QUOTIENT)
    ]
    zeta = (0, 1)
    primitive_rows: list[list[Fq2]] = []
    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        primitive_rows.append(relative_traces(children, zeta)[1:])

    scale = (17, 0)
    rank_one_matrix = [
        primitive_rows[0],
        [f2_mul(scale, value, Q) for value in primitive_rows[0]],
    ]
    actual_matrix = [primitive_rows[0], primitive_rows[1]]
    exponent = RELATIVE_DEGREE

    rank_one_det = det2(rank_one_matrix)
    actual_det = det2(actual_matrix)
    rank_one_plucker_kummer = f2_pow(rank_one_det, exponent, Q)
    actual_plucker_kummer = f2_pow(actual_det, exponent, Q)
    rank_one_entry_kummers = entry_kummers(rank_one_matrix, exponent)
    actual_entry_kummers = entry_kummers(actual_matrix, exponent)

    print("Plucker-Kummer payload toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print(f"kummer_exponent={exponent}")
    print()
    print("rank_one_control")
    print(f"  matrix={rank_one_matrix}")
    print(f"  entry_kummers={rank_one_entry_kummers}")
    print(f"  all_entries_nonzero={int(all_nonzero(rank_one_matrix))}")
    print(f"  all_entry_kummers_nonzero={int(all_nonzero(rank_one_entry_kummers))}")
    print(f"  determinant={rank_one_det}")
    print(f"  plucker_kummer=det^r={rank_one_plucker_kummer}")
    print(
        "  plucker_kummer_detects_zero="
        f"{int((rank_one_det == (0, 0)) == (rank_one_plucker_kummer == (0, 0)))}"
    )
    print()
    print("actual_parent_matrix")
    print(f"  matrix={actual_matrix}")
    print(f"  entry_kummers={actual_entry_kummers}")
    print(f"  all_entries_nonzero={int(all_nonzero(actual_matrix))}")
    print(f"  all_entry_kummers_nonzero={int(all_nonzero(actual_entry_kummers))}")
    print(f"  determinant={actual_det}")
    print(f"  plucker_kummer=det^r={actual_plucker_kummer}")
    print(
        "  plucker_kummer_detects_zero="
        f"{int((actual_det == (0, 0)) == (actual_plucker_kummer == (0, 0)))}"
    )
    print()
    print("interpretation")
    print("  coordinate_kummers_are_too_weak_for_determinants=1")
    print("  plucker_kummer_attached_to_the_determinant_zero_detects_exactly=1")
    print("  p24_target_is_construct_plucker_kummer_of_f_trace_not_entry_kummers=1")
    print("conclusion=reported_plucker_kummer_payload_toy")


if __name__ == "__main__":
    main()
