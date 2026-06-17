#!/usr/bin/env python3
"""H0-specific X_1(8112) bridge payload contract.

The H0 source-to-DANGER3 handoff says that a source-closed H0 theorem still
needs a same-j cross-level bridge.  This gate states the constructive payload
for that bridge: either same-curve exact 16- and 507-torsion components, or an
order-8112 generator whose normalized projections recover the practical
X_1(16) component and the odd H0 component.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm
from pathlib import Path

from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    classify_claim,
)


P25 = 10**25 + 13
X16_LEVEL = 16
ODD_LEVEL = 507
CROSS_LEVEL = 8112
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class BridgeProjectionRow:
    name: str
    multiplier: int
    exact_order: int
    normalized: bool
    role: str
    ok: bool


@dataclass(frozen=True)
class H0X18112BridgePayloadRow:
    name: str
    payload_shape: str
    x1_classifier_executed: bool
    has_h0_source_payload: bool
    has_same_curve_p16: bool
    has_same_curve_q507: bool
    has_same_j_or_curve: bool
    order8112_constructible: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class H0X18112BridgePayloadContract:
    h0_handoff_marker_present: bool
    torsion_gluing_marker_present: bool
    montgomery_chart_marker_present: bool
    halving_payload_marker_present: bool
    levels_are_coprime: bool
    inv_507_mod_16: int
    inv_16_mod_507: int
    normalized_p16_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    projection_rows: tuple[BridgeProjectionRow, ...]
    bridge_rows: tuple[H0X18112BridgePayloadRow, ...]
    row_count: int
    projection_rows_ok: int
    x1_classifier_rows: int
    rejected_rows: int
    same_j_bridge_rows: int
    order8112_constructible_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    if not path.exists() and path.parent == RESEARCH:
        path = RESEARCH / "archive" / "notes" / path.name
    return artifact_present(path) and marker in path.read_text()


def order_of_multiple(order: int, multiplier: int) -> int:
    return order // gcd(order, multiplier)


def projection_rows() -> tuple[BridgeProjectionRow, ...]:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    raw_p16 = ODD_LEVEL
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    raw_q507 = X16_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    return (
        BridgeProjectionRow(
            name="raw_p16_projection",
            multiplier=raw_p16,
            exact_order=order_of_multiple(CROSS_LEVEL, raw_p16),
            normalized=False,
            role="[507]R has exact order 16 but is scaled by 507 mod 16",
            ok=order_of_multiple(CROSS_LEVEL, raw_p16) == X16_LEVEL,
        ),
        BridgeProjectionRow(
            name="normalized_p16_projection",
            multiplier=normalized_p16,
            exact_order=order_of_multiple(CROSS_LEVEL, normalized_p16),
            normalized=True,
            role="P16=[3*507]R=[1521]R",
            ok=normalized_p16 == 1521 and order_of_multiple(CROSS_LEVEL, normalized_p16) == X16_LEVEL,
        ),
        BridgeProjectionRow(
            name="raw_q507_projection",
            multiplier=raw_q507,
            exact_order=order_of_multiple(CROSS_LEVEL, raw_q507),
            normalized=False,
            role="[16]R has exact order 507 but is scaled by 16 mod 507",
            ok=order_of_multiple(CROSS_LEVEL, raw_q507) == ODD_LEVEL,
        ),
        BridgeProjectionRow(
            name="normalized_q507_projection",
            multiplier=normalized_q507,
            exact_order=order_of_multiple(CROSS_LEVEL, normalized_q507),
            normalized=True,
            role="Q507=[412*16]R=[6592]R",
            ok=normalized_q507 == 6592 and order_of_multiple(CROSS_LEVEL, normalized_q507) == ODD_LEVEL,
        ),
    )


def x1_claim(
    name: str,
    *,
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3: bool = False,
    concrete_vpp: bool = False,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=name,
        theorem_body_verified=True,
        odd_payload_object="H0_translate",
        exact_p25_specialization=True,
        odd_level_value_or_divisor=True,
        fiber_product_or_modular_correspondence=fiber_product,
        preserves_j_gluing=j_gluing,
        x16_surface_relation=x16_relation,
        emits_x16_y=emit_y,
        emits_model_root_or_xp16=emit_model_root_xp16,
        emits_halving_chain_or_x0=emit_x0,
        danger3_framing=danger3,
        concrete_vpp_verified_triple=concrete_vpp,
    )


def classified_row(
    *,
    name: str,
    payload_shape: str,
    claim: X18112BridgeTheoremClaim,
    expected_decision: str,
    expected_missing: str,
    has_same_curve_p16: bool,
    has_same_curve_q507: bool,
    has_same_j_or_curve: bool,
    order8112_constructible: bool,
) -> H0X18112BridgePayloadRow:
    decision = classify_claim(claim)
    return H0X18112BridgePayloadRow(
        name=name,
        payload_shape=payload_shape,
        x1_classifier_executed=True,
        has_h0_source_payload=True,
        has_same_curve_p16=has_same_curve_p16,
        has_same_curve_q507=has_same_curve_q507,
        has_same_j_or_curve=has_same_j_or_curve,
        order8112_constructible=order8112_constructible,
        x16_surface_reached=decision.x16_surface_reached,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        decision=decision.decision,
        first_missing_clause=decision.first_missing_clause,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def static_row(
    *,
    name: str,
    payload_shape: str,
    has_h0_source_payload: bool,
    has_same_curve_p16: bool,
    has_same_curve_q507: bool,
    has_same_j_or_curve: bool,
    order8112_constructible: bool,
    decision: str,
    first_missing_clause: str,
) -> H0X18112BridgePayloadRow:
    return H0X18112BridgePayloadRow(
        name=name,
        payload_shape=payload_shape,
        x1_classifier_executed=False,
        has_h0_source_payload=has_h0_source_payload,
        has_same_curve_p16=has_same_curve_p16,
        has_same_curve_q507=has_same_curve_q507,
        has_same_j_or_curve=has_same_j_or_curve,
        order8112_constructible=order8112_constructible,
        x16_surface_reached=False,
        extraction_ready=False,
        submission_ready=False,
        decision=decision,
        first_missing_clause=first_missing_clause,
        ok=True,
    )


def bridge_rows() -> tuple[H0X18112BridgePayloadRow, ...]:
    return (
        classified_row(
            name="h0_source_closed_no_same_curve_bridge",
            payload_shape="source-closed H0 theorem with no level-16 or order-8112 payload",
            claim=x1_claim("h0_source_closed_no_same_curve_bridge"),
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            expected_missing="X_1(16) relation or X_1(8112) fiber-product theorem",
            has_same_curve_p16=False,
            has_same_curve_q507=True,
            has_same_j_or_curve=False,
            order8112_constructible=False,
        ),
        static_row(
            name="independent_p16_and_q507_data",
            payload_shape="separate level-16 and H0/507 data with no same-j proof",
            has_h0_source_payload=True,
            has_same_curve_p16=False,
            has_same_curve_q507=True,
            has_same_j_or_curve=False,
            order8112_constructible=False,
            decision="reject_unglued_components",
            first_missing_clause="same j-invariant or same elliptic curve",
        ),
        static_row(
            name="same_curve_p16_q507_pair",
            payload_shape="same-curve exact P16 and H0-tied Q507 components",
            has_h0_source_payload=True,
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
            decision="construct_order_8112_generator_then_specialize_x16",
            first_missing_clause="practical y, model root, A, and xP16 extraction data",
        ),
        classified_row(
            name="order8112_generator_no_x16_specialization",
            payload_shape="same-j order-8112 bridge R tied to H0, without X_1(16) specialization",
            claim=x1_claim(
                "order8112_generator_no_x16_specialization",
                fiber_product=True,
                j_gluing=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            expected_missing="specialized relation yielding X_1(16) y, A, xP16, or x0",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="order8112_x16_relation_without_y",
            payload_shape="order-8112 bridge plus abstract X_1(16) relation",
            claim=x1_claim(
                "order8112_x16_relation_without_y",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
            ),
            expected_decision="conditional_x16_relation_without_y",
            expected_missing="actual X_1(16) parameter y",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="order8112_x16_y_without_montgomery_surface",
            payload_shape="order-8112 bridge plus X_1(16) y but no model root/A/xP16",
            claim=x1_claim(
                "order8112_x16_y_without_montgomery_surface",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
            ),
            expected_decision="conditional_y_without_montgomery_surface",
            expected_missing="model root x, Montgomery A, and marked xP16",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="order8112_x16_surface_policy_missing",
            payload_shape="order-8112 bridge plus X_1(16) y, model root, A, and xP16",
            claim=x1_claim(
                "order8112_x16_surface_policy_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="order8112_x16_surface_halving_missing",
            payload_shape="DANGER3-framed order-8112 bridge plus X_1(16) surface",
            claim=x1_claim(
                "order8112_x16_surface_halving_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
                danger3=True,
            ),
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            expected_missing="valid halving chain from xP16 to concrete x0",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="order8112_x0_payload_vpp_missing",
            payload_shape="DANGER3-framed order-8112 bridge with concrete A and x0",
            claim=x1_claim(
                "order8112_x0_payload_vpp_missing",
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
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
        classified_row(
            name="verified_pomerance_triple",
            payload_shape="concrete p25 (p,A,x0) verified by official vpp.py",
            claim=x1_claim("verified_pomerance_triple", concrete_vpp=True),
            expected_decision="submission_ready_verified_triple",
            expected_missing="none",
            has_same_curve_p16=True,
            has_same_curve_q507=True,
            has_same_j_or_curve=True,
            order8112_constructible=True,
        ),
    )


def profile_h0_x18112_bridge_payload_contract() -> H0X18112BridgePayloadContract:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    projection_sum = (normalized_p16 + normalized_q507) % CROSS_LEVEL
    projections = projection_rows()
    rows = bridge_rows()
    handoff_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_source_to_danger3_handoff_20260614.md",
        "ksy_y_h0_source_to_danger3_handoff_rows=1/1",
    )
    torsion_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_8112_torsion_gluing_contract_20260614.md",
        "ksy_y_x1_8112_torsion_gluing_contract_rows=1/1",
    )
    montgomery_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    )
    halving_marker = marker_present(
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    )
    x1_classifier = sum(row.x1_classifier_executed for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    same_j = sum(row.has_same_j_or_curve for row in rows)
    order8112 = sum(row.order8112_constructible for row in rows)
    x16_surface = sum(row.x16_surface_reached for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    row_ok = (
        handoff_marker
        and torsion_marker
        and montgomery_marker
        and halving_marker
        and P25 == 10**25 + 13
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CROSS_LEVEL == 8112
        and lcm(X16_LEVEL, ODD_LEVEL) == CROSS_LEVEL
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and inv_507 == 3
        and inv_16 == 412
        and normalized_p16 == 1521
        and normalized_q507 == 6592
        and projection_sum == 1
        and len(projections) == 4
        and sum(row.ok for row in projections) == 4
        and len(rows) == 10
        and x1_classifier == 8
        and rejected == 1
        and same_j == 8
        and order8112 == 8
        and x16_surface == 4
        and extraction_ready == 2
        and submission_ready == 1
        and tuple(row.decision for row in rows)
        == (
            "upstream_odd_value_no_cross_level_bridge",
            "reject_unglued_components",
            "construct_order_8112_generator_then_specialize_x16",
            "cross_level_target_identified_specialization_missing",
            "conditional_x16_relation_without_y",
            "conditional_y_without_montgomery_surface",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready_verified_triple",
        )
        and all(row.ok for row in rows)
    )
    return H0X18112BridgePayloadContract(
        h0_handoff_marker_present=handoff_marker,
        torsion_gluing_marker_present=torsion_marker,
        montgomery_chart_marker_present=montgomery_marker,
        halving_payload_marker_present=halving_marker,
        levels_are_coprime=gcd(X16_LEVEL, ODD_LEVEL) == 1,
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        normalized_p16_multiplier=normalized_p16,
        normalized_q507_multiplier=normalized_q507,
        normalized_projection_sum_mod_8112=projection_sum,
        projection_rows=projections,
        bridge_rows=rows,
        row_count=len(rows),
        projection_rows_ok=sum(row.ok for row in projections),
        x1_classifier_rows=x1_classifier,
        rejected_rows=rejected,
        same_j_bridge_rows=same_j,
        order8112_constructible_rows=order8112,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_x18112_bridge_payload_contract()
    print("p25 KSY-y H0 X1(8112) bridge payload contract gate")
    print("dependencies")
    print(f"  h0_handoff_marker_present={int(profile.h0_handoff_marker_present)}")
    print(f"  torsion_gluing_marker_present={int(profile.torsion_gluing_marker_present)}")
    print(f"  montgomery_chart_marker_present={int(profile.montgomery_chart_marker_present)}")
    print(f"  halving_payload_marker_present={int(profile.halving_payload_marker_present)}")
    print("projection_arithmetic")
    print(f"  levels_are_coprime={int(profile.levels_are_coprime)}")
    print(f"  inv_507_mod_16={profile.inv_507_mod_16}")
    print(f"  inv_16_mod_507={profile.inv_16_mod_507}")
    print(f"  normalized_p16_multiplier={profile.normalized_p16_multiplier}")
    print(f"  normalized_q507_multiplier={profile.normalized_q507_multiplier}")
    print(f"  normalized_projection_sum_mod_8112={profile.normalized_projection_sum_mod_8112}")
    print("projection_rows")
    for row in profile.projection_rows:
        print(
            "  "
            f"{row.name}: multiplier={row.multiplier} order={row.exact_order} "
            f"normalized={int(row.normalized)} role={row.role}"
        )
    print("bridge_rows")
    for row in profile.bridge_rows:
        print(
            "  "
            f"{row.name}: x1={int(row.x1_classifier_executed)} "
            f"same_j={int(row.has_same_j_or_curve)} "
            f"R8112={int(row.order8112_constructible)} "
            f"x16={int(row.x16_surface_reached)} extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} decision={row.decision} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    payload={row.payload_shape}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  projection_rows_ok={profile.projection_rows_ok}")
    print(f"  x1_classifier_rows={profile.x1_classifier_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  order8112_constructible_rows={profile.order8112_constructible_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  same_curve_P16_Q507_or_order8112_R_is_the_required_bridge_payload=1")
    print("  independent_level16_and_level507_data_is_rejected_without_same_j_gluing=1")
    print("  order8112_bridge_still_must_specialize_to_the_practical_X1_16_chart=1")
    print("  only_vpp_verified_pomerance_triple_is_submission_ready=1")
    print(f"ksy_y_h0_x18112_bridge_payload_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 X1(8112) bridge payload contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
