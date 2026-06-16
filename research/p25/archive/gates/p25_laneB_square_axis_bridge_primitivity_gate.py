#!/usr/bin/env python3
"""Primitivity and no-compression gate for the square-axis bridge.

The raw-source bridge gate identifies the local source multiplier

    X^2 Y^3 = 113  ->  (45 mod151, 667 mod677).

This gate records the complementary producer-facing obstruction: that edge is
primitive on the raw local source cycle and the signed bridge has no proper
quotient explanation below C_507.  The raw lift is kernel-trivial, but its
nonzero Fourier support is full on the quotient side.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_factorization_gate import (
    BRIDGE_STEP,
    bridge_coefficients,
)
from p25_laneB_square_axis_bridge_raw_source_gate import (
    raw_bridge_lift,
    source_generators,
    square_axis_case,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER
from p25_selected_defect_value_gate import split_prime_for


PROPER_QUOTIENT_DIVISORS = (1, 3, 13, 39, 169)


@dataclass(frozen=True)
class QuotientCompressionProfile:
    divisor: int
    descends: bool
    nonzero_residue_count: int
    conflicting_residue_count: int
    pullback_support_size: int


@dataclass(frozen=True)
class FourierProfile:
    modulus: int
    zero_count: int
    nonzero_count: int
    nonzero_frequency_min: int
    nonzero_frequency_max: int
    all_nonzero_frequencies_kernel_trivial: bool
    quotient_zero_frequencies: tuple[int, ...]


def gcd(left: int, right: int) -> int:
    while right:
        left, right = right, left % right
    return abs(left)


def multiplicative_order(value: int, modulus: int, limit: int) -> int:
    acc = 1
    for order in range(1, limit + 1):
        acc = acc * value % modulus
        if acc == 1:
            return order
    raise AssertionError(f"order exceeds {limit}")


def compression_profiles() -> tuple[QuotientCompressionProfile, ...]:
    coefficients = bridge_coefficients()
    rows: list[QuotientCompressionProfile] = []
    for divisor in PROPER_QUOTIENT_DIVISORS:
        descends = True
        conflicts = 0
        nonzero_residues: set[int] = set()
        pullback_support = 0
        for residue in range(divisor):
            fiber_values = {
                coefficients.get(q_value, 0)
                for q_value in range(QUOTIENT_ORDER)
                if q_value % divisor == residue
            }
            if len(fiber_values) != 1:
                descends = False
                conflicts += 1
            if any(value != 0 for value in fiber_values):
                nonzero_residues.add(residue)
                pullback_support += QUOTIENT_ORDER // divisor
        rows.append(
            QuotientCompressionProfile(
                divisor=divisor,
                descends=descends,
                nonzero_residue_count=len(nonzero_residues),
                conflicting_residue_count=conflicts,
                pullback_support_size=pullback_support,
            )
        )
    return tuple(rows)


def raw_fourier_profile() -> FourierProfile:
    case = square_axis_case()
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // case.raw_order, modulus)
    raw = raw_bridge_lift(case, modulus)
    nonzero_frequencies: list[int] = []
    quotient_zero_frequencies: list[int] = []
    for frequency in range(case.raw_order):
        total = sum(
            value * pow(zeta, frequency * index, modulus)
            for index, value in enumerate(raw)
            if value
        ) % modulus
        if total:
            nonzero_frequencies.append(frequency)
        elif frequency % case.b_trace == 0:
            quotient_zero_frequencies.append(frequency // case.b_trace)
    return FourierProfile(
        modulus=modulus,
        zero_count=case.raw_order - len(nonzero_frequencies),
        nonzero_count=len(nonzero_frequencies),
        nonzero_frequency_min=min(nonzero_frequencies),
        nonzero_frequency_max=max(nonzero_frequencies),
        all_nonzero_frequencies_kernel_trivial=all(
            frequency % case.b_trace == 0 for frequency in nonzero_frequencies
        ),
        quotient_zero_frequencies=tuple(quotient_zero_frequencies),
    )


def main() -> int:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_multiplier = pow(right_generator, BRIDGE_STEP, right_source.modulus)
    c_multiplier = pow(c_generator, BRIDGE_STEP, c_source.modulus)
    right_order = multiplicative_order(
        right_multiplier, right_source.modulus, right_source.expected_order
    )
    c_order = multiplicative_order(c_multiplier, c_source.modulus, c_source.expected_order)
    product_order = right_order * c_order // gcd(right_order, c_order)
    raw_step_gcd = gcd(BRIDGE_STEP, case.raw_order)
    quotient_step_gcd = gcd(BRIDGE_STEP, QUOTIENT_ORDER)
    quotient_profiles = compression_profiles()
    profile_by_divisor = {profile.divisor: profile for profile in quotient_profiles}
    fourier = raw_fourier_profile()
    expected_conflicts = {
        1: (1, 1, 507),
        3: (3, 3, 507),
        13: (6, 6, 234),
        39: (6, 6, 78),
        169: (6, 6, 18),
    }
    compression_ok = all(
        not profile.descends
        and (
            profile.nonzero_residue_count,
            profile.conflicting_residue_count,
            profile.pullback_support_size,
        )
        == expected_conflicts[profile.divisor]
        for profile in quotient_profiles
    )
    fourier_ok = (
        fourier.modulus == 126751
        and fourier.zero_count == 12171
        and fourier.nonzero_count == 504
        and fourier.nonzero_frequency_min == 25
        and fourier.nonzero_frequency_max == 12650
        and fourier.all_nonzero_frequencies_kernel_trivial
        and fourier.quotient_zero_frequencies == (0, 169, 338)
    )
    row_ok = (
        case.raw_order == RAW_ORDER
        and right_multiplier == 45
        and c_multiplier == 667
        and BRIDGE_STEP % right_source.expected_order == 38
        and BRIDGE_STEP % c_source.expected_order == 113
        and right_order == right_source.expected_order == 75
        and c_order == c_source.expected_order == 169
        and product_order == case.raw_order == 12675
        and raw_step_gcd == 1
        and quotient_step_gcd == 1
        and compression_ok
        and fourier_ok
    )
    print("p25 Lane B square-axis bridge primitivity gate")
    print(
        f"case={case.name} p={P25} raw_order={case.raw_order} "
        f"quotient_order={QUOTIENT_ORDER} B={case.b_trace}"
    )
    print(
        "bridge_step_orders: "
        f"step={BRIDGE_STEP} raw_step_gcd={raw_step_gcd} "
        f"quotient_step_gcd={quotient_step_gcd} "
        f"right_multiplier={right_multiplier} right_order={right_order} "
        f"c_multiplier={c_multiplier} c_order={c_order} "
        f"product_order={product_order}"
    )
    print("proper_quotient_profiles")
    for profile in quotient_profiles:
        print(f"  {profile}")
    print(
        "raw_fourier_profile: "
        f"modulus={fourier.modulus} "
        f"zero_count={fourier.zero_count} "
        f"nonzero_count={fourier.nonzero_count} "
        f"nonzero_frequency_range=({fourier.nonzero_frequency_min},{fourier.nonzero_frequency_max}) "
        f"all_nonzero_frequencies_kernel_trivial={int(fourier.all_nonzero_frequencies_kernel_trivial)} "
        f"quotient_zero_frequencies={list(fourier.quotient_zero_frequencies)}"
    )
    print("interpretation")
    print("  bridge_step_is_primitive_on_raw_and_quotient_cycles=1")
    print("  local_source_multiplier_has_full_order_12675=1")
    print("  signed_bridge_has_no_proper_quotient_below_C507=1")
    print("  raw_bridge_fourier_support_is_exactly_kernel_trivial_quotient_full=1")
    print(f"square_axis_bridge_primitivity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_primitivity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
