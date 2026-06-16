#!/usr/bin/env python3
"""Mixed-graph obligation gate for p25 KSY-y source claims.

The source-parameter hygiene gate separated the source meanings of `[2]`,
`D=2`, raw `D=(22,3)`, and levels `169/507/12675`.  The next theorem-facing
obligation is the mixed graph itself: a source cannot close the KSY-y route by
showing only the `C_169` projection or ordinary Kubert-Lang congruence hygiene.

This gate consolidates the existing row-law, row-labeled-pair, permutation,
reflection-center, and raw-product gates into a single intake rule:

* exact row-labeled pairs, quotient reflection-center data, or a stronger raw
  product satisfy the finite mixed-graph obligation;
* C-axis projections, row masks, wrong pairings, and KL congruences alone do
  not;
* fixed-T cyclic row translates remain conditional until the base row anchor is
  supplied.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate import (
    profile_anti_invariant_producer_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_graph_row_law_gate import (
    profile_graph_row_law,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_graph_separability_gate import (
    profile_graph_separability,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate import (
    profile_reflection_center_candidate,
    profile_reflection_center_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate import (
    profile_row_labeled_pair_candidate,
    profile_row_labeled_pair_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_gate import (
    profile_row_pair_permutation_rigidity,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate import (
    profile_source_parameter_hygiene,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class MixedGraphClaim:
    name: str
    claim_kind: str
    has_c169_projection: bool
    has_kl_congruences: bool
    has_one_pair_per_row: bool
    has_fixed_t_edge: bool
    has_base_row_anchor: bool
    has_exact_row_labeled_pairs: bool
    has_reflection_center: bool
    has_raw_product_payload: bool
    has_arithmetic_producer: bool


@dataclass(frozen=True)
class MixedGraphDecision:
    claim: MixedGraphClaim
    decision: str
    mixed_graph_obligation_met: bool
    closes_arithmetic_route: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class MixedGraphObligationProfile:
    source_parameter_hygiene_ok: bool
    graph_row_law_ok: bool
    graph_separability_ok: bool
    row_labeled_pair_contract_ok: bool
    row_pair_permutation_rigidity_ok: bool
    reflection_center_contract_ok: bool
    anti_invariant_producer_contract_ok: bool
    regression_rows: tuple[MixedGraphDecision, ...]
    finite_obligation_rows: int
    arithmetic_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    row_ok: bool


def classify_claim(claim: MixedGraphClaim) -> MixedGraphDecision:
    if claim.has_raw_product_payload:
        missing = "challenge-legal arithmetic producer theorem"
        route_closes = claim.has_arithmetic_producer
        return MixedGraphDecision(
            claim=claim,
            decision=(
                "closing_raw_product_with_arithmetic_producer"
                if route_closes
                else "finite_mixed_graph_met_by_raw_product"
            ),
            mixed_graph_obligation_met=True,
            closes_arithmetic_route=route_closes,
            first_missing_clause="none" if route_closes else missing,
            next_action=(
                "route through exact-product intake and DANGER3 framing"
                if route_closes
                else "attach a source theorem proving the raw equal-weight product"
            ),
            row_ok=True,
        )

    if claim.has_reflection_center:
        missing = "challenge-legal arithmetic producer theorem"
        route_closes = claim.has_arithmetic_producer
        return MixedGraphDecision(
            claim=claim,
            decision=(
                "closing_reflection_center_with_arithmetic_producer"
                if route_closes
                else "finite_mixed_graph_met_by_reflection_center"
            ),
            mixed_graph_obligation_met=True,
            closes_arithmetic_route=route_closes,
            first_missing_clause="none" if route_closes else missing,
            next_action=(
                "derive base=C-D and T=-2C, then route through certificate path"
                if route_closes
                else "attach a source theorem producing the reflected center and D"
            ),
            row_ok=True,
        )

    if claim.has_exact_row_labeled_pairs:
        missing = "challenge-legal arithmetic producer theorem"
        route_closes = claim.has_arithmetic_producer
        return MixedGraphDecision(
            claim=claim,
            decision=(
                "closing_row_labeled_pairs_with_arithmetic_producer"
                if route_closes
                else "finite_mixed_graph_met_by_row_labeled_pairs"
            ),
            mixed_graph_obligation_met=True,
            closes_arithmetic_route=route_closes,
            first_missing_clause="none" if route_closes else missing,
            next_action=(
                "primitive-K lift, theta2 route, then DANGER3 framing"
                if route_closes
                else "attach a source theorem producing the exact row-labeled pairs"
            ),
            row_ok=True,
        )

    if claim.has_fixed_t_edge and not claim.has_base_row_anchor:
        return MixedGraphDecision(
            claim=claim,
            decision="conditional_fixed_t_without_base_row_anchor",
            mixed_graph_obligation_met=False,
            closes_arithmetic_route=False,
            first_missing_clause="base row anchor selecting the correct cyclic translate",
            next_action="ask for C=-T/2 row or exact source-packet contract data",
            row_ok=True,
        )

    if claim.has_one_pair_per_row:
        return MixedGraphDecision(
            claim=claim,
            decision="reject_one_pair_per_row_without_correct_pairing",
            mixed_graph_obligation_met=False,
            closes_arithmetic_route=False,
            first_missing_clause="exact row-labeled pair assignment",
            next_action="feed the six triples to the row-labeled-pair contract",
            row_ok=True,
        )

    if claim.has_c169_projection or claim.has_kl_congruences:
        return MixedGraphDecision(
            claim=claim,
            decision="reject_c169_or_kl_screen_without_mixed_graph",
            mixed_graph_obligation_met=False,
            closes_arithmetic_route=False,
            first_missing_clause="C_3 row graph and base-row anchor",
            next_action="continue only if the source emits row labels, reflection center, or raw product",
            row_ok=True,
        )

    return MixedGraphDecision(
        claim=claim,
        decision="reject_no_mixed_graph_payload",
        mixed_graph_obligation_met=False,
        closes_arithmetic_route=False,
        first_missing_clause="mixed C_3 x C_169 payload",
        next_action="map the claim to row-labeled pairs, reflection center, or raw product",
        row_ok=True,
    )


def regression_claims() -> tuple[MixedGraphClaim, ...]:
    return (
        MixedGraphClaim(
            "c169_projection_only",
            "C-axis projection",
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        MixedGraphClaim(
            "kl_congruence_hygiene_only",
            "KL exponent screen",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        MixedGraphClaim(
            "one_pair_per_row_wrong_pairing",
            "row-pair shadow",
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        MixedGraphClaim(
            "fixed_t_translate_no_anchor",
            "fixed-T cyclic translate",
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        MixedGraphClaim(
            "exact_row_labeled_pairs",
            "six quotient triples",
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
        ),
        MixedGraphClaim(
            "reflection_center_cd",
            "reflection center",
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
        ),
        MixedGraphClaim(
            "raw_equal_weight_product",
            "raw product",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
        ),
        MixedGraphClaim(
            "raw_product_with_source_theorem",
            "raw product theorem",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
    )


def profile_mixed_graph_obligation() -> MixedGraphObligationProfile:
    hygiene = profile_source_parameter_hygiene()
    row_law = profile_graph_row_law()
    separability = profile_graph_separability()
    row_pairs = profile_row_labeled_pair_contract()
    permutation = profile_row_pair_permutation_rigidity()
    reflection = profile_reflection_center_contract()
    raw_contract = profile_anti_invariant_producer_contract()

    target_pairs = profile_row_labeled_pair_candidate(
        "mixed_graph_obligation_target_pairs",
        {
            (0, 31): 1,
            (0, 138): -1,
            (1, 25): 1,
            (1, 141): -1,
            (2, 28): 1,
            (2, 144): -1,
        },
    )
    target_center = profile_reflection_center_candidate(
        "mixed_graph_obligation_reflection_center",
        (2, 28),
        (1, 3),
        1,
    )
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    finite_rows = sum(int(row.mixed_graph_obligation_met) for row in decisions)
    arithmetic_rows = sum(int(row.closes_arithmetic_route) for row in decisions)
    conditional_rows = sum(int(row.decision.startswith("conditional_")) for row in decisions)
    rejected_rows = sum(int(row.decision.startswith("reject_")) for row in decisions)
    row_ok = (
        hygiene.row_ok
        and row_law.row_ok
        and separability.row_ok
        and row_pairs.row_ok
        and permutation.row_ok
        and reflection.row_ok
        and raw_contract.row_ok
        and target_pairs.ok
        and target_pairs.row_labeled_pairs_exact
        and target_center.ok
        and finite_rows == 4
        and arithmetic_rows == 1
        and conditional_rows == 1
        and rejected_rows == 3
        and tuple(row.decision for row in decisions)
        == (
            "reject_c169_or_kl_screen_without_mixed_graph",
            "reject_c169_or_kl_screen_without_mixed_graph",
            "reject_one_pair_per_row_without_correct_pairing",
            "conditional_fixed_t_without_base_row_anchor",
            "finite_mixed_graph_met_by_row_labeled_pairs",
            "finite_mixed_graph_met_by_reflection_center",
            "finite_mixed_graph_met_by_raw_product",
            "closing_raw_product_with_arithmetic_producer",
        )
        and all(row.row_ok for row in decisions)
    )
    return MixedGraphObligationProfile(
        source_parameter_hygiene_ok=hygiene.row_ok,
        graph_row_law_ok=row_law.row_ok,
        graph_separability_ok=separability.row_ok,
        row_labeled_pair_contract_ok=row_pairs.row_ok,
        row_pair_permutation_rigidity_ok=permutation.row_ok,
        reflection_center_contract_ok=reflection.row_ok,
        anti_invariant_producer_contract_ok=raw_contract.row_ok,
        regression_rows=decisions,
        finite_obligation_rows=finite_rows,
        arithmetic_closing_rows=arithmetic_rows,
        conditional_rows=conditional_rows,
        rejected_rows=rejected_rows,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> MixedGraphClaim:
    return MixedGraphClaim(
        name=args.name,
        claim_kind=args.kind,
        has_c169_projection=args.c169_projection,
        has_kl_congruences=args.kl_congruences,
        has_one_pair_per_row=args.one_pair_per_row,
        has_fixed_t_edge=args.fixed_t_edge,
        has_base_row_anchor=args.base_row_anchor,
        has_exact_row_labeled_pairs=args.exact_row_labeled_pairs,
        has_reflection_center=args.reflection_center,
        has_raw_product_payload=args.raw_product,
        has_arithmetic_producer=args.arithmetic_producer,
    )


def print_decision(decision: MixedGraphDecision) -> None:
    claim = decision.claim
    print(
        "  "
        f"{claim.name}: kind={claim.claim_kind} "
        f"c169={int(claim.has_c169_projection)} "
        f"kl={int(claim.has_kl_congruences)} "
        f"pairs={int(claim.has_one_pair_per_row)} "
        f"fixedT={int(claim.has_fixed_t_edge)} "
        f"base_anchor={int(claim.has_base_row_anchor)} "
        f"exact_pairs={int(claim.has_exact_row_labeled_pairs)} "
        f"reflection={int(claim.has_reflection_center)} "
        f"raw={int(claim.has_raw_product_payload)} "
        f"producer={int(claim.has_arithmetic_producer)} "
        f"decision={decision.decision} "
        f"mixed_graph_met={int(decision.mixed_graph_obligation_met)} "
        f"closes_arithmetic={int(decision.closes_arithmetic_route)} "
        f"missing={decision.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify p25 KSY-y mixed C3 x C169 graph source claims."
    )
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--kind", default="unspecified")
    parser.add_argument("--c169-projection", action="store_true")
    parser.add_argument("--kl-congruences", action="store_true")
    parser.add_argument("--one-pair-per-row", action="store_true")
    parser.add_argument("--fixed-t-edge", action="store_true")
    parser.add_argument("--base-row-anchor", action="store_true")
    parser.add_argument("--exact-row-labeled-pairs", action="store_true")
    parser.add_argument("--reflection-center", action="store_true")
    parser.add_argument("--raw-product", action="store_true")
    parser.add_argument("--arithmetic-producer", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang KSY-y mixed-graph obligation gate")
    if args.candidate:
        decision = classify_claim(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(
            "robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_candidate_rows="
            f"{int(decision.row_ok)}/1"
        )
        return 0 if decision.row_ok and not decision.decision.startswith("reject_") else 1

    profile = profile_mixed_graph_obligation()
    print(f"mixed_graph_obligation_profile={profile}")
    print("dependency_gates")
    print(f"  source_parameter_hygiene_ok={int(profile.source_parameter_hygiene_ok)}")
    print(f"  graph_row_law_ok={int(profile.graph_row_law_ok)}")
    print(f"  graph_separability_ok={int(profile.graph_separability_ok)}")
    print(f"  row_labeled_pair_contract_ok={int(profile.row_labeled_pair_contract_ok)}")
    print(
        "  "
        f"row_pair_permutation_rigidity_ok="
        f"{int(profile.row_pair_permutation_rigidity_ok)}"
    )
    print(f"  reflection_center_contract_ok={int(profile.reflection_center_contract_ok)}")
    print(
        "  "
        f"anti_invariant_producer_contract_ok="
        f"{int(profile.anti_invariant_producer_contract_ok)}"
    )
    print("regression_rows")
    for decision in profile.regression_rows:
        print_decision(decision)
    print("counts")
    print(f"  finite_obligation_rows={profile.finite_obligation_rows}")
    print(f"  arithmetic_closing_rows={profile.arithmetic_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  C169_projection_and_KL_congruences_are_screens_not_payloads=1")
    print("  fixed_T_edge_still_needs_base_row_anchor=1")
    print("  exact_row_labeled_pairs_or_reflection_center_satisfy_finite_graph_obligation=1")
    print("  raw_product_plus_arithmetic_producer_is_the_closing_source_shape=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("mixed-graph obligation regression failed")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
