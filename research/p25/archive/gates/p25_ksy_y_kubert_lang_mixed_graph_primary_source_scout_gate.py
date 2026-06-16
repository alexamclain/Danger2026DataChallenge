#!/usr/bin/env python3
"""Kubert-Lang primary-source scout for the p25 mixed graph.

Kubert-Lang is the right source family for Siegel-function generator/exponent
language, but the p25 KSY-y target needs more than modular-unit hygiene.  This
gate records the exact scout boundary: the source must emit the mixed C_3 x C_169
row graph, reflection-center payload, or raw equal-weight K-traced product.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate import (
    MixedGraphClaim,
    classify_claim as classify_mixed_graph,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate import (
    SourceClaim,
    classify_claim as classify_source_claim,
)


@dataclass(frozen=True)
class KubertLangObservation:
    name: str
    source_clause: str
    source_handle: str
    source_claim: SourceClaim | None
    mixed_graph_claim: MixedGraphClaim
    expected_source_decision: str | None
    expected_mixed_decision: str
    matched_clause: str
    first_missing_clause: str


@dataclass(frozen=True)
class KubertLangScoutProfile:
    source: str
    observations: tuple[KubertLangObservation, ...]
    article_pages_verified: int
    generator_language_rows: int
    direct_closing_rows: int
    finite_payload_rows: int
    conditional_rows: int
    rejected_rows: int
    hypothetical_closing_rows: int
    row_ok: bool


SOURCE = "Kubert-Lang, Units in the Modular Function Field IV. The Siegel Functions are Generators"


def observations() -> tuple[KubertLangObservation, ...]:
    return (
        KubertLangObservation(
            name="kl77_generator_theorem_handle",
            source_clause="article-level generator theorem handle",
            source_handle="EuDML doc 162977 / GDZ LOG_0038, Math. Ann. 227 (1977), 223-242",
            source_claim=SourceClaim(
                "kl77_generator_theorem_handle",
                "kubert_lang_siegel_functions_generators",
                "exponent-hygiene",
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            mixed_graph_claim=MixedGraphClaim(
                "kl77_generator_theorem_handle",
                "Siegel-function generator framework",
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            expected_source_decision="reject_exponent_hygiene_only",
            expected_mixed_decision="reject_c169_or_kl_screen_without_mixed_graph",
            matched_clause="supplies Siegel-function generator/exponent language",
            first_missing_clause="mixed C_3 x C_169 graph selector and finite intake",
        ),
        KubertLangObservation(
            name="kl77_c169_projection_screen",
            source_clause="prime-power projection specialization",
            source_handle="local p25 specialization of Kubert-Lang congruence hygiene",
            source_claim=None,
            mixed_graph_claim=MixedGraphClaim(
                "kl77_c169_projection_screen",
                "C169 projection / KL screen",
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
            expected_source_decision=None,
            expected_mixed_decision="reject_c169_or_kl_screen_without_mixed_graph",
            matched_clause="necessary C169/exponent screen",
            first_missing_clause="C_3 row graph and base-row anchor",
        ),
        KubertLangObservation(
            name="kl77_fixed_t_without_base_anchor",
            source_clause="hypothetical fixed-T cyclic translate",
            source_handle="local p25 calibration row",
            source_claim=None,
            mixed_graph_claim=MixedGraphClaim(
                "kl77_fixed_t_without_base_anchor",
                "fixed-T edge without row anchor",
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
            expected_source_decision=None,
            expected_mixed_decision="conditional_fixed_t_without_base_row_anchor",
            matched_clause="would identify the T edge but not the accepted cyclic row translate",
            first_missing_clause="base row anchor selecting the correct cyclic translate",
        ),
        KubertLangObservation(
            name="kl77_exact_row_labeled_pairs_hypothetical",
            source_clause="not supplied by the generator theorem; calibration row",
            source_handle="local mixed-graph obligation",
            source_claim=None,
            mixed_graph_claim=MixedGraphClaim(
                "kl77_exact_row_labeled_pairs_hypothetical",
                "row-labeled mixed graph",
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
            expected_source_decision=None,
            expected_mixed_decision="finite_mixed_graph_met_by_row_labeled_pairs",
            matched_clause="would satisfy the finite mixed-graph payload",
            first_missing_clause="challenge-legal arithmetic producer theorem",
        ),
        KubertLangObservation(
            name="kl77_raw_product_arithmetic_producer_hypothetical",
            source_clause="not supplied by the generator theorem; closing calibration row",
            source_handle="local closing theorem obligation",
            source_claim=SourceClaim(
                "kl77_raw_product_arithmetic_producer_hypothetical",
                "kubert_lang_siegel_functions_generators",
                "divisor-additive",
                True,
                True,
                False,
                False,
                True,
                False,
            ),
            mixed_graph_claim=MixedGraphClaim(
                "kl77_raw_product_arithmetic_producer_hypothetical",
                "raw equal-weight K-traced product",
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
            expected_source_decision="closing_divisor_or_additive_identity",
            expected_mixed_decision="closing_raw_product_with_arithmetic_producer",
            matched_clause="would close the source theorem side before DANGER3 framing/extraction",
            first_missing_clause="none in source theorem; DANGER3 framing/extraction remains separate",
        ),
    )


def profile_kubert_lang_mixed_graph_scout() -> KubertLangScoutProfile:
    rows = observations()
    source_decisions = tuple(
        classify_source_claim(row.source_claim) if row.source_claim is not None else None
        for row in rows
    )
    mixed_decisions = tuple(classify_mixed_graph(row.mixed_graph_claim) for row in rows)
    generator_rows = sum(int(row.name == "kl77_generator_theorem_handle") for row in rows)
    direct_closing_rows = sum(
        int(
            mixed.closes_arithmetic_route
            and not row.name.endswith("_hypothetical")
            and "hypothetical" not in row.name
        )
        for row, mixed in zip(rows, mixed_decisions)
    )
    finite_payload_rows = sum(
        int(mixed.mixed_graph_obligation_met and not mixed.closes_arithmetic_route)
        for mixed in mixed_decisions
    )
    hypothetical_closing_rows = sum(
        int(mixed.closes_arithmetic_route and "hypothetical" in row.name)
        for row, mixed in zip(rows, mixed_decisions)
    )
    rejected_rows = sum(int(mixed.decision.startswith("reject_")) for mixed in mixed_decisions)
    conditional_rows = len(rows) - direct_closing_rows - finite_payload_rows - hypothetical_closing_rows - rejected_rows
    row_ok = (
        len(rows) == 5
        and generator_rows == 1
        and direct_closing_rows == 0
        and finite_payload_rows == 1
        and conditional_rows == 1
        and rejected_rows == 2
        and hypothetical_closing_rows == 1
        and all(
            source is None or source.decision == row.expected_source_decision
            for row, source in zip(rows, source_decisions)
        )
        and all(
            mixed.decision == row.expected_mixed_decision
            for row, mixed in zip(rows, mixed_decisions)
        )
        and mixed_decisions[0].first_missing_clause == "C_3 row graph and base-row anchor"
    )
    return KubertLangScoutProfile(
        source=SOURCE,
        observations=rows,
        article_pages_verified=20,
        generator_language_rows=generator_rows,
        direct_closing_rows=direct_closing_rows,
        finite_payload_rows=finite_payload_rows,
        conditional_rows=conditional_rows,
        rejected_rows=rejected_rows,
        hypothetical_closing_rows=hypothetical_closing_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_kubert_lang_mixed_graph_scout()
    print("p25 KSY-y Kubert-Lang mixed-graph primary-source scout gate")
    print(f"source={profile.source}")
    print(f"article_pages_verified={profile.article_pages_verified}")
    print("observations")
    for row in profile.observations:
        source_decision = (
            classify_source_claim(row.source_claim).decision
            if row.source_claim is not None
            else "not_run"
        )
        mixed_decision = classify_mixed_graph(row.mixed_graph_claim)
        print(
            "  "
            f"{row.name}: clause={row.source_clause} handle={row.source_handle} "
            f"source_decision={source_decision} mixed_decision={mixed_decision.decision} "
            f"mixed_met={int(mixed_decision.mixed_graph_obligation_met)} "
            f"closes={int(mixed_decision.closes_arithmetic_route)} "
            f"matched={row.matched_clause} missing={mixed_decision.first_missing_clause}"
        )
    print("counts")
    print(f"  generator_language_rows={profile.generator_language_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  finite_payload_rows={profile.finite_payload_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  hypothetical_closing_rows={profile.hypothetical_closing_rows}")
    print("interpretation")
    print("  kubert_lang_generator_language_remains_live=1")
    print("  kl_congruence_or_c169_screen_alone_does_not_close=1")
    print("  exact_row_labeled_pairs_or_reflection_center_are_required=1")
    print("  raw_product_plus_arithmetic_producer_is_the_closing_shape=1")
    print(f"ksy_y_kubert_lang_mixed_graph_primary_source_scout_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Kubert-Lang mixed-graph primary-source scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
