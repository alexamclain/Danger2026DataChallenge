#!/usr/bin/env python3
"""Sparse theta2 producer intake for the p25 KSY/theta route.

The bridge sparse-source harness requires a theorem hit to emit the final
150-cell bridge.  The theta2 resolvent gate weakens that producer burden:
a theorem may instead emit the 300-cell theta2 divisor footprint

    theta2 = 4*bridge - [2]bridge

or the inverse footprint.  This harness coalesces sparse source triples,
checks whether they match theta2 or theta2^-1, applies the finite resolvent,
and audits the recovered bridge contract.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_robert_ksy_theta2_resolvent_gate import (
    SQRT_FLOOR,
    weighted_resolvent_numerator,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import SUPPORT_PERIOD
from p25_laneB_robert_ksy_y_doubling_distribution_gate import (
    divide_ring_exact,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import scale_ring
from p25_laneB_robert_sparse_source_candidate_harness_gate import (
    SparseEntry,
    parse_sparse_source,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER


@dataclass(frozen=True)
class KsyTheta2CandidateProfile:
    name: str
    input_terms: int
    active_source_terms: int
    duplicate_source_terms: int
    candidate_support: int
    candidate_coefficient_counts: tuple[tuple[int, int], ...]
    exact_theta2: bool
    exact_theta2_inverse: bool
    resolvent_divisible: bool
    recovered_support: int
    recovered_sign: int
    normalized_recovered_profile: CandidateProfile
    shifted_theta2_union_support: int
    shifted_theta2_term_budget: int
    term_budget_below_sqrt: bool
    ok: bool


def add_ring_entry(ring: Ring, coord: tuple[int, int], coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def sparse_entries_to_ring(entries: tuple[SparseEntry, ...]) -> tuple[Ring, int, int]:
    source_terms: dict[tuple[int, int], int] = {}
    duplicate_terms = 0
    for right_log, c_log, coefficient in entries:
        coord = (right_log % RIGHT_ORDER, c_log % C_ORDER)
        duplicate_terms += int(coord in source_terms)
        add_ring_entry(source_terms, coord, coefficient)
    return dict(sorted(source_terms.items())), len(source_terms), duplicate_terms


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def theta2_target_rings() -> tuple[Ring, Ring, Ring]:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2_inverse = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2 = scale_ring(theta2_inverse, -1)
    return bridge, theta2, theta2_inverse


def theta2_sparse_entries(ring: Ring) -> tuple[SparseEntry, ...]:
    return tuple((right_log, c_log, coefficient) for (right_log, c_log), coefficient in ring.items())


def recover_by_resolvent(candidate: Ring) -> tuple[Ring | None, bool, int, int]:
    denominator = 4 ** SUPPORT_PERIOD - 1
    numerator, union_support, _returns_after_order, term_budget = weighted_resolvent_numerator(
        candidate,
        SUPPORT_PERIOD,
    )
    try:
        recovered = divide_ring_exact(numerator, denominator)
    except AssertionError:
        return None, False, union_support, term_budget
    return recovered, True, union_support, term_budget


def profile_theta2_candidate(name: str, entries: tuple[SparseEntry, ...]) -> KsyTheta2CandidateProfile:
    bridge, theta2, theta2_inverse = theta2_target_rings()
    candidate, active_terms, duplicate_terms = sparse_entries_to_ring(entries)
    recovered, divisible, union_support, term_budget = recover_by_resolvent(candidate)
    recovered_sign = 0
    normalized: Ring = {}
    if recovered == bridge:
        recovered_sign = 1
        normalized = recovered
    elif recovered == scale_ring(bridge, -1):
        recovered_sign = -1
        normalized = scale_ring(recovered, -1)
    normalized_profile = bridge_profile(f"{name}_theta2_resolvent_normalized_bridge", normalized)
    ok = (
        active_terms == 300
        and len(candidate) == 300
        and (candidate == theta2 or candidate == theta2_inverse)
        and divisible
        and recovered_sign in (-1, 1)
        and normalized_profile.ok
        and term_budget == 46800
        and union_support == 11700
        and term_budget < SQRT_FLOOR
    )
    return KsyTheta2CandidateProfile(
        name=name,
        input_terms=len(entries),
        active_source_terms=active_terms,
        duplicate_source_terms=duplicate_terms,
        candidate_support=len(candidate),
        candidate_coefficient_counts=coefficient_counts(candidate),
        exact_theta2=candidate == theta2,
        exact_theta2_inverse=candidate == theta2_inverse,
        resolvent_divisible=divisible,
        recovered_support=0 if recovered is None else len(recovered),
        recovered_sign=recovered_sign,
        normalized_recovered_profile=normalized_profile,
        shifted_theta2_union_support=union_support,
        shifted_theta2_term_budget=term_budget,
        term_budget_below_sqrt=term_budget < SQRT_FLOOR,
        ok=ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit sparse C_75 x C_169 theta2 source-coordinate triples "
            "and recover the p25 bridge by the finite theta2 resolvent."
        )
    )
    parser.add_argument(
        "--sparse-source",
        type=Path,
        help="optional text file of triples: right_log c_log coefficient",
    )
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/theta2 sparse candidate harness")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        "format='right_log c_log coefficient'"
    )

    bridge, theta2, theta2_inverse = theta2_target_rings()
    if args.sparse_source is not None:
        profile = profile_theta2_candidate(
            str(args.sparse_source),
            parse_sparse_source(args.sparse_source),
        )
        print("mode=theta2_sparse_candidate")
        print(f"theta2_candidate_profile={profile}")
        print("candidate_contract")
        print("  pass requires exact theta2 or theta2_inverse sparse source footprint")
        print("  pass requires finite resolvent recovery of the exact bridge up to global sign")
        print(f"robert_ksy_theta2_candidate_harness_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_candidate_harness_candidate")
        return 0 if profile.ok else 1

    theta2_profile = profile_theta2_candidate(
        "target_theta2_roundtrip",
        theta2_sparse_entries(theta2),
    )
    inverse_profile = profile_theta2_candidate(
        "target_theta2_inverse_roundtrip",
        theta2_sparse_entries(theta2_inverse),
    )
    bridge_control = profile_theta2_candidate(
        "bridge_is_not_theta2_control",
        theta2_sparse_entries(bridge),
    )
    row_ok = (
        theta2_profile.ok
        and inverse_profile.ok
        and not bridge_control.ok
        and theta2_profile.exact_theta2
        and theta2_profile.recovered_sign == 1
        and inverse_profile.exact_theta2_inverse
        and inverse_profile.recovered_sign == -1
        and bridge_control.active_source_terms == 150
        and bridge_control.candidate_support == 150
        and not bridge_control.exact_theta2
        and not bridge_control.exact_theta2_inverse
    )
    print(f"target_theta2_profile={theta2_profile}")
    print(f"target_theta2_inverse_profile={inverse_profile}")
    print(f"bridge_control_profile={bridge_control}")
    print("intake_laws")
    print("  theorem_hit_may_emit_theta2_or_theta2_inverse_sparse_triples=1")
    print("  finite_resolvent_recovers_bridge_from_theta2=1")
    print("  finite_resolvent_recovers_negative_bridge_from_theta2_inverse=1")
    print("  global_sign_normalization_then_passes_existing_bridge_contract=1")
    print("  plain_bridge_sparse_source_is_not_accepted_as_theta2_candidate=1")
    print(f"robert_ksy_theta2_candidate_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_candidate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
