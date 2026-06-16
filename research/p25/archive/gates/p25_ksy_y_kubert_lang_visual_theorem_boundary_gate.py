#!/usr/bin/env python3
"""Visual theorem boundary for the active KL/KSY exact-product lane.

Local OCR is unavailable in the current environment, but the rendered KL IV/V
pages are readable enough for a targeted theorem pass.  This gate records that
pass in executable form so future work does not have to reopen the image pages
just to rediscover that the visible theorem statements are dependence/freeness
results rather than exact p25 finite-product producers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


KL_IV_ROOT = Path("/tmp/p25_lit_scout/kubert_lang_1977_probe/pages_all")
KL_V_ROOT = Path("/tmp/p25_lit_scout/kubert_lang_v_probe/pages_log0016")


@dataclass(frozen=True)
class VisualTheoremRow:
    source: str
    theorem: str
    article_page: int
    local_image: Path
    visible_content: str
    positive_use: str
    direct_p25_payload: bool
    first_missing_clause: str
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class KlVisualTheoremBoundaryProfile:
    rows: tuple[VisualTheoremRow, ...]
    image_rows_present: int
    kl_iv_theorem_rows: int
    kl_v_theorem_or_lemma_rows: int
    dependence_or_freeness_rows: int
    exact_row_label_rows: int
    reflection_center_rows: int
    raw_k_traced_product_rows: int
    direct_closing_rows: int
    ocr_upgrade_still_useful: bool
    row_ok: bool


def theorem_rows() -> tuple[VisualTheoremRow, ...]:
    rows = (
        VisualTheoremRow(
            source="Kubert-Lang IV",
            theorem="Theorem 6",
            article_page=239,
            local_image=KL_IV_ROOT / "page-18.png",
            visible_content=(
                "multiplicative dependence criterion for products of Siegel "
                "functions that are constant/modular"
            ),
            positive_use="necessary dependence and modularity language for KL-style products",
            direct_p25_payload=False,
            first_missing_clause="exact C3 x C169 row labels, orientation, and arithmetic producer",
            decision="kill_dependence_criterion_as_direct_p25_closer",
            row_ok=True,
        ),
        VisualTheoremRow(
            source="Kubert-Lang IV",
            theorem="Theorem 7",
            article_page=240,
            local_image=KL_IV_ROOT / "page-19.png",
            visible_content=(
                "prime-power multiplicative independence modulo constants for "
                "g_a with a in Z(p^n)^*"
            ),
            positive_use="prime-power independence control for Siegel-function products",
            direct_p25_payload=False,
            first_missing_clause="mixed C3 x C169 selector rather than prime-power independence",
            decision="kill_prime_power_independence_as_direct_p25_closer",
            row_ok=True,
        ),
        VisualTheoremRow(
            source="Kubert-Lang IV",
            theorem="Theorem 8 / Lemma 6.1",
            article_page=241,
            local_image=KL_IV_ROOT / "page-20.png",
            visible_content=(
                "Delta/Klein-form dependence and prime-power generated-unit criterion"
            ),
            positive_use="Delta/Klein-form group-generation boundary at prime powers",
            direct_p25_payload=False,
            first_missing_clause="finite p25 row-labeled P/theta2 or raw K-traced product",
            decision="kill_delta_generation_as_direct_p25_closer",
            row_ok=True,
        ),
        VisualTheoremRow(
            source="Kubert-Lang V",
            theorem="Theorem 1",
            article_page=101,
            local_image=KL_V_ROOT / "page-6.png",
            visible_content="G is a one-dimensional free module over the Iwasawa algebra",
            positive_use="p-primary tower/Kummer structure context",
            direct_p25_payload=False,
            first_missing_clause="finite row labels, reflection center, or raw product payload",
            decision="kill_iwasawa_freeness_as_direct_p25_closer",
            row_ok=True,
        ),
        VisualTheoremRow(
            source="Kubert-Lang V",
            theorem="Lemma 1",
            article_page=102,
            local_image=KL_V_ROOT / "page-7.png",
            visible_content="factor group V_m/V_n has no torsion for m >= n",
            positive_use="tower torsion-control context",
            direct_p25_payload=False,
            first_missing_clause="exact mixed graph or finite product theorem",
            decision="kill_tower_torsion_control_as_direct_p25_closer",
            row_ok=True,
        ),
        VisualTheoremRow(
            source="Kubert-Lang V",
            theorem="Lemma 2 / conclusion",
            article_page=103,
            local_image=KL_V_ROOT / "page-8.png",
            visible_content=(
                "maximal unramified p-abelian extension and Vandiver/Iwasawa "
                "cyclicity conclusion"
            ),
            positive_use="class-field/Kummer analogy only",
            direct_p25_payload=False,
            first_missing_clause="challenge-legal finite-field identity for p25",
            decision="kill_unramified_extension_structure_as_direct_p25_closer",
            row_ok=True,
        ),
    )
    return rows


def profile_kl_visual_theorem_boundary() -> KlVisualTheoremBoundaryProfile:
    rows = theorem_rows()
    image_rows_present = sum(row.local_image.exists() and row.local_image.stat().st_size > 0 for row in rows)
    kl_iv = sum(row.source == "Kubert-Lang IV" for row in rows)
    kl_v = sum(row.source == "Kubert-Lang V" for row in rows)
    dependence_or_freeness = sum(
        any(token in row.decision for token in ("dependence", "independence", "freeness", "torsion", "unramified", "delta"))
        for row in rows
    )
    exact_row_label_rows = sum("row label" in row.visible_content.lower() for row in rows)
    reflection_center_rows = sum("reflection center" in row.visible_content.lower() for row in rows)
    raw_product_rows = sum("raw" in row.visible_content.lower() and "product" in row.visible_content.lower() for row in rows)
    direct_closing = sum(row.direct_p25_payload for row in rows)
    row_ok = (
        len(rows) == 6
        and image_rows_present == 6
        and kl_iv == 3
        and kl_v == 3
        and dependence_or_freeness == 6
        and exact_row_label_rows == 0
        and reflection_center_rows == 0
        and raw_product_rows == 0
        and direct_closing == 0
        and all(row.row_ok for row in rows)
    )
    return KlVisualTheoremBoundaryProfile(
        rows=rows,
        image_rows_present=image_rows_present,
        kl_iv_theorem_rows=kl_iv,
        kl_v_theorem_or_lemma_rows=kl_v,
        dependence_or_freeness_rows=dependence_or_freeness,
        exact_row_label_rows=exact_row_label_rows,
        reflection_center_rows=reflection_center_rows,
        raw_k_traced_product_rows=raw_product_rows,
        direct_closing_rows=direct_closing,
        ocr_upgrade_still_useful=True,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_kl_visual_theorem_boundary()
    print("p25 KSY-y Kubert-Lang visual theorem-boundary gate")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.source} {row.theorem} p{row.article_page}: "
            f"image={row.local_image} closes={int(row.direct_p25_payload)} "
            f"decision={row.decision}"
        )
        print(f"    visible={row.visible_content}")
        print(f"    missing={row.first_missing_clause}")
    print("counts")
    print(f"  image_rows_present={profile.image_rows_present}")
    print(f"  kl_iv_theorem_rows={profile.kl_iv_theorem_rows}")
    print(f"  kl_v_theorem_or_lemma_rows={profile.kl_v_theorem_or_lemma_rows}")
    print(f"  dependence_or_freeness_rows={profile.dependence_or_freeness_rows}")
    print(f"  exact_row_label_rows={profile.exact_row_label_rows}")
    print(f"  reflection_center_rows={profile.reflection_center_rows}")
    print(f"  raw_k_traced_product_rows={profile.raw_k_traced_product_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  ocr_upgrade_still_useful={int(profile.ocr_upgrade_still_useful)}")
    print("interpretation")
    print("  KL_IV_visible_theorems_are_dependence_generation_not_p25_payload=1")
    print("  KL_V_visible_theorems_are_iwasawa_tower_context_not_p25_payload=1")
    print("  active_KL_lane_still_needs_exact_row_labels_reflection_or_raw_product=1")
    print(f"ksy_y_kubert_lang_visual_theorem_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Kubert-Lang visual theorem boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
