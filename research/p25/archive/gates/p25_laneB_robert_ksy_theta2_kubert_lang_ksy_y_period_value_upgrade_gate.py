#!/usr/bin/env python3
"""Period-value upgrade gate for p25 KSY-y source hits.

The source-claim intake already says that a finite-field value identity closes
only with period-156 context.  This gate makes the scout contract sharper:
period context is a necessary upgrade for value theorems, but it is not a
substitute for the exact product P, the mixed C_75 x C_169 graph, or a real
arithmetic producer theorem.

This encodes the p24 lesson in p25 terms: small verifier surfaces and broad
class-field generation are useful scaffolding, but they are not certificate
progress without branch/root selection for the embedded target object.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


P25 = 10000000000000000000000013
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780
LIVE_ANCHORS = {
    "ksy_theorem_5_3_ray_class_generation",
    "ksy_normalized_y_siegel_formula",
    "siegel_robert_value_units",
}


@dataclass(frozen=True)
class PeriodValueUpgradeRow:
    name: str
    anchor_name: str
    output_kind: str
    exact_product_p: bool
    mixed_graph_selector: bool
    finite_field_identity: bool
    period_156_context: bool
    ambient_780_only: bool
    decision: str
    closes_route: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class PeriodValueUpgradeProfile:
    uses_existing_closure_template: bool
    uses_existing_period_context: bool
    anchor_names_known: bool
    support_period: int
    support_root_gcd_fp_star: int
    ambient_period: int
    ambient_root_gcd_fp_star: int
    ambient_branch_count_fp_star: int
    upgrade_rows: tuple[PeriodValueUpgradeRow, ...]
    closing_value_shapes: int
    conditional_value_shapes: int
    rejected_value_shadows: int
    p24_transfer_lesson: str
    scout_contract: str
    row_ok: bool


def classify_period_value_row(
    name: str,
    anchor_name: str,
    output_kind: str,
    exact_product_p: bool,
    mixed_graph_selector: bool,
    finite_field_identity: bool,
    period_156_context: bool,
    ambient_780_only: bool,
    expected_decision: str,
) -> PeriodValueUpgradeRow:
    if output_kind == "field-generation":
        decision = "reject_field_generation_not_value_theorem"
        closes = False
        missing = "exact finite-field value identity for P"
        next_action = "discard unless reframed as exact P plus period-156 value context"
    elif output_kind == "finite-verifier":
        decision = "conditional_finite_verifier_without_arithmetic_producer"
        closes = False
        missing = "challenge-legal arithmetic producer theorem"
        next_action = "use as verifier payload only after a real source theorem emits it"
    elif ambient_780_only:
        decision = "reject_ambient_780_mu11_branch"
        closes = False
        missing = "support-period 156 branch/root/telescoping context"
        next_action = "ask for support-period fixedness; ambient values have unresolved F_p branches"
    elif not exact_product_p:
        decision = "conditional_missing_exact_product"
        closes = False
        missing = "exact product P with C=(47,28), D=(22,3), K=(57,0)"
        next_action = "ask the source theorem to emit P, not a broad value family"
    elif not mixed_graph_selector:
        decision = "conditional_missing_mixed_graph"
        closes = False
        missing = "mixed C_75 x C_169 graph selector"
        next_action = "ask for the exact 75 atoms and row/C graph, not a projection"
    elif not finite_field_identity:
        decision = "conditional_missing_finite_field_identity"
        closes = False
        missing = "finite-field value identity for P"
        next_action = "ask for the finite-field identity, not only complex/class-field values"
    elif not period_156_context:
        decision = "conditional_missing_period_156_context"
        closes = False
        missing = "period-156 branch/root/telescoping context"
        next_action = "ask for support-period fixedness so the F_p^* value root is unique"
    else:
        decision = "closing_value_identity_with_period_156"
        closes = True
        missing = "none"
        next_action = "route through value-with-period certificate path and policy check"

    return PeriodValueUpgradeRow(
        name=name,
        anchor_name=anchor_name,
        output_kind=output_kind,
        exact_product_p=exact_product_p,
        mixed_graph_selector=mixed_graph_selector,
        finite_field_identity=finite_field_identity,
        period_156_context=period_156_context,
        ambient_780_only=ambient_780_only,
        decision=decision,
        closes_route=closes,
        first_missing_clause=missing,
        next_action=next_action,
        row_ok=decision == expected_decision,
    )


def profile_period_value_upgrade() -> PeriodValueUpgradeProfile:
    rows = (
        classify_period_value_row(
            "ksy_exact_value_with_period",
            "ksy_normalized_y_siegel_formula",
            "value",
            True,
            True,
            True,
            True,
            False,
            "closing_value_identity_with_period_156",
        ),
        classify_period_value_row(
            "siegel_robert_exact_value_with_period",
            "siegel_robert_value_units",
            "value",
            True,
            True,
            True,
            True,
            False,
            "closing_value_identity_with_period_156",
        ),
        classify_period_value_row(
            "bare_siegel_robert_value",
            "siegel_robert_value_units",
            "value",
            True,
            True,
            True,
            False,
            False,
            "conditional_missing_period_156_context",
        ),
        classify_period_value_row(
            "period_context_without_exact_p",
            "siegel_robert_value_units",
            "value",
            False,
            True,
            True,
            True,
            False,
            "conditional_missing_exact_product",
        ),
        classify_period_value_row(
            "finite_verifier_without_source_theorem",
            "ksy_normalized_y_siegel_formula",
            "finite-verifier",
            True,
            True,
            False,
            True,
            False,
            "conditional_finite_verifier_without_arithmetic_producer",
        ),
        classify_period_value_row(
            "ambient_780_value_only",
            "siegel_robert_value_units",
            "value",
            True,
            True,
            True,
            False,
            True,
            "reject_ambient_780_mu11_branch",
        ),
        classify_period_value_row(
            "generic_ksy_ray_class_generation",
            "ksy_theorem_5_3_ray_class_generation",
            "field-generation",
            False,
            False,
            False,
            False,
            False,
            "reject_field_generation_not_value_theorem",
        ),
    )

    closing = sum(int(row.closes_route) for row in rows)
    conditional = sum(int(row.decision.startswith("conditional")) for row in rows)
    rejected = sum(int(row.decision.startswith("reject")) for row in rows)
    support_root_gcd = gcd(4**SUPPORT_PERIOD - 1, P25 - 1)
    ambient_root_gcd = gcd(4**AMBIENT_PERIOD - 1, P25 - 1)
    anchor_names_known = all(row.anchor_name in LIVE_ANCHORS for row in rows)

    row_ok = (
        SUPPORT_PERIOD == 156
        and AMBIENT_PERIOD == 780
        and support_root_gcd == 1
        and ambient_root_gcd == 11
        and anchor_names_known
        and len(rows) == 7
        and closing == 2
        and conditional == 3
        and rejected == 2
        and all(row.row_ok for row in rows)
        and all(
            not row.closes_route
            for row in rows
            if row.ambient_780_only or row.output_kind in ("field-generation", "finite-verifier")
        )
    )

    return PeriodValueUpgradeProfile(
        uses_existing_closure_template=True,
        uses_existing_period_context=True,
        anchor_names_known=anchor_names_known,
        support_period=SUPPORT_PERIOD,
        support_root_gcd_fp_star=support_root_gcd,
        ambient_period=AMBIENT_PERIOD,
        ambient_root_gcd_fp_star=ambient_root_gcd,
        ambient_branch_count_fp_star=ambient_root_gcd,
        upgrade_rows=rows,
        closing_value_shapes=closing,
        conditional_value_shapes=conditional,
        rejected_value_shadows=rejected,
        p24_transfer_lesson=(
            "small verifier payloads and broad CM/Lang generation do not close "
            "without an embedded branch/root-selected producer theorem"
        ),
        scout_contract=(
            "a value-source hit must emit exact P, preserve the mixed graph, "
            "prove a finite-field identity, and carry period-156 context"
        ),
        row_ok=row_ok,
    )


def print_row(row: PeriodValueUpgradeRow) -> None:
    print(
        "  "
        f"{row.name}: anchor={row.anchor_name} kind={row.output_kind} "
        f"exactP={int(row.exact_product_p)} graph={int(row.mixed_graph_selector)} "
        f"finite={int(row.finite_field_identity)} period156={int(row.period_156_context)} "
        f"ambient780={int(row.ambient_780_only)} closes={int(row.closes_route)} "
        f"decision={row.decision} missing={row.first_missing_clause}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y period-value upgrade gate")
    profile = profile_period_value_upgrade()
    print(f"period_value_upgrade_profile={profile}")
    print("value_route_denominators")
    print(f"  support_period={profile.support_period}")
    print(f"  support_root_gcd_Fp_star={profile.support_root_gcd_fp_star}")
    print(f"  ambient_period={profile.ambient_period}")
    print(f"  ambient_root_gcd_Fp_star={profile.ambient_root_gcd_fp_star}")
    print(f"  ambient_branch_count_Fp_star={profile.ambient_branch_count_fp_star}")
    print("upgrade_rows")
    for row in profile.upgrade_rows:
        print_row(row)
    print("counts")
    print(f"  closing_value_shapes={profile.closing_value_shapes}")
    print(f"  conditional_value_shapes={profile.conditional_value_shapes}")
    print(f"  rejected_value_shadows={profile.rejected_value_shadows}")
    print("interpretation")
    print("  period_156_context_is_required_for_value_route=1")
    print("  period_156_context_does_not_replace_exact_P_or_mixed_graph=1")
    print("  ambient_780_value_only_route_is_rejected=1")
    print("  p24_small_verifier_without_producer_lesson_applied=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
