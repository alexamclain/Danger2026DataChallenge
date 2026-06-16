#!/usr/bin/env python3
"""Reflection precheck for the p25 Gross-Koblitz gamma-unit route.

The targeted HD/GK first gate asks for a normalized odd/even `Gamma_p` divisor
reduced by reflection and Hasse-Davenport multiplication.  This small precheck
does only the reflection part for the naive Jacobi gamma divisor

    U(A) + U(B) - U(A+B),

where `A = t*N/3`, `B = (h-t mod 3)*N/3`, and `N=507`.

Using `p^39 = -1 mod 507`, reflection identifies `U(-x)` with `-U(x)` up to
sign/Teichmuller factors.  The result is a useful obstruction:

* all cells vanish except `(1,2)` and `(2,1)`;
* the two surviving cells have opposite multiples of the same free symbol
  `U(169)`;
* therefore reflection alone is not the anomaly projector.

The full HD/GK route remains alive only if multiplication/reflection/unit
relations remove the `(1,2)` false positive and realize the `(2,1)` phase as
an arithmetic unit, not merely this signed two-cell residue.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import ANOMALY_CELL
from p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate import (
    P,
    multiplicative_order,
)


N = 507
ORDER = multiplicative_order(P, N)
HALF_ORDER = ORDER // 2
SYMBOL = 169


@dataclass(frozen=True)
class ReflectionCell:
    h_value: int
    t_value: int
    residual: tuple[tuple[int, int], ...]
    residual_is_zero: bool
    residual_is_false_positive: bool
    residual_is_anomaly: bool


@dataclass(frozen=True)
class GammaReflectionProfile:
    p_mod_507: int
    p_half_power_mod_507: int
    cells: tuple[ReflectionCell, ...]
    nonzero_cells: tuple[tuple[int, int], ...]
    false_positive_cells: tuple[tuple[int, int], ...]
    anomaly_residual: tuple[tuple[int, int], ...]
    false_positive_residual: tuple[tuple[int, int], ...]
    only_symbol_169_survives: bool
    reflection_alone_is_not_projector: bool


def canonical_symbol(value: int) -> tuple[int | None, int]:
    value %= N
    if value == 0:
        return None, 0
    negative = (-value) % N
    if value < negative:
        return value, 1
    return negative, -1


def gamma_divisor_terms(h_value: int, t_value: int) -> tuple[tuple[int, int], ...]:
    scale = N // 3
    a_value = (t_value * scale) % N
    b_value = (((h_value - t_value) % 3) * scale) % N
    c_value = (a_value + b_value) % N
    return ((a_value, 1), (b_value, 1), (c_value, -1))


def reflected_odd_even_residual(h_value: int, t_value: int) -> tuple[tuple[int, int], ...]:
    coefficients: Counter[int] = Counter()
    multiplier = 1
    terms = gamma_divisor_terms(h_value, t_value)
    for index in range(ORDER):
        parity_sign = 1 if index % 2 == 1 else -1
        for value, coefficient in terms:
            symbol, reflection_sign = canonical_symbol(multiplier * value)
            if symbol is not None:
                coefficients[symbol] += parity_sign * coefficient * reflection_sign
        multiplier = (multiplier * P) % N
    return tuple(sorted((symbol, coeff) for symbol, coeff in coefficients.items() if coeff))


def gamma_reflection_profile() -> GammaReflectionProfile:
    cells: list[ReflectionCell] = []
    nonzero: list[tuple[int, int]] = []
    false_positive: list[tuple[int, int]] = []
    for h_value in range(3):
        for t_value in range(3):
            residual = reflected_odd_even_residual(h_value, t_value)
            coord = (h_value, t_value)
            if residual:
                nonzero.append(coord)
            is_anomaly = coord == ANOMALY_CELL
            is_false_positive = bool(residual) and not is_anomaly
            if is_false_positive:
                false_positive.append(coord)
            cells.append(
                ReflectionCell(
                    h_value=h_value,
                    t_value=t_value,
                    residual=residual,
                    residual_is_zero=not residual,
                    residual_is_false_positive=is_false_positive,
                    residual_is_anomaly=is_anomaly and bool(residual),
                )
            )

    anomaly_residual = reflected_odd_even_residual(*ANOMALY_CELL)
    false_positive_residual = reflected_odd_even_residual(1, 2)
    all_symbols = {
        symbol
        for cell in cells
        for symbol, _coefficient in cell.residual
    }
    return GammaReflectionProfile(
        p_mod_507=P % N,
        p_half_power_mod_507=pow(P, HALF_ORDER, N),
        cells=tuple(cells),
        nonzero_cells=tuple(nonzero),
        false_positive_cells=tuple(false_positive),
        anomaly_residual=anomaly_residual,
        false_positive_residual=false_positive_residual,
        only_symbol_169_survives=all_symbols == {SYMBOL},
        reflection_alone_is_not_projector=tuple(nonzero) != (ANOMALY_CELL,),
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz gamma reflection precheck gate")
    profile = gamma_reflection_profile()
    row_ok = (
        profile.p_mod_507 == 218
        and profile.p_half_power_mod_507 == 506
        and profile.nonzero_cells == ((1, 2), ANOMALY_CELL)
        and profile.false_positive_cells == ((1, 2),)
        and profile.anomaly_residual == ((SYMBOL, -234),)
        and profile.false_positive_residual == ((SYMBOL, 234),)
        and profile.only_symbol_169_survives
        and profile.reflection_alone_is_not_projector
    )

    print(f"gamma_reflection_profile={profile}")
    print("reflection_cells")
    for cell in profile.cells:
        print(f"  h={cell.h_value} t={cell.t_value}: residual={cell.residual}")
    print("reflection_laws")
    print("  p^39=-1 mod 507 pairs odd and even p^2 half-orbits by reflection")
    print("  naive_Jacobi_gamma_reflection_leaves_signed_two_cell_residue=1")
    print("  reflection_alone_is_not_the_anomaly_projector=1")
    print("interpretation")
    print("  HD_multiplication_or_extra_unit_phase_must_remove_the_1_2_false_positive=1")
    print("  free_gamma_symbol_U_169_still_remains_after_reflection_only=1")
    print(f"square_axis_gross_koblitz_gamma_reflection_precheck_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
