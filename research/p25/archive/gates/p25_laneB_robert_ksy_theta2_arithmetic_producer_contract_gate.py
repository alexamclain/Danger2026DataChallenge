#!/usr/bin/env python3
"""Arithmetic-producer contract for the p25 KSY/Hilbert-90 spine.

The minimal producer spine says which finite objects are equivalent verifier
targets.  This gate separates that finite success from the remaining theorem
debt: a challenge-legal arithmetic producer must emit one of those objects, or
must emit theta2 data with the required normalization/branch information.

It is a contract and falsifier for future literature/proof hits, not a new
arithmetic producer.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    profile_theta2_candidate,
    theta2_sparse_entries,
    theta2_target_rings,
)
from p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate import (
    profile_minimal_producer_spine,
)
from p25_laneB_robert_ksy_theta2_resolvent_normalization_gate import (
    profile_theta2_resolvent_normalization,
)
from p25_laneB_robert_ksy_theta2_root_ambiguity_gate import profile_root_ambiguity


@dataclass(frozen=True)
class ProducerInterfaceRow:
    name: str
    payload_kind: str
    finite_input_size: int
    finite_verifier_accepts: bool
    arithmetic_status: str
    first_falsifier_or_extra_requirement: str


@dataclass(frozen=True)
class ArithmeticProducerContractProfile:
    finite_spine_ok: bool
    accepted_interfaces: tuple[ProducerInterfaceRow, ...]
    rejected_or_conditional_interfaces: tuple[ProducerInterfaceRow, ...]
    additive_divisor_theta2_normalization_ok: bool
    multiplicative_unit_exponent_inverse_available: bool
    value_branch_count: int
    finite_bridge_contract_selects_value_branch: bool
    plain_bridge_rejected_as_theta2: bool
    q_cycle_source_coordinate_confusion_rejected: bool
    nonprimitive_k_rejected: bool
    wrong_quotient_d_rejected: bool
    support_resolvent_term_budget: int
    telescoping_compact_budget: int
    contract_summary: str
    row_ok: bool


def profile_arithmetic_producer_contract() -> ArithmeticProducerContractProfile:
    spine = profile_minimal_producer_spine()
    normalization = profile_theta2_resolvent_normalization()
    root = profile_root_ambiguity()
    bridge, theta2, theta2_inverse = theta2_target_rings()
    theta2_profile = profile_theta2_candidate(
        "producer_contract_theta2_divisor",
        theta2_sparse_entries(theta2),
    )
    theta2_inverse_profile = profile_theta2_candidate(
        "producer_contract_theta2_inverse_divisor",
        theta2_sparse_entries(theta2_inverse),
    )
    plain_bridge_control = profile_theta2_candidate(
        "producer_contract_plain_bridge_is_not_theta2_control",
        theta2_sparse_entries(bridge),
    )

    accepted = (
        ProducerInterfaceRow(
            "hilbert90_two_signs",
            "finite signs converted to source quotient packet",
            2,
            spine.hilbert90_packet_adapter_ok,
            "finite verifier target only",
            "still needs arithmetic source of the primitive signs",
        ),
        ProducerInterfaceRow(
            "source_quotient_packet",
            "six signed cells on C3 x C169 plus primitive K",
            spine.source_packet_support,
            spine.source_packet_ok,
            "finite verifier target only",
            "must be emitted by a theorem, not hand-selected",
        ),
        ProducerInterfaceRow(
            "quotient_factor_classes",
            "base, D, T quotient classes plus primitive K",
            spine.quotient_factor_input_cells,
            spine.quotient_factor_ok,
            "finite verifier target only",
            "must explain the selected quotient classes arithmetically",
        ),
        ProducerInterfaceRow(
            "source_factor_tuple",
            "base*K_trace*D_segment*(1-T)",
            spine.factor_certificate_support_budget,
            spine.factor_certificate_ok,
            "finite verifier target only",
            "must supply coupled K_trace, D_segment, and T edge",
        ),
        ProducerInterfaceRow(
            "sparse_theta2_divisor",
            "300 sparse source-coordinate theta2 divisor triples",
            theta2_profile.active_source_terms,
            theta2_profile.ok,
            "accepted if output is divisor/additive data",
            "normalization is additive/divisor scalar division",
        ),
        ProducerInterfaceRow(
            "sparse_theta2_inverse_divisor",
            "300 sparse source-coordinate theta2 inverse divisor triples",
            theta2_inverse_profile.active_source_terms,
            theta2_inverse_profile.ok,
            "accepted if output is divisor/additive data",
            "global sign is normalized after resolvent recovery",
        ),
        ProducerInterfaceRow(
            "compact_ksy_theta2",
            "center/half-edge/orientation data for theta2",
            spine.telescoping_compact_budget,
            spine.telescoping_certificate_ok,
            "accepted finite certificate skeleton",
            "must be produced as a real KSY/theta identity",
        ),
    )
    rejected = (
        ProducerInterfaceRow(
            "theta2_value_unit_without_branch",
            "multiplicative finite-field unit value only",
            root.fp_star_kernel_order,
            False,
            "conditional, not accepted by finite source mask alone",
            "gcd(4^780-1,p-1)=11 gives 11 value branches",
        ),
        ProducerInterfaceRow(
            "plain_bridge_as_theta2",
            "150-term bridge sparse source submitted as theta2",
            plain_bridge_control.active_source_terms,
            plain_bridge_control.ok,
            "rejected control",
            "theta2 harness requires exact theta2 or theta2 inverse footprint",
        ),
        ProducerInterfaceRow(
            "q_cycle_packet_as_source_packet",
            "old q-cycle six-cell coordinates",
            spine.source_packet_support,
            not spine.q_cycle_confusion_rejected,
            "rejected coordinate convention",
            "source packet must be (q mod 3, q mod 169), not coord_from_q",
        ),
        ProducerInterfaceRow(
            "nonprimitive_k_multiplier",
            "six-cell source packet with nonprimitive K",
            spine.source_packet_support,
            not spine.nonprimitive_k_rejected,
            "rejected trace lift",
            "K multiplier must be primitive modulo 25",
        ),
        ProducerInterfaceRow(
            "wrong_quotient_d_class",
            "factor classes with D not congruent to (1,3)",
            spine.quotient_factor_input_cells,
            not spine.wrong_quotient_d_rejected,
            "rejected quotient factor",
            "D_segment class is a hard finite invariant",
        ),
    )
    accepted_ok = all(row.finite_verifier_accepts for row in accepted)
    rejected_ok = all(not row.finite_verifier_accepts for row in rejected)
    row_ok = (
        spine.row_ok
        and normalization.row_ok
        and root.row_ok
        and theta2_profile.ok
        and theta2_inverse_profile.ok
        and not plain_bridge_control.ok
        and normalization.additive_p25_scaling_recovers_bridge
        and not normalization.exponent_inverse_available_fp_star
        and root.fp_star_kernel_order == 11
        and not root.finite_bridge_contract_selects_branch
        and accepted_ok
        and rejected_ok
        and spine.support_resolvent_term_budget == 46800
        and spine.telescoping_compact_budget == 975
    )
    return ArithmeticProducerContractProfile(
        finite_spine_ok=spine.row_ok,
        accepted_interfaces=accepted,
        rejected_or_conditional_interfaces=rejected,
        additive_divisor_theta2_normalization_ok=normalization.row_ok,
        multiplicative_unit_exponent_inverse_available=(
            normalization.exponent_inverse_available_fp_star
        ),
        value_branch_count=root.fp_star_kernel_order,
        finite_bridge_contract_selects_value_branch=root.finite_bridge_contract_selects_branch,
        plain_bridge_rejected_as_theta2=not plain_bridge_control.ok,
        q_cycle_source_coordinate_confusion_rejected=spine.q_cycle_confusion_rejected,
        nonprimitive_k_rejected=spine.nonprimitive_k_rejected,
        wrong_quotient_d_rejected=spine.wrong_quotient_d_rejected,
        support_resolvent_term_budget=spine.support_resolvent_term_budget,
        telescoping_compact_budget=spine.telescoping_compact_budget,
        contract_summary=(
            "future theorem hits must produce a named finite spine interface, "
            "or theta2 divisor/additive data; value-level unit claims require "
            "explicit root/branch selection"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Hilbert-90 arithmetic-producer contract gate")
    profile = profile_arithmetic_producer_contract()
    print(f"arithmetic_producer_contract_profile={profile}")
    print("accepted_interfaces")
    for row in profile.accepted_interfaces:
        print(f"  {row.name}: accepts={int(row.finite_verifier_accepts)} size={row.finite_input_size}")
    print("rejected_or_conditional_interfaces")
    for row in profile.rejected_or_conditional_interfaces:
        print(f"  {row.name}: accepts={int(row.finite_verifier_accepts)} size={row.finite_input_size}")
    print("producer_contract_laws")
    print("  finite_spine_interfaces_are_verified_but_not_arithmetic_producers=1")
    print("  theta2_divisor_or_additive_payload_can_use_resolvent_normalization=1")
    print("  value_level_unit_payload_without_branch_selection_is_not_enough=1")
    print("  q_cycle_coordinate_confusion_nonprimitive_K_and_wrong_D_are_rejected=1")
    print("interpretation")
    print("  next_moonshot_target_is_a_challenge_legal_arithmetic_source_for_this_contract=1")
    print("  this_gate_is_a_contract_and_falsifier_not_the_missing_producer=1")
    print(f"robert_ksy_theta2_arithmetic_producer_contract_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
