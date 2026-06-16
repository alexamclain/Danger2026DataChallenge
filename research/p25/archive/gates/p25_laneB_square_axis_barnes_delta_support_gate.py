#!/usr/bin/env python3
"""Support-only Barnes/Greene delta screen for the p25 GK anomaly.

The targeted literature search found a plausible finite Barnes correction:
Helversen-Pasotto supplies a product delta, while Greene/FLRST supply related
endpoint/point deltas.  Before doing any Gauss-sum evaluation, this gate tests
what kind of exponent predicate can have the required finite support.

The target is the half-orbit interaction projector

    O * (1 - E) = indicator((h,t) = (2,1)).

Results checked here:

* A single order-3 affine product delta through the anomaly is too broad: it
  always fires on a three-cell line.
* A full `C_507` seed-exponent point delta, `q = 138`, fires exactly at
  `(2,1)` and its outer `S`-image is exactly `{138,310,482}`.
* The full `p^2` orbit closure of that point delta is much too large on the
  quotient (`117` classes after the `S` layer), so a successful Barnes/Greene
  identity must supply a local product/point delta, not a plain orbit-closed
  projector.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import ANOMALY_CELL
from p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate import (
    interaction_profile,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate import P
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


CELL_COORDS = tuple((h_value, t_value) for h_value in range(3) for t_value in range(3))


@dataclass(frozen=True)
class LineDelta:
    a_h: int
    b_t: int
    c_const: int
    support: tuple[tuple[int, int], ...]
    extra_cells: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class BarnesDeltaSupportProfile:
    target_support: tuple[tuple[int, int], ...]
    order3_target_line_count: int
    order3_unique_target_lines: tuple[tuple[tuple[int, int], ...], ...]
    order3_min_extra_cells: int
    order3_exact_target_lines: int
    full_seed_delta_support: tuple[tuple[int, int], ...]
    full_seed_delta_outer_s_image: tuple[int, ...]
    full_seed_delta_matches_target: bool
    p2_multiplier_mod_507: int
    p2_orbit_length: int
    p2_orbit_seed_hits: tuple[int, ...]
    p2_orbit_outer_s_support_count: int
    p2_orbit_outer_s_matches_target: bool
    hp_order3_only_killed: bool
    hp_full_seed_delta_support_live: bool
    orbit_closed_delta_killed: bool


def seed_q(h_value: int, t_value: int) -> int:
    return (X_STEP * (h_value + 1) + Y_STEP * t_value) % QUOTIENT_ORDER


def outer_s_image(cells: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            (seed_q(h_value, t_value) + layer * S_STEP) % QUOTIENT_ORDER
            for h_value, t_value in cells
            for layer in range(3)
        )
    )


def order3_target_lines() -> tuple[LineDelta, ...]:
    rows: list[LineDelta] = []
    for a_h, b_t in product(range(3), repeat=2):
        if a_h == 0 and b_t == 0:
            continue
        c_const = (-(a_h * ANOMALY_CELL[0] + b_t * ANOMALY_CELL[1])) % 3
        support = tuple(
            coord
            for coord in CELL_COORDS
            if (a_h * coord[0] + b_t * coord[1] + c_const) % 3 == 0
        )
        rows.append(
            LineDelta(
                a_h=a_h,
                b_t=b_t,
                c_const=c_const,
                support=support,
                extra_cells=tuple(coord for coord in support if coord != ANOMALY_CELL),
            )
        )
    return tuple(rows)


def p2_orbit(start: int) -> tuple[int, ...]:
    multiplier = (P * P) % QUOTIENT_ORDER
    values: list[int] = []
    current = start % QUOTIENT_ORDER
    while current not in values:
        values.append(current)
        current = (current * multiplier) % QUOTIENT_ORDER
    return tuple(values)


def barnes_delta_support_profile() -> BarnesDeltaSupportProfile:
    interaction = interaction_profile()
    target_support = tuple(
        (cell.h_value, cell.t_value)
        for cell in interaction.cells
        if cell.interaction_projector
    )
    lines = order3_target_lines()
    unique_lines = tuple(sorted({line.support for line in lines}))
    exact_lines = tuple(line for line in lines if line.support == target_support)
    min_extra = min(len(line.extra_cells) for line in lines)

    anomaly_q = seed_q(*ANOMALY_CELL)
    full_seed_support = tuple(coord for coord in CELL_COORDS if seed_q(*coord) == anomaly_q)
    full_seed_outer = outer_s_image(full_seed_support)

    orbit = p2_orbit(anomaly_q)
    orbit_set = set(orbit)
    seed_hits = tuple(sorted(seed_q(*coord) for coord in CELL_COORDS if seed_q(*coord) in orbit_set))
    orbit_outer_support = {
        (q_value + layer * S_STEP) % QUOTIENT_ORDER
        for q_value in orbit
        for layer in range(3)
    }
    target_outer = tuple((anomaly_q + layer * S_STEP) % QUOTIENT_ORDER for layer in range(3))
    target_outer_sorted = tuple(sorted(target_outer))

    return BarnesDeltaSupportProfile(
        target_support=target_support,
        order3_target_line_count=len(lines),
        order3_unique_target_lines=unique_lines,
        order3_min_extra_cells=min_extra,
        order3_exact_target_lines=len(exact_lines),
        full_seed_delta_support=full_seed_support,
        full_seed_delta_outer_s_image=full_seed_outer,
        full_seed_delta_matches_target=(
            full_seed_support == target_support
            and full_seed_outer == target_outer_sorted
        ),
        p2_multiplier_mod_507=(P * P) % QUOTIENT_ORDER,
        p2_orbit_length=len(orbit),
        p2_orbit_seed_hits=seed_hits,
        p2_orbit_outer_s_support_count=len(orbit_outer_support),
        p2_orbit_outer_s_matches_target=tuple(sorted(orbit_outer_support)) == target_outer_sorted,
        hp_order3_only_killed=(len(exact_lines) == 0 and min_extra == 2),
        hp_full_seed_delta_support_live=(
            full_seed_support == target_support
            and full_seed_outer == target_outer_sorted
        ),
        orbit_closed_delta_killed=len(orbit_outer_support) != len(target_outer_sorted),
    )


def main() -> int:
    print("p25 Lane B square-axis Barnes/Greene delta support gate")
    profile = barnes_delta_support_profile()
    row_ok = (
        profile.target_support == (ANOMALY_CELL,)
        and profile.order3_target_line_count == 8
        and len(profile.order3_unique_target_lines) == 4
        and profile.order3_min_extra_cells == 2
        and profile.order3_exact_target_lines == 0
        and profile.full_seed_delta_support == (ANOMALY_CELL,)
        and profile.full_seed_delta_outer_s_image == (138, 310, 482)
        and profile.full_seed_delta_matches_target
        and profile.p2_multiplier_mod_507 == 373
        and profile.p2_orbit_length == 39
        and profile.p2_orbit_seed_hits == (138,)
        and profile.p2_orbit_outer_s_support_count == 117
        and not profile.p2_orbit_outer_s_matches_target
        and profile.hp_order3_only_killed
        and profile.hp_full_seed_delta_support_live
        and profile.orbit_closed_delta_killed
    )

    print(f"barnes_delta_support_profile={profile}")
    print("order3_target_lines")
    for support in profile.order3_unique_target_lines:
        print(f"  support={support}")
    print("delta_laws")
    print("  order3_HP_product_delta_is_line_support_not_point_support=1")
    print("  full_C507_seed_exponent_delta_q_138_is_support_viable=1")
    print("  p2_orbit_closed_delta_is_too_large_on_the_quotient=1")
    print("interpretation")
    print("  kill_HP_only_if_it_only_sees_order3_product_parameters=1")
    print("  continue_Barnes_or_Greene_if_it_realizes_the_full_seed_point_delta=1")
    print("  do_not_evaluate_Gauss_sums_before_this_support_screen=1")
    print(f"square_axis_barnes_delta_support_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_barnes_delta_support_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
