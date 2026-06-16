#!/usr/bin/env python3
"""Kummer-cost ledger for p25 Hilbert-90 source-chain corners.

The previous corner raw K-trace gate showed that the active half-bridge corner
must be lifted by the 25-point right-kernel trace.  This gate ties that selector
to the local source/Kummer accounting: the K factor is cheap and right-only, but
every sparse corner direction still has primitive C_169 motion in all kernel
gauges.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factor_kummer_gate import (
    FactorOrderProfile,
    factor_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate import (
    profile as corner_raw_k_trace_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_raw_kummer_gate import (
    KernelGaugeDirectionProfile,
    direction_profile,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import KERNEL_SHIFT
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


EXPECTED_SPARSE_DIRECTIONS = (25, 172, 197, 310, 335, 482)


@dataclass(frozen=True)
class CornerKummerCostRow:
    orientation_mask: int
    boundary_direction_q: int
    chain_q_values: tuple[int, ...]
    coefficient: int
    block_raw_support: int
    block_raw_degree: int
    pair_directions: tuple[int, ...]
    all_pair_directions_primitive_c169: bool
    right_order_three_available: bool
    min_combined_orders: tuple[int, ...]


@dataclass(frozen=True)
class CornerKummerCostProfile:
    active_corner_count: int
    pair_direction_union: tuple[int, ...]
    boundary_direction_values: tuple[int, ...]
    kernel_trace_factor: FactorOrderProfile
    sparse_direction_rows: tuple[KernelGaugeDirectionProfile, ...]
    corner_rows: tuple[CornerKummerCostRow, ...]
    block_k_trace_selector_passes: bool
    sparse_sections_are_invalid_producers: bool
    kernel_trace_is_right_only: bool
    all_sparse_directions_have_primitive_c169_cost: bool
    all_sparse_directions_have_right_order_three_gauge: bool
    all_sparse_directions_have_min_combined_order_507: bool
    all_active_corner_rows_use_the_same_six_sparse_directions: bool


def pair_directions(q_values: tuple[int, ...]) -> tuple[int, ...]:
    directions = {
        (right - left) % QUOTIENT_ORDER
        for left in q_values
        for right in q_values
        if left != right
    }
    return tuple(sorted(directions))


def corner_kummer_cost_profile() -> CornerKummerCostProfile:
    corners = corner_profile()
    raw_k_trace = corner_raw_k_trace_profile()
    block_by_key = {
        (row.orientation_mask, row.boundary_direction_q, row.chain_q_values): row
        for row in raw_k_trace.block_k_trace_rows
    }
    sparse_rows = tuple(direction_profile(direction) for direction in EXPECTED_SPARSE_DIRECTIONS)
    sparse_by_direction = {row.direction_q: row for row in sparse_rows}

    cost_rows: list[CornerKummerCostRow] = []
    pair_union: set[int] = set()
    for active in corners.active_rows:
        key = (active.orientation_mask, active.boundary_direction_q, active.chain_q_values)
        block = block_by_key[key]
        directions = pair_directions(active.chain_q_values)
        pair_union.update(directions)
        direction_rows = tuple(sparse_by_direction[direction] for direction in directions)
        cost_rows.append(
            CornerKummerCostRow(
                orientation_mask=active.orientation_mask,
                boundary_direction_q=active.boundary_direction_q,
                chain_q_values=active.chain_q_values,
                coefficient=block.coefficient,
                block_raw_support=block.raw_support,
                block_raw_degree=block.raw_degree,
                pair_directions=directions,
                all_pair_directions_primitive_c169=all(
                    row.c_order_values == (169,)
                    and row.c_c169_min_degrees == (169,)
                    and row.c_c13_min_degrees == (13,)
                    for row in direction_rows
                ),
                right_order_three_available=all(
                    row.right_order_histogram == ((3, 1), (15, 4), (75, 20))
                    for row in direction_rows
                ),
                min_combined_orders=tuple(row.combined_order_min for row in direction_rows),
            )
        )

    kernel_factor = factor_profile("kernel_trace", KERNEL_SHIFT)
    return CornerKummerCostProfile(
        active_corner_count=len(corners.active_rows),
        pair_direction_union=tuple(sorted(pair_union)),
        boundary_direction_values=tuple(sorted({row.boundary_direction_q for row in corners.active_rows})),
        kernel_trace_factor=kernel_factor,
        sparse_direction_rows=sparse_rows,
        corner_rows=tuple(cost_rows),
        block_k_trace_selector_passes=raw_k_trace.all_block_k_trace_rows_pass,
        sparse_sections_are_invalid_producers=(
            raw_k_trace.all_sparse_sections_are_trace_correct_but_relation_bad
            and raw_k_trace.all_block_plus_hidden_rows_are_trace_correct_but_relation_bad
            and raw_k_trace.all_hidden_only_rows_are_degree_zero_but_trace_bad
        ),
        kernel_trace_is_right_only=(
            kernel_factor.shift == (57, 0)
            and kernel_factor.right_order == 25
            and kernel_factor.c_order == 1
            and kernel_factor.combined_order == 25
            and kernel_factor.right_c75_min_degree == 25
            and kernel_factor.right_c3_min_degree == 1
            and kernel_factor.c_c169_min_degree == 1
            and kernel_factor.c_c13_min_degree == 1
        ),
        all_sparse_directions_have_primitive_c169_cost=all(
            row.c_order_values == (169,)
            and row.c_c169_min_degrees == (169,)
            and row.c_c13_min_degrees == (13,)
            for row in sparse_rows
        ),
        all_sparse_directions_have_right_order_three_gauge=all(
            row.right_order_histogram == ((3, 1), (15, 4), (75, 20))
            and row.right_c3_min_degrees == (3,)
            for row in sparse_rows
        ),
        all_sparse_directions_have_min_combined_order_507=all(
            row.combined_order_min == QUOTIENT_ORDER for row in sparse_rows
        ),
        all_active_corner_rows_use_the_same_six_sparse_directions=all(
            row.pair_directions == EXPECTED_SPARSE_DIRECTIONS for row in cost_rows
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner Kummer-cost gate")
    profile = corner_kummer_cost_profile()
    expected_kernel = FactorOrderProfile(
        "kernel_trace",
        (57, 0),
        125,
        1,
        25,
        1,
        25,
        36,
        25,
        0,
        1,
        0,
        1,
        0,
        1,
    )
    expected_directions = (
        KernelGaugeDirectionProfile(25, (1, 25), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 25, 25, 25, (3, 15, 75), (3,), (169,), (13,)),
        KernelGaugeDirectionProfile(172, (1, 3), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 2200, 25, 3, (3, 15, 75), (3,), (169,), (13,)),
        KernelGaugeDirectionProfile(197, (2, 28), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 2225, 50, 28, (3, 15, 75), (3,), (169,), (13,)),
        KernelGaugeDirectionProfile(310, (1, 141), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 10450, 25, 141, (3, 15, 75), (3,), (169,), (13,)),
        KernelGaugeDirectionProfile(335, (2, 166), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 10475, 50, 166, (3, 15, 75), (3,), (169,), (13,)),
        KernelGaugeDirectionProfile(482, (2, 144), 25, ((3, 1), (15, 4), (75, 20)), (169,), 507, 12650, 50, 144, (3, 15, 75), (3,), (169,), (13,)),
    )
    expected_corner_rows = (
        CornerKummerCostRow(1, 197, (0, 172, 482), -1, 75, -75, EXPECTED_SPARSE_DIRECTIONS, True, True, (507, 507, 507, 507, 507, 507)),
        CornerKummerCostRow(1, 310, (172, 197, 369), 1, 75, 75, EXPECTED_SPARSE_DIRECTIONS, True, True, (507, 507, 507, 507, 507, 507)),
        CornerKummerCostRow(6, 197, (138, 310, 335), -1, 75, -75, EXPECTED_SPARSE_DIRECTIONS, True, True, (507, 507, 507, 507, 507, 507)),
        CornerKummerCostRow(6, 310, (0, 25, 335), 1, 75, 75, EXPECTED_SPARSE_DIRECTIONS, True, True, (507, 507, 507, 507, 507, 507)),
    )
    row_ok = (
        profile.active_corner_count == 4
        and profile.pair_direction_union == EXPECTED_SPARSE_DIRECTIONS
        and profile.boundary_direction_values == (197, 310)
        and profile.kernel_trace_factor == expected_kernel
        and profile.sparse_direction_rows == expected_directions
        and profile.corner_rows == expected_corner_rows
        and profile.block_k_trace_selector_passes
        and profile.sparse_sections_are_invalid_producers
        and profile.kernel_trace_is_right_only
        and profile.all_sparse_directions_have_primitive_c169_cost
        and profile.all_sparse_directions_have_right_order_three_gauge
        and profile.all_sparse_directions_have_min_combined_order_507
        and profile.all_active_corner_rows_use_the_same_six_sparse_directions
    )

    print(
        "corner_kummer_cost_summary: "
        f"active_corner_count={profile.active_corner_count} "
        f"pair_direction_union={profile.pair_direction_union} "
        f"boundary_direction_values={profile.boundary_direction_values} "
        f"block_K_trace_selector_passes={int(profile.block_k_trace_selector_passes)} "
        f"sparse_sections_invalid_producers={int(profile.sparse_sections_are_invalid_producers)} "
        f"kernel_trace_right_only={int(profile.kernel_trace_is_right_only)} "
        f"sparse_C169_primitive={int(profile.all_sparse_directions_have_primitive_c169_cost)} "
        f"right_order_three_gauge={int(profile.all_sparse_directions_have_right_order_three_gauge)} "
        f"min_combined_order_507={int(profile.all_sparse_directions_have_min_combined_order_507)}"
    )
    print(f"kernel_trace_factor={profile.kernel_trace_factor}")
    print("corner_cost_rows")
    for row in profile.corner_rows:
        print(f"  {row}")
    print("sparse_direction_cost_rows")
    for row in profile.sparse_direction_rows:
        print(f"  {row}")
    print("interpretation")
    print("  forced_K_trace_is_a_cheap_right_kernel_trace_factor=1")
    print("  every_active_corner_edge_keeps_primitive_C169_order_in_all_kernel_gauges=1")
    print("  right_kernel_gauge_can_lower_only_the_right_side_not_the_C169_cost=1")
    print("  no_right_gauge_only_escape_remains_for_the_half_bridge_corner=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_kummer_cost_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_kummer_cost_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
