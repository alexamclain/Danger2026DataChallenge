#!/usr/bin/env python3
"""Actual-CM boundary for the p24 internal C/E character filter.

The p24 internal-character filter gate says the remaining theorem can be
phrased as zero trivial C/E character component after the B/C trace.  This
script checks whether that condition is a generic feature of embedded CM
period data.  It is not.

We use the small calibration cycle

    D = -5000, h = 30 = 2 * 5 * 3,

with a norm-3 generator over q=3851.  The top quotient of size 2 plays the
role of the raw quotient layer, and the internal layer is split as C=5 and
B/C=3.  For every origin and top packet, the B/C-traced raw j-period vector
has nonzero trivial C-character projection.

Thus the p24 theorem cannot be "ordinary CM periods have no trivial internal
component"; it must use the specific right-obstruction/product-coboundary
structure.
"""

from __future__ import annotations

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)


Q = 3851
TOP_QUOTIENT = 2
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3


def rotate(values: list[int], shift: int) -> list[int]:
    if shift == 0:
        return values[:]
    return values[shift:] + values[:shift]


def primitive_root_of_order(q: int, order: int) -> int:
    generator = int(sp.primitive_root(q))
    root = pow(generator, (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise RuntimeError("bad root order")
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            raise RuntimeError("root is not primitive")
    return root


def c_bucket_sums(cycle: list[int], top_index: int) -> list[int]:
    buckets: list[int] = []
    for c_index in range(TOY_C_DEGREE):
        total = 0
        for b_index in range(TOY_B_OVER_C_DEGREE):
            raw_index = top_index + TOP_QUOTIENT * (c_index + TOY_C_DEGREE * b_index)
            total = (total + cycle[raw_index % H]) % Q
        buckets.append(total)
    return buckets


def c_character_projections(buckets: list[int], omega: int) -> list[int]:
    projections: list[int] = []
    for character_index in range(TOY_C_DEGREE):
        total = 0
        for c_index, value in enumerate(buckets):
            total = (
                total
                + value * pow(omega, (-character_index * c_index) % TOY_C_DEGREE, Q)
            ) % Q
        projections.append(total)
    return projections


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    omega = primitive_root_of_order(Q, TOY_C_DEGREE)

    trivial_zeroes = 0
    all_nontrivial_nonzero = 0
    rows_checked = 0
    samples: list[tuple[int, int, list[int], list[int]]] = []

    for origin_shift in range(H):
        shifted = rotate(cycle, origin_shift)
        for top_index in range(TOP_QUOTIENT):
            buckets = c_bucket_sums(shifted, top_index)
            projections = c_character_projections(buckets, omega)
            trivial_zeroes += int(projections[0] == 0)
            all_nontrivial_nonzero += int(all(value != 0 for value in projections[1:]))
            rows_checked += 1
            if len(samples) < 4:
                samples.append((origin_shift, top_index, buckets, projections))

    print("Trace-GCD fixed-frequency actual-CM internal character boundary")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell_generator_norm={ELL}")
    print(f"class_number={H}")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"primitive_C_root={omega}")
    print(f"rows_checked={rows_checked}")
    print(f"trivial_C_projection_zeroes={trivial_zeroes}/{rows_checked}")
    print(f"trivial_C_projection_nonzeroes={rows_checked - trivial_zeroes}/{rows_checked}")
    print(f"all_nontrivial_C_projections_nonzero={all_nontrivial_nonzero}/{rows_checked}")
    for index, (origin_shift, top_index, buckets, projections) in enumerate(samples):
        print(
            f"sample_{index}=origin:{origin_shift},top:{top_index},"
            f"buckets:{buckets},C_character_projections:{projections}"
        )
    print("interpretation")
    print("  ordinary_cm_periods_do_not_satisfy_internal_character_filter=1")
    print("  internal_filter_needs_specific_obstruction_not_raw_j_cycle=1")
    print("  small_cm_cycle_has_full_C_character_support=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_internal_character_boundary")

    if len(cycle) != H:
        raise SystemExit(1)
    if rows_checked != H * TOP_QUOTIENT:
        raise SystemExit(1)
    if trivial_zeroes != 0:
        raise SystemExit(1)
    if all_nontrivial_nonzero != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
