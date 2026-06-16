#!/usr/bin/env python3
"""Raw gauge class for the p25 Robert/Siegel translated odd quotient.

The quotient rigidity gate fixes the visible data:

    base=(1,25), D=(1,3), T=(2,113)

up to reversal of the D-segment.  This gate checks the remaining raw-source
ambiguity on `C_75 x C_169`.  Once the `K_trace` factor is present, changing
the raw representatives of the base, D, or T by the kernel shift `K=(57,0)`
does not change the bridge.  These kernel-gauge choices are valid; simple
non-kernel shifts are not.

So a Robert/Siegel producer may choose any raw representative in the kernel
class, but it may not hide a different raw edge or segment outside that class.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    edge_factor,
    geometric_factor,
    monomial,
    multiply_factors,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class RawGaugeProfile:
    kernel_shift: Coord
    forward_exact_kernel_gauge_count: int
    reverse_exact_kernel_gauge_count: int
    total_exact_kernel_gauge_count: int
    expected_kernel_gauge_count: int
    forward_control_failures: tuple[tuple[str, bool], ...]
    reverse_control_failures: tuple[tuple[str, bool], ...]
    all_kernel_gauges_exact: bool
    non_kernel_controls_fail: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return (
        (left[0] + right[0]) % RIGHT_ORDER,
        (left[1] + right[1]) % C_ORDER,
    )


def scale_coord(step: Coord, scale: int) -> Coord:
    return ((step[0] * scale) % RIGHT_ORDER, (step[1] * scale) % C_ORDER)


def inverse_step(step: Coord) -> Coord:
    return ((-step[0]) % RIGHT_ORDER, (-step[1]) % C_ORDER)


def kernel_class(coord: Coord) -> tuple[Coord, ...]:
    return tuple(add_coord(coord, scale_coord(KERNEL_SHIFT, index)) for index in range(25))


def bridge_word(base: Coord, d_step: Coord, edge_step: Coord) -> Ring:
    return multiply_factors(
        (
            ("base", monomial(base)),
            ("kernel_trace", geometric_factor(KERNEL_SHIFT, 25)),
            ("D_segment", geometric_factor(d_step, 3)),
            ("edge", edge_factor(edge_step)),
        )
    )


def exact_count(base_class: tuple[Coord, ...], d_class: tuple[Coord, ...], edge_class: tuple[Coord, ...]) -> int:
    target = raw_source_mask()
    count = 0
    for base in base_class:
        for d_step in d_class:
            for edge_step in edge_class:
                count += int(bridge_word(base, d_step, edge_step) == target)
    return count


def shifted(coord: Coord, delta: Coord) -> Coord:
    return add_coord(coord, delta)


def control_rows(base: Coord, d_step: Coord, edge_step: Coord) -> tuple[tuple[str, bool], ...]:
    target = raw_source_mask()
    controls = (
        ("base_plus_c1", shifted(base, (0, 1)), d_step, edge_step),
        ("D_plus_c1", base, shifted(d_step, (0, 1)), edge_step),
        ("T_plus_c1", base, d_step, shifted(edge_step, (0, 1))),
        ("base_plus_right1", shifted(base, (1, 0)), d_step, edge_step),
        ("D_plus_right1", base, shifted(d_step, (1, 0)), edge_step),
        ("T_plus_right1", base, d_step, shifted(edge_step, (1, 0))),
    )
    return tuple(
        (name, bridge_word(control_base, control_d, control_edge) == target)
        for name, control_base, control_d, control_edge in controls
    )


def raw_gauge_profile() -> RawGaugeProfile:
    forward_base = BASE_POINT
    forward_d = D_SHIFT
    forward_edge = BRIDGE_SHIFT

    reverse_base = add_coord(BASE_POINT, scale_coord(D_SHIFT, 2))
    reverse_d = inverse_step(D_SHIFT)
    reverse_edge = BRIDGE_SHIFT

    forward_count = exact_count(
        kernel_class(forward_base),
        kernel_class(forward_d),
        kernel_class(forward_edge),
    )
    reverse_count = exact_count(
        kernel_class(reverse_base),
        kernel_class(reverse_d),
        kernel_class(reverse_edge),
    )
    expected = 2 * 25 * 25 * 25
    forward_controls = control_rows(forward_base, forward_d, forward_edge)
    reverse_controls = control_rows(reverse_base, reverse_d, reverse_edge)
    return RawGaugeProfile(
        kernel_shift=KERNEL_SHIFT,
        forward_exact_kernel_gauge_count=forward_count,
        reverse_exact_kernel_gauge_count=reverse_count,
        total_exact_kernel_gauge_count=forward_count + reverse_count,
        expected_kernel_gauge_count=expected,
        forward_control_failures=forward_controls,
        reverse_control_failures=reverse_controls,
        all_kernel_gauges_exact=forward_count + reverse_count == expected,
        non_kernel_controls_fail=not any(value for _name, value in forward_controls + reverse_controls),
    )


def main() -> int:
    print("p25 Lane B Robert/Siegel translated odd quotient raw gauge gate")
    profile = raw_gauge_profile()
    row_ok = (
        profile.kernel_shift == (57, 0)
        and profile.forward_exact_kernel_gauge_count == 25 * 25 * 25
        and profile.reverse_exact_kernel_gauge_count == 25 * 25 * 25
        and profile.total_exact_kernel_gauge_count == profile.expected_kernel_gauge_count
        and profile.all_kernel_gauges_exact
        and profile.non_kernel_controls_fail
    )

    print(f"translated_odd_quotient_raw_gauge_profile={profile}")
    print("raw_gauge_laws")
    print("  base_D_and_T_may_each_shift_by_kernel_class_K=(57,0)=1")
    print("  forward_and_reversed_D_segments_have_25^3_valid_raw_gauges_each=1")
    print("  simple_non_kernel_right_or_C_shifts_fail=1")
    print("interpretation")
    print("  robert_siegel_raw_representative_freedom_is_exactly_kernel_gauge=1")
    print("  no_hidden_raw_edge_or_D_segment_outside_kernel_class=1")
    print(f"robert_translated_odd_quotient_raw_gauge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_translated_odd_quotient_raw_gauge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
