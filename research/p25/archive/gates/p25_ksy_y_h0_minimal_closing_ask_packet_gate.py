#!/usr/bin/env python3
"""Minimal closing-ask packet for the current p25 H0 moonshot lane.

Several H0 artifacts now answer adjacent questions.  This gate compresses
them into the smallest expert/search ask that can move the lane: Koo-Shin 6.2
has certified the four exact legal H0 source products, but a win still needs a
period-156 value theorem or divisor/additive theorem for one of those products,
then cross-level extraction and official vpp.py verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class H0MinimalClosingAskRow:
    name: str
    ask: str
    accepted_answer_shape: str
    derived_from: str
    source_theorem_closes: bool
    downstream_followup: bool
    reject_or_conditional: bool
    final_submission_boundary: bool
    decision: str
    first_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0MinimalClosingAskPacket:
    exact_product_packet_marker_present: bool
    post_koo_shin62_router_marker_present: bool
    boundary_value_ambiguity_marker_present: bool
    final_certificate_boundary_marker_present: bool
    exact_product_targets: int
    canonical_targets: int
    h0_translate_targets: int
    support_period: int
    ambient_period: int
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    all_exact_targets_78_over_78: bool
    rows: tuple[H0MinimalClosingAskRow, ...]
    row_count: int
    source_closing_yes_rows: int
    source_certified_only_rows: int
    downstream_followup_rows: int
    reject_or_conditional_rows: int
    final_submission_boundary_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def ask_rows() -> tuple[H0MinimalClosingAskRow, ...]:
    return (
        H0MinimalClosingAskRow(
            name="ks62_status_not_closer",
            ask="What does Koo-Shin 6.2 already give us for the four exact H0 products?",
            accepted_answer_shape="legal conductor-39 source certification only",
            derived_from="h0_translate_post_koo_shin62_upgrade_router",
            source_theorem_closes=False,
            downstream_followup=False,
            reject_or_conditional=False,
            final_submission_boundary=False,
            decision="source_certified_value_or_divisor_missing",
            first_falsifier="answer stops at legal source certification for W/H0",
            next_action="ask only value-period156 or divisor/additive upgrade questions",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="ask_value_period156_identity",
            ask=(
                "Is there a source theorem giving the exact finite-field value "
                "of one exact legal H0 product with support-period-156 "
                "branch/root/telescoping context?"
            ),
            accepted_answer_shape="period-156 value identity for one of the four 78-over-78 H0 products",
            derived_from="h0_translate_theorem_query_packet + boundary_value_ambiguity",
            source_theorem_closes=True,
            downstream_followup=False,
            reject_or_conditional=False,
            final_submission_boundary=False,
            decision="source_theorem_closed_policy_or_framing_missing",
            first_falsifier="wrong product, missing legal translate, or missing period-156 context",
            next_action="route to DANGER3 framing, same-j X1(8112) bridge, X1(16), and vpp.py",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="ask_divisor_additive_identity",
            ask=(
                "Is there an exact divisor/additive theorem for one exact legal "
                "H0 product, preserving the Hilbert-90 boundary to Norm_156(Y_507)?"
            ),
            accepted_answer_shape="divisor/additive identity for one of the four 78-over-78 H0 products",
            derived_from="h0_translate_theorem_query_packet + boundary_value_ambiguity",
            source_theorem_closes=True,
            downstream_followup=False,
            reject_or_conditional=False,
            final_submission_boundary=False,
            decision="source_theorem_closed_policy_or_framing_missing",
            first_falsifier="formal H, projection, nonlegal sparse gauge, or missing H90 boundary",
            next_action="route to DANGER3 framing, same-j X1(8112) bridge, X1(16), and vpp.py",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="ask_same_j_extraction_after_source_yes",
            ask="After a source yes, can it be tied through same-j X1(8112) to the practical X1(16) chart?",
            accepted_answer_shape="same-j order-8112 bridge yielding X1(16) y/x/A/xP16 or direct A,x0",
            derived_from="h0_source_to_danger3_handoff + order8112_x16_chart_specialization",
            source_theorem_closes=False,
            downstream_followup=True,
            reject_or_conditional=False,
            final_submission_boundary=False,
            decision="downstream_cross_level_extraction_required",
            first_falsifier="odd-level theorem has no same-j X1(16)/X1(8112) bridge",
            next_action="specialize to A,xP16, then halve to x0 or emit direct A,x0",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="official_vpp_boundary",
            ask="What is the last line between an internal extraction and a DANGER3 submission?",
            accepted_answer_shape="official vpp.py verifies the concrete p25 (p,A,x0) triple",
            derived_from="h0_x16_final_certificate_boundary",
            source_theorem_closes=False,
            downstream_followup=True,
            reject_or_conditional=False,
            final_submission_boundary=True,
            decision="official_vpp_verified_triple_is_submission_boundary",
            first_falsifier="internal verifier, branch word, x-chain, or direct x0 without official vpp.py",
            next_action="archive vpp output, environment, command, and generate Lean certificate",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="reject_bare_or_ambient_value",
            ask="Can a bare finite value or ambient-period-780 value be accepted?",
            accepted_answer_shape="no; it is conditional until period-156 branch data is supplied",
            derived_from="h0_translate_boundary_value_ambiguity",
            source_theorem_closes=False,
            downstream_followup=False,
            reject_or_conditional=True,
            final_submission_boundary=False,
            decision="conditional_missing_period_156_context",
            first_falsifier="ambient period 780 leaves an 11-branch ambiguity in F_p^*",
            next_action="ask for support-period 156 fixedness or equivalent telescoping witness",
            ok=True,
        ),
        H0MinimalClosingAskRow(
            name="reject_computed_payload_without_source",
            ask="Can a computed H0 finite payload close the moonshot by itself?",
            accepted_answer_shape="no; it remains diagnostic without a challenge-legal arithmetic source theorem",
            derived_from="h0_translate_theorem_query_packet",
            source_theorem_closes=False,
            downstream_followup=False,
            reject_or_conditional=True,
            final_submission_boundary=False,
            decision="conditional_finite_payload_without_source_theorem",
            first_falsifier="finite computation is not emitted by a theorem",
            next_action="keep as verifier data only",
            ok=True,
        ),
    )


def profile_h0_minimal_closing_ask_packet() -> H0MinimalClosingAskPacket:
    exact_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_exact_product_query_packet_20260614.md",
        "ksy_y_h0_translate_exact_product_query_packet_rows=1/1",
    )
    post_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_post_koo_shin62_upgrade_router_20260614.md",
        "ksy_y_h0_translate_post_koo_shin62_upgrade_router_rows=1/1",
    )
    ambiguity_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_boundary_value_ambiguity_20260614.md",
        "ksy_y_h0_translate_boundary_value_ambiguity_rows=1/1",
    )
    final_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_x16_final_certificate_boundary_20260614.md",
        "ksy_y_h0_x16_final_certificate_boundary_rows=1/1",
    )
    support_root_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_root_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    rows = ask_rows()
    source_closing_yes = sum(row.source_theorem_closes for row in rows)
    source_certified_only = sum(row.decision == "source_certified_value_or_divisor_missing" for row in rows)
    downstream_followup = sum(row.downstream_followup for row in rows)
    reject_or_conditional = sum(row.reject_or_conditional for row in rows)
    final_boundary = sum(row.final_submission_boundary for row in rows)
    current_submission_ready = 0
    decisions = tuple(row.decision for row in rows)
    row_ok = (
        exact_marker
        and post_marker
        and ambiguity_marker
        and final_marker
        and SUPPORT_PERIOD == 156
        and AMBIENT_PERIOD == 780
        and support_root_gcd == 1
        and ambient_root_gcd == 11
        and len(rows) == 7
        and source_closing_yes == 2
        and source_certified_only == 1
        and downstream_followup == 2
        and reject_or_conditional == 2
        and final_boundary == 1
        and current_submission_ready == 0
        and decisions
        == (
            "source_certified_value_or_divisor_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "downstream_cross_level_extraction_required",
            "official_vpp_verified_triple_is_submission_boundary",
            "conditional_missing_period_156_context",
            "conditional_finite_payload_without_source_theorem",
        )
        and all(row.ok for row in rows)
    )
    return H0MinimalClosingAskPacket(
        exact_product_packet_marker_present=exact_marker,
        post_koo_shin62_router_marker_present=post_marker,
        boundary_value_ambiguity_marker_present=ambiguity_marker,
        final_certificate_boundary_marker_present=final_marker,
        exact_product_targets=4,
        canonical_targets=1,
        h0_translate_targets=3,
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        support_period_root_gcd=support_root_gcd,
        ambient_period_root_gcd=ambient_root_gcd,
        all_exact_targets_78_over_78=True,
        rows=rows,
        row_count=len(rows),
        source_closing_yes_rows=source_closing_yes,
        source_certified_only_rows=source_certified_only,
        downstream_followup_rows=downstream_followup,
        reject_or_conditional_rows=reject_or_conditional,
        final_submission_boundary_rows=final_boundary,
        current_submission_ready_rows=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_minimal_closing_ask_packet()
    print("p25 KSY-y H0 minimal closing-ask packet gate")
    print("dependencies")
    print(f"  exact_product_packet_marker_present={int(profile.exact_product_packet_marker_present)}")
    print(f"  post_koo_shin62_router_marker_present={int(profile.post_koo_shin62_router_marker_present)}")
    print(f"  boundary_value_ambiguity_marker_present={int(profile.boundary_value_ambiguity_marker_present)}")
    print(f"  final_certificate_boundary_marker_present={int(profile.final_certificate_boundary_marker_present)}")
    print("target_family")
    print(f"  exact_product_targets={profile.exact_product_targets}")
    print(f"  canonical_targets={profile.canonical_targets}")
    print(f"  h0_translate_targets={profile.h0_translate_targets}")
    print(f"  support_period={profile.support_period}")
    print(f"  ambient_period={profile.ambient_period}")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print(f"  all_exact_targets_78_over_78={int(profile.all_exact_targets_78_over_78)}")
    print("ask_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: closes={int(row.source_theorem_closes)} "
            f"downstream={int(row.downstream_followup)} "
            f"conditional={int(row.reject_or_conditional)} "
            f"final_boundary={int(row.final_submission_boundary)} "
            f"decision={row.decision} falsifier={row.first_falsifier}"
        )
        print(f"    ask={row.ask}")
        print(f"    accepts={row.accepted_answer_shape}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_yes_rows={profile.source_closing_yes_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  downstream_followup_rows={profile.downstream_followup_rows}")
    print(f"  reject_or_conditional_rows={profile.reject_or_conditional_rows}")
    print(f"  final_submission_boundary_rows={profile.final_submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  minimal_source_yes_is_value_period156_or_divisor_additive_identity=1")
    print("  exact_H0_targets_are_four_78_over_78_products=1")
    print("  bare_ambient_value_and_computed_payload_do_not_close_source=1")
    print("  official_vpp_verified_A_x0_remains_the_submission_boundary=1")
    print(f"ksy_y_h0_minimal_closing_ask_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 minimal closing-ask packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
