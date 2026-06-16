#!/usr/bin/env python3
"""Challenge-legality boundary for the exact p25 KSY-y theorem target.

The KSY-y formula and period-context gates make the finite payload precise.
This gate turns that progress into a theorem-intake checklist: a claimed
literature/theory hit is useful only if it emits either

* the exact divisor/additive KSY-y product identity, or
* the exact value product plus period-156 theta2 fixedness/telescoping.

Everything weaker is deliberately routed as conditional or rejected, even when
it comes from a serious source family.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate import (
    profile_ksy_y_period_context,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    profile_ksy_y_siegel_formula,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class KsyYTheoremLegalityRow:
    name: str
    source_family: str
    theorem_output: str
    minimum_payload_fields: tuple[str, ...]
    expected_status: str
    observed_status: str
    complete_certificate_route: bool
    first_obligation_or_falsifier: str
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class KsyYTheoremLegalityProfile:
    formula_gate_ok: bool
    period_context_gate_ok: bool
    raw_route_contract_ok: bool
    recorded_falsifiers_ok: bool
    accepted_rows: tuple[KsyYTheoremLegalityRow, ...]
    conditional_rows: tuple[KsyYTheoremLegalityRow, ...]
    rejected_rows: tuple[KsyYTheoremLegalityRow, ...]
    accepted_complete_routes: int
    exact_index_contract: str
    exact_formula_contract: str
    exact_period_contract: str
    moonshot_viability: str
    first_external_question: str
    row_ok: bool


def make_row(
    name: str,
    source_family: str,
    theorem_output: str,
    minimum_payload_fields: tuple[str, ...],
    expected_status: str,
    observed_status: str,
    complete_certificate_route: bool,
    first_obligation_or_falsifier: str,
    recommendation: str,
) -> KsyYTheoremLegalityRow:
    return KsyYTheoremLegalityRow(
        name=name,
        source_family=source_family,
        theorem_output=theorem_output,
        minimum_payload_fields=minimum_payload_fields,
        expected_status=expected_status,
        observed_status=observed_status,
        complete_certificate_route=complete_certificate_route,
        first_obligation_or_falsifier=first_obligation_or_falsifier,
        recommendation=recommendation,
        row_ok=observed_status == expected_status,
    )


def profile_ksy_y_theorem_legality() -> KsyYTheoremLegalityProfile:
    formula = profile_ksy_y_siegel_formula()
    period = profile_ksy_y_period_context()

    raw_center: Coord = formula.raw_center
    raw_d: Coord = formula.raw_d_step
    raw_k: Coord = formula.raw_k_step

    raw_divisor_ok = formula.raw_divisor_route_ok and formula.raw_divisor_emits == "theta2_inverse"
    value_with_period_ok = (
        formula.raw_value_route_unique_fp_root
        and period.row_ok
        and period.formula_fixed_by_period_156
        and period.support_denominator_gcd_fp_star == 1
    )
    raw_value_without_period_is_conditional = (
        formula.raw_value_route_needs_period_context
        and period.ambient_value_branch_count_fp_star == 11
    )
    ambient_value_rejected = period.ambient_value_branch_count_fp_star == 11
    recorded_falsifiers_ok = (
        formula.generic_single_y_value_rejected
        and formula.kl_exponent_screen_ok
        and period.proper_period_divisors_fail
        and ambient_value_rejected
    )

    exact_index_fields = (
        "C=(47,28) in C_75 x C_169",
        "D=(22,3)",
        "primitive K=(57,0)",
        "A=C+jD+kK for j in {-1,0,1}, 0<=k<25",
        "orientation y(A)/y(-A)",
    )
    exact_formula_fields = (
        "y(Q)=-g(2Q)/g(Q)^4",
        "y(A)/y(-A)=g(2A) g(A)^-4 g(-2A)^-1 g(-A)^4",
        "four disjoint 75-point layers",
        "coefficient counts (-4,75),(-1,75),(1,75),(4,75)",
        "theta2-inverse footprint, not only KL congruences",
    )
    period_fields = (
        "support period exactly 156",
        "[2]^156 fixes the formula footprint",
        "all proper divisors of 156 fail",
        "gcd(4^156-1,p-1)=1",
        "telescoping or equivalent branch/root witness supplied by theorem",
    )

    accepted_rows = (
        make_row(
            "exact_ksy_y_divisor_or_additive_identity",
            "Koo-Shin-Yoon / Sprang / Siegel-unit differential",
            "raw divisor/additive identity for the exact KSY-y product",
            exact_index_fields + exact_formula_fields,
            "accepted",
            "accepted" if raw_divisor_ok else "rejected",
            raw_divisor_ok,
            "raw product routes to the theta2-inverse certificate path",
            "take as the best theorem target; route through the theta2-inverse certificate path",
        ),
        make_row(
            "exact_ksy_y_value_identity_with_period_156_context",
            "Koo-Shin-Yoon / Siegel-Robert values",
            "finite-field value identity for the exact KSY-y product with branch control",
            exact_index_fields + exact_formula_fields + period_fields,
            "accepted",
            "accepted" if value_with_period_ok else "conditional",
            value_with_period_ok,
            "period-156 context is supplied, so the F_p^* value root is unique",
            "viable only when the theorem carries the period-156 context, not as a bare value",
        ),
    )

    conditional_rows = (
        make_row(
            "exact_ksy_y_value_identity_without_period_context",
            "Koo-Shin-Yoon / Siegel-Robert values",
            "finite-field value identity for the exact product, but no branch/fixedness data",
            exact_index_fields + exact_formula_fields,
            "conditional",
            "conditional" if raw_value_without_period_is_conditional else "rejected",
            False,
            "value-level hit must include period-156 theta2 fixedness/telescoping",
            "continue only by adding period-156 theta2 fixedness or equivalent telescoping",
        ),
        make_row(
            "finite_spine_payload_without_arithmetic_source",
            "Kubert-Lang exponent matrix / local finite payload",
            "already-normalized finite verifier payload",
            (
                "exact finite theta2/theta2-inverse payload",
                "mixed C_3 x C_169 row graph preserved",
                "challenge-legal arithmetic source still attached",
            ),
            "conditional",
            "conditional" if formula.footprint_matches_anti_invariant_product else "rejected",
            False,
            "finite spine is a verifier target, not an arithmetic proof by itself",
            "use as local intake for a real source theorem, not as the theorem",
        ),
        make_row(
            "cm_lang_or_class_field_generation_without_finite_identity",
            "CM/Lang/ray-class field generation",
            "class-field generation or selected singular value statement only",
            (
                "must be reframed as a finite-field identity for the exact p25 product",
                "must avoid relying on a private or ambiguous CM shortcut",
            ),
            "conditional",
            "conditional",
            False,
            "field generation alone does not emit C/D/K/orientation payload",
            "ask whether the result can be stated as a non-CM finite-field identity",
        ),
    )

    rejected_rows = (
        make_row(
            "ambient_780_value_only",
            "Siegel-Robert value units",
            "bare value on the ambient 780-period orbit",
            ("ambient value",),
            "rejected",
            "rejected" if ambient_value_rejected else "conditional",
            False,
            "ambient 780-period value route has mu_11 ambiguity over F_p^*",
            "reject unless reduced to the support-period route",
        ),
        make_row(
            "wrong_C_D_K_geometry",
            "any source family",
            "KSY-y-looking product with wrong center, D, K, or orientation",
            ("wrong raw geometry",),
            "rejected",
            "rejected" if recorded_falsifiers_ok else "conditional",
            False,
            "wrong center, D, K, or orientation is outside the accepted raw product contract",
            "reject before doing literature/theorem work",
        ),
        make_row(
            "generic_ksy_ray_class_generation",
            "Koo-Shin-Yoon",
            "ray-class generation from y-values without exact p25 product",
            ("generic y-value or field-generation theorem",),
            "rejected",
            "rejected" if formula.generic_single_y_value_rejected else "conditional",
            False,
            "does not select the 75 atoms, orientation, theta2 footprint, or bridge certificate",
            "kill until instantiated as the exact product",
        ),
        make_row(
            "raw_kubert_lang_exponent_balance_only",
            "Kubert-Lang",
            "Siegel exponent congruence hygiene without finite intake geometry",
            ("KL exponent balance",),
            "rejected",
            "rejected" if recorded_falsifiers_ok else "conditional",
            False,
            "many wrong packets pass the same exponent congruence screen",
            "kill unless paired with exact finite payload geometry",
        ),
    )

    accepted_ok = (
        len(accepted_rows) == 2
        and all(row.complete_certificate_route for row in accepted_rows)
        and all(row.row_ok for row in accepted_rows)
    )
    conditional_ok = (
        len(conditional_rows) == 3
        and not any(row.complete_certificate_route for row in conditional_rows)
        and all(row.row_ok for row in conditional_rows)
    )
    rejected_ok = (
        len(rejected_rows) == 4
        and not any(row.complete_certificate_route for row in rejected_rows)
        and all(row.row_ok for row in rejected_rows)
    )
    row_ok = (
        formula.row_ok
        and period.row_ok
        and raw_center == (47, 28)
        and raw_d == (22, 3)
        and raw_k == (57, 0)
        and formula.source_atom_support == 75
        and formula.footprint_support == 300
        and formula.raw_divisor_emits == "theta2_inverse"
        and period.formula_support_period == 156
        and period.support_denominator_gcd_fp_star == 1
        and period.ambient_value_branch_count_fp_star == 11
        and accepted_ok
        and conditional_ok
        and rejected_ok
    )

    return KsyYTheoremLegalityProfile(
        formula_gate_ok=formula.row_ok,
        period_context_gate_ok=period.row_ok,
        raw_route_contract_ok=raw_divisor_ok and value_with_period_ok,
        recorded_falsifiers_ok=recorded_falsifiers_ok,
        accepted_rows=accepted_rows,
        conditional_rows=conditional_rows,
        rejected_rows=rejected_rows,
        accepted_complete_routes=sum(
            int(row.complete_certificate_route) for row in accepted_rows
        ),
        exact_index_contract="C=(47,28), D=(22,3), K=(57,0), j=-1,0,1, k=0..24",
        exact_formula_contract="KSY y(Q)=-g(2Q)/g(Q)^4 instantiated as the 300-term theta2-inverse footprint",
        exact_period_contract="period-156 theta2 fixedness/telescoping; gcd(4^156-1,p-1)=1",
        moonshot_viability=(
            "narrowly viable: finite payload and branch context are executable; "
            "the missing object is a challenge-legal arithmetic theorem for this exact product"
        ),
        first_external_question=(
            "Can KSY/Siegel-Robert/Sprang/Kubert-Lang be stated to produce this "
            "exact C/D/K product identity, or the value identity with period-156 "
            "context, without relying on a forbidden CM shortcut?"
        ),
        row_ok=row_ok,
    )


def print_rows(title: str, rows: tuple[KsyYTheoremLegalityRow, ...]) -> None:
    print(title)
    for row in rows:
        print(
            "  "
            f"{row.name}: expected={row.expected_status} "
            f"observed={row.observed_status} "
            f"complete={int(row.complete_certificate_route)} "
            f"falsifier={row.first_obligation_or_falsifier}"
        )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y theorem-legality gate")
    profile = profile_ksy_y_theorem_legality()
    print(f"ksy_y_theorem_legality_profile={profile}")
    print("exact_contracts")
    print(f"  index={profile.exact_index_contract}")
    print(f"  formula={profile.exact_formula_contract}")
    print(f"  period={profile.exact_period_contract}")
    print_rows("accepted_theorem_outputs", profile.accepted_rows)
    print_rows("conditional_theorem_outputs", profile.conditional_rows)
    print_rows("rejected_theorem_outputs", profile.rejected_rows)
    print("interpretation")
    print("  exact_divisor_or_additive_KSY_y_product_is_the_best_theorem_target=1")
    print("  exact_value_product_is_viable_only_with_period_156_context=1")
    print("  finite_spine_alone_is_not_an_arithmetic_theorem=1")
    print("  generic_KSY_or_CM_field_generation_is_not_a_certificate_payload=1")
    print(f"  accepted_complete_routes={profile.accepted_complete_routes}")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
