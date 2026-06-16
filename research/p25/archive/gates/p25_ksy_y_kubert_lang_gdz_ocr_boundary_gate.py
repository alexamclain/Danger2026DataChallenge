#!/usr/bin/env python3
"""Kubert-Lang GDZ/OCR boundary gate for the p25 KSY-y moonshot.

This records the exact state of the primary-source probe for Kubert-Lang IV:
the GDZ PDF is verified and visually inspected, but the article body is an
image scan locally.  The visible theorem content supports Siegel-unit
generator/dependence language; it does not by itself supply the p25 mixed
C_3 x C_169 row graph, reflection center, or raw equal-weight K-traced product.
"""

from __future__ import annotations

from dataclasses import dataclass


SOURCE = "Kubert-Lang, Units in the Modular Function Field IV"
EUDML = "https://eudml.org/doc/162977"
GDZ_PDF = "https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0227/LOG_0038.pdf"
LOCAL_PDF = "/tmp/p25_lit_scout/kubert_lang_1977_probe/LOG_0038.pdf"
LOCAL_TEXT = "/tmp/p25_lit_scout/kubert_lang_1977_probe/LOG_0038_pypdf_text.txt"
LOCAL_PAGES = "/tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all"
PDF_MD5 = "1a1e75393a31bdb8f921b0169d819562"
PDF_BYTES = 1_596_008
PDF_PAGES = 21
ARTICLE_IMAGE_PAGES = 20


@dataclass(frozen=True)
class KlGdzRow:
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
class KlGdzProfile:
    source: str
    rows: tuple[KlGdzRow, ...]
    pdf_retrieval_rows: int
    render_rows: int
    embedded_article_text_rows: int
    image_only_article_pages: int
    visual_source_rows: int
    generator_language_rows: int
    multiplicative_dependence_rows: int
    delta_dependence_rows: int
    row_labeled_pair_rows: int
    reflection_center_rows: int
    raw_k_traced_product_rows: int
    direct_closing_rows: int
    ocr_required_rows: int
    row_ok: bool


def kl_gdz_rows() -> tuple[KlGdzRow, ...]:
    return (
        KlGdzRow(
            name="kl77_gdz_pdf_handle",
            evidence=(
                f"{GDZ_PDF}; local={LOCAL_PDF}; bytes={PDF_BYTES}; "
                f"md5={PDF_MD5}; pdf_pages={PDF_PAGES}"
            ),
            positive_payload=(
                "EuDML/GDZ handle and Math. Ann. 227 (1977), 223-242 article "
                "range are verified"
            ),
            p25_boundary=(
                "source identity still has to emit exact p25 finite data; a "
                "bibliographic handle is not a theorem payload"
            ),
            verdict="verified_primary_source_handle",
            source_verified=True,
            visual_source_row=False,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_pypdf_image_only_body",
            evidence=(
                f"{LOCAL_TEXT}; page 1 has GDZ/license text, pages 2-21 "
                "extract only page-number-sized text"
            ),
            positive_payload=(
                "local extraction boundary is explicit and reproducible"
            ),
            p25_boundary=(
                "theorem-body search now needs visual inspection, OCR, or an "
                "alternate text source"
            ),
            verdict="article_body_is_image_only_locally",
            source_verified=True,
            visual_source_row=False,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_article_p223_generator_context",
            evidence=f"{LOCAL_PAGES}/page-02.png, printed article page 223",
            positive_payload=(
                "introduction frames the paper as a proof that Siegel functions "
                "generate modular units modulo constants, using q-expansion "
                "and product/root methods"
            ),
            p25_boundary=(
                "generator language alone is exponent hygiene, not the mixed "
                "C_3 x C_169 selector or exact product P"
            ),
            verdict="generator_framework_not_p25_payload",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_article_p224_siegel_function_setup",
            evidence=f"{LOCAL_PAGES}/page-03.png, printed article page 224",
            positive_payload=(
                "the setup defines Siegel functions as powers of Klein forms, "
                "records modularity up to constants, and invokes distribution"
            ),
            p25_boundary=(
                "these are valid source coordinates but do not provide row "
                "labels, a reflection center, or raw K-traced equality"
            ),
            verdict="setup_language_not_row_labeled_payload",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_article_p239_p240_multiplicative_dependence",
            evidence=(
                f"{LOCAL_PAGES}/page-18.png and {LOCAL_PAGES}/page-19.png, "
                "printed article pages 239-240"
            ),
            positive_payload=(
                "the proof records constant products of Siegel functions, "
                "distribution, lower-level induction, and prime-power "
                "independence/dependence criteria"
            ),
            p25_boundary=(
                "the criteria constrain denominators and exponents globally; "
                "they do not select the p25 row graph or orientation"
            ),
            verdict="multiplicative_dependence_not_mixed_graph_selector",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_article_p241_p242_delta_dependence",
            evidence=(
                f"{LOCAL_PAGES}/page-20.png and {LOCAL_PAGES}/page-21.png, "
                "printed article pages 241-242"
            ),
            positive_payload=(
                "the final section states when Delta belongs to the group "
                "generated by Klein forms and summarizes the prime-power "
                "unit-group result"
            ),
            p25_boundary=(
                "Delta/Klein-form generation is still a modular-unit "
                "generation statement, not a finite p25 producer"
            ),
            verdict="delta_dependence_not_p25_payload",
            source_verified=True,
            visual_source_row=True,
            closes_p25=False,
            row_ok=True,
        ),
        KlGdzRow(
            name="kl77_future_exact_row_payload",
            evidence="future OCR, sequel, theorem query, or human-source hit",
            positive_payload=(
                "hypothetical exact row-labeled pairs, reflection center, or "
                "raw equal-weight K-traced product"
            ),
            p25_boundary=(
                "this is the required closing shape before DANGER3 extraction "
                "and official verification"
            ),
            verdict="closing_shape_not_found_in_current_visual_pass",
            source_verified=False,
            visual_source_row=False,
            closes_p25=True,
            row_ok=True,
        ),
    )


