#!/usr/bin/env python3
"""Hilbert-90 two-sign adapter to the KSY source-quotient packet.

The Hilbert-90 lane already has a compact two-sign finite target.  The KSY
lane now has a six-cell source-quotient packet target.  This gate records that
they are the same bridge payload in different coordinates:

    q-cycle bridge point q  ->  source quotient coordinate (q mod 3, q mod 169).

For every active Hilbert-90 sign pair, the q-cycle bridge converts to the
accepted KSY source-quotient packet, which then lifts through the primitive K
trace and passes the bridge contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    profile_source_quotient_packet,
    target_source_quotient_packet,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness import (
    profile_sign_candidate,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness import (
    sign_sparse_source_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER


ACTIVE_SIGNS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)


@dataclass(frozen=True)
class Hilbert90PacketAdapterRow:
    eps: int
    branch: int
    sign_profile_ok: bool
    quotient_bridge_support: int
    q_cycle_coordinates: tuple[tuple[tuple[int, int], int], ...]
    source_quotient_packet: tuple[tuple[tuple[int, int], int], ...]
    source_packet_exact: bool
    source_packet_profile: SourceQuotientPacketProfile
    ok: bool


@dataclass(frozen=True)
class Hilbert90PacketAdapterProfile:
    active_rows: tuple[Hilbert90PacketAdapterRow, ...]
    invalid_sign_ok: bool
    all_rows_emit_same_packet: bool
    all_rows_pass_packet_contract: bool
    q_cycle_coordinate_warning_checked: bool
    row_ok: bool


def source_coord_from_q(q_value: int) -> tuple[int, int]:
    return (q_value % 3, q_value % C_ORDER)


def packet_from_quotient_bridge(bridge_q_items: tuple[tuple[int, int], ...]) -> dict[tuple[int, int], int]:
    return {
        source_coord_from_q(q_value): coefficient
        for q_value, coefficient in bridge_q_items
    }


def adapter_row(eps: int, branch: int) -> Hilbert90PacketAdapterRow:
    sparse_profile = sign_sparse_source_profile(f"hilbert90_packet_eps_{eps}_branch_{branch}", eps, branch)
    packet = packet_from_quotient_bridge(sparse_profile.bridge_q_items)
    packet_profile = profile_source_quotient_packet(
        f"hilbert90_packet_eps_{eps}_branch_{branch}",
        packet_entries(packet),
        1,
    )
    q_cycle_coords = tuple(
        sorted(
            (coord_from_q(q_value), coefficient)
            for q_value, coefficient in sparse_profile.bridge_q_items
        )
    )
    source_packet = tuple(sorted(packet.items()))
    row_ok = (
        sparse_profile.ok
        and len(sparse_profile.bridge_q_items) == 6
        and packet == target_source_quotient_packet()
        and packet_profile.ok
    )
    return Hilbert90PacketAdapterRow(
        eps=eps,
        branch=branch,
        sign_profile_ok=sparse_profile.ok,
        quotient_bridge_support=len(sparse_profile.bridge_q_items),
        q_cycle_coordinates=q_cycle_coords,
        source_quotient_packet=source_packet,
        source_packet_exact=packet == target_source_quotient_packet(),
        source_packet_profile=packet_profile,
        ok=row_ok,
    )


def profile_adapter() -> Hilbert90PacketAdapterProfile:
    rows = tuple(adapter_row(eps, branch) for eps, branch in ACTIVE_SIGNS)
    invalid_sign = profile_sign_candidate("invalid_sign_control", 0, 1)
    emitted_packets = {row.source_quotient_packet for row in rows}
    q_cycle_warning = all(
        tuple(sorted((coord_from_q(q_value), coefficient) for q_value, coefficient in sign_sparse_source_profile(
            f"q_warning_{row.eps}_{row.branch}",
            row.eps,
            row.branch,
        ).bridge_q_items))
        != row.source_quotient_packet
        for row in rows
    )
    row_ok = (
        len(rows) == 4
        and all(row.ok for row in rows)
        and len(emitted_packets) == 1
        and not invalid_sign.ok
        and q_cycle_warning
        and QUOTIENT_ORDER == 507
    )
    return Hilbert90PacketAdapterProfile(
        active_rows=rows,
        invalid_sign_ok=invalid_sign.ok,
        all_rows_emit_same_packet=len(emitted_packets) == 1,
        all_rows_pass_packet_contract=all(row.source_packet_profile.ok for row in rows),
        q_cycle_coordinate_warning_checked=q_cycle_warning,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Hilbert-90 to KSY source-quotient packet adapter gate")
    profile = profile_adapter()
    print(f"hilbert90_packet_adapter_profile={profile}")
    print("adapter_laws")
    print("  every_active_eps_branch_pair_emits_the_same_q_cycle_bridge=1")
    print("  q_cycle_bridge_converts_to_source_packet_by_q_mod_3_and_q_mod_169=1")
    print("  converted_packet_is_the_KSY_source_quotient_packet=1")
    print("  converted_packet_lifts_through_primitive_K_and_passes_bridge_contract=1")
    print("  coord_from_q_coordinates_are_not_the_source_packet_coordinates=1")
    print("interpretation")
    print("  two_sign_Hilbert90_hits_can_feed_the_KSY_packet_verifier_directly=1")
    print("  this_is_a_coordinate_adapter_not_a_new_arithmetic_producer=1")
    print(f"robert_ksy_theta2_hilbert90_packet_adapter_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_hilbert90_packet_adapter_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
