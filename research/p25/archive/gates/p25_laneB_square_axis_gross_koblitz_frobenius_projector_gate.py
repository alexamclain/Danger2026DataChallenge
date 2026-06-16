#!/usr/bin/env python3
"""Frobenius-frequency projector from the p25 multi-digit GK signature.

The multi-digit Gross-Koblitz/Stickelberger signature found the right
valuation-positive mask, but support alone is not a producer.  This gate checks
one sharper finite artifact: the p-orbit carry signature has a quadratic
Frobenius-frequency component that isolates the selected q-binomial anomaly
once the Lucas/no-borrow support is imposed.

For N=507 and N=12675, define

    C(h,t)      = sum_i carry_i(h,t)
    A(h,t)      = sum_i (-1)^i carry_i(h,t)
    projector   = selected(h,t) * (C(h,t) - A(h,t)) / ord_N(p).

The alternating character is the p^39=-1 eigensign on the C_507 quotient
orbit.  The projector is exactly 1 at (h,t)=(2,1) and 0 on every other seed
cell.  After the outer S-layer, this is precisely the anomaly orbit
S*X^3Y = {138,310,482}.  Subtracting the projector from the honest
Lucas/binomial coefficients `[1,1,1,1,2,1]` gives the all-one seed payload.

This is still not a certificate: it is a finite projector that a real
Hasse-Davenport/Gross-Koblitz/Barnes unit phase would have to realize.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

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


FIELD = 2029


@dataclass(frozen=True)
class ProjectorCell:
    h_value: int
    t_value: int
    selected: bool
    anomaly: bool
    quotient_dc: int
    quotient_alt: int
    raw_dc: int
    raw_alt: int
    quotient_projector: int
    raw_projector: int
    expected_projector: int


@dataclass(frozen=True)
class FrobeniusProjectorProfile:
    p_moduli: tuple[tuple[int, int, int, bool], ...]
    cells: tuple[ProjectorCell, ...]
    quotient_projector_support: tuple[tuple[int, int], ...]
    raw_projector_support: tuple[tuple[int, int], ...]
    selected_projector_exact: bool
    raw_matches_quotient_projector: bool
    anomaly_terms: tuple[int, ...]
    projected_anomaly_terms: tuple[int, ...]
    corrected_selected_payload: tuple[tuple[int, int, int], ...]
    projector_equals_lucas_coefficient_anomaly: bool
    corrected_payload_is_all_one_seed: bool
    corrected_payload_terms: tuple[int, ...]
    quotient_frequency_pairs: tuple[tuple[tuple[int, int], int, int], ...]


def alternating_sum(values: tuple[int, ...]) -> int:
    return sum(value if index % 2 == 0 else -value for index, value in enumerate(values))


def projector_value(signature: tuple[int, ...], is_selected: bool) -> int:
    if not is_selected:
        return 0
    order = len(signature)
    numerator = sum(signature) - alternating_sum(signature)
    if numerator % order != 0:
        raise AssertionError(f"nonintegral projector numerator {numerator} for order {order}")
    return numerator // order


def seed_term(h_value: int, t_value: int) -> int:
    return (X_STEP * (h_value + 1) + Y_STEP * t_value) % QUOTIENT_ORDER


def frobenius_projector_profile() -> FrobeniusProjectorProfile:
    p_moduli = tuple(
        (
            modulus,
            P % modulus,
            multiplicative_order(P, modulus),
            pow(P, multiplicative_order(P, modulus) // 2, modulus) == modulus - 1,
        )
        for modulus in MODULI
    )
    cells: list[ProjectorCell] = []
    quotient_support: list[tuple[int, int]] = []
    raw_support: list[tuple[int, int]] = []
    frequency_pairs: list[tuple[tuple[int, int], int, int]] = []
    projected_terms: list[int] = []
    corrected_payload: list[tuple[int, int, int]] = []
    corrected_terms: list[int] = []
    for h_value in range(3):
        for t_value in range(3):
            is_selected = selected(h_value, t_value)
            is_anomaly = (h_value, t_value) == ANOMALY_CELL
            quotient_signature = carry_signature(507, h_value, t_value)
            raw_signature = carry_signature(12675, h_value, t_value)
            quotient_dc = sum(quotient_signature)
            quotient_alt = alternating_sum(quotient_signature)
            raw_dc = sum(raw_signature)
            raw_alt = alternating_sum(raw_signature)
            quotient_projector = projector_value(quotient_signature, is_selected)
            raw_projector = projector_value(raw_signature, is_selected)
            expected = int(is_anomaly)
            if quotient_projector:
                quotient_support.append((h_value, t_value))
                projected_terms.extend(
                    (seed_term(h_value, t_value) + layer * S_STEP) % QUOTIENT_ORDER
                    for layer in range(3)
                )
            if raw_projector:
                raw_support.append((h_value, t_value))
            if is_selected:
                corrected_value = comb(h_value, t_value) - quotient_projector
                corrected_payload.append((h_value, t_value, corrected_value))
                if corrected_value:
                    corrected_terms.extend(
                        (seed_term(h_value, t_value) + layer * S_STEP) % QUOTIENT_ORDER
                        for layer in range(3)
                    )
            frequency_pairs.append(((h_value, t_value), quotient_dc, quotient_alt))
            cells.append(
                ProjectorCell(
                    h_value=h_value,
                    t_value=t_value,
                    selected=is_selected,
                    anomaly=is_anomaly,
                    quotient_dc=quotient_dc,
                    quotient_alt=quotient_alt,
                    raw_dc=raw_dc,
                    raw_alt=raw_alt,
                    quotient_projector=quotient_projector,
                    raw_projector=raw_projector,
                    expected_projector=expected,
                )
            )
    cells_tuple = tuple(cells)
    return FrobeniusProjectorProfile(
        p_moduli=p_moduli,
        cells=cells_tuple,
        quotient_projector_support=tuple(quotient_support),
        raw_projector_support=tuple(raw_support),
        selected_projector_exact=all(
            cell.quotient_projector == cell.expected_projector
            and cell.raw_projector == cell.expected_projector
            for cell in cells_tuple
        ),
        raw_matches_quotient_projector=all(
            cell.raw_projector == cell.quotient_projector for cell in cells_tuple
        ),
        anomaly_terms=tuple(translated_anomaly_terms()),
        projected_anomaly_terms=tuple(sorted(projected_terms)),
        corrected_selected_payload=tuple(corrected_payload),
        projector_equals_lucas_coefficient_anomaly=all(
            (comb(cell.h_value, cell.t_value) - 1 if cell.selected else 0)
            == cell.quotient_projector
            for cell in cells_tuple
        ),
        corrected_payload_is_all_one_seed=all(
            value == 1 for _h_value, _t_value, value in corrected_payload
        ),
        corrected_payload_terms=tuple(sorted(corrected_terms)),
        quotient_frequency_pairs=tuple(frequency_pairs),
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz Frobenius projector gate")
    profile = frobenius_projector_profile()
    expected_frequency_pairs = (
        ((0, 0), 0, 0),
        ((0, 1), 78, 0),
        ((0, 2), 78, 0),
        ((1, 0), 0, 0),
        ((1, 1), 0, 0),
        ((1, 2), 39, 39),
        ((2, 0), 0, 0),
        ((2, 1), 39, -39),
        ((2, 2), 0, 0),
    )
    row_ok = (
        profile.p_moduli == ((507, 218, 78, True), (12675, 5288, 780, False))
        and profile.quotient_projector_support == (ANOMALY_CELL,)
        and profile.raw_projector_support == (ANOMALY_CELL,)
        and profile.selected_projector_exact
        and profile.raw_matches_quotient_projector
        and profile.anomaly_terms == (138, 310, 482)
        and profile.projected_anomaly_terms == profile.anomaly_terms
        and profile.corrected_selected_payload
        == (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 0, 1),
            (2, 1, 1),
            (2, 2, 1),
        )
        and profile.projector_equals_lucas_coefficient_anomaly
        and profile.corrected_payload_is_all_one_seed
        and profile.corrected_payload_terms
        == tuple(
            sorted(
                (seed_term(h_value, t_value) + layer * S_STEP) % QUOTIENT_ORDER
                for h_value in range(3)
                for t_value in range(h_value + 1)
                for layer in range(3)
            )
        )
        and profile.quotient_frequency_pairs == expected_frequency_pairs
    )

    print(f"frobenius_projector_profile={profile}")
    print("projector_cells")
    for cell in profile.cells:
        print(
            f"  h={cell.h_value} t={cell.t_value}: "
            f"selected={int(cell.selected)} anomaly={int(cell.anomaly)} "
            f"quotient_dc={cell.quotient_dc} quotient_alt={cell.quotient_alt} "
            f"raw_dc={cell.raw_dc} raw_alt={cell.raw_alt} "
            f"quotient_projector={cell.quotient_projector} "
            f"raw_projector={cell.raw_projector}"
        )
    print("projector_laws")
    print("  quotient p^39 acts as -1, giving the alternating Frobenius character")
    print("  selected*(DC-ALT)/orbit_length is the anomaly indicator")
    print("  applying the outer S layer gives exactly S*X^3Y = 138,310,482")
    print("  binom(h,t) - projector is the all-one selected seed payload")
    print("interpretation")
    print("  cyclic_gk_signature_contains_a_quadratic_frobenius_projector_for_the_anomaly=1")
    print("  frobenius_projector_flattens_the_lucas_coefficient_anomaly=1")
    print("  projector_still_requires_a_real_HD_or_GK_unit_phase_to_be_a_producer=1")
    print(f"square_axis_gross_koblitz_frobenius_projector_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
