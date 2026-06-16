#!/usr/bin/env python3
"""Priority-1 exact divisor lane gate for the p25 KSY-y moonshot.

The post-scout reduction says to chase exact Sprang/KSY theta2-or-P
divisor/additive data first.  This gate makes that next checkpoint executable:
it distinguishes a real theorem hit from KSY formula language, Sprang D=2
machinery, compact finite payloads, and familiar shortcuts that do not yet
produce the exact anti-invariant normalized-y product.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_ksy_exact_p_primary_source_scout_gate import profile_ksy_exact_p_scout
from p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate import (
    profile_sprang_kronecker_d2_scout,
)
from p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate import (
    profile_d2_theorem_obligation,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate import (
    profile_anti_invariant_producer_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product_claim,
    profile_exact_product_intake,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate import (
    profile_source_parameter_hygiene,
)
from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    profile_normalized_y_product_source_law,
)
from p25_laneB_robert_ksy_theta2_theorem_interface_gate import profile_theorem_interface


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class Priority1DivisorLaneRow:
    name: str
    source_family: str
    row_class: str
    exact_product_claim: ExactProductClaim | None
    expected_decision: str
    observed_decision: str
    finite_status: str
    first_missing_clause: str
    local_probe: str
    recommendation: str
    closes_if_supplied_by_source: bool
    row_ok: bool


@dataclass(frozen=True)
class Priority1ExactDivisorLaneProfile:
    target_product: str
    finite_source_law_ok: bool
    theorem_interface_ok: bool
    d2_obligation_ok: bool
    anti_invariant_contract_ok: bool
    exact_product_intake_ok: bool
    ksy_scout_ok: bool
    sprang_scout_ok: bool
    source_parameter_hygiene_ok: bool
    rows: tuple[Priority1DivisorLaneRow, ...]
    direct_source_closing_rows: int
    theorem_hit_hypotheticals: int
    conditional_rows: int
    rejected_rows: int
    finite_only_rows: int
    row_ok: bool


def exact_claim(
    name: str,
    anchor: str,
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
        anchor,
        output_kind,
        exact_product,
        mixed_graph,
        equal_weight,
        orientation,
        arithmetic_producer,
        challenge_legal,
        finite_intake,
    )


def row_from_claim(
    name: str,
    source_family: str,
    row_class: str,
    claim: ExactProductClaim,
    expected_decision: str,
    finite_status: str,
    first_missing_clause: str,
    local_probe: str,
    recommendation: str,
    closes_if_supplied_by_source: bool,
) -> Priority1DivisorLaneRow:
    decision = classify_exact_product_claim(claim)
    return Priority1DivisorLaneRow(
        name=name,
        source_family=source_family,
        row_class=row_class,
        exact_product_claim=claim,
        expected_decision=expected_decision,
        observed_decision=decision.decision,
        finite_status=finite_status,
        first_missing_clause=first_missing_clause,
        local_probe=local_probe,
        recommendation=recommendation,
        closes_if_supplied_by_source=closes_if_supplied_by_source,
        row_ok=(
            decision.decision == expected_decision
            and decision.closes_route == closes_if_supplied_by_source
        ),
    )


def manual_row(
    name: str,
    source_family: str,
    row_class: str,
    observed_decision: str,
    expected_decision: str,
    finite_status: str,
    first_missing_clause: str,
    local_probe: str,
    recommendation: str,
) -> Priority1DivisorLaneRow:
    return Priority1DivisorLaneRow(
        name=name,
        source_family=source_family,
        row_class=row_class,
        exact_product_claim=None,
        expected_decision=expected_decision,
        observed_decision=observed_decision,
        finite_status=finite_status,
        first_missing_clause=first_missing_clause,
        local_probe=local_probe,
        recommendation=recommendation,
        closes_if_supplied_by_source=False,
        row_ok=observed_decision == expected_decision,
    )


def priority_rows() -> tuple[Priority1DivisorLaneRow, ...]:
    return (
        row_from_claim(
            "sprang_d2_exact_additive_identity_hit",
            "Sprang/Kronecker D=2",
            "theorem_hit_hypothetical",
            exact_claim(
                "sprang_d2_exact_additive_identity_hit",
                "sprang_prop_5_4_kato_siegel_dlog",
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
            "finite landing pad already accepts exact theta2/theta2^-1 data",
            "source theorem specializing even-D Kronecker/differential machinery to exact P",
            "exact-product intake candidate with Sprang anchor and all exact flags",
            "continue_first",
            True,
        ),
        row_from_claim(
            "ksy_normalized_y_product_distribution_hit",
            "Koo-Shin-Yoon normalized-y",
            "theorem_hit_hypothetical",
            exact_claim(
                "ksy_normalized_y_product_distribution_hit",
                "ksy_normalized_y_siegel_formula",
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
            "normalized-y product source law emits theta2^-1/theta2 in finite harness",
            "arithmetic distribution/product theorem for the full K-traced anti-invariant product",
            "exact-product intake candidate with KSY anchor and all exact flags",
            "continue_first",
            True,
        ),
        row_from_claim(
            "compact_ksy_center_half_orientation_payload",
            "finite KSY payload",
            "finite_only",
            exact_claim(
                "compact_ksy_center_half_orientation_payload",
                "ksy_normalized_y_siegel_formula",
                "finite-verifier",
                True,
                True,
                True,
                True,
                False,
                True,
                True,
            ),
            "conditional_verifier_without_arithmetic_producer",
            "compact center/half/orientation data is accepted by finite verifier path",
            "challenge-legal arithmetic theorem producing this compact payload",
            "D=2 theorem-obligation gate accepted compact KSY payload row",
            "keep_as_landing_pad_not_source_closure",
            False,
        ),
        row_from_claim(
            "ksy_equation_3_4_formula_language_only",
            "Koo-Shin-Yoon normalized-y",
            "conditional_source",
            exact_claim(
                "ksy_equation_3_4_formula_language_only",
                "ksy_normalized_y_siegel_formula",
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
            "source formula y(Q)=-g(2Q)/g(Q)^4 remains useful vocabulary",
            "proof that the formula emits exact P for C,D,K and orientation",
            "KSY exact-P scout / source-claim intake",
            "continue_only_if_upgraded_to_exact_product",
            False,
        ),
        row_from_claim(
            "sprang_distribution_relation_without_specialization",
            "Sprang/Kronecker D=2",
            "conditional_source",
            exact_claim(
                "sprang_distribution_relation_without_specialization",
                "sprang_prop_5_4_kato_siegel_dlog",
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
            "even-D Kronecker/differential machinery remains live",
            "explicit specialization to exact P or exact theta2/theta2^-1 divisor data",
            "Sprang primary-source scout / D=2 theorem-obligation gate",
            "continue_only_if_upgraded_to_exact_product",
            False,
        ),
        row_from_claim(
            "ksy_single_y_or_ray_class_generation",
            "Koo-Shin-Yoon generation",
            "rejected_shortcut",
            exact_claim(
                "ksy_single_y_or_ray_class_generation",
                "ksy_normalized_y_siegel_formula",
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
            "single-y or ray-class generation can be true but non-closing",
            "exact divisor/additive identity for the 75-atom product",
            "exact-product intake field-generation control",
            "kill_as_direct_closer",
            False,
        ),
        row_from_claim(
            "nonuniform_or_partial_product",
            "finite product controls",
            "rejected_shortcut",
            exact_claim(
                "nonuniform_or_partial_product",
                "ksy_normalized_y_siegel_formula",
                "divisor-additive",
                True,
                True,
                False,
                True,
                True,
                True,
                True,
            ),
            "reject_nonuniform_atom_weights",
            "D-slice and atom-weight rigidity force equal weights on all 75 atoms",
            "equal weight on every K-traced atom",
            "exact-product intake nonuniform control",
            "kill_unless_equal_weight_exact_product",
            False,
        ),
    )


def profile_priority1_exact_divisor_lane() -> Priority1ExactDivisorLaneProfile:
    source_law = profile_normalized_y_product_source_law()
    theorem_interface = profile_theorem_interface()
    d2_obligation = profile_d2_theorem_obligation()
    anti_invariant = profile_anti_invariant_producer_contract()
    exact_intake = profile_exact_product_intake()
    ksy_scout = profile_ksy_exact_p_scout()
    sprang_scout = profile_sprang_kronecker_d2_scout()
    parameter_hygiene = profile_source_parameter_hygiene()
    rows = priority_rows()

    ordinary_kato = next(
        row
        for row in parameter_hygiene.rows
        if row.name == "ordinary_kato_theta_parameter_2"
    )
    rows = rows + (
        manual_row(
            "ordinary_kato_theta_d2_import",
            "ordinary Kato-Siegel theta_D",
            "rejected_shortcut",
            ordinary_kato.decision,
            "reject_ordinary_kato_theta_2_prime_to_6_violation",
            "ordinary theta_D at D=2 is not the Sprang/Kronecker even-D route",
            "ordinary Dtheta source clause allowing D=2",
            "source-parameter hygiene gate",
            "kill_as_direct_D2_proof",
        ),
        manual_row(
            "missing_or_collapsed_k_trace_control",
            "finite product controls",
            "rejected_shortcut",
            (
                "rejected_missing_or_collapsed_k_trace"
                if source_law.missing_k_rejected and source_law.collapsed_k_rejected
                else "not_rejected"
            ),
            "rejected_missing_or_collapsed_k_trace",
            "normalized-y product controls fail without the honest 25-point K trace",
            "full primitive K trace",
            "normalized-y product source-law controls",
            "kill_missing_or_collapsed_k",
        ),
        manual_row(
            "wrong_d_or_t_control",
            "finite product controls",
            "rejected_shortcut",
            (
                "rejected_wrong_d_or_t"
                if source_law.truncated_d_rejected
                and source_law.wrong_d_rejected
                and source_law.wrong_t_rejected
                else "not_rejected"
            ),
            "rejected_wrong_d_or_t",
            "the finite landing pad rejects truncated D, wrong D, and wrong T",
            "exact short D segment and reflection T edge",
            "normalized-y product source-law controls",
            "kill_wrong_geometry",
        ),
    )

    direct_source_closing = ksy_scout.direct_closing_rows + sprang_scout.direct_closing_rows
    theorem_hit_hypotheticals = sum(
        int(row.row_class == "theorem_hit_hypothetical" and row.closes_if_supplied_by_source)
        for row in rows
    )
    conditional = sum(int(row.row_class == "conditional_source") for row in rows)
    rejected = sum(int(row.row_class == "rejected_shortcut") for row in rows)
    finite_only = sum(int(row.row_class == "finite_only") for row in rows)

    all_inputs_ok = (
        source_law.row_ok
        and theorem_interface.row_ok
        and d2_obligation.row_ok
        and anti_invariant.row_ok
        and exact_intake.row_ok
        and ksy_scout.row_ok
        and sprang_scout.row_ok
        and parameter_hygiene.row_ok
    )
    expected_names = (
        "sprang_d2_exact_additive_identity_hit",
        "ksy_normalized_y_product_distribution_hit",
        "compact_ksy_center_half_orientation_payload",
        "ksy_equation_3_4_formula_language_only",
        "sprang_distribution_relation_without_specialization",
        "ksy_single_y_or_ray_class_generation",
        "nonuniform_or_partial_product",
        "ordinary_kato_theta_d2_import",
        "missing_or_collapsed_k_trace_control",
        "wrong_d_or_t_control",
    )
    row_ok = (
        all_inputs_ok
        and tuple(row.name for row in rows) == expected_names
        and direct_source_closing == 0
        and theorem_hit_hypotheticals == 2
        and conditional == 2
        and rejected == 5
        and finite_only == 1
        and all(row.row_ok for row in rows)
        and source_law.target_support == 300
        and anti_invariant.finite_contract_accepts_anti_invariant_target
        and anti_invariant.finite_contract_rejects_shortcuts
    )

    return Priority1ExactDivisorLaneProfile(
        target_product=TARGET_PRODUCT,
        finite_source_law_ok=source_law.row_ok,
        theorem_interface_ok=theorem_interface.row_ok,
        d2_obligation_ok=d2_obligation.row_ok,
        anti_invariant_contract_ok=anti_invariant.row_ok,
        exact_product_intake_ok=exact_intake.row_ok,
        ksy_scout_ok=ksy_scout.row_ok,
        sprang_scout_ok=sprang_scout.row_ok,
        source_parameter_hygiene_ok=parameter_hygiene.row_ok,
        rows=rows,
        direct_source_closing_rows=direct_source_closing,
        theorem_hit_hypotheticals=theorem_hit_hypotheticals,
        conditional_rows=conditional,
        rejected_rows=rejected,
        finite_only_rows=finite_only,
        row_ok=row_ok,
    )


def print_row(row: Priority1DivisorLaneRow) -> None:
    print(
        "  "
        f"{row.name}: class={row.row_class} source={row.source_family} "
        f"decision={row.observed_decision} expected={row.expected_decision} "
        f"closes_if_source={int(row.closes_if_supplied_by_source)} "
        f"status={row.finite_status} missing={row.first_missing_clause} "
        f"recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_priority1_exact_divisor_lane()
    print("p25 KSY-y priority-1 exact divisor lane gate")
    print(f"target_product={profile.target_product}")
    print("inputs")
    print(f"  finite_source_law_ok={int(profile.finite_source_law_ok)}")
    print(f"  theorem_interface_ok={int(profile.theorem_interface_ok)}")
    print(f"  d2_obligation_ok={int(profile.d2_obligation_ok)}")
    print(f"  anti_invariant_contract_ok={int(profile.anti_invariant_contract_ok)}")
    print(f"  exact_product_intake_ok={int(profile.exact_product_intake_ok)}")
    print(f"  ksy_scout_ok={int(profile.ksy_scout_ok)}")
    print(f"  sprang_scout_ok={int(profile.sprang_scout_ok)}")
    print(f"  source_parameter_hygiene_ok={int(profile.source_parameter_hygiene_ok)}")
    print("rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  direct_source_closing_rows={profile.direct_source_closing_rows}")
    print(f"  theorem_hit_hypotheticals={profile.theorem_hit_hypotheticals}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  finite_only_rows={profile.finite_only_rows}")
    print("interpretation")
    print("  priority1_conversion_clause_is_exact_P_or_theta2_divisor_identity=1")
    print("  ksy_formula_language_and_sprang_distribution_are_conditional_until_specialized=1")
    print("  compact_finite_payload_is_a_landing_pad_not_source_closure=1")
    print("  ordinary_kato_D2_missing_K_wrong_D_wrong_T_and_nonuniform_weights_are_killed=1")
    print(f"ksy_y_priority1_exact_divisor_lane_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 exact divisor lane regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
