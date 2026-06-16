#!/usr/bin/env python3
"""Actual-CM boundary for internal traces of right-combo obstructions.

The p24 target is now an internal trace identity for the right Gauss-reduced
obstruction polynomial.  This boundary checks the closest pinned actual-CM
right-combo analogue already used in the harness:

    D=-13319, q=13463, m=28=4*7, n=5.

Here the E-relative Frobenius on the n-layer has order 2.  The two internal
trace orbits of the actual right-combo obstruction are both nonzero.  Thus
even "right-combo obstruction" is not a generic internal-trace-zero theorem;
the p24 proof must use the specific 211-axis/H-coset equality of the traced
G_chi profile.
"""

from __future__ import annotations

import sympy as sp

from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    load_actual_packet,
    right_combo,
)


def main() -> None:
    packet = load_actual_packet()
    ord_m = int(sp.n_order(packet.q % packet.m, packet.m))
    q_generator = pow(packet.q, ord_m, packet.n)
    q_order = int(sp.n_order(q_generator, packet.n))

    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(1, packet.n):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = value * q_generator % packet.n
        orbits.append(orbit)

    trace_zeroes = 0
    all_terms_nonzero = 0
    trace_values: list[tuple[int, ...]] = []
    for orbit in orbits:
        trace = packet.field.zero
        terms = []
        for a_rel in orbit:
            term = right_combo(packet, a_rel)
            terms.append(term)
            trace = packet.field.add(trace, term)
        all_terms_nonzero += int(all(term != packet.field.zero for term in terms))
        trace_zeroes += int(trace == packet.field.zero)
        trace_values.append(trace)

    print("Trace-GCD fixed-frequency actual-CM right-combo internal trace boundary")
    print(f"D={packet.D}")
    print(f"q={packet.q}")
    print(f"ell={packet.ell}")
    print(f"h={packet.h}")
    print(f"m={packet.m}")
    print(f"n={packet.n}")
    print(f"ord_m_q={ord_m}")
    print(f"internal_q_generator=q^ord_m_mod_n={q_generator}")
    print(f"internal_q_order={q_order}")
    print(f"right_combo_orbits={orbits}")
    print(f"right_combo_orbit_count={len(orbits)}")
    print(f"right_combo_terms_all_nonzero={all_terms_nonzero}/{len(orbits)}")
    print(f"right_combo_internal_trace_zeroes={trace_zeroes}/{len(orbits)}")
    print(f"right_combo_internal_trace_values={trace_values}")
    print("interpretation")
    print("  actual_cm_right_combo_internal_trace_zeroes_are_not_generic=1")
    print("  p24_needs_specific_211_axis_H_coset_equality_after_internal_trace=1")
    print("  right_combo_shape_alone_does_not_prove_trace_zero=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_internal_trace_boundary")

    if (packet.D, packet.q, packet.m, packet.n) != (-13319, 13463, 28, 5):
        raise SystemExit(1)
    if q_order != 2:
        raise SystemExit(1)
    if len(orbits) != 2:
        raise SystemExit(1)
    if all_terms_nonzero != len(orbits):
        raise SystemExit(1)
    if trace_zeroes != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
