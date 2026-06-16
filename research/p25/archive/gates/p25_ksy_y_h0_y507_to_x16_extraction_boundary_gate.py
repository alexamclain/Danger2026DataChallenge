#!/usr/bin/env python3
"""H0/Y507 to X_1(16) extraction-boundary smoke packet.

The H0/Y507 compatibility gate says which odd-level value/divisor claims close
the source stage.  This gate says what those claims still need before they
become DANGER3 extraction progress: an X_1(8112) cross-level bridge, an
X_1(16) Montgomery surface, a halving chain or x0, and official vpp.py.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_period156_value_compatibility_gate import (
    profile_h0_period156_value_compatibility,
)
from p25_ksy_y_x1_16_halving_certificate_payload_gate import (
    profile_halving_certificate_payload_contract,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    classify_claim,
    profile_x1_8112_bridge_theorem_intake,
)


@dataclass(frozen=True)
class H0Y507ExtractionBoundaryRow:
    name: str
    odd_payload_object: str
    expected_decision: str
    actual_decision: str
    expected_missing_clause: str
    actual_missing_clause: str
    odd_target_identified: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    executed_now: bool
    placeholder_requires_concrete_values: bool
    ok: bool


@dataclass(frozen=True)
class H0Y507ExtractionBoundaryPacket:
    h0_period156_compatibility_ok: bool
    x1_8112_intake_ok: bool
    halving_payload_ok: bool
    halving_links: int
    x_chain_points: int
    vpp_doublings: int
    boundary_rows: tuple[H0Y507ExtractionBoundaryRow, ...]
    row_count: int
    executed_rows: int
    placeholder_rows: int
    upstream_only_rows: int
    rejected_rows: int
    cross_level_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def claim(
    name: str,
    *,
    odd_payload_object: str = "canonical_H0",
    exact_p25: bool = True,
    odd_value_or_divisor: bool = True,
    fiber_product: bool = False,
    j_gluing: bool = False,
    x16_relation: bool = False,
    emit_y: bool = False,
    emit_model_root_xp16: bool = False,
    emit_x0: bool = False,
    danger3: bool = False,
    vpp: bool = False,
) -> X18112BridgeTheoremClaim:
    return X18112BridgeTheoremClaim(
        name=name,
        theorem_body_verified=True,
        odd_payload_object=odd_payload_object,
        exact_p25_specialization=exact_p25,
        odd_level_value_or_divisor=odd_value_or_divisor,
        fiber_product_or_modular_correspondence=fiber_product,
        preserves_j_gluing=j_gluing,
        x16_surface_relation=x16_relation,
        emits_x16_y=emit_y,
        emits_model_root_or_xp16=emit_model_root_xp16,
        emits_halving_chain_or_x0=emit_x0,
        danger3_framing=danger3,
        concrete_vpp_verified_triple=vpp,
    )


def executed_row(
    *,
    name: str,
    theorem_claim: X18112BridgeTheoremClaim,
    expected_decision: str,
    expected_missing: str,
) -> H0Y507ExtractionBoundaryRow:
    decision = classify_claim(theorem_claim)
    return H0Y507ExtractionBoundaryRow(
        name=name,
        odd_payload_object=theorem_claim.odd_payload_object,
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        expected_missing_clause=expected_missing,
        actual_missing_clause=decision.first_missing_clause,
        odd_target_identified=decision.odd_target_identified,
        cross_level_bridge_identified=decision.cross_level_bridge_identified,
        x16_surface_reached=decision.x16_surface_reached,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        executed_now=True,
        placeholder_requires_concrete_values=False,
        ok=decision.decision == expected_decision and decision.first_missing_clause == expected_missing,
    )


def boundary_rows() -> tuple[H0Y507ExtractionBoundaryRow, ...]:
    return (
        executed_row(
            name="canonical_h0_source_closed_no_cross_level",
            theorem_claim=claim("canonical_h0_source_closed_no_cross_level"),
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            expected_missing="X_1(16) relation or X_1(8112) fiber-product theorem",
        ),
        executed_row(
            name="y507_source_closed_no_cross_level",
            theorem_claim=claim(
                "y507_source_closed_no_cross_level",
                odd_payload_object="Y_507",
            ),
            expected_decision="upstream_odd_value_no_cross_level_bridge",
            expected_missing="X_1(16) relation or X_1(8112) fiber-product theorem",
        ),
        executed_row(
            name="generic_x16_surface_without_odd_payload",
            theorem_claim=claim(
                "generic_x16_surface_without_odd_payload",
                odd_value_or_divisor=False,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
            ),
            expected_decision="reject_generic_x16_not_ksy_bridge",
            expected_missing="odd-level KSY/Yang/H90 value or divisor payload",
        ),
        executed_row(
            name="unglued_h0_level16_level507_statements",
            theorem_claim=claim(
                "unglued_h0_level16_level507_statements",
                fiber_product=True,
                j_gluing=False,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
            ),
            expected_decision="reject_unvalidated_fiber_product_gluing",
            expected_missing="fiber product over the same j-invariant",
        ),
        executed_row(
            name="h0_x18112_bridge_no_x16_specialization",
            theorem_claim=claim(
                "h0_x18112_bridge_no_x16_specialization",
                fiber_product=True,
                j_gluing=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            expected_missing="specialized relation yielding X_1(16) y, A, xP16, or x0",
        ),
        executed_row(
            name="h0_x16_relation_without_y",
            theorem_claim=claim(
                "h0_x16_relation_without_y",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
            ),
            expected_decision="conditional_x16_relation_without_y",
            expected_missing="actual X_1(16) parameter y",
        ),
        executed_row(
            name="h0_x16_y_without_montgomery_surface",
            theorem_claim=claim(
                "h0_x16_y_without_montgomery_surface",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
            ),
            expected_decision="conditional_y_without_montgomery_surface",
            expected_missing="model root x, Montgomery A, and marked xP16",
        ),
        executed_row(
            name="h0_x16_surface_policy_missing",
            theorem_claim=claim(
                "h0_x16_surface_policy_missing",
                fiber_product=True,
                j_gluing=True,
                x16_relation=True,
                emit_y=True,
                emit_model_root_xp16=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            expected_missing="DANGER3 finite-identity/non-CM framing",
        ),
        executed_row(
            name="h0_x16_surface_halving_missing",
            theorem_claim=claim(
                "h0_x16_surface_halving_missing",
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
        executed_row(
            name="h0_x0_payload_vpp_missing",
            theorem_claim=claim(
                "h0_x0_payload_vpp_missing",
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
        H0Y507ExtractionBoundaryRow(
            name="verified_pomerance_triple_requires_real_values",
            odd_payload_object="p25_(A,x0)",
            expected_decision="not_smoked_without_concrete_A_x0",
            actual_decision="not_smoked_without_concrete_A_x0",
            expected_missing_clause="official vpp.py verification",
            actual_missing_clause="official vpp.py verification",
            odd_target_identified=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            executed_now=False,
            placeholder_requires_concrete_values=True,
            ok=True,
        ),
    )


def profile_h0_y507_to_x16_extraction_boundary() -> H0Y507ExtractionBoundaryPacket:
    h0 = profile_h0_period156_value_compatibility()
    x1 = profile_x1_8112_bridge_theorem_intake()
    halving = profile_halving_certificate_payload_contract()
    rows = boundary_rows()
    executed = sum(row.executed_now for row in rows)
    placeholders = sum(row.placeholder_requires_concrete_values for row in rows)
    upstream = sum(row.actual_decision == "upstream_odd_value_no_cross_level_bridge" for row in rows)
    rejected = sum(row.actual_decision.startswith("reject_") for row in rows)
    cross = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    row_ok = (
        h0.row_ok
        and x1.row_ok
        and halving.row_ok
        and halving.halving_links == 38
        and halving.x_chain_points == 39
        and halving.vpp_doublings == 42
        and len(rows) == 11
        and executed == 10
        and placeholders == 1
        and upstream == 2
        and rejected == 2
        and cross == 6
        and x16 == 3
        and extraction == 1
        and submission == 0
        and all(row.ok for row in rows)
    )
    return H0Y507ExtractionBoundaryPacket(
        h0_period156_compatibility_ok=h0.row_ok,
        x1_8112_intake_ok=x1.row_ok,
        halving_payload_ok=halving.row_ok,
        halving_links=halving.halving_links,
        x_chain_points=halving.x_chain_points,
        vpp_doublings=halving.vpp_doublings,
        boundary_rows=rows,
        row_count=len(rows),
        executed_rows=executed,
        placeholder_rows=placeholders,
        upstream_only_rows=upstream,
        rejected_rows=rejected,
        cross_level_rows=cross,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_y507_to_x16_extraction_boundary()
    print("p25 KSY-y H0/Y507 to X1(16) extraction-boundary gate")
    print("dependencies")
    print(f"  h0_period156_compatibility_ok={int(profile.h0_period156_compatibility_ok)}")
    print(f"  x1_8112_intake_ok={int(profile.x1_8112_intake_ok)}")
    print(f"  halving_payload_ok={int(profile.halving_payload_ok)}")
    print("halving_shape")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print(f"  vpp_doublings={profile.vpp_doublings}")
    print("boundary_rows")
    for row in profile.boundary_rows:
        print(
            "  "
            f"{row.name}: odd={row.odd_payload_object} expected={row.expected_decision} "
            f"actual={row.actual_decision} odd_target={int(row.odd_target_identified)} "
            f"cross={int(row.cross_level_bridge_identified)} "
            f"x16={int(row.x16_surface_reached)} "
            f"extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} "
            f"executed={int(row.executed_now)} placeholder={int(row.placeholder_requires_concrete_values)}"
        )
        print(f"    missing={row.actual_missing_clause}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  executed_rows={profile.executed_rows}")
    print(f"  placeholder_rows={profile.placeholder_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  cross_level_rows={profile.cross_level_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  H0_Y507_source_closure_is_upstream_until_X1_8112_bridge_exists=1")
    print("  X1_16_surface_still_needs_DANGER3_framing_and_halving_or_x0=1")
    print("  verified_triple_row_is_not_smoked_without_concrete_values=1")
    print(f"ksy_y_h0_y507_to_x16_extraction_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0/Y507 to X1(16) extraction-boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
