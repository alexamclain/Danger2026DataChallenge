#!/usr/bin/env python3
"""Integrated producer contract for the p25 anti-invariant KSY/KL target.

Recent gates made the anti-invariant normalized-y target rigid:

* the center and D class are unique up to orientation/reversal;
* the three D slices must have equal weights;
* every one of the 75 K-traced atoms has forced weight.

This gate ties those facts back to the existing KSY finite producer spine.  A
theorem hit may now target the compact anti-invariant data

    C, D, primitive K, orientation

because the T edge is forced by reflection, T=-2C in the quotient and
T=-2C+K upstairs.  But it must still produce the exact equal-weight
anti-invariant normalized-y product, not merely a KL exponent-balanced packet.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    profile_anti_invariant_product_intake,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate import (
    profile_anti_invariant_selector_rigidity,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate import (
    profile_atomic_weight_rigidity,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_gate import (
    profile_d_slice_weight_rigidity,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_exponent_saturation_gate import (
    profile_raw_exponent_saturation,
)
from p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness import (
    QuotientFactorCertificateProfile,
    profile_quotient_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    profile_source_quotient_packet,
    target_source_quotient_packet,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord, scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
QUOTIENT_RIGHT_ORDER = 3


@dataclass(frozen=True)
class AntiInvariantDerivedClasses:
    raw_center: Coord
    raw_d_step: Coord
    raw_k_step: Coord
    raw_base: Coord
    raw_t_from_reflection: Coord
    quotient_center: Coord
    quotient_d_step: Coord
    quotient_base: Coord
    quotient_t_from_reflection: Coord
    quotient_t_half: Coord
    quotient_negative_center: Coord
    t_reflection_matches_factor_edge: bool
    base_matches_factor_base: bool


@dataclass(frozen=True)
class AntiInvariantProducerContractProfile:
    derived: AntiInvariantDerivedClasses
    anti_invariant_intake_ok: bool
    selector_rigidity_ok: bool
    d_slice_weight_rigidity_ok: bool
    atomic_weight_rigidity_ok: bool
    raw_exponent_screen_saturated: bool
    quotient_factor_profile: QuotientFactorCertificateProfile
    source_packet_profile: SourceQuotientPacketProfile
    finite_contract_accepts_anti_invariant_target: bool
    finite_contract_rejects_shortcuts: bool
    compact_theorem_payload: str
    first_falsifiers: tuple[str, ...]
    remaining_debt: str
    row_ok: bool


def inverse_quotient(coord: Coord) -> Coord:
    return ((-coord[0]) % QUOTIENT_RIGHT_ORDER, (-coord[1]) % C_ORDER)


def scale_quotient(coord: Coord, multiplier: int) -> Coord:
    return ((coord[0] * multiplier) % QUOTIENT_RIGHT_ORDER, (coord[1] * multiplier) % C_ORDER)


def half_quotient(coord: Coord) -> Coord:
    return (
        (coord[0] * pow(2, -1, QUOTIENT_RIGHT_ORDER)) % QUOTIENT_RIGHT_ORDER,
        (coord[1] * pow(2, -1, C_ORDER)) % C_ORDER,
    )


def quotient_coord(raw_coord: Coord) -> Coord:
    return (raw_coord[0] % QUOTIENT_RIGHT_ORDER, raw_coord[1] % C_ORDER)


def derive_classes(raw_center: Coord) -> AntiInvariantDerivedClasses:
    raw_base = add_coord(raw_center, scale_coord(D_SHIFT, -1))
    raw_t = add_coord(scale_coord(raw_center, -2), KERNEL_SHIFT)
    q_center = quotient_coord(raw_center)
    q_d = quotient_coord(D_SHIFT)
    q_base = quotient_coord(raw_base)
    q_t = scale_quotient(q_center, -2)
    q_half_t = half_quotient(q_t)
    q_negative_center = inverse_quotient(q_center)
    return AntiInvariantDerivedClasses(
        raw_center=raw_center,
        raw_d_step=D_SHIFT,
        raw_k_step=KERNEL_SHIFT,
        raw_base=raw_base,
        raw_t_from_reflection=raw_t,
        quotient_center=q_center,
        quotient_d_step=q_d,
        quotient_base=q_base,
        quotient_t_from_reflection=q_t,
        quotient_t_half=q_half_t,
        quotient_negative_center=q_negative_center,
        t_reflection_matches_factor_edge=q_t == (2, 113) and raw_t == (38, 113),
        base_matches_factor_base=q_base == (1, 25) and raw_base == (25, 25),
    )


def profile_anti_invariant_producer_contract() -> AntiInvariantProducerContractProfile:
    intake = profile_anti_invariant_product_intake()
    selector = profile_anti_invariant_selector_rigidity()
    d_weights = profile_d_slice_weight_rigidity()
    atomic_weights = profile_atomic_weight_rigidity()
    raw_exponents = profile_raw_exponent_saturation()
    derived = derive_classes(intake.raw_center)
    quotient_factor = profile_quotient_factor_certificate(
        "anti_invariant_contract_quotient_factor",
        derived.quotient_base,
        derived.quotient_d_step,
        derived.quotient_t_from_reflection,
        1,
    )
    source_packet = profile_source_quotient_packet(
        "anti_invariant_contract_source_packet",
        packet_entries(target_source_quotient_packet()),
        1,
    )

    finite_accepts = (
        intake.row_ok
        and selector.row_ok
        and d_weights.row_ok
        and atomic_weights.row_ok
        and quotient_factor.ok
        and source_packet.ok
        and derived.base_matches_factor_base
        and derived.t_reflection_matches_factor_edge
        and derived.quotient_t_half == derived.quotient_negative_center
    )
    shortcuts_rejected = (
        raw_exponents.kl_screen_is_not_selector
        and intake.missing_k_rejected
        and intake.collapsed_k_rejected
        and intake.truncated_d_rejected
        and intake.wrong_d_rejected
        and intake.shifted_center_rejected
        and selector.support_selector_no_extra_unsigned_hits
        and d_weights.disjoint_support_proves_integer_weight_rigidity
        and atomic_weights.linear_nullity_from_disjoint_support == 0
        and atomic_weights.missing_atom_rejected
        and atomic_weights.alternating_k_weights_rejected
    )
    row_ok = (
        RIGHT_ORDER == 75
        and C_ORDER == 169
        and QUOTIENT_RIGHT_ORDER == 3
        and derived.raw_center == (47, 28)
        and derived.raw_base == (25, 25)
        and derived.raw_d_step == (22, 3)
        and derived.raw_k_step == (57, 0)
        and derived.raw_t_from_reflection == (38, 113)
        and derived.quotient_center == (2, 28)
        and derived.quotient_base == (1, 25)
        and derived.quotient_d_step == (1, 3)
        and derived.quotient_t_from_reflection == (2, 113)
        and derived.quotient_t_half == (1, 141)
        and finite_accepts
        and shortcuts_rejected
        and quotient_factor.factor_certificate_profile.factor_support_budget == 31
        and quotient_factor.factor_certificate_profile.product_support == 150
        and source_packet.packet_support == 6
        and source_packet.lifted_source_support == 150
    )
    return AntiInvariantProducerContractProfile(
        derived=derived,
        anti_invariant_intake_ok=intake.row_ok,
        selector_rigidity_ok=selector.row_ok,
        d_slice_weight_rigidity_ok=d_weights.row_ok,
        atomic_weight_rigidity_ok=atomic_weights.row_ok,
        raw_exponent_screen_saturated=raw_exponents.kl_screen_is_not_selector,
        quotient_factor_profile=quotient_factor,
        source_packet_profile=source_packet,
        finite_contract_accepts_anti_invariant_target=finite_accepts,
        finite_contract_rejects_shortcuts=shortcuts_rejected,
        compact_theorem_payload=(
            "C=(47,28), D=(22,3), primitive K=(57,0), orientation; "
            "base=C-D and T=-2C+K are derived"
        ),
        first_falsifiers=(
            "raw KL exponent balance without finite theta2 intake",
            "missing/collapsed/nonprimitive K trace",
            "truncated, wrong, missing, doubled, or reweighted D segment",
            "shifted or inverted center without matching orientation",
            "nonuniform K-layer or atom weights",
            "q-cycle/source-coordinate convention confusion",
        ),
        remaining_debt=(
            "prove a challenge-legal Robert/Siegel/Kubert-Lang/KSY identity "
            "for the exact equal-weight K-traced anti-invariant normalized-y product"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang anti-invariant producer-contract gate")
    profile = profile_anti_invariant_producer_contract()
    print(f"anti_invariant_producer_contract_profile={profile}")
    print("derived_classes")
    print(f"  raw_center={profile.derived.raw_center}")
    print(f"  raw_base=C-D={profile.derived.raw_base}")
    print(f"  raw_T=-2C+K={profile.derived.raw_t_from_reflection}")
    print(f"  quotient_center={profile.derived.quotient_center}")
    print(f"  quotient_base={profile.derived.quotient_base}")
    print(f"  quotient_D={profile.derived.quotient_d_step}")
    print(f"  quotient_T=-2C={profile.derived.quotient_t_from_reflection}")
    print(f"  quotient_T_half={profile.derived.quotient_t_half}")
    print("finite_contract")
    print(f"  anti_invariant_intake_ok={int(profile.anti_invariant_intake_ok)}")
    print(f"  selector_rigidity_ok={int(profile.selector_rigidity_ok)}")
    print(f"  d_slice_weight_rigidity_ok={int(profile.d_slice_weight_rigidity_ok)}")
    print(f"  atomic_weight_rigidity_ok={int(profile.atomic_weight_rigidity_ok)}")
    print(f"  quotient_factor_ok={int(profile.quotient_factor_profile.ok)}")
    print(f"  source_packet_ok={int(profile.source_packet_profile.ok)}")
    print("shortcut_falsifiers")
    for falsifier in profile.first_falsifiers:
        print(f"  {falsifier}")
    print("interpretation")
    print("  anti_invariant_center_D_form_derives_base_and_T_edge=1")
    print("  exact_equal_weight_K_traced_atoms_are_forced=1")
    print("  quotient_factor_and_source_packet_contract_accept_the_derived_target=1")
    print("  raw_KL_exponent_balance_is_not_a_selector=1")
    print(
        "robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    print(
        "conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_"
        "anti_invariant_producer_contract_gate"
    )
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
