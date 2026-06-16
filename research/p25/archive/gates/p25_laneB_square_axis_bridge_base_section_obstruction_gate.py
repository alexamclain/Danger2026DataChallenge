#!/usr/bin/env python3
"""Right-dependent base-section obstruction for the p25 bridge.

The cocycle-period gate rules out C-only section repairs of the nonsplit
C_169 carry.  This gate closes the next natural escape: allow the C_169 fiber
section to depend on the full visible base C_3 x C_13, not just on C_13.

For the bridge steps D and T, the visible translations on C_3 x C_13 are
single 39-cycles.  Changing section on the base adds a coboundary, whose sum
around that cycle is zero.  The actual C_169 carry totals are nonzero, while a
constant fiber translation would have total 39*c = 0 mod 13.  Therefore no
right-dependent section can split either step into a constant C_13 fiber move.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_bridge_raw_source_character_gate import BRIDGE_SHIFT, D_SHIFT


RIGHT_VISIBLE_ORDER = 3
C_LOW_ORDER = 13
BASE_SIZE = RIGHT_VISIBLE_ORDER * C_LOW_ORDER


BaseCoord = tuple[int, int]


@dataclass(frozen=True)
class BaseSectionStepProfile:
    name: str
    raw_shift: tuple[int, int]
    base_step: BaseCoord
    c_step_fiber: int
    orbit_count: int
    orbit_lengths: tuple[int, ...]
    identity_increment_histogram: tuple[tuple[int, int], ...]
    cycle_increment_total: int
    constant_total_possible: bool
    arbitrary_section_constant_possible: bool
    affine_sections_checked: int
    affine_constant_sections: int
    bilinear_sections_checked: int
    bilinear_constant_sections: int


@dataclass(frozen=True)
class BaseSectionObstructionProfile:
    d_profile: BaseSectionStepProfile
    t_profile: BaseSectionStepProfile
    d_then_t_base_span_size: int
    visible_base_size: int


def add_base(left: BaseCoord, right: BaseCoord) -> BaseCoord:
    return ((left[0] + right[0]) % RIGHT_VISIBLE_ORDER, (left[1] + right[1]) % C_LOW_ORDER)


def carry(low: int, step_low: int) -> int:
    return (low + step_low) // C_LOW_ORDER


def base_step(raw_shift: tuple[int, int]) -> BaseCoord:
    return raw_shift[0] % RIGHT_VISIBLE_ORDER, raw_shift[1] % C_LOW_ORDER


def c_step_fiber(raw_shift: tuple[int, int]) -> int:
    return (raw_shift[1] // C_LOW_ORDER) % C_LOW_ORDER


def base_points() -> tuple[BaseCoord, ...]:
    return tuple((right, low) for right in range(RIGHT_VISIBLE_ORDER) for low in range(C_LOW_ORDER))


def orbit(start: BaseCoord, step: BaseCoord) -> tuple[BaseCoord, ...]:
    out: list[BaseCoord] = []
    seen: set[BaseCoord] = set()
    point = start
    while point not in seen:
        seen.add(point)
        out.append(point)
        point = add_base(point, step)
    return tuple(out)


def orbits(step: BaseCoord) -> tuple[tuple[BaseCoord, ...], ...]:
    unseen = set(base_points())
    out: list[tuple[BaseCoord, ...]] = []
    while unseen:
        current = orbit(min(unseen), step)
        out.append(current)
        unseen.difference_update(current)
    return tuple(out)


def identity_increments(raw_shift: tuple[int, int]) -> tuple[int, ...]:
    step_right, step_low = base_step(raw_shift)
    _ = step_right
    fiber = c_step_fiber(raw_shift)
    return tuple((fiber + carry(low, step_low)) % C_LOW_ORDER for _right, low in base_points())


def histogram(values: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(values).items()))


def section_increment(raw_shift: tuple[int, int], section: dict[BaseCoord, int], point: BaseCoord) -> int:
    step = base_step(raw_shift)
    next_point = add_base(point, step)
    _right, low = point
    return (
        c_step_fiber(raw_shift)
        + carry(low, step[1])
        + section[point]
        - section[next_point]
    ) % C_LOW_ORDER


def is_constant_section(raw_shift: tuple[int, int], section: dict[BaseCoord, int]) -> bool:
    values = {section_increment(raw_shift, section, point) for point in base_points()}
    return len(values) == 1


def affine_sections() -> tuple[dict[BaseCoord, int], ...]:
    return tuple(
        {
            (right, low): (constant + right_coeff * right + low_coeff * low) % C_LOW_ORDER
            for right, low in base_points()
        }
        for constant, right_coeff, low_coeff in product(range(C_LOW_ORDER), repeat=3)
    )


def bilinear_sections() -> tuple[dict[BaseCoord, int], ...]:
    return tuple(
        {
            (right, low): (constant + right_coeff * right + low_coeff * low + mixed_coeff * right * low)
            % C_LOW_ORDER
            for right, low in base_points()
        }
        for constant, right_coeff, low_coeff, mixed_coeff in product(range(C_LOW_ORDER), repeat=4)
    )


def section_counts(raw_shift: tuple[int, int], sections: tuple[dict[BaseCoord, int], ...]) -> int:
    return sum(1 for section in sections if is_constant_section(raw_shift, section))


def step_profile(name: str, raw_shift: tuple[int, int]) -> BaseSectionStepProfile:
    step = base_step(raw_shift)
    orbit_list = orbits(step)
    increments = identity_increments(raw_shift)
    cycle_total = sum(section_increment(raw_shift, {point: 0 for point in base_points()}, point) for point in orbit_list[0]) % C_LOW_ORDER
    constant_total_possible = any((len(orbit_list[0]) * value) % C_LOW_ORDER == cycle_total for value in range(C_LOW_ORDER))
    affine = affine_sections()
    bilinear = bilinear_sections()
    return BaseSectionStepProfile(
        name=name,
        raw_shift=raw_shift,
        base_step=step,
        c_step_fiber=c_step_fiber(raw_shift),
        orbit_count=len(orbit_list),
        orbit_lengths=tuple(sorted(len(item) for item in orbit_list)),
        identity_increment_histogram=histogram(increments),
        cycle_increment_total=cycle_total,
        constant_total_possible=constant_total_possible,
        arbitrary_section_constant_possible=constant_total_possible,
        affine_sections_checked=len(affine),
        affine_constant_sections=section_counts(raw_shift, affine),
        bilinear_sections_checked=len(bilinear),
        bilinear_constant_sections=section_counts(raw_shift, bilinear),
    )


def generated_visible_base_size() -> int:
    generated = {
        ((a * base_step(D_SHIFT)[0] + b * base_step(BRIDGE_SHIFT)[0]) % RIGHT_VISIBLE_ORDER,
         (a * base_step(D_SHIFT)[1] + b * base_step(BRIDGE_SHIFT)[1]) % C_LOW_ORDER)
        for a in range(BASE_SIZE)
        for b in range(BASE_SIZE)
    }
    return len(generated)


def profile_base_section_obstruction() -> BaseSectionObstructionProfile:
    return BaseSectionObstructionProfile(
        d_profile=step_profile("D_segment", D_SHIFT),
        t_profile=step_profile("bridge_edge", BRIDGE_SHIFT),
        d_then_t_base_span_size=generated_visible_base_size(),
        visible_base_size=BASE_SIZE,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge right-dependent base-section obstruction gate")
    profile = profile_base_section_obstruction()
    d_profile = profile.d_profile
    t_profile = profile.t_profile
    row_ok = (
        profile.visible_base_size == 39
        and profile.d_then_t_base_span_size == 39
        and d_profile.raw_shift == (22, 3)
        and d_profile.base_step == (1, 3)
        and d_profile.c_step_fiber == 0
        and d_profile.orbit_count == 1
        and d_profile.orbit_lengths == (39,)
        and d_profile.identity_increment_histogram == ((0, 30), (1, 9))
        and d_profile.cycle_increment_total == 9
        and not d_profile.constant_total_possible
        and not d_profile.arbitrary_section_constant_possible
        and d_profile.affine_sections_checked == 2197
        and d_profile.affine_constant_sections == 0
        and d_profile.bilinear_sections_checked == 28561
        and d_profile.bilinear_constant_sections == 0
        and t_profile.raw_shift == (38, 113)
        and t_profile.base_step == (2, 9)
        and t_profile.c_step_fiber == 8
        and t_profile.orbit_count == 1
        and t_profile.orbit_lengths == (39,)
        and t_profile.identity_increment_histogram == ((8, 12), (9, 27))
        and t_profile.cycle_increment_total == 1
        and not t_profile.constant_total_possible
        and not t_profile.arbitrary_section_constant_possible
        and t_profile.affine_sections_checked == 2197
        and t_profile.affine_constant_sections == 0
        and t_profile.bilinear_sections_checked == 28561
        and t_profile.bilinear_constant_sections == 0
    )

    print(f"base_section_obstruction_profile={profile}")
    print("cycle_laws")
    print("  D and T each act as a single 39-cycle on the visible base C3xC13")
    print("  changing a base section adds a coboundary, whose cycle sum is zero")
    print("  D has total C-fiber carry 9 around the 39-cycle")
    print("  T has total C-fiber carry 1 around the 39-cycle")
    print("  a constant fiber translation would have total 39*c = 0 mod 13")
    print("section_scans")
    print("  right-dependent affine sections checked for D and T: 2197 each, zero repairs")
    print("  right/C bilinear sections checked for D and T: 28561 each, zero repairs")
    print("interpretation")
    print("  right_dependent_section_changes_cannot_split_the_C169_bridge_steps=1")
    print("  base_section_coboundaries_do_not_remove_nonzero_C169_monodromy=1")
    print("  producer_must_realize_the_nonsplit_C169_extension_globally_on_C3xC13=1")
    print("  low_C13_shadow_plus_right_dependent_fiber_gauge_is_not_a_producer=1")
    print(f"square_axis_bridge_base_section_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_base_section_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
