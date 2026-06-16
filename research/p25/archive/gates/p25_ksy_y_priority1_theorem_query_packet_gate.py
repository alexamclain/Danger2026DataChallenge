#!/usr/bin/env python3
"""Priority-1 theorem-query packet for the p25 KSY-y moonshot.

The Sprang and KSY source splits say which source handles are still live.  This
gate turns that into an artifact-gated query packet: exact questions to ask of
each source, the first falsifier, and the local probe that should classify any
claimed theorem snippet.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class Priority1QueryRow:
    name: str
    source_url: str
    source_handle: str
    exact_question: str
    positive_artifact: str
    first_falsifier: str
    local_probe: str
    expected_probe_decision: str
    recommendation: str
    row_type: str
    row_ok: bool


@dataclass(frozen=True)
class Priority1TheoremQueryPacketProfile:
    target_product: str
    rows: tuple[Priority1QueryRow, ...]
    source_query_rows: int
    closing_query_rows: int
    context_only_rows: int
    rejected_shadow_rows: int
    all_rows_have_probe: bool
    row_ok: bool


def query_rows() -> tuple[Priority1QueryRow, ...]:
    exact_product_probe = (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py "
        "--candidate --exact-product --mixed-graph --equal-weight --orientation "
        "--arithmetic-producer --challenge-legal --finite-intake"
    )
    return (
        Priority1QueryRow(
            name="sprang_1801_kronecker_exact_product_query",
            source_url="https://arxiv.org/abs/1801.05677",
            source_handle="Sprang, Eisenstein-Kronecker series via the Poincare bundle",
            exact_question=(
                "Is there a Kronecker-section, distribution, or Eisenstein-Kronecker "
                "clause that specializes at D=2 to the exact p25 product P or to "
                "theta2/theta2^-1 divisor data?"
            ),
            positive_artifact=(
                "theorem/proposition/equation number plus a map to C=(47,28), "
                "D=(22,3), K=(57,0), equal weights, and orientation"
            ),
            first_falsifier=(
                "Eisenstein-Kronecker or distribution vocabulary without exact "
                "C/D/K product specialization"
            ),
            local_probe=exact_product_probe + " --anchor sprang_prop_5_4_kato_siegel_dlog",
            expected_probe_decision="closing_exact_product_identity",
            recommendation="continue_first_on_exact_clause_only",
            row_type="closing_query",
            row_ok=True,
        ),
        Priority1QueryRow(
            name="sprang_1802_derham_exact_differential_query",
            source_url="https://arxiv.org/abs/1802.04996",
            source_handle=(
                "Sprang, The algebraic de Rham realization of the elliptic "
                "polylogarithm via the Poincare bundle"
            ),
            exact_question=(
                "Is there an algebraic de Rham polylogarithm or Eisenstein-class "
                "differential-form clause whose D=2 specialization emits exact P "
                "or theta2/theta2^-1 divisor data?"
            ),
            positive_artifact=(
                "explicit differential/additive identity, not just a representative "
                "of a cohomology class, with the p25 mixed graph preserved"
            ),
            first_falsifier=(
                "polylogarithm/Eisenstein-class representative with no exact "
                "anti-invariant normalized-y product output"
            ),
            local_probe=exact_product_probe + " --anchor sprang_prop_5_4_kato_siegel_dlog",
            expected_probe_decision="closing_exact_product_identity",
            recommendation="continue_first_on_exact_clause_only",
            row_type="closing_query",
            row_ok=True,
        ),
        Priority1QueryRow(
            name="ksy_eq_3_4_exact_product_distribution_query",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon Equation (3.4) normalized-y/Siegel formula",
            exact_question=(
                "Does the normalized-y formula y(Q)=-g(2Q)/g(Q)^4 come with a "
                "distribution/product theorem selecting all 75 p25 atoms in P?"
            ),
            positive_artifact=(
                "exact K-traced normalized-y product theorem, or theta2/theta2^-1 "
                "divisor/additive data, with mixed graph and orientation"
            ),
            first_falsifier=(
                "formula language only, one y-value, or broad class-field "
                "generation without exact P"
            ),
            local_probe=exact_product_probe + " --anchor ksy_normalized_y_siegel_formula",
            expected_probe_decision="closing_exact_product_identity",
            recommendation="continue_first_on_exact_clause_only",
            row_type="closing_query",
            row_ok=True,
        ),
        Priority1QueryRow(
            name="ksy_theorem_5_3_generation_shadow",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon Theorem 5.3 ray-class generation",
            exact_question=(
                "Can the generation theorem be strengthened into an exact product "
                "identity for P?  If not, it is not a priority-1 closer."
            ),
            positive_artifact="only an upgraded exact product theorem counts",
            first_falsifier="generation of K(N) or torsion data without exact P",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py "
                "--candidate --anchor ksy_normalized_y_siegel_formula --output-kind field-generation"
            ),
            expected_probe_decision="reject_field_generation_not_product_identity",
            recommendation="kill_as_direct_closer",
            row_type="rejected_shadow",
            row_ok=True,
        ),
        Priority1QueryRow(
            name="ksy_theorem_6_2_corollary_6_4_single_value_shadow",
            source_url="https://arxiv.org/abs/1007.2307",
            source_handle="Koo-Shin-Yoon Theorem 6.2 / Corollary 6.4 single-y invariant",
            exact_question=(
                "Can the single-y invariant output be upgraded to exact P and the "
                "mixed C_3 x C_169 graph?  If not, it remains context only."
            ),
            positive_artifact="exact P plus mixed graph; single-value generation is not enough",
            first_falsifier="single y(0,1/N)-style invariant without the K-traced product",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py "
                "--candidate --name ksy_single_y_value --anchor ksy_normalized_y_siegel_formula "
                "--output-kind value --finite-field"
            ),
            expected_probe_decision="conditional_missing_exact_product",
            recommendation="keep_as_context_only_until_exact_product",
            row_type="context_only",
            row_ok=True,
        ),
    )


def profile_priority1_theorem_query_packet() -> Priority1TheoremQueryPacketProfile:
    rows = query_rows()
    source_query_rows = len(rows)
    closing_query_rows = sum(int(row.row_type == "closing_query") for row in rows)
    context_only_rows = sum(int(row.row_type == "context_only") for row in rows)
    rejected_shadow_rows = sum(int(row.row_type == "rejected_shadow") for row in rows)
    all_rows_have_probe = all(
        "python3" in row.local_probe
        and row.expected_probe_decision
        and row.recommendation
        for row in rows
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and source_query_rows == 5
        and closing_query_rows == 3
        and context_only_rows == 1
        and rejected_shadow_rows == 1
        and all_rows_have_probe
        and all(row.row_ok for row in rows)
        and tuple(row.expected_probe_decision for row in rows)
        == (
            "closing_exact_product_identity",
            "closing_exact_product_identity",
            "closing_exact_product_identity",
            "reject_field_generation_not_product_identity",
            "conditional_missing_exact_product",
        )
    )
    return Priority1TheoremQueryPacketProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        source_query_rows=source_query_rows,
        closing_query_rows=closing_query_rows,
        context_only_rows=context_only_rows,
        rejected_shadow_rows=rejected_shadow_rows,
        all_rows_have_probe=all_rows_have_probe,
        row_ok=row_ok,
    )


def print_row(row: Priority1QueryRow) -> None:
    print(
        "  "
        f"{row.name}: type={row.row_type} source={row.source_handle} "
        f"expected={row.expected_probe_decision} falsifier={row.first_falsifier} "
        f"recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_priority1_theorem_query_packet()
    print("p25 KSY-y priority-1 theorem-query packet gate")
    print(f"target_product={profile.target_product}")
    print("query_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  source_query_rows={profile.source_query_rows}")
    print(f"  closing_query_rows={profile.closing_query_rows}")
    print(f"  context_only_rows={profile.context_only_rows}")
    print(f"  rejected_shadow_rows={profile.rejected_shadow_rows}")
    print(f"  all_rows_have_probe={int(profile.all_rows_have_probe)}")
    print("interpretation")
    print("  priority1_lit_search_is_now_snippet_query_gated=1")
    print("  three_queries_would_close_if_the_exact_product_clause_exists=1")
    print("  ksy_generation_and_single_value_outputs_do_not_close_without_exact_P=1")
    print(f"ksy_y_priority1_theorem_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 theorem-query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
