#!/usr/bin/env python3
"""Multi-digit Gross-Koblitz/Stickelberger signature for the p25 anomaly.

The one-digit carry-twist gate kills a strict local F_3 carry story.  This
gate checks the next layer suggested by the literature search: the full
Frobenius orbit of the Stickelberger carry for an order-3 lift inside
N=507 and N=12675.

For the seed cell (h,t), use the order-3 product exponents

    A = t * N/3
    B = (h - t mod 3) * N/3.

The cyclic Gross-Koblitz valuation signature is the carry sequence

    floor(((p^i A mod N) + (p^i B mod N)) / N),  i=0..ord_N(p)-1.

This multi-digit signature is positive exactly on the desired valuation mask:
the q-binomial anomaly (h,t)=(2,1) and the non-selected cells.  It is zero on
all selected non-anomaly cells.  That is a positive Jacobi-side clue, but only
at the valuation/signature level; it does not supply the unit phase or the
all-one finite payload.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import (
    ANOMALY_CELL,
    selected,
    translated_anomaly_terms,
)


P = 10**25 + 13
MODULI = (507, 12675)


@dataclass(frozen=True)
class CellSignature:
    h_value: int
    t_value: int
    selected: bool
    anomaly: bool
    quotient_sum: int
    raw_sum: int
    quotient_prefix: tuple[int, ...]
    raw_prefix: tuple[int, ...]
    positive_matches_target: bool


@dataclass(frozen=True)
class MultidigitSignatureProfile:
    p_moduli: tuple[tuple[int, int, int], ...]
    anomaly_terms: tuple[int, ...]
    cell_signatures: tuple[CellSignature, ...]
    quotient_positive_cells: tuple[tuple[int, int], ...]
    raw_positive_cells: tuple[tuple[int, int], ...]
    selected_non_anomaly_zero: bool
    anomaly_positive: bool
    outside_positive: bool
    raw_sums_are_ten_times_quotient_sums: bool
    exact_positive_mask: bool


def multiplicative_order(value: int, modulus: int) -> int:
    value %= modulus
    if value == 0:
        raise ValueError("zero has no multiplicative order")
    current = value
    order = 1
    while current != 1:
        current = (current * value) % modulus
        order += 1
        if order > modulus:
            raise AssertionError(f"failed to find order of {value} modulo {modulus}")
    return order


def carry_signature(modulus: int, h_value: int, t_value: int) -> tuple[int, ...]:
    scale = modulus // 3
    a_value = (t_value * scale) % modulus
    b_value = (((h_value - t_value) % 3) * scale) % modulus
    orbit_length = multiplicative_order(P, modulus)
    multiplier = 1
    carries: list[int] = []
    for _index in range(orbit_length):
        a_i = (multiplier * a_value) % modulus
        b_i = (multiplier * b_value) % modulus
        carries.append((a_i + b_i) // modulus)
        multiplier = (multiplier * P) % modulus
    return tuple(carries)


def target_positive(h_value: int, t_value: int) -> bool:
    return (h_value, t_value) == ANOMALY_CELL or not selected(h_value, t_value)


def multidigit_signature_profile() -> MultidigitSignatureProfile:
    p_moduli = tuple((modulus, P % modulus, multiplicative_order(P, modulus)) for modulus in MODULI)
    rows: list[CellSignature] = []
    quotient_positive: list[tuple[int, int]] = []
    raw_positive: list[tuple[int, int]] = []
    for h_value in range(3):
        for t_value in range(3):
            quotient_signature = carry_signature(507, h_value, t_value)
            raw_signature = carry_signature(12675, h_value, t_value)
            quotient_sum = sum(quotient_signature)
            raw_sum = sum(raw_signature)
            if quotient_sum:
                quotient_positive.append((h_value, t_value))
            if raw_sum:
                raw_positive.append((h_value, t_value))
            rows.append(
                CellSignature(
                    h_value=h_value,
                    t_value=t_value,
                    selected=selected(h_value, t_value),
                    anomaly=(h_value, t_value) == ANOMALY_CELL,
                    quotient_sum=quotient_sum,
                    raw_sum=raw_sum,
                    quotient_prefix=quotient_signature[:12],
                    raw_prefix=raw_signature[:12],
                    positive_matches_target=(quotient_sum > 0) == target_positive(h_value, t_value)
                    and (raw_sum > 0) == target_positive(h_value, t_value),
                )
            )
    cells = tuple(rows)
    return MultidigitSignatureProfile(
        p_moduli=p_moduli,
        anomaly_terms=tuple(translated_anomaly_terms()),
        cell_signatures=cells,
        quotient_positive_cells=tuple(quotient_positive),
        raw_positive_cells=tuple(raw_positive),
        selected_non_anomaly_zero=all(
            row.quotient_sum == 0 and row.raw_sum == 0
            for row in cells
            if row.selected and not row.anomaly
        ),
        anomaly_positive=all(
            row.quotient_sum > 0 and row.raw_sum > 0
            for row in cells
            if row.anomaly
        ),
        outside_positive=all(
            row.quotient_sum > 0 and row.raw_sum > 0
            for row in cells
            if not row.selected
        ),
        raw_sums_are_ten_times_quotient_sums=all(
            row.raw_sum == 10 * row.quotient_sum for row in cells
        ),
        exact_positive_mask=all(row.positive_matches_target for row in cells),
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz multi-digit signature gate")
    profile = multidigit_signature_profile()
    expected_positive_cells = ((0, 1), (0, 2), (1, 2), (2, 1))
    row_ok = (
        profile.p_moduli == ((507, 218, 78), (12675, 5288, 780))
        and profile.anomaly_terms == (138, 310, 482)
        and profile.quotient_positive_cells == expected_positive_cells
        and profile.raw_positive_cells == expected_positive_cells
        and profile.selected_non_anomaly_zero
        and profile.anomaly_positive
        and profile.outside_positive
        and profile.raw_sums_are_ten_times_quotient_sums
        and profile.exact_positive_mask
    )

    print(f"multidigit_signature_profile={profile}")
    print("cell_signatures")
    for row in profile.cell_signatures:
        print(
            f"  h={row.h_value} t={row.t_value}: "
            f"selected={int(row.selected)} anomaly={int(row.anomaly)} "
            f"quotient_sum={row.quotient_sum} raw_sum={row.raw_sum} "
            f"quotient_prefix={row.quotient_prefix} "
            f"target_match={int(row.positive_matches_target)}"
        )
    print("signature_laws")
    print("  ord_507(p)=78 and ord_12675(p)=780")
    print("  selected non-anomaly cells have zero cyclic carry signature")
    print("  anomaly and non-selected cells have positive cyclic carry signature")
    print("  raw signatures are ten repetitions of the quotient signature")
    print("interpretation")
    print("  multi_digit_stickelberger_signature_matches_the_desired_valuation_mask=1")
    print("  this_is_not_yet_a_unit_phase_or_finite_payload_producer=1")
    print("  jacobi_next_probe_should_add_HD_or_Barnes_unit_phase_and_emit_raw_candidate=1")
    print(f"square_axis_gross_koblitz_multidigit_signature_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
