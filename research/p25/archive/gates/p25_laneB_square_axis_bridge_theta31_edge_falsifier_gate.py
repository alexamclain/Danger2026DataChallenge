#!/usr/bin/env python3
"""Theta_{3,1} edge falsifier for the p25 square-axis bridge.

The bridge formal-unit shadow is producer-shaped but not yet arithmetic.  The
closest p24-amortized arithmetic object already in the p25 workbench is the
ray-local theta_{3,1} carry pullback.  This gate asks the direct interface
question: do natural finite differences of that pullback along the bridge
directions produce the primitive bridge?

The answer is no.  The canonical D-edge is a serious near miss: it has the
same raw support size, block constancy, kernel mode, raw relation, and full
character payload expected by the bridge harness.  But its six quotient points
are disjoint from the bridge and are not a translate or sign of it.  The T
edges are much larger.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_ray_local_theta31_pullback_falsifier_gate import (
    case_by_name,
    local_coordinates,
    synthetic_raw_y,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    MODULUS,
    profile_candidate,
    quotient_trace,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_factorization_gate import (
    BRIDGE_STEP,
    bridge_coefficients,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER


@dataclass(frozen=True)
class ThetaEdgeProfile:
    name: str
    step: int
    normalized_scale: int
    raw_support: int
    quotient_support: int
    trace_correct: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    target_raw_exact: bool
    source_mask_exact: bool
    quotient_scalar_nonzero: int
    quotient_pure_c_nonzero: int
    quotient_mixed_nonzero: int
    quotient_values: tuple[int, ...]
    support_first: tuple[int, ...]
    support_last: tuple[int, ...]
    support_sum: int
    support_square_sum: int
    bridge_support_overlap: int
    bridge_translation_matches: tuple[tuple[int, int], ...]


def normalize_edge(raw_edge: list[int]) -> tuple[int, list[int]]:
    values = sorted({value % MODULUS for value in raw_edge if value % MODULUS})
    if not values:
        return 1, raw_edge
    scale = values[0]
    inverse = pow(scale, -1, MODULUS)
    return scale, [(value * inverse) % MODULUS for value in raw_edge]


def finite_edge(raw_packet: list[int], step: int) -> tuple[int, list[int]]:
    raw_edge = [
        (raw_packet[index] - raw_packet[(index - step) % RAW_ORDER]) % MODULUS
        for index in range(RAW_ORDER)
    ]
    return normalize_edge(raw_edge)


def quotient_coefficients(raw_edge: list[int]) -> dict[int, int]:
    trace = quotient_trace(raw_edge)
    return {q_value: trace[q_value] for q_value in range(QUOTIENT_ORDER) if trace[q_value] % MODULUS}


def bridge_translation_matches(coefficients: dict[int, int]) -> tuple[tuple[int, int], ...]:
    target = bridge_coefficients()
    matches: list[tuple[int, int]] = []
    for shift in range(QUOTIENT_ORDER):
        for sign in (1, -1):
            translated = {
                (q_value + shift) % QUOTIENT_ORDER: sign * value
                for q_value, value in target.items()
            }
            if translated == coefficients:
                matches.append((shift, sign))
    return tuple(matches)


def theta31_raw_packet() -> list[int]:
    case = case_by_name("square_axis_C3xC169")
    coordinates = local_coordinates(case)
    return synthetic_raw_y(case, coordinates, MODULUS)


def edge_profile(name: str, step: int, raw_packet: list[int]) -> ThetaEdgeProfile:
    scale, normalized = finite_edge(raw_packet, step)
    candidate = profile_candidate(name, normalized, target_raw_bridge())
    coefficients = quotient_coefficients(normalized)
    support = tuple(sorted(coefficients))
    bridge_support = set(bridge_coefficients())
    values = tuple(sorted(set(coefficients.values())))
    return ThetaEdgeProfile(
        name=name,
        step=step,
        normalized_scale=scale,
        raw_support=candidate.raw_support,
        quotient_support=candidate.quotient_support,
        trace_correct=candidate.trace_correct,
        block_constancy_hits=candidate.block_constancy_hits,
        kernel_modes=candidate.kernel_modes,
        raw_relation_mismatches=candidate.raw_relation_mismatches,
        target_raw_exact=candidate.target_raw_exact,
        source_mask_exact=candidate.source_mask_exact,
        quotient_scalar_nonzero=candidate.quotient_scalar_nonzero,
        quotient_pure_c_nonzero=candidate.quotient_pure_c_nonzero,
        quotient_mixed_nonzero=candidate.quotient_mixed_nonzero,
        quotient_values=values,
        support_first=support[:12],
        support_last=support[-12:],
        support_sum=sum(support),
        support_square_sum=sum(value * value for value in support),
        bridge_support_overlap=len(set(support) & bridge_support),
        bridge_translation_matches=bridge_translation_matches(coefficients),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge theta31 edge falsifier gate")
    print(
        f"raw_order={RAW_ORDER} quotient_order={QUOTIENT_ORDER} modulus={MODULUS} "
        f"D={S_STEP} T={BRIDGE_STEP} D3={(3 * S_STEP) % RAW_ORDER}"
    )
    raw_packet = theta31_raw_packet()
    profiles = (
        edge_profile("D_edge", S_STEP, raw_packet),
        edge_profile("negD_edge", (-S_STEP) % RAW_ORDER, raw_packet),
        edge_profile("T_edge", BRIDGE_STEP, raw_packet),
        edge_profile("negT_edge", (-BRIDGE_STEP) % RAW_ORDER, raw_packet),
        edge_profile("D3_edge", (3 * S_STEP) % RAW_ORDER, raw_packet),
    )
    expected = (
        ThetaEdgeProfile("D_edge", 172, 35470, 150, 6, False, 507, (0,), 0, False, False, 0, 168, 336, (-1, 1), (0, 43, 86, 129, 169, 338), (0, 43, 86, 129, 169, 338), 765, 168691, 0, ()),
        ThetaEdgeProfile("negD_edge", 12503, 35470, 150, 6, False, 507, (0,), 0, False, False, 0, 168, 336, (-1, 1), (166, 335, 378, 421, 464, 504), (166, 335, 378, 421, 464, 504), 2268, 929218, 0, ()),
        ThetaEdgeProfile("T_edge", 113, 35470, 8450, 338, False, 507, (0,), 0, False, False, 0, 168, 336, (-1, 1), (1, 4, 5, 6, 8, 10, 13, 14, 15, 17, 19, 22), (490, 491, 492, 493, 494, 497, 498, 499, 501, 502, 503, 506), 86162, 29136682, 3, ()),
        ThetaEdgeProfile("negT_edge", 12562, 35470, 8450, 338, False, 507, (0,), 0, False, False, 0, 168, 336, (-1, 1), (0, 1, 4, 5, 6, 8, 9, 10, 13, 14, 15, 16), (485, 488, 490, 492, 493, 494, 497, 499, 501, 502, 503, 506), 84472, 28362568, 3, ()),
        ThetaEdgeProfile("D3_edge", 516, 35470, 450, 18, False, 507, (0,), 0, False, False, 0, 168, 336, (-1, 1), (0, 3, 6, 43, 86, 129, 169, 172, 175, 215, 258, 301), (169, 172, 175, 215, 258, 301, 338, 341, 344, 387, 430, 473), 3870, 1225350, 0, ()),
    )
    bridge = bridge_coefficients()
    row_ok = (
        profiles == expected
        and bridge == {25: 1, 138: -1, 197: 1, 310: -1, 369: 1, 482: -1}
        and all(not profile.trace_correct for profile in profiles)
        and all(not profile.target_raw_exact for profile in profiles)
        and all(not profile.source_mask_exact for profile in profiles)
        and all(profile.bridge_translation_matches == () for profile in profiles)
    )

    print(f"bridge_coefficients={sorted(bridge.items())}")
    print("theta31_edge_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("near_miss")
    print("  D-edge has raw support 150, quotient support 6, block constancy 507/507, kernel mode (0,), and raw relation mismatches 0")
    print("  D-edge quotient support is [0,43,86,129,169,338], disjoint from bridge support [25,138,197,310,369,482]")
    print("  no tested theta31 edge is a translate or sign of the primitive bridge")
    print("interpretation")
    print("  canonical_theta31_pullback_edges_do_not_produce_the_primitive_bridge=1")
    print("  theta31_D_edge_is_a_real_near_miss_but_not_the_bridge=1")
    print("  p24_amortized_theta_shape_needs_a_new_mixed_edge_correction=1")
    print("  producer_search_should_not_equate_full_character_payload_with_bridge_acceptance=1")
    print(f"square_axis_bridge_theta31_edge_falsifier_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_theta31_edge_falsifier_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
