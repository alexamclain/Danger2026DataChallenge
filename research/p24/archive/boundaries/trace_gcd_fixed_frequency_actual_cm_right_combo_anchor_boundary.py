#!/usr/bin/env python3
"""Actual-CM boundary isolating the recombined anchor equation.

The p24 period-coset balance splits, per nontrivial right character, into
seven nontrivial octic quotient equations plus one anchor equation:

    sum_{k != 0} c_k(chi) = (n - 1) * c_0(chi).

The pinned actual-CM right-combo analogue has

    D=-13319, q=13463, m=28=4*7, n=5.

Here <q> has order 4 modulo n=5, so there is only one nonzero recombined
coset.  Thus the recombined balance is exactly the anchor equation, with no
nontrivial quotient equations to hide behind.  It fails for the actual
right-combo G_chi analogue, so the p24 anchor cannot be a generic
right-combo/decomposition-field trace-zero fact.
"""

from __future__ import annotations

import sympy as sp

from k_character_tensor_rank_scan import FpE
from trace_gcd_fixed_frequency_actual_cm_right_combo_boundary import (
    M,
    RIGHT,
    load_actual_packet,
    quotient_character,
    right_combo,
)


def orbit(modulus: int, generator: int) -> list[int]:
    values: list[int] = []
    value = 1
    while value not in values:
        values.append(value)
        value = value * generator % modulus
    return values


def weighted_coefficients(packet) -> list[FpE]:
    field = packet.field
    coefficients: list[FpE] = []
    for k in range(packet.n):
        total = field.zero
        for r in range(M):
            residue = r % RIGHT
            if residue == 0:
                continue
            weight = quotient_character(residue)
            total = field.add(
                total,
                field.scalar_mul(weight, field.embed(packet.cycle[r + M * k])),
            )
        coefficients.append(total)
    return coefficients


def polynomial_eval(coefficients: list[FpE], point: FpE, field) -> FpE:
    total = field.zero
    power = field.one
    for coeff in coefficients:
        total = field.add(total, field.mul(coeff, power))
        power = field.mul(power, point)
    return total


def main() -> None:
    packet = load_actual_packet()
    coefficients = weighted_coefficients(packet)
    recombined_generator = packet.q % packet.n
    recombined_order = int(sp.n_order(recombined_generator, packet.n))
    recombined_orbit = orbit(packet.n, recombined_generator)

    nonzero_sum = packet.field.zero
    for coeff in coefficients[1:]:
        nonzero_sum = packet.field.add(nonzero_sum, coeff)
    anchor_target = packet.field.scalar_mul(packet.n - 1, coefficients[0])
    anchor_defect = packet.field.sub(nonzero_sum, anchor_target)

    polynomial_trace = packet.field.zero
    right_combo_trace = packet.field.zero
    for exponent in recombined_orbit:
        point = packet.field.pow(packet.zeta_rel, exponent)
        polynomial_trace = packet.field.add(
            polynomial_trace,
            polynomial_eval(coefficients, point, packet.field),
        )
        right_combo_trace = packet.field.add(
            right_combo_trace,
            right_combo(packet, exponent),
        )

    print("Trace-GCD fixed-frequency actual-CM right-combo anchor boundary")
    print(f"D={packet.D}")
    print(f"q={packet.q}")
    print(f"ell={packet.ell}")
    print(f"h={packet.h}")
    print(f"m={packet.m}")
    print(f"n={packet.n}")
    print(f"right={RIGHT}")
    print(f"relative={packet.n}")
    print(f"recombined_q_generator=q_mod_n={recombined_generator}")
    print(f"recombined_q_order={recombined_order}")
    print(f"recombined_nonzero_coset={recombined_orbit}")
    print("recombined_nontrivial_quotient_equations=0")
    print("recombined_anchor_equations=1")
    print(f"anchor_balance_holds={int(anchor_defect == packet.field.zero)}")
    print(f"anchor_defect_nonzero={int(anchor_defect != packet.field.zero)}")
    print(f"anchor_defect={anchor_defect}")
    print(f"weighted_polynomial_recombined_trace_zero={int(polynomial_trace == packet.field.zero)}")
    print(f"weighted_polynomial_recombined_trace={polynomial_trace}")
    print(f"right_combo_recombined_trace_zero={int(right_combo_trace == packet.field.zero)}")
    print(f"right_combo_recombined_trace={right_combo_trace}")
    print("interpretation")
    print("  small_actual_cm_recombined_balance_is_anchor_only=1")
    print("  actual_cm_right_combo_anchor_balance_is_not_generic=1")
    print("  p24_anchor_needs_specific_weighted_G_chi_or_explicit_potential=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary")

    if (packet.D, packet.q, packet.m, packet.n) != (-13319, 13463, 28, 5):
        raise SystemExit(1)
    if recombined_order != packet.n - 1:
        raise SystemExit(1)
    if len(recombined_orbit) != packet.n - 1:
        raise SystemExit(1)
    if anchor_defect == packet.field.zero:
        raise SystemExit(1)
    if polynomial_trace == packet.field.zero:
        raise SystemExit(1)
    if right_combo_trace == packet.field.zero:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
