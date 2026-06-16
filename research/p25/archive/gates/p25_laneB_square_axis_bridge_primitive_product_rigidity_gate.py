#!/usr/bin/env python3
"""Primitive D-coordinate product rigidity for the p25 square-axis bridge.

The primitive D-coordinate normal form turns the accepted bridge into a word
in C_12675:

    z^11275 * K_25 * (1 + z + z^2) * (1 - z^6854).

This gate records the complementary rigidity.  After the unavoidable C_25
kernel trace is collapsed, the quotient C_507 word has only the known forward
and reverse signed 2 x 3 product presentations.  The order-25 trace subgroup
in C_12675 is unique, so alternate trace generators do not give alternate
producer geometry.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
from math import gcd

from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import (
    primitive_d_poly,
    profile_primitive_d_coordinate,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


KERNEL_QUOTIENT_ORDER = 507
KERNEL_TRACE_ORDER = 25

Poly = dict[int, int]
Factor = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class TraceCollapseProfile:
    raw_support: int
    quotient_order: int
    trace_order: int
    nonzero_cosets: int
    full_cosets: int
    partial_cosets: int
    coefficient_conflict_cosets: int
    positive_residues: tuple[int, ...]
    negative_residues: tuple[int, ...]
    coset_size_counts: tuple[tuple[int, int], ...]
    order25_generator_count: int
    order25_generators_first: tuple[int, ...]
    known_kernel_generator_is_order25: bool
    order25_subgroup_unique: bool


@dataclass(frozen=True)
class QuotientProductMatch:
    two_direction: int
    two_sign: int
    three_support: tuple[int, int, int]
    three_coefficients: tuple[int, int, int]
    is_forward_bridge: bool
    is_reverse_bridge: bool


def cyclic_order(exponent: int) -> int:
    if exponent == 0:
        return 1
    return RAW_ORDER // gcd(exponent, RAW_ORDER)


def subgroup(step: int, size: int) -> frozenset[int]:
    return frozenset((step * index) % RAW_ORDER for index in range(size))


def collapse_by_trace(poly: Poly) -> tuple[TraceCollapseProfile, dict[int, int]]:
    primitive_profile = profile_primitive_d_coordinate()
    order25_generators = tuple(
        exponent for exponent in range(RAW_ORDER) if cyclic_order(exponent) == KERNEL_TRACE_ORDER
    )
    canonical_subgroup = subgroup(KERNEL_QUOTIENT_ORDER, KERNEL_TRACE_ORDER)

    quotient: dict[int, int] = {}
    full_cosets = 0
    partial_cosets = 0
    conflict_cosets = 0
    coset_sizes: list[int] = []
    positive: list[int] = []
    negative: list[int] = []

    for residue in range(KERNEL_QUOTIENT_ORDER):
        values = [poly.get(residue + KERNEL_QUOTIENT_ORDER * layer, 0) for layer in range(KERNEL_TRACE_ORDER)]
        nonzero_values = [value for value in values if value]
        if not nonzero_values:
            continue
        coset_sizes.append(len(nonzero_values))
        if len(nonzero_values) == KERNEL_TRACE_ORDER:
            full_cosets += 1
        else:
            partial_cosets += 1
        coefficient_set = set(nonzero_values)
        if len(coefficient_set) != 1:
            conflict_cosets += 1
            continue
        coefficient = nonzero_values[0]
        quotient[residue] = coefficient
        if coefficient > 0:
            positive.append(residue)
        elif coefficient < 0:
            negative.append(residue)

    profile = TraceCollapseProfile(
        raw_support=len(poly),
        quotient_order=KERNEL_QUOTIENT_ORDER,
        trace_order=KERNEL_TRACE_ORDER,
        nonzero_cosets=len(quotient),
        full_cosets=full_cosets,
        partial_cosets=partial_cosets,
        coefficient_conflict_cosets=conflict_cosets,
        positive_residues=tuple(sorted(positive)),
        negative_residues=tuple(sorted(negative)),
        coset_size_counts=tuple(sorted(Counter(coset_sizes).items())),
        order25_generator_count=len(order25_generators),
        order25_generators_first=order25_generators[:10],
        known_kernel_generator_is_order25=cyclic_order(primitive_profile.kernel_exponent)
        == KERNEL_TRACE_ORDER,
        order25_subgroup_unique=all(
            subgroup(generator, KERNEL_TRACE_ORDER) == canonical_subgroup
            for generator in order25_generators
        ),
    )
    return profile, dict(sorted(quotient.items()))


def convolution(left: Factor, right: Factor) -> dict[int, int]:
    out: dict[int, int] = {}
    for left_q, left_coeff in left:
        for right_q, right_coeff in right:
            q_value = (left_q + right_q) % KERNEL_QUOTIENT_ORDER
            out[q_value] = out.get(q_value, 0) + left_coeff * right_coeff
            if out[q_value] == 0:
                del out[q_value]
    return dict(sorted(out.items()))


def quotient_product_matches(quotient: dict[int, int]) -> tuple[QuotientProductMatch, ...]:
    primitive_profile = profile_primitive_d_coordinate()
    forward_direction = primitive_profile.bridge_exponent % KERNEL_QUOTIENT_ORDER
    reverse_direction = (-forward_direction) % KERNEL_QUOTIENT_ORDER
    forward_support = tuple(range(primitive_profile.base_exponent % KERNEL_QUOTIENT_ORDER, primitive_profile.base_exponent % KERNEL_QUOTIENT_ORDER + 3))
    reverse_support = tuple(sorted((value + forward_direction) % KERNEL_QUOTIENT_ORDER for value in forward_support))

    matches: list[QuotientProductMatch] = []
    target_support = tuple(quotient)
    for direction in range(1, KERNEL_QUOTIENT_ORDER):
        for two_sign in (1, -1):
            two_factor = ((0, 1), (direction, two_sign))
            for support in combinations(target_support, 3):
                for coefficients in product((1, -1), repeat=3):
                    three_factor = tuple(zip(support, coefficients))
                    if convolution(two_factor, three_factor) != quotient:
                        continue
                    matches.append(
                        QuotientProductMatch(
                            two_direction=direction,
                            two_sign=two_sign,
                            three_support=support,  # type: ignore[arg-type]
                            three_coefficients=coefficients,  # type: ignore[arg-type]
                            is_forward_bridge=(
                                direction == forward_direction
                                and two_sign == -1
                                and support == forward_support
                                and coefficients == (1, 1, 1)
                            ),
                            is_reverse_bridge=(
                                direction == reverse_direction
                                and two_sign == -1
                                and support == reverse_support
                                and coefficients == (-1, -1, -1)
                            ),
                        )
                    )
    return tuple(matches)


def main() -> int:
    print("p25 Lane B square-axis bridge primitive product-rigidity gate")
    primitive_profile = profile_primitive_d_coordinate()
    poly = primitive_d_poly(
        primitive_profile.base_exponent,
        primitive_profile.kernel_exponent,
        primitive_profile.bridge_exponent,
    )
    trace_profile, quotient = collapse_by_trace(poly)
    matches = quotient_product_matches(quotient)
    direction_counts = Counter((match.two_direction, match.two_sign) for match in matches)
    support_counts = Counter(match.three_support for match in matches)
    raw_trace_product_presentations = trace_profile.order25_generator_count * len(matches)

    expected_matches = (
        QuotientProductMatch(
            two_direction=244,
            two_sign=-1,
            three_support=(384, 385, 386),
            three_coefficients=(-1, -1, -1),
            is_forward_bridge=False,
            is_reverse_bridge=True,
        ),
        QuotientProductMatch(
            two_direction=263,
            two_sign=-1,
            three_support=(121, 122, 123),
            three_coefficients=(1, 1, 1),
            is_forward_bridge=True,
            is_reverse_bridge=False,
        ),
    )
    row_ok = (
        primitive_profile.base_exponent % KERNEL_QUOTIENT_ORDER == 121
        and primitive_profile.kernel_exponent % KERNEL_QUOTIENT_ORDER == 0
        and primitive_profile.bridge_exponent % KERNEL_QUOTIENT_ORDER == 263
        and trace_profile
        == TraceCollapseProfile(
            raw_support=150,
            quotient_order=507,
            trace_order=25,
            nonzero_cosets=6,
            full_cosets=6,
            partial_cosets=0,
            coefficient_conflict_cosets=0,
            positive_residues=(121, 122, 123),
            negative_residues=(384, 385, 386),
            coset_size_counts=((25, 6),),
            order25_generator_count=20,
            order25_generators_first=(507, 1014, 1521, 2028, 3042, 3549, 4056, 4563, 5577, 6084),
            known_kernel_generator_is_order25=True,
            order25_subgroup_unique=True,
        )
        and matches == expected_matches
        and direction_counts == Counter({(244, -1): 1, (263, -1): 1})
        and support_counts == Counter({(384, 385, 386): 1, (121, 122, 123): 1})
        and raw_trace_product_presentations == 40
    )

    print(
        "primitive_coordinate_data: "
        f"base_mod507={primitive_profile.base_exponent % KERNEL_QUOTIENT_ORDER} "
        f"kernel_mod507={primitive_profile.kernel_exponent % KERNEL_QUOTIENT_ORDER} "
        f"bridge_mod507={primitive_profile.bridge_exponent % KERNEL_QUOTIENT_ORDER}"
    )
    print(f"trace_collapse_profile={trace_profile}")
    print(f"collapsed_quotient={sorted(quotient.items())}")
    print(
        "quotient_product_scan: "
        f"matches={len(matches)} "
        f"direction_counts={dict(sorted(direction_counts.items()))} "
        f"three_support_counts={dict(sorted(support_counts.items()))} "
        f"raw_trace_product_presentations={raw_trace_product_presentations}"
    )
    print("matches")
    for match in matches:
        print(f"  {match}")
    print("factor_laws")
    print("  forward = C25_trace * (1 - z^263) * z^121*(1 + z + z^2)")
    print("  reverse = C25_trace * (1 - z^244) * -z^384*(1 + z + z^2)")
    print("  the 20 order-25 trace generators all generate the same C25 subgroup")
    print("interpretation")
    print("  primitive_D_word_is_exactly_six_full_C25_trace_cosets=1")
    print("  collapsed_C507_word_has_only_forward_and_reverse_signed_2x3_products=1")
    print("  alternate_order25_trace_generators_do_not_create_new_geometry=1")
    print("  producer_must_realize_the_same_trace_segment_edge_bridge_not_an_alternate_short_product=1")
    print(f"square_axis_bridge_primitive_product_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_primitive_product_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
