#!/usr/bin/env python3
"""Image-orbit obstruction for the p25 Hilbert-90 corner skew near miss.

The skew-derivative selector leaves a controlled twofold near miss: directions
197 and 310 are the only one-cancellation skew derivatives with residual short
lengths 31 and 53.  This gate records what happens after the Hilbert-90
inversion boundary.

The recorded branch is the unique short skew derivative whose image is a
signed pair of complete S-orbits, with S=172.  The opposite branch is never an
S-layer image: in two rows it is a signed pair of wrong 25-orbits, and in the
other two rows it expands to support eight with no length-three constant-orbit
decomposition at all.
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
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_s_layer_image_gate import (
    signed_s_layer_decomposition,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_gate import (
    skew_derivative_selector_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Items = tuple[tuple[int, int], ...]
OrbitDecomposition = tuple[tuple[tuple[int, ...], int], ...]


@dataclass(frozen=True)
class ImageOrbitBranch:
    branch_name: str
    direction_q: int
    direction_d: int
    image_support: int
    image_items: Items
    s_layer_decomposition: OrbitDecomposition
    length3_orbit_steps_q: tuple[int, ...]
    length3_orbit_steps_d: tuple[int, ...]
    length3_orbit_decompositions: tuple[tuple[int, OrbitDecomposition], ...]
    is_signed_s_layer: bool
    is_bridge_image: bool


@dataclass(frozen=True)
class SkewImageOrbitRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    recorded_branch: ImageOrbitBranch
    opposite_branch: ImageOrbitBranch
    recorded_unique_s_orbit: bool
    opposite_has_no_s_orbit: bool
    opposite_wrong_orbit_step_q: int | None


@dataclass(frozen=True)
class SkewImageOrbitProfile:
    row_count: int
    bridge_decomposition: OrbitDecomposition
    all_recorded_branches_are_signed_s_layer: bool
    all_opposite_branches_have_no_s_layer: bool
    opposite_support_values: tuple[int, ...]
    opposite_wrong_orbit_steps_q: tuple[int, ...]
    rows: tuple[SkewImageOrbitRow, ...]


def as_items(poly: dict[int, int]) -> Items:
    return tuple(sorted(poly.items()))


def orbit_decomposition(poly: dict[int, int], step: int) -> OrbitDecomposition | None:
    seen: set[int] = set()
    out: list[tuple[tuple[int, ...], int]] = []
    for q_value, coefficient in sorted(poly.items()):
        if q_value in seen:
            continue
        orbit = tuple((q_value + index * step) % QUOTIENT_ORDER for index in range(3))
        values = [poly.get(item, 0) for item in orbit]
        if not all(value == coefficient and value != 0 for value in values):
            return None
        seen.update(orbit)
        out.append((tuple(sorted(orbit)), coefficient))
    if seen != set(poly):
        return None
    return tuple(out)


def length3_orbit_decompositions(poly: dict[int, int]) -> tuple[tuple[int, OrbitDecomposition], ...]:
    out: list[tuple[int, OrbitDecomposition]] = []
    for step in range(1, QUOTIENT_ORDER):
        decomp = orbit_decomposition(poly, step)
        if decomp is not None:
            out.append((step, decomp))
    return tuple(out)


def image_branch(name: str, chain: dict[int, int], direction_q: int) -> ImageOrbitBranch:
    image = inversion_boundary(boundary(chain, direction_q))
    decomps = length3_orbit_decompositions(image)
    s_decomp = signed_s_layer_decomposition(image)
    return ImageOrbitBranch(
        branch_name=name,
        direction_q=direction_q,
        direction_d=d_residue_from_q(direction_q),
        image_support=len(image),
        image_items=as_items(image),
        s_layer_decomposition=s_decomp,
        length3_orbit_steps_q=tuple(step for step, _decomp in decomps),
        length3_orbit_steps_d=tuple(d_residue_from_q(step) for step, _decomp in decomps),
        length3_orbit_decompositions=decomps,
        is_signed_s_layer=bool(s_decomp),
        is_bridge_image=image == bridge_coefficients(),
    )


def skew_image_orbit_profile() -> SkewImageOrbitProfile:
    active_by_key = {
        (row.orientation_mask, row.boundary_direction_q): row
        for row in coefficient_rigidity_profile().rows
    }
    rows: list[SkewImageOrbitRow] = []
    for selector_row in skew_derivative_selector_profile().rows:
        active = active_by_key[(selector_row.orientation_mask, selector_row.recorded_direction_q)]
        chain = dict(zip(active.q_values, active.recorded_coefficients))
        recorded = image_branch("recorded", chain, selector_row.recorded_direction_q)
        opposite = image_branch("opposite", chain, selector_row.opposite_direction_q)
        wrong_steps = tuple(
            step for step in opposite.length3_orbit_steps_q if step != S_STEP
        )
        rows.append(
            SkewImageOrbitRow(
                orientation_mask=selector_row.orientation_mask,
                recorded_direction_q=selector_row.recorded_direction_q,
                opposite_direction_q=selector_row.opposite_direction_q,
                recorded_branch=recorded,
                opposite_branch=opposite,
                recorded_unique_s_orbit=(
                    recorded.length3_orbit_steps_q == (S_STEP,)
                    and recorded.s_layer_decomposition == signed_s_layer_decomposition(bridge_coefficients())
                ),
                opposite_has_no_s_orbit=not opposite.is_signed_s_layer and S_STEP not in opposite.length3_orbit_steps_q,
                opposite_wrong_orbit_step_q=wrong_steps[0] if len(wrong_steps) == 1 else None,
            )
        )
    rows_tuple = tuple(rows)
    return SkewImageOrbitProfile(
        row_count=len(rows_tuple),
        bridge_decomposition=signed_s_layer_decomposition(bridge_coefficients()),
        all_recorded_branches_are_signed_s_layer=all(
            row.recorded_unique_s_orbit and row.recorded_branch.is_bridge_image
            for row in rows_tuple
        ),
        all_opposite_branches_have_no_s_layer=all(row.opposite_has_no_s_orbit for row in rows_tuple),
        opposite_support_values=tuple(sorted({row.opposite_branch.image_support for row in rows_tuple})),
        opposite_wrong_orbit_steps_q=tuple(
            sorted({step for row in rows_tuple if row.opposite_wrong_orbit_step_q is not None for step in (row.opposite_wrong_orbit_step_q,)})
        ),
        rows=rows_tuple,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner skew image-orbit gate")
    profile = skew_image_orbit_profile()
    bridge_decomp = (((25, 197, 369), 1), ((138, 310, 482), -1))
    bridge_items = ((25, 1), (138, -1), (197, 1), (310, -1), (369, 1), (482, -1))
    wrong6_items = ((172, -1), (197, -1), (222, -1), (285, 1), (310, 1), (335, 1))
    wrong6_decomp = (((172, 197, 222), -1), ((285, 310, 335), 1))
    wrong8_items = ((59, -1), (113, 1), (172, 1), (197, 1), (310, -1), (335, -1), (394, -1), (448, 1))
    expected_recorded_197 = ImageOrbitBranch("recorded", 197, 122, 6, bridge_items, bridge_decomp, (172,), (1,), ((172, bridge_decomp),), True, True)
    expected_recorded_310 = ImageOrbitBranch("recorded", 310, 385, 6, bridge_items, bridge_decomp, (172,), (1,), ((172, bridge_decomp),), True, True)
    expected_opp_310_wrong6 = ImageOrbitBranch("opposite", 310, 385, 6, wrong6_items, (), (25,), (121,), ((25, wrong6_decomp),), False, False)
    expected_opp_197_wrong6 = ImageOrbitBranch("opposite", 197, 122, 6, wrong6_items, (), (25,), (121,), ((25, wrong6_decomp),), False, False)
    expected_opp_197_wrong8 = ImageOrbitBranch("opposite", 197, 122, 8, wrong8_items, (), (), (), (), False, False)
    expected_opp_310_wrong8 = ImageOrbitBranch("opposite", 310, 385, 8, wrong8_items, (), (), (), (), False, False)
    expected_rows = (
        SkewImageOrbitRow(1, 197, 310, expected_recorded_197, expected_opp_310_wrong6, True, True, 25),
        SkewImageOrbitRow(1, 310, 197, expected_recorded_310, expected_opp_197_wrong8, True, True, None),
        SkewImageOrbitRow(6, 197, 310, expected_recorded_197, expected_opp_310_wrong8, True, True, None),
        SkewImageOrbitRow(6, 310, 197, expected_recorded_310, expected_opp_197_wrong6, True, True, 25),
    )
    row_ok = (
        profile.row_count == 4
        and profile.bridge_decomposition == bridge_decomp
        and profile.all_recorded_branches_are_signed_s_layer
        and profile.all_opposite_branches_have_no_s_layer
        and profile.opposite_support_values == (6, 8)
        and profile.opposite_wrong_orbit_steps_q == (25,)
        and profile.rows == expected_rows
    )

    print(
        "corner_skew_image_orbit_summary: "
        f"recorded_steps={tuple(row.recorded_branch.length3_orbit_steps_q for row in profile.rows)} "
        f"opposite_supports={tuple(row.opposite_branch.image_support for row in profile.rows)} "
        f"opposite_steps={tuple(row.opposite_branch.length3_orbit_steps_q for row in profile.rows)}"
    )
    print("corner_skew_image_orbit_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("image_orbit_laws")
    print("  recorded short skew derivative image is the unique signed S=172 layer")
    print("  support-six opposite branches are signed pairs of wrong q=25 orbits")
    print("  the other opposite branches expand to support eight and have no length-three orbit decomposition")
    print("interpretation")
    print("  producer_must_land_on_the_S_orbit_image_after_the_oriented_skew_derivative=1")
    print("  opposite_short_skew_derivative_has_wrong_orbit_geometry=1")
    print("  short_residual_lengths_do_not_certify_the_Hilbert90_image=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_skew_image_orbit_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_image_orbit_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
