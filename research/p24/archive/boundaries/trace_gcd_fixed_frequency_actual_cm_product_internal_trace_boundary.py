#!/usr/bin/env python3
"""Actual-CM boundary for internal traces of weighted product packets.

The p24 fixed-frequency target is not merely a right-combo statement; the raw
packet has weighted product shape

    sum_a T_left(a) * R_right(a).

The product-coboundary gate shows how such packets would vanish if the right
factor had the matching twisted potential.  This boundary checks the closest
pinned actual-CM analogue already used by the harness:

    D=-13319, q=13463, m=28=4*7, n=5.

For its two E-internal Frobenius orbits on the relative n-layer, the weighted
product internal traces are both nonzero.  The recombined trace over the full
<q> orbit is also nonzero.  Thus even the full product packet shape is not a
generic internal/decomposition-field trace-zero theorem.  The p24 proof still
needs the specific 211-axis/H-coset equality, or an explicit CM/Lang potential
for that weighted packet.
"""

from __future__ import annotations

import sympy as sp

from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    LEFT_U,
    class_trace,
    load_actual_packet,
    right_combo,
)


def internal_orbits(modulus: int, generator: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(1, modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = value * generator % modulus
        orbits.append(orbit)
    return orbits


def main() -> None:
    packet = load_actual_packet()
    ord_m = int(sp.n_order(packet.q % packet.m, packet.m))
    q_generator = pow(packet.q, ord_m, packet.n)
    q_order = int(sp.n_order(q_generator, packet.n))
    orbits = internal_orbits(packet.n, q_generator)
    recombined_generator = packet.q % packet.n
    recombined_q_order = int(sp.n_order(recombined_generator, packet.n))
    recombined_orbits = internal_orbits(packet.n, recombined_generator)

    trace_zeroes = 0
    all_terms_nonzero = 0
    orbit_trace_values: list[tuple[int, ...]] = []
    full_projection = packet.field.zero
    recombined_trace_zeroes = 0
    recombined_trace_values: list[tuple[int, ...]] = []

    for orbit in orbits:
        trace = packet.field.zero
        terms = []
        for a_rel in orbit:
            left = class_trace(packet, LEFT_U, 0, a_rel)
            right = right_combo(packet, a_rel)
            term = packet.field.mul(left, right)
            terms.append(term)
            trace = packet.field.add(trace, term)
            full_projection = packet.field.add(full_projection, term)
        all_terms_nonzero += int(all(term != packet.field.zero for term in terms))
        trace_zeroes += int(trace == packet.field.zero)
        orbit_trace_values.append(trace)

    for orbit in recombined_orbits:
        trace = packet.field.zero
        for a_rel in orbit:
            left = class_trace(packet, LEFT_U, 0, a_rel)
            right = right_combo(packet, a_rel)
            trace = packet.field.add(trace, packet.field.mul(left, right))
        recombined_trace_zeroes += int(trace == packet.field.zero)
        recombined_trace_values.append(trace)

    print("Trace-GCD fixed-frequency actual-CM product internal trace boundary")
    print(f"D={packet.D}")
    print(f"q={packet.q}")
    print(f"ell={packet.ell}")
    print(f"h={packet.h}")
    print(f"m={packet.m}")
    print(f"n={packet.n}")
    print(f"left={4}")
    print(f"right={7}")
    print(f"relative={packet.n}")
    print(f"ord_m_q={ord_m}")
    print(f"internal_q_generator=q^ord_m_mod_n={q_generator}")
    print(f"internal_q_order={q_order}")
    print(f"product_internal_orbits={orbits}")
    print(f"product_internal_orbit_count={len(orbits)}")
    print(f"product_terms_all_nonzero={all_terms_nonzero}/{len(orbits)}")
    print(f"product_internal_trace_zeroes={trace_zeroes}/{len(orbits)}")
    print(f"product_internal_trace_values={orbit_trace_values}")
    print(f"recombined_q_generator=q_mod_n={recombined_generator}")
    print(f"recombined_q_order={recombined_q_order}")
    print(f"recombined_product_orbits={recombined_orbits}")
    print(f"recombined_product_orbit_count={len(recombined_orbits)}")
    print(f"recombined_product_trace_zeroes={recombined_trace_zeroes}/{len(recombined_orbits)}")
    print(f"recombined_product_trace_values={recombined_trace_values}")
    print(f"product_full_projection_zero={int(full_projection == packet.field.zero)}")
    print(f"product_full_projection_value={full_projection}")
    print("interpretation")
    print("  actual_cm_weighted_product_internal_trace_zeroes_are_not_generic=1")
    print("  actual_cm_weighted_product_recombined_trace_zeroes_are_not_generic=1")
    print("  product_packet_shape_alone_does_not_prove_trace_zero=1")
    print("  p24_needs_specific_weighted_G_chi_packet_or_explicit_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_product_internal_trace_boundary")

    if (packet.D, packet.q, packet.m, packet.n) != (-13319, 13463, 28, 5):
        raise SystemExit(1)
    if q_order != 2:
        raise SystemExit(1)
    if recombined_q_order != 4:
        raise SystemExit(1)
    if len(orbits) != 2:
        raise SystemExit(1)
    if len(recombined_orbits) != 1:
        raise SystemExit(1)
    if all_terms_nonzero != len(orbits):
        raise SystemExit(1)
    if trace_zeroes != 0:
        raise SystemExit(1)
    if recombined_trace_zeroes != 0:
        raise SystemExit(1)
    if full_projection == packet.field.zero:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
