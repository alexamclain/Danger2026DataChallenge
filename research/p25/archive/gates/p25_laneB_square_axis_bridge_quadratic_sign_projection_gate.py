#!/usr/bin/env python3
"""Quadratic sign projection gate for the p25 primitive bridge.

The twisted-orientation route needs an anti-invariant coefficient alpha with
alpha^(p^39) = -alpha.  This makes alpha times the signed bridge semilinearly
fixed, but it does not produce a literal base-field bridge by taking ordinary
trace or invariant scalar projections.

This gate records that distinction.  The ordinary p^39 trace of the signed
bridge is zero.  The natural invariant projection obtained by forgetting the
quadratic sign, e.g. coefficient-square/norm/absolute-value on the bridge
coefficients, is the unsigned hull.  That hull keeps several tempting harness
adjacent invariants, but it has nonzero degree and the wrong signed quotient
trace, so it is not a producer certificate.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    quotient_trace,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_frobenius_orbit_obstruction_gate import (
    multiply_set,
    primitive_word_sets,
    quotient_sets,
    signed_sum_support,
)
from p25_laneB_square_axis_bridge_gauge_orbit_union_gate import p39_orbits
from p25_laneB_square_axis_bridge_raw_source_character_gate import raw_source_mask
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER


@dataclass(frozen=True)
class ProjectionCandidateSummary:
    name: str
    raw_support: int
    quotient_support: int
    trace_values: tuple[tuple[int, int], ...]
    integer_degree: int
    normalized_quotient_degree: int
    trace_correct: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    quotient_scalar_nonzero: int
    quotient_mixed_nonzero: int
    ok: bool


@dataclass(frozen=True)
class QuadraticSignProjectionProfile:
    p39_quotient: int
    p39_raw: int
    p39_positive_to_negative: bool
    p39_negative_to_positive: bool
    signed_ordinary_half_trace_support: int
    signed_ordinary_half_trace_raw_support: int
    unsigned_half_trace_support: int
    unsigned_half_trace_value_histogram: tuple[tuple[int, int], ...]
    orbit_count: int
    orbit_signed_sum_histogram: tuple[tuple[int, int], ...]
    orbit_sign_balance_histogram: tuple[tuple[tuple[tuple[int, int], ...], int], ...]
    signed_bridge: ProjectionCandidateSummary
    ordinary_trace_zero: ProjectionCandidateSummary
    unsigned_hull: ProjectionCandidateSummary
    coefficient_square_equals_unsigned_hull: bool
    invariant_projection_keeps_harness_adjacent_structure: bool
    invariant_projection_fails_signed_bridge: bool
    anti_invariant_line_required: bool


def signed_value(value: int, modulus: int) -> int:
    value %= modulus
    if value > modulus // 2:
        return value - modulus
    return value


def candidate_summary(name: str, raw: list[int], target: list[int]) -> ProjectionCandidateSummary:
    candidate = profile_candidate(name, raw, target)
    trace = quotient_trace(raw)
    return ProjectionCandidateSummary(
        name=name,
        raw_support=candidate.raw_support,
        quotient_support=candidate.quotient_support,
        trace_values=tuple((index, value) for index, value in enumerate(trace) if value),
        integer_degree=sum(raw),
        normalized_quotient_degree=sum(trace),
        trace_correct=candidate.trace_correct,
        block_constancy_hits=candidate.block_constancy_hits,
        kernel_modes=candidate.kernel_modes,
        raw_relation_mismatches=candidate.raw_relation_mismatches,
        quotient_scalar_nonzero=candidate.quotient_scalar_nonzero,
        quotient_mixed_nonzero=candidate.quotient_mixed_nonzero,
        ok=candidate.ok,
    )


def unsigned_half_trace_profile(points: frozenset[int], multiplier: int) -> tuple[int, tuple[tuple[int, int], ...]]:
    out: Counter[int] = Counter()
    for point in points:
        out[point] += 1
        out[(multiplier * point) % QUOTIENT_ORDER] += 1
    return len(out), tuple(sorted(Counter(out.values()).items()))


def projection_profile() -> QuadraticSignProjectionProfile:
    target = target_raw_bridge()
    unsigned_hull = [abs(value) for value in target]
    ordinary_zero = [0] * RAW_ORDER

    raw_positive, raw_negative = primitive_word_sets()
    quotient_positive, quotient_negative = quotient_sets(raw_positive, raw_negative)
    p39_q = pow(P25 % QUOTIENT_ORDER, 39, QUOTIENT_ORDER)
    p39_raw = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    signed_half_trace = signed_sum_support(
        quotient_positive,
        quotient_negative,
        p39_q,
        2,
        QUOTIENT_ORDER,
    )
    signed_raw_half_trace = signed_sum_support(
        raw_positive,
        raw_negative,
        p39_raw,
        2,
        RAW_ORDER,
    )
    unsigned_support, unsigned_value_histogram = unsigned_half_trace_profile(
        quotient_positive | quotient_negative,
        p39_q,
    )

    mask = raw_source_mask()
    orbit_signed_sums: list[int] = []
    orbit_sign_balances: list[tuple[tuple[int, int], ...]] = []
    for orbit in p39_orbits():
        orbit_signed_sums.append(sum(mask[coord] for coord in orbit))
        orbit_sign_balances.append(tuple(sorted(Counter(mask[coord] for coord in orbit).items())))

    signed_summary = candidate_summary("signed_bridge", target, target)
    zero_summary = candidate_summary("ordinary_trace_zero", ordinary_zero, target)
    unsigned_summary = candidate_summary("unsigned_hull", unsigned_hull, target)

    coefficient_square = [1 if value else 0 for value in target]
    return QuadraticSignProjectionProfile(
        p39_quotient=p39_q,
        p39_raw=p39_raw,
        p39_positive_to_negative=multiply_set(quotient_positive, p39_q, QUOTIENT_ORDER)
        == quotient_negative,
        p39_negative_to_positive=multiply_set(quotient_negative, p39_q, QUOTIENT_ORDER)
        == quotient_positive,
        signed_ordinary_half_trace_support=len(signed_half_trace),
        signed_ordinary_half_trace_raw_support=len(signed_raw_half_trace),
        unsigned_half_trace_support=unsigned_support,
        unsigned_half_trace_value_histogram=unsigned_value_histogram,
        orbit_count=len(orbit_signed_sums),
        orbit_signed_sum_histogram=tuple(sorted(Counter(orbit_signed_sums).items())),
        orbit_sign_balance_histogram=tuple(sorted(Counter(orbit_sign_balances).items())),
        signed_bridge=signed_summary,
        ordinary_trace_zero=zero_summary,
        unsigned_hull=unsigned_summary,
        coefficient_square_equals_unsigned_hull=coefficient_square == unsigned_hull,
        invariant_projection_keeps_harness_adjacent_structure=(
            unsigned_summary.raw_support == signed_summary.raw_support
            and unsigned_summary.quotient_support == signed_summary.quotient_support
            and unsigned_summary.block_constancy_hits == QUOTIENT_ORDER
            and unsigned_summary.kernel_modes == (0,)
            and unsigned_summary.raw_relation_mismatches == 0
            and unsigned_summary.quotient_mixed_nonzero == signed_summary.quotient_mixed_nonzero
        ),
        invariant_projection_fails_signed_bridge=(
            not unsigned_summary.trace_correct
            and unsigned_summary.normalized_quotient_degree == 6
            and unsigned_summary.integer_degree == 150
            and unsigned_summary.quotient_scalar_nonzero == 1
            and not unsigned_summary.ok
        ),
        anti_invariant_line_required=signed_summary.ok and not zero_summary.ok and not unsigned_summary.ok,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge quadratic sign-projection gate")
    profile = projection_profile()
    expected_signed = ProjectionCandidateSummary(
        name="signed_bridge",
        raw_support=150,
        quotient_support=6,
        trace_values=((25, 1), (138, -1), (197, 1), (310, -1), (369, 1), (482, -1)),
        integer_degree=0,
        normalized_quotient_degree=0,
        trace_correct=True,
        block_constancy_hits=507,
        kernel_modes=(0,),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=0,
        quotient_mixed_nonzero=336,
        ok=True,
    )
    expected_zero = ProjectionCandidateSummary(
        name="ordinary_trace_zero",
        raw_support=0,
        quotient_support=0,
        trace_values=(),
        integer_degree=0,
        normalized_quotient_degree=0,
        trace_correct=False,
        block_constancy_hits=507,
        kernel_modes=(),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=0,
        quotient_mixed_nonzero=0,
        ok=False,
    )
    expected_unsigned = ProjectionCandidateSummary(
        name="unsigned_hull",
        raw_support=150,
        quotient_support=6,
        trace_values=((25, 1), (138, 1), (197, 1), (310, 1), (369, 1), (482, 1)),
        integer_degree=150,
        normalized_quotient_degree=6,
        trace_correct=False,
        block_constancy_hits=507,
        kernel_modes=(0,),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=1,
        quotient_mixed_nonzero=336,
        ok=False,
    )
    expected = QuadraticSignProjectionProfile(
        p39_quotient=506,
        p39_raw=2027,
        p39_positive_to_negative=True,
        p39_negative_to_positive=True,
        signed_ordinary_half_trace_support=0,
        signed_ordinary_half_trace_raw_support=0,
        unsigned_half_trace_support=6,
        unsigned_half_trace_value_histogram=((2, 6),),
        orbit_count=15,
        orbit_signed_sum_histogram=((0, 15),),
        orbit_sign_balance_histogram=(
            (((-1, 1), (1, 1)), 3),
            (((-1, 2), (1, 2)), 6),
            (((-1, 10), (1, 10)), 6),
        ),
        signed_bridge=expected_signed,
        ordinary_trace_zero=expected_zero,
        unsigned_hull=expected_unsigned,
        coefficient_square_equals_unsigned_hull=True,
        invariant_projection_keeps_harness_adjacent_structure=True,
        invariant_projection_fails_signed_bridge=True,
        anti_invariant_line_required=True,
    )
    row_ok = profile == expected

    print(f"quadratic_sign_projection_profile={profile}")
    print("projection_laws")
    print("  ordinary p^39 trace of the signed bridge is zero on quotient and raw lift")
    print("  every p^39 raw orbit has balanced positive and negative coefficients")
    print("  coefficient-square/norm/absolute-value projection is the unsigned hull")
    print("  unsigned hull keeps block constancy, kernel mode {0}, raw relation, and mixed character mass")
    print("  unsigned hull fails signed trace, degree zero, and the bridge harness")
    print("interpretation")
    print("  quadratic_sign_twist_cannot_be_eliminated_by_base_invariant_projection=1")
    print("  semilinear_fixed_alpha_bridge_is_not_a_literal_base_field_certificate=1")
    print("  arithmetic_candidate_must_realize_the_anti_invariant_line_or_equivalent_identity=1")
    print(f"square_axis_bridge_quadratic_sign_projection_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_quadratic_sign_projection_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
