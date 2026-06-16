#!/usr/bin/env python3
"""Siegel-Robert/Siegel-Ramachandra period-value scout for p25 KSY-y.

Schertz and Shin are relevant to the value-unit side: they give ray-class
field generators from elliptic units / Siegel-Ramachandra invariants.  The p25
moonshot needs a narrower object.  A value theorem must emit the exact product
P, preserve the mixed graph, be a finite-field identity, and carry period-156
branch/root/telescoping context.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate import (
    PeriodValueUpgradeRow,
    classify_period_value_row,
    profile_period_value_upgrade,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate import (
    SourceClaim,
    classify_claim as classify_source_claim,
)


SOURCE = "Schertz/Shin Siegel-Robert and Siegel-Ramachandra value units"


@dataclass(frozen=True)
class PeriodValueObservation:
    name: str
    source_clause: str
    source_handle: str
    value_row: PeriodValueUpgradeRow
    source_claim: SourceClaim
    expected_value_decision: str
    expected_source_decision: str
    matched_clause: str
    first_missing_clause: str


@dataclass(frozen=True)
class PeriodValueScoutProfile:
    source: str
    observations: tuple[PeriodValueObservation, ...]
    period_value_upgrade_ok: bool
    support_root_gcd_fp_star: int
    ambient_root_gcd_fp_star: int
    direct_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    hypothetical_closing_rows: int
    row_ok: bool


def period_row(
    name: str,
    output_kind: str,
    exact_product_p: bool,
    mixed_graph_selector: bool,
    finite_field_identity: bool,
    period_156_context: bool,
    ambient_780_only: bool,
    expected_decision: str,
) -> PeriodValueUpgradeRow:
    return classify_period_value_row(
        name,
        "siegel_robert_value_units",
        output_kind,
        exact_product_p,
        mixed_graph_selector,
        finite_field_identity,
        period_156_context,
        ambient_780_only,
        expected_decision,
    )


def observations() -> tuple[PeriodValueObservation, ...]:
    return (
        PeriodValueObservation(
            name="schertz_klein_quotient_generator",
            source_clause="elliptic-unit/Klein-form quotient ray-class generator",
            source_handle="Schertz, EuDML doc 248002 / Numdam JTNB 9 (1997), 383-394",
            value_row=period_row(
                "schertz_klein_quotient_generator",
                "field-generation",
                False,
                False,
                False,
                False,
                False,
                "reject_field_generation_not_value_theorem",
            ),
            source_claim=SourceClaim(
                "schertz_klein_quotient_generator",
                "siegel_robert_value_units",
                "field-generation",
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            expected_value_decision="reject_field_generation_not_value_theorem",
            expected_source_decision="reject_not_closure_theorem",
            matched_clause="elliptic units / Klein-form quotient class-field generator language",
            first_missing_clause="exact finite-field value identity for P",
        ),
        PeriodValueObservation(
            name="shin_siegel_ramachandra_generator",
            source_clause="Siegel-Ramachandra invariant primitive generator",
            source_handle="Shin, arXiv:1009.2253",
            value_row=period_row(
                "shin_siegel_ramachandra_generator",
                "field-generation",
                False,
                False,
                False,
                False,
                False,
                "reject_field_generation_not_value_theorem",
            ),
            source_claim=SourceClaim(
                "shin_siegel_ramachandra_generator",
                "siegel_robert_value_units",
                "field-generation",
                False,
                False,
                False,
                False,
                False,
                False,
            ),
            expected_value_decision="reject_field_generation_not_value_theorem",
            expected_source_decision="reject_not_closure_theorem",
            matched_clause="Siegel-Ramachandra invariants can generate ray class fields",
            first_missing_clause="exact P with mixed graph and finite-field identity",
        ),
        PeriodValueObservation(
            name="siegel_robert_bare_exact_value",
            source_clause="hypothetical exact value without support-period context",
            source_handle="local period-value upgrade calibration row",
            value_row=period_row(
                "siegel_robert_bare_exact_value",
                "value",
                True,
                True,
                True,
                False,
                False,
                "conditional_missing_period_156_context",
            ),
            source_claim=SourceClaim(
                "siegel_robert_bare_exact_value",
                "siegel_robert_value_units",
                "value",
                True,
                True,
                False,
                True,
                False,
                False,
            ),
            expected_value_decision="conditional_missing_period_156_context",
            expected_source_decision="conditional_missing_period_156_context",
            matched_clause="would hit exact P value, but not the branch/root selector",
            first_missing_clause="period-156 branch/root/telescoping context",
        ),
        PeriodValueObservation(
            name="siegel_robert_ambient_780_value",
            source_clause="ambient orbit value without support-period fixedness",
            source_handle="local raw orientation value-route falsifier",
            value_row=period_row(
                "siegel_robert_ambient_780_value",
                "value",
                True,
                True,
                True,
                False,
                True,
                "reject_ambient_780_mu11_branch",
            ),
            source_claim=SourceClaim(
                "siegel_robert_ambient_780_value",
                "generic_field_generation_or_ambient_value",
                "value",
                True,
                True,
                False,
                True,
                False,
                False,
            ),
            expected_value_decision="reject_ambient_780_mu11_branch",
            expected_source_decision="reject_not_closure_theorem",
            matched_clause="records the ambient value branch obstruction",
            first_missing_clause="support-period 156 branch/root/telescoping context",
        ),
        PeriodValueObservation(
            name="siegel_robert_exact_value_with_period_hypothetical",
            source_clause="not supplied by inspected source handles; closing calibration row",
            source_handle="local period-value upgrade gate",
            value_row=period_row(
                "siegel_robert_exact_value_with_period_hypothetical",
                "value",
                True,
                True,
                True,
                True,
                False,
                "closing_value_identity_with_period_156",
            ),
            source_claim=SourceClaim(
                "siegel_robert_exact_value_with_period_hypothetical",
                "siegel_robert_value_units",
                "value",
                True,
                True,
                True,
                True,
                False,
                False,
            ),
            expected_value_decision="closing_value_identity_with_period_156",
            expected_source_decision="closing_value_identity_with_period_156",
            matched_clause="would close the value-theorem side",
            first_missing_clause="DANGER3 policy/extraction and official vpp.py verification remain separate",
        ),
    )


def profile_siegel_robert_period_value_scout() -> PeriodValueScoutProfile:
    rows = observations()
    period_profile = profile_period_value_upgrade()
    value_decisions = tuple(row.value_row for row in rows)
    source_decisions = tuple(classify_source_claim(row.source_claim) for row in rows)

    direct_closing = sum(
        int(row.closes_route and "hypothetical" not in obs.name)
        for obs, row in zip(rows, value_decisions)
    )
    hypothetical_closing = sum(
        int(row.closes_route and "hypothetical" in obs.name)
        for obs, row in zip(rows, value_decisions)
    )
    rejected = sum(int(row.decision.startswith("reject_")) for row in value_decisions)
    conditional = len(rows) - direct_closing - hypothetical_closing - rejected

    row_ok = (
        len(rows) == 5
        and period_profile.row_ok
        and period_profile.support_root_gcd_fp_star == 1
        and period_profile.ambient_root_gcd_fp_star == 11
        and direct_closing == 0
        and conditional == 1
        and rejected == 3
        and hypothetical_closing == 1
        and all(row.value_row.decision == row.expected_value_decision for row in rows)
        and all(
            decision.decision == row.expected_source_decision
            for row, decision in zip(rows, source_decisions)
        )
    )

    return PeriodValueScoutProfile(
        source=SOURCE,
        observations=rows,
        period_value_upgrade_ok=period_profile.row_ok,
        support_root_gcd_fp_star=period_profile.support_root_gcd_fp_star,
        ambient_root_gcd_fp_star=period_profile.ambient_root_gcd_fp_star,
        direct_closing_rows=direct_closing,
        conditional_rows=conditional,
        rejected_rows=rejected,
        hypothetical_closing_rows=hypothetical_closing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_siegel_robert_period_value_scout()
    print("p25 KSY-y Siegel-Robert period-value primary-source scout gate")
    print(f"source={profile.source}")
    print(f"period_value_upgrade_ok={int(profile.period_value_upgrade_ok)}")
    print(f"support_root_gcd_Fp_star={profile.support_root_gcd_fp_star}")
    print(f"ambient_root_gcd_Fp_star={profile.ambient_root_gcd_fp_star}")
    print("observations")
    for row in profile.observations:
        source_decision = classify_source_claim(row.source_claim)
        print(
            "  "
            f"{row.name}: clause={row.source_clause} handle={row.source_handle} "
            f"value_decision={row.value_row.decision} "
            f"source_decision={source_decision.decision} "
            f"closes={int(row.value_row.closes_route)} "
            f"matched={row.matched_clause} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  hypothetical_closing_rows={profile.hypothetical_closing_rows}")
    print("interpretation")
    print("  siegel_robert_value_language_remains_live=1")
    print("  ray_class_generation_without_exact_P_is_rejected=1")
    print("  ambient_780_value_route_is_rejected=1")
    print("  exact_value_requires_period_156_context=1")
    print(
        "ksy_y_siegel_robert_period_value_primary_source_scout_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Siegel-Robert period-value primary-source scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
