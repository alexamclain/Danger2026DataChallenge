#!/usr/bin/env python3
"""Unified finite producer spine for the p25 KSY/Hilbert-90 moonshot.

This gate ties together the compact finite targets accumulated across the
Hilbert-90 and KSY/theta lanes.  It does not add arithmetic content; it records
the currently smallest verified finite spine:

    Hilbert-90 signs
      -> source quotient packet
      -> quotient factor certificate
      -> source factor certificate
      -> compact theta2
      -> telescoping bridge recovery.

The goal is to make the theorem-output target unambiguous and keep future
literature/proof attempts from drifting across equivalent coordinate systems.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_hilbert90_packet_adapter_gate import profile_adapter
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    packet_entries,
    profile_source_quotient_packet,
    q_cycle_confusion_packet,
    target_source_quotient_packet,
)
from p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness import (
    profile_quotient_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_factor_certificate_harness import profile_factor_certificate
from p25_laneB_robert_ksy_theta2_factor_gauge_normal_form_gate import profile_gauge_normal_form
from p25_laneB_robert_ksy_theta2_factor_period_certificate_gate import (
    profile_factor_period_certificate,
)
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    profile_telescoping_certificate,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import (
    theta2_support_resolvent_profile,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    D_SHIFT,
    KERNEL_SHIFT,
)


@dataclass(frozen=True)
class MinimalProducerSpineProfile:
    hilbert90_packet_adapter_ok: bool
    source_packet_ok: bool
    source_packet_support: int
    quotient_factor_ok: bool
    quotient_factor_input_cells: int
    factor_certificate_ok: bool
    factor_certificate_support_budget: int
    factor_gauge_normal_form_ok: bool
    factor_period_certificate_ok: bool
    support_resolvent_ok: bool
    support_resolvent_term_budget: int
    telescoping_certificate_ok: bool
    telescoping_compact_budget: int
    q_cycle_confusion_rejected: bool
    nonprimitive_k_rejected: bool
    wrong_quotient_d_rejected: bool
    equivalent_finite_interfaces: tuple[str, ...]
    current_missing_arithmetic_object: str
    row_ok: bool


def profile_minimal_producer_spine() -> MinimalProducerSpineProfile:
    adapter = profile_adapter()
    source_packet = profile_source_quotient_packet(
        "spine_source_packet",
        packet_entries(target_source_quotient_packet()),
        1,
    )
    q_cycle_confusion = profile_source_quotient_packet(
        "spine_q_cycle_confusion_control",
        packet_entries(q_cycle_confusion_packet()),
        1,
    )
    nonprimitive_packet = profile_source_quotient_packet(
        "spine_nonprimitive_k_control",
        packet_entries(target_source_quotient_packet()),
        5,
    )
    quotient_factor = profile_quotient_factor_certificate(
        "spine_quotient_factor",
        (1, 25),
        (1, 3),
        (2, 113),
        1,
    )
    wrong_quotient_d = profile_quotient_factor_certificate(
        "spine_wrong_quotient_d_control",
        (1, 25),
        (1, 4),
        (2, 113),
        1,
    )
    factor_certificate = profile_factor_certificate(
        "spine_factor_certificate",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    gauge = profile_gauge_normal_form()
    factor_period = profile_factor_period_certificate()
    support_resolvent = theta2_support_resolvent_profile()
    telescoping = profile_telescoping_certificate()

    interfaces = (
        "Hilbert-90 signs: eps,branch in four active pairs",
        "source quotient packet: 6 signed cells on C3 x C169",
        "quotient factor classes: base=(1,25), D=(1,3), T=(2,113), primitive K",
        "source factor tuple: base*K_trace*D_segment*(1-T)",
        "compact KSY theta2: center_base/half_shift plus orientation",
        "telescoping certificate: theta2=(4-[2])B and [2]^156 B=B",
    )
    row_ok = (
        adapter.row_ok
        and source_packet.ok
        and source_packet.packet_support == 6
        and quotient_factor.ok
        and factor_certificate.ok
        and factor_certificate.factor_support_budget == 31
        and gauge.row_ok
        and factor_period.row_ok
        and support_resolvent.row_ok
        and support_resolvent.support_resolvent_term_budget == 46800
        and telescoping.row_ok
        and telescoping.compact_linear_cell_check_budget == 975
        and not q_cycle_confusion.ok
        and not nonprimitive_packet.ok
        and not wrong_quotient_d.ok
    )
    return MinimalProducerSpineProfile(
        hilbert90_packet_adapter_ok=adapter.row_ok,
        source_packet_ok=source_packet.ok,
        source_packet_support=source_packet.packet_support,
        quotient_factor_ok=quotient_factor.ok,
        quotient_factor_input_cells=3,
        factor_certificate_ok=factor_certificate.ok,
        factor_certificate_support_budget=factor_certificate.factor_support_budget,
        factor_gauge_normal_form_ok=gauge.row_ok,
        factor_period_certificate_ok=factor_period.row_ok,
        support_resolvent_ok=support_resolvent.row_ok,
        support_resolvent_term_budget=support_resolvent.support_resolvent_term_budget,
        telescoping_certificate_ok=telescoping.row_ok,
        telescoping_compact_budget=telescoping.compact_linear_cell_check_budget,
        q_cycle_confusion_rejected=not q_cycle_confusion.ok,
        nonprimitive_k_rejected=not nonprimitive_packet.ok,
        wrong_quotient_d_rejected=not wrong_quotient_d.ok,
        equivalent_finite_interfaces=interfaces,
        current_missing_arithmetic_object=(
            "challenge-legal arithmetic producer for the quotient packet / "
            "Hilbert-90 signs / KSY theta2 object"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Hilbert-90 minimal finite producer spine gate")
    profile = profile_minimal_producer_spine()
    print(f"minimal_producer_spine_profile={profile}")
    print("spine_laws")
    print("  Hilbert90_two_signs_and_KSY_source_packet_are_equivalent_finite_interfaces=1")
    print("  source_packet_quotient_factor_source_factor_and_compact_theta2_all_link=1")
    print("  support_period_resolvent_and_telescoping_certificate_recover_bridge=1")
    print("  q_cycle_coordinate_confusion_nonprimitive_K_and_wrong_quotient_D_are_rejected=1")
    print("interpretation")
    print("  current_moonshot_target_is_arithmetic_production_of_this_finite_spine=1")
    print("  this_gate_is_a_spine_ledger_not_a_new_arithmetic_producer=1")
    print(f"robert_ksy_theta2_minimal_producer_spine_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
