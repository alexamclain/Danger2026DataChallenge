#!/usr/bin/env python3
"""Public mirror and sequel-source falsifier for the Koo-Shin p25 lead.

The KOASAS probe made the Koo-Shin 2010 file target exact.  This gate records
the complementary public-source result: the visible mirrors and the open sequel
do not provide the missing theorem body or an exact p25 product producer.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class PublicMirrorRow:
    name: str
    source_url: str
    source_kind: str
    local_evidence: str
    positive_payload: str
    missing_clause: str
    verdict: str
    recommendation: str
    main_theorem_visible: bool
    direct_closer: bool
    row_ok: bool


@dataclass(frozen=True)
class PublicMirrorProfile:
    target_product: str
    rows: tuple[PublicMirrorRow, ...]
    source_handles_checked: int
    unreachable_indexed_preprint_rows: int
    metadata_only_rows: int
    restricted_bitstream_rows: int
    open_sequel_source_rows: int
    inherited_hygiene_clause_rows: int
    public_main_theorem_rows: int
    direct_closing_rows: int
    continue_retrieval_rows: int
    kill_as_direct_closer_rows: int
    all_rows_have_missing_clause: bool
    row_ok: bool


def public_mirror_rows() -> tuple[PublicMirrorRow, ...]:
    return (
        PublicMirrorRow(
            name="asarc_indexed_preprint_url",
            source_url=(
                "https://asarc.kaist.ac.kr/bbs/download.php?"
                "board_id=preprint&file=1239862589_0.691233.pdf&no=14"
            ),
            source_kind="indexed_preprint_unreachable",
            local_evidence=(
                "web search still indexes this as the Koo-Shin 2010 PDF; "
                "local curl and r.jina reader both report asarc.kaist.ac.kr "
                "cannot be resolved"
            ),
            positive_payload=(
                "best public-preprint filename handle for the blocked main paper"
            ),
            missing_clause=(
                "actual PDF bytes or OCR for Koo-Shin 2010 Theorem 5.2"
            ),
            verdict="indexed_but_unreachable_no_theorem_body",
            recommendation="continue_only_via_dns_fix_library_author_or_mirror",
            main_theorem_visible=False,
            direct_closer=False,
            row_ok=True,
        ),
        PublicMirrorRow(
            name="springer_public_article_page",
            source_url="https://link.springer.com/article/10.1007/s00209-008-0456-9",
            source_kind="metadata_only_public_page",
            local_evidence=(
                "/tmp/p25_lit_scout/koo_shin_public_mirror_probe/"
                "koo_shin_springer.pdf is HTML, not PDF; page metadata says "
                "access is not free and rg finds no theorem text"
            ),
            positive_payload=(
                "official metadata, abstract, DOI, pages, authors, and "
                "subscription/access status for the target article"
            ),
            missing_clause=(
                "Theorem 5.2 body and any exact product/distribution clauses"
            ),
            verdict="official_metadata_only_no_public_theorem",
            recommendation="kill_public_page_as_direct_closer_keep_citation",
            main_theorem_visible=False,
            direct_closer=False,
            row_ok=True,
        ),
        PublicMirrorRow(
            name="koasas_public_handle_and_mets",
            source_url="https://koasas.kaist.ac.kr/handle/10203/96547",
            source_kind="metadata_plus_restricted_bitstream",
            local_evidence=(
                "KOASAS handle/OAI metadata are public; METS exposes "
                "bitstream 000271750900008.pdf, size 501978, MD5 "
                "39bf3ab80a349709394165f27f0eafbf; direct bitstream access "
                "redirects to authorization-required HTML"
            ),
            positive_payload=(
                "exact restricted file target for library, author-copy, "
                "Springer, or authorized KOASAS retrieval"
            ),
            missing_clause=(
                "authorized PDF access or alternate mirror matching the METS "
                "size/MD5"
            ),
            verdict="exact_bitstream_target_but_no_theorem_body",
            recommendation="continue_exact_retrieval_packet_not_theorem_use",
            main_theorem_visible=False,
            direct_closer=False,
            row_ok=True,
        ),
        PublicMirrorRow(
            name="jks_koo_shin_ii_arxiv_source",
            source_url="https://arxiv.org/abs/1007.2318",
            source_kind="open_sequel_primary_source",
            local_evidence=(
                "/tmp/p25_lit_scout/koo_shin_public_mirror_probe/"
                "Siegel_II.tex:239-318 gives the Siegel-function definition, "
                "basic transformation/integrality facts, a Kubert-Lang "
                "product modularity criterion, and a corollary for "
                "g_r^(12N/gcd(6,N))"
            ),
            positive_payload=(
                "confirms the standard inherited Siegel-unit hygiene layer "
                "around Koo-Shin, with source TeX available"
            ),
            missing_clause=(
                "an exact mixed C_3 x C_169 product/distribution theorem for "
                "the 75 p25 normalized-y atoms with orientation"
            ),
            verdict="open_sequel_hygiene_only_not_exact_p25_product",
            recommendation="kill_as_direct_closer_keep_as_hygiene_context",
            main_theorem_visible=False,
            direct_closer=False,
            row_ok=True,
        ),
    )


def profile_public_mirror_sequel_falsifier() -> PublicMirrorProfile:
    rows = public_mirror_rows()
    source_handles_checked = len(rows)
    unreachable_indexed_preprint_rows = sum(
        row.source_kind == "indexed_preprint_unreachable" for row in rows
    )
    metadata_only_rows = sum(
        row.source_kind == "metadata_only_public_page" for row in rows
    )
    restricted_bitstream_rows = sum(
        row.source_kind == "metadata_plus_restricted_bitstream" for row in rows
    )
    open_sequel_source_rows = sum(
        row.source_kind == "open_sequel_primary_source" for row in rows
    )
    inherited_hygiene_clause_rows = 3 if open_sequel_source_rows == 1 else 0
    public_main_theorem_rows = sum(int(row.main_theorem_visible) for row in rows)
    direct_closing_rows = sum(int(row.direct_closer) for row in rows)
    continue_retrieval_rows = sum(
        row.recommendation.startswith("continue") for row in rows
    )
    kill_as_direct_closer_rows = sum(
        "kill" in row.recommendation and "direct_closer" in row.recommendation
        for row in rows
    )
    all_rows_have_missing_clause = all(row.missing_clause for row in rows)
    expected_verdicts = (
        "indexed_but_unreachable_no_theorem_body",
        "official_metadata_only_no_public_theorem",
        "exact_bitstream_target_but_no_theorem_body",
        "open_sequel_hygiene_only_not_exact_p25_product",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and source_handles_checked == 4
        and unreachable_indexed_preprint_rows == 1
        and metadata_only_rows == 1
        and restricted_bitstream_rows == 1
        and open_sequel_source_rows == 1
        and inherited_hygiene_clause_rows == 3
        and public_main_theorem_rows == 0
        and direct_closing_rows == 0
        and continue_retrieval_rows == 2
        and kill_as_direct_closer_rows == 2
        and all_rows_have_missing_clause
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return PublicMirrorProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        source_handles_checked=source_handles_checked,
        unreachable_indexed_preprint_rows=unreachable_indexed_preprint_rows,
        metadata_only_rows=metadata_only_rows,
        restricted_bitstream_rows=restricted_bitstream_rows,
        open_sequel_source_rows=open_sequel_source_rows,
        inherited_hygiene_clause_rows=inherited_hygiene_clause_rows,
        public_main_theorem_rows=public_main_theorem_rows,
        direct_closing_rows=direct_closing_rows,
        continue_retrieval_rows=continue_retrieval_rows,
        kill_as_direct_closer_rows=kill_as_direct_closer_rows,
        all_rows_have_missing_clause=all_rows_have_missing_clause,
        row_ok=row_ok,
    )


def print_row(row: PublicMirrorRow) -> None:
    print(
        "  "
        f"{row.name}: kind={row.source_kind} verdict={row.verdict} "
        f"main_theorem={int(row.main_theorem_visible)} "
        f"closes={int(row.direct_closer)} recommendation={row.recommendation}"
    )
    print(f"    missing={row.missing_clause}")


def main() -> int:
    profile = profile_public_mirror_sequel_falsifier()
    print("p25 KSY-y Koo-Shin public mirror / sequel falsifier gate")
    print(f"target_product={profile.target_product}")
    print("rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  source_handles_checked={profile.source_handles_checked}")
    print(
        "  unreachable_indexed_preprint_rows="
        f"{profile.unreachable_indexed_preprint_rows}"
    )
    print(f"  metadata_only_rows={profile.metadata_only_rows}")
    print(f"  restricted_bitstream_rows={profile.restricted_bitstream_rows}")
    print(f"  open_sequel_source_rows={profile.open_sequel_source_rows}")
    print(
        "  inherited_hygiene_clause_rows="
        f"{profile.inherited_hygiene_clause_rows}"
    )
    print(f"  public_main_theorem_rows={profile.public_main_theorem_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  continue_retrieval_rows={profile.continue_retrieval_rows}")
    print(
        "  kill_as_direct_closer_rows="
        f"{profile.kill_as_direct_closer_rows}"
    )
    print(
        "  all_rows_have_missing_clause="
        f"{int(profile.all_rows_have_missing_clause)}"
    )
    print("interpretation")
    print("  no_public_main_theorem_body_recovered=1")
    print("  open_sequel_supplies_hygiene_not_exact_product=1")
    print("  exact_retrieval_packet_remains_the_live_koo_shin_action=1")
    print(
        "ksy_y_koo_shin_public_mirror_sequel_falsifier_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Koo-Shin public mirror / sequel falsifier regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
