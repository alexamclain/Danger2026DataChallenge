#!/usr/bin/env python3
"""Primary-source clause audit for the exact p25 KSY-y closure template.

The closure-theorem template says what would close the route.  This gate checks
the current primary-source families against those clauses.  It is intentionally
strict: a source family remains live only as an upgrade path unless it already
emits the exact p25 product identity or the value identity with period-156
context.

This is a source-clause audit, not a literature proof.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate import (
    profile_ksy_y_closure_theorem_template,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    profile_ksy_y_siegel_formula,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate import (
    profile_ksy_y_period_context,
)


@dataclass(frozen=True)
class SourceClauseAuditRow:
    name: str
    primary_source_url: str
    source_fact: str
    supplies_formula_language: bool
    supplies_exact_cdk_product: bool
    supplies_mixed_graph_selector: bool
    supplies_period_156_context: bool
    supplies_challenge_legal_finite_identity: bool
    status: str
    first_missing_clause: str
    upgrade_question: str
    row_ok: bool


@dataclass(frozen=True)
class SourceClauseAuditProfile:
    closure_template_ok: bool
    formula_gate_ok: bool
    period_gate_ok: bool
    audited_rows: tuple[SourceClauseAuditRow, ...]
    closing_source_rows: int
    conditional_source_rows: int
    rejected_source_rows: int
    exact_product_still_open: bool
    period_context_still_open_on_source_side: bool
    next_best_packet: tuple[str, ...]
    row_ok: bool


def audit_row(
    name: str,
    primary_source_url: str,
    source_fact: str,
    supplies_formula_language: bool,
    supplies_exact_cdk_product: bool,
    supplies_mixed_graph_selector: bool,
    supplies_period_156_context: bool,
    supplies_challenge_legal_finite_identity: bool,
    status: str,
    first_missing_clause: str,
    upgrade_question: str,
) -> SourceClauseAuditRow:
    return SourceClauseAuditRow(
        name=name,
        primary_source_url=primary_source_url,
        source_fact=source_fact,
        supplies_formula_language=supplies_formula_language,
        supplies_exact_cdk_product=supplies_exact_cdk_product,
        supplies_mixed_graph_selector=supplies_mixed_graph_selector,
        supplies_period_156_context=supplies_period_156_context,
        supplies_challenge_legal_finite_identity=supplies_challenge_legal_finite_identity,
        status=status,
        first_missing_clause=first_missing_clause,
        upgrade_question=upgrade_question,
        row_ok=status in ("conditional", "rejected"),
    )


def profile_primary_source_clause_audit() -> SourceClauseAuditProfile:
    closure = profile_ksy_y_closure_theorem_template()
    formula = profile_ksy_y_siegel_formula()
    period = profile_ksy_y_period_context()

    rows = (
        audit_row(
            "koo_shin_yoon_normalized_y",
            "https://arxiv.org/abs/1007.2307",
            (
                "KSY supplies the normalized-y/Siegel-function language and "
                "ray-class-field generation context; the local gate instantiates "
                "y(Q)=-g(2Q)/g(Q)^4 as the exact four-layer p25 footprint."
            ),
            supplies_formula_language=formula.row_ok,
            supplies_exact_cdk_product=False,
            supplies_mixed_graph_selector=False,
            supplies_period_156_context=False,
            supplies_challenge_legal_finite_identity=False,
            status="conditional",
            first_missing_clause="exact C/D/K product identity for P",
            upgrade_question=(
                "Can the normalized-y theorem be specialized to prove the exact "
                "P product identity, rather than only broad ray-class generation?"
            ),
        ),
        audit_row(
            "siegel_robert_value_units",
            "https://eudml.org/doc/162977",
            (
                "Siegel-Robert/Siegel-unit value language is compatible with a "
                "value route, but a bare value route needs branch/root control."
            ),
            supplies_formula_language=True,
            supplies_exact_cdk_product=False,
            supplies_mixed_graph_selector=False,
            supplies_period_156_context=False,
            supplies_challenge_legal_finite_identity=False,
            status="conditional",
            first_missing_clause="period-156 branch/root/telescoping data",
            upgrade_question=(
                "Can a value theorem include support-period 156 fixedness or an "
                "equivalent telescoping witness so gcd(4^156-1,p-1)=1 applies?"
            ),
        ),
        audit_row(
            "sprang_kronecker_d_variant",
            "https://arxiv.org/abs/1802.04996",
            (
                "Sprang/Kronecker supplies D-variant differential/additive "
                "technology, which is the right output type if it emits the "
                "exact anti-invariant product."
            ),
            supplies_formula_language=True,
            supplies_exact_cdk_product=False,
            supplies_mixed_graph_selector=False,
            supplies_period_156_context=False,
            supplies_challenge_legal_finite_identity=False,
            status="conditional",
            first_missing_clause="D=2 differential/additive identity for exact P",
            upgrade_question=(
                "Can the D-variant differential identity be instantiated at "
                "D=2 to emit the exact p25 anti-invariant product?"
            ),
        ),
        audit_row(
            "kubert_lang_siegel_exponent_matrix",
            "https://eudml.org/doc/162977",
            (
                "Kubert-Lang supplies the Siegel-function/exponent-matrix "
                "language; local p25 screens show exponent hygiene is necessary "
                "but saturated by wrong packets."
            ),
            supplies_formula_language=True,
            supplies_exact_cdk_product=False,
            supplies_mixed_graph_selector=False,
            supplies_period_156_context=False,
            supplies_challenge_legal_finite_identity=False,
            status="conditional",
            first_missing_clause="mixed C_75 x C_169 graph selector",
            upgrade_question=(
                "Can the exponent matrix be tied to the exact mixed source graph "
                "and finite intake, rather than only KL congruence hygiene?"
            ),
        ),
        audit_row(
            "ordinary_field_generation_or_ambient_values",
            "https://arxiv.org/abs/1007.2307",
            (
                "Generic class-field generation and ambient value data are too "
                "broad for the DANGER3 certificate route."
            ),
            supplies_formula_language=False,
            supplies_exact_cdk_product=False,
            supplies_mixed_graph_selector=False,
            supplies_period_156_context=False,
            supplies_challenge_legal_finite_identity=False,
            status="rejected",
            first_missing_clause="not an exact finite-field identity for P",
            upgrade_question=(
                "Discard unless reframed as one of the two closure-template "
                "theorem shapes."
            ),
        ),
    )

    closing_source_rows = sum(
        int(
            row.supplies_exact_cdk_product
            and row.supplies_challenge_legal_finite_identity
            and (
                row.supplies_period_156_context
                or row.status == "closing_divisor_or_additive"
            )
        )
        for row in rows
    )
    conditional_source_rows = sum(int(row.status == "conditional") for row in rows)
    rejected_source_rows = sum(int(row.status == "rejected") for row in rows)
    exact_product_still_open = not any(row.supplies_exact_cdk_product for row in rows)
    period_context_still_open = not any(
        row.supplies_period_156_context and row.supplies_challenge_legal_finite_identity
        for row in rows
    )

    next_packet = (
        "Ask KSY for exact P, not generic ray-class generation.",
        "Ask Siegel-Robert for period-156 branch/root/telescoping in the value theorem.",
        "Ask Sprang/Kronecker for D=2 differential/additive output of exact P.",
        "Ask Kubert-Lang for mixed C_75 x C_169 graph selection, not exponent hygiene alone.",
        "Ask DANGER3 policy whether a finite-field identity for P avoids the no-CM concern.",
    )

    row_ok = (
        closure.row_ok
        and formula.row_ok
        and period.row_ok
        and len(rows) == 5
        and closing_source_rows == 0
        and conditional_source_rows == 4
        and rejected_source_rows == 1
        and exact_product_still_open
        and period_context_still_open
        and all(row.row_ok for row in rows)
        and formula.footprint_support == 300
        and period.formula_support_period == 156
        and period.support_denominator_gcd_fp_star == 1
    )
    return SourceClauseAuditProfile(
        closure_template_ok=closure.row_ok,
        formula_gate_ok=formula.row_ok,
        period_gate_ok=period.row_ok,
        audited_rows=rows,
        closing_source_rows=closing_source_rows,
        conditional_source_rows=conditional_source_rows,
        rejected_source_rows=rejected_source_rows,
        exact_product_still_open=exact_product_still_open,
        period_context_still_open_on_source_side=period_context_still_open,
        next_best_packet=next_packet,
        row_ok=row_ok,
    )


def print_row(row: SourceClauseAuditRow) -> None:
    print(
        "  "
        f"{row.name}: status={row.status} "
        f"formula={int(row.supplies_formula_language)} "
        f"exact_product={int(row.supplies_exact_cdk_product)} "
        f"graph={int(row.supplies_mixed_graph_selector)} "
        f"period156={int(row.supplies_period_156_context)} "
        f"finite_identity={int(row.supplies_challenge_legal_finite_identity)} "
        f"missing={row.first_missing_clause}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y primary-source clause audit gate")
    profile = profile_primary_source_clause_audit()
    print(f"primary_source_clause_audit_profile={profile}")
    print("source_rows")
    for row in profile.audited_rows:
        print_row(row)
    print("source_row_counts")
    print(f"  closing_source_rows={profile.closing_source_rows}")
    print(f"  conditional_source_rows={profile.conditional_source_rows}")
    print(f"  rejected_source_rows={profile.rejected_source_rows}")
    print("next_best_packet")
    for item in profile.next_best_packet:
        print(f"  - {item}")
    print("interpretation")
    print("  no_primary_source_family_closes_the_route_as_currently_stated=1")
    print("  KSY_Sprang_Kubert_Lang_remain_live_only_as_exact_product_upgrades=1")
    print("  Siegel_Robert_value_route_remains_live_only_with_period_156_context=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
