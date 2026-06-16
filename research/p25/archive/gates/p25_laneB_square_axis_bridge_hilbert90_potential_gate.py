#!/usr/bin/env python3
"""Hilbert-90 potential gate for the p25 square-axis bridge.

The quadratic sign route naturally suggests a Hilbert-90 style boundary:

    bridge = (1 - sigma) F,    sigma = p^39.

This gate records what that buys and what it does not buy.  The sparse
potentials are exactly the two oriented half-bridges, but they have degree
+/-75.  Degree-zero repair either introduces a non-block-constant fixed-point
spike or a block-constant scalar q=0 block; neither is a bridge producer.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    crt_source_to_raw,
    profile_candidate,
    quotient_trace,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_gauge_orbit_union_gate import p39_orbits
from p25_laneB_square_axis_bridge_half_frobenius_gauge_gate import multiply_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    RAW_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class PotentialSummary:
    name: str
    boundary_ok: bool
    raw_support: int
    quotient_support: int
    trace_values: tuple[tuple[int, int], ...]
    integer_degree: int
    normalized_quotient_degree: int
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    quotient_scalar_nonzero: int
    quotient_pure_c_nonzero: int
    quotient_mixed_nonzero: int
    ok: bool


@dataclass(frozen=True)
class Hilbert90PotentialProfile:
    p39_raw: int
    p39_quotient: int
    full_orbit_count: int
    full_orbit_size_histogram: tuple[tuple[int, int], ...]
    bridge_orbit_count: int
    bridge_orbit_size_histogram: tuple[tuple[int, int], ...]
    minimal_bridge_potential_support: int
    minimal_bridge_degree_min: int
    minimal_bridge_degree_max: int
    minimal_bridge_degree_count: int
    same_support_degree_zero_possible: bool
    invariant_quotient_blocks: tuple[int, ...]
    positive_potential: PotentialSummary
    negative_potential: PotentialSummary
    fixed_point_degree_repair: PotentialSummary
    quotient_scalar_degree_repair: PotentialSummary
    half_boundary_is_real: bool
    degree_zero_repair_is_not_producer: bool


def all_source_coords() -> tuple[Coord, ...]:
    return tuple((right, c_log) for right in range(RIGHT_ORDER) for c_log in range(C_ORDER))


def raw_from_source_values(values: dict[Coord, int]) -> list[int]:
    raw = [0] * RAW_ORDER
    for coord, value in values.items():
        raw[crt_source_to_raw(*coord)] = value
    return raw


def source_values_from_raw(raw: list[int]) -> dict[Coord, int]:
    return {
        (e_value % RIGHT_ORDER, e_value % C_ORDER): value
        for e_value, value in enumerate(raw)
        if value
    }


def boundary_ok(raw: list[int], sigma: int) -> bool:
    target = raw_source_mask()
    values = source_values_from_raw(raw)
    for coord in all_source_coords():
        image = multiply_coord(coord, sigma)
        if values.get(coord, 0) - values.get(image, 0) != target.get(coord, 0):
            return False
    return True


def summarize(name: str, raw: list[int], sigma: int) -> PotentialSummary:
    candidate = profile_candidate(name, raw, target_raw_bridge())
    trace = quotient_trace(raw)
    return PotentialSummary(
        name=name,
        boundary_ok=boundary_ok(raw, sigma),
        raw_support=candidate.raw_support,
        quotient_support=candidate.quotient_support,
        trace_values=tuple((index, value) for index, value in enumerate(trace) if value),
        integer_degree=sum(raw),
        normalized_quotient_degree=sum(trace),
        block_constancy_hits=candidate.block_constancy_hits,
        kernel_modes=candidate.kernel_modes,
        raw_relation_mismatches=candidate.raw_relation_mismatches,
        quotient_scalar_nonzero=candidate.quotient_scalar_nonzero,
        quotient_pure_c_nonzero=candidate.quotient_pure_c_nonzero,
        quotient_mixed_nonzero=candidate.quotient_mixed_nonzero,
        ok=candidate.ok,
    )


def half_potential(sign: int) -> list[int]:
    values = {
        coord: sign
        for coord, value in raw_source_mask().items()
        if value == sign
    }
    return raw_from_source_values(values)


def fixed_point_degree_repair(raw: list[int]) -> list[int]:
    repaired = raw.copy()
    repaired[crt_source_to_raw(0, 0)] -= sum(repaired)
    return repaired


def quotient_scalar_degree_repair(raw: list[int]) -> list[int]:
    degree = sum(raw)
    if degree % 25:
        raise AssertionError("block-constant scalar repair requires degree divisible by 25")
    repaired = raw.copy()
    scalar = -degree // 25
    for layer in range(25):
        repaired[QUOTIENT_ORDER * layer] += scalar
    return repaired


def full_p39_orbits(sigma: int) -> tuple[tuple[Coord, ...], ...]:
    unseen = set(all_source_coords())
    rows: list[tuple[Coord, ...]] = []
    while unseen:
        start = next(iter(unseen))
        orbit: list[Coord] = []
        point = start
        while point not in orbit:
            orbit.append(point)
            unseen.discard(point)
            point = multiply_coord(point, sigma)
        rows.append(tuple(orbit))
    return tuple(sorted(rows, key=lambda orbit: (len(orbit), orbit)))


def orbit_potential_values(orbit: tuple[Coord, ...]) -> tuple[int, ...]:
    mask = raw_source_mask()
    values: list[int] = []
    partial = 0
    for index, coord in enumerate(orbit):
        if index == 0:
            values.append(0)
        else:
            partial += mask[orbit[index - 1]]
            values.append(-partial)
    if sum(mask[coord] for coord in orbit):
        raise AssertionError("bridge orbit has nonzero signed sum")
    return tuple(values)


def minimal_bridge_degree_data() -> tuple[int, int, int, int, bool]:
    supports = 0
    possible_degrees: set[int] = {0}
    for orbit in p39_orbits():
        values = orbit_potential_values(orbit)
        counts = Counter(values)
        max_zero_count = max(counts.values())
        supports += len(values) - max_zero_count
        degree_options = {
            sum(value - zero_value for value in values)
            for zero_value, count in counts.items()
            if count == max_zero_count
        }
        possible_degrees = {
            old_degree + option
            for old_degree in possible_degrees
            for option in degree_options
        }
    return (
        supports,
        min(possible_degrees),
        max(possible_degrees),
        len(possible_degrees),
        0 in possible_degrees,
    )


def invariant_quotient_blocks(sigma: int) -> tuple[int, ...]:
    rows: list[int] = []
    for q_value in range(QUOTIENT_ORDER):
        block = {
            (q_value + QUOTIENT_ORDER * layer) % RAW_ORDER
            for layer in range(25)
        }
        coords = {(e_value % RIGHT_ORDER, e_value % C_ORDER) for e_value in block}
        image = {multiply_coord(coord, sigma) for coord in coords}
        if image == coords:
            rows.append(q_value)
    return tuple(rows)


def hilbert90_profile() -> Hilbert90PotentialProfile:
    sigma = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    full_orbits = full_p39_orbits(sigma)
    bridge_orbits = p39_orbits()
    min_support, degree_min, degree_max, degree_count, degree_zero = minimal_bridge_degree_data()
    positive = half_potential(1)
    negative = half_potential(-1)
    fixed_repair = fixed_point_degree_repair(positive)
    scalar_repair = quotient_scalar_degree_repair(positive)
    positive_summary = summarize("positive_half_boundary", positive, sigma)
    negative_summary = summarize("negative_half_boundary", negative, sigma)
    fixed_summary = summarize("fixed_point_degree_repair", fixed_repair, sigma)
    scalar_summary = summarize("quotient_scalar_degree_repair", scalar_repair, sigma)
    return Hilbert90PotentialProfile(
        p39_raw=sigma,
        p39_quotient=sigma % QUOTIENT_ORDER,
        full_orbit_count=len(full_orbits),
        full_orbit_size_histogram=tuple(sorted(Counter(map(len, full_orbits)).items())),
        bridge_orbit_count=len(bridge_orbits),
        bridge_orbit_size_histogram=tuple(sorted(Counter(map(len, bridge_orbits)).items())),
        minimal_bridge_potential_support=min_support,
        minimal_bridge_degree_min=degree_min,
        minimal_bridge_degree_max=degree_max,
        minimal_bridge_degree_count=degree_count,
        same_support_degree_zero_possible=degree_zero,
        invariant_quotient_blocks=invariant_quotient_blocks(sigma),
        positive_potential=positive_summary,
        negative_potential=negative_summary,
        fixed_point_degree_repair=fixed_summary,
        quotient_scalar_degree_repair=scalar_summary,
        half_boundary_is_real=positive_summary.boundary_ok and negative_summary.boundary_ok,
        degree_zero_repair_is_not_producer=(
            fixed_summary.boundary_ok
            and scalar_summary.boundary_ok
            and fixed_summary.integer_degree == 0
            and scalar_summary.integer_degree == 0
            and not fixed_summary.ok
            and not scalar_summary.ok
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 potential gate")
    profile = hilbert90_profile()
    expected_positive = PotentialSummary(
        name="positive_half_boundary",
        boundary_ok=True,
        raw_support=75,
        quotient_support=3,
        trace_values=((25, 1), (197, 1), (369, 1)),
        integer_degree=75,
        normalized_quotient_degree=3,
        block_constancy_hits=507,
        kernel_modes=(0,),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=1,
        quotient_pure_c_nonzero=168,
        quotient_mixed_nonzero=336,
        ok=False,
    )
    expected_negative = PotentialSummary(
        name="negative_half_boundary",
        boundary_ok=True,
        raw_support=75,
        quotient_support=3,
        trace_values=((138, -1), (310, -1), (482, -1)),
        integer_degree=-75,
        normalized_quotient_degree=-3,
        block_constancy_hits=507,
        kernel_modes=(0,),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=1,
        quotient_pure_c_nonzero=168,
        quotient_mixed_nonzero=336,
        ok=False,
    )
    expected_fixed = PotentialSummary(
        name="fixed_point_degree_repair",
        boundary_ok=True,
        raw_support=76,
        quotient_support=4,
        trace_values=((0, -3), (25, 1), (197, 1), (369, 1)),
        integer_degree=0,
        normalized_quotient_degree=0,
        block_constancy_hits=506,
        kernel_modes=tuple(range(25)),
        raw_relation_mismatches=2,
        quotient_scalar_nonzero=0,
        quotient_pure_c_nonzero=168,
        quotient_mixed_nonzero=336,
        ok=False,
    )
    expected_scalar = PotentialSummary(
        name="quotient_scalar_degree_repair",
        boundary_ok=True,
        raw_support=100,
        quotient_support=4,
        trace_values=((0, -3), (25, 1), (197, 1), (369, 1)),
        integer_degree=0,
        normalized_quotient_degree=0,
        block_constancy_hits=507,
        kernel_modes=(0,),
        raw_relation_mismatches=0,
        quotient_scalar_nonzero=0,
        quotient_pure_c_nonzero=168,
        quotient_mixed_nonzero=336,
        ok=False,
    )
    row_ok = (
        profile.p39_raw == 2027
        and profile.p39_quotient == 506
        and profile.full_orbit_count == 1268
        and profile.full_orbit_size_histogram == ((1, 1), (2, 253), (4, 507), (20, 507))
        and profile.bridge_orbit_count == 15
        and profile.bridge_orbit_size_histogram == ((2, 3), (4, 6), (20, 6))
        and profile.minimal_bridge_potential_support == 75
        and profile.minimal_bridge_degree_min == -75
        and profile.minimal_bridge_degree_max == 75
        and profile.minimal_bridge_degree_count == 76
        and not profile.same_support_degree_zero_possible
        and profile.invariant_quotient_blocks == (0,)
        and profile.positive_potential == expected_positive
        and profile.negative_potential == expected_negative
        and profile.fixed_point_degree_repair == expected_fixed
        and profile.quotient_scalar_degree_repair == expected_scalar
        and profile.half_boundary_is_real
        and profile.degree_zero_repair_is_not_producer
    )

    print(
        "sigma_profile: "
        f"p39_raw={profile.p39_raw} "
        f"p39_quotient={profile.p39_quotient} "
        f"full_orbits={profile.full_orbit_count} "
        f"full_orbit_size_histogram={profile.full_orbit_size_histogram} "
        f"bridge_orbits={profile.bridge_orbit_count} "
        f"bridge_orbit_size_histogram={profile.bridge_orbit_size_histogram}"
    )
    print(
        "minimal_hilbert90_potential: "
        f"support={profile.minimal_bridge_potential_support} "
        f"degree_min={profile.minimal_bridge_degree_min} "
        f"degree_max={profile.minimal_bridge_degree_max} "
        f"degree_count={profile.minimal_bridge_degree_count} "
        f"degree_zero_possible={int(profile.same_support_degree_zero_possible)}"
    )
    print(f"invariant_quotient_blocks={profile.invariant_quotient_blocks}")
    print(f"positive_potential={profile.positive_potential}")
    print(f"negative_potential={profile.negative_potential}")
    print(f"fixed_point_degree_repair={profile.fixed_point_degree_repair}")
    print(f"quotient_scalar_degree_repair={profile.quotient_scalar_degree_repair}")
    print("interpretation")
    print("  bridge_is_a_sparse_half_frobenius_boundary=1")
    print("  sparse_half_boundaries_have_degree_plus_or_minus_75=1")
    print("  same_support_degree_zero_boundary_is_impossible=1")
    print("  fixed_point_degree_repair_breaks_block_constancy_and_kernel_triviality=1")
    print("  block_constant_degree_repair_is_only_the_q0_scalar_block_and_fails_bridge_trace=1")
    print("  producer_must_supply_the_anti_invariant_line_not_only_a_hilbert90_potential=1")
    print(f"square_axis_bridge_hilbert90_potential_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_potential_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
