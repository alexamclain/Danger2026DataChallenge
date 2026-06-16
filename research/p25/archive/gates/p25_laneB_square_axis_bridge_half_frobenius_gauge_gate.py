#!/usr/bin/env python3
"""Half-Frobenius raw gauge law for the p25 primitive bridge.

The twisted-orientation gate works on the collapsed C_507 bridge: p^39 acts
as q -> -q and reverses the signed bridge.  This gate records the same action
on the actual raw source coordinates C_75 x C_169.

The key point is that p^39 is not a plain bridge translation in the raw
source.  It acts as

    (right, c) -> (2 * right, -c)

and maps the positive bridge layer to the negative layer only after permuting
the full C_25 kernel trace and reversing the three-term D segment.  Thus the
degree-39 orientation contract really uses the full K-trace and the equal
S-layer bridge; a sparse kernel section or unrelated orientation cannot be
silently substituted.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import solve_d_exponent
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    RAW_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class FactorGaugeRow:
    name: str
    coord: Coord
    p39_image: Coord
    p78_image: Coord
    d_exponent: int
    p39_d_exponent: int
    p78_d_exponent: int


@dataclass(frozen=True)
class TransitionLaw:
    power: int
    source_layer: str
    target_layer: str
    raw_multiplier: int
    kernel_index_multiplier: int
    i_map: tuple[tuple[int, int], ...]
    offsets_by_i: tuple[tuple[int, int], ...]
    single_kernel_section_image_indices: tuple[int, ...]
    rows_checked: int
    rows_matching_formula: int
    full_kernel_trace_preserved_by_each_i: bool


@dataclass(frozen=True)
class HalfFrobeniusGaugeProfile:
    p39_raw: int
    p39_quotient: int
    p39_right_action: int
    p39_c_action: int
    p78_raw: int
    p78_quotient: int
    p78_right_action: int
    p78_c_action: int
    factor_rows: tuple[FactorGaugeRow, ...]
    transition_laws: tuple[TransitionLaw, ...]
    p39_positive_to_negative: bool
    p39_negative_to_positive: bool
    p78_positive_preserved: bool
    p78_negative_preserved: bool
    p39_is_raw_bridge_translation: bool
    p39_is_quotient_inversion: bool
    p78_is_quotient_identity_kernel_gauge: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def scale_coord(step: Coord, count: int) -> Coord:
    return ((step[0] * count) % RIGHT_ORDER, (step[1] * count) % C_ORDER)


def multiply_coord(coord: Coord, multiplier: int) -> Coord:
    return ((coord[0] * multiplier) % RIGHT_ORDER, (coord[1] * multiplier) % C_ORDER)


def layer_points(layer: str) -> dict[Coord, tuple[int, int]]:
    if layer not in {"positive", "negative"}:
        raise ValueError(f"bad layer {layer}")
    bridge = (0, 0) if layer == "positive" else BRIDGE_SHIFT
    out: dict[Coord, tuple[int, int]] = {}
    for kernel_index in range(25):
        for d_index in range(3):
            coord = add_coord(
                add_coord(
                    add_coord(BASE_POINT, scale_coord(KERNEL_SHIFT, kernel_index)),
                    scale_coord(D_SHIFT, d_index),
                ),
                bridge,
            )
            out[coord] = (kernel_index, d_index)
    if len(out) != 75:
        raise AssertionError(f"{layer} layer parameterization collided")
    return out


def kernel_index_multiplier(raw_multiplier: int) -> int:
    image = multiply_coord(KERNEL_SHIFT, raw_multiplier)
    for index in range(25):
        if scale_coord(KERNEL_SHIFT, index) == image:
            return index
    raise AssertionError("Frobenius image of K is outside the K trace subgroup")


def transition_law(power: int, source_layer: str) -> TransitionLaw:
    raw_multiplier = pow(P25 % RAW_ORDER, power, RAW_ORDER)
    if power == 39:
        target_layer = "negative" if source_layer == "positive" else "positive"
    elif power == 78:
        target_layer = source_layer
    else:
        raise ValueError("this gate only records p^39 and p^78")

    source = layer_points(source_layer)
    target = layer_points(target_layer)
    k_mult = kernel_index_multiplier(raw_multiplier)
    transitions: list[tuple[int, int, int, int]] = []
    for coord, (kernel_index, d_index) in source.items():
        image = multiply_coord(coord, raw_multiplier)
        if image not in target:
            continue
        target_kernel, target_d = target[image]
        transitions.append((kernel_index, d_index, target_kernel, target_d))

    i_map = tuple(sorted({(d_index, target_d) for _, d_index, _, target_d in transitions}))
    offsets_by_i_rows: list[tuple[int, int]] = []
    rows_matching = 0
    for d_index in range(3):
        rows = [
            (kernel_index, target_kernel, target_d)
            for kernel_index, source_d, target_kernel, target_d in transitions
            if source_d == d_index
        ]
        offsets = {
            (target_kernel - k_mult * kernel_index) % 25
            for kernel_index, target_kernel, _ in rows
        }
        if len(offsets) != 1:
            raise AssertionError(f"non-affine kernel transition for d={d_index}")
        offset = next(iter(offsets))
        offsets_by_i_rows.append((d_index, offset))
        for kernel_index, target_kernel, target_d in rows:
            expected_d = 2 - d_index if power == 39 else d_index
            expected_kernel = (k_mult * kernel_index + offset) % 25
            rows_matching += int(target_d == expected_d and target_kernel == expected_kernel)

    single_kernel_indices = tuple(
        sorted(
            {
                target_kernel
                for kernel_index, _, target_kernel, _ in transitions
                if kernel_index == 0
            }
        )
    )
    full_trace_ok = all(
        {
            target_kernel
            for kernel_index, source_d, target_kernel, _ in transitions
            if source_d == d_index
        }
        == set(range(25))
        for d_index in range(3)
    )
    return TransitionLaw(
        power=power,
        source_layer=source_layer,
        target_layer=target_layer,
        raw_multiplier=raw_multiplier,
        kernel_index_multiplier=k_mult,
        i_map=i_map,
        offsets_by_i=tuple(offsets_by_i_rows),
        single_kernel_section_image_indices=single_kernel_indices,
        rows_checked=len(source),
        rows_matching_formula=rows_matching,
        full_kernel_trace_preserved_by_each_i=full_trace_ok,
    )


def factor_row(name: str, coord: Coord, p39_raw: int, p78_raw: int) -> FactorGaugeRow:
    d_exponent = solve_d_exponent(coord)
    return FactorGaugeRow(
        name=name,
        coord=coord,
        p39_image=multiply_coord(coord, p39_raw),
        p78_image=multiply_coord(coord, p78_raw),
        d_exponent=d_exponent,
        p39_d_exponent=(p39_raw * d_exponent) % RAW_ORDER,
        p78_d_exponent=(p78_raw * d_exponent) % RAW_ORDER,
    )


def profile_half_frobenius_gauge() -> HalfFrobeniusGaugeProfile:
    p39_raw = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    p78_raw = pow(P25 % RAW_ORDER, 78, RAW_ORDER)
    positive = set(layer_points("positive"))
    negative = set(layer_points("negative"))
    p39_positive = {multiply_coord(coord, p39_raw) for coord in positive}
    p39_negative = {multiply_coord(coord, p39_raw) for coord in negative}
    p78_positive = {multiply_coord(coord, p78_raw) for coord in positive}
    p78_negative = {multiply_coord(coord, p78_raw) for coord in negative}
    factor_rows = (
        factor_row("base", BASE_POINT, p39_raw, p78_raw),
        factor_row("kernel_trace", KERNEL_SHIFT, p39_raw, p78_raw),
        factor_row("D_segment", D_SHIFT, p39_raw, p78_raw),
        factor_row("bridge_edge", BRIDGE_SHIFT, p39_raw, p78_raw),
        factor_row("Y_raw", (9, 9), p39_raw, p78_raw),
        factor_row("D_cubed", scale_coord(D_SHIFT, 3), p39_raw, p78_raw),
    )
    return HalfFrobeniusGaugeProfile(
        p39_raw=p39_raw,
        p39_quotient=p39_raw % QUOTIENT_ORDER,
        p39_right_action=p39_raw % RIGHT_ORDER,
        p39_c_action=p39_raw % C_ORDER,
        p78_raw=p78_raw,
        p78_quotient=p78_raw % QUOTIENT_ORDER,
        p78_right_action=p78_raw % RIGHT_ORDER,
        p78_c_action=p78_raw % C_ORDER,
        factor_rows=factor_rows,
        transition_laws=(
            transition_law(39, "positive"),
            transition_law(39, "negative"),
            transition_law(78, "positive"),
            transition_law(78, "negative"),
        ),
        p39_positive_to_negative=p39_positive == negative,
        p39_negative_to_positive=p39_negative == positive,
        p78_positive_preserved=p78_positive == positive,
        p78_negative_preserved=p78_negative == negative,
        p39_is_raw_bridge_translation=p39_raw % RAW_ORDER == BRIDGE_SHIFT[0] % RAW_ORDER,
        p39_is_quotient_inversion=p39_raw % QUOTIENT_ORDER == QUOTIENT_ORDER - 1,
        p78_is_quotient_identity_kernel_gauge=(
            p78_raw % QUOTIENT_ORDER == 1
            and p78_raw % RIGHT_ORDER == 4
            and p78_raw % C_ORDER == 1
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge half-Frobenius raw-gauge gate")
    profile = profile_half_frobenius_gauge()
    expected_factors = (
        FactorGaugeRow("base", (25, 25), (50, 144), (25, 25), 11275, 1400, 11275),
        FactorGaugeRow("kernel_trace", (57, 0), (39, 0), (3, 0), 4056, 8112, 3549),
        FactorGaugeRow("D_segment", (22, 3), (44, 166), (13, 3), 1, 2027, 2029),
        FactorGaugeRow("bridge_edge", (38, 113), (1, 56), (2, 113), 6854, 1258, 2291),
        FactorGaugeRow("Y_raw", (9, 9), (18, 160), (36, 9), 8622, 10644, 2538),
        FactorGaugeRow("D_cubed", (66, 9), (57, 160), (39, 9), 3, 6081, 6087),
    )
    expected_transitions = (
        TransitionLaw(39, "positive", "negative", 2027, 2, ((0, 2), (1, 1), (2, 0)), ((0, 24), (1, 12), (2, 0)), (0, 12, 24), 75, 75, True),
        TransitionLaw(39, "negative", "positive", 2027, 2, ((0, 2), (1, 1), (2, 0)), ((0, 1), (1, 14), (2, 2)), (1, 2, 14), 75, 75, True),
        TransitionLaw(78, "positive", "positive", 2029, 4, ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 13), (2, 1)), (0, 1, 13), 75, 75, True),
        TransitionLaw(78, "negative", "negative", 2029, 4, ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 15), (2, 3)), (2, 3, 15), 75, 75, True),
    )
    row_ok = (
        profile.p39_raw == 2027
        and profile.p39_quotient == 506
        and profile.p39_right_action == 2
        and profile.p39_c_action == 168
        and profile.p78_raw == 2029
        and profile.p78_quotient == 1
        and profile.p78_right_action == 4
        and profile.p78_c_action == 1
        and profile.factor_rows == expected_factors
        and profile.transition_laws == expected_transitions
        and profile.p39_positive_to_negative
        and profile.p39_negative_to_positive
        and profile.p78_positive_preserved
        and profile.p78_negative_preserved
        and not profile.p39_is_raw_bridge_translation
        and profile.p39_is_quotient_inversion
        and profile.p78_is_quotient_identity_kernel_gauge
    )

    print(f"half_frobenius_gauge_profile={profile}")
    print("raw_source_action")
    print("  p^39: (right,c) -> (2*right, -c) on C75 x C169")
    print("  p^78: (right,c) -> (4*right, c), quotient identity plus C25 kernel gauge")
    print("transition_laws")
    print("  p^39 positive (j,i) -> negative (2*j + offset_i, 2-i), offsets 24,12,0")
    print("  p^39 negative (j,i) -> positive (2*j + offset_i, 2-i), offsets 1,14,2")
    print("  p^78 preserves signs but still gauges the kernel trace")
    print("interpretation")
    print("  half_frobenius_orientation_uses_full_C25_kernel_trace=1")
    print("  half_frobenius_orientation_reverses_the_three_term_D_segment=1")
    print("  sparse_kernel_section_is_not_stable_under_the_half_frobenius_gauge=1")
    print("  quadratic_sign_local_system_must_be_compatible_with_this_raw_gauge=1")
    print(f"square_axis_bridge_half_frobenius_gauge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_half_frobenius_gauge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
