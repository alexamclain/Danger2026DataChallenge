#!/usr/bin/env python3
"""Koo-Shin/Kubert-Lang hygiene bridge for the p25 KSY-y product.

The Koo-Shin access probe found a promising snippet for a prime-level
Siegel-function product/distribution theorem, but no theorem body.  This gate
records what can already be checked from the open Kubert-Lang-style product
criterion: the exact p25 footprint passes the elementary exponent congruences,
yet that is only a necessary screen and not a mixed-graph producer.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_koo_shin_distribution_access_probe_gate import (
    profile_koo_shin_distribution_access_probe,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    profile_kl_exponent_matrix_screen,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    profile_ksy_y_siegel_formula,
)


@dataclass(frozen=True)
class HygieneBridgeRow:
    name: str
    evidence: str
    level: int | None
    support: int | None
    congruence_ok: bool
    preserves_mixed_graph: bool
    source_theorem_ok: bool
    verdict: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class KooShinKLHygieneBridgeProfile:
    rows: tuple[HygieneBridgeRow, ...]
    target_footprint_rows: int
    congruence_positive_rows: int
    mixed_graph_positive_rows: int
    prime_power_projection_rows: int
    theorem_body_rows: int
    direct_closing_rows: int
    control_rejection_rows: int
    exact_product_intake_decision: str
    access_probe_ok: bool
    kl_screen_ok: bool
    siegel_formula_ok: bool
    row_ok: bool


def exact_product_hygiene_decision() -> str:
    """Classify the exact p25 footprint when no producer theorem is attached."""

    claim = ExactProductClaim(
        name="koo_shin_kl_hygiene_exact_footprint_no_theorem",
        anchor_name="ksy_normalized_y_siegel_formula",
        output_kind="divisor-additive",
        exact_product_p=True,
        mixed_graph_selector=True,
        equal_weight_atoms=True,
        orientation_branch=True,
        arithmetic_producer=False,
        challenge_legal=True,
        finite_intake_geometry=True,
    )
    return classify_exact_product(claim).decision


def bridge_rows() -> tuple[HygieneBridgeRow, ...]:
    access = profile_koo_shin_distribution_access_probe()
    kl = profile_kl_exponent_matrix_screen()
    formula = profile_ksy_y_siegel_formula()
    exact_decision = exact_product_hygiene_decision()
    controls_rejected = (
        kl.truncated_d_rejected
        and kl.wrong_d_rejected
        and kl.wrong_t_rejected
        and kl.positive_only_rejected
    )
    return (
        HygieneBridgeRow(
            name="ksy_y_four_layer_raw_footprint",
            evidence=(
                "KSY y(Q)=-g(2Q)/g(Q)^4 expanded over the 75 atoms; "
                "matches theta2-inverse raw footprint"
            ),
            level=kl.theta2_inverse_profile.level,
            support=formula.footprint_support,
            congruence_ok=kl.theta2_inverse_profile.quadratic_relations_ok,
            preserves_mixed_graph=True,
            source_theorem_ok=False,
            verdict="necessary_KL_hygiene_passes_not_source_theorem",
            first_missing_clause=(
                "source theorem that emits exact P/theta2 footprint, not only "
                "formula language or congruence hygiene"
            ),
            recommendation="continue_only_with_exact_product_theorem_body",
            row_ok=(
                formula.row_ok
                and formula.footprint_support == 300
                and kl.theta2_inverse_profile.level == 12675
                and kl.theta2_inverse_profile.quadratic_relations_ok
                and exact_decision == "conditional_missing_arithmetic_producer"
            ),
        ),
        HygieneBridgeRow(
            name="six_cell_mixed_source_packet",
            evidence=(
                "common-level source packet keeps the C_3 x C_169 row graph "
                "before K-trace expansion"
            ),
            level=kl.source_packet_profile.level,
            support=kl.source_packet_profile.support,
            congruence_ok=kl.source_packet_profile.quadratic_relations_ok,
            preserves_mixed_graph=True,
            source_theorem_ok=False,
            verdict="mixed_packet_hygiene_passes_but_needs_producer",
            first_missing_clause="arithmetic theorem selecting the six row-labeled pairs",
            recommendation="continue_as_first_falsifier_for_any_Koo_Shin_product_theorem",
            row_ok=(
                kl.source_packet_profile.level == 507
                and kl.source_packet_profile.support == 6
                and kl.source_packet_profile.quadratic_relations_ok
            ),
        ),
        HygieneBridgeRow(
            name="c169_prime_power_projection",
            evidence=(
                "prime-power projection preserves a Kubert-Lang congruence "
                "screen but drops the row selector and T-edge"
            ),
            level=kl.c_axis_projection_profile.level,
            support=kl.c_axis_projection_profile.support,
            congruence_ok=kl.c_axis_projection_profile.quadratic_relations_ok,
            preserves_mixed_graph=False,
            source_theorem_ok=False,
            verdict="prime_power_projection_is_necessary_but_insufficient",
            first_missing_clause="C_3 row labels, base anchor, and T-edge orientation",
            recommendation="kill_prime_power_projection_as_direct_closer",
            row_ok=(
                kl.c_axis_projection_profile.level == 169
                and kl.c_axis_projection_profile.quadratic_relations_ok
                and not kl.c_axis_projection_profile.p25_finite_payload_ok
                and kl.prime_power_projection_is_finite_insufficient
            ),
        ),
        HygieneBridgeRow(
            name="odd_prime_snippet_boundary",
            evidence=(
                "Koo-Shin 2010 snippet mentions an odd-prime product theorem, "
                "but access probe has no theorem body"
            ),
            level=None,
            support=None,
            congruence_ok=False,
            preserves_mixed_graph=False,
            source_theorem_ok=access.theorem_body_rows > 0,
            verdict="snippet_positive_not_enough_for_mixed_level_p25",
            first_missing_clause=(
                "full theorem body plus lift from odd-prime/prime-power data "
                "to the p25 mixed levels 507 and 12675"
            ),
            recommendation="continue_retrieval_do_not_claim_closure",
            row_ok=(
                access.row_ok
                and access.snippet_positive_rows == 1
                and access.theorem_body_rows == 0
                and access.direct_closing_rows == 0
            ),
        ),
        HygieneBridgeRow(
            name="local_control_falsifiers",
            evidence=(
                "truncated D, wrong D, wrong T, and positive-only variants fail "
                "the exponent screen"
            ),
            level=507,
            support=None,
            congruence_ok=False,
            preserves_mixed_graph=False,
            source_theorem_ok=False,
            verdict="controls_reject_wrong_geometry",
            first_missing_clause="exact D length, D step, T edge, and anti-invariant pairing",
            recommendation="use_controls_as_first_falsifier_for_theorem_mapping",
            row_ok=controls_rejected,
        ),
    )


def profile_koo_shin_kl_hygiene_bridge() -> KooShinKLHygieneBridgeProfile:
    rows = bridge_rows()
    access = profile_koo_shin_distribution_access_probe()
    kl = profile_kl_exponent_matrix_screen()
    formula = profile_ksy_y_siegel_formula()
    exact_decision = exact_product_hygiene_decision()
    target_footprint_rows = sum(
        row.name in {"ksy_y_four_layer_raw_footprint", "six_cell_mixed_source_packet"}
        for row in rows
    )
    congruence_positive_rows = sum(row.congruence_ok for row in rows)
    mixed_graph_positive_rows = sum(row.preserves_mixed_graph for row in rows)
    prime_power_projection_rows = sum(row.name == "c169_prime_power_projection" for row in rows)
    theorem_body_rows = access.theorem_body_rows
    direct_closing_rows = sum(row.source_theorem_ok and row.preserves_mixed_graph for row in rows)
    control_rejection_rows = sum(row.verdict == "controls_reject_wrong_geometry" and row.row_ok for row in rows)
    row_ok = (
        len(rows) == 5
        and target_footprint_rows == 2
        and congruence_positive_rows == 3
        and mixed_graph_positive_rows == 2
        and prime_power_projection_rows == 1
        and theorem_body_rows == 0
        and direct_closing_rows == 0
        and control_rejection_rows == 1
        and exact_decision == "conditional_missing_arithmetic_producer"
        and access.row_ok
        and kl.row_ok
        and formula.row_ok
        and all(row.row_ok for row in rows)
    )
    return KooShinKLHygieneBridgeProfile(
        rows=rows,
        target_footprint_rows=target_footprint_rows,
        congruence_positive_rows=congruence_positive_rows,
        mixed_graph_positive_rows=mixed_graph_positive_rows,
        prime_power_projection_rows=prime_power_projection_rows,
        theorem_body_rows=theorem_body_rows,
        direct_closing_rows=direct_closing_rows,
        control_rejection_rows=control_rejection_rows,
        exact_product_intake_decision=exact_decision,
        access_probe_ok=access.row_ok,
        kl_screen_ok=kl.row_ok,
        siegel_formula_ok=formula.row_ok,
        row_ok=row_ok,
    )


def print_row(row: HygieneBridgeRow) -> None:
    print(
        "  "
        f"{row.name}: level={row.level} support={row.support} "
        f"congruence_ok={int(row.congruence_ok)} "
        f"mixed_graph={int(row.preserves_mixed_graph)} "
        f"source_theorem={int(row.source_theorem_ok)} verdict={row.verdict}"
    )


def main() -> int:
    profile = profile_koo_shin_kl_hygiene_bridge()
    print("p25 KSY-y Koo-Shin/Kubert-Lang hygiene bridge gate")
    print("bridge_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  target_footprint_rows={profile.target_footprint_rows}")
    print(f"  congruence_positive_rows={profile.congruence_positive_rows}")
    print(f"  mixed_graph_positive_rows={profile.mixed_graph_positive_rows}")
    print(f"  prime_power_projection_rows={profile.prime_power_projection_rows}")
    print(f"  theorem_body_rows={profile.theorem_body_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  control_rejection_rows={profile.control_rejection_rows}")
    print(f"  exact_product_intake_decision={profile.exact_product_intake_decision}")
    print("dependency_checks")
    print(f"  access_probe_ok={int(profile.access_probe_ok)}")
    print(f"  kl_screen_ok={int(profile.kl_screen_ok)}")
    print(f"  siegel_formula_ok={int(profile.siegel_formula_ok)}")
    print("interpretation")
    print("  exact_p25_footprint_passes_KL_hygiene=1")
    print("  odd_prime_or_prime_power_projection_does_not_close_mixed_p25=1")
    print("  theorem_body_still_missing=1")
    print("  first_falsifier_is_exact_row_graph_and_mixed_level_lift=1")
    print(f"ksy_y_koo_shin_kl_hygiene_bridge_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin/Kubert-Lang hygiene bridge regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
