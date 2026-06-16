#!/usr/bin/env python3
"""Frobenius pairing on the 12-pair conductor-39 coset quotient.

The coset-selector gate writes the primitive unit as

    U_chi = 1_{7<2>} - 1_{<2>}.

This gate records the exact cyclic Frobenius action on the ordered pairs
indexed by h_i = 2^i.  For p25, p = 23 = 7*2^11 mod 39, so Frobenius sends
denominator h_i to numerator 7*h_{i+11}; it sends numerator 7*h_i to
denominator h_{i+9}.  Thus Frob_p(U_chi)=-U_chi, while Frob_p^2 is a rotation
by 8 on both 12-cycles.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_coset_selector_gate import (
    COSET_REPRESENTATIVE,
    GENERATOR,
    multiply_residue_set,
    profile_yang_y507_conductor39_coset_selector,
)
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR


ORDER = 12


@dataclass(frozen=True)
class FrobeniusPairRow:
    index: int
    denominator: int
    numerator: int
    frob_denominator: int
    frob_denominator_numerator_index: int
    frob_numerator: int
    frob_numerator_denominator_index: int
    p2_denominator: int
    p2_numerator: int
    ok: bool


@dataclass(frozen=True)
class Conductor39CosetFrobeniusPairing:
    level: int
    generator: int
    coset_representative: int
    p_mod_39: int
    p_as_coset_shift: tuple[int, int]
    p_times_coset_rep_as_kernel_shift: tuple[int, int]
    p2_as_kernel_shift: tuple[int, int]
    denominator_to_numerator_shift: int
    numerator_to_denominator_shift: int
    p2_cycle_shift: int
    pair_rows: tuple[FrobeniusPairRow, ...]
    all_pair_rows_ok: bool
    frob_swaps_layers_with_negative_sign: bool
    frob_squared_rotates_each_layer: bool
    q_value_frobenius_inverse_contract: bool
    w_value_frobenius_inverse_contract: bool
    hilbert90_boundary_contract: str
    coset_selector_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def ordered_kernel() -> tuple[int, ...]:
    return tuple(pow(GENERATOR, index, CONDUCTOR) for index in range(ORDER))


def ordered_coset() -> tuple[int, ...]:
    return tuple((COSET_REPRESENTATIVE * item) % CONDUCTOR for item in ordered_kernel())


def discrete_log_in_ordered(value: int, ordered: tuple[int, ...]) -> int:
    try:
        return ordered.index(value)
    except ValueError as exc:
        raise AssertionError(f"value {value} missing from ordered cycle") from exc


def shift_decomposition(value: int, ordered: tuple[int, ...]) -> tuple[int, int]:
    index = discrete_log_in_ordered(value % CONDUCTOR, ordered)
    return value % CONDUCTOR, index


def pair_rows() -> tuple[FrobeniusPairRow, ...]:
    kernel = ordered_kernel()
    coset = ordered_coset()
    rows: list[FrobeniusPairRow] = []
    for index, denominator in enumerate(kernel):
        numerator = coset[index]
        frob_denominator = (P25 * denominator) % CONDUCTOR
        frob_numerator = (P25 * numerator) % CONDUCTOR
        p2_denominator = (P25 * P25 * denominator) % CONDUCTOR
        p2_numerator = (P25 * P25 * numerator) % CONDUCTOR
        den_to_num = discrete_log_in_ordered(frob_denominator, coset)
        num_to_den = discrete_log_in_ordered(frob_numerator, kernel)
        rows.append(
            FrobeniusPairRow(
                index=index,
                denominator=denominator,
                numerator=numerator,
                frob_denominator=frob_denominator,
                frob_denominator_numerator_index=den_to_num,
                frob_numerator=frob_numerator,
                frob_numerator_denominator_index=num_to_den,
                p2_denominator=p2_denominator,
                p2_numerator=p2_numerator,
                ok=(
                    den_to_num == (index + 11) % ORDER
                    and num_to_den == (index + 9) % ORDER
                    and p2_denominator == kernel[(index + 8) % ORDER]
                    and p2_numerator == coset[(index + 8) % ORDER]
                ),
            )
        )
    return tuple(rows)


def profile_yang_y507_conductor39_coset_frobenius_pairing() -> Conductor39CosetFrobeniusPairing:
    coset = profile_yang_y507_conductor39_coset_selector()
    kernel = ordered_kernel()
    coset_cycle = ordered_coset()
    rows = pair_rows()
    p_mod = P25 % CONDUCTOR
    p_as_coset = shift_decomposition(p_mod * pow(COSET_REPRESENTATIVE, -1, CONDUCTOR), kernel)
    p_times_coset_rep = shift_decomposition(p_mod * COSET_REPRESENTATIVE, kernel)
    p2_as_kernel = shift_decomposition((p_mod * p_mod) % CONDUCTOR, kernel)
    denominator_shift = rows[0].frob_denominator_numerator_index
    numerator_shift = rows[0].frob_numerator_denominator_index
    p2_shift = discrete_log_in_ordered((p_mod * p_mod) % CONDUCTOR, kernel)
    direct_closer = False
    row_ok = (
        coset.row_ok
        and CONDUCTOR == 39
        and GENERATOR == 2
        and COSET_REPRESENTATIVE == 7
        and kernel[0] == 1
        and coset_cycle[0] == 7
        and p_mod == 23
        and p_as_coset == (20, 11)
        and p_times_coset_rep == (5, 9)
        and p2_as_kernel == (22, 8)
        and denominator_shift == 11
        and numerator_shift == 9
        and p2_shift == 8
        and len(rows) == ORDER
        and all(row.ok for row in rows)
        and not direct_closer
    )
    return Conductor39CosetFrobeniusPairing(
        level=CONDUCTOR,
        generator=GENERATOR,
        coset_representative=COSET_REPRESENTATIVE,
        p_mod_39=p_mod,
        p_as_coset_shift=p_as_coset,
        p_times_coset_rep_as_kernel_shift=p_times_coset_rep,
        p2_as_kernel_shift=p2_as_kernel,
        denominator_to_numerator_shift=denominator_shift,
        numerator_to_denominator_shift=numerator_shift,
        p2_cycle_shift=p2_shift,
        pair_rows=rows,
        all_pair_rows_ok=all(row.ok for row in rows),
        frob_swaps_layers_with_negative_sign=True,
        frob_squared_rotates_each_layer=True,
        q_value_frobenius_inverse_contract=True,
        w_value_frobenius_inverse_contract=True,
        hilbert90_boundary_contract=(
            "If Q=prod_{h in <2>} E_{7h}/E_h, then Frob_p(Q)=Q^-1; "
            "W=Q^6 is the boundary (1-Frob_p)(Q^3)."
        ),
        coset_selector_ok=coset.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Frobenius pairing on the compact 12-pair quotient is explicit: "
            "denominators shift to numerators by +11, numerators shift to "
            "denominators by +9, and Frob^2 rotates by +8."
        ),
        first_missing_clause=(
            "pairing gives the descent contract, not the finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask value-side theorems for a quotient Q with Frob_p(Q)=Q^-1, "
            "or for an explicit Hilbert-90 preimage whose boundary is Q^6"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_coset_frobenius_pairing()
    print("p25 KSY-y Yang Y_507 conductor-39 coset Frobenius-pairing gate")
    print(f"level={profile.level}")
    print(f"generator={profile.generator}")
    print(f"coset_representative={profile.coset_representative}")
    print(f"p_mod_39={profile.p_mod_39}")
    print("shift_decompositions")
    print(f"  p_as_coset_shift={profile.p_as_coset_shift}")
    print(f"  p_times_coset_rep_as_kernel_shift={profile.p_times_coset_rep_as_kernel_shift}")
    print(f"  p2_as_kernel_shift={profile.p2_as_kernel_shift}")
    print(f"  denominator_to_numerator_shift={profile.denominator_to_numerator_shift}")
    print(f"  numerator_to_denominator_shift={profile.numerator_to_denominator_shift}")
    print(f"  p2_cycle_shift={profile.p2_cycle_shift}")
    print("sample_pairs")
    for row in profile.pair_rows[:4]:
        print(
            "  "
            f"i={row.index} den={row.denominator} num={row.numerator} "
            f"Fden={row.frob_denominator}->num_i{row.frob_denominator_numerator_index} "
            f"Fnum={row.frob_numerator}->den_i{row.frob_numerator_denominator_index} "
            f"F2den={row.p2_denominator} F2num={row.p2_numerator} ok={int(row.ok)}"
        )
    print("checks")
    print(f"  all_pair_rows_ok={int(profile.all_pair_rows_ok)}")
    print(f"  frob_swaps_layers_with_negative_sign={int(profile.frob_swaps_layers_with_negative_sign)}")
    print(f"  frob_squared_rotates_each_layer={int(profile.frob_squared_rotates_each_layer)}")
    print(f"  q_value_frobenius_inverse_contract={int(profile.q_value_frobenius_inverse_contract)}")
    print(f"  w_value_frobenius_inverse_contract={int(profile.w_value_frobenius_inverse_contract)}")
    print(f"  coset_selector_ok={int(profile.coset_selector_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  compact_quotient_Q_has_Frob_p_Q_equals_Q_inverse=1")
    print("  W_equals_Q6_is_boundary_of_Q3=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_coset_frobenius_pairing_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 coset Frobenius pairing regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
