#!/usr/bin/env python3
"""Subfield descent obstruction for the p25 primitive bridge.

The formal bridge is tiny in the raw source coordinate, but an arithmetic
producer still has to orient it under Frobenius.  The previous orbit gate
checked the full p and p^2 orbit closures.  This gate checks every subfield
degree of the minimal Frobenius orbit degree 78.

For a signed divisor over F_{p^d}, the ordinary Frobenius trace under p^d
must either recover the bridge or produce an admissible replacement.  Every
proper divisor d of 78 either cancels the signed bridge to zero or expands the
nonzero payload beyond the six quotient cells / 150 raw cells.  The only
proper degree preserving the six-cell support is d=39, where p^39 reverses the
bridge orientation, so the ordinary trace is zero; extracting the orientation
requires a p^39-anti-invariant coefficient and hence degree 78.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_frobenius_orbit_obstruction_gate import (
    QUOTIENT_ORDER,
    TRACE_ORDER,
    multiply_set,
    orbit_words,
    pairwise_support_intersections,
    primitive_word_sets,
    quotient_sets,
    signed_sum_support,
    support_union,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


SUBFIELD_DEGREES = (1, 2, 3, 6, 13, 26, 39, 78)


@dataclass(frozen=True)
class SubfieldDescentRow:
    degree: int
    multiplier: int
    orbit_order: int
    first_preserves_signed: bool
    first_reverses_signed: bool
    first_preserves_support: bool
    ordinary_trace_support: int
    ordinary_trace_positive: int
    ordinary_trace_negative: int
    ordinary_trace_zero: bool
    closure_quotient_support: int
    closure_raw_support: int
    raw_trace_support: int
    raw_trace_positive: int
    raw_trace_negative: int
    pairwise_support_intersections: int


@dataclass(frozen=True)
class SubfieldDescentProfile:
    p_mod_quotient: int
    p_order_quotient: int
    quotient_support: int
    raw_support: int
    rows: tuple[SubfieldDescentRow, ...]
    proper_nonzero_min_ordinary_trace_support: int
    proper_nonzero_min_raw_trace_support: int
    proper_support_preserving_degrees: tuple[int, ...]
    proper_signed_preserving_degrees: tuple[int, ...]
    proper_signed_reversing_degrees: tuple[int, ...]
    ordinary_descent_degrees_matching_bridge: tuple[int, ...]
    anti_invariant_half_degree: int
    orientation_min_degree: int


def multiplicative_order(value: int, modulus: int) -> int:
    current = 1
    for order in range(1, modulus + 1):
        current = current * value % modulus
        if current == 1:
            return order
    raise AssertionError(f"order of {value} mod {modulus} exceeds {modulus}")


def subfield_row(degree: int) -> SubfieldDescentRow:
    raw_positive, raw_negative = primitive_word_sets()
    quotient_positive, quotient_negative = quotient_sets(raw_positive, raw_negative)

    multiplier = pow(P25 % QUOTIENT_ORDER, degree, QUOTIENT_ORDER)
    raw_multiplier = pow(P25 % RAW_ORDER, degree, RAW_ORDER)
    orbit_order = multiplicative_order(multiplier, QUOTIENT_ORDER)

    first_positive = multiply_set(quotient_positive, multiplier, QUOTIENT_ORDER)
    first_negative = multiply_set(quotient_negative, multiplier, QUOTIENT_ORDER)
    quotient_words = orbit_words(
        quotient_positive,
        quotient_negative,
        multiplier,
        orbit_order,
        QUOTIENT_ORDER,
    )
    raw_words = orbit_words(
        raw_positive,
        raw_negative,
        raw_multiplier,
        orbit_order,
        RAW_ORDER,
    )
    ordinary_trace = signed_sum_support(
        quotient_positive,
        quotient_negative,
        multiplier,
        orbit_order,
        QUOTIENT_ORDER,
    )
    raw_trace = signed_sum_support(
        raw_positive,
        raw_negative,
        raw_multiplier,
        orbit_order,
        RAW_ORDER,
    )

    return SubfieldDescentRow(
        degree=degree,
        multiplier=multiplier,
        orbit_order=orbit_order,
        first_preserves_signed=first_positive == quotient_positive and first_negative == quotient_negative,
        first_reverses_signed=first_positive == quotient_negative and first_negative == quotient_positive,
        first_preserves_support=(first_positive | first_negative)
        == (quotient_positive | quotient_negative),
        ordinary_trace_support=len(ordinary_trace),
        ordinary_trace_positive=sum(1 for value in ordinary_trace.values() if value > 0),
        ordinary_trace_negative=sum(1 for value in ordinary_trace.values() if value < 0),
        ordinary_trace_zero=not ordinary_trace,
        closure_quotient_support=len(support_union(quotient_words)),
        closure_raw_support=len(support_union(raw_words)),
        raw_trace_support=len(raw_trace),
        raw_trace_positive=sum(1 for value in raw_trace.values() if value > 0),
        raw_trace_negative=sum(1 for value in raw_trace.values() if value < 0),
        pairwise_support_intersections=pairwise_support_intersections(quotient_words),
    )


def descent_profile() -> SubfieldDescentProfile:
    raw_positive, raw_negative = primitive_word_sets()
    quotient_positive, quotient_negative = quotient_sets(raw_positive, raw_negative)
    p_mod_quotient = P25 % QUOTIENT_ORDER
    rows = tuple(subfield_row(degree) for degree in SUBFIELD_DEGREES)
    proper_rows = rows[:-1]
    proper_nonzero_rows = tuple(row for row in proper_rows if not row.ordinary_trace_zero)
    ordinary_matching = tuple(
        row.degree
        for row in rows
        if row.ordinary_trace_support == len(quotient_positive | quotient_negative)
        and row.raw_trace_support == len(raw_positive | raw_negative)
        and not row.ordinary_trace_zero
    )
    return SubfieldDescentProfile(
        p_mod_quotient=p_mod_quotient,
        p_order_quotient=multiplicative_order(p_mod_quotient, QUOTIENT_ORDER),
        quotient_support=len(quotient_positive | quotient_negative),
        raw_support=len(raw_positive | raw_negative),
        rows=rows,
        proper_nonzero_min_ordinary_trace_support=min(
            row.ordinary_trace_support for row in proper_nonzero_rows
        ),
        proper_nonzero_min_raw_trace_support=min(row.raw_trace_support for row in proper_nonzero_rows),
        proper_support_preserving_degrees=tuple(
            row.degree for row in proper_rows if row.first_preserves_support
        ),
        proper_signed_preserving_degrees=tuple(
            row.degree for row in proper_rows if row.first_preserves_signed
        ),
        proper_signed_reversing_degrees=tuple(
            row.degree for row in proper_rows if row.first_reverses_signed
        ),
        ordinary_descent_degrees_matching_bridge=ordinary_matching,
        anti_invariant_half_degree=39,
        orientation_min_degree=78,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge subfield-descent gate")
    profile = descent_profile()
    expected_rows = (
        SubfieldDescentRow(1, 218, 78, False, False, False, 0, 0, 0, True, 234, 5850, 0, 0, 0, 39),
        SubfieldDescentRow(2, 373, 39, False, False, False, 234, 117, 117, False, 234, 5850, 5850, 2925, 2925, 0),
        SubfieldDescentRow(3, 194, 26, False, False, False, 0, 0, 0, True, 78, 1950, 0, 0, 0, 13),
        SubfieldDescentRow(6, 118, 13, False, False, False, 78, 39, 39, False, 78, 1950, 1950, 975, 975, 0),
        SubfieldDescentRow(13, 23, 6, False, False, False, 0, 0, 0, True, 18, 450, 0, 0, 0, 3),
        SubfieldDescentRow(26, 22, 3, False, False, False, 18, 9, 9, False, 18, 450, 450, 225, 225, 0),
        SubfieldDescentRow(39, 506, 2, False, True, True, 0, 0, 0, True, 6, 150, 0, 0, 0, 1),
        SubfieldDescentRow(78, 1, 1, True, False, True, 6, 3, 3, False, 6, 150, 150, 75, 75, 0),
    )
    expected = SubfieldDescentProfile(
        p_mod_quotient=218,
        p_order_quotient=78,
        quotient_support=6,
        raw_support=150,
        rows=expected_rows,
        proper_nonzero_min_ordinary_trace_support=18,
        proper_nonzero_min_raw_trace_support=450,
        proper_support_preserving_degrees=(39,),
        proper_signed_preserving_degrees=(),
        proper_signed_reversing_degrees=(39,),
        ordinary_descent_degrees_matching_bridge=(78,),
        anti_invariant_half_degree=39,
        orientation_min_degree=78,
    )
    row_ok = (
        profile == expected
        and profile.quotient_support * TRACE_ORDER == profile.raw_support
        and profile.proper_nonzero_min_ordinary_trace_support > profile.quotient_support
        and profile.proper_nonzero_min_raw_trace_support > profile.raw_support
        and profile.ordinary_descent_degrees_matching_bridge == (profile.orientation_min_degree,)
    )

    print(f"subfield_descent_profile={profile}")
    print("subfield_rows")
    for row in profile.rows:
        print(
            "  "
            f"d={row.degree} mult={row.multiplier} orbit={row.orbit_order} "
            f"trace_support={row.ordinary_trace_support} "
            f"raw_trace_support={row.raw_trace_support} "
            f"closure={row.closure_quotient_support}/{row.closure_raw_support} "
            f"preserve={int(row.first_preserves_signed)} "
            f"reverse={int(row.first_reverses_signed)} "
            f"support_preserve={int(row.first_preserves_support)}"
        )
    print("descent_laws")
    print("  no proper ordinary Frobenius subfield trace recovers the signed bridge")
    print("  every proper nonzero ordinary trace has at least 18 quotient cells and 450 raw cells")
    print("  degree 39 preserves only the unsigned support and reverses signs, so its ordinary trace is zero")
    print("  orienting the degree-39 anti-invariant bridge requires degree 78 coefficients")
    print("interpretation")
    print("  bridge_cannot_be_a_proper_subfield_rational_signed_divisor=1")
    print("  cheap_Fp_Fp2_Fp6_Fp13_Fp26_descent_expands_or_cancels=1")
    print("  degree_39_shadow_is_anti_invariant_not_a_certificate=1")
    print("  producer_must_supply_full_degree_78_orientation_or_equivalent_nonsplit_identity=1")
    print(f"square_axis_bridge_subfield_descent_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_subfield_descent_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
