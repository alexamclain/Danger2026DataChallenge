#!/usr/bin/env python3
"""Conductor-39 source-theorem intake for the p25 KSY-y/Yang moonshot.

The post-conductor-39 queue made the first theorem target explicit:

    U_chi = -chi_3 * chi_13 on X_1(39),
    Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi).

This gate classifies future theorem/literature hits against that target.  It
keeps the useful near misses visible while preventing old shortcuts from being
mistaken for a closing theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_ksy_y_koo_shin_conductor39_distribution_bridge_gate import (
    profile_koo_shin_conductor39_distribution_bridge,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_gate import (
    profile_hilbert90_legal_gauge_family,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_gate import (
    profile_hilbert90_sparse_selector_structure,
)
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (
    profile_sparse_hilbert90_yang_lift,
)
from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate import (
    profile_yang_y507_conductor39_modular_unit_legality,
)
from p25_ksy_y_yang_y507_conductor39_coset_selector_gate import (
    profile_yang_y507_conductor39_coset_selector,
)
from p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_gate import (
    profile_yang_y507_conductor39_coset_frobenius_pairing,
)
from p25_ksy_y_yang_y507_conductor39_doubling_orbit_norm_gate import (
    profile_yang_y507_conductor39_doubling_orbit_norm,
)
from p25_ksy_y_yang_y507_conductor39_doubling_orbit_minimality_gate import (
    profile_yang_y507_conductor39_doubling_orbit_minimality,
)


LEGAL_SOURCE_OBJECTS = frozenset(
    {
        "U_chi",
        "V_bal",
        "W",
        "coset_quotient",
        "doubling_orbit_norm",
        "legal_sparse_h90_gauge",
    }
)


@dataclass(frozen=True)
class Conductor39SourceTheoremClaim:
    name: str
    theorem_body_verified: bool
    source_object: str
    emits_conductor39_object: bool
    preserves_mixed_tensor: bool
    yang_yu_legal_unit: bool
    sparse_formal_gauge_only: bool
    proper_axis_or_projection_only: bool
    additive_separated: bool
    yang_distribution_to_507: bool
    frobenius_or_hilbert90_descent: bool
    output_kind: str
    finite_field_identity_or_divisor_theorem: bool
    period_156_context: bool
    danger3_framing: bool
    extraction_to_A_x0: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class Conductor39SourceTheoremDecision:
    claim: Conductor39SourceTheoremClaim
    decision: str
    conductor39_source_identified: bool
    theorem_source_closed: bool
    danger3_route_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class Conductor39SourceTheoremIntakeProfile:
    distribution_lift_ok: bool
    mixed_tensor_ok: bool
    modular_unit_legality_ok: bool
    coset_selector_ok: bool
    coset_frobenius_pairing_ok: bool
    doubling_orbit_norm_ok: bool
    doubling_orbit_minimality_ok: bool
    hilbert90_ok: bool
    hilbert90_legal_gauge_family_ok: bool
    hilbert90_sparse_selector_structure_ok: bool
    hilbert90_sparse_yang_lift_ok: bool
    koo_shin_bridge_ok: bool
    regression_rows: tuple[Conductor39SourceTheoremDecision, ...]
    conductor39_source_identified_rows: int
    theorem_source_closed_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_rows: int
    conditional_rows: int
    helper_only_rows: int
    row_ok: bool


def classify_claim(claim: Conductor39SourceTheoremClaim) -> Conductor39SourceTheoremDecision:
    if not claim.theorem_body_verified:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="reject_no_theorem_body",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="verified theorem statement or proof body",
            next_action="obtain theorem text before routing it into the moonshot",
            row_ok=True,
        )

    if claim.proper_axis_or_projection_only or claim.additive_separated:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="reject_loses_mixed_tensor",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="mixed chi_3 tensor chi_13 source on X_1(39)",
            next_action="reject unless the claim restores both mod-3 row sign and mod-13 character",
            row_ok=True,
        )

    if claim.sparse_formal_gauge_only and not claim.frobenius_or_hilbert90_descent:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="reject_formal_sparse_gauge_without_boundary",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="ratio or Hilbert-90 boundary legitimizing the sparse gauge",
            next_action="keep sparse one-coset gauges as formal potentials only",
            row_ok=True,
        )

    if not claim.emits_conductor39_object or claim.source_object not in LEGAL_SOURCE_OBJECTS:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="conditional_missing_conductor39_source_object",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="U_chi, V_bal, or W on X_1(39)",
            next_action=(
                "ask the theorem to emit the legal conductor-39 unit, full "
                "orbit norm, or legal mixed sparse Hilbert-90 gauge"
            ),
            row_ok=True,
        )

    if not claim.preserves_mixed_tensor:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="reject_conductor39_object_missing_mixed_tensor",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="chi_3 tensor chi_13 row/column signs",
            next_action="reject conductor-39 claims that collapse to an axis or projection",
            row_ok=True,
        )

    if not claim.yang_yu_legal_unit:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="reject_not_legal_x1_39_unit",
            conductor39_source_identified=False,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="Yang/Yu X_1(39) modular-unit legality",
            next_action="run the word through the conductor-39 legality gate",
            row_ok=True,
        )

    if not claim.yang_distribution_to_507:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="conditional_missing_yang_distribution_lift",
            conductor39_source_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="13-fiber Yang distribution from level 39 to level 507",
            next_action="attach Yang distribution_lift_39_to_507 and verify against Norm_156(Y_507)",
            row_ok=True,
        )

    if not claim.frobenius_or_hilbert90_descent:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="conditional_missing_frobenius_or_hilbert90_descent",
            conductor39_source_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="Frobenius anti-invariance, twisted trace, ratio, or Hilbert-90 boundary",
            next_action="reject naive norm-only value routes; ask how the anti-invariant word descends",
            row_ok=True,
        )

    if not claim.finite_field_identity_or_divisor_theorem:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="conductor39_source_identified_value_or_divisor_theorem_missing",
            conductor39_source_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value identity or divisor/additive theorem for the source object",
            next_action="continue from the source object to a theorem that can feed certificate extraction",
            row_ok=True,
        )

    if claim.output_kind == "value" and not claim.period_156_context:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="conditional_missing_period_156_context",
            conductor39_source_identified=True,
            theorem_source_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="period-156 branch/root/telescoping context",
            next_action="ask for support-period 156 fixedness before trusting the value branch",
            row_ok=True,
        )

    theorem_source_closed = claim.output_kind in {"value", "divisor-additive"}
    if theorem_source_closed and not claim.danger3_framing:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="source_theorem_closed_policy_or_framing_missing",
            conductor39_source_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            next_action="settle challenge framing, then derive concrete A and x0",
            row_ok=True,
        )

    if theorem_source_closed and not claim.extraction_to_A_x0:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="danger3_unblocked_extraction_missing",
            conductor39_source_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="extraction algorithm for concrete (A, x0)",
            next_action="derive the DANGER3 triple and run official vpp.py",
            row_ok=True,
        )

    if theorem_source_closed and not claim.concrete_vpp_verified_triple:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="ready_to_extract_and_verify_concrete_triple",
            conductor39_source_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=True,
            submission_ready=False,
            first_missing_clause="official vpp.py verification of a concrete triple",
            next_action="run extraction and official verification",
            row_ok=True,
        )

    if theorem_source_closed:
        return Conductor39SourceTheoremDecision(
            claim=claim,
            decision="submission_ready_verified_triple",
            conductor39_source_identified=True,
            theorem_source_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_clause="none",
            next_action="archive certificate, logs, commit, environment, and submit",
            row_ok=True,
        )

    return Conductor39SourceTheoremDecision(
        claim=claim,
        decision="conditional_unclassified_output_kind",
        conductor39_source_identified=True,
        theorem_source_closed=False,
        danger3_route_unblocked=False,
        extraction_ready=False,
        submission_ready=False,
        first_missing_clause="output kind must be value or divisor-additive",
        next_action="restate claim in conductor-39 source-theorem terms",
        row_ok=True,
    )


def regression_claims() -> tuple[Conductor39SourceTheoremClaim, ...]:
    base = {
        "theorem_body_verified": True,
        "source_object": "U_chi",
        "emits_conductor39_object": True,
        "preserves_mixed_tensor": True,
        "yang_yu_legal_unit": True,
        "sparse_formal_gauge_only": False,
        "proper_axis_or_projection_only": False,
        "additive_separated": False,
        "yang_distribution_to_507": True,
        "frobenius_or_hilbert90_descent": True,
        "output_kind": "divisor-additive",
        "finite_field_identity_or_divisor_theorem": True,
        "period_156_context": False,
        "danger3_framing": True,
        "extraction_to_A_x0": True,
        "concrete_vpp_verified_triple": False,
    }
    return (
        Conductor39SourceTheoremClaim(
            "snippet_only",
            False,
            "unknown",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "source-object",
            False,
            False,
            False,
            False,
            False,
        ),
        Conductor39SourceTheoremClaim(
            "prime13_projection_product",
            True,
            "projection",
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            "divisor-additive",
            False,
            False,
            False,
            False,
            False,
        ),
        Conductor39SourceTheoremClaim(
            "sparse_one_coset_standalone",
            True,
            "V_pos",
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            "source-object",
            False,
            False,
            False,
            False,
            False,
        ),
        Conductor39SourceTheoremClaim(
            "mixed_unit_without_yang_lift",
            **{**base, "yang_distribution_to_507": False, "finite_field_identity_or_divisor_theorem": False},
        ),
        Conductor39SourceTheoremClaim(
            "mixed_unit_yang_without_descent",
            **{**base, "frobenius_or_hilbert90_descent": False, "finite_field_identity_or_divisor_theorem": False},
        ),
        Conductor39SourceTheoremClaim(
            "mixed_unit_yang_descent_no_value_theorem",
            **{**base, "finite_field_identity_or_divisor_theorem": False},
        ),
        Conductor39SourceTheoremClaim(
            "finite_value_without_period156",
            **{**base, "output_kind": "value", "period_156_context": False},
        ),
        Conductor39SourceTheoremClaim(
            "divisor_theorem_policy_missing",
            **{**base, "danger3_framing": False, "extraction_to_A_x0": False},
        ),
        Conductor39SourceTheoremClaim(
            "divisor_theorem_extraction_missing",
            **{**base, "extraction_to_A_x0": False},
        ),
        Conductor39SourceTheoremClaim(
            "divisor_theorem_ready_to_verify",
            **base,
        ),
        Conductor39SourceTheoremClaim(
            "submission_ready_control",
            **{**base, "concrete_vpp_verified_triple": True},
        ),
    )


def profile_conductor39_source_theorem_intake() -> Conductor39SourceTheoremIntakeProfile:
    lift = profile_yang_y507_conductor39_distribution_lift()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()
    legality = profile_yang_y507_conductor39_modular_unit_legality()
    coset = profile_yang_y507_conductor39_coset_selector()
    coset_pairing = profile_yang_y507_conductor39_coset_frobenius_pairing()
    doubling_norm = profile_yang_y507_conductor39_doubling_orbit_norm()
    doubling_minimality = profile_yang_y507_conductor39_doubling_orbit_minimality()
    hilbert90 = profile_yang_y507_conductor39_hilbert90_boundary()
    gauge_family = profile_hilbert90_legal_gauge_family()
    sparse_selector = profile_hilbert90_sparse_selector_structure()
    sparse_yang_lift = profile_sparse_hilbert90_yang_lift()
    koo_bridge = profile_koo_shin_conductor39_distribution_bridge()
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    conditional = sum(row.decision.startswith("conditional_") for row in decisions)
    helper_only = sum(
        row.decision == "conductor39_source_identified_value_or_divisor_theorem_missing"
        for row in decisions
    )
    row_ok = (
        lift.row_ok
        and mixed.row_ok
        and legality.row_ok
        and coset.row_ok
        and coset_pairing.row_ok
        and doubling_norm.row_ok
        and doubling_minimality.row_ok
        and hilbert90.row_ok
        and gauge_family.row_ok
        and sparse_selector.row_ok
        and sparse_yang_lift.row_ok
        and koo_bridge.row_ok
        and lift.source_level == 39
        and lift.target_level == 507
        and mixed.tensor_factorization_ok
        and legality.legal_rows == 2
        and legality.formal_only_rows == 2
        and coset.compact_pair_count == 12
        and coset.coset_quotient_word_equals_primitive
        and coset_pairing.q_value_frobenius_inverse_contract
        and coset_pairing.w_value_frobenius_inverse_contract
        and doubling_norm.orbit_norm_equals_primitive_unit
        and doubling_norm.full_orbit_required
        and doubling_minimality.full_orbit_forced_by_yang_yu
        and doubling_minimality.proper_legal_rows == 0
        and hilbert90.balanced_support == 24
        and hilbert90.sparse_support == 12
        and gauge_family.support12_legal_sparse_rows == 4
        and gauge_family.support12_formal_one_coset_rows == 2
        and sparse_selector.legal_sparse_count == 4
        and sparse_selector.all_legal_sparse_have_vanishing_axis_pushforwards
        and sparse_yang_lift.legal_sparse_lift_count == 4
        and sparse_yang_lift.min_legal_lifted_potential_support == 156
        and sparse_yang_lift.sparse_lift_halves_boundary_support
        and sparse_yang_lift.all_legal_lifts_have_vanishing_axis_pushforwards
        and sparse_yang_lift.all_formal_lifts_have_nonzero_axis_pushforwards
        and tuple(row.decision for row in decisions)
        == (
            "reject_no_theorem_body",
            "reject_loses_mixed_tensor",
            "reject_formal_sparse_gauge_without_boundary",
            "conditional_missing_yang_distribution_lift",
            "conditional_missing_frobenius_or_hilbert90_descent",
            "conductor39_source_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "ready_to_extract_and_verify_concrete_triple",
            "submission_ready_verified_triple",
        )
        and rejected == 3
        and conditional == 3
        and helper_only == 1
        and sum(row.theorem_source_closed for row in decisions) == 4
        and sum(row.danger3_route_unblocked for row in decisions) == 3
        and sum(row.extraction_ready for row in decisions) == 2
        and sum(row.submission_ready for row in decisions) == 1
        and all(row.row_ok for row in decisions)
    )
    return Conductor39SourceTheoremIntakeProfile(
        distribution_lift_ok=lift.row_ok,
        mixed_tensor_ok=mixed.row_ok,
        modular_unit_legality_ok=legality.row_ok,
        coset_selector_ok=coset.row_ok,
        coset_frobenius_pairing_ok=coset_pairing.row_ok,
        doubling_orbit_norm_ok=doubling_norm.row_ok,
        doubling_orbit_minimality_ok=doubling_minimality.row_ok,
        hilbert90_ok=hilbert90.row_ok,
        hilbert90_legal_gauge_family_ok=gauge_family.row_ok,
        hilbert90_sparse_selector_structure_ok=sparse_selector.row_ok,
        hilbert90_sparse_yang_lift_ok=sparse_yang_lift.row_ok,
        koo_shin_bridge_ok=koo_bridge.row_ok,
        regression_rows=decisions,
        conductor39_source_identified_rows=sum(row.conductor39_source_identified for row in decisions),
        theorem_source_closed_rows=sum(row.theorem_source_closed for row in decisions),
        danger3_unblocked_rows=sum(row.danger3_route_unblocked for row in decisions),
        extraction_ready_rows=sum(row.extraction_ready for row in decisions),
        submission_ready_rows=sum(row.submission_ready for row in decisions),
        rejected_rows=rejected,
        conditional_rows=conditional,
        helper_only_rows=helper_only,
        row_ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true", help="classify one candidate claim")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--source-object", default="U_chi")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--emits-conductor39", action="store_true")
    parser.add_argument("--mixed-tensor", action="store_true")
    parser.add_argument("--legal-unit", action="store_true")
    parser.add_argument("--sparse-formal", action="store_true")
    parser.add_argument("--proper-axis-projection", action="store_true")
    parser.add_argument("--additive-separated", action="store_true")
    parser.add_argument("--yang-lift", action="store_true")
    parser.add_argument("--descent", action="store_true")
    parser.add_argument("--output-kind", default="source-object")
    parser.add_argument("--finite-or-divisor", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--extraction", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        decision = classify_claim(
            Conductor39SourceTheoremClaim(
                name=args.name,
                theorem_body_verified=args.theorem_body,
                source_object=args.source_object,
                emits_conductor39_object=args.emits_conductor39,
                preserves_mixed_tensor=args.mixed_tensor,
                yang_yu_legal_unit=args.legal_unit,
                sparse_formal_gauge_only=args.sparse_formal,
                proper_axis_or_projection_only=args.proper_axis_projection,
                additive_separated=args.additive_separated,
                yang_distribution_to_507=args.yang_lift,
                frobenius_or_hilbert90_descent=args.descent,
                output_kind=args.output_kind,
                finite_field_identity_or_divisor_theorem=args.finite_or_divisor,
                period_156_context=args.period_156,
                danger3_framing=args.danger3_framing,
                extraction_to_A_x0=args.extraction,
                concrete_vpp_verified_triple=args.vpp_verified,
            )
        )
        print("p25 KSY-y conductor-39 source-theorem intake candidate")
        print(f"name={decision.claim.name}")
        print(f"decision={decision.decision}")
        print(f"conductor39_source_identified={int(decision.conductor39_source_identified)}")
        print(f"theorem_source_closed={int(decision.theorem_source_closed)}")
        print(f"danger3_route_unblocked={int(decision.danger3_route_unblocked)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"first_missing_clause={decision.first_missing_clause}")
        print(f"next_action={decision.next_action}")
        print(f"ksy_y_conductor39_source_theorem_intake_candidate_rows={int(decision.row_ok)}/1")
        if not decision.row_ok:
            raise SystemExit("conductor-39 source-theorem candidate intake failed")
        return 0

    profile = profile_conductor39_source_theorem_intake()
    print("p25 KSY-y conductor-39 source-theorem intake gate")
    print("inputs")
    print(f"  distribution_lift_ok={int(profile.distribution_lift_ok)}")
    print(f"  mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print(f"  modular_unit_legality_ok={int(profile.modular_unit_legality_ok)}")
    print(f"  coset_selector_ok={int(profile.coset_selector_ok)}")
    print(f"  coset_frobenius_pairing_ok={int(profile.coset_frobenius_pairing_ok)}")
    print(f"  doubling_orbit_norm_ok={int(profile.doubling_orbit_norm_ok)}")
    print(f"  doubling_orbit_minimality_ok={int(profile.doubling_orbit_minimality_ok)}")
    print(f"  hilbert90_ok={int(profile.hilbert90_ok)}")
    print(f"  hilbert90_legal_gauge_family_ok={int(profile.hilbert90_legal_gauge_family_ok)}")
    print(f"  hilbert90_sparse_selector_structure_ok={int(profile.hilbert90_sparse_selector_structure_ok)}")
    print(f"  hilbert90_sparse_yang_lift_ok={int(profile.hilbert90_sparse_yang_lift_ok)}")
    print(f"  koo_shin_bridge_ok={int(profile.koo_shin_bridge_ok)}")
    print("regression_claims")
    for row in profile.regression_rows:
        print(
            "  "
            f"name={row.claim.name} decision={row.decision} "
            f"source={int(row.conductor39_source_identified)} "
            f"closed={int(row.theorem_source_closed)} "
            f"danger3={int(row.danger3_route_unblocked)} "
            f"extract={int(row.extraction_ready)} "
            f"submit={int(row.submission_ready)}"
        )
        print(f"    first_missing_clause={row.first_missing_clause}")
    print("counts")
    print(f"  conductor39_source_identified_rows={profile.conductor39_source_identified_rows}")
    print(f"  theorem_source_closed_rows={profile.theorem_source_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print("interpretation")
    print("  conductor39_theorem_hit_must_emit_legal_mixed_unit_and_yang_lift=1")
    print("  sparse_gauges_need_hilbert90_or_ratio_boundary=1")
    print("  prime_projection_and_axis_only_claims_are_killed=1")
    print("  finite_value_claims_need_period156_context=1")
    print(f"ksy_y_conductor39_source_theorem_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 source-theorem intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
