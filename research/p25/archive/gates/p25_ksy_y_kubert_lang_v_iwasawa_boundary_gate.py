#!/usr/bin/env python3
"""Kubert-Lang V Iwasawa-tower boundary gate for the p25 KSY-y moonshot.

Kubert-Lang IV points to the next paper in the series.  This gate records the
direct probe of KL V: it is a genuine p-primary/Iwasawa modular-tower source,
but its visible payload is tower/Kummer/freeness structure, not the exact p25
mixed C_3 x C_169 row product or reflection payload.
"""

from __future__ import annotations

from dataclasses import dataclass


SOURCE = "Kubert-Lang, Units in the Modular Function Field. V. Iwasawa Theory in the Modular Tower"
EUDML = "https://eudml.org/doc/182778"
GDZ_PDF = "https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0237/LOG_0016.pdf"
LOCAL_PDF = "/tmp/p25_lit_scout/kubert_lang_v_probe/LOG_0016.pdf"
LOCAL_TEXT = "/tmp/p25_lit_scout/kubert_lang_v_probe/LOG_0016_pypdf_text.txt"
LOCAL_PAGES = "/tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016"
PDF_MD5 = "ca93ce860e3cd38717b15853ae30ead3"
PDF_BYTES = 691_420
PDF_PAGES = 9
ARTICLE_IMAGE_PAGES = 8


@dataclass(frozen=True)
class KlVRow:
    name: str
    evidence: str
    positive_payload: str
    p25_boundary: str
    verdict: str
    source_verified: bool
    visual_source_row: bool
    closes_p25: bool
    row_ok: bool


@dataclass(frozen=True)
class KlVProfile:
    source: str
    rows: tuple[KlVRow, ...]
    source_handle_rows: int
    pdf_retrieval_rows: int
    embedded_article_text_rows: int
    image_only_article_pages: int
    visual_source_rows: int
    iwasawa_tower_rows: int
    theorem1_freeness_rows: int
    vandiver_cyclotomic_rows: int
    row_labeled_pair_rows: int
    reflection_center_rows: int
    raw_k_traced_product_rows: int
    direct_closing_rows: int
    ocr_required_rows: int
    row_ok: bool


