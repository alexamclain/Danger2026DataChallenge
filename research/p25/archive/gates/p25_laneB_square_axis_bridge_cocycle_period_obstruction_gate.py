#!/usr/bin/env python3
"""C_169 cocycle period obstruction for the p25 square-axis bridge.

The local-axis split contrast says the right source splits but the C source
does not.  This gate turns that into a producer-facing invariant: no change of
visible C_13 section can make the bridge's C-side D and T moves into constant
fiber translations.  Around the visible C_13 cycle, the carry sum is nonzero.

Thus a low-degree C_13 shadow plus a clever section is not enough.  A producer
must realize the primitive cyclic C_169 monodromy, or an equivalent identity
with the same nonsplit cocycle.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_bridge_raw_source_gate import source_generators, square_axis_case
from p25_laneB_square_axis_bridge_raw_source_character_gate import BASE_POINT, BRIDGE_SHIFT, C_ORDER, D_SHIFT


C_LOW_ORDER = 13


@dataclass(frozen=True)
class StepSectionProfile:
    name: str
    step_log: int
    step_low: int
    step_fiber: int
    carry_positions: tuple[int, ...]
    carry_sum_mod_13: int
    identity_increment_histogram: tuple[tuple[int, int], ...]
    affine_sections_checked: int
    affine_constant_sections: int
    affine_sum_invariant_hits: int
    quadratic_sections_checked: int
    quadratic_constant_sections: int
    quadratic_sum_invariant_hits: int
    kernel_monodromy_exponent: int
    kernel_monodromy_value: int
    constant_section_possible: bool


@dataclass(frozen=True)
class CocyclePeriodProfile:
    c_modulus: int
    c_generator: int
    base_low: int
    base_fiber: int
    d_profile: StepSectionProfile
    t_profile: StepSectionProfile
    local_d_carries: tuple[int, ...]
    local_t_carries: tuple[int, ...]
    local_positive_fibers: tuple[int, ...]
    local_negative_fibers: tuple[int, ...]


def split_c(c_log: int) -> tuple[int, int]:
    return c_log % C_LOW_ORDER, c_log // C_LOW_ORDER


def carry(low: int, step_low: int) -> int:
    return (low + step_low) // C_LOW_ORDER


def carry_positions(step_low: int) -> tuple[int, ...]:
    return tuple(low for low in range(C_LOW_ORDER) if carry(low, step_low))


def histogram(values: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(values).items()))


def affine_sections() -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((slope * low + offset) % C_LOW_ORDER for low in range(C_LOW_ORDER))
        for slope, offset in product(range(C_LOW_ORDER), repeat=2)
    )


def quadratic_sections() -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((quad * low * low + slope * low + offset) % C_LOW_ORDER for low in range(C_LOW_ORDER))
        for quad, slope, offset in product(range(C_LOW_ORDER), repeat=3)
    )


def transformed_increments(step_low: int, step_fiber: int, section: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        (step_fiber + carry(low, step_low) + section[low] - section[(low + step_low) % C_LOW_ORDER])
        % C_LOW_ORDER
        for low in range(C_LOW_ORDER)
    )


def section_counts(step_low: int, step_fiber: int, sections: tuple[tuple[int, ...], ...]) -> tuple[int, int]:
    constant_count = 0
    invariant_hits = 0
    for section in sections:
        increments = transformed_increments(step_low, step_fiber, section)
        constant_count += int(len(set(increments)) == 1)
        invariant_hits += int(sum(increments) % C_LOW_ORDER == step_low)
    return constant_count, invariant_hits


def step_profile(name: str, step_log: int, c_generator: int, c_modulus: int) -> StepSectionProfile:
    step_low, step_fiber = split_c(step_log)
    identity_section = tuple(0 for _low in range(C_LOW_ORDER))
    identity_increments = transformed_increments(step_low, step_fiber, identity_section)
    affine = affine_sections()
    quadratic = quadratic_sections()
    affine_constant, affine_invariant = section_counts(step_low, step_fiber, affine)
    quadratic_constant, quadratic_invariant = section_counts(step_low, step_fiber, quadratic)
    monodromy_exponent = (C_LOW_ORDER * step_log) % C_ORDER
    return StepSectionProfile(
        name=name,
        step_log=step_log,
        step_low=step_low,
        step_fiber=step_fiber,
        carry_positions=carry_positions(step_low),
        carry_sum_mod_13=sum(carry(low, step_low) for low in range(C_LOW_ORDER)) % C_LOW_ORDER,
        identity_increment_histogram=histogram(identity_increments),
        affine_sections_checked=len(affine),
        affine_constant_sections=affine_constant,
        affine_sum_invariant_hits=affine_invariant,
        quadratic_sections_checked=len(quadratic),
        quadratic_constant_sections=quadratic_constant,
        quadratic_sum_invariant_hits=quadratic_invariant,
        kernel_monodromy_exponent=monodromy_exponent,
        kernel_monodromy_value=pow(c_generator, monodromy_exponent, c_modulus),
        constant_section_possible=affine_constant > 0 or quadratic_constant > 0,
    )


def advance(pair: tuple[int, int], step_log: int) -> tuple[tuple[int, int], int]:
    low, fiber = pair
    step_low, step_fiber = split_c(step_log)
    bit = carry(low, step_low)
    return ((low + step_low) % C_LOW_ORDER, (fiber + step_fiber + bit) % C_LOW_ORDER), bit


def local_carry_data() -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    pair = split_c(BASE_POINT[1])
    positive = [pair]
    d_carries: list[int] = []
    for _index in range(2):
        pair, bit = advance(pair, D_SHIFT[1])
        d_carries.append(bit)
        positive.append(pair)

    t_carries: list[int] = []
    negative: list[tuple[int, int]] = []
    for item in positive:
        translated, bit = advance(item, BRIDGE_SHIFT[1])
        t_carries.append(bit)
        negative.append(translated)
    return (
        tuple(d_carries),
        tuple(t_carries),
        tuple(fiber for _low, fiber in positive),
        tuple(fiber for _low, fiber in negative),
    )


def profile_cocycle_period() -> CocyclePeriodProfile:
    case = square_axis_case()
    _right_generator, c_generator = source_generators(case)
    d_carries, t_carries, positive_fibers, negative_fibers = local_carry_data()
    base_low, base_fiber = split_c(BASE_POINT[1])
    return CocyclePeriodProfile(
        c_modulus=case.c_source.modulus,
        c_generator=c_generator,
        base_low=base_low,
        base_fiber=base_fiber,
        d_profile=step_profile("D_segment", D_SHIFT[1], c_generator, case.c_source.modulus),
        t_profile=step_profile("bridge_edge", BRIDGE_SHIFT[1], c_generator, case.c_source.modulus),
        local_d_carries=d_carries,
        local_t_carries=t_carries,
        local_positive_fibers=positive_fibers,
        local_negative_fibers=negative_fibers,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge C169 cocycle-period obstruction gate")
    profile = profile_cocycle_period()
    d_profile = profile.d_profile
    t_profile = profile.t_profile
    row_ok = (
        profile.c_modulus == 677
        and profile.c_generator == 354
        and profile.base_low == 12
        and profile.base_fiber == 1
        and d_profile.step_log == 3
        and d_profile.step_low == 3
        and d_profile.step_fiber == 0
        and d_profile.carry_positions == (10, 11, 12)
        and d_profile.carry_sum_mod_13 == 3
        and d_profile.identity_increment_histogram == ((0, 10), (1, 3))
        and d_profile.affine_sections_checked == 169
        and d_profile.affine_constant_sections == 0
        and d_profile.affine_sum_invariant_hits == 169
        and d_profile.quadratic_sections_checked == 2197
        and d_profile.quadratic_constant_sections == 0
        and d_profile.quadratic_sum_invariant_hits == 2197
        and d_profile.kernel_monodromy_exponent == 39
        and d_profile.kernel_monodromy_value == 383
        and not d_profile.constant_section_possible
        and t_profile.step_log == 113
        and t_profile.step_low == 9
        and t_profile.step_fiber == 8
        and t_profile.carry_positions == (4, 5, 6, 7, 8, 9, 10, 11, 12)
        and t_profile.carry_sum_mod_13 == 9
        and t_profile.identity_increment_histogram == ((8, 4), (9, 9))
        and t_profile.affine_sections_checked == 169
        and t_profile.affine_constant_sections == 0
        and t_profile.affine_sum_invariant_hits == 169
        and t_profile.quadratic_sections_checked == 2197
        and t_profile.quadratic_constant_sections == 0
        and t_profile.quadratic_sum_invariant_hits == 2197
        and t_profile.kernel_monodromy_exponent == 117
        and t_profile.kernel_monodromy_value == 365
        and not t_profile.constant_section_possible
        and profile.local_d_carries == (1, 0)
        and profile.local_t_carries == (1, 0, 1)
        and profile.local_positive_fibers == (1, 2, 2)
        and profile.local_negative_fibers == (10, 10, 11)
    )

    print(f"cocycle_period_profile={profile}")
    print("period_laws")
    print("  for a step with visible low part s, the C13 carry vector has total s mod 13")
    print("  changing section adds a coboundary, whose total around the C13 cycle is zero")
    print("  therefore no section can make D or T a constant fiber translation")
    print("  the nonzero totals are the C169 kernel monodromies D^13=g^39 and T^13=g^117")
    print("local_bridge_samples")
    print("  D carries on the positive segment are (1,0), giving fibers 1,2,2")
    print("  T carries from the positive segment are (1,0,1), giving negative fibers 10,10,11")
    print("interpretation")
    print("  c13_shadow_plus_section_is_not_a_split_arithmetic_source=1")
    print("  affine_and_quadratic_section_repairs_cannot_remove_the_cocycle_period=1")
    print("  producer_must_encode_the_nonzero_C169_monodromy=1")
    print("  right_axis_trace_can_split_but_C_axis_D_T_moves_cannot=1")
    print(f"square_axis_bridge_cocycle_period_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_cocycle_period_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
