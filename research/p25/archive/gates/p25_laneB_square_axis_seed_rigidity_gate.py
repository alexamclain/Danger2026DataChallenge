#!/usr/bin/env python3
"""Rigidity of the p25 square-axis no-borrow seed.

The previous gate shows that the 18-point square-axis residual has only the
known S-orbit times 6-term seed product structure.  This gate looks one layer
inside that seed in C_507.

The seed has no hidden affine symmetry, is not a 6-term arithmetic progression,
and has no collision-free 2x3 or 3x2 sumset factorization.  The one compact
geometry it does retain is exactly the known no-borrow one: three 3x3
AP-rectangle completions, each with eight oriented presentations.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from math import gcd

from p25_laneB_square_axis_group_ring_normal_form_gate import seed_terms
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Completion = tuple[int, int, int, tuple[int, ...], tuple[int, ...]]


def seed_set() -> set[int]:
    return set(seed_terms())


def units_mod_q() -> list[int]:
    return [value for value in range(QUOTIENT_ORDER) if gcd(value, QUOTIENT_ORDER) == 1]


def affine_stabilizers() -> list[tuple[int, int]]:
    seed = seed_set()
    stabilizers: list[tuple[int, int]] = []
    for multiplier in units_mod_q():
        for shift in range(QUOTIENT_ORDER):
            image = {
                (multiplier * value + shift) % QUOTIENT_ORDER
                for value in seed
            }
            if image == seed:
                stabilizers.append((multiplier, shift))
    return stabilizers


def arithmetic_progression_presentations() -> list[tuple[int, int]]:
    seed = seed_set()
    presentations: list[tuple[int, int]] = []
    for start in range(QUOTIENT_ORDER):
        for step in range(QUOTIENT_ORDER):
            progression = {
                (start + index * step) % QUOTIENT_ORDER
                for index in range(len(seed))
            }
            if len(progression) == len(seed) and progression == seed:
                presentations.append((start, step))
    return presentations


def normalized_sumset_tilings(
    left_size: int, right_size: int
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    seed = seed_set()
    differences = sorted(
        {
            (left - right) % QUOTIENT_ORDER
            for left in seed
            for right in seed
            if left != right
        }
    )
    tilings: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for rest in combinations(differences, left_size - 1):
        left = (0, *rest)
        right_candidates = set(range(QUOTIENT_ORDER))
        for left_term in left:
            right_candidates &= {
                (point - left_term) % QUOTIENT_ORDER
                for point in seed
            }
        if len(right_candidates) < right_size:
            continue
        for right in combinations(sorted(right_candidates), right_size):
            product = {
                (left_term + right_term) % QUOTIENT_ORDER
                for left_term in left
                for right_term in right
            }
            if len(product) == left_size * right_size == len(seed) and product == seed:
                tilings.append((tuple(sorted(left)), tuple(sorted(right))))
    return tilings


def ap_rectangle_completions() -> list[Completion]:
    seed = seed_set()
    completions: set[Completion] = set()
    for first_step in range(QUOTIENT_ORDER):
        for second_step in range(QUOTIENT_ORDER):
            shape = {
                (row * first_step + column * second_step) % QUOTIENT_ORDER
                for row in range(3)
                for column in range(3)
            }
            if len(shape) != 9:
                continue
            bases = {
                (seed_point - shape_point) % QUOTIENT_ORDER
                for seed_point in seed
                for shape_point in shape
            }
            for base in bases:
                rectangle = tuple(
                    sorted((base + shape_point) % QUOTIENT_ORDER for shape_point in shape)
                )
                rectangle_set = set(rectangle)
                if seed <= rectangle_set:
                    borrow = tuple(sorted(rectangle_set - seed))
                    completions.add((base, first_step, second_step, rectangle, borrow))
    return sorted(completions)


def grouped_completions(
    completions: list[Completion],
) -> dict[tuple[tuple[int, ...], tuple[int, ...]], int]:
    grouped: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = defaultdict(int)
    for _base, _first_step, _second_step, rectangle, borrow in completions:
        grouped[(rectangle, borrow)] += 1
    return dict(sorted(grouped.items()))


def expected_completion_groups() -> dict[tuple[tuple[int, ...], tuple[int, ...]], int]:
    rows = {
        (
            (25, 34, 43, 77, 86, 95, 129, 138, 147),
            (25, 34, 77),
        ): 8,
        (
            (43, 52, 61, 86, 95, 104, 129, 138, 147),
            (52, 61, 104),
        ): 8,
        (
            (43, 86, 95, 129, 138, 147, 181, 190, 233),
            (181, 190, 233),
        ): 8,
    }
    return dict(sorted(rows.items()))


def main() -> int:
    print("p25 Lane B square-axis seed-rigidity gate")
    print(f"quotient_order={QUOTIENT_ORDER}")
    seed = tuple(seed_terms())
    stabilizers = affine_stabilizers()
    ap_presentations = arithmetic_progression_presentations()
    two_by_three = normalized_sumset_tilings(2, 3)
    three_by_two = normalized_sumset_tilings(3, 2)
    completions = ap_rectangle_completions()
    completion_groups = grouped_completions(completions)
    expected_groups = expected_completion_groups()

    affine_ok = stabilizers == [(1, 0)]
    ap_ok = ap_presentations == []
    factorization_ok = two_by_three == [] and three_by_two == []
    rectangle_ok = completion_groups == expected_groups and len(completions) == 24
    row_ok = bool(affine_ok and ap_ok and factorization_ok and rectangle_ok)

    print(
        "seed_rigidity: "
        f"seed={list(seed)} "
        f"affine_stabilizers={len(stabilizers)} "
        f"ap_presentations={len(ap_presentations)} "
        f"two_by_three={len(two_by_three)} "
        f"three_by_two={len(three_by_two)} "
        f"ap_rectangle_oriented_presentations={len(completions)} "
        f"ap_rectangle_groups={len(completion_groups)} "
        f"ok={int(row_ok)}"
    )
    print(f"affine_stabilizers_detail={stabilizers}")
    print("ap_rectangle_completion_groups")
    for (rectangle, borrow), count in completion_groups.items():
        print(
            f"  count={count} "
            f"rectangle={list(rectangle)} "
            f"borrow={list(borrow)}"
        )
    print("expected_ap_rectangle_completion_groups")
    for (rectangle, borrow), count in expected_groups.items():
        print(
            f"  count={count} "
            f"rectangle={list(rectangle)} "
            f"borrow={list(borrow)}"
        )
    print(f"square_axis_seed_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  seed_has_trivial_affine_stabilizer=1")
    print("  seed_is_not_a_6_term_arithmetic_progression=1")
    print("  seed_has_no_collision_free_2x3_or_3x2_sumset_factorization=1")
    print("  seed_rectangle_completions_are_exactly_the_known_no_borrow_frames=1")
    print("  producer_must_explain_the_lower_triangular_no_borrow_seed_itself=1")
    print("conclusion=reported_p25_laneB_square_axis_seed_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
