#!/usr/bin/env python3
"""Even/odd half-orbit interaction for the p25 GK projector.

The half-orbit gate says the odd p^2 suborbit average leaks onto two
non-selected top-row cells.  This gate checks a sharper finite identity: the
even half-orbit average marks exactly those leaks, so the anomaly projector is

    odd_avg * (1 - even_avg).

Thus the Lucas/no-borrow selector can be replaced, on this seed, by an
interaction between the two GK half-orbit averages.  This is a better
arithmetic target for an HD/GK/Barnes identity than "odd half-orbit plus an
external selector": a producer should realize a coupled even/odd half-orbit
delta.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import (
    ANOMALY_CELL,
    selected,
    translated_anomaly_terms,
)
from p25_laneB_square_axis_gross_koblitz_half_orbit_gate import half_orbit_profile
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class InteractionCell:
    h_value: int
    t_value: int
    selected: bool
    anomaly: bool
    even_avg: int
    odd_avg: int
    interaction_projector: int
    selected_odd_projector: int
    expected_projector: int
    corrected_payload_value: int | None


@dataclass(frozen=True)
class HalfOrbitInteractionProfile:
    cells: tuple[InteractionCell, ...]
    odd_support: tuple[tuple[int, int], ...]
    even_support: tuple[tuple[int, int], ...]
    interaction_support: tuple[tuple[int, int], ...]
    even_marks_odd_leaks: bool
    interaction_equals_selected_odd: bool
    interaction_is_exact_anomaly: bool
    corrected_selected_payload: tuple[tuple[int, int, int], ...]
    corrected_payload_is_all_one_seed: bool
    projected_anomaly_terms: tuple[int, ...]


def seed_term(h_value: int, t_value: int) -> int:
    return (X_STEP * (h_value + 1) + Y_STEP * t_value) % QUOTIENT_ORDER


def interaction_profile() -> HalfOrbitInteractionProfile:
    half = half_orbit_profile()
    cells: list[InteractionCell] = []
    odd_support: list[tuple[int, int]] = []
    even_support: list[tuple[int, int]] = []
    interaction_support: list[tuple[int, int]] = []
    corrected_payload: list[tuple[int, int, int]] = []
    projected_terms: list[int] = []

    for cell in half.cells:
        coord = (cell.h_value, cell.t_value)
        even_avg = cell.quotient_even_avg
        odd_avg = cell.quotient_odd_avg
        interaction = odd_avg * (1 - even_avg)
        expected = int(cell.anomaly)
        corrected_value: int | None = None
        if odd_avg:
            odd_support.append(coord)
        if even_avg:
            even_support.append(coord)
        if interaction:
            interaction_support.append(coord)
            projected_terms.extend(
                (seed_term(cell.h_value, cell.t_value) + layer * S_STEP) % QUOTIENT_ORDER
                for layer in range(3)
            )
        if cell.selected:
            corrected_value = comb(cell.h_value, cell.t_value) - interaction
            corrected_payload.append((cell.h_value, cell.t_value, corrected_value))
        cells.append(
            InteractionCell(
                h_value=cell.h_value,
                t_value=cell.t_value,
                selected=cell.selected,
                anomaly=cell.anomaly,
                even_avg=even_avg,
                odd_avg=odd_avg,
                interaction_projector=interaction,
                selected_odd_projector=cell.selected_odd_projector,
                expected_projector=expected,
                corrected_payload_value=corrected_value,
            )
        )

    odd_leaks = tuple(coord for coord in odd_support if coord != ANOMALY_CELL)
    return HalfOrbitInteractionProfile(
        cells=tuple(cells),
        odd_support=tuple(odd_support),
        even_support=tuple(even_support),
        interaction_support=tuple(interaction_support),
        even_marks_odd_leaks=all(coord in even_support for coord in odd_leaks)
        and ANOMALY_CELL not in even_support,
        interaction_equals_selected_odd=all(
            cell.interaction_projector == cell.selected_odd_projector for cell in cells
        ),
        interaction_is_exact_anomaly=all(
            cell.interaction_projector == cell.expected_projector for cell in cells
        ),
        corrected_selected_payload=tuple(corrected_payload),
        corrected_payload_is_all_one_seed=all(
            value == 1 for _h, _t, value in corrected_payload
        ),
        projected_anomaly_terms=tuple(sorted(projected_terms)),
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz half-orbit interaction gate")
    profile = interaction_profile()
    row_ok = (
        profile.odd_support == ((0, 1), (0, 2), (2, 1))
        and profile.even_support == ((0, 1), (0, 2), (1, 2))
        and profile.interaction_support == (ANOMALY_CELL,)
        and profile.even_marks_odd_leaks
        and profile.interaction_equals_selected_odd
        and profile.interaction_is_exact_anomaly
        and profile.corrected_selected_payload
        == (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 0, 1),
            (2, 1, 1),
            (2, 2, 1),
        )
        and profile.corrected_payload_is_all_one_seed
        and profile.projected_anomaly_terms == tuple(translated_anomaly_terms())
    )

    print(f"half_orbit_interaction_profile={profile}")
    print("interaction_cells")
    for cell in profile.cells:
        print(
            f"  h={cell.h_value} t={cell.t_value}: "
            f"selected={int(cell.selected)} anomaly={int(cell.anomaly)} "
            f"even_avg={cell.even_avg} odd_avg={cell.odd_avg} "
            f"interaction={cell.interaction_projector}"
        )
    print("interaction_laws")
    print("  odd_avg leaks to (0,1),(0,2),(2,1)")
    print("  even_avg marks the two odd leaks and misses the anomaly")
    print("  odd_avg*(1-even_avg) is the anomaly projector")
    print("interpretation")
    print("  gk_projector_can_be_written_as_even_odd_half_orbit_interaction=1")
    print("  hd_gk_barnes_candidate_should_realize_a_coupled_half_orbit_delta=1")
    print(f"square_axis_gross_koblitz_half_orbit_interaction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
