#!/usr/bin/env python3
"""Even-D theta2 gate for the p25 Robert/Kato-Siegel route.

The lit scout identified the classical shape

    wp'(z) = -sigma(2z) / sigma(z)^4

and the corresponding Kato-Siegel-looking object

    theta_2(Q) ~ g(Q)^4 / g(2Q).

This is exactly the normalized-y obstruction already seen locally: theta2 or
its inverse has a 300-cell footprint made from the desired bridge and the
doubled bridge.  This gate checks whether the finite p25 source admits a free
even-D escape via a [2]-norm, a [2]-transport, or an integral square-root /
half-dlog normalization.  It does not; multiplication by 2 is an automorphism
on C_75 x C_169, and the remaining low-support recovery still requires exact
doubled-layer subtraction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_dlog_chain_gate import dlog_chain_footprint
from p25_laneB_robert_ksy_y_doubling_distribution_gate import (
    LambdaScanRow,
    divide_ring_exact,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import (
    add_rings,
    double_pushforward,
    scale_ring,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
)


@dataclass(frozen=True)
class KsyTheta2EvenProfile:
    doubling_kernel_size: int
    theta2_inverse_support: int
    theta2_support: int
    theta2_coefficient_counts: tuple[tuple[int, int], ...]
    theta2_inverse_profile: CandidateProfile
    theta2_profile: CandidateProfile
    theta2_norm_equals_theta2: bool
    theta2_norm_profile: CandidateProfile
    inverse_doubling_theta2_support: int
    inverse_doubling_theta2_profile: CandidateProfile
    theta2_integral_square_root_exists: bool
    theta2_inverse_integral_square_root_exists: bool
    dlog_integral_half_exists: bool
    half_dlog_support: int
    half_dlog_profile: CandidateProfile
    half_dlog_lambda_scan: tuple[LambdaScanRow, ...]
    half_dlog_lambda_minus_one_scaled_bridge_ok: bool
    row_ok: bool


def add_ring_entry(ring: Ring, coord: tuple[int, int], coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def coordinate_scalar_pushforward(ring: Ring, right_scalar: int, c_scalar: int) -> Ring:
    out: Ring = {}
    for coord, coefficient in ring.items():
        add_ring_entry(
            out,
            (
                (coord[0] * right_scalar) % RIGHT_ORDER,
                (coord[1] * c_scalar) % C_ORDER,
            ),
            coefficient,
        )
    return dict(sorted(out.items()))


def integral_division_exists(ring: Ring, divisor: int) -> bool:
    return all(coefficient % divisor == 0 for coefficient in ring.values())


def lambda_scan_rows(footprint: Ring, doubled: Ring) -> tuple[LambdaScanRow, ...]:
    rows: list[LambdaScanRow] = []
    for lambda_value in range(-4, 5):
        combo = add_rings(footprint, scale_ring(doubled, lambda_value))
        profile = bridge_profile(f"ksy_theta2_half_dlog_lambda_{lambda_value}", combo)
        rows.append(
            LambdaScanRow(
                lambda_value=lambda_value,
                support=len(combo),
                quotient_support=profile.quotient_support,
                coefficient_counts=coefficient_counts(combo),
                trace_correct=profile.trace_correct,
                ok=profile.ok,
            )
        )
    return tuple(rows)


def profile_theta2_even() -> KsyTheta2EvenProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    doubled = double_pushforward(bridge)
    theta2_inverse = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2 = scale_ring(theta2_inverse, -1)

    kernel_size = gcd(2, RIGHT_ORDER) * gcd(2, C_ORDER)
    theta2_norm = theta2 if kernel_size == 1 else {}
    inverse_doubling_theta2 = coordinate_scalar_pushforward(
        theta2,
        pow(2, -1, RIGHT_ORDER),
        pow(2, -1, C_ORDER),
    )

    dlog = dlog_chain_footprint(bridge)
    half_dlog = divide_ring_exact(dlog, 2)
    half_dlog_expected = add_rings(doubled, scale_ring(bridge, -2))
    lambda_rows = lambda_scan_rows(half_dlog, doubled)
    lambda_minus_one = add_rings(half_dlog, scale_ring(doubled, -1))
    scaled_bridge = divide_ring_exact(lambda_minus_one, -2)

    theta2_inverse_profile = bridge_profile("ksy_theta2_inverse_y_footprint", theta2_inverse)
    theta2_profile = bridge_profile("ksy_theta2_footprint", theta2)
    theta2_norm_profile = bridge_profile("ksy_theta2_trivial_kernel_norm", theta2_norm)
    inverse_doubling_profile = bridge_profile(
        "ksy_theta2_inverse_doubling_transport",
        inverse_doubling_theta2,
    )
    half_dlog_profile = bridge_profile("ksy_theta2_half_dlog", half_dlog)
    scaled_profile = bridge_profile("ksy_theta2_half_dlog_lambda_minus_one_scaled_bridge", scaled_bridge)

    row_ok = (
        kernel_size == 1
        and theta2_inverse == add_rings(doubled, scale_ring(bridge, -4))
        and theta2 == add_rings(scale_ring(bridge, 4), scale_ring(doubled, -1))
        and len(theta2_inverse) == 300
        and len(theta2) == 300
        and coefficient_counts(theta2) == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and not theta2_inverse_profile.ok
        and not theta2_profile.ok
        and theta2_norm == theta2
        and not theta2_norm_profile.ok
        and len(inverse_doubling_theta2) == 300
        and not inverse_doubling_profile.ok
        and not integral_division_exists(theta2, 2)
        and not integral_division_exists(theta2_inverse, 2)
        and integral_division_exists(dlog, 2)
        and half_dlog == half_dlog_expected
        and len(half_dlog) == 300
        and not half_dlog_profile.ok
        and tuple(row.lambda_value for row in lambda_rows if row.support == 150) == (-1,)
        and not any(row.ok for row in lambda_rows)
        and scaled_profile.ok
    )
    return KsyTheta2EvenProfile(
        doubling_kernel_size=kernel_size,
        theta2_inverse_support=len(theta2_inverse),
        theta2_support=len(theta2),
        theta2_coefficient_counts=coefficient_counts(theta2),
        theta2_inverse_profile=theta2_inverse_profile,
        theta2_profile=theta2_profile,
        theta2_norm_equals_theta2=theta2_norm == theta2,
        theta2_norm_profile=theta2_norm_profile,
        inverse_doubling_theta2_support=len(inverse_doubling_theta2),
        inverse_doubling_theta2_profile=inverse_doubling_profile,
        theta2_integral_square_root_exists=integral_division_exists(theta2, 2),
        theta2_inverse_integral_square_root_exists=integral_division_exists(theta2_inverse, 2),
        dlog_integral_half_exists=integral_division_exists(dlog, 2),
        half_dlog_support=len(half_dlog),
        half_dlog_profile=half_dlog_profile,
        half_dlog_lambda_scan=lambda_rows,
        half_dlog_lambda_minus_one_scaled_bridge_ok=scaled_profile.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel theta2 even-D gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_theta2_even()
    print(f"ksy_theta2_even_profile={profile}")
    print("theta2_even_laws")
    print("  theta2_inverse_y_footprint = double_pushforward(bridge) - 4*bridge")
    print("  theta2_footprint = 4*bridge - double_pushforward(bridge)")
    print("  multiplication_by_2_has_trivial_kernel_on_C75xC169=1")
    print("  theta2_norm_over_2_kernel_equals_theta2_and_still_fails_bridge_contract=1")
    print("  inverse_doubling_transport_preserves_support_300_and_still_fails=1")
    print("  theta2_has_no_integral_square_root_footprint=1")
    print("  dlog_has_integral_half_but_half_dlog_still_has_support_300_and_fails=1")
    print("  half_dlog_requires_lambda_-1_doubled_subtraction_then_divide_by_-2=1")
    print("interpretation")
    print("  even_D_theta2_route_needs_a_real_extra_identity_not_a_formal_2_norm_or_square_root=1")
    print("  continue_only_with_direct_theta2_finite_identity_or_half_trace_normalization=1")
    print(f"robert_ksy_theta2_even_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_even_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
