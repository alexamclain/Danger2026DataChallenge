#!/usr/bin/env python3
"""DANGER3 framing gate for p25 KSY-y theorem hits.

The official DANGER3 surface is concrete: a candidate is a Pomerance triple
(p, A, x0), and the repository supplies vpp.py / lean_vpp.py to verify such a
triple.  The KSY-y moonshot gates are producer machinery that might generate a
triple; they are not themselves a submitted triple.

This gate keeps three notions separate:

* final submission readiness: a concrete (p,A,x0) triple verified by vpp;
* policy unblocking: Drew/challenge accepts a finite-field identity for P as a
  challenge-legal way to produce a triple;
* theorem closure: an exact product or value-with-period theorem is still
  required even if policy is unblocked.
"""

from __future__ import annotations

from dataclasses import dataclass


P25 = 10000000000000000000000013
REMOTE_DANGER3_HEAD_CHECKED = "a65658b7b194546957fa62f40d60ca63efc37f93"


@dataclass(frozen=True)
class Danger3FramingRow:
    name: str
    claim_kind: str
    has_concrete_triple: bool
    vpp_verified: bool
    lean_generatable: bool
    finite_field_identity_for_p: bool
    exact_product_or_value_theorem: bool
    policy_accepts_finite_identity: bool
    cm_provenance_only: bool
    decision: str
    closes_submission: bool
    unblocks_policy: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class Danger3FramingProfile:
    p: int
    danger3_remote_head_checked: str
    official_submission_surface: str
    readme_no_cm_ban_observed: bool
    framing_rows: tuple[Danger3FramingRow, ...]
    submission_ready_rows: int
    policy_unblocked_non_submission_rows: int
    policy_only_rows: int
    conditional_rows: int
    rejected_rows: int
    row_ok: bool


def classify_row(
    name: str,
    claim_kind: str,
    has_concrete_triple: bool,
    vpp_verified: bool,
    lean_generatable: bool,
    finite_field_identity_for_p: bool,
    exact_product_or_value_theorem: bool,
    policy_accepts_finite_identity: bool,
    cm_provenance_only: bool,
    expected_decision: str,
) -> Danger3FramingRow:
    if has_concrete_triple:
        if vpp_verified:
            decision = "closing_verified_pomerance_triple"
            closes_submission = True
            unblocks_policy = True
            missing = "none"
            next_action = "archive vpp output, generate Lean certificate, and submit/record the triple"
        else:
            decision = "reject_unverified_triple"
            closes_submission = False
            unblocks_policy = False
            missing = "official vpp.py verification"
            next_action = "run official vpp.py; do not treat as a hit until it verifies"
    elif cm_provenance_only and not finite_field_identity_for_p:
        decision = "reject_cm_provenance_without_finite_identity"
        closes_submission = False
        unblocks_policy = False
        missing = "finite-field identity for P or concrete verified triple"
        next_action = "discard broad CM provenance unless reframed as finite-field identity or actual triple"
    elif policy_accepts_finite_identity and exact_product_or_value_theorem and finite_field_identity_for_p:
        decision = "policy_unblocked_theorem_route_not_submission"
        closes_submission = False
        unblocks_policy = True
        missing = "concrete (p,A,x0) triple verified by vpp.py"
        next_action = "use the theorem route to derive A,x0, then verify with official vpp.py"
    elif exact_product_or_value_theorem and finite_field_identity_for_p:
        decision = "conditional_policy_or_framing_missing"
        closes_submission = False
        unblocks_policy = False
        missing = "DANGER3 acceptance of finite-field identity framing"
        next_action = "ask whether a finite-field identity for P avoids the no-CM concern"
    elif policy_accepts_finite_identity and not exact_product_or_value_theorem:
        decision = "policy_only_not_theorem"
        closes_submission = False
        unblocks_policy = True
        missing = "exact product theorem or value theorem with period-156 context"
        next_action = "continue theorem work; policy yes alone does not produce a triple"
    elif finite_field_identity_for_p:
        decision = "conditional_missing_theorem_or_triple"
        closes_submission = False
        unblocks_policy = False
        missing = "source theorem and concrete triple"
        next_action = "attach arithmetic producer theorem, then derive/verify A,x0"
    else:
        decision = "reject_not_submission_or_theorem_route"
        closes_submission = False
        unblocks_policy = False
        missing = "concrete triple or exact finite-field theorem route"
        next_action = "discard for DANGER3 framing"

    return Danger3FramingRow(
        name=name,
        claim_kind=claim_kind,
        has_concrete_triple=has_concrete_triple,
        vpp_verified=vpp_verified,
        lean_generatable=lean_generatable,
        finite_field_identity_for_p=finite_field_identity_for_p,
        exact_product_or_value_theorem=exact_product_or_value_theorem,
        policy_accepts_finite_identity=policy_accepts_finite_identity,
        cm_provenance_only=cm_provenance_only,
        decision=decision,
        closes_submission=closes_submission,
        unblocks_policy=unblocks_policy,
        first_missing_clause=missing,
        next_action=next_action,
        row_ok=decision == expected_decision,
    )


