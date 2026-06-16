#!/usr/bin/env python3
"""Finite dlog chain-rule gate for the p25 KSY/Kato-Siegel route.

For the normalized Koo-Shin-Yoon coordinate

    y(Q) = -g(2Q) / g(Q)^4,

the exponent footprint is `double_pushforward(bridge) - 4*bridge`.  A
logarithmic derivative in the source variable adds the chain-rule factor on the
`g(2Q)` term:

    dlog footprint = 2*double_pushforward(bridge) - 4*bridge.

This gate checks whether that chain-rule factor cancels the doubled layer for
free.  It does not; it merely changes the exact subtraction needed from
`-1*doubled` to `-2*doubled`.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_ksy_y_doubling_distribution_gate import (
    LambdaScanRow,
    divide_ring_exact,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
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
class KsyDlogChainProfile:
    dlog_support: int
    dlog_coefficient_counts: tuple[tuple[int, int], ...]
    dlog_profile: CandidateProfile
    high_weight_layer_profile: CandidateProfile
    low_weight_layer_profile: CandidateProfile
    dlog_equals_two_doubled_minus_four_bridge: bool
    lambda_scan: tuple[LambdaScanRow, ...]
    lambda_minus_two_scaled_bridge_ok: bool
    row_ok: bool


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def dlog_chain_footprint(bridge: Ring) -> Ring:
    return add_rings(
        scale_ring(double_pushforward(bridge), 2),
        scale_ring(bridge, -4),
    )


def high_weight_bridge_layer(footprint: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in footprint.items():
        if abs(coefficient) == 4:
            if coefficient % -4:
                raise AssertionError("unexpected coefficient in high-weight dlog layer")
            out[coord] = coefficient // -4
    return dict(sorted(out.items()))


def low_weight_doubled_layer(footprint: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in footprint.items():
        if abs(coefficient) == 2:
            if coefficient % 2:
                raise AssertionError("unexpected coefficient in low-weight dlog layer")
            out[coord] = coefficient // 2
    return dict(sorted(out.items()))


def lambda_scan_rows(footprint: Ring, doubled: Ring) -> tuple[LambdaScanRow, ...]:
    rows: list[LambdaScanRow] = []
    for lambda_value in range(-6, 7):
        combo = add_rings(footprint, scale_ring(doubled, lambda_value))
        profile = bridge_profile(f"ksy_dlog_lambda_{lambda_value}_doubled_combo", combo)
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


def profile_dlog_chain() -> KsyDlogChainProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    doubled = double_pushforward(bridge)
    footprint = dlog_chain_footprint(bridge)
    expected = add_rings(scale_ring(doubled, 2), scale_ring(bridge, -4))

    high_layer = high_weight_bridge_layer(footprint)
    low_layer = low_weight_doubled_layer(footprint)
    dlog_profile = bridge_profile("ksy_dlog_chain_footprint", footprint)
    high_profile = bridge_profile("ksy_dlog_high_weight_layer_scaled_bridge", high_layer)
    low_profile = bridge_profile("ksy_dlog_low_weight_doubled_layer", low_layer)
    lambda_rows = lambda_scan_rows(footprint, doubled)
    lambda_minus_two = add_rings(footprint, scale_ring(doubled, -2))
    scaled_bridge = divide_ring_exact(lambda_minus_two, -4)
    scaled_profile = bridge_profile("ksy_dlog_lambda_minus_two_scaled_bridge", scaled_bridge)

    row_ok = (
        footprint == expected
        and len(footprint) == 300
        and coefficient_counts(footprint) == ((-4, 75), (-2, 75), (2, 75), (4, 75))
        and not dlog_profile.ok
        and dlog_profile.raw_support == 300
        and dlog_profile.quotient_support == 12
        and high_layer == bridge
        and high_profile.ok
        and low_layer == doubled
        and not low_profile.ok
        and low_profile.raw_support == 150
        and not low_profile.trace_correct
        and tuple(row.lambda_value for row in lambda_rows if row.support == 150) == (-2,)
        and not any(row.ok for row in lambda_rows)
        and scaled_profile.ok
    )
    return KsyDlogChainProfile(
        dlog_support=len(footprint),
        dlog_coefficient_counts=coefficient_counts(footprint),
        dlog_profile=dlog_profile,
        high_weight_layer_profile=high_profile,
        low_weight_layer_profile=low_profile,
        dlog_equals_two_doubled_minus_four_bridge=footprint == expected,
        lambda_scan=lambda_rows,
        lambda_minus_two_scaled_bridge_ok=scaled_profile.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel dlog chain gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_dlog_chain()
    print(f"ksy_dlog_chain_profile={profile}")
    print("dlog_chain_laws")
    print("  dlog_footprint = 2*double_pushforward(bridge) - 4*bridge")
    print("  coefficient_abs_4_layer_scaled_by_-1/4_is_exact_bridge=1")
    print("  coefficient_abs_2_layer_scaled_by_1/2_is_doubled_bridge_wrong_trace=1")
    print("  dlog_chain_footprint_has_support_300_and_fails_bridge_contract=1")
    print("  among_lambda_-6_to_6_only_lambda_-2_reduces_support_to_150=1")
    print("  lambda_-2_then_exact_divide_by_-4_recovers_bridge=1")
    print("interpretation")
    print("  chain_rule_factor_2_does_not_cancel_the_g2Q_layer=1")
    print("  Kato_Siegel_dlog_route_still_needs_exact_doubled_layer_cancellation=1")
    print(f"robert_ksy_dlog_chain_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_dlog_chain_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
