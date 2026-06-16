#!/usr/bin/env python3
"""Raw K-trace reflection lift for the p25 KL/KSY packet.

The quotient reflection bridge has T=-2C in C3 x C169.  The actual KSY source
product lives upstairs in C75 x C169 with a forced 25-point K trace.  There the
literal relation is

    T = -2C + K.

This gate checks that the K trace absorbs exactly that kernel offset: every
kernel-shifted representative of -2C gives the same traced source packet and
the same normalized-y theta2 footprint, while non-kernel shifts, a sparse K
section, or a truncated D segment fail.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
    source_centers,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class RawReflectionSample:
    offset: int
    k_index: int
    numerator: Coord
    t_denominator: Coord
    reflected_offset: int
    reflected_k_index: int
    reflected_numerator: Coord
    reflected_inverse: Coord
    denominator_match: bool


@dataclass(frozen=True)
class RawKTraceReflectionProfile:
    base: Coord
    d_step: Coord
    k_step: Coord
    t_step: Coord
    center: Coord
    negative_double_center: Coord
    t_minus_negative_double_center: Coord
    t_kernel_offset: int
    half_t: Coord
    negative_center: Coord
    half_t_minus_negative_center: Coord
    half_t_kernel_offset: int
    center_support: int
    source_packet_support: int
    normalized_y_footprint_support: int
    t_packet_equals_inversion_packet: bool
    t_footprint_equals_inversion_footprint: bool
    negative_double_center_footprint_equals_t: bool
    kernel_shifted_t_representatives_ok: int
    nonkernel_t_controls_rejected: tuple[tuple[str, bool], ...]
    sparse_k_section_rejected: bool
    truncated_d_segment_rejected: bool
    raw_reflection_samples: tuple[RawReflectionSample, ...]
    next_debt: str
    row_ok: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def sub_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] - right[0]) % RIGHT_ORDER, (left[1] - right[1]) % C_ORDER)


def scale_coord(step: Coord, scale: int) -> Coord:
    return ((step[0] * scale) % RIGHT_ORDER, (step[1] * scale) % C_ORDER)


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % RIGHT_ORDER, (-coord[1]) % C_ORDER)


def half_coord(coord: Coord) -> Coord:
    return (
        (coord[0] * pow(2, -1, RIGHT_ORDER)) % RIGHT_ORDER,
        (coord[1] * pow(2, -1, C_ORDER)) % C_ORDER,
    )


def add_packet_entry(packet: Ring, coord: Coord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def source_packet_from_denominator(centers: Ring, denominator) -> Ring:
    packet: Ring = {}
    for point, coefficient in centers.items():
        add_packet_entry(packet, point, coefficient)
        add_packet_entry(packet, denominator(point), -coefficient)
    return dict(sorted(packet.items()))


def y_exponent_at(out: Ring, point: Coord, coefficient: int) -> None:
    add_packet_entry(out, scale_coord(point, 2), coefficient)
    add_packet_entry(out, point, -4 * coefficient)


def normalized_y_footprint_from_denominator(centers: Ring, denominator) -> Ring:
    out: Ring = {}
    for point, coefficient in centers.items():
        y_exponent_at(out, point, coefficient)
        y_exponent_at(out, denominator(point), -coefficient)
    return dict(sorted(out.items()))


def trace_shift_offset(step: Coord) -> int | None:
    for index in range(25):
        if scale_coord(KERNEL_SHIFT, index) == step:
            return index
    return None


def raw_segment(center: Coord, k_index: int, offset: int) -> Coord:
    return add_coord(
        add_coord(center, scale_coord(D_SHIFT, offset)),
        scale_coord(KERNEL_SHIFT, k_index),
    )


def sample_reflection_rows(center: Coord, t_step: Coord) -> tuple[RawReflectionSample, ...]:
    rows: list[RawReflectionSample] = []
    for offset in (-1, 0, 1):
        k_index = 0
        numerator = raw_segment(center, k_index, offset)
        t_denominator = add_coord(numerator, t_step)
        reflected_offset = -offset
        reflected_k_index = (-k_index - 1) % 25
        reflected_numerator = raw_segment(center, reflected_k_index, reflected_offset)
        reflected_inverse = inverse_coord(reflected_numerator)
        rows.append(
            RawReflectionSample(
                offset=offset,
                k_index=k_index,
                numerator=numerator,
                t_denominator=t_denominator,
                reflected_offset=reflected_offset,
                reflected_k_index=reflected_k_index,
                reflected_numerator=reflected_numerator,
                reflected_inverse=reflected_inverse,
                denominator_match=t_denominator == reflected_inverse,
            )
        )
    return tuple(rows)


def profile_raw_ktrace_reflection() -> RawKTraceReflectionProfile:
    center = add_coord(BASE_POINT, D_SHIFT)
    negative_double_center = inverse_coord(scale_coord(center, 2))
    t_minus_negative_double_center = sub_coord(BRIDGE_SHIFT, negative_double_center)
    t_kernel_offset = trace_shift_offset(t_minus_negative_double_center)
    half_t = half_coord(BRIDGE_SHIFT)
    negative_center = inverse_coord(center)
    half_t_minus_negative_center = sub_coord(half_t, negative_center)
    half_t_kernel_offset = trace_shift_offset(half_t_minus_negative_center)

    centers = source_centers(BASE_POINT, KERNEL_SHIFT, D_SHIFT, 25, 3)
    t_source_packet = source_packet_from_denominator(
        centers, lambda point: add_coord(point, BRIDGE_SHIFT)
    )
    inversion_source_packet = source_packet_from_denominator(centers, inverse_coord)
    t_footprint = normalized_y_product_footprint(
        BASE_POINT, KERNEL_SHIFT, D_SHIFT, BRIDGE_SHIFT
    )
    inversion_footprint = normalized_y_footprint_from_denominator(centers, inverse_coord)
    negative_double_footprint = normalized_y_product_footprint(
        BASE_POINT, KERNEL_SHIFT, D_SHIFT, negative_double_center
    )

    kernel_shifted_ok = 0
    for index in range(25):
        shifted_t = add_coord(negative_double_center, scale_coord(KERNEL_SHIFT, index))
        shifted_packet = source_packet_from_denominator(
            centers, lambda point, step=shifted_t: add_coord(point, step)
        )
        kernel_shifted_ok += int(shifted_packet == inversion_source_packet)

    nonkernel_controls = (
        (
            "T_plus_D",
            source_packet_from_denominator(
                centers,
                lambda point: add_coord(point, add_coord(BRIDGE_SHIFT, D_SHIFT)),
            )
            != inversion_source_packet,
        ),
        (
            "T_plus_C_axis",
            source_packet_from_denominator(
                centers,
                lambda point: add_coord(point, add_coord(BRIDGE_SHIFT, (0, 1))),
            )
            != inversion_source_packet,
        ),
        (
            "T_plus_right_axis",
            source_packet_from_denominator(
                centers,
                lambda point: add_coord(point, add_coord(BRIDGE_SHIFT, (1, 0))),
            )
            != inversion_source_packet,
        ),
    )
    sparse_centers = source_centers(BASE_POINT, KERNEL_SHIFT, D_SHIFT, 1, 3)
    truncated_centers = source_centers(BASE_POINT, KERNEL_SHIFT, D_SHIFT, 25, 2)
    sparse_rejected = source_packet_from_denominator(
        sparse_centers, lambda point: add_coord(point, BRIDGE_SHIFT)
    ) != source_packet_from_denominator(sparse_centers, inverse_coord)
    truncated_rejected = source_packet_from_denominator(
        truncated_centers, lambda point: add_coord(point, BRIDGE_SHIFT)
    ) != source_packet_from_denominator(truncated_centers, inverse_coord)

    row_ok = (
        center == (47, 28)
        and negative_double_center == (56, 113)
        and t_minus_negative_double_center == KERNEL_SHIFT
        and t_kernel_offset == 1
        and half_t == (19, 141)
        and negative_center == (28, 141)
        and half_t_minus_negative_center == (66, 0)
        and half_t_kernel_offset == 13
        and len(centers) == 75
        and len(t_source_packet) == 150
        and len(t_footprint) == 300
        and t_source_packet == inversion_source_packet
        and t_footprint == inversion_footprint == negative_double_footprint
        and kernel_shifted_ok == 25
        and all(rejected for _name, rejected in nonkernel_controls)
        and sparse_rejected
        and truncated_rejected
        and all(row.denominator_match for row in sample_reflection_rows(center, BRIDGE_SHIFT))
    )
    return RawKTraceReflectionProfile(
        base=BASE_POINT,
        d_step=D_SHIFT,
        k_step=KERNEL_SHIFT,
        t_step=BRIDGE_SHIFT,
        center=center,
        negative_double_center=negative_double_center,
        t_minus_negative_double_center=t_minus_negative_double_center,
        t_kernel_offset=t_kernel_offset if t_kernel_offset is not None else -1,
        half_t=half_t,
        negative_center=negative_center,
        half_t_minus_negative_center=half_t_minus_negative_center,
        half_t_kernel_offset=half_t_kernel_offset if half_t_kernel_offset is not None else -1,
        center_support=len(centers),
        source_packet_support=len(t_source_packet),
        normalized_y_footprint_support=len(t_footprint),
        t_packet_equals_inversion_packet=t_source_packet == inversion_source_packet,
        t_footprint_equals_inversion_footprint=t_footprint == inversion_footprint,
        negative_double_center_footprint_equals_t=t_footprint == negative_double_footprint,
        kernel_shifted_t_representatives_ok=kernel_shifted_ok,
        nonkernel_t_controls_rejected=nonkernel_controls,
        sparse_k_section_rejected=sparse_rejected,
        truncated_d_segment_rejected=truncated_rejected,
        raw_reflection_samples=sample_reflection_rows(center, BRIDGE_SHIFT),
        next_debt=(
            "prove a theorem-side raw K-traced anti-invariant quotient; the "
            "finite K trace absorbs the T=-2C kernel offset, but the "
            "arithmetic producer still has to realize the K trace itself"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang raw K-trace reflection gate")
    profile = profile_raw_ktrace_reflection()
    print(f"raw_ktrace_reflection_profile={profile}")
    print("raw_reflection_law")
    print(
        "  "
        f"C={profile.center} -2C={profile.negative_double_center} "
        f"T={profile.t_step} T-(-2C)={profile.t_minus_negative_double_center} "
        f"kernel_offset={profile.t_kernel_offset}"
    )
    print(
        "  "
        f"T/2={profile.half_t} -C={profile.negative_center} "
        f"T/2-(-C)={profile.half_t_minus_negative_center} "
        f"half_kernel_offset={profile.half_t_kernel_offset}"
    )
    print("sample_denominator_matches")
    for row in profile.raw_reflection_samples:
        print(f"  {row}")
    print("payload_checks")
    print(f"  center_support={profile.center_support}")
    print(f"  source_packet_support={profile.source_packet_support}")
    print(f"  normalized_y_footprint_support={profile.normalized_y_footprint_support}")
    print(f"  kernel_shifted_t_representatives_ok={profile.kernel_shifted_t_representatives_ok}/25")
    print(f"  nonkernel_t_controls_rejected={profile.nonkernel_t_controls_rejected}")
    print("interpretation")
    print("  raw_T_equals_negative_double_center_plus_one_K_step=1")
    print("  K_trace_absorbs_all_25_kernel_shifted_negative_double_center_representatives=1")
    print("  raw_T_edge_source_packet_equals_raw_inversion_pair_source_packet=1")
    print("  normalized_y_theta2_footprint_is_unchanged_by_the_reflection_lift=1")
    print("  sparse_K_section_truncated_D_and_nonkernel_T_shifts_are_rejected=1")
    print(f"robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
