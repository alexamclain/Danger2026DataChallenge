#!/usr/bin/env python3
"""Downstream route propagation for legal H0 translates.

The H0-translate compatibility gate makes the legal finite targets explicit.
This packet checks that those exact targets, and only those exact targets, can
enter the X_1(8112) / X_1(16) extraction ladder.  It is a route map, not an
extraction proof: every live route still stops before a verified DANGER3
triple.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_translate_value_compatibility_gate import (
    H0TranslateCompatibilityRow,
    profile_h0_translate_value_compatibility,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    classify_claim,
    profile_x1_8112_bridge_theorem_intake,
)


@dataclass(frozen=True)
class H0TranslateX16RouteRow:
    name: str
    source_row_name: str
    odd_payload_object: str
    multiplier_from_canonical: int
    legal_translate_product: bool
    source_stage_closed: bool
    x1_claim_executed: bool
    blocked_before_x1: bool
    expected_decision: str
    actual_decision: str
    expected_missing_clause: str
    actual_missing_clause: str
    odd_target_identified: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class H0TranslateX16RoutePropagationPacket:
    h0_translate_compatibility_ok: bool
    x1_8112_intake_ok: bool
    legal_translate_input_rows: int
    noncanonical_legal_translate_rows: int
    canonical_legal_rows: int
    support_period: int
    route_rows: tuple[H0TranslateX16RouteRow, ...]
    row_count: int
    x1_executed_rows: int
    blocked_before_x1_rows: int
    upstream_only_rows: int
    cross_level_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    formal_or_nonlegal_blocked_rows: int
    row_ok: bool


def x1_claim(
    name: str,
    odd_payload_object: str,
    *,
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3: bool = False,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=name,
        theorem_body_verified=True,
        odd_payload_object=odd_payload_object,
        exact_p25_specialization=True,
        odd_level_value_or_divisor=True,
        fiber_product_or_modular_correspondence=fiber_product,
        preserves_j_gluing=j_gluing,
        x16_surface_relation=x16_relation,
        emits_x16_y=emit_y,
        emits_model_root_or_xp16=emit_model_root_xp16,
        emits_halving_chain_or_x0=emit_x0,
        danger3_framing=danger3,
        concrete_vpp_verified_triple=False,
    )


def executed_route_row(
    *,
    name: str,
    source_row: H0TranslateCompatibilityRow,
    claim: X18112BridgeTheoremClaim,
    expected_decision: str,
    expected_missing: str,
) -> H0TranslateX16RouteRow:
    decision = classify_claim(claim)
    return H0TranslateX16RouteRow(
        name=name,
        source_row_name=source_row.name,
        odd_payload_object=claim.odd_payload_object,
        multiplier_from_canonical=source_row.multiplier_from_canonical,
        legal_translate_product=source_row.legal_translate_product,
        source_stage_closed=source_row.source_stage_closed,
        x1_claim_executed=True,
        blocked_before_x1=False,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_clause=expected_missing,
        actual_missing_clause=decision.first_missing_clause,
        odd_target_identified=decision.odd_target_identified,
        cross_level_bridge_identified=decision.cross_level_bridge_identified,
        x16_surface_reached=decision.x16_surface_reached,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        ok=(
            source_row.legal_translate_product
            and source_row.source_stage_closed
            and decision.decision == expected_decision
            and decision.first_missing_clause == expected_missing
        ),
    )


def blocked_route_row(
    *,
    name: str,
    source_row: H0TranslateCompatibilityRow,
) -> H0TranslateX16RouteRow:
    return H0TranslateX16RouteRow(
        name=name,
        source_row_name=source_row.name,
        odd_payload_object=source_row.target_object,
        multiplier_from_canonical=source_row.multiplier_from_canonical,
        legal_translate_product=source_row.legal_translate_product,
        source_stage_closed=source_row.source_stage_closed,
        x1_claim_executed=False,
        blocked_before_x1=True,
        expected_decision="blocked_by_h0_translate_compatibility",
        actual_decision="blocked_by_h0_translate_compatibility",
        expected_missing_clause=source_row.actual_missing_clause,
        actual_missing_clause=source_row.actual_missing_clause,
        odd_target_identified=False,
        cross_level_bridge_identified=False,
        x16_surface_reached=False,
        extraction_ready=False,
        submission_ready=False,
        ok=source_row.rejected and not source_row.legal_translate_product and not source_row.source_stage_closed,
    )


def route_rows(
    legal_rows: tuple[H0TranslateCompatibilityRow, ...],
    nonlegal_row: H0TranslateCompatibilityRow,
    formal_row: H0TranslateCompatibilityRow,
) -> tuple[H0TranslateX16RouteRow, ...]:
    representative_translate = next(
        row
        for row in legal_rows
        if row.target_object == "H0_translate" and row.multiplier_from_canonical == 2
    )
    rows: list[H0TranslateX16RouteRow] = []
    for source_row in legal_rows:
        rows.append(
            executed_route_row(
                name=f"{source_row.name}_no_cross_level",
                source_row=source_row,
                claim=x1_claim(
                    f"{source_row.name}_no_cross_level",
                    source_row.target_object,
                ),
                expected_decision="upstream_odd_value_no_cross_level_bridge",
                expected_missing="X_1(16) relation or X_1(8112) fiber-product theorem",
            )
        )

    rows.extend(
        (
            executed_route_row(
                name="legal_h0_translate_m2_x18112_bridge_no_x16_specialization",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x18112_bridge_no_x16_specialization",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                ),
                expected_decision="cross_level_target_identified_specialization_missing",
                expected_missing="specialized relation yielding X_1(16) y, A, xP16, or x0",
            ),
            executed_route_row(
                name="legal_h0_translate_m2_x16_relation_without_y",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x16_relation_without_y",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                    x16_relation=True,
                ),
                expected_decision="conditional_x16_relation_without_y",
                expected_missing="actual X_1(16) parameter y",
            ),
            executed_route_row(
                name="legal_h0_translate_m2_x16_y_without_montgomery_surface",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x16_y_without_montgomery_surface",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                    x16_relation=True,
                    emit_y=True,
                ),
                expected_decision="conditional_y_without_montgomery_surface",
                expected_missing="model root x, Montgomery A, and marked xP16",
            ),
            executed_route_row(
                name="legal_h0_translate_m2_x16_surface_policy_missing",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x16_surface_policy_missing",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                    x16_relation=True,
                    emit_y=True,
                    emit_model_root_xp16=True,
                ),
                expected_decision="cross_level_surface_policy_or_framing_missing",
                expected_missing="DANGER3 finite-identity/non-CM framing",
            ),
            executed_route_row(
                name="legal_h0_translate_m2_x16_surface_halving_missing",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x16_surface_halving_missing",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                    x16_relation=True,
                    emit_y=True,
                    emit_model_root_xp16=True,
                    danger3=True,
                ),
                expected_decision="x16_surface_reached_halving_or_vpp_missing",
                expected_missing="valid halving chain from xP16 to concrete x0",
            ),
            executed_route_row(
                name="legal_h0_translate_m2_x0_payload_vpp_missing",
                source_row=representative_translate,
                claim=x1_claim(
                    "legal_h0_translate_m2_x0_payload_vpp_missing",
                    "H0_translate",
                    fiber_product=True,
                    j_gluing=True,
                    x16_relation=True,
                    emit_y=True,
                    emit_model_root_xp16=True,
                    emit_x0=True,
                    danger3=True,
                ),
                expected_decision="extraction_ready_vpp_missing",
                expected_missing="official vpp.py verification",
            ),
            blocked_route_row(
                name="nonlegal_h0_translate_blocked_before_x1",
                source_row=nonlegal_row,
            ),
            blocked_route_row(
                name="formal_one_coset_h_blocked_before_x1",
                source_row=formal_row,
            ),
        )
    )
    return tuple(rows)


def profile_h0_translate_x16_route_propagation() -> H0TranslateX16RoutePropagationPacket:
    translate = profile_h0_translate_value_compatibility()
    x1 = profile_x1_8112_bridge_theorem_intake()
    legal_rows = tuple(row for row in translate.compatibility_rows if row.legal_translate_product)
    nonlegal_row = next(row for row in translate.compatibility_rows if row.name == "nonlegal_h0_translate_payload")
    formal_row = next(row for row in translate.compatibility_rows if row.name == "formal_one_coset_h_translate")
    rows = route_rows(legal_rows, nonlegal_row, formal_row)
    x1_executed = sum(row.x1_claim_executed for row in rows)
    blocked = sum(row.blocked_before_x1 for row in rows)
    upstream = sum(row.actual_decision == "upstream_odd_value_no_cross_level_bridge" for row in rows)
    cross = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    formal_or_nonlegal_blocked = sum(
        row.blocked_before_x1
        and row.source_row_name in {"nonlegal_h0_translate_payload", "formal_one_coset_h_translate"}
        for row in rows
    )
    row_ok = (
        translate.row_ok
        and x1.row_ok
        and translate.support_period == 156
        and len(legal_rows) == 4
        and sum(row.target_object == "canonical_H0" for row in legal_rows) == 1
        and sum(row.target_object == "H0_translate" for row in legal_rows) == 3
        and all(row.source_stage_closed for row in legal_rows)
        and all(row.boundary_equals_period_norm for row in legal_rows)
        and len(rows) == 12
        and x1_executed == 10
        and blocked == 2
        and upstream == 4
        and cross == 6
        and x16 == 3
        and extraction_ready == 1
        and submission == 0
        and formal_or_nonlegal_blocked == 2
        and all(row.ok for row in rows)
    )
    return H0TranslateX16RoutePropagationPacket(
        h0_translate_compatibility_ok=translate.row_ok,
        x1_8112_intake_ok=x1.row_ok,
        legal_translate_input_rows=len(legal_rows),
        noncanonical_legal_translate_rows=sum(row.target_object == "H0_translate" for row in legal_rows),
        canonical_legal_rows=sum(row.target_object == "canonical_H0" for row in legal_rows),
        support_period=translate.support_period,
        route_rows=rows,
        row_count=len(rows),
        x1_executed_rows=x1_executed,
        blocked_before_x1_rows=blocked,
        upstream_only_rows=upstream,
        cross_level_rows=cross,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission,
        formal_or_nonlegal_blocked_rows=formal_or_nonlegal_blocked,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_x16_route_propagation()
    print("p25 KSY-y H0 translate X1(16) route-propagation gate")
    print("dependencies")
    print(f"  h0_translate_compatibility_ok={int(profile.h0_translate_compatibility_ok)}")
    print(f"  x1_8112_intake_ok={int(profile.x1_8112_intake_ok)}")
    print("legal_inputs")
    print(f"  support_period={profile.support_period}")
    print(f"  legal_translate_input_rows={profile.legal_translate_input_rows}")
    print(f"  canonical_legal_rows={profile.canonical_legal_rows}")
    print(f"  noncanonical_legal_translate_rows={profile.noncanonical_legal_translate_rows}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: source={row.source_row_name} odd={row.odd_payload_object} "
            f"multiplier={row.multiplier_from_canonical} legal={int(row.legal_translate_product)} "
            f"source_closed={int(row.source_stage_closed)} x1={int(row.x1_claim_executed)} "
            f"blocked={int(row.blocked_before_x1)} decision={row.actual_decision} "
            f"odd_target={int(row.odd_target_identified)} cross={int(row.cross_level_bridge_identified)} "
            f"x16={int(row.x16_surface_reached)} extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} missing={row.actual_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  x1_executed_rows={profile.x1_executed_rows}")
    print(f"  blocked_before_x1_rows={profile.blocked_before_x1_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  cross_level_rows={profile.cross_level_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  formal_or_nonlegal_blocked_rows={profile.formal_or_nonlegal_blocked_rows}")
    print("interpretation")
    print("  every_legal_H0_product_has_the_same_X1_8112_route_contract=1")
    print("  noncanonical_H0_translate_m2_exercises_the_full_X1_16_ladder=1")
    print("  nonlegal_or_formal_H_objects_are_blocked_before_X1_routing=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_x16_route_propagation_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate X1(16) route-propagation regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
