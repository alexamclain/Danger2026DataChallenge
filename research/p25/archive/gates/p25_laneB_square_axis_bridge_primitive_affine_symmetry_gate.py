#!/usr/bin/env python3
"""Primitive D-coordinate affine symmetry gate for the p25 bridge.

The primitive product-rigidity gate leaves one natural escape: perhaps the
one-variable word has a hidden affine/Galois symmetry that a ray-local producer
could exploit.  This gate enumerates affine maps in the primitive coordinate.

On the collapsed C_507 quotient, the only signed affine symmetries are the
identity and the known bridge reversal.  On the raw C_12675 source, every lift
of those symmetries is just a reindexing/translation of the C_25 trace fiber.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import (
    primitive_d_poly,
    profile_primitive_d_coordinate,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


QUOTIENT_ORDER = 507
TRACE_ORDER = 25


@dataclass(frozen=True)
class QuotientAffineProfile:
    quotient_order: int
    positive_residues: tuple[int, ...]
    negative_residues: tuple[int, ...]
    sign_preserving_affines: tuple[tuple[int, int], ...]
    sign_reversing_affines: tuple[tuple[int, int], ...]
    unsigned_support_affines: tuple[tuple[int, int], ...]
    unsigned_extra_affines: int


@dataclass(frozen=True)
class RawAffineProfile:
    raw_order: int
    trace_order: int
    positive_size: int
    negative_size: int
    sign_preserving_count: int
    sign_reversing_count: int
    unsigned_support_count: int
    unsigned_extra_count: int
    preserving_multiplier_residue_mod_507: tuple[int, ...]
    preserving_translation_residue_mod_507: tuple[int, ...]
    reversing_multiplier_residue_mod_507: tuple[int, ...]
    reversing_translation_residue_mod_507: tuple[int, ...]
    preserving_multiplier_count: int
    reversing_multiplier_count: int
    trace_translation_count: int
    preserving_multipliers: tuple[int, ...]
    reversing_multipliers: tuple[int, ...]
    trace_translations: tuple[int, ...]
    all_preserving_lifts_check: bool
    all_reversing_lifts_check: bool


def units(modulus: int) -> tuple[int, ...]:
    return tuple(value for value in range(modulus) if gcd(value, modulus) == 1)


def affine_image(points: frozenset[int], multiplier: int, translation: int, modulus: int) -> frozenset[int]:
    return frozenset((multiplier * point + translation) % modulus for point in points)


def primitive_sets() -> tuple[frozenset[int], frozenset[int]]:
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


def quotient_affine_profile(positive: frozenset[int], negative: frozenset[int]) -> QuotientAffineProfile:
    sign_preserving: list[tuple[int, int]] = []
    sign_reversing: list[tuple[int, int]] = []
    unsigned: list[tuple[int, int]] = []
    support = positive | negative
    base_point = next(iter(positive))
    for multiplier in units(QUOTIENT_ORDER):
        for target in support:
            translation = (target - multiplier * base_point) % QUOTIENT_ORDER
            image_positive = affine_image(positive, multiplier, translation, QUOTIENT_ORDER)
            image_negative = affine_image(negative, multiplier, translation, QUOTIENT_ORDER)
            if image_positive == positive and image_negative == negative:
                sign_preserving.append((multiplier, translation))
            if image_positive == negative and image_negative == positive:
                sign_reversing.append((multiplier, translation))
            if image_positive | image_negative == support:
                unsigned.append((multiplier, translation))
    signed = set(sign_preserving) | set(sign_reversing)
    return QuotientAffineProfile(
        quotient_order=QUOTIENT_ORDER,
        positive_residues=tuple(sorted(positive)),
        negative_residues=tuple(sorted(negative)),
        sign_preserving_affines=tuple(sorted(sign_preserving)),
        sign_reversing_affines=tuple(sorted(sign_reversing)),
        unsigned_support_affines=tuple(sorted(unsigned)),
        unsigned_extra_affines=len(set(unsigned) - signed),
    )


def residue_lifts(multiplier_residue: int, translation_residue: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    multipliers = tuple(
        multiplier
        for multiplier in range(RAW_ORDER)
        if gcd(multiplier, RAW_ORDER) == 1 and multiplier % QUOTIENT_ORDER == multiplier_residue
    )
    translations = tuple(
        translation
        for translation in range(RAW_ORDER)
        if translation % QUOTIENT_ORDER == translation_residue
    )
    return multipliers, translations


def all_lifts_match(
    positive: frozenset[int],
    negative: frozenset[int],
    multipliers: tuple[int, ...],
    translations: tuple[int, ...],
    reverse: bool,
) -> bool:
    target_positive = negative if reverse else positive
    target_negative = positive if reverse else negative
    for multiplier in multipliers:
        for translation in translations:
            if affine_image(positive, multiplier, translation, RAW_ORDER) != target_positive:
                return False
            if affine_image(negative, multiplier, translation, RAW_ORDER) != target_negative:
                return False
    return True


def raw_affine_profile(
    positive: frozenset[int],
    negative: frozenset[int],
    quotient_profile: QuotientAffineProfile,
) -> RawAffineProfile:
    preserving_multiplier_residue, preserving_translation_residue = quotient_profile.sign_preserving_affines[0]
    reversing_multiplier_residue, reversing_translation_residue = quotient_profile.sign_reversing_affines[0]
    preserving_multipliers, preserving_translations = residue_lifts(
        preserving_multiplier_residue,
        preserving_translation_residue,
    )
    reversing_multipliers, reversing_translations = residue_lifts(
        reversing_multiplier_residue,
        reversing_translation_residue,
    )

    preserving_count = len(preserving_multipliers) * len(preserving_translations)
    reversing_count = len(reversing_multipliers) * len(reversing_translations)
    unsigned_count = preserving_count + reversing_count
    return RawAffineProfile(
        raw_order=RAW_ORDER,
        trace_order=TRACE_ORDER,
        positive_size=len(positive),
        negative_size=len(negative),
        sign_preserving_count=preserving_count,
        sign_reversing_count=reversing_count,
        unsigned_support_count=unsigned_count,
        unsigned_extra_count=quotient_profile.unsigned_extra_affines * TRACE_ORDER * TRACE_ORDER,
        preserving_multiplier_residue_mod_507=(preserving_multiplier_residue,),
        preserving_translation_residue_mod_507=(preserving_translation_residue,),
        reversing_multiplier_residue_mod_507=(reversing_multiplier_residue,),
        reversing_translation_residue_mod_507=(reversing_translation_residue,),
        preserving_multiplier_count=len(preserving_multipliers),
        reversing_multiplier_count=len(reversing_multipliers),
        trace_translation_count=len(preserving_translations),
        preserving_multipliers=preserving_multipliers,
        reversing_multipliers=reversing_multipliers,
        trace_translations=preserving_translations,
        all_preserving_lifts_check=all_lifts_match(
            positive,
            negative,
            preserving_multipliers,
            preserving_translations,
            reverse=False,
        ),
        all_reversing_lifts_check=all_lifts_match(
            positive,
            negative,
            reversing_multipliers,
            reversing_translations,
            reverse=True,
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge primitive affine-symmetry gate")
    positive, negative = primitive_sets()
    quotient_positive, quotient_negative = quotient_sets(positive, negative)
    quotient_profile = quotient_affine_profile(quotient_positive, quotient_negative)
    raw_profile = raw_affine_profile(positive, negative, quotient_profile)

    expected_quotient = QuotientAffineProfile(
        quotient_order=507,
        positive_residues=(121, 122, 123),
        negative_residues=(384, 385, 386),
        sign_preserving_affines=((1, 0),),
        sign_reversing_affines=((506, 0),),
        unsigned_support_affines=((1, 0), (506, 0)),
        unsigned_extra_affines=0,
    )
    expected_raw = RawAffineProfile(
        raw_order=12675,
        trace_order=25,
        positive_size=75,
        negative_size=75,
        sign_preserving_count=500,
        sign_reversing_count=500,
        unsigned_support_count=1000,
        unsigned_extra_count=0,
        preserving_multiplier_residue_mod_507=(1,),
        preserving_translation_residue_mod_507=(0,),
        reversing_multiplier_residue_mod_507=(506,),
        reversing_translation_residue_mod_507=(0,),
        preserving_multiplier_count=20,
        reversing_multiplier_count=20,
        trace_translation_count=25,
        preserving_multipliers=(1, 508, 1522, 2029, 2536, 3043, 4057, 4564, 5071, 5578, 6592, 7099, 7606, 8113, 9127, 9634, 10141, 10648, 11662, 12169),
        reversing_multipliers=(506, 1013, 2027, 2534, 3041, 3548, 4562, 5069, 5576, 6083, 7097, 7604, 8111, 8618, 9632, 10139, 10646, 11153, 12167, 12674),
        trace_translations=(0, 507, 1014, 1521, 2028, 2535, 3042, 3549, 4056, 4563, 5070, 5577, 6084, 6591, 7098, 7605, 8112, 8619, 9126, 9633, 10140, 10647, 11154, 11661, 12168),
        all_preserving_lifts_check=True,
        all_reversing_lifts_check=True,
    )
    row_ok = (
        quotient_profile == expected_quotient
        and raw_profile == expected_raw
        and raw_profile.sign_preserving_count
        == raw_profile.preserving_multiplier_count * raw_profile.trace_translation_count
        and raw_profile.sign_reversing_count
        == raw_profile.reversing_multiplier_count * raw_profile.trace_translation_count
    )

    print(f"quotient_affine_profile={quotient_profile}")
    print(f"raw_affine_profile={raw_profile}")
    print("affine_laws")
    print("  quotient C507: only identity preserves signs")
    print("  quotient C507: only inversion e -> -e swaps the positive and negative bridge layers")
    print("  raw C12675: sign-preserving lifts have a = 1 mod 507 and b = 0 mod 507")
    print("  raw C12675: sign-reversing lifts have a = -1 mod 507 and b = 0 mod 507")
    print("  all nontrivial raw freedom is C25 trace-fiber reindexing plus trace translation")
    print("interpretation")
    print("  primitive_bridge_has_no_hidden_quotient_affine_or_diamond_symmetry=1")
    print("  bridge_reversal_is_the_only_quotient_orientation_duplicate=1")
    print("  raw_affine_symmetries_are_only_trace_fiber_gauge_freedom=1")
    print("  producer_cannot_average_over_a_new_small_affine_orbit_to_get_the_bridge=1")
    print(f"square_axis_bridge_primitive_affine_symmetry_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_primitive_affine_symmetry_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
