#!/usr/bin/env python3
"""Quotient selector-rigidity gate for the p25 anti-invariant product.

The raw KL exponent sums are saturated: many anti-invariant packets pass the
elementary Kubert-Lang congruences.  This gate checks the next finite selector.

After quotienting the raw K trace, scan every center and D-step in C_3 x C_169.
The accepted anti-invariant source packet is rigid: the forward theta2^-1
packet has one center and D up to reversal, while the reverse theta2 packet has
the inverse center and the same D reversal symmetry.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    profile_anti_invariant_product,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
)


Q_RIGHT_ORDER = 3
Q_C_ORDER = C_ORDER

Coord = tuple[int, int]
RingTuple = tuple[tuple[Coord, int], ...]


@dataclass(frozen=True)
class QuotientSelectorMatch:
    center: Coord
    d_step: Coord


@dataclass(frozen=True)
class RawSelectorValidation:
    name: str
    raw_center: Coord
    raw_d_step: Coord
    quotient_center: Coord
    quotient_d_step: Coord
    orientation: str
    exact_theta2: bool
    exact_theta2_inverse: bool
    recovered_sign: int
    ok: bool


@dataclass(frozen=True)
class AntiInvariantSelectorRigidityProfile:
    quotient_group: str
    quotient_centers_scanned: int
    quotient_d_steps_scanned: int
    quotient_pairs_scanned: int
    target_forward_ring: RingTuple
    target_reverse_ring: RingTuple
    forward_matches: tuple[QuotientSelectorMatch, ...]
    reverse_matches: tuple[QuotientSelectorMatch, ...]
    support_only_matches: tuple[QuotientSelectorMatch, ...]
    zero_d_support_matches: tuple[QuotientSelectorMatch, ...]
    raw_forward_validations: tuple[RawSelectorValidation, ...]
    raw_reverse_validations: tuple[RawSelectorValidation, ...]
    center_rigid_up_to_orientation: bool
    d_rigid_up_to_reversal: bool
    support_selector_no_extra_unsigned_hits: bool
    quotient_selector_is_rigid: bool
    next_debt: str
    row_ok: bool


def q_add(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % Q_RIGHT_ORDER, (left[1] + right[1]) % Q_C_ORDER)


def q_scale(coord: Coord, multiplier: int) -> Coord:
    return ((coord[0] * multiplier) % Q_RIGHT_ORDER, (coord[1] * multiplier) % Q_C_ORDER)


def q_inverse(coord: Coord) -> Coord:
    return ((-coord[0]) % Q_RIGHT_ORDER, (-coord[1]) % Q_C_ORDER)


def q_ring_entry(ring: dict[Coord, int], coord: Coord, coefficient: int) -> None:
    ring[coord] += coefficient
    if ring[coord] == 0:
        del ring[coord]


def quotient_coord(raw_coord: Coord) -> Coord:
    return (raw_coord[0] % Q_RIGHT_ORDER, raw_coord[1] % Q_C_ORDER)


def quotient_anti_invariant_ring(center: Coord, d_step: Coord, reverse: bool = False) -> RingTuple:
    ring: dict[Coord, int] = defaultdict(int)
    for offset in (-1, 0, 1):
        point = q_add(center, q_scale(d_step, offset))
        inverse = q_inverse(point)
        if reverse:
            q_ring_entry(ring, inverse, 1)
            q_ring_entry(ring, point, -1)
        else:
            q_ring_entry(ring, point, 1)
            q_ring_entry(ring, inverse, -1)
    return tuple(sorted(ring.items()))


def quotient_support(ring: RingTuple) -> tuple[Coord, ...]:
    return tuple(coord for coord, _coefficient in ring)


def scan_quotient_selector(
    target_forward: RingTuple,
    target_reverse: RingTuple,
) -> tuple[
    tuple[QuotientSelectorMatch, ...],
    tuple[QuotientSelectorMatch, ...],
    tuple[QuotientSelectorMatch, ...],
    tuple[QuotientSelectorMatch, ...],
]:
    forward: list[QuotientSelectorMatch] = []
    reverse: list[QuotientSelectorMatch] = []
    support_only: list[QuotientSelectorMatch] = []
    zero_d_support: list[QuotientSelectorMatch] = []
    target_support = quotient_support(target_forward)

    for right in range(Q_RIGHT_ORDER):
        for c_log in range(Q_C_ORDER):
            center = (right, c_log)
            for d_right in range(Q_RIGHT_ORDER):
                for d_c_log in range(Q_C_ORDER):
                    d_step = (d_right, d_c_log)
                    ring = quotient_anti_invariant_ring(center, d_step)
                    match = QuotientSelectorMatch(center, d_step)
                    if ring == target_forward:
                        forward.append(match)
                    if ring == target_reverse:
                        reverse.append(match)
                    if quotient_support(ring) == target_support:
                        support_only.append(match)
                        if d_step == (0, 0):
                            zero_d_support.append(match)

    return (
        tuple(forward),
        tuple(reverse),
        tuple(support_only),
        tuple(zero_d_support),
    )


def validate_raw_product(
    name: str,
    raw_center: Coord,
    raw_d_step: Coord,
    reverse: bool = False,
) -> RawSelectorValidation:
    row = profile_anti_invariant_product(
        name,
        raw_center,
        KERNEL_SHIFT,
        raw_d_step,
        reverse=reverse,
    )
    return RawSelectorValidation(
        name=name,
        raw_center=raw_center,
        raw_d_step=raw_d_step,
        quotient_center=quotient_coord(raw_center),
        quotient_d_step=quotient_coord(raw_d_step),
        orientation=row.orientation,
        exact_theta2=row.exact_theta2,
        exact_theta2_inverse=row.exact_theta2_inverse,
        recovered_sign=row.recovered_sign,
        ok=row.ok,
    )


def profile_anti_invariant_selector_rigidity() -> AntiInvariantSelectorRigidityProfile:
    raw_center = (47, 28)
    raw_inverse_center = (28, 141)
    raw_negative_d = scale_coord(D_SHIFT, -1)
    target_center = quotient_coord(raw_center)
    target_d = quotient_coord(D_SHIFT)
    target_forward = quotient_anti_invariant_ring(target_center, target_d)
    target_reverse = quotient_anti_invariant_ring(target_center, target_d, reverse=True)
    forward, reverse, support_only, zero_d_support = scan_quotient_selector(
        target_forward,
        target_reverse,
    )

    raw_forward = (
        validate_raw_product("rigidity_forward_D", raw_center, D_SHIFT),
        validate_raw_product("rigidity_forward_minus_D", raw_center, raw_negative_d),
    )
    raw_reverse = (
        validate_raw_product("rigidity_inverse_center_D", raw_inverse_center, D_SHIFT),
        validate_raw_product("rigidity_inverse_center_minus_D", raw_inverse_center, raw_negative_d),
    )

    expected_forward = (
        QuotientSelectorMatch((2, 28), (1, 3)),
        QuotientSelectorMatch((2, 28), (2, 166)),
    )
    expected_reverse = (
        QuotientSelectorMatch((1, 141), (1, 3)),
        QuotientSelectorMatch((1, 141), (2, 166)),
    )
    expected_support = expected_reverse + expected_forward
    center_rigid = {match.center for match in forward + reverse} == {(2, 28), (1, 141)}
    d_rigid = {match.d_step for match in forward + reverse} == {(1, 3), (2, 166)}
    support_no_extra = support_only == expected_support and not zero_d_support
    raw_forward_ok = all(
        validation.ok
        and validation.exact_theta2_inverse
        and not validation.exact_theta2
        and validation.recovered_sign == -1
        for validation in raw_forward
    )
    raw_reverse_ok = all(
        validation.ok
        and validation.exact_theta2
        and not validation.exact_theta2_inverse
        and validation.recovered_sign == 1
        for validation in raw_reverse
    )
    row_ok = (
        Q_RIGHT_ORDER * Q_C_ORDER == 507
        and Q_RIGHT_ORDER * Q_C_ORDER * Q_RIGHT_ORDER * Q_C_ORDER == 257049
        and forward == expected_forward
        and reverse == expected_reverse
        and support_no_extra
        and center_rigid
        and d_rigid
        and raw_forward_ok
        and raw_reverse_ok
    )
    return AntiInvariantSelectorRigidityProfile(
        quotient_group="C_3 x C_169",
        quotient_centers_scanned=Q_RIGHT_ORDER * Q_C_ORDER,
        quotient_d_steps_scanned=Q_RIGHT_ORDER * Q_C_ORDER,
        quotient_pairs_scanned=Q_RIGHT_ORDER * Q_C_ORDER * Q_RIGHT_ORDER * Q_C_ORDER,
        target_forward_ring=target_forward,
        target_reverse_ring=target_reverse,
        forward_matches=forward,
        reverse_matches=reverse,
        support_only_matches=support_only,
        zero_d_support_matches=zero_d_support,
        raw_forward_validations=raw_forward,
        raw_reverse_validations=raw_reverse,
        center_rigid_up_to_orientation=center_rigid,
        d_rigid_up_to_reversal=d_rigid,
        support_selector_no_extra_unsigned_hits=support_no_extra,
        quotient_selector_is_rigid=row_ok,
        next_debt=(
            "find a challenge-legal Robert/Siegel/Kubert-Lang identity that "
            "emits this rigid quotient packet, not merely an exponent-balanced "
            "anti-invariant divisor"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang anti-invariant selector-rigidity gate")
    profile = profile_anti_invariant_selector_rigidity()
    print(f"anti_invariant_selector_rigidity_profile={profile}")
    print("quotient_scan")
    print(f"  group={profile.quotient_group}")
    print(f"  centers_scanned={profile.quotient_centers_scanned}")
    print(f"  d_steps_scanned={profile.quotient_d_steps_scanned}")
    print(f"  pairs_scanned={profile.quotient_pairs_scanned}")
    print("matches")
    print(f"  forward={profile.forward_matches}")
    print(f"  reverse={profile.reverse_matches}")
    print(f"  support_only={profile.support_only_matches}")
    print(f"  zero_D_support_matches={profile.zero_d_support_matches}")
    print("raw_validations")
    for validation in profile.raw_forward_validations + profile.raw_reverse_validations:
        print(
            "  "
            f"{validation.name}: center={validation.raw_center} D={validation.raw_d_step} "
            f"q_center={validation.quotient_center} q_D={validation.quotient_d_step} "
            f"orientation={validation.orientation} theta2={int(validation.exact_theta2)} "
            f"theta2_inverse={int(validation.exact_theta2_inverse)} "
            f"sign={validation.recovered_sign} ok={int(validation.ok)}"
        )
    print("interpretation")
    print("  quotient_center_is_rigid_up_to_inversion_orientation=1")
    print("  quotient_D_is_rigid_up_to_reversal=1")
    print("  support_only_scan_has_no_extra_unsigned_hits=1")
    print("  raw_D_reversal_and_inverse_center_validate_against_theta2_resolvent=1")
    print(
        "  theorem_claim_must_emit_this_rigid_center_D_packet_not_only_KL_exponent_balance=1"
    )
    print(
        "robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_rows="
        f"{int(profile.row_ok)}/1"
    )
    print(
        "conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_"
        "anti_invariant_selector_rigidity_gate"
    )
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
