#!/usr/bin/env python3
"""Boundary/value ambiguity gate for the legal H0-translate lane.

Koo-Shin 6.2 certifies the legal H0 source products, and the Hilbert-90
boundary identifies their relation to Norm_156(Y_507).  This gate isolates the
remaining value ambiguity: boundary-only data is not a value theorem, ambient
or bare values retain the wrong branch ambiguity, and period-156 or
divisor/additive identities are the two source-closing exits.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_h0_translate_koo_shin62_screen_gate import (
    profile_h0_translate_koo_shin62_screen,
)
from p25_ksy_y_h0_translate_value_compatibility_gate import (
    H0TranslateCompatibilityRow,
    profile_h0_translate_value_compatibility,
)


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780


@dataclass(frozen=True)
class H0TranslateBoundaryValueAmbiguityRow:
    name: str
    input_shape: str
    certified_h0_product_rows: int
    h90_boundary_known: bool
    period: int | None
    root_gcd_fp_star: int | None
    branch_unique_in_fp_star: bool
    ambient_mu11_ambiguity: bool
    requires_degree6_descent: bool
    direct_shortcut_rejected: bool
    finite_value_or_divisor_theorem: bool
    arithmetic_source_theorem: bool
    decision: str
    source_theorem_closes: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class H0TranslateBoundaryValueAmbiguityPacket:
    koo_shin62_screen_ok: bool
    h0_translate_value_compatibility_ok: bool
    degree6_arithmetic_ok: bool
    support_period: int
    ambient_period: int
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    p_order_mod39: int
    primitive_39_roots_first_in_degree6: bool
    sqrt_minus39_in_fp: bool
    exact_h0_products_certified: int
    boundary_norm_rows: int
    ambiguity_rows: tuple[H0TranslateBoundaryValueAmbiguityRow, ...]
    row_count: int
    source_certified_only_rows: int
    ambient_mu11_rows: int
    branch_unique_rows: int
    source_closing_rows: int
    conditional_rows: int
    rejected_shortcut_rows: int
    submission_ready_rows: int
    row_ok: bool


def row_by_name(
    rows: tuple[H0TranslateCompatibilityRow, ...],
    name: str,
) -> H0TranslateCompatibilityRow:
    return next(row for row in rows if row.name == name)


def multiplicative_order_mod(base: int, modulus: int) -> int:
    if gcd(base, modulus) != 1:
        raise ValueError("base must be a unit modulo modulus")
    value = 1
    for exponent in range(1, modulus + 1):
        value = (value * base) % modulus
        if value == 1:
            return exponent
    raise AssertionError("multiplicative order search exceeded modulus")


def legendre_symbol(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    if residue == prime - 1:
        return -1
    return residue


def profile_h0_translate_boundary_value_ambiguity() -> H0TranslateBoundaryValueAmbiguityPacket:
    ks62 = profile_h0_translate_koo_shin62_screen()
    compat = profile_h0_translate_value_compatibility()

    support_root_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_root_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    p_order_mod39 = multiplicative_order_mod(P25 % 39, 39)
    primitive_39_roots_first_in_degree6 = p_order_mod39 == 6
    discriminant_is_nonsquare_mod_p = legendre_symbol(-39, P25) == -1
    degree6_arithmetic_ok = (
        P25 % 39 == 23
        and p_order_mod39 == 6
        and pow(P25, 3, 39) == 38
        and primitive_39_roots_first_in_degree6
        and discriminant_is_nonsquare_mod_p
    )

    missing_period = row_by_name(
        compat.compatibility_rows,
        "h0_translate_value_missing_period156",
    )
    divisor_boundary = row_by_name(
        compat.compatibility_rows,
        "h0_translate_divisor_boundary_no_period_value_branch",
    )
    finite_payload_no_source = row_by_name(
        compat.compatibility_rows,
        "h0_translate_finite_payload_without_source",
    )
    legal_value_rows = tuple(
        row
        for row in compat.compatibility_rows
        if row.legal_translate_product and row.output_kind == "value"
    )

    rows = (
        H0TranslateBoundaryValueAmbiguityRow(
            name="ks62_boundary_only_source_certificate",
            input_shape="four exact legal H0 products plus Hilbert-90 boundary to Norm_156(Y_507)",
            certified_h0_product_rows=ks62.source_certified_rows,
            h90_boundary_known=ks62.boundary_norm_rows == 4,
            period=SUPPORT_PERIOD,
            root_gcd_fp_star=support_root_gcd,
            branch_unique_in_fp_star=support_root_gcd == 1,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=False,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=False,
            arithmetic_source_theorem=False,
            decision="source_certified_value_or_divisor_missing",
            source_theorem_closes=False,
            first_missing_clause="finite-field value/divisor theorem for one exact H0 product",
            ok=(
                ks62.row_ok
                and ks62.source_certified_rows == 4
                and ks62.boundary_norm_rows == 4
                and ks62.source_theorem_closing_rows == 0
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="ambient780_or_bare_h0_value_branch",
            input_shape="finite H0 value stated without support-period-156 branch/root/telescoping context",
            certified_h0_product_rows=ks62.source_certified_rows,
            h90_boundary_known=True,
            period=AMBIENT_PERIOD,
            root_gcd_fp_star=ambient_root_gcd,
            branch_unique_in_fp_star=False,
            ambient_mu11_ambiguity=ambient_root_gcd == 11,
            requires_degree6_descent=False,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=True,
            arithmetic_source_theorem=True,
            decision=missing_period.actual_decision,
            source_theorem_closes=missing_period.source_stage_closed,
            first_missing_clause=missing_period.actual_missing_clause,
            ok=(
                missing_period.ok
                and missing_period.actual_decision == "conditional_missing_period_156_context"
                and ambient_root_gcd == 11
                and not missing_period.source_stage_closed
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="support156_h0_value_branch",
            input_shape="exact finite H0 value for one legal product with support-period-156 context",
            certified_h0_product_rows=len(legal_value_rows),
            h90_boundary_known=all(row.boundary_equals_period_norm for row in legal_value_rows),
            period=SUPPORT_PERIOD,
            root_gcd_fp_star=support_root_gcd,
            branch_unique_in_fp_star=support_root_gcd == 1,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=False,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=True,
            arithmetic_source_theorem=True,
            decision="source_theorem_closed_policy_or_framing_missing",
            source_theorem_closes=True,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            ok=(
                len(legal_value_rows) == 4
                and all(row.ok for row in legal_value_rows)
                and all(
                    row.actual_decision == "source_theorem_closed_policy_or_framing_missing"
                    for row in legal_value_rows
                )
                and support_root_gcd == 1
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="h0_divisor_additive_boundary",
            input_shape="exact divisor/additive identity for one legal H0 product with Hilbert-90 boundary",
            certified_h0_product_rows=ks62.source_certified_rows,
            h90_boundary_known=True,
            period=None,
            root_gcd_fp_star=None,
            branch_unique_in_fp_star=False,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=False,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=True,
            arithmetic_source_theorem=True,
            decision=divisor_boundary.actual_decision,
            source_theorem_closes=divisor_boundary.source_stage_closed,
            first_missing_clause=divisor_boundary.actual_missing_clause,
            ok=(
                divisor_boundary.ok
                and divisor_boundary.actual_decision == "source_theorem_closed_policy_or_framing_missing"
                and divisor_boundary.source_stage_closed
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="finite_payload_without_source_theorem",
            input_shape="computed H0 finite payload with no challenge-legal arithmetic source theorem",
            certified_h0_product_rows=ks62.source_certified_rows,
            h90_boundary_known=True,
            period=SUPPORT_PERIOD,
            root_gcd_fp_star=support_root_gcd,
            branch_unique_in_fp_star=support_root_gcd == 1,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=False,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=True,
            arithmetic_source_theorem=False,
            decision=finite_payload_no_source.actual_decision,
            source_theorem_closes=finite_payload_no_source.source_stage_closed,
            first_missing_clause=finite_payload_no_source.actual_missing_clause,
            ok=(
                finite_payload_no_source.ok
                and finite_payload_no_source.actual_decision
                == "conditional_finite_payload_without_source_theorem"
                and not finite_payload_no_source.source_stage_closed
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="direct_fp_order39_root_shortcut",
            input_shape="theorem evaluates U_chi using a primitive 39th root inside F_p",
            certified_h0_product_rows=0,
            h90_boundary_known=False,
            period=None,
            root_gcd_fp_star=None,
            branch_unique_in_fp_star=False,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=True,
            direct_shortcut_rejected=True,
            finite_value_or_divisor_theorem=False,
            arithmetic_source_theorem=False,
            decision="reject_direct_Fp_order39_root_shortcut",
            source_theorem_closes=False,
            first_missing_clause="primitive 39th roots first occur over degree 6",
            ok=(
                degree6_arithmetic_ok
                and p_order_mod39 == 6
                and primitive_39_roots_first_in_degree6
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="sqrt_minus39_scalar_shortcut",
            input_shape="theorem collapses the mixed character using sqrt(-39) in F_p",
            certified_h0_product_rows=0,
            h90_boundary_known=False,
            period=None,
            root_gcd_fp_star=None,
            branch_unique_in_fp_star=False,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=True,
            direct_shortcut_rejected=True,
            finite_value_or_divisor_theorem=False,
            arithmetic_source_theorem=False,
            decision="reject_sqrt_minus39_scalar_shortcut",
            source_theorem_closes=False,
            first_missing_clause="sqrt(-39) is not in F_p",
            ok=(
                degree6_arithmetic_ok
                and discriminant_is_nonsquare_mod_p
            ),
        ),
        H0TranslateBoundaryValueAmbiguityRow(
            name="degree6_norm_descent_bare_value",
            input_shape="theorem descends a degree-6 cyclotomic value but omits period-156 branch context",
            certified_h0_product_rows=ks62.source_certified_rows,
            h90_boundary_known=True,
            period=None,
            root_gcd_fp_star=None,
            branch_unique_in_fp_star=False,
            ambient_mu11_ambiguity=False,
            requires_degree6_descent=True,
            direct_shortcut_rejected=False,
            finite_value_or_divisor_theorem=True,
            arithmetic_source_theorem=True,
            decision="conditional_value_theorem_missing_period156_context",
            source_theorem_closes=False,
            first_missing_clause="period-156 branch/root/telescoping context",
            ok=(
                degree6_arithmetic_ok
                and primitive_39_roots_first_in_degree6
                and discriminant_is_nonsquare_mod_p
            ),
        ),
    )

    source_certified_only = sum(
        row.decision == "source_certified_value_or_divisor_missing" for row in rows
    )
    ambient_mu11 = sum(row.ambient_mu11_ambiguity for row in rows)
    branch_unique = sum(row.branch_unique_in_fp_star and row.finite_value_or_divisor_theorem for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    conditional = sum(row.decision.startswith("conditional_") for row in rows)
    rejected_shortcut = sum(row.direct_shortcut_rejected for row in rows)
    submission_ready = 0

    row_ok = (
        ks62.row_ok
        and compat.row_ok
        and degree6_arithmetic_ok
        and SUPPORT_PERIOD == 156
        and AMBIENT_PERIOD == 780
        and support_root_gcd == 1
        and ambient_root_gcd == 11
        and p_order_mod39 == 6
        and primitive_39_roots_first_in_degree6
        and discriminant_is_nonsquare_mod_p
        and ks62.source_certified_rows == 4
        and ks62.boundary_norm_rows == 4
        and len(rows) == 8
        and source_certified_only == 1
        and ambient_mu11 == 1
        and branch_unique == 2
        and source_closing == 2
        and conditional == 3
        and rejected_shortcut == 2
        and submission_ready == 0
        and all(row.ok for row in rows)
    )

    return H0TranslateBoundaryValueAmbiguityPacket(
        koo_shin62_screen_ok=ks62.row_ok,
        h0_translate_value_compatibility_ok=compat.row_ok,
        degree6_arithmetic_ok=degree6_arithmetic_ok,
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        support_period_root_gcd=support_root_gcd,
        ambient_period_root_gcd=ambient_root_gcd,
        p_order_mod39=p_order_mod39,
        primitive_39_roots_first_in_degree6=primitive_39_roots_first_in_degree6,
        sqrt_minus39_in_fp=not discriminant_is_nonsquare_mod_p,
        exact_h0_products_certified=ks62.source_certified_rows,
        boundary_norm_rows=ks62.boundary_norm_rows,
        ambiguity_rows=rows,
        row_count=len(rows),
        source_certified_only_rows=source_certified_only,
        ambient_mu11_rows=ambient_mu11,
        branch_unique_rows=branch_unique,
        source_closing_rows=source_closing,
        conditional_rows=conditional,
        rejected_shortcut_rows=rejected_shortcut,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_boundary_value_ambiguity()
    print("p25 KSY-y H0 translate boundary/value ambiguity gate")
    print("dependencies")
    print(f"  koo_shin62_screen_ok={int(profile.koo_shin62_screen_ok)}")
    print(f"  h0_translate_value_compatibility_ok={int(profile.h0_translate_value_compatibility_ok)}")
    print(f"  degree6_arithmetic_ok={int(profile.degree6_arithmetic_ok)}")
    print("arithmetic")
    print(f"  support_period={profile.support_period}")
    print(f"  ambient_period={profile.ambient_period}")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print(f"  p_order_mod39={profile.p_order_mod39}")
    print(
        "  primitive_39_roots_first_in_degree6="
        f"{int(profile.primitive_39_roots_first_in_degree6)}"
    )
    print(f"  sqrt_minus39_in_Fp={int(profile.sqrt_minus39_in_fp)}")
    print("certified_h0_family")
    print(f"  exact_h0_products_certified={profile.exact_h0_products_certified}")
    print(f"  boundary_norm_rows={profile.boundary_norm_rows}")
    print("ambiguity_rows")
    for row in profile.ambiguity_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} period={row.period} "
            f"root_gcd={row.root_gcd_fp_star} unique={int(row.branch_unique_in_fp_star)} "
            f"mu11={int(row.ambient_mu11_ambiguity)} degree6={int(row.requires_degree6_descent)} "
            f"shortcut_reject={int(row.direct_shortcut_rejected)} "
            f"finite={int(row.finite_value_or_divisor_theorem)} "
            f"source={int(row.arithmetic_source_theorem)} "
            f"closes={int(row.source_theorem_closes)}"
        )
        print(f"    shape={row.input_shape}")
        print(f"    missing={row.first_missing_clause}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  ambient_mu11_rows={profile.ambient_mu11_rows}")
    print(f"  branch_unique_rows={profile.branch_unique_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_shortcut_rows={profile.rejected_shortcut_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  boundary_only_H0_data_is_source_certification_not_a_value_theorem=1")
    print("  ambient_or_bare_H0_values_keep_mu11_or_period_branch_ambiguity=1")
    print("  support_period_156_value_context_makes_the_Fp_star_branch_unique=1")
    print("  divisor_additive_H0_identity_closes_source_without_multiplicative_branch=1")
    print("  direct_Fp_order39_or_sqrt_minus39_shortcuts_are_rejected=1")
    print("  no_DANGER3_extraction_or_vpp_verified_triple_yet=1")
    print(f"ksy_y_h0_translate_boundary_value_ambiguity_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate boundary/value ambiguity regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
