#!/usr/bin/env python3
"""Candidate matcher for H0 source-theorem claims in the p25 moonshot.

This is the executable intake form for future paper snippets, expert answers,
or subagent reports.  It classifies whether a proposed H0 theorem hits one of
the four exact legal products, whether it is one of the two source-closing
answer shapes, and how far it gets through the DANGER3 extraction ladder.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780
LEGAL_MULTIPLIERS = (1, 2, 4, 8)
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class H0ProductTarget:
    multiplier: int
    target_object: str
    constants: tuple[int, ...]
    positive_residues: tuple[int, ...]
    negative_residues: tuple[int, ...]


@dataclass(frozen=True)
class H0SourceTheoremCandidate:
    name: str
    product_multiplier: int | None
    residue_sets_exact: bool
    arithmetic_source_theorem: bool
    output_kind: str
    period156_context: bool
    h90_boundary: bool
    danger3_framing: bool
    same_j_x18112_bridge: bool
    x16_surface: bool
    concrete_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class H0SourceTheoremDecision:
    candidate: H0SourceTheoremCandidate
    legal_h0_product: bool
    source_stage_closed: bool
    downstream_unblocked: bool
    submission_ready: bool
    decision: str
    first_missing_clause: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0SourceTheoremCandidateMatcher:
    exact_product_marker_present: bool
    minimal_ask_marker_present: bool
    final_boundary_marker_present: bool
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    product_targets: tuple[H0ProductTarget, ...]
    regression_rows: tuple[H0SourceTheoremDecision, ...]
    row_count: int
    legal_product_rows: int
    source_closing_rows: int
    source_certified_only_rows: int
    conditional_rows: int
    rejected_rows: int
    downstream_unblocked_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def product_targets() -> tuple[H0ProductTarget, ...]:
    return (
        H0ProductTarget(
            multiplier=1,
            target_object="canonical_H0",
            constants=(3, 3, -3, -3),
            positive_residues=(7, 17, 23, 34, 37, 38),
            negative_residues=(4, 8, 10, 11, 20, 25),
        ),
        H0ProductTarget(
            multiplier=2,
            target_object="H0_translate",
            constants=(-3, 3, 3, -3),
            positive_residues=(7, 14, 29, 34, 35, 37),
            negative_residues=(1, 8, 11, 16, 20, 22),
        ),
        H0ProductTarget(
            multiplier=4,
            target_object="H0_translate",
            constants=(-3, -3, 3, 3),
            positive_residues=(14, 19, 28, 29, 31, 35),
            negative_residues=(1, 2, 5, 16, 22, 32),
        ),
        H0ProductTarget(
            multiplier=8,
            target_object="H0_translate",
            constants=(3, -3, -3, 3),
            positive_residues=(17, 19, 23, 28, 31, 38),
            negative_residues=(2, 4, 5, 10, 25, 32),
        ),
    )


def hits_legal_h0_product(candidate: H0SourceTheoremCandidate) -> bool:
    return (
        candidate.product_multiplier in LEGAL_MULTIPLIERS
        and candidate.residue_sets_exact
    )


def classify_candidate(candidate: H0SourceTheoremCandidate) -> H0SourceTheoremDecision:
    legal_product = hits_legal_h0_product(candidate)
    if candidate.official_vpp and candidate.concrete_x0:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=legal_product,
            source_stage_closed=True,
            downstream_unblocked=True,
            submission_ready=True,
            decision="submission_ready",
            first_missing_clause="none",
            next_action="archive vpp output, environment, command, and generate the Lean certificate",
            ok=True,
        )

    if not legal_product:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=False,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="reject_wrong_or_nonlegal_h0_product",
            first_missing_clause="one of the four exact legal H0 residue products",
            next_action="remap to multiplier 1,2,4,8 with exact P/N residue sets or discard",
            ok=True,
        )

    if not candidate.arithmetic_source_theorem:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="conditional_finite_payload_without_source_theorem",
            first_missing_clause="challenge-legal arithmetic source theorem",
            next_action="keep as verifier data only",
            ok=True,
        )

    if candidate.output_kind == "source-certification":
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="source_certified_value_or_divisor_missing",
            first_missing_clause="finite-field value/divisor theorem for one exact H0 product",
            next_action="ask only value-period156 or divisor/additive upgrade questions",
            ok=True,
        )

    if candidate.output_kind == "value" and not candidate.period156_context:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="conditional_missing_period_156_context",
            first_missing_clause="support-period 156 branch/root/telescoping context",
            next_action="ask for period-156 fixedness or equivalent telescoping witness",
            ok=True,
        )

    if candidate.output_kind == "divisor-additive" and not candidate.h90_boundary:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="conditional_divisor_identity_missing_h90_boundary",
            first_missing_clause="Hilbert-90 boundary to Norm_156(Y_507)",
            next_action="ask for the exact boundary relation on the same H0 product",
            ok=True,
        )

    if not (
        (candidate.output_kind == "value" and candidate.period156_context)
        or (candidate.output_kind == "divisor-additive" and candidate.h90_boundary)
    ):
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=False,
            downstream_unblocked=False,
            submission_ready=False,
            decision="reject_nonclosing_output_kind",
            first_missing_clause="period-156 value identity or divisor/additive identity",
            next_action="discard as source closer unless reframed as an accepted answer shape",
            ok=True,
        )

    if not candidate.danger3_framing:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=True,
            downstream_unblocked=False,
            submission_ready=False,
            decision="source_theorem_closed_policy_or_framing_missing",
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            next_action="resolve challenge framing, then seek same-j X1(8112) bridge",
            ok=True,
        )

    if not candidate.same_j_x18112_bridge:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=True,
            downstream_unblocked=False,
            submission_ready=False,
            decision="upstream_odd_value_no_cross_level_bridge",
            first_missing_clause="X_1(16) relation or X_1(8112) fiber-product theorem",
            next_action="derive a same-j cross-level bridge",
            ok=True,
        )

    if not candidate.x16_surface:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=True,
            downstream_unblocked=False,
            submission_ready=False,
            decision="cross_level_target_identified_specialization_missing",
            first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            next_action="specialize the bridge to the practical X1(16) chart",
            ok=True,
        )

    if not candidate.concrete_x0:
        return H0SourceTheoremDecision(
            candidate=candidate,
            legal_h0_product=True,
            source_stage_closed=True,
            downstream_unblocked=True,
            submission_ready=False,
            decision="x16_surface_reached_halving_or_vpp_missing",
            first_missing_clause="valid halving chain from xP16 to concrete x0",
            next_action="halve from depth 4 to x0 or emit direct A,x0",
            ok=True,
        )

    return H0SourceTheoremDecision(
        candidate=candidate,
        legal_h0_product=True,
        source_stage_closed=True,
        downstream_unblocked=True,
        submission_ready=False,
        decision="extraction_ready_vpp_missing",
        first_missing_clause="official vpp.py verification",
        next_action="run official vpp.py on the concrete (p,A,x0)",
        ok=True,
    )


def regression_candidates() -> tuple[H0SourceTheoremCandidate, ...]:
    return (
        H0SourceTheoremCandidate(
            "ks62_legality_only",
            1,
            True,
            True,
            "source-certification",
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "exact_value_period156_no_framing",
            2,
            True,
            True,
            "value",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "exact_divisor_h90_no_framing",
            4,
            True,
            True,
            "divisor-additive",
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "ambient_bare_value",
            8,
            True,
            True,
            "value",
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "computed_payload_without_source",
            1,
            True,
            False,
            "computed-payload",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "wrong_residue_sets",
            2,
            False,
            True,
            "value",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "nonlegal_projection",
            13,
            True,
            True,
            "value",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "divisor_missing_h90_boundary",
            4,
            True,
            True,
            "divisor-additive",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "framed_source_no_cross_level",
            8,
            True,
            True,
            "value",
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "same_j_bridge_no_x16_specialization",
            1,
            True,
            True,
            "value",
            True,
            True,
            True,
            True,
            False,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "x16_surface_no_x0",
            2,
            True,
            True,
            "divisor-additive",
            False,
            True,
            True,
            True,
            True,
            False,
            False,
        ),
        H0SourceTheoremCandidate(
            "x0_payload_no_vpp",
            4,
            True,
            True,
            "value",
            True,
            True,
            True,
            True,
            True,
            True,
            False,
        ),
        H0SourceTheoremCandidate(
            "official_vpp_verified_triple",
            8,
            True,
            True,
            "value",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
    )


def profile_h0_source_theorem_candidate_matcher() -> H0SourceTheoremCandidateMatcher:
    exact_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_exact_product_query_packet_20260614.md",
        "ksy_y_h0_translate_exact_product_query_packet_rows=1/1",
    )
    minimal_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_minimal_closing_ask_packet_20260614.md",
        "ksy_y_h0_minimal_closing_ask_packet_rows=1/1",
    )
    final_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_x16_final_certificate_boundary_20260614.md",
        "ksy_y_h0_x16_final_certificate_boundary_rows=1/1",
    )
    support_root_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_root_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    targets = product_targets()
    decisions = tuple(classify_candidate(candidate) for candidate in regression_candidates())
    legal_products = sum(row.legal_h0_product for row in decisions)
    source_closing = sum(row.source_stage_closed for row in decisions)
    source_certified = sum(row.decision == "source_certified_value_or_divisor_missing" for row in decisions)
    conditional = sum(row.decision.startswith("conditional_") for row in decisions)
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    downstream = sum(row.downstream_unblocked for row in decisions)
    submission = sum(row.submission_ready for row in decisions)
    row_ok = (
        exact_marker
        and minimal_marker
        and final_marker
        and SUPPORT_PERIOD == 156
        and AMBIENT_PERIOD == 780
        and support_root_gcd == 1
        and ambient_root_gcd == 11
        and tuple(target.multiplier for target in targets) == LEGAL_MULTIPLIERS
        and len(decisions) == 13
        and legal_products == 11
        and source_closing == 7
        and source_certified == 1
        and conditional == 3
        and rejected == 2
        and downstream == 3
        and submission == 1
        and tuple(row.decision for row in decisions)
        == (
            "source_certified_value_or_divisor_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_missing_period_156_context",
            "conditional_finite_payload_without_source_theorem",
            "reject_wrong_or_nonlegal_h0_product",
            "reject_wrong_or_nonlegal_h0_product",
            "conditional_divisor_identity_missing_h90_boundary",
            "upstream_odd_value_no_cross_level_bridge",
            "cross_level_target_identified_specialization_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in decisions)
    )
    return H0SourceTheoremCandidateMatcher(
        exact_product_marker_present=exact_marker,
        minimal_ask_marker_present=minimal_marker,
        final_boundary_marker_present=final_marker,
        support_period_root_gcd=support_root_gcd,
        ambient_period_root_gcd=ambient_root_gcd,
        product_targets=targets,
        regression_rows=decisions,
        row_count=len(decisions),
        legal_product_rows=legal_products,
        source_closing_rows=source_closing,
        source_certified_only_rows=source_certified,
        conditional_rows=conditional,
        rejected_rows=rejected,
        downstream_unblocked_rows=downstream,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> H0SourceTheoremCandidate:
    return H0SourceTheoremCandidate(
        name="cli_candidate",
        product_multiplier=args.product_multiplier,
        residue_sets_exact=args.residue_exact,
        arithmetic_source_theorem=args.source_theorem,
        output_kind=args.output_kind,
        period156_context=args.period_156,
        h90_boundary=args.h90_boundary,
        danger3_framing=args.danger3,
        same_j_x18112_bridge=args.same_j,
        x16_surface=args.x16,
        concrete_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(decision: H0SourceTheoremDecision) -> None:
    candidate = decision.candidate
    print(
        "  "
        f"{candidate.name}: multiplier={candidate.product_multiplier} "
        f"residue_exact={int(candidate.residue_sets_exact)} "
        f"source={int(candidate.arithmetic_source_theorem)} "
        f"kind={candidate.output_kind} period156={int(candidate.period156_context)} "
        f"h90={int(candidate.h90_boundary)} danger3={int(candidate.danger3_framing)} "
        f"same_j={int(candidate.same_j_x18112_bridge)} x16={int(candidate.x16_surface)} "
        f"x0={int(candidate.concrete_x0)} vpp={int(candidate.official_vpp)} "
        f"decision={decision.decision} source_closed={int(decision.source_stage_closed)} "
        f"downstream={int(decision.downstream_unblocked)} "
        f"submission={int(decision.submission_ready)} missing={decision.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify H0 source-theorem candidate shapes.")
    parser.add_argument("--product-multiplier", type=int)
    parser.add_argument("--residue-exact", action="store_true")
    parser.add_argument("--source-theorem", action="store_true")
    parser.add_argument(
        "--output-kind",
        default="source-certification",
        choices=("source-certification", "value", "divisor-additive", "computed-payload", "other"),
    )
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--h90-boundary", action="store_true")
    parser.add_argument("--danger3", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--x16", action="store_true")
    parser.add_argument("--x0", action="store_true")
    parser.add_argument("--vpp", action="store_true")
    args = parser.parse_args()

    print("p25 KSY-y H0 source-theorem candidate matcher gate")
    if args.product_multiplier is not None:
        decision = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(f"ksy_y_h0_source_theorem_candidate_matcher_candidate_rows={int(decision.ok)}/1")
        return 0 if decision.ok else 1

    profile = profile_h0_source_theorem_candidate_matcher()
    print("dependencies")
    print(f"  exact_product_marker_present={int(profile.exact_product_marker_present)}")
    print(f"  minimal_ask_marker_present={int(profile.minimal_ask_marker_present)}")
    print(f"  final_boundary_marker_present={int(profile.final_boundary_marker_present)}")
    print("target_family")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    for target in profile.product_targets:
        print(
            "  "
            f"m={target.multiplier} object={target.target_object} "
            f"constants={target.constants} P={target.positive_residues} "
            f"N={target.negative_residues}"
        )
    print("regression_rows")
    for decision in profile.regression_rows:
        print_decision(decision)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  legal_product_rows={profile.legal_product_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  downstream_unblocked_rows={profile.downstream_unblocked_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  value_claims_need_period156_context=1")
    print("  divisor_claims_need_h90_boundary=1")
    print("  source_yes_still_needs_danger3_same_j_x16_and_vpp=1")
    print("  official_vpp_verified_A_x0_is_the_only_submission_ready_row=1")
    print(f"ksy_y_h0_source_theorem_candidate_matcher_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 source-theorem candidate matcher regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
