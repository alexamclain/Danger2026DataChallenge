#!/usr/bin/env python3
"""Bounded Brandt/Hecke autocorrelation probe for the p24 energy sidecar.

This is a deliberately small calibration on the existing D=-5000 CM toy.  It
checks which matrix-trace identities are exact and whether the relative
autocorrelation sequence has a low-dimensional transfer/recurrence collapse.
"""

from __future__ import annotations

from cypari2 import Pari

from cycle_period_complexity_scan import bm_linear_complexity, dft_support
from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)

Q = 3851
QUOTIENT_SIZE = 6
SUBGROUP_SIZE = H // QUOTIENT_SIZE


def c_shift(cycle: list[int], q: int, shift: int) -> int:
    h = len(cycle)
    return sum(cycle[i] * cycle[(i + shift) % h] for i in range(h)) % q


def trace_d_p_d_pinv(cycle: list[int], q: int, shift: int) -> int:
    """Trace(D_j P_shift D_j P_-shift), computed without materializing matrices."""
    return c_shift(cycle, q, shift)


def trace_unoriented_shift_packet(cycle: list[int], q: int, shift: int) -> int:
    """Trace(D_j (P_s+P_-s) D_j (P_s+P_-s)) for non-2-torsion shifts."""
    return (2 * c_shift(cycle, q, shift)) % q


def relative_autocorrelation(cycle: list[int], q: int, m: int) -> list[int]:
    n = len(cycle) // m
    return [c_shift(cycle, q, m * d) for d in range(n)]


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    c1 = c_shift(cycle, Q, 1)
    brandt_trace = trace_d_p_d_pinv(cycle, Q, 1)
    hecke_unoriented_trace = trace_unoriented_shift_packet(cycle, Q, 1)

    rel = relative_autocorrelation(cycle, Q, QUOTIENT_SIZE)
    rel_bm = bm_linear_complexity(rel * 2, Q)
    rel_support = dft_support(rel, Q)

    print("agent Brandt/Hecke energy probe")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"quotient_m={QUOTIENT_SIZE}")
    print(f"recovery_n={SUBGROUP_SIZE}")
    print()
    print("exact_trace_identities")
    print(f"C_1={c1}")
    print(f"trace_D_P1_D_Pminus1={brandt_trace}")
    print(f"trace_identity_ok={int(c1 == brandt_trace)}")
    print(f"trace_D_B1_D_B1={hecke_unoriented_trace}")
    print(f"unoriented_hecke_equals_2C1={int(hecke_unoriented_trace == (2 * c1) % Q)}")
    print()
    print("relative_autocorrelation")
    print(f"C_d_for_shifts_m_d={rel}")
    print(f"distinct_C_d={len(set(rel))}")
    print(f"bm_complexity={rel_bm}")
    print(f"dft_support={rel_support}")
    print(f"full_bm={int(rel_bm == SUBGROUP_SIZE)}")
    print(f"full_dft_support={int(rel_support == SUBGROUP_SIZE)}")
    print()
    print("interpretation")
    print("  oriented_matrix_trace_identity_is_exact_if_P_shift_is_already_known=1")
    print("  ordinary_unoriented_hecke_packet_gives_C_s_plus_C_minus_s=1")
    print("  relative_C_d_has_full_toy_transfer_dimension=1")
    print("conclusion=trace_bookkeeping_is_exact_but_does_not_compress_the_recovery_subgroup")


if __name__ == "__main__":
    main()
