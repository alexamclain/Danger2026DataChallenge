#!/usr/bin/env python3
"""Actual-CM boundary for mixed right/relative quotient spectrum.

The p24 recombined target has two quotient axes:

    right quotient:     order 7
    relative quotient:  order 8

The closest tiny actual-CM row found by a bounded shape scan is:

    D=-4751, q=4787, h=91=7*13.

Here the right component 7 has quotient order 3 because q has order 2 mod 7,
and the relative component 13 has quotient order 4 because q has order 3
mod 13.  This is not p24, but it is the first cheap row with both axes
nontrivial and a full embedded CM cycle.

The script checks the actual mixed-spectrum equations and the anchor equations
for every global origin shift of the embedded cycle.  They fail for all shifts,
so mixed right/relative quotient vanishing is not a generic actual-CM
consequence of having both quotient axes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_decomposition_calibration import pari_linear_roots
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


PINNED_D = -4751
PINNED_Q = 4787
M = 7
RIGHT = 7
RELATIVE_N = 13
SEED = 20260607


@dataclass(frozen=True)
class ActualMixedPacket:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    right_order: int
    right_quotient: int
    relative_order: int
    relative_quotient: int
    cycle: tuple[int, ...]
    field: ExtensionField
    zeta_right_quotient: FpE
    zeta_relative_quotient: FpE


def rotate(cycle: tuple[int, ...], shift: int) -> tuple[int, ...]:
    shift %= len(cycle)
    return cycle[shift:] + cycle[:shift]


def primitive_log_table(modulus: int) -> dict[int, int]:
    generator = int(sp.primitive_root(modulus))
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad primitive root")
    return logs


def quotient_character(
    value: int,
    modulus: int,
    quotient_order: int,
    zeta_quotient: FpE,
    logs: dict[int, int],
    index: int,
    field: ExtensionField,
) -> FpE:
    residue = value % modulus
    if residue == 0:
        return field.zero
    return field.pow(zeta_quotient, (index * logs[residue]) % quotient_order)


def cosets_for_quotient(modulus: int, quotient_order: int) -> list[list[int]]:
    logs = primitive_log_table(modulus)
    cosets: list[list[int]] = [[] for _ in range(quotient_order)]
    for value in range(1, modulus):
        cosets[logs[value] % quotient_order].append(value)
    return cosets


def load_actual_packet() -> ActualMixedPacket:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(PINNED_D)
    h = int(pari.poldegree(hilbert))
    roots = pari_linear_roots(hilbert, PINNED_Q)
    if len(roots) != h:
        raise RuntimeError("pinned prime does not fully split")
    full = find_full_cycle_prime(roots, PINNED_D, PINNED_Q, ell_bound=89)
    if full is None:
        raise RuntimeError("pinned full cycle not found")
    ell, cycle = full
    right_order = int(sp.n_order(PINNED_Q % RIGHT, RIGHT))
    relative_order = int(sp.n_order(PINNED_Q % RELATIVE_N, RELATIVE_N))
    right_quotient = (RIGHT - 1) // right_order
    relative_quotient = (RELATIVE_N - 1) // relative_order
    root_order = lcm(M, RELATIVE_N, right_quotient, relative_quotient)
    extension_degree = int(sp.n_order(PINNED_Q % root_order, root_order))
    modulus = find_irreducible_modulus(PINNED_Q, extension_degree, SEED)
    field = ExtensionField(PINNED_Q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, root_order, SEED)
    return ActualMixedPacket(
        D=PINNED_D,
        q=PINNED_Q,
        ell=ell,
        h=h,
        m=M,
        n=RELATIVE_N,
        right_order=right_order,
        right_quotient=right_quotient,
        relative_order=relative_order,
        relative_quotient=relative_quotient,
        cycle=tuple(cycle),
        field=field,
        zeta_right_quotient=field.pow(zeta, root_order // right_quotient),
        zeta_relative_quotient=field.pow(zeta, root_order // relative_quotient),
    )


def coefficients_for_chi(
    packet: ActualMixedPacket,
    cycle: tuple[int, ...],
    chi_index: int,
    right_logs: dict[int, int],
) -> list[FpE]:
    field = packet.field
    coeffs: list[FpE] = []
    for k in range(packet.n):
        total = field.zero
        for r in range(packet.m):
            residue = r % RIGHT
            if residue == 0:
                continue
            weight = quotient_character(
                residue,
                RIGHT,
                packet.right_quotient,
                packet.zeta_right_quotient,
                right_logs,
                -chi_index,
                field,
            )
            total = field.add(total, field.mul(weight, field.embed(cycle[r + packet.m * k])))
        coeffs.append(total)
    return coeffs


def mixed_value(
    packet: ActualMixedPacket,
    coeffs: list[FpE],
    lambda_index: int,
    relative_logs: dict[int, int],
) -> FpE:
    field = packet.field
    total = field.zero
    for k in range(1, packet.n):
        weight = quotient_character(
            k,
            packet.n,
            packet.relative_quotient,
            packet.zeta_relative_quotient,
            relative_logs,
            lambda_index,
            field,
        )
        total = field.add(total, field.mul(weight, coeffs[k]))
    return total


def anchor_value(packet: ActualMixedPacket, coeffs: list[FpE]) -> FpE:
    field = packet.field
    nonzero_sum = field.zero
    for coeff in coeffs[1:]:
        nonzero_sum = field.add(nonzero_sum, coeff)
    target = field.scalar_mul(packet.n - 1, coeffs[0])
    return field.sub(nonzero_sum, target)


def balance_count(packet: ActualMixedPacket, coeffs: list[FpE], cosets: list[list[int]]) -> int:
    field = packet.field
    target = field.scalar_mul(packet.relative_order, coeffs[0])
    count = 0
    for coset in cosets:
        total = field.zero
        for index in coset:
            total = field.add(total, coeffs[index])
        count += int(total == target)
    return count


@dataclass(frozen=True)
class ShiftResult:
    shift: int
    mixed_zeroes: int
    anchor_zeroes: int
    balance_passes: int


def evaluate_shift(
    packet: ActualMixedPacket,
    shift: int,
    right_logs: dict[int, int],
    relative_logs: dict[int, int],
    relative_cosets: list[list[int]],
) -> ShiftResult:
    cycle = rotate(packet.cycle, shift)
    mixed_zeroes = 0
    anchor_zeroes = 0
    balance_passes = 0
    for chi_index in range(1, packet.right_quotient):
        coeffs = coefficients_for_chi(packet, cycle, chi_index, right_logs)
        anchor_zeroes += int(anchor_value(packet, coeffs) == packet.field.zero)
        balance_passes += balance_count(packet, coeffs, relative_cosets)
        for lambda_index in range(1, packet.relative_quotient):
            mixed_zeroes += int(
                mixed_value(packet, coeffs, lambda_index, relative_logs)
                == packet.field.zero
            )
    return ShiftResult(
        shift=shift,
        mixed_zeroes=mixed_zeroes,
        anchor_zeroes=anchor_zeroes,
        balance_passes=balance_passes,
    )


def main() -> None:
    packet = load_actual_packet()
    right_logs = primitive_log_table(RIGHT)
    relative_logs = primitive_log_table(packet.n)
    relative_cosets = cosets_for_quotient(packet.n, packet.relative_quotient)
    mixed_total = (packet.right_quotient - 1) * (packet.relative_quotient - 1)
    anchor_total = packet.right_quotient - 1
    balance_total = (packet.right_quotient - 1) * packet.relative_quotient
    results = [
        evaluate_shift(packet, shift, right_logs, relative_logs, relative_cosets)
        for shift in range(packet.h)
    ]
    full_mixed_shifts = sum(result.mixed_zeroes == mixed_total for result in results)
    full_anchor_shifts = sum(result.anchor_zeroes == anchor_total for result in results)
    full_balance_shifts = sum(result.balance_passes == balance_total for result in results)
    best_mixed = max(result.mixed_zeroes for result in results)
    best_anchor = max(result.anchor_zeroes for result in results)
    best_balance = max(result.balance_passes for result in results)
    shift0 = results[0]

    print("Trace-GCD fixed-frequency actual-CM mixed-spectrum boundary")
    print(f"D={packet.D}")
    print(f"q={packet.q}")
    print(f"ell={packet.ell}")
    print(f"h={packet.h}")
    print(f"m={packet.m}")
    print(f"n={packet.n}")
    print(f"right={RIGHT}")
    print(f"right_order_q={packet.right_order}")
    print(f"right_quotient={packet.right_quotient}")
    print(f"relative_order_q={packet.relative_order}")
    print(f"relative_quotient={packet.relative_quotient}")
    print(f"field_degree={packet.field.degree}")
    print(f"mixed_equations_per_shift={mixed_total}")
    print(f"anchor_equations_per_shift={anchor_total}")
    print(f"balance_equations_per_shift={balance_total}")
    print(f"shift0_mixed_zeroes={shift0.mixed_zeroes}/{mixed_total}")
    print(f"shift0_anchor_zeroes={shift0.anchor_zeroes}/{anchor_total}")
    print(f"shift0_balance_passes={shift0.balance_passes}/{balance_total}")
    print(f"full_mixed_zero_shifts={full_mixed_shifts}/{packet.h}")
    print(f"full_anchor_zero_shifts={full_anchor_shifts}/{packet.h}")
    print(f"full_recombined_balance_shifts={full_balance_shifts}/{packet.h}")
    print(f"best_mixed_zeroes_any_shift={best_mixed}/{mixed_total}")
    print(f"best_anchor_zeroes_any_shift={best_anchor}/{anchor_total}")
    print(f"best_balance_passes_any_shift={best_balance}/{balance_total}")
    print("interpretation")
    print("  actual_cm_both_axes_nontrivial_boundary=1")
    print("  actual_cm_mixed_spectrum_vanishing_is_not_generic=1")
    print("  actual_cm_origin_shift_does_not_rescue_mixed_balance=1")
    print("  p24_needs_specific_trace_gcd_cm_lang_relation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_mixed_spectrum_boundary")

    if (packet.D, packet.q, packet.h, packet.m, packet.n) != (-4751, 4787, 91, 7, 13):
        raise SystemExit(1)
    if (packet.right_quotient, packet.relative_quotient) != (3, 4):
        raise SystemExit(1)
    if full_mixed_shifts or full_anchor_shifts or full_balance_shifts:
        raise SystemExit(1)
    if best_mixed >= mixed_total:
        raise SystemExit(1)
    if best_balance >= balance_total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
