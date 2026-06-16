#!/usr/bin/env python3
"""Sprang source-split gate for the p25 priority-1 divisor lane.

Priority 1 keeps Sprang/Kronecker alive, but there are two nearby Sprang
source handles with different jobs:

* arXiv:1801.05677 gives Eisenstein-Kronecker series via the Poincare bundle;
* arXiv:1802.04996 gives the algebraic de Rham realization of the elliptic
  polylogarithm via the Poincare bundle.

Neither source handle currently supplies the exact p25 anti-invariant product.
This gate keeps them distinct and records the exact upgrade needed before a
Sprang hit can be treated as a priority-1 theorem closure.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_priority1_exact_divisor_lane_gate import (
    profile_priority1_exact_divisor_lane,
)
from p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate import (
    profile_sprang_kronecker_d2_scout,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product_claim,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate import (
    profile_source_parameter_hygiene,
)


@dataclass(frozen=True)
class SprangSourceSplitRow:
    name: str
    source_url: str
    verified_title: str
    source_role: str
    priority1_output_type: str
    claim: ExactProductClaim | None
    expected_decision: str
    observed_decision: str
    first_missing_clause: str
    recommendation: str
    closes_priority1: bool
    row_ok: bool


@dataclass(frozen=True)
class SprangSourceSplitProfile:
    priority1_lane_ok: bool
    sprang_scout_ok: bool
    source_parameter_hygiene_ok: bool
    rows: tuple[SprangSourceSplitRow, ...]
    distinct_primary_sources: int
    conditional_source_handles: int
    rejected_imports: int
    closing_hypotheticals: int
    row_ok: bool


def claim(
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
        "sprang_prop_5_4_kato_siegel_dlog",
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
    source_url: str,
    verified_title: str,
    source_role: str,
    priority1_output_type: str,
    product_claim: ExactProductClaim,
    expected_decision: str,
    first_missing_clause: str,
    recommendation: str,
    closes_priority1: bool,
) -> SprangSourceSplitRow:
    decision = classify_exact_product_claim(product_claim)
    return SprangSourceSplitRow(
        name=name,
        source_url=source_url,
        verified_title=verified_title,
        source_role=source_role,
        priority1_output_type=priority1_output_type,
        claim=product_claim,
        expected_decision=expected_decision,
        observed_decision=decision.decision,
        first_missing_clause=first_missing_clause,
        recommendation=recommendation,
        closes_priority1=closes_priority1,
        row_ok=(
            decision.decision == expected_decision
            and decision.closes_route == closes_priority1
        ),
    )


def manual_row(
    name: str,
    source_url: str,
    verified_title: str,
    source_role: str,
    priority1_output_type: str,
    observed_decision: str,
    expected_decision: str,
    first_missing_clause: str,
    recommendation: str,
) -> SprangSourceSplitRow:
    return SprangSourceSplitRow(
        name=name,
        source_url=source_url,
        verified_title=verified_title,
        source_role=source_role,
        priority1_output_type=priority1_output_type,
        claim=None,
        expected_decision=expected_decision,
        observed_decision=observed_decision,
        first_missing_clause=first_missing_clause,
        recommendation=recommendation,
        closes_priority1=False,
        row_ok=observed_decision == expected_decision,
    )


def source_split_rows() -> tuple[SprangSourceSplitRow, ...]:
    return (
        row_from_claim(
            "sprang_1801_eisenstein_kronecker_surface",
            "https://arxiv.org/abs/1801.05677",
            "Eisenstein-Kronecker series via the Poincare bundle",
            "Kronecker-section / Eisenstein-Kronecker construction and distribution vocabulary",
            "formula-language",
            claim(
                "sprang_1801_eisenstein_kronecker_surface",
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
            "explicit specialization to exact P or theta2/theta2^-1 divisor data",
            "continue as source vocabulary only if upgraded to exact product output",
            False,
        ),
        row_from_claim(
            "sprang_1802_derham_polylog_surface",
            "https://arxiv.org/abs/1802.04996",
            "The algebraic de Rham realization of the elliptic polylogarithm via the Poincare bundle",
            "algebraic de Rham polylogarithm / Eisenstein-class differential-form surface",
            "formula-language",
            claim(
                "sprang_1802_derham_polylog_surface",
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
            "exact D=2 differential/additive output for the p25 anti-invariant product",
            "continue as differential-form surface only after exact C/D/K specialization",
            False,
        ),
        row_from_claim(
            "sprang_exact_d2_product_hypothetical",
            "https://arxiv.org/abs/1801.05677 + https://arxiv.org/abs/1802.04996",
            "Sprang source stack upgraded to exact D=2 p25 product",
            "hypothetical source theorem combining even-D geometry with exact p25 payload",
            "divisor-additive",
            claim(
                "sprang_exact_d2_product_hypothetical",
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
            "none in theorem lane; DANGER3 extraction remains separate",
            "accept as priority-1 theorem hit and route through theta2 certificate path",
            True,
        ),
    )


def profile_sprang_source_split() -> SprangSourceSplitProfile:
    priority1 = profile_priority1_exact_divisor_lane()
    sprang_scout = profile_sprang_kronecker_d2_scout()
    hygiene = profile_source_parameter_hygiene()
    rows = source_split_rows()
    ordinary_kato = next(
        row
        for row in hygiene.rows
        if row.name == "ordinary_kato_theta_parameter_2"
    )
    rows = rows + (
        manual_row(
            "ordinary_kato_theta_d2_import",
            "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            "ordinary Kato-Siegel theta_D control",
            "odd-D control theorem, not the Sprang even-D route",
            "rejected-import",
            ordinary_kato.decision,
            "reject_ordinary_kato_theta_2_prime_to_6_violation",
            "ordinary theta_D source clause allowing D=2",
            "kill direct ordinary theta_D import at D=2",
        ),
    )

    distinct_sources = len({row.source_url for row in rows if row.source_url.startswith("https://arxiv.org/abs/180")})
    conditional = sum(int(row.observed_decision.startswith("conditional_")) for row in rows)
    rejected = sum(int(row.observed_decision.startswith("reject_")) for row in rows)
    closing = sum(int(row.closes_priority1) for row in rows)
    row_ok = (
        priority1.row_ok
        and sprang_scout.row_ok
        and hygiene.row_ok
        and len(rows) == 4
        and distinct_sources == 3
        and conditional == 2
        and rejected == 1
        and closing == 1
        and tuple(row.name for row in rows)
        == (
            "sprang_1801_eisenstein_kronecker_surface",
            "sprang_1802_derham_polylog_surface",
            "sprang_exact_d2_product_hypothetical",
            "ordinary_kato_theta_d2_import",
        )
        and all(row.row_ok for row in rows)
    )
    return SprangSourceSplitProfile(
        priority1_lane_ok=priority1.row_ok,
        sprang_scout_ok=sprang_scout.row_ok,
        source_parameter_hygiene_ok=hygiene.row_ok,
        rows=rows,
        distinct_primary_sources=distinct_sources,
        conditional_source_handles=conditional,
        rejected_imports=rejected,
        closing_hypotheticals=closing,
        row_ok=row_ok,
    )


def print_row(row: SprangSourceSplitRow) -> None:
    print(
        "  "
        f"{row.name}: url={row.source_url} output={row.priority1_output_type} "
        f"decision={row.observed_decision} closes={int(row.closes_priority1)} "
        f"missing={row.first_missing_clause} recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_sprang_source_split()
    print("p25 KSY-y priority-1 Sprang source-split gate")
    print(f"priority1_lane_ok={int(profile.priority1_lane_ok)}")
    print(f"sprang_scout_ok={int(profile.sprang_scout_ok)}")
    print(f"source_parameter_hygiene_ok={int(profile.source_parameter_hygiene_ok)}")
    print("source_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  distinct_primary_sources={profile.distinct_primary_sources}")
    print(f"  conditional_source_handles={profile.conditional_source_handles}")
    print(f"  rejected_imports={profile.rejected_imports}")
    print(f"  closing_hypotheticals={profile.closing_hypotheticals}")
    print("interpretation")
    print("  sprang_1801_and_1802_source_handles_are_distinct=1")
    print("  both_source_handles_are_conditional_until_exact_p25_product_specialization=1")
    print("  ordinary_kato_theta_D2_import_is_rejected=1")
    print("  exact_D2_p25_product_identity_would_close_priority1=1")
    print(f"ksy_y_priority1_sprang_source_split_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 Sprang source-split regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
