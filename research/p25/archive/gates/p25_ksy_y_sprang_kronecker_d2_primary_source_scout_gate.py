#!/usr/bin/env python3
"""Sprang/Kronecker D=2 primary-source scout for the p25 KSY-y moonshot.

Sprang is the live source family for an even-D differential/additive producer,
but the local p25 target is much sharper than "D=2 is allowed".  This gate
separates three facts:

* the Kronecker-section construction keeps an even-D differential object live;
* the ordinary Kato-Siegel theta_D theorem still cannot be imported at D=2;
* a p25 win needs exact P, exact theta2/theta2^-1, or compact KSY data with an
  arithmetic producer, not only a general distribution or dlog framework.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate import (
    profile_d2_theorem_obligation,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate import (
    profile_source_parameter_hygiene,
)


SOURCE = "Sprang, Eisenstein-Kronecker series via the Poincare bundle"


@dataclass(frozen=True)
class SprangObservation:
    name: str
    source_clause: str
    source_handle: str
    parameter_row_name: str | None
    product_claim: ExactProductClaim | None
    expected_parameter_decision: str | None
    expected_product_decision: str | None
    matched_clause: str
    first_missing_clause: str


@dataclass(frozen=True)
class SprangScoutProfile:
    source: str
    observations: tuple[SprangObservation, ...]
    d2_obligation_ok: bool
    even_d_live_rows: int
    direct_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    hypothetical_closing_rows: int
    row_ok: bool


def observations() -> tuple[SprangObservation, ...]:
    return (
        SprangObservation(
            name="sprang_even_d_kronecker_section",
            source_clause="introduction / Section 5 Kronecker-section D-variant",
            source_handle="arXiv:1801.05677, intro lines on Kato-Siegel logarithmic derivatives",
            parameter_row_name="sprang_kronecker_even_D_variant",
            product_claim=ExactProductClaim(
                "sprang_even_d_kronecker_section",
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
            expected_parameter_decision="conditional_needs_even_D_kronecker_clause",
            expected_product_decision="conditional_formula_language_without_product_proof",
            matched_clause="even-D Kronecker/differential source family remains live",
            first_missing_clause="explicit even-D identity emitting exact P or exact theta2 data",
        ),
        SprangObservation(
            name="sprang_corollary_5_7_omega_d",
            source_clause="Corollary 5.7 omega_D construction",
            source_handle="arXiv:1801.05677, Corollary 5.7",
            parameter_row_name="sprang_kronecker_even_D_variant",
            product_claim=ExactProductClaim(
                "sprang_corollary_5_7_omega_d",
                "sprang_prop_5_4_kato_siegel_dlog",
                "divisor-additive",
                False,
                False,
                False,
                False,
                True,
                False,
                False,
            ),
            expected_parameter_decision="conditional_needs_even_D_kronecker_clause",
            expected_product_decision="conditional_missing_exact_product",
            matched_clause="omega_D is defined without the ordinary prime-to-6 Kato-Siegel hypothesis",
            first_missing_clause="specialization to the p25 75-atom mixed product P",
        ),
        SprangObservation(
            name="sprang_appendix_distribution_relation",
            source_clause="Appendix A Theorem A.2 / Corollaries A.3-A.4",
            source_handle="arXiv:1801.05677, distribution relation for the Kronecker section",
            parameter_row_name=None,
            product_claim=ExactProductClaim(
                "sprang_appendix_distribution_relation",
                "sprang_prop_5_4_kato_siegel_dlog",
                "divisor-additive",
                False,
                False,
                False,
                False,
                True,
                False,
                False,
            ),
            expected_parameter_decision=None,
            expected_product_decision="conditional_missing_exact_product",
            matched_clause="distribution relations are a plausible arithmetic producer surface",
            first_missing_clause="the exact C=(47,28), D=(22,3), K=(57,0) product and mixed graph",
        ),
        SprangObservation(
            name="ordinary_kato_theta_d2_shortcut",
            source_clause="classical Kato-Siegel theta_D comparison",
            source_handle="arXiv:1801.05677, Corollary 5.7 comparison clause",
            parameter_row_name="ordinary_kato_theta_parameter_2",
            product_claim=None,
            expected_parameter_decision="reject_ordinary_kato_theta_2_prime_to_6_violation",
            expected_product_decision=None,
            matched_clause="ordinary theta_D comparison is only the odd-D control",
            first_missing_clause="ordinary theta_D source clause allowing D=2",
        ),
        SprangObservation(
            name="sprang_exact_p_additive_identity_hypothetical",
            source_clause="not supplied by the inspected source clauses; closing calibration row",
            source_handle="local exact-product intake",
            parameter_row_name=None,
            product_claim=ExactProductClaim(
                "sprang_exact_p_additive_identity_hypothetical",
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
            expected_parameter_decision=None,
            expected_product_decision="closing_exact_product_identity",
            matched_clause="would close the divisor/additive theorem side",
            first_missing_clause="DANGER3 extraction and official vpp.py verification remain separate",
        ),
    )


def profile_sprang_kronecker_d2_scout() -> SprangScoutProfile:
    rows = observations()
    hygiene = profile_source_parameter_hygiene()
    d2_obligation = profile_d2_theorem_obligation()
    parameter_rows = {row.name: row for row in hygiene.rows}

    parameter_decisions = tuple(
        parameter_rows[row.parameter_row_name].decision
        if row.parameter_row_name is not None
        else None
        for row in rows
    )
    product_decisions = tuple(
        classify_exact_product(row.product_claim) if row.product_claim is not None else None
        for row in rows
    )

    even_d_live = sum(
        int(decision == "conditional_needs_even_D_kronecker_clause")
        for decision in parameter_decisions
    )
    direct_closing = sum(
        int(decision is not None and decision.closes_route and "hypothetical" not in row.name)
        for row, decision in zip(rows, product_decisions)
    )
    hypothetical_closing = sum(
        int(decision is not None and decision.closes_route and "hypothetical" in row.name)
        for row, decision in zip(rows, product_decisions)
    )
    rejected = sum(
        int(
            (decision is not None and decision.startswith("reject_"))
            or (
                product is not None
                and product.decision.startswith("reject_")
            )
        )
        for decision, product in zip(parameter_decisions, product_decisions)
    )
    conditional = len(rows) - direct_closing - hypothetical_closing - rejected

    row_ok = (
        len(rows) == 5
        and d2_obligation.row_ok
        and even_d_live == 2
        and direct_closing == 0
        and conditional == 3
        and rejected == 1
        and hypothetical_closing == 1
        and all(
            expected == actual
            for expected, actual in zip(
                (row.expected_parameter_decision for row in rows),
                parameter_decisions,
            )
        )
        and all(
            row.expected_product_decision is None
            or (
                product is not None
                and product.decision == row.expected_product_decision
            )
            for row, product in zip(rows, product_decisions)
        )
    )

    return SprangScoutProfile(
        source=SOURCE,
        observations=rows,
        d2_obligation_ok=d2_obligation.row_ok,
        even_d_live_rows=even_d_live,
        direct_closing_rows=direct_closing,
        conditional_rows=conditional,
        rejected_rows=rejected,
        hypothetical_closing_rows=hypothetical_closing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_sprang_kronecker_d2_scout()
    hygiene = profile_source_parameter_hygiene()
    parameter_rows = {row.name: row for row in hygiene.rows}

    print("p25 KSY-y Sprang/Kronecker D=2 primary-source scout gate")
    print(f"source={profile.source}")
    print(f"d2_obligation_ok={int(profile.d2_obligation_ok)}")
    print("observations")
    for row in profile.observations:
        parameter_decision = (
            parameter_rows[row.parameter_row_name].decision
            if row.parameter_row_name is not None
            else "not_run"
        )
        product_decision = (
            classify_exact_product(row.product_claim).decision
            if row.product_claim is not None
            else "not_run"
        )
        closes = (
            classify_exact_product(row.product_claim).closes_route
            if row.product_claim is not None
            else False
        )
        print(
            "  "
            f"{row.name}: clause={row.source_clause} handle={row.source_handle} "
            f"parameter_decision={parameter_decision} product_decision={product_decision} "
            f"closes={int(closes)} matched={row.matched_clause} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  even_d_live_rows={profile.even_d_live_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  hypothetical_closing_rows={profile.hypothetical_closing_rows}")
    print("interpretation")
    print("  sprang_even_D_kronecker_route_remains_live=1")
    print("  ordinary_kato_theta_D2_import_is_rejected=1")
    print("  distribution_or_dlog_framework_without_exact_P_does_not_close=1")
    print("  exact_P_or_theta2_additive_identity_is_required=1")
    print(f"ksy_y_sprang_kronecker_d2_primary_source_scout_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Sprang/Kronecker D=2 primary-source scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
