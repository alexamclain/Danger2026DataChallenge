#!/usr/bin/env python3
"""Actual-CM boundary for termwise right-combo vanishing.

The p24 fixed-frequency class-character expansion leaves two proof shapes:

    exact packet cancellation:      sum_a T_{1,0,a} R_{chi,-a} = 0;
    stronger termwise vanishing:    R_{chi,-a} = 0 for every a.

This checks the stronger termwise statement on the pinned small actual-CM
analogue D=-13319, q=13463, m=28=4*7, n=5.  The analogue has a nontrivial
right quotient character for the right component 7.  It reports that all
primitive relative right-combos are nonzero, so termwise vanishing is not a
generic CM-packet identity.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from relative_moment_projection_scan import find_splitting_primes, rotate


PINNED_D = -13319
PINNED_Q = 13463
M = 28
LEFT = 4
RIGHT = 7
RELATIVE = 5
LEFT_U = 1
RIGHT_PRIMITIVE = 3
SEED = 20260606


@dataclass(frozen=True)
class ActualPacket:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    cycle: tuple[int, ...]
    field: ExtensionField
    zeta_left: FpE
    zeta_right: FpE
    zeta_rel: FpE


def right_log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_PRIMITIVE % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("RIGHT_PRIMITIVE is not primitive modulo 7")
    return logs


def quotient_character(value: int) -> int:
    # q=13463 is 2 mod 7, so the Frobenius subgroup is {1,2,4}; the quotient
    # character is the quadratic character modulo 7.
    return 1 if right_log_table()[value] % 2 == 0 else -1


def load_actual_packet() -> ActualPacket:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(PINNED_D)
    h = int(pari.poldegree(hilbert))
    splits = find_splitting_primes(
        pari,
        hilbert,
        h,
        PINNED_Q,
        PINNED_Q + 1,
        1,
    )
    if not splits:
        raise RuntimeError("pinned splitting prime not found")
    q, roots = splits[0]
    full = find_full_cycle_prime(roots, PINNED_D, q)
    if full is None:
        raise RuntimeError("pinned full cycle not found")
    ell, cycle = full
    shifted = tuple(rotate(cycle, 0))
    n = h // M
    if n != RELATIVE:
        raise RuntimeError("unexpected relative degree")

    root_order = int(sp.ilcm(M, RELATIVE))
    extension_degree = int(sp.n_order(q % root_order, root_order))
    modulus = find_irreducible_modulus(q, extension_degree, SEED)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, root_order, SEED)

    return ActualPacket(
        D=PINNED_D,
        q=q,
        ell=ell,
        h=h,
        m=M,
        n=n,
        cycle=shifted,
        field=field,
        zeta_left=field.pow(zeta, root_order // LEFT),
        zeta_right=field.pow(zeta, root_order // RIGHT),
        zeta_rel=field.pow(zeta, root_order // RELATIVE),
    )


def class_trace(packet: ActualPacket, u_left: int, v_right: int, a_rel: int) -> FpE:
    field = packet.field
    total = field.zero
    for index, j_value in enumerate(packet.cycle):
        weight = field.mul(
            field.mul(
                field.pow(packet.zeta_left, (u_left * (index % LEFT)) % LEFT),
                field.pow(packet.zeta_right, (v_right * (index % RIGHT)) % RIGHT),
            ),
            field.pow(packet.zeta_rel, (a_rel * (index // M)) % RELATIVE),
        )
        total = field.add(total, field.mul(weight, field.embed(j_value)))
    return total


def right_combo(packet: ActualPacket, a_rel: int) -> FpE:
    field = packet.field
    total = field.zero
    for v in range(1, RIGHT):
        total = field.add(
            total,
            field.scalar_mul(
                quotient_character(v),
                class_trace(packet, 0, v, -a_rel),
            ),
        )
    return total


def packet_projection(packet: ActualPacket) -> tuple[FpE, list[FpE], list[FpE], list[FpE]]:
    field = packet.field
    left_traces: list[FpE] = []
    right_combos: list[FpE] = []
    terms: list[FpE] = []
    total = field.zero
    for a_rel in range(1, RELATIVE):
        left = class_trace(packet, LEFT_U, 0, a_rel)
        right = right_combo(packet, a_rel)
        term = field.mul(left, right)
        left_traces.append(left)
        right_combos.append(right)
        terms.append(term)
        total = field.add(total, term)
    return total, left_traces, right_combos, terms


def right_neutral_control(packet: ActualPacket) -> int:
    field = packet.field
    failures = 0
    values = [
        packet.cycle[(left + LEFT * rel) % len(packet.cycle)]
        for rel in range(RELATIVE)
        for left in range(LEFT)
    ]
    for a_rel in range(1, RELATIVE):
        combo = field.zero
        for v in range(1, RIGHT):
            trace = field.zero
            for index in range(packet.h):
                left = index % LEFT
                rel = index // M
                j_value = values[rel * LEFT + left]
                weight = field.mul(
                    field.pow(packet.zeta_right, (v * (index % RIGHT)) % RIGHT),
                    field.pow(packet.zeta_rel, (-a_rel * rel) % RELATIVE),
                )
                trace = field.add(trace, field.mul(weight, field.embed(j_value)))
            combo = field.add(combo, field.scalar_mul(quotient_character(v), trace))
        failures += int(combo != field.zero)
    return failures


def main() -> None:
    packet = load_actual_packet()
    projection, left_traces, right_combos, terms = packet_projection(packet)
    neutral_failures = right_neutral_control(packet)

    print("Trace-GCD fixed-frequency actual-CM right-combo boundary")
    print(f"D={packet.D}")
    print(f"q={packet.q}")
    print(f"ell={packet.ell}")
    print(f"h={packet.h}")
    print(f"m={packet.m}")
    print(f"n={packet.n}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"relative={RELATIVE}")
    print(f"root_field_degree={packet.field.degree}")
    print(f"right_quotient_character={[quotient_character(v) for v in range(1, RIGHT)]}")
    print(f"left_packet_traces_nonzero={sum(value != packet.field.zero for value in left_traces)}/{len(left_traces)}")
    print(f"right_multiplicative_packet_combos_nonzero={sum(value != packet.field.zero for value in right_combos)}/{len(right_combos)}")
    print(f"product_terms_nonzero={sum(value != packet.field.zero for value in terms)}/{len(terms)}")
    print(f"packet_projection_nonzero={int(projection != packet.field.zero)}")
    print(f"right_neutral_control_combo_failures={neutral_failures}")
    print("interpretation")
    print("  actual_cm_refutes_generic_termwise_right_combo_vanishing=1")
    print("  termwise_right_combo_vanishing_is_sufficient_but_too_strong=1")
    print("  fixed_frequency_target_must_use_packet_cancellation_or_p24_specific_extra_structure=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_right_combo_boundary")

    if any(value == packet.field.zero for value in right_combos):
        raise SystemExit(1)
    if projection == packet.field.zero:
        raise SystemExit(1)
    if neutral_failures != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
