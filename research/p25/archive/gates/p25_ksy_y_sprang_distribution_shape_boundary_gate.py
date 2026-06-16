#!/usr/bin/env python3
"""Finite shape boundary for the Sprang/Kronecker D=2 route.

Sprang's Kronecker distribution machinery is a live theorem surface, but its
displayed distribution shapes are sums over isogeny kernels and D-torsion
translations.  The p25 target is more rigid:

    base * K_trace * (1 + D + D^2) * (1 - T)

where the visible D step has order 507.  Thus the three D points are a short
arithmetic segment, not an order-3 subgroup/coset, and D=2 is useful only via
an exact normalized-y/theta2 specialization, not as a literal 2-torsion selector
on the odd p25 source quotient.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm


Coord = tuple[int, int]

RIGHT_ORDER = 3
C_ORDER = 169
BASE = (1, 25)
D_STEP = (1, 3)
T_EDGE = (2, 113)
ROW_ORDER3_STEP = (1, 0)
C13_STEP = (0, 13)
C169_STEP = (0, 1)


@dataclass(frozen=True)
class ShapeProfile:
    name: str
    positive_layer: tuple[Coord, ...]
    negative_layer: tuple[Coord, ...]
    support: int
    equals_target: bool
    preserves_row_graph: bool
    preserves_t_edge: bool
    verdict: str


@dataclass(frozen=True)
class SprangDistributionShapeBoundaryProfile:
    target_profile: ShapeProfile
    kernel_only_profile: ShapeProfile
    row_order3_kernel_profile: ShapeProfile
    c13_kernel_profile: ShapeProfile
    c169_axis_profile: ShapeProfile
    c169_projection_profile: ShapeProfile
    d_visible_order: int
    d_after_three: Coord
    d_segment_is_not_order3_subgroup: bool
    odd_source_has_nonzero_2_torsion: bool
    d2_literal_torsion_selector_killed: bool
    exact_specialization_required: str
    row_ok: bool


def add(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def scale(step: Coord, scalar: int) -> Coord:
    return ((step[0] * scalar) % RIGHT_ORDER, (step[1] * scalar) % C_ORDER)


def coord_order(step: Coord) -> int:
    right_order = 1 if step[0] % RIGHT_ORDER == 0 else RIGHT_ORDER // gcd(RIGHT_ORDER, step[0])
    c_order = 1 if step[1] % C_ORDER == 0 else C_ORDER // gcd(C_ORDER, step[1])
    return lcm(right_order, c_order)


def target_positive() -> tuple[Coord, ...]:
    return tuple(sorted(add(BASE, scale(D_STEP, index)) for index in range(3)))


def translate(points: tuple[Coord, ...], edge: Coord = T_EDGE) -> tuple[Coord, ...]:
    return tuple(sorted(add(point, edge) for point in points))


def layer_from_step(base: Coord, step: Coord, length: int) -> tuple[Coord, ...]:
    return tuple(sorted(add(base, scale(step, index)) for index in range(length)))


def profile_shape(
    name: str,
    positive: tuple[Coord, ...],
    verdict: str,
    preserves_row_graph: bool,
    preserves_t_edge: bool,
    edge: Coord = T_EDGE,
) -> ShapeProfile:
    negative = translate(positive, edge)
    target_pos = target_positive()
    target_neg = translate(target_pos)
    support = len(set(positive) | set(negative))
    equals_target = tuple(sorted(positive)) == target_pos and tuple(sorted(negative)) == target_neg
    return ShapeProfile(
        name=name,
        positive_layer=tuple(sorted(positive)),
        negative_layer=tuple(sorted(negative)),
        support=support,
        equals_target=equals_target,
        preserves_row_graph=preserves_row_graph,
        preserves_t_edge=preserves_t_edge,
        verdict=verdict,
    )


def c169_projection(points: tuple[Coord, ...]) -> tuple[Coord, ...]:
    return tuple(sorted((0, point[1]) for point in points))


def nonzero_two_torsion() -> tuple[Coord, ...]:
    return tuple(
        (right, c_value)
        for right in range(RIGHT_ORDER)
        for c_value in range(C_ORDER)
        if (right, c_value) != (0, 0)
        and scale((right, c_value), 2) == (0, 0)
    )


def profile_sprang_distribution_shape_boundary() -> SprangDistributionShapeBoundaryProfile:
    target = profile_shape(
        "exact_mixed_row_labeled_specialization",
        target_positive(),
        "accept_only_if_source_theorem_emits_this_shape",
        preserves_row_graph=True,
        preserves_t_edge=True,
    )
    kernel_only = profile_shape(
        "k_trace_or_base_edge_only",
        (BASE,),
        "reject_too_small_kernel_only_shadow",
        preserves_row_graph=False,
        preserves_t_edge=True,
    )
    row_order3 = profile_shape(
        "literal_order3_kernel_coset",
        layer_from_step(BASE, ROW_ORDER3_STEP, 3),
        "reject_order3_kernel_coset_wrong_c_coordinates",
        preserves_row_graph=False,
        preserves_t_edge=True,
    )
    c13_kernel = profile_shape(
        "literal_c13_kernel_coset",
        layer_from_step(BASE, C13_STEP, 13),
        "reject_too_broad_c13_kernel_shadow",
        preserves_row_graph=False,
        preserves_t_edge=True,
    )
    c169_axis = profile_shape(
        "literal_c169_axis_sum",
        layer_from_step(BASE, C169_STEP, 169),
        "reject_full_c169_axis_too_broad",
        preserves_row_graph=False,
        preserves_t_edge=True,
    )
    projection = profile_shape(
        "c169_projection_of_target",
        c169_projection(target_positive()),
        "reject_projection_loses_c3_row_graph_and_T_edge",
        preserves_row_graph=False,
        preserves_t_edge=False,
        edge=(0, T_EDGE[1]),
    )

    d_after_three = scale(D_STEP, 3)
    d_order = coord_order(D_STEP)
    d_segment = {scale(D_STEP, index) for index in range(3)}
    d_segment_is_not_subgroup = (
        d_order == 507
        and d_after_three == (0, 9)
        and add(D_STEP, scale(D_STEP, 2)) not in d_segment
    )
    two_torsion = nonzero_two_torsion()
    d2_torsion_killed = len(two_torsion) == 0

    row_ok = (
        target.equals_target
        and target.support == 6
        and kernel_only.support == 2
        and not kernel_only.equals_target
        and row_order3.positive_layer == ((0, 25), (1, 25), (2, 25))
        and row_order3.support == 6
        and not row_order3.equals_target
        and c13_kernel.support == 26
        and not c13_kernel.equals_target
        and c169_axis.support == 338
        and not c169_axis.equals_target
        and projection.support == 6
        and not projection.equals_target
        and not projection.preserves_row_graph
        and not projection.preserves_t_edge
        and d_segment_is_not_subgroup
        and d2_torsion_killed
    )

    return SprangDistributionShapeBoundaryProfile(
        target_profile=target,
        kernel_only_profile=kernel_only,
        row_order3_kernel_profile=row_order3,
        c13_kernel_profile=c13_kernel,
        c169_axis_profile=c169_axis,
        c169_projection_profile=projection,
        d_visible_order=d_order,
        d_after_three=d_after_three,
        d_segment_is_not_order3_subgroup=d_segment_is_not_subgroup,
        odd_source_has_nonzero_2_torsion=bool(two_torsion),
        d2_literal_torsion_selector_killed=d2_torsion_killed,
        exact_specialization_required=(
            "Sprang/Kronecker can continue only if an even-D theorem emits the "
            "exact mixed row-labeled P/theta2 payload; literal kernel, torsion, "
            "or C169-projection distributions are insufficient."
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_sprang_distribution_shape_boundary()
    print("p25 KSY-y Sprang/Kronecker distribution-shape boundary gate")
    print("profiles")
    for row in (
        profile.target_profile,
        profile.kernel_only_profile,
        profile.row_order3_kernel_profile,
        profile.c13_kernel_profile,
        profile.c169_axis_profile,
        profile.c169_projection_profile,
    ):
        print(
            "  "
            f"{row.name}: support={row.support} exact={int(row.equals_target)} "
            f"row_graph={int(row.preserves_row_graph)} T={int(row.preserves_t_edge)} "
            f"verdict={row.verdict}"
        )
    print("shape_laws")
    print(f"  D_visible_order={profile.d_visible_order}")
    print(f"  three_D={profile.d_after_three}")
    print(f"  D_segment_is_not_order3_subgroup={int(profile.d_segment_is_not_order3_subgroup)}")
    print(f"  odd_source_has_nonzero_2_torsion={int(profile.odd_source_has_nonzero_2_torsion)}")
    print(f"  D2_literal_torsion_selector_killed={int(profile.d2_literal_torsion_selector_killed)}")
    print("interpretation")
    print("  literal_kernel_or_torsion_distribution_shapes_do_not_emit_p25_P=1")
    print("  C169_projection_is_only_a_screen_not_a_payload=1")
    print("  Sprang_route_requires_exact_mixed_row_labeled_specialization=1")
    print(f"ksy_y_sprang_distribution_shape_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Sprang distribution-shape boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
