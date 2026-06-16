#!/usr/bin/env python3
"""Universal finite-producer intake for the p25 KSY/Hilbert-90 spine.

The arithmetic-producer contract says which finite payloads are meaningful
targets for a future theorem hit.  This harness gives those payloads a single
front door while continuing to delegate the real checks to the specialized
gates.

No-argument mode runs positive and negative controls for every accepted
interface.  Candidate mode dispatches one supplied payload to the appropriate
underlying harness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    profile_theta2_candidate,
    theta2_sparse_entries,
    theta2_target_rings,
)
from p25_laneB_robert_ksy_theta2_compact_harness import profile_compact_theta2
from p25_laneB_robert_ksy_theta2_factor_certificate_harness import (
    profile_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness import (
    profile_quotient_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    packet_entries,
    parse_packet,
    profile_source_quotient_packet,
    q_cycle_confusion_packet,
    target_source_quotient_packet,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import profile_half_edge_footprint
from p25_laneB_robert_sparse_source_candidate_harness_gate import parse_sparse_source
from p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness import (
    sign_sparse_source_profile,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


@dataclass(frozen=True)
class UniversalIntakeRow:
    mode: str
    input_shape: str
    finite_input_size: int
    underlying_gate: str
    ok: bool


@dataclass(frozen=True)
class UniversalProducerIntakeProfile:
    accepted_rows: tuple[UniversalIntakeRow, ...]
    rejected_control_rows: tuple[UniversalIntakeRow, ...]
    accepted_modes_all_pass: bool
    rejected_controls_all_fail: bool
    supported_candidate_modes: tuple[str, ...]
    row_ok: bool


SUPPORTED_MODES = (
    "hilbert90-signs",
    "source-packet",
    "quotient-factor",
    "source-factor",
    "compact-theta2",
    "theta2-sparse",
)


def target_compact_profiles() -> tuple[Any, Any]:
    half_profile = profile_half_edge_footprint()
    inverse_profile = profile_compact_theta2(
        "universal_target_compact_theta2_inverse",
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
        False,
    )
    theta2_profile = profile_compact_theta2(
        "universal_target_compact_theta2",
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
        True,
    )
    return inverse_profile, theta2_profile


def default_universal_producer_intake_profile() -> UniversalProducerIntakeProfile:
    target_packet = target_source_quotient_packet()
    bridge, theta2, theta2_inverse = theta2_target_rings()
    compact_inverse, compact_theta2 = target_compact_profiles()

    sign_profile = sign_sparse_source_profile("universal_hilbert90_signs", 1, -1)
    source_packet_profile = profile_source_quotient_packet(
        "universal_source_packet",
        packet_entries(target_packet),
        1,
    )
    quotient_factor_profile = profile_quotient_factor_certificate(
        "universal_quotient_factor",
        (1, 25),
        (1, 3),
        (2, 113),
        1,
    )
    source_factor_profile = profile_factor_certificate(
        "universal_source_factor",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    theta2_profile = profile_theta2_candidate(
        "universal_theta2_sparse",
        theta2_sparse_entries(theta2),
    )
    theta2_inverse_profile = profile_theta2_candidate(
        "universal_theta2_inverse_sparse",
        theta2_sparse_entries(theta2_inverse),
    )

    accepted = (
        UniversalIntakeRow(
            "hilbert90-signs",
            "eps branch",
            2,
            "corner_sign_sparse_source_harness",
            sign_profile.ok,
        ),
        UniversalIntakeRow(
            "source-packet",
            "six right_class c coeff rows plus primitive K",
            source_packet_profile.packet_support,
            "source_quotient_packet_harness",
            source_packet_profile.ok,
        ),
        UniversalIntakeRow(
            "quotient-factor",
            "base,D,T quotient classes plus primitive K",
            3,
            "quotient_factor_certificate_harness",
            quotient_factor_profile.ok,
        ),
        UniversalIntakeRow(
            "source-factor",
            "base,K,D,T source coordinates",
            source_factor_profile.factor_support_budget,
            "factor_certificate_harness",
            source_factor_profile.ok,
        ),
        UniversalIntakeRow(
            "compact-theta2-inverse",
            "center_base half_shift invert=0",
            compact_inverse.footprint_support,
            "compact_theta2_harness",
            compact_inverse.ok,
        ),
        UniversalIntakeRow(
            "compact-theta2",
            "center_base half_shift invert=1",
            compact_theta2.footprint_support,
            "compact_theta2_harness",
            compact_theta2.ok,
        ),
        UniversalIntakeRow(
            "theta2-sparse",
            "300 right_log c_log coeff rows for theta2",
            theta2_profile.active_source_terms,
            "theta2_candidate_harness",
            theta2_profile.ok,
        ),
        UniversalIntakeRow(
            "theta2-inverse-sparse",
            "300 right_log c_log coeff rows for theta2 inverse",
            theta2_inverse_profile.active_source_terms,
            "theta2_candidate_harness",
            theta2_inverse_profile.ok,
        ),
    )

    rejected = (
        UniversalIntakeRow(
            "invalid-hilbert90-signs",
            "eps=0 branch=1",
            2,
            "corner_sign_sparse_source_harness",
            sign_sparse_source_profile("universal_invalid_signs", 0, 1).ok,
        ),
        UniversalIntakeRow(
            "q-cycle-as-source-packet",
            "old q-cycle coordinates",
            6,
            "source_quotient_packet_harness",
            profile_source_quotient_packet(
                "universal_q_cycle_packet_control",
                packet_entries(q_cycle_confusion_packet()),
                1,
            ).ok,
        ),
        UniversalIntakeRow(
            "nonprimitive-k-source-packet",
            "target source packet with K multiplier 5",
            6,
            "source_quotient_packet_harness",
            profile_source_quotient_packet(
                "universal_nonprimitive_k_source_packet_control",
                packet_entries(target_packet),
                5,
            ).ok,
        ),
        UniversalIntakeRow(
            "wrong-d-quotient-factor",
            "D class (1,4)",
            3,
            "quotient_factor_certificate_harness",
            profile_quotient_factor_certificate(
                "universal_wrong_d_quotient_factor_control",
                (1, 25),
                (1, 4),
                (2, 113),
                1,
            ).ok,
        ),
        UniversalIntakeRow(
            "collapsed-k-source-factor",
            "K=(0,0)",
            31,
            "factor_certificate_harness",
            profile_factor_certificate(
                "universal_collapsed_k_source_factor_control",
                BASE_POINT,
                (0, 0),
                D_SHIFT,
                BRIDGE_SHIFT,
            ).ok,
        ),
        UniversalIntakeRow(
            "plain-bridge-as-theta2",
            "150 bridge rows submitted to theta2 sparse mode",
            150,
            "theta2_candidate_harness",
            profile_theta2_candidate(
                "universal_plain_bridge_theta2_control",
                theta2_sparse_entries(bridge),
            ).ok,
        ),
        UniversalIntakeRow(
            "wrong-compact-theta2",
            "base without required center shift",
            4,
            "compact_theta2_harness",
            profile_compact_theta2(
                "universal_wrong_compact_theta2_control",
                BASE_POINT,
                profile_half_edge_footprint().half_edge,
                False,
            ).ok,
        ),
    )
    accepted_ok = all(row.ok for row in accepted)
    rejected_ok = all(not row.ok for row in rejected)
    return UniversalProducerIntakeProfile(
        accepted_rows=accepted,
        rejected_control_rows=rejected,
        accepted_modes_all_pass=accepted_ok,
        rejected_controls_all_fail=rejected_ok,
        supported_candidate_modes=SUPPORTED_MODES,
        row_ok=accepted_ok
        and rejected_ok
        and source_factor_profile.factor_support_budget == 31
        and source_packet_profile.packet_support == 6
        and quotient_factor_profile.k_multiplier_primitive
        and theta2_profile.shifted_theta2_term_budget == 46800
        and compact_theta2.candidate_profile.shifted_theta2_term_budget == 46800,
    )


def require(value: Any, name: str) -> Any:
    if value is None:
        raise SystemExit(f"{name} is required for this mode")
    return value


def run_candidate(args: argparse.Namespace) -> tuple[str, bool, Any]:
    if args.mode == "hilbert90-signs":
        profile = sign_sparse_source_profile(
            "universal_candidate_hilbert90_signs",
            require(args.eps, "--eps"),
            require(args.branch, "--branch"),
        )
        return args.mode, profile.ok, profile

    if args.mode == "source-packet":
        packet = parse_packet(require(args.packet, "--packet"))
        profile = profile_source_quotient_packet(
            "universal_candidate_source_packet",
            packet,
            args.k_multiplier,
        )
        return args.mode, profile.ok, profile

    if args.mode == "quotient-factor":
        profile = profile_quotient_factor_certificate(
            "universal_candidate_quotient_factor",
            (require(args.base_right_class, "--base-right-class"), require(args.base_c, "--base-c")),
            (require(args.d_right_class, "--d-right-class"), require(args.d_c, "--d-c")),
            (require(args.t_right_class, "--t-right-class"), require(args.t_c, "--t-c")),
            args.k_multiplier,
        )
        return args.mode, profile.ok, profile

    if args.mode == "source-factor":
        profile = profile_factor_certificate(
            "universal_candidate_source_factor",
            (require(args.base_right, "--base-right"), require(args.base_c, "--base-c")),
            (require(args.k_right, "--k-right"), require(args.k_c, "--k-c")),
            (require(args.d_right, "--d-right"), require(args.d_c, "--d-c")),
            (require(args.t_right, "--t-right"), require(args.t_c, "--t-c")),
        )
        return args.mode, profile.ok, profile

    if args.mode == "compact-theta2":
        profile = profile_compact_theta2(
            "universal_candidate_compact_theta2",
            (require(args.center_right, "--center-right"), require(args.center_c, "--center-c")),
            (require(args.half_right, "--half-right"), require(args.half_c, "--half-c")),
            args.invert,
        )
        return args.mode, profile.ok, profile

    if args.mode == "theta2-sparse":
        sparse_source = parse_sparse_source(require(args.sparse_source, "--sparse-source"))
        profile = profile_theta2_candidate(
            "universal_candidate_theta2_sparse",
            sparse_source,
        )
        return args.mode, profile.ok, profile

    raise SystemExit(f"unsupported mode: {args.mode}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Universal intake for p25 KSY/Hilbert-90 finite producer payloads."
    )
    parser.add_argument("--mode", choices=SUPPORTED_MODES)
    parser.add_argument("--eps", type=int)
    parser.add_argument("--branch", type=int)
    parser.add_argument("--packet", type=Path)
    parser.add_argument("--sparse-source", type=Path)
    parser.add_argument("--k-multiplier", type=int, default=1)
    parser.add_argument("--base-right-class", type=int)
    parser.add_argument("--base-right", type=int)
    parser.add_argument("--base-c", type=int)
    parser.add_argument("--d-right-class", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--t-right-class", type=int)
    parser.add_argument("--t-right", type=int)
    parser.add_argument("--t-c", type=int)
    parser.add_argument("--k-right", type=int)
    parser.add_argument("--k-c", type=int)
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--half-right", type=int)
    parser.add_argument("--half-c", type=int)
    parser.add_argument("--invert", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/Hilbert-90 universal producer intake")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} quotient_group=C_3xC_{C_ORDER}")

    if args.mode is not None:
        mode, ok, profile = run_candidate(args)
        print(f"mode={mode}")
        print(f"candidate_profile={profile}")
        print("candidate_laws")
        print("  candidate_is_checked_by_the_specialized_underlying_harness=1")
        print("  pass_means_finite_payload_matches_an_accepted_spine_interface=1")
        print("  pass_does_not_by_itself_prove_the_arithmetic_producer=1")
        print(f"robert_ksy_theta2_universal_producer_intake_candidate_rows={int(ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_universal_producer_intake_candidate")
        return 0 if ok else 1

    profile = default_universal_producer_intake_profile()
    print(f"universal_producer_intake_profile={profile}")
    print("accepted_modes")
    for row in profile.accepted_rows:
        print(f"  {row.mode}: ok={int(row.ok)} size={row.finite_input_size}")
    print("rejected_controls")
    for row in profile.rejected_control_rows:
        print(f"  {row.mode}: ok={int(row.ok)} size={row.finite_input_size}")
    print("universal_intake_laws")
    print("  all_accepted_producer_contract_modes_dispatch_to_specialized_harnesses=1")
    print("  all_recorded_near_miss_controls_fail_through_the_same_front_door=1")
    print("  universal_intake_is_a_finite_payload_checker_not_the_missing_producer=1")
    print(f"robert_ksy_theta2_universal_producer_intake_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_universal_producer_intake")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
