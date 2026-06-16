#!/usr/bin/env python3
"""Source-family front-door router for the p25 KSY-y moonshot.

The priority-1 intake classifies abstract theorem claims.  This layer maps the
actual source families we keep discussing onto that intake, so the next
literature/expert pass can ask only for clauses that can close source stage.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    Conductor39SourceTheoremClaim,
    classify_claim as classify_conductor39_claim,
)
from p25_ksy_y_conductor39_twisted_descent_candidate_router_gate import (
    TwistedDescentCandidate,
    classify_candidate as classify_twisted_candidate,
)
from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    H0SourceTheoremCandidate,
    classify_candidate as classify_h0_candidate,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    ClosingTheoremClaim,
    classify_claim as classify_exact_product_claim,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate import (
    CornerProducerCandidate,
    classify_candidate as classify_curved_corner_candidate,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_koo_shin_source_clause_matrix_20260614.md",
        "ksy_y_h0_koo_shin_source_clause_matrix_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_primary_source_verdict_20260613.md",
        "ksy_y_priority1_primary_source_verdict_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_sprang_exact_specialization_frontier_20260614.md",
        "ksy_y_sprang_exact_specialization_frontier_rows=1/1",
    ),
    (
        RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_theorem_source_screen.md",
        "robert_ksy_theta2_theorem_source_screen_rows=1/1",
    ),
    (
        RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation.md",
        "robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows=1/1",
    ),
)


@dataclass(frozen=True)
class SourceFrontdoorRow:
    name: str
    source_family: str
    frontdoor: str
    classifier: str
    decision: str
    current_evidence: bool
    source_stage_closes: bool
    priority1: bool
    avoids_value_branch: bool
    needs_period156_context: bool
    continue_external_search: bool
    kill_as_direct_closer: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class SourceFrontdoorRouterProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    rows: tuple[SourceFrontdoorRow, ...]
    row_count: int
    current_evidence_rows: int
    source_closing_shape_rows: int
    current_source_theorem_rows: int
    priority1_rows: int
    avoids_value_branch_rows: int
    needs_period156_context_rows: int
    continue_external_search_rows: int
    kill_as_direct_closer_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def decision_missing(decision: Any) -> str:
    return str(
        getattr(
            decision,
            "first_missing_or_falsifier",
            getattr(decision, "first_missing_clause", ""),
        )
    )


def decision_ok(decision: Any) -> bool:
    return bool(getattr(decision, "ok", getattr(decision, "row_ok", False)))


def row_from_decision(
    *,
    name: str,
    source_family: str,
    frontdoor: str,
    classifier: str,
    decision: Any,
    current_evidence: bool = False,
    priority1: bool = False,
    avoids_value_branch: bool = False,
    needs_period156_context: bool = False,
    continue_external_search: bool = True,
    kill_as_direct_closer: bool = False,
) -> SourceFrontdoorRow:
    closes = bool(
        getattr(decision, "source_stage_closed", False)
        or getattr(decision, "theorem_source_closed", False)
        or getattr(decision, "source_theorem_closed", False)
    )
    return SourceFrontdoorRow(
        name=name,
        source_family=source_family,
        frontdoor=frontdoor,
        classifier=classifier,
        decision=decision.decision,
        current_evidence=current_evidence,
        source_stage_closes=closes,
        priority1=priority1,
        avoids_value_branch=avoids_value_branch,
        needs_period156_context=needs_period156_context,
        continue_external_search=continue_external_search,
        kill_as_direct_closer=kill_as_direct_closer,
        first_missing_or_falsifier=decision_missing(decision),
        next_action=str(getattr(decision, "next_action", "")),
        ok=decision_ok(decision),
    )


def manual_row(
    *,
    name: str,
    source_family: str,
    frontdoor: str,
    decision: str,
    current_evidence: bool,
    source_stage_closes: bool,
    priority1: bool,
    avoids_value_branch: bool,
    needs_period156_context: bool,
    continue_external_search: bool,
    kill_as_direct_closer: bool,
    first_missing_or_falsifier: str,
    next_action: str,
) -> SourceFrontdoorRow:
    return SourceFrontdoorRow(
        name=name,
        source_family=source_family,
        frontdoor=frontdoor,
        classifier="recorded_source_screen",
        decision=decision,
        current_evidence=current_evidence,
        source_stage_closes=source_stage_closes,
        priority1=priority1,
        avoids_value_branch=avoids_value_branch,
        needs_period156_context=needs_period156_context,
        continue_external_search=continue_external_search,
        kill_as_direct_closer=kill_as_direct_closer,
        first_missing_or_falsifier=first_missing_or_falsifier,
        next_action=next_action,
        ok=True,
    )


def h0_candidate(
    name: str,
    *,
    output_kind: str,
    source: bool,
    h90_boundary: bool = True,
    period156: bool = False,
) -> H0SourceTheoremCandidate:
    return H0SourceTheoremCandidate(
        name=name,
        product_multiplier=1,
        residue_sets_exact=True,
        arithmetic_source_theorem=source,
        output_kind=output_kind,
        period156_context=period156,
        h90_boundary=h90_boundary,
        danger3_framing=False,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_x0=False,
        official_vpp=False,
    )


def conductor39_claim(
    name: str,
    *,
    output_kind: str = "divisor-additive",
    finite_or_divisor: bool = True,
    period156: bool = False,
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    projection: bool = False,
) -> Conductor39SourceTheoremClaim:
    return Conductor39SourceTheoremClaim(
        name=name,
        theorem_body_verified=True,
        source_object="W" if emits else "projection",
        emits_conductor39_object=emits,
        preserves_mixed_tensor=mixed,
        yang_yu_legal_unit=legal,
        sparse_formal_gauge_only=False,
        proper_axis_or_projection_only=projection,
        additive_separated=False,
        yang_distribution_to_507=emits,
        frobenius_or_hilbert90_descent=emits,
        output_kind=output_kind,
        finite_field_identity_or_divisor_theorem=finite_or_divisor,
        period_156_context=period156,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def twisted_candidate(name: str, *, period156: bool = True) -> TwistedDescentCandidate:
    return TwistedDescentCandidate(
        name=name,
        theorem_body_verified=True,
        uses_degree6_orbit=True,
        uses_pure_norm=False,
        uses_pair_sum=False,
        uses_signed_shadow=False,
        uses_quotient_or_ratio=True,
        uses_hilbert90_boundary=True,
        finite_value_or_divisor_theorem=True,
        period156_context=period156,
        arithmetic_source_theorem=True,
        danger3_framing=False,
        extraction_to_A_x0=False,
        official_vpp=False,
    )


def exact_product_claim(
    name: str,
    *,
    exact_p: bool,
    mixed: bool,
    source: bool,
    output_kind: str = "divisor-additive",
    finite_identity: bool = True,
    period156: bool = False,
) -> ClosingTheoremClaim:
    return ClosingTheoremClaim(
        name=name,
        source_family="Kubert-Lang/KSY exact normalized-y product",
        emits_exact_p=exact_p,
        preserves_mixed_graph=mixed,
        equal_weight_atoms=True,
        orientation_recorded=True,
        arithmetic_source_theorem=source,
        output_kind=output_kind,
        finite_field_identity_for_p=finite_identity,
        period_156_context=period156,
        danger3_policy_or_non_cm_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def curved_corner_candidate(name: str, *, period156: bool = True) -> CornerProducerCandidate:
    return CornerProducerCandidate(
        name=name,
        theorem_body_verified=True,
        exact_curved_row_triangle=True,
        primitive_newton_curvature=True,
        recorded_half_bridge_edge=True,
        full_order25_k_trace=True,
        raw_d3_y_relation=True,
        raw_kernel_trace_accounted=True,
        primitive_c169_motion=True,
        active_c169_lift_selected=True,
        quadratic_fiber_section=True,
        nonsplit_c169_carry_transport=True,
        unit_triangle_law=True,
        finite_value_or_divisor_theorem=True,
        period156_context=period156,
        arithmetic_source_theorem=True,
        danger3_framing=False,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_A_x0=False,
        official_vpp=False,
    )


def frontdoor_rows() -> tuple[SourceFrontdoorRow, ...]:
    return (
        manual_row(
            name="inspected_sprang_ksy_primary_sources",
            source_family="Sprang/KSY inspected primary sources",
            frontdoor="exact P product specialization",
            decision="current_sources_missing_exact_product_specialization",
            current_evidence=True,
            source_stage_closes=False,
            priority1=False,
            avoids_value_branch=False,
            needs_period156_context=False,
            continue_external_search=True,
            kill_as_direct_closer=True,
            first_missing_or_falsifier="exact finite p25 product P with mixed graph, equal weights, and orientation",
            next_action="search only for an external exact specialization; do not reread broad Sprang/KSY clauses",
        ),
        row_from_decision(
            name="koo_shin_6_2_h0_source_certification",
            source_family="Koo-Shin 2010 Theorem 6.2",
            frontdoor="H0 product legality",
            classifier="h0_source_theorem_candidate_matcher",
            decision=classify_h0_candidate(
                h0_candidate(
                    "koo_shin_6_2_h0_source_certification",
                    output_kind="source-certification",
                    source=True,
                )
            ),
            current_evidence=True,
            continue_external_search=True,
        ),
        row_from_decision(
            name="h0_exact_divisor_boundary_theorem",
            source_family="H0/Yang/Kubert-Lang",
            frontdoor="exact H0 divisor/additive identity with H90 boundary",
            classifier="h0_source_theorem_candidate_matcher",
            decision=classify_h0_candidate(
                h0_candidate(
                    "h0_exact_divisor_boundary_theorem",
                    output_kind="divisor-additive",
                    source=True,
                    h90_boundary=True,
                )
            ),
            priority1=True,
            avoids_value_branch=True,
        ),
        row_from_decision(
            name="conductor39_mixed_divisor_theorem",
            source_family="mixed conductor-39 unit / Yang distribution",
            frontdoor="U_chi/W divisor or additive identity",
            classifier="conductor39_source_theorem_intake",
            decision=classify_conductor39_claim(
                conductor39_claim("conductor39_mixed_divisor_theorem")
            ),
            priority1=True,
            avoids_value_branch=True,
        ),
        row_from_decision(
            name="twisted_h90_divisor_theorem",
            source_family="twisted ratio / Hilbert-90",
            frontdoor="twisted/H90 divisor identity with period-156 bridge context",
            classifier="twisted_descent_candidate_router",
            decision=classify_twisted_candidate(
                twisted_candidate("twisted_h90_divisor_theorem")
            ),
            priority1=True,
            avoids_value_branch=True,
            needs_period156_context=True,
        ),
        row_from_decision(
            name="curved_corner_divisor_theorem",
            source_family="unit-triangle curved K-traced corner",
            frontdoor="curved-corner divisor identity with period-156 context",
            classifier="curved_corner_producer_intake",
            decision=classify_curved_corner_candidate(
                curved_corner_candidate("curved_corner_divisor_theorem")
            ),
            priority1=True,
            avoids_value_branch=True,
            needs_period156_context=True,
        ),
        row_from_decision(
            name="exact_75_atom_product_divisor_theorem",
            source_family="Kubert-Lang / KSY normalized-y",
            frontdoor="exact 75-atom P divisor/additive theorem",
            classifier="closing_theorem_obligation",
            decision=classify_exact_product_claim(
                exact_product_claim(
                    "exact_75_atom_product_divisor_theorem",
                    exact_p=True,
                    mixed=True,
                    source=True,
                )
            ),
            priority1=True,
            avoids_value_branch=True,
        ),
        row_from_decision(
            name="exact_75_atom_value_no_period",
            source_family="Kubert-Lang / KSY normalized-y",
            frontdoor="exact P value identity without support-period context",
            classifier="closing_theorem_obligation",
            decision=classify_exact_product_claim(
                exact_product_claim(
                    "exact_75_atom_value_no_period",
                    exact_p=True,
                    mixed=True,
                    source=True,
                    output_kind="value",
                    finite_identity=True,
                    period156=False,
                )
            ),
            priority1=False,
            avoids_value_branch=False,
            needs_period156_context=True,
        ),
        row_from_decision(
            name="generic_modular_unit_or_cm_generation",
            source_family="generic Kubert-Lang/Koo-Shin/CM generator",
            frontdoor="field generation or broad modular-unit vocabulary",
            classifier="closing_theorem_obligation",
            decision=classify_exact_product_claim(
                exact_product_claim(
                    "generic_modular_unit_or_cm_generation",
                    exact_p=False,
                    mixed=False,
                    source=False,
                    output_kind="field-generation",
                    finite_identity=False,
                )
            ),
            continue_external_search=False,
            kill_as_direct_closer=True,
        ),
        row_from_decision(
            name="finite_payload_without_source",
            source_family="local finite harness",
            frontdoor="computed verifier payload only",
            classifier="closing_theorem_obligation",
            decision=classify_exact_product_claim(
                exact_product_claim(
                    "finite_payload_without_source",
                    exact_p=True,
                    mixed=True,
                    source=False,
                )
            ),
            continue_external_search=True,
        ),
        row_from_decision(
            name="prime_projection_or_axis_shadow",
            source_family="projection shortcut",
            frontdoor="prime-13/C169 or axis-only shadow",
            classifier="conductor39_source_theorem_intake",
            decision=classify_conductor39_claim(
                conductor39_claim(
                    "prime_projection_or_axis_shadow",
                    finite_or_divisor=False,
                    emits=False,
                    mixed=False,
                    legal=False,
                    projection=True,
                )
            ),
            continue_external_search=False,
            kill_as_direct_closer=True,
        ),
    )


def profile_source_frontdoor_router() -> SourceFrontdoorRouterProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = frontdoor_rows()
    current = sum(row.current_evidence for row in rows)
    source_closing = sum(row.source_stage_closes for row in rows)
    current_sources = sum(row.current_evidence and row.source_stage_closes for row in rows)
    priority1 = sum(row.priority1 for row in rows)
    avoids_value = sum(row.avoids_value_branch for row in rows)
    needs_period = sum(row.needs_period156_context for row in rows)
    continue_rows = sum(row.continue_external_search for row in rows)
    kill_rows = sum(row.kill_as_direct_closer for row in rows)
    decisions = tuple(row.decision for row in rows)
    expected = (
        "current_sources_missing_exact_product_specialization",
        "source_certified_value_or_divisor_missing",
        "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_value_missing_period_156",
            "reject_not_exact_p",
            "conditional_finite_payload_without_source_theorem",
        "reject_loses_mixed_tensor",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 11
        and current == 2
        and source_closing == 5
        and current_sources == 0
        and priority1 == 5
        and avoids_value == 5
        and needs_period == 3
        and continue_rows == 9
        and kill_rows == 3
        and decisions == expected
        and all(row.ok for row in rows)
    )
    return SourceFrontdoorRouterProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        source_closing_shape_rows=source_closing,
        current_source_theorem_rows=current_sources,
        priority1_rows=priority1,
        avoids_value_branch_rows=avoids_value,
        needs_period156_context_rows=needs_period,
        continue_external_search_rows=continue_rows,
        kill_as_direct_closer_rows=kill_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_source_frontdoor_router()
    print("p25 KSY-y source-family front-door router gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("frontdoor_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: family={row.source_family} classifier={row.classifier} "
            f"decision={row.decision} current={int(row.current_evidence)} "
            f"source_closes={int(row.source_stage_closes)} "
            f"priority1={int(row.priority1)} avoids_value={int(row.avoids_value_branch)} "
            f"period156={int(row.needs_period156_context)} "
            f"continue={int(row.continue_external_search)} kill={int(row.kill_as_direct_closer)}"
        )
        print(f"    frontdoor={row.frontdoor}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  source_closing_shape_rows={profile.source_closing_shape_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  avoids_value_branch_rows={profile.avoids_value_branch_rows}")
    print(f"  needs_period156_context_rows={profile.needs_period156_context_rows}")
    print(f"  continue_external_search_rows={profile.continue_external_search_rows}")
    print(f"  kill_as_direct_closer_rows={profile.kill_as_direct_closer_rows}")
    print("interpretation")
    print("  current_sources_do_not_close_source_stage=1")
    print("  best_next_frontdoors_are_h0_conductor39_twisted_curved_or_exact75_divisor=1")
    print("  generic_generation_projection_and_broad_vocabulary_are_direct_closer_kills=1")
    print("  exact_value_hits_still_need_period156_context=1")
    print(f"ksy_y_source_frontdoor_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("source front-door router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
