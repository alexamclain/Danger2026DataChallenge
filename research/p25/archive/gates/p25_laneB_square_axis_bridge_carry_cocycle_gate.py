#!/usr/bin/env python3
"""Nonsplit C_169 carry cocycle for the p25 square-axis bridge.

The C_13 descent gate shows that the bridge has a cheap shadow but is not the
pullback of that shadow.  This gate isolates the missing ingredient: the true
C_169 lift uses the carry cocycle of the nonsplit cyclic extension

    0 -> C_13 -> C_169 -> C_13 -> 0.

A tempting split model treats the C coordinate as C_13 x C_13 with no carry.
It has the same C_13 shadow, the same 150-cell support, kernel-triviality, raw
D^3=Y, and even full mixed right/C character support.  It still fails the
bridge trace because the fiber carry is wrong.  Thus a producer must realize
the cyclic C_169 carry law, not just the C_13 shadow plus an independent fiber.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_axis_hull_character_gap_gate import support_profile
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    quotient_mask,
    quotient_trace,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    formal_factors,
    multiply_factors,
    source_mask_to_raw,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


SplitCoord = tuple[int, int, int]
C13Pair = tuple[int, int]


@dataclass(frozen=True)
class CarryCocycleProfile:
    true_support: int
    split_support: int
    same_c13_projection: bool
    true_candidate_ok: bool
    split_trace_correct: bool
    split_block_constancy_hits: int
    split_kernel_modes: tuple[int, ...]
    split_raw_relation_mismatches: int
    split_pure_c_characters: int
    split_mixed_characters: int
    true_positive_classes: tuple[tuple[int, int, int, int, int], ...]
    true_negative_classes: tuple[tuple[int, int, int, int, int], ...]
    split_positive_classes: tuple[tuple[int, int, int, int, int], ...]
    split_negative_classes: tuple[tuple[int, int, int, int, int], ...]
    true_fiber_counts: tuple[tuple[int, int], ...]
    split_fiber_counts: tuple[tuple[int, int], ...]
    d_carries: tuple[int, ...]
    t_carries: tuple[int, ...]
    true_t_translate_is_reversed_inversion: bool
    split_t_translate_is_reversed_inversion: bool


def split_c(c_log: int) -> C13Pair:
    return c_log % 13, c_log // 13


def unsplit_c(low: int, fiber: int) -> int:
    return low + 13 * fiber


def add_split(left: SplitCoord, right: SplitCoord) -> SplitCoord:
    return (
        (left[0] + right[0]) % RIGHT_ORDER,
        (left[1] + right[1]) % 13,
        (left[2] + right[2]) % 13,
    )


def scale_split(step: SplitCoord, scale: int) -> SplitCoord:
    return (
        (step[0] * scale) % RIGHT_ORDER,
        (step[1] * scale) % 13,
        (step[2] * scale) % 13,
    )


def multiply_split(left: dict[SplitCoord, int], right: dict[SplitCoord, int]) -> dict[SplitCoord, int]:
    out: dict[SplitCoord, int] = {}
    for left_coord, left_value in left.items():
        for right_coord, right_value in right.items():
            coord = add_split(left_coord, right_coord)
            out[coord] = out.get(coord, 0) + left_value * right_value
            if out[coord] == 0:
                del out[coord]
    return dict(sorted(out.items()))


def geometric_split(step: SplitCoord, length: int) -> dict[SplitCoord, int]:
    return {scale_split(step, index): 1 for index in range(length)}


def split_formal_shadow() -> Ring:
    base_low, base_fiber = split_c(BASE_POINT[1])
    kernel_low, kernel_fiber = split_c(KERNEL_SHIFT[1])
    d_low, d_fiber = split_c(D_SHIFT[1])
    t_low, t_fiber = split_c(BRIDGE_SHIFT[1])
    factors = (
        {(BASE_POINT[0], base_low, base_fiber): 1},
        geometric_split((KERNEL_SHIFT[0], kernel_low, kernel_fiber), 25),
        geometric_split((D_SHIFT[0], d_low, d_fiber), 3),
        {
            (0, 0, 0): 1,
            (BRIDGE_SHIFT[0], t_low, t_fiber): -1,
        },
    )
    product: dict[SplitCoord, int] = {(0, 0, 0): 1}
    for factor in factors:
        product = multiply_split(product, factor)

    ring: Ring = {}
    for (right_log, c_low, c_fiber), value in product.items():
        coord = (right_log, unsplit_c(c_low, c_fiber))
        ring[coord] = ring.get(coord, 0) + value
        if ring[coord] == 0:
            del ring[coord]
    return dict(sorted(ring.items()))


def project_to_c13(ring: Ring) -> dict[tuple[int, int], int]:
    out: dict[tuple[int, int], int] = {}
    for (right_log, c_log), value in ring.items():
        coord = (right_log, c_log % 13)
        out[coord] = out.get(coord, 0) + value
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def source_classes(ring: Ring, sign: int) -> tuple[tuple[int, int, int, int, int], ...]:
    counts = Counter((right_log % 3, c_log) for (right_log, c_log), value in ring.items() if value == sign)
    return tuple(
        sorted(
            (right_mod3, c_log, c_log % 13, c_log // 13, count)
            for (right_mod3, c_log), count in counts.items()
        )
    )


def fiber_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(c_log // 13 for (_right_log, c_log) in ring).items()))


def add_carry(pair: C13Pair, step: C13Pair) -> tuple[C13Pair, int]:
    low, fiber = pair
    step_low, step_fiber = step
    total_low = low + step_low
    carry = total_low // 13
    return ((total_low % 13, (fiber + step_fiber + carry) % 13), carry)


def d_order_c_values(use_carry: bool) -> tuple[int, int, int]:
    pair = split_c(BASE_POINT[1])
    step = split_c(D_SHIFT[1])
    values = [BASE_POINT[1]]
    for _index in range(2):
        if use_carry:
            pair, _carry = add_carry(pair, step)
        else:
            pair = ((pair[0] + step[0]) % 13, (pair[1] + step[1]) % 13)
        values.append(unsplit_c(*pair))
    return tuple(values)


def t_translate_values(c_values: tuple[int, int, int], use_carry: bool) -> tuple[int, int, int]:
    step = split_c(BRIDGE_SHIFT[1])
    translated: list[int] = []
    for c_log in c_values:
        pair = split_c(c_log)
        if use_carry:
            pair, _carry = add_carry(pair, step)
        else:
            pair = ((pair[0] + step[0]) % 13, (pair[1] + step[1]) % 13)
        translated.append(unsplit_c(*pair))
    return tuple(translated)


def carry_sequences() -> tuple[tuple[int, ...], tuple[int, ...]]:
    pair = split_c(BASE_POINT[1])
    d_step = split_c(D_SHIFT[1])
    d_carries: list[int] = []
    positive_pairs = [pair]
    for _index in range(2):
        pair, carry = add_carry(pair, d_step)
        d_carries.append(carry)
        positive_pairs.append(pair)

    t_step = split_c(BRIDGE_SHIFT[1])
    t_carries = [add_carry(pair, t_step)[1] for pair in positive_pairs]
    return tuple(d_carries), tuple(t_carries)


def reversed_inversion_ok(c_values: tuple[int, int, int], translated: tuple[int, int, int]) -> bool:
    return translated == tuple((-c_log) % C_ORDER for c_log in reversed(c_values))


def profile_carry_cocycle() -> tuple[CarryCocycleProfile, CandidateProfile, CandidateProfile]:
    true_ring = multiply_factors(formal_factors())
    split_ring = split_formal_shadow()
    target = target_raw_bridge()
    true_candidate = profile_candidate("cyclic_carry_bridge", source_mask_to_raw(true_ring), target)
    split_candidate = profile_candidate("split_no_carry_bridge", source_mask_to_raw(split_ring), target)
    split_q_profile = support_profile(
        "split_no_carry_quotient",
        quotient_mask(quotient_trace(source_mask_to_raw(split_ring))),
    )
    true_c_values = d_order_c_values(use_carry=True)
    split_c_values = d_order_c_values(use_carry=False)
    d_carries, t_carries = carry_sequences()

    profile = CarryCocycleProfile(
        true_support=len(true_ring),
        split_support=len(split_ring),
        same_c13_projection=project_to_c13(true_ring) == project_to_c13(split_ring),
        true_candidate_ok=true_candidate.ok,
        split_trace_correct=split_candidate.trace_correct,
        split_block_constancy_hits=split_candidate.block_constancy_hits,
        split_kernel_modes=split_candidate.kernel_modes,
        split_raw_relation_mismatches=split_candidate.raw_relation_mismatches,
        split_pure_c_characters=split_q_profile.pure_c_nonzero,
        split_mixed_characters=split_q_profile.mixed_nonzero,
        true_positive_classes=source_classes(true_ring, 1),
        true_negative_classes=source_classes(true_ring, -1),
        split_positive_classes=source_classes(split_ring, 1),
        split_negative_classes=source_classes(split_ring, -1),
        true_fiber_counts=fiber_counts(true_ring),
        split_fiber_counts=fiber_counts(split_ring),
        d_carries=d_carries,
        t_carries=t_carries,
        true_t_translate_is_reversed_inversion=reversed_inversion_ok(
            true_c_values,
            t_translate_values(true_c_values, use_carry=True),
        ),
        split_t_translate_is_reversed_inversion=reversed_inversion_ok(
            split_c_values,
            t_translate_values(split_c_values, use_carry=False),
        ),
    )
    return profile, true_candidate, split_candidate


def main() -> int:
    print("p25 Lane B square-axis bridge carry-cocycle gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT} "
        f"C169_low_high=(mod13,fiber)"
    )
    profile, true_candidate, split_candidate = profile_carry_cocycle()
    expected_true_positive = (
        (0, 31, 5, 2, 25),
        (1, 25, 12, 1, 25),
        (2, 28, 2, 2, 25),
    )
    expected_true_negative = (
        (0, 138, 8, 10, 25),
        (1, 141, 11, 10, 25),
        (2, 144, 1, 11, 25),
    )
    expected_split_positive = (
        (0, 18, 5, 1, 25),
        (1, 25, 12, 1, 25),
        (2, 15, 2, 1, 25),
    )
    expected_split_negative = (
        (0, 125, 8, 9, 25),
        (1, 128, 11, 9, 25),
        (2, 118, 1, 9, 25),
    )
    row_ok = (
        profile.true_support == 150
        and profile.split_support == 150
        and profile.same_c13_projection
        and profile.true_candidate_ok
        and not profile.split_trace_correct
        and profile.split_block_constancy_hits == 507
        and profile.split_kernel_modes == (0,)
        and profile.split_raw_relation_mismatches == 0
        and profile.split_pure_c_characters == 168
        and profile.split_mixed_characters == 336
        and profile.true_positive_classes == expected_true_positive
        and profile.true_negative_classes == expected_true_negative
        and profile.split_positive_classes == expected_split_positive
        and profile.split_negative_classes == expected_split_negative
        and profile.true_fiber_counts == ((1, 25), (2, 50), (10, 50), (11, 25))
        and profile.split_fiber_counts == ((1, 75), (9, 75))
        and profile.d_carries == (1, 0)
        and profile.t_carries == (1, 0, 1)
        and profile.true_t_translate_is_reversed_inversion
        and not profile.split_t_translate_is_reversed_inversion
        and true_candidate.ok
        and not split_candidate.ok
    )

    print(f"carry_cocycle_profile={profile}")
    print(f"true_candidate={true_candidate}")
    print(f"split_no_carry_candidate={split_candidate}")
    print("carry_laws")
    print("  write c = c0 + 13*f with c0,f in C13")
    print("  adding D_c=3 from base c=25 has C13 carries (1,0), giving fibers 1,2,2")
    print("  adding T_c=113=9+13*8 has carries (1,0,1), giving negative fibers 10,10,11")
    print("  true T-translate is the reversed inversion of the D-segment")
    print("  split C13xC13 no-carry addition keeps fibers 1 and 9 and breaks that inversion lift")
    print("interpretation")
    print("  C169_extension_carry_is_required_not_optional=1")
    print("  same_C13_shadow_and_full_mixed_characters_do_not_certify_the_bridge=1")
    print("  split_C13xC13_fiber_model_is_a_rejected_producer_control=1")
    print("  arithmetic_realization_must_encode_the_nonsplit_fiber_cocycle=1")
    print(f"square_axis_bridge_carry_cocycle_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_carry_cocycle_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
