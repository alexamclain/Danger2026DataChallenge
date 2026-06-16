#!/usr/bin/env python3
"""Selector law for the p25 Hilbert-90 corner skew derivative.

The skew-derivative gate shows that the selected half-source-edge is the
nonzero residual of the curved three-point graph under the recorded 197/310
boundary.  This gate scans all nonzero source translations and records the
remaining ambiguity.

For every active corner, exactly two translations make a skew derivative with
one Newton-vertex cancellation and the attractive residual short lengths
31 and 53: the 197/310 pair.  The q=0 endpoint condition removes this
ambiguity only in two of the four rows.  The Hilbert-90 bridge-pair
orientation is the condition that selects the recorded direction in all four
rows; the opposite short skew derivative never inverts to the signed bridge.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    boundary,
    inversion_boundary,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_potential_gate import (
    bridge_pairs,
    half_potential_representatives,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_gate import (
    source_items,
    source_mask,
    row_edges,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_gate import (
    chain_by_source_row,
    signed_short_step,
    source_coord,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Items = tuple[tuple[int, int], ...]
SourceItems = tuple[tuple[tuple[int, int], int], ...]


@dataclass(frozen=True)
class SkewDerivativeSelectorRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    chain_q_values: tuple[int, ...]
    skew_short_candidate_directions_q: tuple[int, ...]
    skew_short_candidate_directions_d: tuple[int, ...]
    q0_skew_short_candidate_directions_q: tuple[int, ...]
    exact_half_potential_directions_q: tuple[int, ...]
    bridge_image_directions_q: tuple[int, ...]
    opposite_direction_q: int
    opposite_first_boundary: Items
    opposite_source_values: SourceItems
    q0_endpoint_selector_sufficient: bool
    opposite_has_q0_endpoint: bool
    opposite_inverts_to_bridge: bool


@dataclass(frozen=True)
class SkewDerivativeSelectorProfile:
    row_count: int
    all_rows_have_exactly_two_short_skew_derivatives: bool
    all_short_skew_derivatives_are_197_310: bool
    all_recorded_directions_are_exact_bridge_half_potentials: bool
    q0_endpoint_is_not_always_sufficient: bool
    all_opposite_short_derivatives_miss_bridge: bool
    rows: tuple[SkewDerivativeSelectorRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


def residual_short_steps(chain: dict[int, int], direction_q: int) -> tuple[int, ...]:
    direction_row, direction_c = source_coord(direction_q)
    rows = chain_by_source_row(chain)
    out: list[int] = []
    for target_row in range(RIGHT_DEGREE):
        shifted_from_row = (target_row - direction_row) % RIGHT_DEGREE
        _orig_q, original_c, _orig_coeff = rows[target_row]
        _shift_q, shift_c, _shift_coeff = rows[shifted_from_row]
        shifted_c = (shift_c + direction_c) % SQUARE_C
        delta = (shifted_c - original_c) % SQUARE_C
        if delta:
            out.append(signed_short_step(delta))
    return tuple(sorted(out))


def has_one_skew_cancellation(chain: dict[int, int], direction_q: int) -> bool:
    direction_row, direction_c = source_coord(direction_q)
    rows = chain_by_source_row(chain)
    cancellation_count = 0
    for target_row in range(RIGHT_DEGREE):
        shifted_from_row = (target_row - direction_row) % RIGHT_DEGREE
        _orig_q, original_c, _orig_coeff = rows[target_row]
        _shift_q, shift_c, _shift_coeff = rows[shifted_from_row]
        cancellation_count += int((shift_c + direction_c) % SQUARE_C == original_c)
    return cancellation_count == 1


def is_two_primitive_row_edges(poly: dict[int, int]) -> bool:
    if len(poly) != 4:
        return False
    edges = row_edges(source_mask(poly))
    return len(edges) == 2 and all(edge.primitive_c169_steps for edge in edges)


def is_short_skew_derivative(chain: dict[int, int], direction_q: int) -> bool:
    first = boundary(chain, direction_q)
    return (
        has_one_skew_cancellation(chain, direction_q)
        and is_two_primitive_row_edges(first)
        and residual_short_steps(chain, direction_q) == (31, 53)
    )


def scan_row(active_row, pairs: tuple[tuple[int, int], ...]) -> SkewDerivativeSelectorRow:
    chain = dict(zip(active_row.q_values, active_row.recorded_coefficients))
    short_candidates: list[int] = []
    q0_candidates: list[int] = []
    exact_candidates: list[int] = []
    bridge_candidates: list[int] = []
    for direction_q in range(1, QUOTIENT_ORDER):
        first = boundary(chain, direction_q)
        if is_short_skew_derivative(chain, direction_q):
            short_candidates.append(direction_q)
            if 0 in first:
                q0_candidates.append(direction_q)
        if half_potential_representatives(first, pairs) is not None:
            exact_candidates.append(direction_q)
        if inversion_boundary(first) == bridge_coefficients():
            bridge_candidates.append(direction_q)

    opposites = tuple(
        direction for direction in short_candidates if direction != active_row.boundary_direction_q
    )
    if len(opposites) != 1:
        raise AssertionError(f"expected one opposite short skew derivative, got {opposites}")
    opposite = opposites[0]
    opposite_first = boundary(chain, opposite)
    return SkewDerivativeSelectorRow(
        orientation_mask=active_row.orientation_mask,
        recorded_direction_q=active_row.boundary_direction_q,
        recorded_direction_d=d_residue_from_q(active_row.boundary_direction_q),
        chain_q_values=active_row.q_values,
        skew_short_candidate_directions_q=tuple(short_candidates),
        skew_short_candidate_directions_d=tuple(d_residue_from_q(direction) for direction in short_candidates),
        q0_skew_short_candidate_directions_q=tuple(q0_candidates),
        exact_half_potential_directions_q=tuple(exact_candidates),
        bridge_image_directions_q=tuple(bridge_candidates),
        opposite_direction_q=opposite,
        opposite_first_boundary=as_items(opposite_first),
        opposite_source_values=source_items(opposite_first),
        q0_endpoint_selector_sufficient=tuple(q0_candidates) == (active_row.boundary_direction_q,),
        opposite_has_q0_endpoint=0 in opposite_first,
        opposite_inverts_to_bridge=inversion_boundary(opposite_first) == bridge_coefficients(),
    )


def skew_derivative_selector_profile() -> SkewDerivativeSelectorProfile:
    pairs = bridge_pairs()
    rows = tuple(scan_row(row, pairs) for row in coefficient_rigidity_profile().rows)
    return SkewDerivativeSelectorProfile(
        row_count=len(rows),
        all_rows_have_exactly_two_short_skew_derivatives=all(
            len(row.skew_short_candidate_directions_q) == 2 for row in rows
        ),
        all_short_skew_derivatives_are_197_310=all(
            row.skew_short_candidate_directions_q == (197, 310)
            and row.skew_short_candidate_directions_d == (122, 385)
            for row in rows
        ),
        all_recorded_directions_are_exact_bridge_half_potentials=all(
            row.exact_half_potential_directions_q == (row.recorded_direction_q,)
            and row.bridge_image_directions_q == (row.recorded_direction_q,)
            for row in rows
        ),
        q0_endpoint_is_not_always_sufficient=any(
            not row.q0_endpoint_selector_sufficient for row in rows
        ),
        all_opposite_short_derivatives_miss_bridge=all(
            not row.opposite_inverts_to_bridge for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner skew-derivative selector gate")
    profile = skew_derivative_selector_profile()
    expected_rows = (
        SkewDerivativeSelectorRow(1, 197, 122, (0, 172, 482), (197, 310), (122, 385), (197, 310), (197,), (197,), 310, ((0, -1), (172, -1), (285, 1), (310, 1)), (((0, 0), -1), ((0, 116), 1), ((1, 3), -1), ((1, 141), 1)), False, True, False),
        SkewDerivativeSelectorRow(1, 310, 385, (172, 197, 369), (197, 310), (122, 385), (310,), (310,), (310,), 197, ((59, -1), (172, 1), (197, 1), (394, -1)), (((1, 3), 1), ((1, 56), -1), ((2, 28), 1), ((2, 59), -1)), True, False, False),
        SkewDerivativeSelectorRow(6, 197, 122, (138, 310, 335), (197, 310), (122, 385), (197,), (197,), (197,), 310, ((113, 1), (310, -1), (335, -1), (448, 1)), (((1, 110), 1), ((1, 141), -1), ((2, 113), 1), ((2, 166), -1)), True, False, False),
        SkewDerivativeSelectorRow(6, 310, 385, (0, 25, 335), (197, 310), (122, 385), (197, 310), (310,), (310,), 197, ((0, 1), (197, -1), (222, -1), (335, 1)), (((0, 0), 1), ((0, 53), -1), ((2, 28), -1), ((2, 166), 1)), False, True, False),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_have_exactly_two_short_skew_derivatives
        and profile.all_short_skew_derivatives_are_197_310
        and profile.all_recorded_directions_are_exact_bridge_half_potentials
        and profile.q0_endpoint_is_not_always_sufficient
        and profile.all_opposite_short_derivatives_miss_bridge
        and profile.rows == expected_rows
    )

    print(
        "corner_skew_derivative_selector_summary: "
        f"short_candidates={tuple(row.skew_short_candidate_directions_q for row in profile.rows)} "
        f"q0_candidates={tuple(row.q0_skew_short_candidate_directions_q for row in profile.rows)} "
        f"exact_hits={tuple(row.exact_half_potential_directions_q for row in profile.rows)} "
        f"opposites={tuple(row.opposite_direction_q for row in profile.rows)}"
    )
    print("corner_skew_derivative_selector_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("selector_laws")
    print("  one-cancellation skew derivatives with residual short steps 31/53 are exactly directions 197 and 310")
    print("  the q=0 endpoint condition removes this ambiguity only in two of the four active rows")
    print("  the Hilbert-90 bridge-pair orientation selects the recorded direction in all four rows")
    print("interpretation")
    print("  producer_must_realize_the_oriented_skew_derivative_not_only_the_short_residual_shape=1")
    print("  opposite_197_310_short_derivative_is_a_near_miss_control=1")
    print("  q0_endpoint_plus_31_53_is_still_not_a_complete_certificate=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
