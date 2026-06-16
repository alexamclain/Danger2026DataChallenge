#!/usr/bin/env python3
"""KSY source-split gate for the p25 priority-1 divisor lane.

Koo-Shin-Yoon is live for priority 1 only through the normalized-y/Siegel
formula after it is upgraded to an exact p25 product theorem.  The same paper
also contains ray-class generation and single-y-value invariant statements;
those are useful context, but they are not the exact K-traced anti-invariant
product needed by the moonshot.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_ksy_exact_p_primary_source_scout_gate import profile_ksy_exact_p_scout
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product_claim,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    profile_ksy_y_siegel_formula,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate import (
    SourceClaim,
    classify_claim as classify_source_claim,
)


@dataclass(frozen=True)
class KsySourceSplitRow:
    name: str
    source_url: str
    verified_clause: str
    source_role: str
    priority1_output_type: str
    observed_decision: str
    expected_decision: str
    first_missing_clause: str
    recommendation: str
    closes_priority1: bool
    row_ok: bool


@dataclass(frozen=True)
class KsySourceSplitProfile:
    ksy_scout_ok: bool
    siegel_formula_ok: bool
    rows: tuple[KsySourceSplitRow, ...]
    formula_language_rows: int
    generation_rejected_rows: int
    single_value_conditional_rows: int
    closing_hypotheticals: int
    row_ok: bool


def exact_claim(
    name: str,
    output_kind: str,
    exact_product: bool,
    mixed_graph: bool,
    equal_weight: bool,
    orientation: bool,
    arithmetic_producer: bool,
    challenge_legal: bool,
    finite_intake: bool,
) -> ExactProductClaim:
    return ExactProductClaim(
        name,
        "ksy_normalized_y_siegel_formula",
        output_kind,
        exact_product,
        mixed_graph,
        equal_weight,
        orientation,
        arithmetic_producer,
        challenge_legal,
        finite_intake,
    )


def source_claim(
    name: str,
    anchor_name: str,
    output_kind: str,
    exact_product_p: bool,
    mixed_graph_selector: bool,
    period_156_context: bool,
    finite_field_identity: bool,
    divisor_or_additive: bool,
    policy_accepts_finite_identity: bool,
) -> SourceClaim:
    return SourceClaim(
        name,
        anchor_name,
        output_kind,
        exact_product_p,
        mixed_graph_selector,
        period_156_context,
        finite_field_identity,
        divisor_or_additive,
        policy_accepts_finite_identity,
    )


def row_from_exact_claim(
    name: str,
    source_url: str,
    verified_clause: str,
    source_role: str,
    priority1_output_type: str,
    claim: ExactProductClaim,
    expected_decision: str,
    first_missing_clause: str,
    recommendation: str,
    closes_priority1: bool,
) -> KsySourceSplitRow:
    decision = classify_exact_product_claim(claim)
    return KsySourceSplitRow(
        name=name,
        source_url=source_url,
        verified_clause=verified_clause,
        source_role=source_role,
        priority1_output_type=priority1_output_type,
        observed_decision=decision.decision,
        expected_decision=expected_decision,
        first_missing_clause=first_missing_clause,
        recommendation=recommendation,
        closes_priority1=closes_priority1,
        row_ok=(
            decision.decision == expected_decision
            and decision.closes_route == closes_priority1
        ),
    )


def row_from_source_claim(
    name: str,
    source_url: str,
    verified_clause: str,
    source_role: str,
    priority1_output_type: str,
    claim: SourceClaim,
    expected_decision: str,
    first_missing_clause: str,
    recommendation: str,
) -> KsySourceSplitRow:
    decision = classify_source_claim(claim)
    return KsySourceSplitRow(
        name=name,
        source_url=source_url,
        verified_clause=verified_clause,
        source_role=source_role,
        priority1_output_type=priority1_output_type,
        observed_decision=decision.decision,
        expected_decision=expected_decision,
        first_missing_clause=first_missing_clause,
        recommendation=recommendation,
        closes_priority1=False,
        row_ok=decision.decision == expected_decision and not decision.closes_route,
    )


def source_split_rows() -> tuple[KsySourceSplitRow, ...]:
    source_url = "https://arxiv.org/abs/1007.2307"
    return (
        row_from_exact_claim(
            "ksy_equation_3_4_normalized_y_formula",
            source_url,
            "Equation (3.4)",
            "normalized-y/Siegel formula language y(Q)=-g(2Q)/g(Q)^4",
            "formula-language",
            exact_claim(
                "ksy_equation_3_4_normalized_y_formula",
                "formula-language",
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            "conditional_formula_language_without_product_proof",
            "proof that the formula emits exact P over the p25 C,D,K atoms",
            "continue only if upgraded to exact K-traced product theorem",
            False,
        ),
        row_from_exact_claim(
            "ksy_theorem_5_3_ray_class_generation",
            source_url,
            "Theorem 5.3",
            "ray-class generation by torsion data",
            "field-generation",
            exact_claim(
                "ksy_theorem_5_3_ray_class_generation",
                "field-generation",
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            "reject_field_generation_not_product_identity",
            "exact divisor/additive identity for P",
            "kill as direct priority-1 closer unless reframed as exact product",
            False,
        ),
        row_from_source_claim(
            "ksy_theorem_6_2_corollary_6_4_single_y_value",
            source_url,
            "Theorem 6.2 / Corollary 6.4",
            "single normalized-y value / ray-class invariant statement",
            "single-value",
            source_claim(
                "ksy_theorem_6_2_corollary_6_4_single_y_value",
                "ksy_normalized_y_siegel_formula",
                "value",
                False,
                False,
                False,
                True,
                False,
                False,
            ),
            "conditional_missing_exact_product",
            "exact P and mixed C_3 x C_169 graph selector",
            "keep as vocabulary only; not a K-traced product theorem",
        ),
        row_from_exact_claim(
            "ksy_exact_product_distribution_hypothetical",
            source_url,
            "not supplied by inspected KSY clauses",
            "hypothetical exact normalized-y product/distribution theorem",
            "divisor-additive",
            exact_claim(
                "ksy_exact_product_distribution_hypothetical",
                "divisor-additive",
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            ),
            "closing_exact_product_identity",
            "none in priority-1 theorem lane; DANGER3 extraction remains separate",
            "accept as priority-1 theorem hit and route through theta2 certificate path",
            True,
        ),
    )


def profile_ksy_source_split() -> KsySourceSplitProfile:
    ksy_scout = profile_ksy_exact_p_scout()
    siegel_formula = profile_ksy_y_siegel_formula()
    rows = source_split_rows()
    formula_language = sum(int(row.priority1_output_type == "formula-language") for row in rows)
    generation_rejected = sum(int(row.observed_decision.startswith("reject_")) for row in rows)
    single_value_conditional = sum(
        int(row.name == "ksy_theorem_6_2_corollary_6_4_single_y_value" and row.observed_decision.startswith("conditional_"))
        for row in rows
    )
    closing = sum(int(row.closes_priority1) for row in rows)
    row_ok = (
        ksy_scout.row_ok
        and siegel_formula.row_ok
        and len(rows) == 4
        and formula_language == 1
        and generation_rejected == 1
        and single_value_conditional == 1
        and closing == 1
        and tuple(row.name for row in rows)
        == (
            "ksy_equation_3_4_normalized_y_formula",
            "ksy_theorem_5_3_ray_class_generation",
            "ksy_theorem_6_2_corollary_6_4_single_y_value",
            "ksy_exact_product_distribution_hypothetical",
        )
        and all(row.row_ok for row in rows)
        and siegel_formula.footprint_support == 300
        and siegel_formula.raw_divisor_emits == "theta2_inverse"
        and siegel_formula.raw_value_route_period == 156
    )
    return KsySourceSplitProfile(
        ksy_scout_ok=ksy_scout.row_ok,
        siegel_formula_ok=siegel_formula.row_ok,
        rows=rows,
        formula_language_rows=formula_language,
        generation_rejected_rows=generation_rejected,
        single_value_conditional_rows=single_value_conditional,
        closing_hypotheticals=closing,
        row_ok=row_ok,
    )


def print_row(row: KsySourceSplitRow) -> None:
    print(
        "  "
        f"{row.name}: clause={row.verified_clause} output={row.priority1_output_type} "
        f"decision={row.observed_decision} closes={int(row.closes_priority1)} "
        f"missing={row.first_missing_clause} recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_ksy_source_split()
    print("p25 KSY-y priority-1 KSY source-split gate")
    print(f"ksy_scout_ok={int(profile.ksy_scout_ok)}")
    print(f"siegel_formula_ok={int(profile.siegel_formula_ok)}")
    print("source_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  formula_language_rows={profile.formula_language_rows}")
    print(f"  generation_rejected_rows={profile.generation_rejected_rows}")
    print(f"  single_value_conditional_rows={profile.single_value_conditional_rows}")
    print(f"  closing_hypotheticals={profile.closing_hypotheticals}")
    print("interpretation")
    print("  ksy_equation_3_4_is_formula_language_not_product_proof=1")
    print("  ksy_theorem_5_3_generation_is_rejected_as_direct_priority1_closer=1")
    print("  ksy_theorem_6_2_corollary_6_4_single_value_is_conditional_until_exact_product=1")
    print("  exact_K_traced_normalized_y_product_theorem_would_close_priority1=1")
    print(f"ksy_y_priority1_ksy_source_split_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 KSY source-split regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
