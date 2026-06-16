#!/usr/bin/env python3
"""D=2 theorem-obligation gate for the p25 KSY/Kato-Siegel moonshot.

The finite work has made theta2 an accepted producer interface.  This gate
states the remaining theorem-side obligation in executable form:

* a divisor/additive theta2 or theta2-inverse payload is acceptable;
* compact KSY center/half/orientation data is acceptable;
* value-level multiplicative unit data still needs branch/root selection;
* formal coefficient filtering, dlog chain-rule factors, [2]-norms,
  inverse-doubling transport, and square-root/half-dlog shortcuts do not by
  themselves produce the bridge.

It is not an arithmetic proof.  It is a falsifiable checklist for what such a
proof must supply.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_dlog_chain_gate import profile_dlog_chain
from p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate import (
    profile_arithmetic_producer_contract,
)
from p25_laneB_robert_ksy_theta2_even_gate import profile_theta2_even
from p25_laneB_robert_ksy_theta2_universal_producer_intake import (
    default_universal_producer_intake_profile,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import profile_half_edge_footprint
from p25_laneB_robert_ksy_y_projection_gate import profile_projection


@dataclass(frozen=True)
class TheoremObligationRow:
    name: str
    finite_status: str
    must_prove: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class D2TheoremObligationProfile:
    half_edge_data_ok: bool
    projection_structure_ok: bool
    dlog_chain_obstruction_ok: bool
    even_d_obstruction_ok: bool
    producer_contract_ok: bool
    universal_intake_ok: bool
    accepted_obligations: tuple[TheoremObligationRow, ...]
    rejected_shortcuts: tuple[TheoremObligationRow, ...]
    exact_theta2_payload_is_current_primary_target: bool
    compact_ksy_payload_is_current_smallest_theorem_output: bool
    doubled_layer_cancellation_still_required_for_direct_bridge: bool
    value_level_branch_selection_required: bool
    row_ok: bool


def profile_d2_theorem_obligation() -> D2TheoremObligationProfile:
    half = profile_half_edge_footprint()
    projection = profile_projection()
    dlog = profile_dlog_chain()
    even = profile_theta2_even()
    contract = profile_arithmetic_producer_contract()
    universal = default_universal_producer_intake_profile()

    accepted = (
        TheoremObligationRow(
            "divisor_theta2_or_inverse",
            "accepted finite payload",
            "prove a challenge-legal identity emitting exact theta2 or theta2^-1 divisor data",
            "plain 150-cell bridge is rejected as theta2",
            contract.additive_divisor_theta2_normalization_ok,
        ),
        TheoremObligationRow(
            "compact_ksy_center_half_orientation",
            "accepted finite payload",
            "derive center_base=(44,166), half_shift=(56,28), and orientation from the theorem",
            "wrong half orientation, full-edge half-shift, and missing center shift fail",
            universal.row_ok and half.accepted_center_base == (44, 166),
        ),
        TheoremObligationRow(
            "source_packet_or_factor_shadow",
            "accepted finite payload",
            "emit the six-cell packet or quotient factor classes from an arithmetic identity",
            "q-cycle convention, nonprimitive K, and wrong quotient D fail",
            contract.finite_spine_ok
            and contract.q_cycle_source_coordinate_confusion_rejected
            and contract.nonprimitive_k_rejected
            and contract.wrong_quotient_d_rejected,
        ),
    )

    rejected = (
        TheoremObligationRow(
            "normalized_y_footprint_as_bridge",
            "rejected shortcut",
            "separate or cancel the doubled g(2Q) layer theorem-side",
            "coefficient-blind 300-cell footprint fails bridge contract",
            projection.coefficient_blind_killed,
        ),
        TheoremObligationRow(
            "coefficient_abs_4_layer_filter",
            "not a theorem by itself",
            "authorize the coefficient-layer selection arithmetically",
            "the abs-4 layer is the bridge only after a post-hoc finite filter",
            projection.high_weight_layer_is_bridge and projection.low_weight_layer_is_doubled_bridge,
        ),
        TheoremObligationRow(
            "kato_siegel_dlog_chain_rule_alone",
            "rejected shortcut",
            "provide exact doubled-layer cancellation beyond the chain-rule factor",
            "dlog footprint still has support 300 and only lambda=-2 repair works",
            dlog.row_ok and not dlog.dlog_profile.ok,
        ),
        TheoremObligationRow(
            "formal_two_norm_or_transport",
            "rejected shortcut",
            "supply a real even-D/theta2 identity, not a formal [2] norm or transport",
            "multiplication by 2 has trivial kernel and transported theta2 still fails",
            even.row_ok
            and even.doubling_kernel_size == 1
            and even.theta2_norm_equals_theta2
            and not even.theta2_norm_profile.ok
            and not even.inverse_doubling_theta2_profile.ok,
        ),
        TheoremObligationRow(
            "square_root_or_half_dlog_escape",
            "rejected shortcut",
            "supply a theorem-side half-trace identity if using halves",
            "theta2 has no integral square-root footprint; half-dlog still has support 300",
            even.row_ok
            and not even.theta2_integral_square_root_exists
            and even.dlog_integral_half_exists
            and not even.half_dlog_profile.ok,
        ),
        TheoremObligationRow(
            "value_unit_without_branch",
            "conditional, not enough",
            "select the multiplicative root/branch explicitly",
            "gcd(4^780-1,p-1)=11 and the finite bridge contract cannot select a value branch",
            contract.value_branch_count == 11
            and not contract.multiplicative_unit_exponent_inverse_available
            and not contract.finite_bridge_contract_selects_value_branch,
        ),
    )

    accepted_ok = all(row.ok for row in accepted)
    rejected_ok = all(row.ok for row in rejected)
    row_ok = (
        half.row_ok
        and projection.row_ok
        and dlog.row_ok
        and even.row_ok
        and contract.row_ok
        and universal.row_ok
        and accepted_ok
        and rejected_ok
        and contract.support_resolvent_term_budget == 46800
        and contract.telescoping_compact_budget == 975
    )
    return D2TheoremObligationProfile(
        half_edge_data_ok=half.row_ok,
        projection_structure_ok=projection.row_ok,
        dlog_chain_obstruction_ok=dlog.row_ok,
        even_d_obstruction_ok=even.row_ok,
        producer_contract_ok=contract.row_ok,
        universal_intake_ok=universal.row_ok,
        accepted_obligations=accepted,
        rejected_shortcuts=rejected,
        exact_theta2_payload_is_current_primary_target=True,
        compact_ksy_payload_is_current_smallest_theorem_output=True,
        doubled_layer_cancellation_still_required_for_direct_bridge=True,
        value_level_branch_selection_required=True,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel D=2 theorem-obligation gate")
    profile = profile_d2_theorem_obligation()
    print(f"d2_theorem_obligation_profile={profile}")
    print("accepted_theorem_obligations")
    for row in profile.accepted_obligations:
        print(f"  {row.name}: ok={int(row.ok)} status={row.finite_status}")
    print("rejected_or_conditional_shortcuts")
    for row in profile.rejected_shortcuts:
        print(f"  {row.name}: checked={int(row.ok)} status={row.finite_status}")
    print("d2_obligation_laws")
    print("  exact_theta2_or_theta2_inverse_divisor_payload_is_accepted=1")
    print("  compact_KSY_center_half_orientation_is_smallest_theorem_output=1")
    print("  normalized_y_dlog_two_norm_transport_and_square_root_shortcuts_are_not_enough=1")
    print("  value_level_unit_route_requires_explicit_branch_selection=1")
    print("interpretation")
    print("  next_theory_target_is_a_challenge_legal_D2_theta2_identity_emitting_an_accepted_payload=1")
    print("  this_gate_is_a_theorem_obligation_not_an_arithmetic_producer=1")
    print(f"robert_ksy_theta2_d2_theorem_obligation_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
