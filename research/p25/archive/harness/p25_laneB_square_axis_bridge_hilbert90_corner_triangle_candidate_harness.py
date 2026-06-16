#!/usr/bin/env python3
"""Row-labeled triangle intake for Hilbert-90 bridge corner candidates.

The sign intake is the smallest current bridge interface, but a theorem hit may
more naturally emit the primitive C_169 corner triangle itself.  This harness
accepts three row-labeled low/fiber points in C_3 x C_13 x C_13, matches them
against the four active two-sign corners, and then reuses the sign-to-sparse
source promotion.

Passing this harness is still only a finite intake check.  It verifies that a
proposed triangle is the exact nonsplit C_169 corner already connected to the
Robert sparse-source bridge contract.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Optional

from p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness import (
    sign_sparse_source_profile,
)


LowFiber = tuple[int, int]
PointsByRow = tuple[LowFiber, LowFiber, LowFiber]
InputCoefficients = tuple[Optional[int], Optional[int], Optional[int]]


ACTIVE_SIGNS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)


@dataclass(frozen=True)
class CornerTriangleCandidateProfile:
    name: str
    input_points_by_source_row: PointsByRow | None
    input_coefficients_by_source_row: InputCoefficients | None
    matched_active_corner_count: int
    matched_primitive_unit_sign: int | None
    matched_branch_coefficient: int | None
    matched_recorded_direction_q: int | None
    quotient_support_ladder: tuple[int, int, int] | None
    raw_sparse_support: int | None
    sparse_entries_equal_target: bool
    sparse_source_bridge_ok: bool
    ok: bool


def active_sparse_profiles():
    return tuple(
        sign_sparse_source_profile(f"active_eps_{eps}_branch_{branch}", eps, branch)
        for eps, branch in ACTIVE_SIGNS
    )


def parse_point_args(point_args: list[list[str]] | None) -> tuple[PointsByRow | None, InputCoefficients | None]:
    if point_args is None:
        return None, None

    points: list[LowFiber | None] = [None, None, None]
    coefficients: list[int | None] = [None, None, None]
    for tokens in point_args:
        if len(tokens) not in (3, 4):
            raise ValueError("--point must be ROW LOW FIBER or ROW LOW FIBER COEFF")
        row, low, fiber = (int(tokens[0]), int(tokens[1]), int(tokens[2]))
        if row not in (0, 1, 2):
            raise ValueError(f"source row out of range: {row}")
        if not (0 <= low < 13 and 0 <= fiber < 13):
            raise ValueError(f"low/fiber out of C13 range: {(low, fiber)}")
        if points[row] is not None:
            raise ValueError(f"duplicate source row: {row}")
        coefficient = int(tokens[3]) if len(tokens) == 4 else None
        if coefficient is not None and coefficient not in (-1, 1):
            raise ValueError(f"coefficient must be +1 or -1: {coefficient}")
        points[row] = (low, fiber)
        coefficients[row] = coefficient

    if any(point is None for point in points):
        raise ValueError("exactly one point for each source row 0,1,2 is required")
    return (
        tuple(points),  # type: ignore[arg-type]
        tuple(coefficients),  # type: ignore[arg-type]
    )


def triangle_candidate_profile(
    name: str,
    points_by_source_row: PointsByRow | None,
    coefficients_by_source_row: InputCoefficients | None,
) -> CornerTriangleCandidateProfile:
    if points_by_source_row is None or coefficients_by_source_row is None:
        return CornerTriangleCandidateProfile(
            name=name,
            input_points_by_source_row=None,
            input_coefficients_by_source_row=None,
            matched_active_corner_count=0,
            matched_primitive_unit_sign=None,
            matched_branch_coefficient=None,
            matched_recorded_direction_q=None,
            quotient_support_ladder=None,
            raw_sparse_support=None,
            sparse_entries_equal_target=False,
            sparse_source_bridge_ok=False,
            ok=False,
        )

    matches = []
    for sparse_profile in active_sparse_profiles():
        sign_profile = sparse_profile.sign_profile
        if sign_profile.points_by_source_row != points_by_source_row:
            continue
        branch = sign_profile.branch_coefficient
        if any(
            coefficient is not None and coefficient != branch
            for coefficient in coefficients_by_source_row
        ):
            continue
        matches.append(sparse_profile)

    if len(matches) != 1:
        return CornerTriangleCandidateProfile(
            name=name,
            input_points_by_source_row=points_by_source_row,
            input_coefficients_by_source_row=coefficients_by_source_row,
            matched_active_corner_count=len(matches),
            matched_primitive_unit_sign=None,
            matched_branch_coefficient=None,
            matched_recorded_direction_q=None,
            quotient_support_ladder=None,
            raw_sparse_support=None,
            sparse_entries_equal_target=False,
            sparse_source_bridge_ok=False,
            ok=False,
        )

    matched = matches[0]
    sparse_source_ok = (
        matched.sparse_source_profile is not None
        and matched.sparse_source_profile.ok
    )
    ladder = (
        len(matched.chain_q_items),
        len(matched.first_boundary_q_items),
        len(matched.bridge_q_items),
    )
    ok = (
        matched.ok
        and ladder == (3, 4, 6)
        and matched.sparse_entry_count == 150
        and matched.sparse_entries_equal_target
        and sparse_source_ok
    )
    return CornerTriangleCandidateProfile(
        name=name,
        input_points_by_source_row=points_by_source_row,
        input_coefficients_by_source_row=coefficients_by_source_row,
        matched_active_corner_count=1,
        matched_primitive_unit_sign=matched.sign_profile.primitive_unit_sign,
        matched_branch_coefficient=matched.sign_profile.branch_coefficient,
        matched_recorded_direction_q=matched.sign_profile.recorded_direction_q,
        quotient_support_ladder=ladder,
        raw_sparse_support=matched.sparse_entry_count,
        sparse_entries_equal_target=matched.sparse_entries_equal_target,
        sparse_source_bridge_ok=sparse_source_ok,
        ok=ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a row-labeled Hilbert-90 corner triangle candidate."
    )
    parser.add_argument(
        "--point",
        action="append",
        nargs="+",
        metavar="VALUE",
        help="source-row point; repeat three times. COEFF is optional and must be +/-1.",
    )
    args = parser.parse_args()

    print("p25 Lane B Hilbert-90 bridge corner triangle-candidate harness")
    print("format='--point ROW LOW FIBER [COEFF]' repeated for rows 0,1,2")

    if args.point is not None:
        points, coefficients = parse_point_args(args.point)
        profile = triangle_candidate_profile("triangle_candidate", points, coefficients)
        print("mode=single_triangle_candidate")
        print(f"corner_triangle_candidate_profile={profile}")
        print("candidate_contract")
        print("  triangle must be one of the four active row-labeled C169 corners")
        print("  optional coefficients must agree with the matched branch sign")
        print("  matched triangle must promote through sign-to-sparse-source bridge")
        print(f"square_axis_bridge_hilbert90_corner_triangle_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate")
        return 0 if profile.ok else 1

    profiles = []
    for sparse_profile in active_sparse_profiles():
        sign_profile = sparse_profile.sign_profile
        if sign_profile.points_by_source_row is None:
            raise AssertionError("active sign profile has no source triangle")
        branch = sign_profile.branch_coefficient
        coefficients = (branch, branch, branch)
        profiles.append(
            triangle_candidate_profile(
                f"target_eps_{sign_profile.primitive_unit_sign}_branch_{branch}",
                sign_profile.points_by_source_row,
                coefficients,
            )
        )
    profiles_tuple = tuple(profiles)
    row_ok = (
        all(profile.ok for profile in profiles_tuple)
        and tuple(
            (profile.matched_primitive_unit_sign, profile.matched_branch_coefficient)
            for profile in profiles_tuple
        )
        == ACTIVE_SIGNS
        and tuple(profile.quotient_support_ladder for profile in profiles_tuple)
        == ((3, 4, 6), (3, 4, 6), (3, 4, 6), (3, 4, 6))
        and tuple(profile.raw_sparse_support for profile in profiles_tuple)
        == (150, 150, 150, 150)
    )

    print("target_triangle_profiles")
    for profile in profiles_tuple:
        print(f"  {profile}")
    print("intake_law")
    print("  all four active row-labeled triangles match unique eps/branch signs")
    print("  each triangle promotes to the exact sparse-source bridge contract")
    print("  coefficients may be omitted, but if supplied they must match the branch")
    print(f"square_axis_bridge_hilbert90_corner_triangle_candidate_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  theorem hits may emit a three-point primitive C169 triangle before signs")
    print("  primitive C169 producer debt remains; this is an intake check only")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
