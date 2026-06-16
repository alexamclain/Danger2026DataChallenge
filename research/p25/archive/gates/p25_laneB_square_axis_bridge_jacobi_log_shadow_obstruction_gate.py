#!/usr/bin/env python3
"""Square-axis bridge Jacobi-log shadow obstruction for p25 Lane B.

The C13 Jacobi-log gate rules out a natural p24-style shortcut for the first
theta_{3,1} lab.  The current moonshot target is sharper: the primitive
square-axis bridge on C_3 x C_169.  This gate repeats the same producer-shaped
test against the actual bridge mask.

Natural discrete-log shadows of the raw and single-anchor-corrected Jacobi
packets have rank two and full C169 Fourier support, but they do not scale to
the six-point bridge.  After row/column normalization they are dense and
violate the bridge inversion relation.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_c_axis_fourier_payload_gate import c_fourier_support, c_root_powers
from p25_laneB_diamond_conjugacy_gate import negative_inversion
from p25_laneB_divisor_footprint_gate import rank_mod
from p25_laneB_jacobi_log_shadow_obstruction_gate import (
    discrete_log_table,
    row_column_mixed,
    scalar_ratio,
)
from p25_laneB_punctured_hd_anchor_gate import (
    anchor_corrected,
    make_context,
    packet_values,
    primitive_root,
)
from p25_laneB_right_eigenbasis_gate import right_eigenvectors
from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import source_bridge_mask
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


C_AXIS = 169
ORDER = RIGHT_DEGREE * C_AXIS
MODULUS = split_prime_for(ORDER)


@dataclass(frozen=True)
class BridgeTargetProfile:
    direct_support: int
    mixed_rank: int
    diamond_conjugacy: bool
    mixed_support: int
    mixed_c_support: int
    e1_support: int
    e2_support: int
    e1_fourier_support: int
    e2_fourier_support: int
    zero_mean: bool


@dataclass(frozen=True)
class BridgeLogShadowProfile:
    source_name: str
    transform_name: str
    direct_support: int
    direct_scale_to_bridge: int | None
    mixed_scale_to_bridge: int | None
    mixed_rank: int
    diamond_conjugacy: bool
    mixed_support: int
    mixed_c_support: int
    e1_support: int
    e2_support: int
    e1_fourier_support: int
    e2_fourier_support: int
    zero_mean: bool


def bridge_target_packet() -> list[int]:
    packet = [0] * ORDER
    for (right, c_index), value in source_bridge_mask().items():
        packet[right * C_AXIS + c_index] = value % MODULUS
    return packet


def mixed_flat(packet: list[int]) -> list[int]:
    return [value for row in row_column_mixed(packet, C_AXIS, MODULUS) for value in row]


def target_profile(packet: list[int]) -> BridgeTargetProfile:
    mixed = row_column_mixed(packet, C_AXIS, MODULUS)
    _e0, eigen_1, eigen_2 = right_eigenvectors(mixed, C_AXIS, MODULUS)
    powers = c_root_powers(C_AXIS, MODULUS)
    support_1 = c_fourier_support(eigen_1, powers, MODULUS)
    support_2 = c_fourier_support(eigen_2, powers, MODULUS)
    return BridgeTargetProfile(
        direct_support=sum(1 for value in packet if value % MODULUS),
        mixed_rank=rank_mod([eigen_1, eigen_2], MODULUS),
        diamond_conjugacy=eigen_2 == negative_inversion(eigen_1, MODULUS),
        mixed_support=sum(1 for row in mixed for value in row if value % MODULUS),
        mixed_c_support=len(
            {
                c_index
                for row in mixed
                for c_index, value in enumerate(row)
                if value % MODULUS
            }
        ),
        e1_support=sum(1 for value in eigen_1 if value % MODULUS),
        e2_support=sum(1 for value in eigen_2 if value % MODULUS),
        e1_fourier_support=len(support_1),
        e2_fourier_support=len(support_2),
        zero_mean=0 not in support_1 and 0 not in support_2,
    )


def transformed_packets(logs: list[int]) -> tuple[tuple[str, list[int]], ...]:
    return (
        ("log_mod_2029", [value % MODULUS for value in logs]),
        ("log_mod_507", [value % ORDER for value in logs]),
        ("log_mod_169", [value % C_AXIS for value in logs]),
        ("507_times_log_mod_2029", [(ORDER * value) % MODULUS for value in logs]),
    )


def shadow_profiles(target: list[int]) -> tuple[BridgeLogShadowProfile, ...]:
    ctx = make_context(ORDER)
    generator = primitive_root(ctx.value_field_l)
    logs = discrete_log_table(ctx.value_field_l, generator)
    q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
    raw_values = packet_values(ctx, C_AXIS, RIGHT_DEGREE, 1)
    sources = (
        ("raw_jacobi", raw_values),
        (
            "anchor_corrected_jacobi",
            anchor_corrected(raw_values, q_minus_2, ctx.value_field_l),
        ),
    )
    target_mixed_flat = mixed_flat(target)
    powers = c_root_powers(C_AXIS, MODULUS)
    profiles: list[BridgeLogShadowProfile] = []
    for source_name, values in sources:
        source_logs = [logs[value] for value in values]
        for transform_name, packet in transformed_packets(source_logs):
            mixed = row_column_mixed(packet, C_AXIS, MODULUS)
            _e0, eigen_1, eigen_2 = right_eigenvectors(mixed, C_AXIS, MODULUS)
            support_1 = c_fourier_support(eigen_1, powers, MODULUS)
            support_2 = c_fourier_support(eigen_2, powers, MODULUS)
            profiles.append(
                BridgeLogShadowProfile(
                    source_name=source_name,
                    transform_name=transform_name,
                    direct_support=sum(1 for value in packet if value % MODULUS),
                    direct_scale_to_bridge=scalar_ratio(packet, target, MODULUS),
                    mixed_scale_to_bridge=scalar_ratio(
                        [value for row in mixed for value in row],
                        target_mixed_flat,
                        MODULUS,
                    ),
                    mixed_rank=rank_mod([eigen_1, eigen_2], MODULUS),
                    diamond_conjugacy=eigen_2 == negative_inversion(eigen_1, MODULUS),
                    mixed_support=sum(1 for row in mixed for value in row if value % MODULUS),
                    mixed_c_support=len(
                        {
                            c_index
                            for row in mixed
                            for c_index, value in enumerate(row)
                            if value % MODULUS
                        }
                    ),
                    e1_support=sum(1 for value in eigen_1 if value % MODULUS),
                    e2_support=sum(1 for value in eigen_2 if value % MODULUS),
                    e1_fourier_support=len(support_1),
                    e2_fourier_support=len(support_2),
                    zero_mean=0 not in support_1 and 0 not in support_2,
                )
            )
    return tuple(profiles)


def main() -> int:
    print("p25 Lane B square-axis bridge Jacobi-log shadow obstruction gate")
    ctx = make_context(ORDER)
    print(
        f"c_axis={C_AXIS} order={ORDER} modulus={MODULUS} "
        f"jacobi_base_q={ctx.base_field_q} jacobi_value_l={ctx.value_field_l}"
    )
    target = bridge_target_packet()
    bridge_profile = target_profile(target)
    profiles = shadow_profiles(target)
    expected_target = BridgeTargetProfile(
        direct_support=6,
        mixed_rank=2,
        diamond_conjugacy=True,
        mixed_support=18,
        mixed_c_support=6,
        e1_support=6,
        e2_support=6,
        e1_fourier_support=168,
        e2_fourier_support=168,
        zero_mean=True,
    )
    expected_profiles = (
        BridgeLogShadowProfile("raw_jacobi", "log_mod_2029", 507, None, None, 2, False, 506, 169, 169, 169, 168, 168, True),
        BridgeLogShadowProfile("raw_jacobi", "log_mod_507", 504, None, None, 2, False, 506, 169, 168, 169, 168, 168, True),
        BridgeLogShadowProfile("raw_jacobi", "log_mod_169", 501, None, None, 2, False, 507, 169, 169, 169, 168, 168, True),
        BridgeLogShadowProfile("raw_jacobi", "507_times_log_mod_2029", 507, None, None, 2, False, 506, 169, 169, 169, 168, 168, True),
        BridgeLogShadowProfile("anchor_corrected_jacobi", "log_mod_2029", 506, None, None, 2, False, 506, 169, 169, 169, 168, 166, True),
        BridgeLogShadowProfile("anchor_corrected_jacobi", "log_mod_507", 503, None, None, 2, False, 506, 169, 169, 169, 168, 168, True),
        BridgeLogShadowProfile("anchor_corrected_jacobi", "log_mod_169", 500, None, None, 2, False, 506, 169, 169, 169, 167, 168, True),
        BridgeLogShadowProfile("anchor_corrected_jacobi", "507_times_log_mod_2029", 506, None, None, 2, False, 506, 169, 169, 169, 168, 166, True),
    )
    row_ok = bridge_profile == expected_target and profiles == expected_profiles

    print(f"bridge_target_profile={bridge_profile}")
    print("shadow_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("bridge_contract_comparison")
    print("  target direct support is six signed bridge points; target mixed support is eighteen cells")
    print("  log shadows have rank two and full nontrivial C169 Fourier mass, so frequency tests alone are too weak")
    print("  every log shadow is dense after row/column normalization and has no direct or mixed scalar to the bridge")
    print("  every log shadow violates the bridge inversion/diamond conjugacy relation")
    print("interpretation")
    print("  square_axis_bridge_is_not_the_natural_Jacobi_log_shadow=1")
    print("  anchor_correction_does_not_recover_the_primitive_bridge=1")
    print("  full_C169_fourier_support_does_not_certify_a_bridge_producer=1")
    print("  producer_must_add_a_new_mixed_correction_not_plain_Jacobi_logs=1")
    print(f"square_axis_bridge_jacobi_log_shadow_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_jacobi_log_shadow_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
