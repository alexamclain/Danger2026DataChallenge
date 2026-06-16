#!/usr/bin/env python3
"""Post-Koo-Shin-6.2 router for the legal H0-translate lane.

The Koo-Shin 6.2 screen now certifies that all four exact H0 products are
legal conductor-39 modular-unit source words.  This gate records the immediate
upgrade map: which nearby Koo-Shin-style facts remain context only, and which
exact theorem shapes would actually close the H0 source stage.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_translate_koo_shin62_screen_gate import (
    profile_h0_translate_koo_shin62_screen,
)
from p25_ksy_y_h0_translate_theorem_query_packet_gate import (
    H0TranslateTheoremQueryRow,
    profile_h0_translate_theorem_query_packet,
)
from p25_ksy_y_koo_shin_2010_full_surface_screen_gate import (
    profile_koo_shin_2010_full_surface_screen,
)
from p25_ksy_y_koo_shin_2010_ray_class_generator_guardrail_gate import (
    profile_koo_shin_ray_class_generator_guardrail,
)
from p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_gate import (
    profile_actual_theorem52_verdict,
)


@dataclass(frozen=True)
class H0TranslatePostKooShin62UpgradeRow:
    name: str
    source_handle: str
    claim_shape: str
    decision: str
    exact_h0_products_certified: bool
    context_only: bool
    source_certified_only: bool
    source_theorem_closes: bool
    conditional: bool
    rejected: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0TranslatePostKooShin62UpgradeRouter:
    koo_shin62_screen_ok: bool
    theorem_query_packet_ok: bool
    theorem52_actual_verdict_ok: bool
    full_surface_screen_ok: bool
    ray_class_guardrail_ok: bool
    all_exact_h0_products_ks62_certified: bool
    theorem62_certified_product_rows: int
    router_rows: tuple[H0TranslatePostKooShin62UpgradeRow, ...]
    row_count: int
    context_only_rows: int
    source_certified_only_rows: int
    source_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    continue_rows: int
    kill_rows: int
    row_ok: bool


def query_row(
    rows: tuple[H0TranslateTheoremQueryRow, ...],
    name: str,
) -> H0TranslateTheoremQueryRow:
    return next(row for row in rows if row.name == name)


def profile_h0_translate_post_koo_shin62_upgrade_router() -> H0TranslatePostKooShin62UpgradeRouter:
    ks62 = profile_h0_translate_koo_shin62_screen()
    query = profile_h0_translate_theorem_query_packet()
    t52 = profile_actual_theorem52_verdict()
    full = profile_koo_shin_2010_full_surface_screen()
    ray = profile_koo_shin_ray_class_generator_guardrail()

    value_period = query_row(query.query_rows, "ask_value_with_period156")
    divisor_boundary = query_row(query.query_rows, "ask_divisor_additive_identity")
    finite_without_source = query_row(query.query_rows, "ask_finite_payload_without_source")
    nonlegal = query_row(query.query_rows, "reject_nonlegal_h0_translate")
    formal = query_row(query.query_rows, "reject_formal_one_coset_h")

    all_exact_h0_products_ks62_certified = (
        ks62.row_ok
        and ks62.row_count == 4
        and ks62.theorem62_congruence_rows == 4
        and ks62.source_certified_rows == 4
        and ks62.source_theorem_closing_rows == 0
        and ks62.boundary_norm_rows == 4
    )

    rows = (
        H0TranslatePostKooShin62UpgradeRow(
            name="koo_shin62_product_legality_for_exact_h0_rows",
            source_handle="Koo-Shin 2010 Theorem 6.2 plus exact H0 translates",
            claim_shape="four legal 78-over-78 H0 products pass conductor-39 congruence screen",
            decision="source_certified_value_or_divisor_missing",
            exact_h0_products_certified=True,
            context_only=False,
            source_certified_only=True,
            source_theorem_closes=False,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value/divisor theorem for one exact H0 product",
            next_action="ask only value-period156 or divisor/additive upgrade questions",
            ok=all_exact_h0_products_ks62_certified,
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="koo_shin52_prime_level_root_descent_context",
            source_handle="Koo-Shin 2010 Theorem 5.2",
            claim_shape="prime-level Siegel-product rigidity and l-th-root descent",
            decision=t52.intake_decision,
            exact_h0_products_certified=False,
            context_only=True,
            source_certified_only=False,
            source_theorem_closes=False,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=t52.first_missing_clause,
            next_action="keep as root-descent/constant-rigidity context only",
            ok=(
                t52.row_ok
                and t52.intake_decision == "reject_prime_power_only_missing_mixed_lift"
                and not t52.exact_p25_product_emitted
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="koo_shin39_orbit_sum_hygiene",
            source_handle="Koo-Shin 2010 Theorem 3.9",
            claim_shape="orbit-sum/integrality hygiene on KSY/Yang source packets",
            decision="context_only_integrality_hygiene_not_exact_selector",
            exact_h0_products_certified=False,
            context_only=True,
            source_certified_only=False,
            source_theorem_closes=False,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=full.remaining_upgrade,
            next_action="do not treat one-axis or orbit hygiene as a product producer",
            ok=(
                full.row_ok
                and full.text_scan.has_theorem_3_9
                and full.theorem_3_9_is_hygiene_not_selector
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="koo_shin9_ray_class_generator_context",
            source_handle="Koo-Shin 2010 Theorems 9.8/9.10/9.11",
            claim_shape="ray-class generator vocabulary and all-unit/single-index products",
            decision="context_only_ray_class_generator_not_mixed_u_chi_value_theorem",
            exact_h0_products_certified=False,
            context_only=True,
            source_certified_only=False,
            source_theorem_closes=False,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=ray.remaining_upgrade,
            next_action="use as vocabulary/context; require independent mixed-character value theorem",
            ok=(
                ray.row_ok
                and ray.theorem_98_present
                and ray.theorem_910_present
                and ray.theorem_911_present
                and ray.ray_class_context_rows == 2
                and ray.finite_value_theorem_ready_rows == 0
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="h0_value_period156_upgrade",
            source_handle=value_period.source_obligation_row,
            claim_shape=value_period.accepted_answer_shape,
            decision=value_period.actual_decision,
            exact_h0_products_certified=True,
            context_only=False,
            source_certified_only=False,
            source_theorem_closes=True,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=value_period.first_falsifier,
            next_action=value_period.continue_recommendation,
            ok=(
                value_period.ok
                and value_period.source_theorem_closes
                and value_period.downstream_relevant
                and value_period.actual_decision == "source_theorem_closed_policy_or_framing_missing"
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="h0_divisor_additive_upgrade",
            source_handle=divisor_boundary.source_obligation_row,
            claim_shape=divisor_boundary.accepted_answer_shape,
            decision=divisor_boundary.actual_decision,
            exact_h0_products_certified=True,
            context_only=False,
            source_certified_only=False,
            source_theorem_closes=True,
            conditional=False,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=divisor_boundary.first_falsifier,
            next_action=divisor_boundary.continue_recommendation,
            ok=(
                divisor_boundary.ok
                and divisor_boundary.source_theorem_closes
                and divisor_boundary.downstream_relevant
                and divisor_boundary.actual_decision == "source_theorem_closed_policy_or_framing_missing"
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="finite_payload_without_source",
            source_handle=finite_without_source.source_obligation_row,
            claim_shape=finite_without_source.accepted_answer_shape,
            decision=finite_without_source.actual_decision,
            exact_h0_products_certified=True,
            context_only=False,
            source_certified_only=False,
            source_theorem_closes=False,
            conditional=True,
            rejected=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=finite_without_source.first_falsifier,
            next_action=finite_without_source.continue_recommendation,
            ok=(
                finite_without_source.ok
                and finite_without_source.actual_decision
                == "conditional_finite_payload_without_source_theorem"
                and not finite_without_source.source_theorem_closes
            ),
        ),
        H0TranslatePostKooShin62UpgradeRow(
            name="formal_or_nonlegal_h",
            source_handle=f"{nonlegal.source_obligation_row}; {formal.source_obligation_row}",
            claim_shape="formal one-coset H object or H0 translate outside the legal Yang/H90 family",
            decision="reject_before_source_or_x1_routing",
            exact_h0_products_certified=False,
            context_only=False,
            source_certified_only=False,
            source_theorem_closes=False,
            conditional=False,
            rejected=True,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause=f"{nonlegal.first_falsifier}; {formal.first_falsifier}",
            next_action="discard unless remapped to one of the four exact legal products",
            ok=(
                nonlegal.ok
                and formal.ok
                and nonlegal.actual_decision == "reject_target_fails_yang_or_h90_legality"
                and formal.actual_decision == "reject_illegal_or_insufficient_target"
            ),
        ),
    )

    context_only = sum(row.context_only for row in rows)
    source_certified_only = sum(row.source_certified_only for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    conditional = sum(row.conditional for row in rows)
    rejected = sum(row.rejected for row in rows)
    danger3_unblocked = sum(row.danger3_unblocked for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    continue_rows = sum(
        row.source_theorem_closes or row.source_certified_only or row.conditional
        for row in rows
    )
    kill_rows = sum(row.rejected for row in rows)

    row_ok = (
        ks62.row_ok
        and query.row_ok
        and t52.row_ok
        and full.row_ok
        and ray.row_ok
        and all_exact_h0_products_ks62_certified
        and len(rows) == 8
        and context_only == 3
        and source_certified_only == 1
        and source_closing == 2
        and conditional == 1
        and rejected == 1
        and danger3_unblocked == 0
        and extraction_ready == 0
        and submission_ready == 0
        and continue_rows == 4
        and kill_rows == 1
        and all(row.ok for row in rows)
    )

    return H0TranslatePostKooShin62UpgradeRouter(
        koo_shin62_screen_ok=ks62.row_ok,
        theorem_query_packet_ok=query.row_ok,
        theorem52_actual_verdict_ok=t52.row_ok,
        full_surface_screen_ok=full.row_ok,
        ray_class_guardrail_ok=ray.row_ok,
        all_exact_h0_products_ks62_certified=all_exact_h0_products_ks62_certified,
        theorem62_certified_product_rows=ks62.source_certified_rows,
        router_rows=rows,
        row_count=len(rows),
        context_only_rows=context_only,
        source_certified_only_rows=source_certified_only,
        source_closing_rows=source_closing,
        conditional_rows=conditional,
        rejected_rows=rejected,
        danger3_unblocked_rows=danger3_unblocked,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        continue_rows=continue_rows,
        kill_rows=kill_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_post_koo_shin62_upgrade_router()
    print("p25 KSY-y H0 translate post-Koo-Shin-6.2 upgrade router gate")
    print("dependencies")
    print(f"  koo_shin62_screen_ok={int(profile.koo_shin62_screen_ok)}")
    print(f"  theorem_query_packet_ok={int(profile.theorem_query_packet_ok)}")
    print(f"  theorem52_actual_verdict_ok={int(profile.theorem52_actual_verdict_ok)}")
    print(f"  full_surface_screen_ok={int(profile.full_surface_screen_ok)}")
    print(f"  ray_class_guardrail_ok={int(profile.ray_class_guardrail_ok)}")
    print("post_62_fact")
    print(f"  all_exact_h0_products_ks62_certified={int(profile.all_exact_h0_products_ks62_certified)}")
    print(f"  theorem62_certified_product_rows={profile.theorem62_certified_product_rows}")
    print("router_rows")
    for row in profile.router_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} context={int(row.context_only)} "
            f"source_cert={int(row.source_certified_only)} closes={int(row.source_theorem_closes)} "
            f"conditional={int(row.conditional)} rejected={int(row.rejected)} "
            f"danger3={int(row.danger3_unblocked)} extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    source={row.source_handle}")
        print(f"    shape={row.claim_shape}")
        print(f"    missing={row.first_missing_clause}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  context_only_rows={profile.context_only_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  kill_rows={profile.kill_rows}")
    print("interpretation")
    print("  Koo_Shin_6_2_now_certifies_the_four_exact_H0_products_as_legal_sources=1")
    print("  Koo_Shin_5_2_3_9_and_9_x_remain_context_or_hygiene_not_H0_value_theorems=1")
    print("  only_value_period156_or_divisor_additive_identity_closes_H0_source_stage=1")
    print("  no_DANGER3_unblocked_extraction_or_vpp_verified_triple_yet=1")
    print(f"ksy_y_h0_translate_post_koo_shin62_upgrade_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate post-Koo-Shin-6.2 upgrade router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
