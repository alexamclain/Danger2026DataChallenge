#!/usr/bin/env python3
"""Odd Frobenius half-orbit form of the p25 GK projector.

The Frobenius-projector gate uses DC-ALT.  This equivalent gate rewrites the
same finite object in a more arithmetic-facing form: average the odd powers in
the p^2 Frobenius orbit, then impose the Lucas/no-borrow selected support.

For a carry signature c_i, define

    even_avg = (sum c_{2j}) / (ord_N(p)/2)
    odd_avg  = (sum c_{2j+1}) / (ord_N(p)/2).

On the selected seed, odd_avg is exactly the anomaly projector.  Without the
selected support it leaks onto the two non-selected top-row cells, so a real
HD/GK/Barnes producer must realize the odd half-orbit phase together with the
Lucas selector, not the half-orbit average alone.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import (
    ANOMALY_CELL,
    selected,
    translated_anomaly_terms,
)
from p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate import (
    MODULI,
    P,
    carry_signature,
    multiplicative_order,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class HalfOrbitCell:
    h_value: int
    t_value: int
    selected: bool
    anomaly: bool
    quotient_even_sum: int
    quotient_odd_sum: int
    quotient_even_avg: int
    quotient_odd_avg: int
    raw_even_sum: int
    raw_odd_sum: int
    raw_even_avg: int
    raw_odd_avg: int
    selected_odd_projector: int
    expected_projector: int


@dataclass(frozen=True)
class HalfOrbitProfile:
    p_moduli: tuple[tuple[int, int, int, int, int], ...]
    cells: tuple[HalfOrbitCell, ...]
    odd_avg_support: tuple[tuple[int, int], ...]
    even_avg_support: tuple[tuple[int, int], ...]
    selected_odd_support: tuple[tuple[int, int], ...]
    selected_even_support: tuple[tuple[int, int], ...]
    odd_half_orbit_leaks_without_lucas_selector: bool
    selected_odd_is_exact_projector: bool
    raw_and_quotient_averages_match: bool
    projected_anomaly_terms: tuple[int, ...]


def split_sums(signature: tuple[int, ...]) -> tuple[int, int]:
    even_sum = sum(value for index, value in enumerate(signature) if index % 2 == 0)
    odd_sum = sum(value for index, value in enumerate(signature) if index % 2 == 1)
    return even_sum, odd_sum


def average(sum_value: int, denominator: int) -> int:
    if sum_value % denominator != 0:
        raise AssertionError(f"nonintegral half-orbit average {sum_value}/{denominator}")
    return sum_value // denominator


def seed_term(h_value: int, t_value: int) -> int:
    return (X_STEP * (h_value + 1) + Y_STEP * t_value) % QUOTIENT_ORDER


def half_orbit_profile() -> HalfOrbitProfile:
    p_moduli = tuple(
        (
            modulus,
            P % modulus,
            multiplicative_order(P, modulus),
            multiplicative_order((P * P) % modulus, modulus),
            pow(P, multiplicative_order(P, modulus) // 2, modulus),
        )
        for modulus in MODULI
    )
    cells: list[HalfOrbitCell] = []
    odd_support: list[tuple[int, int]] = []
    even_support: list[tuple[int, int]] = []
    selected_odd_support: list[tuple[int, int]] = []
    selected_even_support: list[tuple[int, int]] = []
    projected_terms: list[int] = []

    for h_value in range(3):
        for t_value in range(3):
            is_selected = selected(h_value, t_value)
            is_anomaly = (h_value, t_value) == ANOMALY_CELL
            quotient_signature = carry_signature(507, h_value, t_value)
            raw_signature = carry_signature(12675, h_value, t_value)
            quotient_half = len(quotient_signature) // 2
            raw_half = len(raw_signature) // 2
            quotient_even_sum, quotient_odd_sum = split_sums(quotient_signature)
            raw_even_sum, raw_odd_sum = split_sums(raw_signature)
            quotient_even_avg = average(quotient_even_sum, quotient_half)
            quotient_odd_avg = average(quotient_odd_sum, quotient_half)
            raw_even_avg = average(raw_even_sum, raw_half)
            raw_odd_avg = average(raw_odd_sum, raw_half)
            selected_odd = int(is_selected) * quotient_odd_avg
            selected_even = int(is_selected) * quotient_even_avg
            expected = int(is_anomaly)

            if quotient_odd_avg:
                odd_support.append((h_value, t_value))
            if quotient_even_avg:
                even_support.append((h_value, t_value))
            if selected_odd:
                selected_odd_support.append((h_value, t_value))
                projected_terms.extend(
                    (seed_term(h_value, t_value) + layer * S_STEP) % QUOTIENT_ORDER
                    for layer in range(3)
                )
            if selected_even:
                selected_even_support.append((h_value, t_value))

            cells.append(
                HalfOrbitCell(
                    h_value=h_value,
                    t_value=t_value,
                    selected=is_selected,
                    anomaly=is_anomaly,
                    quotient_even_sum=quotient_even_sum,
                    quotient_odd_sum=quotient_odd_sum,
                    quotient_even_avg=quotient_even_avg,
                    quotient_odd_avg=quotient_odd_avg,
                    raw_even_sum=raw_even_sum,
                    raw_odd_sum=raw_odd_sum,
                    raw_even_avg=raw_even_avg,
                    raw_odd_avg=raw_odd_avg,
                    selected_odd_projector=selected_odd,
                    expected_projector=expected,
                )
            )

    cells_tuple = tuple(cells)
    return HalfOrbitProfile(
        p_moduli=p_moduli,
        cells=cells_tuple,
        odd_avg_support=tuple(odd_support),
        even_avg_support=tuple(even_support),
        selected_odd_support=tuple(selected_odd_support),
        selected_even_support=tuple(selected_even_support),
        odd_half_orbit_leaks_without_lucas_selector=tuple(odd_support)
        == ((0, 1), (0, 2), ANOMALY_CELL),
        selected_odd_is_exact_projector=all(
            cell.selected_odd_projector == cell.expected_projector for cell in cells_tuple
        ),
        raw_and_quotient_averages_match=all(
            cell.raw_even_avg == cell.quotient_even_avg
            and cell.raw_odd_avg == cell.quotient_odd_avg
            for cell in cells_tuple
        ),
        projected_anomaly_terms=tuple(sorted(projected_terms)),
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz half-orbit gate")
    profile = half_orbit_profile()
    row_ok = (
        profile.p_moduli
        == (
            (507, 218, 78, 39, 506),
            (12675, 5288, 780, 390, 7099),
        )
        and profile.odd_avg_support == ((0, 1), (0, 2), (2, 1))
        and profile.even_avg_support == ((0, 1), (0, 2), (1, 2))
        and profile.selected_odd_support == (ANOMALY_CELL,)
        and profile.selected_even_support == ()
        and profile.odd_half_orbit_leaks_without_lucas_selector
        and profile.selected_odd_is_exact_projector
        and profile.raw_and_quotient_averages_match
        and profile.projected_anomaly_terms == tuple(translated_anomaly_terms())
    )

    print(f"half_orbit_profile={profile}")
    print("half_orbit_cells")
    for cell in profile.cells:
        print(
            f"  h={cell.h_value} t={cell.t_value}: "
            f"selected={int(cell.selected)} anomaly={int(cell.anomaly)} "
            f"q_even_sum={cell.quotient_even_sum} q_odd_sum={cell.quotient_odd_sum} "
            f"q_even_avg={cell.quotient_even_avg} q_odd_avg={cell.quotient_odd_avg} "
            f"selected_odd_projector={cell.selected_odd_projector}"
        )
    print("half_orbit_laws")
    print("  odd Frobenius p^2-suborbit average is the arithmetic-facing projector source")
    print("  odd average alone leaks to non-selected top-row cells")
    print("  Lucas/no-borrow selected support times odd average isolates the anomaly")
    print("interpretation")
    print("  gk_projector_can_be_written_as_selected_odd_frobenius_half_orbit_average=1")
    print("  hd_gk_unit_phase_candidate_must_couple_half_orbit_with_lucas_selector=1")
    print(f"square_axis_gross_koblitz_half_orbit_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_half_orbit_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