def profile_danger3_framing() -> Danger3FramingProfile:
    rows = (
        classify_row(
            "verified_p25_triple",
            "official triple",
            True,
            True,
            True,
            False,
            False,
            True,
            False,
            "closing_verified_pomerance_triple",
        ),
        classify_row(
            "exact_product_theorem_policy_yes",
            "exact product theorem",
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            "policy_unblocked_theorem_route_not_submission",
        ),
        classify_row(
            "value_period_theorem_policy_yes",
            "value theorem with period-156 context",
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            "policy_unblocked_theorem_route_not_submission",
        ),
        classify_row(
            "exact_product_theorem_policy_unknown",
            "exact product theorem",
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            "conditional_policy_or_framing_missing",
        ),
        classify_row(
            "finite_payload_no_source_theorem",
            "finite verifier payload",
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            "conditional_missing_theorem_or_triple",
        ),
        classify_row(
            "danger3_policy_yes_only",
            "policy answer",
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            "policy_only_not_theorem",
        ),
        classify_row(
            "generic_cm_lang_generation",
            "CM/Lang generation",
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            "reject_cm_provenance_without_finite_identity",
        ),
        classify_row(
            "claimed_triple_fails_vpp",
            "official triple",
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            "reject_unverified_triple",
        ),
    )

    submission_ready = sum(int(row.closes_submission) for row in rows)
    policy_unblocked_non_submission = sum(
        int(row.unblocks_policy and not row.closes_submission and row.exact_product_or_value_theorem)
        for row in rows
    )
    policy_only = sum(int(row.decision == "policy_only_not_theorem") for row in rows)
    conditional = sum(int(row.decision.startswith("conditional")) for row in rows)
    rejected = sum(int(row.decision.startswith("reject")) for row in rows)
    row_ok = (
        P25 == 10000000000000000000000013
        and len(rows) == 8
        and submission_ready == 1
        and policy_unblocked_non_submission == 2
        and policy_only == 1
        and conditional == 2
        and rejected == 2
        and all(row.row_ok for row in rows)
        and all(not row.closes_submission for row in rows if not row.has_concrete_triple)
        and all(not row.closes_submission for row in rows if row.has_concrete_triple and not row.vpp_verified)
    )

    return Danger3FramingProfile(
        p=P25,
        danger3_remote_head_checked=REMOTE_DANGER3_HEAD_CHECKED,
        official_submission_surface="concrete (p,A,x0) Pomerance triple verified by vpp.py / lean_vpp.py",
        readme_no_cm_ban_observed=True,
        framing_rows=rows,
        submission_ready_rows=submission_ready,
        policy_unblocked_non_submission_rows=policy_unblocked_non_submission,
        policy_only_rows=policy_only,
        conditional_rows=conditional,
        rejected_rows=rejected,
        row_ok=row_ok,
    )


def print_row(row: Danger3FramingRow) -> None:
    print(
        "  "
        f"{row.name}: kind={row.claim_kind} triple={int(row.has_concrete_triple)} "
        f"vpp={int(row.vpp_verified)} lean={int(row.lean_generatable)} "
        f"finite_identity={int(row.finite_field_identity_for_p)} "
        f"theorem={int(row.exact_product_or_value_theorem)} "
        f"policy={int(row.policy_accepts_finite_identity)} "
        f"cm_only={int(row.cm_provenance_only)} "
        f"submission={int(row.closes_submission)} decision={row.decision} "
        f"missing={row.first_missing_clause}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y DANGER3 framing gate")
    profile = profile_danger3_framing()
    print(f"danger3_framing_profile={profile}")
    print("official_surface")
    print(f"  p={profile.p}")
    print(f"  danger3_remote_head_checked={profile.danger3_remote_head_checked}")
    print(f"  official_submission_surface={profile.official_submission_surface}")
    print(f"  readme_no_cm_ban_observed={int(profile.readme_no_cm_ban_observed)}")
    print("framing_rows")
    for row in profile.framing_rows:
        print_row(row)
    print("counts")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  policy_unblocked_non_submission_rows={profile.policy_unblocked_non_submission_rows}")
    print(f"  policy_only_rows={profile.policy_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  verified_triple_is_the_final_DANGER3_submission_surface=1")
    print("  policy_yes_unblocks_but_does_not_replace_theorem_or_triple=1")
    print("  theorem_route_still_must_derive_A_x0_and_pass_vpp=1")
    print("  generic_CM_provenance_without_finite_identity_is_rejected=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
