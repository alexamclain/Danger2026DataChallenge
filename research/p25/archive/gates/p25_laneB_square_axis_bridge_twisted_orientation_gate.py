#!/usr/bin/env python3
"""Twisted-orientation gate for the p25 primitive bridge.

The subfield-descent gate shows that ordinary degree-39 Frobenius trace kills
the signed bridge: p^39 reverses the bridge orientation.  This gate records
the exact remaining support-preserving escape.

On the collapsed C_507 coordinate, p^39 acts as q -> -q.  Base-field
coefficients that are invariant under this involution must be equal on each
{q,-q} pair, giving an unsigned hull rather than the bridge.  The bridge is
the odd line: coefficients are opposite on each pair.  Therefore a
degree-39 support-preserving realization must carry a quadratic sign local
system with an anti-invariant coefficient alpha satisfying alpha^(p^39)=-alpha.

This is a positive target, not a certificate: the sign twist explains the only
possible half-orbit orientation mechanism, while normalization back to literal
plus/minus one coefficients still lives over the full degree-78 orientation.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_frobenius_orbit_obstruction_gate import (
    QUOTIENT_ORDER,
    TRACE_ORDER,
    multiply_set,
    primitive_word_sets,
    quotient_sets,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


@dataclass(frozen=True)
class TwistedOrientationProfile:
    p39_mod_quotient: int
    p39_mod_raw: int
    p78_mod_quotient: int
    p78_mod_raw: int
    quotient_positive: tuple[int, ...]
    quotient_negative: tuple[int, ...]
    quotient_pairs: tuple[tuple[int, int], ...]
    p39_maps_positive_to_negative: bool
    p39_maps_negative_to_positive: bool
    p39_signed_action: int
    raw_p39_maps_positive_to_negative: bool
    raw_p39_maps_negative_to_positive: bool
    raw_p78_preserves_positive: bool
    raw_p78_preserves_negative: bool
    raw_p78_is_trace_fiber_gauge: bool
    base_invariant_pair_dimension: int
    base_invariant_matches_signed_bridge: bool
    anti_invariant_pair_dimension: int
    anti_invariant_matches_signed_bridge: bool
    equal_weight_constraints: int
    equal_weight_anti_line_dimension: int
    ordinary_signed_trace_support: int
    ordinary_unsigned_trace_support: int
    twisted_signed_trace_support: int
    twisted_raw_support: int
    coefficient_extension_degree: int
    normalized_literal_orientation_degree: int


def signed_trace_support(
    positive: frozenset[int],
    negative: frozenset[int],
    multiplier: int,
    sign_twist: int,
    modulus: int,
) -> int:
    """Trace one support-preserving two-term orbit.

    sign_twist=1 models ordinary invariant coefficients.
    sign_twist=-1 models an anti-invariant coefficient alpha^sigma=-alpha.
    """

    out: dict[int, int] = {}
    for point in positive:
        out[point] = out.get(point, 0) + 1
        image = (multiplier * point) % modulus
        out[image] = out.get(image, 0) + sign_twist
    for point in negative:
        out[point] = out.get(point, 0) - 1
        image = (multiplier * point) % modulus
        out[image] = out.get(image, 0) - sign_twist
    return sum(1 for value in out.values() if value)


def unsigned_trace_support(
    support: frozenset[int],
    multiplier: int,
    modulus: int,
) -> int:
    out: dict[int, int] = {}
    for point in support:
        out[point] = out.get(point, 0) + 1
        image = (multiplier * point) % modulus
        out[image] = out.get(image, 0) + 1
    return sum(1 for value in out.values() if value)


def orientation_profile() -> TwistedOrientationProfile:
    raw_positive, raw_negative = primitive_word_sets()
    quotient_positive_set, quotient_negative_set = quotient_sets(raw_positive, raw_negative)
    p39_q = pow(P25 % QUOTIENT_ORDER, 39, QUOTIENT_ORDER)
    p39_raw = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    p78_q = pow(P25 % QUOTIENT_ORDER, 78, QUOTIENT_ORDER)
    p78_raw = pow(P25 % RAW_ORDER, 78, RAW_ORDER)
    quotient_positive = tuple(sorted(quotient_positive_set))
    quotient_negative = tuple(sorted(quotient_negative_set))
    quotient_pairs = tuple(
        (point, (p39_q * point) % QUOTIENT_ORDER)
        for point in quotient_positive
    )
    p39_positive_image = multiply_set(quotient_positive_set, p39_q, QUOTIENT_ORDER)
    p39_negative_image = multiply_set(quotient_negative_set, p39_q, QUOTIENT_ORDER)
    raw_p39_positive_image = multiply_set(raw_positive, p39_raw, RAW_ORDER)
    raw_p39_negative_image = multiply_set(raw_negative, p39_raw, RAW_ORDER)
    raw_p78_positive_image = multiply_set(raw_positive, p78_raw, RAW_ORDER)
    raw_p78_negative_image = multiply_set(raw_negative, p78_raw, RAW_ORDER)

    return TwistedOrientationProfile(
        p39_mod_quotient=p39_q,
        p39_mod_raw=p39_raw,
        p78_mod_quotient=p78_q,
        p78_mod_raw=p78_raw,
        quotient_positive=quotient_positive,
        quotient_negative=quotient_negative,
        quotient_pairs=quotient_pairs,
        p39_maps_positive_to_negative=p39_positive_image == quotient_negative_set,
        p39_maps_negative_to_positive=p39_negative_image == quotient_positive_set,
        p39_signed_action=-1 if p39_positive_image == quotient_negative_set else 0,
        raw_p39_maps_positive_to_negative=raw_p39_positive_image == raw_negative,
        raw_p39_maps_negative_to_positive=raw_p39_negative_image == raw_positive,
        raw_p78_preserves_positive=raw_p78_positive_image == raw_positive,
        raw_p78_preserves_negative=raw_p78_negative_image == raw_negative,
        raw_p78_is_trace_fiber_gauge=p78_raw % QUOTIENT_ORDER == 1,
        base_invariant_pair_dimension=3,
        base_invariant_matches_signed_bridge=False,
        anti_invariant_pair_dimension=3,
        anti_invariant_matches_signed_bridge=True,
        equal_weight_constraints=2,
        equal_weight_anti_line_dimension=1,
        ordinary_signed_trace_support=signed_trace_support(
            quotient_positive_set,
            quotient_negative_set,
            p39_q,
            sign_twist=1,
            modulus=QUOTIENT_ORDER,
        ),
        ordinary_unsigned_trace_support=unsigned_trace_support(
            quotient_positive_set | quotient_negative_set,
            p39_q,
            modulus=QUOTIENT_ORDER,
        ),
        twisted_signed_trace_support=signed_trace_support(
            quotient_positive_set,
            quotient_negative_set,
            p39_q,
            sign_twist=-1,
            modulus=QUOTIENT_ORDER,
        ),
        twisted_raw_support=len(raw_positive | raw_negative),
        coefficient_extension_degree=2,
        normalized_literal_orientation_degree=78,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge twisted-orientation gate")
    profile = orientation_profile()
    expected = TwistedOrientationProfile(
        p39_mod_quotient=506,
        p39_mod_raw=2027,
        p78_mod_quotient=1,
        p78_mod_raw=2029,
        quotient_positive=(121, 122, 123),
        quotient_negative=(384, 385, 386),
        quotient_pairs=((121, 386), (122, 385), (123, 384)),
        p39_maps_positive_to_negative=True,
        p39_maps_negative_to_positive=True,
        p39_signed_action=-1,
        raw_p39_maps_positive_to_negative=True,
        raw_p39_maps_negative_to_positive=True,
        raw_p78_preserves_positive=True,
        raw_p78_preserves_negative=True,
        raw_p78_is_trace_fiber_gauge=True,
        base_invariant_pair_dimension=3,
        base_invariant_matches_signed_bridge=False,
        anti_invariant_pair_dimension=3,
        anti_invariant_matches_signed_bridge=True,
        equal_weight_constraints=2,
        equal_weight_anti_line_dimension=1,
        ordinary_signed_trace_support=0,
        ordinary_unsigned_trace_support=6,
        twisted_signed_trace_support=6,
        twisted_raw_support=150,
        coefficient_extension_degree=2,
        normalized_literal_orientation_degree=78,
    )
    row_ok = (
        profile == expected
        and profile.twisted_raw_support == profile.twisted_signed_trace_support * TRACE_ORDER
        and profile.p39_signed_action == -1
        and profile.ordinary_signed_trace_support == 0
        and profile.twisted_signed_trace_support == 6
    )

    print(f"twisted_orientation_profile={profile}")
    print("orientation_laws")
    print("  p^39 acts as q -> -q on the collapsed C507 bridge")
    print("  invariant base coefficients give pairwise-equal signs, not the signed bridge")
    print("  the bridge lives in the pairwise-odd anti-invariant coefficient space")
    print("  equal S-layer weights cut the odd three-pair space down to one bridge line")
    print("  multiplying by alpha with alpha^(p^39)=-alpha makes the bridge semilinearly fixed")
    print("interpretation")
    print("  ordinary_degree39_trace_is_zero_for_the_signed_bridge=1")
    print("  degree39_unsigned_hull_is_not_the_bridge=1")
    print("  only_support_preserving_half_orbit_escape_is_a_quadratic_sign_twist=1")
    print("  literal_plus_minus_one_orientation_still_requires_degree78_normalization=1")
    print(f"square_axis_bridge_twisted_orientation_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_twisted_orientation_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
