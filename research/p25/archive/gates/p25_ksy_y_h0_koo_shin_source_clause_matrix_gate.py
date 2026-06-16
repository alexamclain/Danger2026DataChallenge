#!/usr/bin/env python3
"""Koo-Shin 2010 source-clause matrix for the p25 H0 lane.

The H0 source-theorem matcher says how to classify a hypothetical theorem hit.
This gate applies that intake to the actual Koo-Shin 2010 text surfaces so
future work does not accidentally promote useful context clauses into source
closures.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path

from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    H0SourceTheoremCandidate,
    classify_candidate,
)


P25 = 10**25 + 13
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780
REPO = Path(__file__).resolve().parents[2]
TEXT_PATH = REPO / "incoming" / "extracted" / "s00209-008-0456-9.pdf.extract.txt"
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class KooShinH0SourceClauseRow:
    name: str
    source_surface: str
    text_present: bool
    theorem_scope: str
    h0_candidate_executed: bool
    h0_candidate_decision: str
    source_theorem_closes: bool
    source_certified_only: bool
    context_only: bool
    rejected_as_closer: bool
    first_missing_clause: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class KooShinH0SourceClauseMatrix:
    exact_product_marker_present: bool
    matcher_marker_present: bool
    text_path: str
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    rows: tuple[KooShinH0SourceClauseRow, ...]
    row_count: int
    present_rows: int
    h0_candidate_rows: int
    source_closing_rows: int
    source_certified_only_rows: int
    context_only_rows: int
    rejected_as_closer_rows: int
    value_or_divisor_missing_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def load_text() -> str:
    return TEXT_PATH.read_text(encoding="utf-8", errors="ignore")


def has_all(text: str, *patterns: str) -> bool:
    return all(pattern in text for pattern in patterns)


def h0_decision(
    *,
    product_multiplier: int | None,
    residue_sets_exact: bool,
    arithmetic_source_theorem: bool,
    output_kind: str,
    period156_context: bool = False,
    h90_boundary: bool = False,
) -> tuple[str, bool, str, str]:
    candidate = H0SourceTheoremCandidate(
        name="koo_shin_source_clause",
        product_multiplier=product_multiplier,
        residue_sets_exact=residue_sets_exact,
        arithmetic_source_theorem=arithmetic_source_theorem,
        output_kind=output_kind,
        period156_context=period156_context,
        h90_boundary=h90_boundary,
        danger3_framing=False,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_x0=False,
        official_vpp=False,
    )
    decision = classify_candidate(candidate)
    return (
        decision.decision,
        decision.source_stage_closed,
        decision.first_missing_clause,
        decision.next_action,
    )


def context_row(
    *,
    name: str,
    source_surface: str,
    text_present: bool,
    theorem_scope: str,
    first_missing_clause: str,
    next_action: str,
) -> KooShinH0SourceClauseRow:
    return KooShinH0SourceClauseRow(
        name=name,
        source_surface=source_surface,
        text_present=text_present,
        theorem_scope=theorem_scope,
        h0_candidate_executed=False,
        h0_candidate_decision="context_only_not_h0_source_candidate",
        source_theorem_closes=False,
        source_certified_only=False,
        context_only=True,
        rejected_as_closer=True,
        first_missing_clause=first_missing_clause,
        next_action=next_action,
        ok=text_present,
    )


def candidate_row(
    *,
    name: str,
    source_surface: str,
    text_present: bool,
    theorem_scope: str,
    product_multiplier: int | None,
    residue_sets_exact: bool,
    arithmetic_source_theorem: bool,
    output_kind: str,
    period156_context: bool = False,
    h90_boundary: bool = False,
) -> KooShinH0SourceClauseRow:
    decision, source_closed, missing, next_action = h0_decision(
        product_multiplier=product_multiplier,
        residue_sets_exact=residue_sets_exact,
        arithmetic_source_theorem=arithmetic_source_theorem,
        output_kind=output_kind,
        period156_context=period156_context,
        h90_boundary=h90_boundary,
    )
    return KooShinH0SourceClauseRow(
        name=name,
        source_surface=source_surface,
        text_present=text_present,
        theorem_scope=theorem_scope,
        h0_candidate_executed=True,
        h0_candidate_decision=decision,
        source_theorem_closes=source_closed,
        source_certified_only=decision == "source_certified_value_or_divisor_missing",
        context_only=False,
        rejected_as_closer=not source_closed,
        first_missing_clause=missing,
        next_action=next_action,
        ok=text_present,
    )


def clause_rows(text: str) -> tuple[KooShinH0SourceClauseRow, ...]:
    theorem_3_9 = has_all(text, "Theorem 3.9 Let", "for each orbit")
    theorem_5_2 = has_all(text, "Theorem 5.2 (1) For an odd prime p", "Theorem 5.2(2)")
    theorem_6_2 = has_all(text, "Theorem 6.2 A product", "is an element of K(X1(N))")
    section_7_value = has_all(text, "Corollary 7.3", "we can express C(τ0)", "evaluate C(τ0) exactly")
    theorem_9_8 = has_all(text, "Theorem 9.8 For N", "TN (τ)")
    theorem_9_10 = has_all(text, "Theorem 9.10 For N", "MN (τ)")
    theorem_9_11 = has_all(text, "Theorem 9.11 For a prime p")

    return (
        context_row(
            name="theorem3_9_orbit_integrality_hygiene",
            source_surface="Koo-Shin 2010 Theorem 3.9",
            text_present=theorem_3_9,
            theorem_scope="prime-power orbit-sum integrality criterion",
            first_missing_clause="exact H0 product value/divisor theorem",
            next_action="use as necessary integrality hygiene only",
        ),
        context_row(
            name="theorem5_2_prime_level_root_descent",
            source_surface="Koo-Shin 2010 Theorem 5.2",
            text_present=theorem_5_2,
            theorem_scope="odd-prime product rigidity and l-th-root descent",
            first_missing_clause="mixed-level H0 lift preserving C3 row graph and T edge",
            next_action="keep as constant/root-descent context after a separate H0 source hit",
        ),
        candidate_row(
            name="theorem6_2_exact_h0_source_legality",
            source_surface="Koo-Shin 2010 Theorem 6.2 plus exact H0 translate screen",
            text_present=theorem_6_2,
            theorem_scope="complete one-axis X1(N) product/order formula used as H0 source legality",
            product_multiplier=1,
            residue_sets_exact=True,
            arithmetic_source_theorem=True,
            output_kind="source-certification",
            h90_boundary=True,
        ),
        candidate_row(
            name="theorem6_2_as_h0_value_closer_control",
            source_surface="Koo-Shin 2010 Theorem 6.2 misread as value/divisor theorem",
            text_present=theorem_6_2,
            theorem_scope="source certification only; no finite value or divisor/additive identity",
            product_multiplier=1,
            residue_sets_exact=True,
            arithmetic_source_theorem=True,
            output_kind="source-certification",
            h90_boundary=True,
        ),
        context_row(
            name="section7_ramanujan_value_evaluation",
            source_surface="Koo-Shin 2010 Section 7 / Corollary 7.3",
            text_present=section_7_value,
            theorem_scope="radical evaluation of Ramanujan cubic continued fraction values",
            first_missing_clause="one of the four exact legal H0 products",
            next_action="do not import X1(6)/continued-fraction value formula as H0 value theorem",
        ),
        context_row(
            name="theorem9_8_ray_class_sum_generator",
            source_surface="Koo-Shin 2010 Theorem 9.8",
            text_present=theorem_9_8,
            theorem_scope="ray-class generator using a sum of Siegel values",
            first_missing_clause="exact H0 finite value/divisor identity",
            next_action="use as generator vocabulary only",
        ),
        context_row(
            name="theorem9_10_ray_class_product_generator",
            source_surface="Koo-Shin 2010 Theorem 9.10",
            text_present=theorem_9_10,
            theorem_scope="ray-class generator using an all-unit product",
            first_missing_clause="exact H0 finite value/divisor identity",
            next_action="use as generator vocabulary only",
        ),
        context_row(
            name="theorem9_11_prime_ray_class_generator",
            source_surface="Koo-Shin 2010 Theorem 9.11",
            text_present=theorem_9_11,
            theorem_scope="prime-level CM singular-value generator",
            first_missing_clause="mixed H0 product at conductor 39/507, not prime-only generator",
            next_action="reject as direct H0 closer; keep as CM vocabulary",
        ),
    )


def profile_h0_koo_shin_source_clause_matrix() -> KooShinH0SourceClauseMatrix:
    exact_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_translate_exact_product_query_packet_20260614.md",
        "ksy_y_h0_translate_exact_product_query_packet_rows=1/1",
    )
    matcher_marker = marker_present(
        RESEARCH / "p25_ksy_y_h0_source_theorem_candidate_matcher_20260614.md",
        "ksy_y_h0_source_theorem_candidate_matcher_rows=1/1",
    )
    text = load_text()
    rows = clause_rows(text)
    support_root_gcd = gcd(pow(4, SUPPORT_PERIOD, P25 - 1) - 1, P25 - 1)
    ambient_root_gcd = gcd(pow(4, AMBIENT_PERIOD, P25 - 1) - 1, P25 - 1)
    present_rows = sum(row.text_present for row in rows)
    h0_candidates = sum(row.h0_candidate_executed for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    source_certified = sum(row.source_certified_only for row in rows)
    context_only = sum(row.context_only for row in rows)
    rejected = sum(row.rejected_as_closer for row in rows)
    value_or_divisor_missing = sum(
        row.first_missing_clause in {
            "finite-field value/divisor theorem for one exact H0 product",
            "exact H0 product value/divisor theorem",
            "exact H0 finite value/divisor identity",
        }
        for row in rows
    )
    row_ok = (
        exact_marker
        and matcher_marker
        and TEXT_PATH.exists()
        and support_root_gcd == 1
        and ambient_root_gcd == 11
        and len(rows) == 8
        and present_rows == 8
        and h0_candidates == 2
        and source_closing == 0
        and source_certified == 2
        and context_only == 6
        and rejected == 8
        and value_or_divisor_missing == 5
        and tuple(row.h0_candidate_decision for row in rows)
        == (
            "context_only_not_h0_source_candidate",
            "context_only_not_h0_source_candidate",
            "source_certified_value_or_divisor_missing",
            "source_certified_value_or_divisor_missing",
            "context_only_not_h0_source_candidate",
            "context_only_not_h0_source_candidate",
            "context_only_not_h0_source_candidate",
            "context_only_not_h0_source_candidate",
        )
        and all(row.ok for row in rows)
    )
    return KooShinH0SourceClauseMatrix(
        exact_product_marker_present=exact_marker,
        matcher_marker_present=matcher_marker,
        text_path=str(TEXT_PATH),
        support_period_root_gcd=support_root_gcd,
        ambient_period_root_gcd=ambient_root_gcd,
        rows=rows,
        row_count=len(rows),
        present_rows=present_rows,
        h0_candidate_rows=h0_candidates,
        source_closing_rows=source_closing,
        source_certified_only_rows=source_certified,
        context_only_rows=context_only,
        rejected_as_closer_rows=rejected,
        value_or_divisor_missing_rows=value_or_divisor_missing,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_koo_shin_source_clause_matrix()
    print("p25 KSY-y H0 Koo-Shin source-clause matrix gate")
    print("dependencies")
    print(f"  exact_product_marker_present={int(profile.exact_product_marker_present)}")
    print(f"  matcher_marker_present={int(profile.matcher_marker_present)}")
    print(f"  text_path={profile.text_path}")
    print("arithmetic")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print("clause_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: present={int(row.text_present)} "
            f"candidate={int(row.h0_candidate_executed)} "
            f"decision={row.h0_candidate_decision} "
            f"source_closed={int(row.source_theorem_closes)} "
            f"cert_only={int(row.source_certified_only)} "
            f"context={int(row.context_only)} "
            f"reject_closer={int(row.rejected_as_closer)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    surface={row.source_surface}")
        print(f"    scope={row.theorem_scope}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  present_rows={profile.present_rows}")
    print(f"  h0_candidate_rows={profile.h0_candidate_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  context_only_rows={profile.context_only_rows}")
    print(f"  rejected_as_closer_rows={profile.rejected_as_closer_rows}")
    print(f"  value_or_divisor_missing_rows={profile.value_or_divisor_missing_rows}")
    print("interpretation")
    print("  Koo_Shin_2010_current_clauses_do_not_close_H0_source=1")
    print("  theorem_6_2_certifies_H0_source_legality_but_not_value_or_divisor=1")
    print("  theorem_5_2_and_9x_remain_context_not_closers=1")
    print("  source_hit_still_needs_period156_value_or_divisor_additive_identity=1")
    print(f"ksy_y_h0_koo_shin_source_clause_matrix_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 Koo-Shin source-clause matrix regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
