#!/usr/bin/env python3
"""Corner normal form for p25 Hilbert-90 source chains.

The primitive-word gate showed that a bridge-compatible source chain can be
written as

    C = -(1 + z + z^(1-e)),       e = 122 in C_507.

This gate ties that word back to the earlier square-axis bridge factors.  The
six-point bridge is the unique anti-invariant length-three run in the primitive
D-coordinate: its run direction is the known outer S/D step, and its center is
the half-separation of the bridge edge.  The first Hilbert-90 boundary is the
corresponding half-edge, so the scary curved source chain is a corner

    {0, S, S - E}

before the source-graph and K-trace constraints are attached.

The formal corner identity also has non-graph controls; those are recorded so
that a producer cannot pass by using only a cyclic C_507 antiderivative while
collapsing the C_3 source rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_boundary,
    d_inversion_boundary,
    d_residue_from_q,
    primitive_word_profile,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    coord_from_q as shift_coord_from_q,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


N = QUOTIENT_ORDER
Poly = dict[int, int]
Items = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class AntiRunRepresentation:
    center_d: int
    unit_d: int
    sign: int
    center_q: int
    unit_q: int
    positive_d: tuple[int, ...]
    negative_d: tuple[int, ...]
    positive_q: tuple[int, ...]
    negative_q: tuple[int, ...]


@dataclass(frozen=True)
class CornerAntiderivative:
    center_d: int
    unit_d: int
    sign: int
    chain_word: Items
    chain_q_values: tuple[int, ...]
    source_rows: tuple[int, ...]
    source_graph: bool
    recovers_bridge: bool


@dataclass(frozen=True)
class ActiveCornerRow:
    orientation_mask: int
    boundary_step_d: int
    boundary_direction_q: int
    boundary_is_half_bridge: bool
    chain_word: Items
    chain_q_values: tuple[int, ...]
    source_rows: tuple[int, ...]
    source_graph: bool
    cancellation_vertex_d: int
    cancellation_vertex_q: int
    cancellation_is_unit_vertex: bool
    first_boundary_support: int
    recovers_bridge: bool


@dataclass(frozen=True)
class CornerNormalFormProfile:
    bridge_sep_q: int
    bridge_sep_d: int
    half_bridge_d: int
    half_bridge_q: int
    opposite_half_q: int
    unit_d: int
    unit_q: int
    unit_shift_coord: tuple[int, int]
    half_shift_coord: tuple[int, int]
    bridge_sep_shift_coord: tuple[int, int]
    anti_run_representations: tuple[AntiRunRepresentation, ...]
    corner_antiderivatives: tuple[CornerAntiderivative, ...]
    active_rows: tuple[ActiveCornerRow, ...]
    anti_run_unique_up_to_orientation: bool
    all_corner_antiderivatives_recover_bridge: bool
    corner_antiderivative_graph_count: int
    active_rows_all_source_graphs: bool
    active_rows_all_half_boundaries: bool
    active_rows_all_cancel_at_unit_vertices: bool
    active_rows_all_recover_bridge: bool


def as_items(poly: Poly) -> Items:
    return tuple(sorted(poly.items()))


@cache
def primitive_profile():
    return primitive_word_profile()


@cache
def d_to_q_map() -> tuple[int, ...]:
    out = [-1] * N
    for q_value in range(N):
        out[d_residue_from_q(q_value)] = q_value
    if any(q_value < 0 for q_value in out):
        raise AssertionError("D-coordinate map is not surjective on C_507")
    return tuple(out)


def q_from_d_residue(residue: int) -> int:
    return d_to_q_map()[residue % N]


def source_rows(q_values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(q_value % RIGHT_DEGREE for q_value in q_values))


def is_source_graph(q_values: tuple[int, ...]) -> bool:
    return source_rows(q_values) == tuple(range(RIGHT_DEGREE))


def anti_run(center: int, unit: int, sign: int) -> Poly:
    out: Poly = {}
    for point in ((center - unit) % N, center % N, (center + unit) % N):
        out[point] = out.get(point, 0) + sign
    for point in ((-center - unit) % N, (-center) % N, (-center + unit) % N):
        out[point] = out.get(point, 0) - sign
    return {point: coefficient for point, coefficient in sorted(out.items()) if coefficient}


def anti_run_representations() -> tuple[AntiRunRepresentation, ...]:
    bridge_word = dict(primitive_profile().bridge_word)
    rows: list[AntiRunRepresentation] = []
    for center in range(N):
        for unit in range(1, N):
            if gcd(unit, N) != 1:
                continue
            for sign in (-1, 1):
                candidate = anti_run(center, unit, sign)
                if candidate != bridge_word:
                    continue
                positive_d = tuple(sorted(point for point, value in candidate.items() if value > 0))
                negative_d = tuple(sorted(point for point, value in candidate.items() if value < 0))
                rows.append(
                    AntiRunRepresentation(
                        center_d=center,
                        unit_d=unit,
                        sign=sign,
                        center_q=q_from_d_residue(center),
                        unit_q=q_from_d_residue(unit),
                        positive_d=positive_d,
                        negative_d=negative_d,
                        positive_q=tuple(sorted(q_from_d_residue(point) for point in positive_d)),
                        negative_q=tuple(sorted(q_from_d_residue(point) for point in negative_d)),
                    )
                )
    return tuple(sorted(rows, key=lambda row: (row.center_d, row.unit_d, row.sign)))


def corner_chain(center: int, unit: int, sign: int) -> Poly:
    coefficient = -sign
    points = (0, unit % N, (unit - center) % N)
    return {point: coefficient for point in sorted(points)}


def corner_antiderivatives() -> tuple[CornerAntiderivative, ...]:
    bridge_word = dict(primitive_profile().bridge_word)
    rows: list[CornerAntiderivative] = []
    for anti in anti_run_representations():
        chain = corner_chain(anti.center_d, anti.unit_d, anti.sign)
        q_values = tuple(sorted(q_from_d_residue(point) for point in chain))
        recovered = d_inversion_boundary(d_boundary(chain, anti.center_d)) == bridge_word
        rows.append(
            CornerAntiderivative(
                center_d=anti.center_d,
                unit_d=anti.unit_d,
                sign=anti.sign,
                chain_word=as_items(chain),
                chain_q_values=q_values,
                source_rows=source_rows(q_values),
                source_graph=is_source_graph(q_values),
                recovers_bridge=recovered,
            )
        )
    return tuple(rows)


def active_corner_rows() -> tuple[ActiveCornerRow, ...]:
    bridge_word = primitive_profile().bridge_word
    half_d = (-d_residue_from_q(BRIDGE_STEP) * pow(2, -1, N)) % N
    unit_vertices = {1, (-1) % N}
    rows: list[ActiveCornerRow] = []
    for primitive_row in primitive_profile().rows:
        chain = dict(primitive_row.chain_word)
        shifted_points = {(point + primitive_row.boundary_step_d) % N for point in chain}
        overlap = tuple(sorted(set(chain) & shifted_points))
        if len(overlap) != 1:
            raise AssertionError(f"expected one cancellation point, got {overlap}")
        q_values = tuple(sorted(primitive_row.q_values))
        rows.append(
            ActiveCornerRow(
                orientation_mask=primitive_row.orientation_mask,
                boundary_step_d=primitive_row.boundary_step_d,
                boundary_direction_q=primitive_row.boundary_direction_q,
                boundary_is_half_bridge=primitive_row.boundary_step_d in {half_d, (-half_d) % N},
                chain_word=primitive_row.chain_word,
                chain_q_values=q_values,
                source_rows=source_rows(q_values),
                source_graph=is_source_graph(q_values),
                cancellation_vertex_d=overlap[0],
                cancellation_vertex_q=q_from_d_residue(overlap[0]),
                cancellation_is_unit_vertex=overlap[0] in unit_vertices,
                first_boundary_support=len(primitive_row.first_boundary_word),
                recovers_bridge=primitive_row.bridge_word == bridge_word,
            )
        )
    return tuple(rows)


def corner_profile() -> CornerNormalFormProfile:
    bridge_sep_d = d_residue_from_q(BRIDGE_STEP)
    half_d = (-bridge_sep_d * pow(2, -1, N)) % N
    anti_runs = anti_run_representations()
    corners = corner_antiderivatives()
    active = active_corner_rows()
    return CornerNormalFormProfile(
        bridge_sep_q=BRIDGE_STEP,
        bridge_sep_d=bridge_sep_d,
        half_bridge_d=half_d,
        half_bridge_q=q_from_d_residue(half_d),
        opposite_half_q=q_from_d_residue((-half_d) % N),
        unit_d=1,
        unit_q=q_from_d_residue(1),
        unit_shift_coord=shift_coord_from_q(q_from_d_residue(1)),
        half_shift_coord=shift_coord_from_q(q_from_d_residue(half_d)),
        bridge_sep_shift_coord=shift_coord_from_q(BRIDGE_STEP),
        anti_run_representations=anti_runs,
        corner_antiderivatives=corners,
        active_rows=active,
        anti_run_unique_up_to_orientation=anti_runs
        == (
            AntiRunRepresentation(122, 1, 1, 197, 172, (121, 122, 123), (384, 385, 386), (25, 197, 369), (138, 310, 482)),
            AntiRunRepresentation(122, 506, 1, 197, 335, (121, 122, 123), (384, 385, 386), (25, 197, 369), (138, 310, 482)),
            AntiRunRepresentation(385, 1, -1, 310, 172, (121, 122, 123), (384, 385, 386), (25, 197, 369), (138, 310, 482)),
            AntiRunRepresentation(385, 506, -1, 310, 335, (121, 122, 123), (384, 385, 386), (25, 197, 369), (138, 310, 482)),
        ),
        all_corner_antiderivatives_recover_bridge=all(row.recovers_bridge for row in corners),
        corner_antiderivative_graph_count=sum(row.source_graph for row in corners),
        active_rows_all_source_graphs=all(row.source_graph for row in active),
        active_rows_all_half_boundaries=all(row.boundary_is_half_bridge for row in active),
        active_rows_all_cancel_at_unit_vertices=all(row.cancellation_is_unit_vertex for row in active),
        active_rows_all_recover_bridge=all(row.recovers_bridge for row in active),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner-normal-form gate")
    profile = corner_profile()
    expected_corners = (
        CornerAntiderivative(122, 1, 1, ((0, -1), (1, -1), (386, -1)), (0, 172, 482), (0, 1, 2), True, True),
        CornerAntiderivative(122, 506, 1, ((0, -1), (384, -1), (506, -1)), (0, 138, 335), (0, 0, 2), False, True),
        CornerAntiderivative(385, 1, -1, ((0, 1), (1, 1), (123, 1)), (0, 172, 369), (0, 0, 1), False, True),
        CornerAntiderivative(385, 506, -1, ((0, 1), (121, 1), (506, 1)), (0, 25, 335), (0, 1, 2), True, True),
    )
    expected_active = (
        ActiveCornerRow(1, 122, 197, True, ((0, -1), (1, -1), (386, -1)), (0, 172, 482), (0, 1, 2), True, 1, 172, True, 4, True),
        ActiveCornerRow(1, 385, 310, True, ((1, 1), (122, 1), (123, 1)), (172, 197, 369), (0, 1, 2), True, 1, 172, True, 4, True),
        ActiveCornerRow(6, 122, 197, True, ((384, -1), (385, -1), (506, -1)), (138, 310, 335), (0, 1, 2), True, 506, 335, True, 4, True),
        ActiveCornerRow(6, 385, 310, True, ((0, 1), (121, 1), (506, 1)), (0, 25, 335), (0, 1, 2), True, 506, 335, True, 4, True),
    )
    row_ok = (
        profile.bridge_sep_q == 113
        and profile.bridge_sep_d == 263
        and profile.half_bridge_d == 122
        and profile.half_bridge_q == 197
        and profile.opposite_half_q == 310
        and profile.unit_d == 1
        and profile.unit_q == S_STEP == 172
        and profile.unit_shift_coord == (1, 1)
        and profile.half_shift_coord == (2, 122)
        and profile.bridge_sep_shift_coord == (2, 94)
        and profile.anti_run_unique_up_to_orientation
        and profile.corner_antiderivatives == expected_corners
        and profile.active_rows == expected_active
        and profile.all_corner_antiderivatives_recover_bridge
        and profile.corner_antiderivative_graph_count == 2
        and profile.active_rows_all_source_graphs
        and profile.active_rows_all_half_boundaries
        and profile.active_rows_all_cancel_at_unit_vertices
        and profile.active_rows_all_recover_bridge
    )

    print(
        "corner_normal_form_summary: "
        f"bridge_sep_q={profile.bridge_sep_q} bridge_sep_d={profile.bridge_sep_d} "
        f"half_bridge_d={profile.half_bridge_d} half_bridge_q={profile.half_bridge_q} "
        f"opposite_half_q={profile.opposite_half_q} unit_q={profile.unit_q} "
        f"unit_shift_coord={profile.unit_shift_coord} "
        f"half_shift_coord={profile.half_shift_coord} "
        f"bridge_sep_shift_coord={profile.bridge_sep_shift_coord}"
    )
    print("anti_run_representations")
    for row in profile.anti_run_representations:
        print(f"  {row}")
    print("formal_corner_antiderivatives")
    for row in profile.corner_antiderivatives:
        print(f"  {row}")
    print("active_source_graph_rows")
    for row in profile.active_rows:
        print(f"  {row}")
    print("corner_identity")
    print("  bridge = anti_run(center=e, unit=1) with e = -bridge_sep/2 = 122 in C_507")
    print("  canonical_chain = -(1 + z + z^(1-e)); first_boundary_step = e")
    print("  source_corner = {0, S, S-E}, where S is the outer D/S unit and E is the half-bridge edge")
    print("interpretation")
    print("  bridge_has_unique_anti_invariant_length_three_run_direction_up_to_orientation=1")
    print("  hilbert90_source_chain_is_a_half_bridge_corner_not_an_arbitrary_three_point_set=1")
    print("  formal_cyclic_corner_antiderivatives_include_non_source_graph_controls=1")
    print("  producer_must_realize_the_source_graph_corner_and_not_only_a_C507_antiderivative=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_normal_form_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
