#!/usr/bin/env python3
"""Operational falsifier for the "try 75 atoms" misreading.

The KSY-y target has 75 fixed normalized-y atoms.  Those atoms are not 75
candidate searches: the accepted finite geometry forces the whole equal-weight
product, and DANGER3 completion still needs cross-level `X_1(8112)`/`X_1(16)`
data or an official verified triple.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_atom_terminology_guardrail_gate import profile_atom_terminology_guardrail
from p25_ksy_y_cross_level_extraction_gap_gate import profile_cross_level_extraction_gap
from p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate import (
    profile_atomic_weight_rigidity,
)


@dataclass(frozen=True)
class AtomEnumerationClaim:
    name: str
    treats_atoms_as_search_candidates: bool
    selected_atom_count: int
    equal_weights: bool
    orientation_recorded: bool
    finite_product_identity: bool
    challenge_legal_framing: bool
    cross_level_bridge_or_x16_payload: bool
    official_vpp_verified: bool
    current_evidence: bool


@dataclass(frozen=True)
class AtomEnumerationDecision:
    claim: AtomEnumerationClaim
    decision: str
    source_stage_closed: bool
    extraction_ready: bool
    submission_ready: bool
    current_submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class AtomEnumerationFalsifierProfile:
    atom_guardrail_ok: bool
    atomic_weight_rigidity_ok: bool
    cross_level_extraction_gap_ok: bool
    atom_count: int
    atoms_are_search_candidates: bool
    footprint_terms: int
    atomic_nullity: int
    missing_atom_rejected: bool
    nonuniform_weights_rejected: bool
    rows: tuple[AtomEnumerationDecision, ...]
    row_count: int
    rejected_rows: int
    theorem_missing_rows: int
    source_stage_closed_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def classify_claim(claim: AtomEnumerationClaim) -> AtomEnumerationDecision:
    if claim.official_vpp_verified:
        return AtomEnumerationDecision(
            claim=claim,
            decision="submission_ready_after_official_vpp",
            source_stage_closed=True,
            extraction_ready=True,
            submission_ready=True,
            current_submission_ready=claim.current_evidence,
            first_missing_or_falsifier="none",
            next_action="archive official vpp/Lean bundle and report the triple",
            ok=True,
        )
    if claim.treats_atoms_as_search_candidates:
        return AtomEnumerationDecision(
            claim=claim,
            decision="reject_atom_enumeration_not_a_route",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="75 atoms are fixed product factors, not 75 candidate tries",
            next_action="replace enumeration with an all-75 product identity or a concrete verified triple",
            ok=True,
        )
    if claim.selected_atom_count != 75:
        return AtomEnumerationDecision(
            claim=claim,
            decision="reject_missing_or_extra_atom_count",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="exact theta2 payload forces all 75 fixed atoms",
            next_action="restore the full j=-1..1, k=0..24 product",
            ok=True,
        )
    if not claim.equal_weights:
        return AtomEnumerationDecision(
            claim=claim,
            decision="reject_nonuniform_atom_weights",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="atomic-weight rigidity has nullity 0",
            next_action="use the equal-weight product or an exactly equivalent payload",
            ok=True,
        )
    if not claim.orientation_recorded:
        return AtomEnumerationDecision(
            claim=claim,
            decision="all75_product_orientation_missing",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="theta2/theta2^-1 orientation",
            next_action="record the global product orientation before source/extraction routing",
            ok=True,
        )
    if not claim.finite_product_identity:
        return AtomEnumerationDecision(
            claim=claim,
            decision="all75_product_identity_missing",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="finite arithmetic identity selecting the all-75 product",
            next_action="ask/prove a product, divisor, or value theorem for the fixed product",
            ok=True,
        )
    if not claim.challenge_legal_framing:
        return AtomEnumerationDecision(
            claim=claim,
            decision="all75_product_framing_missing",
            source_stage_closed=False,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="challenge-legal non-CM/finite-field framing",
            next_action="frame the identity as DANGER3-legal finite-field data",
            ok=True,
        )
    if not claim.cross_level_bridge_or_x16_payload:
        return AtomEnumerationDecision(
            claim=claim,
            decision="source_closed_cross_level_extraction_missing",
            source_stage_closed=True,
            extraction_ready=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="same-j X_1(8112) bridge, X_1(16) payload, or concrete triple",
            next_action="route through the cross-level bridge before claiming DANGER3 extraction",
            ok=True,
        )
    return AtomEnumerationDecision(
        claim=claim,
        decision="extraction_ready_official_vpp_missing",
        source_stage_closed=True,
        extraction_ready=True,
        submission_ready=False,
        current_submission_ready=False,
        first_missing_or_falsifier="official DANGER3 vpp.py stdout True",
        next_action="run official vpp.py on the concrete p25 A,x0 payload",
        ok=True,
    )


def regression_claims() -> tuple[AtomEnumerationClaim, ...]:
    return (
        AtomEnumerationClaim(
            "literal_75_tries_plan",
            True,
            1,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "single_atom_payload",
            False,
            1,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "seventy_four_atom_subset",
            False,
            74,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "nonuniform_all75_weights",
            False,
            75,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "all75_orientation_missing",
            False,
            75,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "all75_identity_missing",
            False,
            75,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "all75_framing_missing",
            False,
            75,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "all75_source_closed_extraction_missing",
            False,
            75,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "all75_extraction_ready_vpp_missing",
            False,
            75,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
        ),
        AtomEnumerationClaim(
            "official_vpp_verified_boundary",
            False,
            75,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
        ),
    )


def profile_atom_enumeration_falsifier() -> AtomEnumerationFalsifierProfile:
    atom = profile_atom_terminology_guardrail()
    weights = profile_atomic_weight_rigidity()
    cross = profile_cross_level_extraction_gap()
    rows = tuple(classify_claim(claim) for claim in regression_claims())

    rejected = sum(row.decision.startswith("reject_") for row in rows)
    theorem_missing = sum("identity_missing" in row.decision or "orientation_missing" in row.decision for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)

    expected_decisions = (
        "reject_atom_enumeration_not_a_route",
        "reject_missing_or_extra_atom_count",
        "reject_missing_or_extra_atom_count",
        "reject_nonuniform_atom_weights",
        "all75_product_orientation_missing",
        "all75_product_identity_missing",
        "all75_product_framing_missing",
        "source_closed_cross_level_extraction_missing",
        "extraction_ready_official_vpp_missing",
        "submission_ready_after_official_vpp",
    )
    row_ok = (
        atom.row_ok
        and weights.row_ok
        and cross.row_ok
        and atom.atom_count == 75
        and not atom.atoms_are_search_candidates
        and atom.theta_footprint_terms == 300
        and weights.linear_nullity_from_disjoint_support == 0
        and weights.missing_atom_rejected
        and weights.alternating_k_weights_rejected
        and tuple(row.decision for row in rows) == expected_decisions
        and len(rows) == 10
        and rejected == 4
        and theorem_missing == 2
        and source_closed == 3
        and extraction_ready == 2
        and submission_ready == 1
        and current_submission == 0
    )
    return AtomEnumerationFalsifierProfile(
        atom_guardrail_ok=atom.row_ok,
        atomic_weight_rigidity_ok=weights.row_ok,
        cross_level_extraction_gap_ok=cross.row_ok,
        atom_count=atom.atom_count,
        atoms_are_search_candidates=atom.atoms_are_search_candidates,
        footprint_terms=atom.theta_footprint_terms,
        atomic_nullity=weights.linear_nullity_from_disjoint_support,
        missing_atom_rejected=weights.missing_atom_rejected,
        nonuniform_weights_rejected=weights.alternating_k_weights_rejected,
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        theorem_missing_rows=theorem_missing,
        source_stage_closed_rows=source_closed,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        current_submission_ready_rows=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_atom_enumeration_falsifier()
    print("p25 KSY-y atom-enumeration falsifier gate")
    print("dependencies")
    print(f"  atom_guardrail_ok={int(profile.atom_guardrail_ok)}")
    print(f"  atomic_weight_rigidity_ok={int(profile.atomic_weight_rigidity_ok)}")
    print(f"  cross_level_extraction_gap_ok={int(profile.cross_level_extraction_gap_ok)}")
    print("invariants")
    print(f"  atom_count={profile.atom_count}")
    print(f"  atoms_are_search_candidates={int(profile.atoms_are_search_candidates)}")
    print(f"  footprint_terms={profile.footprint_terms}")
    print(f"  atomic_nullity={profile.atomic_nullity}")
    print(f"  missing_atom_rejected={int(profile.missing_atom_rejected)}")
    print(f"  nonuniform_weights_rejected={int(profile.nonuniform_weights_rejected)}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.claim.name}: decision={row.decision} "
            f"source={int(row.source_stage_closed)} "
            f"extract={int(row.extraction_ready)} "
            f"submit={int(row.submission_ready)} "
            f"current={int(row.current_submission_ready)}"
        )
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  theorem_missing_rows={profile.theorem_missing_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  literal_75_tries_plan_is_rejected=1")
    print("  only_all75_equal_weight_product_can_continue=1")
    print("  all75_product_still_needs_theorem_framing_and_cross_level_extraction=1")
    print(f"ksy_y_atom_enumeration_falsifier_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("atom-enumeration falsifier regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
