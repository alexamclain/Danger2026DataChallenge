#!/usr/bin/env python3
"""McCarthy well-poised hypergeometric point-delta contract for p25 Lane B.

The Barnes support screen kept one live target: a full `C_507` seed-exponent
point delta at q=138, whose outer S-image is {138,310,482}.  A targeted scout
identified the exceptional term in McCarthy's well-poised finite-field
hypergeometric transformation: it contains a character delta of the form

    delta(A_0^-1 * A_{n-1} * A_n).

In exponent notation on C_507 this is one linear equation.  This gate records
that the exceptional term has the right support granularity when tuned to
q=138, unlike order-3-only conditions or full p^2 orbit closure.  It is a
contract for the next numeric hypergeometric check, not that check itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP


P25 = 10**25 + 13
ORDER = 507
TARGET_Q = 138


@dataclass(frozen=True)
class McCarthyDeltaContractProfile:
    order: int
    target_q: int
    exponent_offset: int
    delta_support: tuple[int, ...]
    outer_s_image: tuple[int, ...]
    order3_support_size: int
    p2_multiplier: int
    p2_orbit_length: int
    p2_orbit_outer_s_support_size: int
    full_character_delta_is_single_point: bool
    order3_only_is_too_broad: bool
    p2_orbit_closure_is_too_broad: bool


def full_delta_support(exponent_offset: int) -> tuple[int, ...]:
    return tuple(q for q in range(ORDER) if q == exponent_offset % ORDER)


def order3_delta_support(exponent_offset: int) -> tuple[int, ...]:
    target = exponent_offset % 3
    return tuple(q for q in range(ORDER) if q % 3 == target)


def orbit_under_multiplier(seed: int, multiplier: int) -> tuple[int, ...]:
    seen: list[int] = []
    value = seed % ORDER
    while value not in seen:
        seen.append(value)
        value = (value * multiplier) % ORDER
    return tuple(seen)


def outer_s_image(support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted({(q + i * S_STEP) % ORDER for q in support for i in range(3)}))


def mccarthy_delta_contract_profile() -> McCarthyDeltaContractProfile:
    # Choose exponents with a0 - a_{n-1} - a_n = TARGET_Q; only the difference
    # matters for the character-delta support.
    exponent_offset = TARGET_Q
    support = full_delta_support(exponent_offset)
    order3_support = order3_delta_support(exponent_offset)
    p2_multiplier = pow(P25, 2, ORDER)
    p2_orbit = orbit_under_multiplier(TARGET_Q, p2_multiplier)
    p2_outer = outer_s_image(p2_orbit)
    return McCarthyDeltaContractProfile(
        order=ORDER,
        target_q=TARGET_Q,
        exponent_offset=exponent_offset,
        delta_support=support,
        outer_s_image=outer_s_image(support),
        order3_support_size=len(order3_support),
        p2_multiplier=p2_multiplier,
        p2_orbit_length=len(p2_orbit),
        p2_orbit_outer_s_support_size=len(p2_outer),
        full_character_delta_is_single_point=support == (TARGET_Q,),
        order3_only_is_too_broad=len(order3_support) == 169,
        p2_orbit_closure_is_too_broad=len(p2_outer) == 117,
    )


def main() -> int:
    print("p25 Lane B McCarthy well-poised point-delta contract gate")
    profile = mccarthy_delta_contract_profile()
    row_ok = (
        profile.delta_support == (138,)
        and profile.outer_s_image == (138, 310, 482)
        and profile.order3_support_size == 169
        and profile.p2_multiplier == 373
        and profile.p2_orbit_length == 39
        and profile.p2_orbit_outer_s_support_size == 117
        and profile.full_character_delta_is_single_point
        and profile.order3_only_is_too_broad
        and profile.p2_orbit_closure_is_too_broad
    )

    print(f"mccarthy_delta_contract_profile={profile}")
    print("delta_contract_laws")
    print("  full_C507_character_delta_can_be_tuned_to_q=138=1")
    print("  outer_S_image_is_(138,310,482)=1")
    print("  order_3_only_delta_has_169_seed_points_and_is_too_broad=1")
    print("  p2_orbit_closure_has_117_outer_S_points_and_is_too_broad=1")
    print("interpretation")
    print("  mccarthy_exceptional_delta_is_support_compatible=1")
    print("  next_check_must_numerically_verify_no_extra_transformed_difference_support=1")
    print(f"square_axis_mccarthy_well_poised_delta_contract_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
