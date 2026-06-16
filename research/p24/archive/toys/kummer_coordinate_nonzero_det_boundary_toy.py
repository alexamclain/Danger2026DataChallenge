#!/usr/bin/env python3
"""Coordinatewise Kummer nonzero is not determinant nonzero.

The direct trace-GCD route would like to use relative Kummer p-units to prove
that a determinant section is nonzero.  The finite Kummer bridge proves only
that primitive relative traces are nonzero.  This toy demonstrates the gap:
one can have every primitive Kummer coordinate nonzero while a determinant
built from those coordinates vanishes by row dependence.

It reuses the D=-5000 degree-3 calibration tower traces from
``relative_kummer_nonvanishing_bridge_toy.py``.
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
    f2_add,
    f2_mul,
    f2_pow,
    f2_scalar_mul,
)


Fq2 = tuple[int, int]


def f2_sub(x: Fq2, y: Fq2, q: int = Q) -> Fq2:
    return ((x[0] - y[0]) % q, (x[1] - y[1]) % q)


def det2(matrix: list[list[Fq2]]) -> Fq2:
    return f2_sub(
        f2_mul(matrix[0][0], matrix[1][1], Q),
        f2_mul(matrix[0][1], matrix[1][0], Q),
        Q,
    )


def product(values: list[Fq2]) -> Fq2:
    out = (1, 0)
    for value in values:
        out = f2_mul(out, value, Q)
    return out


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
    kummer_rows: list[list[Fq2]] = []
    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        traces = relative_traces(children, zeta)
        primitive = traces[1:]
        primitive_rows.append(primitive)
        kummer_rows.append([f2_pow(value, RELATIVE_DEGREE, Q) for value in primitive])

    scale = (17, 0)
    rank_one_matrix = [
        primitive_rows[0],
        [f2_mul(scale, value, Q) for value in primitive_rows[0]],
    ]
    rank_one_kummers = [
        [f2_pow(value, RELATIVE_DEGREE, Q) for value in row]
        for row in rank_one_matrix
    ]
    actual_parent_matrix = [primitive_rows[0], primitive_rows[1]]

    print("Kummer coordinate nonzero determinant boundary toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print(f"zeta_pair={zeta}")
    print()
    print("actual_parent_primitive_trace_rows")
    for parent, row in enumerate(primitive_rows):
        print(f"  parent={parent} traces={row}")
        print(f"  parent={parent} kummer_powers={kummer_rows[parent]}")
        print(
            f"  parent={parent} primitive_product="
            f"{product(row)} kummer_product={product(kummer_rows[parent])}"
        )
    print(f"  actual_parent_det={det2(actual_parent_matrix)}")
    print()
    print("rank_one_control")
    print(f"  scale={scale}")
    print(f"  matrix={rank_one_matrix}")
    print(f"  kummer_powers={rank_one_kummers}")
    print(f"  all_entries_nonzero={int(all(value != (0, 0) for row in rank_one_matrix for value in row))}")
    print(f"  all_kummers_nonzero={int(all(value != (0, 0) for row in rank_one_kummers for value in row))}")
    print(f"  determinant={det2(rank_one_matrix)}")
    print(f"  determinant_zero_with_nonzero_kummers={int(det2(rank_one_matrix) == (0, 0))}")
    print()
    print("interpretation")
    print("  coordinatewise_kummer_punits_do_not_imply_determinant_punit=1")
    print("  p24_needs_plucker_or_fitting_kummer_zero_detection=1")
    print("conclusion=reported_kummer_coordinate_nonzero_det_boundary_toy")


if __name__ == "__main__":
    main()
