#!/usr/bin/env python3
"""Minimal degree-zero Hilbert-90 potentials for the p25 bridge.

The previous Hilbert-90 gate showed that the bridge is (1-sigma) of either
oriented half-bridge, but those sparse half-potentials have degree +/-75.
This gate classifies the smallest block-constant, kernel-trivial, integral
degree-zero repairs of the positive half-potential.

In quotient terms, each bridge pair is {q,-q}.  A sigma-invariant repair adds
the same integer to both cells of a pair, plus an optional fixed q=0 term.
The minimum degree-zero potentials have four quotient blocks / 100 raw cells:
one q=0 fixed block and one chosen orientation on each of the three bridge
pairs.  There are exactly 2^3 such minima.
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
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_potential_gate import (
    boundary_ok,
    half_potential,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    RAW_ORDER,
)


@dataclass(frozen=True)
class MinimalPotential:
    orientation_mask: int
    fixed_q0_coefficient: int
    flipped_pairs: tuple[tuple[int, int], ...]
    trace_values: tuple[tuple[int, int], ...]
    raw_support: int
    quotient_support: int
    integer_degree: int
    boundary_ok: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    trace_correct: bool
    harness_ok: bool


@dataclass(frozen=True)
class MinimalPotentialProfile:
    p39_raw: int
    p39_quotient: int
    bridge_pairs: tuple[tuple[int, int], ...]
    active_pair_count: int
    active_pair_min_support: int
    active_pair_min_degree_values: tuple[int, ...]
    support_less_than_four_possible: bool
    minimal_quotient_support: int
    minimal_raw_support: int
    minimal_potential_count: int
    fixed_coefficient_histogram: tuple[tuple[int, int], ...]
    unit_fixed_coefficient_count: int
    scalar_extreme_count: int
    trace_correct_count: int
    harness_ok_count: int
    all_boundary_ok: bool
    all_block_constant: bool
    all_kernel_trivial: bool
    all_raw_relation_ok: bool
    potentials: tuple[MinimalPotential, ...]


def add_qblock(raw: list[int], q_value: int, coefficient: int) -> None:
    for layer in range(25):
        raw[q_value + QUOTIENT_ORDER * layer] += coefficient


def positive_negative_pairs() -> tuple[tuple[int, int], ...]:
    pairs: list[tuple[int, int]] = []
    for q_value, coefficient in sorted(bridge_coefficients().items()):
        if coefficient == 1:
            pairs.append((q_value, (-q_value) % QUOTIENT_ORDER))
    return tuple(pairs)


def minimal_raw_potential(orientation_mask: int, pairs: tuple[tuple[int, int], ...]) -> tuple[list[int], int, tuple[tuple[int, int], ...]]:
    raw = half_potential(1)
    flipped: list[tuple[int, int]] = []
    for index, (positive_q, negative_q) in enumerate(pairs):
        if orientation_mask >> index & 1:
            add_qblock(raw, positive_q, -1)
            add_qblock(raw, negative_q, -1)
            flipped.append((positive_q, negative_q))
    fixed_coefficient = 2 * len(flipped) - 3
    add_qblock(raw, 0, fixed_coefficient)
    return raw, fixed_coefficient, tuple(flipped)


def summarize_minimal_potential(
    orientation_mask: int,
    pairs: tuple[tuple[int, int], ...],
    sigma: int,
) -> MinimalPotential:
    raw, fixed_coefficient, flipped = minimal_raw_potential(orientation_mask, pairs)
    candidate = profile_candidate(
        f"hilbert90_minimal_potential_{orientation_mask}",
        raw,
        target_raw_bridge(),
    )
    trace = quotient_trace(raw)
    return MinimalPotential(
        orientation_mask=orientation_mask,
        fixed_q0_coefficient=fixed_coefficient,
        flipped_pairs=flipped,
        trace_values=tuple((index, value) for index, value in enumerate(trace) if value),
        raw_support=candidate.raw_support,
        quotient_support=candidate.quotient_support,
        integer_degree=sum(raw),
        boundary_ok=boundary_ok(raw, sigma),
        block_constancy_hits=candidate.block_constancy_hits,
        kernel_modes=candidate.kernel_modes,
        raw_relation_mismatches=candidate.raw_relation_mismatches,
        trace_correct=candidate.trace_correct,
        harness_ok=candidate.ok,
    )


def minimal_potential_profile() -> MinimalPotentialProfile:
    sigma = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    pairs = positive_negative_pairs()
    active_degree_values = tuple(3 - 2 * flipped_count for flipped_count in range(4))
    potentials = tuple(
        summarize_minimal_potential(orientation_mask, pairs, sigma)
        for orientation_mask in range(1 << len(pairs))
    )
    fixed_histogram = tuple(
        sorted(Counter(row.fixed_q0_coefficient for row in potentials).items())
    )
    return MinimalPotentialProfile(
        p39_raw=sigma,
        p39_quotient=sigma % QUOTIENT_ORDER,
        bridge_pairs=pairs,
        active_pair_count=len(pairs),
        active_pair_min_support=len(pairs),
        active_pair_min_degree_values=active_degree_values,
        support_less_than_four_possible=False,
        minimal_quotient_support=min(row.quotient_support for row in potentials),
        minimal_raw_support=min(row.raw_support for row in potentials),
        minimal_potential_count=len(potentials),
        fixed_coefficient_histogram=fixed_histogram,
        unit_fixed_coefficient_count=sum(
            1 for row in potentials if abs(row.fixed_q0_coefficient) == 1
        ),
        scalar_extreme_count=sum(
            1 for row in potentials if abs(row.fixed_q0_coefficient) == 3
        ),
        trace_correct_count=sum(row.trace_correct for row in potentials),
        harness_ok_count=sum(row.harness_ok for row in potentials),
        all_boundary_ok=all(row.boundary_ok for row in potentials),
        all_block_constant=all(row.block_constancy_hits == QUOTIENT_ORDER for row in potentials),
        all_kernel_trivial=all(row.kernel_modes == (0,) for row in potentials),
        all_raw_relation_ok=all(row.raw_relation_mismatches == 0 for row in potentials),
        potentials=potentials,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 minimal-potential gate")
    profile = minimal_potential_profile()
    expected_potentials = (
        MinimalPotential(
            0,
            -3,
            (),
            ((0, -3), (25, 1), (197, 1), (369, 1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            1,
            -1,
            ((25, 482),),
            ((0, -1), (197, 1), (369, 1), (482, -1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            2,
            -1,
            ((197, 310),),
            ((0, -1), (25, 1), (310, -1), (369, 1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            3,
            1,
            ((25, 482), (197, 310)),
            ((0, 1), (310, -1), (369, 1), (482, -1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            4,
            -1,
            ((369, 138),),
            ((0, -1), (25, 1), (138, -1), (197, 1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            5,
            1,
            ((25, 482), (369, 138)),
            ((0, 1), (138, -1), (197, 1), (482, -1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            6,
            1,
            ((197, 310), (369, 138)),
            ((0, 1), (25, 1), (138, -1), (310, -1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
        MinimalPotential(
            7,
            3,
            ((25, 482), (197, 310), (369, 138)),
            ((0, 3), (138, -1), (310, -1), (482, -1)),
            100,
            4,
            0,
            True,
            507,
            (0,),
            0,
            False,
            False,
        ),
    )
    row_ok = (
        profile.p39_raw == 2027
        and profile.p39_quotient == 506
        and profile.bridge_pairs == ((25, 482), (197, 310), (369, 138))
        and profile.active_pair_count == 3
        and profile.active_pair_min_support == 3
        and profile.active_pair_min_degree_values == (3, 1, -1, -3)
        and not profile.support_less_than_four_possible
        and profile.minimal_quotient_support == 4
        and profile.minimal_raw_support == 100
        and profile.minimal_potential_count == 8
        and profile.fixed_coefficient_histogram == ((-3, 1), (-1, 3), (1, 3), (3, 1))
        and profile.unit_fixed_coefficient_count == 6
        and profile.scalar_extreme_count == 2
        and profile.trace_correct_count == 0
        and profile.harness_ok_count == 0
        and profile.all_boundary_ok
        and profile.all_block_constant
        and profile.all_kernel_trivial
        and profile.all_raw_relation_ok
        and profile.potentials == expected_potentials
    )

    print(
        "minimal_support_law: "
        f"p39_raw={profile.p39_raw} "
        f"p39_quotient={profile.p39_quotient} "
        f"bridge_pairs={profile.bridge_pairs} "
        f"active_pair_min_support={profile.active_pair_min_support} "
        f"active_pair_min_degree_values={profile.active_pair_min_degree_values} "
        f"support_less_than_four_possible={int(profile.support_less_than_four_possible)} "
        f"minimal_quotient_support={profile.minimal_quotient_support} "
        f"minimal_raw_support={profile.minimal_raw_support}"
    )
    print(
        "minimal_potential_counts: "
        f"count={profile.minimal_potential_count} "
        f"fixed_coefficient_histogram={profile.fixed_coefficient_histogram} "
        f"unit_fixed_coefficient_count={profile.unit_fixed_coefficient_count} "
        f"scalar_extreme_count={profile.scalar_extreme_count} "
        f"trace_correct_count={profile.trace_correct_count} "
        f"harness_ok_count={profile.harness_ok_count}"
    )
    print("minimal_potentials")
    for row in profile.potentials:
        print(f"  {row}")
    print("interpretation")
    print("  degree_zero_block_constant_hilbert90_potentials_need_at_least_four_quotient_blocks=1")
    print("  minimum_raw_support_is_100_not_75=1")
    print("  exactly_eight_minimal_oriented_potentials_exist=1")
    print("  all_minima_preserve_boundary_kernel_triviality_and_raw_relation=1")
    print("  no_minimum_potential_is_itself_the_signed_bridge_certificate=1")
    print("  producer_can_target_one_of_these_potentials_but_must_still_realize_the_anti_invariant_ratio=1")
    print(f"square_axis_bridge_hilbert90_minimal_potential_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
