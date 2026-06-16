#!/usr/bin/env python3
"""Route-level certificate stack for the conductor-39 p25 source.

Recent Koo-Shin 2010 refinements changed the status of the conductor-39 lane:
the small source object is no longer just a formal character word.  It has a
stack of independent certificates:

* Yang/Yu legality and primitive U_chi structure;
* mixed chi_3 tensor chi_13 non-projection structure;
* Koo-Shin 6.2 one-axis X_1(39) product certification;
* Koo-Shin 9.x guardrails against ray-class generator false positives;
* Yang's 13-fiber lift to the level-507 period norm.

This gate records that the source side is certified, while the finite-field
value/divisor theorem, cross-level X_1(16) extraction, halving payload, and
official vpp.py verification remain missing.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_koo_shin_2010_ray_class_generator_guardrail_gate import (
    profile_koo_shin_ray_class_generator_guardrail,
)
from p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_gate import (
    profile_koo_shin_theorem62_conductor39_unit,
)
from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    profile_yang_y507_conductor39_distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate import (
    profile_yang_y507_conductor39_mixed_tensor_character,
)
from p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate import (
    profile_yang_y507_conductor39_modular_unit_legality,
)
from p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate import (
    profile_yang_y507_conductor39_primitive_character_unit,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)


@dataclass(frozen=True)
class SourceCertificateRow:
    name: str
    certificate_type: str
    evidence: str
    certified: bool
    direct_value_theorem: bool
    extraction_ready: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class SourceStackRouteRow:
    name: str
    decision: str
    source_certified: bool
    value_or_divisor_theorem_ready: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class Conductor39SourceCertificateStack:
    primitive_unit_ok: bool
    mixed_tensor_ok: bool
    modular_unit_legality_ok: bool
    koo_shin_62_ok: bool
    koo_shin_9x_guardrail_ok: bool
    distribution_lift_ok: bool
    sparse_h90_normal_form_ok: bool
    certificate_rows: tuple[SourceCertificateRow, ...]
    route_rows: tuple[SourceStackRouteRow, ...]
    source_certified_rows: int
    direct_value_theorem_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_direct_rows: int
    conditional_rows: int
    positive_payload: str
    remaining_upgrade: str
    row_ok: bool


def certificate_rows(
    primitive,
    mixed,
    legality,
    ks62,
    ks9,
    lift,
    h90,
) -> tuple[SourceCertificateRow, ...]:
    return (
        SourceCertificateRow(
            name="primitive_unit",
            certificate_type="legal_mixed_unit",
            evidence="U_chi=-chi_39 is legal and has support 24 with +/-1 coefficients",
            certified=primitive.row_ok and legality.legal_rows == 2,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="finite-field value/divisor theorem",
            ok=primitive.row_ok and legality.row_ok,
        ),
        SourceCertificateRow(
            name="mixed_tensor_nonprojection",
            certificate_type="projection_guard",
            evidence="proper pushforwards vanish and pullbacks to mod 3 or mod 13 fail",
            certified=mixed.row_ok and mixed.proper_pushforwards_vanish,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="finite-field value/divisor theorem",
            ok=mixed.row_ok and mixed.proper_pushforwards_vanish,
        ),
        SourceCertificateRow(
            name="koo_shin_62_source_product",
            certificate_type="one_axis_source_certificate",
            evidence="U_chi, V_bal, and W satisfy Koo-Shin 6.2 congruences at N=39",
            certified=ks62.row_ok and ks62.theorem62_congruence_rows == 3,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="finite-field value/divisor theorem and Yang/H90 descent",
            ok=ks62.row_ok and ks62.direct_product_closer_rows == 0,
        ),
        SourceCertificateRow(
            name="koo_shin_9x_guardrail",
            certificate_type="ray_class_false_positive_guard",
            evidence="all-unit and single-index ray-class generator shapes are not scaled U_chi",
            certified=ks9.row_ok and ks9.rejected_direct_rows == 3,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="independent mixed-character value/divisor theorem",
            ok=ks9.row_ok and ks9.finite_value_theorem_ready_rows == 0,
        ),
        SourceCertificateRow(
            name="yang_13_fiber_lift",
            certificate_type="level_39_to_507_lift",
            evidence="distribution_lift_39_to_507(6*U_chi) equals Norm_156(Y_507)",
            certified=lift.row_ok and lift.lifted_equals_period_norm,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="the theorem that evaluates or identifies the period norm",
            ok=lift.row_ok and lift.period_norm_support == 312,
        ),
        SourceCertificateRow(
            name="sparse_h90_normal_form",
            certificate_type="period_156_formal_payload",
            evidence="canonical 78-over-78 Yang-fiber product normal form is recorded",
            certified=h90.row_ok and h90.legal_rows_are_78_over_78_products,
            direct_value_theorem=False,
            extraction_ready=False,
            first_missing_clause="Hilbert-90/value theorem and challenge extraction",
            ok=h90.row_ok,
        ),
    )


def route_rows() -> tuple[SourceStackRouteRow, ...]:
    return (
        SourceStackRouteRow(
            name="source_certificate_stack",
            decision="source_certified_value_theorem_missing",
            source_certified=True,
            value_or_divisor_theorem_ready=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value/divisor theorem for the conductor-39 source",
            next_action="seek theorem that evaluates or identifies U_chi/W/Norm_156(Y_507)",
            ok=True,
        ),
        SourceStackRouteRow(
            name="source_certificate_as_product_closer",
            decision="reject_source_certificate_not_exact_75_atom_product",
            source_certified=True,
            value_or_divisor_theorem_ready=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact p25 finite value/divisor identity and 75-atom/extraction bridge",
            next_action="do not equate source legality with the KSY/KL exact product",
            ok=True,
        ),
        SourceStackRouteRow(
            name="source_certificate_as_submission",
            decision="reject_source_certificate_not_danger3_submission",
            source_certified=True,
            value_or_divisor_theorem_ready=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="A,xP16 surface, halving payload, and vpp.py-verified x0",
            next_action="keep DANGER3 extraction as a separate downstream stage",
            ok=True,
        ),
    )


def profile_conductor39_source_certificate_stack() -> Conductor39SourceCertificateStack:
    primitive = profile_yang_y507_conductor39_primitive_character_unit()
    mixed = profile_yang_y507_conductor39_mixed_tensor_character()
    legality = profile_yang_y507_conductor39_modular_unit_legality()
    ks62 = profile_koo_shin_theorem62_conductor39_unit()
    ks9 = profile_koo_shin_ray_class_generator_guardrail()
    lift = profile_yang_y507_conductor39_distribution_lift()
    h90 = profile_sparse_h90_product_normal_form()
    certificates = certificate_rows(primitive, mixed, legality, ks62, ks9, lift, h90)
    routes = route_rows()
    source_certified = sum(row.certified for row in certificates)
    direct_value = sum(row.direct_value_theorem for row in certificates)
    extraction_ready = sum(row.extraction_ready for row in certificates) + sum(
        row.extraction_ready for row in routes
    )
    submission_ready = sum(row.submission_ready for row in routes)
    rejected = sum(row.decision.startswith("reject_") for row in routes)
    conditional = sum("missing" in row.decision for row in routes)
    row_ok = (
        primitive.row_ok
        and mixed.row_ok
        and legality.row_ok
        and ks62.row_ok
        and ks9.row_ok
        and lift.row_ok
        and h90.row_ok
        and len(certificates) == 6
        and source_certified == 6
        and direct_value == 0
        and extraction_ready == 0
        and submission_ready == 0
        and rejected == 2
        and conditional == 1
        and all(row.ok for row in certificates)
        and all(row.ok for row in routes)
    )
    return Conductor39SourceCertificateStack(
        primitive_unit_ok=primitive.row_ok,
        mixed_tensor_ok=mixed.row_ok,
        modular_unit_legality_ok=legality.row_ok,
        koo_shin_62_ok=ks62.row_ok,
        koo_shin_9x_guardrail_ok=ks9.row_ok,
        distribution_lift_ok=lift.row_ok,
        sparse_h90_normal_form_ok=h90.row_ok,
        certificate_rows=certificates,
        route_rows=routes,
        source_certified_rows=source_certified,
        direct_value_theorem_rows=direct_value,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        rejected_direct_rows=rejected,
        conditional_rows=conditional,
        positive_payload=(
            "The conductor-39 source object U_chi/W is certified as a legal, "
            "mixed, non-projection X_1(39) source and lifted to Norm_156(Y_507)."
        ),
        remaining_upgrade=(
            "finite-field value/divisor theorem, DANGER3 framing, X_1(16) "
            "surface, halving payload, and official vpp.py verification"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_conductor39_source_certificate_stack()
    print("p25 KSY-y conductor-39 source certificate stack gate")
    print("inputs")
    print(f"  primitive_unit_ok={int(profile.primitive_unit_ok)}")
    print(f"  mixed_tensor_ok={int(profile.mixed_tensor_ok)}")
    print(f"  modular_unit_legality_ok={int(profile.modular_unit_legality_ok)}")
    print(f"  koo_shin_62_ok={int(profile.koo_shin_62_ok)}")
    print(f"  koo_shin_9x_guardrail_ok={int(profile.koo_shin_9x_guardrail_ok)}")
    print(f"  distribution_lift_ok={int(profile.distribution_lift_ok)}")
    print(f"  sparse_h90_normal_form_ok={int(profile.sparse_h90_normal_form_ok)}")
    print("certificate_rows")
    for row in profile.certificate_rows:
        print(
            "  "
            f"{row.name}: type={row.certificate_type} certified={int(row.certified)} "
            f"value_theorem={int(row.direct_value_theorem)} "
            f"extraction={int(row.extraction_ready)} "
            f"missing={row.first_missing_clause} evidence={row.evidence}"
        )
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} source={int(row.source_certified)} "
            f"value={int(row.value_or_divisor_theorem_ready)} "
            f"danger3={int(row.danger3_unblocked)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  source_certified_rows={profile.source_certified_rows}")
    print(f"  direct_value_theorem_rows={profile.direct_value_theorem_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_direct_rows={profile.rejected_direct_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  conductor39_source_certificate_stack_is_complete=1")
    print("  source_certificate_is_not_value_theorem_or_submission=1")
    print(f"  remaining_upgrade={profile.remaining_upgrade}")
    print(f"ksy_y_conductor39_source_certificate_stack_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Conductor-39 source certificate stack regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