def profile_kl_gdz_ocr_boundary() -> KlGdzProfile:
    rows = kl_gdz_rows()
    pdf_retrieval_rows = sum(row.verdict == "verified_primary_source_handle" for row in rows)
    render_rows = int(all(row.source_verified for row in rows[:6]) and ARTICLE_IMAGE_PAGES == 20)
    embedded_article_text_rows = 0
    image_only_article_pages = ARTICLE_IMAGE_PAGES
    visual_source_rows = sum(row.visual_source_row for row in rows)
    generator_language_rows = sum("generator" in row.verdict for row in rows)
    multiplicative_dependence_rows = sum("multiplicative_dependence" in row.name for row in rows)
    delta_dependence_rows = sum("delta_dependence" in row.name for row in rows)
    row_labeled_pair_rows = sum("row-labeled" in row.positive_payload and row.source_verified for row in rows)
    reflection_center_rows = sum("reflection center" in row.positive_payload and row.source_verified for row in rows)
    raw_k_traced_product_rows = sum("K-traced" in row.positive_payload and row.source_verified for row in rows)
    direct_closing_rows = sum(row.source_verified and row.closes_p25 for row in rows)
    ocr_required_rows = int(embedded_article_text_rows == 0 and image_only_article_pages == 20)
    expected_verdicts = (
        "verified_primary_source_handle",
        "article_body_is_image_only_locally",
        "generator_framework_not_p25_payload",
        "setup_language_not_row_labeled_payload",
        "multiplicative_dependence_not_mixed_graph_selector",
        "delta_dependence_not_p25_payload",
        "closing_shape_not_found_in_current_visual_pass",
    )
    row_ok = (
        PDF_BYTES == 1_596_008
        and PDF_MD5 == "1a1e75393a31bdb8f921b0169d819562"
        and PDF_PAGES == 21
        and ARTICLE_IMAGE_PAGES == 20
        and len(rows) == 7
        and pdf_retrieval_rows == 1
        and render_rows == 1
        and embedded_article_text_rows == 0
        and image_only_article_pages == 20
        and visual_source_rows == 4
        and generator_language_rows == 1
        and multiplicative_dependence_rows == 1
        and delta_dependence_rows == 1
        and row_labeled_pair_rows == 0
        and reflection_center_rows == 0
        and raw_k_traced_product_rows == 0
        and direct_closing_rows == 0
        and ocr_required_rows == 1
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return KlGdzProfile(
        source=SOURCE,
        rows=rows,
        pdf_retrieval_rows=pdf_retrieval_rows,
        render_rows=render_rows,
        embedded_article_text_rows=embedded_article_text_rows,
        image_only_article_pages=image_only_article_pages,
        visual_source_rows=visual_source_rows,
        generator_language_rows=generator_language_rows,
        multiplicative_dependence_rows=multiplicative_dependence_rows,
        delta_dependence_rows=delta_dependence_rows,
        row_labeled_pair_rows=row_labeled_pair_rows,
        reflection_center_rows=reflection_center_rows,
        raw_k_traced_product_rows=raw_k_traced_product_rows,
        direct_closing_rows=direct_closing_rows,
        ocr_required_rows=ocr_required_rows,
        row_ok=row_ok,
    )


def print_row(row: KlGdzRow) -> None:
    print(
        "  "
        f"{row.name}: verdict={row.verdict} "
        f"source={int(row.source_verified)} visual={int(row.visual_source_row)} "
        f"closes={int(row.closes_p25)}"
    )
    print(f"    evidence={row.evidence}")
    print(f"    boundary={row.p25_boundary}")


def main() -> int:
    profile = profile_kl_gdz_ocr_boundary()
    print("p25 KSY-y Kubert-Lang GDZ/OCR boundary gate")
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
        print_row(row)
    print("counts")
    print(f"  pdf_retrieval_rows={profile.pdf_retrieval_rows}")
    print(f"  render_rows={profile.render_rows}")
    print(f"  embedded_article_text_rows={profile.embedded_article_text_rows}")
    print(f"  image_only_article_pages={profile.image_only_article_pages}")
    print(f"  visual_source_rows={profile.visual_source_rows}")
    print(f"  generator_language_rows={profile.generator_language_rows}")
    print(f"  multiplicative_dependence_rows={profile.multiplicative_dependence_rows}")
    print(f"  delta_dependence_rows={profile.delta_dependence_rows}")
    print(f"  row_labeled_pair_rows={profile.row_labeled_pair_rows}")
    print(f"  reflection_center_rows={profile.reflection_center_rows}")
    print(f"  raw_k_traced_product_rows={profile.raw_k_traced_product_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  ocr_required_rows={profile.ocr_required_rows}")
    print("interpretation")
    print("  kubert_lang_iv_is_framework_not_p25_producer=1")
    print("  exact_row_labels_reflection_or_raw_product_required=1")
    print("  full_ocr_or_alternate_text_needed_for_theorem_body_search=1")
    print(f"ksy_y_kubert_lang_gdz_ocr_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Kubert-Lang GDZ/OCR boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