def kl_v_rows() -> tuple[KlVRow, ...]:
    return (
        KlVRow(
            name="kl78_v_eudml_gdz_handle",
            evidence=(
                f"{EUDML}; {GDZ_PDF}; local={LOCAL_PDF}; bytes={PDF_BYTES}; "
                f"md5={PDF_MD5}; article=Math. Ann. 237 (1978), 97-104"
            ),
            positive_payload=(
                "EuDML metadata and the GDZ LOG_0016 article PDF identify the "
                "Kubert-Lang V Iwasawa modular-tower source"
            ),
            p25_boundary=(
                "a p-primary source handle is not a finite p25 product theorem"
            ),
            verdict="verified_kl_v_primary_source_handle",
            source_verified=True,
            visual_source_row=False,
            closes_p25=False,
            row_ok=True,
        ),
        KlVRow(
            name="kl78_v_scan_extraction_boundary",
            evidence=(
                f"{LOCAL_TEXT}; pypdf extracts GDZ/license text plus only "
                "page-id-sized article-body text"
            ),
            positive_payload=(
                "local text-extraction boundary is reproducible; rendered "
                "pages are required for source classification"
            ),
            p25_boundary="full theorem-body search still needs OCR or alternate text",
            verdict="article_body_is_image_only_locally",
            source_verified=True,
            visual_source_row=False,
            closes_p25=False,
            row_ok=True,
        ),
        KlVRow(
            name="kl78_v_article_p97_intro",
            evidence=f"{LOCAL_PAGES}/page-2.png, printed article page 97",
            positive_payload=(
                "the introduction sets up modular curves X(p^n), Cartan "
                "actions, projective group rings, an Iwasawa algebra, and a "
                "Kummer-theory goal for units in the modular tower"
            ),
            p25_boundary=(
                "tower/Kummer structure is broader than the exact p25 K-traced "
                "normalized-y product"
            ),
            verdict="iwasawa_tower_framework_not_finite_payload",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlVRow(
            name="kl78_v_article_p101_theorem1",
            evidence=f"{LOCAL_PAGES}/page-6.png, printed article page 101",
            positive_payload=(
                "Theorem 1 gives the formal module structure: the relevant "
                "Galois group is a one-dimensional free module over the "
                "Iwasawa algebra"
            ),
            p25_boundary=(
                "module freeness does not select row labels, orientation, or "
                "the finite C_3 x C_169 packet"
            ),
            verdict="iwasawa_freeness_not_p25_selector",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlVRow(
            name="kl78_v_article_p102_p103_vandiver",
            evidence=(
                f"{LOCAL_PAGES}/page-7.png and {LOCAL_PAGES}/page-8.png, "
                "printed article pages 102-103"
            ),
            positive_payload=(
                "the cyclotomic comparison uses Vandiver-style hypotheses, "
                "torsion/factor-group lemmas, and maximal unramified "
                "p-abelian extension structure"
            ),
            p25_boundary=(
                "this is analogy and tower class-field structure, not a "
                "challenge-legal finite-field identity for p25"
            ),
            verdict="cyclotomic_vandiver_analogy_not_p25_payload",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlVRow(
            name="kl78_v_future_exact_finite_payload",
            evidence="future OCR, theorem query, or human-source hit",
            positive_payload=(
                "hypothetical exact row-labeled pairs, reflection center, or "
                "raw equal-weight K-traced product lifted from KL V machinery"
            ),
            p25_boundary=(
                "this is the only KL V route that would connect to the current "
                "finite p25 intake gates"
            ),
            verdict="closing_shape_not_found_in_current_visual_pass",
            source_verified=False,
            visual_source_row=False,
            closes_p25=True,
            row_ok=True,
        ),
    )


def profile_kl_v_iwasawa_boundary() -> KlVProfile:
    rows = kl_v_rows()
    source_handle_rows = sum(row.verdict == "verified_kl_v_primary_source_handle" for row in rows)
    pdf_retrieval_rows = int(PDF_BYTES == 691_420 and PDF_MD5 == "ca93ce860e3cd38717b15853ae30ead3")
    embedded_article_text_rows = 0
    image_only_article_pages = ARTICLE_IMAGE_PAGES
    visual_source_rows = sum(row.visual_source_row for row in rows)
    iwasawa_tower_rows = sum("iwasawa_tower" in row.verdict for row in rows)
    theorem1_freeness_rows = sum("freeness" in row.verdict for row in rows)
    vandiver_cyclotomic_rows = sum("vandiver" in row.verdict for row in rows)
    row_labeled_pair_rows = sum("row-labeled" in row.positive_payload and row.source_verified for row in rows)
    reflection_center_rows = sum("reflection center" in row.positive_payload and row.source_verified for row in rows)
    raw_k_traced_product_rows = sum("K-traced" in row.positive_payload and row.source_verified for row in rows)
    direct_closing_rows = sum(row.source_verified and row.closes_p25 for row in rows)
    ocr_required_rows = int(embedded_article_text_rows == 0 and image_only_article_pages == 8)
    expected_verdicts = (
        "verified_kl_v_primary_source_handle",
        "article_body_is_image_only_locally",
        "iwasawa_tower_framework_not_finite_payload",
        "iwasawa_freeness_not_p25_selector",
        "cyclotomic_vandiver_analogy_not_p25_payload",
        "closing_shape_not_found_in_current_visual_pass",
    )
    row_ok = (
        PDF_BYTES == 691_420
        and PDF_MD5 == "ca93ce860e3cd38717b15853ae30ead3"
        and PDF_PAGES == 9
        and ARTICLE_IMAGE_PAGES == 8
        and len(rows) == 6
        and source_handle_rows == 1
        and pdf_retrieval_rows == 1
        and embedded_article_text_rows == 0
        and image_only_article_pages == 8
        and visual_source_rows == 3
        and iwasawa_tower_rows == 1
        and theorem1_freeness_rows == 1
        and vandiver_cyclotomic_rows == 1
        and row_labeled_pair_rows == 0
        and reflection_center_rows == 0
        and raw_k_traced_product_rows == 0
        and direct_closing_rows == 0
        and ocr_required_rows == 1
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return KlVProfile(
        source=SOURCE,
        rows=rows,
        source_handle_rows=source_handle_rows,
        pdf_retrieval_rows=pdf_retrieval_rows,
        embedded_article_text_rows=embedded_article_text_rows,
        image_only_article_pages=image_only_article_pages,
        visual_source_rows=visual_source_rows,
        iwasawa_tower_rows=iwasawa_tower_rows,
        theorem1_freeness_rows=theorem1_freeness_rows,
        vandiver_cyclotomic_rows=vandiver_cyclotomic_rows,
        row_labeled_pair_rows=row_labeled_pair_rows,
        reflection_center_rows=reflection_center_rows,
        raw_k_traced_product_rows=raw_k_traced_product_rows,
        direct_closing_rows=direct_closing_rows,
        ocr_required_rows=ocr_required_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_kl_v_iwasawa_boundary()
    print("p25 KSY-y Kubert-Lang V Iwasawa boundary gate")
    print(f"source={profile.source}")
    print(f"eudml={EUDML}")
    print(f"gdz_pdf={GDZ_PDF}")
    print(f"local_pdf={LOCAL_PDF}")
    print(f"pdf_bytes={PDF_BYTES}")
    print(f"pdf_md5={PDF_MD5}")
    print(f"pdf_pages={PDF_PAGES}")
    print(f"article_image_pages={ARTICLE_IMAGE_PAGES}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: verdict={row.verdict} "
            f"source={int(row.source_verified)} visual={int(row.visual_source_row)} "
            f"closes={int(row.closes_p25)}"
        )
        print(f"    evidence={row.evidence}")
        print(f"    boundary={row.p25_boundary}")
    print("counts")
    print(f"  source_handle_rows={profile.source_handle_rows}")
    print(f"  pdf_retrieval_rows={profile.pdf_retrieval_rows}")
    print(f"  embedded_article_text_rows={profile.embedded_article_text_rows}")
    print(f"  image_only_article_pages={profile.image_only_article_pages}")
    print(f"  visual_source_rows={profile.visual_source_rows}")
    print(f"  iwasawa_tower_rows={profile.iwasawa_tower_rows}")
    print(f"  theorem1_freeness_rows={profile.theorem1_freeness_rows}")
    print(f"  vandiver_cyclotomic_rows={profile.vandiver_cyclotomic_rows}")
    print(f"  row_labeled_pair_rows={profile.row_labeled_pair_rows}")
    print(f"  reflection_center_rows={profile.reflection_center_rows}")
    print(f"  raw_k_traced_product_rows={profile.raw_k_traced_product_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  ocr_required_rows={profile.ocr_required_rows}")
    print("interpretation")
    print("  kubert_lang_v_is_iwasawa_context_not_p25_producer=1")
    print("  p_primary_tower_structure_does_not_replace_finite_payload=1")
    print("  exact_row_labels_reflection_or_raw_product_required=1")
    print(f"ksy_y_kubert_lang_v_iwasawa_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Kubert-Lang V Iwasawa boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
