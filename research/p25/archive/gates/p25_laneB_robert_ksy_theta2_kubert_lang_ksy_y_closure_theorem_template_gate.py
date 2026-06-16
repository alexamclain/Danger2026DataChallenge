#!/usr/bin/env python3
"""Closure-theorem template for the exact p25 KSY-y moonshot target.

The theorem-legality gate says which output types are acceptable.  This gate
turns that into a compact theorem template: the exact product statement, the
minimum clauses that would close the moonshot route, and the first falsifier
for source claims that look nearby but do not close it.

This is an intake artifact, not a proof of the theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate import (
    profile_ksy_y_period_context,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    profile_ksy_y_siegel_formula,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_gate import (
    profile_ksy_y_theorem_legality,
)


@dataclass(frozen=True)
class ClosureTheoremClause:
    name: str
    theorem_shape: str
    minimum_clauses: tuple[str, ...]
    local_evidence: tuple[str, ...]
    status: str
    closes_certificate_route: bool
    first_falsifier_if_missing: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class ClosureTheoremTemplateProfile:
    formula_gate_ok: bool
    period_gate_ok: bool
    legality_gate_ok: bool
    formal_product: str
    finite_payload_budget: int
    compact_telescoping_budget: int
    factor_period_budget: int
    closing_clauses: tuple[ClosureTheoremClause, ...]
    nonclosing_clauses: tuple[ClosureTheoremClause, ...]
    source_question_packet: tuple[str, ...]
    moonshot_position: str
    row_ok: bool


def clause(
    name: str,
    theorem_shape: str,
    minimum_clauses: tuple[str, ...],
    local_evidence: tuple[str, ...],
    status: str,
    closes_certificate_route: bool,
    first_falsifier_if_missing: str,
    next_action: str,
) -> ClosureTheoremClause:
    return ClosureTheoremClause(
        name=name,
        theorem_shape=theorem_shape,
        minimum_clauses=minimum_clauses,
        local_evidence=local_evidence,
        status=status,
        closes_certificate_route=closes_certificate_route,
        first_falsifier_if_missing=first_falsifier_if_missing,
        next_action=next_action,
        row_ok=status in ("closing", "conditional", "rejected"),
    )


def profile_ksy_y_closure_theorem_template() -> ClosureTheoremTemplateProfile:
    formula = profile_ksy_y_siegel_formula()
    period = profile_ksy_y_period_context()
    legality = profile_ksy_y_theorem_legality()

    formal_product = (
        "P = prod_{j=-1..1} prod_{k=0..24} "
        "y(C+jD+kK) / y(-C-jD-kK), "
        "C=(47,28), D=(22,3), K=(57,0), "
        "y(Q)=-g(2Q)/g(Q)^4"
    )
    exact_index_clauses = (
        "bind C=(47,28), D=(22,3), primitive K=(57,0)",
        "use A=C+jD+kK with j=-1,0,1 and 0<=k<25",
        "preserve orientation y(A)/y(-A)",
        "preserve the mixed C_75 x C_169 source graph, not only C_169 projection",
    )
    exact_formula_clauses = (
        "expand y(Q)=-g(2Q)/g(Q)^4",
        "emit g(2A) g(A)^-4 g(-2A)^-1 g(-A)^4",
        "recover the 300-term theta2-inverse footprint",
        "do not stop at Kubert-Lang exponent congruence hygiene",
    )
    value_clauses = (
        "supply support period 156, not ambient period 780",
        "prove [2]^156 fixedness or equivalent telescoping",
        "prove proper period shortcuts fail or otherwise select the same support object",
        "use gcd(4^156-1,p-1)=1 to select the F_p^* root",
    )

    closing = (
        clause(
            "divisor_or_additive_product_identity",
            "prove the exact KSY-y divisor/additive product identity for P",
            exact_index_clauses + exact_formula_clauses,
            (
                f"source atoms={formula.source_atom_support}",
                f"formula footprint support={formula.footprint_support}",
                f"coefficient counts={formula.footprint_coefficient_counts}",
                "raw divisor route emits theta2_inverse",
                "theta2-inverse certificate path already passes",
            ),
            "closing",
            True,
            "wrong C/D/K/orientation or value-only output leaves the certificate route",
            "ask source/lit work for this exact product identity first",
        ),
        clause(
            "value_identity_with_period_156_context",
            "prove the exact finite-field value identity for P with period-156 context",
            exact_index_clauses + exact_formula_clauses + value_clauses,
            (
                f"support period={period.formula_support_period}",
                f"gcd(4^156-1,p-1)={period.support_denominator_gcd_fp_star}",
                f"ambient value branches={period.ambient_value_branch_count_fp_star}",
                f"telescoping budget={period.compact_telescoping_budget}",
                f"factor-period budget={period.factor_period_budget}",
            ),
            "closing",
            True,
            "bare values fall back to the ambient mu_11 branch ambiguity",
            "ask source/lit work to supply branch/root data as part of the theorem",
        ),
    )
    nonclosing = (
        clause(
            "exact_value_without_period_context",
            "prove only the exact finite-field value of P",
            exact_index_clauses + exact_formula_clauses,
            (
                "exact product is necessary",
                "period/root context is still absent",
                "ambient route has 11 branches",
            ),
            "conditional",
            False,
            "value-level hit must include period-156 theta2 fixedness/telescoping",
            "continue only by upgrading it to the period-156 value theorem",
        ),
        clause(
            "finite_spine_without_arithmetic_source",
            "emit theta2/theta2-inverse finite payload or compact verifier skeleton",
            (
                "exact finite payload",
                "mixed row graph preserved",
                "arithmetic producer attached separately",
            ),
            (
                "finite payloads are verifier targets",
                "local intake accepts them",
                "they are not theorem-side arithmetic by themselves",
            ),
            "conditional",
            False,
            "finite spine alone is not an arithmetic theorem",
            "use only as a handoff from a real source theorem",
        ),
        clause(
            "generic_class_field_or_ksy_generation",
            "prove broad ray-class generation from y-values or CM/Lang units",
            (
                "must instantiate exact C/D/K atoms",
                "must emit finite-field identity or divisor/additive identity",
                "must avoid relying on a forbidden CM shortcut",
            ),
            (
                "generic KSY generation does not select the 75 atoms",
                "field generation does not pick orientation",
                "class-field output does not select the bridge certificate",
            ),
            "conditional",
            False,
            "field generation alone does not emit C/D/K/orientation payload",
            "ask whether the result can be reframed as a non-CM finite-field identity",
        ),
        clause(
            "ambient_or_exponent_hygiene_only",
            "use ambient value data or Kubert-Lang exponent balance alone",
            (
                "ambient 780-period values",
                "KL exponent sums",
            ),
            (
                "ambient value route has mu_11 ambiguity",
                "wrong packets pass KL exponent balance",
            ),
            "rejected",
            False,
            "does not identify the accepted product or value branch",
            "discard unless paired with one of the two closing theorem shapes",
        ),
    )

    source_questions = (
        "KSY: can the normalized-y formula be used to prove the exact P identity, not just generate a ray class field?",
        "Siegel-Robert: can the value theorem include the period-156 branch/root/telescoping data?",
        "Sprang/Kronecker: can the D=2 differential/additive identity emit this exact anti-invariant product?",
        "Kubert-Lang: can the exponent matrix be tied to the mixed C_75 x C_169 graph rather than only congruence hygiene?",
        "Challenge policy: if phrased as a finite-field identity for P, is this considered non-CM enough for DANGER3?",
    )

    row_ok = (
        formula.row_ok
        and period.row_ok
        and legality.row_ok
        and formula.source_atom_support == 75
        and formula.footprint_support == 300
        and period.compact_telescoping_budget == 975
        and period.factor_period_budget == 31
        and len(closing) == 2
        and len(nonclosing) == 4
        and all(row.closes_certificate_route for row in closing)
        and not any(row.closes_certificate_route for row in nonclosing)
        and all(row.row_ok for row in closing + nonclosing)
    )
    return ClosureTheoremTemplateProfile(
        formula_gate_ok=formula.row_ok,
        period_gate_ok=period.row_ok,
        legality_gate_ok=legality.row_ok,
        formal_product=formal_product,
        finite_payload_budget=formula.footprint_support,
        compact_telescoping_budget=period.compact_telescoping_budget,
        factor_period_budget=period.factor_period_budget,
        closing_clauses=closing,
        nonclosing_clauses=nonclosing,
        source_question_packet=source_questions,
        moonshot_position=(
            "the finite side is sub-sqrt and executable; the open item is a "
            "challenge-legal source theorem matching one of the two closing shapes"
        ),
        row_ok=row_ok,
    )


def print_clause(prefix: str, row: ClosureTheoremClause) -> None:
    print(
        "  "
        f"{prefix}: status={row.status} "
        f"closes={int(row.closes_certificate_route)} "
        f"falsifier={row.first_falsifier_if_missing}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y closure-theorem template gate")
    profile = profile_ksy_y_closure_theorem_template()
    print(f"ksy_y_closure_theorem_template_profile={profile}")
    print("formal_product")
    print(f"  {profile.formal_product}")
    print("budgets")
    print(f"  finite_payload_budget={profile.finite_payload_budget}")
    print(f"  compact_telescoping_budget={profile.compact_telescoping_budget}")
    print(f"  factor_period_budget={profile.factor_period_budget}")
    print("closing_theorem_shapes")
    for row in profile.closing_clauses:
        print_clause(row.name, row)
    print("nonclosing_theorem_shapes")
    for row in profile.nonclosing_clauses:
        print_clause(row.name, row)
    print("source_question_packet")
    for question in profile.source_question_packet:
        print(f"  - {question}")
    print("interpretation")
    print("  exact_divisor_or_additive_identity_would_close_route=1")
    print("  exact_value_identity_needs_period_156_context_to_close_route=1")
    print("  finite_payloads_and_field_generation_are_not_closure_theorems=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
