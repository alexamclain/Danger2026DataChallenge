#!/usr/bin/env python3
"""Primary-source verdict gate for the p25 priority-1 KSY-y moonshot.

The theorem-query packet asked whether Sprang 1801/1802 or KSY 1007 contains
an exact theorem that closes the p25 anti-invariant normalized-y product.  This
gate records the first direct source pass: which theorem blocks were inspected,
what they positively give, and which missing clause keeps them from closing.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class PrimarySourceVerdictRow:
    name: str
    source_url: str
    source_handle: str
    inspected_clause: str
    local_source_window: str
    positive_payload: str
    verdict: str
    first_missing_clause: str
    recommendation: str
    closes_priority1: bool
    row_ok: bool


@dataclass(frozen=True)
class Priority1PrimarySourceVerdictProfile:
    target_product: str
    rows: tuple[PrimarySourceVerdictRow, ...]
    inspected_source_rows: int
    exact_formula_rows: int
    distribution_rows: int
    field_generation_rows: int
    direct_closing_rows: int
    continue_rows: int
    kill_as_direct_closer_rows: int
    all_rows_have_missing_clause: bool
    row_ok: bool


def verdict_rows() -> tuple[PrimarySourceVerdictRow, ...]:
    return (
        PrimarySourceVerdictRow(
            name="sprang_1801_kronecker_distribution_relation",
            source_url="https://arxiv.org/abs/1801.05677",
            source_handle="Sprang 1801, Eisenstein-Kronecker series via the Poincare bundle",
            inspected_clause=(
                "Appendix distribution relation for the Kronecker section and its "
                "isogeny/torsion corollaries"
            ),
            local_source_window=(
                "/tmp/p25_lit_scout/1801.05677/PaperEisensteinPoincare.tex:"
                "1714-1798"
            ),
            positive_payload=(
                "genuine additive distribution relation for translated Kronecker "
                "sections, including sums over torsion and isogeny kernels"
            ),
            verdict="conditional_additive_section_distribution_not_exact_P",
            first_missing_clause=(
                "specialization from the additive section identity to the exact "
                "finite K-traced normalized-y product P, with mixed graph and "
                "orientation"
            ),
            recommendation="continue_only_if_exact_product_specialization_is_found",
            closes_priority1=False,
            row_ok=True,
        ),
        PrimarySourceVerdictRow(
            name="sprang_1802_d_variant_distribution",
            source_url="https://arxiv.org/abs/1802.04996",
            source_handle=(
                "Sprang 1802, de Rham realization of the elliptic polylogarithm "
                "via the Poincare bundle"
            ),
            inspected_clause=(
                "D-variant Kronecker section, imported distribution relation, and "
                "Kato-Siegel logarithmic derivative comparison"
            ),
            local_source_window=(
                "/tmp/p25_lit_scout/1802.04996/deRhamRealization.tex:1100-1182"
            ),
            positive_payload=(
                "connects the D-variant Kronecker section to an additive "
                "distribution relation and to dlog theta_D in the Kato-Siegel "
                "setting"
            ),
            verdict="conditional_derham_dlog_not_d2_product",
            first_missing_clause=(
                "D=2 multiplicative product identity; the displayed Kato-Siegel "
                "function comparison is stated under a prime-to-6 condition, so "
                "it does not by itself certify the p25 theta2 product"
            ),
            recommendation="continue_as_source_vocabulary_not_as_closer",
            closes_priority1=False,
            row_ok=True,
        ),
        PrimarySourceVerdictRow(
            name="sprang_1802_derham_eisenstein_class_formula",
            source_url="https://arxiv.org/abs/1802.04996",
            source_handle=(
                "Sprang 1802, de Rham Eisenstein-class specialization formula"
            ),
            inspected_clause=(
                "specialization of the de Rham polylogarithm to Eisenstein "
                "classes using sums of Eisenstein-Kronecker series"
            ),
            local_source_window=(
                "/tmp/p25_lit_scout/1802.04996/deRhamRealization.tex:1645-1708"
            ),
            positive_payload=(
                "explicit cohomology/Eisenstein-series formula after applying "
                "translation compatibility and the distribution relation"
            ),
            verdict="cohomology_eisenstein_class_not_finite_product",
            first_missing_clause=(
                "finite multiplicative normalized-y product or theta2/theta2^-1 "
                "divisor payload over the p25 C,D,K atoms"
            ),
            recommendation="kill_as_direct_closer_keep_as_context",
            closes_priority1=False,
            row_ok=True,
        ),
        PrimarySourceVerdictRow(
            name="ksy_equation_3_4_normalized_y_formula",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon 1007, normalized-y/Siegel formula",
            inspected_clause="Equation (3.4) normalized y-coordinate formula",
            local_source_window="/tmp/p25_lit_scout/1007.2307/source.tex:420-466",
            positive_payload=(
                "exact atomic formula y_(r1,r2)=-g_(2r1,2r2)/g_(r1,r2)^4"
            ),
            verdict="formula_language_not_product_distribution",
            first_missing_clause=(
                "distribution/product theorem selecting the 75 atoms of P with "
                "the required signs, trace graph, and arithmetic producer"
            ),
            recommendation="continue_only_if_upgraded_to_exact_product_theorem",
            closes_priority1=False,
            row_ok=True,
        ),
        PrimarySourceVerdictRow(
            name="ksy_main_theorem_torsion_generation",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon 1007, main torsion-generation theorem",
            inspected_clause=(
                "Theorem 5.3-style generation of a ray class field by a torsion "
                "point using x and y"
            ),
            local_source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1000-1080",
            positive_payload=(
                "field-generation theorem for a single torsion point and its "
                "normalized y-coordinate"
            ),
            verdict="field_generation_not_product_identity",
            first_missing_clause=(
                "an equality for the whole p25 anti-invariant product P, not just "
                "generation of K_(N)"
            ),
            recommendation="kill_as_direct_closer",
            closes_priority1=False,
            row_ok=True,
        ),
        PrimarySourceVerdictRow(
            name="ksy_schertz_single_value_generator",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon 1007, Schertz-style primitive generator",
            inspected_clause=(
                "Theorem 6.2 / Corollary 6.4-style primitive generator from a "
                "single Siegel-Ramachandra ratio or y-value"
            ),
            local_source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1160-1280",
            positive_payload=(
                "single-value generator and Siegel-Ramachandra ratio "
                "g_f(C')/g_f(C0)^4"
            ),
            verdict="single_value_generator_not_k_traced_product",
            first_missing_clause=(
                "upgrade from one generator value to the exact K-traced p25 "
                "product over C+jD+kK"
            ),
            recommendation="keep_as_context_only_until_exact_product",
            closes_priority1=False,
            row_ok=True,
        ),
    )


def profile_priority1_primary_source_verdict() -> Priority1PrimarySourceVerdictProfile:
    rows = verdict_rows()
    inspected_source_rows = len(rows)
    exact_formula_rows = sum("formula" in row.verdict for row in rows)
    distribution_rows = sum(
        "distribution" in row.inspected_clause
        or "distribution" in row.positive_payload
        for row in rows
    )
    field_generation_rows = sum(
        row.verdict
        in {
            "field_generation_not_product_identity",
            "single_value_generator_not_k_traced_product",
        }
        for row in rows
    )
    direct_closing_rows = sum(int(row.closes_priority1) for row in rows)
    continue_rows = sum(row.recommendation.startswith("continue") for row in rows)
    kill_as_direct_closer_rows = sum(
        row.recommendation.startswith("kill") for row in rows
    )
    all_rows_have_missing_clause = all(row.first_missing_clause for row in rows)
    expected_verdicts = (
        "conditional_additive_section_distribution_not_exact_P",
        "conditional_derham_dlog_not_d2_product",
        "cohomology_eisenstein_class_not_finite_product",
        "formula_language_not_product_distribution",
        "field_generation_not_product_identity",
        "single_value_generator_not_k_traced_product",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and inspected_source_rows == 6
        and exact_formula_rows == 1
        and distribution_rows == 3
        and field_generation_rows == 2
        and direct_closing_rows == 0
        and continue_rows == 3
        and kill_as_direct_closer_rows == 2
        and all_rows_have_missing_clause
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return Priority1PrimarySourceVerdictProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        inspected_source_rows=inspected_source_rows,
        exact_formula_rows=exact_formula_rows,
        distribution_rows=distribution_rows,
        field_generation_rows=field_generation_rows,
        direct_closing_rows=direct_closing_rows,
        continue_rows=continue_rows,
        kill_as_direct_closer_rows=kill_as_direct_closer_rows,
        all_rows_have_missing_clause=all_rows_have_missing_clause,
        row_ok=row_ok,
    )


def print_row(row: PrimarySourceVerdictRow) -> None:
    print(
        "  "
        f"{row.name}: verdict={row.verdict} closes={int(row.closes_priority1)} "
        f"recommendation={row.recommendation} missing={row.first_missing_clause}"
    )


def main() -> int:
    profile = profile_priority1_primary_source_verdict()
    print("p25 KSY-y priority-1 primary-source verdict gate")
    print(f"target_product={profile.target_product}")
    print("verdict_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  inspected_source_rows={profile.inspected_source_rows}")
    print(f"  exact_formula_rows={profile.exact_formula_rows}")
    print(f"  distribution_rows={profile.distribution_rows}")
    print(f"  field_generation_rows={profile.field_generation_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  kill_as_direct_closer_rows={profile.kill_as_direct_closer_rows}")
    print(f"  all_rows_have_missing_clause={int(profile.all_rows_have_missing_clause)}")
    print("interpretation")
    print("  primary_sources_have_real_distribution_and_formula_payloads=1")
    print("  primary_sources_do_not_yet_contain_exact_p25_product_theorem=1")
    print("  next_search_must_target_external_exact_product_specialization=1")
    print(f"ksy_y_priority1_primary_source_verdict_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 primary-source verdict regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
