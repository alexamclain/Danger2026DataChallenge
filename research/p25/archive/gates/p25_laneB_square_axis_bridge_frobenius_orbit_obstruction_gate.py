#!/usr/bin/env python3
"""Frobenius-orbit obstruction for the p25 primitive bridge.

The primitive D-coordinate gates leave a natural arithmetic escape: perhaps a
Frobenius or diamond orbit average produces the bridge cheaply.  This gate
checks the finite obstruction in the collapsed C_507 coordinate.

Multiplication by p has order 78 on C_507, with p^39 = -1.  Thus the full
p-orbit of the signed bridge cancels in opposite orientations.  Over p^2 the
39 supports are pairwise disjoint, so a p^2-stable orbit closure of the bridge
has support 234 on C_507 and 5850 on the raw C_12675 block lift.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import (
    primitive_d_poly,
    profile_primitive_d_coordinate,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


QUOTIENT_ORDER = 507
TRACE_ORDER = 25


@dataclass(frozen=True)
class FrobeniusOrbitProfile:
    p_mod_raw: int
    p2_mod_raw: int
    p_mod_quotient: int
    p2_mod_quotient: int
    p_order_quotient: int
    p2_order_quotient: int
    p_half_power: int
    quotient_positive: tuple[int, ...]
    quotient_negative: tuple[int, ...]
    p_image_positive: tuple[int, ...]
    p_image_negative: tuple[int, ...]
    p2_image_positive: tuple[int, ...]
    p2_image_negative: tuple[int, ...]
    p_preserving_exponents: tuple[int, ...]
    p_reversing_exponents: tuple[int, ...]
    p_support_return_exponents: tuple[int, ...]
    p_orbit_signed_count: int
    p_orbit_support_count: int
    p_orbit_signed_sum_support: int
    p2_orbit_signed_count: int
    p2_orbit_support_count: int
    p2_support_union_size: int
    p2_pairwise_support_intersections: int
    p2_raw_support_union_size: int
    p2_raw_positive_count: int
    p2_raw_negative_count: int


def multiplicative_order(value: int, modulus: int) -> int:
    acc = 1
    for order in range(1, modulus + 1):
        acc = acc * value % modulus
        if acc == 1:
            return order
    raise AssertionError(f"order of {value} mod {modulus} exceeds {modulus}")


def primitive_word_sets() -> tuple[frozenset[int], frozenset[int]]:
    primitive_profile = profile_primitive_d_coordinate()
    poly = primitive_d_poly(
        primitive_profile.base_exponent,
        primitive_profile.kernel_exponent,
        primitive_profile.bridge_exponent,
    )
    positive = frozenset(exponent for exponent, coefficient in poly.items() if coefficient == 1)
    negative = frozenset(exponent for exponent, coefficient in poly.items() if coefficient == -1)
    return positive, negative


def quotient_sets(positive: frozenset[int], negative: frozenset[int]) -> tuple[frozenset[int], frozenset[int]]:
    return (
        frozenset(exponent % QUOTIENT_ORDER for exponent in positive),
        frozenset(exponent % QUOTIENT_ORDER for exponent in negative),
    )


def multiply_set(points: frozenset[int], multiplier: int, modulus: int) -> frozenset[int]:
    return frozenset((multiplier * point) % modulus for point in points)


def signed_sum_support(
    positive: frozenset[int],
    negative: frozenset[int],
    multiplier: int,
    orbit_order: int,
    modulus: int,
) -> dict[int, int]:
    out: dict[int, int] = {}
    current = 1
    for _index in range(orbit_order):
        for point in positive:
            image = current * point % modulus
            out[image] = out.get(image, 0) + 1
            if out[image] == 0:
                del out[image]
        for point in negative:
            image = current * point % modulus
            out[image] = out.get(image, 0) - 1
            if out[image] == 0:
                del out[image]
        current = current * multiplier % modulus
    return dict(sorted(out.items()))


def orbit_words(
    positive: frozenset[int],
    negative: frozenset[int],
    multiplier: int,
    orbit_order: int,
    modulus: int,
) -> tuple[tuple[frozenset[int], frozenset[int]], ...]:
    out: list[tuple[frozenset[int], frozenset[int]]] = []
    current = 1
    for _index in range(orbit_order):
        out.append(
            (
                multiply_set(positive, current, modulus),
                multiply_set(negative, current, modulus),
            )
        )
        current = current * multiplier % modulus
    return tuple(out)


def support_union(words: tuple[tuple[frozenset[int], frozenset[int]], ...]) -> frozenset[int]:
    out: set[int] = set()
    for positive, negative in words:
        out.update(positive)
        out.update(negative)
    return frozenset(out)


def pairwise_support_intersections(words: tuple[tuple[frozenset[int], frozenset[int]], ...]) -> int:
    count = 0
    supports = [positive | negative for positive, negative in words]
    for left_index, left_support in enumerate(supports):
        for right_support in supports[left_index + 1 :]:
            count += int(bool(left_support & right_support))
    return count


def orbit_profile() -> FrobeniusOrbitProfile:
    raw_positive, raw_negative = primitive_word_sets()
    quotient_positive, quotient_negative = quotient_sets(raw_positive, raw_negative)
    p_raw = P25 % RAW_ORDER
    p2_raw = (p_raw * p_raw) % RAW_ORDER
    p_quotient = P25 % QUOTIENT_ORDER
    p2_quotient = (p_quotient * p_quotient) % QUOTIENT_ORDER
    p_order = multiplicative_order(p_quotient, QUOTIENT_ORDER)
    p2_order = multiplicative_order(p2_quotient, QUOTIENT_ORDER)
    p_words = orbit_words(quotient_positive, quotient_negative, p_quotient, p_order, QUOTIENT_ORDER)
    p2_words = orbit_words(quotient_positive, quotient_negative, p2_quotient, p2_order, QUOTIENT_ORDER)
    p2_raw_words = orbit_words(raw_positive, raw_negative, p2_raw, p2_order, RAW_ORDER)
    p2_raw_sum = signed_sum_support(raw_positive, raw_negative, p2_raw, p2_order, RAW_ORDER)

    p_preserving: list[int] = []
    p_reversing: list[int] = []
    p_support_returns: list[int] = []
    current = 1
    quotient_support = quotient_positive | quotient_negative
    for exponent in range(p_order):
        image_positive = multiply_set(quotient_positive, current, QUOTIENT_ORDER)
        image_negative = multiply_set(quotient_negative, current, QUOTIENT_ORDER)
        if image_positive == quotient_positive and image_negative == quotient_negative:
            p_preserving.append(exponent)
        if image_positive == quotient_negative and image_negative == quotient_positive:
            p_reversing.append(exponent)
        if image_positive | image_negative == quotient_support:
            p_support_returns.append(exponent)
        current = current * p_quotient % QUOTIENT_ORDER

    return FrobeniusOrbitProfile(
        p_mod_raw=p_raw,
        p2_mod_raw=p2_raw,
        p_mod_quotient=p_quotient,
        p2_mod_quotient=p2_quotient,
        p_order_quotient=p_order,
        p2_order_quotient=p2_order,
        p_half_power=pow(p_quotient, p_order // 2, QUOTIENT_ORDER),
        quotient_positive=tuple(sorted(quotient_positive)),
        quotient_negative=tuple(sorted(quotient_negative)),
        p_image_positive=tuple(sorted(p_words[1][0])),
        p_image_negative=tuple(sorted(p_words[1][1])),
        p2_image_positive=tuple(sorted(p2_words[1][0])),
        p2_image_negative=tuple(sorted(p2_words[1][1])),
        p_preserving_exponents=tuple(p_preserving),
        p_reversing_exponents=tuple(p_reversing),
        p_support_return_exponents=tuple(p_support_returns),
        p_orbit_signed_count=len(set(p_words)),
        p_orbit_support_count=len({positive | negative for positive, negative in p_words}),
        p_orbit_signed_sum_support=len(
            signed_sum_support(quotient_positive, quotient_negative, p_quotient, p_order, QUOTIENT_ORDER)
        ),
        p2_orbit_signed_count=len(set(p2_words)),
        p2_orbit_support_count=len({positive | negative for positive, negative in p2_words}),
        p2_support_union_size=len(support_union(p2_words)),
        p2_pairwise_support_intersections=pairwise_support_intersections(p2_words),
        p2_raw_support_union_size=len(support_union(p2_raw_words)),
        p2_raw_positive_count=sum(1 for value in p2_raw_sum.values() if value > 0),
        p2_raw_negative_count=sum(1 for value in p2_raw_sum.values() if value < 0),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Frobenius-orbit obstruction gate")
    profile = orbit_profile()
    expected = FrobeniusOrbitProfile(
        p_mod_raw=5288,
        p2_mod_raw=1894,
        p_mod_quotient=218,
        p2_mod_quotient=373,
        p_order_quotient=78,
        p2_order_quotient=39,
        p_half_power=506,
        quotient_positive=(121, 122, 123),
        quotient_negative=(384, 385, 386),
        p_image_positive=(14, 232, 450),
        p_image_negative=(57, 275, 493),
        p2_image_positive=(10, 249, 383),
        p2_image_negative=(124, 258, 497),
        p_preserving_exponents=(0,),
        p_reversing_exponents=(39,),
        p_support_return_exponents=(0, 39),
        p_orbit_signed_count=78,
        p_orbit_support_count=39,
        p_orbit_signed_sum_support=0,
        p2_orbit_signed_count=39,
        p2_orbit_support_count=39,
        p2_support_union_size=234,
        p2_pairwise_support_intersections=0,
        p2_raw_support_union_size=5850,
        p2_raw_positive_count=2925,
        p2_raw_negative_count=2925,
    )
    row_ok = (
        profile == expected
        and gcd(profile.p_mod_quotient, QUOTIENT_ORDER) == 1
        and profile.p_half_power == QUOTIENT_ORDER - 1
        and profile.p2_support_union_size == profile.p2_orbit_support_count * 6
        and profile.p2_raw_support_union_size == profile.p2_support_union_size * TRACE_ORDER
    )

    print(f"frobenius_orbit_profile={profile}")
    print("frobenius_laws")
    print("  p mod C507 has order 78 and p^39 = -1")
    print("  the only p-power support returns are identity and the known bridge reversal")
    print("  the full signed p-orbit cancels pairwise")
    print("  the p^2-orbit has 39 pairwise disjoint quotient supports")
    print("  p^2-stable orbit closure costs 234 quotient classes and 5850 raw cells")
    print("interpretation")
    print("  bridge_is_not_a_small_frobenius_or_diamond_average=1")
    print("  p_stable_signed_average_of_the_bridge_is_zero=1")
    print("  p2_stable_nonzero_orbit_closure_is_much_larger_than_the_150_cell_bridge=1")
    print("  producer_must_supply_a_specific_oriented_bridge_not_a_plain_frobenius_closure=1")
    print(f"square_axis_bridge_frobenius_orbit_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_frobenius_orbit_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
