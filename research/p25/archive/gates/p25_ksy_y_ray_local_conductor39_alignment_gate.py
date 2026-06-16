#!/usr/bin/env python3
"""Finite alignment check between the ray-local theta31 target and U_chi.

The current p25 moonshot has two compact languages:

* the ray-local 151 x 677 theta31 / curved-corner finite payload; and
* the conductor-39 source U_chi=-chi_3*chi_13.

Both are useful, but they are not the same finite object.  This gate compares
them on the common C_3 x C_13 quotient surface and records the exact mismatch:
support, row/column sums, mixed rank, and inner products.  It is a guardrail
against treating conductor-39 source certification as a ray-local payload or a
DANGER3 certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import chi3, legendre13
from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_ray_local_modular_unit_pullback_router_gate import (
    profile_ray_local_modular_unit_pullback_router,
)


RIGHT_DEGREE = 3
C_AXIS = 13


Matrix = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class RayLocalConductor39Alignment:
    ray_local_router_ok: bool
    conductor39_mixed_tensor_ok: bool
    theta31_support: int
    u_chi_support: int
    support_intersection: int
    theta_only_support: int
    u_chi_only_support: int
    theta31_row_sums: tuple[int, ...]
    u_chi_row_sums: tuple[int, ...]
    theta31_column_sums: tuple[int, ...]
    u_chi_column_sums: tuple[int, ...]
    raw_signed_dot: int
    theta31_mixed_scaled_support: int
    u_chi_mixed_support: int
    mixed_signed_dot: int
    theta31_mixed_rank: int
    u_chi_rank: int
    combined_mixed_rank: int
    mixed_proportional_ratios: tuple[str, ...]
    theta_mixed_on_u_chi_zero_support: int
    u_chi_is_theta31_payload: bool
    u_chi_is_value_source_only: bool
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def theta31_matrix() -> Matrix:
    return tuple(
        tuple(template_bits(C_AXIS, c_index)[right] for c_index in range(C_AXIS))
        for right in range(RIGHT_DEGREE)
    )


def u_chi_matrix() -> Matrix:
    return tuple(
        tuple(-chi3(right) * legendre13(c_index) for c_index in range(C_AXIS))
        for right in range(RIGHT_DEGREE)
    )


def support(matrix: Matrix) -> set[tuple[int, int]]:
    return {
        (right, c_index)
        for right, row in enumerate(matrix)
        for c_index, value in enumerate(row)
        if value
    }


def row_sums(matrix: Matrix) -> tuple[int, ...]:
    return tuple(sum(row) for row in matrix)


def column_sums(matrix: Matrix) -> tuple[int, ...]:
    return tuple(sum(matrix[right][c_index] for right in range(RIGHT_DEGREE)) for c_index in range(C_AXIS))


def dot(left: Matrix, right: Matrix) -> int:
    return sum(
        left[row][c_index] * right[row][c_index]
        for row in range(RIGHT_DEGREE)
        for c_index in range(C_AXIS)
    )


def theta_mixed_scaled_by_3(theta: Matrix) -> Matrix:
    col_sums = column_sums(theta)
    return tuple(
        tuple(3 * theta[right][c_index] - col_sums[c_index] for c_index in range(C_AXIS))
        for right in range(RIGHT_DEGREE)
    )


def rank_over_q(matrix: Matrix) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col_index in range(col_count):
        pivot = None
        for row_index in range(rank, row_count):
            if rows[row_index][col_index]:
                pivot = row_index
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][col_index]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row_index in range(row_count):
            if row_index == rank or not rows[row_index][col_index]:
                continue
            factor = rows[row_index][col_index]
            rows[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row_index], rows[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def proportional_ratios_on_u_support(theta_mixed: Matrix, u_chi: Matrix) -> tuple[str, ...]:
    ratios = {
        Fraction(theta_mixed[right][c_index], u_chi[right][c_index])
        for right in range(RIGHT_DEGREE)
        for c_index in range(C_AXIS)
        if u_chi[right][c_index]
    }
    return tuple(str(ratio) for ratio in sorted(ratios))


def profile_ray_local_conductor39_alignment() -> RayLocalConductor39Alignment:
    ray = profile_ray_local_modular_unit_pullback_router()
    conductor = profile_yang_y507_conductor39_mixed_tensor_character()
    theta = theta31_matrix()
    u_chi = u_chi_matrix()
    theta_supp = support(theta)
    u_supp = support(u_chi)
    intersection = theta_supp & u_supp
    theta_mixed = theta_mixed_scaled_by_3(theta)
    theta_mixed_supp = support(theta_mixed)
    u_mixed_supp = support(u_chi)
    theta_on_u_zero = sum(
        1
        for right in range(RIGHT_DEGREE)
        for c_index in range(C_AXIS)
        if u_chi[right][c_index] == 0 and theta_mixed[right][c_index] != 0
    )
    combined_rank = rank_over_q(theta_mixed + u_chi)
    ratios = proportional_ratios_on_u_support(theta_mixed, u_chi)
    u_is_theta = False
    row_ok = (
        ray.row_ok
        and conductor.row_ok
        and len(theta_supp) == 18
        and len(u_supp) == 24
        and len(intersection) == 12
        and len(theta_supp - u_supp) == 6
        and len(u_supp - theta_supp) == 12
        and row_sums(theta) == (6, 6, 6)
        and row_sums(u_chi) == (0, 0, 0)
        and column_sums(theta) == (0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3)
        and column_sums(u_chi) == (0,) * C_AXIS
        and dot(theta, u_chi) == 0
        and len(theta_mixed_supp) == 18
        and len(u_mixed_supp) == 24
        and dot(theta_mixed, u_chi) == 0
        and rank_over_q(theta_mixed) == 2
        and rank_over_q(u_chi) == 1
        and combined_rank == 3
        and ratios == ("-2", "-1", "0", "1", "2")
        and theta_on_u_zero == 6
        and not u_is_theta
    )
    return RayLocalConductor39Alignment(
        ray_local_router_ok=ray.row_ok,
        conductor39_mixed_tensor_ok=conductor.row_ok,
        theta31_support=len(theta_supp),
        u_chi_support=len(u_supp),
        support_intersection=len(intersection),
        theta_only_support=len(theta_supp - u_supp),
        u_chi_only_support=len(u_supp - theta_supp),
        theta31_row_sums=row_sums(theta),
        u_chi_row_sums=row_sums(u_chi),
        theta31_column_sums=column_sums(theta),
        u_chi_column_sums=column_sums(u_chi),
        raw_signed_dot=dot(theta, u_chi),
        theta31_mixed_scaled_support=len(theta_mixed_supp),
        u_chi_mixed_support=len(u_mixed_supp),
        mixed_signed_dot=dot(theta_mixed, u_chi),
        theta31_mixed_rank=rank_over_q(theta_mixed),
        u_chi_rank=rank_over_q(u_chi),
        combined_mixed_rank=combined_rank,
        mixed_proportional_ratios=ratios,
        theta_mixed_on_u_chi_zero_support=theta_on_u_zero,
        u_chi_is_theta31_payload=u_is_theta,
        u_chi_is_value_source_only=True,
        first_missing_clause=(
            "a theorem must bridge or evaluate U_chi/H0/Y_507; U_chi is not "
            "the ray-local theta31 or curved-corner finite payload"
        ),
        recommendation=(
            "accept conductor-39 theorems as source/value routes; reject any "
            "claim that merely renames U_chi as the 151 x 677 theta31 payload "
            "without an explicit bridge/value theorem"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_ray_local_conductor39_alignment()
    print("p25 KSY-y ray-local / conductor-39 alignment gate")
    print("dependencies")
    print(f"  ray_local_router_ok={int(profile.ray_local_router_ok)}")
    print(f"  conductor39_mixed_tensor_ok={int(profile.conductor39_mixed_tensor_ok)}")
    print("support")
    print(f"  theta31_support={profile.theta31_support}")
    print(f"  u_chi_support={profile.u_chi_support}")
    print(f"  support_intersection={profile.support_intersection}")
    print(f"  theta_only_support={profile.theta_only_support}")
    print(f"  u_chi_only_support={profile.u_chi_only_support}")
    print("raw_shape")
    print(f"  theta31_row_sums={profile.theta31_row_sums}")
    print(f"  u_chi_row_sums={profile.u_chi_row_sums}")
    print(f"  theta31_column_sums={profile.theta31_column_sums}")
    print(f"  u_chi_column_sums={profile.u_chi_column_sums}")
    print(f"  raw_signed_dot={profile.raw_signed_dot}")
    print("mixed_projection")
    print(f"  theta31_mixed_scaled_support={profile.theta31_mixed_scaled_support}")
    print(f"  u_chi_mixed_support={profile.u_chi_mixed_support}")
    print(f"  mixed_signed_dot={profile.mixed_signed_dot}")
    print(f"  theta31_mixed_rank={profile.theta31_mixed_rank}")
    print(f"  u_chi_rank={profile.u_chi_rank}")
    print(f"  combined_mixed_rank={profile.combined_mixed_rank}")
    print(f"  mixed_proportional_ratios={profile.mixed_proportional_ratios}")
    print(f"  theta_mixed_on_u_chi_zero_support={profile.theta_mixed_on_u_chi_zero_support}")
    print("verdict")
    print(f"  u_chi_is_theta31_payload={int(profile.u_chi_is_theta31_payload)}")
    print(f"  u_chi_is_value_source_only={int(profile.u_chi_is_value_source_only)}")
    print(f"  first_missing_clause={profile.first_missing_clause}")
    print("interpretation")
    print("  conductor39_source_certification_is_not_ray_local_payload_certification=1")
    print("  u_chi_value_theorem_would_be_source_progress_not_a_raw_theta31_hit=1")
    print("  require_explicit_bridge_value_theorem_before_downstream_DANGER3_work=1")
    print(f"ksy_y_ray_local_conductor39_alignment_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("ray-local / conductor-39 alignment regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
