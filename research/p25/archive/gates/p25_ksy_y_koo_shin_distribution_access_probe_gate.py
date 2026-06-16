#!/usr/bin/env python3
"""Koo-Shin distribution access probe for the p25 KSY-y moonshot.

This gate records the current evidence level for the Koo-Shin 2010
Siegel-function lead.  The important guardrail is that search snippets and
metadata are not theorem text, and theorem text is not a p25 product closer
unless it maps to the exact mixed graph.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class KooShinProbeRow:
    name: str
    source_url: str
    evidence_level: str
    local_evidence: str
    positive_payload: str
    blocker: str
    verdict: str
    first_missing_clause: str
    recommendation: str
    direct_closer: bool
    row_ok: bool


@dataclass(frozen=True)
class KooShinProbeProfile:
    target_product: str
    rows: tuple[KooShinProbeRow, ...]
    source_handle_verified_rows: int
    snippet_positive_rows: int
    theorem_body_rows: int
    access_failure_rows: int
    context_product_criterion_rows: int
    direct_closing_rows: int
    continue_rows: int
    kill_as_direct_closer_rows: int
    all_rows_have_missing_clause: bool
    row_ok: bool


def probe_rows() -> tuple[KooShinProbeRow, ...]:
    return (
        KooShinProbeRow(
            name="springer_primary_metadata",
            source_url="https://link.springer.com/article/10.1007/s00209-008-0456-9",
            evidence_level="source_handle_verified",
            local_evidence=(
                "Springer page verifies Koo-Shin, Math. Z. 264 (2010), "
                "137-177, DOI 10.1007/s00209-008-0456-9; abstract says the "
                "paper establishes criteria for products of Siegel functions"
            ),
            positive_payload=(
                "right article family: products of Siegel functions, modular "
                "units, generators, and ray class invariants"
            ),
            blocker="article page is subscription preview; no theorem body",
            verdict="source_handle_positive_but_not_theorem_body",
            first_missing_clause=(
                "Theorem 5.2 body and exact map to p25 mixed graph/equal "
                "weights/orientation"
            ),
            recommendation="continue_only_with_full_pdf_or_ocr",
            direct_closer=False,
            row_ok=True,
        ),
        KooShinProbeRow(
            name="asarc_search_snippet_theorem_5_2",
            source_url=(
                "https://asarc.kaist.ac.kr/bbs/download.php?"
                "board_id=preprint&file=1239862589_0.691233.pdf&no=14"
            ),
            evidence_level="snippet_positive_not_source_text",
            local_evidence=(
                "/tmp/p25_lit_scout/koo_shin_2010_probe/fetch_24.bin:147-155 "
                "preserves the Google result snippet: distribution relations "
                "of Siegel functions; Theorem 5.2 begins with an odd-prime "
                "product over a primitive 1/p lattice quotient"
            ),
            positive_payload=(
                "highest-value exact-product bridge lead found so far: a "
                "prime-level Siegel-function product/distribution theorem"
            ),
            blocker="search snippet is not enough to know hypotheses or conclusion",
            verdict="snippet_positive_but_not_usable_theorem",
            first_missing_clause=(
                "full theorem statement, hypotheses, exponent conventions, "
                "and whether it emits exact row-labeled p25 product data"
            ),
            recommendation="continue_with_full_text_retrieval_or_subagent",
            direct_closer=False,
            row_ok=True,
        ),
        KooShinProbeRow(
            name="access_probe_failures",
            source_url=(
                "direct ASARC URL, r.jina.ai reader variants, Google cache, "
                "and Springer PDF endpoint"
            ),
            evidence_level="access_failures_verified",
            local_evidence=(
                "local DNS and r.jina report asarc.kaist.ac.kr NXDOMAIN; "
                "Springer PDF endpoint returns HTML/idp access flow; Google "
                "cache returns search challenge HTML"
            ),
            positive_payload="none beyond confirming why the previous scout stalled",
            blocker="no accessible theorem body from the tested handles",
            verdict="current_handles_do_not_recover_pdf",
            first_missing_clause=(
                "alternate mirror, library access, author preprint, or OCR of "
                "the PDF"
            ),
            recommendation="kill_current_handles_as_direct_access_continue_retrieval",
            direct_closer=False,
            row_ok=True,
        ),
        KooShinProbeRow(
            name="koo_shin_ii_open_product_criterion_context",
            source_url="https://arxiv.org/abs/1007.2318",
            evidence_level="primary_source_context_not_theorem_5_2",
            local_evidence=(
                "/tmp/p25_lit_scout/koo_shin_ii_1007_2318/src/Siegel.tex:"
                "282-299 gives a Kubert-Lang product modularity criterion; "
                "it cites Koo-Shin I for basic properties but does not supply "
                "the Koo-Shin I Theorem 5.2 body"
            ),
            positive_payload=(
                "confirms the surrounding Siegel-product language and the "
                "standard modularity congruence constraints"
            ),
            blocker=(
                "Kubert-Lang congruence hygiene alone is not the p25 mixed "
                "product producer"
            ),
            verdict="verified_context_product_criterion_not_exact_p25_product",
            first_missing_clause=(
                "exact product/distribution specialization selecting the "
                "75 p25 atoms with equal weights and orientation"
            ),
            recommendation="kill_as_direct_closer_keep_as_hygiene_context",
            direct_closer=False,
            row_ok=True,
        ),
    )


def profile_koo_shin_distribution_access_probe() -> KooShinProbeProfile:
    rows = probe_rows()
    source_handle_verified_rows = sum(
        row.evidence_level in {
            "source_handle_verified",
            "primary_source_context_not_theorem_5_2",
        }
        for row in rows
    )
    snippet_positive_rows = sum(
        row.evidence_level == "snippet_positive_not_source_text" for row in rows
    )
    theorem_body_rows = sum(row.evidence_level == "theorem_body_verified" for row in rows)
    access_failure_rows = sum(row.evidence_level == "access_failures_verified" for row in rows)
    context_product_criterion_rows = sum(
        row.verdict == "verified_context_product_criterion_not_exact_p25_product"
        for row in rows
    )
    direct_closing_rows = sum(int(row.direct_closer) for row in rows)
    continue_rows = sum("continue" in row.recommendation for row in rows)
    kill_as_direct_closer_rows = sum(
        "kill" in row.recommendation and "direct" in row.recommendation for row in rows
    )
    all_rows_have_missing_clause = all(row.first_missing_clause for row in rows)
    expected_verdicts = (
        "source_handle_positive_but_not_theorem_body",
        "snippet_positive_but_not_usable_theorem",
        "current_handles_do_not_recover_pdf",
        "verified_context_product_criterion_not_exact_p25_product",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and len(rows) == 4
        and source_handle_verified_rows == 2
        and snippet_positive_rows == 1
        and theorem_body_rows == 0
        and access_failure_rows == 1
        and context_product_criterion_rows == 1
        and direct_closing_rows == 0
        and continue_rows == 3
        and kill_as_direct_closer_rows == 2
        and all_rows_have_missing_clause
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return KooShinProbeProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        source_handle_verified_rows=source_handle_verified_rows,
        snippet_positive_rows=snippet_positive_rows,
        theorem_body_rows=theorem_body_rows,
        access_failure_rows=access_failure_rows,
        context_product_criterion_rows=context_product_criterion_rows,
        direct_closing_rows=direct_closing_rows,
        continue_rows=continue_rows,
        kill_as_direct_closer_rows=kill_as_direct_closer_rows,
        all_rows_have_missing_clause=all_rows_have_missing_clause,
        row_ok=row_ok,
    )


def print_row(row: KooShinProbeRow) -> None:
    print(
        "  "
        f"{row.name}: evidence={row.evidence_level} verdict={row.verdict} "
        f"closes={int(row.direct_closer)} recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_koo_shin_distribution_access_probe()
    print("p25 KSY-y Koo-Shin distribution access probe gate")
    print(f"target_product={profile.target_product}")
    print("probe_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  source_handle_verified_rows={profile.source_handle_verified_rows}")
    print(f"  snippet_positive_rows={profile.snippet_positive_rows}")
    print(f"  theorem_body_rows={profile.theorem_body_rows}")
    print(f"  access_failure_rows={profile.access_failure_rows}")
    print(f"  context_product_criterion_rows={profile.context_product_criterion_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  kill_as_direct_closer_rows={profile.kill_as_direct_closer_rows}")
    print(f"  all_rows_have_missing_clause={int(profile.all_rows_have_missing_clause)}")
    print("interpretation")
    print("  koo_shin_2010_remains_high_value_retrieval_lead=1")
    print("  snippet_is_not_theorem_body=1")
    print("  current_handles_do_not_close_access=1")
    print("  koo_shin_ii_supplies_context_not_exact_p25_product=1")
    print(f"ksy_y_koo_shin_distribution_access_probe_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin distribution access probe regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
