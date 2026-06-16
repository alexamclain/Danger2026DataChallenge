#!/usr/bin/env python3
"""External exact-product bridge scout for the p25 KSY-y moonshot.

The primary Sprang/KSY source pass left one missing object: an exact theorem
bridging Kronecker/Siegel distribution vocabulary to the p25 finite product.
This gate records the first narrow external scout so later work does not treat
nearby distribution language as a product certificate.
"""

from __future__ import annotations

from dataclasses import dataclass


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class ExternalBridgeRow:
    name: str
    source_url: str
    source_handle: str
    verification_status: str
    inspected_evidence: str
    positive_payload: str
    verdict: str
    first_missing_clause: str
    recommendation: str
    direct_closer: bool
    row_ok: bool


@dataclass(frozen=True)
class ExternalBridgeScoutProfile:
    target_product: str
    rows: tuple[ExternalBridgeRow, ...]
    source_handle_rows: int
    verified_theorem_rows: int
    access_blocked_candidate_rows: int
    direct_closing_rows: int
    continue_rows: int
    kill_as_direct_closer_rows: int
    all_rows_have_missing_clause: bool
    row_ok: bool


def bridge_rows() -> tuple[ExternalBridgeRow, ...]:
    return (
        ExternalBridgeRow(
            name="koo_shin_2010_siegel_function_distribution_candidate",
            source_url="https://link.springer.com/article/10.1007/s00209-008-0456-9",
            source_handle=(
                "Koo-Shin, On some arithmetic properties of Siegel functions, "
                "Math. Z. 264 (2010), 137-177"
            ),
            verification_status="source_handle_verified_not_theorem_verified",
            inspected_evidence=(
                "Springer primary page verifies the article and abstract; ASARC "
                "PDF/search snippets indicate a Theorem 3.1 and Siegel-function "
                "distribution relation, but local shell access to the KAIST PDF "
                "failed and Springer returned HTML rather than PDF"
            ),
            positive_payload=(
                "promising exact source family for products of Siegel functions, "
                "integrality criteria, generators, and possibly a distribution "
                "relation"
            ),
            verdict="candidate_needs_pdf_or_ocr_before_theorem_use",
            first_missing_clause=(
                "full theorem text plus a map to exact p25 row-labeled atoms, "
                "mixed C_3 x C_169 graph, equal weights, and orientation"
            ),
            recommendation="continue_with_pdf_or_ocr_then_exact_product_intake",
            direct_closer=False,
            row_ok=True,
        ),
        ExternalBridgeRow(
            name="bannai_kobayashi_kronecker_theta_distribution",
            source_url="https://arxiv.org/abs/math/0610163",
            source_handle=(
                "Bannai-Kobayashi, Algebraic theta functions and the p-adic "
                "interpolation of Eisenstein-Kronecker numbers"
            ),
            verification_status="verified_primary_tex",
            inspected_evidence=(
                "/tmp/p25_lit_scout/bannai_kobayashi_0610163/"
                "EKnumber-v3.0-2007.12.11.tex:1070-1182"
            ),
            positive_payload=(
                "exact Kronecker theta distribution relation over ideal-torsion "
                "sums; this is the ancestor of the Sprang distribution machinery"
            ),
            verdict="verified_additive_theta_distribution_not_product_bridge",
            first_missing_clause=(
                "finite multiplicative normalized-y/Siegel product selecting the "
                "p25 K-traced anti-invariant atoms"
            ),
            recommendation="kill_as_direct_closer_keep_as_sprang_ancestor",
            direct_closer=False,
            row_ok=True,
        ),
        ExternalBridgeRow(
            name="scholl_kato_siegel_multiplicative_distribution_control",
            source_url="https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            source_handle="Scholl, An introduction to Kato's Euler systems",
            verification_status="verified_primary_pdf_text",
            inspected_evidence=(
                "/tmp/p25_lit_scout/scholl_kato/scholl_euler.txt:377-600"
            ),
            positive_payload=(
                "multiplicative Kato-Siegel norm/distribution relation for "
                "canonical functions theta_D"
            ),
            verdict="verified_multiplicative_distribution_but_D2_ineligible",
            first_missing_clause=(
                "the theorem assumes (6,D)=1 and Robert subgroup order prime to 6; "
                "p25 needs the even D=2 theta2/normalized-y product"
            ),
            recommendation="kill_direct_D2_import_keep_as_odd_D_control",
            direct_closer=False,
            row_ok=True,
        ),
    )


def profile_external_exact_product_bridge_scout() -> ExternalBridgeScoutProfile:
    rows = bridge_rows()
    source_handle_rows = len(rows)
    verified_theorem_rows = sum(
        row.verification_status.startswith("verified_") for row in rows
    )
    access_blocked_candidate_rows = sum(
        row.verification_status == "source_handle_verified_not_theorem_verified"
        for row in rows
    )
    direct_closing_rows = sum(int(row.direct_closer) for row in rows)
    continue_rows = sum(row.recommendation.startswith("continue") for row in rows)
    kill_as_direct_closer_rows = sum(
        row.recommendation.startswith("kill") for row in rows
    )
    all_rows_have_missing_clause = all(row.first_missing_clause for row in rows)
    expected_verdicts = (
        "candidate_needs_pdf_or_ocr_before_theorem_use",
        "verified_additive_theta_distribution_not_product_bridge",
        "verified_multiplicative_distribution_but_D2_ineligible",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and source_handle_rows == 3
        and verified_theorem_rows == 2
        and access_blocked_candidate_rows == 1
        and direct_closing_rows == 0
        and continue_rows == 1
        and kill_as_direct_closer_rows == 2
        and all_rows_have_missing_clause
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return ExternalBridgeScoutProfile(
        target_product=TARGET_PRODUCT,
        rows=rows,
        source_handle_rows=source_handle_rows,
        verified_theorem_rows=verified_theorem_rows,
        access_blocked_candidate_rows=access_blocked_candidate_rows,
        direct_closing_rows=direct_closing_rows,
        continue_rows=continue_rows,
        kill_as_direct_closer_rows=kill_as_direct_closer_rows,
        all_rows_have_missing_clause=all_rows_have_missing_clause,
        row_ok=row_ok,
    )


def print_row(row: ExternalBridgeRow) -> None:
    print(
        "  "
        f"{row.name}: status={row.verification_status} verdict={row.verdict} "
        f"closes={int(row.direct_closer)} recommendation={row.recommendation}"
    )


def main() -> int:
    profile = profile_external_exact_product_bridge_scout()
    print("p25 KSY-y external exact-product bridge scout gate")
    print(f"target_product={profile.target_product}")
    print("bridge_rows")
    for row in profile.rows:
        print_row(row)
    print("counts")
    print(f"  source_handle_rows={profile.source_handle_rows}")
    print(f"  verified_theorem_rows={profile.verified_theorem_rows}")
    print(f"  access_blocked_candidate_rows={profile.access_blocked_candidate_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  continue_rows={profile.continue_rows}")
    print(f"  kill_as_direct_closer_rows={profile.kill_as_direct_closer_rows}")
    print(f"  all_rows_have_missing_clause={int(profile.all_rows_have_missing_clause)}")
    print("interpretation")
    print("  bannai_kobayashi_is_sprang_ancestor_not_exact_product=1")
    print("  scholl_kato_siegel_is_multiplicative_but_D2_ineligible=1")
    print("  koo_shin_2010_is_highest_value_external_pdf_ocr_candidate=1")
    print(f"ksy_y_external_exact_product_bridge_scout_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("external exact-product bridge scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
