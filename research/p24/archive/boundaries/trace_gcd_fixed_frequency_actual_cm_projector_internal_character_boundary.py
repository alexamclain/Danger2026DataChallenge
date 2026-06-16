#!/usr/bin/env python3
"""Actual-CM boundary for projector plus internal-character trace zero.

The p24 target now asks for final internal trace zero in each nontrivial
right-projector channel after the B/C trace.  A too-optimistic theorem would
say that any nontrivial quotient projector kills the trivial internal
component.

This checks that claim on the small embedded CM calibration

    D=-5000, h=30 = 2 * 5 * 3.

The top quotient has order 2, the C/E analogue has degree 5, and B/C has
degree 3.  For each origin, the nontrivial top projector is the difference of
the two top packets.  Its final internal trace is generically nonzero.  So the
p24 proof cannot be "nontrivial quotient projector implies no trivial C
component"; it must use the specific weighted right/G_chi packet structure.
"""

from __future__ import annotations

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


def packet_value(cycle: list[int], top_index: int, c_index: int, b_index: int) -> int:
    raw_index = top_index + TOP_QUOTIENT * (c_index + TOY_C_DEGREE * b_index)
    return cycle[raw_index % H]


def b_over_c_trace(cycle: list[int], top_index: int) -> list[int]:
    buckets: list[int] = []
    for c_index in range(TOY_C_DEGREE):
        total = 0
        for b_index in range(TOY_B_OVER_C_DEGREE):
            total = (total + packet_value(cycle, top_index, c_index, b_index)) % Q
        buckets.append(total)
    return buckets


def final_trace(bucket_sums: list[int]) -> int:
    return sum(bucket_sums) % Q


def nontrivial_top_projected_b_trace(cycle: list[int]) -> list[int]:
    even = b_over_c_trace(cycle, 0)
    odd = b_over_c_trace(cycle, 1)
    return [(even_value - odd_value) % Q for even_value, odd_value in zip(even, odd)]


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    projected_final_zeroes = 0
    projected_final_nonzeroes = 0
    projected_b_trace_nonzeroes = 0
    raw_top_final_zeroes = 0
    rows_checked = 0
    samples: list[tuple[int, list[int], int]] = []

    for origin_shift in range(H):
        shifted = rotate(cycle, origin_shift)
        projected_b = nontrivial_top_projected_b_trace(shifted)
        projected_final = final_trace(projected_b)
        projected_final_zeroes += int(projected_final == 0)
        projected_final_nonzeroes += int(projected_final != 0)
        projected_b_trace_nonzeroes += int(any(projected_b))
        for top_index in range(TOP_QUOTIENT):
            raw_top_final_zeroes += int(final_trace(b_over_c_trace(shifted, top_index)) == 0)
        rows_checked += 1
        if len(samples) < 4:
            samples.append((origin_shift, projected_b, projected_final))

    print("Trace-GCD fixed-frequency actual-CM projector/internal-character boundary")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell_generator_norm={ELL}")
    print(f"class_number={H}")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"origins_checked={rows_checked}")
    print(f"projected_B_over_C_trace_nonzeroes={projected_b_trace_nonzeroes}/{rows_checked}")
    print(f"projected_final_trace_zeroes={projected_final_zeroes}/{rows_checked}")
    print(f"projected_final_trace_nonzeroes={projected_final_nonzeroes}/{rows_checked}")
    print(f"raw_top_final_trace_zeroes={raw_top_final_zeroes}/{rows_checked * TOP_QUOTIENT}")
    for index, (origin_shift, projected_b, projected_final) in enumerate(samples):
        print(
            f"sample_{index}=origin:{origin_shift},"
            f"projected_B_trace:{projected_b},projected_final:{projected_final}"
        )
    print("interpretation")
    print("  nontrivial_top_projector_does_not_force_internal_trace_zero=1")
    print("  actual_cm_projector_channel_can_have_trivial_C_component=1")
    print("  p24_needs_specific_weighted_G_chi_packet_not_generic_projector=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary")

    if len(cycle) != H:
        raise SystemExit(1)
    if rows_checked != H:
        raise SystemExit(1)
    if projected_b_trace_nonzeroes != rows_checked:
        raise SystemExit(1)
    if projected_final_nonzeroes == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
