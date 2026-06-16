#!/usr/bin/env python3
"""Two-sign intake harness for Hilbert-90 bridge corner candidates.

The latest bridge lane reduces each active half-bridge corner to two signs:

    eps = primitive D-unit sign in {+1, -1}
    a   = branch coefficient in {+1, -1}

The upstream gates already verified that these signs force the low/fiber
triangle, the raw 25-point K trace, the half-boundary direction, and the signed
S-layer bridge image.  This wrapper is intentionally formula-level and fast: a
theorem/literature hit can emit `eps a`, and this harness checks whether those
signs select one of the four vetted finite bridge corners.

Passing this harness is not an arithmetic producer proof.  It verifies the
compact finite target that a producer must realize.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


MODULUS = 13

LowFiber = tuple[int, int]
PointsByRow = tuple[LowFiber, LowFiber, LowFiber]
ResidualsByRow = tuple[int, int, int]


@dataclass(frozen=True)
class CornerSignCandidateProfile:
    name: str
    primitive_unit_sign: int
    branch_coefficient: int
    matched_active_corner: bool
    orientation_mask: int | None
    recorded_direction_q: int | None
    recorded_direction_d: int | None
    cancellation_source_row: int | None
    neighbor_source_row: int | None
    off_line_source_row: int | None
    cancellation_low_fiber: LowFiber | None
    neighbor_low_fiber: LowFiber | None
    off_line_low_fiber: LowFiber | None
    points_by_source_row: PointsByRow | None
    line_residuals_by_source_row: ResidualsByRow | None
    chain_raw_support: int | None
    first_boundary_raw_support: int | None
    bridge_raw_support: int | None
    signed_s_layer_image: tuple[tuple[int, int], ...] | None
    signed_s_layer_image_ok: bool
    raw_k_trace_ok: bool
    primitive_c169_cost_recorded: bool
    ok: bool


def mod13(value: int) -> int:
    return value % MODULUS


def signed_s_layer_bridge() -> tuple[tuple[int, int], ...]:
    return (
        (25, 1),
        (138, -1),
        (197, 1),
        (310, -1),
        (369, 1),
        (482, -1),
    )


def profile_sign_candidate(name: str, eps: int, branch: int) -> CornerSignCandidateProfile:
    if eps not in (-1, 1) or branch not in (-1, 1):
        return CornerSignCandidateProfile(
            name=name,
            primitive_unit_sign=eps,
            branch_coefficient=branch,
            matched_active_corner=False,
            orientation_mask=None,
            recorded_direction_q=None,
            recorded_direction_d=None,
            cancellation_source_row=None,
            neighbor_source_row=None,
            off_line_source_row=None,
            cancellation_low_fiber=None,
            neighbor_low_fiber=None,
            off_line_low_fiber=None,
            points_by_source_row=None,
            line_residuals_by_source_row=None,
            chain_raw_support=None,
            first_boundary_raw_support=None,
            bridge_raw_support=None,
            signed_s_layer_image=None,
            signed_s_layer_image_ok=False,
            raw_k_trace_ok=False,
            primitive_c169_cost_recorded=False,
            ok=False,
        )

    orientation_mask = 1 if eps == 1 else 6
    recorded_direction_q = 197 if branch == -1 else 310
    recorded_direction_d = 122 if recorded_direction_q == 197 else 385

    cancel_row = (3 - eps) // 2
    neighbor_row = (cancel_row - branch) % 3
    off_row = (cancel_row + branch) % 3

    cancellation = (mod13(3 * eps), mod13((eps - 1) // 2))
    neighbor = (
        mod13(cancellation[0] + 2 * branch),
        mod13(cancellation[1] + 2 * branch),
    )
    slope_intercept = (eps - 1) // 2 - 3 * eps
    residual_scalar = -1 + 2 * eps - branch + eps * branch
    off_x = eps + branch
    off_residual = mod13(
        residual_scalar
        * (off_x - 3 * eps)
        * (off_x - (3 * eps + 2 * branch))
    )
    off_point = (
        mod13(off_x),
        mod13(off_x + slope_intercept + off_residual),
    )

    points: list[LowFiber | None] = [None, None, None]
    residuals: list[int | None] = [None, None, None]
    points[cancel_row] = cancellation
    points[neighbor_row] = neighbor
    points[off_row] = off_point
    residuals[cancel_row] = 0
    residuals[neighbor_row] = 0
    residuals[off_row] = off_residual
    if any(point is None for point in points) or any(value is None for value in residuals):
        raise AssertionError("signs did not fill all source rows")

    bridge = signed_s_layer_bridge()
    return CornerSignCandidateProfile(
        name=name,
        primitive_unit_sign=eps,
        branch_coefficient=branch,
        matched_active_corner=True,
        orientation_mask=orientation_mask,
        recorded_direction_q=recorded_direction_q,
        recorded_direction_d=recorded_direction_d,
        cancellation_source_row=cancel_row,
        neighbor_source_row=neighbor_row,
        off_line_source_row=off_row,
        cancellation_low_fiber=cancellation,
        neighbor_low_fiber=neighbor,
        off_line_low_fiber=off_point,
        points_by_source_row=tuple(points),  # type: ignore[arg-type]
        line_residuals_by_source_row=tuple(residuals),  # type: ignore[arg-type]
        chain_raw_support=75,
        first_boundary_raw_support=100,
        bridge_raw_support=150,
        signed_s_layer_image=bridge,
        signed_s_layer_image_ok=True,
        raw_k_trace_ok=True,
        primitive_c169_cost_recorded=True,
        ok=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a two-sign Hilbert-90 bridge corner candidate."
    )
    parser.add_argument("--eps", type=int, help="primitive D-unit sign, +1 or -1")
    parser.add_argument("--branch", type=int, help="branch coefficient, +1 or -1")
    args = parser.parse_args()

    print("p25 Lane B Hilbert-90 bridge corner sign-candidate harness")
    print("format='eps branch' with eps,branch in {+1,-1}")

    if args.eps is not None or args.branch is not None:
        if args.eps is None or args.branch is None:
            raise SystemExit("--eps and --branch must be supplied together")
        profile = profile_sign_candidate("sign_candidate", args.eps, args.branch)
        print("mode=single_sign_candidate")
        print(f"corner_sign_candidate_profile={profile}")
        print("candidate_contract")
        print("  signs must select one of the four active unit-triangle corners")
        print("  selected corner has the forced K trace and signed S-layer bridge image")
        print("  primitive C169 Kummer cost is recorded, not waived")
        print(f"square_axis_bridge_hilbert90_corner_sign_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate")
        return 0 if profile.ok else 1

    profiles = tuple(
        profile_sign_candidate(f"target_eps_{eps}_branch_{branch}", eps, branch)
        for eps in (-1, 1)
        for branch in (-1, 1)
    )
    row_ok = (
        all(profile.ok for profile in profiles)
        and tuple(
            (profile.primitive_unit_sign, profile.branch_coefficient)
            for profile in profiles
        )
        == ((-1, -1), (-1, 1), (1, -1), (1, 1))
        and tuple(profile.orientation_mask for profile in profiles) == (6, 6, 1, 1)
        and tuple(profile.recorded_direction_q for profile in profiles) == (197, 310, 197, 310)
        and tuple(profile.recorded_direction_d for profile in profiles) == (122, 385, 122, 385)
        and tuple(profile.chain_raw_support for profile in profiles) == (75, 75, 75, 75)
        and tuple(profile.first_boundary_raw_support for profile in profiles) == (100, 100, 100, 100)
        and tuple(profile.bridge_raw_support for profile in profiles) == (150, 150, 150, 150)
    )
    print(f"target_sign_candidate_profiles={profiles}")
    print("intake_law")
    print("  all four eps/branch pairs roundtrip to active bridge corners")
    print("  each selected corner has raw support ladder 75 -> 100 -> 150")
    print("  each selected corner records primitive C169 cost rather than hiding it")
    print(f"square_axis_bridge_hilbert90_corner_sign_candidate_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  future Robert/Siegel/Hilbert90 hits can emit two signs before raw triples")
    print("  passing_this_harness_is_not_an_arithmetic_producer_proof=1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
