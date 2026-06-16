#!/usr/bin/env python3
"""Jacobi-log shadow obstruction gate for p25 Lane B.

The punctured Hasse-Davenport gate supplies a very natural multiplicative
object: the raw and single-anchor-corrected Jacobi-sum packets.  A tempting
producer shortcut is to take discrete logs of those packets in the small value
field and hope that, after harmless scalar/row/column normalizations, the logs
are the required theta_{3,1} half-arc packet.

This gate checks that shortcut on the first C_3 x C_13 lab.  It fails.  The
Jacobi-log shadows have a nontrivial rank-2 mixed payload and full C_13 Fourier
support after row/column normalization, but the mixed payload is not the
canonical half-arc: it has full C-axis coordinate support, violates the
negative-inversion diamond relation, and is not a scalar multiple of the
canonical theta_{3,1} right-character vector.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_c_axis_fourier_payload_gate import c_fourier_support, c_root_powers
from p25_laneB_canonical_half_arc_gate import support_interval
from p25_laneB_diamond_conjugacy_gate import negative_inversion
from p25_laneB_divisor_footprint_gate import packet_matrix, rank_mod
from p25_laneB_literal_jacobi_packet_model import carry_packet
from p25_laneB_punctured_hd_anchor_gate import (
    anchor_corrected,
    make_context,
    packet_values,
    primitive_root,
)
from p25_laneB_ray_local_theta31_pullback_falsifier_gate import quotient_scale
from p25_laneB_right_eigenbasis_gate import right_eigenvectors
from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    raw_producer_conditions,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


C_AXIS = 13
ORDER = RIGHT_DEGREE * C_AXIS


@dataclass(frozen=True)
class ShadowProfile:
    source_name: str
    transform_name: str
    direct_scale: int | None
    direct_selected_defect_ok: bool
    direct_raw_product_ok: bool
    mixed_rank: int
    diamond_conjugacy: bool
    support: tuple[int | None, int | None, int]
    zero_mean: bool
    fourier_support_size: int
    scalar_multiple_of_canonical: bool


def discrete_log_table(modulus: int, generator: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        table[value] = exponent
        value = value * generator % modulus
    if value != 1:
        raise AssertionError("primitive root did not close")
    return table


def row_column_mixed(packet: list[int], c_axis: int, modulus: int) -> list[list[int]]:
    matrix = packet_matrix(packet, c_axis)
    inv_right = pow(RIGHT_DEGREE, -1, modulus)
    inv_c = pow(c_axis, -1, modulus)
    inv_width = pow(RIGHT_DEGREE * c_axis, -1, modulus)
    row_means = [
        sum(matrix[right][c_index] for c_index in range(c_axis)) * inv_c % modulus
        for right in range(RIGHT_DEGREE)
    ]
    column_means = [
        sum(matrix[right][c_index] for right in range(RIGHT_DEGREE))
        * inv_right
        % modulus
        for c_index in range(c_axis)
    ]
    global_mean = sum(packet) * inv_width % modulus
    return [
        [
            (
                matrix[right][c_index]
                - row_means[right]
                - column_means[c_index]
                + global_mean
            )
            % modulus
            for c_index in range(c_axis)
        ]
        for right in range(RIGHT_DEGREE)
    ]


def scalar_ratio(left: list[int], right: list[int], modulus: int) -> int | None:
    ratio: int | None = None
    for left_value, right_value in zip(left, right):
        if right_value % modulus == 0:
            if left_value % modulus:
                return None
            continue
        current = left_value * pow(right_value, -1, modulus) % modulus
        if ratio is None:
            if current == 0:
                return None
            ratio = current
        elif ratio != current:
            return None
    return ratio


def transformed_packets(logs: list[int], modulus: int) -> dict[str, list[int]]:
    return {
        "log_mod_79": [value % modulus for value in logs],
        "log_mod_39": [value % ORDER for value in logs],
        "log_mod_13": [value % C_AXIS for value in logs],
        "39_times_log_mod_79": [(ORDER * value) % modulus for value in logs],
    }


def shadow_profiles() -> list[ShadowProfile]:
    modulus = split_prime_for(ORDER)
    ctx = make_context(ORDER)
    generator = primitive_root(ctx.value_field_l)
    logs = discrete_log_table(ctx.value_field_l, generator)
    q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
    sources = {
        "raw_jacobi": packet_values(ctx, C_AXIS, RIGHT_DEGREE, 1),
        "anchor_corrected_jacobi": anchor_corrected(
            packet_values(ctx, C_AXIS, RIGHT_DEGREE, 1),
            q_minus_2,
            ctx.value_field_l,
        ),
    }
    canonical = carry_packet(C_AXIS, RIGHT_DEGREE, 1, modulus)
    canonical_mixed = row_column_mixed(canonical, C_AXIS, modulus)
    _canonical_e0, canonical_e1, _canonical_e2 = right_eigenvectors(
        canonical_mixed, C_AXIS, modulus
    )
    powers = c_root_powers(C_AXIS, modulus)
    profiles: list[ShadowProfile] = []
    for source_name, values in sources.items():
        source_logs = [logs[value] for value in values]
        for transform_name, packet in transformed_packets(source_logs, modulus).items():
            mixed = row_column_mixed(packet, C_AXIS, modulus)
            _e0, eigen_1, eigen_2 = right_eigenvectors(mixed, C_AXIS, modulus)
            support_1 = c_fourier_support(eigen_1, powers, modulus)
            support_2 = c_fourier_support(eigen_2, powers, modulus)
            profiles.append(
                ShadowProfile(
                    source_name=source_name,
                    transform_name=transform_name,
                    direct_scale=quotient_scale(packet, canonical, modulus),
                    direct_selected_defect_ok=value_conditions_hold(
                        selected_defect(packet, C_AXIS, modulus), C_AXIS, modulus
                    ),
                    direct_raw_product_ok=raw_producer_conditions(
                        packet, C_AXIS, modulus
                    ),
                    mixed_rank=rank_mod([eigen_1, eigen_2], modulus),
                    diamond_conjugacy=eigen_2
                    == negative_inversion(eigen_1, modulus),
                    support=support_interval(eigen_1, modulus),
                    zero_mean=0 not in support_1 and 0 not in support_2,
                    fourier_support_size=len(support_1),
                    scalar_multiple_of_canonical=scalar_ratio(
                        eigen_1, canonical_e1, modulus
                    )
                    is not None,
                )
            )
    return profiles


def main() -> int:
    print("p25 Lane B Jacobi-log shadow obstruction gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"c_axis={C_AXIS} order={ORDER} modulus={split_prime_for(ORDER)}")
    profiles = shadow_profiles()
    ok_rows = 0
    for profile in profiles:
        row_ok = (
            profile.direct_scale is None
            and not profile.direct_selected_defect_ok
            and not profile.direct_raw_product_ok
            and profile.mixed_rank == 2
            and not profile.diamond_conjugacy
            and profile.support == (0, C_AXIS - 1, C_AXIS)
            and profile.zero_mean
            and profile.fourier_support_size == C_AXIS - 1
            and not profile.scalar_multiple_of_canonical
        )
        ok_rows += int(row_ok)
        print(
            f"shadow source={profile.source_name} transform={profile.transform_name} "
            f"direct_scale={profile.direct_scale} "
            f"direct_selected_defect_ok={int(profile.direct_selected_defect_ok)} "
            f"direct_raw_product_ok={int(profile.direct_raw_product_ok)} "
            f"mixed_rank={profile.mixed_rank} "
            f"diamond_conjugacy={int(profile.diamond_conjugacy)} "
            f"support={profile.support} "
            f"zero_mean={int(profile.zero_mean)} "
            f"fourier_support_size={profile.fourier_support_size}/12 "
            f"scalar_multiple_of_canonical={int(profile.scalar_multiple_of_canonical)} "
            f"ok={int(row_ok)}"
        )
    print(f"jacobi_log_shadow_obstruction_rows={ok_rows}/{len(profiles)}")
    print("interpretation")
    print("  naive_discrete_logs_of_raw_or_anchor_corrected_Jacobi_packets_fail=1")
    print("  row_column_normalized_log_shadows_still_have_wrong_half_arc_support=1")
    print("  row_column_normalized_log_shadows_violate_diamond_conjugacy=1")
    print("  natural_Jacobi_log_shadow_is_not_the_missing_ray_local_pullback=1")
    print("conclusion=reported_p25_laneB_jacobi_log_shadow_obstruction_gate")
    return 0 if ok_rows == len(profiles) else 1


if __name__ == "__main__":
    raise SystemExit(main())
