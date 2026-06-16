#!/usr/bin/env python3
"""Ambient local sign obstruction for the p25 primitive bridge.

The twisted-orientation gate says a support-preserving degree-39 bridge
producer must supply a quadratic sign local system.  The first cheap place
to look for that sign is the two-primary part of the actual local residue
fields above the square-axis source:

    mod 151: F_l^* has C_2 x C_75, source order C_75,
    mod 677: F_l^* has C_4 x C_169, source order C_169.

This gate checks that the established bridge source subgroup lies entirely in
the trivial two-primary coset in both fields.  Consequently no Legendre,
quartic, or product two-primary local character separates the positive and
negative bridge layers.  A successful sign-twist producer must introduce a
new anti-invariant coefficient/local system, not recover it from the ambient
signs already present in the p24-amortized local source coordinates.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_raw_source_gate import (
    source_generators,
    square_axis_case,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)


Coord = tuple[int, int]
Tag = tuple[int, int]


@dataclass(frozen=True)
class SourceTwoPrimaryProfile:
    name: str
    modulus: int
    expected_order: int
    unit_order: int
    primitive_root: int
    source_generator: int
    source_generator_log: int
    two_primary_tag_modulus: int
    source_tag_values: tuple[int, ...]
    source_tags_trivial: bool
    minus_one_tag: int


@dataclass(frozen=True)
class FactorTwoPrimaryProfile:
    name: str
    shift: Coord
    right_multiplier: int
    c_multiplier: int
    right_tag: int
    c_tag: int


@dataclass(frozen=True)
class BridgeLocalSignProfile:
    right_tag_modulus: int
    c_tag_modulus: int
    source_profiles: tuple[SourceTwoPrimaryProfile, ...]
    factor_profiles: tuple[FactorTwoPrimaryProfile, ...]
    raw_support: int
    positive_support: int
    negative_support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    all_tag_counts: tuple[tuple[Tag, int], ...]
    positive_tag_counts: tuple[tuple[Tag, int], ...]
    negative_tag_counts: tuple[tuple[Tag, int], ...]
    all_bridge_tags_trivial: bool
    nontrivial_two_primary_characters_checked: int
    separating_two_primary_characters: int
    minus_one_tags: Tag


def primitive_log_table(root: int, modulus: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        if value in table:
            raise AssertionError("primitive-root table repeated early")
        table[value] = exponent
        value = value * root % modulus
    if value != 1:
        raise AssertionError("primitive-root table did not close")
    return table


def two_power_part(value: int) -> int:
    out = 1
    while value % 2 == 0:
        out *= 2
        value //= 2
    return out


def source_profile(name: str, modulus: int, expected_order: int, source_generator: int) -> SourceTwoPrimaryProfile:
    root = primitive_root(modulus)
    table = primitive_log_table(root, modulus)
    unit_order = modulus - 1
    tag_modulus = two_power_part(unit_order)
    if unit_order // expected_order != tag_modulus:
        raise AssertionError("source order is not the odd part of the local unit group")
    tags = tuple(
        sorted(
            {
                table[pow(source_generator, exponent, modulus)] % tag_modulus
                for exponent in range(expected_order)
            }
        )
    )
    return SourceTwoPrimaryProfile(
        name=name,
        modulus=modulus,
        expected_order=expected_order,
        unit_order=unit_order,
        primitive_root=root,
        source_generator=source_generator,
        source_generator_log=table[source_generator],
        two_primary_tag_modulus=tag_modulus,
        source_tag_values=tags,
        source_tags_trivial=tags == (0,),
        minus_one_tag=table[modulus - 1] % tag_modulus,
    )


def local_tag(value: int, modulus: int, tag_modulus: int) -> int:
    root = primitive_root(modulus)
    table = primitive_log_table(root, modulus)
    return table[value % modulus] % tag_modulus


def factor_profile(name: str, shift: Coord) -> FactorTwoPrimaryProfile:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_multiplier = pow(right_generator, shift[0], right_source.modulus)
    c_multiplier = pow(c_generator, shift[1], c_source.modulus)
    right_tag_modulus = two_power_part(right_source.modulus - 1)
    c_tag_modulus = two_power_part(c_source.modulus - 1)
    return FactorTwoPrimaryProfile(
        name=name,
        shift=shift,
        right_multiplier=right_multiplier,
        c_multiplier=c_multiplier,
        right_tag=local_tag(right_multiplier, right_source.modulus, right_tag_modulus),
        c_tag=local_tag(c_multiplier, c_source.modulus, c_tag_modulus),
    )


def bridge_tag_counts() -> tuple[
    int,
    int,
    int,
    tuple[tuple[int, int], ...],
    tuple[tuple[Tag, int], ...],
    tuple[tuple[Tag, int], ...],
    tuple[tuple[Tag, int], ...],
]:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_tag_modulus = two_power_part(right_source.modulus - 1)
    c_tag_modulus = two_power_part(c_source.modulus - 1)
    mask = raw_source_mask()
    all_tags: Counter[Tag] = Counter()
    positive_tags: Counter[Tag] = Counter()
    negative_tags: Counter[Tag] = Counter()
    coefficients: Counter[int] = Counter()
    for (right_coord, c_coord), coefficient in mask.items():
        right_value = pow(right_generator, right_coord, right_source.modulus)
        c_value = pow(c_generator, c_coord, c_source.modulus)
        tag = (
            local_tag(right_value, right_source.modulus, right_tag_modulus),
            local_tag(c_value, c_source.modulus, c_tag_modulus),
        )
        all_tags[tag] += 1
        coefficients[coefficient] += 1
        if coefficient > 0:
            positive_tags[tag] += 1
        elif coefficient < 0:
            negative_tags[tag] += 1
        else:
            raise AssertionError("bridge mask contains a zero coefficient")
    return (
        len(mask),
        coefficients[1],
        coefficients[-1],
        tuple(sorted(coefficients.items())),
        tuple(sorted(all_tags.items())),
        tuple(sorted(positive_tags.items())),
        tuple(sorted(negative_tags.items())),
    )


def separating_character_count(
    positive_tag_counts: tuple[tuple[Tag, int], ...],
    negative_tag_counts: tuple[tuple[Tag, int], ...],
    right_tag_modulus: int,
    c_tag_modulus: int,
) -> int:
    """Count two-primary tag characters that could distinguish bridge signs.

    Embed the right C_2 tag into C_4, then scan all homomorphisms from
    C_2 x C_4 to C_4.  A separator would be constant on each sign layer and
    differ by the order-two value 2 in C_4.
    """

    positives = [tag for tag, count in positive_tag_counts for _ in range(count)]
    negatives = [tag for tag, count in negative_tag_counts for _ in range(count)]
    hits = 0
    for right_weight in range(right_tag_modulus):
        for c_weight in range(c_tag_modulus):
            if right_weight == 0 and c_weight == 0:
                continue
            pos_values = {
                (right_weight * (c_tag_modulus // right_tag_modulus) * tag[0] + c_weight * tag[1])
                % c_tag_modulus
                for tag in positives
            }
            neg_values = {
                (right_weight * (c_tag_modulus // right_tag_modulus) * tag[0] + c_weight * tag[1])
                % c_tag_modulus
                for tag in negatives
            }
            if (
                len(pos_values) == 1
                and len(neg_values) == 1
                and ((next(iter(pos_values)) - next(iter(neg_values))) % c_tag_modulus)
                == c_tag_modulus // 2
            ):
                hits += 1
    return hits


def profile_bridge_local_sign() -> BridgeLocalSignProfile:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_source_profile = source_profile(
        right_source.name,
        right_source.modulus,
        right_source.expected_order,
        right_generator,
    )
    c_source_profile = source_profile(
        c_source.name,
        c_source.modulus,
        c_source.expected_order,
        c_generator,
    )
    right_tag_modulus = right_source_profile.two_primary_tag_modulus
    c_tag_modulus = c_source_profile.two_primary_tag_modulus
    raw_support, positive_support, negative_support, coefficient_counts, all_tags, pos_tags, neg_tags = bridge_tag_counts()
    factors = (
        factor_profile("base", BASE_POINT),
        factor_profile("kernel_trace", KERNEL_SHIFT),
        factor_profile("D_segment", D_SHIFT),
        factor_profile("bridge_edge", BRIDGE_SHIFT),
        factor_profile("Y_raw", (9, 9)),
        factor_profile(
            "D_cubed",
            ((3 * D_SHIFT[0]) % RIGHT_ORDER, (3 * D_SHIFT[1]) % C_ORDER),
        ),
    )
    return BridgeLocalSignProfile(
        right_tag_modulus=right_tag_modulus,
        c_tag_modulus=c_tag_modulus,
        source_profiles=(right_source_profile, c_source_profile),
        factor_profiles=factors,
        raw_support=raw_support,
        positive_support=positive_support,
        negative_support=negative_support,
        coefficient_counts=coefficient_counts,
        all_tag_counts=all_tags,
        positive_tag_counts=pos_tags,
        negative_tag_counts=neg_tags,
        all_bridge_tags_trivial=all_tags == (((0, 0), raw_support),),
        nontrivial_two_primary_characters_checked=right_tag_modulus * c_tag_modulus - 1,
        separating_two_primary_characters=separating_character_count(
            pos_tags,
            neg_tags,
            right_tag_modulus,
            c_tag_modulus,
        ),
        minus_one_tags=(right_source_profile.minus_one_tag, c_source_profile.minus_one_tag),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge local sign obstruction gate")
    profile = profile_bridge_local_sign()
    expected_sources = (
        SourceTwoPrimaryProfile("mod151", 151, 75, 150, 6, 62, 98, 2, (0,), True, 1),
        SourceTwoPrimaryProfile("mod677", 677, 169, 676, 2, 354, 384, 4, (0,), True, 2),
    )
    expected_factors = (
        FactorTwoPrimaryProfile("base", (25, 25), 32, 148, 0, 0),
        FactorTwoPrimaryProfile("kernel_trace", (57, 0), 125, 1, 0, 0),
        FactorTwoPrimaryProfile("D_segment", (22, 3), 55, 85, 0, 0),
        FactorTwoPrimaryProfile("bridge_edge", (38, 113), 45, 667, 0, 0),
        FactorTwoPrimaryProfile("Y_raw", (9, 9), 123, 86, 0, 0),
        FactorTwoPrimaryProfile("D_cubed", (66, 9), 124, 86, 0, 0),
    )
    row_ok = (
        profile.right_tag_modulus == 2
        and profile.c_tag_modulus == 4
        and profile.source_profiles == expected_sources
        and profile.factor_profiles == expected_factors
        and profile.raw_support == 150
        and profile.positive_support == 75
        and profile.negative_support == 75
        and profile.coefficient_counts == ((-1, 75), (1, 75))
        and profile.all_tag_counts == (((0, 0), 150),)
        and profile.positive_tag_counts == (((0, 0), 75),)
        and profile.negative_tag_counts == (((0, 0), 75),)
        and profile.all_bridge_tags_trivial
        and profile.nontrivial_two_primary_characters_checked == 7
        and profile.separating_two_primary_characters == 0
        and profile.minus_one_tags == (1, 2)
    )

    print(f"bridge_local_sign_profile={profile}")
    print("local_two_primary_laws")
    print("  mod151 source C75 is the full odd part of F_151^*, so Legendre is trivial")
    print("  mod677 source C169 is the full odd part after C4, so quartic tags are trivial")
    print("  K, D, T, Y, and D^3 all have two-primary tag (0,0)")
    print("  all 150 raw bridge support points have tag (0,0), including both signs")
    print("interpretation")
    print("  ambient_legendre_or_quartic_signs_do_not_supply_the_degree39_orientation=1")
    print("  multiplying_by_minus_one_leaves_the_established_source_subgroup_coset=1")
    print("  sign_twist_must_be_a_new_anti_invariant_local_system_or_equivalent_identity=1")
    print(f"square_axis_bridge_local_sign_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_local_sign_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
