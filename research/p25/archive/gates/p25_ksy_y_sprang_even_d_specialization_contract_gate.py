#!/usr/bin/env python3
"""Sprang even-D specialization contract for the p25 KSY-y moonshot.

Sprang remains the highest-priority open source family after the blocked
Koo-Shin retrieval lane, because his Kronecker-section construction explicitly
has an even-D surface.  This gate records the current boundary: the open TeX
clauses give additive/distribution/cohomology machinery, but not yet the exact
p25 K-traced normalized-y product or theta2 payload.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class SprangEvenDRow:
    name: str
    source_url: str
    local_source_window: str
    source_payload: str
    p25_relevance: str
    missing_clause: str
    verdict: str
    recommendation: str
    source_evidence: bool
    closes_p25: bool
    row_ok: bool


@dataclass(frozen=True)
class SprangEvenDProfile:
    target_product: str
    rows: tuple[SprangEvenDRow, ...]
    source_evidence_rows: int
    even_d_surface_rows: int
    distribution_rows: int
    prime_to_6_blocked_rows: int
    cohomology_output_rows: int
    direct_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    hypothetical_closing_rows: int
    all_rows_have_missing_clause: bool
    row_ok: bool


def sprang_even_d_rows() -> tuple[SprangEvenDRow, ...]:
    return (
        SprangEvenDRow(
            name="sprang_1801_even_d_omega_surface",
            source_url="https://arxiv.org/abs/1801.05677",
            local_source_window=(
                "/tmp/p25_lit_scout/1801.05677/"
                "PaperEisensteinPoincare.tex:771-777,1019-1027"
            ),
            source_payload=(
                "Kronecker-section construction of omega^D does not require "
                "6 coprime to D; when D is coprime to 6 it agrees with "
                "dlog theta_D"
            ),
            p25_relevance=(
                "keeps the D=2 source family alive at the additive/differential "
                "level"
            ),
            missing_clause=(
                "a multiplicative or divisor/additive identity for exact p25 "
                "P or theta2/theta2^-1, not only omega^D language"
            ),
            verdict="conditional_even_d_surface_not_exact_product",
            recommendation="continue_only_with_exact_p25_specialization",
            source_evidence=True,
            closes_p25=False,
            row_ok=True,
        ),
        SprangEvenDRow(
            name="sprang_1801_kronecker_distribution",
            source_url="https://arxiv.org/abs/1801.05677",
            local_source_window=(
                "/tmp/p25_lit_scout/1801.05677/"
                "PaperEisensteinPoincare.tex:1714-1798"
            ),
            source_payload=(
                "general Kronecker-section distribution relation summing over "
                "isogeny kernels and D-torsion translations"
            ),
            p25_relevance=(
                "plausible arithmetic-producer surface, but the displayed "
                "sums are not the p25 three-slice D segment with 25-point K trace"
            ),
            missing_clause=(
                "specialization selecting C=(47,28), D=(22,3), primitive "
                "K=(57,0), equal weights, orientation, and mixed graph"
            ),
            verdict="conditional_distribution_not_p25_mixed_graph",
            recommendation="continue_only_if_row_labeled_specialization_is_found",
            source_evidence=True,
            closes_p25=False,
            row_ok=True,
        ),
        SprangEvenDRow(
            name="sprang_1802_kato_siegel_comparison",
            source_url="https://arxiv.org/abs/1802.04996",
            local_source_window=(
                "/tmp/p25_lit_scout/1802.04996/"
                "deRhamRealization.tex:1105-1182"
            ),
            source_payload=(
                "D-variant Kronecker section and distribution relation; "
                "comparison with Kato-Siegel theta_D is stated under D prime to 6"
            ),
            p25_relevance=(
                "confirms the ordinary theta_D shortcut is blocked at D=2 even "
                "though the Kronecker D-variant remains meaningful"
            ),
            missing_clause=(
                "a D=2 theorem replacing the prime-to-6 theta_D comparison with "
                "the exact p25 theta2/normalized-y payload"
            ),
            verdict="reject_direct_theta_d2_import_keep_even_d_variant",
            recommendation="kill_direct_thetaD2_import_continue_kronecker_variant",
            source_evidence=True,
            closes_p25=False,
            row_ok=True,
        ),
        SprangEvenDRow(
            name="sprang_1802_derham_eisenstein_formula",
            source_url="https://arxiv.org/abs/1802.04996",
            local_source_window=(
                "/tmp/p25_lit_scout/1802.04996/"
                "deRhamRealization.tex:1627-1711"
            ),
            source_payload=(
                "translation compatibility plus distribution yields de Rham "
                "Eisenstein-class formulas in terms of Kato Eisenstein series"
            ),
            p25_relevance=(
                "useful differential-form vocabulary but not a finite "
                "multiplicative normalized-y product"
            ),
            missing_clause=(
                "finite p25 P/theta2 divisor payload or value identity with "
                "period-156 context"
            ),
            verdict="reject_cohomology_formula_as_direct_product",
            recommendation="kill_as_direct_closer_keep_as_context",
            source_evidence=True,
            closes_p25=False,
            row_ok=True,
        ),
        SprangEvenDRow(
            name="sprang_exact_p25_even_d_payload_hypothetical",
            source_url="https://arxiv.org/abs/1801.05677 + https://arxiv.org/abs/1802.04996",
            local_source_window="future theorem/OCR/formula hit",
            source_payload=(
                "hypothetical even-D specialization emits exact P or exact "
                "theta2/theta2^-1 divisor data for the p25 C/D/K atoms"
            ),
            p25_relevance=(
                "would close the priority-1 theorem side before DANGER3 "
                "extraction and vpp.py verification"
            ),
            missing_clause="none for source-theorem lane; extraction remains separate",
            verdict="closing_exact_even_d_p25_payload",
            recommendation="accept_and_route_through_theta2_certificate",
            source_evidence=False,
            closes_p25=True,
            row_ok=True,
        ),
    )


def profile_sprang_even_d_specialization_contract() -> SprangEvenDProfile:
    rows = sprang_even_d_rows()
    source_evidence_rows = sum(int(row.source_evidence) for row in rows)
    even_d_surface_rows = sum(
        row.verdict == "conditional_even_d_surface_not_exact_product"
        for row in rows
    )
    distribution_rows = sum("distribution" in row.verdict for row in rows)
    prime_to_6_blocked_rows = sum("theta_d2" in row.verdict for row in rows)
    cohomology_output_rows = sum("cohomology" in row.verdict for row in rows)
    direct_closing_rows = sum(
        int(row.source_evidence and row.closes_p25) for row in rows
    )
    conditional_rows = sum(row.verdict.startswith("conditional_") for row in rows)
    rejected_rows = sum(row.verdict.startswith("reject_") for row in rows)
    hypothetical_closing_rows = sum(
        int((not row.source_evidence) and row.closes_p25) for row in rows
    )
    all_rows_have_missing_clause = all(row.missing_clause for row in rows)
    expected_verdicts = (
        "conditional_even_d_surface_not_exact_product",
        "conditional_distribution_not_p25_mixed_graph",
        "reject_direct_theta_d2_import_keep_even_d_variant",
        "reject_cohomology_formula_as_direct_product",
        "closing_exact_even_d_p25_payload",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and len(rows) == 5
        and source_evidence_rows == 4
        and even_d_surface_rows == 1
        and distribution_rows == 1
        and prime_to_6_blocked_rows == 1
        and cohomology_output_rows == 1
        and direct_closing_rows == 0
        and conditional_rows == 2
        and rejected_rows == 2
        and hypothetical_closing_rows == 1
        and all_rows_have_missing_clause
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return SprangEvenDProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        source_evidence_rows=source_evidence_rows,
        even_d_surface_rows=even_d_surface_rows,
        distribution_rows=distribution_rows,
        prime_to_6_blocked_rows=prime_to_6_blocked_rows,
        cohomology_output_rows=cohomology_output_rows,
        direct_closing_rows=direct_closing_rows,
        conditional_rows=conditional_rows,
        rejected_rows=rejected_rows,
        hypothetical_closing_rows=hypothetical_closing_rows,
        all_rows_have_missing_clause=all_rows_have_missing_clause,
        row_ok=row_ok,
    )


def print_row(row: SprangEvenDRow) -> None:
    print(
        "  "
        f"{row.name}: verdict={row.verdict} "
        f"source={int(row.source_evidence)} closes={int(row.closes_p25)} "
        f"recommendation={row.recommendation}"
    )
    print(f"    window={row.local_source_window}")
    print(f"    missing={row.missing_clause}")


def main() -> int:
    profile = profile_sprang_even_d_specialization_contract()
    print("p25 KSY-y Sprang even-D specialization contract gate")
    print(f"target_product={profile.target_product}")
    print("rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  source_evidence_rows={profile.source_evidence_rows}")
    print(f"  even_d_surface_rows={profile.even_d_surface_rows}")
    print(f"  distribution_rows={profile.distribution_rows}")
    print(f"  prime_to_6_blocked_rows={profile.prime_to_6_blocked_rows}")
    print(f"  cohomology_output_rows={profile.cohomology_output_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  hypothetical_closing_rows={profile.hypothetical_closing_rows}")
    print(
        "  all_rows_have_missing_clause="
        f"{int(profile.all_rows_have_missing_clause)}"
    )
    print("interpretation")
    print("  sprang_even_d_surface_remains_live=1")
    print("  ordinary_thetaD2_import_is_rejected=1")
    print("  available_sprang_clauses_do_not_emit_exact_p25_product=1")
    print(
        "ksy_y_sprang_even_d_specialization_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Sprang even-D specialization contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
